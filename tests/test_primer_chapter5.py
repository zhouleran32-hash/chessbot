"""Chapter 5 replay, grading and tactical-outcome regressions."""
import importlib.util
import unittest

import chess

from core.primer import _lesson, grade
from core.primer_study import check_concept, example_frames, validate_guide


class ChapterFiveTests(unittest.TestCase):
    def load_content(self):
        self.assertIsNotNone(importlib.util.find_spec('core.primer_chapter5'), 'Chapter 5 board lessons must exist')
        self.assertIsNotNone(importlib.util.find_spec('core.primer_guides_chapter5'), 'Chapter 5 study guides must exist')
        from core.primer_chapter5 import LESSONS
        from core.primer_guides_chapter5 import GUIDES
        return {item['id']: item for item in LESSONS}, GUIDES

    def test_every_board_exercise_and_explained_replay_is_playable(self):
        specs, guides = self.load_content()
        self.assertEqual(set(specs), set(guides))
        for ident, spec in specs.items():
            with self.subTest(lesson=ident):
                item = _lesson(spec)
                self.assertEqual(item.chapter, 5)
                self.assertTrue(ident.startswith('ch5-'))
                for frame in item.steps:
                    self.assertTrue(chess.Board(frame.fen).is_valid())
                board = chess.Board(item.quiz_fen)
                self.assertFalse(board.is_game_over())
                self.assertTrue(any(c.correct for c in item.choices))
                self.assertTrue(any(not c.correct for c in item.choices))
                for choice in item.choices:
                    self.assertEqual(board.san(board.parse_san(choice.san)), choice.san)
                    result = grade(item, choice.san)
                    self.assertEqual(result.correct, choice.correct, choice.san)
                    self.assertTrue(result.explanation.strip())
                validate_guide(guides[ident], 5)
                for question in guides[ident]['checks']:
                    feedback = set()
                    for index, option in enumerate(question['options']):
                        self.assertEqual(check_concept(guides[ident], question['id'], index).correct, option['correct'])
                        feedback.add(option['explanation'])
                    self.assertEqual(len(feedback), len(question['options']))

    def example_end(self, ident, index=0):
        _, guides = self.load_content()
        frames = example_frames(guides[ident]['examples'][index])
        return chess.Board(frames[-1].fen)

    def test_underpromotion_forks_king_and_queen(self):
        specs, _ = self.load_content()
        board = chess.Board(specs['ch5-promotion-fork']['quiz_fen'])
        board.push_san('bxc8=N+')
        self.assertEqual(board.piece_at(chess.C8), chess.Piece(chess.KNIGHT, chess.WHITE))
        self.assertTrue(board.is_check())
        self.assertIn(chess.E7, board.attacks(chess.C8))
        queen = chess.Board(specs['ch5-promotion-fork']['quiz_fen'])
        queen.push_san('bxc8=Q')
        self.assertFalse(queen.is_check())

    def test_line_opening_obstruction_and_double_check_end_in_mate(self):
        for ident in ('ch5-open-lines', 'ch5-obstruction', 'ch5-double-check', 'ch5-king-hunt'):
            with self.subTest(lesson=ident):
                self.assertTrue(self.example_end(ident).is_checkmate())

    def test_stalemate_is_not_checkmate(self):
        board = self.example_end('ch5-stalemate-rescue')
        self.assertTrue(board.is_stalemate())
        self.assertFalse(board.is_check())

    def test_interference_promotes_on_either_capture(self):
        for index, square in ((0, chess.H1), (1, chess.D1)):
            board = self.example_end('ch5-interference', index)
            self.assertEqual(board.piece_at(square), chess.Piece(chess.QUEEN, chess.BLACK))

    def test_wrong_bishop_draw_removes_non_rook_pawn(self):
        board = self.example_end('ch5-fortress-rescue')
        self.assertEqual(board.pieces(chess.PAWN, chess.BLACK), chess.SquareSet([chess.A7, chess.A6]))
        self.assertNotEqual(chess.square_rank(chess.C6) % 2 ^ chess.square_file(chess.C6) % 2,
                            chess.square_rank(chess.A1) % 2 ^ chess.square_file(chess.A1) % 2)

    def test_legal_trap_declined_keeps_black_material(self):
        board = self.example_end('ch5-traps', 1)
        self.assertEqual(len(board.pieces(chess.KNIGHT, chess.WHITE)), 1)
        self.assertEqual(len(board.pieces(chess.QUEEN, chess.WHITE)), 1)
        self.assertEqual(len(board.pieces(chess.QUEEN, chess.BLACK)), 1)

    def test_defensive_queen_capture_is_mate_and_counterattack_is_mate(self):
        self.assertTrue(self.example_end('ch5-find-refutation', 1).is_checkmate())
        self.assertTrue(self.example_end('ch5-counter-combination').is_checkmate())

    def test_line_opening_covers_the_bishop_countercheck(self):
        _, guides = self.load_content()
        examples = guides['ch5-open-lines']['examples']
        self.assertEqual(len(examples), 3)
        alternative = examples[2]
        self.assertIn('Bh7+', alternative['moves'])
        self.assertTrue(self.example_end('ch5-open-lines', 2).is_checkmate())

    def test_discovered_check_and_alternative_defences(self):
        _, guides = self.load_content()
        examples = guides['ch5-counter-combination']['examples']
        board = chess.Board(examples[0]['fen'])
        for san in examples[0]['moves'][:5]:
            board.push_san(san)
        # Nf5 uncovers the queen; the knight does not check a king on f8.
        self.assertEqual(board.checkers(), chess.SquareSet([chess.A3]))
        self.assertEqual({board.san(m) for m in board.legal_moves},
                         {'Kg8', 'Ke8', 'Qd6', 'Qb4', 'Rc5'})
        self.assertEqual(len(examples), 6)
        for index in range(6):
            self.assertTrue(self.example_end('ch5-counter-combination', index).is_checkmate())
        board.push_san('Qd6')
        board.push_san('Qxd6+')
        self.assertEqual({board.san(m) for m in board.legal_moves}, {'Kg8', 'Ke8'})
        board.push_san('Ke8')
        board.push_san('Ng7#')
        self.assertTrue(board.is_checkmate())


    def test_recurring_pattern_concept_names_a_legal_mating_threat(self):
        _, guides = self.load_content()
        guide = guides['ch5-recurring-patterns']
        board = chess.Board(guide['examples'][0]['fen'])
        for san in ('Rxa7+', 'Qxa7', 'Ra5'):
            board.push_san(san)
        board.push(chess.Move.null())  # Test the stated threat if Black does nothing.
        question = next(q for q in guide['checks'] if q['id'] == 'ch5-pattern-threat')
        answer = next(o['text'] for o in question['options'] if o['correct'])
        board.push_san(answer.split()[0])
        self.assertTrue(board.is_checkmate())


if __name__ == '__main__':
    unittest.main()
