"""Part Nine: studies and master endings. Short points, diagrams first."""

from core.primer_build import custom, step
from core.silman_study import point_lesson as lesson


GREEN = "#1B7F4E"
RED = "#C0392B"

TOMB = custom({
    "g2": "K", "c8": "B", "a6": "P", "f6": "P", "g5": "P", "h4": "P",
    "f8": "k", "b5": "n", "f7": "p", "g6": "p", "h5": "p",
})
SAC = custom({
    "h2": "K", "a7": "R", "a6": "R", "e6": "B", "h5": "P", "g2": "P",
    "f4": "k", "e5": "r", "a1": "r", "a4": "p", "g5": "p",
}, turn="b")
LASKER = custom({
    "f1": "K", "a1": "R", "b1": "N", "a2": "P", "b2": "P", "c2": "P", "e4": "P", "g3": "P", "h2": "P",
    "g8": "k", "a8": "r", "c8": "b", "a7": "p", "c7": "p", "c6": "p", "d4": "p", "g7": "p", "h7": "p",
}, turn="b")
TIE = custom({
    "f3": "K", "f5": "R", "a2": "P", "e3": "P", "g2": "P", "h2": "P",
    "e7": "k", "b2": "r", "a7": "p", "g7": "p", "h7": "p",
})
MAJORITY = custom({
    "g1": "K", "c3": "R", "e4": "B", "a3": "P", "b2": "P", "e3": "P", "f2": "P", "g3": "P", "h2": "P",
    "g8": "k", "d8": "r", "e6": "b", "a7": "p", "b5": "p", "c4": "p", "f7": "p", "g6": "p", "h7": "p",
}, turn="b")
SIMPLE = custom({
    "f4": "K", "e4": "B", "a5": "P", "d5": "P", "h2": "P",
    "d6": "k", "c8": "b", "a7": "p", "h6": "p",
})
BLOCK = custom({
    "g1": "K", "f8": "B", "b3": "P", "g4": "P", "g2": "P",
    "c8": "k", "e5": "b", "b5": "p", "d4": "p",
}, turn="b")

LESSONS = [
    lesson(9, "end-entombed", "Seal the knight in", """
- Bishop on c8. Knight on b5. Black king on f8
- Bd7. If the knight steps to a7, it has no move
- a7 lets the knight take the pawn. Be6 loses the bishop
""", [
        step(TOMB, "The knight's escape square is a7. The bishop has to be there first.", (("c8", "d7", GREEN), ("a6", "a7", RED))),
        step(TOMB, "Bd7. Seal the square before the pawn steps.", (("c8", "d7", GREEN),)),
    ], "Play Bd7.", [
        ("Bd7", True, "Na7 leaves the knight with no move. The king stays shut in, and the a-pawn is still on the board."),
        ("a7", False, "Nxa7. The knight takes the pawn and is not sealed in."),
        ("Be6", False, "fxe6 takes the bishop."),
    ]),
    lesson(9, "end-rook-sacrifice", "The rook on the first rank", """
- Black rook on a1, king on f4. White king on h2
- Rh1+ is the only legal check, and Kxh1 is the only reply
- Kg3 follows. Re1 then mates along the first rank
- Taking the bishop on e6 gives the other rook away
""", [
        step(SAC, "The rook on a1 can check on h1. The king then steps to g3.", (("a1", "h1", GREEN), ("e5", "e6", RED))),
        step(SAC, "Rh1+. Give up the rook.", (("a1", "h1", GREEN),)),
    ], "Sacrifice the rook on h1.", [
        ("Rh1+", True, "Kxh1 is the only reply. Kg3 follows, and Re1 mates along the first rank."),
        ("Rxe6", False, "Rxe6 takes the rook. The bishop was not worth it."),
        ("Rd5", False, "Bxd5 takes the rook."),
    ]),
    lesson(9, "end-lasker-lift", "The rook lifts to the fifth", """
- Rook on a8, bishop on c8, pawn on d4. White knight still on b1
- Rb8, then Rb5. The rook torments the queenside from the fifth rank
- Pushing d3 drops the pawn. Bf5 drops the bishop
""", [
        step(LASKER, "The rook belongs on the fifth rank, not in a pawn push.", (("a8", "b8", GREEN), ("d4", "d3", RED))),
        step(LASKER, "Rb8. The rook is on the way to b5.", (("a8", "b8", GREEN),)),
    ], "Move the rook to b8.", [
        ("Rb8", True, "b3 is met by Rb5. From the fifth rank the rook can swing to a5, c5, or h5."),
        ("d3", False, "cxd3. The pawn was not protected."),
        ("Bf5", False, "exf5 takes the bishop."),
    ]),
    lesson(9, "end-tie-down", "Tie the rook to the pawn", """
- Extra pawn. Black pawn on a7, rook active on b2
- Ra5 attacks a7 and makes the black rook defend it
- A check on f7 gives the rook away
""", [
        step(TIE, "The weakness is a7. Put the rook on it before doing anything else.", (("f5", "a5", GREEN), ("f5", "f7", RED))),
        step(TIE, "Ra5. Tie the enemy rook to the pawn.", (("f5", "a5", GREEN),)),
    ], "Play Ra5.", [
        ("Ra5", True, "Rb7, Ra6. The black rook is stuck on the a-pawn, and the white king can start on the kingside."),
        ("Rf7+", False, "Kxf7 takes the rook."),
        ("Rb5", False, "Rxb5. The rook stepped onto the black rook's file."),
    ]),
    lesson(9, "end-stop-the-king", "The rook stops the king", """
- Queenside pawns on a7, b5, and c4. Rook on d8, bishop on e6
- White king on g1. Rd1+ stops it from stepping up
- Rd4 loses the rook. Ra8 loses the rook
""", [
        step(MAJORITY, "The queenside pawns are the winners. The white king must not be allowed to walk over.", (("d8", "d1", GREEN), ("d8", "d4", RED))),
        step(MAJORITY, "Rd1+. Check before the pawns move.", (("d8", "d1", GREEN),)),
    ], "Check on d1.", [
        ("Rd1+", True, "Kg2, a5, Rc2, b4. The rook keeps the king back while the pawns advance."),
        ("Rd4", False, "exd4. The rook landed on a square nothing defends."),
        ("Ra8", False, "Bxa8 takes the rook."),
    ]),
    lesson(9, "end-simple-zug", "One bishop move", """
- King on f4, bishop on e4, passed pawn on d5
- Black king on d6 blockades the pawn. Bishop on c8
- Bf5 forces that bishop off the long diagonal
- a6 loses the pawn. Bd3 loses the d-pawn
""", [
        step(SIMPLE, "The black bishop holds f5. Take that square.", (("e4", "f5", GREEN), ("e4", "d3", RED))),
        step(SIMPLE, "Bf5. Do not touch the pawns yet.", (("e4", "f5", GREEN),)),
    ], "Play Bf5.", [
        ("Bf5", True, "Ba6 is the reply that keeps the bishop. Bb7 loses to Be6. Bxf5 Kxf5 leaves a lost pawn ending."),
        ("a6", False, "Bxa6. The bishop on c8 was watching that square."),
        ("Bd3", False, "Kxd5. The bishop left the pawn, and nothing else defends it."),
    ]),
    lesson(9, "end-bishop-block", "The bishop builds the block", """
- Bishop on e5, pawn on d4, king on c8
- White bishop on f8, king on g1, pawns on g2 and g4
- Bg3 builds a block with the d-pawn. White has to part with a pawn
- Bd6 and Bh2+ both lose the bishop
""", [
        step(BLOCK, "The bishop and the d-pawn have to stand together. Bg3 is the square.", (("e5", "g3", GREEN), ("e5", "h2", RED))),
        step(BLOCK, "Bg3. Build the block before the pawn steps.", (("e5", "g3", GREEN),)),
    ], "Play Bg3.", [
        ("Bg3", True, "Kf1, d3, Bb4. The bishop and the pawn block the white king, and White has to give up a pawn to untangle."),
        ("Bd6", False, "Bxd6 takes the bishop."),
        ("Bh2+", False, "Kxh2 takes the bishop. The check gave it away."),
    ]),
]
