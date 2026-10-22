#!/usr/bin/env python3
"""CLI utility to verify FEN positions, move sequences, and defensive replies."""

import argparse
import sys
import chess


def main():
    parser = argparse.ArgumentParser(description="Verify chess FEN and move sequences.")
    parser.add_argument("--fen", required=True, help="Starting FEN string")
    parser.add_argument("--move", help="Test move (SAN or UCI)")
    parser.add_argument("--moves", nargs="*", help="Sequence of moves to play sequentially")
    parser.add_argument("--check-defenses", action="store_true", help="List all legal opponent replies after --move")

    args = parser.parse_args()

    try:
        board = chess.Board(args.fen)
    except ValueError as e:
        print(f"ERROR: Invalid FEN: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Starting FEN valid. Side to move: {'White' if board.turn == chess.WHITE else 'Black'}")
    print(f"Legal moves count: {board.legal_moves.count()}")

    if args.move:
        try:
            # Try parsing as SAN or UCI
            try:
                move_obj = board.parse_san(args.move)
            except ValueError:
                move_obj = chess.Move.from_uci(args.move)
            
            if move_obj not in board.legal_moves:
                print(f"ERROR: Move {args.move} is not legal in this position!", file=sys.stderr)
                sys.exit(1)
            
            board.push(move_obj)
            print(f"Move {args.move} is LEGAL. Resulting FEN: {board.fen()}")

            if args.check_defenses:
                print(f"Opponent ({'White' if board.turn == chess.WHITE else 'Black'}) has {board.legal_moves.count()} legal replies:")
                for m in board.legal_moves:
                    san_m = board.san(m)
                    print(f"  - {san_m} ({m.uci()})")

        except Exception as e:
            print(f"ERROR parsing move: {e}", file=sys.stderr)
            sys.exit(1)

    if args.moves:
        print("\nVerifying move sequence:")
        for idx, m_str in enumerate(args.moves, start=1):
            try:
                try:
                    m = board.parse_san(m_str)
                except ValueError:
                    m = chess.Move.from_uci(m_str)

                if m not in board.legal_moves:
                    print(f"ERROR at step {idx}: Move {m_str} is ILLEGAL!", file=sys.stderr)
                    sys.exit(1)
                
                san = board.san(m)
                board.push(m)
                print(f"  Step {idx}: {san} (FEN: {board.fen()})")
            except Exception as e:
                print(f"ERROR processing {m_str}: {e}", file=sys.stderr)
                sys.exit(1)

        print("\nAll moves in sequence verified successfully!")


if __name__ == "__main__":
    main()
