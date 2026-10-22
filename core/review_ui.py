"""Interactive, independent move-by-move review using retained engine evidence."""

from collections import Counter
from functools import partial

import chess
import streamlit as st

from core.board_widget import board_state, chess_board
from core.coach import ChessCoach
from core.continuation import continuation_steps
from core.move_quality import QUALITY_ORDER


VIEWS = ["Before your move", "After your move", "Best continuation", "Reply to your move"]


def _reset_view() -> None:
    st.session_state.review_board_view = VIEWS[0]
    st.session_state.review_line_step = 0


def _step_move(plies: list[int], delta: int) -> None:
    index = plies.index(st.session_state.review_move)
    st.session_state.review_move = plies[max(0, min(len(plies) - 1, index + delta))]
    _reset_view()


def _select_table_move(table_key: str, plies: list[int]) -> None:
    event = st.session_state.get(table_key, {})
    selection = event.get("selection", {}).get("rows", [])
    if selection and 0 <= selection[0] < len(plies):
        st.session_state.review_move = plies[selection[0]]
        _reset_view()


def _reset_line_step() -> None:
    st.session_state.review_line_step = 0


def evaluation_label(move: dict, side: str) -> str:
    mate = move[f"mate_{side}"]
    cp = move[f"eval_{side}_cp"]
    if mate is not None:
        if mate == 0:
            return "Checkmate for you" if cp > 0 else "You are checkmated"
        return f"Mate {'for' if mate > 0 else 'against'} you in {abs(mate)}"
    return f"{cp / 100:+.2f}"


def _move_label(move: dict) -> str:
    dots = "." if move["color"] == "white" else "..."
    return f"{move['move_number']}{dots} {move['played_move']} · {move['classification']['label']}"


def render_move_review(game: dict, record: dict, user_rating: int) -> None:
    moves = record["moves"]
    if record["is_mock"]:
        st.warning("Mock analysis · development preview using a simple material search. Stockfish quality labels are unavailable.")
    else:
        st.caption("Independent Stockfish review · these estimates are not official Chess.com move classifications.")
    if not moves:
        st.info("This game contains no moves played by the selected player.")
        return
    counts = Counter(move["classification"]["key"] for move in moves)
    accuracy, blunders, reviewed = st.columns(3)
    published = game.get("accuracy")
    accuracy.metric("Accuracy", f"{published:.1f}%" if published is not None else "—", help="Only the accuracy published by Chess.com is displayed.")
    blunders.metric("Blunders", "—" if record["is_mock"] else counts["blunder"])
    reviewed.metric("Moves reviewed", len(moves))
    st.caption(
        "Accuracy is the score published by Chess.com; move labels below are independent."
        if published is not None else "Chess.com did not publish an accuracy score for this game."
    )
    if not record["is_mock"]:
        labels = {move["classification"]["key"]: move["classification"]["label"] for move in moves}
        st.caption(" · ".join(f"{labels[key]}: {counts[key]}" for key in QUALITY_ORDER if counts[key]))

    plies = [move["ply"] for move in moves]
    by_ply = {move["ply"]: move for move in moves}
    token = (game["game_url"], record["signature"])
    bookmarks = st.session_state.setdefault("review_move_bookmarks", {})
    if st.session_state.get("review_moves_for") != token or st.session_state.get("review_move") not in by_ply:
        st.session_state.review_moves_for = token
        default = next((move["ply"] for move in moves if move["classification"]["key"] in {"blunder", "mistake"}), plies[0])
        saved = bookmarks.get(game["game_url"], default)
        st.session_state.review_move = saved if saved in by_ply else default
        _reset_view()

    st.markdown("#### Every move you played")
    st.caption("Select a row or use the move menu below. Scores are from your side: positive means better for you.")
    table_key = f"move_table_{game['game_url']}_{record['signature'][:12]}"
    st.dataframe(
        [{"Move": f"{move['move_number']}{'.' if move['color'] == 'white' else '...'}",
          "Played": move["played_move"], "Assessment": move["classification"]["label"],
          "Before": evaluation_label(move, "before"), "After": evaluation_label(move, "after"),
          "Best move": move["best_move"],
          "Expected-points loss": None if record["is_mock"] else round(move["classification"]["loss"], 3)} for move in moves],
        hide_index=True, width="stretch", height=min(318, 38 + 35 * len(moves)),
        key=table_key, on_select=partial(_select_table_move, table_key, plies), selection_mode="single-row",
        # The callback executes before the move selector is rendered on the next run.
        alt="Every move played by this player, with independent assessments and evaluations.",
    )
    selected = st.selectbox("Review a move", plies, key="review_move", format_func=lambda ply: _move_label(by_ply[ply]), on_change=_reset_view, filter_mode=None)
    bookmarks[game["game_url"]] = selected
    index = plies.index(selected)
    previous, following = st.columns(2, gap="small", wrap=False)
    previous.button("Previous move", key="review_previous_move", disabled=index == 0, width="stretch", icon=":material/chevron_left:", on_click=_step_move, args=(plies, -1))
    following.button("Next move", key="review_next_move", disabled=index == len(plies) - 1, width="stretch", icon=":material/chevron_right:", icon_position="right", on_click=_step_move, args=(plies, 1))
    move = by_ply[selected]
    board_column, explanation_column = st.columns([1.05, 1], gap="medium")
    with board_column:
        view = st.selectbox("Board view", VIEWS, key="review_board_view", on_change=_reset_line_step, filter_mode=None)
        start = "fen_after" if view in {VIEWS[1], VIEWS[3]} else "fen_before"
        board = chess.Board(move[start])
        pv = move["best_pv"] if view == VIEWS[2] else move["reply_pv"] if view == VIEWS[3] else []
        last_move = None
        line_caption = ""
        step_description = ""
        if view == VIEWS[1]:
            played = chess.Move.from_uci(move["played_uci"])
            last_move = [chess.square_name(played.from_square), chess.square_name(played.to_square)]
        if view in {VIEWS[2], VIEWS[3]}:
            if pv:
                explained_steps = continuation_steps(board.fen(), pv, expected_first=move["best_move"] if view == VIEWS[2] else None)
                cursor = st.session_state.get("review_line_step", 0)
                if not isinstance(cursor, int) or not 0 <= cursor <= len(pv):
                    st.session_state.review_line_step = 0
                step = st.slider("Line position", 0, len(pv), key="review_line_step")
                for san in pv[:step]:
                    played = board.parse_san(san)
                    last_move = [chess.square_name(played.from_square), chess.square_name(played.to_square)]
                    board.push(played)
                line_caption = "Start" if step == 0 else f"After {pv[step - 1]} · step {step} of {len(pv)}"
                if 0 < step <= len(explained_steps):
                    step_description = explained_steps[step - 1]["description"]
            else:
                line_caption = "No continuation: this position is terminal or the analysis supplied no line."
        arrows = []
        if view == VIEWS[0]:
            played = board.parse_san(move["played_move"])
            best = board.parse_san(move["best_move"])
            bad = move["classification"]["key"] in {"inaccuracy", "mistake", "blunder"}
            arrows.append({"from": chess.square_name(played.from_square), "to": chess.square_name(played.to_square), "brush": "red" if bad else "yellow"})
            if best != played:
                arrows.append({"from": chess.square_name(best.from_square), "to": chess.square_name(best.to_square), "brush": "green"})
            else:
                arrows[0]["brush"] = "green"
        state = board_state(board)
        chess_board(fen=board.fen(), orientation=game["user_color"], turn=state["turn"], check=state["check"], last_move=last_move, arrows=arrows, key=f"full-review-board-{record['signature'][:12]}")
        if line_caption:
            st.caption(line_caption)
        if step_description:
            st.caption(step_description)
        st.caption("Green: engine's preferred move. Amber: your move; red marks an inaccuracy, mistake, or blunder.")
        st.caption("Engine lines are possibilities found within this search, not a claim that every reply is forced.")
    with explanation_column:
        with st.container(border=True):
            st.markdown(f"#### {_move_label(move)}")
            current, best = st.columns(2)
            current.metric("You played", move["played_move"])
            best.metric("Engine's choice", move["best_move"])
            st.caption(f"Evaluation: {evaluation_label(move, 'before')} → {evaluation_label(move, 'after')}")
            st.markdown(ChessCoach.review_move_locally(move, user_rating=user_rating))
            if not record["is_mock"]:
                st.caption(f"Search depth {move['depth'] or '—'} before / {move['depth_after'] or '—'} after · current coaching level {user_rating}")
    with st.expander("How the assessments work"):
        st.write("These are ChessBot estimates using Stockfish's expected-result model. They can differ from Chess.com's rating-dependent Game Review. Your current Chess.com rating controls the coaching explanations; it is not used to invent Chess.com's private formula.")
        st.write("Expected-points loss: up to 0.02 Excellent; up to 0.05 Good; up to 0.10 Inaccuracy; up to 0.20 Mistake; larger losses Blunder. The engine's first choice is Best; a position with one legal move is Forced. Brilliant and Great are conservative candidates, not official awards.")
        st.write("A bounded search can change its evaluation between positions. Best identifies the first choice before the move; it is not an exhaustive proof. Book and Miss labels require evidence this analysis does not have, so they are not guessed.")
        st.markdown("[Chess.com category definitions](https://support.chess.com/en/articles/8572705-how-are-moves-classified-what-is-a-blunder-or-brilliant-etc) · [python-chess expected outcomes](https://python-chess.readthedocs.io/en/latest/engine.html#chess.engine.Score.wdl)")
