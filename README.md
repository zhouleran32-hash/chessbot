# ChessBot

The dark study-room interface adds main-screen game loading, responsive boards,
compact lesson navigation, and coaching beside the position. See
[`UI_UPDATE.md`](UI_UPDATE.md) for the interface changes and GitHub references.

A Streamlit chess coaching dashboard combining Chess.com games, python-chess
and Stockfish analysis, and principles retrieved from uploaded chess book PDFs
using ChromaDB.

The 19 October 2026 continuation corrects appendix checking-piece and rook-pin
explanations, clears cancelled promotion choices, and preserves the selected
replay variation when navigating. The chapter 6 relative-strength exercise
now explicitly offers both legal mates. All 239 tests pass. See `REVIEW.md`
for the exact verification scope and limitations.

## Project structure

```text
ChessBot/
├── core/
│   ├── __init__.py
│   ├── config.py       # Environment and local storage settings
│   ├── chess_client.py # Public Chess.com API client
│   ├── analyzer.py     # Stockfish blunder analysis and mock fallback
│   ├── coach.py        # Model feedback and weekly practice plans
│   ├── rag_engine.py   # PDF ingestion, semantic retrieval, and seed advice
│   ├── primer.py      # Lesson model and legal-move grading
│   ├── primer_chapter*.py        # Chapter positions and board exercises
│   ├── primer_guides_chapter*.py # Detailed teaching and annotated examples
│   ├── primer_appendix*.py       # Composition foundations, problems and studies
│   ├── primer_tactics.py         # Complete mate-in-two defensive checking
│   ├── primer_study.py           # Source references and validated replay
│   ├── primer_progress.py        # Saved learning progress
│   └── primer_ui.py              # Guided Streamlit course
├── data/
│   ├── cache/          # Local SQLite cache
│   ├── books/          # Uploaded chess book PDFs
│   └── chroma/         # Persistent ChromaDB vector store
├── app.py
├── tests/
├── requirements.txt
└── .env.example
```

## Setup

From the project folder:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

On Windows, activate the environment with `.venv\Scripts\activate` instead.

Edit `.env` with your OpenAI API key and Chess.com username. Install the Stockfish
executable separately and set `STOCKFISH_PATH` to its full path, or leave it as
`stockfish` if it is available on your system PATH.

Use the dashboard's **Feed a Chess Book** uploader to save and index a text PDF.

```sh
streamlit run app.py
```

## Your game review

The dashboard opens in a focused game-review mode. Your local `.env` controls
the default username (`CHESS_COM_USERNAME`). The app loads the player's latest
published Chess.com rating on opening, checks it every minute while the page is
active, and refreshes it when fetching games or choosing **Refresh rating**.
The main badge and coaching feedback follow that rating, even for older games.

Chess.com keeps separate rapid, blitz, bullet and daily ratings. The sidebar
defaults to the most recently played category and lets you choose another
available category. If a refresh fails, the previous rating remains visible as
the last successful update; another player's rating is never reused. When no
published rating is available, **Manual coaching level** uses `CHESS_COM_RATING`
as a fallback. It is explicitly labeled as manual.

These are the latest values published by the
[Chess.com public API](https://www.chess.com/news/view/published-data-api#pubapi-general-caching).
Chess.com's caching can delay changes compared with the website; checking every
minute does not guarantee an immediate post-game update. Rate-limit retry
deadlines are honored, including when the refresh button is pressed.

Choose **Fetch Games** to load your latest ten completed games and immediately
analyze the newest one. Use **Choose a game** to review another. Step through
**Every move** to inspect all moves you played: an independent quality label,
evaluation before and after, the engine's preferred move, concrete board facts,
and legal lines you can replay. Select a table row or use **Review a move**.
**Board view** switches between the position before/after your move and the
suggested continuations. Your current rating guides the explanations.

Labels include Best, Excellent, Good, Inaccuracy, Mistake, Blunder and Forced.
Brilliant and Great are conservative **candidates**, clearly identified as
independent estimates. These are not imported Chess.com awards; the public API
does not expose move-by-move Game Review labels. Overall accuracy remains only
the value published by Chess.com. See [`MOVE_REVIEW.md`](MOVE_REVIEW.md) for
the classification rules, evidence requirements and sources.

Choose **Stockfish analysis**, then **Run Stockfish review**, for a separate,
more detailed report. It gives Stockfish one second per search, compares up to
three candidates at every move you played, and retains up to twelve half-moves
per line. Compare evaluations and search depths, choose an alternative or your
played move in **Explore a line**, and replay the annotated replies with the
fixed-position navigation controls. This report does not replace the independent
assessments. Results and failures are cached separately; rerunning is explicit.
Stockfish is required, and no AI key is needed.

Choose **Key mistakes** for the faster, original review of moves losing more
than 1.5 pawns, including the existing optional AI/book coaching. Its material
threshold differs from the expected-result thresholds used in Every move.
The selected mistake now explains what the recommendation achieves, the
opponent's analyzed reply, and the follow-up moves. **Board line** switches
between your actual game, the better move's continuation, and the replies after
your move. Use **Line position** or the previous/next buttons to replay each step.

Position-based feedback works without an AI key. It names the pieces and squares
involved in attacks, checks, captures, development, and opened lines. Each
continuation is replayed legally before it is described. The resulting-position
summary reports observed material changes and activity; the sample is not a
promise that every reply is forced or that the game is won. If an AI key is configured, the
existing model-based coach provides richer feedback.

Books and weekly plans are hidden in this mode. Set `CHESSBOT_REVIEW_ONLY=false`
in `.env` and restart Streamlit to restore the full dashboard described below.

## Learning with The Soviet Chess Primer

Choose **The Soviet Chess Primer** beside **Your games**. The guided course
covers **chapters 1–10 and the appendix**, using the supplied 2014 English
edition. All 261 earlier lesson IDs and their saved practice checks are
preserved. Original explanations, annotated games and studies, and questions
develop the book's ideas. Chapters 1–10 use representative examples; the
appendix follows all 98 numbered compositions. Not every printed variation
or complete game is reproduced.

The course now contains **367 lessons** and **735 conceptual checks**, plus a
playable board task in every lesson. Each lesson provides learning goals,
source references, detailed explanations, annotated replays, common mistakes,
answer-specific feedback, and a recap. The lessons work without an AI key or
a running Stockfish engine.

The **Appendix · Chess compositions** entry has six collections:

- **Getting started — 8 lessons:** reading stipulations, keys and tries,
  complete defensive trees, pure and model mates, winning and drawing study
  endpoints, soundness, and a repeatable solving method.
- **Two-move problems — all 20:** quiet keys, sacrifices, interference,
  blocked escape squares, and a complete response map for every legal defence.
- **Three-move problems — all 20:** clearance, the Indian and Bristol themes,
  promotion choices, branching calculation, and coordinated mating nets.
- **Longer problems — all 15:** pawn staircases, waiting moves, zugzwang,
  king journeys, underpromotion, and the book's 17-move composition.
- **Winning studies — all 32:** promotion races, decoys, rook staircases,
  king activity, domination, underpromotion, and converting the endpoint.
- **Drawing studies — all 11:** stalemate, repeated checks, opposition,
  defensive sacrifices, underpromotion replies, and active defence.

The 106 appendix lessons include the original diagrams, a purposeful note for
each replayed move, important alternative defences, and two understanding
questions each. Diagram and solution pages are identified separately. The
warm-up illustrations are explicitly distinguished from numbered compositions.
The two-mover checker evaluates every legal defence and accepts any first
move that really forces mate within two. Longer problems and studies use
clearly stated tasks about the demonstrated method; a different move is not
therefore declared losing. A single illustrated branch is not presented as
an exhaustive proof of every longer composition.

Part Two remains fully available: **36 endgame lessons**, **32 middlegame
lessons**, and **18 opening-theory lessons**. Historical assessments are
distinguished from proven outcomes. The guide retains the source/engine
disagreement in diagram 372; finite engine searches are not exhaustive
endgame proofs.

Use the **Chapter** and **Lesson** menus, and the appendix’s **Collection**
menu, then work through four views:

- **Learn** gives learning goals, fuller explanations, common mistakes, and
  introductory diagrams.
- **Worked examples** lets you replay connected legal moves with a note for
  every position, including the opponent's replies.
- **Practice** combines the clickable board with questions about why the idea
  works. Choose an answer and press **Check my answer** for its explanation.
  Open-ended checkmate and mate-in-two exercises accept valid alternatives,
  not just the answer buttons.
- **Review** gives the key points and shows which practice checks are completed.

Printed-book page references appear beside each lesson. In the supplied PDF,
the PDF page is one greater than the printed page number. Some study-method
material also refers to the advice-to-beginners page before chapter 1.

The course saves successful checks and your last lesson in
`data/cache/primer.sqlite3`, separately for the username submitted in the sidebar.
Changing players restores that player's saved lesson and checks. Switching
to game review and back also keeps your place in the course. During the same
session, each lesson remembers its selected worked variation and replay step;
changing players resets those replay choices. These are
practice-completion records, not a claim that one correct answer proves mastery.
Return to a lesson later and explain its example without the notes. Primer
lessons and their feedback work without an AI key or a running Stockfish engine.
Worked lines include notes for both sides. An illustrative reply is identified
as such; it is not automatically the opponent's only move. Specific movement
tasks may ask for one demonstrated operation even when other moves are playable.
Open-ended checkmate tasks accept every legal mating move.

## Full dashboard

1. Enter your Chess.com username in the sidebar and choose **Fetch Games**.
   The latest ten completed games appear with both players, your result, and
   the date in UTC. Choose a game below the table to start analysis.
2. Watch analysis progress, then review your blunder count and moves reviewed.
   Accuracy is the player's published Chess.com score when the API supplies
   it; a dash means it was unavailable. ChessBot does not invent an accuracy
   percentage from blunder counts.
3. Step through blunders with the slider. The board shows the position before
   your move, with a red arrow for the played move and green for the suggested
   move. The AI review includes the tactical breakdown, a retrieved principle
   with its source/page citation, and a mental check.
4. Open **Improvement plan** and choose **Generate My Weekly Improvement Plan**
   for three practice exercises based on all games analyzed in this session.

The sidebar checks whether the configured Stockfish executable can start. If
it is unavailable, you can use the clearly labeled mock preview or disable
mock mode until you install Stockfish. **Check again** refreshes engine status.
Key mistakes uses 0.1 seconds per position. Every move uses 0.2 seconds before
and after each of your moves, including two candidate lines before the move;
a long game can take tens of seconds. Completed analysis is reused when navigating.
Key mistakes reuses matching full-review evidence when available. Otherwise,
only the selected mistake gets two additional 0.5-second searches. The first
is restricted to the already displayed recommendation, keeping its arrow,
explanation, and replay consistent. These lines are cached; a failed search
keeps the original review usable and offers **Retry continuation**.

Without an AI key, game analysis and weekly plans still work. The review shows
position-based feedback, retrieved principles, and a mental check.
An empty library uses the ten built-in beginner principles. To index PDFs and
search their passages, set `OPENAI_API_KEY`; the selected AI coach can use
OpenAI GPT-4o or Anthropic with `ANTHROPIC_API_KEY` and `ANTHROPIC_MODEL`.

PDFs are indexed automatically on upload, with a spinner. Files are stored in
`data/books/<content-hash>/<original-filename>` and repeated uploads of the same
content are skipped during the session. New indexed books refresh cached
reviews so subsequent coaching uses the updated library. A PDF with no usable
explanatory text displays a message instead of claiming successful indexing.

Analyses, AI reviews, and the practice plan are cached in Streamlit session
state. Changing the selected blunder or revisiting a game reuses prior work.
Failures expose a **Retry** button and are not automatically repeated on every
rerun. Fetching another player's games resets that player's review history.
Reloading into a new session loses game/review history; book files, Chroma, and
Primer study progress remain on disk. SQLite caching of games is reserved for
a later feature.

## Configuration

`core.config.load_config()` reads the project-root `.env` file. Existing
environment variables take precedence. The project can start without credentials;
the default username and API key are empty, and the default engine is `stockfish`.

Storage paths are absolute paths based on the project folder, so they do not
depend on the current working directory:

- SQLite cache: `data/cache/games.sqlite3`
- Book PDFs: `data/books/`
- ChromaDB vector store: `data/chroma/`

The SQLite game cache will be created when caching is implemented. The RAG engine
creates the persistent Chroma store when accessed. Local data and `.env` are
excluded from version control.

## Game ingestion

The Chess.com client uses the [public Published-Data API](https://www.chess.com/news/view/published-data-api)
and does not require an API key:

```python
from core.chess_client import ChessDotComClient, ChessDotComError

client = ChessDotComClient()
try:
    games = client.get_recent_games("magnuscarlsen", count=3)
    # Or: client.get_monthly_games("magnuscarlsen", year=2026, month=10)
except ChessDotComError as error:
    print(error)
```

Games are returned newest first. Each dictionary contains `game_url`, `played_at`,
`white_username`, `white_rating`, `black_username`, `black_rating`, `user_color`,
`result`, and the unmodified `pgn`. An optional `accuracy` field preserves a
valid 0–100 score for the requested player when Chess.com supplies it.
`played_at` is an ISO 8601 UTC string based on
the game's end time. `user_color` is `white` or `black`, and `result` is `win`,
`loss`, or `draw` from the requested player's perspective. Missing ratings are
`None`. Records without a completed result, end time, or usable PGN are skipped.

Recent-game lookup starts at the current UTC month, then visits older available
archives. It stops when enough games are found or the player's history is
exhausted, in which case it returns the available games. A count of zero returns
an empty list; negative or non-integer counts raise `ValueError`.

Requests use the configured User-Agent and a 15-second timeout by default.
`UserNotFoundError`, `RateLimitError`, and `ChessDotComTimeoutError` all inherit
from `ChessDotComError`. Rate limits expose the server's `Retry-After` header as
`error.retry_after`; requests are not retried automatically. Request failures
raise an error rather than silently returning partial history.

Run the three-game CLI example or the offline tests from the project folder:

```sh
python core/chess_client.py
python -m unittest discover -s tests -v
```

## Blunder analysis

Download the [Stockfish executable](https://stockfishchess.org/download/) for your
platform, then set `STOCKFISH_PATH` or pass its path directly. The analyzer uses
[python-chess engine analysis](https://python-chess.readthedocs.io/en/latest/engine.html)
and renders positions with [chess.svg](https://python-chess.readthedocs.io/en/latest/svg.html).

```python
from core.analyzer import GameAnalyzer
from core.config import load_config

config = load_config()
pgn = "1. e4 e5 2. Qh5 Nc6 3. Qxe5+ Nxe5 *"
with GameAnalyzer(config.stockfish_path, time_limit=0.1) as analyzer:
    blunders = analyzer.analyze_game(pgn, player_color="white", eval_threshold=150)
```

The analyzer replays the main line and evaluates positions before and after each
move by the requested player. Both scores use that player's perspective. Only
drops **greater than** the threshold are returned. The default time limit is
0.1 seconds per analyzed position, with two positions per player move. Pass
`depth=12, time_limit=None` for depth-only analysis, or set both limits to stop
when either is reached.

For a UI progress indicator, pass `progress_callback=callback` to
`analyze_game`. The callback receives `(completed_plies, total_plies)`, starting
at zero and advancing after every replayed move, including the opponent's.

Each blunder contains:

- `move_number`: the full move number from the PGN, including custom starting positions.
- `fen_before`: the position before the player's move.
- `played_move` and `best_move`: SAN notation calculated in that position.
- `eval_drop`: the loss in pawns, such as `2.3` for 230 centipawns.
- `board_svg`: a 400-pixel SVG oriented toward the player, with the played move
  in red and the engine recommendation in green.

Mate scores are converted using a conventional 100,000-centipawn bound, so
blunders involving forced mate can have large `eval_drop` values. Checkmate and
automatic draw positions are scored directly. Empty, malformed, or illegal PGNs
raise `InvalidPGNError`; engine failures raise `GameAnalysisError`.

By default, a missing or unusable executable raises `EngineUnavailableError`
with download and `STOCKFISH_PATH` guidance. For development before Stockfish is
installed, pass `allow_mock=True`. If the engine is unavailable, initialization
emits a warning and enables a deterministic two-ply material search. Use
`analyzer.is_mock` to label these results as mock analysis in the UI;
`analyzer.mock_reason` provides the engine setup error. Engine failures during
analysis raise an error to keep a game from mixing real and mock scores.

The context manager closes the engine process even when analysis raises an
error. If you keep an analyzer outside a `with` block, call `analyzer.close()`
when finished. Use an analyzer instance for one caller at a time.

## Chess book knowledge base

```python
from core.rag_engine import ChessBookKnowledgeBase

knowledge_base = ChessBookKnowledgeBase()

# Before any book is ingested, this returns built-in beginner principles.
advice = knowledge_base.search_advice("hanging undefended pieces", n_results=3)

# Set OPENAI_API_KEY in .env before embedding and searching book passages.
chunks_processed = knowledge_base.ingest_pdf("data/books/my_chess_book.pdf")
advice = knowledge_base.search_advice("early queen development loses time", n_results=3)
```

The knowledge base loads PDF pages with `PyPDFLoader`, splits them with
`RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=80)`, and removes
notation-only lines. In lines dominated by moves, it trims the move sequence and
keeps the explanatory text. Explanatory sentences that contain moves are retained.
This is a text heuristic; scanned books need
OCR before ingestion. Blank or notation-only PDFs return zero eligible chunks.

The default vector store is `data/chroma/` under the project folder, independent
of the current working directory. Pass `persist_directory` to use another
location. Chunks include the source filename, original path, one-based PDF page
number, and a content hash. Identical PDF imports reuse stable IDs through
upserts, avoiding duplicate chunks. `ingest_pdf` returns the number of eligible
chunks processed, including chunks refreshed by an identical import.

Book search uses [OpenAI text-embedding-3-small](https://developers.openai.com/api/docs/models/text-embedding-3-small)
and [Chroma vector queries](https://docs.trychroma.com/docs/querying-collections/query-and-get).
Book chunks and query text are sent to the configured embedding provider;
extracted passages, metadata, and vectors are stored locally. Set `OPENAI_API_KEY`
in `.env`, pass `openai_api_key` explicitly, or inject a LangChain `Embeddings`
provider through the constructor. A custom provider must also supply a stable
`embedding_id`, such as `local-provider:model-name:dimensions:v1`; change this ID
whenever its model, dimensions, or vector-affecting configuration changes.
Embeddings are initialized only when needed. Keep the same provider, model, and
identity when reopening a collection; use a new collection for different
embeddings.

`search_advice` returns `list[str]`, with a citation appended to each passage:

```text
Do not bring the queen out too early. Develop minor pieces first...

[Source: my_chess_book.pdf | page 12]
```

The default collection is `chess_books`. Passing `collection_name` to `ingest_pdf`
selects that collection for subsequent searches. Pass the same name to the
constructor to reopen a custom collection later. Search returns up to
`n_results` available passages; zero returns an empty list, and invalid queries
or counts raise `ValueError`.

When the active collection has no book passages, ten beginner principles are
ranked by query keywords in memory. They cover center control, development,
early queen moves, castling, loose pieces, tactical threats, king protection,
opening tempi, rook activity, and simplifying a material advantage. This fallback
works without an API key and is labeled `Built-in beginner principles`, with
`page n/a`; it does not invent book citations or persist seed documents.

Unreadable PDFs raise `PDFIngestionError`. Embedding or storage failures raise
`KnowledgeBaseError`, rather than being presented as an empty library. The
offline test suite exercises real PDF extraction and local Chroma persistence
with controlled embedding vectors, without paid API requests.

## Coaching and weekly practice

Pass a synchronous OpenAI or Anthropic SDK client and a knowledge base to
`ChessCoach`. OpenAI defaults to the requested `gpt-4o` model:

```python
from openai import OpenAI
from core.coach import ChessCoach
from core.config import load_config
from core.rag_engine import ChessBookKnowledgeBase

config = load_config()
knowledge_base = ChessBookKnowledgeBase()

# blunders is the list returned by GameAnalyzer.analyze_game(...).
with OpenAI(api_key=config.openai_api_key, max_retries=2) as client:
    coach = ChessCoach(client, knowledge_base)
    if blunders:
        blunder = blunders[0]
        feedback = coach.review_blunder(
            fen=blunder["fen_before"],
            played_move=blunder["played_move"],
            best_move=blunder["best_move"],
            eval_drop=blunder["eval_drop"],
            user_rating=700,
        )
    weekly_plan = coach.generate_weekly_plan([{"blunders": blunders}])
```

`fen` is the position **before** the move. Both moves must be legal SAN in that
position, and `eval_drop` is the loss in pawns from the analyzer. The review
classifies the position, retrieves three relevant knowledge-base passages, and
asks the model to adapt its explanation to the student's rating (700 by default).
It returns Markdown with exactly these three sections:

- **The Tactical Breakdown**: a plain-English explanation and the better move.
- **The Principle from the Books**: an exact retrieved excerpt with its original
  source/page citation, followed by an explanation connecting it to the position.
- **The Mental Check**: one short question to ask before moving next time.

The application assembles the sections from validated model JSON and inserts
the chosen excerpt itself. OpenAI requests use [Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs).
Anthropic requests use the [Messages API](https://platform.claude.com/docs/en/api/messages/create)
with the same JSON contract. Invalid, empty, or truncated model responses raise
`CoachingError`. Retrieval and provider failures also raise `CoachingError` with
configuration guidance. Each model request has a 30-second timeout by default;
pass `timeout` to the coach to change it. The caller controls SDK retries and
closes the client.

You can inspect a category without constructing a model client with
`ChessCoach.classify_blunder(fen, played_move, best_move)`. The categories are
`hanging_piece`, `opening_principle_violation`, `king_safety`, and
`tactical_oversight`. Heuristics use legal captures and checks, so pinned
attackers are excluded. Immediate mating threats take priority, followed by
unrecapturable captures, early queen development, and king-shelter changes.
These are coaching hints rather than complete tactical proofs. The prompt
requires explanations to stay within the supplied facts and avoid invented
forced continuations.

For Anthropic, set the optional `ANTHROPIC_API_KEY` and `ANTHROPIC_MODEL` values
in `.env`, or configure the client and model in your calling code:

```python
import os
from anthropic import Anthropic

with Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"], max_retries=2) as client:
    coach = ChessCoach(client, knowledge_base, model=os.environ["ANTHROPIC_MODEL"])
```

An Anthropic model must be explicitly selected; GPT-4o is never sent to an
Anthropic client. Book retrieval still uses the knowledge base's chosen
embedding provider, while an empty library uses the key-free seed principles.
Coaching sends the position, moves, rating, and retrieved snippets to the
selected model provider.

`generate_weekly_plan` accepts a list of game dictionaries, each containing a
`blunders` list. Each blunder can carry a category (underscores or spaces are
accepted), or the raw analyzer fields `fen_before`, `played_move`, and `best_move`.
An analyzed game without mistakes uses `{"blunders": []}`. The result contains
`games_analyzed`, `total_blunders`, `category_counts`, and a three-item
`practice_plan`. Each focus includes a title, category, observed blunder count,
practice exercise, mental-check question, and reason for selection.

You can also call `ChessCoach.generate_weekly_plan(analyzed_games)` directly,
without an SDK client or API key. Practice priorities follow category frequency, with a stable tie order of
undefended pieces, opening principles, king safety, and general tactics.
If fewer than three categories appear, remaining focuses are labeled foundation
practice. Weekly aggregation is deterministic and makes no model or RAG calls.

The test suite uses real SDKs with intercepted HTTP responses and Streamlit's
AppTest widget harness. It covers both provider formats, game selection,
session caching, uploads, retry flows, mock labeling, and weekly aggregation
without paid model calls.
