"""Regression tests for real tactical claims and replayable Chapter 3 teaching."""
import importlib.util
import unittest

import chess

from core.primer_chapter3 import LESSONS


class ChapterThreeTeachingTests(unittest.TestCase):
    def setUp(self):
        self.specs = {item['id']: item for item in LESSONS}

    def test_piece_value_answer_does_not_sacrifice_queen_to_enemy_king(self):
        item = self.specs['piece-values']
        board = chess.Board(item['quiz_fen'])
        answer = next(c[0] for c in item['choices'] if c[1])
        move = board.parse_san(answer)
        board.push(move)
        self.assertNotIn(move.to_square, board.attacks(board.king(chess.BLACK)))

    def test_time_lesson_promotion_threat_is_legal_and_cannot_be_recaptured(self):
        board = chess.Board(self.specs['time']['quiz_fen'])
        board.push_san('Kh2')
        promotions = [m for m in board.legal_moves if m.promotion == chess.QUEEN]
        self.assertTrue(promotions, 'The pawn must actually be able to promote.')
        board.push(promotions[0])
        self.assertFalse(any(board.is_capture(m) and m.to_square == promotions[0].to_square for m in board.legal_moves))

    def test_both_queen_moves_really_create_same_mate_threat(self):
        item = self.specs['threats']
        for san in ('Qh5', 'Qf3'):
            self.assertTrue(next(c[1] for c in item['choices'] if c[0] == san), san)
            board = chess.Board(item['quiz_fen'])
            for move in (san, 'a6', 'Qxf7#'):
                board.push_san(move)
            self.assertTrue(board.is_checkmate())

    def test_attraction_really_moves_the_king_onto_the_bait_square(self):
        item = self.specs['attraction']
        board = chess.Board(item['quiz_fen'])
        move = board.parse_san(next(c[0] for c in item['choices'] if c[1]))
        destination = move.to_square
        board.push(move)
        replies = list(board.legal_moves)
        self.assertEqual(len(replies), 1)
        self.assertEqual(replies[0].to_square, destination)
        self.assertEqual(board.piece_type_at(replies[0].from_square), chess.KING)
        board.push(replies[0])
        board.push_san('Ng6+')
        self.assertTrue(board.is_check())
        self.assertTrue(board.is_attacked_by(chess.WHITE, board.king(chess.BLACK)))
        self.assertIn(chess.F8, board.attacks(chess.G6))

    def test_safe_unpin_also_keeps_knight_defended(self):
        item = self.specs['pin']
        board = chess.Board(item['quiz_fen'])
        board.push_san(next(c[0] for c in item['choices'] if c[1]))
        self.assertFalse(board.is_pinned(chess.WHITE, chess.C3))
        self.assertTrue(board.is_attacked_by(chess.WHITE, chess.C3))

    def test_mixed_threat_involves_mate_and_a_real_material_target(self):
        board = chess.Board(self.specs['many-sided-threats']['quiz_fen'])
        self.assertIn(chess.Move.from_uci('d1h5'), board.legal_moves)
        board.push_san('Qh5')
        self.assertIn(chess.A5, board.attacks(chess.H5))
        for reply, continuation in [('g6', 'Qxa5'), ('Bb6', 'Qxf7#')]:
            branch = board.copy()
            branch.push_san(reply)
            branch.push_san(continuation)
            if continuation.endswith('#'):
                self.assertTrue(branch.is_checkmate())
            else:
                self.assertEqual(branch.piece_type_at(chess.A5), chess.QUEEN)

    def test_spare_pawn_tempo_preserves_a_central_pawn_position(self):
        item = self.specs['zugzwang']
        board = chess.Board(item['quiz_fen'])
        self.assertEqual(board.piece_at(chess.E4), chess.Piece(chess.PAWN, chess.WHITE))
        self.assertTrue(next(c[1] for c in item['choices'] if c[0] == 'h3'))
        self.assertTrue(next(c[1] for c in item['choices'] if c[0] == 'h4'))

    def test_missing_core_topics_have_dedicated_exercises(self):
        required = {'bishop-vs-knight', 'queen-vs-pawn', 'relative-pin', 'overloaded-defender',
                    'skewer', 'discovered-attack', 'underpromotion', 'bishop-knight-mate',
                    'triangulation', 'purposeful-exchanges', 'chapter3-practice'}
        self.assertTrue(required <= self.specs.keys(), required - self.specs.keys())

    def test_overload_payoff_cannot_be_undone_by_another_queen_recapture(self):
        board = chess.Board(self.specs['overloaded-defender']['quiz_fen'])
        self.assertIn(chess.G5, board.attacks(chess.D8))
        for san in ('Rxc8', 'Qxc8', 'Bxg5'):
            board.push_san(san)
        self.assertFalse(any(move.to_square == chess.G5 for move in board.legal_moves))

    def test_rook_underpromotion_avoids_queen_stalemate_and_reaches_mate(self):
        board = chess.Board(self.specs['underpromotion']['quiz_fen'])
        queen = board.copy()
        queen.push_san('c8=Q')
        self.assertTrue(queen.is_stalemate())
        for san in ('c8=R', 'Ka6', 'Ra8#'):
            board.push_san(san)
        self.assertTrue(board.is_checkmate())

    def test_every_guide_has_substantial_teaching_and_connected_legal_examples(self):
        self.assertIsNotNone(importlib.util.find_spec('core.primer_guides_chapter3'))
        from core.primer_study import guide_for
        for lesson_id in self.specs:
            guide = guide_for(lesson_id, 3)
            self.assertIsNotNone(guide, lesson_id)
            with self.subTest(lesson=lesson_id):
                self.assertGreaterEqual(len(guide['goals']), 2)
                self.assertGreaterEqual(len(guide['sections']), 3)
                word_count = sum(len(s['body'].split()) for s in guide['sections'])
                self.assertGreaterEqual(word_count, 300)
                self.assertGreaterEqual(len(guide['pitfalls']), 2)
                self.assertEqual(len(guide['recap']), 3)
                self.assertGreaterEqual(len(guide['checks']), 2)
                for check in guide['checks']:
                    self.assertEqual(sum(o['correct'] for o in check['options']), 1)
                self.assertTrue(guide['examples'])
                for example in guide['examples']:
                    board = chess.Board(example['fen'])
                    self.assertTrue(board.is_valid())
                    self.assertGreaterEqual(len(example['moves']), 2)
                    self.assertEqual(len(example['notes']), len(example['moves']) + 1)
                    for san in example['moves']:
                        self.assertIsNone(board.outcome(), f'{lesson_id}: move after terminal position')
                        move = board.parse_san(san)
                        self.assertEqual(board.san(move), san, f'{lesson_id}: canonical notation')
                        board.push(move)
                        self.assertTrue(board.is_valid())
