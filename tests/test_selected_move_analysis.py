"""Selected-position evidence keeps the stored recommendation and legal lines."""

import sys
import unittest
from unittest.mock import MagicMock, patch

import chess
import chess.engine

from core.analyzer import GameAnalysisError, GameAnalyzer


def info(score, turn, pv, depth=12):
    return {
        "score": chess.engine.PovScore(score, turn),
        "pv": [chess.Move.from_uci(move) for move in pv.split()],
        "depth": depth,
    }


class SelectedMoveAnalysisTests(unittest.TestCase):
    def setUp(self):
        self.engine = MagicMock(spec=chess.engine.SimpleEngine)
        factory = patch("core.analyzer.chess.engine.SimpleEngine.popen_uci", return_value=self.engine)
        factory.start()
        self.addCleanup(factory.stop)
        self.analyzer = GameAnalyzer(sys.executable, time_limit=0.5)
        self.addCleanup(self.analyzer.close)

    def test_evidence_preserves_supplied_recommendation_with_bounded_legal_lines(self):
        self.engine.analyse.side_effect = [
            info(chess.engine.Cp(40), chess.WHITE, "d2d4 d7d5 g1f3 g8f6 c2c4 e7e6 b1c3"),
            info(chess.engine.Cp(20), chess.BLACK, "e7e5 g1f3 b8c6 f1b5 a7a6 b5a4 g8f6", depth=11),
        ]
        evidence = self.analyzer.review_move(chess.STARTING_FEN, "e4", "d4")
        self.assertEqual(set(evidence), {
            "move_number", "color", "fen_before", "fen_after", "played_move", "played_uci",
            "best_move", "best_uci", "eval_before_cp", "eval_after_cp", "eval_drop", "mate_before", "mate_after",
            "expected_before", "expected_after", "best_pv", "reply_pv", "legal_move_count", "depth", "depth_after",
        })
        self.assertEqual((evidence["move_number"], evidence["color"]), (1, "white"))
        self.assertEqual(evidence["fen_before"], chess.STARTING_FEN)
        self.assertEqual(evidence["fen_after"], "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1")
        self.assertEqual((evidence["played_move"], evidence["played_uci"], evidence["best_move"], evidence["best_uci"]), ("e4", "e2e4", "d4", "d2d4"))
        self.assertEqual((evidence["eval_before_cp"], evidence["eval_after_cp"], evidence["eval_drop"]), (40, -20, 0.6))
        self.assertEqual((evidence["mate_before"], evidence["mate_after"]), (None, None))
        self.assertAlmostEqual(evidence["expected_before"], chess.engine.Cp(40).wdl(model="sf16", ply=0).expectation())
        self.assertAlmostEqual(evidence["expected_after"], chess.engine.Cp(-20).wdl(model="sf16", ply=1).expectation())
        self.assertEqual(evidence["best_pv"], ["d4", "d5", "Nf3", "Nf6", "c4", "e6"])
        self.assertEqual(evidence["reply_pv"], ["e5", "Nf3", "Nc6", "Bb5", "a6", "Ba4"])
        self.assertEqual((evidence["legal_move_count"], evidence["depth"], evidence["depth_after"]), (20, 12, 11))
        before, after = self.engine.analyse.call_args_list
        self.assertEqual(before.kwargs["root_moves"], [chess.Move.from_uci("d2d4")])
        self.assertNotIn("root_moves", after.kwargs)
        self.assertNotIn("multipv", before.kwargs)
        self.assertEqual(before.args[0].fen(), evidence["fen_before"])
        self.assertEqual(after.args[0].fen(), evidence["fen_after"])
        self.assertTrue(all(call.args[1] is self.analyzer.limit for call in (before, after)))
        self.assertEqual((self.analyzer.limit.time, self.analyzer.limit.depth), (0.5, None))

    def test_black_position_keeps_black_perspective_and_actual_move_number(self):
        fen = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 42"
        self.engine.analyse.side_effect = [
            info(chess.engine.Cp(-30), chess.WHITE, "c7c5 g1f3"),
            info(chess.engine.Cp(250), chess.WHITE, "g1f3"),
        ]
        evidence = self.analyzer.review_move(fen, "e5", "c5")
        self.assertEqual((evidence["color"], evidence["move_number"], evidence["best_pv"]), ("black", 42, ["c5", "Nf3"]))
        self.assertEqual((evidence["eval_before_cp"], evidence["eval_after_cp"], evidence["eval_drop"]), (30, -250, 2.8))
        self.assertAlmostEqual(evidence["expected_before"], chess.engine.Cp(30).wdl(model="sf16", ply=83).expectation())
        self.assertAlmostEqual(evidence["expected_after"], chess.engine.Cp(-250).wdl(model="sf16", ply=84).expectation())

    def test_better_played_score_has_zero_eval_drop(self):
        self.engine.analyse.side_effect = [
            info(chess.engine.Cp(20), chess.WHITE, "d2d4"),
            info(chess.engine.Cp(-50), chess.BLACK, "e7e5"),
        ]
        self.assertEqual(self.analyzer.review_move(chess.STARTING_FEN, "e4", "d4")["eval_drop"], 0.0)

    def test_delivering_mate_scores_after_position_without_another_engine_call(self):
        fen = "rnbqkbnr/pppp1ppp/8/4p3/6P1/5P2/PPPPP2P/RNBQKBNR b KQkq - 0 2"
        self.engine.analyse.return_value = info(chess.engine.Mate(1), chess.BLACK, "d8h4")
        evidence = self.analyzer.review_move(fen, "Qh4#", "Qh4#")
        self.assertEqual((evidence["mate_before"], evidence["mate_after"]), (1, 0))
        self.assertEqual((evidence["eval_after_cp"], evidence["expected_after"]), (100_000, 1.0))
        self.assertEqual(evidence["reply_pv"], [])
        self.assertIsNone(evidence["depth_after"])
        self.assertEqual(self.engine.analyse.call_count, 1)

    def test_stalemate_after_move_has_terminal_draw_evidence(self):
        fen = "7k/5K2/8/5Q2/8/8/8/8 w - - 0 42"
        self.engine.analyse.return_value = info(chess.engine.Mate(1), chess.WHITE, "f5h5")
        evidence = self.analyzer.review_move(fen, "Qg6", "Qh5#")
        self.assertEqual((evidence["eval_after_cp"], evidence["expected_after"], evidence["mate_after"]), (0, 0.5, None))
        self.assertEqual(evidence["reply_pv"], [])
        self.assertEqual(self.engine.analyse.call_count, 1)

    def test_losing_mate_after_move_keeps_signed_distance_for_moving_player(self):
        self.engine.analyse.side_effect = [
            info(chess.engine.Cp(0), chess.WHITE, "d2d4"),
            info(chess.engine.Mate(2), chess.BLACK, "e7e5"),
        ]
        evidence = self.analyzer.review_move(chess.STARTING_FEN, "e4", "d4")
        self.assertEqual((evidence["mate_after"], evidence["expected_after"]), (-2, 0.0))
        self.assertEqual(evidence["eval_after_cp"], -99_998)

    def test_invalid_fen_and_terminal_start_are_rejected_before_engine_io(self):
        terminal = "rnb1kbnr/pppp1ppp/8/4p3/6Pq/5P2/PPPPP2P/RNBQKBNR w KQkq - 1 3"
        for fen in (None, "", "not a fen", "8/8/8/8/8/8/8/8 w - - 0 1", terminal, "7k/8/8/8/8/8/8/7K w - - 0 1"):
            with self.subTest(fen=fen), self.assertRaises(ValueError):
                self.analyzer.review_move(fen, "e4", "d4")
        self.engine.analyse.assert_not_called()

    def test_moves_must_be_legal_san_and_null_and_coordinate_moves_are_rejected(self):
        for bad in (None, "", "--", "e5", "e2e4", "e4+", "Nf3!"):
            for field in ("played", "best"):
                with self.subTest(move=bad, field=field), self.assertRaises(ValueError):
                    self.analyzer.review_move(chess.STARTING_FEN, bad if field == "played" else "e4", bad if field == "best" else "d4")
        self.engine.analyse.assert_not_called()

    def test_engine_recommendation_cannot_replace_supplied_root_move(self):
        self.engine.analyse.return_value = info(chess.engine.Cp(40), chess.WHITE, "e2e4 e7e5")
        with self.assertRaisesRegex(GameAnalysisError, "root|recommendation"):
            self.analyzer.review_move(chess.STARTING_FEN, "e4", "d4")
        self.assertEqual(self.engine.analyse.call_count, 1)

    def test_all_pv_moves_are_validated_even_beyond_display_limit(self):
        for pv in ("d2d4 d7d4", "d2d4 d7d5 g1f3 g8f6 c2c4 e7e6 b1e8"):
            with self.subTest(pv=pv):
                self.engine.analyse.return_value = info(chess.engine.Cp(0), chess.WHITE, pv)
                with self.assertRaisesRegex(GameAnalysisError, "[Vv]ariation|PV"):
                    self.analyzer.review_move(chess.STARTING_FEN, "e4", "d4")

    def test_invalid_reply_is_rejected(self):
        self.engine.analyse.side_effect = [
            info(chess.engine.Cp(0), chess.WHITE, "d2d4"),
            info(chess.engine.Cp(0), chess.BLACK, "e7e5 g1g5"),
        ]
        with self.assertRaises(GameAnalysisError):
            self.analyzer.review_move(chess.STARTING_FEN, "e4", "d4")

    def test_missing_evidence_is_an_error(self):
        for broken in ({}, {"pv": [chess.Move.from_uci("d2d4")]}, {"score": chess.engine.PovScore(chess.engine.Cp(0), chess.WHITE)}):
            with self.subTest(broken=broken):
                self.engine.analyse.return_value = broken
                with self.assertRaises(GameAnalysisError):
                    self.analyzer.review_move(chess.STARTING_FEN, "e4", "d4")

    def test_engine_failure_does_not_switch_to_mock_and_context_closes_process(self):
        self.engine.analyse.side_effect = chess.engine.EngineTerminatedError("stopped")
        with self.assertRaisesRegex(GameAnalysisError, "Stockfish"):
            with self.analyzer:
                self.analyzer.review_move(chess.STARTING_FEN, "e4", "d4")
        self.assertFalse(self.analyzer.is_mock)
        self.engine.quit.assert_called_once()
        self.analyzer.close()
        self.engine.quit.assert_called_once()
        with self.assertRaisesRegex(GameAnalysisError, "closed"):
            self.analyzer.review_move(chess.STARTING_FEN, "e4", "d4")

    def test_mock_uses_material_search_but_preserves_recommended_root(self):
        self.analyzer.is_mock = True
        evidence = self.analyzer.review_move(chess.STARTING_FEN, "d4", "e4")
        self.assertEqual(evidence, self.analyzer.review_move(chess.STARTING_FEN, "d4", "e4"))
        self.assertEqual((evidence["best_move"], evidence["best_uci"], evidence["best_pv"]), ("e4", "e2e4", ["e4"]))
        self.assertEqual((evidence["eval_before_cp"], evidence["eval_after_cp"], evidence["eval_drop"]), (0, 0, 0.0))
        self.assertEqual((evidence["depth"], evidence["depth_after"]), (2, 2))
        for fen_field, pv_field in (("fen_before", "best_pv"), ("fen_after", "reply_pv")):
            board = chess.Board(evidence[fen_field])
            for san in evidence[pv_field]:
                board.push_san(san)
        self.engine.analyse.assert_not_called()

    def test_mock_scores_forced_recommendation_instead_of_another_material_winning_move(self):
        self.analyzer.is_mock = True
        for fen, played, recommended, color in (
            ("4k3/8/8/8/8/8/q7/R3K3 w - - 0 12", "Rxa2", "Kf1", "white"),
            ("r3k3/Q7/8/8/8/8/8/4K3 b - - 0 12", "Rxa7", "Kf8", "black"),
        ):
            with self.subTest(color=color):
                evidence = self.analyzer.review_move(fen, played, recommended)
                self.assertEqual(evidence["color"], color)
                self.assertEqual(evidence["best_pv"], [recommended])
                self.assertEqual((evidence["eval_before_cp"], evidence["eval_after_cp"]), (-900, 500))
                self.assertEqual(evidence["eval_drop"], 0.0)
        self.engine.analyse.assert_not_called()


if __name__ == "__main__":
    unittest.main()
