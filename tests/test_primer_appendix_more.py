"""Regression checks for playable source compositions, not prose wording."""
import importlib.util
from pathlib import Path
import chess
import unittest
from functools import lru_cache


def content():
    path = Path(__file__).resolve().parents[1] / 'core/primer_appendix_more.py'
    assert path.exists(), 'Three-mover and more-mover teaching is missing'
    spec = importlib.util.spec_from_file_location('appendix_more_test', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_every_source_problem_has_playable_teaching():
    module = content()
    ids = {f'app-three-{i:02}' for i in range(1,21)} | {f'app-more-{i:02}' for i in range(1,16)}
    assert set(module.GUIDES) == ids
    assert {item['id'] for item in module.EXERCISES} == ids
    for item in module.EXERCISES:
        board = chess.Board(item['fen'])
        assert board.is_valid(), item['id']
        assert sum(bool(choice[1]) for choice in item['choices']) == 1, item['id']
        for san, _, _ in item['choices']:
            move = board.parse_san(san)
            assert board.san(move) == san, (item['id'], san)
        for ex in module.GUIDES[item['id']]['examples']:
            board = chess.Board(ex['fen'])
            assert board.is_valid(), item['id']
            assert len(ex['notes']) == len(ex['moves']) + 1, item['id']
            for san in ex['moves']:
                move = board.parse_san(san)
                assert board.san(move) == san, (item['id'], san)
                board.push(move)
            assert board.is_checkmate(), (item['id'], ex['title'], board.fen())


def test_source_exception_checking_key_and_long_mate_are_retained():
    module = content()
    items = {item['id']: item for item in module.EXERCISES}
    assert next(c[0] for c in items['app-three-01']['choices'] if c[1]) == 'Qh7+'
    assert max(len(ex['moves']) for ex in module.GUIDES['app-more-11']['examples']) == 33
    assert len(module.GUIDES['app-more-11']['examples']) >= 2


@lru_cache(maxsize=None)
def _white_can_mate(fen, plies):
    board = chess.Board(fen)
    if board.is_checkmate():
        return board.turn == chess.BLACK
    if plies == 0 or board.is_stalemate():
        return False
    moves = list(board.legal_moves)
    if board.turn == chess.WHITE:
        for move in moves:
            board.push(move)
            wins = _white_can_mate(board.epd(), plies - 1)
            board.pop()
            if wins:
                return True
        return False
    for move in moves:
        board.push(move)
        wins = _white_can_mate(board.epd(), plies - 1)
        board.pop()
        if not wins:
            return False
    return bool(moves)


class AppendixMoreTests(unittest.TestCase):
    def test_every_source_problem_has_playable_teaching(self):
        test_every_source_problem_has_playable_teaching()

    def test_checking_key_and_both_long_finishes(self):
        test_source_exception_checking_key_and_long_mate_are_retained()

    def test_three_move_keys_cover_every_legal_defence(self):
        for item in content().EXERCISES:
            if not item['id'].startswith('app-three-'):
                continue
            with self.subTest(problem=item['id']):
                board = chess.Board(item['fen'])
                board.push_san(next(c[0] for c in item['choices'] if c[1]))
                self.assertTrue(_white_can_mate(board.epd(), 4))
                _white_can_mate.cache_clear()

    def test_source_plan_choices_grade_without_unknown_objective(self):
        from core.primer import _lesson, grade
        from core.primer_build import lesson as build_lesson, step
        for item in content().EXERCISES:
            with self.subTest(problem=item['id']):
                self.assertIsNone(item['objective'])
                lesson = _lesson(build_lesson(11, item["id"], item["title"], item["summary"],
                    [step(item["fen"], item["inventory"])], item["prompt"], item["choices"],
                    objective=item.get("objective")))
                for san, correct, _ in item['choices']:
                    self.assertEqual(grade(lesson, san).correct, correct)


if __name__ == '__main__':
    unittest.main()
