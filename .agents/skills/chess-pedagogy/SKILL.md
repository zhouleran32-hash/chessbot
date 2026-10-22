---
name: chess-pedagogy
description: >-
  Design, author, and verify chess instructional content, lessons, conceptual checks,
  and curriculum based on classical chess pedagogy and The Soviet Chess Primer.
  Use when creating or modifying chess lessons, board exercises, multiple-choice
  checks, tactical puzzles, hints, or learning progression.
---

# Chess Pedagogy & Curriculum Design

Guidelines and workflows for designing high-impact chess teaching lessons, interactive board exercises, and conceptual diagnostic checks inspired by classical Russian/Soviet chess instruction (Ilya Maizelis' *The Soviet Chess Primer*, Mark Dvoretsky, Artur Yusupov).

---

## 1. Pedagogical Principles

1. **Understand First, Calculate Second**:
   - Beginners (<800) don't lose because of complex 5-ply tactical calculations; they lose because they do not notice undefended pieces or immediate checks.
   - Teach the *function* of pieces (guarding squares, pinning attackers, controlling open files), not abstract rules.
2. **The "Why" Behind Mistakes**:
   - Never just say "Move A is wrong, Move B is correct."
   - Explain the concrete punishment: "If 1...Ne4, White responds with 2.Qxd5! forking the knight and the undefended rook on a8."
3. **Rating-Calibrated Scope**:
   - **Beginner (Rating 400–800)**: Single-move threats, hanging pieces, counting attackers vs defenders, basic checkmates (ladder mate, back rank, scholar's mate defense), castling safely.
   - **Novice (Rating 800–1200)**: 2-move tactics (forks, pins, skewers, removal of guard), simple pawn endgames, opening principles (center control, piece development).
   - **Intermediate (Rating 1200–1600)**: Multi-step combinations, discovered checks, decoy/deflection, weak square complexes, rook endgames.

---

## 2. Anatomy of a Primer Lesson

Every lesson must follow a consistent, pedagogically complete structure:

```text
Lesson
├── 1. Title & Learning Goals: Clear statement of the concept to master
├── 2. Source Attribution: Book, chapter, diagram number, printed & PDF page
├── 3. Conceptual Explanation: The idea, key piece relationships, typical traps
├── 4. Annotated Replay: Step-by-step master or illustrative line with commentary
├── 5. Board Exercise: Concrete playable position with clear objective
├── 6. Conceptual Checks: Diagnostic multiple-choice questions with answer-specific feedback
└── 7. Recap: 1-2 sentence takeaway rule
```

### Conceptual Checks: Diagnostic Distractors
A good conceptual check does not have obvious "joke" options. Every distractor should reflect a real, common mental trap:
- **Option A (Correct)**: Identifies the key tactical or positional mechanism.
- **Option B (Tempting Tactical Mistake)**: Looks aggressive but falls into a counter-tactic (e.g., hanging a piece).
- **Option C (Passive / Superficial)**: Protects a phantom threat while neglecting active development or defense.
- **Feedback for Each Choice**: Specifically explain *why* that choice succeeds or fails.

---

## 3. Move Validation & Verification Rules

1. **Strict Legal Move Verification**:
   - Always verify board positions using `python-chess`.
   - Never write move sequences by hand without verifying them against an actual `chess.Board()`.
   - Check that all moves are legal in the given FEN.
2. **Exhaustive Defense in Tactics**:
   - In mate-in-two (or single-move tactical problems), verify that the winning key works against **all** legal replies by the opponent.
   - If Black has 5 legal moves in reply to the key move, the solution must account for all 5 branches.
3. **Pawn Promotions**:
   - Never omit promotion pieces. Use canonical notation: `e7e8q` (UCI) or `e8=Q` (SAN).
4. **Distinguish Demonstrated Lines vs Forced Wins**:
   - In endgame studies or deep combinations, clarify when a line is an *illustrative principal variation* versus when every alternative move is strictly refuted.

---

## 4. Helper Script: Lesson Verifier

Use the project's bundled script to verify any position, move, or defense branch:

```bash
work/verify-env/bin/python .agents/skills/chess-pedagogy/scripts/verify_lesson.py \
  --fen "r1bqkb1r/pppp1ppp/2n5/4p3/2B1n3/5N2/PPPP1PPP/RNBQK2R w KQkq - 0 5" \
  --move "d1e2"
```

---

## 5. Additional References

- See [reference.md](reference.md) for Soviet Chess Primer chapter themes, composition types, and common pedagogical pitfalls.
- See [teach-chess-book](../teach-chess-book/SKILL.md) when a new book should be taught in this same shape.
