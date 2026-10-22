"""Detailed study guides, source coverage, and legally replayable examples."""

from dataclasses import dataclass
from importlib import import_module
import random

import chess

from core.primer import Grade


BOOK_CHAPTERS = {
    1: ("The game explained", 13, 34),
    2: ("Aim of the game", 35, 56),
    3: ("Tactics and strategy", 57, 126),
    4: ("Techniques of calculation", 127, 164),
    5: ("Combination", 165, 210),
    6: ("Positional play", 211, 240),
    7: ("How to begin a game", 241, 260),
    8: ("The endgame", 261, 318),
    9: ("The middlegame", 319, 368),
    10: ("The foundations of opening theory", 369, 376),
    11: ("Chess compositions", 377, 400),
}


@dataclass(frozen=True)
class StudyFrame:
    fen: str
    note: str
    move_label: str
    arrow: tuple[str, str] | None = None


def example_frames(example: dict) -> tuple[StudyFrame, ...]:
    """Validate every move and align its explanation with the resulting board."""
    board = chess.Board(example["fen"])
    if not board.is_valid():
        raise ValueError("The worked example has an invalid starting position.")
    moves, notes = example["moves"], example["notes"]
    if len(notes) != len(moves) + 1 or any(not isinstance(note, str) or not note.strip() for note in notes):
        raise ValueError("A worked example needs a starting note and one explanation for every move.")
    frames = [StudyFrame(board.fen(), notes[0], "Starting position")]
    for index, notation in enumerate(moves, start=1):
        ended = board.is_checkmate() or board.is_stalemate() or (
            board.is_game_over() and not board.is_insufficient_material()
        )
        if ended:
            raise ValueError(f"The game already ended before worked-example step {index}.")
        try:
            move = board.parse_san(notation)
            if move not in board.legal_moves:
                raise ValueError("Illegal or null move")
        except (ValueError, TypeError) as error:
            raise ValueError(f"Illegal move {notation!r} in the worked example at step {index}.") from error
        if notation != board.san(move):
            raise ValueError(f"Incorrect notation {notation!r}; this move is {board.san(move)!r} at step {index}.")
        label = f"{board.fullmove_number}{'.' if board.turn == chess.WHITE else '...'} {board.san(move)}"
        arrow = (chess.square_name(move.from_square), chess.square_name(move.to_square))
        board.push(move)
        frames.append(StudyFrame(board.fen(), notes[index], label, arrow))
    return tuple(frames)


def guide_for(lesson_id: str, chapter: int) -> dict | None:
    """Load a chapter's authored guide; older/custom lessons can omit a guide."""
    module_names = [f"core.primer_guides_chapter{chapter}"]
    if chapter == 3:
        module_names.append("core.primer_guides_chapter3_extra")
    for module_name in module_names:
        try:
            module = import_module(module_name)
        except ModuleNotFoundError as error:
            if error.name == module_name:
                continue
            raise
        if lesson_id in module.GUIDES:
            return module.GUIDES[lesson_id]
    return None


def validate_guide(guide: dict, chapter: int) -> None:
    """Reject broken source references, answer keys, or disconnected examples."""
    start, end = guide["pages"]
    _, chapter_start, chapter_end = BOOK_CHAPTERS[chapter]
    if chapter == 1:
        chapter_start = 12  # The preceding advice-to-beginners page informs study method.
    if not chapter_start <= start <= end <= chapter_end:
        raise ValueError("Guide pages must lie inside the cited chapter's printed page range.")
    if not guide["goals"] or not guide["sections"] or not guide["examples"] or not guide["checks"] or not guide["recap"]:
        raise ValueError("A guide needs teaching goals, explanations, worked examples, questions, and recap points.")
    for section in guide["sections"]:
        if not section["title"].strip() or not section["body"].strip():
            raise ValueError("Every explanation section needs a title and substantive text.")
    for example in guide["examples"]:
        example_frames(example)
    identifiers = set()
    for question in guide["checks"]:
        if question["id"] in identifiers:
            raise ValueError("Concept-check IDs must be unique within a lesson.")
        identifiers.add(question["id"])
        if sum(option["correct"] is True for option in question["options"]) != 1:
            raise ValueError("Each concept question must have exactly one correct answer.")
        if not question["prompt"].strip() or any(not item["text"].strip() or not item["explanation"].strip() for item in question["options"]):
            raise ValueError("Every concept option needs its own explanatory feedback.")


def check_concept(guide: dict, question_id: str, option_index: int) -> Grade:
    for question in guide["checks"]:
        if question["id"] == question_id:
            if type(option_index) is not int or not 0 <= option_index < len(question["options"]):
                raise ValueError("Choose one of this question's answers.")
            option = question["options"][option_index]
            return Grade(option["correct"], option["explanation"])
    raise ValueError("This concept question does not belong to the lesson.")


def required_checks(guide: dict | None) -> set[str]:
    return {"board"} | {f"concept:{question['id']}" for question in (guide or {}).get("checks", ())}


def concept_option_order(lesson_id: str, question: dict) -> list[int]:
    """Vary answer placement while preserving each option's stable grading ID."""
    indices = list(range(len(question["options"])))
    random.Random(f"{lesson_id}:{question['id']}").shuffle(indices)
    return indices
