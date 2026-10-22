"""Session snapshot behavior with real client validation at the HTTP boundary."""

import json
import unittest
from unittest.mock import patch

import requests

from core.ratings import choose_rating_category, refresh_rating_snapshot


def stats_response(rating=1500, *, status=200, headers=None, empty=False):
    result = requests.Response()
    result.status_code = status
    result.url = "https://api.chess.com/pub/player/alice/stats"
    payload = {} if empty else {
        "chess_rapid": {"last": {"rating": rating, "date": 1792280000, "rd": 54}},
    }
    result._content = json.dumps(payload).encode()
    result.headers.update(headers or {})
    return result


@patch("core.chess_client.requests.get")
class RatingSnapshotTests(unittest.TestCase):
    def test_initial_request_is_cached_until_the_next_check_and_then_updates(self, get):
        get.side_effect = [stats_response(1500), stats_response(1517)]
        snapshots = {}

        first = refresh_rating_snapshot(" ALICE ", snapshots, now=10)
        self.assertEqual(first, {
            "ratings": {"rapid": {"rating": 1500, "last_played": 1792280000}},
            "updated_at": 10,
            "last_attempt": 10,
            "next_check": 70,
            "blocked_until": 0,
            "error": None,
        })
        self.assertEqual(refresh_rating_snapshot("alice", snapshots, now=69.9), first)
        self.assertEqual(get.call_count, 1)
        updated = refresh_rating_snapshot("alice", snapshots, now=70)
        self.assertEqual(updated["ratings"]["rapid"]["rating"], 1517)
        self.assertEqual(updated["updated_at"], 70)
        self.assertEqual(updated["next_check"], 130)
        self.assertEqual(set(snapshots), {"alice"})
        self.assertEqual(get.call_count, 2)
        self.assertEqual(get.call_args.kwargs["timeout"], 5)

    def test_manual_force_refreshes_before_normal_ttl(self, get):
        get.side_effect = [stats_response(1500), stats_response(1520)]
        snapshots = {}
        refresh_rating_snapshot("alice", snapshots, now=10)
        updated = refresh_rating_snapshot("alice", snapshots, force=True, now=11)
        self.assertEqual(updated["ratings"]["rapid"]["rating"], 1520)
        self.assertEqual(updated["updated_at"], 11)
        self.assertEqual(get.call_count, 2)

    def test_failure_preserves_last_good_data_and_timestamp_until_retry_succeeds(self, get):
        get.side_effect = [stats_response(1500), stats_response(status=503), stats_response(1530)]
        snapshots = {}
        first = refresh_rating_snapshot("alice", snapshots, now=10)
        failed = refresh_rating_snapshot("alice", snapshots, now=70)
        self.assertEqual(failed["ratings"], first["ratings"])
        self.assertEqual(failed["updated_at"], 10)
        self.assertEqual(failed["last_attempt"], 70)
        self.assertEqual(failed["next_check"], 130)
        self.assertIn("503", failed["error"])
        self.assertEqual(refresh_rating_snapshot("alice", snapshots, now=129), failed)
        self.assertEqual(get.call_count, 2)
        recovered = refresh_rating_snapshot("alice", snapshots, now=130)
        self.assertEqual(recovered["ratings"]["rapid"]["rating"], 1530)
        self.assertEqual(recovered["updated_at"], 130)
        self.assertIsNone(recovered["error"])

    def test_failed_initial_request_has_no_invented_rating_or_success_time(self, get):
        get.side_effect = requests.Timeout("offline")
        failed = refresh_rating_snapshot("alice", {}, now=0)
        self.assertEqual(failed["ratings"], {})
        self.assertIsNone(failed["updated_at"])
        self.assertEqual(failed["last_attempt"], 0)
        self.assertEqual(failed["next_check"], 60)
        self.assertTrue(failed["error"])

    def test_value_error_is_recorded_without_losing_the_last_success(self, get):
        get.return_value = stats_response(1500)
        snapshots = {}
        first = refresh_rating_snapshot("alice", snapshots, now=10)
        with patch("core.ratings.ChessDotComClient.get_player_ratings", side_effect=ValueError("bad stats")):
            failed = refresh_rating_snapshot("alice", snapshots, now=70)
        self.assertEqual(failed["ratings"], first["ratings"])
        self.assertEqual(failed["updated_at"], 10)
        self.assertEqual(failed["error"], "bad stats")

    def test_player_snapshots_do_not_share_ratings_or_request_timing(self, get):
        get.side_effect = [stats_response(1500), stats_response(900)]
        snapshots = {}
        alice = refresh_rating_snapshot("alice", snapshots, now=10)
        bob = refresh_rating_snapshot(" BOB ", snapshots, now=11)
        self.assertEqual(alice["ratings"]["rapid"]["rating"], 1500)
        self.assertEqual(bob["ratings"]["rapid"]["rating"], 900)
        self.assertEqual(set(snapshots), {"alice", "bob"})
        self.assertEqual(refresh_rating_snapshot("ALICE", snapshots, now=12), alice)
        self.assertEqual(get.call_count, 2)
        self.assertEqual(get.call_args.args[0], "https://api.chess.com/pub/player/bob/stats")

    def test_blank_username_returns_an_empty_snapshot_without_fetching_or_caching(self, get):
        snapshots = {}
        for username in ("", "  "):
            with self.subTest(username=username):
                empty = refresh_rating_snapshot(username, snapshots, now=10)
                self.assertEqual(empty["ratings"], {})
                self.assertIsNone(empty["updated_at"])
                self.assertIsNone(empty["last_attempt"])
                self.assertIsNone(empty["error"])
        self.assertEqual(snapshots, {})
        get.assert_not_called()

    def test_success_with_no_ratings_clears_previous_ratings_and_error(self, get):
        get.side_effect = [stats_response(1500), stats_response(status=503), stats_response(empty=True)]
        snapshots = {}
        refresh_rating_snapshot("alice", snapshots, now=10)
        refresh_rating_snapshot("alice", snapshots, now=70)
        empty = refresh_rating_snapshot("alice", snapshots, now=130)
        self.assertEqual(empty["ratings"], {})
        self.assertEqual(empty["updated_at"], 130)
        self.assertIsNone(empty["error"])

    def test_unspecified_now_uses_monotonic_clock(self, get):
        get.return_value = stats_response()
        with patch("core.ratings.time.monotonic", return_value=123.5):
            actual = refresh_rating_snapshot("alice", {})
        self.assertEqual(actual["last_attempt"], 123.5)
        self.assertEqual(actual["next_check"], 183.5)

    def test_rate_limit_delay_begins_after_the_response_arrives(self, get):
        get.return_value = stats_response(status=429, headers={"Retry-After": "120"})
        with patch("core.ratings.time.monotonic", side_effect=[10, 15]):
            limited = refresh_rating_snapshot("alice", {})
        self.assertEqual(limited["last_attempt"], 10)
        self.assertEqual(limited["blocked_until"], 135)
        self.assertEqual(limited["next_check"], 135)

    def test_normal_deadlines_and_freshness_use_request_completion_time(self, get):
        for status in (200, 503):
            with self.subTest(status=status):
                get.return_value = stats_response(status=status)
                with patch("core.ratings.time.monotonic", side_effect=[10, 15]):
                    snapshot = refresh_rating_snapshot("alice", {})
                self.assertEqual(snapshot["last_attempt"], 10)
                self.assertEqual(snapshot["next_check"], 75)
                self.assertEqual(snapshot["updated_at"], 15 if status == 200 else None)

    def test_rate_limit_backoff_blocks_forced_refresh_and_preserves_last_success(self, get):
        get.side_effect = [
            stats_response(1500),
            stats_response(status=429, headers={"Retry-After": "120"}),
            stats_response(1510),
        ]
        snapshots = {}
        refresh_rating_snapshot("alice", snapshots, now=10)
        limited = refresh_rating_snapshot("alice", snapshots, now=70)
        self.assertEqual(limited["ratings"]["rapid"]["rating"], 1500)
        self.assertEqual(limited["updated_at"], 10)
        self.assertEqual(limited["blocked_until"], 190)
        self.assertEqual(limited["next_check"], 190)
        self.assertEqual(refresh_rating_snapshot("alice", snapshots, force=True, now=189), limited)
        self.assertEqual(get.call_count, 2)
        recovered = refresh_rating_snapshot("alice", snapshots, force=True, now=190)
        self.assertEqual(recovered["ratings"]["rapid"]["rating"], 1510)
        self.assertEqual(recovered["blocked_until"], 0)
        self.assertIsNone(recovered["error"])

    def test_rate_limit_uses_minimum_or_default_delay_for_numeric_or_invalid_headers(self, get):
        for header, delay in (("1", 60), ("0", 60), ("-1", 60), ("90.5", 90.5), (None, 300), ("invalid", 300), ("nan", 300), ("inf", 300)):
            with self.subTest(header=header):
                get.return_value = stats_response(status=429, headers={"Retry-After": header} if header else {})
                limited = refresh_rating_snapshot("alice", {}, now=10)
                self.assertEqual(limited["next_check"], 10 + delay)
                self.assertEqual(limited["blocked_until"], 10 + delay)

    def test_http_date_retry_after_is_converted_to_a_monotonic_deadline(self, get):
        get.return_value = stats_response(status=429, headers={"Retry-After": "Mon, 19 Oct 2026 00:02:00 GMT"})
        with patch("core.ratings.time.time", return_value=1792368000):
            limited = refresh_rating_snapshot("alice", {}, now=10)
        self.assertEqual(limited["blocked_until"], 130)
        self.assertEqual(limited["next_check"], 130)

        get.return_value = stats_response(status=429, headers={"Retry-After": "Sun, 18 Oct 2026 23:00:00 GMT"})
        with patch("core.ratings.time.time", return_value=1792368000):
            expired = refresh_rating_snapshot("alice", {}, now=10)
        self.assertEqual(expired["blocked_until"], 70)


class RatingCategoryTests(unittest.TestCase):
    def test_explicit_available_preference_wins_over_latest_activity(self):
        ratings = {"rapid": {"rating": 1500, "last_played": 30}, "daily": {"rating": 1400, "last_played": 10}}
        self.assertEqual(choose_rating_category(ratings, "daily"), "daily")

    def test_missing_preference_uses_latest_played_category(self):
        ratings = {"rapid": {"rating": 1500, "last_played": 10}, "bullet": {"rating": 1000, "last_played": 30}}
        self.assertEqual(choose_rating_category(ratings, "daily"), "bullet")

    def test_timestamp_ties_and_missing_dates_use_deterministic_category_order(self):
        tied = {"daily": {"rating": 1400, "last_played": 10}, "blitz": {"rating": 1300, "last_played": 10}, "rapid": {"rating": 1500, "last_played": 10}}
        self.assertEqual(choose_rating_category(tied), "rapid")
        missing = {"daily": {"rating": 1400, "last_played": None}, "blitz": {"rating": 1300, "last_played": None}, "bullet": {"rating": 1000, "last_played": None}}
        self.assertEqual(choose_rating_category(missing), "blitz")

    def test_no_ratings_has_no_category(self):
        self.assertIsNone(choose_rating_category({}, "rapid"))


if __name__ == "__main__":
    unittest.main()
