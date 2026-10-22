"""Chess-behaviour regressions for Chapter 1's independent-study material."""

import importlib.util
import unittest

import chess

from core.primer import feedback_for_played_move, lessons


class ChapterOneChessTests(unittest.TestCase):
    def lesson(self, lesson_id):
        return next(item for item in lessons() if item.id == lesson_id)

    def test_rook_mate_answer_is_actually_checkmate(self):
        lesson = self.lesson("mate")
        board = chess.Board(lesson.quiz_fen)
        answer = next(choice for choice in lesson.choices if choice.correct)
        board.push_san(answer.san)
        self.assertTrue(board.is_checkmate(), "The rook-mate answer must leave no legal capture or escape")

    def test_every_chapter_one_choice_uses_truthful_check_and_mate_suffixes(self):
        for lesson in lessons():
            if lesson.chapter != 1:
                continue
            board = chess.Board(lesson.quiz_fen)
            for choice in lesson.choices:
                with self.subTest(lesson=lesson.id, san=choice.san):
                    self.assertEqual(choice.san, board.san(board.parse_san(choice.san)))

    def test_correct_moves_pass_the_same_grading_path_as_the_board(self):
        for lesson in lessons():
            if lesson.chapter != 1:
                continue
            board = chess.Board(lesson.quiz_fen)
            for choice in lesson.choices:
                if choice.correct:
                    with self.subTest(lesson=lesson.id):
                        played = board.san(board.parse_san(choice.san))
                        self.assertTrue(feedback_for_played_move(lesson, played).correct)

    def test_exchange_example_really_gives_a_minor_piece_for_a_rook(self):
        lesson = self.lesson("exchanges")
        board = chess.Board(lesson.quiz_fen)
        answer = next(choice for choice in lesson.choices if choice.correct)
        move = board.parse_san(answer.san)
        self.assertEqual(board.piece_type_at(move.to_square), chess.ROOK)
        self.assertEqual(board.piece_type_at(move.from_square), chess.BISHOP)
        board.push(move)
        replies = [reply for reply in board.legal_moves if reply.to_square == move.to_square]
        self.assertTrue(replies, "The opponent must be able to recapture the bishop for an actual exchange")

    def test_perpetual_example_really_repeats_with_forced_king_replies(self):
        lesson = self.lesson("perpetual-check")
        board = chess.Board(lesson.quiz_fen)
        start = board.fen().split()[:4]
        for san in ("Qf1+", "Kh2", "Qf2+", "Kh1") * 2:
            if board.is_check():
                self.assertEqual(board.legal_moves.count(), 1)
            try:
                board.push_san(san)
            except ValueError:
                self.fail(f"The perpetual example cannot play its advertised cycle: {san}")
        self.assertEqual(board.fen().split()[:4], start)
        self.assertTrue(board.can_claim_threefold_repetition())


class ChapterOneGuideTests(unittest.TestCase):
    def test_every_lesson_has_complete_guidance_and_replayable_examples(self):
        self.assertIsNotNone(importlib.util.find_spec("core.primer_guides_chapter1"), "Detailed Chapter 1 guides are missing")
        from core.primer_guides_chapter1 import GUIDES
        chapter = [lesson for lesson in lessons() if lesson.chapter == 1]
        self.assertEqual(set(GUIDES), {lesson.id for lesson in chapter})
        for lesson in chapter:
            guide = GUIDES[lesson.id]
            with self.subTest(lesson=lesson.id):
                self.assertEqual(len(guide["pages"]), 2)
                self.assertTrue(12 <= guide["pages"][0] <= guide["pages"][1] <= 34)
                self.assertGreaterEqual(len(guide["goals"]), 2)
                self.assertGreaterEqual(len(guide["sections"]), 3)
                self.assertGreaterEqual(len(" ".join(section["body"] for section in guide["sections"]).split()), 280)
                self.assertGreaterEqual(len(guide["pitfalls"]), 2)
                self.assertEqual(len(guide["recap"]), 3)
                self.assertGreaterEqual(len(guide["checks"]), 2)
                self.assertGreaterEqual(len(guide["examples"]), 1)
                for check in guide["checks"]:
                    self.assertEqual(sum(option["correct"] for option in check["options"]), 1)
                    self.assertTrue(all(option["explanation"] for option in check["options"]))
                for example in guide["examples"]:
                    board = chess.Board(example["fen"])
                    self.assertTrue(board.is_valid())
                    self.assertEqual(len(example["notes"]), len(example["moves"]) + 1)
                    self.assertTrue(all(note.strip() for note in example["notes"]))
                    for san in example["moves"]:
                        move = board.parse_san(san)
                        self.assertIn(move, board.legal_moves)
                        self.assertEqual(san, board.san(move))
                        board.push(move)
                        self.assertTrue(board.is_valid())


if __name__ == "__main__":
    unittest.main()
