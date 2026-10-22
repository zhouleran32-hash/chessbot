"""Study guides for the beginner band of Silman's Complete Endgame Course.

Pages are the printed book. Diagram numbers are the book's. The notes are original.
"""

from core.silman_chapter1 import BOX, QUEEN_ROOK, QUEENS, ROOK_MATE, ROOKS, STAIR, STALEMATE
from core.silman_study import check, example, guide, section


GUIDES = {
    "end-staircase": guide(
        (3, 5),
        ("Cut a king off with one major piece, then check with the other.",
         "Keep the fence piece far enough away that the king cannot capture it."),
        (
            section("A fence, then a check", """
                Diagrams 1 through 4 show the staircase with a queen and a rook. The rook on g6 is the fence:
                the king on c7 cannot cross the sixth rank. Qf7 is the check on the next rank. The king is not
                mated yet. It is pushed to the eighth rank, and only then does the rook climb from g6 to g8.
            """),
            section("Every reply on the eighth rank loses", """
                After Qf7+ the king has three legal moves, Kb8, Kc8, and Kd8. None of them crosses the rook's
                fence. Rg8 is mate against all three. The rook on g8 is protected by the queen on f7, and the
                queen also covers the seventh rank. This is a forced mate, not one sample line.
            """),
        ),
        (
            example("Diagrams 3 and 4: fence, then mate", STAIR, ["Qf7+", "Kc8", "Rg8#"], (
                "The rook on g6 fences the sixth rank. The queen is still on f1, ready to check on the seventh.",
                "Qf7 checks along the seventh rank. The king on c7 is too far away to capture the queen, and the rook still owns the sixth rank, so the king cannot step backward.",
                "Kc8 is one of the three legal replies. Kb8 and Kd8 lose the same way.",
                "Rg8 is mate. The rook is protected by the queen. The king has no capture, no block, and no flight square.",
            )),
        ),
        (
            "Checking with the rook from the square next to the king. If the queen does not defend that square, the king takes the rook.",
            "Moving the white king first and leaving both major pieces idle.",
        ),
        (
            check("fence", "What is the rook on g6 doing before the queen moves?",
                ("It fences the sixth rank, so the king cannot step backward.", True,
                 "A fence takes a whole rank away. The queen can then check on the next rank without the king slipping past."),
                ("It is attacking the king and the game is already mate.", False,
                 "The rook on g6 does not attack c7. The king is not in check until the queen moves."),
                ("It should move to c6, next to the king, to finish at once.", False,
                 "Rc6 is check, and it is also a capture for Black. The queen does not defend c6, so Kxc6 wins the rook."),
            ),
        ),
        (
            "One major piece holds a rank or file. The other checks on the next one. Do not put the fence piece where the king can take it.",
        ),
    ),
    "end-two-queens": guide(
        (5, 6),
        ("Mate with two queens by taking one rank at a time.",
         "Refuse a queen move that the lone king can capture."),
        (
            section("The queens trade ranks", """
                Diagram 5 starts with queens on a1 and b1 and the black king on d5. Qb5 checks. When the king
                goes to e6, the queen on b5 owns the fifth rank, and the queen from a1 checks on a6. The same
                swap continues, b7 and then a8, until the king is on the edge and the second queen mates.
            """),
            section("A shorter mate is not the lesson", """
                From this position there are faster mates than the staircase. They are real, and they are not
                what this lesson asks you to see. The staircase is the method that still works when you have
                a queen and a rook, or two rooks, and the faster queen jump is not available. Train the method.
            """),
        ),
        (
            example("Diagrams 5 to 7: two queens up the board", QUEENS,
                    ["Qb5+", "Ke6", "Qaa6+", "Ke7", "Qbb7+", "Kf8", "Qaa8#"], (
                "Both queens are safe on the first rank. The king on d5 cannot touch them.",
                "Qb5 checks. The queen will own the fifth rank as soon as the king leaves it.",
                "Ke6 steps up. Other replies exist; this is the book's staircase, not the only legal move.",
                "The queen from a1 checks on a6. The queen on b5 still mines the fifth rank, so the king cannot come forward.",
                "Ke7 steps back.",
                "The b5-queen checks on b7 and fences the seventh rank.",
                "Kf8 is on the edge.",
                "The queen from a6 mates on a8. She is protected by the queen on b7.",
            )),
        ),
        (
            "Putting a queen on a square next to the king when the other queen does not defend it.",
            "Taking the king's last square without giving check, which is stalemate.",
        ),
        (
            check("two-queens", "Why is Qb5 the move to learn here, rather than a queen drop next to the king?",
                ("It checks and builds a rank the king cannot cross, while the other queen stays safe.", True,
                 "The staircase uses one queen as a fence and the other as the checking piece. Both queens are still on the board afterward."),
                ("It is the fastest possible mate, so every other check is a mistake.", False,
                 "Faster mates exist from this position. The staircase is the method that transfers to a queen and rook, and to two rooks."),
                ("It wins because the king on d5 has no legal reply.", False,
                 "The king has several replies to Qb5+. The check drives it; it does not end the game on the spot."),
            ),
        ),
        (
            "Take one rank with one queen, check on the next rank with the other, and never hand a queen to the lone king.",
        ),
    ),
    "end-queen-rook": guide(
        (7, 7),
        ("Climb with queen and rook the same way as with two queens.",
         "Check with the rook only from a square the queen defends."),
        (
            section("The queen goes first", """
                Diagram 8 has the queen on g1, the rook on f1, and the black king on e5. Qg5 checks along the
                fifth rank. The queen on g5 also looks at f4. That matters on the next move: Rf4 is check, and
                the king cannot take the rook, because the queen defends it.
            """),
            section("The king can eat an undefended rook", """
                An undefended piece beside the king is lost, whether it is a queen or a rook. The rook is the
                piece beginners hang here, because it has to step closer to check. Rf5 checks, and the queen
                on g1 does not defend f5. Kxf5 takes the rook.
            """),
        ),
        (
            example("Diagrams 8 and 9: the queen guards the rook", QUEEN_ROOK,
                    ["Qg5+", "Kd4", "Rf4+", "Ke3", "Qg3+"], (
                "The king is in the center. The rook on f1 is safe only while it stays off squares the king can take.",
                "Qg5 checks along the fifth rank. From g5 the queen will defend f4.",
                "Kd4 steps toward the queenside. Ke6, Kd6, and Ke4 are also legal; this line follows one of them.",
                "Rf4 checks along the fourth rank. The queen on g5 defends the rook, so the king cannot take it.",
                "Ke3 steps back, inside the shrinking net.",
                "Qg3 checks and fences the third rank. The rook on f4 still holds the fourth. The king is being walked to the first rank. This line is an illustration of the method, not yet the mating move.",
            )),
        ),
        (
            "Leading with an undefended rook check beside the king.",
            "Assuming the rook is as safe as the queen.",
        ),
        (
            check("guard-the-rook", "After Qg5, why is Rf4 a good check and Rf5 a bad one?",
                ("The queen on g5 defends f4. She does not defend f5, so the king can take the rook there.", True,
                 "A rook check is only safe when the king cannot capture the rook. Look at the queen's lines before you move the rook."),
                ("Rf5 is better because a check on the fifth rank is closer to the king.", False,
                 "Closer is the problem. The king on e5 captures the rook on f5."),
                ("Both checks are equal, because any check drives the king backward.", False,
                 "Rf5 loses the rook. A check that hangs the mating piece is not progress."),
            ),
        ),
        (
            "The queen builds the rank and defends the square where the rook will check.",
        ),
    ),
    "end-two-rooks": guide(
        (8, 10),
        ("Cut the king off one file at a time with the rooks kept far apart from it.",
         "Move a rook that the king attacks along its own fence, not onto a square the king controls."),
        (
            section("Distance is the safety rule", """
                Diagram 10 starts with rooks on g1 and g2 and the king on e3, close enough to punish a careless
                rook. Re1 checks and makes the e-file a fence. If the king then attacks that rook, the rook
                steps up the e-file to e7. It keeps the fence and leaves the king's reach. The other rook stays
                on the g-file until it is time to take the next file.
            """),
            section("The mate is a file-by-file walk", """
                The worked line runs the king to the a-file and mates with Ra1. The rook that mates is defended
                by the other rook. Along the way, several of Black's moves are choices, not the only legal reply.
                The line shows the method. It is not a claim that every other defense has been listed.
            """),
        ),
        (
            example("Diagrams 10 to 12: files e, d, c, b, then mate", ROOKS,
                    ["Re1+", "Kd3", "Rg8", "Kd2", "Re7", "Kd3", "Rd8+", "Kc4", "Rc7+", "Kb5", "Rb8+", "Ka6", "Rc1", "Ka7", "Rb2", "Ka6", "Ra1#"], (
                "The king on e3 can reach a rook that steps beside it. Both white rooks are still on the g-file.",
                "Re1 checks and fences the e-file. The king cannot cross to the kingside.",
                "Kd3 attacks the rook on e1. That is a threat, not a capture yet.",
                "Rg8 sends the other rook up the file, far from the king.",
                "Kd2 still attacks the rook on e1.",
                "Re7 keeps the e-file fence and steps out of the king's reach.",
                "Kd3 leaves the first rank.",
                "Rd8 checks. The e7-rook still holds the e-file, so the king is pushed toward the queenside.",
                "Kc4 steps left.",
                "Rc7 checks and takes the c-file. The rook on d8 still fences the d-file.",
                "Kb5 continues toward the edge.",
                "Rb8 checks on the b-file. The king is being driven onto the a-file.",
                "Ka6 is on the edge file.",
                "Rc1 moves the checking rook far down the c-file, out of reach, while the b8-rook keeps the fence.",
                "Ka7 approaches the rook on b8.",
                "Rb2 steps down the b-file, still fencing it, and out of the king's reach.",
                "Ka6 returns.",
                "Ra1 is mate. The rook on b2 defends the mating rook, and the king cannot leave the a-file.",
            )),
        ),
        (
            "Checking with a rook on the square next to the king.",
            "Leaving a rook on a square the king attacks when a move along the fence was available.",
        ),
        (
            check("rook-distance", "The king on d2 is attacking your rook on e1. What should that rook do?",
                ("Move along the e-file to a distant square such as e7, and keep the fence.", True,
                 "The file stays closed to the king, and the rook is no longer on a square the king attacks."),
                ("Stay on e1. A rook cannot be taken if it is giving no check.", False,
                 "The king captures an undefended rook whether or not that rook is checking. On the next move Kxe1 would win it."),
                ("Move the rook to d2 and capture toward the king.", False,
                 "The king is standing on d2. A rook cannot capture the king, and stepping beside it is how rooks get taken."),
            ),
        ),
        (
            "Take one file at a time, and move an attacked rook along its fence instead of abandoning the fence.",
        ),
    ),
    "end-shrinking-box": guide(
        (10, 14),
        ("Use the queen to draw a box the king cannot leave.",
         "Bring your own king in only after the box exists, and mate with the queen defended by the king."),
        (
            section("The queen draws the walls", """
                A lone queen cannot mate a lone king. Diagram 16 starts with the queen on g1 and the black king
                on d5. Qe3 builds two walls at once: the e-file from e4 to e8, and the third rank from a3 to d3.
                The king is inside that box. Kg2 then starts the white king toward the box. Later queen checks
                make the box smaller, and the white king takes the squares the queen cannot cover.
            """),
            section("The king has other tries", """
                The worked line follows one path to Qb5 mate, including the reply Ka5. Ka7 on the last move also
                loses, to Qb7 mate. Black has other choices earlier. Treat the line as the book's picture of a
                shrinking box, and check any different reply on the board before you call it a win.
            """),
        ),
        (
            example("Diagrams 16 to 18: the box closes on the a-file", BOX,
                    ["Qe3", "Kc4", "Kg2", "Kd5", "Kf3", "Kc4", "Ke4", "Kb4", "Kd5", "Kb5", "Qb3+", "Ka6", "Kc6", "Ka5", "Qb5#"], (
                "The queen has not yet drawn a wall. The king on d5 is free.",
                "Qe3 builds the box. The king cannot cross the e-file or the third rank.",
                "Kc4 stays inside the box.",
                "The white king leaves h1 and starts toward the queen.",
                "Kd5 stays in the center of the box.",
                "Kf3 comes closer and will help cover squares near the king.",
                "Kc4 steps aside.",
                "Ke4 takes d5 away from the black king. The king and queen are now a team.",
                "Kb4 is pushed toward the edge.",
                "Kd5 keeps contact with the enemy king.",
                "Kb5 is on the b-file.",
                "Qb3 checks and fences the b-file. The white king on d5 defends the queen.",
                "Ka6 is on the edge.",
                "Kc6 comes up to support the mating square. A king move is doing the work a queen cannot do alone.",
                "Ka5 stays on the edge. Ka7 loses as well, to a queen check on b7.",
                "Qb5 is mate. The king on c6 defends the queen, and the black king has no flight square.",
            )),
        ),
        (
            "Checking with an undefended queen from the square next to the king.",
            "Marching the white king before the queen has built a box.",
        ),
        (
            check("box", "Why does the queen move to e3 before the white king leaves h1?",
                ("Qe3 draws the walls. Until those walls exist, the king march has nothing to shrink.", True,
                 "The queen traps the king in a region. The white king then removes squares inside that region."),
                ("The white king is in check on h1 and has to escape.", False,
                 "The king on h1 is not in check. Leaving h1 first does not build the box."),
                ("A queen on e3 mates at once, so the king is only a spectator.", False,
                 "Qe3 is not check, and a lone queen cannot mate a lone king. The white king has to join."),
            ),
        ),
        (
            "The queen draws the box. The king shrinks it. The mating queen stands on a square her own king defends.",
        ),
    ),
    "end-king-rook": guide(
        (14, 15),
        ("Fence the king on the edge with the rook, then bring your king alongside.",
         "Do not check with the rook until your king has taken the flight squares."),
        (
            section("The rook waits on the seventh", """
                Diagram 20 has the rook on a7 and the kings on e6 and d8. The seventh rank is the fence, so the
                black king is stuck on the eighth. Kd6 does not check. It puts the white king where it covers
                the flight squares on the seventh rank. Ra8 checks too soon: the rook leaves the seventh rank,
                and the black king steps off the edge to c7.
            """),
            section("One defense is a waiting move", """
                If the king goes to c8, Rh7 and a king march to c6 produce the mate on h8. If the king goes to
                e8, the direct Ke6 does not mate. Rb7 gives Black a move and keeps the fence. The king is then
                forced toward the white king, which is the mate shown when a king and rook finish on the edge.
                Both defenses are in the worked examples.
            """),
        ),
        (
            example("The king goes to the c-file", ROOK_MATE,
                    ["Kd6", "Kc8", "Rh7", "Kb8", "Kc6", "Ka8", "Kb6", "Kb8", "Rh8#"], (
                "The rook fences the seventh rank. The white king is one step from opposition.",
                "Kd6 threatens mate. It is not check, so the black king may choose a side.",
                "Kc8 steps toward the queenside.",
                "The rook swings to h7, far from the king, and still fences the seventh rank.",
                "Kb8 stays on the edge.",
                "Kc6 follows the king and covers the flight squares on the c-file side.",
                "Ka8 is in the corner.",
                "Kb6 takes the remaining flight squares beside the corner.",
                "Kb8 steps back next to the white king. This is the self-blocking step the rook was waiting for.",
                "Rh8 is mate. The rook checks along the eighth rank and is protected by the king on b6.",
            )),
            example("The king goes to e8, so the rook waits", ROOK_MATE,
                    ["Kd6", "Ke8", "Rb7", "Kf8", "Ke6"], (
                "The same start. The rook is on a7 and the king is ready to step to d6.",
                "Kd6 again. Black now chooses the other side.",
                "Ke8 steps in front of the white king's file.",
                "Rb7 passes. The direct Ke6 does not mate. The rook keeps the seventh-rank fence and makes Black move.",
                "Kf8 leaves the square in front of the white king.",
                "Ke6 comes back alongside. The king has been walked toward the position where a rook check on the eighth rank will mate. The finish is the same team effort as diagram 19: king covering the flight squares, rook checking on the edge.",
            )),
        ),
        (
            "Checking on the edge rank before the white king has arrived.",
            "Stepping the white king away from the enemy king and calling it opposition.",
        ),
        (
            check("rook-king", "The rook already fences the seventh rank. What is Kd6 for?",
                ("It brings the king to the rank next to the edge, so a later rook check can be mate.", True,
                 "The rook holds the king on the eighth. The white king has to cover the squares on the seventh. Kd6 starts that job."),
                ("It checks the king on d8 and forces an immediate capture.", False,
                 "Kd6 is not check. The king on d8 is not attacked by the king on d6, because a king does not attack the square two steps away."),
                ("It is a waiting move, and the rook should have checked on a8 instead.", False,
                 "Ra8 gives check and abandons the seventh rank. The black king leaves the edge with Kc7."),
            ),
        ),
        (
            "The rook keeps the king on the edge. Your king takes the flight squares. Check with the rook only when that help is in place.",
        ),
    ),
    "end-stalemate": guide(
        (20, 20),
        ("Tell checkmate from stalemate by asking whether the king is in check.",
         "Mate a king in the corner with a queen move that attacks it, not with a quiet king move."),
        (
            section("No move is not enough", """
                Diagram 27 puts the black king on a1, the white king on c2, and the queen on b3. The king in
                the corner already has no flight square that is both empty and safe. If White moves the king
                to c1, Black is not in check and has no legal move. That is stalemate, a draw. If the queen
                moves to b1, she checks, the king on c2 defends her, and there is still no flight. That is mate.
            """),
            section("Four queen moves win", """
                Qb1, Qb2, Qa3, and Qa4 all mate. The exercise accepts any of them, because each one attacks the
                king and leaves no escape. Qc3 checks and fails: the king walks out to a2. The lesson is the
                question, not a single square. Is the king in check, and can it still move?
            """),
        ),
        (
            example("Diagram 27: the queen mates", STALEMATE, ["Qb1#"], (
                "The king is buried on a1. The queen on b3 and the king on c2 cover the neighborhood, and it is White to move.",
                "Qb1 checks and is defended by the king on c2. The black king cannot take the queen, and a2 and b2 are covered. That is mate.",
            )),
            example("The same position thrown away", STALEMATE, ["Kc1"], (
                "The net around a1 is already complete. White only has to give check.",
                "Kc1 does not check. The black king has no legal move, so the game is stalemate and White has drawn a won ending.",
            )),
        ),
        (
            "Making a quiet move when the enemy king has exactly one legal answer left: none. If you are not giving check, that is stalemate.",
            "Checking from a square that lets the king out of the corner.",
        ),
        (
            check("mate-or-draw", "The black king on a1 has no safe square. White plays Kc1. What is the result?",
                ("Stalemate. The king is not in check, and Black has no legal move.", True,
                 "No legal move ends the game only when the king is not in check. Kc1 draws."),
                ("Checkmate. No legal move always means the king has lost.", False,
                 "Checkmate requires check. A king with no move and no check is a draw."),
                ("Black plays on, because a king move cannot end the game.", False,
                 "Black has nothing legal to play. The game has already ended, as a draw."),
            ),
        ),
        (
            "Before the last move, ask two questions: am I giving check, and does the king still have a square?",
        ),
    ),
}
