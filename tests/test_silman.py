"""Silman Part One lessons replay the book's methods and tell mate from stalemate."""

import unittest

import chess

from core.primer import feedback_for_played_move, grade
from core.primer_study import example_frames
from core.silman import lessons, pdf_page
from core.silman_study import PARTS, guide_for, validate_guide


class SilmanCourseTests(unittest.TestCase):
    def test_part_one_is_playable_and_later_parts_are_only_mapped(self):
        catalog = lessons()
        self.assertEqual(
            [item.id for item in catalog],
            ["end-staircase", "end-two-queens", "end-queen-rook", "end-two-rooks",
             "end-shrinking-box", "end-king-rook", "end-stalemate",
             "end-two-knights", "end-queen-vs-bishop", "end-knight-fork",
             "end-opposition", "end-seventh-rank", "end-rook-pawn",
             "end-distant-opposition", "end-h-pawn-draw", "end-one-square",
             "end-two-squares", "end-bishop-stops-pawn", "end-rook-escorts",
             "end-pawn-square", "end-outside-pawn", "end-wrong-bishop",
             "end-lucena", "end-philidor", "end-queen-sixth", "end-queen-seventh",
             "end-connected-pawns", "end-breakthrough", "end-triangulation",
             "end-outflanking", "end-rook-on-seventh", "end-two-bishops",
             "end-opposite-bishops",
             "end-pawn-mate", "end-reti", "end-fifth-rank", "end-four-files",
             "end-vancura", "end-short-side", "end-tie-the-king", "end-queen-box",
             "end-f-pawn", "end-king-first", "end-philidor-bad", "end-same-color",
             "end-wrong-color", "end-rook-shuttle", "end-bishop-blockade",
             "end-cat-mouse", "end-two-weaknesses", "end-whose-move",
             "end-outside-knight", "end-fighting-king", "end-queen-passer",
             "end-entombed", "end-rook-sacrifice", "end-lasker-lift", "end-tie-down",
             "end-stop-the-king", "end-simple-zug", "end-bishop-block"],
        )
        self.assertEqual(set(PARTS), set(range(1, 10)))
        self.assertEqual(
            [item.chapter for item in catalog],
            [1] * 7 + [2] * 6 + [3] * 6 + [4] * 7 + [5] * 7 + [6] * 8 + [7] * 7 + [8] * 6 + [9] * 7,
        )
        self.assertEqual(pdf_page(7), 21)

    def test_every_lesson_and_guide_is_legal(self):
        for lesson in lessons():
            guide = guide_for(lesson.id)
            validate_guide(guide, lesson.chapter)
            quiz = chess.Board(lesson.quiz_fen)
            self.assertTrue(quiz.is_valid(), lesson.id)
            self.assertGreaterEqual(len(lesson.steps), 2)
            for choice in lesson.choices:
                move = quiz.parse_san(choice.san)
                self.assertEqual(choice.san, quiz.san(move), lesson.id)
                self.assertEqual(feedback_for_played_move(lesson, choice.san).correct, choice.correct)
            for item in guide["examples"]:
                example_frames(item)

    def test_staircase_mates_every_reply(self):
        lesson = next(item for item in lessons() if item.id == "end-staircase")
        board = chess.Board(lesson.quiz_fen)
        board.push_san("Qf7+")
        replies = sorted(board.san(move) for move in board.legal_moves)
        self.assertEqual(replies, ["Kb8", "Kc8", "Kd8"])
        for reply in replies:
            follow = board.copy()
            follow.push_san(reply)
            follow.push_san("Rg8#")
            self.assertTrue(follow.is_checkmate(), reply)
        self.assertFalse(grade(lesson, "Rc6+").correct)
        punished = chess.Board(lesson.quiz_fen)
        punished.push_san("Rc6+")
        self.assertIn("Kxc6", [punished.san(move) for move in punished.legal_moves])

    def test_book_lines_reach_the_claimed_result(self):
        mates = {
            "end-two-queens": ["Qb5+", "Ke6", "Qaa6+", "Ke7", "Qbb7+", "Kf8", "Qaa8#"],
            "end-two-rooks": ["Re1+", "Kd3", "Rg8", "Kd2", "Re7", "Kd3", "Rd8+", "Kc4", "Rc7+", "Kb5", "Rb8+", "Ka6", "Rc1", "Ka7", "Rb2", "Ka6", "Ra1#"],
            "end-shrinking-box": ["Qe3", "Kc4", "Kg2", "Kd5", "Kf3", "Kc4", "Ke4", "Kb4", "Kd5", "Kb5", "Qb3+", "Ka6", "Kc6", "Ka5", "Qb5#"],
            "end-king-rook": ["Kd6", "Kc8", "Rh7", "Kb8", "Kc6", "Ka8", "Kb6", "Kb8", "Rh8#"],
        }
        by_id = {item.id: item for item in lessons()}
        for lesson_id, moves in mates.items():
            board = chess.Board(by_id[lesson_id].quiz_fen)
            for san in moves:
                board.push_san(san)
            self.assertTrue(board.is_checkmate(), lesson_id)

    def test_stalemate_is_a_draw_and_any_real_mate_counts(self):
        lesson = next(item for item in lessons() if item.id == "end-stalemate")
        board = chess.Board(lesson.quiz_fen)
        drawn = board.copy()
        drawn.push_san("Kc1")
        self.assertTrue(drawn.is_stalemate())
        self.assertFalse(grade(lesson, "Kc1").correct)
        for san in ("Qb1#", "Qb2#", "Qa3#", "Qa4#"):
            finished = board.copy()
            finished.push_san(san)
            self.assertTrue(finished.is_checkmate(), san)
            self.assertTrue(grade(lesson, san).correct, san)
        escaped = board.copy()
        escaped.push_san("Qc3+")
        self.assertIn("Ka2", [escaped.san(move) for move in escaped.legal_moves])

    def test_part_two_lines_match_the_book(self):
        by_id = {item.id: item for item in lessons()}
        knights = chess.Board(by_id["end-two-knights"].quiz_fen)
        self.assertEqual(sorted(knights.san(move) for move in knights.legal_moves), ["Kf8", "Kh8"])
        lost = knights.copy()
        lost.push_san("Kh8")
        lost.push_san("Nf7#")
        self.assertTrue(lost.is_checkmate())
        safe = knights.copy()
        safe.push_san("Kf8")
        self.assertFalse(safe.is_check())

        drawn = chess.Board(by_id["end-opposition"].quiz_fen)
        for san in ["Kd6", "Ke4", "Ke6", "d5+", "Kd6", "Kd4", "Kd7", "Ke5", "Ke7", "d6+", "Kd7", "Kd5", "Kd8", "Kc6", "Kc8", "d7+", "Kd8", "Kd6"]:
            drawn.push_san(san)
        self.assertTrue(drawn.is_stalemate())
        self.assertFalse(grade(by_id["end-opposition"], "Ke6").correct)

        seventh = chess.Board(by_id["end-seventh-rank"].quiz_fen)
        self.assertTrue(grade(by_id["end-seventh-rank"], "Kd6").correct)
        for san in ("Kb7", "Kd5"):
            lost_pawn = seventh.copy()
            lost_pawn.push_san(san)
            self.assertIn("Kxd7", [lost_pawn.san(move) for move in lost_pawn.legal_moves])

        rook_pawn = chess.Board(by_id["end-rook-pawn"].quiz_fen)
        for san in ["g7", "Kh7", "Kf7", "Kh6", "g8=Q", "Kh5", "Qg3", "Kh6", "Qg6#"]:
            rook_pawn.push_san(san)
        self.assertTrue(rook_pawn.is_checkmate())
        abandoned = chess.Board(by_id["end-rook-pawn"].quiz_fen)
        abandoned.push_san("Ke7")
        attacked = abandoned.copy()
        attacked.push_san("Kg7")
        self.assertTrue(attacked.is_attacked_by(chess.BLACK, chess.parse_square("g6")))
        self.assertFalse(attacked.is_attacked_by(chess.WHITE, chess.parse_square("g6")))

        fork = chess.Board(by_id["end-knight-fork"].quiz_fen)
        fork.push_san("Kg2")
        fork.push_san("Nf4+")
        self.assertTrue(fork.is_check())
        self.assertTrue(fork.is_attacked_by(chess.BLACK, chess.parse_square("d3")))

    def test_part_four_lines_match_the_book(self):
        by_id = {item.id: item for item in lessons()}

        square = chess.Board(by_id["end-pawn-square"].quiz_fen)
        self.assertEqual(square.turn, chess.BLACK)
        caught = square.copy()
        for san in ["Ke6", "a5", "Kd5", "a6", "Kc6", "a7", "Kb7"]:
            caught.push_san(san)
        self.assertTrue(caught.is_attacked_by(chess.BLACK, chess.parse_square("a7")))
        missed = square.copy()
        for san in ["Kf6", "a5", "Ke5", "a6", "Kd6", "a7", "Kc7", "a8=Q"]:
            missed.push_san(san)
        self.assertEqual(missed.piece_at(chess.A8).piece_type, chess.QUEEN)

        outside = chess.Board(by_id["end-outside-pawn"].quiz_fen)
        for san in ["d5+", "Kd6", "Kd4", "Kd7", "Ke5", "Ke7", "d6+", "Kf7", "Kd5", "Kf8", "Ke6", "Ke8", "Kf6"]:
            outside.push_san(san)
        self.assertTrue(outside.is_attacked_by(chess.WHITE, chess.parse_square("g5")))
        self.assertTrue(outside.is_attacked_by(chess.WHITE, chess.parse_square("g6")))
        decoy = chess.Board(by_id["end-outside-pawn"].quiz_fen)
        decoy.push_san("Kf4")
        self.assertIn("Kd5", [decoy.san(move) for move in decoy.legal_moves])

        bishop = chess.Board(by_id["end-wrong-bishop"].quiz_fen)
        for san in ("h7", "Bd5"):
            stuck = bishop.copy()
            stuck.push_san(san)
            self.assertTrue(stuck.is_stalemate(), san)
        self.assertFalse(grade(by_id["end-wrong-bishop"], "h7").correct)
        self.assertTrue(grade(by_id["end-wrong-bishop"], "Bf5").correct)
        shuttle = bishop.copy()
        for san in ["Bf5", "Kg8", "h7+", "Kh8", "Kg5", "Kg7"]:
            shuttle.push_san(san)
        self.assertFalse(shuttle.is_game_over())

        lucena = chess.Board(by_id["end-lucena"].quiz_fen)
        for san in ["Rf2+", "Kg7", "Rf4", "Rc2", "Ke7", "Re2+", "Kd6", "Rd2+", "Ke6", "Re2+", "Kd5", "Rd2+", "Rd4"]:
            lucena.push_san(san)
        self.assertTrue(lucena.is_attacked_by(chess.WHITE, chess.D4))
        repeated = chess.Board(by_id["end-lucena"].quiz_fen)
        for san in ["Re7+", "Kf8", "Re8+", "Kf7", "Re7+", "Kf8"]:
            repeated.push_san(san)
        self.assertEqual(repeated.piece_at(chess.D8).piece_type, chess.KING)
        self.assertEqual(repeated.piece_at(chess.D7).piece_type, chess.PAWN)
        self.assertEqual(repeated.king(chess.BLACK), chess.F8)

        philidor = chess.Board(by_id["end-philidor"].quiz_fen)
        self.assertEqual(philidor.turn, chess.BLACK)
        for san in ["Rh6", "Rg7+", "Ke8", "Ra7", "Rg6"]:
            philidor.push_san(san)
        self.assertEqual(philidor.piece_at(chess.G6).piece_type, chess.ROOK)
        hung = chess.Board(by_id["end-philidor"].quiz_fen)
        hung.push_san("Rh8")
        self.assertIn("Rxh8", [hung.san(move) for move in hung.legal_moves])

        sixth = chess.Board(by_id["end-queen-sixth"].quiz_fen)
        sixth.push_san("Kb6")
        sixth.push_san("e2")
        self.assertFalse(sixth.is_attacked_by(chess.WHITE, chess.E1))
        stopped = chess.Board(by_id["end-queen-sixth"].quiz_fen)
        for san in ["Qa5+", "Kd3", "Qe1"]:
            stopped.push_san(san)
        self.assertTrue(stopped.is_attacked_by(chess.WHITE, chess.E2))

        seventh = chess.Board(by_id["end-queen-seventh"].quiz_fen)
        promoted = seventh.copy()
        promoted.push_san("Kb7")
        self.assertIn("e1=Q", [promoted.san(move) for move in promoted.legal_moves])
        hunted = seventh.copy()
        for san in ["Qb4+", "Kd1", "Qd4+", "Kc2", "Qe3", "Kd1", "Qd3+", "Ke1", "Kb7"]:
            hunted.push_san(san)
        self.assertEqual(hunted.piece_at(chess.E1).piece_type, chess.KING)
        self.assertEqual(hunted.piece_at(chess.E2).piece_type, chess.PAWN)

    def test_part_five_lines_match_the_book(self):
        by_id = {item.id: item for item in lessons()}

        connected = chess.Board(by_id["end-connected-pawns"].quiz_fen)
        self.assertEqual(connected.turn, chess.WHITE)
        for san in ["Kb7", "Kxe3", "f5", "Ke4", "f6", "Kf5", "f7", "Kg6", "f8=Q"]:
            connected.push_san(san)
        self.assertEqual(connected.piece_at(chess.F8).piece_type, chess.QUEEN)
        pushed = chess.Board(by_id["end-connected-pawns"].quiz_fen)
        pushed.push_san("f5")
        self.assertIn("Kxe3", [pushed.san(move) for move in pushed.legal_moves])
        self.assertIn("Kxf5", [pushed.san(move) for move in pushed.legal_moves])

        broken = chess.Board(by_id["end-breakthrough"].quiz_fen)
        for san in ["g5", "fxg5", "f6", "g4", "f7", "g3", "f8=Q"]:
            broken.push_san(san)
        self.assertEqual(broken.piece_at(chess.F8).piece_type, chess.QUEEN)
        self.assertFalse(grade(by_id["end-breakthrough"], "Kb1").correct)

        triangle = chess.Board(by_id["end-triangulation"].quiz_fen)
        for san in ["Kf2", "e3+", "Ke2", "Ke5", "Kxe3"]:
            triangle.push_san(san)
        self.assertEqual(triangle.piece_at(chess.E3).piece_type, chess.KING)
        walked = chess.Board(by_id["end-triangulation"].quiz_fen)
        walked.push_san("Ke3")
        self.assertIn("Ke5", [walked.san(move) for move in walked.legal_moves])

        flank = chess.Board(by_id["end-outflanking"].quiz_fen)
        for san in ["Ka2", "Kb8", "Kb2", "Kc8", "Kc2", "Kd8", "Kd2", "Ke8", "Ke2", "Kf8", "Kf2", "Kg8", "Kg2", "Kh8", "Kf3"]:
            flank.push_san(san)
        self.assertEqual(flank.king(chess.WHITE), chess.F3)
        direct = chess.Board(by_id["end-outflanking"].quiz_fen)
        direct.push_san("Kb2")
        self.assertIn("Kb8", [direct.san(move) for move in direct.legal_moves])

        rook = chess.Board(by_id["end-rook-on-seventh"].quiz_fen)
        self.assertTrue(grade(by_id["end-rook-on-seventh"], "Rb7").correct)
        dropped = rook.copy()
        dropped.push_san("Rd8+")
        self.assertIn("Rxd8", [dropped.san(move) for move in dropped.legal_moves])
        escaped = rook.copy()
        escaped.push_san("Rd6")
        self.assertIn("Ke7", [escaped.san(move) for move in escaped.legal_moves])

        bishops = chess.Board(by_id["end-two-bishops"].quiz_fen)
        bishops.push_san("Bg6+")
        self.assertTrue(bishops.is_check())
        self.assertFalse(grade(by_id["end-two-bishops"], "Kb7").correct)

        opposite = chess.Board(by_id["end-opposite-bishops"].quiz_fen)
        for san in ["Kg6", "Ba2", "f5", "Bb3", "f6", "Ke8"]:
            opposite.push_san(san)
        self.assertEqual(opposite.king(chess.BLACK), chess.E8)
        checked = chess.Board(by_id["end-opposite-bishops"].quiz_fen)
        checked.push_san("Kg4")
        self.assertIn("Bd1+", [checked.san(move) for move in checked.legal_moves])

    def test_part_six_lines_match_the_book(self):
        by_id = {item.id: item for item in lessons()}

        mate = chess.Board(by_id["end-pawn-mate"].quiz_fen)
        for san in ["Kf6", "a2", "Ke6", "a1=Q", "d7"]:
            mate.push_san(san)
        self.assertTrue(mate.is_checkmate())
        early = chess.Board(by_id["end-pawn-mate"].quiz_fen)
        early.push_san("d7+")
        self.assertIn("Kxe7", [early.san(move) for move in early.legal_moves])

        reti = chess.Board(by_id["end-reti"].quiz_fen)
        for san in ["Kg7", "h4", "Kf6", "h3", "Ke7", "h2", "c7", "Kb7", "Kd7"]:
            reti.push_san(san)
        self.assertEqual(reti.piece_at(chess.C7).piece_type, chess.PAWN)
        pushed = chess.Board(by_id["end-reti"].quiz_fen)
        pushed.push_san("c7")
        pushed.push_san("Kb7")
        pushed.push_san("c8=Q+")
        self.assertIn("Kxc8", [pushed.san(move) for move in pushed.legal_moves])

        fifth = chess.Board(by_id["end-fifth-rank"].quiz_fen)
        for san in ["Ka6", "Kd8", "Kb6", "Kd7", "Kb7", "Kd8", "Kc6", "Ke7", "Kc7", "Ke8", "Kxd6", "Kd8", "Ke6", "Ke8", "d6", "Kd8", "d7", "Kc7", "Ke7"]:
            fifth.push_san(san)
        self.assertTrue(fifth.is_attacked_by(chess.WHITE, chess.D7))
        front = chess.Board(by_id["end-fifth-rank"].quiz_fen)
        front.push_san("Kc4")
        self.assertIn("Kb6", [front.san(move) for move in front.legal_moves])

        files = chess.Board(by_id["end-four-files"].quiz_fen)
        for san in ["Rc1", "Ke7", "Rc8", "Kd6", "Rb8", "Ra2", "Kb7"]:
            files.push_san(san)
        self.assertEqual(files.king(chess.WHITE), chess.B7)
        hung = chess.Board(by_id["end-four-files"].quiz_fen)
        hung.push_san("Re7+")
        self.assertIn("Kxe7", [hung.san(move) for move in hung.legal_moves])

        vancura = chess.Board(by_id["end-vancura"].quiz_fen)
        self.assertEqual(vancura.turn, chess.BLACK)
        self.assertTrue(grade(by_id["end-vancura"], "Rf5+").correct)
        taken = vancura.copy()
        taken.push_san("Rxa6")
        self.assertIn("Rxa6", [taken.san(move) for move in taken.legal_moves])

        short = chess.Board(by_id["end-short-side"].quiz_fen)
        for san in ["Rh8", "d6", "Rh4+", "Ke5", "Rh5+", "Kf6"]:
            short.push_san(san)
        self.assertEqual(short.king(chess.WHITE), chess.F6)
        grabbed = chess.Board(by_id["end-short-side"].quiz_fen)
        grabbed.push_san("Rxd5+")
        self.assertIn("Kxd5", [grabbed.san(move) for move in grabbed.legal_moves])

        tied = chess.Board(by_id["end-tie-the-king"].quiz_fen)
        self.assertTrue(grade(by_id["end-tie-the-king"], "Ba2").correct)
        captured = tied.copy()
        captured.push_san("Bxe4")
        self.assertIn("Kxe4", [captured.san(move) for move in captured.legal_moves])

        queen = chess.Board(by_id["end-queen-box"].quiz_fen)
        queen.push_san("Kg6")
        queen.push_san("Kg2")
        queen.push_san("Kf5+")
        self.assertTrue(queen.is_check())
        stale = chess.Board(by_id["end-queen-box"].quiz_fen)
        stale.push_san("Kh6")
        self.assertTrue(stale.is_stalemate())

    def test_part_seven_lines_match_the_book(self):
        by_id = {item.id: item for item in lessons()}

        fpawn = chess.Board(by_id["end-f-pawn"].quiz_fen)
        self.assertEqual(fpawn.turn, chess.BLACK)
        self.assertTrue(grade(by_id["end-f-pawn"], "f4").correct)
        for san in ["f4", "Ra8", "f3+", "Kxf3", "Rf1+", "Kg2", "a1=Q"]:
            fpawn.push_san(san)
        self.assertEqual(fpawn.piece_at(chess.A1).piece_type, chess.QUEEN)
        deserted = chess.Board(by_id["end-f-pawn"].quiz_fen)
        deserted.push_san("Rh1")
        self.assertIn("Rxa2", [deserted.san(move) for move in deserted.legal_moves])
        self.assertFalse(deserted.is_attacked_by(chess.BLACK, chess.A2))

        king = chess.Board(by_id["end-king-first"].quiz_fen)
        for san in ["Kf2", "Kf5", "Kf3", "g5", "Re8"]:
            king.push_san(san)
        self.assertEqual(king.piece_at(chess.E8).piece_type, chess.ROOK)
        pushed = chess.Board(by_id["end-king-first"].quiz_fen)
        pushed.push_san("d5")
        self.assertIn("Rxd5", [pushed.san(move) for move in pushed.legal_moves])
        late = chess.Board(by_id["end-king-first"].quiz_fen)
        for san in ["c4", "Rb4", "Kf2"]:
            late.push_san(san)
        self.assertIn("Rxc4", [late.san(move) for move in late.legal_moves])

        philidor = chess.Board(by_id["end-philidor-bad"].quiz_fen)
        for san in ["Rg6", "Kd7", "Ra6", "Rh1", "Ra7+", "Ke8", "Kd6"]:
            philidor.push_san(san)
        self.assertEqual(philidor.king(chess.WHITE), chess.D6)
        checked = chess.Board(by_id["end-philidor-bad"].quiz_fen)
        checked.push_san("Rg7+")
        self.assertIn("Rxg7", [checked.san(move) for move in checked.legal_moves])
        early = chess.Board(by_id["end-philidor-bad"].quiz_fen)
        early.push_san("e6")
        self.assertIn("Rh6", [early.san(move) for move in early.legal_moves])

        same = chess.Board(by_id["end-same-color"].quiz_fen)
        for san in ["Be5", "Kg6", "Bc7"]:
            same.push_san(san)
        self.assertFalse(same.is_attacked_by(chess.BLACK, chess.D8))
        queened = chess.Board(by_id["end-same-color"].quiz_fen)
        for san in ["d8=Q", "Bxd8", "Kxd8"]:
            queened.push_san(san)
        self.assertTrue(queened.is_insufficient_material())

        wrong = chess.Board(by_id["end-wrong-color"].quiz_fen)
        self.assertEqual(wrong.turn, chess.BLACK)
        for san in ["Bg4", "e6", "Bxe6", "Kxe6"]:
            wrong.push_san(san)
        self.assertFalse(wrong.is_attacked_by(chess.WHITE, chess.H8))
        grabbed = chess.Board(by_id["end-wrong-color"].quiz_fen)
        grabbed.push_san("Bxh5")
        self.assertIn("Bxh5", [grabbed.san(move) for move in grabbed.legal_moves])
        hung = chess.Board(by_id["end-wrong-color"].quiz_fen)
        hung.push_san("Bc4")
        self.assertIn("Bxc4", [hung.san(move) for move in hung.legal_moves])

        shuttle = chess.Board(by_id["end-rook-shuttle"].quiz_fen)
        for san in ["Rg4", "Kg6", "Re4"]:
            shuttle.push_san(san)
        self.assertEqual(shuttle.piece_at(chess.E4).piece_type, chess.ROOK)
        check = chess.Board(by_id["end-rook-shuttle"].quiz_fen)
        check.push_san("Re5+")
        self.assertIn("Kxe5", [check.san(move) for move in check.legal_moves])

        block = chess.Board(by_id["end-bishop-blockade"].quiz_fen)
        for san in ["Bxd4+", "exd4", "Rxd4", "Qc7+", "Kh1", "Qh7+", "Kg1", "Qb1+", "Kh2"]:
            block.push_san(san)
        self.assertEqual(block.king(chess.WHITE), chess.H2)
        fire = chess.Board(by_id["end-bishop-blockade"].quiz_fen)
        for san in ["Re4", "Qc5", "Bg3", "d3", "Rxe5", "Qxe5", "Bxe5", "d2"]:
            fire.push_san(san)
        self.assertEqual(fire.piece_at(chess.D2).piece_type, chess.PAWN)
        rook = chess.Board(by_id["end-bishop-blockade"].quiz_fen)
        rook.push_san("Rxd4")
        self.assertIn("exd4", [rook.san(move) for move in rook.legal_moves])

    def test_part_eight_lines_match_the_book(self):
        by_id = {item.id: item for item in lessons()}

        cat = chess.Board(by_id["end-cat-mouse"].quiz_fen)
        self.assertTrue(grade(by_id["end-cat-mouse"], "Nc5").correct)
        for san in ["Nc5", "Ra7", "Nd3", "Ra1+", "Kg2"]:
            cat.push_san(san)
        self.assertEqual(cat.king(chess.WHITE), chess.G2)
        grabbed = chess.Board(by_id["end-cat-mouse"].quiz_fen)
        grabbed.push_san("Rxb5")
        self.assertIn("Rxb5", [grabbed.san(move) for move in grabbed.legal_moves])

        targets = chess.Board(by_id["end-two-weaknesses"].quiz_fen)
        for san in ["a4", "e4", "a5"]:
            targets.push_san(san)
        self.assertEqual(targets.piece_at(chess.A5).piece_type, chess.PAWN)
        queen = chess.Board(by_id["end-two-weaknesses"].quiz_fen)
        queen.push_san("Qxe5")
        self.assertIn("Qxe5", [queen.san(move) for move in queen.legal_moves])

        tempo = chess.Board(by_id["end-whose-move"].quiz_fen)
        for san in ["Kh2", "h4", "Kh3", "Kf7", "Kg4"]:
            tempo.push_san(san)
        self.assertEqual(tempo.turn, chess.BLACK)
        self.assertEqual(tempo.king(chess.WHITE), chess.G4)
        short = chess.Board(by_id["end-whose-move"].quiz_fen)
        for san in ["Kf3", "h4", "Kg4", "Kf7"]:
            short.push_san(san)
        self.assertEqual(short.turn, chess.WHITE)
        self.assertEqual(short.board_fen(), tempo.board_fen())
        pushed = chess.Board(by_id["end-whose-move"].quiz_fen)
        pushed.push_san("d7+")
        self.assertIn("Kxd7", [pushed.san(move) for move in pushed.legal_moves])
        self.assertIn("Kxe7", [pushed.san(move) for move in pushed.legal_moves])

        knight = chess.Board(by_id["end-outside-knight"].quiz_fen)
        self.assertEqual(knight.turn, chess.BLACK)
        for san in ["g5", "hxg5", "fxg5", "Nb4"]:
            knight.push_san(san)
        self.assertEqual(knight.piece_at(chess.G5).piece_type, chess.PAWN)
        center = chess.Board(by_id["end-outside-knight"].quiz_fen)
        center.push_san("d4")
        self.assertFalse(center.is_attacked_by(chess.BLACK, chess.D4))
        self.assertIn("exd4", [center.san(move) for move in center.legal_moves])

        fight = chess.Board(by_id["end-fighting-king"].quiz_fen)
        for san in ["Bd5", "Bb1", "d2", "Kxd2", "Be4"]:
            fight.push_san(san)
        self.assertEqual(fight.piece_at(chess.E4).piece_type, chess.BISHOP)
        lost = chess.Board(by_id["end-fighting-king"].quiz_fen)
        lost.push_san("Bf3")
        self.assertIn("Kxf3", [lost.san(move) for move in lost.legal_moves])
        taken = chess.Board(by_id["end-fighting-king"].quiz_fen)
        taken.push_san("Bd5")
        taken.push_san("Kxd3")
        self.assertIn("Bxa2", [taken.san(move) for move in taken.legal_moves])

        passer = chess.Board(by_id["end-queen-passer"].quiz_fen)
        for san in ["Qd4+", "Kg8", "b6"]:
            passer.push_san(san)
        self.assertTrue(passer.is_attacked_by(chess.WHITE, chess.B6))
        early = chess.Board(by_id["end-queen-passer"].quiz_fen)
        early.push_san("b6")
        self.assertFalse(early.is_attacked_by(chess.WHITE, chess.B6))
        self.assertIn("Qxb6", [early.san(move) for move in early.legal_moves])
        hung = chess.Board(by_id["end-queen-passer"].quiz_fen)
        hung.push_san("Qxh5")
        self.assertIn("gxh5", [hung.san(move) for move in hung.legal_moves])

    def test_part_nine_lines_match_the_book(self):
        by_id = {item.id: item for item in lessons()}

        tomb = chess.Board(by_id["end-entombed"].quiz_fen)
        tomb.push_san("Bd7")
        tomb.push_san("Na7")
        self.assertFalse(any(tomb.piece_at(move.from_square).piece_type == chess.KNIGHT for move in tomb.legal_moves))
        opened = chess.Board(by_id["end-entombed"].quiz_fen)
        opened.push_san("a7")
        self.assertIn("Nxa7", [opened.san(move) for move in opened.legal_moves])

        sac = chess.Board(by_id["end-rook-sacrifice"].quiz_fen)
        for san in ["Rh1+", "Kxh1", "Kg3", "Rf7", "Re1+", "Rf1", "Rxf1"]:
            sac.push_san(san)
        self.assertTrue(sac.is_checkmate())
        grabbed = chess.Board(by_id["end-rook-sacrifice"].quiz_fen)
        grabbed.push_san("Rxe6")
        self.assertIn("Rxe6", [grabbed.san(move) for move in grabbed.legal_moves])

        lasker = chess.Board(by_id["end-lasker-lift"].quiz_fen)
        for san in ["Rb8", "b3", "Rb5"]:
            lasker.push_san(san)
        self.assertEqual(lasker.piece_at(chess.B5).piece_type, chess.ROOK)
        pawn = chess.Board(by_id["end-lasker-lift"].quiz_fen)
        pawn.push_san("d3")
        self.assertIn("cxd3", [pawn.san(move) for move in pawn.legal_moves])

        tie = chess.Board(by_id["end-tie-down"].quiz_fen)
        for san in ["Ra5", "Rb7", "Ra6"]:
            tie.push_san(san)
        self.assertEqual(tie.piece_at(chess.A6).piece_type, chess.ROOK)
        checked = chess.Board(by_id["end-tie-down"].quiz_fen)
        checked.push_san("Rf7+")
        self.assertIn("Kxf7", [checked.san(move) for move in checked.legal_moves])

        majority = chess.Board(by_id["end-stop-the-king"].quiz_fen)
        for san in ["Rd1+", "Kg2", "a5", "Rc2", "b4"]:
            majority.push_san(san)
        self.assertEqual(majority.piece_at(chess.B4).piece_type, chess.PAWN)
        loose = chess.Board(by_id["end-stop-the-king"].quiz_fen)
        loose.push_san("Rd4")
        self.assertIn("exd4", [loose.san(move) for move in loose.legal_moves])

        simple = chess.Board(by_id["end-simple-zug"].quiz_fen)
        simple.push_san("Bf5")
        self.assertIn("Ba6", [simple.san(move) for move in simple.legal_moves])
        traded = chess.Board(by_id["end-simple-zug"].quiz_fen)
        for san in ["Bf5", "Bxf5", "Kxf5"]:
            traded.push_san(san)
        self.assertEqual(traded.king(chess.WHITE), chess.F5)
        dropped = chess.Board(by_id["end-simple-zug"].quiz_fen)
        dropped.push_san("Bd3")
        self.assertIn("Kxd5", [dropped.san(move) for move in dropped.legal_moves])

        block = chess.Board(by_id["end-bishop-block"].quiz_fen)
        for san in ["Bg3", "Kf1", "d3", "Bb4"]:
            block.push_san(san)
        self.assertEqual(block.piece_at(chess.B4).piece_type, chess.BISHOP)
        lost = chess.Board(by_id["end-bishop-block"].quiz_fen)
        lost.push_san("Bh2+")
        self.assertIn("Kxh2", [lost.san(move) for move in lost.legal_moves])


if __name__ == "__main__":
    unittest.main()
