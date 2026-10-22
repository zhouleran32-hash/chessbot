"""Chapter 3: plans, piece values, and the main tactical ideas."""

import chess

from core.primer_build import after, custom, lesson, step

GREEN = "#1B7F4E"
RED = "#C0392B"
START = chess.STARTING_FEN

LESSONS = [
    lesson(3, "plan", "A plan is a purpose for the moves", """
The pieces do not move for decoration. A plan is a short list of aims that tells you which move fits and which move only looks active. In the opening the ordinary plan is to put pawns and pieces on squares that control the center, develop the knights and bishops, and castle the king. After that, the plan follows the position: attack a weak pawn, use an open file, or start a pawn push where you have more space.
A move can be legal and still be planless. Sending the queen out on move two may attack a pawn, but it ignores development, and the queen will be chased while the opponent brings pieces out with tempo. Before you touch a piece, name the aim in one sentence. If you cannot name it, the move is probably a wish. A plan can change when the opponent creates a new weakness. What it should not do is change every move with no memory of the last one.
""", [
        step(after(["e4", "e5"]), "Both sides have a pawn in the center. White's minor pieces can come out, and the queen already has a diagonal if someone sends her too early."),
        step(after(["e4", "e5"]), "A useful plan is a knight toward the center. Qh5 is the raid that skips development."),
    ], "Start a plan of development. Bring out the king's knight toward the center.", [
        ("Nf3", True, "The knight develops toward the center and attacks e5 and d4. That fits a plan of development. The queen has not been sent on an early raid."),
        ("Qh5", False, "Qh5 attacks along a diagonal, but the queen comes out before the minor pieces. She will be driven back while Black develops."),
        ("a3", False, "a3 does not fight for the center and does not develop a piece. It spends a move without a plan you could name."),
    ]),
    lesson(3, "piece-values", "What the pieces are worth", """
The usual counting is a pawn one, a knight three, a bishop three, a rook five, and a queen nine. The king is not given a trade value, because losing him loses the game. From the pawn count, a rook is worth about five pawns. A queen is worth about two rooks, or about three minor pieces, though a rook and a pawn beside two minor pieces can be just as lively. Winning a rook for a bishop or a knight is winning the exchange, about two points.
Use the numbers before a capture, not after you regret it. When both captures are safe and no stronger threat intervenes, winning a rook gains more material than winning a bishop. The numbers are a starting count for quiet positions. The next lesson is about when a pawn near promotion, or a piece with no squares, is not worth its label. Until that happens, do not give a rook for a knight because the knight move looks clever.
""", [
        step(custom({"g2": "K", "d4": "Q", "a7": "r", "h4": "b", "g8": "k"}), "The queen on d4 can reach the rook on a7 and the bishop on h4. A rook counts about five. A bishop counts about three.", (("d4", "a7", GREEN), ("d4", "h4", RED))),
        step(custom({"g2": "K", "d4": "Q", "a7": "r", "h4": "b", "g8": "k"}), "Neither black piece is defended. The queen can take only one of them on this move, so the count decides."),
    ], "Take the more valuable piece.", [
        ("Qxa7", True, "The queen captures the rook. A rook is worth about five pawns, a bishop about three, so the rook is the greater gain."),
        ("Qxh4", False, "The bishop is free, but it is worth less than the rook. Taking it leaves the rook on the board."),
        ("Qe3", False, "Qe3 moves the queen and captures nothing. Both enemy pieces remain."),
    ]),
    lesson(3, "values-depend-on-position", "The count changes with the position", """
The pawn count is a guide, not a law. A pawn one step from promotion can be worth more than a knight sitting on the rim, because the pawn is about to become a queen. A bishop locked behind its own pawns can be worth less than a knight that has outposts. In the endgame, pawns gain value as they advance, sometimes faster than the extra piece that is trying to stop them.
Before you grab a loose piece, ask what your own most advanced pawn is doing. If it can promote safely, promotion is usually the bigger point. If the promotion square is attacked and the piece you could take is a queen, the count swings back the other way. The position decides which number is real. A knight in the center attacking the king is not "three points" in the same way as a knight buried on a8.
""", [
        step(custom({"e2": "K", "e7": "P", "b4": "B", "a5": "n", "h8": "k"}), "The pawn on e7 is one step from queening. The knight on a5 is loose, and the bishop could take it, but the pawn is about to become a queen.", (("e7", "e8", GREEN), ("b4", "a5", RED))),
        step(custom({"e2": "K", "e7": "P", "b4": "B", "a5": "n", "h8": "k"}), "Promotion gives check along the eighth rank. Promoting now gives check. Capturing the knight is also winning here: the pawn remains safe and can promote later."),
    ], "Promote the pawn. Do not turn aside for the knight.", [
        ("e8=Q+", True, "The pawn becomes a queen and checks. A queen on the board is worth far more than the knight on a5, and the check comes first."),
        ("Bxa5", False, "This wins the knight and still leaves a winning promotion next turn. It does not answer this exercise, which specifically asks you to promote now."),
        ("Ke3", False, "Ke3 moves the king and neither promotes nor captures. The pawn's value is in the next square, not in waiting."),
    ], objective="promotion"),
    lesson(3, "piece-characteristics", "How each piece likes to live", """
The queen is a rook and a bishop in one piece. She wants open lines and should not be sent to do a pawn's job. The rook wants open or half-open files, and it likes the seventh rank once it gets there. The bishop wants open diagonals and stays on one color forever, so a bishop blocked by its own pawns is a tall pawn. The knight jumps, changes color each move, and likes a supported square in the center. It is clumsy on the edge, where its possible jumps shrink to two, three or four.
The king hides early and fights late. In the endgame he is a strong piece and should walk to the center. Pawns are slow and cannot retreat. Their job is to claim space, open lines, and sometimes to become a queen. Put each piece on the square that matches its movement. A rook on a closed file and a knight on the rim are pieces standing in the wrong kind of place.
""", [
        step(custom({"g1": "K", "a1": "R", "h8": "k"}), "The e-file has no pawns on it. That is an open file, the road a rook wants. The rook is still sitting on a1.", (("a1", "e1", GREEN),)),
        step(custom({"g1": "K", "a1": "R", "h8": "k"}), "e1 is the rook's square on that open file. From there it looks up the file toward the enemy camp."),
    ], "Put the rook on the open e-file.", [
        ("Re1", True, "The rook moves to e1. No pawn blocks the e-file, so the rook now uses the kind of road rooks are built for."),
        ("Ra4", False, "Ra4 moves the rook along its own file, which is also open, but the question was the e-file, the file in the center."),
        ("Kg2", False, "Kg2 moves the king. The piece that belongs on the open file is the rook."),
    ]),
    lesson(3, "obstruction", "Your own pieces get in the way", """
A rook, bishop, or queen cannot jump. Any piece of either color standing on its line is an obstruction. Your own pawn on e2 blocks the light-squared bishop on f1. Your own knight on f3 can block a rook that wanted the f-file. The knight is the exception: it jumps, so a crowded square in front of it does not matter.
When a piece has no moves, look first for your own men in the way. Sometimes the plan is simply to move the blocker. Advancing the e-pawn opens the bishop. Moving a pawn off a file opens it for a rook. Do not add a second blocker while you are trying to free a piece. If the bishop is buried, another pawn move on a closed diagonal will not help it.
""", [
        step(START, "The bishop on f1 has no diagonal. Its own pawn on e2 is the obstruction, not an enemy piece.", (("f1", "a6", RED), ("e2", "e4", GREEN))),
        step(START, "If the e-pawn steps two squares, e2 becomes empty and the bishop can see toward c4 and a6."),
    ], "Move the e-pawn off e2 to open the bishop’s diagonal toward c4.", [
        ("e4", True, "The e-pawn leaves e2. The bishop on f1 is no longer obstructed on the diagonal toward c4."),
        ("Nf3", False, "Nf3 develops a knight and does not move the e-pawn. The bishop on f1 is still blocked."),
        ("e3", True, "e3 also vacates e2 and opens the bishop's diagonal. A one-square pawn move can remove this obstruction just as a two-square move can."),
    ]),
    lesson(3, "cutting-off", "Cutting squares off", """
Cutting a piece off means taking away a whole rank, file, or area, not just attacking one square. A rook on the fifth rank cuts the enemy king off from every square below it, as long as the rook stays there and cannot be driven away. The king may still move on his own side of the fence. He may not cross it.
This is the same idea as the rook's mating method, used earlier and for a wider purpose. You can cut a king off from the center, or cut a rook off from a file, before any capture happens. The move that builds the fence is often quiet. A check that abandons the fence lets the piece back into the area you had denied. Build the fence on a square the enemy piece does not attack, then improve your other pieces behind it.
""", [
        step(custom({"a8": "k", "g2": "K", "h1": "R"}), "The black king is on the eighth rank. A rook on the fifth rank would stop him from crossing downward, without standing next to him.", (("h1", "h5", GREEN),)),
        step(custom({"a8": "k", "g2": "K", "h1": "R"}), "h5 is far from the king on a8, so he cannot take the rook. The fifth rank becomes the line he must not cross."),
    ], "Cut the king off along the fifth rank.", [
        ("Rh5", True, "The rook fences the fifth rank. The king on a8 cannot cross it, and he does not attack h5."),
        ("Rh8+", False, "Rh8 checks along the eighth rank, but it does not build a fence in front of the king. He can step off the rank and the rook has not cut the board."),
        ("Kg3", False, "Kg3 moves the king and leaves the rook on h1. No line has been denied to Black."),
    ]),
    lesson(3, "edge-restriction", "The edge takes moves away", """
An unobstructed knight in the center can have eight jumps. A knight on the edge has three or four. A knight in the corner has two. The king also loses neighbouring squares at the edge. An empty-board rook always attacks fourteen squares; a corner bishop attacks seven, compared with thirteen on a central square. The edge is a poor home for a piece that wants mobility, and a good place to trap a piece that is already short of squares.
When you develop a knight, prefer a square toward the center over a square on the rim. Na3 and Nh3 are legal and usually weak. Nc3 and Nf3 point at the center. When the enemy knight is on the rim, you do not always need to capture it at once. Restrict it further, or take it when the capture does not ruin your own position. A piece with two moves is halfway to a piece with none.
""", [
        step(START, "The queen's knight on b1 can jump toward the center, to c3, or toward the edge, to a3. d2 is occupied by its own pawn and is unavailable. The center jump keeps more future moves.", (("b1", "c3", GREEN), ("b1", "a3", RED))),
        step(START, "c3 looks at d5 and e4. a3 looks mostly at empty squares on the rim. The edge is the restriction you should not choose for yourself."),
    ], "Move the queen's knight toward the center, not to the edge.", [
        ("Nc3", True, "The knight goes from b1 to c3. From the center side of the board it will have more jumps than it would on a3."),
        ("Na3", False, "Na3 is a legal knight move onto the rim. A knight there has fewer jumps, which is the restriction this lesson is about."),
        ("Nf3", False, "Nf3 is a good central knight move, but it moves the king's knight. The question was the knight on b1."),
    ]),
    lesson(3, 'defensive-piece', 'A piece tied to defence', """
A defensive piece has a job that limits its freedom: if it moves, a piece or an important square loses protection. This is different from simply being attacked. On this board the bishop on f3 protects the rook on e4, which Black's rook attacks along the fourth rank. Moving the bishop away carelessly would leave the rook unprotected.
One way to release the bishop is to remove the danger it is dealing with. Re3 moves the rook off the attacking rank, so the bishop is free to choose a new task. Another possibility in other positions is to add a different defender. Before moving a defender, name what it protects and check what the opponent could capture after it leaves. A useful attacking plan often starts by identifying exactly this kind of obligation.
""", [
        step(custom({'h1': 'K', 'e4': 'R', 'f3': 'B', 'a4': 'r', 'h8': 'k'}), 'The bishop on f3 defends the attacked rook on e4. Relocate the rook to release that defensive duty.'),
        step(custom({'h1': 'K', 'e4': 'R', 'f3': 'B', 'a4': 'r', 'h8': 'k'}), 'Your turn: Free the bishop from defending the attacked rook: move the rook to e3.'),
    ], 'Free the bishop from defending the attacked rook: move the rook to e3.', [
        ('Re3', True, 'The rook leaves the fourth rank. The bishop can move later without abandoning it to Rxe4.'),
        ('Be2', False, 'Be2 removes the bishop from the defence of e4 while the rook remains attacked.'),
        ('Kh2', False, 'This king move does not change the rook attack or release the bishop.'),
    ]),
    lesson(3, "pin", "The pin", """
A pin is a line attack on a piece that cannot move without exposing a more important piece behind it. If the piece behind it is the king, the pin is absolute: no move may expose that king to check. A pinned rook or bishop can sometimes move along the pin line; a pinned knight cannot jump away. A bishop or a queen pins on a diagonal. A rook or a queen pins on a rank or file. Knights do not pin, because they do not attack along a line.
Do not move a pinned piece and hope the rules will make an exception. They will not. You can break a pin by capturing the pinning piece, by putting something else in the way, or by moving the king off the line. While the king stays on the line, the pinned knight is a statue. In the position for this lesson, the bishop on a5 pins the knight on c3 to the king on e1. The knight has no legal move until the pin is broken. Moving the king to e2 breaks the pin; the pawn on b2 continues to protect the knight. d2 lies on the same diagonal, so Kd2 would not break this pin.
""", [
        step(custom({"e1": "K", "c3": "N", "a2": "P", "b2": "P", "h2": "P", "a5": "b", "h8": "k"}), "The bishop on a5, the knight on c3, and the king on e1 stand on one diagonal. The knight is pinned and cannot legally jump away.", (("a5", "e1", RED),)),
        step(custom({"e1": "K", "c3": "N", "a2": "P", "b2": "P", "h2": "P", "a5": "b", "h8": "k"}), "If the king steps to e2, he leaves the diagonal. The pawn on b2 protects the knight against Bxc3."),
    ], "Move the king to e2, off the pin line; the b2-pawn will keep the knight defended.", [
        ("Ke2", True, "The king leaves the diagonal. The knight can now move, and after Bxc3 the b2-pawn can recapture with bxc3."),
        ("a3", False, "a3 moves a pawn and does not attack the bishop on a5. The king is still on e1, so the knight stays pinned."),
        ("h3", False, "h3 is a pawn move on the other wing. It does not change the diagonal from a5 through c3 to e1."),
    ]),
    lesson(3, 'time', 'You may not have time', """
Chess time is measured in moves. A plan that needs two quiet turns can fail against a threat that arrives on the opponent's next turn. The first calculation is therefore not just what you want, but what the opponent can do immediately after your move.
Here Black's pawn on f2 can legally advance to f1 and become a queen. The rook on b2 can remove it now with Rxf2. A king move such as Kh2 gives Black the chance to promote; unlike a rook directly in front of the pawn, this rook does not block promotion or recapture the new queen from b2. The exact geometry matters. Checks can also deny the opponent time by making him answer king danger instead of advancing a pawn. Count alternate turns, and verify that every move you imagine is legal before comparing the speed of two plans.
""", [
        step(custom({'h1': 'K', 'b2': 'R', 'f2': 'p', 'a8': 'k'}), 'The f1 promotion square is empty. The rook can capture along rank two before the pawn promotes.'),
        step(custom({'h1': 'K', 'b2': 'R', 'f2': 'p', 'a8': 'k'}), 'Your turn: Stop the immediate promotion by capturing the pawn.'),
    ], 'Stop the immediate promotion by capturing the pawn.', [
        ('Rxf2', True, 'The rook captures the pawn before Black gets another move, so the promotion threat disappears.'),
        ('Kh2', False, 'Black can now play f1=Q. The rook on b2 cannot capture a queen on f1.'),
        ('Rb4', False, 'This leaves the pawn free to promote on f1, with check against the king on h1.'),
    ]),
    lesson(3, "forcing-moves", "Forcing moves", """
A forcing move is one the opponent cannot ignore. Checks are forcing, because the reply must answer the check. Captures are forcing when the captured piece matters and the recapture is the only sensible answer. Threats of mate, of promotion, or of winning a piece are forcing when the opponent has no time to start his own idea.
Some quiet moves leave the opponent a broad choice; others, such as a quiet mate threat, can be highly forcing. If you have a forcing move that improves your position, it is usually the one to calculate first. Calculate forcing moves in order: checks, then captures, then threats. That order does not mean every check is good. It means the check is the move that most limits his reply, so it is the easiest to see to the end. In this position the queen can check at once, or she can step sideways and give Black a free turn.
""", [
        step(custom({"a1": "K", "h2": "Q", "e8": "k"}), "The queen can check from h5, and Black would have to answer. A move along the second rank gives check to nobody.", (("h2", "h5", GREEN),)),
        step(custom({"a1": "K", "h2": "Q", "e8": "k"}), "From h5 the queen attacks the king on e8 along the diagonal. That is a forcing move. Qa2 is not."),
    ], "Play the forcing move: check the king.", [
        ("Qh5+", True, "The queen checks. Black's next move must answer the check, so White has forced the reply."),
        ("Qa2", False, "Qa2 does not check and does not threaten a piece. Black may play whatever he likes."),
        ("Qh4", False, "Qh4 moves the queen closer and still does not attack the king. It is not forcing."),
    ], objective="check"),
    lesson(3, "check-as-forcing", "Check comes before other plans", """
A check is the strongest ordinary forcing move because the rules themselves demand an answer. The opponent cannot push a pawn, win a piece, or continue an attack unless that action also answers the check. This is why a check gains time. Your attack lands, and his plan waits.
A check is still a move you must examine. If he can take the checking piece and win it, the check was a gift. If he can answer the check and improve his king, the check may have helped him. Use a check when the piece is safe, or when the reply you force is the one your plan needs. Do not check from habit. In this position the queen check is safe and limits Black to king moves; it does not remove Black's turn. The quiet queen moves do not.
""", [
        step(custom({"a1": "K", "d5": "Q", "e8": "k"}), "The queen on d5 can check from e5, a square the king does not attack. She can also step onto d8, beside the king, where he can capture her.", (("d5", "e5", GREEN), ("d5", "d8", RED))),
        step(custom({"a1": "K", "d5": "Q", "e8": "k"}), "Every check forces a legal response, including a possible capture of the checker. Qe5 is that check. Qd8 gives the queen away."),
    ], "Give the safe check on e5; do not offer the queen beside the king.", [
        ("Qe5+", True, "The queen checks up the e-file from e5. The king cannot capture her there, and he must answer the check."),
        ("Qd8+", False, "Qd8 checks from the square beside the king, and nothing protects the queen. He captures her and the check has cost you the queen."),
        ("Qd4", False, "Qd4 does not check. Black is not forced to do anything about the queen."),
    ]),
    lesson(3, "dual-attack", "One move, two targets", """
A dual attack, often called a fork, is one piece attacking two enemy pieces at the same time. The opponent can save only one of them on the next move, unless one of the targets captures the attacker or a move answers both threats. Knights fork well because they attack in a shape the other pieces do not share. Pawns fork by attacking two diagonal squares. Queens fork from a distance along any of their lines.
Before you play a fork, check that the forking piece is not simply taken by one of the targets, and that you are not in check yourself. A knight that attacks the king and the queen is a classic fork when the knight cannot be captured. In this position the knight on b5 can jump to c7, checking the king on a8 and attacking the queen on e8. The king does not attack c7, and the queen does not either.
""", [
        step(custom({"h1": "K", "b5": "N", "a8": "k", "e8": "q"}), "The knight on b5 can jump to c7. From c7 a knight attacks both a8 and e8, the king and the queen.", (("b5", "c7", GREEN),)),
        step(custom({"h1": "K", "b5": "N", "a8": "k", "e8": "q"}), "c7 is not attacked by the king or the queen. The check comes first, so the queen cannot simply capture the knight."),
    ], "Fork the king and the queen with the knight.", [
        ("Nc7+", True, "The knight checks the king on a8 and attacks the queen on e8. Black must answer the king check, after which Nxe8 captures the queen. The remaining king and knight against king is a draw, so the fork rescues the game rather than forcing a win."),
        ("Nd6", False, "Nd6 moves the knight and does not attack both the king and the queen. There is no fork."),
        ("Na3", False, "Na3 jumps back toward the edge. Neither the king nor the queen is attacked."),
    ]),
    lesson(3, "capture-as-forcing", "A capture that must be faced", """
A capture removes a piece at once. If the piece was undefended, the opponent does not get it back. If it was defended, he is forced to decide whether to recapture. That decision is what makes a capture forcing: his best move is often the recapture, so you can see the next position clearly.
Do not capture a defended piece of equal value just to make him move, unless the trade helps your plan. Do capture an undefended queen, rook, or minor piece when your own piece will survive. In this position the black queen stands on an open file in front of a white rook, and nothing defends her. Taking her is not a trade. It is a capture he cannot undo.
""", [
        step(custom({"g1": "K", "e1": "R", "e6": "q", "a8": "k"}), "The rook looks up the e-file at the queen on e6. No black piece defends that square.", (("e1", "e6", GREEN),)),
        step(custom({"g1": "K", "e1": "R", "e6": "q", "a8": "k"}), "Rxe6 would remove the queen. Black has no recapture, so the capture ends the question of whether she escapes."),
    ], "Capture the undefended queen.", [
        ("Rxe6", True, "The rook takes the queen on e6. Nothing can take the rook back, so the capture wins the queen outright."),
        ("Re4", False, "Re4 moves the rook up the file and does not capture. The queen can leave e6 on the next move."),
        ("Kg2", False, "Kg2 moves the king. The queen remains on e6, undefended only until Black notices."),
    ]),
    lesson(3, "promotion-as-forcing", "Promotion forces a reply", """
Promotion is forcing when the new piece gives check or attacks something the opponent cannot ignore. A pawn that becomes a queen with check combines two forcing events: a new queen appears, and the king must answer the check. He does not get a free move to take your other piece or to push his own pawn.
Underpromotion can be the forcing move when a knight check is the only way to stop his idea. Most of the time the queen is the forcing piece you want. Look at the promotion square before you push. If the new queen can be captured at once, calculate that continuation too; promotion is worthwhile only if the resulting benefit justifies the material involved. If she gives check and cannot be taken, his reply is tied to the king, and you have gained the move as well as the queen.
""", [
        step(custom({"a1": "K", "b7": "P", "g8": "k", "h2": "n"}), "The pawn on b7 can promote. The knight on h2 is a distraction worth far less than a new queen that also gives check.", (("b7", "b8", GREEN),)),
        step(custom({"a1": "K", "b7": "P", "g8": "k", "h2": "n"}), "A queen on b8 checks along the eighth rank. Black must answer that check and cannot spend the move taking nothing of equal value."),
    ], "Promote to a queen and give check. Ignore the knight for now.", [
        ("b8=Q+", True, "The pawn becomes a queen and checks the king on g8. Black must answer the check, though several king replies are legal. The new queen is the largest change on the board."),
        ("b8=N", False, "A knight on b8 does not check the king on g8. Promotion without a check, and without the queen, does not force his reply."),
        ("Kb1", False, "Kb1 moves the king and leaves the pawn on b7. Black is not forced to do anything."),
    ]),
    lesson(3, "threats", "A threat he must answer", """
A threat is a move you could play next that would damage him: mate, a capture he cannot meet, or a promotion. The move you play now may be quiet. It becomes forcing when the threat is so strong that he must stop it. Beginners look only at checks and captures. A quiet move that threatens mate can be just as forcing, because mate ends the game if it is not prevented.
Name the threat out loud. "If he does nothing, I play this." If that sentence is mate or a free queen, he will use his move to stop it, and you have directed his reply. If the sentence is only "I attack a pawn he can defend easily," you have not forced anything. In this position the bishop already aims at f7. Queen to h5 threatens to capture on f7 with mate. That threat is the point of the move, even though h5 itself is not check.
""", [
        step(after(["e4", "e5", "Bc4", "Nc6"]), "The bishop on c4 aims at f7. The queen is still on d1. Qh5 would join her to that diagonal's target without giving check yet.", (("d1", "h5", GREEN), ("c4", "f7", RED))),
        step(after(["e4", "e5", "Bc4", "Nc6"]), "From h5 the queen attacks f7 as well. If Black ignores her, Qxf7 is mate. He must answer the threat."),
    ], "Threaten mate on f7. The move itself does not have to be check.", [
        ("Qh5", True, "The queen arrives on h5 and threatens Qxf7 mate together with the bishop. Black must meet that threat on his next move."),
        ("Qf3", True, "Qf3 also threatens Qxf7 mate: the queen attacks up the f-file and the bishop protects f7. Black can defend, for example with Qf6 or Nf6."),
        ("Nf3", False, "Nf3 is good development, and it does not create the mate threat on f7. A threat has to be a specific next blow."),
    ], objective="mate_threat"),
    lesson(3, "coordination", "Pieces must work together", """
One piece rarely mates or wins a defended pawn. Coordination means two or more pieces attack the same target, or one piece defends what the other is doing. The bishop on c4 and the queen on h5 both strike f7. A rook on an open file and a queen behind it double on that file. A knight on c3 and a pawn on d4 share the defense of the center.
Before an attack, count your pieces that touch the target and his pieces that defend it. The count helps identify candidates, but values, pins, capture order and counterchecks decide whether a capture works. A queen capturing a pawn defended by a pawn still loses material, however many pieces attack that pawn. Bringing the second piece up is often the quiet move that makes the capture work on the next turn. Do not start the capture until the second piece has arrived, unless the target is undefended.
""", [
        step(after(["e4", "e5", "Bc4", "Nc6"]), "Only the bishop attacks f7 so far. The king protects f7, so Bxf7 alone would allow Kxf7. A second attacker can change that calculation.", (("c4", "f7", RED),)),
        step(after(["e4", "e5", "Bc4", "Nc6"]), "The queen can come to h5 and become the second attacker. Two pieces against f7 are coordination. One piece was only a wish."),
    ], "Bring the queen to h5 so she and the bishop both attack f7.", [
        ("Qh5", True, "The queen and the bishop now both attack f7. That is two pieces working on one point, which is coordination."),
        ("Qe2", False, "Qe2 moves the queen and does not attack f7. The bishop is still working alone."),
        ("a3", False, "a3 touches neither f7 nor the bishop's plan. No second piece joins the attack."),
    ]),
    lesson(3, "unprotected-king", "The king left in the center", """
A king on e1 or e8 with the center files opening is a target, not a developed piece. Lines open onto him, and checks gain time against the side that still has to castle. The cure in the opening is to castle. Castling puts the king toward the edge, behind pawns, and it also brings a rook toward the center. Leaving the king in the center while you hunt a pawn is how quick mates appear.
You attack an uncastled king by opening the e-file or the diagonals toward f2 and f7, then checking before he leaves. You defend your own king by castling before those lines open. In this position kingside castling is legal. The strategic point is not the hand movement of castling. It is getting the king out of the center before Black can open a file onto e1.
""", [
        step(after(["e4", "e5", "Nf3", "Nc6", "Bc4", "Bc5"]), "Both kings are still on the e-file. The center pawn has already moved, so that file can open later. White can castle now.", (("e1", "g1", GREEN),)),
        step(after(["e4", "e5", "Nf3", "Nc6", "Bc4", "Bc5"]), "g1 is behind a pawn shield. The king in the center would be the unprotected piece if the e-file opened."),
    ], "Castle the king out of the center.", [
        ("O-O", True, "The king leaves e1 for g1, and a rook comes to f1. He is no longer the unprotected piece in the center."),
        ("d3", False, "d3 is a solid pawn move and leaves the king on e1. The center is still his address."),
        ("Nc3", False, "Nc3 develops a knight and does not move the king. An uncastled king remains the target."),
    ]),
    lesson(3, "centralization", "Pieces belong in the center", """
The center consists of the four squares d4, d5, e4, and e5. Pieces can occupy those squares or control them from elsewhere. A knight in the center attacks more squares than a knight on the rim. A queen in the center can swing to either wing. A central king in a quiet endgame often has shorter routes to targets on both sides.
Centralizing is not the same as moving any piece forward. The piece should land on a square it can keep, or on a square that attacks the center. Nf3 centralizes a knight. Nh3 puts it on the rim. In the middlegame, look for a chance to put a knight on d5 or e5 when that square is supported. In an endgame, compare centralization with capturing a pawn, taking opposition, or escorting your own passer. The concrete task decides; do not visit the center automatically before pursuing a nearby target. A centrally placed piece can often reach useful squares on either wing more quickly. Count the actual moves: a central knight or king cannot reach every wing square in one move.
""", [
        step(START, "The king's knight can occupy f3, from which it attacks d4 and e5, two central squares. h3 attacks neither of them.", (("g1", "f3", GREEN), ("g1", "h3", RED))),
        step(START, "f3 is the centralizing square. The knight will influence the middle of the board instead of the edge."),
    ], "Centralize the king's knight.", [
        ("Nf3", True, "The knight moves to f3 and attacks the center. That is centralization, not a rim development."),
        ("Nh3", False, "Nh3 is legal and places the knight on the edge, where it attacks fewer squares and misses the center."),
        ("Nc3", False, "Nc3 centralizes the other knight. The question was the king's knight, from g1 to f3."),
    ]),
    lesson(3, "seventh-rank", "The seventh rank", """
When a white rook reaches the seventh rank, Black's rank 7, it can attack pawns from the side and, when the rank is unobstructed, cut the king off from coming down. A black rook on rank 2 does the same to White. Two rooks on the seventh rank can be especially strong because they combine side attacks on pawns with mating threats against a king stuck on the eighth. Their reach still depends on blockers; they do not automatically attack every square of the rank.
You invade on an open file. The rook should not land on a square attacked by a pawn unless you want the trade or the square is the mate. From the seventh rank the rook looks sideways at pawns that were safe from a frontal attack. In this position the a-file is open and a7 is empty. The rook can occupy the seventh rank in one move. That is the invasion. Captures can wait until the rook is there.
""", [
        step(custom({"b1": "K", "a1": "R", "h8": "k", "b7": "p", "h7": "p"}), "The a-file is open. A rook on a7 would attack the pawn on b7 from the side, illustrating why this rank offers targets.", (("a1", "a7", GREEN),)),
        step(custom({"b1": "K", "a1": "R", "h8": "k", "b7": "p", "h7": "p"}), "a7 is safe and empty. The b7-pawn initially blocks the rook's view farther along the rank; after capturing it, more squares become accessible."),
    ], "Put the rook on the seventh rank.", [
        ("Ra7", True, "The rook invades on a7. It attacks b7 from the side. The pawn blocks its view farther along the rank, so do not claim it already fences every seventh-rank square."),
        ("Ra4", False, "Ra4 stays on the fourth rank. The rook has moved, and it has not reached the seventh."),
        ("Kb2", False, "Kb2 moves the king. The seventh rank is a rook's idea."),
    ]),
    lesson(3, "concentration", "More attackers than defenders", """
Concentration means aiming more pieces at one point than the opponent has defenders. Two attackers against one defender can sometimes win a pawn, but only if the whole capture sequence is profitable. Count the value of everything lost and gained; a defended pawn is not a fair trade for a knight. Count before you take. The move that adds the extra attacker is the preparation. The capture is the second step.
The weak point can be a pawn, a piece, or the square in front of the king. Name it, then bring a piece to a square that attacks it without abandoning a more important defence of your own. In this position the knight on c3 already attacks the pawn on d5, and the queen on d8 is the one defender. The white queen can join the attack from d4. After she arrives, two white pieces attack d5 and only one black piece defends it.
""", [
        step(custom({"e1": "K", "d1": "Q", "c3": "N", "d5": "p", "d8": "q", "a8": "k"}), "The knight attacks d5. The black queen defends it. Nxd5 alone would allow Qxd5, giving up a knight for a pawn. The white queen can become a second attacker.", (("d1", "d4", GREEN), ("c3", "d5", RED))),
        step(custom({"e1": "K", "d1": "Q", "c3": "N", "d5": "p", "d8": "q", "a8": "k"}), "d4 attacks d5. With the queen there, White would have two attackers against one defender."),
    ], "Move the queen to d4, adding a second attacker and stopping the pawn from advancing.", [
        ("Qd4", True, "The queen moves to d4 and attacks d5. Together with the knight, White has more attackers than Black has defenders."),
        ("Qh5", False, "Qh5 moves the queen away from the d-pawn. The knight remains the only attacker, so the count is still one against one."),
        ("Ne4", False, "A knight on e4 does not attack d5. This removes the existing knight attack instead of adding the queen."),
    ]),
    lesson(3, 'deflection', 'Drawing a defender away', """
Deflection makes a defender leave a useful square so that another action becomes possible. Name the defender, its duty and the action that its departure permits. Capturing a defender removes it altogether; a deflection usually leaves it alive on a less useful square. Both may lead to the same result, but they are different mechanisms.
The black knight on f6 guards g8, so an immediate g8=Q would be met by Nxg8. White can offer the knight on e4 with check. If Black answers Nxe4, the defender leaves f6 and g8 is free for promotion. A king reply is also legal: in that case White's knight on e4 can capture f6 instead. The position teaches a concrete defensive duty, not merely the capture of a loose piece. Always inspect whether the opponent can decline the offer and keep the duty intact.
""", [
        step(custom({'h3': 'K', 'g7': 'P', 'g5': 'N', 'f2': 'k', 'f6': 'n'}), 'The knight on f6 controls g8. A knight check on e4 attacks that defender and offers to draw it away.'),
        step(custom({'h3': 'K', 'g7': 'P', 'g5': 'N', 'f2': 'k', 'f6': 'n'}), 'Your turn: Check with the knight on e4, offering to deflect the knight guarding promotion.'),
    ], 'Check with the knight on e4, offering to deflect the knight guarding promotion.', [
        ('Ne4+', True, 'After Nxe4, g8=Q is safe from that knight. After a king move, Nxf6 removes the defender instead.'),
        ('g8=Q', False, 'The defender is still on f6 and can capture the new queen with Nxg8.'),
        ('Nf3', False, 'This neither checks the king nor attacks the knight on f6; its defensive duty remains intact.'),
    ]),
    lesson(3, 'attraction', 'Drawing a piece onto a bad square', """
Attraction draws an enemy piece onto a square where a later tactic becomes possible. The square must be one the enemy can legally occupy. A protected queen that the king cannot capture is not bait that attracts that king onto her square.
Here Rh8+ offers a rook beside the black king. The king has only one legal response, Kxh8: f8, f7 and g7 are occupied by its own men, and the rook controls h7. Once the king reaches h8, Ng6+ forks it and the queen on f8. White then captures the queen. The rook sacrifice is justified by the whole sequence, not by the check alone. The knight may later be recaptured, so count that too. The remaining white queen is strong, but evaluate the remaining rook and pawns before claiming a result. Attraction and a fork cooperate: first change the king's square, then use the knight's geometry.
""", [
        step(custom({'a1': 'K', 'a4': 'Q', 'h1': 'R', 'f4': 'N', 'f6': 'P', 'g8': 'k', 'f8': 'q', 'f7': 'r', 'g7': 'p'}), 'The rook can force the king onto h8, where a knight on g6 checks it and attacks the queen on f8.'),
        step(custom({'a1': 'K', 'a4': 'Q', 'h1': 'R', 'f4': 'N', 'f6': 'P', 'g8': 'k', 'f8': 'q', 'f7': 'r', 'g7': 'p'}), 'Your turn: Offer the rook on h8 with check to attract the king onto the knight-fork square.'),
    ], 'Offer the rook on h8 with check to attract the king onto the knight-fork square.', [
        ('Rh8+', True, 'Kxh8 is the only legal reply. Ng6+ then attacks both the king on h8 and the queen on f8.'),
        ('Ng6', False, 'This attacks the queen without checking the king on g8. It does not perform the requested rook attraction onto h8.'),
        ('Qb4', False, 'This does not draw the king onto h8, so the planned knight fork is not established.'),
    ]),
    lesson(3, 'many-sided-threats', 'One move with two different threats', """
A move can create two threats that require different defences. This is broader than one piece forking two pieces: you might threaten mate and a material gain at the same time. Name both continuations and test whether one opponent move can meet both.
On this board Qh5 threatens Qxf7 mate because the bishop on c4 protects f7 and Black's own rook occupies h8. The same queen move attacks the bishop on a5 along the fifth rank. A move such as g6 blocks the mating diagonal but leaves Qxa5. Moving the bishop to b6 saves the bishop but permits Qxf7 mate. The bishop cannot defend the light squares f7 or g6 because it travels on dark squares. These are illustrative branches, not a claim that Black has only two legal moves. Search for checks or captures that might answer both threats before assuming a double threat wins.
""", [
        step(custom({'h1': 'K', 'd1': 'Q', 'c4': 'B', 'g8': 'k', 'h8': 'r', 'f7': 'p', 'g7': 'p', 'h7': 'p', 'a5': 'b'}), 'The bishop on a5 is a material target; f7 is a mating target. One queen move can threaten both.'),
        step(custom({'h1': 'K', 'd1': 'Q', 'c4': 'B', 'g8': 'k', 'h8': 'r', 'f7': 'p', 'g7': 'p', 'h7': 'p', 'a5': 'b'}), 'Your turn: Move the queen to h5, threatening mate on f7 and the bishop on a5.'),
    ], 'Move the queen to h5, threatening mate on f7 and the bishop on a5.', [
        ('Qh5', True, 'The two threats are Qxf7 mate and Qxa5. For example g6 meets mate but loses the bishop.'),
        ('Qe2', False, 'The queen does not attack the bishop on a5 or create the Qxf7 mating threat from this square.'),
        ('Bb3', False, 'This retreats the bishop and does not create the two requested threats.'),
    ]),
    lesson(3, "open-lines", "Opening a line", """
Rooks and queens need files and ranks. Bishops and queens need diagonals. Opening a line means a pawn capture or a pawn push that clears those squares. If your rook is on d1 and your own pawn leaves the d-file, the file opens and the rook starts to work. Closing a line is the defender's idea and is taught next. Do not open a file that only his rook occupies.
When you capture toward the center or trade the pawn that blocks your own piece, name the piece that will use the new road. "I take on e5 and the d-file opens for the rook" is a complete thought. "I take because captures are good" is not. In this position the rook is already on d1 and the pawn on d4 can capture on e5. After that capture the d-file has no white pawn on it.
""", [
        step(custom({"g1": "K", "d1": "R", "d4": "P", "e5": "p", "a8": "k"}), "The rook on d1 sits behind its own pawn. Capturing on e5 pulls that pawn off the d-file and opens the road.", (("d4", "e5", GREEN), ("d1", "d8", RED))),
        step(custom({"g1": "K", "d1": "R", "d4": "P", "e5": "p", "a8": "k"}), "Capturing e5 moves your own blocking d4-pawn off the d-file. d5 would push that blocker forward while keeping it on the file."),
    ], "Open the d-file for the rook by capturing on e5.", [
        ("dxe5", True, "The d-pawn captures on e5 and leaves the d-file. The rook on d1 now has an open file."),
        ("d5", False, "d5 pushes the pawn and keeps it on the d-file. The rook remains blocked by its own pawn."),
        ("Rd2", False, "Rd2 moves the rook and does not open the file. The pawn on d4 still stands between the rook and the enemy camp."),
    ]),
    lesson(3, 'block-lines', 'Blocking a line', """
A sliding piece attacks along a continuous rank, file or diagonal. Interposing a piece breaks that line. You can answer some checks this way, although a knight check or a check from an adjacent attacker cannot be blocked because there is no square between the attacker and the king.
Here the rook on e8 checks the king on e1. Ne2 puts the knight between them. The king protects that knight, so Rxe2+ would be an unfavourable rook-for-knight exchange after Kxe2. Blocking does not magically remove every problem: the knight is now pinned to the king and cannot leave the e-file while that would expose check. A later king move can release it. Always evaluate the position after the block, including captures of the blocker, rather than stopping your calculation as soon as the check disappears.
""", [
        step(custom({'e1': 'K', 'c3': 'N', 'a2': 'P', 'e8': 'r', 'a8': 'k'}), 'White is in check down the e-file. A knight can interpose on e2, where the king will protect it.'),
        step(custom({'e1': 'K', 'c3': 'N', 'a2': 'P', 'e8': 'r', 'a8': 'k'}), 'Your turn: Answer the rook check by blocking the e-file with the knight.'),
    ], 'Answer the rook check by blocking the e-file with the knight.', [
        ('Ne2', True, 'The knight blocks e8–e1. The king protects e2, so a rook capture would allow Kxe2.'),
        ('Kd2', False, 'This is a legal escape, but the requested defence is to interpose the knight on the e-file.'),
        ('Kf2', False, 'This also escapes the check, but does not practise blocking its line.'),
    ]),
    lesson(3, 'breakthrough', 'Breaking through a pawn chain', """
A pawn breakthrough creates a passed pawn by arranging exchanges through an opposing pawn chain. It often begins with a sacrifice. The important result is not the first pawn captured, but the surviving pawn that reaches a route to promotion.
White's a5, b5 and c5 pawns face Black's a7, b7 and c7 pawns. After b6, Black can capture from either side. If cxb6, White plays a6, and after bxa6 the c-pawn runs with c6. If axb6, White instead plays c6; after bxc6, a6 creates the surviving passer. Calculate both branches: memorizing b6 without seeing the follow-up will not help in a changed position. The kings are far enough away here that the advanced passer cannot be caught. In a real game king distance, whose turn it is, checks and remaining blockers can change the result completely.
""", [
        step(custom({'a1': 'K', 'a5': 'P', 'b5': 'P', 'c5': 'P', 'a7': 'p', 'b7': 'p', 'c7': 'p', 'h8': 'k'}), 'Three white pawns can sacrifice two of themselves to leave one passed pawn with a clear route.'),
        step(custom({'a1': 'K', 'a5': 'P', 'b5': 'P', 'c5': 'P', 'a7': 'p', 'b7': 'p', 'c7': 'p', 'h8': 'k'}), 'Your turn: Start the breakthrough by pushing the middle pawn to b6.'),
    ], 'Start the breakthrough by pushing the middle pawn to b6.', [
        ('b6', True, 'After cxb6 play a6; after axb6 play c6. The second sacrifice creates an outside passed pawn.'),
        ('a6', False, 'Black can answer bxa6 without opening the same forced route for another white pawn.'),
        ('c6', False, 'Black can answer bxc6. The central pawn must first divert one of the outside pawns.'),
    ]),
    lesson(3, "tempo", "Gaining a move by a threat", """
A tempo is a move's worth of time. You gain a tempo when your move contains a threat, so the opponent must answer it, and your piece has also improved. Developing a pawn onto a square that attacks his bishop does both: the pawn claims space, and the bishop must spend a move responding. He does not get to develop freely.
Losing a tempo is the opposite. You move the same piece twice without a threat, and he uses those moves to bring two pieces out. The early queen chase is a loss of tempo for the queen's owner and a gain for the player doing the chasing. In this position a pawn step to c3 attacks the bishop on b4. Black must deal with the bishop. You have developed the pawn and taken the move. That is a gained tempo.
""", [
        step(custom({"e1": "K", "c2": "P", "d2": "P", "a2": "P", "g1": "N", "b4": "b", "h8": "k"}), "The bishop on b4 can be attacked by c3. The pawn on d2 stops that bishop from checking the king on e1, so White is free to gain the tempo.", (("c2", "c3", GREEN), ("c3", "b4", RED))),
        step(custom({"e1": "K", "c2": "P", "d2": "P", "a2": "P", "g1": "N", "b4": "b", "h8": "k"}), "a4 would push a pawn and not attack b4. Nf3 would develop a knight and not touch the bishop. Of these listed choices, c3 attacks the bishop. a3 would also attack it, but this exercise asks you to use the c-pawn."),
    ], "Gain a tempo: attack the bishop with the c-pawn.", [
        ("c3", True, "The pawn steps to c3 and attacks the bishop on b4. Black must answer that threat, so White has gained a move of time."),
        ("a4", False, "a4 pushes a pawn and does not attack the bishop. Black can ignore it and continue his own plan."),
        ("Nf3", False, "Nf3 develops the knight and does not attack the bishop on b4. There is no threat, so there is no gained tempo against that piece."),
    ]),
    lesson(3, 'zugzwang', 'When the obligation to move hurts', """
Zugzwang is a position in which having to move causes a disadvantage compared with being allowed to pass. It is not simply being short of attractive moves, and it is not stalemate. In stalemate the player has no legal move and is not in check; in zugzwang legal moves exist but the obligation to choose one is harmful.
Here the kings stand on e5 and e7, with White's central pawn behind its king on e4. White can preserve the king arrangement by moving the h-pawn. Either h3 or h4 hands the move to Black. Black's king must yield space, and White can penetrate on the other side; after h3 Kd7, Kf6 is an example. The central pawn gives that penetration a useful purpose. A distant rook pawn alone would not justify a claim that opposition wins. Reserve pawn moves are resources to count carefully rather than spend automatically. This exercise practises preparation with spare tempi; the guide separately compares a genuine win-or-draw zugzwang with the h-pawn removed.
""", [
        step(custom({'e5': 'K', 'e4': 'P', 'h2': 'P', 'e7': 'k'}), 'White has a central pawn to support. A spare h-pawn move keeps the king on e5 while Black must yield space.'),
        step(custom({'e5': 'K', 'e4': 'P', 'h2': 'P', 'e7': 'k'}), 'Your turn: Use a spare h-pawn move to keep the king opposition and hand the move to Black.'),
    ], 'Use a spare h-pawn move to keep the king opposition and hand the move to Black.', [
        ('h3', True, 'h3 keeps the king on e5 and makes Black move. For example Kd7 allows Kf6 toward promotion.'),
        ('h4', True, 'h4 also preserves opposition and hands the move to Black. Both legal h-pawn advances meet this task.'),
        ('Kd4', False, 'This moves the king away from its advanced post. The exercise asks you to use the spare pawn tempo.'),
    ]),
    lesson(3, 'counterplan', 'Choose a route that obstructs his plan', """
A counterplan does more than notice the opponent's pieces: it takes their intended moves into account. Sometimes the best defence is a capture, but sometimes you can pursue your own aim while denying a square the opponent needs. This can make two routes of equal length have very different results.
White wants to reach the h7-pawn, remove it and promote h6. Black wants to bring the king from f3 through e4 and f5 towards g6 and the corner. White's Ke5 heads towards the h7-pawn while controlling e4, so Black cannot use the intended route. Ke6 would approach the target too, but would allow Ke4. The difference is one lost tempo in Black's journey. This is a useful habit in any phase of the game: before choosing between natural moves, ask what each one prevents as well as what it attacks. A plan succeeds against resistance, not against an opponent who politely waits.
""", [
        step(custom({'d6': 'K', 'h6': 'P', 'f3': 'k', 'h7': 'p'}), 'Both kings have a route in mind. White can advance to e5 while preventing Black from stepping onto e4.'),
        step(custom({'d6': 'K', 'h6': 'P', 'f3': 'k', 'h7': 'p'}), 'Your turn: Head toward h7 while barring e4: move the white king to e5.'),
    ], 'Head toward h7 while barring e4: move the white king to e5.', [
        ('Ke5', True, 'The king approaches the h-pawn and controls e4, denying a key step in Black’s intended route.'),
        ('Ke6', False, 'This approaches h7 but allows Ke4. It misses the requested obstruction of the opposing king.'),
        ('Kc6', False, 'This walks away from h7 and does not prevent Black from using e4.'),
    ]),

    lesson(3, 'bishop-vs-knight', 'Choose the piece that suits the position', """
A bishop and a knight have roughly similar average value, but their work differs. Bishops travel far along open diagonals and can act on both wings quickly; a pair of bishops covers both colours. A knight jumps over obstacles and can attack squares of either colour over successive moves. A supported central knight can be especially useful when fixed pawns obstruct bishops.
Here the black bishop on g7 is hemmed in by its own pawns on f6 and h6. White can place the knight on d5, supported by the c4-pawn, where it attacks f6. After a bishop retreat, Nxf6 wins that pawn. This does not mean every knight is better than every bishop in a closed position. Check possible pawn breaks, entry squares and whether the knight can be chased by a pawn. Compare the jobs available to the actual pieces, rather than applying their three-point labels mechanically.
""", [
        step(custom({'g1': 'K', 'f4': 'N', 'c4': 'P', 'h8': 'k', 'g7': 'b', 'f6': 'p', 'h6': 'p'}), 'The bishop has little scope behind f6 and h6. The c4-pawn supports a knight on d5.'),
        step(custom({'g1': 'K', 'f4': 'N', 'c4': 'P', 'h8': 'k', 'g7': 'b', 'f6': 'p', 'h6': 'p'}), 'Your turn: Place the knight on d5, supported by c4 and attacking f6.'),
    ], 'Place the knight on d5, supported by c4 and attacking f6.', [
        ('Nd5', True, 'The knight reaches a supported central square and attacks f6, while the bishop remains obstructed.'),
        ('Nh3', False, 'This retreats to the rim and does not attack the f6-pawn.'),
        ('Kh2', False, 'This king move does not improve the knight or exploit the obstructed bishop.'),
    ]),
    lesson(3, 'queen-vs-pawn', 'A queen can be held by stalemate', """
A queen normally beats one pawn with king support, but a pawn close to promotion can create stalemate resources. Rook pawns and bishop pawns on the seventh rank deserve particular attention when the stronger king is far away. This is an exception based on geometry, not a general rule that one advanced pawn equals a queen.
Here Black is in check from the queen on g3. Kh1 shelters the king beside its own h2-pawn. Black's pawn then cannot move because h1 is occupied by the king; g1 and g2 are controlled by the queen. If White casually moves the distant king, Black has no legal move and the game is drawn by stalemate. White must avoid that immediate draw, but repeated queen checks alone do not necessarily create time to bring the king closer. Always look for the defender's legal moves after a proposed waiting move. Removing its last move can destroy your own winning chances.
""", [
        step(custom({'a1': 'K', 'g3': 'Q', 'g1': 'k', 'h2': 'p'}, turn='b'), 'Black is in check. The corner h1 offers a stalemate resource because its own pawn cannot move through the king.'),
        step(custom({'a1': 'K', 'g3': 'Q', 'g1': 'k', 'h2': 'p'}, turn='b'), 'Your turn: As Black, step into h1 to create the stalemate shelter beside the h-pawn.'),
    ], 'As Black, step into h1 to create the stalemate shelter beside the h-pawn.', [
        ('Kh1', True, 'If White now makes an ordinary distant king move, Black is stalemated. This is a real defensive resource.'),
        ('Kf1', False, 'This legal escape leaves Black with more movement and does not create the requested corner stalemate shelter.'),
    ]),
    lesson(3, 'relative-pin', 'A relative pin is legal to break, but costly', """
An absolute pin shields a king: exposing check is illegal. A relative pin shields a valuable piece, so moving the blocker is legal but may lose material. Confusing these two cases leads to both missed tactics and imaginary restrictions.
Here the bishop on b4 looks through the knight on c3 towards the queen on e1. The knight may legally jump, but after Nd5 Black can take the queen with Bxe1. Move the queen off the diagonal first. Qe2 releases the knight while the pawn on b2 continues to protect c3; if the bishop captures it, bxc3 can recapture. There are other queen moves that could break this relative pin, but this exercise specifically practises e2. The useful habit is to name what lies behind the blocker and calculate the consequences of moving it. A legal move is not automatically a safe move, and a relative pin can sometimes be ignored if a stronger forcing tactic exists.
""", [
        step(custom({'g1': 'K', 'e1': 'Q', 'c3': 'N', 'b2': 'P', 'b4': 'b', 'g8': 'k'}), 'The knight shields the queen, not the king. It can move legally, but doing so would expose the queen.'),
        step(custom({'g1': 'K', 'e1': 'Q', 'c3': 'N', 'b2': 'P', 'b4': 'b', 'g8': 'k'}), 'Your turn: Move the queen to e2 to release the knight from its relative pin.'),
    ], 'Move the queen to e2 to release the knight from its relative pin.', [
        ('Qe2', True, 'The queen leaves the b4–e1 diagonal. The b2-pawn still protects the knight on c3.'),
        ('Nd5', False, 'This is legal, but Bxe1 would win the queen behind the knight.'),
        ('Kh2', False, 'Moving the king does not remove the queen from the bishop’s diagonal.'),
    ]),
    lesson(3, 'overloaded-defender', 'One defender cannot do every job', """
An overloaded defender is responsible for two important things that cannot both be kept safe after a forcing sequence. It may appear to defend each target adequately when you examine them separately. The tactic works by linking the targets, so that fulfilling one duty abandons the other.
Black's queen on d8 defends both rooks on c8 and g5. White can capture the c8-rook with Rxc8. If the queen recaptures, Bxg5 removes the second rook. White has given a rook and won two rooks in that line. The queen is not literally compelled to recapture: Black may choose to lose the c8-rook instead, or seek a counter-threat. The bishop on f4 attacks g5, while the rook attacks c8. The queen can defend each target separately but cannot sustain both recaptures. Count the whole sequence, check counterchecks and inspect the new position after the defender moves. Calling a piece overloaded is a conclusion to prove, not a substitute for calculation.
""", [
        step(custom({'h1': 'K', 'g1': 'N', 'b4': 'Q', 'c1': 'R', 'f4': 'B', 'h7': 'k', 'd8': 'q', 'c8': 'r', 'g5': 'r'}), 'The queen defends c8 along the rank and g5 along a diagonal. Capturing one can divert her from the other.'),
        step(custom({'h1': 'K', 'g1': 'N', 'b4': 'Q', 'c1': 'R', 'f4': 'B', 'h7': 'k', 'd8': 'q', 'c8': 'r', 'g5': 'r'}), 'Your turn: Capture the c8-rook to test the queen’s two defensive duties.'),
    ], 'Capture the c8-rook to test the queen’s two defensive duties.', [
        ('Rxc8', True, 'After Qxc8, Bxg5 wins the second rook. Declining the recapture leaves Black down the rook already captured.'),
        ('Qb3', False, 'This moves the queen away from the c8 target and does not exploit the two duties.'),
        ('Kh2', False, 'This spends a move without testing either of the queen’s defensive duties.'),
    ]),
    lesson(3, 'skewer', 'The valuable piece stands in front', """
A skewer is a line attack in which the front piece must move and exposes a piece behind it. The front piece is often the king, so check forces a response before the piece at the back can escape. Compare a pin: in a pin the less valuable shielding piece stands in front; in a skewer the more valuable piece stands in front.
White's rook can reach a7 with check against the king on d7. The black rook on h7 lies farther along the same rank, behind that king. Black cannot move the rook away while remaining in check. Once the king steps off the seventh rank, Rxh7 captures the rear rook. This example also shows why it is useful to examine alignment even when your own attacker is not yet on the line. Verify the capture after the king moves: a rear piece protected by another unit, a countercheck or an interposition can sometimes spoil an apparent skewer.
""", [
        step(custom({'g1': 'K', 'a1': 'R', 'd7': 'k', 'h7': 'r'}), 'The king on d7 and rook on h7 are aligned. A rook check on a7 attacks through the king towards the rear rook.'),
        step(custom({'g1': 'K', 'a1': 'R', 'd7': 'k', 'h7': 'r'}), 'Your turn: Skewer the king and rook with a check on the seventh rank.'),
    ], 'Skewer the king and rook with a check on the seventh rank.', [
        ('Ra7+', True, 'The king must leave the line, after which the rook on h7 can be captured.'),
        ('Rd1+', False, 'This checks up the d-file, but does not align the attacking rook with the rear rook on h7.'),
        ('Ra4', False, 'This does not check or create the requested seventh-rank skewer.'),
    ]),
    lesson(3, 'discovered-attack', 'Move one piece and uncover another', """
A discovered attack occurs when moving one of your pieces uncovers a line for another. A discovered check is especially forcing: the opponent must answer the newly exposed king attack, while the moving piece may capture or attack something elsewhere. The two pieces work on different tasks within one move.
The bishop on e4 currently blocks the rook on e1. Moving that bishop off the e-file opens a rook check against the king on e8. Bxb7+ also captures the black queen on b7. The bishop itself does not check the king from b7; the rook is the checking piece. Naming both jobs prevents a beginner from treating the move as a mysterious exception. In other positions the blocker may be pinned to its own king and unable to move, or opening the line may expose your own queen. Check both kings and all newly opened lines before celebrating a discovery.
""", [
        step(custom({'g1': 'K', 'e1': 'R', 'e4': 'B', 'e8': 'k', 'b7': 'q'}), 'The bishop blocks the e-file. Moving it to b7 captures the queen and uncovers the rook’s check.'),
        step(custom({'g1': 'K', 'e1': 'R', 'e4': 'B', 'e8': 'k', 'b7': 'q'}), 'Your turn: Capture the queen while uncovering a rook check.'),
    ], 'Capture the queen while uncovering a rook check.', [
        ('Bxb7+', True, 'The bishop captures b7 and the rook now checks along the clear e-file.'),
        ('Bf3+', False, 'This is a discovered check, but it leaves the queen on b7. The task asks you to capture her too.'),
        ('Re2', False, 'This does not move the blocking bishop or capture the queen.'),
    ]),
    lesson(3, 'underpromotion', 'Sometimes a rook is the right promotion', """
Promotion allows a queen, rook, bishop or knight. A queen is usually strongest, but its extra controlled squares can cause stalemate. A knight may instead be needed for a checking fork or a unique tempo. Decide from the resulting position rather than automatically choosing the most valuable piece.
Here c8=Q would leave the black king on a7 with no legal move while it is not in check. The queen covers a6 along the diagonal and a8 along the rank; White's king covers b5, b6 and b7. A rook on c8 controls a8 but leaves a6 available. After c8=R Ka6, Ra8 is mate. The weaker promoted piece therefore wins, while the strongest piece draws immediately. That is why counting legal replies is essential before promotion. Underpromotion does not mean choosing an unusual piece for style: it must solve a specific problem that promotion to a queen fails to solve.
""", [
        step(custom({'c6': 'K', 'c7': 'P', 'a7': 'k'}), 'A queen on c8 would take away every black move. A rook leaves a6 available and allows a forced mate.'),
        step(custom({'c6': 'K', 'c7': 'P', 'a7': 'k'}), 'Your turn: Promote without stalemating: choose the rook.'),
    ], 'Promote without stalemating: choose the rook.', [
        ('c8=R', True, 'Black can play Ka6, after which Ra8 is mate. The rook promotion preserves a win.'),
        ('c8=Q', False, 'This is stalemate: Black is not in check and has no legal move.'),
        ('c8=N+', False, 'This avoids stalemate but leaves only king and knight against king, which cannot force mate.'),
    ]),
    lesson(3, 'bishop-knight-mate', 'A bishop and knight: learn the corner pattern', """
King, bishop and knight can force mate against a lone king, but this is a demanding technique requiring coordinated control of squares. The target corner must have the same colour as the bishop. The defending king tries to stay central and, if driven back, heads for a corner of the other colour.
This exercise teaches only the final corner pattern. Nh6+ sends the black king from g8 to h8 and controls its return square g8. White's king on g6 controls g7 and h7. Bf6 then checks along f6–g7–h8, giving mate. Each white piece has a distinct job, and removing any one of those controls would create an escape. Knowing this pattern does not mean you have mastered the full ending. Practise recognizing the correct corner, building a bishop-and-knight barrier, bringing the king up and transferring the defender from a wrong corner before attempting a complete game under the fifty-move rule.
""", [
        step(custom({'g6': 'K', 'f5': 'N', 'e7': 'B', 'g8': 'k'}), 'The bishop can mate on the dark h8 corner. The knight first controls g8 while the white king controls g7 and h7.'),
        step(custom({'g6': 'K', 'f5': 'N', 'e7': 'B', 'g8': 'k'}), 'Your turn: Give the knight check on h6 that prepares the bishop mate on f6.'),
    ], 'Give the knight check on h6 that prepares the bishop mate on f6.', [
        ('Nh6+', True, 'Kh8 is forced. Bf6 then gives mate, with the knight covering g8 and king covering g7 and h7.'),
        ('Nd6', False, 'This does not check the king or establish the h8-corner mating net.'),
        ('Bf6', False, 'This bishop move does not yet check a king on g8. The knight must first control its return square.'),
    ]),
    lesson(3, 'triangulation', 'Return to the same board with the other side to move', """
Triangulation is a manoeuvre in which one king uses three squares while the other king can only shuttle between two useful squares. The board returns to the same arrangement with the other player to move. This can turn a drawn-looking position into a win when the obligation to move is harmful.
Here White can play Kd5, followed in the illustrated defence by Kf6, then Ke4 Ke7 and Ke5. The original arrangement returns, but now it is Black's turn. White has changed no pawn square and has not magically taken two moves in succession: count the three white king moves and two black replies. The pawns restrict Black's useful routes, making the difference in available waiting moves meaningful. This idea is not a license to walk a triangle in any ending. You must show that the opponent cannot use the extra time to capture a pawn, escape, make a pawn break or choose a better route.
""", [
        step(custom({'e5': 'K', 'g6': 'P', 'f5': 'P', 'e7': 'k', 'g7': 'p'}), 'White can use the triangle e5–d5–e4 while Black’s useful king routes are restricted by the pawns.'),
        step(custom({'e5': 'K', 'g6': 'P', 'f5': 'P', 'e7': 'k', 'g7': 'p'}), 'Your turn: Begin the king triangle by stepping to d5 without moving a pawn.'),
    ], 'Begin the king triangle by stepping to d5 without moving a pawn.', [
        ('Kd5', True, 'In the worked defence Kf6, Ke4 Ke7, Ke5 returns to the starting board with Black to move.'),
        ('f6+', False, 'This changes the pawn structure and does not begin the requested king triangulation.'),
        ('Kf4', False, 'This is not the d5–e4 triangle demonstrated in the lesson; do not assume any king circuit gains a tempo.'),
    ]),
    lesson(3, 'purposeful-exchanges', 'Ask what an exchange changes', """
An exchange can do more than remove equal point values. It may damage pawn structure, remove a defender, open or close a line, simplify a winning ending or eliminate a dangerous active piece. A sacrifice differs because you deliberately give more material than you immediately receive, expecting another benefit.
In the opening position here Bxc6 exchanges a bishop for a knight. After dxc6, Black has doubled c-pawns and a newly opened d-file for the queen, but also retains both bishops. White has changed the character of the position, not won a piece. Do not conclude that doubled pawns alone decide the game or that e5 is automatically free because its knight defender vanished. Black may have tactical replies to Nxe5. The useful question before any trade is: what remains, which lines open, which pawns become weak and whose pieces benefit? Compare that resulting position with a retreat such as Ba4 before deciding whether the exchange fits your plan.
""", [
        step(after(["e4", "e5", "Nf3", "Nc6", "Bb5", "a6"]), 'The bishop can exchange for the c6-knight, changing Black’s pawn structure if the d-pawn recaptures.'),
        step(after(["e4", "e5", "Nf3", "Nc6", "Bb5", "a6"]), 'Your turn: Exchange the bishop for the c6-knight, then examine the structural consequences.'),
    ], 'Exchange the bishop for the c6-knight, then examine the structural consequences.', [
        ('Bxc6', True, 'The exchange gives up bishop for knight. After dxc6 Black has doubled c-pawns and the bishop pair; assess both.'),
        ('Ba4', False, 'This is a reasonable retreat in a game, but the exercise requests the exchange on c6.'),
        ('O-O', False, 'Castling is also a normal developing move, but does not perform the requested structural exchange.'),
    ]),
    lesson(3, 'chapter3-practice', 'Mixed practice: calculate before naming the motif', """
In a real game nobody announces which tactical theme is available. Begin with the position: identify checks, captures, threats, loose pieces and restricted king squares. Then calculate the opponent's best replies. Naming the motif afterwards helps you remember it, but the name does not prove a move works.
Here Black has just developed a knight to f6 and attacked the white queen on h5. Moving the queen to safety is natural, but White has a stronger reply: Qxf7 is checkmate. The bishop on c4 protects the queen, Black's own pieces obstruct escape and no interposition can stop an adjacent queen check. This combines coordination, a forcing capture, king restriction and attention to the opponent's threat. If Black had played g6 one move earlier, the mating diagonal would have been blocked and White would need a different plan. Compare those positions carefully so that a remembered pattern does not become an automatic, unsound move.
""", [
        step(after(["e4", "e5", "Bc4", "Nc6", "Qh5", "Nf6"]), 'The knight attacks the queen, but an immediate mating capture is stronger than a retreat.'),
        step(after(["e4", "e5", "Bc4", "Nc6", "Qh5", "Nf6"]), 'Your turn: Find checkmate in one, even though your queen is attacked.'),
    ], 'Find checkmate in one, even though your queen is attacked.', [
        ('Qxf7#', True, 'The protected queen gives an adjacent check. The king cannot capture her, escape or block.'),
        ('Qf3', False, 'This saves the queen, but misses the immediate checkmate available on f7.'),
        ('Qh3', False, 'This retreats from the knight but misses mate in one.'),
    ], objective='checkmate'),
]
