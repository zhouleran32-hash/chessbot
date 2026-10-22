"""Replay engine samples and explain only facts verified on their legal boards.

An engine variation is one sample of play, not proof that every reply is forced.
Descriptions deliberately distinguish an attack from a guaranteed material gain.
"""

import chess


_VALUES = {chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3, chess.ROOK: 5, chess.QUEEN: 9}
_CENTER = chess.SquareSet([chess.D4, chess.E4, chess.D5, chess.E5])


def _board(fen: str) -> chess.Board:
    try:
        if not isinstance(fen, str) or not fen.strip():
            raise ValueError("Missing position")
        board = chess.Board(fen)
        if not board.is_valid():
            raise ValueError("Invalid position")
    except ValueError as exc:
        raise ValueError("Provide a valid chess FEN") from exc
    return board


def _legal_move(board: chess.Board, san: str) -> chess.Move:
    if not isinstance(san, str):
        raise ValueError("Provide a legal move in SAN")
    move = board.parse_san(san)
    if move not in board.legal_moves:
        raise ValueError("Provide a legal move in SAN")
    return move


def _capture_pairs(board: chess.Board, color: chess.Color) -> set[tuple[int, int]]:
    """Legal captures for a color, excluding pinned pieces' pseudo-attacks."""
    probe = board.copy(stack=False)
    if probe.turn != color:
        probe.turn = color
        probe.ep_square = None
    return {
        (move.from_square, move.to_square) for move in probe.legal_moves
        if probe.is_capture(move) and probe.piece_at(move.to_square) is not None
        and probe.piece_type_at(move.to_square) != chess.KING
    }


def _piece_on(board: chess.Board, square: int) -> str:
    return f"the {chess.piece_name(board.piece_type_at(square))} on {chess.square_name(square)}"


def _move_description(before: chess.Board, move: chess.Move, after: chess.Board) -> str:
    piece = before.piece_at(move.from_square)
    name = chess.piece_name(piece.piece_type)
    origin, destination = map(chess.square_name, (move.from_square, move.to_square))
    facts = [f"Moves the {name} from {origin} to {destination}."]
    capture = before.is_capture(move)
    if before.is_castling(move):
        kingside = before.is_kingside_castling(move)
        rank = origin[1]
        facts.append(
            f"Castles {'kingside' if kingside else 'queenside'}, bringing the king toward the corner "
            f"and moving the rook from {'h' if kingside else 'a'}{rank} to {'f' if kingside else 'd'}{rank}."
        )
    elif capture:
        square = move.to_square
        if before.is_en_passant(move):
            square += -8 if piece.color == chess.WHITE else 8
        victim = before.piece_at(square)
        recapture = bool(before.move_stack) and before.peek().to_square == move.to_square
        # A previous move landing on this square is only a recapture when it
        # actually captured something, rather than a quiet move onto the square.
        if recapture:
            previous = before.copy()
            prior_move = previous.pop()
            recapture = previous.is_capture(prior_move)
        verb = "recaptures" if recapture else "captures"
        facts.append(f"It {verb} the {chess.piece_name(victim.piece_type)} on {chess.square_name(square)}"
                     + (" (en passant)." if before.is_en_passant(move) else "."))
    if move.promotion:
        facts.append(f"The pawn promotes to a {chess.piece_name(move.promotion)}.")
    if after.is_checkmate():
        facts.append("Delivers checkmate: the king is in check and the opponent has no legal reply.")
        return " ".join(facts)
    if after.is_stalemate():
        facts.append("Leaves stalemate: the opponent has no legal move and is not in check, so the game is drawn.")
        return " ".join(facts)
    if after.is_check():
        facts.append("Gives check, so the opponent must answer the attack on the king.")

    attacks_before = _capture_pairs(before, piece.color)
    attacks_after = _capture_pairs(after, piece.color)
    targets = sorted(
        (target for source, target in attacks_after if source == move.to_square),
        key=lambda target: _VALUES.get(after.piece_type_at(target), 0), reverse=True,
    )
    if targets:
        facts.append("From its new square it attacks " + ", ".join(_piece_on(after, target) for target in targets[:2])
                     + ".")

    # Moving a blocker can create a threat from another, stationary piece.
    discovered = sorted(
        (source, target) for source, target in attacks_after - attacks_before
        if source != move.to_square and before.piece_at(source) == after.piece_at(source)
    )
    for source, target in discovered[:2]:
        if target not in before.attacks(source):
            facts.append(f"This opens a line for {_piece_on(after, source)}, which now attacks {_piece_on(after, target)}.")
        else:
            facts.append(f"This allows {_piece_on(after, source)} to attack {_piece_on(after, target)} legally.")

    enemy_before = _capture_pairs(before, not piece.color)
    was_attacked = [source for source, target in enemy_before if target == move.from_square]
    enemy_after = _capture_pairs(after, not piece.color)
    if was_attacked and not any(target == move.to_square for _, target in enemy_after) and not capture:
        facts.append(f"Moves the {name} away from {_piece_on(before, was_attacked[0])}, which was attacking it.")

    home_rank = 0 if piece.color == chess.WHITE else 7
    if (piece.piece_type in (chess.KNIGHT, chess.BISHOP)
            and chess.square_rank(move.from_square) == home_rank
            and chess.square_rank(move.to_square) != home_rank):
        facts.append("Develops a piece off the back rank and into play.")
    if move.to_square in _CENTER:
        facts.append(f"Occupies the center on {destination}.")
    controlled = sorted(after.attacks(move.to_square) & _CENTER)
    if controlled:
        facts.append("Influences the center on " + ", ".join(map(chess.square_name, controlled)) + ".")
    if piece.piece_type == chess.PAWN and not capture and not move.promotion:
        # Count newly opened bishop/queen/rook rays, including empty squares.
        opened = []
        for square, slider in after.piece_map().items():
            if slider.color == piece.color and slider.piece_type in (chess.BISHOP, chess.ROOK, chess.QUEEN):
                if before.piece_at(square) == slider and after.attacks(square) - before.attacks(square):
                    opened.append(_piece_on(after, square))
        if opened:
            facts.append("Opens more room for " + " and ".join(opened[:2]) + " to move.")
        elif len(facts) == 1:
            facts.append("Advances the pawn toward promotion and attacks the squares diagonally in front of it.")
    if len(facts) == 1:
        facts.append("Repositions the piece; this move alone establishes no immediate capture or check.")
    return " ".join(facts)


def continuation_steps(
    fen: str, san_moves, expected_first: str | None = None, max_plies: int = 8,
) -> list[dict]:
    """Return the legal prefix of a sample line, with board facts for each ply.

    ``mover`` is relative to the side to move in ``fen``. A mismatched advertised
    first move invalidates the whole sample; an illegal later entry truncates it.
    """
    board = _board(fen)
    if type(max_plies) is not int or max_plies < 0:
        raise ValueError("max_plies must be a non-negative integer")
    if not isinstance(san_moves, (list, tuple)):
        return []
    expected = _legal_move(board, expected_first) if expected_first is not None else None
    player, steps = board.turn, []
    for san in san_moves[:max_plies]:
        if board.is_game_over():
            break
        try:
            move = _legal_move(board, san)
        except ValueError:
            break
        if not steps and expected is not None and move != expected:
            return []
        canonical = board.san(move)
        label = f"{board.fullmove_number}{'.' if board.turn == chess.WHITE else '...'} {canonical}"
        before = board.copy()
        board.push(move)
        steps.append({
            "fen_before": before.fen(), "fen_after": board.fen(),
            "san": canonical, "uci": move.uci(), "label": label,
            "mover": "you" if before.turn == player else "opponent",
            "description": _move_description(before, move, board),
        })
    return steps


def _material_balance(board: chess.Board, player: chess.Color) -> int:
    return sum(value * (len(board.pieces(kind, player)) - len(board.pieces(kind, not player)))
               for kind, value in _VALUES.items())


def _outcome(board: chess.Board, steps: list[dict]) -> str:
    final = chess.Board(steps[-1]["fen_after"])
    if final.is_checkmate():
        winner = "You deliver" if final.turn != board.turn else "The opponent delivers"
        return f"{winner} checkmate in this displayed line; the game ends here."
    if final.is_stalemate():
        return "The displayed line ends in stalemate, a draw."
    if final.is_insufficient_material():
        return "The displayed position has insufficient material to checkmate, so it is drawn."
    if final.is_seventyfive_moves():
        return "The displayed position is a draw under the automatic 75-move rule."
    change = _material_balance(final, board.turn) - _material_balance(board, board.turn)
    if change:
        direction = "improve" if change > 0 else "reduce"
        amount = abs(change)
        material = (f"The displayed captures and promotions {direction} your material balance by {amount} "
                    f"{'point' if amount == 1 else 'points'}, using the usual piece values.")
    else:
        material = "The material balance is unchanged in the displayed line."
    activity = []
    for color, owner in ((board.turn, "Your"), (not board.turn, "The opponent's")):
        attacks = sorted(
            _capture_pairs(final, color),
            key=lambda pair: _VALUES.get(final.piece_type_at(pair[1]), 0), reverse=True,
        )
        if attacks:
            source, target = attacks[0]
            activity.append(f"{owner} {chess.piece_name(final.piece_type_at(source))} on {chess.square_name(source)} "
                            f"attacks {_piece_on(final, target)}.")
    position = (" " + " ".join(activity)) if activity else ""
    next_player = "You move" if final.turn == board.turn else "The opponent moves"
    return material + position + f" {next_player} next."


def explain_recommendation(
    fen: str, best_move: str, best_pv, user_rating: int = 700,
) -> str:
    """Explain the recommendation, replies, and bounded outcome as Markdown."""
    if type(user_rating) is not int or user_rating < 0:
        raise ValueError("user_rating must be a non-negative integer")
    board = _board(fen)
    best = _legal_move(board, best_move)
    after = board.copy()
    after.push(best)
    purpose = _move_description(board, best, after)
    steps = continuation_steps(fen, best_pv, expected_first=best_move)
    result = [f"**What {board.san(best)} achieves**\n\n{purpose}"]
    if not steps:
        result.append("No legal continuation matching this recommendation was supplied. Replay the move and inspect the opponent's legal replies.")
        if after.is_checkmate() or after.is_stalemate() or after.is_insufficient_material():
            result.append(_outcome(board, [{"fen_after": after.fen()}]))
        return "\n\n".join(result)
    if not after.is_game_over() and len(steps) > 1:
        result.append("**One analyzed sample line**\n\nThese are the engine's analyzed choices; replies are not necessarily forced.")
        result.append("\n".join(
            f"- **{step['label']} — {'You' if step['mover'] == 'you' else 'Opponent'}:** {step['description']}"
            for step in steps
        ))
    elif len(steps) == 1 and not after.is_game_over():
        result.append("Only the recommendation was supplied; no analyzed opponent reply is available.")
    result.append("**Position reached**\n\n" + _outcome(board, steps))
    return "\n\n".join(result)
