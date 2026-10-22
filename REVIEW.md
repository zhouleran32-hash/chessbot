# ChessBot continuation — 19 October 2026

The interrupted work was the appendix integration and final content review.
The recovered source already contained all 367 lessons, 735 conceptual checks,
the complete 98-composition appendix, and the lesson-resume fix. This update
retains that work and corrects the remaining concrete errors found in this pass.

## Corrections in this update

- **Three-mover 7:** Ng4+ uncovers the queen on b2 along the second rank.
  The knight on g4 does not attack the black king on g2. Corrected the lesson
  title, explanation, and all four replay branches to identify the queen.
- **Longer problem 11:** Rg6 temporarily blocks the h7 bishop's diagonal.
  Both Rd6+ and the alternative Rg4+ uncover that bishop's check on b1;
  neither is a direct rook check. The main line's Rd3 blocks the diagonal
  again before the final rook capture. Corrected both finishing explanations.
- **Winning study 2:** the final Rxh2 pins the c2 rook to its king on a2.
  Thus ...Rxc7 is illegal, while ...Rxh2 allows c8=Q. Added this concrete
  reason to the explanation, final annotation, feedback and recap. Also
  distinguished the illustrated king retreats from the full set of legal replies.

No lesson IDs, concept-check IDs, starting positions or replay moves were
changed. No player settings, credentials, books or progress databases are
included in or modified by this update.

## Fresh verification

- The unmodified recovered copy passed **236 tests**.
- The revised copy passed **236 tests** in 9.977 seconds using the existing
  Python environment and `python -m unittest discover -s tests -v`.
- The full course audit checked **367 lessons, 536 examples, 3,489 replay
  plies and 735 conceptual checks**. Starting boards, canonical move notation,
  replay continuity, terminal positions, answer grading and source-page ranges
  pass their existing validators. The original 261-lesson ID/order/check
  contract is preserved, as are all appendix IDs and checks.
- The suite includes all-defence mate-in-two and three-move composition checks,
  study endpoints, game review, per-player persistence, all six appendix
  collections, and returning from Your games to the saved lesson.
- Seven additional direct board checks confirm the actual checking piece in
  all four three-mover branches and both long-problem finishes, plus the final
  rook pin and legal promotion in Lasker's study.
- A targeted annotation audit reviewed discovered-check frames, forcing-move
  claims and piece-location flags throughout chapters 4–10 and the appendix.
  Previously repaired chapter 5 mating threats, chapter 6 interference and
  chapter 8 rook/knight restrictions are retained.

## Scope and limits

This is a finalization and targeted correctness pass, not a claim of a new
line-by-line manual rereading of all 130,449 teaching words. The recovered
chapter 1–3 review and earlier author reports remain in the original project's
work folder. The expected separate final chapter 4–7 and 8–10 review reports
were absent when this continuation began; this report records what was freshly
verified rather than inventing those missing reports.

Legal replays and finite engine analysis do not establish every strategic
judgment, a unique key, or a complete win/draw proof. The existing qualification
for the 17-move problem, alternative study keys and illustrative defensive
branches remains in place. AppTest exercised the UI without paid API calls;
this session could not run a local HTTP server for a fresh visual browser check.

## Applying the update

The original project was read-only in this session. The accompanying installer
updates only files listed in its manifest, checks for intervening edits, and
backs up previous versions before applying changes. It leaves `.env` and
`data/` untouched. Restart the original Streamlit process afterward to load
the revised lesson modules.

## Follow-up: practice and replay navigation

After confirming the first update was installed, a second pass reproduced and
fixed two interaction bugs:

- A pending pawn-promotion menu survived selecting a different piece. Each new
  square selection now clears the old promotion before processing the click.
  A promotion destination still presents all four choices; nothing moves or
  earns progress until a choice is made.
- Streamlit discarded the selected worked variation when the lesson was
  hidden. A separate session-state map now retains the variation alongside its
  move cursor when visiting another lesson or Your games. Changing players
  resets that map and all replay cursors. This is session state, not an added
  database field or a promise of replay persistence across app restarts.

The chapter 6 relative-strength task already accepted both Qg7# and Qxf8#.
Its prompt now invites either mate, and a Qxf8# answer button explains the
alternative. The h6-supported Qg7# worked example remains the teaching focus.
All lesson IDs, check IDs, initial positions and worked replay moves remain
unchanged.

Fresh checks for this follow-up:

- **239 tests pass** in 10.866 seconds. The two interaction regressions failed
  before their fixes and pass afterward. A third new test verifies black
  knight underpromotion, delayed board grading, and saved completion.
- The complete course audit passes again: **367 lessons, 536 examples, 3,489
  replay plies and 735 conceptual checks**. Both chapter 6 mating answers are
  legal, actually checkmate, and accepted by the objective-based grader.
- The six automated wording flags were inspected: five explicitly disclaim
  an only-move claim; the sixth describes the reply after the shown move,
  whereas the audit flag counts moves before it.

The earlier scope limits still apply. This follow-up tests interaction and
board claims; it does not claim a fresh manual rereading of every lesson.
