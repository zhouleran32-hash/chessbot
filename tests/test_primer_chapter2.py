"""Chess-grounded regression checks for chapter two teaching and practice."""

import importlib
import importlib.util
import unittest

import chess

from core.primer_chapter2 import LESSONS


class ChapterTwoTeachingTests(unittest.TestCase):
    def guides(self):
        self.assertIsNotNone(
            importlib.util.find_spec("core.primer_guides_chapter2"),
            "Chapter two needs substantive source-mapped teaching guides.",
        )
        return importlib.import_module("core.primer_guides_chapter2").GUIDES

    def test_all_choice_san_is_canonical_and_mates_are_never_rejected(self):
        for spec in LESSONS:
            board = chess.Board(spec["quiz_fen"])
            for san, correct, _ in spec["choices"]:
                with self.subTest(lesson=spec["id"], san=san):
                    move = board.parse_san(san)
                    self.assertEqual(board.san(move), san)
                    after = board.copy()
                    after.push(move)
                    if after.is_checkmate():
                        self.assertTrue(correct, "An actual mate cannot be a wrong answer.")
            if spec["id"] in {"queen-mates", "avoid-stalemate"}:
                self.assertEqual(spec.get("objective"), "checkmate")

    def test_promotion_exercise_acknowledges_rook_also_wins(self):
        spec = next(item for item in LESSONS if item["id"] == "queening-a-pawn")
        by_move = {san: correct for san, correct, _ in spec["choices"]}
        self.assertTrue(by_move.get("e8=Q+"))
        self.assertTrue(by_move.get("e8=R+"), "A rook also forces mate against a lone king.")
        self.assertFalse(by_move.get("e8=N"))

    def test_missing_source_pawn_and_mating_skills_are_taught(self):
        found = {spec["id"] for spec in LESSONS}
        self.assertTrue({
            "mating-method-two-bishops", "active-stalemate", "pawn-opposition",
            "pawn-fifth-rank", "rook-pawn-draw", "knight-pawn-stalemate",
        }.issubset(found))

    def test_every_lesson_has_substantive_source_mapped_guide(self):
        guides = self.guides()
        self.assertEqual(set(guides), {spec["id"] for spec in LESSONS})
        for lesson_id, guide in guides.items():
            with self.subTest(lesson=lesson_id):
                start, end = guide["pages"]
                self.assertLessEqual(35, start)
                self.assertLessEqual(start, end)
                self.assertLessEqual(end, 56)
                self.assertGreaterEqual(len(guide["goals"]), 2)
                self.assertGreaterEqual(len(guide["sections"]), 3)
                self.assertGreaterEqual(sum(len(section["body"].split()) for section in guide["sections"]), 300)
                self.assertGreaterEqual(len(guide["pitfalls"]), 2)
                self.assertEqual(len(guide["recap"]), 3)
                self.assertGreaterEqual(len(guide["checks"]), 2)
                for check in guide["checks"]:
                    self.assertEqual(sum(option["correct"] for option in check["options"]), 1)
                    self.assertTrue(all(option["explanation"].strip() for option in check["options"]))

    def test_every_example_is_a_legal_connected_line_with_a_note_per_position(self):
        for lesson_id, guide in self.guides().items():
            self.assertTrue(guide["examples"], lesson_id)
            for example in guide["examples"]:
                with self.subTest(lesson=lesson_id, example=example["title"]):
                    board = chess.Board(example["fen"])
                    self.assertTrue(board.is_valid())
                    self.assertGreater(len(example["moves"]), 0)
                    self.assertEqual(len(example["notes"]), len(example["moves"]) + 1)
                    for san in example["moves"]:
                        self.assertFalse(board.is_game_over(), f"Continuation after game ended: {san}")
                        move = board.parse_san(san)
                        self.assertEqual(board.san(move), san)
                        board.push(move)
                        self.assertTrue(board.is_valid())

    def test_major_mating_methods_reach_checkmate_in_a_connected_demonstration(self):
        guides = self.guides()
        for lesson_id in ("mating-method-queen", "mating-method-rook", "two-rook-mates", "mating-method-two-bishops"):
            examples = guides[lesson_id]["examples"]
            complete = []
            for example in examples:
                board = chess.Board(example["fen"])
                for san in example["moves"]:
                    board.push_san(san)
                if len(example["moves"]) >= 7 and board.is_checkmate():
                    complete.append(example)
            self.assertTrue(complete, f"{lesson_id} must teach the process through an actual mate.")

    def test_two_knights_defence_tests_the_actual_corner_trap(self):
        spec = next(item for item in LESSONS if item["id"] == "two-knights-draw")
        board = chess.Board(spec["quiz_fen"])
        self.assertTrue(board.is_check())
        choices = {san: correct for san, correct, _ in spec["choices"]}
        self.assertTrue(choices.get("Kf8"))
        self.assertFalse(choices.get("Kh8"))
        board.push_san("Kh8")
        board.push_san("Nef7#")
        self.assertTrue(board.is_checkmate())


if __name__ == "__main__":
    unittest.main()
