"""Transparent, independent Stockfish move labels, never official review data.

Base loss bands follow the published expected-points cutoffs at:
https://support.chess.com/en/articles/8572705-how-are-moves-classified-what-is-a-blunder-or-brilliant-etc

The caller supplies expected scores from its chosen engine WDL model. This is
not Chess.com's undisclosed rating-dependent expected-points model. Boundary
ties use the lower-severity band. No player-rating adjustment is invented.

Special awards are deliberately conservative candidates: an exact engine best
move is Great only with a >= 0.10 second-best gap. Brilliant requires <= 0.02
loss, a legal capture of the offered non-pawn piece at the start of the reply
PV, and a material deficit of at least two pawn units that survives the whole
PV (at least three plies). Candidates require expected_before < 0.95 and
expected_after >= 0.50. These are this app's rules, not Chess.com's algorithm.
"""

import math
from collections.abc import Mapping

import chess


QUALITY_ORDER = (
    "brilliant", "great", "best", "excellent", "good", "inaccuracy",
    "mistake", "blunder", "forced",
)
QUALITY_COLORS = {
    "brilliant": "#0d9488", "great": "#2563eb", "best": "#16a34a",
    "excellent": "#65a30d", "good": "#64748b", "inaccuracy": "#ca8a04",
    "mistake": "#ea580c", "blunder": "#dc2626", "forced": "#7c3aed",
}
_LABELS = {
    key: key.capitalize() for key in QUALITY_ORDER
} | {"brilliant": "Brilliant candidate", "great": "Great candidate"}
_PIECE_VALUES = {
    chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3,
    chess.ROOK: 5, chess.QUEEN: 9, chess.KING: 0,
}


def _expected(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a finite expected score from 0 to 1")
    if not math.isfinite(value) or not 0 <= value <= 1:
        raise ValueError(f"{name} must be a finite expected score from 0 to 1")
    return float(value)


def _position(row):
    """Only legal, mutually consistent positions can support special awards."""
    try:
        board = chess.Board(row["fen_before"])
        move = chess.Move.from_uci(row["played_uci"])
        if not board.is_valid() or move not in board.legal_moves:
            return None, None
        after = board.copy()
        after.push(move)
        if row.get("fen_after") and chess.Board(row["fen_after"]).fen() != after.fen():
            return None, None
        return board, move
    except (KeyError, TypeError, ValueError):
        return None, None


def _material(board, color):
    return sum(
        value * (len(board.pieces(piece, color)) - len(board.pieces(piece, not color)))
        for piece, value in _PIECE_VALUES.items()
    )


def _sacrifice_evidence(board, move, pv):
    """Return sacrificed material only when a complete legal PV demonstrates it."""
    piece = board.piece_at(move.from_square)
    if piece.piece_type in (chess.PAWN, chess.KING) or move.promotion:
        return None
    if not isinstance(pv, (list, tuple)) or len(pv) < 3:
        return None

    initial_material = _material(board, piece.color)
    branch = board.copy()
    branch.push(move)
    minimum_loss = None
    try:
        for index, san in enumerate(pv):
            reply = branch.parse_san(san)
            if reply not in branch.legal_moves:
                return None
            if index == 0 and (
                not branch.is_capture(reply)
                or reply.to_square != move.to_square
                or branch.is_en_passant(reply)
            ):
                return None
            branch.push(reply)
            material_loss = initial_material - _material(branch, piece.color)
            # Following even one immediate recovery below the sacrifice
            # threshold is insufficient evidence for this conservative award.
            if material_loss < 2:
                return None
            minimum_loss = material_loss if minimum_loss is None else min(minimum_loss, material_loss)
    except (TypeError, ValueError):
        return None
    return minimum_loss


def classify_move(row: Mapping) -> dict:
    """Return key, label, expected-score loss and an auditable explanation.

    Required expected_before/after values are fractions from the mover's point
    of view. Engine move identities use UCI. Positions and a legal reply PV
    strengthen candidate labels; missing evidence never creates a candidate.
    """
    before = _expected(row.get("expected_before"), "expected_before")
    after = _expected(row.get("expected_after"), "expected_after")
    measured_loss = round(max(0.0, before - after), 12)
    loss = measured_loss
    best = bool(row.get("played_uci")) and row.get("played_uci") == row.get("best_uci")
    board, move = _position(row)

    if board is not None and board.legal_moves.count() == 1:
        key = "forced"
        loss = 0.0
        reason = "This was the only legal move; expected-score loss is treated as zero."
    else:
        if best:
            key = "best"
            loss = 0.0
            reason = "Matches the engine's top move; independent search noise is treated as zero loss."
        else:
            bands = (
                (0.02, "excellent", "0–2"),
                (0.05, "good", "over 2–5"),
                (0.10, "inaccuracy", "over 5–10"),
                (0.20, "mistake", "over 10–20"),
                (1.00, "blunder", "over 20–100"),
            )
            for cutoff, key, interval in bands:
                if loss <= cutoff:
                    reason = (
                        f"Independent expected-score loss: {loss * 100:.2f} percentage points "
                        f"({interval} point band)."
                    )
                    break

        candidate_position = before < 0.95 and after >= 0.50 and measured_loss <= 0.02
        if candidate_position and board is not None:
            sacrificed = _sacrifice_evidence(board, move, row.get("reply_pv"))
            if sacrificed is not None:
                key = "brilliant"
                reason = (
                    "Independent candidate: near-best (loss ≤2 percentage points), expected score "
                    "at least 0.50 afterward and below 0.95 beforehand. A legal capture of the "
                    f"offered piece leaves at least {sacrificed:g} pawn units of material lost "
                    "through the reply line (at least three plies). This is an estimate."
                )
            elif best:
                second = row.get("second_best_expected")
                if (
                    isinstance(second, (int, float)) and not isinstance(second, bool)
                    and math.isfinite(second) and 0 <= second <= 1
                    and round(before - second, 12) >= 0.10
                ):
                    key = "great"
                    reason = (
                        "Independent candidate: the engine's best move keeps an expected score "
                        "of at least 0.50, from below 0.95 beforehand; the second-best move is "
                        f"{(before - second) * 100:.2f} percentage points worse (threshold ≥10). "
                        "This is an estimate of a uniquely important move."
                    )

    mate_before = row.get("mate_before")
    mate_after = row.get("mate_after")
    if (
        not best and isinstance(mate_before, (int, float)) and mate_before > 0
        and (mate_after is None or isinstance(mate_after, (int, float)) and mate_after <= 0)
        and not (mate_after == 0 and after == 1.0)
    ):
        reason += " The engine's prior line contained a forced mate that this move no longer preserves."

    return {"key": key, "label": _LABELS[key], "loss": loss, "reason": reason}
