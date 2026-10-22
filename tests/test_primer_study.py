"""Worked examples replay legally and concept checks explain the chosen answer."""

import unittest
from types import SimpleNamespace
from unittest.mock import patch
import chess

from core.primer_study import example_frames, check_concept, concept_option_order, guide_for


class StudyTests(unittest.TestCase):
    def test_chapter_three_loads_original_and_additional_guides(self):
        original = {"sections": ("Original teaching",)}
        extra = {"sections": ("Additional teaching",)}
        modules = {
            "core.primer_guides_chapter3": SimpleNamespace(GUIDES={"original": original}),
            "core.primer_guides_chapter3_extra": SimpleNamespace(GUIDES={"new-topic": extra}),
        }
        with patch("core.primer_study.import_module", side_effect=modules.__getitem__):
            self.assertIs(guide_for("original", 3), original)
            self.assertIs(guide_for("new-topic", 3), extra)
            self.assertIsNone(guide_for("unknown", 3))

    def test_example_replays_both_sides_with_notes_at_each_position(self):
        frames = example_frames({
            "fen": chess.STARTING_FEN, "moves": ("e4", "e5", "Nf3"),
            "notes": ("Start.", "White takes central space.", "Black contests it.", "White develops and attacks e5."),
        })
        self.assertEqual(len(frames), 4)
        final = chess.Board(frames[-1].fen)
        self.assertEqual(final.piece_at(chess.F3), chess.Piece(chess.KNIGHT, chess.WHITE))
        self.assertIsNone(final.piece_at(chess.G1))
        self.assertEqual(frames[-1].move_label, "2. Nf3")
        self.assertEqual(frames[-1].note, "White develops and attacks e5.")

    def test_illegal_or_unannotated_example_is_rejected(self):
        for example in (
            {"fen": chess.STARTING_FEN, "moves": ("e5",), "notes": ("Start.", "Wrong move.")},
            {"fen": chess.STARTING_FEN, "moves": ("e4",), "notes": ("Missing move explanation.",)},
            {"fen": chess.STARTING_FEN, "moves": ("e4+",), "notes": ("Start.", "This move is incorrectly labelled check.")},
            {"fen": chess.STARTING_FEN, "moves": ("--",), "notes": ("Start.", "Passing is not a legal move.")},
        ):
            with self.subTest(example=example), self.assertRaises(ValueError):
                example_frames(example)

    def test_concept_check_returns_the_explanation_for_the_chosen_option(self):
        guide = {"checks": ({"id": "king", "prompt": "Can a king move into check?", "options": (
            {"text": "Yes", "correct": False, "explanation": "A king must stay off attacked squares."},
            {"text": "No", "correct": True, "explanation": "Correct: king safety is a rule, not just advice."},
        )},)}
        wrong = check_concept(guide, "king", 0)
        self.assertFalse(wrong.correct)
        self.assertIn("attacked squares", wrong.explanation)
        self.assertTrue(check_concept(guide, "king", 1).correct)
        with self.assertRaises(ValueError):
            check_concept(guide, "king", -1)

    def test_example_cannot_continue_after_a_draw_has_ended_the_game(self):
        with self.assertRaisesRegex(ValueError, "ended"):
            example_frames({
                "fen": "k7/8/8/8/8/3r4/8/5BK1 w - - 0 1",
                "moves": ("Bxd3", "Kb8"),
                "notes": ("A bishop can capture the rook.", "Only a lone bishop remains: drawn.", "This is too late."),
            })

    def test_correct_answer_placement_varies_and_stays_stable_on_rerun(self):
        orders = []
        for number in range(12):
            question = {"id": f"question-{number}", "options": ({}, {}, {})}
            order = concept_option_order("fixture", question)
            self.assertCountEqual(order, [0, 1, 2])
            self.assertEqual(order, concept_option_order("fixture", question))
            orders.append(order.index(0))
        self.assertEqual(set(orders), {0, 1, 2})


if __name__ == "__main__":
    unittest.main()
