"""Analyzer behavior with real chess parsing/SVG and a controlled engine boundary."""

import os
import sys
import unittest
from unittest.mock import MagicMock, patch
from xml.etree import ElementTree

import chess
import chess.engine

from core.analyzer import (
    EngineUnavailableError,
    GameAnalysisError,
    GameAnalyzer,
    InvalidPGNError,
)


def engine_info(score, turn, best_move):
    return {
        "score": chess.engine.PovScore(score, turn),
        "pv": [chess.Move.from_uci(best_move)],
        "depth": 10,
    }


class AnalyzerTests(unittest.TestCase):
    def setUp(self):
        self.engine = MagicMock(spec=chess.engine.SimpleEngine)
        factory = patch("core.analyzer.chess.engine.SimpleEngine.popen_uci", return_value=self.engine)
        self.factory = factory.start()
        self.addCleanup(factory.stop)

    def analyzer(self, **kwargs):
        analyzer = GameAnalyzer(sys.executable, **kwargs)
        self.addCleanup(analyzer.close)
        return analyzer

    def test_white_blunder_uses_fixed_perspective_and_renders_both_arrows(self):
        self.engine.analyse.side_effect = [
            engine_info(chess.engine.Cp(80), chess.WHITE, "d2d4"),
            engine_info(chess.engine.Cp(150), chess.BLACK, "e7e5"),
            engine_info(chess.engine.Cp(25), chess.WHITE, "g1f3"),
            engine_info(chess.engine.Cp(0), chess.BLACK, "b8c6"),
        ]
        blunders = self.analyzer().analyze_game("1. e4 e5 2. Nf3 *", "white")
        self.assertEqual(len(blunders), 1)
        blunder = blunders[0]
        self.assertEqual(set(blunder), {
            "move_number", "fen_before", "played_move", "best_move", "eval_drop", "board_svg",
        })
        self.assertEqual(blunder["move_number"], 1)
        self.assertEqual(blunder["fen_before"], chess.STARTING_FEN)
        self.assertEqual(blunder["played_move"], "e4")
        self.assertEqual(blunder["best_move"], "d4")
        self.assertEqual(blunder["eval_drop"], 2.3)
        self.assertIsInstance(blunder["eval_drop"], float)
        svg = ElementTree.fromstring(blunder["board_svg"])
        self.assertEqual(svg.tag, "{http://www.w3.org/2000/svg}svg")
        colors = {element.get("fill") for element in svg.iter()}
        self.assertIn("#ff0000", colors)
        self.assertIn("#00aa00", colors)
        self.assertEqual(self.engine.analyse.call_count, 4)

    def test_progress_reports_every_replayed_ply_including_opponents_moves(self):
        self.engine.analyse.side_effect = [
            engine_info(chess.engine.Cp(0), chess.WHITE, "d2d4"),
            engine_info(chess.engine.Cp(0), chess.BLACK, "e7e5"),
            engine_info(chess.engine.Cp(0), chess.WHITE, "g1f3"),
            engine_info(chess.engine.Cp(0), chess.BLACK, "b8c6"),
        ]
        updates = []
        self.analyzer().analyze_game(
            "1. e4 e5 2. Nf3 *", "white",
            progress_callback=lambda done, total: updates.append((done, total)),
        )
        self.assertEqual(updates, [(0, 3), (1, 3), (2, 3), (3, 3)])

    def test_black_blunder_uses_black_perspective(self):
        self.engine.analyse.side_effect = [
            engine_info(chess.engine.Cp(30), chess.WHITE, "c7c5"),
            engine_info(chess.engine.Cp(-250), chess.BLACK, "g1f3"),
        ]
        blunder = self.analyzer().analyze_game("1. e4 e5 *", " BLACK ")[0]
        self.assertEqual(blunder["move_number"], 1)
        self.assertEqual(blunder["played_move"], "e5")
        self.assertEqual(blunder["best_move"], "c5")
        self.assertEqual(blunder["eval_drop"], 2.2)
        self.assertEqual(
            blunder["fen_before"],
            "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1",
        )

    def test_threshold_is_strictly_greater_and_reports_pawns(self):
        for after_cp, expected in [(-150, []), (-151, [1.51]), (100, [])]:
            with self.subTest(after_cp=after_cp):
                self.engine.analyse.side_effect = [
                    engine_info(chess.engine.Cp(0), chess.WHITE, "d2d4"),
                    engine_info(chess.engine.Cp(after_cp), chess.WHITE, "e7e5"),
                ]
                result = self.analyzer().analyze_game("1. e4 *", "white", eval_threshold=150)
                self.assertEqual([item["eval_drop"] for item in result], expected)

    def test_mate_scores_are_converted_from_players_perspective(self):
        self.engine.analyse.side_effect = [
            engine_info(chess.engine.Cp(0), chess.WHITE, "d2d4"),
            engine_info(chess.engine.Mate(1), chess.BLACK, "e7e5"),
        ]
        result = self.analyzer().analyze_game("1. e4 *", "white")
        self.assertEqual(result[0]["eval_drop"], 999.99)

    def test_stalemate_after_move_is_scored_as_zero_without_an_engine_call(self):
        pgn = '[SetUp "1"]\n[FEN "7k/5K2/8/5Q2/8/8/8/8 w - - 0 42"]\n\n42. Qg6 1/2-1/2'
        self.engine.analyse.return_value = engine_info(chess.engine.Cp(900), chess.WHITE, "f5h5")
        result = self.analyzer().analyze_game(pgn, "white")
        self.assertEqual(result[0]["move_number"], 42)
        self.assertEqual(result[0]["eval_drop"], 9.0)
        self.assertEqual(result[0]["best_move"], "Qh5#")
        self.assertEqual(self.engine.analyse.call_count, 1)

    def test_delivering_checkmate_is_not_a_blunder(self):
        pgn = '[SetUp "1"]\n[FEN "rnbqkbnr/pppp1ppp/8/4p3/6P1/5P2/PPPPP2P/RNBQKBNR b KQkq - 0 2"]\n\n2... Qh4# 0-1'
        self.engine.analyse.return_value = engine_info(chess.engine.Mate(1), chess.BLACK, "d8h4")
        self.assertEqual(self.analyzer().analyze_game(pgn, "black"), [])
        self.assertEqual(self.engine.analyse.call_count, 1)

    def test_promotion_san_is_calculated_before_the_board_changes(self):
        pgn = '[SetUp "1"]\n[FEN "7k/P7/8/8/8/8/8/7K w - - 0 1"]\n\n1. a8=N *'
        self.engine.analyse.return_value = engine_info(chess.engine.Cp(900), chess.WHITE, "a7a8q")
        result = self.analyzer().analyze_game(pgn, "white")
        self.assertEqual(result[0]["played_move"], "a8=N")
        self.assertEqual(result[0]["best_move"], "a8=Q+")

    def test_depth_only_and_combined_limits_are_passed_to_engine(self):
        for time_limit, depth in [(None, 12), (0.2, 8), (0.1, None)]:
            with self.subTest(time_limit=time_limit, depth=depth):
                self.engine.analyse.side_effect = [
                    engine_info(chess.engine.Cp(0), chess.WHITE, "e2e4"),
                    engine_info(chess.engine.Cp(0), chess.BLACK, "e7e5"),
                ]
                self.analyzer(time_limit=time_limit, depth=depth).analyze_game("1. e4 *", "white")
                limit = self.engine.analyse.call_args.args[1]
                self.assertEqual((limit.time, limit.depth), (time_limit, depth))

    def test_opponents_moves_are_replayed_without_analysis(self):
        pgn = '[SetUp "1"]\n[FEN "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1"]\n\n1... e5 *'
        self.assertEqual(self.analyzer().analyze_game(pgn, "white"), [])
        self.engine.analyse.assert_not_called()

    def test_invalid_color_or_threshold_is_rejected(self):
        analyzer = self.analyzer()
        for color in ("red", "", None):
            with self.subTest(color=color), self.assertRaises(ValueError):
                analyzer.analyze_game("1. e4 *", color)
        for threshold in (-1, 1.5, True):
            with self.subTest(threshold=threshold), self.assertRaises(ValueError):
                analyzer.analyze_game("1. e4 *", "white", threshold)
        self.engine.analyse.assert_not_called()

    def test_empty_or_non_game_pgn_is_rejected(self):
        analyzer = self.analyzer()
        for pgn in ("", "not a chess game", '[Event "No moves"]\n\n*'):
            with self.subTest(pgn=pgn), self.assertRaises(InvalidPGNError):
                analyzer.analyze_game(pgn, "white")
        self.engine.analyse.assert_not_called()

    def test_illegal_moves_are_rejected_instead_of_analyzing_a_truncated_game(self):
        with self.assertLogs("chess.pgn", level="ERROR"):
            with self.assertRaises(InvalidPGNError):
                self.analyzer().analyze_game("1. e4 e5 2. Bh6 *", "white")
        self.engine.analyse.assert_not_called()

    def test_null_moves_are_rejected(self):
        with self.assertRaises(InvalidPGNError):
            self.analyzer().analyze_game("1. -- *", "white")
        self.engine.analyse.assert_not_called()

    def test_engine_failure_raises_clear_error_without_switching_to_mock_midgame(self):
        self.engine.analyse.side_effect = chess.engine.EngineTerminatedError("engine exited")
        analyzer = self.analyzer(allow_mock=True)
        with self.assertRaisesRegex(GameAnalysisError, "Stockfish"):
            analyzer.analyze_game("1. e4 *", "white")
        self.assertFalse(analyzer.is_mock)

    def test_missing_scores_or_illegal_best_moves_are_reported(self):
        cases = [
            {"pv": [chess.Move.from_uci("e2e4")]},
            {"score": chess.engine.PovScore(chess.engine.Cp(0), chess.WHITE)},
            engine_info(chess.engine.Cp(0), chess.WHITE, "e2e5"),
        ]
        for info in cases:
            with self.subTest(info=info), self.assertRaises(GameAnalysisError):
                self.engine.analyse.return_value = info
                self.analyzer().analyze_game("1. e4 *", "white")

    def test_context_manager_closes_engine_even_when_analysis_raises(self):
        analyzer = self.analyzer()
        with self.assertRaises(InvalidPGNError):
            with analyzer:
                analyzer.analyze_game("", "white")
        analyzer.close()
        self.engine.quit.assert_called_once()
        with self.assertRaisesRegex(GameAnalysisError, "closed"):
            analyzer.analyze_game("1. e4 *", "white")


class EngineSetupTests(unittest.TestCase):
    def test_missing_engine_has_download_and_environment_guidance(self):
        with patch("core.analyzer.shutil.which", return_value=None):
            with self.assertRaises(EngineUnavailableError) as caught:
                GameAnalyzer("missing-stockfish")
        self.assertIn("STOCKFISH_PATH", str(caught.exception))
        self.assertIn("https://stockfishchess.org/download/", str(caught.exception))

    def test_broken_executable_is_reported_as_an_engine_setup_error(self):
        with patch("core.analyzer.chess.engine.SimpleEngine.popen_uci", side_effect=chess.engine.EngineError("bad UCI")):
            with self.assertRaisesRegex(EngineUnavailableError, "STOCKFISH_PATH"):
                GameAnalyzer(sys.executable)

    def test_path_defaults_to_stockfish_environment_variable(self):
        engine = MagicMock(spec=chess.engine.SimpleEngine)
        with patch.dict(os.environ, {"STOCKFISH_PATH": sys.executable}):
            with patch("core.analyzer.chess.engine.SimpleEngine.popen_uci", return_value=engine) as factory:
                with GameAnalyzer() as analyzer:
                    self.assertFalse(analyzer.is_mock)
                self.assertEqual(factory.call_args.args[0], sys.executable)

    def test_invalid_limits_are_rejected_before_starting_engine(self):
        with patch("core.analyzer.chess.engine.SimpleEngine.popen_uci") as factory:
            for kwargs in (
                {"time_limit": 0}, {"time_limit": -1}, {"time_limit": float("inf")},
                {"depth": 0}, {"depth": 1.5}, {"time_limit": None, "depth": None},
            ):
                with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                    GameAnalyzer(sys.executable, **kwargs)
            factory.assert_not_called()

    def test_mock_fallback_is_labeled_deterministic_and_returns_usable_blunders(self):
        pgn = "1. e4 e5 2. Qh5 Nc6 3. Qxe5+ Nxe5 *"
        with patch("core.analyzer.shutil.which", return_value=None):
            with self.assertWarnsRegex(RuntimeWarning, "[Mm]ock"):
                analyzer = GameAnalyzer("missing-stockfish", allow_mock=True)
        with analyzer:
            self.assertTrue(analyzer.is_mock)
            first = analyzer.analyze_game(pgn, "white")
            self.assertEqual(first, analyzer.analyze_game(pgn, "white"))
            queen_blunders = [item for item in first if item["played_move"] == "Qxe5+"]
            self.assertEqual(len(queen_blunders), 1)
            self.assertGreater(queen_blunders[0]["eval_drop"], 1.5)
            board = chess.Board(queen_blunders[0]["fen_before"])
            self.assertIn(board.parse_san(queen_blunders[0]["best_move"]), board.legal_moves)
            ElementTree.fromstring(queen_blunders[0]["board_svg"])


if __name__ == "__main__":
    unittest.main()
