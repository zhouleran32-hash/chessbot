"""Interactive lessons for Silman's Complete Endgame Course."""

import sqlite3

import chess
import streamlit as st

from core.board_widget import board_state, chess_board, legal_destinations
from core.primer import feedback_for_played_move, san_for_squares
from core.primer_progress import LearningProgress
from core.primer_study import check_concept, concept_option_order, example_frames, required_checks
from core.silman import lessons, part_label, pdf_page
from core.silman_study import PARTS, guide_for


def _reset_quiz() -> None:
    st.session_state.silman_board_fen = None
    st.session_state.silman_from = None
    st.session_state.silman_promotion = None
    st.session_state.silman_moved = None
    st.session_state.silman_feedback = None
    st.session_state.silman_try = st.session_state.get("silman_try", 0) + 1


def _set_lesson(lesson_id: str) -> None:
    st.session_state.silman_lesson = lesson_id
    st.session_state.silman_part = next(item.chapter for item in lessons() if item.id == lesson_id)
    st.session_state.silman_step = 0
    _reset_quiz()


def _play(lesson, move: chess.Move) -> None:
    board = chess.Board(lesson.quiz_fen)
    san = board.san(move)
    board.push(move)
    st.session_state.silman_board_fen = board.fen()
    st.session_state.silman_moved = (
        chess.square_name(move.from_square), chess.square_name(move.to_square), san,
    )
    st.session_state.silman_from = None
    st.session_state.silman_promotion = None
    result = feedback_for_played_move(lesson, san)
    st.session_state.silman_feedback = (result.correct, result.explanation)
    _record(lesson.id, "board", result.correct)


def _choose_square(lesson, square: str) -> None:
    if st.session_state.get("silman_board_fen"):
        return
    st.session_state.silman_promotion = None
    board = chess.Board(lesson.quiz_fen)
    origin = st.session_state.get("silman_from")
    target = chess.parse_square(square)
    if origin:
        moves = [
            move for move in board.legal_moves
            if chess.square_name(move.from_square) == origin and move.to_square == target
        ]
        if len(moves) > 1:
            st.session_state.silman_promotion = (origin, square)
            return
        if len(moves) == 1:
            _play(lesson, moves[0])
            return
    piece = board.piece_at(target)
    if piece and piece.color == board.turn and any(move.from_square == target for move in board.legal_moves):
        st.session_state.silman_from = square if origin != square else None
    else:
        st.session_state.silman_from = None


def _drop(lesson, origin: str, target: str) -> None:
    if st.session_state.get("silman_board_fen"):
        return
    st.session_state.silman_from = origin
    _choose_square(lesson, target)


def _prepare(config) -> dict[str, set[str]]:
    player = (st.session_state.get("username") or config.chess_com_username or "local-learner").strip() or "local-learner"
    path = config.sqlite_path.parent / "silman.sqlite3"
    identity = (str(path), player.casefold())
    if st.session_state.get("silman_profile") != identity:
        st.session_state.silman_profile = identity
        st.session_state.silman_passed = {}
        st.session_state.silman_concept_feedback = {}
        st.session_state.silman_example_choices = {}
        for key in list(st.session_state):
            if key in {"silman_lesson", "silman_part", "silman_shown"} or key.startswith(("silman_concept_choice_", "silman_concept_check_", "silman_worked_", "silman_example_")):
                del st.session_state[key]
        _reset_quiz()
        try:
            store = LearningProgress(path, player)
            st.session_state.silman_progress_store = store
            st.session_state.silman_passed = store.all_passed()
            saved = store.last_lesson()
            if saved and any(item.id == saved for item in lessons()):
                st.session_state.silman_lesson = saved
        except (OSError, sqlite3.Error):
            st.session_state.silman_progress_store = None
            st.warning("Lessons work, but progress could not be saved locally. Check the data/cache folder permissions.")
    return st.session_state.silman_passed


def _record(lesson_id: str, exercise: str, correct: bool) -> None:
    if correct:
        st.session_state.silman_passed.setdefault(lesson_id, set()).add(exercise)
    store = st.session_state.get("silman_progress_store")
    if store:
        try:
            store.record(lesson_id, exercise, correct)
        except (OSError, sqlite3.Error):
            st.warning("Your answer was checked, but progress could not be saved to disk.")


def _bookmark(lesson_id: str) -> None:
    store = st.session_state.get("silman_progress_store")
    if store:
        try:
            store.bookmark(lesson_id)
        except (OSError, sqlite3.Error):
            st.warning("Your place in the course could not be saved to disk.")


def _coverage(catalog) -> str:
    taught = sorted({item.chapter for item in catalog})
    label = f"Parts {taught[0]}–{taught[-1]}" if len(taught) > 1 else f"Part {taught[0]}"
    if any(number not in taught for number in PARTS):
        return f"{label} are playable. Later rating bands are mapped and not taught yet."
    return f"{label} are playable."


def _step_example(position_key: str, direction: int, last_position: int) -> None:
    st.session_state[position_key] = max(0, min(st.session_state[position_key] + direction, last_position))


def render_silman(config) -> None:
    catalog = lessons()
    passed = _prepare(config)
    by_id = {item.id: item for item in catalog}
    if st.session_state.get("silman_lesson") not in by_id:
        previous = st.session_state.get("silman_shown")
        st.session_state.silman_lesson = previous if previous in by_id else catalog[0].id
    if "silman_part" not in st.session_state:
        st.session_state.silman_part = by_id[st.session_state.silman_lesson].chapter
    completed = sum(required_checks(guide_for(item.id)) <= passed.get(item.id, set()) for item in catalog)
    heading, progress = st.columns([3, 1], gap="small", vertical_alignment="center")
    heading.subheader("Silman's endgame course")
    progress.progress(completed / len(catalog), text=f"Course practice · {completed}/{len(catalog)} lessons")
    st.caption(_coverage(catalog))
    part_column, lesson_column = st.columns([1, 2], gap="small", vertical_alignment="bottom")
    with part_column:
        part = st.selectbox(
            "Part", sorted({item.chapter for item in catalog}), format_func=part_label,
            key="silman_part", filter_mode=None,
        )
    part_ids = [item.id for item in catalog if item.chapter == part]
    if st.session_state.silman_lesson not in part_ids:
        st.session_state.silman_lesson = part_ids[0]
    with lesson_column:
        selected = st.selectbox(
            "Lesson", part_ids, key="silman_lesson", filter_mode=None,
            format_func=lambda identifier: by_id[identifier].title,
        )
    if st.session_state.get("silman_shown") != selected:
        st.session_state.silman_shown = selected
        st.session_state.silman_step = 0
        _reset_quiz()
        st.session_state.silman_try = 0
        _bookmark(selected)
    lesson = by_id[selected]
    index = [item.id for item in catalog].index(selected)
    with st.container(horizontal=True, wrap=False, gap="small"):
        st.button(
            "Previous lesson", disabled=index == 0, key="silman_previous_lesson",
            icon=":material/arrow_back:", on_click=_set_lesson, args=(catalog[max(0, index - 1)].id,),
        )
        st.button(
            "Next lesson", disabled=index == len(catalog) - 1, key="silman_next_lesson",
            icon=":material/arrow_forward:", icon_position="right",
            on_click=_set_lesson, args=(catalog[min(len(catalog) - 1, index + 1)].id,),
        )
    guide = guide_for(lesson.id)
    required = required_checks(guide)
    done = passed.get(lesson.id, set()) & required
    title_column, lesson_progress = st.columns([3, 1], gap="small", vertical_alignment="center")
    with title_column:
        st.markdown(f"### {lesson.title}")
        st.caption(f"{part_label(lesson.chapter)} · lesson {index + 1} of {len(catalog)}")
        if guide:
            start, end = guide["pages"]
            st.caption(
                f"Silman's Complete Endgame Course · printed pages {start}–{end} · PDF pages {pdf_page(start)}–{pdf_page(end)}"
            )
    lesson_progress.progress(len(done) / len(required), text=f"Practice · {len(done)}/{len(required)} checks")
    learn_tab, example_tab, practice_tab, review_tab = st.tabs(["Learn", "Worked examples", "Practice", "Review"])
    with learn_tab:
        _learn(lesson, guide)
    with example_tab:
        _examples(lesson, guide)
    with practice_tab:
        _practice(lesson)
        _checks(lesson, guide)
    with review_tab:
        _review(lesson, guide, passed)
    with st.expander("Where this sits in the book"):
        available = {item.chapter for item in catalog}
        st.write(_coverage(catalog))
        for number, (title, band, start, end) in PARTS.items():
            state = "Guided lessons available" if number in available else "Not yet taught"
            st.markdown(f"- **Part {number} · {title}** ({band}) · pp. {start}–{end} · {state}")


def _learn(lesson, guide) -> None:
    index = min(st.session_state.get("silman_step", 0), len(lesson.steps) - 1)
    step = lesson.steps[index]
    position = chess.Board(step.fen)
    state = board_state(position)
    board_column, note_column = st.columns([1.15, 1], gap="medium")
    with board_column:
        chess_board(
            fen=step.fen, orientation=lesson.orientation, turn=state["turn"], check=state["check"],
            arrows=[{"from": item[0], "to": item[1], "brush": "green"} for item in step.arrows],
            key=f"silman-diagram-{lesson.id}",
        )
        back, forward = st.columns(2)
        if back.button("Back", disabled=index == 0, key="silman_back", width="stretch", icon=":material/chevron_left:"):
            st.session_state.silman_step = index - 1
            st.rerun()
        if forward.button("Next", disabled=index == len(lesson.steps) - 1, key="silman_next", width="stretch", icon=":material/chevron_right:", icon_position="right"):
            st.session_state.silman_step = index + 1
            st.rerun()
    with note_column:
        st.caption(f"Diagram {index + 1} of {len(lesson.steps)}")
        st.markdown(step.caption)
        st.markdown(lesson.explanation)
        if guide and guide["pitfalls"]:
            st.markdown("**Avoid**")
            for pitfall in guide["pitfalls"]:
                st.markdown(f"- {pitfall}")


def _examples(lesson, guide) -> None:
    if not guide:
        st.info("A worked example is being prepared for this lesson.")
        return
    examples = guide["examples"]
    choices = st.session_state.setdefault("silman_example_choices", {})
    example_index = 0
    if len(examples) > 1:
        selection_key = f"silman_worked_{lesson.id}"
        if selection_key not in st.session_state:
            st.session_state[selection_key] = max(0, min(choices.get(lesson.id, 0), len(examples) - 1))
        example_index = st.selectbox(
            "Worked example", list(range(len(examples))),
            format_func=lambda index: examples[index]["title"],
            key=selection_key, filter_mode=None,
        )
    choices[lesson.id] = example_index
    shown = examples[example_index]
    st.markdown(f"#### {shown['title']}")
    frames = example_frames(shown)
    position_key = f"silman_example_{lesson.id}_{example_index}"
    move_index = max(0, min(st.session_state.get(position_key, 0), len(frames) - 1))
    st.session_state[position_key] = move_index
    frame = frames[move_index]
    board_column, note_column = st.columns([1, 1], gap="medium")
    with board_column:
        position = chess.Board(frame.fen)
        state = board_state(position)
        chess_board(
            fen=frame.fen, orientation=lesson.orientation, turn=state["turn"], check=state["check"],
            last_move=list(frame.arrow) if frame.arrow else None,
            arrows=[{"from": frame.arrow[0], "to": frame.arrow[1], "brush": "green"}] if frame.arrow else [],
            key=f"silman-example-board-{lesson.id}-{example_index}",
        )
        previous, following = st.columns(2, gap="small", wrap=False)
        previous.button(
            "Previous", key=f"silman_example_previous_{lesson.id}_{example_index}",
            disabled=move_index == 0, width="stretch", icon=":material/chevron_left:",
            on_click=_step_example, args=(position_key, -1, len(frames) - 1),
        )
        following.button(
            "Forward", key=f"silman_example_next_{lesson.id}_{example_index}",
            disabled=move_index == len(frames) - 1, width="stretch",
            icon=":material/chevron_right:", icon_position="right",
            on_click=_step_example, args=(position_key, 1, len(frames) - 1),
        )
    with note_column:
        st.markdown(f"**{frame.move_label}**")
        st.markdown(frame.note)
        st.caption(f"Position {move_index + 1} of {len(frames)}.")
        st.markdown("**The line**")
        st.write(" · ".join(item.move_label for item in frames[1:]))


def _practice(lesson) -> None:
    st.markdown("**Your turn**")
    st.write(lesson.prompt)
    display_fen = st.session_state.get("silman_board_fen") or lesson.quiz_fen
    position = chess.Board(display_fen)
    state = board_state(position)
    interactive = not st.session_state.get("silman_board_fen")
    board_column, answer_column = st.columns([1.15, 1], gap="medium")
    with board_column:
        st.caption("Drag a piece, or click it and then the square.")
        result = chess_board(
            fen=display_fen, orientation=lesson.orientation, interactive=interactive,
            dests=legal_destinations(display_fen) if interactive else {},
            turn=state["turn"], check=state["check"],
            last_move=list(st.session_state.get("silman_moved") or ())[:2] or None,
            key=f"silman-practice-{lesson.id}-{st.session_state.get('silman_try', 0)}",
        )
    dropped = st.session_state.pop("silman_board_drop", None)
    clicked = st.session_state.pop("silman_square_click", None)
    move = getattr(result, "move", None)
    if isinstance(move, dict) and move.get("from") and move.get("to"):
        _drop(lesson, move["from"], move["to"])
        st.rerun()
    if isinstance(dropped, (list, tuple)) and len(dropped) == 2:
        _drop(lesson, dropped[0], dropped[1])
        st.rerun()
    if isinstance(clicked, str):
        _choose_square(lesson, clicked)
        st.rerun()
    with answer_column:
        promotion = st.session_state.get("silman_promotion")
        if promotion:
            st.caption("Choose the piece this pawn becomes.")
            with st.container(horizontal=True, gap="xsmall"):
                for name, symbol in (("Queen", "q"), ("Rook", "r"), ("Bishop", "b"), ("Knight", "n")):
                    if st.button(name, key=f"silman-promo-{lesson.id}-{symbol}"):
                        san = san_for_squares(lesson.quiz_fen, promotion[0], promotion[1], promotion=symbol)
                        if san:
                            _play(lesson, chess.Board(lesson.quiz_fen).parse_san(san))
                            st.rerun()
        st.caption("Or choose the move by name")
        with st.container(horizontal=True, gap="xsmall"):
            for choice in lesson.choices:
                if st.button(choice.san, key=f"silman-choice-{lesson.id}-{choice.san}"):
                    _play(lesson, chess.Board(lesson.quiz_fen).parse_san(choice.san))
                    st.rerun()
        moved = st.session_state.get("silman_moved")
        if moved:
            st.caption(f"You played {moved[2]}.")
        feedback = st.session_state.get("silman_feedback")
        if feedback:
            (st.success if feedback[0] else st.warning)(feedback[1])
        if st.session_state.get("silman_board_fen") and st.button("Try again", key="silman_try_again", icon=":material/replay:"):
            _reset_quiz()
            st.rerun()


def _checks(lesson, guide) -> None:
    if not guide:
        return
    st.markdown("#### Explain the idea")
    results = st.session_state.silman_concept_feedback
    for number, question in enumerate(guide["checks"], start=1):
        with st.container(border=True):
            choice = st.radio(
                f"{number}. {question['prompt']}", concept_option_order(lesson.id, question), index=None,
                format_func=lambda index, options=question["options"]: options[index]["text"],
                key=f"silman_concept_choice_{lesson.id}_{question['id']}",
            )
            if st.button("Check my answer", key=f"silman_concept_check_{lesson.id}_{question['id']}", disabled=choice is None, icon=":material/check:"):
                result = check_concept(guide, question["id"], choice)
                results[(lesson.id, question["id"])] = (choice, result)
                _record(lesson.id, f"concept:{question['id']}", result.correct)
                st.rerun()
            checked = results.get((lesson.id, question["id"]))
            if isinstance(checked, tuple):
                checked_choice, result = checked
                if checked_choice == choice:
                    (st.success if result.correct else st.warning)(result.explanation)
                else:
                    st.info("Check your changed answer to see its explanation.")


def _review(lesson, guide, passed) -> None:
    st.markdown("#### What to remember")
    for point in (guide or {}).get("recap", ()):
        st.markdown(f"- {point}")
    required = required_checks(guide)
    completed = passed.get(lesson.id, set()) & required
    st.progress(len(completed) / len(required), text=f"{len(completed)} of {len(required)} practice checks completed")
    if completed == required:
        st.success("Lesson practice completed. Close the notes and say the idea in your own words.")
    else:
        st.info("Finish the board task and the understanding check. Your place is saved on this computer.")
