"""Offline contract tests; only the external HTTP boundary is replaced."""

import copy
import json
import unittest
from datetime import datetime, timezone
from unittest.mock import patch

import requests

from core.chess_client import (
    ChessDotComClient,
    ChessDotComError,
    ChessDotComTimeoutError,
    RateLimitError,
    UserNotFoundError,
)


def response(payload, status=200, headers=None):
    result = requests.Response()
    result.status_code = status
    result.url = "https://api.chess.com/pub/player/alice/games/2026/01"
    result._content = json.dumps(payload).encode()
    result.headers.update(headers or {})
    return result


def game(number=1, end_time=1704067200, white_result="win", black_result="resigned"):
    return {
        "url": f"https://www.chess.com/game/live/{number}",
        "pgn": '[Result "1-0"]\n\n1. e4 e5 1-0',
        "end_time": end_time,
        "rated": True,
        "time_control": "300",
        "time_class": "blitz",
        "rules": "chess",
        "white": {"username": "Alice", "rating": 1500, "result": white_result},
        "black": {"username": "Bob", "rating": 1550, "result": black_result},
    }


class FrozenDateTime(datetime):
    @classmethod
    def now(cls, tz=None):
        return datetime(2026, 1, 15, tzinfo=timezone.utc)


@patch("core.chess_client.requests.get")
class PlayerRatingsTests(unittest.TestCase):
    def test_fetches_current_ratings_from_stats_and_normalizes_username(self, get):
        get.return_value = response({
            "chess_rapid": {
                "last": {"rating": 1512, "date": 1792280000, "rd": 54},
                "best": {"rating": 1600, "date": 1790000000, "game": "https://www.chess.com/game/live/1"},
                "record": {"win": 12, "loss": 8, "draw": 1},
            },
            "chess_blitz": {"last": {"rating": 1422, "date": 1792270000, "rd": 38}},
            "chess_bullet": {"last": {"rating": 4110, "date": 1792260000, "rd": 40}},
            "chess_daily": {"last": {"rating": 1630, "date": 1792250000, "rd": 65}},
            "chess960_daily": {"last": {"rating": 900, "date": 1792240000}},
            "tactics": {"highest": {"rating": 2100, "date": 1792230000}},
        })

        ratings = ChessDotComClient(timeout=8).get_player_ratings(" ALICE ")

        self.assertEqual(ratings, {
            "rapid": {"rating": 1512, "last_played": 1792280000},
            "blitz": {"rating": 1422, "last_played": 1792270000},
            "bullet": {"rating": 4110, "last_played": 1792260000},
            "daily": {"rating": 1630, "last_played": 1792250000},
        })
        get.assert_called_once_with(
            "https://api.chess.com/pub/player/alice/stats",
            headers={"User-Agent": "ChessCoachBot/1.0 (contact: user@example.com)"},
            timeout=8,
        )

    def test_omits_unrated_categories_without_using_best_or_record_as_a_rating(self, get):
        for payload in (
            {},
            {"chess_rapid": {}},
            {"chess_rapid": {"last": {}}},
            {"chess_rapid": {"last": {"rating": None}}},
            {"chess_rapid": {"best": {"rating": 1700}, "record": {"win": 10}}},
        ):
            with self.subTest(payload=payload):
                get.return_value = response(payload)
                self.assertEqual(ChessDotComClient().get_player_ratings("alice"), {})

    def test_preserves_rating_without_inventing_a_missing_last_played_time(self, get):
        for last in ({"rating": 1200}, {"rating": 1200, "date": None}):
            with self.subTest(last=last):
                get.return_value = response({"chess_rapid": {"last": last}})
                self.assertEqual(ChessDotComClient().get_player_ratings("alice"), {
                    "rapid": {"rating": 1200, "last_played": None},
                })

    def test_rejects_malformed_rating_data_instead_of_reporting_an_unrated_player(self, get):
        malformed = [None, [], "rated", {"last": None}, {"last": []}, {"last": "rated"}]
        malformed.extend({"last": {"rating": value}} for value in (True, False, 0, -1, 1500.5, "1500"))
        malformed.extend({"last": {"rating": 1500, "date": value}} for value in (True, False, -1, 1.5, "1792280000"))
        for category in malformed:
            with self.subTest(category=category):
                get.return_value = response({"chess_rapid": category})
                with self.assertRaises(ChessDotComError):
                    ChessDotComClient().get_player_ratings("alice")

    def test_invalid_username_never_reaches_the_network(self, get):
        for username in (None, 123, True, "", " "):
            with self.subTest(username=username), self.assertRaises(ValueError):
                ChessDotComClient().get_player_ratings(username)
        get.assert_not_called()

    def test_username_is_escaped_as_a_single_path_segment(self, get):
        get.return_value = response({})
        self.assertEqual(ChessDotComClient().get_player_ratings(" A/B "), {})
        self.assertEqual(get.call_args.args[0], "https://api.chess.com/pub/player/a%2Fb/stats")

    def test_stats_requests_preserve_shared_error_mapping(self, get):
        invalid_json = response({})
        invalid_json._content = b"not-json"
        cases = (
            (response({}, status=404), UserNotFoundError),
            (response({}, status=429, headers={"Retry-After": "60"}), RateLimitError),
            (response({}, status=503), ChessDotComError),
            (invalid_json, ChessDotComError),
            (response([]), ChessDotComError),
            (requests.Timeout("read timed out"), ChessDotComTimeoutError),
            (requests.ConnectionError("offline"), ChessDotComError),
        )
        for result, expected_error in cases:
            with self.subTest(result=result, expected_error=expected_error):
                get.reset_mock()
                get.side_effect = result if isinstance(result, Exception) else None
                get.return_value = result
                with self.assertRaises(expected_error) as caught:
                    ChessDotComClient().get_player_ratings("alice")
                self.assertEqual(get.call_count, 1)
                if expected_error is RateLimitError:
                    self.assertEqual(caught.exception.retry_after, "60")


@patch("core.chess_client.requests.get")
class MonthlyGamesTests(unittest.TestCase):
    def test_preserves_only_valid_published_accuracy_for_the_requested_player(self, get):
        for value in (86.4, 0, 100, None, -1, 101, True, "90", float("nan")):
            with self.subTest(value=value):
                raw = game()
                raw["accuracies"] = {"white": 99.1, "black": value}
                get.return_value = response({"games": [raw]})
                actual = ChessDotComClient().get_monthly_games("bob", 2024, 1)[0]
                if type(value) in (int, float) and 0 <= value <= 100:
                    self.assertEqual(actual["accuracy"], value)
                else:
                    self.assertNotIn("accuracy", actual)

    def test_monthly_request_and_clean_game_schema(self, get):
        get.return_value = response({"games": [game()]})
        games = ChessDotComClient().get_monthly_games(" ALICE ", 2024, 1)
        self.assertEqual(games, [{
            "game_url": "https://www.chess.com/game/live/1",
            "played_at": "2024-01-01T00:00:00+00:00",
            "white_username": "Alice",
            "white_rating": 1500,
            "black_username": "Bob",
            "black_rating": 1550,
            "user_color": "white",
            "result": "win",
            "pgn": '[Result "1-0"]\n\n1. e4 e5 1-0',
        }])
        get.assert_called_once_with(
            "https://api.chess.com/pub/player/alice/games/2024/01",
            headers={"User-Agent": "ChessCoachBot/1.0 (contact: user@example.com)"},
            timeout=15.0,
        )

    def test_results_are_from_the_requested_players_perspective(self, get):
        cases = [
            ("win", "resigned", "alice", "white", "win"),
            ("win", "checkmated", "BOB", "black", "loss"),
            ("timeout", "win", "bob", "black", "win"),
        ]
        for draw in ("agreed", "repetition", "stalemate", "insufficient", "50move", "timevsinsufficient"):
            cases.append((draw, draw, "bob", "black", "draw"))
        for loss in ("checkmated", "timeout", "resigned", "lose", "abandoned", "kingofthehill", "threecheck", "bughousepartnerlose"):
            cases.append((loss, "win", "alice", "white", "loss"))
        for white, black, username, color, expected in cases:
            with self.subTest(white=white, black=black, username=username):
                get.return_value = response({"games": [game(white_result=white, black_result=black)]})
                actual = ChessDotComClient().get_monthly_games(username, 2024, 1)[0]
                self.assertEqual((actual["user_color"], actual["result"]), (color, expected))

    def test_omits_unfinished_or_unusable_games_and_sorts_newest_first(self, get):
        unfinished = game(3)
        unfinished.pop("end_time")
        unknown_result = game(4, white_result="inprogress")
        missing_pgn = game(5)
        missing_pgn.pop("pgn")
        invalid_time = game(6, end_time="not-a-timestamp")
        wrong_player = copy.deepcopy(game(7))
        wrong_player["white"]["username"] = "Carol"
        get.return_value = response({"games": [
            game(1), unfinished, unknown_result, missing_pgn,
            invalid_time, wrong_player, None, game(2, end_time=1704067260),
        ]})
        games = ChessDotComClient().get_monthly_games("alice", 2024, 1)
        self.assertEqual([item["game_url"] for item in games], [
            "https://www.chess.com/game/live/2",
            "https://www.chess.com/game/live/1",
        ])

    def test_missing_rating_is_preserved_as_none(self, get):
        raw = game()
        raw["white"].pop("rating")
        get.return_value = response({"games": [raw]})
        self.assertIsNone(ChessDotComClient().get_monthly_games("alice", 2024, 1)[0]["white_rating"])

    def test_invalid_username_or_month_never_reaches_the_network(self, get):
        for username, year, month in [(" ", 2024, 1), ("alice", 2024, 0), ("alice", 2024, 13), ("alice", 0, 1)]:
            with self.subTest(username=username, year=year, month=month):
                with self.assertRaises(ValueError):
                    ChessDotComClient().get_monthly_games(username, year, month)
        get.assert_not_called()


@patch("core.chess_client.datetime", FrozenDateTime)
@patch("core.chess_client.requests.get")
class RecentGamesTests(unittest.TestCase):
    def test_current_month_satisfies_count_without_fetching_history(self, get):
        get.return_value = response({"games": [game(1), game(2, end_time=1704067260)]})
        games = ChessDotComClient().get_recent_games("alice", count=1)
        self.assertEqual(games[0]["game_url"], "https://www.chess.com/game/live/2")
        self.assertEqual(get.call_count, 1)
        self.assertEqual(get.call_args.args[0], "https://api.chess.com/pub/player/alice/games/2026/01")

    def test_walks_back_across_year_boundary_and_skips_empty_month_gaps(self, get):
        get.side_effect = [
            response({"games": [game(3, end_time=1767225660)]}),
            response({"archives": [
                "https://api.chess.com/pub/player/alice/games/2025/09",
                "https://api.chess.com/pub/player/alice/games/2026/01",
                "https://api.chess.com/pub/player/alice/games/2025/12",
                "https://api.chess.com/pub/player/alice/games/2025/12",
                "https://api.chess.com/pub/player/alice/games/2026/02",
            ]}),
            response({"games": [game(2, end_time=1764547260)]}),
            response({"games": [game(1, end_time=1756684860)]}),
        ]
        games = ChessDotComClient().get_recent_games("alice", count=3)
        self.assertEqual([item["game_url"] for item in games], [
            "https://www.chess.com/game/live/3",
            "https://www.chess.com/game/live/2",
            "https://www.chess.com/game/live/1",
        ])
        self.assertEqual([call.args[0].rsplit("/", 2)[-2:] for call in get.call_args_list], [
            ["2026", "01"], ["games", "archives"], ["2025", "12"], ["2025", "09"],
        ])

    def test_exhausted_history_returns_available_games(self, get):
        get.side_effect = [response({"games": [game()]}), response({"archives": []})]
        self.assertEqual(len(ChessDotComClient().get_recent_games("alice", 10)), 1)
        self.assertEqual(get.call_count, 2)

    def test_empty_history_returns_empty_list(self, get):
        get.side_effect = [response({"games": []}), response({"archives": []})]
        self.assertEqual(ChessDotComClient().get_recent_games("alice"), [])

    def test_unavailable_current_month_still_checks_older_archives(self, get):
        get.side_effect = [
            response({}, status=404),
            response({"archives": ["https://api.chess.com/pub/player/alice/games/2025/12"]}),
            response({"games": [game(1, end_time=1764547260)]}),
        ]
        games = ChessDotComClient().get_recent_games("alice", 1)
        self.assertEqual(games[0]["game_url"], "https://www.chess.com/game/live/1")

    def test_zero_or_invalid_count_does_not_fetch(self, get):
        self.assertEqual(ChessDotComClient().get_recent_games("alice", 0), [])
        for count in (-1, 1.5, True):
            with self.subTest(count=count), self.assertRaises(ValueError):
                ChessDotComClient().get_recent_games("alice", count)
        get.assert_not_called()

    def test_history_request_failure_is_not_silently_returned_as_partial_success(self, get):
        get.side_effect = [response({"games": [game()]}), response({}, status=429)]
        with self.assertRaises(RateLimitError):
            ChessDotComClient().get_recent_games("alice", 3)

    def test_malformed_archive_list_is_reported(self, get):
        for archives in (None, ["not-an-archive"]):
            get.side_effect = [response({"games": []}), response({"archives": archives})]
            with self.subTest(archives=archives), self.assertRaises(ChessDotComError):
                ChessDotComClient().get_recent_games("alice")


@patch("core.chess_client.requests.get")
class RequestErrorTests(unittest.TestCase):
    def test_404_reports_user_not_found(self, get):
        get.return_value = response({}, status=404)
        with self.assertRaisesRegex(UserNotFoundError, "alice"):
            ChessDotComClient().get_monthly_games("alice", 2024, 1)

    def test_429_preserves_retry_after_without_retrying(self, get):
        get.return_value = response({}, status=429, headers={"Retry-After": "60"})
        with self.assertRaises(RateLimitError) as caught:
            ChessDotComClient().get_monthly_games("alice", 2024, 1)
        self.assertEqual(caught.exception.retry_after, "60")
        self.assertEqual(get.call_count, 1)

    def test_timeouts_produce_a_client_error(self, get):
        get.side_effect = requests.Timeout("read timed out")
        with self.assertRaises(ChessDotComTimeoutError):
            ChessDotComClient().get_monthly_games("alice", 2024, 1)

    def test_other_http_or_connection_errors_produce_a_client_error(self, get):
        get.return_value = response({}, status=503)
        with self.assertRaisesRegex(ChessDotComError, "503"):
            ChessDotComClient().get_monthly_games("alice", 2024, 1)
        get.side_effect = requests.ConnectionError("offline")
        with self.assertRaises(ChessDotComError):
            ChessDotComClient().get_monthly_games("alice", 2024, 1)

    def test_invalid_json_or_payload_shape_produces_a_client_error(self, get):
        invalid_json = response({})
        invalid_json._content = b"not-json"
        for item in (invalid_json, response([]), response({"games": None}), response({})):
            get.return_value = item
            with self.subTest(body=item.content), self.assertRaises(ChessDotComError):
                ChessDotComClient().get_monthly_games("alice", 2024, 1)


if __name__ == "__main__":
    unittest.main()
