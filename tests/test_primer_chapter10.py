"""Chapter10 source-game mechanisms and replay/answer contracts."""
import importlib.util
import unittest
import chess
from core.primer import _lesson, grade
from core.primer_study import example_frames, validate_guide, check_concept


class ChapterTenTests(unittest.TestCase):
    def content(self):
        self.assertIsNotNone(importlib.util.find_spec('core.primer_chapter10'),
                             'Chapter10 has not been implemented')
        from core.primer_chapter10 import LESSONS
        from core.primer_guides_chapter10 import GUIDES
        return LESSONS, GUIDES

    def test_every_guide_and_practice_move_can_be_used(self):
        specs, guides = self.content()
        self.assertEqual({s['id'] for s in specs}, set(guides))
        for spec in specs:
            with self.subTest(lesson=spec['id']):
                lesson = _lesson(spec)
                g = guides[lesson.id]
                validate_guide(g, 10)
                for frame in lesson.steps:
                    self.assertTrue(chess.Board(frame.fen).is_valid())
                board = chess.Board(lesson.quiz_fen)
                for choice in lesson.choices:
                    move = board.parse_san(choice.san)
                    self.assertEqual(board.san(move), choice.san)
                    self.assertEqual(grade(lesson, choice.san).correct, choice.correct)
                for q in g['checks']:
                    for i, option in enumerate(q['options']):
                        self.assertEqual(check_concept(g, q['id'], i).correct, option['correct'])

    def test_castling_really_checks_and_attacks_the_rook(self):
        _, guides = self.content()
        ex = guides['ch10-pawn-raid']['examples'][0]
        board = chess.Board(example_frames(ex)[-1].fen)
        self.assertTrue(board.is_check())
        self.assertEqual(board.piece_at(chess.C1), chess.Piece(chess.KING, chess.WHITE))
        self.assertEqual(board.piece_at(chess.B2), chess.Piece(chess.ROOK, chess.BLACK))
        for reply in list(board.legal_moves):
            branch = board.copy(); branch.push(reply)
            self.assertIn(chess.Move.from_uci('c1b2'), branch.legal_moves)

    def test_material_compensation_is_counted_from_the_final_board(self):
        _, guides = self.content()
        ex = guides['ch10-compensation']['examples'][0]
        board = chess.Board(example_frames(ex)[-1].fen)
        self.assertEqual(len(board.pieces(chess.QUEEN, chess.WHITE)), 1)
        self.assertEqual(len(board.pieces(chess.QUEEN, chess.BLACK)), 0)
        self.assertEqual(len(board.pieces(chess.ROOK, chess.WHITE)), 0)
        self.assertEqual(len(board.pieces(chess.ROOK, chess.BLACK)), 1)
        self.assertEqual(len(board.pieces(chess.BISHOP, chess.BLACK)), 2)
        self.assertEqual(len(board.pieces(chess.KNIGHT, chess.WHITE)), 1)
        self.assertEqual(len(board.pieces(chess.KNIGHT, chess.BLACK)), 1)


if __name__ == '__main__':
    unittest.main()
