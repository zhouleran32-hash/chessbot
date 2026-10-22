"""Endgame methods must preserve legal resistance and their concrete outcomes."""
import importlib.util
import unittest
import chess
from core.primer import _lesson, grade
from core.primer_study import example_frames, validate_guide, check_concept


class ChapterEightTests(unittest.TestCase):
    def modules(self):
        self.assertIsNotNone(importlib.util.find_spec('core.primer_chapter8'), 'Chapter 8 is not implemented')
        from core.primer_chapter8 import LESSONS
        from core.primer_guides_chapter8 import GUIDES
        return LESSONS, GUIDES

    def test_all_lessons_have_legal_complete_teaching_and_graded_practice(self):
        specs, guides = self.modules()
        self.assertEqual({s['id'] for s in specs}, set(guides))
        for spec in specs:
            with self.subTest(lesson=spec['id']):
                lesson = _lesson(spec)
                guide = guides[lesson.id]
                validate_guide(guide, 8)
                self.assertGreaterEqual(len(guide['checks']), 2)
                for frame in lesson.steps:
                    self.assertTrue(chess.Board(frame.fen).is_valid())
                for choice in lesson.choices:
                    board = chess.Board(lesson.quiz_fen)
                    self.assertEqual(board.san(board.parse_san(choice.san)), choice.san)
                    self.assertEqual(grade(lesson, choice.san).correct, choice.correct)
                for question in guide['checks']:
                    for i, option in enumerate(question['options']):
                        self.assertEqual(check_concept(guide, question['id'], i).correct, option['correct'])

    def ending(self, key, index=0):
        _, guides = self.modules()
        return chess.Board(example_frames(guides['ch8-' + key]['examples'][index])[-1].fen)

    def test_opposition_conversion_reaches_a_protected_promotion(self):
        board = self.ending('opposition')
        self.assertEqual(board.piece_at(chess.E8), chess.Piece(chess.QUEEN, chess.WHITE))
        self.assertFalse(board.is_stalemate())

    def test_breakthrough_creates_a_passed_pawn_and_promotes(self):
        board = self.ending('breakthrough')
        self.assertEqual(board.piece_at(chess.A8), chess.Piece(chess.QUEEN, chess.WHITE))
        self.assertEqual(len(board.pieces(chess.PAWN, chess.BLACK)), 3)

    def test_wrong_bishop_and_rook_pawn_example_reaches_stalemate(self):
        self.assertTrue(self.ending('wrong-bishop').is_stalemate())

    def test_lucena_bridge_really_blocks_the_check_and_pawn_can_advance(self):
        board = self.ending('bridge')
        self.assertEqual(board.piece_at(chess.G4), chess.Piece(chess.ROOK, chess.WHITE))
        self.assertFalse(board.is_check())
        self.assertFalse(board.is_attacked_by(chess.BLACK, chess.G5))
        board.push_san('Rxg4+')
        board.push_san('Kxg4')
        self.assertEqual(board.piece_at(chess.G4), chess.Piece(chess.KING, chess.WHITE))
        self.assertEqual(len(board.pieces(chess.ROOK, chess.BLACK)), 0)

    def test_philidor_switches_from_rank_barrier_to_rear_checks(self):
        board = self.ending('sixth-rank')
        self.assertEqual(board.piece_at(chess.C1), chess.Piece(chess.ROOK, chess.BLACK))
        self.assertEqual(board.piece_at(chess.E6), chess.Piece(chess.PAWN, chess.WHITE))
        self.assertIn(board.parse_san('Kg5'), board.legal_moves)
        board.push_san('Kg5')
        self.assertTrue(board.gives_check(board.parse_san('Rg1+')))

    def test_lateral_checking_stalemate_is_a_draw(self):
        self.assertTrue(self.ending('lateral-exceptions').is_stalemate())

    def test_two_pawn_rook_sacrifice_is_stalemate_with_white_rook_still_present(self):
        board = self.ending('two-pawns', 1)
        self.assertTrue(board.is_stalemate())
        self.assertEqual(board.piece_at(chess.F7), chess.Piece(chess.ROOK, chess.WHITE))
        self.assertEqual(len(board.pieces(chess.ROOK, chess.BLACK)), 0)

    def test_bad_attacking_rook_placement_allows_the_pawn_to_be_captured(self):
        board = self.ending('lateral-exceptions', 2)
        self.assertEqual(len(board.pieces(chess.PAWN, chess.WHITE)), 0)
        self.assertEqual(board.piece_at(chess.E7), chess.Piece(chess.ROOK, chess.BLACK))

    def test_exchange_destination_finishes_in_a_safe_promotion(self):
        board = self.ending('transitions')
        self.assertEqual(len(board.pieces(chess.ROOK, chess.WHITE)), 0)
        self.assertEqual(len(board.pieces(chess.ROOK, chess.BLACK)), 0)
        self.assertEqual(board.piece_at(chess.E8), chess.Piece(chess.QUEEN, chess.WHITE))

    def test_race_promotions_are_forcing_detours_and_final_pawn_survives(self):
        _, guides = self.modules()
        replay = guides['ch8-pawn-races']['examples'][0]
        board = chess.Board(replay['fen'])
        promotions = []
        for san in replay['moves']:
            move = board.parse_san(san)
            if move.promotion:
                promotions.append((san, board.gives_check(move)))
            board.push(move)
        self.assertEqual(promotions, [('a1=Q+', True), ('b8=Q+', True)])
        self.assertEqual(board.piece_at(chess.E7), chess.Piece(chess.PAWN, chess.WHITE))
        self.assertEqual(board.king(chess.BLACK), chess.B8)

    def test_opposite_bishop_sacrifice_is_recaptured_by_the_pawn_not_the_king(self):
        board = self.ending('opposite-bishops')
        board.push_san('Bxe7')
        self.assertNotIn(chess.Move.from_uci('d7e7'), board.legal_moves)
        board.push_san('fxe7+')
        self.assertEqual(board.piece_at(chess.E7), chess.Piece(chess.PAWN, chess.WHITE))
        self.assertIn(chess.D7, board.attackers(chess.WHITE, chess.E7))
        self.assertNotIn(chess.Move.from_uci('f8e7'), board.legal_moves)

    def test_underpromotion_gives_the_required_check(self):
        board = self.ending('rook-v-pawn')
        self.assertTrue(board.is_check())
        self.assertEqual(board.piece_at(chess.C1), chess.Piece(chess.KNIGHT, chess.BLACK))

    def test_queen_promotion_allows_rook_mate_but_knight_promotion_checks(self):
        _, guides = self.modules()
        replay = guides['ch8-rook-v-pawn']['examples'][0]
        board = chess.Board(replay['fen'])
        for san in replay['moves'][:-1]:
            board.push_san(san)
        queen = board.copy()
        queen.push_san('c1=Q')
        self.assertFalse(queen.is_check())
        queen.push_san('Rh1#')
        self.assertTrue(queen.is_checkmate())
        knight = board.copy()
        knight.push_san('c1=N+')
        self.assertTrue(knight.is_check())
        self.assertNotIn(chess.Move.from_uci('h2h1'), knight.legal_moves)

    def test_unprotected_knight_is_won_by_double_attack(self):
        board = self.ending('rook-v-minor')
        self.assertEqual(len(board.pieces(chess.KNIGHT, chess.BLACK)), 0)

    def test_rook_restriction_covers_knight_exits_not_the_g4_knight(self):
        from core.primer_chapter8 import EXAMPLES
        ex = EXAMPLES['ch8-rook-v-minor'][0]
        board = chess.Board(ex['fen'])
        for san in ex['moves'][:5]:
            board.push_san(san)
        self.assertEqual(board.piece_at(chess.H3), chess.Piece(chess.ROOK, chess.WHITE))
        self.assertNotIn(chess.G4, board.attacks(chess.H3))
        for square in (chess.E3, chess.H2, chess.H6):
            self.assertIn(square, board.attacks(chess.H3))
        board.push_san('Nf2')
        board.push_san('Rf3+')
        self.assertTrue(board.is_check())
        self.assertIn(chess.F2, board.attacks(chess.F3))
        self.assertEqual(len(board.pieces(chess.ROOK, chess.WHITE)), 1)


if __name__ == '__main__':
    unittest.main()
