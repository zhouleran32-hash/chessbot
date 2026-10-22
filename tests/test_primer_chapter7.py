"""Opening examples must teach legal play and preserve their tactical point."""
import importlib.util
import unittest
import chess
from core.primer import _lesson, grade
from core.primer_study import example_frames, validate_guide


class ChapterSevenTests(unittest.TestCase):
    def modules(self):
        self.assertIsNotNone(importlib.util.find_spec('core.primer_chapter7'), 'Chapter 7 is not implemented')
        from core.primer_chapter7 import LESSONS
        from core.primer_guides_chapter7 import GUIDES
        return LESSONS, GUIDES

    def test_every_opening_lesson_has_replayable_teaching_and_legal_practice(self):
        specs, guides = self.modules()
        self.assertEqual({s['id'] for s in specs}, set(guides))
        for spec in specs:
            with self.subTest(lesson=spec['id']):
                lesson = _lesson(spec)
                validate_guide(guides[lesson.id], 7)
                for choice in lesson.choices:
                    board = chess.Board(lesson.quiz_fen)
                    self.assertEqual(board.san(board.parse_san(choice.san)), choice.san)
                    self.assertEqual(grade(lesson, choice.san).correct, choice.correct)

    def test_morphy_finish_is_checkmate_and_not_just_a_free_queen(self):
        _, guides = self.modules()
        final = example_frames(guides['ch7-open-lines']['examples'][0])[-1]
        self.assertTrue(chess.Board(final.fen).is_checkmate())

    def test_composed_king_route_and_pawn_journey_finish_in_mate(self):
        _, guides = self.modules()
        for lesson_id in ('ch7-quiet-route', 'ch7-pawn-journey'):
            with self.subTest(lesson=lesson_id):
                final = chess.Board(example_frames(guides[lesson_id]['examples'][0])[-1].fen)
                self.assertTrue(final.is_checkmate())
        pawn_final = chess.Board(example_frames(guides['ch7-pawn-journey']['examples'][0])[-1].fen)
        self.assertEqual(pawn_final.piece_at(chess.A8), chess.Piece(chess.QUEEN, chess.WHITE))

    def test_bait_line_really_wins_the_knight_with_check(self):
        _, guides = self.modules()
        frames = example_frames(guides['ch7-opening-bait']['examples'][0])
        board = chess.Board(frames[-1].fen)
        self.assertEqual(board.piece_at(chess.E5), chess.Piece(chess.QUEEN, chess.BLACK))
        self.assertEqual(len(board.pieces(chess.KNIGHT, chess.WHITE)), 1)

    def test_saving_cycle_forces_every_reply_and_reaches_threefold(self):
        _, guides = self.modules()
        example = guides['ch7-composition-lessons']['examples'][0]
        board = chess.Board(example['fen'])
        for san in example['moves']:
            if board.turn == chess.BLACK:
                self.assertEqual(list(board.legal_moves), [board.parse_san(san)])
            board.push_san(san)
        self.assertTrue(board.can_claim_threefold_repetition())

    def test_the_shown_queen_chase_mistake_is_actually_mate(self):
        _, guides = self.modules()
        final = example_frames(guides['ch7-queen']['examples'][1])[-1]
        self.assertTrue(chess.Board(final.fen).is_checkmate())

if __name__ == '__main__':
    unittest.main()
