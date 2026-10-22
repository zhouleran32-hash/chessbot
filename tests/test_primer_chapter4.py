"""Chapter 4 teaching must survive replay, board grading, and its claimed payoffs."""
import importlib.util
import unittest

import chess

from core.primer import _lesson, grade
from core.primer_study import check_concept, example_frames, validate_guide


class ChapterFourTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if importlib.util.find_spec('core.primer_chapter4') is None:
            return
        from core.primer_chapter4 import LESSONS
        from core.primer_guides_chapter4 import GUIDES
        cls.specs = {s['id']: s for s in LESSONS}
        cls.guides = GUIDES

    def test_chapter_is_available(self):
        self.assertIsNotNone(importlib.util.find_spec('core.primer_chapter4'),
                             'Chapter 4 needs playable lessons and independent-study guides.')

    def require_content(self):
        if not hasattr(self, 'specs'):
            self.skipTest('Chapter not authored yet')

    def test_all_boards_and_answer_keys_are_playable(self):
        self.require_content()
        self.assertEqual(set(self.specs), set(self.guides))
        for ident, spec in self.specs.items():
            with self.subTest(lesson=ident):
                self.assertTrue(ident.startswith('ch4-'))
                self.assertEqual(spec['chapter'], 4)
                for fen, caption, arrows in spec['steps']:
                    self.assertTrue(chess.Board(fen).is_valid())
                    self.assertTrue(caption.strip())
                board = chess.Board(spec['quiz_fen'])
                self.assertIsNone(board.outcome())
                self.assertTrue(any(c[1] for c in spec['choices']))
                self.assertTrue(any(not c[1] for c in spec['choices']))
                for san, accepted, feedback in spec['choices']:
                    move = board.parse_san(san)
                    self.assertEqual(board.san(move), san)
                    self.assertEqual(grade(_lesson(spec), san).correct, accepted)
                    self.assertTrue(feedback)

    def test_guides_have_explained_legal_replays_and_concept_feedback(self):
        self.require_content()
        for ident, item in self.guides.items():
            with self.subTest(lesson=ident):
                validate_guide(item, 4)
                self.assertGreaterEqual(len(item['sections']), 3)
                self.assertGreaterEqual(len(item['checks']), 2)
                for example in item['examples']:
                    frames = example_frames(example)
                    self.assertEqual(len(frames), len(example['moves']) + 1)
                    self.assertGreaterEqual(len(frames), 3)
                for question in item['checks']:
                    feedback = [o['explanation'] for o in question['options']]
                    self.assertEqual(len(set(feedback)), len(feedback))
                    for index, option in enumerate(question['options']):
                        self.assertEqual(check_concept(item, question['id'], index).correct,
                                         option['correct'])

    def end_board(self, lesson_id, index=0):
        return chess.Board(example_frames(self.guides[lesson_id]['examples'][index])[-1].fen)

    def test_square_catch_and_double_step_have_different_outcomes(self):
        self.require_content()
        caught = self.end_board('ch4-square-rule')
        self.assertEqual(caught.king(chess.BLACK), chess.H8)
        self.assertEqual(len(caught.pieces(chess.PAWN, chess.WHITE)), 0)
        self.assertEqual(len(caught.pieces(chess.QUEEN, chess.WHITE)), 0)
        escaped = self.end_board('ch4-square-exceptions')
        self.assertEqual(escaped.piece_at(chess.H8), chess.Piece(chess.QUEEN, chess.WHITE))

    def test_reti_line_reaches_supported_promotion(self):
        self.require_content()
        board = self.end_board('ch4-reti')
        self.assertEqual(board.piece_at(chess.C8), chess.Piece(chess.QUEEN, chess.WHITE))
        self.assertEqual(board.piece_at(chess.H1), chess.Piece(chess.QUEEN, chess.BLACK))

    def test_pinned_defender_cannot_recapture(self):
        self.require_content()
        board = self.end_board('ch4-count-attacks')
        self.assertEqual(board.piece_at(chess.D5), chess.Piece(chess.PAWN, chess.WHITE))
        self.assertFalse(any(m.from_square == chess.E6 and m.to_square == chess.D5
                             for m in board.legal_moves))

    def test_blocked_pawn_capture_preserves_defensive_opposition(self):
        self.require_content()
        board = self.end_board('ch4-blocked-pawns')
        self.assertEqual(board.king(chess.WHITE), chess.D5)
        self.assertEqual(board.king(chess.BLACK), chess.D7)
        self.assertEqual(board.piece_at(chess.D4), chess.Piece(chess.PAWN, chess.WHITE))
        self.assertEqual(len(board.pieces(chess.PAWN, chess.BLACK)), 0)

    def test_triangulation_changes_turn_without_changing_position(self):
        self.require_content()
        item = self.guides['ch4-triangulation']['examples'][0]
        frames = example_frames(item)
        initial, returned = chess.Board(frames[0].fen), chess.Board(frames[5].fen)
        self.assertEqual(initial.board_fen(), returned.board_fen())
        self.assertNotEqual(initial.turn, returned.turn)

    def test_short_games_and_rook_puzzle_reach_actual_mate(self):
        self.require_content()
        for ident, index in [('ch4-short-games', 0), ('ch4-short-games', 1),
                             ('ch4-opposition-puzzle', 0), ('ch4-analysis-tree', 2)]:
            with self.subTest(lesson=ident, example=index):
                self.assertTrue(self.end_board(ident, index).is_checkmate())
        frames = example_frames(self.guides['ch4-opposition-puzzle']['examples'][0])
        self.assertTrue(all(chess.Board(f.fen).piece_at(chess.C1) == chess.Piece(chess.ROOK, chess.WHITE)
                            for f in frames[:-1]))


if __name__ == '__main__':
    unittest.main()
