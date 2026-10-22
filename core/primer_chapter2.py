"""Source-mapped chapter two practice: mating methods, draws, and pawn endings."""

from core.primer_build import after, custom, lesson, step

GREEN = "#1B7F4E"
RED = "#C0392B"

QUEEN_START = custom({"e5": "k", "e1": "K", "d2": "Q"})
ROOK_START = custom({"d6": "k", "d4": "K", "a2": "R"})
LADDER_START = custom({"f4": "k", "h1": "K", "a2": "R", "b3": "R"})
BISHOPS_START = custom({"d4": "k", "f2": "K", "b8": "B", "h5": "B"})

LESSONS = [
    lesson(2, "mate-on-the-edge", "Mate happens on the edge", """
A king in the center has eight neighboring squares before other pieces intervene. On an edge he has five, and in a corner only three. The board therefore helps an attacker restrict his escape. Your job is still to account for every actual flight square, the checking piece's safety, and any possible block. The edge alone does not turn a check into mate.
Here the white king on g6 controls f7, g7 and h7. A queen check along the eighth rank then removes the remaining sideways flights. First understand what each white piece contributes; then find the final check. Later lessons show how to drive a king into such a position rather than hoping he arrives there.
""", [
        step(custom({"g8": "k", "g6": "K", "d8": "Q"}, turn="b"), "This is the finished mating picture: the queen covers the eighth rank and the king covers f7, g7 and h7."),
        step(custom({"g8": "k", "g6": "K", "d1": "Q"}), "Now find the move that builds that picture from this position.", (("d1", "d8", GREEN),)),
    ], "Deliver checkmate in one move.", [
        ("Qd8#", True, "The queen checks along the eighth rank; the white king controls every seventh-rank flight."),
        ("Qd5+", False, "This is check, but Kf8 or Kh8 remains legal. A check must close every escape to be mate."),
        ("Qb3+", False, "This diagonal check leaves sideways escapes on the eighth rank. It is not mate."),
    ], objective="checkmate"),
    lesson(2, "queen-mates", "Two queen mating pictures", """
A queen can finish a lone king in two familiar ways. She may check along his edge from a safe distance while her king covers the flight squares in front. Or she may stand directly beside him, protected by her king. The second picture works because the enemy king cannot capture a piece on a defended square. A queen placed beside the king without protection can simply disappear.
In this position both Qd8 and Qg7 give mate. They show the two different pictures, and either answer is accepted. Do not memorize one square as the only right answer. Verify the check, list the king's possible destinations, and identify the piece that forbids each destination.
""", [
        step(custom({"g8": "k", "g6": "K", "g7": "Q"}, turn="b"), "In this close mating pattern, the white king protects the queen on g7. Black cannot capture her."),
        step(custom({"g8": "k", "g6": "K", "d4": "Q"}), "You can build either a protected adjacent mate or a distant rank mate here.", (("d4", "g7", GREEN), ("d4", "d8", GREEN))),
    ], "Checkmate in one. Both queen mating patterns are available.", [
        ("Qd8#", True, "A safe distant check along the eighth rank mates because the white king covers all forward flights."),
        ("Qg7#", True, "The queen checks next to Black's king and is protected by Kg6; every escape is covered."),
        ("Qd5+", False, "A check from d5 leaves Kf8 and Kh8 available. It does not complete either mating picture."),
    ], objective="checkmate"),
    lesson(2, "rook-mates", "The king and rook finish together", """
A rook checks along a rank or file and has no diagonal attack. Against a lone king, its own king normally has to cover the squares in front of the defender. In the standard edge mate, the two kings have one empty rank or file between them, and the rook checks from the side. Kings cannot stand next to each other.
Here Black is in the corner. White's king on g6 covers g7 and h7, while the rook can check along the eighth rank from a8. The rook is many squares away from the enemy king, so it does not need direct protection on a8. Being unprotected is dangerous only when an opponent can actually capture the piece.
""", [
        step(custom({"h8": "k", "g6": "K", "a8": "R"}, turn="b"), "Ra8 is a safe distant check: Black cannot reach the rook, and Kg6 controls both seventh-rank flights."),
        step(custom({"h8": "k", "g6": "K", "a4": "R"}), "Build the final rook mating picture. Check the two possible forward flights before moving.", (("a4", "a8", GREEN),)),
    ], "Deliver checkmate with the rook.", [
        ("Ra8#", True, "The rook controls the eighth rank and Kg6 controls g7 and h7. Black has no legal reply."),
        ("Ra7", False, "The rook cuts off the seventh rank but does not check. Black can still move along the eighth rank."),
        ("Kg5", False, "This removes the king's control of h7 and gives no check. The mating net is not completed."),
    ], objective="checkmate"),
    lesson(2, "two-rook-mates", "Two rooks: the ladder method", """
Two rooks can force mate without help from their king. One rook draws a barrier across a rank, and the other checks on the next rank. The enemy king must move away from the barrier; then the rooks exchange jobs. Repeating this coordinated movement drives him to an edge. The complete worked example includes a quiet sideways move when the king approaches a rook, because checking is less important than keeping both rooks safe.
In the final practice position, Ra7 covers g7 and h7 while the other rook checks from b8. Ra7 does not protect b8: rooks cannot move diagonally. The checking rook is safe because the black king on h8 is far away. Each rook has a separate, necessary job.
""", [
        step(LADDER_START, "Begin with the king in the middle. The rooks will take turns building a barrier and checking."),
        step(after(("Ra4+", "Ke5", "Rb5+", "Kd6", "Ra6+", "Kc7"), LADDER_START), "The rooks have climbed three ranks. Black now approaches a6, so move a rook sideways before continuing."),
        step(custom({"h8": "k", "a7": "R", "b1": "R", "c2": "K"}), "In this separate final exercise, Ra7 covers the seventh rank; the other rook must give the edge check.", (("b1", "b8", GREEN),)),
    ], "Give checkmate with the second rook.", [
        ("Rb8#", True, "Rb8 checks along rank eight. Ra7 covers g7 and h7; it does not need to protect the distant checking rook."),
        ("Ra8+", False, "Black can escape to g7 or h7 because the seventh-rank barrier has disappeared. Black cannot capture a8 from h8."),
        ("Rg1", False, "This covers g8 without checking h8. Together with Ra7 it removes every legal move: stalemate."),
    ], objective="checkmate"),
    lesson(2, "minor-piece-and-pawn-mates", "Bishop, knight and pawn mating patterns", """
A king and a single bishop cannot mate a lone king, and neither can a king and a single knight. This does not mean bishops or knights cannot deliver mate in a larger position. Another piece, a pawn, or the defender's own pieces may close the missing flights. The worked examples show a bishop delivering mate, a smothered knight mate and a pawn delivering mate without promotion.
In this practice position the dark-squared bishop on a7 covers b8. White's king on b6 covers a7 and b7. A knight check from c7 then completes the net. Moving the knight elsewhere without check leaves Black no legal move, so both listed quiet knight moves cause stalemate rather than helping the king escape.
""", [
        step(custom({"a8": "k", "b6": "K", "a7": "B", "c7": "N"}, turn="b"), "The knight checks a8, the dark-squared bishop covers b8, and the white king covers a7 and b7."),
        step(custom({"a8": "k", "b6": "K", "a7": "B", "b5": "N"}), "Find the knight move that checks. A quiet knight move here risks immediate stalemate.", (("b5", "c7", GREEN), ("a7", "b8", GREEN))),
    ], "Deliver checkmate with the knight.", [
        ("Nc7#", True, "The knight checks a8. Ba7 controls b8, and Kb6 controls a7 and b7."),
        ("Nd6", False, "This gives no check, while the bishop and king still cover all Black's flights. It is stalemate."),
        ("Na3", False, "Black is not checked and has no legal move. Moving the knight away produces stalemate."),
    ], objective="checkmate"),
    lesson(2, "mating-method-queen", "A complete king and queen mating method", """
The method has three stages: restrict the enemy king, bring your king into useful contact, and deliver a protected edge mate. A quiet queen move can be excellent when it builds the barrier you need. Repeated checks that let the king return to open space may accomplish very little. The worked line starts with a central defending king and continues through every reply to mate.
As the box becomes small, check for stalemate before each quiet move. The example pauses at a position where one tempting queen move stalemates, while a king move preserves a legal reply and prepares mate. Your aim is safe progress, not checking on every turn. At the final checkpoint below, either of the two listed mating checks succeeds.
""", [
        step(QUEEN_START, "Black begins in the center. Qd7 will fence off the upper board without giving check."),
        step(after(("Qd7", "Ke4", "Kf2", "Ke5", "Kf3", "Kf6", "Kf4", "Kg6", "Qe7", "Kh6"), QUEEN_START), "The king has reached the edge, but Qf7 would stalemate. Kf5 brings support while leaving Kh5 legal."),
        step(after(("Qd7", "Ke4", "Kf2", "Ke5", "Kf3", "Kf6", "Kf4", "Kg6", "Qe7", "Kh6", "Kf5", "Kh5"), QUEEN_START), "The king move has prepared the finish. Find any checkmate from this final checkpoint."),
    ], "Finish the demonstrated queen method with checkmate.", [
        ("Qh7#", True, "The queen checks down the h-file, while Kf5 closes g4, g5 and g6."),
        ("Qg5#", True, "The queen checks beside Black's king and is protected by Kf5. This is another valid finish."),
        ("Qe8+", False, "The diagonal check still allows Kh4. It checks, but it does not complete the mate."),
    ], objective="checkmate"),
    lesson(2, "mating-method-rook", "A complete king and rook mating method", """
A rook can cut a king off, but usually needs its own king to force further retreat. Bring your king opposite the defender with one square between them. A distant rook check then removes the rank on which the defender stands, while your king prevents him moving forward. When he avoids opposition, follow with your king; sometimes move the rook sideways and let him commit first.
The long worked example shows the complete process, including a waiting move, and a second example gives a shorter finish. There is no rule that an unprotected rook on the enemy king's rank is lost: the king must actually be close enough to capture it. Always calculate distance and attacked squares instead of assuming that every check is either good or bad.
""", [
        step(ROOK_START, "The kings are in opposition. A rook check on a6 drives Black back because the fifth-rank flights are controlled."),
        step(after(("Ra6+", "Kd7", "Kc5", "Ke7", "Kd5", "Kf7", "Ke5", "Kg7", "Kf5", "Kh7"), ROOK_START), "White has followed the defender. The guide explains how to regain opposition and why a waiting rook move may be needed."),
        step(custom({"h8": "k", "f7": "K", "g6": "R"}), "In the shorter worked line White has reached this finish. The king covers g7 and g8; the rook must cover the h-file."),
    ], "Finish the rook method with checkmate.", [
        ("Rh6#", True, "Rh6 checks along the h-file; Kf7 covers g7 and g8. Every flight is closed."),
        ("Rg8+", False, "Black can move to h7. The rook is protected, but this is only check, not mate."),
        ("Ke6", False, "The king steps away from the mating job and gives no check. Rh6 mates immediately."),
    ], objective="checkmate"),
    lesson(2, "mating-method-two-bishops", "Two bishops close the diagonals", """
Two bishops on opposite colors can force a lone king into a corner with their king's help. They work as neighboring diagonal barriers. One bishop controls the dark squares, the other the light squares; the king blocks the defender from crossing between them. Coordinated steps make the available region smaller until the last checks force the corner mate.
This is a different task from waving the bishops about independently. The full worked line shows their regrouping, the king's approach, a stalemate danger, and the final checks. For now, learn how the diagonals fit together and verify the final net. Bishop and knight mate requires a different, harder method which the book postpones until later; this two-bishop example does not teach that endgame.
""", [
        step(BISHOPS_START, "The bishops start far apart. They first regroup into diagonal barriers while the king prepares to approach."),
        step(after(("Bf3", "Kd3", "Be5", "Kd2", "Be4", "Kc1"), BISHOPS_START), "Black is nearly boxed in. Ke2 would now stalemate, so the king must approach via e3."),
        step(custom({"h1": "k", "g3": "K", "d4": "B", "d3": "B"}), "Both bishops and the king have reached their final jobs. Find the bishop check that removes the last flights."),
    ], "Checkmate with a bishop.", [
        ("Be4#", True, "Be4 checks h1 and covers h7 along its diagonal; Bd4 covers g1 and Kg3 covers h2 and g2."),
        ("Bc3", False, "This does not check h1. The bishop abandons its role in the finishing arrangement."),
        ("Kf2", False, "This gives no check and leaves h2 available. The final bishop check is ready now."),
    ], objective="checkmate"),
    lesson(2, "avoid-stalemate", "Count the defender's moves", """
Stalemate means the player to move is not in check and has no legal move with any piece. It ends the game as a draw even if the other side has a large material advantage. Against a lone king, inspect each neighboring square; with other pieces present, also ask whether one of those pieces can move.
A won queen ending can become drawn through one careless quiet move. Before restricting the defender further, imagine his next turn. If he has no move, make sure your move gives check; otherwise choose a move that leaves a legal reply. Here Qb6 and Qe5 cause stalemate. Qa7, Qc8 and Qf8 give genuine checkmate, and all are accepted when played on the board.
""", [
        step(custom({"a8": "k", "a6": "K", "b6": "Q"}, turn="b"), "This is stalemate: Black is not checked, and a7, b7 and b8 are all forbidden."),
        step(custom({"a8": "k", "a6": "K", "c5": "Q"}), "Reset before the mistake. Find a checking move that closes every escape instead of merely removing all moves.", (("c5", "a7", GREEN), ("c5", "b6", RED))),
    ], "Deliver checkmate; avoid a quiet stalemate.", [
        ("Qa7#", True, "The queen checks and is protected by Ka6. The king cannot escape, capture or block."),
        ("Qb6", False, "Black is not in check and has no legal move. That ends the game in stalemate."),
        ("Qe5", False, "The queen covers b8 while Ka6 controls a7 and b7. Black is not checked: stalemate."),
    ], objective="checkmate"),
    lesson(2, "two-knights-draw", "Two knights: possible mate, no forced mate", """
A king and two knights can form a checkmate position, but cannot force a lone king into it against correct defence. This is different from king and one knight, where no legal checkmate position against a bare king exists. The defender of a two-knight ending must still avoid voluntarily entering a mating trap.
Here White is in check from the knight on h6. Moving into the corner with Kh8 permits Nef7 mate. Moving away with Kf8 avoids that immediate trap and preserves the theoretical draw. The exercise tests a genuine defensive decision, not an arbitrary improving move in a position where every move draws. Do not confuse having a possible mating pattern with being able to force an unwilling opponent into it.
""", [
        step(custom({"h8": "K", "g6": "k", "h6": "n", "f7": "n"}), "This is the trap after Kh8 and Nef7: the knights check and seal the exits with their king's support."),
        step(custom({"g8": "K", "g6": "k", "h6": "n", "e5": "n"}), "White is checked on g8. Choose the king move that avoids the corner trap."),
    ], "Escape check without allowing a mate on Black's next move.", [
        ("Kf8", True, "The king avoids the corner. Two knights cannot force mate against correct defence from this ending."),
        ("Kh8", False, "Black replies Nef7#. A possible mate becomes real only because the defender enters this corner trap."),
    ]),
    lesson(2, "drawn-material", "Recognize material that cannot mate", """
King against king, king and bishop against king, and king and knight against king are dead positions: no legal sequence can produce checkmate. The game ends in a draw when such a position arises. You do not have to walk your king toward the center, offer a draw, or wait for an opponent to agree. Two knights are different: a mate position can exist, although it cannot be forced against correct defence of a lone king.
Promotion offers a useful way to see the distinction. In this exercise, promoting to a bishop or knight leaves a dead position, while a queen or rook retains the ability to force mate. Choose a drawing promotion to demonstrate the material rule, not because drawing is normally the best goal when you could win.
""", [
        step(custom({"h8": "k", "a1": "K", "e8": "B"}, turn="b"), "The bishop has appeared, but this material cannot mate a bare king. The game is already drawn."),
        step(custom({"h8": "k", "a1": "K", "e7": "P"}), "For this classification exercise, choose a promotion that immediately produces insufficient mating material."),
    ], "Demonstrate a dead draw by promoting to a minor piece.", [
        ("e8=B", True, "King and bishop against king cannot produce checkmate. The game immediately becomes a dead draw."),
        ("e8=N", True, "King and knight against king is also a dead draw. Either minor-piece promotion demonstrates the rule."),
        ("e8=Q+", False, "A queen retains enough material to force mate. It wins with correct play instead of demonstrating the requested draw."),
    ]),
    lesson(2, "active-stalemate", "Use stalemate as a defensive resource", """
Stalemate is not only an accident committed by the stronger side. A defender may deliberately close the attacker's remaining moves and save an otherwise hopeless position. Count the opponent's pawn moves as carefully as his king moves: a blocked pawn may leave him with no move at all.
Here Black's pawn on a2 wants to promote on a1, but Black's own king occupies that square. White can keep that king imprisoned by moving to c1. Black is not in check, cannot move his king, and cannot move the blocked pawn: immediate stalemate. The related wrong-bishop rook-pawn example in the guide shows why extra material can still fail to dislodge a king from the right corner.
""", [
        step(custom({"a1": "k", "a2": "p", "c1": "K"}, turn="b"), "The black pawn is blocked by its own king, and White's king closes b1 and b2. Black is stalemated."),
        step(custom({"a1": "k", "a2": "p", "c2": "K"}), "White can reach that drawing position immediately. Find the move that closes the prison."),
    ], "Force an immediate stalemate for Black.", [
        ("Kc1", True, "Black has no king move, no pawn move, and is not in check. The result is a draw."),
        ("Kd2", False, "This leaves b1 available to the black king, so it does not force stalemate now."),
        ("Kb3", False, "The white king stops guarding b1. Black is able to leave a1, so the immediate drawing resource is missed."),
    ]),
    lesson(2, "queening-a-pawn", "Promotion must preserve the result", """
Promotion means replacing a pawn that reaches the far rank with a queen, rook, bishop or knight of the same color. Against a lone king, a queen or rook normally gives enough material to force mate with your king's help. A single bishop or knight does not. The queen is usually the practical choice because it is stronger, but a rook is also a winning promotion in this position.
Do not assume every promotion is safe. Check whether the new piece can be captured and whether promotion creates stalemate. Here e8 is safe, and both queen and rook promotion give check. The worked example follows the pawn's last steps and explains why choosing a knight would instead turn the game into a dead draw.
""", [
        step(custom({"h8": "k", "a1": "K", "e6": "P"}), "The pawn still needs e7 and e8. Black is too far away to stop those two moves."),
        step(custom({"h8": "k", "a1": "K", "e7": "P"}), "Choose a promotion that retains enough material to force mate against the lone king."),
    ], "Promote while keeping a forced win. A queen or rook both work.", [
        ("e8=Q+", True, "The queen checks from a safe square and can force mate with its king's help."),
        ("e8=R+", True, "The rook also checks safely and can force mate with its king. A queen is stronger, but a rook still wins."),
        ("e8=N", False, "This leaves king and knight against king, a dead draw. Promotion happened, but the win disappeared."),
    ]),
    lesson(2, "king-helps-the-pawn", "The king escorts the pawn", """
When the opposing king can reach a pawn's route, the stronger king must control the squares the pawn needs. Often the king belongs in front of or beside the pawn, clearing a path and preventing capture. This is more than keeping the pawn defended on its current square: the promotion square must eventually be safe too.
Here e7 is defended by Kd6, so Black cannot capture the pawn after it advances. Black's only reply is Kf7, and White then plays Kd7 to protect e8 before promoting. The full sequence matters: a defended pawn on e7 does not mean you should automatically promote if the enemy king can take the new queen. Walking backward with the king in the quiz gives Black time to establish a drawn blockade.
""", [
        step(custom({"e8": "k", "d6": "K", "e5": "P"}), "The king controls e6 and e7. Its job is to protect the pawn's route, not merely follow behind it."),
        step(custom({"e8": "k", "d6": "K", "e6": "P"}), "The pawn has reached e6. Find the protected advance that maintains the win, then study Black's reply in the guide.", (("d6", "e7", GREEN),)),
    ], "Keep the win by advancing to the square your king protects.", [
        ("e7", True, "Kd6 protects e7. After Kf7, play Kd7 before promoting so that e8 is protected too."),
        ("Ke5", False, "Black can answer Ke7 and establish a drawn blockade. The king abandons its advanced escorting position."),
        ("Kc5", False, "Black can play Ke7 and hold the pawn. Moving away surrenders the winning position."),
    ]),
    lesson(2, "pawn-opposition", "Opposition: make the other king give way", """
When kings face each other with one empty square between them, the player who must move usually has to give way. That relationship is called opposition. It is a tool for controlling access to squares, not a magical rule that always wins. Pawn location, board edges, and whose turn it is decide whether gaining opposition matters.
In this defensive exercise White has Kc5 and Pc6; Black's king on c7 must retreat. Kc8 keeps the king directly in front of the pawn. If White then approaches on b6, Black answers Kb8; if White approaches on d6, Black answers Kd8. Retreating sideways too early lets White's king penetrate on the opposite side. Learn the drawing defence as well as the winning technique.
""", [
        step(custom({"c8": "k", "c6": "K", "d6": "P"}), "With White to move, d7+ lets Black blockade on d8. The guide compares this drawn case with a winning advance without check."),
        step(custom({"c7": "k", "c5": "K", "c6": "P"}, turn="b"), "Black must retreat. Choose the square directly in front of the pawn, keeping both defensive replies available."),
    ], "Black to move: preserve the draw by retreating directly in front of the pawn.", [
        ("Kc8", True, "This is the only drawing retreat. Meet Kb6 with Kb8 and Kd6 with Kd8, preserving the blockade."),
        ("Kb8", False, "White plays Kd6, approaching on the opposite side and securing a winning promotion route."),
        ("Kd8", False, "White plays Kb6, taking the opposite side and controlling the pawn's path to promotion."),
    ]),
    lesson(2, "pawn-fifth-rank", "Use the pawn's spare move", """
With a non-rook pawn on the fifth rank and its king securely in front on the sixth, the stronger side can often use the pawn's remaining move as a reserve tempo. First secure the useful king position; then spend the pawn move when it forces the defender to abandon opposition. Pushing immediately can throw away that reserve and reach a drawn sixth-rank position.
Here Kc6 gains opposition against Kc8. When the black king steps aside, White's king goes to the opposite side and clears the promotion route. By contrast, c6 immediately allows Kd8, leaving White's king on d6 with the move and no useful spare pawn tempo. Compare both lines in the guide instead of memorizing that all pawn pushes are good.
""", [
        step(custom({"c8": "k", "c6": "K", "c5": "P"}, turn="b"), "The king has taken opposition first. Black must step aside, allowing White to enter on the opposite side."),
        step(custom({"c8": "k", "d6": "K", "c5": "P"}), "White must choose king improvement before spending the pawn's remaining waiting move."),
    ], "Maintain the win: take opposition with your king before pushing the pawn.", [
        ("Kc6", True, "Black must step to b8 or d8; White then goes to the opposite side and protects the pawn's route."),
        ("c6", False, "After Kd8, the defender has opposition against Kd6. The premature push changes this win into a draw."),
        ("Ke6", False, "The king moves away from the c-pawn. Black can maintain a drawn blockade instead of yielding the route."),
    ]),
    lesson(2, "rook-pawn-draw", "The rook-pawn corner exception", """
A rook pawn is a pawn on the a-file or h-file. If the defending king reaches the corner in front of it and the stronger side cannot force him out, king and rook pawn cannot win. The edge removes the square that would let the stronger king go around the blockade. A seemingly powerful king position may lead only to stalemate or loss of the pawn.
Here Black must choose between h8 and f8. Kh8 reaches the safe corner and draws; Kf8 allows the white king to support promotion. This is a genuine result-changing defensive choice. The guide then shows how White's attempt to push h7 produces a familiar corner blockade. Do not apply ordinary central-pawn winning rules unchanged to an edge pawn.
""", [
        step(custom({"h8": "k", "g6": "K", "h6": "P"}), "The defender has reached the promotion corner. White cannot make the king leave h8 and force the pawn through."),
        step(custom({"g8": "k", "g6": "K", "h6": "P"}, turn="b"), "Black must find the drawing king move now. The correct corner matters more than material."),
    ], "Black to move: enter the promotion corner and draw.", [
        ("Kh8", True, "The corner in front of the h-pawn is the drawing fortress. White cannot force the king out."),
        ("Kf8", False, "White can play h7, bring the king to g7 and promote safely. Moving away from the corner loses."),
    ]),
    lesson(2, "knight-pawn-stalemate", "A knight pawn needs one extra precaution", """
A knight pawn is a pawn on the b-file or g-file. It can win where a rook pawn draws, but the nearby edge creates extra stalemate traps. In this position an immediate g6+ lets the defender retreat to h8 and draw. White instead moves the king to f7, preserving the pawn's spare move and the ability to maneuver.
The worked line reaches Kh8 with White Kf7 and Pg5. Pushing g6 there would stalemate because the black king has no square to the right of the board. White must first reposition the king with Kg6 and Kh6 so that Black can step to g8. Only then does the pawn advance. This is a precise exception, not a reason to fear all g-pawn endings.
""", [
        step(custom({"h8": "k", "f7": "K", "g5": "P"}), "Pushing g6 here would stalemate. White must rearrange the king before spending the pawn move."),
        step(custom({"h7": "k", "f6": "K", "g5": "P"}), "Find the king move that preserves the winning maneuver. A checking pawn push now gives away the win."),
    ], "Keep the win by preparing the pawn advance with your king.", [
        ("Kf7", True, "This prepares Kg6 and Kh6 if Black chooses Kh8, avoiding the stalemate trap before pushing."),
        ("g6+", False, "Black replies Kh8 and draws. Advancing with check here loses the useful spare pawn move."),
        ("Ke6", False, "The king leaves the key winning route. Black can establish a drawn defence."),
    ]),
    lesson(2, "outside-pawn", "Supplement: a pawn can race alone", """
This is an extra pawn-race illustration, rather than a separate topic taught in the chapter's printed pages. A passed pawn has no opposing pawn on its file or an adjacent file ahead of it that can stop or capture it by ordinary pawn play. Whether it can promote also depends on the enemy king and the move order.
Here the kings are far away on the h-file and the a-pawn has a clear route. Advancing it is an easy way to make progress. King moves also preserve the win in this particular position, so they should not be described as losing moves. The exercise asks you to practice a pawn advance; the guide follows the alternating moves until promotion and explains why Black cannot catch the pawn.
""", [
        step(custom({"h8": "k", "h2": "K", "a4": "P"}), "The pawn needs four moves to promote. Black's king needs far more travel to intercept its route."),
        step(custom({"h8": "k", "h2": "K", "a4": "P"}), "Practice the direct pawn advance. Other moves can also win; this task specifically asks you to move the pawn.", (("a4", "a5", GREEN),)),
    ], "Practice moving the passed pawn one square toward promotion.", [
        ("a5", True, "The pawn advances toward a8. The defender remains too far away to catch it."),
        ("Kg3", False, "This also keeps a winning position, but the practice task asks for a pawn move. It is not a losing king move."),
        ("Kg1", False, "This also leaves the pawn able to win. It does not perform the requested pawn advance."),
    ]),
]
