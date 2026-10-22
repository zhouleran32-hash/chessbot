"""Load ChessBot settings from the environment and the project's .env file."""

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"


@dataclass(frozen=True)
class Settings:
    """Application settings with local storage defaults and optional credentials."""

    openai_api_key: str = field(default="", repr=False)
    stockfish_path: str = "stockfish"
    chess_com_username: str = ""
    user_rating: int = 700
    review_only: bool = True
    sqlite_path: Path = DATA_DIR / "cache" / "games.sqlite3"
    books_dir: Path = DATA_DIR / "books"
    chroma_dir: Path = DATA_DIR / "chroma"


def load_config() -> Settings:
    """Read settings, preserving environment values over .env values.

    Missing credentials are allowed so the starter dashboard can launch before
    setup is complete. Stockfish defaults to an executable on the system PATH.
    """
    load_dotenv(dotenv_path=PROJECT_ROOT / ".env", override=False)
    try:
        rating = int(os.getenv("CHESS_COM_RATING", "700"))
    except ValueError:
        rating = 700
    if not 0 <= rating <= 4000:
        rating = 700
    return Settings(
        openai_api_key=os.getenv("OPENAI_API_KEY", ""),
        stockfish_path=os.getenv("STOCKFISH_PATH", "").strip() or "stockfish",
        chess_com_username=os.getenv("CHESS_COM_USERNAME", "").strip(),
        user_rating=rating,
        review_only=os.getenv("CHESSBOT_REVIEW_ONLY", "true").strip().lower() not in {"false", "0", "no"},
    )
