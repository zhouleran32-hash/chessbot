"""Part Five: class B endings. Short points, diagrams first."""

from core.primer_build import after, custom, step
from core.silman_study import point_lesson as lesson


GREEN = "#1B7F4E"
RED = "#C0392B"

CONNECTED = custom({"a8": "K", "e3": "P", "f4": "P", "d5": "k"}, turn="b")
CONNECTED_QUIZ = after(["Ke4"], CONNECTED)
BREAK = custom({"a1": "K", "f5": "P", "g4": "P", "b3": "k", "a4": "p", "f6": "p"})
TRIANGLE = custom({
    "e2": "K", "b3": "P", "c4": "P", "f5": "P", "g4": "P",
    "d6": "k", "c5": "p", "e4": "p", "f6": "p", "g5": "p",
})
FLANK = custom({"a1": "K", "a8": "k"})
SEVENTH = custom({
    "c2": "K", "d7": "R", "a6": "P", "b5": "P", "c4": "P", "g5": "P", "h4": "P",
    "g8": "k", "a8": "r", "a7": "p", "b6": "p", "c5": "p", "f7": "p", "g6": "p", "h5": "p",
}, turn="b")
SEVENTH_QUIZ = after(["Kf8"], SEVENTH)
BISHOPS = custom({"a8": "K", "f7": "B", "h6": "B", "e4": "k"})
OPPOSITE = custom({"f5": "K", "b4": "B", "d6": "P", "f4": "P", "d7": "k", "b3": "b"})

LESSONS = [
    lesson(5, "end-connected-pawns", "Connected pawns defend themselves", """
- Pawns on e3 and f4. The king is far away on a8
- e3 protects f4. The king cannot take the front pawn
- Taking e3 lets the f-pawn run
- Walk the king over. Do not push yet
""", [
        step(CONNECTED, "The pawns touch. e3 guards f4.", (("e3", "f4", GREEN),)),
        step(CONNECTED_QUIZ, "The black king has stepped to e4. Kb7 walks over.", (("a8", "b7", GREEN),)),
    ], "Walk the king to b7.", [
        ("Kb7", True, "The king starts toward the pawns. If Black takes on e3, f5, f6, f7, and f8=Q. The pawns do not need a push yet."),
        ("f5", False, "The push leaves both pawns loose. The king can take on e3 or on f5."),
        ("Kb8", False, "The king steps the wrong way. Kxe3 takes the rear pawn."),
    ]),
    lesson(5, "end-breakthrough", "The pawn break", """
- Pawns on f5 and g4. Black's f6-pawn looks like a block
- g5 pulls that pawn off f6
- f6, f7, f8=Q. The pawn queens
- Kb1 leaves the break unplayed
""", [
        step(BREAK, "f6 blocks the f-pawn. g5 pulls it away.", (("g4", "g5", GREEN), ("f6", "g5", RED))),
        step(BREAK, "g5. The only other legal move is Kb1.", (("g4", "g5", GREEN),)),
    ], "Break with g5.", [
        ("g5", True, "fxg5 is met by f6. Then g4, f7, g3, f8=Q. One pawn was given up so the other could queen."),
        ("Kb1", False, "The king walks and the f-pawn stays blocked. The break was g5."),
    ]),
    lesson(5, "end-triangulation", "Triangulation", """
- King on e2. Black king on d6, pawn on e4
- Kf2 steps aside and loses a move
- Black's best is e3+. Ke2 keeps the opposition
- Ke3 walks into Ke5. Black then has the opposition
""", [
        step(TRIANGLE, "The king can step to f2, then back to e2.", (("e2", "f2", GREEN), ("f2", "e2", RED))),
        step(TRIANGLE, "Kf2. Do not step straight to e3.", (("e2", "f2", GREEN),)),
    ], "Step aside to f2.", [
        ("Kf2", True, "e3+ is the reply. Ke2 steps back, and Ke5 is met by Kxe3. White has lost a move and kept the opposition."),
        ("Ke3", False, "Ke5 takes the opposition. The black king can reach f4, and the pawn on g4 is unprotected."),
        ("Ke1", False, "The king steps backward. Black plays e3 and the passed pawn moves closer."),
    ]),
    lesson(5, "end-outflanking", "Outflanking", """
- White king on a1. Black king on a8
- The squares to reach are f8, g8, and h8
- Ka2 takes the opposition
- Kb2 lets Black play Kb8 and take it instead
""", [
        step(FLANK, "One file between the kings would let Black step in front.", (("a1", "a2", GREEN),)),
        step(FLANK, "Ka2. The kings stay on the same file, with you to move.", (("a1", "a2", GREEN),)),
    ], "Take the opposition with Ka2.", [
        ("Ka2", True, "Kb8 is met by Kb2, then Kc2, Kd2, Ke2, Kf2, Kg2. Kf3 is the outflank. The king reaches the kingside."),
        ("Kb2", False, "Kb8 takes the opposition. The direct path does not reach f8, g8, or h8."),
        ("Kb1", False, "Kb8 still faces the king. You have not taken the opposition."),
    ]),
    lesson(5, "end-rook-on-seventh", "Rook on the seventh", """
- Rook on d7. Black king on g8, rook stuck on a8
- Kf8 is met by Rb7
- The rook on b7 freezes the king on the back rank
- Rd8+ loses the rook. Rd6 lets the king out
""", [
        step(SEVENTH, "The rook is already on the seventh rank.", (("d7", "b7", GREEN),)),
        step(SEVENTH_QUIZ, "The king stepped to f8. Swing the rook to b7.", (("d7", "b7", GREEN),)),
    ], "Swing the rook to b7.", [
        ("Rb7", True, "The king stays on the back rank. Ke8 is met by Kc3, and the rook keeps the seventh."),
        ("Rd8+", False, "Rxd8 takes the rook. Nothing defends d8."),
        ("Rd6", False, "The rook leaves the seventh. Ke7 steps off the back rank."),
    ]),
    lesson(5, "end-two-bishops", "Two bishops against a king", """
- Bishops on f7 and h6. King on a8. Enemy king on e4
- Bg6+ checks and builds a fence of diagonals
- The king then walks to b7
- Kb7 and Bh5 do not check
""", [
        step(BISHOPS, "The bishops already cover two diagonals. Bg6+ adds the next one.", (("f7", "g6", GREEN),)),
        step(BISHOPS, "Bg6+ checks the king on e4.", (("f7", "g6", GREEN),)),
    ], "Check on g6.", [
        ("Bg6+", True, "Ke5 is the reply. Kb7 brings the king over. The bishops keep the enemy king on one side of the fence."),
        ("Kb7", False, "No check. The king on e4 can still step through the center."),
        ("Bh5", False, "The bishop leaves the long diagonal and does not check."),
    ]),
    lesson(5, "end-opposite-bishops", "Opposite-colored bishops", """
- Bishop on b4, pawns on d6 and f4. One file between the pawns
- Black bishop on b3, the other color
- Kg6 controls f7 and steps off the f-pawn
- The black king and bishop can blockade both pawns
""", [
        step(OPPOSITE, "d6 is one file from the f-pawn. The bishops never meet.", (("d6", "f4", GREEN),)),
        step(OPPOSITE, "Kg6 gets off the f-pawn and attacks f7.", (("f5", "g6", GREEN), ("g6", "f7", RED))),
    ], "Step to g6.", [
        ("Kg6", True, "Ba2, f5, Bb3, f6, Ke8. The black king then shuttles, and the bishop stays on the other color. Neither pawn queens."),
        ("Kg4", False, "Bd1+ checks. The king stepped onto the black bishop's diagonal."),
        ("Ke4", False, "Bd5+ checks. The king walked into the bishop."),
    ]),
]
