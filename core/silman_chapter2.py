"""Part Two of Silman's endgame course: class E, original lessons.

Positions follow the book's diagrams. The wording is written for ChessBot.
"""

from core.primer_build import custom, step
from core.silman_study import point_lesson as lesson


GREEN = "#1B7F4E"
RED = "#C0392B"

KNIGHTS = custom({"g6": "K", "e5": "N", "f6": "N", "g8": "k"}, turn="b")
BISHOP = custom({"g5": "K", "f8": "B", "c2": "k", "a2": "p"}, turn="b")
FORK = custom({"h1": "K", "d3": "Q", "e5": "k", "d5": "n"})
PAWN = custom({"d3": "K", "d4": "P", "d5": "k"}, turn="b")
SEVENTH = custom({"c6": "K", "d7": "P", "d8": "k"})
ROOK_PAWN = custom({"f6": "K", "g6": "P", "g8": "k"})

LESSONS = [
    lesson(2, "end-two-knights", "Two knights cannot force mate", """
- Queen, rook, two bishops, bishop+knight: can mate
- Bishop, knight, two knights: cannot force mate
- In check: Kf8 stays out of the corner
- Kh8 loses. Nf7 mate
""", [
        step(KNIGHTS, "Check from the knight on f6. Two replies.", (("f6", "g8", RED),)),
        step(KNIGHTS, "Kf8 draws. Kh8 loses to Nf7.", (("g8", "f8", GREEN), ("g8", "h8", RED))),
    ], "You are in check. Step off the corner. Do not play the move that walks into Nf7.", [
        ("Kf8", True, "The king leaves the corner. It is not in check after this move, and two knights cannot force it back onto h8. The game is a draw if Black keeps avoiding the corner."),
        ("Kh8", False, "The king steps onto the corner square. Nf7 is then mate: the knight on e5 lands on f7, and the king has no capture, block, or flight."),
    ]),
    lesson(2, "end-queen-vs-bishop", "Queen against a bishop", """
- Promote now: a1=Q
- If you wait, Bg7 attacks a1
- Later, Kxe7 can be stalemate. Do not grab the bishop
""", [
        step(BISHOP, "Pawn on a2. Bishop still on f8.", (("a2", "a1", GREEN),)),
        step(BISHOP, "a1=Q now. Bg7 would attack a1.", (("f8", "g7", RED), ("g7", "a1", RED))),
    ], "Promote the pawn to a queen now.", [
        ("a1=Q", True, "The pawn becomes a queen before White can play Bg7. The new queen, helped by the king, can then drive White's king to the edge. The bishop cannot stop that if you avoid stalemate."),
        ("Kd3", False, "The king steps up and the pawn stays on a2. White can play Bg7, and the bishop then attacks a1. The promotion square is no longer available."),
        ("a1=N", False, "The pawn promotes, but to a knight on a1. That knight does not check, and it does not control ranks and files the way a queen does. The lesson is the queen."),
    ]),
    lesson(2, "end-knight-fork", "Do not walk into the fork", """
- Kh2 walks toward the queen
- Kg2 loses. Nf4+ forks king and queen
- Qd4+ hangs the queen. Kxd4
""", [
        step(FORK, "Knight on d5. g2 is the fork square.", (("d5", "f4", RED), ("h1", "g2", RED))),
        step(FORK, "Kh2 is safe. Kg2 allows Nf4+.", (("h1", "h2", GREEN),)),
    ], "Bring the king toward the queen without stepping onto the fork.", [
        ("Kh2", True, "The king moves toward the queen, and the knight has no check. From h2 the king can keep helping the queen push Black's king back."),
        ("Kg2", False, "Nf4+ checks the king on g2 and attacks the queen on d3 at the same time. The king cannot take the knight, and the queen cannot take it. The queen is lost."),
        ("Qd4+", False, "The queen checks from the square next to the king, and nothing defends her. Black plays Kxd4 and the queen is gone."),
    ]),
    lesson(2, "end-opposition", "Take the opposition", """
- Step straight back: Kd6
- After Ke4, answer Ke6. White has to move
- Ke6 first gives the opposition away
- Kc6 lets the white king reach e5
""", [
        step(PAWN, "King in front of the pawn. Black to move.", (("d5", "d4", RED), ("d3", "d4", GREEN))),
        step(PAWN, "Kd6, straight back.", (("d5", "d6", GREEN),)),
    ], "Step straight back and keep the opposition. Do not step sideways.", [
        ("Kd6", True, "The king stays on the pawn's file. After Ke4, Ke6 puts the kings face to face with White to move. The verified continuation runs the pawn to d7 and ends in stalemate. That is a draw."),
        ("Ke6", False, "White plays Ke4. The kings then face each other and it is Black's turn, so Black has given away the opposition. In the drawing line, those same squares arise only when it is White who must move."),
        ("Kc6", False, "The king leaves the pawn's file. White can play Ke5 and the king has stepped forward, past the pawn. The drawing move was straight back, to d6."),
    ]),
    lesson(2, "end-seventh-rank", "Whoever moves fails", """
- Pawn on d7. Black king blocks d8
- Kd6 = stalemate. A draw
- Any other king move loses the pawn. Kxd7
""", [
        step(SEVENTH, "Pawn on d7. King blocks d8.", (("d7", "d8", RED), ("c6", "d6", GREEN))),
        step(SEVENTH, "Kd6. No check. Stalemate.", (("c6", "d6", GREEN),)),
    ], "It is your move. Do not lose the pawn. Find the king move that stalemates.", [
        ("Kd6", True, "The king steps to d6 and does not check. c7, d7, and e7 are covered by the king, and c8 and e8 are covered by the pawn. Black has no move. The game is drawn."),
        ("Kb7", False, "The king steps away from the pawn. Black plays Kxd7 and the pawn is gone. The position was a stalemate draw with Kd6; this move gives the pawn away instead."),
        ("Kd5", False, "The king retreats and stops defending the pawn. Black plays Kxd7. The drawing move was Kd6, which stalemates without losing the pawn."),
    ], objective="stalemate"),
    lesson(2, "end-rook-pawn", "A rook pawn is different", """
- g7 wins. King goes to h7, then you take f7
- Same shape on the h-file: h7 is stalemate
- Ke7 leaves the pawn. Kg7 attacks g6
""", [
        step(ROOK_PAWN, "g-pawn. King on f6, enemy king on g8.", (("g6", "g7", GREEN), ("f6", "f7", RED))),
        step(ROOK_PAWN, "g7, then the king takes f7.", (("g6", "g7", GREEN),)),
    ], "Win with the g-pawn. Push it. Do not step the king away from the pawn.", [
        ("g7", True, "The pawn checks and the king must go to h7. Kf7 then takes the promotion square. The pawn queens, and Qg6 is mate after the black king is driven to h6."),
        ("Ke7", False, "The king leaves g6 unguarded. Black plays Kg7 and attacks the pawn, and the king on e7 does not defend g6. The winning move was g7, followed by Kf7."),
        ("Kf5", False, "The king walks down, away from f7, and the pawn does not move. The black king can stay on g8 or step to f8. The winning idea was g7, then Kf7."),
    ]),
]
