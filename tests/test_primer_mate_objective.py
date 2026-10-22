"""Mate-in-two tasks must prove the result against every legal defence."""
import unittest

from core.primer import Choice, Lesson, grade


class MateObjectiveTests(unittest.TestCase):
    def task(self, fen, choices=()):
        return Lesson('fixture', 11, 'Mate within two', '', (), fen,
                      'Force mate within two moves.',
                      choices, 'white', 'mate_in_2')

    def test_accepts_alternate_key_outside_suggested_choices(self):
        task = self.task('7k/8/5K2/5Q2/8/8/8/8 w - - 0 1',
                         (Choice('Qd7', True, 'A quiet key.'),))
        self.assertTrue(grade(task, 'Qd7').correct)
        self.assertTrue(grade(task, 'Qg5').correct)

    def test_rejects_check_that_allows_escape_and_stalemating_key(self):
        task = self.task('7k/8/5K2/5Q2/8/8/8/8 w - - 0 1')
        self.assertFalse(grade(task, 'Qh5+').correct)
        self.assertFalse(grade(task, 'Qg6').correct)

    def test_each_defence_can_require_a_different_mating_reply(self):
        task = self.task('6k1/8/5K2/4Q3/8/8/8/8 w - - 0 1')
        self.assertTrue(grade(task, 'Qc7').correct)

    def test_works_for_black_and_accepts_immediate_mate_within_limit(self):
        black = self.task('8/8/8/8/5q2/5k2/8/7K b - - 0 1')
        self.assertTrue(grade(black, 'Qd2').correct)
        self.assertFalse(grade(black, 'Qh4+').correct)
        task = self.task('7k/8/5KQ1/8/8/8/8/8 w - - 0 1')
        self.assertTrue(grade(task, 'Qg7#').correct)


if __name__ == '__main__':
    unittest.main()
