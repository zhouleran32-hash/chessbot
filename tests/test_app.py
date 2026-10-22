"""Exercise the dashboard through Streamlit widgets with external work isolated."""

import copy
from contextlib import ExitStack
from dataclasses import replace
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import MagicMock, patch

import chess
import chess.svg
from streamlit.testing.v1 import AppTest

from core.analyzer import EngineUnavailableError, GameAnalysisError
from core.chess_client import ChessDotComTimeoutError
from core.config import Settings
from core.coach import CoachingError
from core.rag_engine import KnowledgeBaseError
from core.primer import lessons


ROOT = Path(__file__).resolve().parents[1]
PGN = "1. e4 e5 2. Qh5 Nc6 3. Qxe5+ Nxe5 0-1"
board = chess.Board()
for san in ("e4", "e5", "Qh5", "Nc6"):
    board.push_san(san)
BLUNDER = {
    "move_number": 3, "fen_before": board.fen(), "played_move": "Qxe5+",
    "best_move": "Bc4", "eval_drop": 8.73,
    "board_svg": chess.svg.board(board),
}


def game(number, **changes):
    row = {
        "game_url": f"https://www.chess.com/game/live/{number}",
        "played_at": f"2026-10-{number:02d}T12:00:00+00:00",
        "white_username": "Alice", "white_rating": 700,
        "black_username": "Bob", "black_rating": 720,
        "user_color": "white", "result": "loss", "pgn": PGN,
    }
    return row | changes


def full_review_rows():
    """Three real player positions with independently chosen engine evidence."""
    position = chess.Board()
    rows = []
    for ply, san in enumerate(("e4", "e5", "Qh5", "Nc6", "Qxe5+", "Nxe5"), 1):
        before = position.copy()
        played = position.parse_san(san)
        position.push(played)
        if before.turn != chess.WHITE:
            continue
        best, reply, score, expectation = {
            1: ("d4", "e5", 30, .5),
            3: ("Nf3", "Nc6", -200, .25),
            5: ("Bc4", "Nxe5", -843, .0),
        }[ply]
        rows.append({
            "ply": ply, "move_number": before.fullmove_number, "color": "white",
            "fen_before": before.fen(), "fen_after": position.fen(),
            "played_move": san, "played_uci": played.uci(),
            "best_move": best, "best_uci": before.parse_san(best).uci(),
            "eval_before_cp": 30, "eval_after_cp": score,
            "eval_drop": max(0, (30 - score) / 100), "mate_before": None, "mate_after": None,
            "expected_before": .5, "expected_after": expectation,
            "second_best_expected": None, "second_best_move": None,
            "best_pv": [best], "reply_pv": [reply],
            "legal_move_count": before.legal_moves.count(), "depth": 12, "depth_after": 12,
        })
    return rows


class DashboardTests(unittest.TestCase):
    def setUp(self):
        self.stack = ExitStack()
        self.addCleanup(self.stack.close)
        temp = Path(self.stack.enter_context(tempfile.TemporaryDirectory()))
        self.config = replace(Settings(), stockfish_path="fixture-stockfish", sqlite_path=temp / "cache" / "games.sqlite3", books_dir=temp / "books", chroma_dir=temp / "chroma", review_only=False)
        self.stack.enter_context(patch("core.config.load_config", side_effect=lambda: self.config))
        self.stack.enter_context(patch.dict(os.environ, {"ANTHROPIC_API_KEY": "", "ANTHROPIC_MODEL": ""}))
        self.fetch = self.stack.enter_context(patch("core.chess_client.ChessDotComClient.get_recent_games", return_value=[game(2, accuracy=86.4), game(1)]))
        self.ratings = self.stack.enter_context(patch("core.chess_client.ChessDotComClient.get_player_ratings", return_value={}))
        self.analysis_calls = []
        self.analysis_error = None
        self.position_analysis_calls = []
        self.position_analysis_error = None
        self.blunders = [BLUNDER, BLUNDER | {"eval_drop": 2.0}]
        self.full_moves = full_review_rows()
        self.stockfish_calls = []
        self.engine_missing = False

        def make_analyzer(*args, **kwargs):
            if self.engine_missing and not kwargs.get("allow_mock"):
                raise EngineUnavailableError("Set STOCKFISH_PATH to a valid executable.")
            analyzer = MagicMock()
            analyzer.is_mock = self.engine_missing
            analyzer.__enter__.return_value = analyzer

            def analyze(pgn, color, **options):
                self.analysis_calls.append((pgn, color))
                if self.analysis_error:
                    raise self.analysis_error
                callback = options["progress_callback"]
                callback(0, 6)
                callback(6, 6)
                return copy.deepcopy(self.blunders)

            analyzer.analyze_game.side_effect = analyze
            def full_review(pgn, color, **options):
                self.analysis_calls.append((pgn, color))
                if options.get("engine_details"):
                    self.stockfish_calls.append(kwargs["time_limit"])
                if self.analysis_error:
                    raise self.analysis_error
                options["progress_callback"](6, 6)
                rows = copy.deepcopy(self.full_moves)
                if options.get("engine_details"):
                    for row in rows:
                        row["candidates"] = [
                            {"move": row["best_move"], "uci": row["best_uci"], "cp": 30,
                             "mate": None, "expected": .5, "depth": 18, "pv": row["best_pv"]},
                            {"move": row["played_move"], "uci": row["played_uci"], "cp": row["eval_after_cp"],
                             "mate": row["mate_after"], "expected": row["expected_after"], "depth": 18,
                             "pv": [row["played_move"], *row["reply_pv"]]},
                        ]
                return rows
            analyzer.review_game.side_effect = full_review
            def position_review(fen, played_move, best_move):
                self.position_analysis_calls.append((fen, played_move, best_move))
                if self.position_analysis_error:
                    raise self.position_analysis_error
                row = copy.deepcopy(self.full_moves[-1])
                row.update(fen_before=fen, played_move=played_move, best_move=best_move,
                           best_pv=["Bc4", "Nf6", "d3"], reply_pv=["Nxe5"])
                return row
            analyzer.review_move.side_effect = position_review
            return analyzer

        self.stack.enter_context(patch("core.analyzer.GameAnalyzer", side_effect=make_analyzer))
        self.kb = MagicMock()
        self.kb.search_advice.return_value = ["Protect your pieces.\n\n[Source: Built-in beginner principles | page n/a]"]
        self.kb.ingest_pdf.return_value = 4
        self.stack.enter_context(patch("core.rag_engine.ChessBookKnowledgeBase", return_value=self.kb))
        self.app = AppTest.from_file(str(ROOT / "app.py"), default_timeout=15)
        self.app.session_state["review_detail"] = "Key mistakes"

    def run_app(self):
        self.app.run()
        self.assertEqual(list(self.app.exception), [])
        return self.app

    def button(self, label):
        return next(button for button in self.app.button if button.label == label)

    def fetch_games(self):
        self.run_app()
        self.app.text_input(key="username").set_value("Alice")
        self.button("Fetch Games").click()
        self.run_app()

    def choose(self, number=2):
        self.app.selectbox(key="selected_game").select(f"https://www.chess.com/game/live/{number}")
        return self.run_app()

    def text(self):
        return "\n".join(item.value for kind in (self.app.markdown, self.app.caption, self.app.info, self.app.warning, self.app.success, self.app.error) for item in kind)

    def test_empty_dashboard_has_sidebar_controls_and_no_automatic_fetch(self):
        self.run_app()
        self.assertEqual(self.app.title[0].value, "ChessBot")
        self.assertEqual(self.app.file_uploader[0].label, "Feed a Chess Book")
        self.assertTrue(self.button("Generate My Weekly Improvement Plan").disabled)
        self.fetch.assert_not_called()

    def test_quick_review_explains_and_replays_the_better_line_without_reanalysis(self):
        self.fetch_games()
        self.choose()
        self.assertIn("knight from g8 to f6", self.text())
        self.assertIn("Nf6", self.text())
        self.assertEqual(len(self.position_analysis_calls), 1)
        self.app.radio(key="quick_review_line").set_value("Better move")
        self.run_app()
        self.app.slider(key="quick_line_step").set_value(2)
        self.run_app()
        self.assertIn("3... Nf6", self.text())
        self.assertEqual(len(self.position_analysis_calls), 1)
        self.assertEqual(len(self.analysis_calls), 1)

    def test_quick_review_reuses_matching_full_review_evidence(self):
        self.app.session_state["review_detail"] = "Every move"
        self.fetch_games()
        self.choose()
        self.app.radio(key="review_detail").set_value("Key mistakes")
        self.run_app()
        self.assertIn("quick_review_line", [item.key for item in self.app.radio])
        self.assertEqual(self.position_analysis_calls, [])

    def test_back_to_mistake_leaves_hypothetical_line_and_restores_original_position(self):
        self.fetch_games()
        self.choose()
        self.app.radio(key="quick_review_line").set_value("After your move")
        self.run_app()
        self.button("Back to this mistake").click()
        self.run_app()
        self.assertEqual(self.app.radio(key="quick_review_line").value, "Your game")
        self.assertNotIn("Back to this mistake", [item.label for item in self.app.button])
        self.assertEqual(len(self.position_analysis_calls), 1)

    def test_failed_continuation_waits_for_explicit_retry_and_keeps_original_review(self):
        self.position_analysis_error = GameAnalysisError("Continuation search stopped.")
        self.fetch_games()
        self.choose()
        self.assertIn("Best move", [item.label for item in self.app.metric])
        self.assertIn("Continuation search stopped", self.text())
        self.run_app()
        self.assertEqual(len(self.position_analysis_calls), 1)
        self.position_analysis_error = None
        self.button("Retry continuation").click()
        self.run_app()
        self.assertIn("knight from g8 to f6", self.text())
        self.assertEqual(len(self.position_analysis_calls), 2)

    def test_detailed_review_lists_every_player_move_and_independent_quality(self):
        self.app.session_state["review_detail"] = "Every move"
        self.fetch_games()
        self.choose()
        self.assertIn("review_move", [item.key for item in self.app.selectbox])
        table = next(item.value for item in self.app.dataframe if "Assessment" in item.value.columns)
        self.assertEqual(list(table["Played"]), ["e4", "Qh5", "Qxe5+"])
        self.assertEqual(list(table["Assessment"]), ["Excellent", "Blunder", "Blunder"])
        self.assertIn("independent", self.text().lower())
        self.assertIn("What your move does", self.text())

    def test_detailed_selection_and_line_replay_do_not_repeat_analysis(self):
        self.app.session_state["review_detail"] = "Every move"
        self.fetch_games()
        self.choose()
        self.assertIn("review_move", [item.key for item in self.app.selectbox])
        self.app.selectbox(key="review_move").set_value(1)
        self.run_app()
        self.assertIn("pawn from e2 to e4", self.text())
        self.app.selectbox(key="review_board_view").set_value("Best continuation")
        self.run_app()
        self.app.slider(key="review_line_step").set_value(1)
        self.run_app()
        self.assertEqual(len(self.analysis_calls), 1)
        self.app.button(key="review_next_move").click()
        self.run_app()
        self.assertEqual(self.app.selectbox(key="review_move").value, 3)
        self.assertEqual(self.app.selectbox(key="review_board_view").value, "Before your move")

    def test_detailed_zero_blunders_still_reviews_good_moves(self):
        self.app.session_state["review_detail"] = "Every move"
        for move in self.full_moves:
            move.update(best_move=move["played_move"], best_uci=move["played_uci"], best_pv=[move["played_move"]], expected_after=.5, eval_after_cp=30, eval_drop=0)
        self.fetch_games()
        self.choose()
        self.assertIn("review_move", [item.key for item in self.app.selectbox])
        self.assertEqual(self.app.selectbox(key="review_move").value, 1)
        self.assertEqual(next(metric.value for metric in self.app.metric if metric.label == "Blunders"), "0")
        self.assertIn("What your move does", self.text())

    def test_detailed_mate_score_is_not_displayed_as_hundreds_of_pawns(self):
        self.app.session_state["review_detail"] = "Every move"
        self.full_moves[-1].update(mate_after=-2, eval_after_cp=-99998, eval_drop=1000.28)
        self.fetch_games()
        self.choose()
        self.assertIn("review_move", [item.key for item in self.app.selectbox])
        self.app.selectbox(key="review_move").set_value(5)
        self.run_app()
        table = next(item.value for item in self.app.dataframe if "Assessment" in item.value.columns)
        self.assertEqual(table.iloc[-1]["After"], "Mate against you in 2")
        self.assertNotIn("1000.28 pawns", self.text())

    def test_detailed_mock_mode_does_not_award_stockfish_quality_labels(self):
        self.app.session_state["review_detail"] = "Every move"
        self.engine_missing = True
        self.fetch_games()
        self.app.checkbox(key="allow_mock").check()
        self.choose()
        self.assertIn("review_move", [item.key for item in self.app.selectbox])
        table = next(item.value for item in self.app.dataframe if "Assessment" in item.value.columns)
        self.assertEqual(set(table["Assessment"]), {"Preview"})

    def test_detailed_upgrade_failure_preserves_quick_review_and_waits_for_retry(self):
        self.fetch_games()
        self.choose()
        self.analysis_error = GameAnalysisError("Detailed analysis stopped.")
        self.app.radio(key="review_detail").set_value("Every move")
        self.run_app()
        record = self.app.session_state["analyses"][game(2)["game_url"]]
        self.assertIn("blunders", record)
        self.assertEqual(len(record["blunders"]), 2)
        self.assertEqual(len(self.analysis_calls), 2)
        self.app.radio(key="review_detail").set_value("Key mistakes")
        self.run_app()
        self.assertEqual(next(metric.value for metric in self.app.metric if metric.label == "Blunders"), "2")
        self.analysis_error = None
        self.app.radio(key="review_detail").set_value("Every move")
        self.run_app()
        self.assertEqual(len(self.analysis_calls), 2)
        self.button("Retry detailed analysis").click()
        self.run_app()
        self.assertEqual(len(self.analysis_calls), 3)
        self.assertIn("review_move", [item.key for item in self.app.selectbox])

    def test_detailed_selected_move_resumes_after_quick_review(self):
        self.app.session_state["review_detail"] = "Every move"
        self.fetch_games()
        self.choose()
        self.app.selectbox(key="review_move").set_value(5)
        self.run_app()
        self.app.radio(key="review_detail").set_value("Key mistakes")
        self.run_app()
        self.app.radio(key="review_detail").set_value("Every move")
        self.run_app()
        self.assertEqual(self.app.selectbox(key="review_move").value, 5)
        self.assertEqual(len(self.analysis_calls), 1)

    def test_stockfish_review_is_separate_and_replay_uses_cached_candidates(self):
        self.app.session_state["review_detail"] = "Every move"
        self.fetch_games()
        self.choose()
        original = copy.deepcopy(self.app.session_state["analyses"])
        self.app.radio(key="review_detail").set_value("Stockfish analysis")
        self.run_app()
        self.assertEqual(self.stockfish_calls, [])
        self.button("Run Stockfish review").click()
        self.run_app()
        self.assertEqual(self.stockfish_calls, [1.0])
        self.assertEqual(self.app.session_state["analyses"], original)
        self.assertIn("sf_move", [item.key for item in self.app.selectbox])
        self.app.selectbox(key="sf_move").set_value(5)
        self.run_app()
        self.app.selectbox(key="sf_line").set_value("candidate_1")
        self.run_app()
        self.app.button(key="sf_next_position").click()
        self.run_app()
        self.assertIn("3. Qxe5+", self.text())
        self.assertEqual(self.stockfish_calls, [1.0])
        self.app.radio(key="review_detail").set_value("Every move")
        self.run_app()
        self.assertEqual(self.app.session_state["analyses"], original)
        self.app.radio(key="review_detail").set_value("Stockfish analysis")
        self.run_app()
        self.assertEqual(self.app.selectbox(key="sf_move").value, 5)
        self.assertEqual(self.stockfish_calls, [1.0])

    def test_stockfish_failure_does_not_overwrite_independent_review_or_auto_retry(self):
        self.fetch_games()
        self.choose()
        original = copy.deepcopy(self.app.session_state["analyses"])
        self.app.radio(key="review_detail").set_value("Stockfish analysis")
        self.run_app()
        self.analysis_error = GameAnalysisError("Deep search stopped.")
        self.button("Run Stockfish review").click()
        self.run_app()
        self.assertIn("Deep search stopped", self.text())
        self.run_app()
        self.assertEqual(self.stockfish_calls, [1.0])
        self.assertEqual(self.app.session_state["analyses"], original)
        self.analysis_error = None
        self.button("Retry Stockfish review").click()
        self.run_app()
        self.assertEqual(self.stockfish_calls, [1.0, 1.0])
        self.assertIn("sf_move", [item.key for item in self.app.selectbox])

    def test_stockfish_review_requires_real_engine_even_with_preview_enabled(self):
        self.engine_missing = True
        self.fetch_games()
        self.app.checkbox(key="allow_mock").check()
        self.choose()
        self.app.radio(key="review_detail").set_value("Stockfish analysis")
        self.run_app()
        self.assertNotIn("Run Stockfish review", [item.label for item in self.app.button])
        self.assertEqual(self.stockfish_calls, [])

    def test_start_screen_loads_games_without_opening_sidebar(self):
        self.config = replace(self.config, review_only=True)
        self.run_app()
        self.assertIn("welcome_username", [item.key for item in self.app.text_input])
        self.app.text_input(key="welcome_username").set_value(" Alice ")
        self.app.button(key="start_review").click()
        self.run_app()
        self.assertEqual(self.app.text_input(key="username").value, "Alice")
        self.assertEqual(self.app.session_state["loaded_username"], "alice")
        self.assertEqual(self.app.selectbox(key="selected_game").value, game(2)["game_url"])
        self.assertEqual(len(self.analysis_calls), 1)
        self.run_app()
        self.assertEqual(len(self.analysis_calls), 1)

    def test_start_screen_can_recover_from_fetch_failure(self):
        self.config = replace(self.config, review_only=True)
        self.fetch.side_effect = ChessDotComTimeoutError("Chess.com timed out. Try again.")
        self.run_app()
        self.assertIn("welcome_username", [item.key for item in self.app.text_input])
        self.app.text_input(key="welcome_username").set_value("Alice")
        self.app.button(key="start_review").click()
        self.run_app()
        self.assertIn("timed out", self.text())
        self.assertEqual(self.app.session_state["games"], [])
        self.fetch.side_effect = None
        self.app.button(key="start_review").click()
        self.run_app()
        self.assertEqual(len(self.app.session_state["games"]), 2)
        self.assertNotIn("timed out", self.text())

    def test_start_screen_opens_primer_without_fetching_games(self):
        self.config = replace(self.config, review_only=True)
        self.run_app()
        self.assertIn("start_primer", [item.key for item in self.app.button])
        self.app.button(key="start_primer").click()
        self.run_app()
        self.assertEqual(self.app.radio(key="main_section").value, "The Soviet Chess Primer")
        self.assertEqual(self.app.selectbox(key="primer_lesson").value, "board-setup")
        self.fetch.assert_not_called()

    def test_current_rating_loads_on_open_without_fetching_games(self):
        self.config = replace(self.config, review_only=True, chess_com_username="Alice", user_rating=564)
        self.ratings.return_value = {
            "rapid": {"rating": 591, "last_played": 200},
            "blitz": {"rating": 870, "last_played": 100},
        }
        self.run_app()
        self.assertEqual(self.app.session_state["user_rating"], 591)
        self.assertEqual(self.app.selectbox(key="rating_category").value, "rapid")
        self.assertEqual(next(metric.value for metric in self.app.metric if metric.label == "Rapid rating"), "591")
        self.assertNotIn("user_rating", [item.key for item in self.app.number_input])
        self.fetch.assert_not_called()

    def test_rating_category_selection_updates_coaching_level(self):
        self.config = replace(self.config, review_only=True, chess_com_username="Alice")
        self.ratings.return_value = {
            "rapid": {"rating": 591, "last_played": 200},
            "blitz": {"rating": 870, "last_played": 100},
        }
        self.run_app()
        self.assertIn("rating_category", [item.key for item in self.app.selectbox])
        self.app.selectbox(key="rating_category").set_value("blitz")
        self.run_app()
        self.assertEqual(self.app.session_state["user_rating"], 870)
        self.assertEqual(self.app.session_state["rating_source"]["category"], "blitz")

    def test_expired_rating_refresh_updates_without_game_fetch(self):
        self.config = replace(self.config, review_only=True, chess_com_username="Alice")
        self.ratings.return_value = {"rapid": {"rating": 591, "last_played": 200}}
        self.run_app()
        self.assertIn("rating_snapshots", self.app.session_state)
        self.ratings.return_value = {"rapid": {"rating": 612, "last_played": 300}}
        self.app.session_state["rating_snapshots"]["alice"]["next_check"] = 0
        self.run_app()
        self.assertEqual(self.app.session_state["user_rating"], 612)
        self.fetch.assert_not_called()

    def test_rating_refresh_failure_keeps_last_rating_and_marks_it_stale(self):
        self.config = replace(self.config, review_only=True, chess_com_username="Alice")
        self.ratings.return_value = {"rapid": {"rating": 591, "last_played": 200}}
        self.run_app()
        self.assertIn("refresh_live_rating", [item.key for item in self.app.button])
        self.ratings.side_effect = ChessDotComTimeoutError("Chess.com timed out. Try again.")
        self.app.button(key="refresh_live_rating").click()
        self.run_app()
        self.assertEqual(self.app.session_state["user_rating"], 591)
        self.assertTrue(self.app.session_state["rating_source"]["stale"])
        self.assertIn("last successful", self.text())
        self.ratings.side_effect = None
        self.ratings.return_value = {"rapid": {"rating": 612, "last_played": 300}}
        self.app.button(key="refresh_live_rating").click()
        self.run_app()
        self.assertEqual(self.app.session_state["user_rating"], 612)
        self.assertFalse(self.app.session_state["rating_source"]["stale"])

    def test_failed_rating_for_new_player_does_not_show_previous_players_rating(self):
        self.config = replace(self.config, review_only=True, chess_com_username="Alice", user_rating=564)
        self.ratings.return_value = {"rapid": {"rating": 591, "last_played": 200}}
        self.run_app()
        self.assertEqual(self.app.session_state["user_rating"], 591)
        self.ratings.side_effect = ChessDotComTimeoutError("Chess.com timed out. Try again.")
        self.app.text_input(key="username").set_value("Bob")
        self.button("Fetch Games").click()
        self.run_app()
        self.assertEqual(self.app.session_state["user_rating"], 564)
        self.assertIsNone(self.app.session_state["rating_source"])
        self.assertEqual(self.app.number_input(key="user_rating").label, "Manual coaching level")

    def test_selection_analyzes_once_slider_reruns_and_weekly_plan_uses_each_game_once(self):
        self.fetch_games()
        self.assertEqual(list(self.app.dataframe[0].value.columns), ["White", "Black", "Result", "Date (UTC)"])
        self.choose()
        self.assertEqual(len(self.analysis_calls), 1)
        self.assertEqual(next(metric.value for metric in self.app.metric if metric.label == "Accuracy"), "86.4%")
        self.assertIn("[Source: Built-in beginner principles", self.text())
        self.app.selectbox(key="review_mistake").set_value(2)
        self.run_app()
        self.assertEqual(len(self.analysis_calls), 1)
        self.choose(1)
        self.assertEqual(next(metric.value for metric in self.app.metric if metric.label == "Accuracy"), "—")
        self.choose(2)
        self.assertEqual(len(self.analysis_calls), 2)
        self.button("Generate My Weekly Improvement Plan").click()
        self.run_app()
        self.assertIn("2 games", self.text())
        self.assertIn("4 blunders", self.text())
        self.assertIn("Focus 1:", self.text())

    def test_fetch_error_preserves_loaded_games_and_can_recover(self):
        self.fetch_games()
        self.fetch.side_effect = ChessDotComTimeoutError("Chess.com timed out. Try again.")
        self.button("Fetch Games").click()
        self.run_app()
        self.assertIn("timed out", self.text())
        self.assertEqual(len(self.app.dataframe[0].value), 2)
        self.fetch.side_effect = None
        self.button("Fetch Games").click()
        self.run_app()
        self.assertNotIn("timed out", self.text())

    def test_mock_mode_is_labeled_and_can_be_disabled(self):
        self.engine_missing = True
        self.fetch_games()
        self.assertFalse(self.app.checkbox(key="allow_mock").value)
        self.choose()
        self.assertEqual(self.analysis_calls, [])
        self.assertIn("STOCKFISH_PATH", self.text())
        self.app.checkbox(key="allow_mock").check()
        self.run_app()
        self.assertEqual(len(self.analysis_calls), 1)
        self.assertIn("Mock analysis", self.text())

    def test_failed_analysis_waits_for_explicit_retry(self):
        self.analysis_error = GameAnalysisError("Stockfish stopped unexpectedly.")
        self.fetch_games()
        self.choose()
        self.assertIsNotNone(self.button("Retry analysis"))
        self.run_app()
        self.assertEqual(len(self.analysis_calls), 1)
        self.analysis_error = None
        self.button("Retry analysis").click()
        self.run_app()
        self.assertEqual(len(self.analysis_calls), 2)
        self.assertTrue(self.app.metric)

    def test_pdf_indexes_once_preserves_filename_and_allows_explicit_retry(self):
        self.run_app()
        self.kb.ingest_pdf.side_effect = KnowledgeBaseError("Set OPENAI_API_KEY for book indexing.")
        self.app.file_uploader[0].set_value(("../tactics.pdf", b"%PDF-fixture", "application/pdf"))
        self.run_app()
        self.assertIsNotNone(self.button("Retry indexing"))
        self.run_app()
        self.assertEqual(self.kb.ingest_pdf.call_count, 1)
        self.kb.ingest_pdf.side_effect = None
        self.button("Retry indexing").click()
        self.run_app()
        self.assertEqual(self.kb.ingest_pdf.call_count, 2)
        path = Path(self.kb.ingest_pdf.call_args.args[0])
        self.assertEqual(path.name, "tactics.pdf")
        self.assertTrue(path.is_relative_to(self.config.books_dir))
        self.assertEqual(path.read_bytes(), b"%PDF-fixture")
        self.run_app()
        self.assertEqual(self.kb.ingest_pdf.call_count, 2)
        self.assertIn("4 passages", self.text())

    def test_ai_review_is_cached_and_new_book_refreshes_context(self):
        self.config = replace(self.config, openai_api_key="test-key")
        self.stack.enter_context(patch("openai.OpenAI", return_value=MagicMock()))
        review = self.stack.enter_context(patch("core.coach.ChessCoach.review_blunder", return_value="**The Tactical Breakdown**\nKeep your queen safe.\n\n**The Principle from the Books**\n[Source: tactics.pdf | page 7]\n\n**The Mental Check**\nWhat can be captured?"))
        self.fetch_games()
        self.choose()
        self.run_app()
        self.assertEqual(review.call_count, 1)
        self.assertIn("tactics.pdf | page 7", self.text())
        self.assertEqual(review.call_args.kwargs["user_rating"], 700)
        self.app.file_uploader[0].set_value(("tactics.pdf", b"%PDF-new", "application/pdf"))
        self.run_app()
        self.assertEqual(review.call_count, 2)

    def test_ai_failure_is_not_automatically_repeated(self):
        self.config = replace(self.config, openai_api_key="test-key")
        self.stack.enter_context(patch("openai.OpenAI", return_value=MagicMock()))
        review = self.stack.enter_context(patch("core.coach.ChessCoach.review_blunder", side_effect=CoachingError("Could not generate coaching feedback.")))
        self.fetch_games()
        self.choose()
        self.assertIsNotNone(self.button("Retry coaching"))
        self.run_app()
        self.assertEqual(review.call_count, 1)
        self.assertIn("Could not generate", self.text())
        review.side_effect = None
        review.return_value = "**The Mental Check**\nWhat can be captured?"
        self.button("Retry coaching").click()
        self.run_app()
        self.assertEqual(review.call_count, 2)

    def test_zero_blunders_is_a_complete_analysis_and_has_no_slider(self):
        self.blunders = []
        self.fetch_games()
        self.choose()
        self.assertIn("No blunders", self.text())
        self.assertFalse(any(slider.label == "Blunder" for slider in self.app.slider))
        self.assertFalse(self.button("Generate My Weekly Improvement Plan").disabled)

    def test_switching_players_resets_session_analysis(self):
        self.fetch_games()
        self.choose()
        self.app.text_input(key="username").set_value("Charlie")
        self.fetch.return_value = [game(3, white_username="Charlie")]
        self.button("Fetch Games").click()
        self.run_app()
        self.assertTrue(self.button("Generate My Weekly Improvement Plan").disabled)
        self.assertIsNone(self.app.selectbox(key="selected_game").value)

    def test_empty_history_and_notation_only_pdf_are_explained(self):
        self.fetch.return_value = []
        self.kb.ingest_pdf.return_value = 0
        self.fetch_games()
        self.assertIn("No completed games", self.text())
        self.app.file_uploader[0].set_value(("moves.pdf", b"%PDF-moves", "application/pdf"))
        self.run_app()
        self.assertIn("No explanatory text", self.text())
        self.assertFalse(self.app.dataframe)

    def test_book_search_failure_has_an_immediate_retry_and_keeps_weekly_plan_usable(self):
        self.kb.search_advice.side_effect = KnowledgeBaseError("Book search is temporarily unavailable.")
        self.fetch_games()
        self.choose()
        self.assertIsNotNone(self.button("Retry book search"))
        self.assertFalse(self.button("Generate My Weekly Improvement Plan").disabled)
        self.kb.search_advice.side_effect = None
        self.button("Retry book search").click()
        self.run_app()
        self.assertIn("Protect your pieces", self.text())

    def test_new_analysis_requires_regenerating_the_weekly_plan(self):
        self.fetch_games()
        self.choose()
        self.button("Generate My Weekly Improvement Plan").click()
        self.run_app()
        self.assertIn("Focus 1:", self.text())
        self.choose(1)
        self.assertNotIn("Focus 1:", self.text())
        self.button("Generate My Weekly Improvement Plan").click()
        self.run_app()
        self.assertIn("2 games · 4 blunders", self.text())

    def test_anthropic_selection_uses_the_configured_provider(self):
        self.stack.enter_context(patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key", "ANTHROPIC_MODEL": "fixture-claude-model"}))
        client = MagicMock()
        client.chat = None
        factory = self.stack.enter_context(patch("anthropic.Anthropic", return_value=client))
        review = self.stack.enter_context(patch("core.coach.ChessCoach.review_blunder", return_value="A grounded review."))
        self.fetch_games()
        self.assertEqual(self.app.selectbox(key="coach_provider").value, "Anthropic")
        self.choose()
        factory.assert_called_once()
        review.assert_called_once()
        self.assertIn("A grounded review", self.text())

    def test_personal_review_fetches_and_analyzes_latest_game_with_no_book_or_plan_controls(self):
        self.config = replace(self.config, chess_com_username="Lawrence-Zhou", user_rating=564, review_only=True)
        self.fetch.return_value = [game(2, white_username="Lawrence-Zhou", white_rating=590)]
        self.run_app()
        self.assertEqual(self.app.text_input(key="username").value, "Lawrence-Zhou")
        self.assertEqual(self.app.number_input(key="user_rating").value, 564)
        self.button("Fetch Games").click()
        self.run_app()
        self.assertEqual(len(self.analysis_calls), 1)
        self.assertIn("Nxe5", self.text())
        self.assertIn("bishop from f1 to c4", self.text())
        self.assertFalse(self.app.file_uploader)
        self.assertFalse(self.app.tabs)
        self.assertNotIn("Enable the AI coach", self.text())

    def test_primer_teaches_all_three_chapters_and_game_review_stays_available(self):
        self.config = replace(self.config, review_only=True, chess_com_username="Lawrence-Zhou", user_rating=564)
        self.run_app()
        self.assertEqual(self.app.radio(key="main_section").value, "Your games")
        self.app.radio(key="main_section").set_value("The Soviet Chess Primer")
        self.run_app()
        options = list(self.app.selectbox(key="primer_lesson").options)
        self.assertTrue(any("The board and the armies" in option for option in options))
        self.assertEqual(set(options), {item.title for item in lessons() if item.chapter == 1})
        self.app.selectbox(key="primer_chapter").select(3)
        self.run_app()
        self.assertEqual(set(self.app.selectbox(key="primer_lesson").options), {item.title for item in lessons() if item.chapter == 3})
        self.app.selectbox(key="primer_lesson").select("counterplan")
        self.run_app()
        self.assertEqual(self.app.selectbox(key="primer_lesson").value, "counterplan")
        self.app.selectbox(key="primer_chapter").select(1)
        self.run_app()
        self.assertIn("The board and the armies", self.text())
        self.assertIn("Or choose the move by name", self.text())
        self.button("Next").click()
        self.run_app()
        self.assertIn("Queens stand on d1", self.text())
        self.button("e4").click()
        self.run_app()
        self.assertIn("The king starts on e1", self.text())
        self.button("Try again").click()
        self.run_app()
        self.app.session_state["primer_board_drop"] = ("e2", "e4")
        self.run_app()
        self.assertIn("You played e4.", self.text())
        self.assertIn("The king starts on e1", self.text())
        self.app.radio(key="main_section").set_value("Your games")
        self.run_app()
        self.button("Fetch Games").click()
        self.run_app()
        self.assertEqual(len(self.analysis_calls), 1)

    def test_pending_promotion_cancels_when_selecting_another_piece(self):
        self.config = replace(self.config, review_only=True, chess_com_username="Alice")
        self.run_app()
        self.app.radio(key="main_section").set_value("The Soviet Chess Primer")
        self.run_app()
        self.app.selectbox(key="primer_lesson").select("promotion")
        self.run_app()

        def click_square(square):
            self.app.session_state["primer_square_click"] = square
            self.run_app()

        click_square("e7")
        click_square("e8")
        self.assertEqual(self.app.session_state["primer_promotion"], ("e7", "e8"))
        self.assertTrue(any(button.key == "promo-promotion-q" for button in self.app.button))
        click_square("g1")
        self.assertIsNone(self.app.session_state["primer_promotion"])
        self.assertFalse(any(button.key and button.key.startswith("promo-promotion-")
                             for button in self.app.button))
        click_square("f2")
        board = chess.Board(self.app.session_state["primer_board_fen"])
        self.assertEqual(board.king(chess.WHITE), chess.F2)
        self.assertEqual(board.piece_at(chess.E7), chess.Piece(chess.PAWN, chess.WHITE))

    def test_black_underpromotion_waits_for_choice_then_saves_the_correct_move(self):
        from core.primer_progress import LearningProgress
        self.config = replace(self.config, review_only=True, chess_com_username="Alice")
        store = LearningProgress(self.config.sqlite_path.parent / "primer.sqlite3", "Alice")
        store.bookmark("ch8-rook-v-pawn")
        self.run_app()
        self.app.radio(key="main_section").set_value("The Soviet Chess Primer")
        self.run_app()
        for square in ("c2", "c1"):
            self.app.session_state["primer_square_click"] = square
            self.run_app()
        self.assertIsNone(self.app.session_state["primer_board_fen"])
        self.assertNotIn("board", store.passed("ch8-rook-v-pawn"))
        self.app.button(key="promo-ch8-rook-v-pawn-n").click()
        self.run_app()
        board = chess.Board(self.app.session_state["primer_board_fen"])
        self.assertEqual(board.piece_at(chess.C1), chess.Piece(chess.KNIGHT, chess.BLACK))
        self.assertTrue(board.is_check())
        self.assertIn("board", store.passed("ch8-rook-v-pawn"))
        self.assertIsNone(self.app.session_state["primer_promotion"])

    def test_worked_variation_and_move_survive_navigation_without_crossing_players(self):
        from core.primer_progress import LearningProgress
        self.config = replace(self.config, review_only=True, chess_com_username="Alice")
        path = self.config.sqlite_path.parent / "primer.sqlite3"
        for player in ("Alice", "Bob"):
            LearningProgress(path, player).bookmark("app-more-11")
        self.run_app()
        self.app.radio(key="main_section").set_value("The Soviet Chess Primer")
        self.run_app()
        self.app.selectbox(key="worked_app-more-11").select(1)
        self.run_app()
        for _ in range(3):
            self.app.button(key="example_next_app-more-11_1").click()
            self.run_app()
        self.assertEqual(self.app.session_state["example_app-more-11_1"], 3)
        self.app.radio(key="main_section").set_value("Your games")
        self.run_app()
        self.app.radio(key="main_section").set_value("The Soviet Chess Primer")
        self.run_app()
        self.assertEqual(self.app.selectbox(key="worked_app-more-11").value, 1)
        self.assertIn("Position 4 of 34", self.text())
        self.app.button(key="primer_previous_lesson").click()
        self.run_app()
        self.app.button(key="primer_next_lesson").click()
        self.run_app()
        self.assertEqual(self.app.selectbox(key="worked_app-more-11").value, 1)
        self.assertIn("Position 4 of 34", self.text())
        self.app.text_input(key="username").set_value("Bob")
        self.button("Fetch Games").click()
        self.run_app()
        self.assertEqual(self.app.selectbox(key="worked_app-more-11").value, 0)
        self.assertEqual(self.app.session_state["example_app-more-11_0"], 0)

    def test_new_chapters_are_navigable_and_their_saved_place_is_restored(self):
        from core.primer_progress import LearningProgress
        self.config = replace(self.config, review_only=True, chess_com_username="Lawrence-Zhou")
        store = LearningProgress(self.config.sqlite_path.parent / "primer.sqlite3", "Lawrence-Zhou")
        store.bookmark("ch7-queen")
        self.run_app()
        self.app.radio(key="main_section").set_value("The Soviet Chess Primer")
        self.run_app()
        self.assertEqual(self.app.selectbox(key="primer_chapter").value, 7)
        self.assertEqual(self.app.selectbox(key="primer_lesson").value, "ch7-queen")
        self.assertIn("printed pages 247–248", self.text())
        self.app.button(key="example_next_ch7-queen_0").click()
        self.run_app()
        self.assertIn("blocks the h5–f7 diagonal", self.text())
        self.button("g6").click()
        self.run_app()
        self.assertIn("board", store.passed("ch7-queen"))
        for chapter in (4, 5, 6, 7):
            self.app.selectbox(key="primer_chapter").select(chapter)
            self.run_app()
            self.assertEqual(set(self.app.selectbox(key="primer_lesson").options), {item.title for item in lessons() if item.chapter == chapter})
            self.assertIn("Book reference: printed pages", self.text())
            self.assertEqual([tab.label for tab in self.app.tabs], ["Learn", "Worked examples", "Practice", "Review"])
        self.assertIn("chapters 1–10", self.text())
        self.assertIn("and the appendix", self.text())
        self.assertNotIn("appendix is not yet taught", self.text())
        self.assertNotIn("Chapters 11–10", self.text())

    def test_appendix_is_named_navigable_and_remembers_practice(self):
        from core.primer_progress import LearningProgress
        self.config = replace(self.config, review_only=True, chess_com_username="Lawrence-Zhou")
        store = LearningProgress(self.config.sqlite_path.parent / "primer.sqlite3", "Lawrence-Zhou")
        store.record("board-setup", "board", True)
        store.bookmark("app-introduction")
        self.run_app()
        self.app.radio(key="main_section").set_value("The Soviet Chess Primer")
        self.run_app()
        self.assertEqual(self.app.selectbox(key="primer_chapter").value, 11)
        self.assertIn("Appendix · Chess compositions", self.text())
        self.assertNotIn("Chapter 11", self.text())
        self.assertIn("printed pages 377–378", self.text())
        self.assertEqual(self.app.selectbox(key="primer_lesson").value, "app-introduction")
        self.app.button(key="example_next_app-introduction_0").click()
        self.run_app()
        self.assertIn("queen retreats to d7", self.text())
        self.button("Qd7").click()
        self.run_app()
        self.assertIn("board", store.passed("app-introduction"))
        self.app.button(key="primer_previous_lesson").click()
        self.run_app()
        self.assertEqual(self.app.selectbox(key="primer_chapter").value, 10)
        self.app.button(key="primer_next_lesson").click()
        self.run_app()
        self.assertEqual(self.app.selectbox(key="primer_lesson").value, "app-introduction")
        self.assertIn("board", store.passed("board-setup"))

    def test_appendix_collections_filter_lessons_and_follow_cross_group_navigation(self):
        self.config = replace(self.config, review_only=True)
        self.run_app()
        self.app.radio(key="main_section").set_value("The Soviet Chess Primer")
        self.run_app()
        self.app.selectbox(key="primer_chapter").select(11)
        self.run_app()
        self.app.selectbox(key="primer_collection").select("Two-move problems")
        self.run_app()
        self.assertEqual(self.app.selectbox(key="primer_lesson").value, "app-two-01")
        self.assertTrue(all("Two-mover" in option for option in self.app.selectbox(key="primer_lesson").options))
        self.app.button(key="primer_previous_lesson").click()
        self.run_app()
        self.assertEqual(self.app.selectbox(key="primer_lesson").value, "app-study-method")
        self.assertEqual(self.app.selectbox(key="primer_collection").value, "Getting started")
        self.app.button(key="primer_next_lesson").click()
        self.run_app()
        self.assertEqual(self.app.selectbox(key="primer_collection").value, "Two-move problems")

    def test_complete_appendix_collections_and_last_study_save_progress(self):
        from core.primer_progress import LearningProgress
        self.config = replace(self.config, review_only=True, chess_com_username="Lawrence-Zhou")
        self.run_app()
        self.app.radio(key="main_section").set_value("The Soviet Chess Primer")
        self.run_app()
        self.app.selectbox(key="primer_chapter").select(11)
        self.run_app()
        for label, count in (
            ("Getting started", 8), ("Two-move problems", 20),
            ("Three-move problems", 20), ("Longer problems", 15),
            ("Winning studies", 32), ("Drawing studies", 11),
        ):
            self.app.selectbox(key="primer_collection").select(label)
            self.run_app()
            self.assertEqual(len(self.app.selectbox(key="primer_lesson").options), count)
            self.assertIn("Book reference: printed pages", self.text())
        self.app.selectbox(key="primer_lesson").select("app-draw-11")
        self.run_app()
        self.assertTrue(self.app.button(key="primer_next_lesson").disabled)
        self.app.button(key="example_next_app-draw-11_0").click()
        self.run_app()
        self.assertIn("1. Ne3", self.text())
        self.button("Ne3").click()
        self.run_app()
        store = LearningProgress(self.config.sqlite_path.parent / "primer.sqlite3", "Lawrence-Zhou")
        self.assertIn("board", store.passed("app-draw-11"))
        self.assertEqual(store.last_lesson(), "app-draw-11")
        self.app.button(key="primer_previous_lesson").click()
        self.run_app()
        self.assertEqual(self.app.selectbox(key="primer_lesson").value, "app-draw-10")
        self.app.button(key="primer_next_lesson").click()
        self.run_app()
        self.assertEqual(self.app.selectbox(key="primer_lesson").value, "app-draw-11")
        self.app.radio(key="main_section").set_value("Your games")
        self.run_app()
        self.button("Fetch Games").click()
        self.run_app()
        self.assertTrue(self.analysis_calls)
        self.app.radio(key="main_section").set_value("The Soviet Chess Primer")
        self.run_app()
        self.assertEqual(self.app.selectbox(key="primer_lesson").value, "app-draw-11")

    def test_part_two_bookmark_replay_practice_and_chapter_navigation(self):
        from core.primer_progress import LearningProgress
        self.config = replace(self.config, review_only=True, chess_com_username="Lawrence-Zhou")
        store = LearningProgress(self.config.sqlite_path.parent / "primer.sqlite3", "Lawrence-Zhou")
        store.bookmark("ch10-symmetry")
        self.run_app()
        self.app.radio(key="main_section").set_value("The Soviet Chess Primer")
        self.run_app()
        self.assertEqual(self.app.selectbox(key="primer_chapter").value, 10)
        self.assertEqual(self.app.selectbox(key="primer_lesson").value, "ch10-symmetry")
        self.app.button(key="example_next_ch10-symmetry_0").click()
        self.run_app()
        self.assertIn("immediately copies the capture", self.text())
        self.button("d6").click()
        self.run_app()
        self.assertIn("board", store.passed("ch10-symmetry"))
        for chapter in (8, 9, 10):
            self.app.selectbox(key="primer_chapter").select(chapter)
            self.run_app()
            self.assertEqual(set(self.app.selectbox(key="primer_lesson").options), {item.title for item in lessons() if item.chapter == chapter})
            self.assertIn("Book reference: printed pages", self.text())
            self.assertEqual([tab.label for tab in self.app.tabs], ["Learn", "Worked examples", "Practice", "Review"])
        self.assertIn("board", store.passed("ch10-symmetry"))

    def test_primer_guide_shows_book_pages_replays_examples_and_saves_checked_answers(self):
        self.config = replace(self.config, review_only=True, chess_com_username="Lawrence-Zhou")
        guide = {
            "pages": (13, 14), "goals": ("Keep the king safe.",),
            "sections": ({"title": "Why safety matters", "body": "A king cannot move to an attacked square."},),
            "examples": ({"title": "Develop with a purpose", "fen": chess.STARTING_FEN, "moves": ("e4", "e5", "Nf3"), "notes": ("Start.", "White takes space.", "Black contests the center.", "The knight attacks e5.")},),
            "pitfalls": ("Checking is not always checkmate.",),
            "checks": ({"id": "king-safety", "prompt": "May your king move into check?", "options": (
                {"text": "Yes", "correct": False, "explanation": "Moving into check is illegal."},
                {"text": "No", "correct": True, "explanation": "The king must always stay safe."},
            )},), "recap": ("Examine enemy attacks before moving your king.",),
        }
        self.stack.enter_context(patch("core.primer_ui.guide_for", return_value=guide))
        self.run_app()
        self.app.radio(key="main_section").set_value("The Soviet Chess Primer")
        self.run_app()
        self.assertIn("Book reference: printed pages 13–14", self.text())
        self.assertIn("Why safety matters", self.text())
        self.assertFalse(any(slider.label == "Move through the example" for slider in self.app.slider))
        self.assertTrue(self.app.button(key="example_previous_board-setup_0").disabled)
        for _ in range(3):
            self.app.button(key="example_next_board-setup_0").click()
            self.run_app()
        self.assertIn("The knight attacks e5.", self.text())
        self.assertTrue(self.app.button(key="example_next_board-setup_0").disabled)
        self.app.button(key="example_previous_board-setup_0").click()
        self.run_app()
        self.assertIn("Black contests the center.", self.text())
        self.assertFalse(self.app.button(key="example_next_board-setup_0").disabled)
        self.app.radio(key="concept_choice_board-setup_king-safety").set_value(1)
        self.run_app()
        self.app.button(key="concept_check_board-setup_king-safety").click()
        self.run_app()
        self.assertIn("The king must always stay safe", self.text())
        self.app.radio(key="concept_choice_board-setup_king-safety").set_value(0)
        self.run_app()
        self.assertNotIn("The king must always stay safe", self.text())
        self.assertIn("Check your changed answer", self.text())
        from core.primer_progress import LearningProgress
        saved = LearningProgress(self.config.sqlite_path.parent / "primer.sqlite3", "Lawrence-Zhou")
        self.assertIn("concept:king-safety", saved.passed("board-setup"))

    def test_coaching_uses_current_rating_instead_of_historical_game_rating(self):
        self.config = replace(self.config, openai_api_key="test-key", user_rating=564)
        self.stack.enter_context(patch("openai.OpenAI", return_value=MagicMock()))
        review = self.stack.enter_context(patch("core.coach.ChessCoach.review_blunder", return_value="Beginner feedback."))
        self.fetch_games()
        self.choose()
        self.assertEqual(review.call_args.kwargs["user_rating"], 564)
        self.app.number_input(key="user_rating").set_value(580)
        self.run_app()
        self.assertEqual(review.call_args.kwargs["user_rating"], 580)

    def test_primer_switching_player_restores_their_place_and_keeps_progress_separate(self):
        from core.primer import lessons
        from core.primer_progress import LearningProgress
        self.config = replace(self.config, review_only=True, chess_com_username="Alice")
        path = self.config.sqlite_path.parent / "primer.sqlite3"
        alice = LearningProgress(path, "Alice")
        bob = LearningProgress(path, "Bob")
        alice.bookmark("rook")
        bob.bookmark("queen-mates")
        self.run_app()
        self.app.radio(key="main_section").set_value("The Soviet Chess Primer")
        self.run_app()
        self.assertEqual(self.app.selectbox(key="primer_lesson").value, "rook")
        rook = next(item for item in lessons() if item.id == "rook")
        self.button(next(choice.san for choice in rook.choices if choice.correct)).click()
        self.run_app()
        self.assertTrue(self.app.session_state["primer_board_fen"])
        self.app.text_input(key="username").set_value(" Bob ")
        self.button("Fetch Games").click()
        self.run_app()
        self.assertEqual(self.app.selectbox(key="primer_lesson").value, "queen-mates")
        self.assertEqual(self.app.selectbox(key="primer_chapter").value, 2)
        self.assertIsNone(self.app.session_state["primer_board_fen"])
        self.button("Qg7#").click()
        self.run_app()
        self.assertIn("board", bob.passed("queen-mates"))
        self.assertNotIn("board", alice.passed("queen-mates"))
        self.app.text_input(key="username").set_value("Alice")
        self.button("Fetch Games").click()
        self.run_app()
        self.assertEqual(self.app.selectbox(key="primer_lesson").value, "rook")


if __name__ == "__main__":
    unittest.main()
