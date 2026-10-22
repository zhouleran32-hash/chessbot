"""Appendix warm-ups teach complete tasks with playable, correctly graded boards."""
import importlib.util
import unittest

import chess
from core.primer import _lesson, grade
from core.primer_build import lesson, step
from core.primer_study import example_frames


class AppendixFoundationTests(unittest.TestCase):
    def content(self):
        self.assertIsNotNone(importlib.util.find_spec('core.primer_appendix_foundations'))
        from core.primer_appendix_foundations import GUIDES, EXERCISES
        return GUIDES, EXERCISES

    def test_warmups_can_be_replayed_and_graded(self):
        guides, exercises = self.content()
        for item in exercises:
            with self.subTest(lesson=item['id']):
                g = guides[item['id']]
                for example in g['examples']:
                    example_frames(example)
                spec = lesson(11, item['id'], item['title'], item['summary'],
                              [step(item['fen'], item['inventory']), step(item['fen'], item['prompt'])],
                              item['prompt'], item['choices'], objective=item.get('objective'))
                for choice in _lesson(spec).choices:
                    self.assertEqual(grade(_lesson(spec), choice.san).correct, choice.correct)

    def test_model_mate_and_draw_have_distinct_endpoints(self):
        guides, _ = self.content()
        mate = example_frames(guides['app-model-mate']['examples'][0])[-1]
        drawn = example_frames(guides['app-drawing-task']['examples'][0])[-1]
        self.assertTrue(chess.Board(mate.fen).is_checkmate())
        self.assertTrue(chess.Board(drawn.fen).is_stalemate())


if __name__ == '__main__':
    unittest.main()
