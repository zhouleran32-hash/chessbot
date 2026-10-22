"""Drag-and-drop study board shared by game review and the primer.

The visible board is Lichess chessground. Python still decides which moves are
legal and how a move is graded.
"""

import chess
import streamlit as st


_BOARD = None

_HTML = """
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/chessground@9.1.1/assets/chessground.base.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/chessground@9.1.1/assets/chessground.brown.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/chessground@9.1.1/assets/chessground.cburnett.css">
<div class="frame">
  <div id="bar" hidden><i></i></div>
  <div id="rank-labels" class="board-axis" aria-label="Ranks, top to bottom"></div>
  <div id="board"></div>
  <div id="file-labels" class="board-axis" aria-label="Files, left to right"></div>
</div>
"""

_CSS = """
:host { display: block; }
.frame {
  box-sizing: border-box;
  width: 100%;
  max-width: 560px;
  margin-inline: auto;
  padding: 10px;
  display: grid;
  grid-template-columns: 24px minmax(0, 1fr);
  grid-template-areas: "ranks board" ". files";
  gap: 4px;
  align-items: stretch;
  border: 1px solid var(--st-border-color, #39463d);
  border-radius: 14px;
  background: var(--st-secondary-background-color, #202925);
  color: var(--st-text-color, #ecebdc);
}
.frame.with-bar {
  grid-template-columns: 12px 24px minmax(0, 1fr);
  grid-template-areas: "bar ranks board" ". . files";
  column-gap: 8px;
}
#bar { grid-area: bar; width: 12px; border-radius: 6px; background: #131b17; display: none; flex-direction: column-reverse; overflow: hidden; }
#bar.show { display: flex; }
#bar i { display: block; width: 100%; background: #e9e6d5; }
.board-axis {
  display: grid;
  min-width: 0;
  min-height: 0;
  color: var(--st-text-color, #ecebdc);
  font: 700 14px / 1 ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  user-select: none;
}
.board-axis span { display: flex; align-items: center; justify-content: center; }
#rank-labels { grid-area: ranks; grid-template-rows: repeat(8, minmax(0, 1fr)); }
#file-labels { grid-area: files; grid-template-columns: repeat(8, minmax(0, 1fr)); height: 24px; }
#board {
  grid-area: board;
  min-width: 0;
  width: 100%;
  aspect-ratio: 1;
  align-self: flex-start;
  position: relative;
  border-radius: 5px;
  overflow: hidden;
  box-shadow: 0 3px 12px rgba(0, 0, 0, 0.22);
}
#board cg-container, #board cg-board { width: 100% !important; height: 100% !important; }
#board cg-board {
  background-color: #e9e6d5;
  background-image: conic-gradient(#849781 25%, #e9e6d5 0 50%, #849781 0 75%, #e9e6d5 0);
  background-size: 25% 25%;
}
#board square.last-move { background-color: rgba(232, 188, 92, 0.46); }
#board square.selected { background-color: rgba(70, 151, 177, 0.50); }
#board square.check { background: radial-gradient(ellipse at center, #e4504d 0%, rgba(211, 64, 63, 0.85) 35%, rgba(211, 64, 63, 0) 75%); }
"""

_JS = """
export default function (component) {
  const { data, parentElement, setTriggerValue } = component;
  const frame = parentElement.querySelector(".frame");
  const boardEl = parentElement.querySelector("#board");
  const bar = parentElement.querySelector("#bar");
  const fill = parentElement.querySelector("#bar i");
  if (!boardEl || !bar || !fill) return;

  const orientation = data.orientation === "black" ? "black" : "white";
  const renderAxis = (selector, labels) => {
    const axis = parentElement.querySelector(selector);
    axis.replaceChildren(...Array.from(labels, (label) => {
      const span = document.createElement("span");
      span.textContent = label;
      return span;
    }));
  };
  renderAxis("#file-labels", orientation === "black" ? "HGFEDCBA" : "ABCDEFGH");
  renderAxis("#rank-labels", orientation === "black" ? "12345678" : "87654321");
  frame.classList.toggle("with-bar", data.loss != null || data.reserveLossBar === true);

  if (data.loss == null) {
    bar.classList.remove("show");
  } else {
    bar.classList.add("show");
    const portion = Math.max(8, Math.min(100, (Number(data.loss) / 8) * 100));
    fill.style.height = portion + "%";
    bar.title = "Lost " + data.loss + " pawns";
  }

  const paint = (Chessground) => {
    const dests = new Map(Object.entries(data.dests || {}));
    const config = {
      fen: data.fen,
      orientation: orientation,
      turnColor: data.turn || "white",
      // Keep coordinates in dedicated gutters, away from pieces and grid lines.
      coordinates: false,
      viewOnly: !data.interactive,
      lastMove: data.lastMove || undefined,
      check: data.check || false,
      animation: { enabled: true, duration: 180 },
      movable: {
        free: false,
        color: data.interactive ? data.turn : undefined,
        dests: dests,
        showDests: true,
        events: {
          after: (orig, dest) => setTriggerValue("move", { from: orig, to: dest }),
        },
      },
      premovable: { enabled: false },
      draggable: { enabled: !!data.interactive },
      selectable: { enabled: !!data.interactive },
      drawable: {
        enabled: false,
        visible: true,
        autoShapes: (data.arrows || []).map((arrow) => ({
          orig: arrow.from,
          dest: arrow.to,
          brush: arrow.brush || "green",
        })),
      },
    };
    if (!boardEl._ground) boardEl._ground = Chessground(boardEl, config);
    else boardEl._ground.set(config);
    requestAnimationFrame(() => {
      if (boardEl._ground) boardEl._ground.redrawAll();
    });
    if (!boardEl._observer) {
      boardEl._observer = new ResizeObserver(() => {
        const rect = boardEl.getBoundingClientRect();
        if (rect.width > 8 && rect.height > 8 && boardEl._ground) {
          boardEl._ground.redrawAll();
        }
      });
      boardEl._observer.observe(boardEl);
    }
  };

  if (boardEl._Chessground) {
    paint(boardEl._Chessground);
    return;
  }
  if (boardEl._loading) return;
  boardEl._loading = true;
  import("https://cdn.jsdelivr.net/npm/chessground@9.1.1/+esm")
    .then((mod) => {
      boardEl._Chessground = mod.Chessground;
      paint(mod.Chessground);
    })
    .catch(() => {
      boardEl.textContent = "The board could not load. Check the network connection and refresh.";
    });
}
"""


def _component():
    global _BOARD
    if _BOARD is None:
        _BOARD = st.components.v2.component(
            "study_board",
            html=_HTML,
            css=_CSS,
            js=_JS,
        )
    return _BOARD


def legal_destinations(fen: str) -> dict[str, list[str]]:
    """Map each origin square to the destinations chessground may allow."""
    board = chess.Board(fen)
    dests: dict[str, list[str]] = {}
    for move in board.legal_moves:
        origin = chess.square_name(move.from_square)
        target = chess.square_name(move.to_square)
        bucket = dests.setdefault(origin, [])
        if target not in bucket:
            bucket.append(target)
    return dests


def board_state(board: chess.Board) -> dict:
    """Turn and check marker for a python-chess position."""
    king = board.king(board.turn)
    return {
        "turn": "white" if board.turn == chess.WHITE else "black",
        "check": chess.square_name(king) if board.is_check() and king is not None else False,
    }


def chess_board(
    *,
    fen: str,
    orientation: str = "white",
    interactive: bool = False,
    dests: dict[str, list[str]] | None = None,
    arrows: list[dict] | None = None,
    last_move: list[str] | None = None,
    check: bool | str = False,
    turn: str = "white",
    loss: float | None = None,
    reserve_loss_bar: bool = False,
    key: str,
):
    """Mount the study board. A completed drag is `result.move` for this run."""
    return _component()(
        key=key,
        data={
            "fen": fen,
            "orientation": orientation,
            "interactive": interactive,
            "dests": dests or {},
            "arrows": arrows or [],
            "lastMove": list(last_move) if last_move else None,
            "check": check,
            "turn": turn,
            "loss": loss,
            "reserveLossBar": reserve_loss_bar,
        },
        on_move_change=lambda: None,
        width="stretch",
        height="content",
    )
