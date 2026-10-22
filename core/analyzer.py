"""Find tactical blunders with python-chess and a Stockfish UCI process."""

import io
import math
import os
import shutil
import warnings
from pathlib import Path
from collections.abc import Callable

import chess
import chess.engine
import chess.pgn
import chess.svg


class GameAnalysisError(RuntimeError):
    """A game could not be evaluated reliably."""


class EngineUnavailableError(GameAnalysisError):
    """Stockfish could not be found or started."""


class InvalidPGNError(GameAnalysisError):
    """The input does not contain a valid game with legal moves."""


class GameAnalyzer:
    """Compare evaluations before and after each move by one player.

    Normal mode requires Stockfish. Set allow_mock=True to permit a development
    fallback when the executable is unavailable. Check is_mock before displaying
    results as coaching. Use a context manager or call close() to release the
    engine process. An analyzer instance should be used by one caller at a time.
    """

    MATE_SCORE = 100_000
    PIECE_VALUES = {
        chess.PAWN: 100, chess.KNIGHT: 320, chess.BISHOP: 330,
        chess.ROOK: 500, chess.QUEEN: 900,
    }

    def __init__(
        self,
        stockfish_path: str | Path | None = None,
        *,
        time_limit: float | None = 0.1,
        depth: int | None = None,
        allow_mock: bool = False,
    ):
        """Use a time limit, depth limit, or both (whichever is reached first).

        Omit stockfish_path to read STOCKFISH_PATH, falling back to stockfish on
        PATH. For depth-only analysis, pass time_limit=None with a positive depth.
        """
        if time_limit is not None and (
            isinstance(time_limit, bool)
            or not isinstance(time_limit, (int, float))
            or not math.isfinite(time_limit)
            or time_limit <= 0
        ):
            raise ValueError("time_limit must be a positive finite number or None")
        if depth is not None and (
            isinstance(depth, bool) or not isinstance(depth, int) or depth <= 0
        ):
            raise ValueError("depth must be a positive integer or None")
        if time_limit is None and depth is None:
            raise ValueError("Set a time_limit or depth to bound engine analysis")

        self.limit = chess.engine.Limit(time=time_limit, depth=depth)
        self.is_mock = False
        self.mock_reason: str | None = None
        self._engine: chess.engine.SimpleEngine | None = None
        self._closed = False
        candidate = stockfish_path if stockfish_path is not None else os.getenv("STOCKFISH_PATH", "stockfish")
        guidance = (
            f"Stockfish could not be started at {str(candidate)!r}. "
            "Download it from https://stockfishchess.org/download/ and set "
            "STOCKFISH_PATH to the executable, or pass stockfish_path explicitly."
        )
        try:
            executable = shutil.which(os.path.expanduser(os.fspath(candidate)))
            if executable is None:
                raise EngineUnavailableError(guidance)
            try:
                self._engine = chess.engine.SimpleEngine.popen_uci(executable, timeout=10.0)
            except (OSError, chess.engine.EngineError, TimeoutError) as exc:
                raise EngineUnavailableError(guidance) from exc
        except EngineUnavailableError as exc:
            if not allow_mock:
                raise
            self.is_mock = True
            self.mock_reason = str(exc)
            warnings.warn(
                "Stockfish is unavailable. Using mock analysis: a shallow material "
                "search for development and UI testing.",
                RuntimeWarning,
                stacklevel=2,
            )

    def analyze_game(
        self, pgn_text: str, player_color: str, eval_threshold: int = 150, *,
        progress_callback: Callable[[int, int], None] | None = None,
    ) -> list[dict]:
        """Return moves that lose strictly more than eval_threshold centipawns.

        Scores use the same player's perspective on both sides of the move.
        Mate scores use a conventional 100,000-centipawn bound; eval_drop is
        returned in pawns. The main line of a single PGN game is analyzed.
        An optional callback receives (completed_plies, total_plies), starting
        at zero and advancing after each replayed move, including the opponent's.
        """
        if self._closed:
            raise GameAnalysisError("This analyzer is closed. Create a new GameAnalyzer.")
        if not isinstance(player_color, str) or player_color.strip().lower() not in {"white", "black"}:
            raise ValueError("player_color must be 'white' or 'black'")
        color = chess.WHITE if player_color.strip().lower() == "white" else chess.BLACK
        if isinstance(eval_threshold, bool) or not isinstance(eval_threshold, int) or eval_threshold < 0:
            raise ValueError("eval_threshold must be a non-negative integer in centipawns")
        if not isinstance(pgn_text, str) or not pgn_text.strip():
            raise InvalidPGNError("Provide a PGN game containing legal moves.")

        try:
            game = chess.pgn.read_game(io.StringIO(pgn_text))
            if game is None or game.errors or not game.variations:
                raise InvalidPGNError("PGN is empty, malformed, or contains illegal moves.")
            board = game.board()
            if not board.is_valid():
                raise InvalidPGNError("PGN contains an invalid starting position.")
        except ValueError as exc:
            raise InvalidPGNError(f"Could not parse the PGN: {exc}") from exc

        moves = list(game.mainline_moves())
        if progress_callback:
            progress_callback(0, len(moves))
        blunders = []
        for completed, move in enumerate(moves, start=1):
            if move not in board.legal_moves:
                raise InvalidPGNError("PGN contains an illegal or null move.")
            if board.turn != color:
                board.push(move)
                if progress_callback:
                    progress_callback(completed, len(moves))
                continue

            before_board = board.copy()
            before_score, best_move = self._evaluate(board, color)
            if best_move is None:
                raise GameAnalysisError("Stockfish did not provide a legal best move.")
            played_san, best_san = board.san(move), board.san(best_move)
            board.push(move)
            after_score, _ = self._evaluate(board, color)
            drop = before_score - after_score
            if drop > eval_threshold:
                blunders.append({
                    "move_number": before_board.fullmove_number,
                    "fen_before": before_board.fen(),
                    "played_move": played_san,
                    "best_move": best_san,
                    "eval_drop": round(drop / 100.0, 2),
                    "board_svg": chess.svg.board(
                        before_board,
                        orientation=color,
                        size=400,
                        arrows=[
                            chess.svg.Arrow(move.from_square, move.to_square, color="#ff0000"),
                            chess.svg.Arrow(best_move.from_square, best_move.to_square, color="#00aa00"),
                        ],
                    ),
                })
            if progress_callback:
                progress_callback(completed, len(moves))
        return blunders

    def review_game(
        self, pgn_text: str, player_color: str, *,
        progress_callback: Callable[[int, int], None] | None = None,
        engine_details: bool = False,
    ) -> list[dict]:
        """Return engine evidence for every move played by one player.

        ``ply`` is the one-based index within the PGN main line, including
        opponent moves. Evaluations, mate distances and expected results use
        the requested player's perspective. Expectations use the Stockfish 16
        WDL model at each board's actual ply, including custom starting FENs.
        Before-move analysis requests two principal variations; after-move
        analysis examines the actual resulting position. Stored variations
        contain at most six legal SAN moves. Quality labels belong to callers.

        This richer API is independent of the legacy blunder-only contract.
        With engine_details, retain up to three scored candidates and twelve
        legal plies per line. Search time still follows this analyzer's limit.
        """
        if self._closed:
            raise GameAnalysisError("This analyzer is closed. Create a new GameAnalyzer.")
        if not isinstance(player_color, str) or player_color.strip().lower() not in {"white", "black"}:
            raise ValueError("player_color must be 'white' or 'black'")
        color_name = player_color.strip().lower()
        color = chess.WHITE if color_name == "white" else chess.BLACK
        if not isinstance(pgn_text, str) or not pgn_text.strip():
            raise InvalidPGNError("Provide a PGN game containing legal moves.")
        try:
            game = chess.pgn.read_game(io.StringIO(pgn_text))
            if game is None or game.errors or not game.variations:
                raise InvalidPGNError("PGN is empty, malformed, or contains illegal moves.")
            board = game.board()
            if not board.is_valid():
                raise InvalidPGNError("PGN contains an invalid starting position.")
        except ValueError as exc:
            raise InvalidPGNError(f"Could not parse the PGN: {exc}") from exc

        moves = list(game.mainline_moves())
        if progress_callback:
            progress_callback(0, len(moves))
        reviews = []
        for ply, move in enumerate(moves, start=1):
            if move not in board.legal_moves:
                raise InvalidPGNError("PGN contains an illegal or null move.")
            if board.turn != color:
                board.push(move)
            else:
                before_board = board.copy()
                choices = self._review_position(
                    before_board, color, alternatives=True,
                    candidate_count=3 if engine_details else 2,
                    pv_plies=12 if engine_details else 6,
                )
                before = choices[0]
                best = before["move"]
                if best is None:
                    raise GameAnalysisError("Stockfish did not provide a legal best move.")
                second = choices[1] if len(choices) > 1 else None
                played_san, best_san = board.san(move), board.san(best)
                board.push(move)
                after = self._review_position(board, color, pv_plies=12 if engine_details else 6)[0]
                reviews.append({
                    "ply": ply,
                    "move_number": before_board.fullmove_number,
                    "color": color_name,
                    "fen_before": before_board.fen(),
                    "fen_after": board.fen(),
                    "played_move": played_san,
                    "played_uci": move.uci(),
                    "best_move": best_san,
                    "best_uci": best.uci(),
                    "eval_before_cp": before["cp"],
                    "eval_after_cp": after["cp"],
                    "eval_drop": round(max(0, before["cp"] - after["cp"]) / 100.0, 2),
                    "mate_before": before["mate"],
                    "mate_after": after["mate"],
                    "expected_before": before["expected"],
                    "expected_after": after["expected"],
                    "second_best_expected": second["expected"] if second else None,
                    "second_best_move": before_board.san(second["move"]) if second else None,
                    "best_pv": before["pv"],
                    "reply_pv": after["pv"],
                    "legal_move_count": before_board.legal_moves.count(),
                    "depth": before["depth"],
                    "depth_after": after["depth"],
                })
                if engine_details:
                    reviews[-1]["candidates"] = [
                        {**choice, "move": before_board.san(choice["move"]),
                         "uci": choice["move"].uci()}
                        for choice in choices
                    ]
            if progress_callback:
                progress_callback(ply, len(moves))
        return reviews

    def review_move(self, fen: str, played_move: str, best_move: str) -> dict:
        """Review a selected move against an already advertised recommendation.

        Both moves must be legal SAN in a valid, ongoing starting position.
        The before-move search is constrained to ``best_move``: its score and
        PV evaluate that stored recommendation, without claiming it is the
        unrestricted best move at this search depth. The after-move search
        evaluates the played position from the same moving player's view.
        Limits and mock-mode labeling follow the analyzer instance, as with
        ``review_game``. Invalid input raises ValueError; engine evidence
        failures raise GameAnalysisError.
        """
        if self._closed:
            raise GameAnalysisError("This analyzer is closed. Create a new GameAnalyzer.")
        if not isinstance(fen, str) or not fen.strip():
            raise ValueError("Provide a valid FEN position.")
        try:
            board = chess.Board(fen)
        except ValueError as exc:
            raise ValueError(f"Could not parse the FEN: {exc}") from exc
        if not board.is_valid():
            raise ValueError("FEN contains an invalid position.")
        if not board.legal_moves or board.outcome() is not None:
            raise ValueError("The starting position must be ongoing and have legal moves.")

        moves = []
        for name, san in (("played_move", played_move), ("best_move", best_move)):
            if not isinstance(san, str) or not san.strip():
                raise ValueError(f"{name} must be a legal SAN move.")
            try:
                move = board.parse_san(san.strip())
            except ValueError as exc:
                raise ValueError(f"{name} must be a legal SAN move.") from exc
            if move not in board.legal_moves or board.san(move) != san.strip():
                raise ValueError(f"{name} must be a legal SAN move.")
            moves.append(move)
        played, best = moves
        color = board.turn
        before = self._review_position(board, color, root_moves=[best])[0]
        after_board = board.copy()
        after_board.push(played)
        after = self._review_position(after_board, color)[0]
        return {
            "move_number": board.fullmove_number,
            "color": "white" if color == chess.WHITE else "black",
            "fen_before": board.fen(),
            "fen_after": after_board.fen(),
            "played_move": board.san(played),
            "played_uci": played.uci(),
            "best_move": board.san(best),
            "best_uci": best.uci(),
            "eval_before_cp": before["cp"],
            "eval_after_cp": after["cp"],
            "eval_drop": round(max(0, before["cp"] - after["cp"]) / 100.0, 2),
            "mate_before": before["mate"],
            "mate_after": after["mate"],
            "expected_before": before["expected"],
            "expected_after": after["expected"],
            "best_pv": before["pv"],
            "reply_pv": after["pv"],
            "legal_move_count": board.legal_moves.count(),
            "depth": before["depth"],
            "depth_after": after["depth"],
        }

    def _review_position(
        self, board: chess.Board, color: chess.Color, *, alternatives: bool = False,
        root_moves: list[chess.Move] | None = None,
        candidate_count: int = 2, pv_plies: int = 6,
    ) -> list[dict]:
        """Retain full score information and validated variations for review."""
        outcome = board.outcome()
        if outcome is not None:
            score = (
                chess.engine.Cp(0) if outcome.winner is None else
                chess.engine.MateGiven if outcome.winner == color else chess.engine.Mate(0)
            )
            return [self._review_summary(board, score, [], None)]
        if self.is_mock:
            if root_moves is None:
                value, move = self._mock_search(board, depth=2)
            else:
                maximizing = board.turn == chess.WHITE
                value = -math.inf if maximizing else math.inf
                move = None
                for candidate in root_moves:
                    preview = board.copy()
                    preview.push(candidate)
                    candidate_value, _ = self._mock_search(preview, depth=1)
                    if move is None or (candidate_value > value if maximizing else candidate_value < value):
                        value, move = candidate_value, candidate
            own_value = value if color == chess.WHITE else -value
            return [self._review_summary(board, chess.engine.Cp(own_value), [move], 2)]
        options = {"info": chess.engine.INFO_SCORE | chess.engine.INFO_PV}
        if alternatives:
            options["multipv"] = candidate_count
        if root_moves is not None:
            options["root_moves"] = root_moves
        try:
            result = self._engine.analyse(board.copy(), self.limit, **options)
        except (chess.engine.EngineError, OSError, TimeoutError) as exc:
            raise GameAnalysisError(
                "Stockfish analysis failed. Check the executable and restart the analyzer."
            ) from exc
        if alternatives:
            if not isinstance(result, list) or not result:
                raise GameAnalysisError("Stockfish returned no analysis variations.")
            results = result[:candidate_count]
        else:
            results = [result]
        summaries = []
        for info in results:
            if not isinstance(info, dict) or not isinstance(info.get("score"), chess.engine.PovScore):
                raise GameAnalysisError("Stockfish returned no evaluation score.")
            pv = info.get("pv")
            if not isinstance(pv, (list, tuple)) or not pv:
                raise GameAnalysisError("Stockfish returned no legal PV variation.")
            if root_moves is not None and pv[0] not in root_moves:
                raise GameAnalysisError("Stockfish returned a PV outside the requested root recommendation.")
            summaries.append(self._review_summary(board, info["score"].pov(color), pv, info.get("depth"), pv_plies=pv_plies))
        return summaries

    @classmethod
    def _review_summary(cls, board: chess.Board, score: chess.engine.Score, pv: list, depth: int | None, *, pv_plies: int = 6) -> dict:
        """Convert evidence once, replaying every PV move before displaying it."""
        preview = board.copy()
        san_moves = []
        for move in pv:
            if not isinstance(move, chess.Move) or move not in preview.legal_moves:
                raise GameAnalysisError("Stockfish returned an illegal PV variation.")
            if len(san_moves) < pv_plies:
                san_moves.append(preview.san(move))
            preview.push(move)
        centipawns = score.score(mate_score=cls.MATE_SCORE)
        if centipawns is None:
            raise GameAnalysisError("Stockfish returned an unusable evaluation score.")
        return {
            "cp": centipawns,
            "mate": score.mate(),
            "expected": score.wdl(model="sf16", ply=board.ply()).expectation(),
            "move": pv[0] if pv else None,
            "pv": san_moves,
            "depth": depth if type(depth) is int and depth >= 0 else None,
        }

    def _evaluate(self, board: chess.Board, color: chess.Color) -> tuple[int, chess.Move | None]:
        terminal = self._terminal_score(board)
        if terminal is not None:
            return (terminal if color == chess.WHITE else -terminal), None
        if self.is_mock:
            score, best_move = self._mock_search(board, depth=2)
            return (score if color == chess.WHITE else -score), best_move

        try:
            info = self._engine.analyse(
                board, self.limit, info=chess.engine.INFO_SCORE | chess.engine.INFO_PV
            )
        except (chess.engine.EngineError, OSError, TimeoutError) as exc:
            raise GameAnalysisError(
                "Stockfish analysis failed. Check the executable and restart the analyzer."
            ) from exc
        score, pv = info.get("score"), info.get("pv")
        if not isinstance(score, chess.engine.PovScore):
            raise GameAnalysisError("Stockfish returned no evaluation score.")
        if not pv or not isinstance(pv[0], chess.Move) or pv[0] not in board.legal_moves:
            raise GameAnalysisError("Stockfish returned no legal best move.")
        centipawns = score.pov(color).score(mate_score=self.MATE_SCORE)
        if centipawns is None:
            raise GameAnalysisError("Stockfish returned an unusable evaluation score.")
        return centipawns, pv[0]

    @classmethod
    def _terminal_score(cls, board: chess.Board) -> int | None:
        """Score terminal boards from White's perspective without engine I/O."""
        outcome = board.outcome()
        if outcome is None:
            return None
        if outcome.winner is None:
            return 0
        return cls.MATE_SCORE if outcome.winner == chess.WHITE else -cls.MATE_SCORE

    @classmethod
    def _mock_search(cls, board: chess.Board, depth: int) -> tuple[int, chess.Move | None]:
        """Deterministic two-ply material search for development fixtures."""
        terminal = cls._terminal_score(board)
        if terminal is not None:
            return terminal, None
        if depth == 0:
            material = sum(
                value * (len(board.pieces(piece, chess.WHITE)) - len(board.pieces(piece, chess.BLACK)))
                for piece, value in cls.PIECE_VALUES.items()
            )
            return material, None

        maximizing = board.turn == chess.WHITE
        best_score = -math.inf if maximizing else math.inf
        best_move = None
        for move in sorted(board.legal_moves, key=lambda move: move.uci()):
            board.push(move)
            try:
                score, _ = cls._mock_search(board, depth - 1)
            finally:
                board.pop()
            if best_move is None or (score > best_score if maximizing else score < best_score):
                best_score, best_move = score, move
        return int(best_score), best_move

    def close(self) -> None:
        """Release the engine process. Safe to call more than once."""
        if self._closed:
            return
        self._closed = True
        if self._engine is not None:
            try:
                self._engine.quit()
            except (chess.engine.EngineError, OSError, TimeoutError):
                self._engine.close()
            finally:
                self._engine = None

    def __enter__(self):
        if self._closed:
            raise GameAnalysisError("This analyzer is closed. Create a new GameAnalyzer.")
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()
