# Soviet Chess Primer Reference & Teaching Themes

## 1. Soviet Chess Primer Structure & Topics

| Chapter | Topic / Theme | Core Pedagogical Focus |
|---|---|---|
| Chapter 1 | The Game and the Board | Coordinates, piece movement, rules, check, checkmate, stalemate |
| Chapter 2 | Comparative Value & Trades | Absolute vs relative piece values, material counting, exchanges |
| Chapter 3 | Elementary Checkmates | King + Queen vs King, King + Rook vs King, two Bishops vs King |
| Chapter 4 | Basic Tactical Elements | Fork, pin, skewer, discovered check, double check, deflection |
| Chapter 5 | Attacking the Castled King | Pawn storms, sacrificial breaks on h7/f7, clearance tactics |
| Chapter 6 | Combination Play | Motifs, themes, geometry, relative piece activity |
| Chapter 7 | Pawn Play & Endgames | Passed pawns, square of the pawn, opposition, triangulation |
| Chapter 8 | Strategic Elements | Open files, outposts, pawn weaknesses (isolated, doubled, backward) |
| Chapter 9 | Opening Principles | Center control, rapid piece development, king safety |
| Chapter 10 | Practical Mastery | Calculating variations, candidate moves, prophylactic thinking |
| Appendix | 98 Compositions & Studies | 2-movers, 3-movers, longer problems, winning & drawing studies |

---

## 2. Common Pedagogical Traps in AI Chess Instruction

1. **Hallucinating Coordinates**:
   - Generative models frequently say "Bishop on e4 attacks the pawn on b7" when the diagonal is actually blocked or on a different color.
   - *Prevention*: Always verify geometry using `python-chess` board representation before outputting coordinate claims.

2. **Assuming One Move is Forced When Alternatives Exist**:
   - Stating "Black must play 1...Kh8" when 1...Kf8 is also legal (even if slightly worse).
   - *Prevention*: Always check `board.legal_moves`. State: "Black can try 1...Kh8 or 1...Kf8; in either case, White continues with..."

3. **Incomplete Mate-in-Two Defenses**:
   - In problem composition, a true mate-in-two must guarantee checkmate on move 2 against *every* legal defensive reply.
   - If White plays 1.Qf3, checkmate must occur whether Black plays 1...g6, 1...Kh7, 1...f5, etc.

4. **Over-complicating Advice for Low-Rating Players**:
   - Telling a 560-rated player about "imbalanced pawn majorities on the queenside" when they lost a full queen on move 8.
   - *Prevention*: Follow the hierarchy of blunder analysis: (1) Hanging pieces -> (2) King safety -> (3) Simple tactics -> (4) Strategy.
