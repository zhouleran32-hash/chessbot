"""Study guides for class E in Silman's Complete Endgame Course.

Pages are the printed book. Diagram numbers are the book's. The notes are original.
"""

from core.primer_build import custom
from core.silman_chapter2 import BISHOP, FORK, KNIGHTS, PAWN, ROOK_PAWN, SEVENTH
from core.silman_study import check, example, guide, section


H_PAWN = custom({"g6": "K", "h6": "P", "h8": "k"})
STALE_BISHOP = custom({"h8": "K", "e7": "B", "g6": "q", "e6": "k"}, turn="b")
SEVENTH_BLACK = custom({"c6": "K", "d7": "P", "d8": "k"}, turn="b")

GUIDES = {
    "end-two-knights": guide(
        (33, 34),
        ("Name which pieces can mate a lone king, and which cannot.",
         "When two knights have driven the king to the edge, stay out of the corner."),
        (
            section("The list worth memorizing", """
                Diagram 38 is the surprising case. A queen mates a lone king. So does a rook, so do two
                bishops on opposite colors, and so does a bishop with a knight. A pawn mates only if it
                promotes. A single bishop does not. A single knight does not. Two knights do not, unless
                the defending king chooses the corner.
            """),
            section("One reply loses", """
                The knight on f6 checks the king on g8, and Black has two legal moves. Kh8 is the corner.
                Nf7, from the knight on e5, is then mate. Kf8 is not a corner square. After that move White
                has no way to force the king onto h8, a8, or a1. Two knights can mate only a king that
                cooperates.
            """),
        ),
        (
            example("Diagram 38: the corner loses", KNIGHTS, ["Kh8", "Nf7#"], (
                "Black is in check from the knight on f6. The other knight waits on e5.",
                "Kh8 steps into the corner. It is legal, and it is the losing choice.",
                "Nf7 is mate. The knight is protected by the knight on f6 and by the king on g6. The king has no flight square.",
            )),
            example("The move that draws", KNIGHTS, ["Kf8"], (
                "The same check. Black can also leave the corner.",
                "Kf8 is not check, and it is not mate. The king has stayed off h8. Keep it off every corner and two knights cannot force mate.",
            )),
        ),
        (
            "Stepping into the corner because it looks like the only way out of check.",
            "Assuming two extra knights must be enough to mate.",
        ),
        (
            check("corner", "Black is in check from the knight on f6. Which reply should the defender play?",
                ("Kf8. The king leaves the corner, and two knights cannot force it back.", True,
                 "Mate with two knights requires the king to occupy a corner. Staying off h8 draws."),
                ("Kh8. The corner is the safest square when several pieces are checking.", False,
                 "Kh8 is the corner the knights want. Nf7 is mate."),
                ("Capture the knight on f6. A king can take any piece that gives check.", False,
                 "The king on g8 does not attack f6. Those squares are two steps apart. The knight is not capturable."),
            ),
        ),
        (
            "Two knights do not force mate. If you are the defender, never step into the corner.",
        ),
    ),
    "end-queen-vs-bishop": guide(
        (35, 37),
        ("Promote a passed pawn before the bishop can attack the promotion square.",
         "Do not capture a bishop when that capture is stalemate."),
        (
            section("Promote first", """
                Diagram 39 has Black's pawn on a2. a1=Q must be played now. If the king moves instead,
                White plays Bg7. The bishop on g7 attacks a1, so the pawn can no longer promote there.
                A queen against a bishop is a win when you use the same box you used against a lone king,
                and you do not stalemate.
            """),
            section("The bishop can still draw by sacrifice", """
                Late in the book's line the bishop sits on e7, the black king on e6, and the queen on g6,
                with White's king in the corner on h8. Capturing the bishop with Kxe7 is stalemate. The
                bishop was not defending anything you needed to take. Leaving it on the board and mating
                with the queen is the win.
            """),
        ),
        (
            example("Diagram 39: the pawn queens", BISHOP, ["a1=Q", "Bd6", "Kd3"], (
                "The pawn is one square from queening. The bishop is still on f8.",
                "a1=Q promotes before White can organize Bg7.",
                "Bd6 brings the bishop back toward the king. It does not stop a queen that already exists.",
                "Kd3 steps the black king up to help the queen. The ending is now queen and king against king and bishop.",
            )),
            example("Do not take the bishop", STALE_BISHOP, ["Kxe7"], (
                "The queen is on g6 and White's king is stuck on h8. The bishop on e7 is offering itself.",
                "Kxe7 captures the bishop and does not give check. White has no piece left that can move, and the king is not in check. That is stalemate.",
            )),
        ),
        (
            "Waiting with the king while the bishop reaches g7.",
            "Capturing a bishop that was only there to be taken into stalemate.",
        ),
        (
            check("promote", "The pawn is on a2 and the bishop can still reach g7. What is the priority?",
                ("Promote to a queen immediately, before the bishop attacks a1.", True,
                 "a1=Q wins the race. Bg7 on the next move would have attacked the promotion square."),
                ("Move the king first so that it protects the new queen.", False,
                 "Kd3 gives White the move Bg7. The bishop then attacks a1, and the pawn has missed its turn."),
                ("Promote to a knight, because a knight forks and a queen can stalemate.", False,
                 "a1=N does not check and does not control the board. The queen is the piece that mates."),
            ),
        ),
        (
            "Queen the pawn at once. Then mate as you would against a lone king, and do not capture a bishop into stalemate.",
        ),
    ),
    "end-knight-fork": guide(
        (37, 38),
        ("Bring the king toward a queen-versus-knight ending without stepping onto a fork.",
         "See a knight check that also attacks the queen before you move the king."),
        (
            section("The square g2 is mined", """
                Diagram 41 has the queen on d3, the king on h1, and the knight on d5. Kg2 looks like a
                normal king step. It is not. Nf4+ checks the king on g2, and the same knight attacks the
                queen on d3. The king does not attack f4, and the queen does not attack f4. White must
                step out of check and then lose the queen.
            """),
            section("Kh2 is the safe step", """
                Kh2 also moves the king toward the queen, and the knight has no check from d5. The queen
                can then move up, as in Qd4, and the king and queen squeeze the knight the same way they
                squeeze a lone king. The extra rule is only the fork.
            """),
        ),
        (
            example("The fork the book warns about", FORK, ["Kg2", "Nf4+"], (
                "The queen is on d3. The king on h1 has a choice of neighboring squares.",
                "Kg2 steps next to the knight's fork square.",
                "Nf4+ checks and attacks d3. The queen cannot capture the knight, and the king cannot capture it either.",
            )),
            example("The safe king step", FORK, ["Kh2", "Ke6", "Qd4"], (
                "The same start. The king can move toward the queen on a different square.",
                "Kh2 does not allow a knight check.",
                "Ke6 makes room. The knight has not forked anything.",
                "Qd4 moves the queen up and takes more squares. She is not attacked. King and queen now work as a pair.",
            )),
        ),
        (
            "Moving the king to g2 because it is one step closer to the center.",
            "Checking with an undefended queen from the square beside the enemy king.",
        ),
        (
            check("fork", "Why is Kg2 a mistake when the knight is on d5 and the queen is on d3?",
                ("Nf4+ checks the king and attacks the queen on the same move.", True,
                 "A knight on f4 attacks both g2 and d3. White cannot take the knight and cannot save the queen."),
                ("The king on g2 blocks the queen's path along the second rank.", False,
                 "The queen is on d3, not on the second rank. The damage is the fork, not a blocked rank."),
                ("Kg2 loses because the knight on d5 already checks the king.", False,
                 "The knight on d5 does not check the king on h1 or on g2. The check is Nf4+, after the king has stepped to g2."),
            ),
        ),
        (
            "Before the king steps toward a knight, name the square the knight would jump to with check, and see whether the queen is on that jump as well.",
        ),
    ),
    "end-opposition": guide(
        (41, 43),
        ("Draw king and pawn against king by stepping straight back and taking the opposition.",
         "Recognize when the same king placement is a draw or a loss according to whose turn it is."),
        (
            section("Straight back", """
                Diagram 43 is the everyday pawn ending: white king on d3, pawn on d4, black king on d5,
                Black to move. Kd6 stays on the pawn's file. White plays Ke4, and Black answers Ke6. The
                kings face each other and it is White's turn, so Black owns the opposition. The book's
                continuation advances the pawn to d7 and ends with Kd6 stalemate. Black has drawn.
            """),
            section("Sideways gives the opposition away", """
                Ke6 on the first move lets White play Ke4. The kings are again on e4 and e6, but now it is
                Black's turn. That is the opposite of the drawing position. Kc6 leaves the file, and White
                can answer Ke5, stepping the king forward. The move that holds the draw is the retreat
                straight down the pawn's file.
            """),
        ),
        (
            example("Diagram 43: the drawing retreat", PAWN,
                    ["Kd6", "Ke4", "Ke6", "d5+", "Kd6", "Kd4", "Kd7", "Ke5", "Ke7", "d6+", "Kd7", "Kd5", "Kd8", "Kc6", "Kc8", "d7+", "Kd8", "Kd6"], (
                "The black king stands in front of the pawn. Black to move must not abandon that file.",
                "Kd6 steps straight back. The king still blocks the pawn.",
                "The white king steps to e4, trying to get beside the pawn.",
                "Ke6 faces that king. White is now the side that must move. Black has the opposition.",
                "d5+ checks and pushes the pawn.",
                "Kd6 goes back in front of it.",
                "Kd4 returns to the pawn's file.",
                "Kd7 continues straight back.",
                "Ke5 shoulders forward again.",
                "Ke7 meets it. White must move.",
                "d6+ checks.",
                "Kd7 stays in front.",
                "Kd5 keeps contact.",
                "Kd8 is the square directly in front of the pawn's next step.",
                "Kc6 steps sideways, and the pawn is ready.",
                "Kc8 stays near the promotion square.",
                "d7+ checks. The pawn is one square from queening.",
                "Kd8 occupies the promotion square.",
                "Kd6 does not check. The pawn and the king cover every flight square. Stalemate. The pawn never queens.",
            )),
        ),
        (
            "Stepping sideways on the first move and letting the white king take the opposition.",
            "Leaving the pawn's file so the white king can walk to e5.",
        ),
        (
            check("opposition", "The kings will stand on e4 and e6 either way. What decides the result?",
                ("Whose turn it is. If White must move, Black has the opposition and draws.", True,
                 "After Kd6 and Ke4, Black plays Ke6 and White is to move. After Ke6 first, White plays Ke4 and Black is to move."),
                ("The pawn. A pawn on d4 always queens against a lone king.", False,
                 "The verified drawing line reaches stalemate with the pawn on d7. The pawn's file is not enough by itself."),
                ("The black king should capture the pawn on d4 at the first chance.", False,
                 "The king on d3 defends the pawn. The black king on d5 cannot capture it."),
            ),
        ),
        (
            "Step straight back, face the enemy king, and make that king be the one who has to move.",
        ),
    ),
    "end-seventh-rank": guide(
        (45, 45),
        ("See when a pawn on the seventh rank wins and when the same pieces draw.",
         "Choose stalemate over a king move that loses the pawn."),
        (
            section("The same pieces, two results", """
                Diagram 47 has White's king on c6, the pawn on d7, and the black king on d8. With Black to
                move, the only legal move is Ke7, and White plays Kc7. The white king then owns d8, the
                promotion square. With White to move, the pawn cannot advance, because the black king is
                standing on d8. Kd6 is stalemate. Every other king move lets Black play Kxd7.
            """),
            section("Stalemate is the successful defense", """
                Kd6 is not a failed mating attempt. It is the move that holds the draw when White is the
                side to move. The king covers c7, d7, and e7. The pawn covers c8 and e8. The black king is
                not in check and has nothing legal. Call that before you move the king toward b7.
            """),
        ),
        (
            example("White to move: stalemate holds the draw", SEVENTH, ["Kd6"], (
                "The pawn is on d7 and the black king blocks d8. White to move.",
                "Kd6 covers the remaining flight squares and does not give check. Black has no legal move. Stalemate.",
            )),
            example("Black to move: the king is driven off", SEVENTH_BLACK, ["Ke7", "Kc7"], (
                "Shift the turn. The pieces are the same, and now Black must move. Only Ke7 is legal.",
                "Ke7 leaves d8.",
                "Kc7 takes the promotion square. The pawn on d7 is defended by the king, and d8 is now available to the pawn.",
            )),
        ),
        (
            "Moving the king to b7 so the pawn looks free, and allowing Kxd7.",
            "Retreating the king to d5 and abandoning the pawn.",
        ),
        (
            check("seventh", "It is White's move. The black king stands on the promotion square. What does Kd6 do?",
                ("It stalemates. Black is not in check and has no legal move, so the game is drawn.", True,
                 "c8 and e8 are covered by the pawn. c7, d7, and e7 are covered by the king. That is the draw."),
                ("It queens the pawn, because any king move on the seventh rank promotes.", False,
                 "The pawn cannot move to d8 while the black king is standing there. Kd6 does not move the pawn at all."),
                ("It loses, because a stalemate is scored as a win for the side that cannot move.", False,
                 "Stalemate is a draw. The side that cannot move has not lost."),
            ),
        ),
        (
            "If it is your move and the enemy king blocks the pawn, Kd6 draws. If it is the enemy's move, your king takes the promotion square.",
        ),
    ),
    "end-rook-pawn": guide(
        (45, 47),
        ("Win the same shape with a g-pawn, and recognize the h-pawn stalemate.",
         "Do not step the king off a pawn that is about to advance."),
        (
            section("One file changes the result", """
                With a king on g6, a pawn on h6, and the black king on h8, h7 is immediate stalemate. The
                king has no square to the right of the pawn. Move every piece one file toward the center:
                white king on f6, pawn on g6, black king on g8. Now g7 wins. The black king must go to h7,
                and the white king takes f7.
            """),
            section("The defender in front of a rook pawn", """
                If Black is to move in the g-pawn position, Kf8, g7+, Kg8, Kg6 is stalemate. The defender
                kept the opposition and the pawn still could not queen. That resource is even stronger on
                the h-file, where the king cannot step away from the edge. A rook pawn gives the defender
                draws that a center pawn does not.
            """),
        ),
        (
            example("Diagram 49: the g-pawn queens and mates", ROOK_PAWN,
                    ["g7", "Kh7", "Kf7", "Kh6", "g8=Q", "Kh5", "Qg3", "Kh6", "Qg6#"], (
                "The pawn is a g-pawn. The king on f6 is ready to take the square in front of it.",
                "g7 checks. Unlike the h-pawn, the black king has a square to the side.",
                "Kh7 steps off the promotion file.",
                "Kf7 takes the promotion square and defends the pawn.",
                "Kh6 is pushed to the side.",
                "The pawn queens on g8.",
                "Kh5 steps down. The new queen will cut it off.",
                "Qg3 checks along the rank and the diagonal and takes the king's escape toward the center.",
                "Kh6 goes back.",
                "Qg6 is mate. The queen is protected by the king on f7.",
            )),
            example("The h-pawn version is stalemate", H_PAWN, ["h7"], (
                "The same pattern one file to the right: king on g6, pawn on h6, black king on h8.",
                "h7 fills the last neighbor of the black king and does not give check. Black has no legal move. Stalemate.",
            )),
        ),
        (
            "Stepping the king to e7 and leaving the g-pawn unguarded.",
            "Pushing an h-pawn to the seventh rank and calling it mate.",
        ),
        (
            check("rook-pawn", "Why does h7 draw in the h-pawn position, while g7 wins with a g-pawn?",
                ("The king beside an h-pawn has no square on the outer side of the pawn, so h7 is stalemate. A g-pawn still leaves h7.", True,
                 "After h7 the king on h8 cannot move. After g7 the king goes to h7, and White's king takes f7."),
                ("An h-pawn cannot promote, so the result is always a draw.", False,
                 "An h-pawn promotes on h8 like any other pawn. It draws here because the king in front of it gets stalemated, not because promotion is illegal."),
                ("g7 wins because it captures the black king.", False,
                 "g7 checks the king on g8. The king moves to h7. The pawn does not capture anything."),
            ),
        ),
        (
            "A rook pawn draws when the enemy king is in front of it. One file toward the center, push the pawn and put your king on the promotion square.",
        ),
    ),
}
