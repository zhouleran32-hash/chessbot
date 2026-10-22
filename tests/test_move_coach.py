"""Position-grounded coaching for every move, without model or retrieval calls."""

import unittest

import chess

from core.coach import ChessCoach


def move_row(previous=(), played="e4", best=None, key="best", **updates):
    board = chess.Board()
    for san in previous:
        board.push_san(san)
    row = {
        "fen_before": board.fen(), "played_move": played,
        "best_move": best or played, "eval_drop": 0.0, "depth": 14,
        "classification": {"key": key, "label": key.title(), "reason": "Keeps the position's chances."},
        "best_pv": [], "reply_pv": [],
    }
    row.update(updates)
    return row


class MoveCoachTests(unittest.TestCase):
    def test_alternative_explains_target_reply_followup_and_bounded_result(self):
        fen = "4k3/8/8/2n5/8/8/1P6/4K3 w - - 0 6"
        row = move_row(played="b3", best="b4", key="mistake", fen_before=fen,
                       best_pv=["b4", "Nb7", "b5", "Nd6"], reply_pv=["Nd3+"])
        review = ChessCoach.review_move_locally(row, 591)
        self.assertIn("attacks the knight on c5", review)
        self.assertIn("6... Nb7", review)
        self.assertIn("7. b5", review)
        self.assertIn("Opponent", review)
        self.assertIn("material balance is unchanged", review.lower())

    def test_quick_review_uses_supplied_analysis_for_a_detailed_alternative(self):
        fen = "4k3/8/8/2n5/8/8/1P6/4K3 w - - 0 6"
        review = ChessCoach.review_blunder_locally(
            fen, "b3", "b4", user_rating=591,
            analysis={"best_pv": ["b4", "Nb7", "b5", "Nd6"], "reply_pv": ["Nd3+"]},
        )
        self.assertIn("**A better move to explore**", review)
        self.assertIn("attacks the knight on c5", review)
        self.assertIn("6... Nb7", review)
        self.assertIn("7. b5", review)
        self.assertIn("material balance is unchanged", review.lower())
        self.assertLess(review.index("**A better move to explore**"), review.index("**After your move**"))

    def test_pinned_moving_piece_does_not_get_an_impossible_capture_target(self):
        fen = "k3r3/8/8/8/8/5q2/4R3/4K3 w - - 0 20"
        review = ChessCoach.review_move_locally(move_row(
            played="Re3", best="Kd1", key="mistake", fen_before=fen,
        ))
        self.assertNotIn("attacks the queen on f3", review)

    def test_best_opening_move_explains_its_purpose_and_opponents_legal_reply(self):
        review = ChessCoach.review_move_locally(move_row(
            best_pv=["e4", "e5", "Nf3"], reply_pv=["e5", "Nf3"],
        ), user_rating=591)
        for heading in ("What your move does", "Why this assessment", "What to explore", "Before your next move"):
            self.assertIn(f"**{heading}**", review)
        self.assertIn("pawn from e2 to e4", review)
        self.assertIn("center", review)
        self.assertIn("pawn from e7 to e5", review)
        self.assertIn("e5", review)
        self.assertIn("limited", review.lower())
        self.assertNotIn("mistake", review.lower())
        self.assertNotIn("better", review.lower())
        self.assertNotIn("centipawn", review.lower())

    def test_good_alternative_gets_positive_feedback_without_a_mistake_template(self):
        row = move_row(best="d4", key="good", best_pv=["d4", "d5"], reply_pv=["e5"])
        row["classification"]["reason"] = "Preserves most of your chances."
        review = ChessCoach.review_move_locally(row, 591)
        self.assertIn("Preserves most of your chances.", review)
        self.assertIn("Good", review)
        self.assertNotIn("mistake", review.lower())
        self.assertNotIn("better", review.lower())

    def test_hanging_queen_is_explained_with_the_actual_capture_and_alternative(self):
        row = move_row(("e4", "e5", "Qh5", "Nc6"), "Qxe5+", "Bc4", "blunder",
                       best_pv=["Bc4", "Nf6"], reply_pv=["Nxe5"], eval_drop=8.7)
        review = ChessCoach.review_move_locally(row, 591)
        self.assertIn("queen from h5 to e5", review)
        self.assertIn("captures the pawn on e5", review)
        self.assertIn("Nxe5", review)
        self.assertIn("taking your queen", review)
        self.assertIn("bishop from f1 to c4", review)
        self.assertIn("Compare", review)
        self.assertNotIn("forced continuation", review)

    def test_delivering_checkmate_is_celebrated_without_an_opponent_reply(self):
        review = ChessCoach.review_move_locally(move_row(
            ("f3", "e5", "g4"), "Qh4#", best_pv=["Qh4#"],
            reply_pv=["Ke2"],
        ), 591)
        self.assertIn("queen from d8 to h4", review)
        self.assertIn("checkmate", review.lower())
        self.assertNotIn("Ke2", review)
        self.assertNotIn("mistake", review.lower())
        self.assertNotIn("better", review.lower())

    def test_promotion_explains_which_piece_the_pawn_becomes(self):
        row = move_row(played="a8=Q+", fen_before="7k/P7/8/8/8/8/8/7K w - - 0 40")
        review = ChessCoach.review_move_locally(row, 591)
        self.assertIn("pawn from a7 to a8", review)
        self.assertIn("promotes to a queen", review)
        self.assertIn("check", review.lower())

    def test_castling_explains_both_the_king_and_rook_moves(self):
        review = ChessCoach.review_move_locally(move_row(
            ("e4", "e5", "Nf3", "Nc6", "Bc4", "Nf6"), "O-O",
        ), 591)
        self.assertIn("king from e1 to g1", review)
        self.assertIn("rook from h1 to f1", review)
        self.assertIn("castl", review.lower())

    def test_black_move_and_white_reply_are_described_from_the_correct_positions(self):
        review = ChessCoach.review_move_locally(move_row(
            ("e4",), "c5", best_pv=["c5", "Nf3"], reply_pv=["Nf3"],
        ), 591)
        self.assertIn("pawn from c7 to c5", review)
        self.assertIn("knight from g1 to f3", review)

    def test_development_and_attacked_piece_are_supported_by_the_board(self):
        review = ChessCoach.review_move_locally(move_row(
            ("e4", "e5", "Nf3", "Nc6"), "Bb5",
        ), 591)
        self.assertIn("bishop from f1 to b5", review)
        self.assertIn("off the back rank", review)
        self.assertIn("attacks the knight on c6", review)

    def test_en_passant_names_the_captured_pawns_actual_square(self):
        review = ChessCoach.review_move_locally(move_row(
            ("e4", "a6", "e5", "d5"), "exd6",
        ), 591)
        self.assertIn("pawn from e5 to d6", review)
        self.assertIn("captures the pawn on d5", review)
        self.assertIn("en passant", review)

    def test_bad_pv_entries_and_every_move_after_them_are_not_quoted(self):
        review = ChessCoach.review_move_locally(move_row(
            best_pv=["e4", "Not_a_move", "Qh4#"], reply_pv=["Nonsense", "Nf3"],
        ), 591)
        for invalid in ("Not_a_move", "Qh4#", "Nonsense", "Nf3"):
            self.assertNotIn(invalid, review)

    def test_best_line_must_begin_with_the_advertised_best_move(self):
        review = ChessCoach.review_move_locally(move_row(
            best_pv=["d4", "d5"], reply_pv=["e5", "Illegal", "Nf3"],
        ), 591)
        self.assertNotIn("d4", review)
        self.assertNotIn("**d5**", review)
        self.assertNotIn("Illegal", review)
        self.assertNotIn("Nf3", review)
        self.assertIn("e5", review)

    def test_allowing_mate_in_one_names_the_verified_mating_reply(self):
        review = ChessCoach.review_move_locally(move_row(
            ("f3", "e5"), "g4", "Nc3", "blunder", reply_pv=["Qh4#"],
        ), 591)
        self.assertIn("checkmate next with Qh4#", review)
        self.assertIn("knight from b1 to c3", review)

    def test_same_move_as_engine_never_gets_a_negative_comparison(self):
        row = move_row(key="mistake")
        row["classification"]["reason"] = "A mistake loses chances."
        review = ChessCoach.review_move_locally(row, 591)
        self.assertNotIn("mistake", review.lower())
        self.assertNotIn("better", review.lower())

    def test_invalid_required_inputs_raise_a_clear_value_error(self):
        for rating in (True, -1, 591.5):
            with self.subTest(rating=rating), self.assertRaises(ValueError):
                ChessCoach.review_move_locally(move_row(), rating)
        for row in (None, {}, move_row(fen_before="invalid"), move_row(played_move="Qh5")):
            with self.subTest(row=row), self.assertRaises(ValueError):
                ChessCoach.review_move_locally(row, 591)


if __name__ == "__main__":
    unittest.main()
