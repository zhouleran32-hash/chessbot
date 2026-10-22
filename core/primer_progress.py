"""Local per-player study progress; a passed exercise is not a mastery claim."""

from contextlib import closing
from pathlib import Path
import sqlite3


class LearningProgress:
    def __init__(self, path: str | Path, player: str):
        self.path = Path(path)
        self.player = player.strip().casefold() or "local-learner"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with closing(sqlite3.connect(self.path, timeout=10)) as connection:
            connection.executescript("""
                CREATE TABLE IF NOT EXISTS primer_checks (
                    player TEXT NOT NULL, lesson TEXT NOT NULL, exercise TEXT NOT NULL,
                    passed INTEGER NOT NULL, attempts INTEGER NOT NULL DEFAULT 1,
                    PRIMARY KEY (player, lesson, exercise)
                );
                CREATE TABLE IF NOT EXISTS primer_bookmarks (
                    player TEXT PRIMARY KEY, lesson TEXT NOT NULL
                );
            """)

    def record(self, lesson: str, exercise: str, correct: bool) -> None:
        with closing(sqlite3.connect(self.path, timeout=10)) as connection:
            with connection:
                connection.execute("""
                    INSERT INTO primer_checks (player, lesson, exercise, passed)
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(player, lesson, exercise) DO UPDATE SET
                    passed = MAX(primer_checks.passed, excluded.passed),
                    attempts = primer_checks.attempts + 1
                """, (self.player, lesson, exercise, int(correct)))

    def passed(self, lesson: str) -> set[str]:
        with closing(sqlite3.connect(self.path, timeout=10)) as connection:
            return {row[0] for row in connection.execute(
                "SELECT exercise FROM primer_checks WHERE player=? AND lesson=? AND passed=1",
                (self.player, lesson),
            )}

    def all_passed(self) -> dict[str, set[str]]:
        result = {}
        with closing(sqlite3.connect(self.path, timeout=10)) as connection:
            for lesson, exercise in connection.execute(
                "SELECT lesson, exercise FROM primer_checks WHERE player=? AND passed=1", (self.player,),
            ):
                result.setdefault(lesson, set()).add(exercise)
        return result

    def bookmark(self, lesson: str) -> None:
        with closing(sqlite3.connect(self.path, timeout=10)) as connection:
            with connection:
                connection.execute("""
                    INSERT INTO primer_bookmarks (player, lesson) VALUES (?, ?)
                    ON CONFLICT(player) DO UPDATE SET lesson=excluded.lesson
                """, (self.player, lesson))

    def last_lesson(self) -> str | None:
        with closing(sqlite3.connect(self.path, timeout=10)) as connection:
            row = connection.execute("SELECT lesson FROM primer_bookmarks WHERE player=?", (self.player,)).fetchone()
        return row[0] if row else None
