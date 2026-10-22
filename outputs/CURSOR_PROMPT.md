# ChessBot handoff for Cursor

Open and work directly in this existing project folder. Read and edit these
files directly; do not create another project or extract a separate copy from
the ZIP.

We are building ChessBot, a Python Streamlit app that fetches public
Chess.com games and analyzes mistakes with python-chess and Stockfish.
The Chess.com username and rating come from `.env`.
The current priority is detailed teaching from **The Soviet Chess Primer**,
now covering chapters 1–10 and the appendix. Keep game review available beside
the course. Teach why each idea works, show legal connected examples and
opponent replies, explain wrong answers, and check understanding. Chapters
1–10 use representative examples; the appendix covers all 98 numbered
compositions. Do not claim every printed variation has been reproduced.
Book uploads and weekly plans remain available in full mode.

The course has 367 lessons and 735 conceptual checks. The 261 earlier lessons
retain their IDs and saved checks. The appendix adds 106 lessons: 8 foundations,
20 two-movers, 20 three-movers, 15 longer problems, 32 winning studies and 11
drawing studies. It is internal chapter 11 but displayed as **Appendix · Chess
compositions**, with a selection-only Collection menu. Source diagrams and
solution pages are cited separately; PDF page = printed page + 1.

Preserve stable lesson/check IDs and regression tests. Compare legal move
identities when grading. The mate-in-two checker must test every legal defence;
other open-ended tasks also accept valid alternatives. Longer compositions
use explicit demonstrated-method practice tasks. Do not call an unlisted move
losing without establishing that result. Stop replay lines when the game ends.
Distinguish a displayed defensive branch from a forced line, and practice
completion from mastery. Keep the selection-only Chapter/Collection/Lesson/Game
menus and the < and > buttons below the worked-example boards.

The course retains its place when switching to Your games and back: Streamlit
removes hidden widget state, so ordinary session state preserves the last shown
lesson. The selected replay variation and its move cursor also survive lesson
navigation and switching views within the session. `primer_example_choices`
holds selections independently of the temporary `worked_` widget keys.
Changing player clears those choices and loads the other player's saved
progress. Test both behaviors after navigation changes. Selecting another
board square cancels a pending promotion before processing the new selection.

Reports and source maps are under work/primer-expansion/, work/primer-part2/,
and work/primer-appendix/. The source/engine discrepancy for diagram 372 remains
qualified. The long appendix mate and study endpoints distinguish a demonstrated
line from an exhaustive result. Do not turn a finite engine result or one
historical game into an unsupported forced-win or uniqueness claim.

The 19 October continuation is documented in `REVIEW.md`. It corrects the
checker identities in appendix three-mover 7 and longer problem 11, and explains
the final rook pin in winning study 2. The follow-up repairs promotion and replay
navigation and exposes both valid mates in chapter 6's relative-strength task.
The full 239-test suite and course audit
pass: 367 lessons, 536 examples, 3,489 replay plies and 735 conceptual checks.
Preserve these corrections if regenerating modules from older scratch drafts.
The original local scratch generator inputs may predate the final corrections;
the shipped `core/` modules are authoritative for these explanations.

Start by reading `README.md`, `app.py`, and the relevant files under `core/`:

- `config.py`: environment settings, current coaching rating, review-only mode.
- `chess_client.py`: public Chess.com API ingestion without an API key.
- `analyzer.py`: Stockfish evaluation, blunder detection, board SVG arrows.
- `coach.py`: AI reviews and position-based feedback without an AI key.
- `rag_engine.py`: optional PDF/Chroma knowledge base.
- `primer.py`, `primer_chapter*.py`: lesson positions and objective-based grading.
- `primer_guides_chapter*.py`: source-mapped detailed explanations, examples, and questions.
- `primer_appendix*.py`: foundations and all numbered appendix compositions.
- `primer_tactics.py`: cached, exhaustive mate-in-two defensive checks.
- `primer_study.py`, `primer_ui.py`: validated replay and the guided learning interface.
- `primer_progress.py`: persistent per-player practice progress and bookmarks.

Keep the configured current rating as the coaching level, even when an older
game records another rating. Preserve session caching and explicit retries.
Use real Stockfish when available and label any explicitly enabled mock mode.
Do not invent accuracy scores, tactical continuations, or book citations.

Local settings are in `.env`; preserve them and do not expose credentials.
No AI key is required for the existing position-based feedback. The project
currently has a verification environment at `work/verify-env/` and a configured
local Stockfish executable. Dependencies are listed in `requirements.txt`.

From the project root, verify with:

```sh
work/verify-env/bin/python -m unittest discover -s tests
```

Run the suite to check the current count, including curriculum/chess/UI regressions. The dashboard is
currently served at `http://127.0.0.1:8501/`; reuse it if it is still running.
To start it when needed:

```sh
work/verify-env/bin/python -m streamlit run app.py
```

First confirm that this folder is open, inspect the current implementation,
and give me a brief overview of how game fetching, analysis, and feedback work.
Wait for my next requested change before modifying application behavior.
