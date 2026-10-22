"""Bounded, synchronous refreshes of per-player Chess.com rating snapshots."""

import math
import time
from datetime import timezone
from email.utils import parsedate_to_datetime

from core.chess_client import ChessDotComClient, ChessDotComError, RateLimitError


RATING_INTERVAL = 60
_CATEGORIES = ("rapid", "blitz", "bullet", "daily")


def _empty_snapshot() -> dict:
    return {
        "ratings": {},
        "updated_at": None,
        "last_attempt": None,
        "next_check": 0.0,
        "blocked_until": 0.0,
        "error": None,
    }


def _rate_limit_delay(retry_after: str | None) -> float:
    """Translate Retry-After seconds or an HTTP date into a bounded delay."""
    if not retry_after:
        return 300
    try:
        delay = float(retry_after)
    except (TypeError, ValueError):
        try:
            deadline = parsedate_to_datetime(retry_after)
            if deadline.tzinfo is None:
                deadline = deadline.replace(tzinfo=timezone.utc)
            delay = deadline.timestamp() - time.time()
        except (AttributeError, TypeError, ValueError, OverflowError, OSError):
            return 300
    if not math.isfinite(delay):
        return 300
    return max(RATING_INTERVAL, delay)


def refresh_rating_snapshot(
    username: str,
    snapshots: dict,
    *,
    force: bool = False,
    now: float | None = None,
) -> dict:
    """Refresh and cache one player's ratings, retaining the last good result.

    All snapshot times are monotonic clock values. Ordinary refreshes wait at
    least 60 seconds; explicit refreshes can bypass that interval but always
    respect Chess.com's rate-limit deadline. No background work is started.
    """
    username = username.strip().lower()
    if not username:
        return _empty_snapshot()
    use_clock = now is None
    if use_clock:
        now = time.monotonic()

    previous = snapshots.get(username, _empty_snapshot())
    if now < previous["blocked_until"]:
        return previous
    if not force and now < previous["next_check"]:
        return previous

    error = None
    try:
        ratings = ChessDotComClient(timeout=5).get_player_ratings(username)
    except (ChessDotComError, ValueError) as exc:
        error = exc
    completed_at = time.monotonic() if use_clock else now
    snapshot = {
        **previous,
        "last_attempt": now,
        "next_check": completed_at + RATING_INTERVAL,
        "blocked_until": 0.0,
    }
    if error is None:
        snapshot.update(ratings=ratings, updated_at=completed_at, error=None)
    else:
        snapshot["error"] = str(error)
        if isinstance(error, RateLimitError):
            deadline = completed_at + _rate_limit_delay(error.retry_after)
            snapshot.update(next_check=deadline, blocked_until=deadline)
    snapshots[username] = snapshot
    return snapshot


def choose_rating_category(ratings: dict, preferred: str | None = None) -> str | None:
    """Prefer an explicit available category, then the most recently played."""
    if preferred in ratings:
        return preferred
    available = [category for category in _CATEGORIES if category in ratings]
    if not available:
        return None

    def last_played(category: str) -> int:
        timestamp = ratings[category].get("last_played")
        return timestamp if type(timestamp) is int and timestamp >= 0 else -1

    return max(available, key=last_played)
