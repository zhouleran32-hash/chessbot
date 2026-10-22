"""Chapter 9 positions must demonstrate their stated attacking/defensive jobs."""
import unittest

import chess

from core.primer import _lesson, grade
from core.primer_study import check_concept, example_frames, validate_guide


class ChapterNineTests(unittest.TestCase):
    def modules(self):
        from core.primer_chapter9 import LESSONS
        from core.primer_guides_chapter9 import GUIDES
        return LESSONS, GUIDES

    def test_all_lessons_have_valid_replays_and_graded_legal_exercises(self):
        specs, guides = self.modules()
        self.assertEqual({s['id'] for s in specs}, set(guides))
        self.assertGreaterEqual(len(specs), 24)
        for spec in specs:
            with self.subTest(lesson=spec['id']):
                item = _lesson(spec)
                validate_guide(guides[item.id], 9)
                self.assertTrue(item.id.startswith('ch9-'))
                self.assertTrue(chess.Board(item.quiz_fen).is_valid())
                self.assertTrue(any(c.correct for c in item.choices))
                self.assertTrue(any(not c.correct for c in item.choices))
                for frame in item.steps:
                    self.assertTrue(chess.Board(frame.fen).is_valid())
                for choice in item.choices:
                    board = chess.Board(item.quiz_fen)
                    self.assertEqual(board.san(board.parse_san(choice.san)), choice.san)
                    self.assertEqual(grade(item, choice.san).correct, choice.correct)
                for question in guides[item.id]['checks']:
                    for index, option in enumerate(question['options']):
                        self.assertEqual(check_concept(guides[item.id], question['id'], index).correct, option['correct'])

    def ending(self, name, index=0):
        _, guides = self.modules()
        return chess.Board(example_frames(guides['ch9-' + name]['examples'][index])[-1].fen)

    def test_steinitz_pin_discourages_but_does_not_forbid_castling(self):
        from core.primer_guides_chapter9 import STEINITZ
        from core.primer_build import after
        board = chess.Board(after(('Bxe7', 'Nxe7', 'Re1'), STEINITZ))
        self.assertTrue(board.is_pinned(chess.BLACK, chess.E7))
        board.push_san('O-O')
        self.assertIn(board.parse_san('Rxe7'), board.legal_moves)

    def test_stalemate_trap_really_leaves_no_move_without_check(self):
        board = self.ending('trap')
        self.assertTrue(board.is_stalemate())
        self.assertFalse(board.is_check())

    def test_reti_must_answer_the_pawn_mating_threat(self):
        from core.primer_guides_chapter9 import RETI, RETI_MOVES
        from core.primer_build import after
        board = chess.Board(after(RETI_MOVES[:27], RETI))
        board.push_san('Rxd7')
        board.push_san('gxf5#')
        self.assertTrue(board.is_checkmate())
        correct = self.ending('opposite-bishops-ending', 1)
        self.assertEqual(correct.piece_at(chess.G6), chess.Piece(chess.PAWN, chess.WHITE))
        self.assertFalse(correct.is_game_over())

    def test_geller_exchange_sequence_preserves_the_exchange_advantage(self):
        _, guides = self.modules()
        frames = example_frames(guides['ch9-exchange-combination']['examples'][0])
        board = chess.Board(frames[5].fen)
        self.assertEqual(len(board.pieces(chess.ROOK, chess.BLACK)), 2)
        self.assertEqual(len(board.pieces(chess.ROOK, chess.WHITE)), 1)
        self.assertEqual(len(board.pieces(chess.BISHOP, chess.WHITE)), 1)
        for color in (chess.WHITE, chess.BLACK):
            self.assertFalse(board.pieces(chess.QUEEN, color))
            self.assertFalse(board.pieces(chess.KNIGHT, color))


if __name__ == '__main__':
    unittest.main()
