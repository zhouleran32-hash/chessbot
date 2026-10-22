"""Independent validation of Chapter 6 positions, teaching, and grading."""
import unittest
import chess

from core.primer import _lesson, grade
from core.primer_study import check_concept, example_frames, validate_guide


class ChapterSixTests(unittest.TestCase):
    def setUp(self):
        from core.primer_chapter6 import LESSONS
        from core.primer_guides_chapter6 import GUIDES
        self.specs, self.guides = LESSONS, GUIDES

    def test_guides_and_every_replay_are_valid(self):
        self.assertGreaterEqual(len(self.specs), 20)
        self.assertEqual({s['id'] for s in self.specs}, set(self.guides))
        for spec in self.specs:
            with self.subTest(lesson=spec['id']):
                self.assertEqual(spec['chapter'], 6)
                self.assertTrue(spec['id'].startswith('ch6-'))
                guide = self.guides[spec['id']]
                validate_guide(guide, 6)
                self.assertGreaterEqual(len(guide['sections']), 3)
                self.assertGreaterEqual(sum(len(s['body'].split()) for s in guide['sections']), 350)
                self.assertGreaterEqual(len(guide['checks']), 2)
                self.assertTrue(guide['pitfalls'])
                for example in guide['examples']:
                    frames = example_frames(example)
                    self.assertEqual(len(frames), len(example['moves']) + 1)
                    for frame in frames:
                        self.assertTrue(chess.Board(frame.fen).is_valid())
                for question in guide['checks']:
                    for index, option in enumerate(question['options']):
                        self.assertEqual(check_concept(guide, question['id'], index).correct, option['correct'])

    def test_all_board_choices_are_canonical_and_correctly_graded(self):
        for spec in self.specs:
            with self.subTest(lesson=spec['id']):
                lesson = _lesson(spec)
                self.assertTrue(any(c.correct for c in lesson.choices))
                self.assertTrue(any(not c.correct for c in lesson.choices))
                for frame in lesson.steps:
                    self.assertTrue(chess.Board(frame.fen).is_valid())
                    self.assertGreaterEqual(len(frame.caption.split()), 8)
                board = chess.Board(lesson.quiz_fen)
                for choice in lesson.choices:
                    move = board.parse_san(choice.san)
                    self.assertIn(move, board.legal_moves)
                    self.assertEqual(board.san(move), choice.san)
                    self.assertEqual(grade(lesson, choice.san).correct, choice.correct)

    def end(self, key, index=0):
        return chess.Board(example_frames(self.guides['ch6-' + key]['examples'][index])[-1].fen)

    def test_concrete_outcomes(self):
        self.assertEqual(self.end('outposts').piece_at(chess.C6), chess.Piece(chess.PAWN, chess.WHITE))
        self.assertEqual(self.end('backward-pawns').piece_at(chess.D5), chess.Piece(chess.KNIGHT, chess.WHITE))
        self.assertFalse(self.end('king-hooks').piece_at(chess.H3))
        self.assertEqual(self.end('fortress').piece_at(chess.E1), chess.Piece(chess.QUEEN, chess.BLACK))
        for key, count in [('queen-geometry', 2), ('rectangle-pendulum', 2), ('return-trip', 1), ('knight-rook-routes', 2)]:
            for index in range(count):
                self.assertTrue(self.end(key, index).is_checkmate(), (key, index))

    def test_repetition_is_real(self):
        ex = self.guides['ch6-perpetual']['examples'][0]
        board = chess.Board(ex['fen'])
        for san in ex['moves']:
            board.push_san(san)
        self.assertTrue(board.can_claim_threefold_repetition())

    def test_pawn_chain_rook_can_really_attack_the_base(self):
        ex = self.guides['ch6-pawn-skeleton']['examples'][0]
        board = chess.Board(example_frames(ex)[-1].fen)
        rooks = board.pieces(chess.ROOK, chess.BLACK)
        self.assertTrue(any(chess.F5 in board.attacks(square) for square in rooks))

    def test_source_diagrams_preserve_critical_obstructions(self):
        amble = chess.Board(self.guides['ch6-knight-rook-routes']['examples'][0]['fen'])
        self.assertEqual(amble.piece_at(chess.D7), chess.Piece(chess.PAWN, chess.BLACK))
        self.assertIsNone(amble.piece_at(chess.E7))
        self.assertNotIn('dxe7', [amble.san(m) for m in amble.legal_moves])
        rook = chess.Board(self.guides['ch6-knight-rook-routes']['examples'][1]['fen'])
        self.assertEqual(rook.piece_at(chess.C2), chess.Piece(chess.BISHOP, chess.WHITE))
        triangle = self.end('queen-geometry', 1)
        self.assertEqual(triangle.piece_at(chess.F1), chess.Piece(chess.KING, chess.WHITE))
        self.assertEqual(triangle.piece_at(chess.F2), chess.Piece(chess.QUEEN, chess.WHITE))

    def test_central_retreat_is_not_onto_a_knight_capture(self):
        board = self.end('piece-centre')
        black_knight = next(iter(board.pieces(chess.KNIGHT, chess.BLACK)))
        self.assertFalse(board.is_attacked_by(chess.WHITE, black_knight))

    def test_triangle_returns_same_arrangement_with_black_to_move(self):
        ex = self.guides['ch6-queen-geometry']['examples'][1]
        initial = chess.Board(ex['fen'])
        board = initial.copy()
        for san in ex['moves'][:5]:
            board.push_san(san)
        self.assertEqual(board.board_fen(), initial.board_fen())
        self.assertEqual(initial.turn, chess.WHITE)
        self.assertEqual(board.turn, chess.BLACK)
        for move in board.legal_moves:
            branch = board.copy()
            self.assertEqual(branch.piece_at(move.from_square), chess.Piece(chess.KNIGHT, chess.BLACK))
            branch.push(move)
            finish = chess.Move.from_uci('g1f2')
            self.assertIn(finish, branch.legal_moves)
            branch.push(finish)
            self.assertTrue(branch.is_checkmate())

    def test_knight_escort_really_forces_every_displayed_king_step(self):
        ex = self.guides['ch6-knight-rook-routes']['examples'][0]
        board = chess.Board(ex['fen'])
        for index, san in enumerate(ex['moves']):
            if board.turn == chess.BLACK:
                self.assertEqual(len(list(board.legal_moves)), 1)
            board.push_san(san)
        self.assertTrue(board.is_checkmate())

    def test_real_mate_alternative_is_accepted(self):
        spec = next(s for s in self.specs if s['id'] == 'ch6-relative-strength')
        self.assertTrue(grade(_lesson(spec), 'Qxf8#').correct)

    def test_all_named_final_section_themes_have_lessons(self):
        required = {'relative-strength', 'bishop-pair', 'knights-and-barriers',
                    'evaluate-position', 'games-centre-decisions', 'perpetual',
                    'king-detour', 'fortress', 'maintain-threat', 'queen-geometry',
                    'rectangle-pendulum', 'return-trip', 'knight-rook-routes'}
        self.assertTrue({'ch6-' + key for key in required} <= self.guides.keys())


if __name__ == '__main__':
    unittest.main()
