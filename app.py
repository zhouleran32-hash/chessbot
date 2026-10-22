"""Interactive ChessBot dashboard. Run with: streamlit run app.py."""

import hashlib
import io
import os
from pathlib import Path
import time
from datetime import datetime

import chess
import chess.pgn
import chess.svg
import streamlit as st

from core.analyzer import EngineUnavailableError, GameAnalysisError, GameAnalyzer
from core.board_widget import board_state, chess_board
from core.chess_client import ChessDotComClient, ChessDotComError
from core.coach import ChessCoach, CoachingError
from core.config import load_config
from core.continuation import continuation_steps, explain_recommendation
from core.primer_ui import render_primer
from core.silman_ui import render_silman
from core.rag_engine import ChessBookKnowledgeBase, KnowledgeBaseError
from core.ratings import RATING_INTERVAL, choose_rating_category, refresh_rating_snapshot
from core.move_quality import classify_move
from core.review_ui import render_move_review
from core.stockfish_ui import render_stockfish_review
from core.ui import study_room_styles


def _retry_cached(cache_name: str, key) -> None:
    """Clear a failed attempt before the button's normal Streamlit rerun."""
    st.session_state[cache_name].pop(key, None)


def _retry_detailed_analysis(game_url: str) -> None:
    st.session_state.analyses[game_url].pop("detailed_error", None)


def _initialize_session(config) -> None:
    defaults = {
        "games": [], "loaded_username": "", "analyses": {}, "reviews": {}, "stockfish_analyses": {},
        "book_advice": {}, "weekly_plan": None, "book_uploads": {},
        "library_revision": 0, "fetch_error": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
    if "knowledge_base" not in st.session_state:
        st.session_state.knowledge_base = ChessBookKnowledgeBase(
            persist_directory=config.chroma_dir, openai_api_key=config.openai_api_key or None,
        )


def _engine_status(path: str, refresh: bool) -> dict:
    status = st.session_state.get("engine_status")
    if refresh or not status or status["path"] != path or time.monotonic() - status["checked"] > 60:
        try:
            with GameAnalyzer(path, time_limit=0.01, depth=1):
                status = {"ready": True, "message": "Stockfish is ready"}
        except EngineUnavailableError as error:
            status = {"ready": False, "message": str(error)}
        status.update(path=path, checked=time.monotonic())
        st.session_state.engine_status = status
    return status


def _fetch_games(username: str, *, select_latest: bool = False) -> None:
    st.session_state.fetch_error = None
    if not username.strip():
        st.session_state.fetch_error = "Enter a Chess.com username first."
        return
    try:
        with st.spinner("Finding your latest games…"):
            games = ChessDotComClient().get_recent_games(username, count=10)
    except (ChessDotComError, ValueError) as error:
        st.session_state.fetch_error = str(error)
        return

    normalized = username.strip().lower()
    if normalized != st.session_state.loaded_username:
        st.session_state.analyses = {}
        st.session_state.stockfish_analyses = {}
        st.session_state.reviews = {}
        st.session_state.weekly_plan = None
        st.session_state.pop("selected_game", None)
    elif st.session_state.get("selected_game") not in {game["game_url"] for game in games}:
        st.session_state.pop("selected_game", None)
    st.session_state.games = games
    st.session_state.loaded_username = normalized
    refresh_rating_snapshot(normalized, st.session_state.setdefault("rating_snapshots", {}), force=True)
    if select_latest and games:
        st.session_state.selected_game = games[0]["game_url"]


def _start_review(select_latest: bool) -> None:
    """Submit the welcome form before keyed sidebar controls render again."""
    username = st.session_state.get("welcome_username", "").strip()
    st.session_state.username = username
    _fetch_games(username, select_latest=select_latest)


def _open_primer() -> None:
    st.session_state.main_section = "The Soviet Chess Primer"


def _open_silman() -> None:
    st.session_state.main_section = "Silman's endgame course"


def _welcome(config) -> None:
    review, primer = st.columns([1.3, 1], gap="medium")
    with review:
        with st.container(border=True, key="welcome_review"):
            st.caption("01 / REVIEW YOUR GAMES")
            st.subheader("Find your next better move.")
            st.write("Bring in a recent game. Explore the moments that mattered and take one useful habit to your next game.")
            with st.form("welcome_games_form", border=False):
                st.text_input(
                    "Chess.com player", value=st.session_state.get("username", config.chess_com_username),
                    key="welcome_username", placeholder="Your Chess.com username",
                    help="Your latest ten completed games. No Chess.com login needed.",
                )
                st.form_submit_button(
                    "Review my games", key="start_review", type="primary", width="stretch",
                    icon=":material/arrow_forward:", icon_position="right",
                    on_click=_start_review, args=(config.review_only,),
                )
            if st.session_state.fetch_error:
                st.error(st.session_state.fetch_error)
            elif st.session_state.loaded_username:
                st.info("No completed games were found. Try another player or return after playing a game.")
            st.caption("Load a game → explore a mistake → build a better habit")
    with primer:
        with st.container(border=True, key="welcome_primer"):
            st.caption("02 / LEARN ONE IDEA")
            st.subheader("Build your chess intuition.")
            st.image(
                chess.svg.board(
                    chess.Board(), size=260, coordinates=False,
                    colors={"square light": "#E6E4D5", "square dark": "#73866B"},
                ),
                width="stretch", alt="Starting chess position, previewing the lesson boards",
            )
            st.write("Work through the Primer, or start Silman's endgame course with the beginner mating methods.")
            if config.review_only:
                st.button("Open the Primer", key="start_primer", width="stretch", icon=":material/menu_book:", on_click=_open_primer)
                st.button("Open endgames", key="start_silman", width="stretch", icon=":material/school:", on_click=_open_silman)
            else:
                st.caption("Open The Soviet Chess Primer or Silman's endgame course in the tabs above.")
            st.caption("Primer chapters 1–10 + appendix · Silman parts 1–9 · progress saved")


def _book_uploader(config) -> None:
    uploaded = st.file_uploader("Feed a Chess Book", type=["pdf"], key="book_pdf")
    st.caption("Text PDFs become searchable book passages. Scans need OCR first.")
    if uploaded is None:
        return
    content = uploaded.getvalue()
    digest = hashlib.sha256(content).hexdigest()
    previous = st.session_state.book_uploads.get(digest)
    if previous is None:
        # Keep citations readable while isolating different files with the same name.
        filename = Path(uploaded.name.replace("\\", "/")).name
        if filename in {"", ".", ".."}:
            filename = "chess-book.pdf"
        target = config.books_dir / digest / filename
        try:
            with st.spinner("Reading and indexing your chess book…"):
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(content)
                chunks = st.session_state.knowledge_base.ingest_pdf(str(target))
            previous = {"name": filename, "chunks": chunks}
            if chunks:
                st.session_state.library_revision += 1
                st.session_state.reviews = {}
                st.session_state.book_advice = {}
        except (KnowledgeBaseError, OSError, ValueError) as error:
            previous = {"name": filename, "error": str(error)}
        st.session_state.book_uploads[digest] = previous
    if previous.get("error"):
        st.error(previous["error"])
        st.button("Retry indexing", on_click=_retry_cached, args=("book_uploads", digest))
    elif previous["chunks"]:
        st.success(f"Indexed {previous['name']} · {previous['chunks']} passages")
    else:
        st.warning("No explanatory text was found. Try a text PDF or run OCR on this book.")


def _request_rating_refresh() -> None:
    refresh_rating_snapshot(
        st.session_state.get("username", ""),
        st.session_state.setdefault("rating_snapshots", {}), force=True,
    )


@st.fragment(run_every=RATING_INTERVAL)
def _rating_controls(config) -> None:
    """Poll independently; redraw the app only when its coaching level changes."""
    username = st.session_state.get("username", config.chess_com_username).strip().lower()
    if st.session_state.get("rating_profile") != username:
        st.session_state.rating_profile = username
        st.session_state.user_rating = config.user_rating
        st.session_state.pop("rating_category", None)
    snapshots = st.session_state.setdefault("rating_snapshots", {})
    snapshot = refresh_rating_snapshot(username, snapshots)
    ratings = snapshot["ratings"]
    source = None
    if ratings:
        preferences = st.session_state.setdefault("rating_preferences", {})
        categories = [name for name in ("rapid", "blitz", "bullet", "daily") if name in ratings]
        if st.session_state.get("rating_category") not in categories:
            st.session_state.rating_category = choose_rating_category(ratings, preferences.get(username))
        category = st.selectbox(
            "Rating category", categories, key="rating_category", format_func=str.title,
            filter_mode=None, help="Chess.com keeps separate ratings for each time control.",
        )
        preferences[username] = category
        st.session_state.user_rating = ratings[category]["rating"]
        source = {"username": username, "category": category, "stale": bool(snapshot["error"])}
        st.metric(f"{category.title()} rating", st.session_state.user_rating)
        if snapshot["error"]:
            st.warning("Showing your last successful rating update. " + snapshot["error"])
        else:
            age = max(0, int(time.monotonic() - snapshot["updated_at"]))
            checked = "just now" if age < 60 else f"{age // 60} min ago"
            st.caption(f"Checked {checked} · checks every minute")
        st.caption("Latest published by Chess.com. Changes can take time to appear here.")
    else:
        if username:
            if snapshot["error"]:
                st.warning("Current Chess.com rating is unavailable. " + snapshot["error"])
            else:
                st.caption("This player has no published rapid, blitz, bullet, or daily rating yet.")
        st.number_input(
            "Manual coaching level", min_value=0, max_value=4000,
            step=1, key="user_rating",
            help="Fallback for coaching while a current Chess.com rating is unavailable. This is not a live rating.",
        )
    st.session_state.rating_source = source
    if username:
        st.button("Refresh rating", key="refresh_live_rating", icon=":material/refresh:", on_click=_request_rating_refresh)
    signature = (username, st.session_state.user_rating, source and source["category"], source and source["stale"])
    previous = st.session_state.get("rating_display_signature")
    st.session_state.rating_display_signature = signature
    if previous is not None and previous != signature:
        # A timed fragment run must also update the main badge and coaching.
        st.rerun()


def _sidebar(config) -> tuple[dict, bool, str, str | None]:
    with st.sidebar:
        st.header("ChessBot")
        st.caption("YOUR PERSONAL CHESS CLUB")
        with st.form("fetch_games_form"):
            username = st.text_input("Chess.com username", value=config.chess_com_username, key="username", placeholder="Your username")
            if st.form_submit_button("Fetch Games", type="primary", width="stretch", icon=":material/download:"):
                _fetch_games(username, select_latest=config.review_only)
        _rating_controls(config)
        if st.session_state.fetch_error:
            st.error(st.session_state.fetch_error)
        if st.session_state.loaded_username:
            st.caption(f"{st.session_state.loaded_username} · {len(st.session_state.games)} recent games in this session")
        status = _engine_status(config.stockfish_path, False)
        if status["ready"]:
            st.badge("Stockfish is ready", icon=":material/check_circle:", color="green")
            allow_mock = False
            with st.expander("Engine settings"):
                st.caption("Stockfish checks the moves in your games.")
                if st.button("Check again", icon=":material/refresh:", help="Recheck your configured Stockfish executable."):
                    _engine_status(config.stockfish_path, True)
                    st.rerun()
        else:
            st.warning("Stockfish is unavailable")
            if st.button("Check again", icon=":material/refresh:"):
                _engine_status(config.stockfish_path, True)
                st.rerun()
            allow_mock = st.checkbox("Use mock analysis", value=False, key="allow_mock", help="Development only: a simple material search, with no Stockfish accuracy.")
            with st.expander("Set up Stockfish"):
                st.write(status["message"])
                st.markdown("[Download Stockfish](https://stockfishchess.org/download/) and set `STOCKFISH_PATH` in `.env`.")
        anthropic_key = os.getenv("ANTHROPIC_API_KEY", "").strip()
        anthropic_model = os.getenv("ANTHROPIC_MODEL", "").strip()
        use_anthropic = not config.openai_api_key and anthropic_key and anthropic_model
        if config.review_only:
            provider = "Anthropic" if use_anthropic else "OpenAI · GPT-4o"
        else:
            st.subheader("Your chess library")
            _book_uploader(config)
            st.caption("Book indexing and semantic search use OPENAI_API_KEY. Until a book is indexed, beginner principles are available for free.")
            st.subheader("AI coach")
            provider = st.selectbox(
                "Coach provider", ["OpenAI · GPT-4o", "Anthropic"], key="coach_provider",
                index=1 if use_anthropic else 0, filter_mode=None,
            )
        ready = bool(config.openai_api_key) if provider.startswith("OpenAI") else bool(anthropic_key and anthropic_model)
        if ready:
            st.caption("AI reviews are enabled for the blunder you view.")
        elif not config.review_only:
            setting = "OPENAI_API_KEY" if provider.startswith("OpenAI") else "ANTHROPIC_API_KEY and ANTHROPIC_MODEL"
            st.caption(f"Add {setting} to .env to enable AI reviews.")
        else:
            st.caption("Position-based feedback is ready. No AI key is needed.")
        st.caption("Games and notes stay in this session.")
    return status, allow_mock, provider, anthropic_model or None


def _date_label(game: dict) -> str:
    return datetime.fromisoformat(game["played_at"]).strftime("%d %b %Y · %H:%M")


def _game_label(game: dict) -> str:
    opponent = game["black_username"] if game["user_color"] == "white" else game["white_username"]
    return f"{_date_label(game)} · vs {opponent} · {game['result'].title()}"


def _analyze(game: dict, config, status: dict, allow_mock: bool, *, detailed: bool = False) -> dict | None:
    signature = hashlib.sha256(repr((
        game["pgn"], game["user_color"], config.stockfish_path, status["ready"], allow_mock, "review-v2",
    )).encode()).hexdigest()
    record = st.session_state.analyses.get(game["game_url"])
    if record and record["signature"] != signature:
        del st.session_state.analyses[game["game_url"]]
        st.session_state.weekly_plan = None
        record = None
    if not status["ready"] and not allow_mock:
        st.info("Set STOCKFISH_PATH or enable mock analysis in the sidebar to review this game.")
        return None
    if record is None or (detailed and "moves" not in record and not record.get("error") and not record.get("detailed_error")):
        progress = st.progress(0.0, text="Preparing your game…")

        def update(done: int, total: int) -> None:
            progress.progress(done / max(total, 1), text=f"Reviewing moves · {done} of {total}")

        try:
            with GameAnalyzer(config.stockfish_path, time_limit=0.2 if detailed else 0.1, allow_mock=allow_mock) as analyzer:
                if detailed:
                    moves = analyzer.review_game(game["pgn"], game["user_color"], progress_callback=update)
                    for move in moves:
                        move["classification"] = (
                            {"key": "preview", "label": "Preview", "loss": 0.0,
                             "reason": "Development preview from a shallow material search; no Stockfish quality label is assigned."}
                            if analyzer.is_mock else classify_move(move)
                        )
                    # Keep the existing material-loss contract for quick review and weekly plans.
                    blunders = (record or {}).get("blunders", [move for move in moves if move["eval_drop"] > 1.5])
                else:
                    blunders = analyzer.analyze_game(game["pgn"], game["user_color"], progress_callback=update)
                is_mock = analyzer.is_mock
            parsed = chess.pgn.read_game(io.StringIO(game["pgn"]))
            color = chess.WHITE if game["user_color"] == "white" else chess.BLACK
            player_moves = sum(node.parent.board().turn == color for node in parsed.mainline())
            continuations = (record or {}).get("continuations", {})
            record = {"signature": signature, "blunders": blunders, "is_mock": is_mock, "player_moves": player_moves,
                      "continuations": continuations}
            if detailed:
                record["moves"] = moves
            st.session_state.weekly_plan = None
        except (GameAnalysisError, ValueError) as error:
            if detailed and record is not None:
                record = {**record, "detailed_error": str(error)}
            else:
                record = {"signature": signature, "error": str(error)}
        finally:
            progress.empty()
        st.session_state.analyses[game["game_url"]] = record
    if detailed and record.get("detailed_error"):
        st.error(record["detailed_error"])
        st.button("Retry detailed analysis", on_click=_retry_detailed_analysis, args=(game["game_url"],))
        return None
    if record.get("error"):
        st.error(record["error"])
        st.button("Retry analysis", on_click=_retry_cached, args=("analyses", game["game_url"]))
        return None
    return record


def _book_principles(category: str) -> None:
    key = (st.session_state.library_revision, category)
    cache = st.session_state.book_advice
    cached = cache.get(key)
    if cached is None:
        try:
            excerpts = st.session_state.knowledge_base.search_advice(ChessCoach.CATEGORY_DETAILS[category]["query"], n_results=1)
            cached = {"excerpts": excerpts}
        except (KnowledgeBaseError, ValueError) as error:
            cached = {"error": str(error)}
        cache[key] = cached
    st.markdown("**A principle to practice**")
    if cached.get("error"):
        st.warning(cached["error"])
        st.button("Retry book search", on_click=_retry_cached, args=("book_advice", key))
    else:
        for excerpt in cached["excerpts"]:
            st.markdown(excerpt)
    st.markdown(f"**Your mental check**\n\n{ChessCoach.CATEGORY_DETAILS[category]['mental_check']}")


def _stockfish_review(game: dict, config, status: dict) -> None:
    """Run a deeper, separately cached review only on explicit button clicks."""
    st.markdown("### Detailed Stockfish review")
    st.caption("Compare the engine's candidate moves and explore their replies. Your independent assessments remain in Every move.")
    if not status["ready"]:
        st.info("This view needs a working Stockfish engine. Set STOCKFISH_PATH and use Check again in the sidebar.")
        return
    signature = hashlib.sha256(repr((
        game["pgn"], game["user_color"], config.stockfish_path, "stockfish-detail-v1", 1.0, 3, 12,
    )).encode()).hexdigest()
    cache = st.session_state.stockfish_analyses
    record = cache.get(game["game_url"])
    if record and record["signature"] != signature:
        record = None
        cache.pop(game["game_url"], None)
    if record is None:
        st.write("Search every move you played, compare up to three options, and keep longer lines to replay. "
                 "Allow roughly two seconds per move you played. Results stay ready while you explore.")
    elif record.get("error"):
        st.error(record["error"])
    label = "Run Stockfish review" if record is None else "Retry Stockfish review" if record.get("error") else "Run Stockfish again"
    if st.button(label, key="run_stockfish", type="primary" if not record or record.get("error") else "secondary"):
        progress = st.progress(0.0, text="Preparing Stockfish review…")
        def update(done: int, total: int) -> None:
            progress.progress(done / max(total, 1), text=f"Stockfish review · {done} of {total} game plies")
        try:
            with GameAnalyzer(config.stockfish_path, time_limit=1.0) as analyzer:
                moves = analyzer.review_game(game["pgn"], game["user_color"], engine_details=True, progress_callback=update)
            record = {"signature": signature, "moves": moves}
        except (GameAnalysisError, ValueError) as error:
            # A failed rerun must not discard a completed report.
            record = {**(record or {"signature": signature}), "error": str(error)}
        finally:
            progress.empty()
        cache[game["game_url"]] = record
        st.rerun()
    if record and "moves" in record:
        render_stockfish_review(game, record)


def _continuation_key(blunder: dict) -> tuple:
    return (blunder["fen_before"], blunder["played_move"], blunder["best_move"])


def _retry_continuation(game_url: str, key: tuple) -> None:
    st.session_state.analyses[game_url].get("continuations", {}).pop(key, None)


def _continuation_details(record: dict, blunder: dict, config) -> dict:
    """Reuse matching full-review evidence or analyze only this selected position."""
    if record["is_mock"]:
        return {}
    key = _continuation_key(blunder)
    cache = record.setdefault("continuations", {})
    if key not in cache:
        matching = next((move for move in record.get("moves", [])
                         if _continuation_key(move) == key), None)
        if matching is not None:
            cache[key] = {"analysis": matching}
        else:
            try:
                with st.spinner("Exploring the suggested move…"):
                    with GameAnalyzer(config.stockfish_path, time_limit=0.5) as analyzer:
                        analysis = analyzer.review_move(*key)
                cache[key] = {"analysis": analysis}
            except (GameAnalysisError, ValueError) as error:
                cache[key] = {"error": str(error)}
    return cache[key]


def _coaching(game: dict, record: dict, index: int, config, provider: str, anthropic_model: str | None, analysis: dict | None = None) -> None:
    blunder = record["blunders"][index]
    category = ChessCoach.classify_blunder(blunder["fen_before"], blunder["played_move"], blunder["best_move"])
    st.caption(f"Practice theme: {ChessCoach.CATEGORY_DETAILS[category]['title']} · suggested by board patterns")
    is_openai = provider.startswith("OpenAI")
    api_key = config.openai_api_key if is_openai else os.getenv("ANTHROPIC_API_KEY", "").strip()
    rating = st.session_state.get("user_rating", config.user_rating)
    if not api_key or (not is_openai and not anthropic_model):
        st.caption("Position-based coaching · the suggested move and its continuation")
        st.markdown(ChessCoach.review_blunder_locally(blunder["fen_before"], blunder["played_move"], blunder["best_move"], user_rating=rating, analysis=analysis))
        if not config.review_only:
            _book_principles(category)
        return
    key = (game["game_url"], record["signature"], index, st.session_state.library_revision, provider, anthropic_model, rating)
    cached = st.session_state.reviews.get(key)
    if cached is None:
        try:
            with st.spinner("Your coach is reviewing this position…"):
                if is_openai:
                    from openai import OpenAI
                    client = OpenAI(api_key=api_key, max_retries=0, timeout=30)
                else:
                    from anthropic import Anthropic
                    client = Anthropic(api_key=api_key, max_retries=0, timeout=30)
                with client:
                    coach = ChessCoach(client, st.session_state.knowledge_base, model="gpt-4o" if is_openai else anthropic_model)
                    review = coach.review_blunder(
                        fen=blunder["fen_before"], played_move=blunder["played_move"],
                        best_move=blunder["best_move"], eval_drop=blunder["eval_drop"], user_rating=rating,
                    )
            cached = {"text": review}
        except CoachingError as error:
            cached = {"error": str(error)}
        except Exception:
            # SDK initialization errors can contain configuration values; keep those private.
            cached = {"error": "The AI coach could not start. Check your provider settings and try again."}
        st.session_state.reviews[key] = cached
    if cached.get("error"):
        st.warning(cached["error"])
        st.button("Retry coaching", on_click=_retry_cached, args=("reviews", key))
        st.markdown(ChessCoach.review_blunder_locally(blunder["fen_before"], blunder["played_move"], blunder["best_move"], user_rating=rating, analysis=analysis))
        if not config.review_only:
            _book_principles(category)
    else:
        st.markdown(cached["text"])
        if analysis:
            st.markdown(explain_recommendation(blunder["fen_before"], blunder["best_move"], analysis.get("best_pv"), user_rating=rating))


def _mainline(pgn: str) -> list[dict]:
    """Replay a game into positions. Each ply's FEN is the position after that move."""
    parsed = chess.pgn.read_game(io.StringIO(pgn))
    if parsed is None:
        return [{"ply": 0, "fen": chess.STARTING_FEN, "label": "Start", "last": None}]
    board = parsed.board()
    positions = [{"ply": 0, "fen": board.fen(), "label": "Start", "last": None}]
    for move in parsed.mainline_moves():
        label = f"{board.fullmove_number}{'.' if board.turn == chess.WHITE else '...'} {board.san(move)}"
        last = [chess.square_name(move.from_square), chess.square_name(move.to_square)]
        board.push(move)
        positions.append({"ply": len(positions), "fen": board.fen(), "label": label, "last": last})
    return positions


def _ply_for_fen(positions: list[dict], fen: str) -> int | None:
    for item in positions:
        if item["fen"] == fen:
            return item["ply"]
    return None


def _mistake_mark(drop: float) -> str:
    return " ??" if drop >= 3 else " ?"


def _focus_mistake(ply_key: str, plies: list[int | None]) -> None:
    st.session_state.quick_review_line = "Your game"
    st.session_state.quick_line_step = 0
    choice = st.session_state.get("review_mistake")
    if isinstance(choice, int) and 1 <= choice <= len(plies) and isinstance(plies[choice - 1], int):
        st.session_state[ply_key] = plies[choice - 1]


def _step_review(ply_key: str, delta: int, last: int) -> None:
    st.session_state[ply_key] = max(0, min(last, st.session_state.get(ply_key, 0) + delta))


def _reset_quick_line() -> None:
    st.session_state.quick_line_step = 0


def _game_review(config, status: dict, allow_mock: bool, provider: str, anthropic_model: str | None) -> None:
    games = st.session_state.games
    if not games:
        _welcome(config)
        return
    st.subheader("Recent games")
    st.caption(f"The latest finished games for {st.session_state.loaded_username}. Results are from your side of the board.")
    recent_games = [
        {"White": f"{game['white_username']} ({game['white_rating'] or '—'})",
         "Black": f"{game['black_username']} ({game['black_rating'] or '—'})",
         "Result": game["result"].title(), "Date (UTC)": _date_label(game)}
        for game in games
    ]
    if config.review_only:
        with st.expander(f"Browse all {len(games)} recent games"):
            st.dataframe(recent_games, hide_index=True, width="stretch", height=210)
    else:
        st.dataframe(recent_games, hide_index=True, width="stretch", height="auto")
    by_url = {game["game_url"]: game for game in games}
    selected = st.selectbox("Choose a game", list(by_url), index=None, key="selected_game", format_func=lambda url: _game_label(by_url[url]), placeholder="Select a game to start your review", filter_mode=None)
    if selected is None:
        return
    game = by_url[selected]
    st.subheader("This game")
    st.caption(f"You played {game['user_color']} · {_game_label(game)} (UTC)")
    detail = st.radio(
        "Review detail", ["Every move", "Key mistakes", "Stockfish analysis"], horizontal=True, key="review_detail",
        help="Every move gives independent quality labels. Key mistakes is a faster review. Stockfish analysis compares more candidate moves with longer searches and replay lines.",
    )
    if detail == "Stockfish analysis":
        _stockfish_review(game, config, status)
        return
    record = _analyze(game, config, status, allow_mock, detailed=detail == "Every move")
    if record is None:
        return
    if detail == "Every move":
        render_move_review(game, record, st.session_state.get("user_rating", config.user_rating))
        return
    if record["is_mock"]:
        st.warning("Mock analysis · development preview using a simple material search. These findings are not Stockfish evaluations.")
    columns = st.columns(3)
    accuracy = game.get("accuracy")
    columns[0].metric("Accuracy", f"{accuracy:.1f}%" if accuracy is not None else "—", help="Published Chess.com accuracy for this player, when supplied by the API.")
    columns[1].metric("Blunders", len(record["blunders"]))
    columns[2].metric("Moves reviewed", record["player_moves"])
    if accuracy is None:
        st.caption("Chess.com did not publish an accuracy score for this game.")
    else:
        st.caption("Accuracy is the score published by Chess.com; blunders below use the selected analyzer.")
    st.caption("A marked move lost more than 1.5 pawns. Red is what you played. Green is the suggestion. The bar is that loss, not a running engine score.")
    blunders = record["blunders"]
    if not blunders:
        st.success("No blunders above the 1.5-pawn threshold were found in this game.")
        st.caption("Keep checking your opponent's checks, captures, and threats before each move.")
        return
    positions = _mainline(game["pgn"])
    mistake_plies = [_ply_for_fen(positions, item["fen_before"]) for item in blunders]
    ply_key = f"review_ply_{game['game_url']}"
    if st.session_state.get("review_mistake_for") != record["signature"]:
        st.session_state.review_mistake_for = record["signature"]
        st.session_state.review_mistake = 1
        first_ply = next((ply for ply in mistake_plies if ply is not None), 0)
        st.session_state[ply_key] = first_ply
    number = st.session_state.get("review_mistake", 1)
    if len(blunders) > 1:
        number = st.selectbox(
            "Mistake", list(range(1, len(blunders) + 1)),
            format_func=lambda choice: (
                f"{choice}. Move {blunders[choice - 1]['move_number']} · {blunders[choice - 1]['played_move']}"
                f"{_mistake_mark(blunders[choice - 1]['eval_drop'])}"
            ),
            key="review_mistake",
            on_change=_focus_mistake,
            args=(ply_key, mistake_plies),
            filter_mode=None,
        )
    blunder = blunders[number - 1]
    details = _continuation_details(record, blunder, config)
    analysis = details.get("analysis")
    line_token = (record["signature"], _continuation_key(blunder))
    if st.session_state.get("quick_line_for") != line_token:
        st.session_state.quick_line_for = line_token
        st.session_state.quick_line_step = 0
    ply = st.session_state.get(ply_key, 0)
    fallback = mistake_plies[number - 1]
    if not isinstance(ply, int) or not 0 <= ply < len(positions):
        ply = fallback if isinstance(fallback, int) else 0
    shown = positions[ply]
    board_column, coach_column = st.columns([1.05, 1], gap="medium")
    replaying = False
    move_description = ""
    navigation_key, navigation_index, navigation_last = ply_key, ply, len(positions) - 1
    with board_column:
        if analysis:
            mode = st.radio("Board line", ["Your game", "Better move", "After your move"],
                            horizontal=True, key="quick_review_line", on_change=_reset_quick_line)
            if mode != "Your game":
                replaying = True
                start = chess.Board(blunder["fen_before"])
                if mode == "After your move":
                    start.push_san(blunder["played_move"])
                line = analysis.get("best_pv") if mode == "Better move" else analysis.get("reply_pv")
                steps = continuation_steps(start.fen(), line, expected_first=blunder["best_move"] if mode == "Better move" else None)
                cursor = st.session_state.get("quick_line_step", 0)
                if type(cursor) is not int or not 0 <= cursor <= len(steps):
                    st.session_state.quick_line_step = 0
                step = st.slider("Line position", 0, len(steps), key="quick_line_step") if steps else 0
                if step:
                    item = steps[step - 1]
                    played = chess.Move.from_uci(item["uci"])
                    shown = {"fen": item["fen_after"], "label": item["label"],
                             "last": [chess.square_name(played.from_square), chess.square_name(played.to_square)]}
                    move_description = item["description"]
                else:
                    shown = {"fen": start.fen(), "label": f"Start · {mode.lower()}", "last": None}
                navigation_key, navigation_index, navigation_last = "quick_line_step", step, len(steps)
                st.caption("Stockfish's sample continuation. Other replies may be available.")
    teaching = shown["fen"] == blunder["fen_before"]
    arrows = []
    if teaching:
        try:
            preview = chess.Board(blunder["fen_before"])
            played = preview.parse_san(blunder["played_move"])
            best = preview.parse_san(blunder["best_move"])
            arrows = [
                {"from": chess.square_name(played.from_square), "to": chess.square_name(played.to_square), "brush": "red"},
                {"from": chess.square_name(best.from_square), "to": chess.square_name(best.to_square), "brush": "green"},
            ]
        except ValueError:
            arrows = []
    state = board_state(chess.Board(shown["fen"]))
    with board_column:
        chess_board(
            fen=shown["fen"], orientation=game["user_color"], turn=state["turn"], check=state["check"],
            last_move=shown["last"], arrows=arrows, loss=blunder["eval_drop"] if teaching and not replaying else None,
            reserve_loss_bar=True,
            key=f"review-board-{record['signature'][:12]}",
        )
        previous, following = st.columns(2, gap="small", wrap=False)
        previous.button(
            "Previous position", key="review_previous", disabled=navigation_index == 0, width="stretch",
            icon=":material/chevron_left:",
            on_click=_step_review, args=(navigation_key, -1, navigation_last),
        )
        following.button(
            "Next position", key="review_next", disabled=navigation_index == navigation_last, width="stretch",
            icon=":material/chevron_right:", icon_position="right",
            on_click=_step_review, args=(navigation_key, 1, navigation_last),
        )
        st.caption(f"{game['user_color'].title()} at the bottom · {shown['label']}")
        if move_description:
            st.caption(move_description)
    with coach_column:
        with st.container(border=True):
            st.markdown(f"#### Mistake {number} of {len(blunders)}")
            played, best = st.columns(2)
            played.metric("You played", blunder["played_move"])
            best.metric("Suggested move" if record["is_mock"] else "Best move", blunder["best_move"])
            st.caption(f"Lost {blunder['eval_drop']:.2f} pawns")
            if not teaching:
                st.info(f"Exploring {shown['label']}. Feedback below explains mistake {number}.")
                st.button(
                    "Back to this mistake", key="review_return", icon=":material/my_location:",
                    on_click=_focus_mistake, args=(ply_key, mistake_plies),
                )
            if details.get("error"):
                st.warning(f"The continuation could not be analyzed: {details['error']}")
                st.button("Retry continuation", on_click=_retry_continuation, args=(game["game_url"], _continuation_key(blunder)))
            _coaching(game, record, number - 1, config, provider, anthropic_model, analysis=analysis)
        with st.expander("Full game move list"):
            moves = []
            for item in positions:
                if item["ply"] == 0:
                    continue
                mark = ""
                matched = next((index for index, ply_index in enumerate(mistake_plies) if ply_index == item["ply"] - 1), None)
                if matched is not None:
                    mark = _mistake_mark(blunders[matched]["eval_drop"])
                text = f"{item['label']}{mark}"
                if item["ply"] == ply + (1 if teaching else 0):
                    text = f"**{text}**"
                moves.append(text)
            st.markdown(" · ".join(moves))


def _improvement_plan() -> None:
    st.subheader("A small plan. A stronger next game.")
    records = [record for record in st.session_state.analyses.values() if not record.get("error")]
    st.caption(f"Based on {len(records)} game{'s' if len(records) != 1 else ''} analyzed in this session. Each game counts once.")
    if st.button("Generate My Weekly Improvement Plan", type="primary", disabled=not records, icon=":material/event_note:"):
        st.session_state.weekly_plan = ChessCoach.generate_weekly_plan(records)
    if not records:
        st.info("Review a game first, then come back for three focused practice exercises.")
        return
    if any(record["is_mock"] for record in records):
        st.warning("This session includes mock analysis. Use Stockfish for a reliable practice plan.")
    plan = st.session_state.weekly_plan
    if plan is None:
        st.write("Build a weekly routine around the patterns in your games. No AI key is needed.")
        return
    game_count, blunder_count = plan["games_analyzed"], plan["total_blunders"]
    st.markdown(f"**{game_count} game{'s' if game_count != 1 else ''} · {blunder_count} blunder{'s' if blunder_count != 1 else ''} · 3 practice focuses**")
    for item in plan["practice_plan"]:
        with st.container(border=True):
            st.markdown(f"#### {item['title']}")
            st.caption(item["reason"])
            st.write(item["practice"])
            st.markdown(f"**Before you move:** {item['mental_check']}")


def main() -> None:
    st.set_page_config(page_title="ChessBot · Your chess coach", page_icon=":material/chess_pawn:", layout="wide")
    study_room_styles()
    config = load_config()
    _initialize_session(config)
    status, allow_mock, provider, anthropic_model = _sidebar(config)
    with st.container(key="study_header"):
        st.caption("THE STUDY ROOM / CHESSBOT")
        st.title("ChessBot")
    if config.review_only:
        rating = st.session_state.user_rating
        level = "beginner explanations" if rating < 1000 else "your current level"
        st.write("A clearer plan for your next move.")
        source = st.session_state.get("rating_source")
        rating_label = (("saved " if source["stale"] else "") + source["category"]) if source else "manual coaching level"
        st.badge(f"{rating} {rating_label} · {level}", icon=":material/school:", color="green")
        with st.container(key="primary_navigation"):
            section = st.radio(
                "Open", ["Your games", "The Soviet Chess Primer", "Silman's endgame course"], horizontal=True,
                format_func=lambda value: {
                    "Your games": "Your games",
                    "The Soviet Chess Primer": "Learn chess",
                    "Silman's endgame course": "Endgames",
                }[value],
                key="main_section", label_visibility="collapsed",
            )
        if section == "The Soviet Chess Primer":
            render_primer(config)
            return
        if section == "Silman's endgame course":
            render_silman(config)
            return
        _game_review(config, status, allow_mock, provider, anthropic_model)
        return
    st.write("Understand the move. Learn the principle. Play with a plan.")
    review_tab, plan_tab, primer_tab, silman_tab = st.tabs(
        ["Game review", "Improvement plan", "The Soviet Chess Primer", "Silman's endgame course"]
    )
    with review_tab:
        _game_review(config, status, allow_mock, provider, anthropic_model)
    with plan_tab:
        _improvement_plan()
    with primer_tab:
        render_primer(config)
    with silman_tab:
        render_silman(config)


if __name__ == "__main__":
    main()
