"""Position helpers shared by the primer lessons."""

import chess


def after(moves, start=None):
    board = chess.Board(start) if start else chess.Board()
    for san in moves:
        board.push_san(san)
    if not board.is_valid():
        raise ValueError(f"Invalid line {moves}: {board.fen()}")
    return board.fen()


def custom(pieces, turn="w", castle="-", ep=None):
    board = chess.Board.empty()
    for square, symbol in pieces.items():
        board.set_piece_at(chess.parse_square(square), chess.Piece.from_symbol(symbol))
    board.turn = chess.WHITE if turn == "w" else chess.BLACK
    rights = 0
    for flag, square in {"K": chess.H1, "Q": chess.A1, "k": chess.H8, "q": chess.A8}.items():
        if flag in castle:
            rights |= chess.BB_SQUARES[square]
    board.castling_rights = rights
    if ep:
        board.ep_square = chess.parse_square(ep)
    if not board.is_valid():
        raise ValueError(f"Invalid position {pieces}: {board.fen()}")
    return board.fen()


def lesson(chapter, lesson_id, title, explanation, steps, prompt, choices, *, objective=None):
    return {
        "chapter": chapter,
        "id": lesson_id,
        "title": title,
        "explanation": " ".join(explanation.split()),
        "steps": steps,
        "quiz_fen": steps[-1][0],
        "prompt": " ".join(prompt.split()),
        "choices": choices,
        "objective": objective,
    }


def step(fen, caption, arrows=()):
    return (fen, caption, arrows)
