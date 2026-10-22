"""Complete move reviews retain engine evidence without changing blunder analysis."""

import sys
import unittest
from unittest.mock import MagicMock, patch

import chess
import chess.engine

from core.analyzer import GameAnalysisError, GameAnalyzer, InvalidPGNError


def info(score, turn, pv, depth=12):
    return {
        "score": chess.engine.PovScore(score, turn),
        "pv": [chess.Move.from_uci(move) for move in pv.split()],
        "depth": depth,
    }


class FullReviewTests(unittest.TestCase):
    def setUp(self):
        self.engine = MagicMock(spec=chess.engine.SimpleEngine)
        factory = patch("core.analyzer.chess.engine.SimpleEngine.popen_uci", return_value=self.engine)
        factory.start()
        self.addCleanup(factory.stop)
        self.analyzer = GameAnalyzer(sys.executable, time_limit=0.2, depth=10)
        self.addCleanup(self.analyzer.close)

    def test_every_player_move_has_stable_identity_and_bounded_engine_evidence(self):
        self.engine.analyse.side_effect = [
            [
                info(chess.engine.Cp(40), chess.WHITE, "d2d4 d7d5 g1f3 g8f6 c2c4 e7e6 b1c3"),
                info(chess.engine.Cp(30), chess.WHITE, "e2e4 e7e5"),
            ],
            info(chess.engine.Cp(20), chess.BLACK, "e7e5 g1f3 b8c6 f1b5 a7a6 b5a4 g8f6", depth=9),
            [info(chess.engine.Cp(25), chess.WHITE, "g1f3 b8c6")],
            info(chess.engine.Cp(-30), chess.BLACK, "b8c6"),
        ]
        updates = []
        rows = self.analyzer.review_game("1. e4 e5 2. Nf3 *", " WHITE ", progress_callback=lambda done, total: updates.append((done, total)))
        self.assertEqual([row["played_move"] for row in rows], ["e4", "Nf3"])
        self.assertEqual([row["ply"] for row in rows], [1, 3])
        self.assertEqual([row["move_number"] for row in rows], [1, 2])
        first = rows[0]
        self.assertEqual(set(first), {
            "ply", "move_number", "color", "fen_before", "fen_after", "played_move", "played_uci",
            "best_move", "best_uci", "eval_before_cp", "eval_after_cp", "eval_drop", "mate_before", "mate_after",
            "expected_before", "expected_after", "second_best_expected", "second_best_move", "best_pv", "reply_pv",
            "legal_move_count", "depth", "depth_after",
        })
        self.assertEqual((first["color"], first["played_uci"], first["best_move"], first["best_uci"]), ("white", "e2e4", "d4", "d2d4"))
        self.assertEqual(first["fen_before"], chess.STARTING_FEN)
        after = chess.Board()
        after.push_san("e4")
        self.assertEqual(first["fen_after"], after.fen())
        self.assertEqual((first["eval_before_cp"], first["eval_after_cp"], first["eval_drop"]), (40, -20, 0.6))
        self.assertEqual((first["mate_before"], first["mate_after"]), (None, None))
        self.assertAlmostEqual(first["expected_before"], chess.engine.Cp(40).wdl(model="sf16", ply=0).expectation())
        self.assertAlmostEqual(first["expected_after"], chess.engine.Cp(-20).wdl(model="sf16", ply=1).expectation())
        self.assertAlmostEqual(first["second_best_expected"], chess.engine.Cp(30).wdl(model="sf16", ply=0).expectation())
        self.assertEqual(first["second_best_move"], "e4")
        self.assertEqual(first["best_pv"], ["d4", "d5", "Nf3", "Nf6", "c4", "e6"])
        self.assertEqual(first["reply_pv"], ["e5", "Nf3", "Nc6", "Bb5", "a6", "Ba4"])
        self.assertEqual((first["legal_move_count"], first["depth"], first["depth_after"]), (20, 12, 9))
        self.assertEqual(rows[1]["eval_drop"], 0.0)
        self.assertIsNone(rows[1]["second_best_expected"])
        self.assertEqual(updates, [(0, 3), (1, 3), (2, 3), (3, 3)])
        calls = self.engine.analyse.call_args_list
        self.assertEqual(len(calls), 4)
        self.assertEqual([call.kwargs.get("multipv") for call in calls], [2, None, 2, None])
        self.assertTrue(all(call.args[1] is self.analyzer.limit for call in calls))

    def test_black_moves_use_black_perspective_on_both_sides(self):
        self.engine.analyse.side_effect = [
            [info(chess.engine.Cp(50), chess.BLACK, "c7c5")],
            info(chess.engine.Cp(100), chess.WHITE, "g1f3"),
            [info(chess.engine.Cp(-20), chess.BLACK, "b8c6")],
            info(chess.engine.Cp(10), chess.WHITE, "f1b5"),
        ]
        rows = self.analyzer.review_game("1. e4 e5 2. Nf3 Nc6 *", "black")
        self.assertEqual([row["ply"] for row in rows], [2, 4])
        self.assertEqual([row["color"] for row in rows], ["black", "black"])
        self.assertEqual((rows[0]["eval_before_cp"], rows[0]["eval_after_cp"], rows[0]["eval_drop"]), (50, -100, 1.5))
        self.assertEqual(rows[1]["eval_drop"], 0.0)
        self.assertAlmostEqual(rows[0]["expected_before"], chess.engine.Cp(50).wdl(model="sf16", ply=1).expectation())

    def test_engine_details_keep_three_scored_candidates_and_longer_legal_lines(self):
        self.engine.analyse.side_effect = [
            [info(chess.engine.Cp(40), chess.WHITE,
                  "d2d4 d7d5 g1f3 g8f6 c2c4 e7e6 b1c3 f8e7 c1f4 e8g8 e2e3 b8d7"),
             info(chess.engine.Cp(30), chess.WHITE, "e2e4 e7e5"),
             info(chess.engine.Cp(20), chess.WHITE, "g1f3 d7d5")],
            info(chess.engine.Cp(-30), chess.BLACK, "e7e5 g1f3"),
        ]
        row = self.analyzer.review_game("1. e4 *", "white", engine_details=True)[0]
        self.assertEqual([c["move"] for c in row["candidates"]], ["d4", "e4", "Nf3"])
        self.assertEqual([c["cp"] for c in row["candidates"]], [40, 30, 20])
        self.assertEqual(row["candidates"][0]["pv"],
                         ["d4", "d5", "Nf3", "Nf6", "c4", "e6", "Nc3", "Be7", "Bf4", "O-O", "e3", "Nbd7"])
        self.assertEqual(row["best_pv"], row["candidates"][0]["pv"])
        self.assertEqual(row["candidates"][2]["uci"], "g1f3")
        self.assertEqual(self.engine.analyse.call_args_list[0].kwargs["multipv"], 3)

    def test_engine_details_candidates_keep_black_perspective_and_mate_distance(self):
        self.engine.analyse.side_effect = [
            [info(chess.engine.Mate(3), chess.BLACK, "c7c5"),
             info(chess.engine.Cp(-50), chess.WHITE, "e7e5")],
            info(chess.engine.Cp(100), chess.WHITE, "g1f3"),
        ]
        row = self.analyzer.review_game("1. e4 e5 *", "black", engine_details=True)[0]
        self.assertEqual(len(row["candidates"]), 2)
        self.assertEqual(row["candidates"][0]["mate"], 3)
        self.assertEqual(row["candidates"][1]["cp"], 50)
        self.assertEqual(row["eval_after_cp"], -100)

    def test_engine_details_reject_illegal_third_candidate(self):
        self.engine.analyse.return_value = [
            info(chess.engine.Cp(40), chess.WHITE, "d2d4"),
            info(chess.engine.Cp(30), chess.WHITE, "e2e4"),
            info(chess.engine.Cp(20), chess.WHITE, "g1f3 d7d3"),
        ]
        with self.assertRaises(GameAnalysisError):
            self.analyzer.review_game("1. e4 *", "white", engine_details=True)

    def test_custom_black_start_retains_fullmove_number_and_relative_ply(self):
        pgn = '[SetUp "1"]\n[FEN "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 42"]\n\n42... e5 *'
        self.engine.analyse.side_effect = [
            [info(chess.engine.Cp(250), chess.BLACK, "e7e5")],
            info(chess.engine.Cp(0), chess.WHITE, "g1f3"),
        ]
        row = self.analyzer.review_game(pgn, "black")[0]
        self.assertEqual((row["ply"], row["move_number"], row["played_move"]), (1, 42, "e5"))
        self.assertEqual(chess.Board(row["fen_before"]).ply(), 83)
        self.assertAlmostEqual(row["expected_before"], chess.engine.Cp(250).wdl(model="sf16", ply=83).expectation())

    def test_delivering_mate_scores_terminal_position_without_engine_call(self):
        pgn = '[SetUp "1"]\n[FEN "rnbqkbnr/pppp1ppp/8/4p3/6P1/5P2/PPPPP2P/RNBQKBNR b KQkq - 0 2"]\n\n2... Qh4# 0-1'
        self.engine.analyse.return_value = [info(chess.engine.Mate(1), chess.BLACK, "d8h4")]
        row = self.analyzer.review_game(pgn, "black")[0]
        self.assertEqual((row["mate_before"], row["mate_after"]), (1, 0))
        self.assertEqual(row["eval_after_cp"], GameAnalyzer.MATE_SCORE)
        self.assertEqual(row["expected_after"], 1.0)
        self.assertEqual(row["reply_pv"], [])
        self.assertIsNone(row["depth_after"])
        self.assertEqual(row["eval_drop"], 0.0)
        self.assertEqual(self.engine.analyse.call_count, 1)

    def test_stalemate_is_a_terminal_draw(self):
        pgn = '[SetUp "1"]\n[FEN "7k/5K2/8/5Q2/8/8/8/8 w - - 0 42"]\n\n42. Qg6 1/2-1/2'
        self.engine.analyse.return_value = [info(chess.engine.Mate(1), chess.WHITE, "f5h5")]
        row = self.analyzer.review_game(pgn, "white")[0]
        self.assertEqual((row["eval_after_cp"], row["expected_after"], row["mate_after"]), (0, 0.5, None))
        self.assertEqual(row["reply_pv"], [])
        self.assertEqual(self.engine.analyse.call_count, 1)

    def test_losing_mate_retains_signed_distance_and_expectation(self):
        self.engine.analyse.side_effect = [
            [info(chess.engine.Cp(0), chess.WHITE, "d2d4")],
            info(chess.engine.Mate(2), chess.BLACK, "e7e5"),
        ]
        row = self.analyzer.review_game("1. e4 *", "white")[0]
        self.assertEqual(row["mate_after"], -2)
        self.assertEqual(row["expected_after"], 0.0)
        self.assertLess(row["eval_after_cp"], -99_000)

    def test_illegal_pv_after_first_move_is_rejected_instead_of_displayed(self):
        for invalid_pv in ("e2e4 e7e4", "e2e4 e7e5 g1f3 b8c6 f1b5 a7a6 b5e8"):
            with self.subTest(pv=invalid_pv):
                self.engine.analyse.return_value = [info(chess.engine.Cp(0), chess.WHITE, invalid_pv)]
                with self.assertRaisesRegex(GameAnalysisError, "[Vv]ariation|[Pp][Vv]"):
                    self.analyzer.review_game("1. e4 *", "white")

    def test_invalid_reply_and_second_variations_are_rejected(self):
        for before, after in (
            ([info(chess.engine.Cp(0), chess.WHITE, "e2e4")], info(chess.engine.Cp(0), chess.BLACK, "e7e5 g1g5")),
            ([info(chess.engine.Cp(0), chess.WHITE, "e2e4"), info(chess.engine.Cp(-10), chess.WHITE, "d2d4 d7d4")], None),
        ):
            with self.subTest(before=before, after=after):
                self.engine.analyse.side_effect = [before, after]
                with self.assertRaises(GameAnalysisError):
                    self.analyzer.review_game("1. e4 *", "white")

    def test_missing_engine_evidence_is_reported(self):
        for broken in ({"pv": [chess.Move.from_uci("e2e4")]}, {"score": chess.engine.PovScore(chess.engine.Cp(0), chess.WHITE)}, {}):
            with self.subTest(broken=broken):
                self.engine.analyse.return_value = [broken]
                with self.assertRaises(GameAnalysisError):
                    self.analyzer.review_game("1. e4 *", "white")

    def test_engine_failure_stays_an_error_even_if_mock_was_allowed(self):
        self.engine.analyse.side_effect = chess.engine.EngineTerminatedError("stopped")
        with self.assertRaisesRegex(GameAnalysisError, "Stockfish"):
            self.analyzer.review_game("1. e4 *", "white")
        self.assertFalse(self.analyzer.is_mock)

    def test_invalid_inputs_and_closed_analyzer_are_rejected(self):
        for color in ("", "red", None):
            with self.subTest(color=color), self.assertRaises(ValueError):
                self.analyzer.review_game("1. e4 *", color)
        for pgn in ("", "nonsense", "1. -- *"):
            with self.subTest(pgn=pgn), self.assertRaises(InvalidPGNError):
                self.analyzer.review_game(pgn, "white")
        with self.assertLogs("chess.pgn", level="ERROR"):
            with self.assertRaises(InvalidPGNError):
                self.analyzer.review_game("1. e4 e5 2. Bh6 *", "white")
        self.analyzer.close()
        with self.assertRaisesRegex(GameAnalysisError, "closed"):
            self.analyzer.review_game("1. e4 *", "white")

    def test_opponent_only_game_replays_progress_without_engine_requests(self):
        updates = []
        rows = self.analyzer.review_game("1. e4 *", "black", progress_callback=lambda done, total: updates.append((done, total)))
        self.assertEqual(rows, [])
        self.assertEqual(updates, [(0, 1), (1, 1)])
        self.engine.analyse.assert_not_called()

    def test_mock_full_review_is_deterministic_and_keeps_move_evidence_legal(self):
        self.analyzer.is_mock = True
        first = self.analyzer.review_game("1. e4 e5 2. Qh5 *", "white")
        self.assertEqual(first, self.analyzer.review_game("1. e4 e5 2. Qh5 *", "white"))
        self.assertEqual([row["played_move"] for row in first], ["e4", "Qh5"])
        for row in first:
            for fen_field, pv_field in (("fen_before", "best_pv"), ("fen_after", "reply_pv")):
                board = chess.Board(row[fen_field])
                for san in row[pv_field]:
                    board.push_san(san)
            self.assertGreaterEqual(row["expected_before"], 0.0)
            self.assertLessEqual(row["expected_before"], 1.0)
        self.engine.analyse.assert_not_called()


if __name__ == "__main__":
    unittest.main()
