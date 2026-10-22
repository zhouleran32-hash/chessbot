"""Source-study coverage, playable boards, and the actual terminal mechanisms."""
import unittest
import chess
from core.primer_study import validate_guide


class AppendixStudiesTests(unittest.TestCase):
    def content(self):
        from core.primer_appendix_studies import GUIDES, EXERCISES
        return GUIDES, EXERCISES

    def test_complete_coverage_and_legal_replays(self):
        guides, exercises = self.content()
        expected = {f'app-win-{n:02d}' for n in range(1, 33)} | {f'app-draw-{n:02d}' for n in range(1, 12)}
        self.assertEqual(set(guides), expected)
        self.assertEqual({e['id'] for e in exercises}, expected)
        for identifier, guide in guides.items():
            with self.subTest(study=identifier):
                validate_guide(guide, 11)
                self.assertGreaterEqual(len(guide['sections']), 4)
                self.assertGreaterEqual(sum(len(s['body'].split()) for s in guide['sections']), 290)
                self.assertGreaterEqual(len(guide['checks']), 2)
                self.assertTrue(guide['pitfalls'])
                self.assertIn('Printed diagram', guide['sections'][0]['body'])
                for example in guide['examples']:
                    board = chess.Board(example['fen'])
                    self.assertTrue(board.is_valid())
                    self.assertEqual(len(example['notes']), len(example['moves']) + 1)
                    self.assertFalse(any(note.startswith(('White moves the ', 'Black moves the '))
                                         for note in example['notes'][1:]))
                    for san in example['moves']:
                        move = board.parse_san(san)
                        self.assertEqual(board.san(move), san)
                        board.push(move)
        for exercise in exercises:
            board = chess.Board(exercise['fen'])
            self.assertTrue(exercise['inventory'])
            self.assertNotIn('by playing ', exercise['prompt'])
            self.assertTrue(any(c[1] for c in exercise['choices']))
            for san, _, _ in exercise['choices']:
                self.assertEqual(board.san(board.parse_san(san)), san)

    def endpoint(self, key, index=0):
        guides, _ = self.content()
        ex = guides[key]['examples'][index]
        board = chess.Board(ex['fen'])
        for san in ex['moves']:
            board.push_san(san)
        return board

    def test_stalemates_have_no_legal_moves_but_no_check(self):
        for n in (1, 2, 3, 4, 8, 9):
            with self.subTest(study=n):
                self.assertTrue(self.endpoint(f'app-draw-{n:02d}').is_stalemate())

    def test_checkmates_are_checkmates(self):
        for n in (9, 10, 12, 15, 21, 27, 31):
            with self.subTest(study=n):
                self.assertTrue(self.endpoint(f'app-win-{n:02d}').is_checkmate())

    def test_saavedra_and_kok_choose_different_underpromotions(self):
        self.assertEqual(self.endpoint('app-win-07').piece_at(chess.C8), chess.Piece(chess.ROOK, chess.WHITE))
        self.assertEqual(self.endpoint('app-win-24').piece_at(chess.C8), chess.Piece(chess.KNIGHT, chess.WHITE))
        self.assertTrue(self.endpoint('app-win-07', 1).is_stalemate())

    def test_minor_piece_promotions_do_not_refute_drawing_study_two(self):
        self.assertTrue(self.endpoint('app-draw-02', 1).is_insufficient_material())
        self.assertTrue(self.endpoint('app-draw-02', 2).is_insufficient_material())

    def test_knight_mate_source_branch_has_forced_final_replies(self):
        guides, _ = self.content()
        ex = guides['app-win-10']['examples'][0]
        board = chess.Board(ex['fen'])
        for san in ex['moves'][:5]:
            board.push_san(san)
        for expected in ('Kxg2', 'Nf4+', 'Kg1', 'Ke1', 'g2', 'Ne2#'):
            if board.turn == chess.BLACK:
                self.assertEqual([board.san(m) for m in board.legal_moves], [expected])
            board.push_san(expected)
        self.assertTrue(board.is_checkmate())

    def test_kasparian_net_mates_after_every_remaining_rook_move(self):
        guides, _ = self.content()
        ex = guides['app-win-31']['examples'][0]
        board = chess.Board(ex['fen'])
        for san in ex['moves'][:-2]:
            board.push_san(san)
        for reply in list(board.legal_moves):
            child = board.copy(); child.push(reply)
            mates = []
            for move in list(child.legal_moves):
                end = child.copy(); end.push(move)
                if end.is_checkmate():
                    mates.append(move)
            self.assertTrue(mates, board.san(reply))


if __name__ == '__main__':
    unittest.main()
