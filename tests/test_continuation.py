"""Legal, position-grounded descriptions of analyzed sample continuations."""

import unittest

import chess

from core.continuation import continuation_steps, explain_recommendation


class ContinuationTests(unittest.TestCase):
    def test_pawn_attack_names_the_knight_and_each_side_gets_a_purpose(self):
        fen = "4k3/8/8/2n5/8/8/1P6/4K3 w - - 0 6"
        steps = continuation_steps(fen, ["b4", "Nb7", "b5", "Nd6"], expected_first="b4")
        self.assertEqual([step["label"] for step in steps], ["6. b4", "6... Nb7", "7. b5", "7... Nd6"])
        self.assertEqual([step["mover"] for step in steps], ["you", "opponent", "you", "opponent"])
        self.assertIn("attacks the knight on c5", steps[0]["description"])
        self.assertIn("pawn", steps[1]["description"])
        self.assertIn("attack", steps[1]["description"])
        text = explain_recommendation(fen, "b4", ["b4", "Nb7", "b5", "Nd6"])
        outcome = text.split("**Position reached**", 1)[1]
        self.assertIn("knight on d6", outcome)
        self.assertIn("attacks the pawn on b5", outcome)
        self.assertEqual(steps[0]["uci"], "b2b4")
        self.assertEqual(steps[0]["fen_before"], fen)
        self.assertEqual(steps[1]["fen_before"], steps[0]["fen_after"])

    def test_captures_and_recapture_are_replayed_before_summarizing_material(self):
        board = chess.Board()
        board.push_san("e4")
        board.push_san("d5")
        steps = continuation_steps(board.fen(), ["exd5", "Qxd5", "Nc3"])
        self.assertIn("captures the pawn on d5", steps[0]["description"])
        self.assertIn("recaptures", steps[1]["description"])
        self.assertIn("queen on d5", steps[2]["description"])
        text = explain_recommendation(board.fen(), "exd5", ["exd5", "Qxd5", "Nc3"])
        self.assertIn("material balance is unchanged", text.lower())
        outcome = text.split("**Position reached**", 1)[1]
        self.assertIn("knight on c3", outcome)
        self.assertIn("queen on d5", outcome)
        self.assertIn("sample", text.lower())
        self.assertNotIn("wins a", text.lower())

    def test_moving_a_blocker_explains_the_new_attack_by_the_rook(self):
        fen = "q6k/8/8/8/8/8/B6K/R7 w - - 0 20"
        steps = continuation_steps(fen, ["Bb3"])
        self.assertIn("rook on a1", steps[0]["description"])
        self.assertIn("queen on a8", steps[0]["description"])
        self.assertIn("opens", steps[0]["description"])

    def test_black_start_has_correct_numbering_and_player_perspective(self):
        board = chess.Board()
        board.push_san("e4")
        steps = continuation_steps(board.fen(), ["c5", "Nf3", "d6"])
        self.assertEqual([step["label"] for step in steps], ["1... c5", "2. Nf3", "2... d6"])
        self.assertEqual([step["mover"] for step in steps], ["you", "opponent", "you"])
        text = explain_recommendation(board.fen(), "c5", ["c5", "Nf3", "d6"])
        self.assertIn("Opponent", text)
        self.assertIn("knight from g1 to f3", text)

    def test_bad_entries_truncate_the_line_and_wrong_first_move_is_rejected(self):
        steps = continuation_steps(chess.STARTING_FEN, ["e4", "Illegal", "Nf3"])
        self.assertEqual([step["san"] for step in steps], ["e4"])
        self.assertEqual(continuation_steps(chess.STARTING_FEN, ["d4", "d5"], expected_first="e4"), [])
        self.assertEqual(continuation_steps(chess.STARTING_FEN, "e4 e5"), [])
        self.assertEqual(len(continuation_steps(chess.STARTING_FEN, ["e4", "e5", "Nf3"], max_plies=2)), 2)
        text = explain_recommendation(chess.STARTING_FEN, "e4", ["d4", "d5"])
        self.assertNotIn("1... d5", text)
        self.assertIn("No legal", text)

    def test_terminal_positions_stop_the_line_and_only_claim_verified_results(self):
        fen = "7k/5Q2/6K1/8/8/8/8/8 w - - 0 40"
        mate = explain_recommendation(fen, "Qg7#", ["Qg7#", "Kh7"])
        self.assertIn("checkmate", mate.lower())
        self.assertNotIn("Kh7", mate)
        stale = explain_recommendation(fen, "Qe6", ["Qe6", "Kh7"])
        self.assertIn("stalemate", stale.lower())
        self.assertNotIn("Kh7", stale)

    def test_pinned_knights_pseudo_attack_is_not_a_capture_or_free_material_claim(self):
        fen = "4k3/4n3/8/8/8/5Q2/8/4R2K w - - 0 20"
        text = explain_recommendation(fen, "Qd5", ["Qd5"])
        self.assertNotIn("Nxd5", text)
        self.assertNotIn("hanging", text.lower())
        self.assertNotIn("free", text.lower())
        self.assertNotIn("wins", text.lower())

    def test_endpoint_has_no_unverified_winning_evaluation(self):
        text = explain_recommendation(chess.STARTING_FEN, "e4", ["e4", "e5", "Nf3"])
        self.assertIn("position", text.lower())
        self.assertIn("material balance is unchanged", text.lower())
        for unsupported in ("winning position", "decisive advantage", "forced win", "will win", "wins a pawn"):
            self.assertNotIn(unsupported, text.lower())

    def test_material_change_counts_the_capture_and_not_a_threatened_future_capture(self):
        board = chess.Board()
        board.push_san("e4")
        board.push_san("d5")
        text = explain_recommendation(board.fen(), "exd5", ["exd5"])
        self.assertIn("1 point", text)
        self.assertNotIn("9 points", text)

    def test_a_quiet_move_onto_the_previous_square_is_not_called_a_recapture(self):
        board = chess.Board()
        board.push_san("e4")
        steps = continuation_steps(board.fen(), ["d5", "exd5"])
        self.assertIn("captures the pawn", steps[1]["description"])
        self.assertNotIn("recaptures", steps[1]["description"])

    def test_automatic_move_count_draw_is_not_described_as_still_in_play(self):
        fen = "4k3/8/8/8/8/8/8/R3K3 w - - 149 90"
        text = explain_recommendation(fen, "Ra2", ["Ra2", "Kd7"])
        self.assertIn("draw", text.lower())
        self.assertNotIn("still in play", text)
        self.assertNotIn("Kd7", text)

    def test_available_en_passant_at_endpoint_does_not_name_an_empty_square_as_a_piece(self):
        fen = "4k3/8/8/8/4p3/8/3P4/4K3 w - - 0 20"
        text = explain_recommendation(fen, "d4", ["d4"])
        self.assertIn("material balance is unchanged", text.lower())
        self.assertIn("opponent moves next", text.lower())
        self.assertNotIn("pawn on d3", text)
        replay = continuation_steps(fen, ["d4", "exd3"])
        self.assertIn("captures the pawn on d4 (en passant)", replay[1]["description"])


if __name__ == "__main__":
    unittest.main()
