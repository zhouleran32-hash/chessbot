"""Exercise goals and legal moves, including answers omitted from preset buttons."""

from dataclasses import replace
import unittest

import chess

from core.primer import Choice, Lesson, Step, feedback_for_played_move, grade, san_for_squares


def exercise(fen=chess.STARTING_FEN, choices=None, **changes):
    lesson = Lesson(
        id="fixture", chapter=1, title="Fixture", explanation="A controlled exercise.",
        steps=(Step(fen, "A position."),), quiz_fen=fen, prompt="Find the requested move.",
        choices=choices or (Choice("e4", True, "Move the king pawn."),), orientation="white",
    )
    return replace(lesson, **changes)


class PrimerGradingTests(unittest.TestCase):
    def test_notation_suffix_does_not_change_the_identity_of_a_legal_answer(self):
        lesson = exercise(choices=(Choice("e4+", True, "The pawn advances."),))
        self.assertTrue(grade(lesson, "e4").correct)

    def test_any_checkmate_satisfies_a_checkmate_exercise(self):
        fen = "7k/8/5KQ1/8/8/8/8/8 w - - 0 1"
        lesson = exercise(fen, (Choice("Qh5+", False, "The king can escape."),), objective="checkmate")
        self.assertTrue(feedback_for_played_move(lesson, "Qg7#").correct)
        self.assertFalse(feedback_for_played_move(lesson, "Qh5+").correct)

    def test_illegal_move_is_not_presented_as_an_acceptable_legal_try(self):
        for move in ("e5", "--"):
            with self.subTest(move=move):
                result = feedback_for_played_move(exercise(), move)
                self.assertFalse(result.correct)
                self.assertIn("not legal", result.explanation)

    def test_mate_threat_accepts_both_queen_routes(self):
        board = chess.Board()
        for san in ("e4", "e5", "Bc4", "Nc6"):
            board.push_san(san)
        lesson = exercise(board.fen(), (Choice("Qh5", True, "Threatens the f7 pawn."),), objective="mate_threat")
        self.assertTrue(feedback_for_played_move(lesson, "Qf3").correct)
        self.assertFalse(feedback_for_played_move(lesson, "a3").correct)

    def test_invalid_promotion_choice_returns_no_move(self):
        fen = "k7/4P3/8/8/8/8/8/7K w - - 0 1"
        self.assertIsNone(san_for_squares(fen, "e7", "e8", promotion="not-a-piece"))

    def test_stalemate_cannot_be_graded_as_a_future_mate_threat(self):
        lesson = exercise("k7/8/K7/2Q5/8/8/8/8 w - - 0 1", (Choice("Qb6", False, "This is stalemate."),), objective="mate_threat")
        self.assertFalse(feedback_for_played_move(lesson, "Qb6").correct)


if __name__ == "__main__":
    unittest.main()
