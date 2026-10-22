"""The extended primer course preserves the original chapter skills."""

import unittest

import chess

from core.primer import feedback_for_played_move, grade, legal_board_moves, lessons, san_for_squares, step_svg


REQUIRED = {
    1: [
        "board-setup", "object-checkmate", "ranks-files-colors", "square-names",
        "recording-a-position", "order-of-play", "how-a-capture-works", "rook",
        "bishop", "queen", "knight", "king", "attack-defence", "exchanges",
        "pawn-move", "en-passant", "promotion", "check", "mate", "draw",
        "perpetual-check", "stalemate", "castling", "algebraic-notation",
    ],
    2: [
        "mate-on-the-edge", "queen-mates", "rook-mates", "two-rook-mates",
        "minor-piece-and-pawn-mates", "mating-method-queen", "mating-method-rook",
        "avoid-stalemate", "two-knights-draw", "drawn-material", "queening-a-pawn",
        "king-helps-the-pawn", "outside-pawn",
    ],
    3: [
        "plan", "piece-values", "values-depend-on-position", "piece-characteristics",
        "obstruction", "cutting-off", "edge-restriction", "defensive-piece", "pin",
        "time", "forcing-moves", "check-as-forcing", "dual-attack", "capture-as-forcing",
        "promotion-as-forcing", "threats", "coordination", "unprotected-king",
        "centralization", "seventh-rank", "concentration", "deflection", "attraction",
        "many-sided-threats", "open-lines", "block-lines", "breakthrough", "tempo",
        "zugzwang", "counterplan",
    ],
}


class PrimerCourseTests(unittest.TestCase):
    def test_first_three_chapters_include_every_listed_skill(self):
        found = {}
        for lesson in lessons():
            found.setdefault(lesson.chapter, []).append(lesson.id)
        self.assertEqual(set(found), set(range(1, 12)))
        for chapter, required in REQUIRED.items():
            self.assertTrue(set(required) <= set(found[chapter]))
            self.assertEqual([identifier for identifier in found[chapter] if identifier in required], required)

    def test_each_lesson_has_a_written_explanation_and_a_legal_exercise(self):
        seen = set()
        for lesson in lessons():
            self.assertNotIn(lesson.id, seen)
            seen.add(lesson.id)
            self.assertTrue(lesson.explanation.strip())
            self.assertGreaterEqual(len(lesson.steps), 2)
            self.assertGreaterEqual(sum(choice.correct for choice in lesson.choices), 1)
            quiz = chess.Board(lesson.quiz_fen)
            self.assertTrue(quiz.is_valid(), lesson.id)
            for choice in lesson.choices:
                move = quiz.parse_san(choice.san)
                self.assertIn(move, quiz.legal_moves, f"{lesson.id} {choice.san}")
                self.assertEqual(choice.san, quiz.san(move), f"{lesson.id}: misleading check/mate notation")
                self.assertTrue(choice.explanation.strip())
                self.assertEqual(feedback_for_played_move(lesson, quiz.san(move)).correct, choice.correct, f"{lesson.id}: board grading contradicts answer explanation")
            correct = next(choice for choice in lesson.choices if choice.correct)
            wrong = next(choice for choice in lesson.choices if not choice.correct)
            self.assertTrue(grade(lesson, correct.san).correct)
            self.assertFalse(grade(lesson, wrong.san).correct)
            for step in lesson.steps:
                board = chess.Board(step.fen)
                self.assertTrue(board.is_valid(), f"{lesson.id} step")
                self.assertIn("<svg", step_svg(step, lesson.orientation))
                self.assertGreaterEqual(len(step.caption.split()), 8)

    def test_a_piece_moved_on_the_board_answers_the_question(self):
        lesson = next(item for item in lessons() if item.id == "board-setup")
        self.assertEqual(san_for_squares(lesson.quiz_fen, "e2", "e4"), "e4")
        self.assertIsNone(san_for_squares(lesson.quiz_fen, "e2", "e5"))
        played = next(move for move in legal_board_moves(lesson.quiz_fen) if move["from"] == "e2" and move["to"] == "e4")
        self.assertEqual(played["san"], "e4")
        self.assertTrue(feedback_for_played_move(lesson, played["san"]).correct)
        self.assertFalse(feedback_for_played_move(lesson, "a4").correct)

        promotion = next(item for item in lessons() if item.id == "promotion")
        self.assertIsNone(san_for_squares(promotion.quiz_fen, "e7", "e8"))
        self.assertEqual(san_for_squares(promotion.quiz_fen, "e7", "e8", promotion="q"), "e8=Q+")
        queen = feedback_for_played_move(promotion, "e8=Q+")
        self.assertTrue(queen.correct)
        self.assertIn("queen", queen.explanation.lower())


if __name__ == "__main__":
    unittest.main()
