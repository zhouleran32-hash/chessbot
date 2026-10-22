"""Part One of Silman's endgame course: original lessons for the beginner band.

Positions follow the book's diagrams. The wording is written for ChessBot.
"""

from core.primer_build import custom, step
from core.silman_study import point_lesson as lesson


GREEN = "#1B7F4E"
RED = "#C0392B"

STAIR = custom({"e4": "K", "f1": "Q", "g6": "R", "c7": "k"})
QUEENS = custom({"g1": "K", "a1": "Q", "b1": "Q", "d5": "k"})
QUEEN_ROOK = custom({"h1": "K", "g1": "Q", "f1": "R", "e5": "k"})
ROOKS = custom({"h1": "K", "g1": "R", "g2": "R", "e3": "k"})
BOX = custom({"h1": "K", "g1": "Q", "d5": "k"})
ROOK_MATE = custom({"e6": "K", "a7": "R", "d8": "k"})
STALEMATE = custom({"c2": "K", "b3": "Q", "a1": "k"})

LESSONS = [
    lesson(1, "end-staircase", "The staircase", """
- Rook on g6 = fence on the 6th rank
- Queen checks on the next rank: Qf7+
- Then the rook climbs: Rg8 mate
- Rc6+ loses the rook. Kxc6
""", [
        step(STAIR, "Rook fences the 6th rank.", (("a6", "g6", GREEN),)),
        step(STAIR, "Queen checks on the 7th: Qf7+.", (("f1", "f7", RED),)),
    ], "Push the king backward. Check with the queen on the next rank, and leave the rook on its fence.", [
        ("Qf7+", True, "The queen checks along the seventh rank. The rook on g6 still fences the sixth, so the king's only replies are Kb8, Kc8, and Kd8. In every one of those positions, Rg8 is mate."),
        ("Rc6+", False, "The rook does give check, but it has stepped next to the king and the queen does not defend c6. Black can play Kxc6 and the rook is gone."),
        ("Ke5", False, "The white king walks toward the enemy and neither major piece moves. The fence is still on g6, but you have not checked on the next rank, so the king is not driven back."),
    ]),
    lesson(1, "end-two-queens", "King and two queens", """
- One queen takes a rank. The other checks on the next rank
- Qb5+ starts it. The queen on a1 stays back
- Qd4+ hangs a queen. Kxd4
""", [
        step(QUEENS, "Queens on a1 and b1. King on d5.", (("a1", "d5", GREEN), ("b1", "d5", RED))),
        step(QUEENS, "Qb5+ takes the 5th rank.", (("b1", "b5", RED),)),
    ], "Start the staircase. Check with the queen from b1, and keep the queen on a1 for the next rank.", [
        ("Qb5+", True, "The queen from b1 checks and will own the fifth rank once the king steps off it. The queen on a1 is ready to check on the sixth rank. That is the staircase, and it leads to mate."),
        ("Qd4+", False, "The queen from a1 lands next to the king and gives check, but nothing defends her. Black plays Kxd4 and one queen has disappeared."),
        ("Kg2", False, "The king steps off g1 while both queens stay on the first rank. The enemy king is not pushed backward, and no rank has been taken away."),
    ]),
    lesson(1, "end-queen-rook", "Queen and rook together", """
- Queen first: Qg5+
- Rook checks only from a square the queen defends
- Rf5+ hangs the rook. Kxf5
""", [
        step(QUEEN_ROOK, "King on e5 can grab a rook that steps too close.", (("e5", "f5", RED),)),
        step(QUEEN_ROOK, "Qg5+ checks, and the queen will defend f4.", (("g1", "g5", GREEN), ("g5", "f4", RED))),
    ], "Check with the queen so that she can defend the rook's next check. Do not lead with the rook.", [
        ("Qg5+", True, "The queen checks along the fifth rank, from g5 through f5 to the king on e5. After the king steps away, Rf4 is check, and the queen on g5 defends the rook on f4."),
        ("Rf5+", False, "The rook checks from the square beside the king. The queen on g1 does not defend f5. Black plays Kxf5 and wins the rook."),
        ("Kh2", False, "Stepping the king to h2 does not take a rank away and does not check. The black king is still free in the center."),
    ]),
    lesson(1, "end-two-rooks", "King and two rooks", """
- Re1+ fences the e-file
- Attacked rook? Move it along the same fence
- Rg3+ does not cut the king off
""", [
        step(ROOKS, "Rooks on g1 and g2. King on e3.", (("g1", "e1", GREEN),)),
        step(ROOKS, "Re1+ fences the e-file.", (("g1", "e1", GREEN),)),
    ], "Cut the king off from the kingside. Check with the rook from g1, along the first rank to the e-file.", [
        ("Re1+", True, "The rook checks along the e-file and the king cannot cross that file. If the king attacks this rook, it will step up the same file, to e7, instead of being captured."),
        ("Rg3+", False, "The rook checks along the third rank, but it does not build a fence the king cannot cross. The king still has squares on both sides, including f4, e4, d4, f2, e2, and d2."),
        ("Kh2", False, "The king steps aside and both rooks stay on the g-file. The black king is not cut off from any new file."),
    ]),
    lesson(1, "end-shrinking-box", "The shrinking box", """
- Queen draws the box: Qe3
- Walls: the e-file, and the 3rd rank
- King walks in after the box exists
- Qd4+ hangs the queen. Kxd4
""", [
        step(BOX, "Queen still on g1. No box yet.", (("g1", "e3", GREEN),)),
        step(BOX, "Qe3: e-file and 3rd rank.", (("e3", "e8", GREEN), ("e3", "a3", RED))),
    ], "Build the box before you move your king. Place the queen on e3.", [
        ("Qe3", True, "The queen's walls run up the e-file and along the third rank. The king on d5 is inside the box. Your king can now walk up from h1 and help the queen shrink it."),
        ("Qd4+", False, "The queen checks from the square beside the king, and nothing defends her. Black plays Kxd4. A queen given away cannot build a box."),
        ("Kg2", False, "The king starts walking while the queen is still on g1. No wall has been drawn, so the black king is not trapped and the king march has no box to shrink."),
    ]),
    lesson(1, "end-king-rook", "King and rook", """
- Rook on a7 keeps the king on the 8th rank
- Bring your king: Kd6
- Ra8+ abandons the fence. Kc7 steps out
""", [
        step(ROOK_MATE, "Rook fences the 7th. King is stuck on the 8th.", (("a7", "h7", GREEN),)),
        step(ROOK_MATE, "Kd6. Not a check. The king takes the flight squares.", (("e6", "d6", RED),)),
    ], "Bring the king to the sixth rank, opposite the enemy king. Leave the rook on the seventh rank.", [
        ("Kd6", True, "The king comes to d6 and threatens mate without giving check yet. If the black king goes to c8, the rook swings to h7 and the king follows to c6. If the black king goes to e8, Rb7 waits, and a direct Ke6 does not mate."),
        ("Ra8+", False, "The rook checks along the eighth rank and leaves the seventh rank empty. The king is no longer fenced in. Black steps off the edge with Kc7, and the mate has disappeared."),
        ("Kf6", False, "The king walks to f6, away from opposition with the king on d8. The rook still holds the seventh rank, but you have not taken the flight squares d7 and c7, so no mate is threatened."),
    ]),
    lesson(1, "end-stalemate", "Mate, not stalemate", """
- No legal move + check = mate
- No legal move, no check = stalemate, a draw
- Qb1, Qb2, Qa3, and Qa4 all mate
- Kc1 is stalemate
""", [
        step(STALEMATE, "King in the corner. Queen and king cover the escape squares.", (("b3", "a1", RED), ("c2", "b1", GREEN))),
        step(STALEMATE, "Qb1 checks, and the king on c2 defends the queen.", (("b3", "b1", RED),)),
    ], "Mate the king in the corner. Do not move your own king.", [
        ("Qb1#", True, "The queen checks the king on a1 and is defended by the king on c2. The king cannot capture her, and a2 and b2 are both covered. Qa3, Qa4, and Qb2 are also mate."),
        ("Kc1", False, "The white king steps to c1 and does not give check. The black king on a1 has no legal move, because a2, b1, and b2 are still covered. That is stalemate, a draw."),
        ("Qc3+", False, "The queen checks along the diagonal, but she has left the net. The black king walks out with Ka2 and is no longer mated."),
    ], objective="checkmate"),
]
