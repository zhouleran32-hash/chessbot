"""Small exact searches for composition exercises; no engine is required."""
from functools import lru_cache

import chess


@lru_cache(maxsize=2048)
def mate_in_two(fen: str, uci: str) -> tuple[bool, str | None]:
    """Check a proposed key against every reply, returning a refutation if any.

    A quicker mate also meets the 'within two moves' limit. A stalemate or
    other terminal draw cannot succeed through an empty list of defences.
    The attacking side is inferred from the position, so Black tasks work too.
    """
    board = chess.Board(fen)
    move = chess.Move.from_uci(uci)
    if move not in board.legal_moves:
        raise ValueError('The proposed key must be legal.')
    board.push(move)
    if board.is_checkmate():
        return True, None
    if board.is_game_over():
        return False, None
    for defence in list(board.legal_moves):
        notation = board.san(defence)
        board.push(defence)
        mating_reply = False
        if not board.is_game_over():
            for reply in list(board.legal_moves):
                board.push(reply)
                mating_reply = board.is_checkmate()
                board.pop()
                if mating_reply:
                    break
        board.pop()
        if not mating_reply:
            return False, notation
    return True, None
