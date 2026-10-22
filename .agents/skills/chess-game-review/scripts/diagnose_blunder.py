#!/usr/bin/env python3
"""Diagnose tactical blunders and classify mistakes with python-chess."""

import argparse
import sys
import chess

PIECE_NAMES = {
    chess.PAWN: "pawn",
    chess.KNIGHT: "knight",
    chess.BISHOP: "bishop",
    chess.ROOK: "rook",
    chess.QUEEN: "queen",
    chess.KING: "king",
}


def diagnose(fen: str, played_move_str: str, best_move_str: str | None = None):
    board = chess.Board(fen)
    player_color = board.turn
    opponent_color = not player_color

    try:
        played_move = board.parse_san(played_move_str)
    except ValueError:
        played_move = chess.Move.from_uci(played_move_str)

    if played_move not in board.legal_moves:
        print(f"Error: played move {played_move_str} is not legal in {fen}", file=sys.stderr)
        sys.exit(1)

    moving_piece = board.piece_at(played_move.from_square)
    moving_piece_name = PIECE_NAMES.get(moving_piece.piece_type if moving_piece else None, "piece")

    # Push played move to analyze the board after
    board.push(played_move)

    findings = []
    category = "tactical_oversight"

    # 1. Did the opponent gain immediate checkmate?
    for reply in board.legal_moves:
        board.push(reply)
        if board.is_checkmate():
            findings.append(f"Allows immediate checkmate with {board.san(reply)}!")
            category = "king_safety"
            board.pop()
            break
        board.pop()

    # 2. Is the moved piece hanging?
    to_sq = played_move.to_square
    attackers = board.attackers(opponent_color, to_sq)
    defenders = board.attackers(player_color, to_sq)
    if attackers and not defenders:
        findings.append(f"The {moving_piece_name} on {chess.square_name(to_sq)} is completely undefended and attacked by opponent!")
        category = "hanging_piece"
    elif len(attackers) > len(defenders):
        findings.append(f"The {moving_piece_name} on {chess.square_name(to_sq)} has more attackers ({len(attackers)}) than defenders ({len(defenders)}).")
        category = "hanging_piece"

    # 3. Did any other piece become undefended and attacked?
    for sq in chess.SQUARES:
        p = board.piece_at(sq)
        if p and p.color == player_color and sq != to_sq and p.piece_type != chess.KING:
            p_attackers = board.attackers(opponent_color, sq)
            p_defenders = board.attackers(player_color, sq)
            if p_attackers and not p_defenders:
                findings.append(f"Leaves the {PIECE_NAMES[p.piece_type]} on {chess.square_name(sq)} undefended!")
                if category != "king_safety":
                    category = "hanging_piece"

    # 4. Opening check (first 10 moves): early queen movement
    if board.fullmove_number <= 7 and moving_piece and moving_piece.piece_type == chess.QUEEN:
        findings.append("Early Queen development before minor pieces are developed.")
        if category == "tactical_oversight":
            category = "opening_principle_violation"

    print("=== Blunder Diagnosis ===")
    print(f"Position FEN: {fen}")
    print(f"Move played: {played_move_str}")
    if best_move_str:
        print(f"Engine recommendation: {best_move_str}")
    print(f"Classified Category: {category}")
    print("Concrete tactical consequences:")
    if findings:
        for f in findings:
            print(f"  - {f}")
    else:
        print("  - Subtle positional or calculation loss (no immediate hanging piece or mate).")


def main():
    parser = argparse.ArgumentParser(description="Diagnose chess mistake.")
    parser.add_argument("--fen", required=True, help="FEN before mistake was played")
    parser.add_argument("--played", required=True, help="Mistake move (SAN or UCI)")
    parser.add_argument("--best", help="Best engine move (SAN or UCI)")

    args = parser.parse_args()
    diagnose(args.fen, args.played, args.best)


if __name__ == "__main__":
    main()
