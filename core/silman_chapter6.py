"""Part Six: class A endings. Short points, diagrams first."""

from core.primer_build import after, custom, step
from core.silman_study import point_lesson as lesson


GREEN = "#1B7F4E"
RED = "#C0392B"

MATE = custom({"g6": "K", "d6": "P", "e7": "P", "e8": "k", "a3": "p"})
RETI = custom({"h8": "K", "c6": "P", "a6": "k", "h5": "p"})
FIFTH = custom({"b5": "K", "d5": "P", "c7": "k", "d6": "p"})
FILES = custom({"a8": "K", "a7": "P", "e1": "R", "f7": "k", "b2": "r"})
VANCURA = custom({"a8": "R", "a6": "P", "c5": "K", "g7": "k", "f6": "r"}, turn="b")
VANCURA_LOOSE = after(["Rf5+", "Kc6", "Rf6+", "Kd5", "Rb6", "Ke5"], VANCURA)
SHORT = custom({"d4": "K", "d5": "P", "c1": "R", "b6": "k", "d8": "r"}, turn="b")
TIED = custom({"e2": "K", "b1": "B", "e5": "k", "f4": "b", "d5": "p", "e4": "p"}, turn="b")
TIED_QUIZ = after(["Kd4"], TIED)
QUEEN = custom({"g7": "K", "g8": "Q", "h1": "k", "h2": "p"})

LESSONS = [
    lesson(6, "end-pawn-mate", "Mate before the new queen", """
- Pawns on d6 and e7. Black's pawn is running to a1
- Kf6, then Ke6. The king arrives in time to support d7
- a1=Q does not save Black. d7 is mate
- d7+ at once loses a pawn. Kh6 lets the pawn queen
""", [
        step(MATE, "The a-pawn is faster. The king has to join the pawns.", (("g6", "f6", GREEN),)),
        step(MATE, "Kf6. The king is on the way to e6.", (("g6", "f6", GREEN),)),
    ], "Step to f6.", [
        ("Kf6", True, "a2 is met by Ke6. The pawn queens on a1, and d7 is mate. The new queen never gets a move."),
        ("d7+", False, "The king takes on e7 or on d7. One pawn is gone, and the mate has not been built."),
        ("Kh6", False, "The king steps away. a2 queens before the king can reach e6, and d7 is not mate."),
    ]),
    lesson(6, "end-reti", "One king, two jobs", """
- King on h8, pawn on c6. Black king on a6, pawn on h5
- Kg7 walks the diagonal. The king threatens both pawns' paths
- Chasing one pawn loses the other
- c7 at once drops the pawn
""", [
        step(RETI, "The king can head for the h-pawn and still reach the c-pawn.", (("h8", "g7", GREEN), ("c6", "c8", RED))),
        step(RETI, "Kg7. Do not push the pawn yet.", (("h8", "g7", GREEN),)),
    ], "Step to g7.", [
        ("Kg7", True, "h4, Kf6, h3, Ke7. The king is inside the square of the h-pawn, and c7 still queens. Kd7 holds the draw."),
        ("c7", False, "Kb7 attacks the pawn. c8=Q+ is met by Kxc8. The new queen is taken."),
        ("Kh7", False, "The king chases only the h-pawn. Kb6 takes the unprotected pawn on c6."),
    ]),
    lesson(6, "end-fifth-rank", "A pawn on the fifth", """
- Pawn on d5. Black pawn on d6, king on c7
- Giving up the pawn and taking the opposition usually draws
- A pawn already on the fifth is the exception
- Ka6 shoulders the enemy king off the queenside
""", [
        step(FIFTH, "The pawn is on the fifth. The king must keep Black from stepping in front.", (("b5", "a6", GREEN),)),
        step(FIFTH, "Ka6. The king takes the shoulder.", (("b5", "a6", GREEN),)),
    ], "Shoulder with Ka6.", [
        ("Ka6", True, "The king is pushed to the back rank. White takes on d6 with the opposition, and d6, d7 follow. The pawn is protected."),
        ("Kc4", False, "Kb6 steps in front of the pawn. The pawn on the fifth never gets through."),
        ("Ka5", False, "The king does not shoulder Black off. Kd8 holds the draw."),
    ]),
    lesson(6, "end-four-files", "Four files away", """
- Rook pawn on a7. White king on a8, rook on e1
- Black king on f7, four files from the pawn
- The rook has to reach b8 before the king can escape
- Rc1 starts that plan. A check on e7 drops the rook
""", [
        step(FILES, "The enemy king is four files from the pawn. Get the rook to the b-file.", (("e1", "c1", GREEN), ("c1", "b8", RED))),
        step(FILES, "Rc1. The rook is on the way to b8.", (("e1", "c1", GREEN),)),
    ], "Move the rook to c1.", [
        ("Rc1", True, "Ke7, Rc8, Kd6, Rb8. The rook is on b8, and Kb7 steps out of the corner."),
        ("Re7+", False, "Kxe7 takes the rook. The check gave the rook away."),
        ("Re8", False, "Kxe8 takes the rook. The king was not kept out of the corner."),
    ]),
    lesson(6, "end-vancura", "The Vancura draw", """
- Pawn on a6. White rook stuck on a8
- Black rook on f6. It attacks the pawn from the side
- Checks along the f-file keep the white king away
- Taking the pawn loses the rook
""", [
        step(VANCURA, "The rook on f6 attacks a6 and can check along the file.", (("f6", "f5", GREEN), ("f6", "a6", RED))),
        step(VANCURA, "Rf5+ checks the king on c5.", (("f6", "f5", GREEN),)),
    ], "Check on f5.", [
        ("Rf5+", True, "Kc6 is met by Rf6+. The rook then swings to b6 and keeps attacking the pawn. The white rook stays stuck on a8."),
        ("Rxa6", False, "The pawn is protected. Rxa6 takes the rook."),
        ("Rf8", False, "The rook leaves the sixth rank and stops attacking the pawn. a7 steps it forward."),
    ]),
    lesson(6, "end-short-side", "Checking distance", """
- Pawn on d5. Defending king on b6, the short side
- The rook belongs on the long side, the h-file
- Rh8 is ready to check from a distance
- Taking the pawn drops the rook
""", [
        step(SHORT, "The king is on the short side. The rook needs the far file.", (("d8", "h8", GREEN),)),
        step(SHORT, "Rh8. The checks will come from the h-file.", (("d8", "h8", GREEN),)),
    ], "Swing the rook to h8.", [
        ("Rh8", True, "d6 is met by Rh4+. The rook checks from the side, and the white king cannot both hide and stay with the pawn."),
        ("Rxd5+", False, "Kxd5 takes the rook. The pawn was not free."),
        ("Rc8", False, "The rook stays near the pawn. Ke5 walks in, and there is no distant file for the checks."),
    ]),
    lesson(6, "end-tie-the-king", "Tie the king to its pawn", """
- Bishops on opposite colors. Black pawns on d5 and e4
- Kd4 tries to walk in beside the pawns
- Ba2 attacks d5. The king has to stay and defend it
- Taking on e4 drops the bishop
""", [
        step(TIED, "The pawns want the king beside them. The bishop can pin that king to d5.", (("b1", "a2", GREEN), ("a2", "d5", RED))),
        step(TIED_QUIZ, "The king has stepped to d4. Ba2 attacks the pawn on d5.", (("b1", "a2", GREEN),)),
    ], "Attack the pawn from a2.", [
        ("Ba2", True, "The pawn on d5 is attacked. The king has to stay near it, and the bishop on the other color cannot drive yours off."),
        ("Bxe4", False, "Kxe4 takes the bishop. The pawn capture gave the piece away."),
        ("Bd3", False, "exd3+ takes the bishop with check."),
    ]),
    lesson(6, "end-queen-box", "The king in the box", """
- Queen on g8. Black pawn on h2, king on h1
- A rook pawn on the seventh usually draws against a queen
- Kg6 steps closer and keeps the queen's control of the g-file
- Kh6 is stalemate
""", [
        step(QUEEN, "The king has to enter the box by the pawn. Kh6 leaves Black no move.", (("g7", "g6", GREEN), ("g7", "h6", RED))),
        step(QUEEN, "Kg6. The g-file stays under the queen.", (("g7", "g6", GREEN),)),
    ], "Step to g6.", [
        ("Kg6", True, "Kg2 is met by Kf5+. The king is inside the box, and the pawn on h2 is frozen."),
        ("Kh6", False, "Stalemate. The king on h1 has no square, and the pawn blocks h2."),
        ("Kf6", False, "Stalemate as well. The king on h1 has no move. Only Kg6 leaves Black a legal move."),
    ]),
]
