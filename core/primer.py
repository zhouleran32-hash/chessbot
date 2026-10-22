"""Lessons for all ten chapters and the appendix of the Maizelis syllabus.

Explanations are authored for ChessBot. Original teaching illustrations and
identified book games/studies follow the uploaded book's order of skills.
"""

from dataclasses import dataclass

import chess
import chess.svg


CHAPTER_TITLES = {
    1: "The game explained",
    2: "Aim of the game",
    3: "Tactics and strategy",
    4: "Techniques of calculation",
    5: "Combination",
    6: "Positional play",
    7: "How to begin a game",
    8: "The endgame",
    9: "The middlegame",
    10: "The foundations of opening theory",
    11: "Chess compositions",
}


def chapter_label(number: int) -> str:
    """Keep the appendix's book name while retaining stable numeric storage."""
    return f"{'Appendix' if number == 11 else f'Chapter {number}'} · {CHAPTER_TITLES[number]}"


@dataclass(frozen=True)
class Choice:
    san: str
    correct: bool
    explanation: str


@dataclass(frozen=True)
class Step:
    fen: str
    caption: str
    arrows: tuple[tuple[str, str, str], ...] = ()


@dataclass(frozen=True)
class Lesson:
    id: str
    chapter: int
    title: str
    explanation: str
    steps: tuple[Step, ...]
    quiz_fen: str
    prompt: str
    choices: tuple[Choice, ...]
    orientation: str
    objective: str | None = None


@dataclass(frozen=True)
class Grade:
    correct: bool
    explanation: str


def lessons() -> tuple[Lesson, ...]:
    from core.primer_course import COURSE

    built = tuple(_lesson(spec) for spec in COURSE)
    if [lesson.id for lesson in built] != [spec["id"] for spec in COURSE]:
        raise RuntimeError("Primer lessons were not loaded in syllabus order.")
    return built


def grade(lesson: Lesson, san: str) -> Grade:
    board = chess.Board(lesson.quiz_fen)
    try:
        move = board.parse_san(san)
        if move not in board.legal_moves:
            raise ValueError("Illegal or null move")
    except (ValueError, TypeError) as error:
        raise ValueError("That move is not legal in this exercise position.") from error
    matching = None
    for choice in lesson.choices:
        if board.parse_san(choice.san) == move:
            matching = choice
            break
    if lesson.objective:
        result = _objective_grade(board, move, lesson.objective)
        if matching and matching.correct == result.correct:
            return Grade(result.correct, matching.explanation)
        return result
    if matching:
        return Grade(matching.correct, matching.explanation)
    return Grade(False, f"{board.san(move)} is legal, but it does not answer this exercise's specific question. Re-read the task and compare the candidates.")


def _objective_grade(board: chess.Board, move: chess.Move, objective: str) -> Grade:
    after = board.copy()
    after.push(move)
    if objective == "mate_in_2":
        from core.primer_tactics import mate_in_two

        correct, defence = mate_in_two(board.fen(), move.uci())
        if correct:
            return Grade(True, "This forces checkmate within two of your moves. Every legal defensive reply has been checked; each may require a different mating move.")
        if defence:
            return Grade(False, f"The defence {defence} prevents mate on your next turn. After your candidate, picture that reply and look for the escape square or defender you missed. Then try a different first move.")
        return Grade(False, "This move ends in a draw rather than forcing checkmate. Check for stalemate and whether any mating material remains.")
    if objective == "mate_threat":
        if not after.is_check() and not after.is_game_over():
            threat = after.copy()
            threat.turn = board.turn
            threat.ep_square = None
            for candidate in list(threat.legal_moves):
                notation = threat.san(candidate)
                threat.push(candidate)
                mate = threat.is_checkmate()
                threat.pop()
                if mate:
                    return Grade(True, f"This creates the threat {notation} if the opponent does not stop it. It is a threat, not a forced mate: the opponent still gets a move.")
        return Grade(False, "Look for a quiet move that threatens checkmate on your next turn. Check the king's escape squares as well as the checking piece.")
    outcomes = {
        "checkmate": (after.is_checkmate(), "checkmate"),
        "check": (after.is_check(), "check"),
        "promotion": (move.promotion is not None, "pawn promotion"),
        "stalemate": (after.is_stalemate(), "stalemate"),
    }
    if objective not in outcomes:
        raise ValueError(f"Unknown exercise objective: {objective}")
    correct, description = outcomes[objective]
    return Grade(correct, f"{board.san(move)} {'achieves' if correct else 'does not achieve'} {description}. " + (
        "Your move meets the task, even if it was not one of the suggested answers."
        if correct else "Check every legal reply before deciding the position is finished."
    ))


def legal_board_moves(fen: str) -> list[dict]:
    """Legal moves a player can make by moving a piece from one square to another."""
    board = chess.Board(fen)
    return [
        {
            "from": chess.square_name(move.from_square),
            "to": chess.square_name(move.to_square),
            "san": board.san(move),
            "uci": move.uci(),
        }
        for move in board.legal_moves
    ]


def san_for_squares(fen: str, from_square: str, to_square: str, promotion: str | None = None) -> str | None:
    """Return the SAN for a piece moved between two squares, if that move is legal.

    A pawn that can promote returns None until promotion is q, r, b, or n.
    """
    board = chess.Board(fen)
    try:
        origin = chess.parse_square(from_square)
        target = chess.parse_square(to_square)
    except ValueError:
        return None
    if promotion is not None and promotion.lower() not in {"q", "r", "b", "n"}:
        return None
    requested = chess.Piece.from_symbol(promotion).piece_type if promotion else None
    matches = [
        move for move in board.legal_moves
        if move.from_square == origin and move.to_square == target
        and (requested is None or move.promotion == requested)
    ]
    if requested is None:
        plain = [move for move in matches if move.promotion is None]
        if plain:
            matches = plain
    if len(matches) != 1:
        return None
    return board.san(matches[0])


def feedback_for_played_move(lesson: Lesson, san: str) -> Grade:
    """Grade a move played on the board, including a legal move outside the choices."""
    try:
        return grade(lesson, san)
    except ValueError as error:
        return Grade(False, str(error))


def step_svg(step: Step, orientation: str) -> str:
    board = chess.Board(step.fen)
    arrows = [
        chess.svg.Arrow(chess.parse_square(src), chess.parse_square(dst), color=color)
        for src, dst, color in step.arrows
    ]
    side = chess.WHITE if orientation == "white" else chess.BLACK
    return chess.svg.board(board, arrows=arrows, orientation=side, size=400)


def _lesson(spec: dict) -> Lesson:
    steps = tuple(
        Step(fen, caption, tuple(arrows))
        for fen, caption, arrows in spec["steps"]
    )
    choices = tuple(Choice(san, correct, explanation) for san, correct, explanation in spec["choices"])
    quiz = chess.Board(spec["quiz_fen"])
    orientation = spec.get("orientation") or ("white" if quiz.turn == chess.WHITE else "black")
    return Lesson(
        id=spec["id"], chapter=spec["chapter"], title=spec["title"],
        explanation=spec["explanation"].strip(), steps=steps, quiz_fen=spec["quiz_fen"],
        prompt=spec["prompt"].strip(), choices=choices, orientation=orientation,
        objective=spec.get("objective"),
    )
