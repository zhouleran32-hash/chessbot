"""Personal coaching settings are normalized at the environment boundary."""

import os
import unittest
from unittest.mock import patch

from core.config import load_config


class ConfigTests(unittest.TestCase):
    @patch("core.config.load_dotenv")
    def test_profile_controls_the_default_player_rating_and_review_mode(self, dotenv):
        with patch.dict(os.environ, {"CHESS_COM_USERNAME": " player ", "CHESS_COM_RATING": "564", "CHESSBOT_REVIEW_ONLY": "true"}, clear=True):
            config = load_config()
        self.assertEqual(config.chess_com_username, "player")
        self.assertEqual(config.user_rating, 564)
        self.assertTrue(config.review_only)

    @patch("core.config.load_dotenv")
    def test_invalid_ratings_fall_back_and_full_dashboard_can_be_restored(self, dotenv):
        for value in ("", "unknown", "-1", "4001"):
            with self.subTest(value=value), patch.dict(os.environ, {"CHESS_COM_RATING": value, "CHESSBOT_REVIEW_ONLY": "false"}, clear=True):
                config = load_config()
                self.assertEqual(config.user_rating, 700)
                self.assertFalse(config.review_only)


if __name__ == "__main__":
    unittest.main()
