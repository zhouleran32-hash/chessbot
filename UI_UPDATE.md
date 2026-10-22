# ChessBot study-room interface — 19 October 2026

The interface uses a dark chess-club palette with charcoal-green surfaces,
ivory text, sage chess squares, native sans-serif body text and serif headings.
Fonts no longer depend on Google Fonts loading.

## Changes

- Main-screen game loading, including retryable errors and a direct Primer shortcut.
- Clearly selected, keyboard-accessible navigation between games and lessons.
- A wide study workspace, responsive square boards and compact replay controls.
- Coaching directly beside the game board; the full move list is optional.
- An explicit return to the selected mistake while exploring other positions.
- Short lesson labels, compact chapter navigation, and current-lesson practice progress.
- Desktop practice panels beside the board, stacking naturally on phones.
- Quieter engine diagnostics with the existing configuration and retry controls.

The update preserves the course content, identifiers, grading, player progress,
existing Chessground board, Stockfish analysis, and coaching caches. It adds no
runtime dependencies. Local settings, uploaded books and progress databases are
not part of the source update.

## GitHub references

- [Streamlit documentation](https://github.com/streamlit/docs), especially
  [theming](https://github.com/streamlit/docs/blob/main/content/develop/concepts/configuration/theming.md):
  native theme configuration and responsive layout patterns.
- [cm-chessboard](https://github.com/shaack/cm-chessboard), especially its
  [accessibility extension](https://github.com/shaack/cm-chessboard/blob/master/src/extensions/accessibility/Accessibility.js):
  explicit move controls and alternatives to dragging. Existing SAN answer buttons
  remain available; this update does not introduce its board or copy its sprites.
- [Lucide](https://github.com/lucide-icons/lucide): a reference for restrained,
  consistent action iconography. Native Streamlit Material icons are retained;
  no Lucide assets were copied.

These projects informed the UI choices. No third-party source or assets were
copied into the update.
