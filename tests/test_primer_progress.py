"""Learning progress survives new sessions and stays separate for each player."""

from pathlib import Path
import tempfile
import unittest

from core.primer_progress import LearningProgress


class ProgressTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.path = Path(temp.name) / "cache" / "primer.sqlite3"

    def test_passed_checks_survive_reopening_without_counting_failed_attempts_as_passed(self):
        progress = LearningProgress(self.path, "player")
        progress.record("check", "board", False)
        self.assertEqual(progress.passed("check"), set())
        progress.record("check", "board", True)
        progress.record("check", "concept:safety", True)
        reopened = LearningProgress(self.path, "lawrence-zhou")
        self.assertEqual(reopened.passed("check"), {"board", "concept:safety"})
        self.assertEqual(LearningProgress(self.path, "other-player").passed("check"), set())

    def test_bookmark_is_per_player_and_persistent(self):
        progress = LearningProgress(self.path, "player")
        progress.bookmark("rook")
        self.assertEqual(LearningProgress(self.path, "lawrence-zhou").last_lesson(), "rook")
        self.assertIsNone(LearningProgress(self.path, "other-player").last_lesson())


if __name__ == "__main__":
    unittest.main()
