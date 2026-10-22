"""Part Seven: expert endings. Short points, diagrams first."""

from core.primer_build import custom, step
from core.silman_study import point_lesson as lesson


GREEN = "#1B7F4E"
RED = "#C0392B"

FPAWN = custom({"g2": "K", "a7": "R", "f6": "k", "a1": "r", "a2": "p", "f5": "p"}, turn="b")
KING = custom({"g1": "K", "e4": "R", "c3": "P", "d4": "P", "g6": "k", "b5": "r", "g7": "p"})
PHILIDOR = custom({"d5": "K", "e5": "P", "g8": "R", "e7": "k", "h7": "r"})
SAME = custom({"c8": "K", "b2": "B", "d7": "P", "h7": "k", "a5": "b"})
WRONG = custom({"e7": "K", "f7": "B", "e5": "P", "h5": "P", "g7": "k", "e2": "b"}, turn="b")
SHUTTLE = custom({"g1": "K", "e4": "R", "f3": "P", "g2": "P", "f5": "k", "c2": "q", "g5": "p"})
BLOCK = custom({"h2": "K", "f2": "B", "g4": "R", "f3": "P", "g2": "P", "b6": "k", "c1": "q", "d4": "p", "e5": "p", "g5": "p"})

LESSONS = [
    lesson(7, "end-f-pawn", "An f-pawn takes both squares", """
- Rook on a7, in front of the pawn on a2. White king on g2
- Black rook on a1. The other pawn is on f5
- f4 pulls the king off g2 and off h2
- A g-pawn or an h-pawn can take only one of those squares
- The rook has to stay on a1. Leaving it drops the a-pawn
""", [
        step(FPAWN, "The f-pawn can take both critical squares. The rook stays behind the a-pawn.", (("f5", "f4", GREEN), ("a1", "h1", RED))),
        step(FPAWN, "f4. Do not move the rook off a1.", (("f5", "f4", GREEN),)),
    ], "Push the f-pawn.", [
        ("f4", True, "Ra8 is met by f3+. Kxf3 loses to Rf1+ and a1=Q. Kf2 loses to Rh1, and the rook takes on a2."),
        ("Rh1", False, "The rook left the pawn. Rxa2 takes it. Nothing on a1 defends a2 anymore."),
        ("Rb1", False, "The rook left a1 along the rank. Rxa2 takes the passed pawn."),
    ]),
    lesson(7, "end-king-first", "The king joins the pawns", """
- Passed pawns on c3 and d4. Rook on e4. King still on g1
- Black king on g6, rook on b5, pawn on g7
- Kf2. The king has to join before either pawn steps
- d5 drops the pawn. c4 is attacked by Rb4
""", [
        step(KING, "The pawns are connected. The king is the piece that has to move.", (("g1", "f2", GREEN), ("d4", "d5", RED))),
        step(KING, "Kf2. Leave both pawns where they are.", (("g1", "f2", GREEN),)),
    ], "Bring the king to f2.", [
        ("Kf2", True, "Kf5, Kf3, g5, Re8. The king is in the center before either pawn steps."),
        ("d5", False, "Rxd5. The pawn was not protected, and the king is still on g1."),
        ("c4", False, "Rb4 attacks c4. Kf2 is one move late, and Rxc4 takes the pawn."),
    ]),
    lesson(7, "end-philidor-bad", "Take the sixth rank first", """
- The Philidor position, with White to move
- Black's rook on h7 wants h6
- Rg6 takes the sixth rank before that rook can
- Rg7+ gives the rook away. e6 lets Rh6 happen
""", [
        step(PHILIDOR, "Black wants the sixth rank. The rook on g8 can get there first.", (("g8", "g6", GREEN), ("e5", "e6", RED))),
        step(PHILIDOR, "Rg6. Do not check, and do not push.", (("g8", "g6", GREEN),)),
    ], "Put the rook on g6.", [
        ("Rg6", True, "Kd7, Ra6, Ra7+, and Kd6. The king comes up beside the pawn. Rh6 is met by Rxh6."),
        ("Rg7+", False, "Rxg7. The check lands on a square nothing defends."),
        ("e6", False, "Rh6. The rook reaches the sixth rank and attacks the pawn."),
    ]),
    lesson(7, "end-same-color", "Block the bishop's diagonal", """
- Pawn on d7. Bishop on b2. King on c8
- Black bishop on a5 holds d8. The black king is on h7, not in front of the pawn
- Be5, then Bc7. That bishop takes the a5–d8 diagonal
- d8=Q loses the pawn and leaves a lone bishop
""", [
        step(SAME, "The bishop on a5 watches d8. Be5 is the way onto that diagonal.", (("b2", "e5", GREEN), ("d7", "d8", RED))),
        step(SAME, "Be5. Do not queen the pawn yet.", (("b2", "e5", GREEN),)),
    ], "Play Be5.", [
        ("Be5", True, "Kg6, Bc7. The bishop on c7 blocks a5–d8, so the black bishop no longer attacks d8. c7 is protected by the king."),
        ("d8=Q", False, "Bxd8. Kxd8 leaves a lone bishop. That ending cannot force mate."),
        ("Bd4", False, "The bishop on a5 still attacks d8. The pawn is still stopped."),
    ]),
    lesson(7, "end-wrong-color", "Give the bishop for the e-pawn", """
- White pawns on e5 and h5. Bishop on f7
- Black bishop on e2, king on g7
- Bg4 keeps the bishop aimed at the e-pawn
- The bishop does not attack h8. Giving it up for the e-pawn leaves that h-pawn
- Bxh5 and Bc4 both lose the bishop
""", [
        step(WRONG, "The e-pawn is the one to take. The h-pawn promotes on a square this bishop does not attack.", (("e2", "g4", GREEN), ("e2", "h5", RED))),
        step(WRONG, "Bg4. Save the bishop for the e-pawn.", (("e2", "g4", GREEN),)),
    ], "Play Bg4.", [
        ("Bg4", True, "e6 is met by Bxe6. Kxe6 leaves the h-pawn, and the bishop on f7 does not attack h8."),
        ("Bxh5", False, "Bxh5. The bishop took the h-pawn and is lost. The e-pawn is still on the board."),
        ("Bc4", False, "Bxc4. The bishop stepped onto the diagonal from f7."),
    ]),
    lesson(7, "end-rook-shuttle", "Two squares for the rook", """
- Queen on c2, king on f5, pawn on g5
- Rook on e4. Pawns on f3 and g2. King on g1
- The pawn on f3 protects both e4 and g4
- Rg4 shuttles. Re5+ and Rf4+ give the rook away
""", [
        step(SHUTTLE, "e4 and g4 are the safe squares. Both are protected by the pawn on f3.", (("e4", "g4", GREEN), ("e4", "e5", RED))),
        step(SHUTTLE, "Rg4. The rook stays on the two safe squares.", (("e4", "g4", GREEN),)),
    ], "Move the rook to g4.", [
        ("Rg4", True, "The pawn on f3 protects the rook. Kg6 can be met by Re4, back on the other safe square."),
        ("Re5+", False, "Kxe5. The check came from a square the pawn on f3 does not defend."),
        ("Rf4+", False, "Kxf4. The pawn on f3 defends e4 and g4, not f4."),
    ]),
    lesson(7, "end-bishop-blockade", "Sacrifice into the blockade", """
- Queen on c1. Pawns on d4, e5, and g5
- Bishop on f2, rook on g4, king on h2
- Bxd4+ removes the passed pawn. The rook recaptures and can sit on e4 or g4
- Re4 lets the d-pawn through. Rxd4 gives the rook away
""", [
        step(BLOCK, "The bishop can remove the d-pawn. The rook then takes its place.", (("f2", "d4", GREEN), ("g4", "e4", RED))),
        step(BLOCK, "Bxd4+. Give up the bishop for the passed pawn.", (("f2", "d4", GREEN),)),
    ], "Sacrifice the bishop on d4.", [
        ("Bxd4+", True, "exd4, Rxd4, Qc7+, Kh1. The king stays off g1. Kg1 would allow Qc5, and the rook on d4 is unprotected."),
        ("Re4", False, "Qc5 and d3 follow. The rook takes on e5, the queen takes back, and d2 queens."),
        ("Rxd4", False, "exd4 takes the rook. Bxd4+ can recover the pawn, and the queen is still on c1."),
    ]),
]
