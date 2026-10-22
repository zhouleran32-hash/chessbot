---
name: chess-engine-and-board-dev
description: >-
  Build, test, and troubleshoot chess applications using python-chess, Stockfish UCI,
  chess.svg rendering, and interactive Streamlit UI state management. Use when working on
  chess engine communication, PGN/FEN parsing, board SVGs, move input handling, promotion modals,
  or Streamlit session state persistence across views.
---

# Chess Engine & Interactive Board Development

Best practices for engineering chess software using `python-chess`, Stockfish UCI integration, SVG board rendering, and Streamlit state management.

---

## 1. python-chess Core Patterns

### Board State and Move Identity
Always compare move identity with `chess.Move` objects rather than raw strings:

```python
import chess

board = chess.Board("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1")

# Safe SAN parsing
try:
    move = board.parse_san("c5")  # Sicilian Defense
except ValueError:
    ...

# Legality check
if move in board.legal_moves:
    board.push(move)

# Accessing piece info
piece = board.piece_at(chess.C5)  # chess.Piece(chess.PAWN, chess.BLACK)
```

### SVG Board Rendering
Use `chess.svg.board()` with explicit styling to communicate threats and moves clearly:

```python
import chess.svg

svg_data = chess.svg.board(
    board=board,
    orientation=chess.WHITE,
    lastmove=move,
    check=board.king(board.turn) if board.is_check() else None,
    arrows=[chess.svg.Arrow(chess.E2, chess.E4, color="#1b783780")],
    fill={chess.C5: "#cc000040"},  # Highlight specific square
    size=420,
)
```

---

## 2. Stockfish UCI Management

### Robust Engine Lifecycle
UCI engines are external subprocesses. Always guard against missing binaries, timeouts, and process leaks:

```python
import chess.engine

def analyze_position(fen: str, stockfish_path: str, depth: int = 15):
    board = chess.Board(fen)
    with chess.engine.SimpleEngine.popen_uci(stockfish_path) as engine:
        limit = chess.engine.Limit(depth=depth, time=1.0)
        info = engine.analyse(board, limit)
        score = info["score"].relative  # Normalized to side to move
        
        # Distinguish mate scores from centipawn evaluations
        if score.is_mate():
            eval_str = f"M{score.mate()}"
        else:
            eval_str = f"{score.score() / 100:+.2f}"
            
        pv_moves = info.get("pv", [])
        return eval_str, pv_moves
```

---

## 3. Streamlit Chess UI State Patterns

Streamlit reruns the script top-to-bottom on every user interaction. Without proper state encapsulation, board state and multi-step moves will reset.

### Rule 1: Two-Click Move Execution & Promotion
When a player clicks a piece, store `selected_square` in `st.session_state`.
- **First click**: Set `st.session_state.selected_square = sq`. Highlight that square in the SVG.
- **Second click on different square**:
  - Check if move is a pawn promotion (`pawn reaching rank 8 or rank 1`).
  - If promotion: pause and render a promotion selector (`Q`, `R`, `B`, `N`).
  - If regular legal move: `board.push(move)` and clear `selected_square`.
- **Cancellation**: If user clicks an invalid square or another of their own pieces, update `selected_square` and cancel any pending promotion cleanly.

### Rule 2: Widget State vs Session State Survival
Streamlit destroys widget keys when tabs switch or views toggle (e.g. switching between "Your games" and "The Soviet Chess Primer"):
- Never rely solely on `st.session_state["worked_example_dropdown"]`.
- Store the canonical application state in dedicated, persistent session keys (e.g., `st.session_state.primer_example_choices` or `st.session_state.current_lesson_id`).
- When changing players, explicitly reset choices and reload that player's saved database progress.

### Rule 3: Replay Variation Navigation
- Provide `<` and `>` buttons below worked-example boards.
- Keep the variation move cursor in `st.session_state.replay_cursor`.
- Bounding: Ensure cursor clamps between `0` and `len(variation_moves)`.

---

## 4. Testing & Verification

Always run the full regression test suite after modifying core logic or UI components:

```bash
work/verify-env/bin/python -m unittest discover -s tests
```

For testing Streamlit app components without browser interaction, use Streamlit's `AppTest`:

```python
from streamlit.testing.v1 import AppTest

at = AppTest.from_file("app.py", default_timeout=10)
at.run()
assert not at.exception
```
