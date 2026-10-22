"""Fetch completed games and current ratings from Chess.com's public API.

API reference: https://www.chess.com/news/view/published-data-api
"""

import re
import sys
from datetime import datetime, timezone
from urllib.parse import quote

import requests


class ChessDotComError(RuntimeError):
    """A Chess.com request failed or returned an unexpected response."""


class UserNotFoundError(ChessDotComError):
    """The requested player or archive could not be found (HTTP 404)."""


class RateLimitError(ChessDotComError):
    """Chess.com rate-limited the request; retry later rather than in a loop."""

    def __init__(self, retry_after: str | None = None):
        self.retry_after = retry_after
        message = "Chess.com is rate limiting requests. Please try again later."
        if retry_after:
            message += f" Retry-After: {retry_after}."
        super().__init__(message)


class ChessDotComTimeoutError(ChessDotComError):
    """The connection or response exceeded the configured request timeout."""


class ChessDotComClient:
    """Retrieve games in newest-first order using serial, bounded requests.

    ``played_at`` is the game-end time as an ISO 8601 string in UTC.
    ``result`` is ``win``, ``loss``, or ``draw`` from the requested user's
    perspective; ``user_color`` is ``white`` or ``black``. Missing ratings
    are represented as None. PGN text is preserved without modification.
    """

    BASE_URL = "https://api.chess.com/pub"
    USER_AGENT = "ChessCoachBot/1.0 (contact: user@example.com)"
    DRAW_RESULTS = frozenset({
        "agreed", "repetition", "stalemate", "insufficient", "50move",
        "timevsinsufficient",
    })
    LOSS_RESULTS = frozenset({
        "checkmated", "timeout", "resigned", "lose", "abandoned",
        "kingofthehill", "threecheck", "bughousepartnerlose",
    })

    def __init__(self, timeout: float = 15.0):
        if timeout <= 0:
            raise ValueError("timeout must be greater than zero")
        self.timeout = timeout

    def get_player_ratings(self, username: str) -> dict[str, dict[str, int | None]]:
        """Return published current ratings for rapid, blitz, bullet, and daily.

        Each rated category contains ``rating`` and ``last_played`` (the API's
        Unix timestamp, or None when absent). Unrated categories are omitted;
        best ratings and game records are never substituted for current ratings.
        Malformed published values raise ChessDotComError.
        """
        username = self._validate_username(username)
        url = f"{self.BASE_URL}/player/{quote(username, safe='')}/stats"
        payload = self._get_json(url, username)
        ratings = {}
        for category in ("rapid", "blitz", "bullet", "daily"):
            key = f"chess_{category}"
            if key not in payload:
                continue
            stats = payload[key]
            if not isinstance(stats, dict):
                raise ChessDotComError(f"Chess.com returned invalid {category} statistics.")
            if "last" not in stats:
                continue
            last = stats["last"]
            if not isinstance(last, dict):
                raise ChessDotComError(f"Chess.com returned an invalid current {category} rating.")
            rating = last.get("rating")
            if rating is None:
                continue
            if type(rating) is not int or rating <= 0:
                raise ChessDotComError(f"Chess.com returned an invalid current {category} rating.")
            last_played = last.get("date")
            if last_played is not None and (type(last_played) is not int or last_played < 0):
                raise ChessDotComError(f"Chess.com returned an invalid {category} rating date.")
            ratings[category] = {"rating": rating, "last_played": last_played}
        return ratings

    def get_monthly_games(self, username: str, year: int, month: int) -> list[dict]:
        """Fetch and normalize completed games from a single monthly archive.

        Incomplete or unusable records (including missing PGN) are omitted.
        Raises ChessDotComError for request failures, rather than returning an
        empty list that could be mistaken for a month without games.
        """
        username = self._validate_username(username)
        datetime(year, month, 1)  # Validate the calendar date before requesting.
        url = f"{self.BASE_URL}/player/{quote(username, safe='')}/games/{year:04d}/{month:02d}"
        payload = self._get_json(url, username)
        raw_games = payload.get("games")
        if not isinstance(raw_games, list):
            raise ChessDotComError("Chess.com returned an invalid games list.")

        games = []
        for raw_game in raw_games:
            game = self._normalize_game(raw_game, username)
            if game is not None:
                games.append(game)
        return sorted(games, key=lambda game: game["played_at"], reverse=True)

    def get_recent_games(self, username: str, count: int = 10) -> list[dict]:
        """Start with the current UTC month, then visit older available months.

        The archive index lets us skip inactive months and stop at the end of
        the player's history. Returns fewer than count games if necessary.
        Any request failure raises ChessDotComError, even after partial results.
        """
        username = self._validate_username(username)
        if not isinstance(count, int) or isinstance(count, bool) or count < 0:
            raise ValueError("count must be a non-negative integer")
        if count == 0:
            return []

        now = datetime.now(timezone.utc)
        current_month = (now.year, now.month)
        try:
            games = self.get_monthly_games(username, *current_month)
        except UserNotFoundError:
            # A monthly 404 can mean no archive; the index below distinguishes
            # that case from a missing player, whose index will also return 404.
            games = []
        if len(games) >= count:
            return games[:count]

        url = f"{self.BASE_URL}/player/{quote(username, safe='')}/games/archives"
        archives = self._get_json(url, username).get("archives")
        if not isinstance(archives, list):
            raise ChessDotComError("Chess.com returned an invalid archive list.")

        # Parse only dates; never follow an arbitrary URL from the response.
        pattern = re.compile(
            re.escape(self.BASE_URL) + r"/player/[^/]+/games/(\d{4})/(\d{2})/?"
        )
        months = set()
        for archive in archives:
            match = pattern.fullmatch(archive) if isinstance(archive, str) else None
            if match is None:
                raise ChessDotComError("Chess.com returned an invalid archive URL.")
            year, month = map(int, match.groups())
            try:
                datetime(year, month, 1)
            except ValueError as exc:
                raise ChessDotComError("Chess.com returned an invalid archive date.") from exc
            if (year, month) < current_month:
                months.add((year, month))

        for year, month in sorted(months, reverse=True):
            games.extend(self.get_monthly_games(username, year, month))
            if len(games) >= count:
                break
        return games[:count]

    def _get_json(self, url: str, username: str) -> dict:
        try:
            response = requests.get(
                url,
                headers={"User-Agent": self.USER_AGENT},
                timeout=self.timeout,
            )
            if response.status_code == 404:
                raise UserNotFoundError(
                    f"Chess.com player '{username}' was not found, or the requested archive is unavailable."
                )
            if response.status_code == 429:
                raise RateLimitError(response.headers.get("Retry-After"))
            response.raise_for_status()
        except requests.Timeout as exc:
            raise ChessDotComTimeoutError(
                f"Chess.com did not respond within the {self.timeout:g}-second request timeout. Please try again."
            ) from exc
        except requests.HTTPError as exc:
            raise ChessDotComError(
                f"Chess.com returned HTTP {response.status_code}. Please try again later."
            ) from exc
        except requests.RequestException as exc:
            raise ChessDotComError(
                "Could not connect to Chess.com. Check your connection and try again."
            ) from exc

        try:
            payload = response.json()
        except ValueError as exc:
            raise ChessDotComError("Chess.com returned invalid JSON.") from exc
        if not isinstance(payload, dict):
            raise ChessDotComError("Chess.com returned an unexpected response format.")
        return payload

    @staticmethod
    def _validate_username(username: str) -> str:
        if not isinstance(username, str) or not username.strip():
            raise ValueError("username must be a non-empty string")
        return username.strip().lower()

    def _normalize_game(self, game: dict, username: str) -> dict | None:
        if not isinstance(game, dict):
            return None
        try:
            white, black = game["white"], game["black"]
            white_username, black_username = white["username"], black["username"]
            if not isinstance(white_username, str) or not isinstance(black_username, str):
                return None
            if white_username.lower() == username:
                color, player = "white", white
            elif black_username.lower() == username:
                color, player = "black", black
            else:
                return None

            code = player.get("result")
            if code == "win":
                result = "win"
            elif code in self.DRAW_RESULTS:
                result = "draw"
            elif code in self.LOSS_RESULTS:
                result = "loss"
            else:
                return None

            if not isinstance(game["pgn"], str) or not game["pgn"].strip():
                return None
            if not isinstance(game["url"], str) or not game["url"]:
                return None
            played_at = datetime.fromtimestamp(game["end_time"], timezone.utc).isoformat()
            normalized = {
                "game_url": game["url"],
                "played_at": played_at,
                "white_username": white_username,
                "white_rating": white.get("rating"),
                "black_username": black_username,
                "black_rating": black.get("rating"),
                "user_color": color,
                "result": result,
                "pgn": game["pgn"],
            }
            accuracies = game.get("accuracies")
            accuracy = accuracies.get(color) if isinstance(accuracies, dict) else None
            if type(accuracy) in (int, float) and 0 <= accuracy <= 100:
                normalized["accuracy"] = float(accuracy)
            return normalized
        except (KeyError, TypeError, ValueError, OverflowError, OSError):
            return None


if __name__ == "__main__":
    try:
        recent_games = ChessDotComClient().get_recent_games("magnuscarlsen", count=3)
    except ChessDotComError as error:
        print(f"Unable to fetch games: {error}", file=sys.stderr)
        sys.exit(1)

    if not recent_games:
        print("No completed games found for magnuscarlsen.")
    for index, game in enumerate(recent_games, start=1):
        print(
            f"{index}. {game['played_at']} | "
            f"{game['white_username']} ({game['white_rating']}) vs "
            f"{game['black_username']} ({game['black_rating']}) | "
            f"magnuscarlsen: {game['user_color']}, {game['result']}\n"
            f"   {game['game_url']}"
        )
