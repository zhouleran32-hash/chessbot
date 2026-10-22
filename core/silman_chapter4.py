"""Part Four: class C endings. Short points, diagrams first."""

from core.primer_build import custom, step
from core.silman_study import point_lesson as lesson


GREEN = "#1B7F4E"
RED = "#C0392B"

SQUARE = custom({"h1": "K", "a4": "P", "f7": "k"}, turn="b")
SQUARE_WHITE = custom({"h1": "K", "a4": "P", "f7": "k"})
OUTSIDE = custom({"e4": "K", "d4": "P", "g5": "P", "h4": "P", "e6": "k", "g6": "p", "h5": "p"})
BISHOP = custom({"g6": "K", "h6": "P", "e4": "B", "h8": "k"})
LUCENA = custom({"d8": "K", "d7": "P", "e2": "R", "f7": "k", "c1": "r"})
PHILIDOR = custom({"d5": "K", "e5": "P", "g8": "R", "e7": "k", "h7": "r"}, turn="b")
QUEEN_SIXTH = custom({"a8": "Q", "b7": "K", "c3": "k", "e3": "p"})
QUEEN_SEVENTH = custom({"a8": "K", "b8": "Q", "d2": "k", "e2": "p"})

LESSONS = [
    lesson(4, "end-pawn-square", "Square of the pawn", """
- Pawn on a4. Black king on f7. Black to move
- Draw the square a4–e8–e4
- A king that steps inside stops the pawn
- Kg6 and Kf6 stay outside. The pawn queens
""", [
        step(SQUARE, "The square runs from a4 to e8 to e4.", (("a4", "e8", GREEN), ("e8", "e4", GREEN))),
        step(SQUARE, "Ke6 steps inside and toward the pawn.", (("f7", "e6", GREEN),)),
    ], "Step to e6, inside the square.", [
        ("Ke6", True, "The square is a4–e8–e4. Ke6 is inside it. After a5 the king reaches b7 in time to stop the pawn."),
        ("Kg6", False, "g6 is outside the square. White pushes a5, a6, a7, and a8=Q. The king arrives too late."),
        ("Kf6", False, "f6 is also outside. The same straight push queens before the king can take the pawn."),
    ]),
    lesson(4, "end-outside-pawn", "Outside passed pawn", """
- Passed pawn on d4, far from the kingside pawns
- d5+ pulls the black king off e5
- The white king then walks to the g- and h-pawns
- Kf4 leaves the d-pawn to be attacked
""", [
        step(OUTSIDE, "The d-pawn is the decoy. The pawns that matter are on g5 and h4.", (("d4", "d8", GREEN), ("e4", "g5", RED))),
        step(OUTSIDE, "d5+ checks. The black king must deal with the pawn.", (("d4", "d5", GREEN),)),
    ], "Check with the outside pawn.", [
        ("d5+", True, "Kd6 is met by Kd4. The black king has left e5, so the white king walks in: Ke5, then d6+, and Kf6 attacks the kingside pawns."),
        ("Kf4", False, "The d-pawn never moves. Black plays Kd5 and attacks it, so you are defending the decoy."),
        ("Ke3", False, "The king steps backward. d5+ was the check that pulls the black king off e5."),
    ]),
    lesson(4, "end-wrong-bishop", "Wrong-colored bishop", """
- Bishop on e4. Rook pawn on h6. Corner is h8
- h8 is the other color. The bishop never attacks it
- h7 and Bd5 are stalemate
- Bf5 keeps the game going, and it is still a draw
""", [
        step(BISHOP, "The bishop's diagonal reaches h7, not h8.", (("e4", "h7", RED),)),
        step(BISHOP, "Bf5. Do not push h7.", (("e4", "f5", GREEN),)),
    ], "Avoid the immediate stalemate.", [
        ("Bf5", True, "Black plays Kg8. Then h7+ Kh8, and Kg5 lets the king come back to g7. The bishop cannot kick the king off h8."),
        ("h7", False, "The king on h8 is not in check, and g7, g8, and h7 are all closed. That is stalemate."),
        ("Bd5", False, "The bishop still does not attack h8. Same stalemate: no check, and no legal move."),
    ]),
    lesson(4, "end-lucena", "The Lucena position", """
- King on d8 blocks its own pawn on d7
- Rf2+ drives the black king to the side
- The rook then waits on f4. That is the bridge
- Re7+ checks forever and never frees the king
""", [
        step(LUCENA, "The king is in the pawn's way. The rook is on e2.", (("d8", "d7", RED), ("e2", "f2", GREEN))),
        step(LUCENA, "Rf2+ checks along the f-file.", (("e2", "f2", GREEN),)),
    ], "Check on f2. Then build the bridge.", [
        ("Rf2+", True, "Kg7 is the reply. Rf4 builds the bridge. The king walks out to d5, and Rd4 blocks the checks. The king on d5 protects that rook."),
        ("Re7+", False, "Kf8 steps aside. Re8+ Kf7 Re7+ Kf8 repeats. The king on d8 is still blocking the pawn."),
        ("Re1", False, "The black rook is on c1. Rxe1 takes your rook. It was not protected."),
    ]),
    lesson(4, "end-philidor", "The Philidor position", """
- Pawn on e5. Black king on e7, in front of it
- The rook belongs on the sixth rank
- Rh6 cuts the white king off
- Rh8 walks into the white rook on g8
""", [
        step(PHILIDOR, "The sixth rank is the drawing rank.", (("a6", "h6", GREEN),)),
        step(PHILIDOR, "Rh6. The rook takes that rank.", (("h7", "h6", GREEN),)),
    ], "Put the rook on the sixth rank.", [
        ("Rh6", True, "The white king cannot cross the sixth rank. Rg7+ is met by Ke8, and the rook returns to g6."),
        ("Rf7", False, "The rook leaves the sixth rank to stop a check that has not happened. White plays Ra8, and Ra7+ follows."),
        ("Rh8", False, "The white rook is already on g8. Rxh8 takes your rook."),
    ]),
    lesson(4, "end-queen-sixth", "Queen vs pawn on the sixth", """
- Pawn on e3. Queen far away on a8
- Qa5+ checks, then Qe1 stops the pawn on the file
- The white king can then walk over
- Kb6 lets the pawn step to e2
""", [
        step(QUEEN_SIXTH, "The pawn has two steps left. The queen can still reach the e-file.", (("a8", "e1", GREEN),)),
        step(QUEEN_SIXTH, "Qa5+ first. The king is driven before the pawn moves.", (("a8", "a5", GREEN),)),
    ], "Check on a5, then stop the pawn.", [
        ("Qa5+", True, "Kd3 is the reply. Qe1 stops the pawn on the e-file. Then the king walks: Kc6, Kc5, Kd5, Kc4, Kd3, and the pawn falls."),
        ("Kb6", False, "The pawn plays e2. The queen on a8 does not attack e2 or e1."),
        ("Qa4", False, "No check, and the queen does not reach the e-file. Black plays e2."),
    ]),
    lesson(4, "end-queen-seventh", "Queen vs pawn on the seventh", """
- Pawn on e2. One step from a queen
- Qb4+ starts the hunt
- Force the black king in front of the pawn
- Then step the white king closer
- Kb7 lets the pawn queen
""", [
        step(QUEEN_SEVENTH, "e1 is one move away. The queen must not allow that.", (("e2", "e1", RED),)),
        step(QUEEN_SEVENTH, "Qb4+ checks the king on d2.", (("b8", "b4", GREEN),)),
    ], "Check on b4. Do not let the pawn queen.", [
        ("Qb4+", True, "Kd1 Qd4+ Kc2 Qe3, and Qd3+ forces Ke1 in front of the pawn. Only then does the white king step to b7."),
        ("Kb7", False, "The king walks and the queen stays on b8. Black plays e1=Q."),
        ("Qb3", False, "The queen does not check, and it does not cover e1. Black plays e1=Q."),
    ]),
]
