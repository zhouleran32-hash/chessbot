"""Part Three: class D pawn endings. Short points, diagrams first."""

from core.primer_build import after, custom, step
from core.silman_study import point_lesson as lesson


GREEN = "#1B7F4E"
RED = "#C0392B"

DISTANT = custom({"d1": "K", "d8": "k"})
ROOK_PAWN = custom({"h6": "K", "h2": "P", "h8": "k"})
ONE = custom({"d3": "K", "d2": "P", "d5": "k"})
TWO = custom({"e4": "K", "d2": "P", "e6": "k"})
STOP = custom({"h5": "K", "g5": "B", "c2": "k", "a2": "p"})
ESCORT = custom({"f4": "K", "g5": "P", "c2": "k", "b1": "r"})
ESCORT_QUIZ = after(["g6", "Kd3"], ESCORT)

LESSONS = [
    lesson(3, "end-distant-opposition", "Distant opposition", """
- Kings on d1 and d8. Six squares between them
- Even gap, your move: you have the opposition
- Kd2 keeps it. They meet on d4 and d6
- Ke2 gives it away. Black plays Ke7
""", [
        step(DISTANT, "Count the squares between the kings. d2 through d7 is six. Even.", (("d2", "d7", GREEN),)),
        step(DISTANT, "Kd2. If Black comes to d7, you answer Kd3, then Kd4.", (("d1", "d2", GREEN),)),
    ], "Keep the distant opposition.", [
        ("Kd2", True, "The kings stay on the d-file. Kd7 is met by Kd3, and Kd6 by Kd4. That is the same face-off as close opposition, reached from a distance."),
        ("Ke2", False, "You leave the file. Black plays Ke7 and now faces your king. Black has the opposition."),
        ("Kc2", False, "Same mistake on the other side. Black can play Kc7 and take the opposition."),
    ]),
    lesson(3, "end-h-pawn-draw", "Rook pawn, king in front", """
- King on h6, pawn on h2, enemy king on h8
- The king cannot be driven off the corner
- h4, then h5, h6, h7
- h7 is stalemate, not mate
""", [
        step(ROOK_PAWN, "Black's king is already in front of the h-pawn.", (("h8", "g8", GREEN),)),
        step(ROOK_PAWN, "h4 starts the pawn. The king stays on h6 until Kg6 shoulders it.", (("h2", "h4", GREEN),)),
    ], "Push the h-pawn. Do not step the king off h6.", [
        ("h4", True, "The pawn advances. The book's line is h4, Kg6, h5, h6, h7, and h7 is stalemate. A rook pawn with the enemy king in front does not win."),
        ("Kg5", False, "The king leaves h6. Black can play Kg7 and step in front of the pawn from the side."),
        ("Kh5", False, "The king steps the wrong way, off the pawn. Black again has Kg7."),
    ]),
    lesson(3, "end-one-square", "One square in front", """
- King on d3, one square in front of the pawn on d2
- Black's king on d5 has the opposition
- Ke3. Black answers Ke5 and you make no progress
- Kc3 lets the black king step to e4, in front of you
""", [
        step(ONE, "One rank between your king and the pawn. Black stands in front.", (("d3", "d2", GREEN), ("d5", "d3", RED))),
        step(ONE, "Ke3 keeps Black from stepping forward. The answer is Ke5.", (("d3", "e3", GREEN),)),
    ], "Black has the opposition. Play to e3.", [
        ("Ke3", True, "Black's drawing answer is Ke5. Then Kd3 Kd5, Kc3 Kc5. You cannot get the king in front of the pawn."),
        ("Kc3", False, "Black plays Ke4 and steps in front of your king. That is the advance you were trying to prevent."),
        ("Ke2", False, "Black plays Ke4. The kings face each other and you have not gained a rank. This is the basic draw."),
    ]),
    lesson(3, "end-two-squares", "Two squares in front", """
- King on e4. Pawn on d2. Two squares in front
- Not a rook pawn, so this wins whoever is to move
- Push: d4
- Ke3 steps back to only one square in front
""", [
        step(TWO, "Count the ranks. Pawn on the 2nd, king on the 4th.", (("d2", "e4", GREEN),)),
        step(TWO, "d4. The king is already far enough. Do not step back to e3.", (("d2", "d4", GREEN),)),
    ], "The king is two squares ahead. Push the pawn.", [
        ("d4", True, "The king stays two squares in front of a pawn that is not on the a- or h-file. Black cannot take the opposition away from that lead."),
        ("Ke3", False, "The king drops back next to the pawn. Black can play Ke5 and face you. You just gave away the second square."),
        ("Kf3", False, "The king steps off the pawn. Black can play Ke5 or Kd5 and get in front of it."),
    ]),
    lesson(3, "end-bishop-stops-pawn", "Bishop stops a pawn", """
- Pawn on a2. One move from a queen
- Bishop on g5 can reach f6 from a distance
- Bf6 attacks a1. The pawn cannot queen safely
- Kg4 does nothing. Black plays a1=Q
""", [
        step(STOP, "The bishop is far from the pawn. One step to f6.", (("g5", "f6", GREEN),)),
        step(STOP, "Bf6. The diagonal f6–e5–d4–c3–b2–a1 now belongs to the bishop.", (("f6", "a1", RED),)),
    ], "Stop the pawn from a distance.", [
        ("Bf6", True, "The bishop attacks a1. Black's king goes to b1, and the pawn never becomes a queen. Your own king can stay on g5."),
        ("Kg4", False, "The king walks toward the pawn and the bishop stays on c3. Black plays a1=Q. A queen beats a bishop."),
        ("Bh6", False, "The bishop steps the wrong way. a1 is still safe, so Black plays a1=Q."),
    ]),
    lesson(3, "end-rook-escorts", "Rook against a pawn", """
- Pawn on g6. Black king on d3. Rook on b1
- Escort the pawn with the king: Kf5
- g7 loses. The rook plays Rg1 and attacks the pawn
- The king on f4 does not defend g7
""", [
        step(ESCORT, "First the pawn goes to g6. The black king comes to d3.", (("g5", "g6", GREEN), ("c2", "d3", RED))),
        step(ESCORT_QUIZ, "Escort. Kf5. The rook check Rb5+ does not win the pawn.", (("f4", "f5", GREEN), ("b1", "g1", RED))),
    ], "Escort the pawn. Do not push it to g7.", [
        ("Kf5", True, "The king walks with the pawn. Rb5+ is check, and it does not stop the escort. g7 would be the mistake."),
        ("g7", False, "The rook plays Rg1. From g1 it attacks the pawn on g7 up the open file, and the king on f4 does not defend that pawn."),
        ("Kf3", False, "The king steps backward, away from the pawn. The escort square is f5."),
    ]),
]
