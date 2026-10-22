"""Guided, source-referenced Primer teaching and interactive practice."""

import sqlite3

import chess
import streamlit as st

from core.board_widget import board_state, chess_board, legal_destinations
from core.primer import CHAPTER_TITLES, chapter_label, feedback_for_played_move, lessons, san_for_squares
from core.primer_progress import LearningProgress
from core.primer_study import BOOK_CHAPTERS, check_concept, concept_option_order, example_frames, guide_for, required_checks


def _reset_quiz_position() -> None:
    st.session_state.primer_board_fen = None
    st.session_state.primer_from = None
    st.session_state.primer_promotion = None
    st.session_state.primer_moved = None
    st.session_state.primer_feedback = None
    st.session_state.primer_try = st.session_state.get("primer_try", 0) + 1


def _set_primer_lesson(lesson_id: str) -> None:
    st.session_state.primer_lesson = lesson_id
    st.session_state.primer_chapter = next(item.chapter for item in lessons() if item.id == lesson_id)
    st.session_state.primer_step = 0
    _reset_quiz_position()


def _appendix_collection(lesson_id: str) -> str:
    for prefix, label in (
        ("app-two-", "Two-move problems"),
        ("app-three-", "Three-move problems"),
        ("app-more-", "Longer problems"),
        ("app-win-", "Winning studies"),
        ("app-draw-", "Drawing studies"),
    ):
        if lesson_id.startswith(prefix):
            return label
    return "Getting started"


def _change_primer_collection() -> None:
    selected = st.session_state.primer_collection
    first = next(item.id for item in lessons()
                 if item.chapter == 11 and _appendix_collection(item.id) == selected)
    _set_primer_lesson(first)


def _play_quiz_move(lesson, move: chess.Move) -> None:
    board = chess.Board(lesson.quiz_fen)
    san = board.san(move)
    board.push(move)
    st.session_state.primer_board_fen = board.fen()
    st.session_state.primer_moved = (
        chess.square_name(move.from_square), chess.square_name(move.to_square), san,
    )
    st.session_state.primer_from = None
    st.session_state.primer_promotion = None
    result = feedback_for_played_move(lesson, san)
    st.session_state.primer_feedback = (result.correct, result.explanation)
    _record_result(lesson.id, "board", result.correct)


def _drop_quiz_piece(lesson, origin: str, target: str) -> None:
    """Apply a completed drag. Promotion waits for an explicit piece choice."""
    if st.session_state.get("primer_board_fen"):
        return
    st.session_state.primer_promotion = None
    st.session_state.primer_from = origin
    _choose_quiz_square(lesson, target)


def _choose_quiz_square(lesson, square: str) -> None:
    """Select a piece, or move the selected piece onto this square."""
    if st.session_state.get("primer_board_fen"):
        return
    st.session_state.primer_promotion = None
    board = chess.Board(lesson.quiz_fen)
    origin = st.session_state.get("primer_from")
    target = chess.parse_square(square)
    if origin:
        moves = [
            move for move in board.legal_moves
            if chess.square_name(move.from_square) == origin and move.to_square == target
        ]
        if len(moves) > 1:
            st.session_state.primer_promotion = (origin, square)
            return
        if len(moves) == 1:
            _play_quiz_move(lesson, moves[0])
            return
    piece = board.piece_at(target)
    if piece and piece.color == board.turn and any(move.from_square == target for move in board.legal_moves):
        st.session_state.primer_from = square if origin != square else None
    else:
        st.session_state.primer_from = None


def _prepare_progress(config) -> dict[str, set[str]]:
    player = (st.session_state.get("username") or config.chess_com_username or "local-learner").strip() or "local-learner"
    path = config.sqlite_path.parent / "primer.sqlite3"
    identity = (str(path), player.casefold())
    if st.session_state.get("primer_profile") != identity:
        st.session_state.primer_profile = identity
        st.session_state.primer_passed = {}
        st.session_state.primer_concept_feedback = {}
        st.session_state.primer_example_choices = {}
        for key in list(st.session_state):
            if key in {"primer_lesson", "primer_chapter", "primer_collection", "primer_shown"} or key.startswith(("concept_choice_", "concept_check_", "worked_", "example_")):
                del st.session_state[key]
        _reset_quiz_position()
        try:
            store = LearningProgress(path, player)
            st.session_state.primer_progress_store = store
            st.session_state.primer_passed = store.all_passed()
            saved = store.last_lesson()
            if saved:
                st.session_state.primer_lesson = saved
        except (OSError, sqlite3.Error):
            st.session_state.primer_progress_store = None
            st.warning("Lessons work, but progress could not be saved locally. Check the data/cache folder permissions.")
    return st.session_state.primer_passed


def _record_result(lesson_id: str, exercise: str, correct: bool) -> None:
    if correct:
        st.session_state.primer_passed.setdefault(lesson_id, set()).add(exercise)
    store = st.session_state.get("primer_progress_store")
    if store:
        try:
            store.record(lesson_id, exercise, correct)
        except (OSError, sqlite3.Error):
            st.warning("Your answer was checked, but progress could not be saved to disk.")


def _bookmark(lesson_id: str) -> None:
    store = st.session_state.get("primer_progress_store")
    if store:
        try:
            store.bookmark(lesson_id)
        except (OSError, sqlite3.Error):
            st.warning("Your place in the course could not be saved to disk.")


def _course_navigation(catalog, passed):
    by_id = {item.id: item for item in catalog}
    if st.session_state.get("primer_lesson") not in by_id:
        # Streamlit removes hidden widget values while the game view is open.
        # primer_shown is ordinary session state and retains this player's place.
        previous = st.session_state.get("primer_shown")
        st.session_state.primer_lesson = previous if previous in by_id else catalog[0].id
    if "primer_chapter" not in st.session_state:
        st.session_state.primer_chapter = by_id[st.session_state.primer_lesson].chapter
    selector_columns = st.columns(
        [1.1, 1, 1.8] if st.session_state.primer_chapter == 11 else [1, 2],
        gap="small", vertical_alignment="bottom",
    )
    with selector_columns[0]:
        chapter = st.selectbox("Chapter", sorted({item.chapter for item in catalog}), format_func=chapter_label, key="primer_chapter", filter_mode=None)
    chapter_ids = [item.id for item in catalog if item.chapter == chapter]
    if st.session_state.primer_lesson not in chapter_ids:
        st.session_state.primer_lesson = chapter_ids[0]
    if chapter == 11:
        current = _appendix_collection(st.session_state.primer_lesson)
        if st.session_state.get("primer_shown") != st.session_state.primer_lesson or "primer_collection" not in st.session_state:
            st.session_state.primer_collection = current
        collections = list(dict.fromkeys(_appendix_collection(identifier) for identifier in chapter_ids))
        with selector_columns[1]:
            collection = st.selectbox("Collection", collections, key="primer_collection",
                                      filter_mode=None, on_change=_change_primer_collection)
        chapter_ids = [identifier for identifier in chapter_ids
                       if _appendix_collection(identifier) == collection]
    with selector_columns[-1]:
        selected = st.selectbox(
            "Lesson", chapter_ids, key="primer_lesson", filter_mode=None,
            format_func=lambda identifier: by_id[identifier].title,
        )
    if st.session_state.get("primer_shown") != selected:
        st.session_state.primer_shown = selected
        st.session_state.primer_step = 0
        _reset_quiz_position()
        # Initial attempts retain stable board keys for keyboard/accessibility use.
        st.session_state.primer_try = 0
        _bookmark(selected)
    index = [item.id for item in catalog].index(selected)
    with st.container(horizontal=True, wrap=False, gap="small"):
        st.button(
            "Previous lesson", disabled=index == 0, key="primer_previous_lesson",
            icon=":material/arrow_back:", on_click=_set_primer_lesson, args=(catalog[max(0, index - 1)].id,),
        )
        st.button(
            "Next lesson", disabled=index == len(catalog) - 1, key="primer_next_lesson",
            icon=":material/arrow_forward:", icon_position="right",
            on_click=_set_primer_lesson, args=(catalog[min(len(catalog) - 1, index + 1)].id,),
        )
    return by_id[selected], index


def _introductory_diagrams(lesson) -> None:
    with st.expander("Introductory diagrams", expanded=False):
        index = min(st.session_state.get("primer_step", 0), len(lesson.steps) - 1)
        step = lesson.steps[index]
        position = chess.Board(step.fen)
        state = board_state(position)
        chess_board(
            fen=step.fen, orientation=lesson.orientation, turn=state["turn"], check=state["check"],
            arrows=[{"from": item[0], "to": item[1], "brush": "green"} for item in step.arrows],
            key=f"diagram-{lesson.id}",
        )
        back, forward = st.columns(2)
        if back.button("Back", disabled=index == 0, key="primer_back", width="stretch", icon=":material/chevron_left:"):
            st.session_state.primer_step = index - 1
            st.rerun()
        if forward.button("Next", disabled=index == len(lesson.steps) - 1, key="primer_next", width="stretch", icon=":material/chevron_right:", icon_position="right"):
            st.session_state.primer_step = index + 1
            st.rerun()
        st.caption(f"Step {index + 1} of {len(lesson.steps)}. {step.caption}")


def _learn(lesson, guide: dict | None) -> None:
    if guide:
        st.markdown("**By the end of this lesson, you should be able to:**")
        for goal in guide["goals"]:
            st.markdown(f"- {goal}")
    if not guide or not any(section["body"].strip() == lesson.explanation.strip() for section in guide["sections"]):
        st.markdown(lesson.explanation)
    if guide:
        for section in guide["sections"]:
            st.markdown(f"#### {section['title']}")
            st.markdown(section["body"])
        st.markdown("#### Common mistakes to avoid")
        for misconception in guide["pitfalls"]:
            st.markdown(f"- {misconception}")
    _introductory_diagrams(lesson)


def _step_example(position_key: str, direction: int, last_position: int) -> None:
    st.session_state[position_key] = max(0, min(st.session_state[position_key] + direction, last_position))


def _worked_examples(lesson, guide: dict | None) -> None:
    if not guide:
        st.info("A detailed worked example is being prepared for this lesson.")
        return
    examples = guide["examples"]
    # Widget state is discarded when a lesson is hidden. Keep its selected
    # variation alongside the replay cursors so returning resumes the same line.
    choices = st.session_state.setdefault("primer_example_choices", {})
    example_index = 0
    if len(examples) > 1:
        selection_key = f"worked_{lesson.id}"
        if selection_key not in st.session_state:
            st.session_state[selection_key] = max(0, min(choices.get(lesson.id, 0), len(examples) - 1))
        example_index = st.selectbox(
            "Worked example", list(range(len(examples))),
            format_func=lambda index: examples[index]["title"],
            key=selection_key, filter_mode=None,
        )
    choices[lesson.id] = example_index
    example = examples[example_index]
    st.markdown(f"#### {example['title']}")
    frames = example_frames(example)
    position_key = f"example_{lesson.id}_{example_index}"
    move_index = max(0, min(st.session_state.get(position_key, 0), len(frames) - 1))
    st.session_state[position_key] = move_index
    frame = frames[move_index]
    board_column, explanation_column = st.columns([1, 1], gap="medium")
    with board_column:
        position = chess.Board(frame.fen)
        state = board_state(position)
        chess_board(
            fen=frame.fen, orientation=lesson.orientation, turn=state["turn"], check=state["check"],
            last_move=list(frame.arrow) if frame.arrow else None,
            arrows=[{"from": frame.arrow[0], "to": frame.arrow[1], "brush": "green"}] if frame.arrow else [],
            key=f"example-board-{lesson.id}-{example_index}",
        )
        previous, following = st.columns(2, gap="small", wrap=False)
        previous.button(
            "Previous", key=f"example_previous_{lesson.id}_{example_index}", help="Previous move",
            disabled=move_index == 0, width="stretch", icon=":material/chevron_left:",
            on_click=_step_example, args=(position_key, -1, len(frames) - 1),
        )
        following.button(
            "Forward", key=f"example_next_{lesson.id}_{example_index}", help="Next move",
            disabled=move_index == len(frames) - 1, width="stretch",
            icon=":material/chevron_right:", icon_position="right",
            on_click=_step_example, args=(position_key, 1, len(frames) - 1),
        )
    with explanation_column:
        st.markdown(f"**{frame.move_label}**")
        st.markdown(frame.note)
        st.caption(f"Position {move_index + 1} of {len(frames)}. Step one move at a time and say what changed before you read on.")
        st.markdown("**The complete line**")
        st.write(" · ".join(item.move_label for item in frames[1:]))


def _board_practice(lesson) -> None:
    st.markdown("**Your turn**")
    st.write(lesson.prompt)
    display_fen = st.session_state.get("primer_board_fen") or lesson.quiz_fen
    position = chess.Board(display_fen)
    state = board_state(position)
    interactive = not st.session_state.get("primer_board_fen")
    board_column, answer_column = st.columns([1.15, 1], gap="medium")
    with board_column:
        st.caption("Drag a piece, or click it and then the square. Dots mark the legal squares.")
        result = chess_board(
            fen=display_fen, orientation=lesson.orientation, interactive=interactive,
            dests=legal_destinations(display_fen) if interactive else {},
            turn=state["turn"], check=state["check"],
            last_move=list(st.session_state.get("primer_moved") or ())[:2] or None,
            key=f"practice-board-{lesson.id}",
        )
    dropped = st.session_state.pop("primer_board_drop", None)
    clicked = st.session_state.pop("primer_square_click", None)
    move = getattr(result, "move", None)
    if isinstance(move, dict) and move.get("from") and move.get("to"):
        _drop_quiz_piece(lesson, move["from"], move["to"])
        st.rerun()
    if isinstance(dropped, (list, tuple)) and len(dropped) == 2:
        _drop_quiz_piece(lesson, dropped[0], dropped[1])
        st.rerun()
    if isinstance(clicked, str):
        _choose_quiz_square(lesson, clicked)
        st.rerun()
    with answer_column:
        promotion = st.session_state.get("primer_promotion")
        if promotion:
            st.caption("Choose the piece this pawn becomes.")
            with st.container(horizontal=True, gap="xsmall"):
                for name, symbol in (("Queen", "q"), ("Rook", "r"), ("Bishop", "b"), ("Knight", "n")):
                    if st.button(name, key=f"promo-{lesson.id}-{symbol}"):
                        san = san_for_squares(lesson.quiz_fen, promotion[0], promotion[1], promotion=symbol)
                        if san:
                            _play_quiz_move(lesson, chess.Board(lesson.quiz_fen).parse_san(san))
                            st.rerun()
        st.caption("Or choose the move by name")
        with st.container(horizontal=True, gap="xsmall"):
            for choice in lesson.choices:
                if st.button(choice.san, key=f"primer-choice-{lesson.id}-{choice.san}"):
                    _play_quiz_move(lesson, chess.Board(lesson.quiz_fen).parse_san(choice.san))
                    st.rerun()
        moved = st.session_state.get("primer_moved")
        if moved:
            st.caption(f"You played {moved[2]}.")
        feedback = st.session_state.get("primer_feedback")
        if feedback:
            (st.success if feedback[0] else st.warning)(feedback[1])
        if st.session_state.get("primer_board_fen") and st.button("Try again", key="primer_try_again", icon=":material/replay:"):
            _reset_quiz_position()
            st.rerun()


def _concept_checks(lesson, guide: dict | None) -> None:
    if not guide:
        return
    st.markdown("#### Explain the idea")
    st.caption("These questions check why the move or rule works. Every answer has an explanation.")
    results = st.session_state.primer_concept_feedback
    for number, question in enumerate(guide["checks"], start=1):
        with st.container(border=True):
            choice = st.radio(
                f"{number}. {question['prompt']}", concept_option_order(lesson.id, question), index=None,
                format_func=lambda index, options=question["options"]: options[index]["text"],
                key=f"concept_choice_{lesson.id}_{question['id']}",
            )
            if st.button("Check my answer", key=f"concept_check_{lesson.id}_{question['id']}", disabled=choice is None, icon=":material/check:"):
                result = check_concept(guide, question["id"], choice)
                results[(lesson.id, question["id"])] = (choice, result)
                _record_result(lesson.id, f"concept:{question['id']}", result.correct)
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
        st.success("Lesson practice completed. Revisit the example later and try explaining the idea without the notes.")
    else:
        st.info("Complete the board task and each understanding check in Practice. Your place and successful checks are saved locally.")
    st.markdown("**Take it into a game:** Before your next move, name the idea from this lesson and explain whether it applies to the position in front of you.")


def render_primer(config) -> None:
    catalog = lessons()
    passed = _prepare_progress(config)
    available_chapters = {item.chapter for item in catalog}
    last_chapter = max(number for number in available_chapters if number <= 10)
    scope = f"chapters 1–{last_chapter}" + (" and the appendix" if 11 in available_chapters else "")
    completed = sum(required_checks(guide_for(item.id, item.chapter)) <= passed.get(item.id, set()) for item in catalog)
    course_heading, course_progress = st.columns([3, 1], gap="small", vertical_alignment="center")
    course_heading.subheader("The Soviet Chess Primer")
    course_progress.progress(completed / len(catalog), text=f"Course practice · {completed}/{len(catalog)} lessons")
    st.caption(f"Read one idea, replay it, then try the move. This course covers {scope}.")
    lesson, index = _course_navigation(catalog, passed)
    guide = guide_for(lesson.id, lesson.chapter)
    required = required_checks(guide)
    lesson_completed = passed.get(lesson.id, set()) & required
    lesson_heading, lesson_progress = st.columns([3, 1], gap="small", vertical_alignment="center")
    with lesson_heading:
        st.markdown(f"### {lesson.title}")
        st.caption(f"{chapter_label(lesson.chapter)} · lesson {index + 1} of {len(catalog)}")
        if guide:
            start, end = guide["pages"]
            st.caption(f"Book reference: printed pages {start}–{end} · PDF pages {start + 1}–{end + 1}")
    lesson_progress.progress(
        len(lesson_completed) / len(required), text=f"Practice · {len(lesson_completed)}/{len(required)} checks",
    )
    learn_tab, example_tab, practice_tab, review_tab = st.tabs(["Learn", "Worked examples", "Practice", "Review"])
    with learn_tab:
        _learn(lesson, guide)
    with example_tab:
        _worked_examples(lesson, guide)
    with practice_tab:
        _board_practice(lesson)
        _concept_checks(lesson, guide)
    with review_tab:
        _review(lesson, guide, passed)
    with st.expander("Course coverage and how to study"):
        st.write("Read one idea, replay the line slowly, try a different move, then do the practice. Short, attentive sessions are more useful than rushing through many lessons.")
        st.write(f"This course develops the concepts in {scope}, using detailed explanations, annotated games and studies, and practice with feedback. Chapters 1–10 use representative examples; the appendix follows the book’s numbered problems and studies. Not every variation is displayed. A completed practice task is a checkpoint: return later and explain the idea without the notes.")
        for number, (title, start, end) in BOOK_CHAPTERS.items():
            state = "Guided lessons available" if number in available_chapters else "Not yet taught"
            st.markdown(f"- **{chapter_label(number)}** · pp. {start}–{end} · {state}")


