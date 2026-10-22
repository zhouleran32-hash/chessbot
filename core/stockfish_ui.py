"""Detailed engine evidence and stable replay, separate from quality labels."""

from functools import partial

import chess
import streamlit as st

from core.board_widget import board_state, chess_board
from core.continuation import continuation_steps
from core.review_ui import evaluation_label


def _move_name(move: dict) -> str:
    return f"{move['move_number']}{'.' if move['color'] == 'white' else '...'} {move['played_move']}"


def _candidate_score(candidate: dict) -> str:
    return evaluation_label({"mate_before": candidate["mate"], "eval_before_cp": candidate["cp"]}, "before")


def _reset_position() -> None:
    st.session_state.sf_position = 0


def _reset_move() -> None:
    st.session_state.sf_line = "candidate_0"
    _reset_position()


def _step_move(plies: list[int], delta: int) -> None:
    current = plies.index(st.session_state.sf_move)
    st.session_state.sf_move = plies[max(0, min(len(plies) - 1, current + delta))]
    _reset_move()


def _select_row(key: str, plies: list[int]) -> None:
    rows = st.session_state.get(key, {}).get("selection", {}).get("rows", [])
    if rows and 0 <= rows[0] < len(plies):
        st.session_state.sf_move = plies[rows[0]]
        _reset_move()


def _step_position(delta: int, end: int) -> None:
    st.session_state.sf_position = max(0, min(end, st.session_state.sf_position + delta))


def render_stockfish_review(game: dict, record: dict) -> None:
    moves = record["moves"]
    if not moves:
        st.info("This game contains no moves played by the selected player.")
        return
    st.caption(
        "1 second per search · up to 3 candidates · up to 12 half-moves per line. "
        "Scores are from your side: positive favors you, negative favors your opponent. "
        "Search depth varies by position; these are sampled continuations."
    )
    reviewed, candidates = st.columns(2)
    reviewed.metric("Moves analyzed", len(moves))
    candidates.metric("Candidate moves compared", sum(len(move["candidates"]) for move in moves))
    by_ply = {move["ply"]: move for move in moves}
    plies = list(by_ply)
    token = (game["game_url"], record["signature"])
    bookmarks = st.session_state.setdefault("sf_bookmarks", {})
    if st.session_state.get("sf_game") != token or st.session_state.get("sf_move") not in by_ply:
        st.session_state.sf_game = token
        default = max(moves, key=lambda move: move["expected_before"] - move["expected_after"])["ply"]
        saved = bookmarks.get(token, default)
        st.session_state.sf_move = saved if saved in by_ply else default
        _reset_move()

    st.markdown("#### Every move · engine evaluations")
    table_key = f"sf_table_{record['signature']}"
    st.dataframe(
        [{"Move": _move_name(move), "Best available": evaluation_label(move, "before"),
          "After your move": evaluation_label(move, "after"), "Engine's choice": move["best_move"],
          "Depth before / after": f"{move['depth'] or '—'} / {move['depth_after'] or '—'}"}
         for move in moves],
        hide_index=True, width="stretch", height=min(318, 38 + 35 * len(moves)),
        key=table_key, on_select=partial(_select_row, table_key, plies), selection_mode="single-row",
        alt="Detailed Stockfish evaluations for every move you played.",
    )
    selected = st.selectbox("Analyze a move", plies, key="sf_move",
                            format_func=lambda ply: _move_name(by_ply[ply]),
                            on_change=_reset_move, filter_mode=None)
    bookmarks[token] = selected
    previous, following = st.columns(2, gap="small", wrap=False)
    previous.button("Previous move", key="sf_previous_move", width="stretch", disabled=selected == plies[0],
                    on_click=_step_move, args=(plies, -1), icon=":material/chevron_left:")
    following.button("Next move", key="sf_next_move", width="stretch", disabled=selected == plies[-1],
                     on_click=_step_move, args=(plies, 1), icon=":material/chevron_right:", icon_position="right")

    move = by_ply[selected]
    board_column, details_column = st.columns([1.05, 1], gap="medium")
    with board_column:
        choices = {f"candidate_{index}": candidate for index, candidate in enumerate(move["candidates"])}
        choices["played"] = {
            "move": move["played_move"], "cp": move["eval_after_cp"], "mate": move["mate_after"],
            "pv": [move["played_move"], *move["reply_pv"]][:12], "depth": move["depth_after"],
        }
        def line_name(key: str) -> str:
            candidate = choices[key]
            prefix = "Your move" if key == "played" else f"Option {int(key.split('_')[1]) + 1}"
            return f"{prefix}: {candidate['move']} · {_candidate_score(candidate)}"

        if st.session_state.get("sf_line") not in choices:
            _reset_move()
        line = st.selectbox("Explore a line", list(choices), key="sf_line", format_func=line_name,
                            on_change=_reset_position, filter_mode=None)
        candidate = choices[line]
        steps = continuation_steps(move["fen_before"], candidate["pv"], expected_first=candidate["move"], max_plies=12)
        if not 0 <= st.session_state.get("sf_position", 0) <= len(steps):
            _reset_position()
        position = st.slider("Line position", 0, max(1, len(steps)), key="sf_position", disabled=not steps)
        board = chess.Board(steps[position - 1]["fen_after"] if position else move["fen_before"])
        last_move, arrows = None, []
        if position:
            last = chess.Move.from_uci(steps[position - 1]["uci"])
            last_move = [chess.square_name(last.from_square), chess.square_name(last.to_square)]
        elif steps:
            first = chess.Move.from_uci(steps[0]["uci"])
            arrows = [{"from": chess.square_name(first.from_square), "to": chess.square_name(first.to_square), "brush": "green"}]
        state = board_state(board)
        chess_board(fen=board.fen(), orientation=game["user_color"], turn=state["turn"], check=state["check"],
                    last_move=last_move, arrows=arrows, key=f"sf_board_{record['signature'][:12]}")
        previous, following = st.columns(2, gap="small", wrap=False)
        previous.button("Previous position", key="sf_previous_position", width="stretch", disabled=position == 0,
                        on_click=_step_position, args=(-1, len(steps)), icon=":material/chevron_left:")
        following.button("Next position", key="sf_next_position", width="stretch", disabled=position >= len(steps),
                         on_click=_step_position, args=(1, len(steps)), icon=":material/chevron_right:", icon_position="right")
        st.caption("Line start" if not position else f"{steps[position - 1]['label']} · position {position} of {len(steps)}")
        if position:
            st.write(steps[position - 1]["description"])
        st.caption(
            "The evaluation is for the position after your played move; stepping the board does not run a new search."
            if line == "played" else
            "The evaluation is for this candidate from the position before your move; stepping the board does not run a new search."
        )

    with details_column:
        with st.container(border=True):
            st.markdown(f"#### Comparing {_move_name(move)}")
            before, after = st.columns(2)
            before.metric("Best available", evaluation_label(move, "before"))
            after.metric("After your move", evaluation_label(move, "after"))
            if move["played_uci"] == move["best_uci"]:
                st.write("You played the engine's first choice. Small score differences can come from searching the two positions separately.")
            elif move["mate_before"] is not None or move["mate_after"] is not None:
                st.write("Compare the mate status above and replay the lines to see the checks and replies found by this search.")
            else:
                st.write(f"The searched evaluation falls by {move['eval_drop']:.2f} pawns after your move. "
                         "This measures position strength, including activity and king safety; it is not a count of pieces lost.")
            st.markdown("**Candidate moves**")
            st.dataframe(
                [{"Option": index + 1, "Move": item["move"], "Evaluation": _candidate_score(item),
                  "Depth": item["depth"]} for index, item in enumerate(move["candidates"])],
                hide_index=True, width="stretch", alt="Scored candidate moves from the same position.",
            )
            st.caption("The candidates share one search budget. Your played move is also evaluated separately after it is played.")
            st.markdown(f"**What {candidate['move']} does**")
            if steps:
                st.write(steps[0]["description"])
            if len(steps) > 1:
                st.markdown("**What could happen next**")
                st.write(f"Your opponent's analyzed reply is {steps[1]['label']}. {steps[1]['description']}")
                if len(steps) > 2:
                    st.write(f"You can continue with {steps[2]['label']}. {steps[2]['description']}")
            else:
                st.caption("No further reply was supplied for this line. It may end the game or be shorter than the display limit.")
            st.markdown("**Full sample line**")
            st.write(" → ".join(step["label"] for step in steps) or "No continuation available.")
            with st.expander("Explain every move in this line"):
                for step in steps:
                    st.markdown(f"**{step['label']} · {'You' if step['mover'] == 'you' else 'Opponent'}**")
                    st.write(step["description"])
            st.caption("Other replies are possible. A longer search can change the ranking and evaluation.")
            st.markdown("**Before your next move**")
            st.write("Which checks, captures, and threats can my opponent play after my intended move?")
