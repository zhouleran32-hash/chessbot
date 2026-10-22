---
name: teach-chess-book
description: >-
  Turn a chess book the user supplies into ChessBot lessons and study guides,
  using the same shape as The Soviet Chess Primer. Use when the user provides
  a new chess book, PDF, EPUB, or chapter and asks the bot to teach it,
  extract exercises, or build a course from it.
---

# Teach a chess book in ChessBot

The Primer is the template. A new book gets its own course, written in original words, with every position checked by python-chess. Do not append it to the Primer syllabus.

Read [chess-pedagogy](../chess-pedagogy/SKILL.md) before authoring a lesson. Use [onboard-book](../onboard-book/SKILL.md) for a puzzle book and [docling](../docling/SKILL.md) when a textbook's layout needs a real document conversion.

## How the Primer teaches

Two layers, both tied to the book's order of ideas:

1. **Playable lesson** in `core/primer_chapterN.py`, built with `lesson()`, `step()`, `after()`, and `custom()` from `core/primer_build.py`. One skill per lesson: a short explanation, one or two board steps, a prompt, and three choices `(san, correct, explanation)`. The quiz position is the last step. Set `objective` (`checkmate`, `mate_in_2`, `mate_threat`) when the move should be graded by the result, not only by the listed choice.
2. **Study guide** in `core/primer_guides_chapterN.py`, keyed by the same lesson id. Each guide has a printed-page span, goals, sections, worked examples, pitfalls, conceptual checks, and a recap. A worked example is `example(title, fen, moves, notes)` with one note for the starting position and one note after every move. `core.primer_study.example_frames` rejects an illegal move and notation that is not the canonical SAN.

`core/primer_study.py` records chapter titles and printed page spans. The Primer comment says this scan's PDF page is the printed page plus one. Measure that offset on the new file; do not reuse it.

The Primer's prose is original. Citations are the book title, chapter, diagram number, and page. Do the same.

## Which tool reads the file

Keep the user's file in `data/books/`. That directory is gitignored.

| Book | Read it with | Then |
|---|---|---|
| Numbered diagrams plus solutions | `chesspdf` via the onboard-book skill. `chesspdf` 0.2.1 is installed (`uv tool install chesspdf`). | Accept a position only when the printed solution replays. Teach a chosen subset, not an unlabeled dump of every puzzle. |
| Chapters that explain an idea, then show a position | Text layer first. Use the docling skill when columns, scans, or tables defeat a plain text read. | Map chapters to skills in the book's order. Author the lesson from the idea. |
| The file is not in the workspace yet | Stop. | Ask for the file. Do not invent positions from memory of a book you have not opened. |

`chesspdf probe probe <file.pdf>` says whether the PDF is born-digital and whether a diagram font is present. Born-digital diagram fonts need no vision API. Scanned books need `GEMINI_API_KEY`; if it is missing, stop and ask. The onboard-book skill was written against a slightly different CLI surface: if a flag is rejected, run `chesspdf <cmd> --help` and follow the installed command.

The Docling skill is vendored. The `docling` package is not installed, because it pulls a large model stack. Install it only when this book needs it: `uv tool install docling`.

## Build the course

Mirror the Primer's file split under a new name. Do not reuse Primer lesson ids or edit `core/primer_course.py`.

- `core/<book>_chapterN.py` for lessons
- `core/<book>_guides_chapterN.py` for guides
- `core/<book>_course.py` to concatenate chapters in book order
- `tests/test_<book>.py` that loads every lesson, checks each FEN with `chess.Board.is_valid()`, and runs every worked example through `example_frames`

Build positions with `after(moves)` or `custom(pieces)`. Do not hand-write a FEN. Verify a quiz move with:

```bash
work/verify-env/bin/python .agents/skills/chess-pedagogy/scripts/verify_lesson.py \
  --fen "<quiz fen>" --move "<san>" --check-defenses
```

For a mate problem, the key must mate against every legal reply. Say so when a line is only an illustration.

Each conceptual check needs one correct option, one tempting mistake, and one passive or superficial option, with feedback that names the concrete result of that choice.

## Copyright

Write the teaching text. A citation may name the book, chapter, diagram number, page, and the move sequence needed to identify the exercise. Do not copy paragraphs, solution essays, or a reconstructed chapter into the repo, the chat, or a generated skill.
