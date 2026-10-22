---
name: chess-game-review
description: >-
  Analyze, explain, and review played chess games from Chess.com, PGN, or manual moves.
  Use when diagnosing blunders, translating engine evaluations into actionable coaching feedback,
  identifying recurrent mistake patterns, formulating player mental checks, or designing
  personalized practice plans.
---

# Chess Game Review & Blunder Diagnosis

Expert workflows for reviewing chess games, interpreting Stockfish engine output, and delivering empathetic, rating-calibrated coaching feedback to improve a player's chess thinking.

---

## 1. Core Review Philosophy

1. **Empathy & Encouragement**:
   - Chess can be frustrating when losing pieces. Keep feedback constructive and forward-looking.
   - Celebrate good moves or solid opening development before diving into mistakes.
2. **Translate Centipawns to Plain English**:
   - Do NOT just report: *"Evaluation dropped from +0.4 to -3.8 with 12.Nxd5."*
   - Translate to board reality: *"With 12.Nxd5?, the knight moves away from protecting the e4 pawn, allowing Black's queen to capture it with check (12...Qxe4+)."*
3. **Calibrate to Player Rating**:
   - **For Rating <800 (e.g., beginner / ~564)**: Focus 90% on board awareness—hanging pieces, undefended squares, and immediate checks. Avoid lines deeper than 2 plies.
   - **For Rating 800–1200**: Focus on 2-move tactics, king safety, castling timing, and opening principles.
   - **For Rating 1200+**: Introduce positional weaknesses, pawn structure, rook activity, and piece trades.

---

## 2. Mistake Classification Taxonomy

When reviewing an evaluation drop (typically $\ge 200$ centipawns or turning an advantage into a loss), categorize the error into one of five primary categories:

| Category | Typical Rating Impact | Concrete Symptoms |
|---|---|---|
| `hanging_piece` | Primary cause of losses <1000 | Moving a piece to an attacked square without defender; moving a defender away from another piece; missing a free opponent piece. |
| `king_safety` | High frequency <1200 | Delaying castling past move 10; opening the f-pawn (f3/f6) prematurely; ignoring an opponent queen/bishop battery aimed at h7/g7/f7. |
| `opening_principle_violation` | Common in beginners | Developing Queen on move 2–4; moving the same piece 3 times in the opening; neglecting central pawns (e4/d4/c4). |
| `tactical_oversight` | Universal across all levels | Falling for basic forks (Knight on c7/e7/f7), pins (Rook against King/Queen), or skewers; missing an opponent's mate-in-1 threat. |
| `endgame_technique` | Critical 1000+ | Leaving the king passive in King+Pawn endings; failing to push passed pawns; rushing trades into lost pawn endgames. |

---

## 3. The "Mental Check" Framework

Every reviewed mistake must conclude with a **Mental Check**: a memorable, single-sentence question the player can silently ask before finalizing their next move.

- **For Undefended Pieces**:
  > *"Before I let go of this piece: is my target square defended, and did I leave anything undefended behind me?"*
- **For King Safety**:
  > *"Can my opponent check my king or threaten checkmate on their very next turn?"*
- **For Premature Attacks**:
  > *"Have I developed my minor pieces and castled before launching this attack?"*
- **For Tactical Awareness**:
  > *"What did my opponent's last move just attack?"*

---

## 4. Diagnosing with python-chess

When diagnosing a mistake in code or scripts, check the board state mechanically:
1. **Was a piece captured for free?**
   - Check `board.is_attacked_by()` on the target square.
   - Check if attackers outnumber defenders.
2. **Is there an immediate checkmate?**
   - Does opponent have a legal move where `board.is_checkmate()` is True?
3. **Did the move open a line against the King?**
   - Check ray attacks from opponent queens, rooks, bishops to the king square.

Use the bundled diagnostic helper:
```bash
work/verify-env/bin/python .agents/skills/chess-game-review/scripts/diagnose_blunder.py \
  --fen "r1bqkb1r/pppp1ppp/2n5/4p3/2B1n3/5N2/PPPP1PPP/RNBQK2R w KQkq - 0 5" \
  --played "d2d3" \
  --best "c4f7"
```

---

## 5. Weekly Practice Plan Generation

Aggregate error frequencies across the last 10 games to build a prioritized training schedule:
1. **Identify Top Leak**: Pick the category that caused the most cumulative evaluation loss or game losses.
2. **Design Daily Routine (15–20 minutes/day)**:
   - 5 min: 5–10 untimed tactical puzzles targeting the specific leak (e.g., hanging pieces).
   - 10 min: 1 slow game (15+10 or 30+0) practicing *only* the single Mental Check rule.
3. **Milestone Metric**: E.g., reduce hanging pieces from 2.4 per game to under 1.0 per game over the next 10 games.
