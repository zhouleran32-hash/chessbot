"""Exercise the authored appendix boards, lines, and full mate-in-two promise."""
import importlib
import importlib.util

import chess
import unittest


KEYS = ('Qf7', 'Rd2', 'Rg4', 'Qd7', 'Qa1', 'Qh8', 'a4', 'Qg3', 'Bc7', 'Ba4',
        'Rf1', 'Bf5', 'Nf2', 'Kg7', 'Qh1', 'Qg8', 'Qb2', 'Qf1', 'Ne8', 'Qf6')
DEFENCE_COUNTS = (31, 4, 6, 32, 4, 5, 16, 19, 15, 18, 13, 5, 21, 2, 1, 24, 18, 3, 24, 25)


def content():
    assert importlib.util.find_spec('core.primer_appendix_two') is not None, 'The two-mover teaching module is missing'
    return importlib.import_module('core.primer_appendix_two')


def has_mate_in_one(board):
    for move in list(board.legal_moves):
        board.push(move)
        mate = board.is_checkmate()
        board.pop()
        if mate:
            return True
    return False


def forces_mate_in_two(board, move):
    board = board.copy()
    board.push(move)
    if board.is_checkmate():
        return True
    replies = list(board.legal_moves)
    if not replies:
        return False
    for reply in replies:
        board.push(reply)
        succeeds = has_mate_in_one(board)
        board.pop()
        if not succeeds:
            return False
    return True


def test_all_twenty_have_accessible_teaching_and_practice():
    module = content()
    expected = {f'app-two-{n:02d}' for n in range(1, 21)}
    assert set(module.GUIDES) == expected
    assert {x['id'] for x in module.EXERCISES} == expected
    assert len(module.EXERCISES) == 20
    for exercise in module.EXERCISES:
        teaching = module.GUIDES[exercise['id']]
        assert len(teaching['sections']) >= 4
        assert len(teaching['checks']) >= 2
        assert teaching['examples']
        assert exercise['objective'] == 'mate_in_2'
        for concept in teaching['checks']:
            assert sum(option['correct'] for option in concept['options']) == 1


def check_source_key(number):
    exercise = content().EXERCISES[number - 1]
    board = chess.Board(exercise['fen'])
    assert board.is_valid()
    assert board.turn == chess.WHITE
    key = board.parse_san(KEYS[number - 1])
    assert forces_mate_in_two(board, key), exercise['id']
    after = board.copy()
    after.push(key)
    assert after.legal_moves.count() == DEFENCE_COUNTS[number - 1]
    solutions = [board.san(move) for move in list(board.legal_moves) if forces_mate_in_two(board, move)]
    assert solutions == [KEYS[number - 1]]


def test_every_practice_choice_is_legal_canonical_and_graded_by_the_real_objective():
    for exercise in content().EXERCISES:
        board = chess.Board(exercise['fen'])
        assert any(ok for _, ok, _ in exercise['choices'])
        for san, correct, explanation in exercise['choices']:
            move = board.parse_san(san)
            assert board.san(move) == san
            assert forces_mate_in_two(board, move) == correct
            assert explanation.strip()


def test_all_narrated_branches_are_canonical_and_reach_checkmate():
    for key, teaching in content().GUIDES.items():
        for replay in teaching['examples']:
            board = chess.Board(replay['fen'])
            assert board.is_valid(), key
            assert len(replay['notes']) == len(replay['moves']) + 1, key
            assert all(note.strip() for note in replay['notes'])
            for san in replay['moves']:
                move = board.parse_san(san)
                assert board.san(move) == san, (key, san)
                board.push(move)
            assert board.is_checkmate(), (key, replay['title'])


def test_complete_defence_maps_cover_each_legal_reply_and_give_real_mates():
    module = content()
    for exercise in module.EXERCISES:
        board = chess.Board(exercise['fen'])
        board.push_san(KEYS[int(exercise['id'][-2:]) - 1])
        answers = module.DEFENCE_ANSWERS[exercise['id']]
        assert set(answers) == {board.san(move) for move in board.legal_moves}
        for defence, finish in answers.items():
            branch = board.copy()
            branch.push_san(defence)
            move = branch.parse_san(finish)
            assert branch.san(move) == finish
            branch.push(move)
            assert branch.is_checkmate(), (exercise['id'], defence, finish)


def test_babson_initial_double_push_and_gottschall_underpromotion_are_preserved():
    module = content()
    babson = chess.Board(module.EXERCISES[6]['fen'])
    assert babson.piece_at(chess.A2) == chess.Piece(chess.PAWN, chess.WHITE)
    assert babson.parse_san('a4') in babson.legal_moves
    gottschall = module.GUIDES['app-two-12']['examples']
    assert any(replay['moves'] == ('Bf5', 'exf5', 'g8=N#') for replay in gottschall)


def test_source_keys_survive_every_defence_and_have_no_other_keys():
    for number in range(1, 21):
        check_source_key(number)


def load_tests(loader, tests, pattern):
    return unittest.TestSuite(unittest.FunctionTestCase(value)
                              for name, value in globals().items()
                              if name.startswith('test_') and callable(value))
