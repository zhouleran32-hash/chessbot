"""Part Eight: master endings. Short points, diagrams first."""

from core.primer_build import after, custom, step
from core.silman_study import point_lesson as lesson


GREEN = "#1B7F4E"
RED = "#C0392B"

CAT = custom({
    "g1": "K", "d5": "R", "a6": "N", "b4": "P", "e3": "P", "f2": "P", "g3": "P", "h2": "P",
    "g8": "k", "b7": "r", "f8": "b", "b5": "p", "f7": "p", "g6": "p", "h6": "p",
})
TARGETS = custom({
    "g1": "K", "e2": "Q", "a1": "R", "d1": "R", "c3": "N",
    "a2": "P", "b2": "P", "c2": "P", "d5": "P", "f2": "P", "g2": "P", "h2": "P",
    "g8": "k", "g7": "q", "a8": "r", "f8": "r", "b7": "b",
    "a7": "p", "b6": "p", "c5": "p", "e5": "p", "f5": "p", "g6": "p", "h7": "p",
})
PAWN = custom({"g2": "K", "c4": "P", "d6": "P", "e6": "P", "f8": "k", "c5": "p", "g5": "p", "h5": "p"})
TEMPO = after(["e7+", "Ke8"], PAWN)
KNIGHT = custom({
    "f2": "K", "d3": "N", "a2": "P", "b3": "P", "e3": "P", "f3": "P", "g3": "P", "h4": "P",
    "g8": "k", "c6": "b", "a4": "p", "b5": "p", "d5": "p", "f6": "p", "g7": "p", "h7": "p",
}, turn="b")
FIGHT = custom({
    "e3": "K", "a2": "B", "b4": "P", "g3": "P", "h2": "P",
    "e5": "k", "e4": "b", "a7": "p", "d3": "p", "g5": "p", "h7": "p",
}, turn="b")
PASSER = custom({
    "h2": "K", "d1": "Q", "a6": "P", "b5": "P", "f2": "P", "g3": "P",
    "g7": "k", "b8": "q", "a7": "p", "d5": "p", "d6": "p", "f7": "p", "g6": "p", "h5": "p",
})

LESSONS = [
    lesson(8, "end-cat-mouse", "Improve, then take", """
- Knight on a6, rook on d5. The b-pawn is on b4
- Black rook on b7, bishop on f8, pawn on b5
- Nc5 improves the knight. The b-pawn can wait
- Grabbing on b5 gives the rook away
""", [
        step(CAT, "The opponent is tied to b5. Improve the knight before you touch that pawn.", (("a6", "c5", GREEN), ("d5", "b5", RED))),
        step(CAT, "Nc5. Do not take on b5.", (("a6", "c5", GREEN),)),
    ], "Jump the knight to c5.", [
        ("Nc5", True, "Ra7 is met by Nd3, and the king can step up to f3. Bxc5 is met by Rxc5."),
        ("Rxb5", False, "Rxb5 takes the rook. The pawn was not worth the rook."),
        ("Rd7", False, "Rxd7 takes the rook. The invasion landed on a square the black rook already watches."),
    ]),
    lesson(8, "end-two-weaknesses", "Make a second weakness", """
- Passed pawn on d5. It can step to d6
- Black pawns on b6 and a7. Queen on g7, bishop on b7
- a4 aims at a5 and axb6. That makes b6 a second target
- One weakness is not enough. The passer has to wait
""", [
        step(TARGETS, "The d-pawn is already a weakness. a4 creates another one.", (("a2", "a4", GREEN), ("d5", "d6", RED))),
        step(TARGETS, "a4. Leave the passed pawn where it is.", (("a2", "a4", GREEN),)),
    ], "Push the a-pawn.", [
        ("a4", True, "The pawn is on the way to a5. axb6 will weaken b6, and the d-pawn is still there."),
        ("d6", False, "The passer steps, and b6 is still a solid pawn. Nothing new was attacked."),
        ("Qxe5", False, "Qxe5. The pawn on e5 was protected, and the queen was not."),
    ]),
    lesson(8, "end-whose-move", "Whose move it is", """
- The e-pawn is already on e7. King on g2. Black king on e8
- Kh2 is the triangle. The king returns to g2 only after Black has moved twice
- Kf3 reaches the same squares with White to move, and that is a draw
- d7+ gives a pawn away
""", [
        step(TEMPO, "Black to move in this pawn ending loses. White to move draws. Lose a tempo.", (("g2", "h2", GREEN), ("d6", "d7", RED))),
        step(TEMPO, "Kh2. Start the triangle.", (("g2", "h2", GREEN),)),
    ], "Step the king to h2.", [
        ("Kh2", True, "h4, Kh3, Kf7, Kg4. Black is to move, and that position is lost for Black."),
        ("Kf3", False, "h4, Kg4, Kf7 reaches the same squares, but it is White to move. That is a draw."),
        ("d7+", False, "The king takes on d7 or on e7. Neither pawn was protected."),
    ]),
    lesson(8, "end-outside-knight", "A pawn on the other wing", """
- Knight on d3. Holes on b4, c3, and d4. Weak pawn on d5
- Black bishop on c6. Pawns on a4, b5, d5, and the kingside
- g5 makes an outside passed pawn. The knight cannot be on both wings
- Kf7 lets the knight jump to b4. d4 drops the pawn
""", [
        step(KNIGHT, "The knight wants the queenside holes. Give it a passed pawn to chase on the other wing.", (("g7", "g5", GREEN), ("d5", "d4", RED))),
        step(KNIGHT, "g5. Create the outside pawn.", (("g7", "g5", GREEN),)),
    ], "Push the g-pawn.", [
        ("g5", True, "hxg5, fxg5, Nb4. The new pawn is on the wing, away from the holes the knight wants."),
        ("Kf7", False, "Nb4 attacks the bishop on c6. axb3 axb3 leaves the knight aimed at c3 and d4."),
        ("d4", False, "exd4. The pawn was not protected."),
    ]),
    lesson(8, "end-fighting-king", "Give a pawn, gain the king", """
- Black king on e5, bishop on e4, passed pawn on d3
- White king on e3, bishop on a2, pawn on b4
- Bd5, then d2. The pawn is given up so the king can reach d4
- Bf3 loses the bishop. Bg2 loses the passed pawn
""", [
        step(FIGHT, "The king is the piece that has to enter. The pawn on d3 is the ticket.", (("e4", "d5", GREEN), ("e4", "f3", RED))),
        step(FIGHT, "Bd5. Do not step the bishop off the pawn.", (("e4", "d5", GREEN),)),
    ], "Play Bd5.", [
        ("Bd5", True, "Bb1, d2. Kxd2 is met by Be4, and the king comes to d4. Kxd3 instead of Bb1 is met by Bxa2."),
        ("Bf3", False, "Kxf3 takes the bishop."),
        ("Bg2", False, "The bishop left e4. Kxd3 takes the passed pawn."),
    ]),
    lesson(8, "end-queen-passer", "Make the passed pawn", """
- Queens on d1 and b8. White is two pawns down
- Pawns on a6 and b5 can become a passer
- Qd4+ first. The queen then protects b6
- b6 at once loses the pawn. Qxh5 loses the queen
""", [
        step(PASSER, "A passed pawn matters more than the pawn count. The queen has to protect it.", (("d1", "d4", GREEN), ("b5", "b6", RED))),
        step(PASSER, "Qd4+. The queen goes to the square that will defend b6.", (("d1", "d4", GREEN),)),
    ], "Check with Qd4+.", [
        ("Qd4+", True, "Kg8, b6. The new passed pawn is protected by the queen on d4."),
        ("b6", False, "Qxb6. The pawn stepped onto a square the queen on d1 does not defend."),
        ("Qxh5", False, "gxh5 takes the queen. The h-pawn was not worth it."),
    ]),
]
