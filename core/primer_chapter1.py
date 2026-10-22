"""Chapter 1: the rules, written for ChessBot."""

import chess

from core.primer_build import after, custom, lesson, step

GREEN = "#1B7F4E"
RED = "#C0392B"
START = chess.STARTING_FEN

LESSONS = [
    lesson(1, "board-setup", "The board and the armies", """
The board has 64 squares, eight along each side. Turn it so the corner at White's right hand is light. Black's right-hand corner is light as well. A dark square in White's right-hand corner means the board is backwards, and later lessons about bishops and colors will be looking at the wrong board.
Each army has one king, one queen, two rooks, two bishops, two knights, and eight pawns. White's pieces stand on rank 1 and the pawns on rank 2. Black's pieces stand on rank 8 and the pawns on rank 7. Rooks start in the corners, knights beside them, bishops beside the knights. The queen starts on her own color: White's queen on light d1, Black's queen on dark d8. The king takes the remaining center square, e1 or e8. That arrangement is the only starting position.
""", [
        step(START, "White is at the bottom. The light corner beside White's right-hand rook is h1."),
        step(START, "Queens stand on d1 and d8. Kings stand on e1 and e8. Each queen is on a square of her own color.", (("d1", "d8", GREEN), ("e1", "e8", RED))),
    ], "The board is set and White moves first. Advance the pawn that starts in front of White's king by two squares.", [
        ("e4", True, "The king starts on e1, so the pawn in front of him is the e-pawn. Its first move may be one square or two, and e4 uses the two-square step."),
        ("a4", False, "a4 moves the a-pawn, which starts in front of the queenside rook, not in front of the king."),
        ("Nf3", False, "Nf3 moves the king's knight. The piece that starts on the king's file is the e-pawn."),
    ]),
    lesson(1, "object-checkmate", "The object of the game", """
Chess is won by checkmate, not by collecting the most pieces. Checkmate means the king is attacked and none of the three answers works. The king cannot move to a safe square, no friendly piece can capture the attacker, and nothing can be placed between the attacker and the king. The mated king is not taken off the board. The attack itself ends the game.
Captures matter because they strip away defenders, but a captured queen is not mate while the king can still escape. A larger army can also fail to win if the game ends in a draw. On every move, keep the object in sight: are you building an attack on the king, or only taking pieces with no way to finish?
""", [
        step(after(["e4", "e5", "Qh5", "Nc6", "Bc4"]), "The queen on h5 and the bishop on c4 both aim at the pawn on f7, the weak point in front of the uncastled king.", (("h5", "f7", RED), ("c4", "f7", GREEN))),
        step(after(["e4", "e5", "Qh5", "Nc6", "Bc4", "Nf6"]), "Black moved a knight and left f7 to White. The queen can capture there, and the bishop protects her."),
    ], "Checkmate the black king. Taking a different pawn does not finish the game.", [
        ("Qxf7#", True, "The queen captures the pawn on f7 and gives check. The bishop on c4 protects her, so the king cannot take the queen. No capture, block, or flight square saves the king."),
        ("Qxe5+", False, "The queen takes the pawn on e5 and gives check along the file, but the king is not mated. Black can answer the check and play on."),
        ("Bxf7+", False, "The bishop takes on f7 with check, and the queen protects the bishop. The king can still leave e8, so this check is not mate."),
    ], objective="checkmate"),
    lesson(1, "ranks-files-colors", "Ranks, files, and colors", """
Both players use the same names for the squares. Files are the columns, lettered a to h from White's left to White's right. Ranks are the rows, numbered 1 to 8 starting at White's side. White's back row is rank 1. Black's back row is rank 8, even though it is the nearest row from Black's chair. Calling it Black's first rank during a game confuses the numbers.
Light and dark squares alternate. The a1 square is dark, so h1 is light. A file is a straight road from rank 1 to rank 8. A rank is a straight road from the a-file to the h-file. Rooks need those roads. A bishop is stuck on one color for the whole game: the bishop from c1 never reaches a light square, and the bishop from f1 never reaches a dark square.
""", [
        step(START, "The a-file is White's left edge and the h-file is White's right edge. Rank 1 is the bottom row.", (("a1", "a8", GREEN), ("a1", "h1", RED))),
        step(after(["e4", "e5"]), "Both e-pawns have stepped forward, so the light-squared bishop on f1 can see along the diagonal toward c4."),
    ], "Move the light-squared bishop from f1 to c4.", [
        ("Bc4", True, "The bishop that starts on f1 lives on light squares. After the e-pawn moves, c4 is a legal square on that bishop's diagonal."),
        ("Nc3", False, "Nc3 moves the queen's knight from b1. It is not the light-squared bishop."),
        ("a3", False, "a3 steps the a-pawn one square. The light-squared bishop is the piece on f1."),
    ]),
    lesson(1, "square-names", "Naming a square", """
Every square has one name, made from its file letter and its rank number. The square under White's king's knight is g1: the g-file and the first rank. The square two steps up that file and one step toward the center is f3. You read the letter first, then the number: f3, not 3f.
Name a square before you move a piece to it. That habit stops you from pointing at "that one" and playing a different move. The same name is used by both players and by every scoresheet. g1 is g1 from Black's side of the board too. The letter comes from the file, counting from White's left, and the number comes from the rank, counting from White's side.
""", [
        step(START, "The king's knight starts on g1. The file letters run a to h along the bottom, and the rank numbers run 1 to 8 up the side."),
        step(START, "f3 is one file toward the center and two ranks forward from g1. That square is the knight's most common first jump.", (("g1", "f3", GREEN),)),
    ], "Move the king's knight to the square named f3.", [
        ("Nf3", True, "The knight on g1 moves to f3. The name f3 means the f-file and the third rank."),
        ("Nh3", False, "Nh3 is a knight jump from g1, but the square is h3, on the edge, not f3."),
        ("Nc3", False, "Nc3 moves the other knight, from b1. The square in the question is f3, which belongs to the knight on g1."),
    ]),
    lesson(1, "recording-a-position", "Recording a position", """
A position can be written down without a picture. First say whose turn it is. Then list each piece with the square it stands on. A short record of the starting position begins: White to move; White king e1, queen d1, rooks a1 and h1, knights b1 and g1, bishops c1 and f1, pawns a2 through h2. Black's pieces mirror them on ranks 7 and 8.
A move note records a change to a position, rather than replacing the complete piece list. Write the piece that moves, the square it leaves, and the square it lands on. "White rook, a1 to d1" tells you that change, but you still need the existing board to know whether the path is clear and the king stays safe. Update the moving piece, remove any captured enemy, and switch the player to move before reading the next note.
""", [
        step(custom({"e1": "K", "a1": "R", "e8": "k"}), "White's king is on e1 and the rook is on a1. Black's king is on e8. It is White to move."),
        step(custom({"e1": "K", "a1": "R", "e8": "k"}), "The note for the next move names one piece and one landing square: rook from a1 to d1.", (("a1", "d1", GREEN),)),
    ], "The written note says: White rook from a1 to d1. Play that move.", [
        ("Rd1", True, "The rook travels along rank 1 from a1 to d1. The squares b1 and c1 are empty, so the road is clear."),
        ("Ra4", False, "Ra4 moves the rook, but the note named d1, not a4. A recorded move has one landing square."),
        ("Ke2", False, "Ke2 moves the king. The note named the rook."),
    ]),
    lesson(1, "order-of-play", "Whose turn it is", """
White always makes the first move of the game. After that, the players alternate. An ordinary move moves or captures with one piece; castling, taught later, moves king and rook together during one turn. You do not get a second move because the first one was a pawn, and you may not move a black piece on White's turn.
A move is required when it is your turn. You can never skip a turn. If you have no legal move and are not in check, the game ends as a draw called stalemate; you do not pass and continue. In ordinary play, touching a piece and then wanting to move a different one is settled by the practical rule used in serious games: if you touch your own piece, you move it, provided it has a legal move. For learning, the rule to practice is simpler. Decide the move, play exactly one, then stop and look at the opponent's reply.
""", [
        step(START, "It is White's turn. Every white piece is still on its home square, and Black must wait."),
        step(START, "One move will change one white piece. Black's army does not move on this turn."),
    ], "It is White's turn. Move the king's pawn one square forward, not two.", [
        ("e3", True, "e3 is one move: the e-pawn advances a single square. White's turn is then over, and Black would move next."),
        ("e4", False, "e4 is still only one move, but it advances the pawn two squares. This question asked for the one-square step."),
        ("Nf3", False, "Nf3 is one white move, but it moves the knight. The question asked for the king's pawn."),
    ]),
    lesson(1, "how-a-capture-works", "How a capture works", """
An ordinary capture is a move onto a square occupied by an enemy piece; the later en-passant lesson gives one precise exception. The enemy piece is removed, and your piece stands on that square. Even a knight captures only the piece on its landing square; it never captures a piece it jumps over. You never capture your own piece. Two pieces cannot share a square.
The captured piece leaves the board at once. It does not get a rescue move. If another enemy piece can legally take your piece on the next turn, the capture may be a trade rather than a gain. Before you capture, name the piece you are taking and ask what can take you back. If nothing can take you back, you have won that piece. If something can, compare the values before you grab.
""", [
        step(custom({"g1": "K", "e1": "R", "e5": "p", "a8": "k"}), "The white rook on e1 looks up the open e-file at the black pawn on e5.", (("e1", "e5", GREEN),)),
        step(custom({"g1": "K", "e1": "R", "e5": "p", "a8": "k"}), "A capture would remove the pawn and leave the rook standing on e5. The pawn would be off the board."),
    ], "Capture the black pawn with the rook.", [
        ("Rxe5", True, "The rook moves to e5 and the pawn is removed. Nothing protects that pawn, so Black cannot take the rook back."),
        ("Re4", False, "Re4 moves the rook up the file, but e4 is empty. A capture has to land on the enemy piece."),
        ("Ra1+", False, "Ra1 moves the rook sideways along the first rank. The black pawn is still on e5."),
    ]),
    lesson(1, "rook", "The rook", """
A rook moves any number of squares along a rank or a file, forward, backward, or sideways. It cannot jump over a piece. If a friendly piece stands in the way, the rook stops before that square. If an enemy piece stands in the way, the rook may capture it and must stop there.
On an otherwise empty board a rook can reach fourteen squares from any square, including a corner. In a crowded starting position it cannot move at all, because its own pawns and pieces block every road. Rooks become active on clear ranks and files. An open file has no pawns of either color, although pieces can still block it. Two rooks with a clear line between them on a file protect each other and can coordinate against targets.
""", [
        step(custom({"e1": "K", "a4": "R", "e8": "k"}), "The rook on a4 can travel the whole fourth rank, or the whole a-file, until it meets a piece.", (("a4", "h4", GREEN), ("a4", "a8", RED))),
        step(custom({"e1": "K", "a4": "R", "e8": "k"}), "a8 is the far end of the rook's file. The squares between a4 and a8 are empty, so the rook may go there in one move."),
    ], "Move the rook from a4 to a8.", [
        ("Ra8+", True, "The rook uses the open a-file and lands on a8, giving check to the king on e8 along the eighth rank."),
        ("Rh4", False, "Rh4 is a legal rook move, but it travels along the rank to h4. The question asked for a8, at the end of the file."),
        ("Ke2", False, "Ke2 moves the king. The rook is the piece with the long straight move."),
    ]),
    lesson(1, "bishop", "The bishop", """
A bishop moves any number of squares diagonally and cannot jump. Each bishop is locked to one color. The bishop that starts on c1 always stays on dark squares. The bishop that starts on f1 always stays on light squares. No later move can change that, so a bishop that is blocked by its own pawns on its color can sit useless for a long time.
On an empty board a central bishop reaches more squares than a corner bishop because more diagonal arms are available. Two bishops, one on each color, can eventually reach both colors; they do not attack every square at once. One bishop always leaves the other color unattacked, which is why a lone bishop cannot control every escape square around an enemy king.
""", [
        step(custom({"e1": "K", "c1": "B", "e8": "k"}), "This is the dark-squared bishop. Every square it can reach from c1, such as a3 and h6, is dark.", (("c1", "h6", GREEN), ("c1", "a3", RED))),
        step(custom({"e1": "K", "c1": "B", "e8": "k"}), "h6 is the far end of the long diagonal. The bishop cannot be sent to a light square on this or any later move."),
    ], "Movement drill: move the dark-squared bishop from c1 to h6. A real game with only these pieces would already be drawn; this board isolates the bishop's movement.", [
        ("Bh6", True, "The bishop travels on the dark diagonal c1, d2, e3, f4, g5, and h6. All of those squares are dark."),
        ("Ba3", False, "Ba3 is a legal diagonal move, but it is the short diagonal toward a3, not the long one to h6."),
        ("Ke2", False, "Ke2 moves the king. A king steps one square, while this bishop can cross the board in one move."),
    ]),
    lesson(1, "queen", "The queen", """
The queen combines the rook and the bishop. She moves any number of squares along a rank, a file, or a diagonal, and she cannot jump. She does not move like a knight. One queen move uses only one of those directions: she cannot turn a corner in the middle of the move.
Because she has both the rook's roads and the bishop's diagonals, she is the most mobile piece. She is also a target. If the queen comes out while the other pieces are still on their home squares, the opponent can attack her and gain time by developing. Use the queen's reach when a file or diagonal is open, and do not send her on an errand one piece can do.
""", [
        step(custom({"e1": "K", "d1": "Q", "e8": "k"}), "From d1 the queen can choose the d-file, the first rank, or a diagonal. One move uses only one of those roads.", (("d1", "d8", GREEN), ("d1", "h5", RED))),
        step(custom({"e1": "K", "d1": "Q", "e8": "k"}), "d8 is straight up the file. The queen stops at the end of the chosen direction and does not continue around a corner."),
    ], "Move the queen straight up the d-file to d8.", [
        ("Qd8+", True, "The queen uses the open d-file and lands on d8, next to the black king, so the move is check."),
        ("Qh5+", False, "Qh5 is a legal queen move along the diagonal. The question asked for the file move to d8."),
        ("Qa4+", False, "Qa4 travels diagonally from d1 through c2 and b3 to a4, giving check. The d-file is the road from d1 to d8."),
    ]),
    lesson(1, "knight", "The knight", """
The knight moves in an L: two squares in one direction and then one square to the side. It is the only piece that jumps. Pieces standing between the knight and its landing square do not block it. The knight captures only on the square where it lands, not on the squares it jumps over.
From a center square a knight has eight possible jumps. From a corner it has two. Each jump changes the color of the square the knight stands on. A knight on a dark square moves to a light square, and the next jump returns it to dark. That color change is a useful check: if a knight is not attacking the square you care about, it may be on the wrong color for that job.
""", [
        step(START, "The king's knight starts on g1, a dark square. In the starting position it can jump to f3 or h3. Its own pawn occupies e2, so that jump is not available yet.", (("g1", "f3", GREEN), ("g1", "h3", RED))),
        step(START, "f3 is two squares up and one square toward the center. The pawns on g2 and f2 do not block a knight, because a knight jumps."),
    ], "Jump the king's knight to f3.", [
        ("Nf3", True, "From g1, f3 is two ranks forward and one file toward the center. The knight changes from a dark square to a light square."),
        ("Nh3", False, "Nh3 is a knight jump from g1, but it lands on the h-file at the edge. The center jump from this square is f3."),
        ("Nc3", False, "Nc3 jumps the queen's knight from b1. The king's knight is the piece on g1."),
    ]),
    lesson(1, "king", "The king", """
The king moves one square in any direction: rank, file, or diagonal. He cannot jump. He also may not move to a square attacked by an enemy piece, and he may not stand next to the enemy king. Those two bans are why a king move that looks short can still be illegal.
In the opening the king usually needs shelter rather than an early march into the attack. He is the piece you must keep safe, because mate ends the game. Later, when few pieces remain, the king becomes a strong helper and should walk toward the action. Castling, taught in its own lesson, is the one king move that travels two squares. Every ordinary king move is a single step. If you want the king two squares up the board, that takes two separate turns.
""", [
        step(custom({"e4": "K", "e6": "k"}), "These kings are two squares apart. The white king may not step to e5, because kings are not allowed to touch.", (("e4", "e5", RED),)),
        step(custom({"e1": "K", "e8": "k"}), "The white king on e1 can step to d1, d2, e2, f1, or f2. He cannot leap to e3 in one move.", (("e1", "e2", GREEN),)),
    ], "Movement drill: move the white king one square straight forward. A real game with only the kings is already drawn; here you are practising the movement rule.", [
        ("Ke2", True, "Ke2 is one square up the e-file. The black king on e8 is far enough away that the kings do not touch."),
        ("Kd2", False, "Kd2 is one square, but it is diagonal, not straight forward. Straight forward from e1 is e2."),
        ("Kf1", False, "Kf1 slides the king along the first rank. The forward step is e2."),
    ]),
    lesson(1, "attack-defence", "Attack and defence", """
An attack follows a piece's movement and the blockers on its line. A pawn attacks the two squares diagonally in front of it, not the square it moves to. For ordinary exchanges, check whether a defender can legally recapture: a piece pinned to its king may be unable to do so. King safety has a special rule: even a pinned piece still attacks its usual squares, so the enemy king may not enter them.
To defend a piece, you either move it, put another piece where it can legally recapture, capture the attacker, or block a sliding attack. "It is defended" means that if the opponent takes it, you can take back. Before you leave a piece on a square, ask what attacks that square and what can recapture there. A piece with no defender and an attacker on it is loose, and loose pieces are how beginners lose material.
""", [
        step(custom({"g1": "K", "e1": "R", "f3": "B", "e4": "p", "a8": "k"}), "The rook attacks the pawn on e4 along the file. The bishop on f3 also attacks e4, so the bishop can defend a rook that lands there.", (("e1", "e4", GREEN), ("f3", "e4", RED))),
        step(custom({"g1": "K", "e1": "R", "f3": "B", "e4": "p", "a8": "k"}), "If the rook captures on e4, the bishop still attacks that square. Black's king is too far away to take the rook."),
    ], "Capture the pawn with the rook. The bishop will defend the rook on e4.", [
        ("Rxe4", True, "The rook takes the pawn. The bishop on f3 attacks e4, so the rook is defended after the capture."),
        ("Bxe4+", False, "The bishop can take the pawn, but then the rook is not the piece doing the capturing. The question asked for the rook, with the bishop left as the defender."),
        ("Re3", False, "Re3 moves the rook to an empty square. The pawn on e4 is not captured, and no defence has been shown."),
    ]),
    lesson(1, "exchanges", "Exchanges", """
An exchange is a capture followed by a recapture, or any trade of pieces. If you take a knight and the opponent takes your knight, neither side has gained material; the changed position may still favor one player. If you gain a rook and lose a bishop or knight in return, you have won the exchange. If the opponent cannot recapture at all, you have won a whole rook instead. Players use that name for a rook against a minor piece, because the rook is the stronger piece.
Do not trade just because a capture is legal. First compare what each player loses, then examine the resulting position. A trade can also serve a concrete aim such as removing an attacker or reaching a favorable endgame. Winning the exchange, a bishop or knight for a rook, is a real advantage. Giving up a rook for a bishop is a material sacrifice; it needs concrete compensation such as an attack, passed pawns, or a saving draw, rather than an automatic rule that it is always wrong.
""", [
        step(custom({"e1": "K", "a2": "B", "h8": "k", "g8": "r"}), "The bishop on a2 looks along the long diagonal at the black rook on g8.", (("a2", "g8", GREEN),)),
        step(custom({"e1": "K", "a2": "B", "h8": "k", "g8": "r"}), "After Bxg8 the black king can recapture with Kxg8. White then loses a bishop but Black loses a rook: White wins the exchange."),
    ], "Win the exchange: capture the rook with the bishop.", [
        ("Bxg8", True, "The bishop captures the rook on g8. After Kxg8 White has given a bishop for a rook, winning the exchange. Count both captures, not only the first."),
        ("Bb3", False, "Bb3 moves the bishop along the diagonal but does not capture. The rook remains on g8."),
        ("Ke2", False, "Ke2 moves the king and leaves the rook untouched. No exchange has happened."),
    ]),
    lesson(1, "pawn-move", "The pawn's move", """
A pawn moves forward only, one square at a time. From its starting square it may instead move two squares, provided both squares are empty. It never moves backward or sideways. It captures on the diagonal one square forward, not on the square directly in front of it. An enemy piece blocking the pawn's nose stops the pawn. An enemy piece on the diagonal can be captured.
Because pawns cannot retreat, a pawn move is a small commitment. Pushing several pawns creates holes behind them. In the opening, the useful pawn moves are the ones that claim a share of the center or open a road for a bishop. A pawn that reaches the far rank promotes, which is a separate lesson, and a pawn may also capture en passant, also taught separately.
""", [
        step(custom({"e1": "K", "e4": "P", "d5": "p", "f5": "p", "a8": "k"}), "The white pawn on e4 can step to e5, or capture diagonally on d5 or f5. It cannot capture straight ahead.", (("e4", "d5", GREEN), ("e4", "f5", RED), ("e4", "e5", "#1A5276"))),
        step(custom({"e1": "K", "e4": "P", "d5": "p", "f5": "p", "a8": "k"}), "d5 holds a black pawn. The white pawn attacks that square even though it could not move there without capturing."),
    ], "Capture the black pawn on d5. A pawn captures diagonally.", [
        ("exd5", True, "The pawn moves from e4 to d5 and removes the black pawn. That is a diagonal capture, the only way a pawn takes a piece."),
        ("e5", False, "e5 is the straight forward move. The pawn does not capture the piece in front of it, and d5 is not in front of it anyway."),
        ("exf5", False, "exf5 is a legal pawn capture, but it takes the pawn on f5. The question asked for the pawn on d5."),
    ]),
    lesson(1, "en-passant", "Capturing en passant", """
En passant is a special pawn capture. It can happen only when an enemy pawn uses its two-square first move and lands beside your pawn. Your pawn must already be on the fifth rank, which is rank 5 for White and rank 4 for Black. On the very next move, and not later, your pawn may capture as if the enemy pawn had moved only one square. You move diagonally to that empty square, and the pawn that jumped is removed.
The capture is optional, but the opportunity lasts for only this immediate reply. If you play any other move, the right to capture en passant is gone. The captured pawn is the one that just jumped, not a piece standing on the square you land on. That landing square was empty. This rule exists so a pawn cannot sneak past an opposing pawn by using the double step.
""", [
        step(after(["e4", "a6", "e5"]), "White's pawn has reached the fifth rank. Black's d-pawn is still on d7 and may try to step two squares past it."),
        step(after(["e4", "a6", "e5", "d5"]), "Black played d5, using the two-square step, and landed beside the white pawn. White may capture en passant now or lose the chance.", (("e5", "d6", GREEN),)),
    ], "Capture the pawn that just moved two squares. Take it en passant.", [
        ("exd6", True, "The white pawn moves from e5 to d6, and the black pawn on d5 is removed. White captured as if that pawn had stopped on d6."),
        ("e6", False, "e6 pushes the pawn straight ahead. The black pawn on d5 stays on the board, and the en passant chance disappears."),
        ("a4", False, "a4 moves a different pawn. Any move other than the en passant capture gives up the right to take the d5 pawn that way."),
    ]),
    lesson(1, "promotion", "Pawn promotion", """
A pawn that reaches the last rank is promoted. White promotes on rank 8. Black promotes on rank 1. The pawn is replaced, on the same move, by a queen, rook, bishop, or knight. It cannot stay a pawn and it cannot become a king. The new piece works immediately, so a promotion can give check on the same turn.
A queen is normally best, but examine the resulting position. Underpromotion can avoid stalemate or achieve a particular tactical purpose; a knight check is one common example. Promoting to a rook, bishop, or knight on purpose is called underpromotion. It is legal and sometimes necessary, but it is the exception. When the promotion square is safe and the queen does useful work, take the queen. A pawn move that reaches the last rank without naming the new piece is not finished.
""", [
        step(custom({"g1": "K", "e7": "P", "a8": "k"}), "The white pawn on e7 is one step from the last rank. The square e8 is empty, so the pawn can promote on this move.", (("e7", "e8", GREEN),)),
        step(custom({"g1": "K", "e7": "P", "a8": "k"}), "On e8 the pawn must become another piece at once. A queen on e8 would attack the black king along the eighth rank."),
    ], "Promote the pawn to a queen.", [
        ("e8=Q+", True, "The pawn reaches e8 and becomes a queen. She gives check along the eighth rank. Nothing required an underpromotion here."),
        ("e8=R+", False, "A rook on e8 also gives check, but it does not gain the queen's diagonals. With a free promotion and no stalemate, choose the queen."),
        ("e8=N", False, "A knight is a legal promotion, and from e8 it does not even attack the king on a8. The queen does."),
    ]),
    lesson(1, "check", "Check", """
Check means the king is attacked. You must answer it before you do anything else. There are exactly three answers. Move the king to a square that is not attacked. Capture the piece that gives check. Or put one of your own pieces between the attacker and the king, which works only against a rook, bishop, or queen, because a knight jumps and a pawn checks from the next square.
A check from two pieces at once is double check. The only answer then is a king move, because one move cannot capture both attackers or block both lines. Ignoring a check and making a different move is illegal. When you are the one giving check, remember that the opponent's next move is forced to deal with it, which is why a check can gain time.
""", [
        step(custom({"e1": "K", "a2": "Q", "a1": "r", "h8": "k"}), "The black rook on a1 checks the white king along the first rank. The queen on a2 can capture that rook or step onto the line.", (("a1", "e1", RED), ("a2", "a1", GREEN))),
        step(custom({"e1": "K", "a2": "Q", "a1": "r", "h8": "k"}), "Capturing the checking piece is one of the three answers. Blocking and moving the king are the other two."),
    ], "Answer the check by capturing the rook that gives it.", [
        ("Qxa1+", True, "The queen captures the rook on a1. The check disappears because the attacker has left the board."),
        ("Qb1", False, "Qb1 blocks the first rank, so it is a legal answer to check, but the rook is still on a1. The question asked for the capture."),
        ("Ke2", False, "Ke2 walks the king off the checked rank. That also answers the check, but it lets the rook stay on the board."),
    ]),
    lesson(1, "mate", "Checkmate", """
Checkmate is a check that cannot be answered. Apply the three checks in order. Can the king move to a safe square? Can the attacker be captured? Can the line be blocked? If every answer is no, the position is mate and the game is over. Look at the king's neighboring squares one by one. A square occupied by his own piece does not count as an escape. A square attacked by you does not count either, even if it looks empty.
Mate on the edge of the board is common because the edge already takes away flight squares. A check in the center often leaves the king several ways out, so it is only a check. Calling out check is optional. Whether or not anyone announces it, a check must be answered; claim mate only after all three kinds of defence have failed.
""", [
        step(custom({"e6": "K", "h1": "R", "e8": "k"}), "The black king is on the edge. A rook check along the eighth rank would leave him little room, because the white king on e6 controls d7, e7, and f7.", (("h1", "h8", GREEN),)),
        step(custom({"e6": "K", "h1": "R", "e8": "k"}), "The rook can reach h8 in one move. From there it checks along rank 8. The king on e8 is too far away to capture it, and the white king covers the three seventh-rank flights."),
    ], "Checkmate the black king with the rook.", [
        ("Rh8#", True, "The rook checks along rank 8, covering d8 and f8. The white king on e6 covers d7, e7, and f7. The black king cannot reach the rook on h8, and has no piece to capture or block: checkmate."),
        ("Rh7", False, "Rh7 controls rank 7 but does not attack the king on e8. Black can play Kd8 or Kf8. Restricting the king without checking is not mate."),
        ("Kf5", False, "Kf5 moves the white king and does not check. Mate requires an attack on the king that cannot be answered."),
    ], objective="checkmate"),
    lesson(1, "draw", "Drawn games", """
Not every game ends in mate. The players may agree a draw. A position where neither side has enough material to mate is also drawn: king against king, king and bishop against king, and king and knight against king cannot produce any legal mate, even with cooperation. Two knights against a lone king cannot force mate either, though a mate position exists if the defender blunders into it.
A draw is a result, not a failure to finish the scoresheet. If you are lost, a draw saves half a point. If you are winning, do not agree a draw from habit. Threefold repetition and fifty moves by each side without a pawn move or capture also support draw claims; the detailed guide explains those conditions and their modern automatic counterparts. In a king-against-king position there is nothing left to attack with, so walking the king around cannot create a mate. Learn to recognize a dead position so you do not sit there hunting a mate that the pieces cannot deliver.
""", [
        step(custom({"e1": "K", "e8": "k"}), "Only the two kings remain. Neither can attack the other without stepping next to him, which is illegal, so mate is impossible."),
        step(custom({"e1": "K", "e8": "k"}), "White can still move. This is a movement illustration only: a real game with only these kings has already ended as a draw, so further play is unnecessary."),
    ], "For this movement illustration, move the white king one square forward. In a real game the king-only position is already drawn.", [
        ("Ke2", True, "The king steps to e2. Black's king is not in check, both kings remain, and no mate can ever appear from this material."),
        ("Kd2", False, "Kd2 is legal, but it is a diagonal step. The forward square from e1 is e2. The result would still be a draw."),
        ("Kf2", False, "Kf2 is also a king step, diagonally the other way. Straight forward is e2, and the material remains a draw."),
    ]),
    lesson(1, "perpetual-check", "Perpetual check", """
Perpetual check is a series of checks the opponent cannot stop. The usual end is a draw by threefold repetition: the same position, with the same player to move and the same rights, comes up three times. A queen is especially good at this, because she can check from a distance and then return to the first checking square.
Perpetual check is a saving tool when you are behind in material and a winning tool only in the sense that a draw saves you. It is not mate. The king is attacked every move, but he always has an answer, and that answer walks into the next check. Before you rely on it, make sure the king cannot step out of both checking squares, and that your checking piece cannot simply be captured.
""", [
        step(custom({"h1": "K", "h4": "Q", "g3": "P", "h3": "P", "c5": "k", "f2": "q"}, turn="b"), "Black is two pawns behind. The queen can force a repeating check on f1 and f2; White's own pawns restrict his king.", (("f2", "f1", GREEN),)),
        step(custom({"h1": "K", "h4": "Q", "g3": "P", "h3": "P", "c5": "k", "f2": "q"}, turn="b"), "After ...Qf1+ White must play Kh2. Then ...Qf2+ forces Kh1, returning to this same position with Black to move."),
    ], "Black to move. Begin the verified f1–f2 perpetual-check cycle.", [
        ("Qf1+", True, "Qf1+ forces Kh2; Qf2+ then forces Kh1. Black repeats the same position and can claim a draw when the repetition condition is met."),
        ("Qe2", False, "Qe2 is not check. It lets White choose a move instead of forcing the king into the repeating cycle."),
        ("Qh2+", False, "Qh2+ checks, but White can simply capture the unprotected queen with Kxh2. A check that loses its attacker does not force a perpetual."),
    ]),
    lesson(1, "stalemate", "Stalemate", """
Stalemate is a draw. It happens when the player to move is not in check, but every legal move is impossible. The king has no safe square, and no other piece can move either. Because it is not check, it is not mate. Beginners throw away won games by taking the last flight square without giving check.
Before a queen move against a lone king, look at the position as if it will be the opponent's turn. If the king is not in check and has nowhere to go, you have stalemated him and drawn. Leave him one legal move, or give check. A king stuck in the corner is the usual victim: his own edge has already taken half of his squares, so one careless queen move can take the rest.
""", [
        step(custom({"a8": "k", "a6": "K", "c5": "Q"}), "The black king is buried in the corner. Some queen moves from c5 give mate. Others take away his last squares and do not give check, which is stalemate.", (("c5", "a7", GREEN), ("c5", "b6", RED))),
        step(custom({"a8": "k", "a6": "K", "c5": "Q"}), "Qa7 is check, and the white king protects the queen. Qb6 would not check the king on a8, and he would have no move left."),
    ], "Checkmate the king in the corner. Do not stalemate him.", [
        ("Qa7#", True, "The queen checks from a7 and the king on a6 protects her. The corner king has no capture, no block, and no flight square."),
        ("Qb6", False, "Qb6 does not check the king on a8, and it covers a7, b7, and b8. Black has no legal move and is not in check, so this is stalemate, a draw."),
        ("Qe5", False, "Qe5 also leaves the king unchecked and without a move. That is stalemate. The mating square in this position is a7."),
    ], objective="checkmate"),
    lesson(1, "castling", "Castling", """
Castling is the only move that shifts two pieces. The king moves two squares toward a rook, and that rook jumps to the square the king has just crossed. Kingside castling puts the white king on g1 and the rook on f1. Queenside castling puts the king on c1 and the rook on d1. Black's castling uses rank 8 in the same way.
You may castle only if the king and that rook have never moved, the squares between them are empty, the king is not in check, and the king does not pass through or land on an attacked square. The rook is allowed to cross an attacked square. Castling is a king move, so it answers a threat to the king by removing him from the center. It is illegal as a way to get out of check.
""", [
        step(after(["e4", "e5", "Nf3", "Nc6", "Bc4", "Bc5"]), "The king's knight and the light-squared bishop have left the kingside. The king on e1 and the rook on h1 have not moved, so kingside castling is legal.", (("e1", "g1", GREEN), ("h1", "f1", RED))),
        step(after(["e4", "e5", "Nf3", "Nc6", "Bc4", "Bc5"]), "Queenside castling is not available yet: the queen, the dark-squared bishop, and the queen's knight still stand between the king and the a1 rook."),
    ], "Castle kingside.", [
        ("O-O", True, "The king steps from e1 to g1, and the rook comes from h1 to f1. The king was not in check and did not cross an attacked square."),
        ("d3", False, "d3 is a pawn move. The king remains on e1, so this is not castling."),
        ("Nc3", False, "Nc3 develops the queen's knight. Development is useful, but the question asked for kingside castling."),
    ]),
    lesson(1, "algebraic-notation", "Writing the moves", """
Algebraic notation names the landing square. A pawn move is just that square: e4. A piece move puts the piece letter first: Nf3, Bc4, Ra1, Qd8, Ke2. The letters are N for knight, because K is the king, then B, R, Q, and K. A capture adds an x: Rxe5, exd5. Check adds a plus sign. Mate adds a hash. Promotion adds an equals sign and the new piece: e8=Q. Kingside castling is O-O. Queenside castling is O-O-O.
When two identical pieces can reach the same square, add the file or rank that tells them apart, as in Nbd2. The long form e2-e4 is readable, but ordinary scoresheets use the short form. Write the move you played, not the move you meant. The symbol x is only for a capture, never for an ordinary move.
""", [
        step(custom({"g1": "K", "e1": "R", "e5": "p", "a8": "k"}), "The rook can capture the pawn on e5. On a scoresheet that capture is not written Re5. The x has to appear.", (("e1", "e5", GREEN),)),
        step(custom({"g1": "K", "e1": "R", "e5": "p", "a8": "k"}), "Re4 would be a move to an empty square, so it has no x. Rxe5 names the capture."),
    ], "Play the capture that is written Rxe5. The x is the sign for a capture.", [
        ("Rxe5", True, "Rxe5 says a rook captures on e5. The pawn is removed, and the x in the notation is what records that capture."),
        ("Re4", False, "Re4 is a rook move to an empty square. There is no capture, so the notation has no x."),
        ("Ra1+", False, "Ra1 moves the rook along the rank. It neither captures nor lands on e5."),
    ]),
]
