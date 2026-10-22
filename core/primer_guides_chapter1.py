"""Original independent-study teaching for Chapter 1 of the Maizelis syllabus.

Pages refer to the printed book; its PDF page number is one greater.
Worked lines are legal illustrations unless a note explicitly identifies a
forced reply. They are not recommendations for every similar position.
"""

import chess

from core.primer_build import after, custom


def section(title, body):
    return {"title": title, "body": " ".join(body.split())}


def example(title, fen, moves, notes):
    return {"title": title, "fen": fen, "moves": tuple(moves), "notes": tuple(notes)}


def check(check_id, prompt, *options):
    return {"id": check_id, "prompt": prompt, "options": tuple(
        {"text": text, "correct": correct, "explanation": explanation}
        for text, correct, explanation in options
    )}


def guide(pages, goals, sections, examples, pitfalls, checks, recap):
    return dict(pages=pages, goals=tuple(goals), sections=tuple(sections),
                examples=tuple(examples), pitfalls=tuple(pitfalls),
                checks=tuple(checks), recap=tuple(recap))


GUIDES = {
    "board-setup": guide(
        (12, 14),
        ("Set up both armies without a picture.", "Identify each piece and the two wings of the board."),
        (
            section("Build a reliable starting picture", """
                Put a light square at the right-hand corner of each player. From White's seat that corner is h1;
                from Black's seat it is a8. Put a rook in each corner, then a knight beside each rook, then a
                bishop. The two central squares are for king and queen. Use 'queen on her own color': White's
                queen stands on light d1 and Black's on dark d8. Their kings occupy e1 and e8. Finish by putting
                eight pawns in front of each army. Check both sides separately rather than assuming a mirrored
                mistake must be correct.
            """),
            section("Names, symbols, and the wings", """
                The king has a cross in the usual set; the queen has a crown, the rook resembles a tower,
                the bishop has a split head, and the knight a horse's head. Pawns are the eight small soldiers.
                In written moves use K, Q, R, B, and N; the knight uses N because K already belongs to the king.
                Pawn moves normally omit a piece letter. The kingside is the wing toward the starting king's rook,
                the f-, g-, and h-files. The queenside lies toward the a1/a8 rook, especially the a-, b-, and c-files.
                The central d- and e-files connect the two wings.
            """),
            section("How to study a position", """
                Treat the diagram as a board you can investigate. First identify whose turn it is, then name the
                pieces involved. Play the demonstrated moves slowly and explain what changed: a square became
                available, a defender moved, or a king came under attack. Reset and try a different legal move;
                compare the result instead of memorizing an arrow. Study a few positions carefully, pause when
                attention fades, and combine lessons with slower games. Keep the moves of your games and review
                wins as well as losses. A good result does not prove that every decision was sound. The goal here
                is a repeatable way to think, not a race through lesson titles.
            """),
        ),
        (example("Two armies begin developing", chess.STARTING_FEN, ("e4", "e5", "Nf3", "Nc6"), (
            "White moves first. Identify both kings, both queens, and all eight pawns on each side.",
            "White's e-pawn takes central space and opens a diagonal for the f1 bishop.",
            "Black makes the equivalent central advance; Black's forward direction is toward lower rank numbers.",
            "White's g1 knight jumps to f3. A pawn does not have to move before its knight can jump.",
            "Black's b8 knight develops to c6 and defends e5. Both players have made two moves, in alternation.",
        )),),
        ("A board with a dark right-hand corner needs turning before the armies are set up.",
         "Both queens begin on the d-file; they do not both begin on light squares."),
        (
            check("setup-queen", "Where does Black's queen start?",
                  ("d8, a dark square", True, "The black queen starts on her own color on d8."),
                  ("e8, opposite White's queen", False, "e8 belongs to Black's king. Both queens start on the d-file.")),
            check("setup-wing", "Which squares belong to the kingside wing?",
                  ("The f-, g-, and h-files", True, "These lie toward the starting king's rook, for both players."),
                  ("Whichever edge is on the viewer's right", False, "The board's names remain fixed when you look from Black's seat.")),
        ),
        ("Light corner on the right.", "Queen on her own color; kings on the e-file.", "Play out, explain, reset, and compare."),
    ),
    "object-checkmate": guide(
        (13, 22),
        ("Distinguish the game's objective from material gain.", "Recognize the three possible answers to check."),
        (
            section("A preview of the destination", """
                Your task is to checkmate the enemy king while keeping your own king safe. A check is an attack
                on a king. A checkmate is a check for which there is no legal answer, so the game ends immediately.
                The king stays on the board; you never finish by capturing it. If the movement of a queen or bishop
                is still unfamiliar, use this lesson as a preview. The movement lessons will explain their paths, and
                the later check and mate lessons return to this idea in detail. You do not need to copy a quick-mate
                opening to understand what victory means.
            """),
            section("Inspect the defender's choices", """
                After a checking move, put yourself in the defender's seat. Could the king move to a neighboring
                square that is empty or occupied by a capturable enemy, without entering an attack? Could the king
                or another piece capture the checker legally? Could a friendly piece block the line between checker
                and king? A distant queen, rook, or bishop check may be blocked, but an adjacent checker leaves no
                intervening square. A knight check cannot be blocked. Mate requires every applicable defence to fail;
                simply seeing two attackers near the king does not establish it. In the example, the bishop's most
                important job is protecting the checking queen.
            """),
            section("Why captures still matter", """
                Material means the pieces and pawns available to each player. Winning material often makes a later
                mate easier because you remove defenders and keep more attacking resources. However, a large army
                does not automatically win: the king may escape, the game may be stalemated, or the opponent may
                create a perpetual check. Conversely, a player who is behind can win by mate immediately. Before
                grabbing a piece, ask whether either king faces a more urgent threat. In the worked opening Black
                attacks White's queen with a knight, but that threat arrives too late because White can deliver mate
                on the very next move. The final check takes priority over the threatened capture.
            """),
        ),
        (example("A threat to the queen arrives too late", after(("e4", "e5", "Qh5", "Nc6", "Bc4")), ("Nf6", "Qxf7#"), (
            "Black to move. White's queen on h5 and bishop on c4 both point at f7. This is a teaching illustration, not an opening recommendation.",
            "Black develops and attacks h5, but leaves the immediate mating threat unanswered.",
            "The queen checks from f7. The bishop protects her; the king's other exits are occupied or attacked, and an adjacent queen check cannot be blocked.",
        )),),
        ("A capture is not checkmate unless it attacks the king and leaves no legal answer.",
         "Attacking a queen does not help if the opponent can checkmate before the capture occurs."),
        (
            check("goal-capture", "You have captured the enemy queen, but their king can still move legally. Is the game over?",
                  ("No; continue playing unless another ending condition applies", True, "A material advantage is valuable, but queen capture itself does not end chess."),
                  ("Yes; the strongest piece decides the game", False, "The objective is checkmate, not the capture of a particular non-king piece.")),
            check("goal-mate", "What must be true for checkmate?",
                  ("The king is in check and no legal response removes it", True, "Check plus the failure of every legal defence is mate."),
                  ("The king has no safe square, even if it is not in check", False, "Without check and without any legal move, the result is stalemate, a draw.")),
        ),
        ("Check attacks the king.", "Test move, capture, and block.", "Checkmate ends the game before another turn occurs."),
    ),
    "ranks-files-colors": guide(
        (14, 16),
        ("Locate ranks, files, and diagonals from either side.", "Use square color to check a bishop's route."),
        (
            section("The coordinate grid stays fixed", """
                A rank is a horizontal row of eight squares. Rank 1 holds White's starting pieces and rank 8 holds
                Black's. A file is a vertical column labeled from a to h, reading from White's left to White's right.
                The a-file contains a1 through a8; the fourth rank contains a4 through h4. Looking from Black's
                seat reverses what appears left, right, near, and far, but it never changes a square's name. Black's
                pawns begin on rank 7 and generally move toward rank 1. Say 'Black's back rank is rank 8' to keep
                the shared grid distinct from the way the board looks on screen.
            """),
            section("Diagonals and colors", """
                A diagonal changes file and rank by the same number of squares. From f1 toward the center, one
                diagonal is e2, d3, c4, b5, a6. Every square on it is light. The bishop that starts on f1 can follow
                these routes but can never reach a dark square, however many moves it makes. The c1 bishop lives
                on dark squares instead. Horizontal or vertical steps alternate color each square; diagonal steps
                preserve it. This gives you a useful error check: if you imagine a bishop traveling from dark to light,
                the proposed move is impossible even before you examine intervening pieces. Color is a property of
                the square, not of the piece occupying it.
            """),
            section("A road can exist and still be blocked", """
                Naming a line does not mean a piece may immediately travel along it. In the starting position, the
                f1 bishop's first diagonal squares e2 and g2 contain friendly pawns. White's e-pawn move clears e2,
                so the bishop can later use e2, d3, and c4 if no new blocker appears. A rook likewise needs a clear
                rank or file; it cannot jump through its own pawn. Practice tracing the route square by square and
                stopping at the first occupied square. This combines board geography with legal movement. Rotate
                a real board or imagine sitting on the opposite side, then name the same route again to check that
                you are using coordinates rather than the picture's apparent direction.
            """),
        ),
        (example("Opening the light bishop's diagonal", chess.STARTING_FEN, ("e4", "e5", "Bc4", "Nf6"), (
            "Locate the e-file, ranks 2 and 7, and the light diagonal from f1 toward a6.",
            "The pawn leaves e2 and lands on e4, opening the bishop's route through e2 and d3.",
            "Black also clears e7. Both moves use the same file but opposite forward directions.",
            "The bishop follows f1–e2–d3–c4 without changing square color.",
            "Black's knight jumps from g8 to f6; unlike the bishop, its move changes square color.",
        )),),
        ("The e-file is the same column from Black's side; it does not become the d-file.",
         "A diagonal of the correct color is unusable if a friendly piece blocks the first square."),
        (
            check("grid-back", "From Black's seat, what is the name of Black's starting back rank?",
                  ("Rank 8", True, "All coordinates are counted from White's side regardless of the viewer."),
                  ("Rank 1", False, "It looks nearest to Black, but its shared coordinate remains rank 8.")),
            check("grid-bishop", "Can the original c1 bishop ever move to a light square?",
                  ("No, every diagonal move preserves its square color", True, "The c1 bishop is permanently a dark-squared bishop."),
                  ("Yes, after it makes two moves", False, "Two diagonal moves preserve color just as one does.")),
        ),
        ("Ranks use numbers; files use letters.", "Coordinates stay fixed when the board turns.", "Bishops preserve square color and need clear diagonals."),
    ),
    "square-names": guide(
        (14, 15),
        ("Read and locate a square without relying on an arrow.", "Keep the same coordinates when playing Black."),
        (
            section("Read the letter before the number", """
                A square's name joins its file letter to its rank number. To find f3, locate file f and follow it
                to rank 3; their intersection is f3. The name is f3, never 3f. The letters run a through h and the
                numbers 1 through 8. At the start White's king is on e1, queen on d1, and kingside knight on g1.
                Black's corresponding pieces are on e8, d8, and g8. These reference points help you rebuild the
                grid when you feel lost. Name the origin and destination before moving, especially when two
                similar pieces could otherwise be confused.
            """),
            section("Change the viewpoint, not the labels", """
                From White's seat a1 appears at the near left corner. From Black's seat that same square appears
                at the far right corner. Its occupant and name have not changed. A Black move from g8 to f6
                therefore travels toward smaller rank numbers, although on a board viewed from Black it may look
                like a forward jump upward. Practice pairs: a1 and h8, c2 and f7, g1 and b8. Identify each square
                from both seats rather than memorizing one screen arrangement. In a game record, 'c5' tells both
                players one definite destination; no extra instruction about which way the board is facing is needed.
            """),
            section("Turn naming into a useful playing habit", """
                Coordinate knowledge supports calculation and communication. If you say 'my knight goes from g1
                to f3', you can check both the correct knight and its landing square before releasing it. If a lesson
                says 'the pawn on d5 is attacked', you can inspect that exact pawn. Start with visible labels, then
                cover the edges and name a few squares by counting from known anchors. Accuracy matters more
                than speed. Also distinguish finding a square from proving a legal move: a rook can be told to go
                to f3 even when its current square cannot reach f3. First locate the target, then apply the piece's
                movement rule, blockers, and king safety. The exercise combines those two separate skills.
            """),
        ),
        (example("The same names in Black's opening", after(("e4",)), ("c5", "Nf3", "d6", "d4"), (
            "Black to move after e2–e4. Locate c7, c5, g1, f3, d7, and d6 before playing.",
            "Black's c7 pawn advances toward a lower numbered rank, reaching c5.",
            "White's g1 knight lands on f3, changing both file and rank.",
            "Black's d7 pawn advances one square to d6; 'forward' depends on color, but d6 has one fixed name.",
            "White's d2 pawn advances to d4. Both players now have a pawn on the d-file, on different ranks.",
        )),),
        ("A square name does not encode who occupies it; f3 may later hold any legal occupant.",
         "A correct destination name is not proof that the selected piece can legally reach it."),
        (
            check("names-order", "Which is the standard square name?",
                  ("b6", True, "File letter first, rank number second."),
                  ("6b", False, "This reverses the standard order and is not the square's chess name.")),
            check("names-black", "Black turns the board around. What happens to the square g1?",
                  ("It stays g1, now seen from the opposite direction", True, "Both players share a fixed coordinate system."),
                  ("It becomes b8", False, "b8 may look like the corresponding location in a rotated picture, but it is a different square.")),
        ),
        ("Find file, then rank.", "Say origin and destination precisely.", "Turning the board never renames its squares."),
    ),
    "recording-a-position": guide(
        (14, 15),
        ("Rebuild a position from a complete piece list.", "Separate a position description from a move record."),
        (
            section("Describe the complete snapshot", """
                A position description tells you where all the pieces are at one moment. Group the pieces by
                color, identify their types, and list the square occupied by each. For the small worked position,
                write 'White: king e1, rook a1. Black: king e8. White to move.' Start with an empty board and place
                exactly those pieces. Do not leave the normal starting pawns on the board unless they are listed.
                Check that both kings are present and no square holds two pieces. Saying whose turn it is matters:
                the same arrangement can offer a win to one player and a defence to the other, depending on who acts.
            """),
            section("A move is a change to the snapshot", """
                'Rook a1 to d1' describes one change, not the entire position. You need the earlier position to
                know what else is on the board and whether the path is clear. Move the rook off a1, leave b1 and
                c1 empty, and place it on d1; do not create a second rook. If a capture occurs, remove the enemy
                piece at the destination as well. Now switch the player to move. This habit prevents a common
                reading error: following only the moving piece and forgetting the opponent's reply or a newly
                opened line. After each move, reconstruct the whole position in words before continuing to the
                next instruction in the lesson.
            """),
            section("What a diagram cannot tell you by itself", """
                Piece placement and side to move are enough for many simple studies, but some rules depend on
                history. A king and rook back on their starting squares may already have lost castling rights by
                moving earlier. An adjacent pawn may be capturable en passant only if it has just made a double
                step. A full game record preserves such information. For a standalone exercise, the lesson must
                supply the relevant rights or preceding move explicitly. When transferring a diagram, therefore,
                read its caption as well as its pieces. You need not learn a computer position code yet; accurate
                piece lists, turn information, and a note about any special right already let you follow the teaching
                without guessing what happened before the diagram.
            """),
        ),
        (example("Reconstruct, move, and update", custom({"e1": "K", "a1": "R", "e8": "k"}), ("Rd1", "Ke7", "Rd7+", "Ke6"), (
            "White: Ke1, Ra1. Black: Ke8. White to move. The other 61 squares are empty.",
            "Remove the rook from a1 and put it on d1. The clear first rank makes this legal; Black now moves.",
            "Black's king steps from e8 to e7. This is one illustrative reply, not the only legal move.",
            "The rook advances on the clear d-file to d7, checking along rank 7.",
            "Black moves off the attacked rank to e6. Update both the king square and side to move before reading further.",
        )),),
        ("A move record such as Rd1 cannot reconstruct every other piece without the earlier position.",
         "Returning a king and rook home does not restore castling rights."),
        (
            check("record-list", "A study lists only White Ke1/Ra1 and Black Ke8. Should you add starting pawns?",
                  ("No; place only the listed pieces", True, "A study is a complete specified position, not a partly filled starting board."),
                  ("Yes; unlisted pieces are assumed to be at home", False, "That changes the position and may block the intended moves.")),
            check("record-history", "Can piece placement alone prove that castling is legal?",
                  ("No; the king and rook's previous moves also matter", True, "Castling rights depend on history as well as placement and attacks."),
                  ("Yes; home squares always permit castling", False, "A king that has moved cannot castle even after returning home.")),
        ),
        ("List every piece, its square, and whose turn it is.", "A move updates an existing snapshot.", "Special rights sometimes require history as well as a diagram."),
    ),
    "order-of-play": guide(
        (15, 21),
        ("Track alternating turns and complete move numbers.", "Distinguish taking a turn from touching or adjusting a piece."),
        (
            section("One player acts, then the other", """
                White always makes the first move. After White has made one legal move, Black must make one,
                then White moves again. A move may be a quiet relocation, a capture, a pawn advance, promotion,
                or castling. Most moves change one piece; castling is the special move that changes king and rook
                together during a single turn. A two-square pawn advance is still one move, not two turns. Neither
                player may decline a turn because every available move is unpleasant. If there is no legal move,
                determine whether it is checkmate or stalemate; the game ends rather than letting that player pass
                while the opponent moves again.
            """),
            section("Count moves and replies accurately", """
                A written game commonly groups White's turn and Black's reply under one move number. In '1. e4
                e5 2. Nf3 Nc6', White plays e4, Black answers e5, White plays Nf3, and Black answers Nc6. Four
                individual turns have occurred, but both players have completed two moves. In an exercise, 'Black
                to move' overrides the visual habit of starting with the pieces nearest you. Before planning a
                combination, point to the side to move and ask what the opponent can do after your candidate.
                Imagining two consecutive moves for your own army often creates a plan that looks strong only
                because you forgot to allow the other player a reply.
            """),
            section("Decide before committing the move", """
                Over a physical board, deliberate touching has consequences under touch-move conventions: an
                eligible own piece touched to move must be moved, and an eligible enemy piece deliberately touched
                to capture must be captured. If the required move or capture is impossible, that obligation cannot
                force an illegal move. If you only want to straighten a piece, announce the adjustment first. On
                ChessBot's board, selecting a piece is part of the interface, so take the opportunity to inspect its
                destinations before making the move. The transferable habit is to choose deliberately, play once,
                and examine the opponent's reply. Do not move on autopilot simply because a piece happens to be
                under your hand or highlighted on screen.
            """),
        ),
        (example("Four turns, two complete move numbers", chess.STARTING_FEN, ("e4", "e5", "Nf3", "Nc6"), (
            "White has the first turn. Neither side can move twice in succession.",
            "White advances two squares in one move. It is now Black's first turn.",
            "Black answers. Move number 1 is complete; White begins move number 2.",
            "White develops a knight, threatening e5. White must now allow a reply.",
            "Black develops and defends e5. This reply changes what White can safely capture next.",
        )),),
        ("You cannot pass; stalemate ends the game instead of skipping a turn.",
         "A plan requiring your opponent to make no intervening move is not yet a calculated variation."),
        (
            check("turn-double", "White plays e2–e4. Who moves next?",
                  ("Black", True, "The pawn's double step counts as White's single turn."),
                  ("White, because the pawn moved two squares", False, "Distance traveled does not create extra turns.")),
            check("turn-stalemate", "A player has no legal move and is not in check. What happens?",
                  ("The game ends as a draw by stalemate", True, "There is no passing rule that continues the game."),
                  ("That player skips a turn", False, "Stalemate ends play immediately.")),
        ),
        ("White starts; turns alternate.", "A move number usually pairs White's move with Black's reply.", "Never omit the opponent's turn when calculating."),
    ),
    "how-a-capture-works": guide(
        (15, 18),
        ("Execute a capture and update the board correctly.", "Look for a legal recapture before counting a gain."),
        (
            section("One piece replaces another", """
                To capture, move your piece onto a square occupied by an enemy piece, remove the enemy piece,
                and leave your own piece on that destination. A rook on e1 capturing a pawn on e5 finishes on
                e5, with e1 empty and the pawn off the board. You cannot capture a friendly piece or put two
                pieces on the same square. Capturing is normally optional, except that a check may leave a capture
                as the only legal answer. A capture must follow the moving piece's rule and preserve the safety
                of your king. A piece being within reach is only the beginning of deciding whether taking it is sensible.
            """),
            section("The path and landing square are different", """
                A rook, bishop, or queen cannot pass through any occupied square on its way to a target. The
                first enemy piece on the chosen line may be captured, but the capturing piece stops there. The
                knight jumps over intervening pieces, yet captures only an enemy on its landing square. It does
                not remove pieces underneath the jump. A pawn differs from the other pieces because its quiet
                move goes straight forward while its ordinary capture goes one square diagonally forward. The
                later en-passant lesson explains the special case in which a pawn lands on an empty square and
                removes the neighboring pawn that just advanced two squares. Learn the ordinary pattern first,
                then attach that precise exception.
            """),
            section("Count the reply before claiming a win", """
                After imagining your capture, switch sides and search for everything that can take your piece.
                Include kings, pawns, and distant sliders whose lines have just opened. If a defender can recapture,
                compare the pieces both players lose; taking a pawn with a queen and losing the queen is usually
                a disaster. If no recapture exists, the enemy may still have a stronger check, threat, or attack on
                another piece. In the small worked example there are no hidden attackers: the enemy king is far
                away, so the rook really wins the pawn. In crowded games use the same sequence of questions,
                but inspect the whole board instead of assuming an apparently free piece has no tactical consequences.
            """),
        ),
        (example("Capture first, then allow a reply", custom({"g1": "K", "e1": "R", "e5": "p", "a8": "k"}), ("Rxe5", "Kb7", "Re7+", "Kc6"), (
            "White's rook can reach e5 because e2, e3, and e4 are empty. Black's king cannot defend that pawn.",
            "The pawn disappears and the rook occupies e5. White has won a pawn, not an extra turn.",
            "Black moves the king closer. This is an illustrative legal reply; Black has other king moves.",
            "White uses the clear e-file to reach e7 and checks along rank 7.",
            "Black steps to c6, off the checked rank. Capturing a pawn did not itself end the game.",
        )),),
        ("A knight captures its destination, never the pieces it jumps over.",
         "The first capture does not tell you the trade's result; inspect the recapture."),
        (
            check("capture-place", "After Rxe5, where is the capturing rook?",
                  ("On e5, replacing the captured enemy", True, "A normal capture ends on the captured piece's square."),
                  ("On e6, one square beyond the captured enemy", False, "Chess captures do not jump over an enemy as in draughts.")),
            check("capture-own", "A friendly pawn stands between your rook and an enemy queen. Can the rook capture through it?",
                  ("No; the friendly pawn blocks the line", True, "Rooks cannot jump, even when the target is very valuable."),
                  ("Yes, because captures override blockers", False, "Captures still obey the piece's movement and path rules.")),
        ),
        ("Remove the enemy and occupy its square.", "Check the entire path and your king's safety.", "Imagine the opponent's recapture before deciding."),
    ),
    "rook": guide(
        (15, 16),
        ("Trace every legal rook ray and stop at blockers.", "Distinguish an open line from permission to ignore enemy attacks."),
        (
            section("Four straight directions", """
                A rook moves along its rank or file, in one straight direction for any distance. From a4 it can
                travel sideways along rank 4 or vertically on the a-file. It cannot move diagonally or turn a corner
                during one move. On an otherwise empty board a rook can reach fourteen squares from any square:
                seven along the rank and seven along the file. Being in the center does not increase that empty-board
                total, although the quality of its targets may change. To inspect a rook, trace four rays from its
                square and list the destinations on each; this is more reliable than guessing from the board's appearance.
            """),
            section("The first blocker determines the boundary", """
                Stop a ray when you meet an occupied square. A friendly piece makes that square and everything
                beyond it unavailable. An enemy piece may be captured if king safety permits, but the rook must
                stop on the capture square. In the worked example the white pawn on a6 prevents Ra6, Ra7, or
                Ra8. White can still play Ra5 because that square lies before the blocker. Along rank 4 the enemy
                pawn on d4 permits Rxd4 but prevents a move through it to e4 or beyond. Moving or capturing a
                blocker changes the rook's possibilities on later turns, so recalculate the rays after each move.
            """),
            section("Use clear lines for a purpose", """
                Rooks often need preparation because their starting pawns and pieces block them. A file without
                pawns of either color is called open; a file with no friendly pawn but an enemy pawn is commonly
                called half-open. An open file may still contain pieces, so 'open' does not mean a rook may jump
                through them. Once active, a rook can attack pawns, invade a rank, check the king, or support another
                rook along the same file. Check whether its destination is defended before sending it deep into enemy
                territory. A rook is allowed to move onto an attacked square if that does not expose its own king,
                but voluntarily losing it may still be a bad decision.
            """),
        ),
        (example("A friendly blocker and an enemy stopping point", custom({"g1": "K", "a4": "R", "a6": "P", "d4": "p", "g8": "k"}), ("Rxd4", "Kf7", "Rd7+", "Ke6"), (
            "The a6 pawn blocks the rook upward after a5; the d4 pawn is the first enemy along rank 4.",
            "The rook captures on d4 and stops there. It cannot keep sliding to h4 in the same turn.",
            "Black approaches with the king. This illustrative reply places it on rank 7.",
            "White uses the newly available d-file to check from d7, showing that a rook can change direction on its next turn.",
            "Black leaves the attacked rank. White must now inspect the new position rather than assume every check is mate.",
        )),),
        ("An open file has no pawns; other pieces can still obstruct it.",
         "A rook stops at the first occupied square and never changes direction mid-move."),
        (
            check("rook-blocker", "Your rook on a4 has a friendly pawn on a6. Which upward move is possible if all other conditions are safe?",
                  ("Ra5", True, "a5 is empty and before the friendly blocker."),
                  ("Ra8", False, "The rook cannot pass through its own pawn on a6.")),
            check("rook-reach", "How many destinations has a rook on an otherwise empty board?",
                  ("Fourteen from any square", True, "Seven other squares share its rank and seven share its file."),
                  ("More in the center than in a corner", False, "A rook's rank-plus-file total stays fourteen; bishops and knights have different center effects.")),
        ),
        ("Ranks and files only.", "Trace four rays; stop at the first blocker.", "Activity matters only when the destination serves a concrete purpose."),
    ),
    "bishop": guide(
        (16, 18),
        ("Trace a bishop's diagonals and color limits.", "Compare central mobility with blocked-pawn restrictions."),
        (
            section("A long diagonal move stays on one color", """
                A bishop travels diagonally in one straight line for any distance. Each diagonal step changes the
                file and rank together: c1–d2–e3–f4–g5–h6 is one route. All those squares are dark. A bishop
                cannot make a rook move and cannot jump over a blocker. The c1 bishop therefore remains a
                dark-squared bishop for its whole life, while the f1 bishop remains light-squared. This is why two
                bishops complement one another: each can operate on colors the other will never reach. Having a
                bishop does not mean you can attack every enemy square; first check whether the target lies on
                a reachable diagonal of the appropriate color.
            """),
            section("Mobility depends on square and surroundings", """
                On an empty board a bishop on one of the four central squares can reach thirteen destinations.
                From a corner it has seven. Near the center several diagonal arms are available, while the edge
                cuts some arms short or removes them altogether. Actual mobility may be much lower because
                pawns or pieces interrupt the diagonals. In the initial position both bishops are blocked by their
                own pawns. Moving the d-pawn opens the c1 bishop's route through d2; moving the e-pawn opens
                the f1 bishop's route through e2. Do not count a beautiful long diagonal as usable until you have
                inspected every intervening square and the first occupied destination.
            """),
            section("A long-range defender as well as an attacker", """
                A bishop can protect a piece from far away. Trace its diagonal all the way to a contested square:
                if an enemy captures your piece there, could the bishop legally recapture? The book uses this
                relationship to explain why a knight may be safely defended by a bishop and why taking a protected
                pawn can lose a more valuable piece. Position matters as well as reach. A bishop locked behind
                its own same-colored pawns may need pawn preparation or a different diagonal. A bishop whose
                diagonal points toward the enemy king can help a queen deliver mate without moving again.
                Always inspect its role after another piece moves; removing a blocker can suddenly reveal an attack
                or a defence that was previously hidden.
            """),
        ),
        (example("Release the dark-squared bishop", chess.STARTING_FEN, ("d4", "d5", "Bf4", "Nf6"), (
            "White's c1 bishop has a diagonal route through d2, but its own pawn initially blocks that square.",
            "The d-pawn leaves d2, opening the diagonal. It does not move the bishop itself.",
            "Black claims central space. This reply does not block White's c1–f4 route.",
            "The bishop travels through d2 and e3 to f4; each square is dark.",
            "Black develops a knight. White must now consider the changed central attacks before choosing the bishop's next job.",
        )),),
        ("A bishop on a dark square can never switch to light by making several diagonal moves.",
         "A bishop can defend a distant friendly piece only when its square lies on an unobstructed diagonal of the bishop's color."),
        (
            check("bishop-path", "Which route is a single bishop move from c1?",
                  ("c1–d2–e3–f4, if clear", True, "Both coordinates change equally along one diagonal."),
                  ("c1–c3–f3", False, "This uses straight moves and a turn, neither of which a bishop can make.")),
            check("bishop-center", "Why can an empty-board central bishop reach more squares than a corner bishop?",
                  ("It has more diagonal arms available before the edges stop them", True, "The board boundary changes the bishop's total reach."),
                  ("It is allowed to jump in the center", False, "A bishop can never jump, regardless of its square.")),
        ),
        ("Diagonals only, with clear paths.", "One bishop keeps one square color.", "Inspect distant attacks and defences after blockers move."),
    ),
    "queen": guide(
        (16, 17),
        ("Use the queen's rook-like and bishop-like directions correctly.", "Distinguish mobility from a safe or useful move."),
        (
            section("Combine two movement patterns", """
                The queen can move like a rook or a bishop: along a rank, a file, or a diagonal, for any distance.
                She chooses one straight direction for the whole move. She cannot travel partway up a file and
                then turn along a rank, and she cannot make a knight's L-shaped jump. From d1, both d8 along
                a file and h5 along a diagonal are geometrically reachable if the paths are clear. A move to a4
                is also diagonal, through c2 and b3; it is not a first-rank move. Naming the intervening squares is
                a useful way to catch a mistaken imagined route before playing it.
            """),
            section("Reach gives power but does not remove blockers", """
                A queen on an empty central square has twenty-seven destinations, combining the rook's fourteen
                with the bishop's thirteen. She can change the color of the square she occupies by using a rank
                or file, so unlike a bishop she is not restricted to one color. Nevertheless, she cannot jump over
                either army. A friendly piece blocks the ray completely; an enemy may be captured, but the queen
                stops on that square. Being able to reach an enemy is not proof that capturing it is good. Before
                moving the queen, imagine where it will stand and ask which enemy piece can capture it or attack
                it on the next turn.
            """),
            section("The strongest piece still needs teammates", """
                Early queen excursions can let the opponent develop pieces while attacking her, forcing repeated
                retreats instead of helping your other pieces enter the game. A queen near a king can also fail to
                mate because she is unprotected: the king may simply capture her. In the worked line White gives
                checks from a distance and Black escapes legally; this illustrates movement and responses rather
                than a forced winning method. Later lessons show how a supporting king or bishop can deny
                capture and flight squares. For optional geometric practice, place several queens so that none
                attacks another. The classic eight-queens puzzle requires avoiding shared ranks, files, and diagonals;
                it is a reach exercise, not a position that could occur with the normal starting queens alone.
            """),
        ),
        (example("Two straight directions on different turns", custom({"e1": "K", "d1": "Q", "e8": "k"}), ("Qh5+", "Ke7", "Qe5+", "Kd7"), (
            "White's queen can use a clear file, rank, or diagonal. First trace d1–e2–f3–g4–h5.",
            "Qh5+ checks along h5–g6–f7–e8. The move uses one diagonal throughout.",
            "Black steps to e7, off that diagonal. This is one legal response, not the only one.",
            "White now changes direction on a later turn, moving along rank 5 to e5 and checking up the e-file.",
            "Black escapes to d7. Several checks have occurred, but no mate has been established.",
        )),),
        ("The queen cannot turn corners or jump like a knight.",
         "A queen beside the enemy king may be capturable unless another piece protects her."),
        (
            check("queen-knight", "Can a queen make a knight's L-shaped move?",
                  ("No; she uses ranks, files, and diagonals", True, "Combining rook and bishop movement does not include the knight's jump."),
                  ("Yes; the strongest piece may use every move", False, "Strength does not change the defined movement rule.")),
            check("queen-safety", "Your queen can capture an unprotected pawn. What still needs checking?",
                  ("The queen's destination, king safety, and the opponent's reply", True, "An apparently free pawn can be tactically poisoned."),
                  ("Nothing; any legal queen capture is favorable", False, "A legal move can lose the queen or allow mate elsewhere.")),
        ),
        ("A rook direction or bishop direction, never a mid-move turn.", "The queen cannot jump through blockers.", "Powerful reach still requires safety and coordination."),
    ),
    "knight": guide(
        (17, 18),
        ("Find a knight's destinations without tracing false intermediate steps.", "Use jumping and color change to inspect attacks."),
        (
            section("One jump with a fixed shape", """
                A knight's destination is two squares along one axis and one along the perpendicular axis. From
                g1, f3 and h3 are examples; e2 is another geometrical destination but is initially occupied by a
                friendly pawn. The L is a memory aid for the displacement, not a route whose intermediate squares
                must be empty. You may imagine the long part first or the short part first and reach the same
                target. What matters is the final difference in file and rank. A knight cannot stop after the first
                two squares, extend the long arm to three, or add another turn during the same move.
            """),
            section("Jumping changes the meaning of a blocker", """
                A knight can jump over friendly and enemy pieces. This lets the starting knights develop while
                their own pawns are still on rank 2 or rank 7. However, the destination must be empty or occupied
                by an enemy that can legally be captured. A friendly piece on the destination makes that jump
                unavailable. Only an enemy on the landing square is captured; none of the pieces between origin
                and target is removed. Near the center a knight may have eight geometrical destinations, whereas
                a corner knight has only two. Moving toward the edge often reduces its useful choices, although a
                concrete check or capture can justify such a move in a particular position.
            """),
            section("Color, attacks, and practice", """
                Every knight move changes square color. A knight currently on a dark square attacks light-square
                destinations, then after jumping it attacks dark ones. Use that as a quick check on a proposed
                move, but still verify the L shape. Because a knight jumps, its check cannot be stopped by placing
                a piece between knight and king; the defender must move the king or capture the knight. For extra
                movement practice, try a knight tour that visits squares without repeating one. Start with a small
                route rather than demanding a complete tour at once. The book's full-board tour demonstrates
                the range of connected jumps; the important beginner skill is identifying all legal destinations and
                noticing attacks from a piece whose lines cannot be blocked.
            """),
        ),
        (example("Develop over a full pawn row", chess.STARTING_FEN, ("Nf3", "Nf6", "Nc3", "Nc6"), (
            "All pawns still block the sliders, but a knight only needs a legal landing square.",
            "White's g1 knight jumps to f3 over its own crowded position and changes from dark to light.",
            "Black's g8 knight jumps toward the center to f6, changing from light to dark.",
            "White's other knight develops from b1 to c3. This is a different piece, even though both moves begin with N.",
            "Black develops from b8 to c6. Four jumps have occurred without any pawn having to clear a path.",
        )),),
        ("The knight's intermediate L-shaped route does not have to be empty.",
         "A knight cannot land on a friendly piece, even though it can jump over one."),
        (
            check("knight-block", "A pawn stands between your knight and its L-shaped target. Is that alone a blocker?",
                  ("No; the knight jumps to its destination", True, "Intervening occupancy does not stop a knight's jump."),
                  ("Yes; every piece needs a clear path", False, "The knight is the exception to the clear-path requirement.")),
            check("knight-color", "A knight is on a dark square. What color will its next landing square have?",
                  ("Light", True, "The two-plus-one displacement always changes square color."),
                  ("Either color, depending on the direction", False, "Every legal direction changes color in exactly the same way.")),
        ),
        ("Two along one axis and one along the other.", "Jump over pieces; capture only at the destination.", "Every jump changes square color."),
    ),
    "king": guide(
        (18, 19),
        ("Find safe neighboring squares and legal king captures.", "Apply attacks even when an enemy defender is pinned."),
        (
            section("One square, with a safety condition", """
                The king moves one square along a rank, file, or diagonal. In the center an otherwise unrestricted
                king has eight neighboring squares; near an edge it has fewer. It cannot jump over a piece,
                share a square with a friendly piece, or step into an enemy attack. A capture is permitted only
                if the king's resulting square is safe after the captured piece has been removed. Unlike a queen
                sacrifice, putting your king on an attacked square is never a legal risk you may choose to take.
                The king is not captured in chess: illegal exposure is prevented, and an unavoidable attack ends
                the game as checkmate.
            """),
            section("Inspect the board after the imagined capture", """
                To test Kxe4, first imagine the enemy on e4 removed and your king placed there. Now ask whether
                any remaining enemy pawn, knight, bishop, rook, queen, or king attacks e4. Removing a blocker
                may reveal a distant rook or bishop, so testing only the piece you are capturing is insufficient.
                Enemy pawns attack diagonally, including empty squares, while knights jump. Enemy kings attack
                every neighboring square, which is why kings may never stand next to each other. Even a piece
                pinned to its own king counts as attacking its usual destinations for this safety test. Do not
                treat an enemy pinned knight as permission to walk your king onto one of its attacked squares.
            """),
            section("Safety changes into activity as armies shrink", """
                In the opening, exposed kings are easy targets for several developing attackers. Castling often
                helps by moving the king toward shelter and developing a rook. Later, when major threats have
                disappeared, the king can become a powerful helper: it attacks nearby pawns, protects promotion,
                and removes escape squares during mate. Activity is still constrained by the same safety rule.
                Kings facing one another with a square between them restrict each other's progress; this arrangement
                is called opposition and becomes important in pawn endings. Do not read 'activate the king' as
                permission to rush into checks. Examine each destination, move only one square, and allow the
                opponent's reply before planning the next step. A route of three king steps takes three separate turns.
            """),
        ),
        (example("Capture an unprotected piece safely", custom({"e1": "K", "e2": "p", "a8": "k", "h7": "p"}), ("Kxe2", "Kb7", "Kd3", "h6"), (
            "The black pawn on e2 attacks d1 and f1, not e1. White may capture it if e2 has no other attacker.",
            "The king captures on e2. The distant black king and h-pawn do not attack that square.",
            "Black moves closer on the queenside; this is an illustrative legal reply.",
            "White steps diagonally to d3, using the king actively in a sparse ending.",
            "Black advances the remaining pawn. White must now reassess its attacks, not merely continue a memorized king route.",
        )),),
        ("A defended enemy piece is not a legal king capture, even if its defender cannot legally move because of a pin.",
         "Kings two squares apart can be legal; kings on neighboring squares are never legal."),
        (
            check("king-pinned", "An enemy knight is pinned to its king. May your king enter a square that knight attacks?",
                  ("No; its attacked squares still count for king safety", True, "A pin may prevent ordinary recaptures, but does not permit an enemy king to enter its attacks."),
                  ("Yes; the knight cannot legally move", False, "This confuses legal recapture with the attacked-square rule used for kings.")),
            check("king-capture", "Your king can reach an enemy rook one square away. What decides whether capture is legal?",
                  ("Whether the destination is safe after the rook is removed", True, "Other defenders and newly opened lines must all be checked."),
                  ("The rook is more valuable, so capture is always legal", False, "Piece value never overrides king safety.")),
        ),
        ("One square in any direction.", "Test attacks on the resulting square, including pinned attackers.", "An active endgame king still obeys every safety rule."),
    ),

    "attack-defence": guide(
        (18, 22),
        ("Identify attackers and verify legal recaptures.", "Distinguish tactical defence from attacks that restrict the king."),
        (
            section("Attack follows movement, not intention", """
                A piece attacks squares according to its movement pattern and the blockers on its rays. A rook
                attacks along its rank and file; a bishop along diagonals; a knight by jumping; a pawn one square
                diagonally forward. A pawn does not attack the empty square directly in front of it, even though
                it can move there. To assess a target, trace every enemy piece's route to its square. Count pawns
                and kings too, not just large pieces. Then check whether a proposed capture would expose the
                attacker's king. Geometry identifies a possible relationship, while legality decides whether that
                ordinary capture can actually be played in the current position.
            """),
            section("A defender must survive the whole calculation", """
                A piece is defended in an exchange when another friendly piece could legally capture an enemy
                that takes it. Imagine the first capture, remove the captured piece, and only then inspect the
                recapture. In the worked line the bishop on f3 defends e4: after White's rook captures a pawn
                there and Black's rook takes it, the bishop can take that rook. Merely counting one attacker and
                one defender can mislead because pieces have different values and later captures may follow.
                Defenders can also become overloaded or pinned. If moving a defender would expose its own king,
                its ordinary recapture may be illegal. Test the resulting position rather than trusting a label such
                as 'protected' that belonged to an earlier position.
            """),
            section("King safety uses the attacked-square rule", """
                There is a crucial qualification to the pin discussion: a pinned piece still attacks its normal
                squares for the purpose of an enemy king's movement and castling. Suppose White has Ke1, Ne2,
                and Pf4, while Black has Re8 and Kg4. The knight cannot move freely because it shields the
                white king from the rook, yet Black cannot play Kxf4: f4 is attacked by that knight. Do not
                confuse 'this piece cannot legally make an ordinary recapture' with 'the enemy king may enter
                its attacks'. Practical defence also includes moving the threatened piece, capturing its attacker,
                or blocking a sliding line. Choose the method that meets the threat while keeping your own king safe.
            """),
        ),
        (example("A genuine recapture behind the defender", custom({"g1": "K", "e1": "R", "f3": "B", "e4": "p", "e8": "r", "a8": "k"}), ("Rxe4", "Rxe4", "Bxe4+"), (
            "The pawn on e4 is attacked by White's rook and bishop. Black's rook can recapture down the e-file.",
            "White captures the pawn but has not yet kept the rook: Black has a legal recapture.",
            "Black takes the white rook. The black rook now stands on the bishop's f3–e4 diagonal.",
            "White recaptures with the bishop, trading rooks and taking the pawn. The diagonal gives check, but only king and bishop versus king remain, so the game ends drawn by insufficient material. Winning a pawn did not win this game.",
        )),),
        ("A pawn's forward movement square is different from its diagonal attack squares.",
         "Pinned pieces can fail as ordinary recapturers but still forbid enemy king destinations."),
        (
            check("defence-pawn", "A white pawn stands on e4. Which squares does it attack?",
                  ("d5 and f5", True, "Pawns attack one square diagonally forward, whether occupied or empty."),
                  ("e5 and e6", False, "Those are forward-file squares, not pawn capture squares.")),
            check("defence-legal", "Your bishop appears to defend a rook, but moving it would expose your king. Can you assume it will recapture an ordinary enemy piece?",
                  ("No; the recapture must be legal after the capture", True, "A geometric line alone is insufficient when the defender is pinned to its king."),
                  ("Yes; one defender always cancels one attacker", False, "Legality, values, and further captures all matter.")),
        ),
        ("Trace all attacks, including pawn attacks.", "Play out the capture and legal recapture.", "Keep king-safety attacks distinct from ordinary recapture legality."),
    ),
    "exchanges": guide(
        (18, 26),
        ("Account for both sides of a trade.", "Use 'the exchange' precisely for rook versus minor piece."),
        (
            section("Count what disappears, not what moves first", """
                An exchange in the broad sense is a trade: one side captures and the other recaptures, or both
                sides give up material during a sequence. Write down the pieces removed from each army. If
                White loses a knight and Black loses a knight, material is unchanged, although the new position
                may favor one player. If a bishop takes a rook and is never recaptured, White has won a whole
                rook, not merely traded a bishop for it. The fact that a weaker piece made the capture does not
                mean that weaker piece has been lost. Always include the opponent's actual reply before announcing
                the result of a supposed exchange.
            """),
            section("The special phrase 'winning the exchange'", """
                Bishops and knights are minor pieces; rooks and queens are major pieces. A rook is normally
                stronger than one bishop or knight. The material difference between a rook and a minor piece is
                called the exchange. Gaining a rook while giving up a bishop or knight wins the exchange; the
                reverse loses it. This names a material difference, not a guarantee of victory. In the lesson's
                small quiz, Bxg8 followed by Kxg8 removes Black's rook and White's bishop, leaving only kings:
                White has gained that material difference but saved a draw rather than created a winning army.
                Extra material elsewhere would change the final assessment.
            """),
            section("Use value as a starting point, then inspect placement", """
                Rough piece values help you avoid obvious losses, but they do not replace calculation. A trade
                that loses material may stop mate, create a dangerous passed pawn, or secure a perpetual check.
                Conversely, an apparently favorable capture may expose your king or stalemate the opponent.
                The book contrasts positions with the same rook-versus-bishop material but different arrangements:
                one permits a winning tactic, another resists it. Before trading, ask what each side loses, what
                checking moves follow, which king is safer, and what the remaining pieces can accomplish.
                For a beginner, complete a short reliable capture sequence before trying a speculative sacrifice.
                Do not interpret either 'always trade when ahead' or 'never sacrifice a rook' as an exceptionless law.
            """),
        ),
        (example("A rook for a bishop, with another rook remaining", custom({"e1": "K", "a1": "R", "a2": "B", "h8": "k", "g8": "r"}), ("Bxg8", "Kxg8"), (
            "White's bishop attacks g8. Black's king on h8 can legally recapture a bishop that lands there.",
            "White takes the rook. This is not check: a bishop on g8 does not attack h8.",
            "Black recaptures the bishop. White lost B, Black lost R, and White's other rook remains against the lone king. The reply illustrates the trade; Black could choose a different legal king move instead.",
        )),),
        ("Taking a rook with a bishop wins a whole rook if the bishop is never lost; inspect the recapture.",
         "Winning the exchange describes material gained, not an automatic game result."),
        (
            check("exchange-count", "You gain a rook and lose a bishop in return. What have you gained?",
                  ("The exchange", True, "This is the standard rook-versus-minor-piece material difference."),
                  ("A whole rook without cost", False, "The bishop was lost, so the gain must account for that cost.")),
            check("exchange-none", "Your bishop captures an undefended rook and stays safe. What has happened?",
                  ("You have won a whole rook", True, "No bishop has been lost, so there is no bishop-for-rook trade to subtract."),
                  ("You automatically sacrificed the bishop because it made a capture", False, "A piece that captures remains on the board unless the opponent later captures it.")),
        ),
        ("List both armies' losses.", "The exchange is a rook for a bishop or knight.", "Judge the resulting position as well as the material difference."),
    ),
    "pawn-move": guide(
        (19, 20),
        ("Separate pawn movement from pawn attacks for both colors.", "Recognize basic pawn-structure vocabulary."),
        (
            section("Forward is different for the two armies", """
                A white pawn normally moves one square toward a higher rank number; a black pawn moves toward
                a lower number. From its starting square a pawn may advance two squares instead, but both the
                crossed square and destination must be empty. It may not jump a blocker. White therefore has a
                possible e2–e4, while Black has e7–e5. Once the pawn has left its starting rank, every ordinary
                forward advance is only one square. Pawns never move backward or sideways. An enemy directly
                ahead blocks the pawn just as a friendly piece does; a pawn cannot solve that obstruction by
                capturing straight forward. These restrictions make pawn moves lasting commitments.
            """),
            section("Capture diagonally, protect diagonally", """
                A pawn's ordinary capture goes one square diagonally forward. A white pawn on e4 attacks d5
                and f5, while a black pawn on e4 attacks d3 and f3. Those attacks exist even when the target
                squares are empty, which matters for king safety. A pawn does not attack the square it can quietly
                advance to. Two opposing pawns on the same file can therefore block one another without either
                being able to capture the other. When one pawn advances to support a neighbor diagonally, it
                may turn a loose pawn into a defended one. Before pushing, inspect both what the pawn will
                attack and which squares it will stop defending behind it.
            """),
            section("Read the pawn structure as a set of relationships", """
                Doubled pawns are two friendly pawns on one file; isolated pawns have no friendly pawn on either
                adjacent file. Connected or united pawns occupy neighboring files and may support each other's
                advance. Doubled and isolated are independent descriptions, so a pair can be both. The book also
                introduces 'backward' for pawns lagging behind adjacent friendly pawns. In practical analysis the
                term usually needs more care: ask whether the pawn can safely advance and receive support,
                rather than calling every trailing pawn weak. A passed pawn has no opposing pawn ahead on its
                file or adjacent files that can stop its advance by ordinary pawn movement or capture. Pieces
                can still stop a passed pawn. These names describe structure, not a verdict that every such pawn wins or loses.
            """),
        ),
        (example("Black captures forward toward smaller numbers", custom({"g1": "K", "e4": "P", "d5": "p", "f5": "p", "a8": "k"}, turn="b"), ("dxe4", "Kf2", "e3+", "Kxe3"), (
            "Black to move. The d5 pawn moves toward rank 1 and attacks the white pawn on e4.",
            "Black captures diagonally from d5 to e4, leaving d5 empty. Its ordinary advance would have been d4 instead.",
            "White approaches with the king. f2 is safe: the e4 pawn attacks d3 and f3, not f2.",
            "Black advances to e3 and checks the king on f2 by attacking diagonally.",
            "White captures the unprotected checking pawn on e3. The f5 pawn attacks e4 and g4, not e3.",
        )),),
        ("The two-square option requires two empty squares; it is not a jump over a piece.",
         "A passed pawn can be stopped by a king or piece even though no enemy pawn blocks its path."),
        (
            check("pawn-black", "A black pawn on f4 attacks which squares?",
                  ("e3 and g3", True, "Black captures toward lower rank numbers, diagonally one square."),
                  ("e5 and g5", False, "Those are the attack directions of a white pawn on f4.")),
            check("pawn-isolated", "What makes a pawn isolated?",
                  ("No friendly pawn on either neighboring file", True, "The absence of adjacent-file pawns prevents ordinary pawn support."),
                  ("It is far from its king", False, "King distance can matter, but it does not define pawn isolation.")),
        ),
        ("Advance straight; capture diagonally; never retreat.", "Black moves toward smaller rank numbers.", "Pawn-structure names describe relationships, not automatic results."),
    ),
    "en-passant": guide(
        (19, 20),
        ("Recognize every requirement of an en-passant capture.", "Remove the correct pawn and respect the immediate deadline."),
        (
            section("What the exception prevents", """
                A starting pawn may use a two-square advance, but this must not let it bypass an enemy pawn
                that would have been able to capture it after a one-square move. If the double step lands beside
                an opposing pawn already on its fifth rank, that opposing pawn may capture as though the mover
                had stopped on the crossed square. White must already be on rank 5, Black on rank 4. White's
                e5 pawn can therefore answer ...d7–d5 by moving to d6. Black's pawn disappears from d5 even
                though the white pawn did not land there. This unusual removal is the defining feature of en passant.
            """),
            section("Check all conditions, including the previous move", """
                The neighboring pawn must have advanced two squares from its starting square on the immediately
                preceding turn. A pawn that advanced only one square, or reached that neighboring square several
                turns ago, is not eligible. The capture must be made on your very next move; choosing any other
                move permanently gives up that particular opportunity. Capturing is optional, not compulsory.
                If two pawns could capture the double-step pawn en passant, either eligible capture may be
                chosen. As with every move, it must leave your own king safe. Removing both pawns from their
                original rank can open a rook's line, so an apparently available en-passant capture can be illegal
                when it would expose your king to check.
            """),
            section("Reconstruct the before and after positions", """
                Say three squares aloud: your pawn's origin, its diagonal destination, and the enemy pawn's actual
                square. For e5xd6 en passant they are e5, d6, and d5. Empty e5, remove the black pawn from d5,
                and put the white pawn on d6. It is a capture and a pawn move within a single turn. Black uses
                the same rule in the opposite direction: a black pawn on f4 may answer g2–g4 with ...fxg3,
                landing on g3 while removing the pawn on g4. A static diagram cannot prove the opportunity exists;
                you need the previous move or an explicit statement of the right. Practice both colors so that
                the rule is understood as a relationship rather than one memorized white arrow.
            """),
        ),
        (example("Black captures the pawn that tried to pass", custom({"a1": "K", "g2": "P", "f4": "p", "a8": "k"}), ("g4", "fxg3", "Kb2", "Kb7"), (
            "White's pawn is on its starting square. The black pawn already stands on its own fifth rank, rank 4.",
            "g2–g4 crosses g3 and lands beside the black pawn. Black has exactly this reply to use the special capture.",
            "Black's pawn moves from f4 to g3, and White's pawn is removed from g4. Nothing was captured on the empty landing square.",
            "White moves the king; the special capture has already been completed as one black turn.",
            "Black moves the king too. The en-passant rule did not grant an extra turn or a reusable capture right.",
        )),),
        ("En passant is optional, but waiting one move loses that opportunity.",
         "The captured pawn is removed from its adjacent square, not from the empty destination.",
         "An en-passant capture that exposes your own king is illegal."),
        (
            check("ep-time", "The opponent double-stepped beside your eligible pawn, but you moved a knight. Can you capture en passant on your next turn?",
                  ("No; the opportunity has expired", True, "It is available only as the immediate reply to that double step."),
                  ("Yes; adjacent pawns keep the right", False, "Adjacency alone does not preserve the historical right.")),
            check("ep-remove", "After White e5xd6 en passant against a pawn that just moved d7–d5, which black pawn is removed?",
                  ("The pawn on d5", True, "White lands on d6 while removing the pawn that just double-stepped to d5."),
                  ("A pawn on d6", False, "d6 was empty; landing on that empty square is the special exception.")),
        ),
        ("A neighboring enemy must have just double-stepped.", "Capture immediately or lose that opportunity.", "Land diagonally on the crossed square and remove the adjacent pawn."),
    ),
    "promotion": guide(
        (20, 21),
        ("Promote on a quiet move or capture with either color.", "Choose a promotion by its resulting position, including underpromotion."),
        (
            section("The pawn is replaced during the same move", """
                When a white pawn reaches rank 8 or a black pawn reaches rank 1, it must immediately become
                a queen, rook, bishop, or knight of its own color. It cannot remain a pawn or become a king.
                Moving to the last rank and replacing the pawn together count as one turn, so the new piece
                acts immediately: promotion may give check or mate. The choice is not limited to pieces previously
                captured. You may have two or more queens, three knights, or another legal promoted collection.
                A pawn reaching the last rank by a diagonal capture promotes just as one advancing straight does.
                Remove the captured enemy as well as replacing the pawn.
            """),
            section("A queen is usual, but inspect the result", """
                The queen normally gives the greatest power, yet 'always choose a queen' fails in positions where
                it stalemates the enemy or a different piece has a specific tactical function. Choosing a rook,
                bishop, or knight is called underpromotion. A knight may check or fork squares a queen cannot,
                and a rook may preserve a legal enemy move that a queen's diagonal would remove. In the worked
                example White Kc6/Pc7 faces Black Ka7. Promoting to a queen on c8 leaves Black unchecked
                with every flight controlled: stalemate. Promoting to a rook preserves a6 as a legal move and
                keeps a winning rook-and-king force. Evaluate after replacing the pawn, not from its old movement.
            """),
            section("Getting there is part of the calculation", """
                A passed pawn has no opposing pawn ahead on its file or the neighboring files that can obstruct
                its normal advance or capture it. This does not guarantee promotion: enemy kings and pieces may
                still blockade or capture it. Supporting a passed pawn, diverting a blocker, or sacrificing another
                piece can clear its route. A promoted queen may also be captured immediately, and that does not
                invalidate the promotion; count the full continuation. The book uses examples where a pawn's
                promotion draws a piece onto a square and another attacker then recaptures it. Practice asking
                both 'what can this pawn become?' and 'what will the opponent do next?' A promotion is a move
                within the game, not an automatic victory ceremony.
            """),
        ),
        (example("A rook promotion avoids stalemate", custom({"c6": "K", "c7": "P", "a7": "k"}), ("c8=R", "Ka6"), (
            "White to move. A queen on c8 would cover a6 diagonally as well as a8 and b8, leaving Black stalemated.",
            "White chooses a rook. It controls rank 8 but does not attack a6, so the enemy king retains a legal move.",
            "Black moves to a6, its only legal destination. White retains king and rook against king rather than ending the game in a stalemate draw.",
        )), example("Promotion by a capture", custom({"g1": "K", "a7": "P", "b8": "n", "h8": "k"}), ("axb8=Q+", "Kg7"), (
            "The a7 pawn can advance to a8 or capture the enemy knight on b8; either last-rank move requires promotion.",
            "The pawn captures the knight and becomes a queen on b8, checking across rank 8 immediately.",
            "Black leaves the eighth rank. The new queen remains on b8 and is usable on White's next turn.",
        ))),
        ("You may promote to an additional queen even if your original queen survives.",
         "Underpromotion has several tactical uses; a knight check and avoiding stalemate are examples, not an exhaustive list."),
        (
            check("promo-extra", "Your original queen is still on the board. What may a pawn promote to?",
                  ("Any queen, rook, bishop, or knight of your color", True, "The promotion choice is not limited by the original inventory or captured pieces."),
                  ("Only a piece you have already lost", False, "Chess permits extra queens and other additional pieces.")),
            check("promo-stale", "A queen promotion gives immediate stalemate, while a rook promotion keeps a winning ending. Which should you choose?",
                  ("The rook", True, "The result of the move matters more than the queen's greater nominal strength."),
                  ("The queen automatically", False, "A stalemate ends the game as a draw, regardless of how much material you gain.")),
        ),
        ("Replace the last-rank pawn immediately.", "Quiet moves and captures can both promote.", "Compare the resulting positions before choosing the new piece."),
    ),
    "check": guide(
        (21, 22),
        ("Test capture, block, and king movement as answers to check.", "Recognize discovered check, double check, and a king pin."),
        (
            section("A check creates an immediate obligation", """
                Check means the king is attacked. The defender's next move must remove every attack on that
                king. There are three categories of response: capture the checking piece, put a piece between
                checker and king, or move the king to a safe neighboring square. Each candidate must be legal
                after the whole move; capturing one attacker is insufficient if another still checks. Blocking
                applies only to a line check with an intervening square. A knight jumps, and adjacent checking
                pieces leave no space to interpose. Announcing check aloud is optional. A player cannot ignore
                an unannounced check, and giving check does not grant the attacker an extra move.
            """),
            section("A moved piece may uncover someone else's check", """
                A discovered check occurs when moving one piece opens the line of another piece behind it.
                In the worked position the bishop on d7 blocks White's rook on a7 from attacking the king on
                h7. Moving that bishop away reveals the rook check. If the bishop moves to f5, it also attacks
                h7 along f5–g6–h7, creating double check. The defender must move the king: capturing or blocking
                only one checker leaves the other attack intact. Do not look only at the piece that just moved;
                inspect the lines it uncovered. The same discovered-line idea explains how an apparently quiet
                relocation can be forcing and why moving a defender carelessly can expose your own king.
            """),
            section("Blocking a check may create a pin", """
                Instead of Bf5+, White may discover the rook check with Be8+. Black can answer by moving
                the knight from h5 to g7, placing it between the rook and king. That knight is now pinned to
                its king along rank 7: moving it off the line would expose check, so such a move is illegal.
                Some pinned pieces can move along the pinning line or capture the attacker, so 'pinned' does
                not always mean completely immobile. For each check, search all three response categories
                before claiming mate. Practice the defender's view as carefully as the attacker's; noticing that
                a tempting capture fails to answer a second check is often the difference between legal defence
                and an impossible imagined variation.
            """),
        ),
        (example("Discovered check becomes double check", custom({"e5": "K", "a7": "R", "d7": "B", "h7": "k", "h5": "n"}), ("Bf5+", "Kg8"), (
            "The bishop on d7 blocks the rook's seventh-rank line. Black is not yet in check.",
            "The bishop moves away and checks diagonally while the rook also checks along rank 7: double check.",
            "Black moves the king off both attacks. Every legal defence here is a king move; Kg8 is one example.",
        )), example("A block creates a pin", custom({"e5": "K", "a7": "R", "d7": "B", "h7": "k", "h5": "n"}), ("Be8+", "Ng7"), (
            "Use the same initial arrangement, but choose a bishop destination that does not itself check h7.",
            "Be8+ reveals only the rook's check, so interposing a piece can work.",
            "The knight blocks on g7 and is pinned to the king. It cannot jump away and reopen the rook's line.",
        ))),
        ("A check is compulsory to answer even if nobody says 'check'.", "A double check cannot be answered by blocking only one checking line."),
        (
            check("check-knight", "Can you answer a knight check by putting a piece between knight and king?",
                  ("No; move the king or capture the knight if legal", True, "A knight's jump has no blockable checking line."),
                  ("Yes; any piece halfway along the L blocks it", False, "Intermediate squares do not interrupt knight attacks.")),
            check("check-double", "Two pieces give check at once. What category of response is possible?",
                  ("A legal king move", True, "The king must leave both attacks; stopping only one checker is insufficient."),
                  ("Any capture of either checker", False, "That would leave the other check unanswered unless the king itself moves to safety.")),
        ),
        ("Answer every check immediately.", "Test capture, block, and safe king movement.", "Look behind a moved piece for discovered or double check."),
    ),

    "mate": guide(
        (21, 23),
        ("Prove checkmate by exhausting the three defences.", "Distinguish restricting a king from actually checking it."),
        (
            section("Begin with the check itself", """
                Before searching for escape squares, identify the exact attacking line or jump that reaches the
                king. If the king is not attacked, the position cannot be mate, however cramped it looks. A rook
                on h8 attacks a king on e8 along rank 8; a rook on h7 does not attack that same king. Make this
                first test explicit rather than letting an impressive-looking move persuade you. The mark # in
                a move record is a claim about the resulting position, not a decoration that turns a check into
                mate. When studying an answer, verify its attack yourself and then inspect every legal kind of defence.
            """),
            section("Audit every neighboring square", """
                A king in the center has eight neighboring squares, but a king on e8 has only five: d8, f8,
                d7, e7, and f7. After Rh8 in the worked position, the rook controls d8 and f8 along the eighth
                rank. White's king on e6 controls d7, e7, and f7. None is a legal escape. A square occupied by
                a friendly piece is not available either, unless the king has a legal capture there—which it does
                not have against its own army. Do not omit a diagonal flight merely because the king seems
                pinned against an edge. Naming each candidate square is slower initially but builds a dependable
                checking habit you can later perform quickly.
            """),
            section("Test capture and block separately", """
                Covering flight squares is not enough if the checker can be taken or its line interrupted. In the
                example, Black's king on e8 is three files from the rook on h8, so it cannot capture it in one
                move. Black has no other pieces to capture the rook or interpose. Therefore the check is mate.
                Contrast a king on g8 facing an unprotected rook arriving on h8: that king could capture the rook,
                so the same-looking check would fail. Supporting pieces matter, but only in their actual geometry.
                Ask three independent questions—safe king move, capture of checker, block—and prove every
                answer fails. Checkmate ends the game immediately; Black does not get a final move to take
                something valuable elsewhere.
            """),
        ),
        (example("A rook mate with every escape accounted for", custom({"e6": "K", "h1": "R", "e8": "k"}), ("Rh8#",), (
            "White's king controls d7, e7, and f7. The rook has a clear h-file and Black has no other defenders.",
            "The rook checks along rank 8, taking d8 and f8. The distant king cannot capture h8, and no piece can block: all three defences fail.",
        )), example("Restriction without check is not mate", custom({"e6": "K", "h1": "R", "e8": "k"}), ("Rh7", "Kd8"), (
            "Reset the same position and try controlling rank 7 instead of checking along rank 8.",
            "Rh7 prevents a move onto rank 7, but does not attack e8. The move is not check, much less checkmate.",
            "Black steps to d8 legally. Naming this flight exposes the difference between confinement and mate.",
        ))),
        ("An unprotected checker beside the enemy king may simply be captured.",
         "A king with no safe flight is not necessarily mated; check, capture, and block all need testing."),
        (
            check("mate-checkfirst", "The king has no legal move but is not attacked, and no other piece can move. Is this mate?",
                  ("No; it is stalemate", True, "Check is essential to mate. No legal moves without check produces a draw."),
                  ("Yes; no king move always means mate", False, "This omits both the check requirement and possible moves by other pieces.")),
            check("mate-capture", "Your rook checks next to the king, but no friendly piece protects it. What must you examine?",
                  ("Whether the king can legally capture the rook", True, "A checker must survive every possible capture, not just restrict flights."),
                  ("Only the king's empty escape squares", False, "Capturing the checker is another independent defence.")),
        ),
        ("Prove that the king is checked.", "Name every possible flight square.", "Rule out capture and interposition before declaring mate."),
    ),
    "draw": guide(
        (23, 26),
        ("Separate impossible mate from mate that cannot be forced.", "Recognize draw claims and automatic modern draw rules."),
        (
            section("Material alone is not the whole result", """
                A draw gives each player half a point. With king against king, or king and a single bishop or
                knight against a lone king, no legal sequence can produce mate: there is no reason to continue
                searching for one. This differs from two knights against a lone king: a mate position exists, but
                it cannot be forced against correct defence. That ending is not automatically dead just because
                forcing mate is impossible. More pieces can even create mating possibilities by blocking their
                own king's escape squares. The book's contrasting diagrams teach this important distinction:
                assess all the pieces and their arrangement, not only the stronger side's nominal surplus.
            """),
            section("Opposition and agreement", """
                Kings facing each other with one square between them restrict one another's forward squares.
                This arrangement is called opposition. With only kings remaining it does not create a winning
                weapon; the game is still drawn. With pawns or mating pieces, the same geometry may be useful,
                which is why recognizing it now helps later endings. Players can also agree a draw, subject to
                the event's rules. Agreement is a result chosen by the players, whereas stalemate and a dead
                position have conditions on the board. Do not assume 'I cannot see a win' proves a draw or
                'I have more material' proves a win. First check for concrete threats and the actual ending conditions.
            """),
            section("Repetition and move-count rules", """
                The book introduces a claim when the same position occurs three times with the same player to
                move. Legal possibilities must match too: relevant castling and en-passant rights matter, and the
                occurrences need not be consecutive. Repeating a piece's route alone is insufficient if other pieces
                have changed. It also teaches the fifty-move claim: fifty moves by each player without a pawn
                move or capture, counting one White move plus one Black reply as a complete move. Any pawn
                move or capture resets that count. Under current FIDE rules, a correct claim is needed for these
                conditions; fivefold repetition or seventy-five such moves by each player is automatic, with checkmate
                on the final move taking precedence. Online platforms may implement claims for the players.
                Rule reference: [FIDE Laws, Articles 9.2–9.6](https://handbook.fide.com/chapter/e012023).
            """),
        ),
        (example("A cooperative repetition, not a forced perpetual", chess.STARTING_FEN, ("Nf3", "Nf6", "Ng1", "Ng8", "Nf3", "Nf6", "Ng1", "Ng8"), (
            "The initial position is the first occurrence. Both sides still have the same castling rights.",
            "White develops a knight. Nothing forces Black to copy it; this is a counting illustration.",
            "Black develops a knight too. The position differs from the starting snapshot.",
            "White returns the knight, but Black's knight remains on f6, so the initial position has not yet returned.",
            "Black returns its knight. The complete starting position occurs for the second time, with White to move.",
            "White repeats the first knight move, creating another occurrence of that intermediate position.",
            "Black repeats its reply. The other pieces and special rights remain unchanged.",
            "White returns again. One more black return will restore the complete initial snapshot.",
            "Black returns to g8. The initial position has now occurred three times, supporting a draw claim; no checking sequence forced this cooperation.",
        )),),
        ("Cannot force mate is different from no legal mate being possible.",
         "Fifty moves means fifty by each player, not fifty individual turns.",
         "A repeated board picture may differ legally if castling or en-passant rights changed."),
        (
            check("draw-knights", "Two knights versus a lone king cannot force mate. Does that make every such position automatically dead?",
                  ("No; legal mate positions exist with cooperation", True, "Failure to force mate is different from complete impossibility of mate."),
                  ("Yes; every ending that cannot force mate ends automatically", False, "Dead-position rules ask whether mate is possible by any legal sequence.")),
            check("draw-reset", "Which move resets the fifty-move count?",
                  ("Any pawn move or any capture", True, "Either event starts that no-pawn-move/no-capture count again."),
                  ("Any check", False, "A non-capturing check by a piece does not itself reset the count.")),
        ),
        ("Distinguish dead material from unforceable mate.", "Repetition includes side to move and relevant rights.", "Pawn moves and captures reset the move-count clock."),
    ),
    "perpetual-check": guide(
        (23, 26),
        ("Demonstrate a continuous checking cycle against every reply.", "Use repetition as a saving resource without confusing it with mate."),
        (
            section("A chain of checks needs a guarantee", """
                Perpetual check describes an attack in which checks can continue indefinitely despite the defender's
                choices. One check, or even two, does not establish it. The king might reach shelter, a piece
                might interpose, or the checking queen might be captured. To prove a perpetual, examine every
                legal response at each stage and show another safe check after each. If the same full position
                recurs with the same player to move, you have a cycle you can inspect directly. In modern play
                the draw is normally secured through repetition rules rather than a separate automatic rule
                triggered merely by announcing that your intention is to keep checking.
            """),
            section("The defending side's own pawns form the cage", """
                In the example Black has a king on c5 and queen on f2. White has Kh1, Qh4, and pawns on
                g3 and h3. Black is two pawns behind, but can check from f1. White's king cannot capture the
                distant queen or block the adjacent-rank checking line with its own pieces. Its pawns occupy
                g3 and h3, helping restrict the king after it reaches h2. The white queen is trapped behind the
                h3 pawn for the required defensive task. After ...Qf1+, Kh2 is the only legal reply; ...Qf2+
                then forces Kh1. The black king is not doing the checking, but its safety still matters: a legal
                checking move must never expose it to an enemy attack.
            """),
            section("Preserve the resource instead of chasing material", """
                The two checking squares matter because each denies the exits available against the other.
                A tempting ...Qh2+ is quite different: White can capture that unprotected queen with Kxh2.
                Therefore 'it is check' is not a sufficient reason to select a move. When behind, search for
                perpetuals before resigning, and when ahead, ask whether your opponent can force one before
                taking another pawn. A draw saved from a worse position is useful even though it is not a win.
                In the replay, count the initial snapshot as the first occurrence and observe the exact returns.
                This is stronger evidence than assuming a lone king can always be chased by a queen: an open
                board often gives the king choices, whereas this particular cage makes the replies forced.
            """),
        ),
        (example("The f1–f2 checking cycle", custom({"h1": "K", "h4": "Q", "g3": "P", "h3": "P", "c5": "k", "f2": "q"}, turn="b"), ("Qf1+", "Kh2", "Qf2+", "Kh1", "Qf1+", "Kh2", "Qf2+", "Kh1"), (
            "Black to move. This is the first occurrence of the complete position; Black can force the cycle.",
            "The queen checks across rank 1 and controls g2 diagonally, leaving only Kh2.",
            "White's sole legal reply is Kh2; its pawns and the queen's attacks remove the other destinations.",
            "Black checks across rank 2. The same pawns prevent escape upward, while g1 is also attacked by the queen.",
            "White must return to h1. The initial position, Black to move, has occurred a second time.",
            "Black repeats the safe check from f1 instead of sacrificing the queen on h2.",
            "Kh2 is again forced; no new defender has appeared because White had no free turn to rearrange pieces.",
            "The queen returns to f2 with check, recreating the same restriction of the king.",
            "Kh1 restores the initial position for the third time. The repetition condition for a draw claim has been reached.",
        )),),
        ("Any first check does not prove a perpetual; every defensive reply needs an answer.",
         "An attacked king that always has a legal reply is not checkmated."),
        (
            check("perpetual-proof", "What proves a checking cycle is forced?",
                  ("Every legal defensive reply leads to another safe check and a repeated position", True, "The defender must have no route to shelter or capture that breaks the chain."),
                  ("The queen can give one distant check", False, "One checking move does not show what happens after the king escapes.")),
            check("perpetual-result", "You are behind but can force a legal threefold repetition and claim correctly. What have you secured?",
                  ("A draw", True, "Perpetual checking can save half a point without producing mate."),
                  ("A win because every move gives check", False, "Checks alone do not score a win; checkmate has no legal reply.")),
        ),
        ("Check every reply, not just the one you expect.", "Keep the checker safe on each move.", "Use the exact repeated position to justify the draw."),
    ),
    "stalemate": guide(
        (23, 26),
        ("Recognize stalemate using all the player's pieces.", "Use stalemate both as a danger when winning and a resource when losing."),
        (
            section("No legal move, and no check", """
                Stalemate occurs when the player to move is not in check and has no legal move with any piece.
                The game immediately ends as a draw. A king with no safe destination is not enough if that
                player can move a pawn or another piece. Conversely, pieces may appear to have movement but
                be pinned so that every attempted move would expose their king; those are not legal alternatives.
                Always identify whose turn it is and test check first. Check plus no legal move is mate. No
                check plus no legal move is stalemate. A quiet move that fills the last escape square may therefore
                change a winning position into a draw rather than bring the king closer to defeat.
            """),
            section("Avoid taking every square without checking", """
                Against a lone king, queens are especially prone to accidental stalemate because they control so
                many directions. Before moving, imagine the resulting position from the enemy king's seat and
                name at least one legal reply unless your move gives mate. In the quiz, Qa7 checks and is
                protected by White's king on a6, so Black cannot capture it and has no flight. Qb6 instead
                covers a7, b7, and b8 without checking a8: the result is stalemate. A board edge contributes
                to the confinement, but does not change the rule. Do not rely on the word 'corner' as a verdict;
                check the actual attacks and whether any other piece can move.
            """),
            section("A losing player may offer a piece to disappear", """
                The defender can sometimes arrange stalemate by giving away its last movable piece. In the
                worked example White's king is trapped on h1, but the rook can still move, so White is not
                stalemated yet. Rg3+ offers that rook to Black's king. If Black captures it, White has no legal
                move and is not checked, so the material advantage produces only a draw. Black may decline
                the capture, which is why a sound saving combination must examine those replies too. Here
                Rg3+ Kh4 is answered by Rg4+. Keep the rook on the g-file, level with the king on the h-file.
                The king cannot cross that file without capturing the rook and leaving White stalemated.
                This connects stalemate to perpetual check. When
                winning, look for this resource before accepting a sacrifice; when losing, inspect your own legal
                moves and ask what would happen if your final active piece vanished.
            """),
        ),
        (example("Capture the last active piece and concede stalemate", custom({"h1": "K", "g6": "R", "h3": "k", "a2": "q", "h8": "b", "h2": "p"}), ("Rg3+", "Kxg3"), (
            "White to move. The king has no legal move, but the rook can move, so the initial position is not stalemate.",
            "White checks and offers the rook. Black can decline with Kh4; the displayed capture is one branch, not a forced reply.",
            "The rook disappears. White's king on h1 is not checked, but g1 is attacked by the h2 pawn, g2 by the queen and king, and h2 is protected. White has no legal move: stalemate.",
        )), example("If Black refuses the rook, keep the g-file checks", custom({"h1": "K", "g6": "R", "h3": "k", "a2": "q", "h8": "b", "h2": "p"}), ("Rg3+", "Kh4", "Rg4+", "Kh3", "Rg3+", "Kh4", "Rg4+", "Kh3", "Rg3+"), (
            "Reset the same position. Now examine the alternative to capturing the offered rook.",
            "Rg3+ gives the first check and offers the rook. Capturing it would stalemate White.",
            "Black declines with Kh4. White must keep the king on the h-file rather than choose an arbitrary check.",
            "Rg4+ matches the king's rank while keeping the g-file barrier. Kxg4 would again stalemate White.",
            "Black chooses Kh3. Kh5 was also legal and would be met by Rg5+ using the same rule.",
            "Rg3+ restores the first checking position. White's confined king still has no independent move.",
            "Black again declines the rook. The moves are not all forced; the drawing mechanism answers the alternatives too.",
            "Rg4+ keeps the same barrier and stalemate offer instead of allowing the king across the g-file.",
            "Black returns to h3 again. A capture on g4 would end the game by stalemate instead.",
            "Rg3+ restores this checking position for the third time, supporting a repetition claim. The rook's precise file is the useful pattern.",
        )), example("Choose mate instead of stalemate", custom({"a8": "k", "a6": "K", "c5": "Q"}), ("Qa7#",), (
            "White's king protects a7 and b7, preparing a safe queen check.",
            "Qa7 checks from a protected square. The king on a8 has no flight or capture, so the game ends in mate rather than a draw.",
        ))),
        ("A motionless king is not stalemate if another piece has a legal move.",
         "Giving away your last movable piece can be a saving idea, but the opponent may decline it."),
        (
            check("stale-pawn", "The king is not in check and cannot move, but its pawn can advance legally. Is the position stalemate?",
                  ("No; the pawn supplies a legal move", True, "Stalemate requires no legal move by any piece."),
                  ("Yes; only king moves are relevant", False, "All of the player's pieces and pawns must be considered.")),
            check("stale-sac", "You are winning material and can capture the opponent's last active rook. What should you check first?",
                  ("Whether the remaining position leaves the opponent stalemated", True, "Removing the only movable piece may force a draw."),
                  ("Only how much material the capture wins", False, "A game-ending stalemate makes the material count irrelevant.")),
        ),
        ("Identify the player to move and test check first.", "Count legal moves by the whole army.", "Inspect stalemate before confining a king or taking its last active piece."),
    ),
    "castling": guide(
        (26, 27),
        ("Carry out both castlings with either color.", "Apply the king-path tests without inventing restrictions on the rook."),
        (
            section("Two pieces change squares in one turn", """
                Castling is a single king move that also relocates one rook. Move the king two squares toward
                that rook, then place the rook on the square the king crossed. White's kingside castle is Ke1–g1
                and Rh1–f1, written O-O. White's queenside castle is Ke1–c1 and Ra1–d1, written O-O-O.
                Black uses the same files on rank 8: king to g8 and rook to f8, or king to c8 and rook to d8.
                The king always travels two squares, although the queenside rook travels farther than the kingside
                rook. Castling can help shelter the king and bring a rook toward central action during the same turn.
            """),
            section("Rights and empty squares", """
                The king and the chosen rook must never have moved. Returning either to its starting square
                does not restore the lost right. Moving one rook does not by itself remove the option of castling
                with the other, provided the king and that other rook retain their rights. Every square between
                king and chosen rook must be empty, including b1 or b8 for queenside castling, even though the
                king does not cross that square. A promoted rook cannot replace an original rook's lost right.
                Read the history supplied with a study; the visible home-square arrangement alone cannot prove
                that castling remains available. Each side can castle at most once because its king then has moved.
            """),
            section("Test the king's three squares, not every rook square", """
                The king may not castle while in check, pass through an attacked square, or finish on one.
                For White kingside, test e1, f1, and g1; for queenside test e1, d1, and c1. Black uses the
                corresponding eighth-rank squares. The rook may be under attack, and on the queenside it may
                cross an attacked b-file square: those facts alone do not forbid castling. All intervening squares
                must still be empty. This distinction prevents two opposite errors—castling through an attack on
                the king's path, and refusing a legal castle because only the rook is threatened. Castling is not
                a way to answer check. Nor is it guaranteed safety: after a legal castle, continue checking which
                files and diagonals the opponent can open against your new king position.
            """),
        ),
        (example("White castles short; Black castles long", custom({"e1": "K", "a1": "R", "h1": "R", "e8": "k", "a8": "r", "h8": "r"}, castle="KQkq"), ("O-O", "O-O-O"), (
            "Both kings and all rooks have their original castling rights. Paths are empty and neither king's required squares are attacked.",
            "White's king reaches g1 and rook reaches f1 in one turn. The a1 rook remains in place.",
            "Black's king reaches c8 and a8 rook reaches d8. The king did not travel to b8, but b8 still had to be empty for the rook's path.",
        )), example("An attacked rook does not prevent castling", custom({"e1": "K", "h1": "R", "a8": "k", "b7": "b"}, castle="K"), ("O-O",), (
            "The bishop on b7 attacks the rook on h1 along c6–d5–e4–f3–g2–h1. It does not attack e1, f1, or g1.",
            "White legally castles: only the rook was under attack, and all king-path conditions are satisfied.",
        ))),
        ("Moving back home does not recover castling rights.",
         "Queenside b1/b8 must be empty but need not be unattacked.",
         "An attacked rook may castle with its king; a checked king may not."),
        (
            check("castle-return", "Your king moved earlier and returned to e1. May you castle now?",
                  ("No; the king's first move permanently removed the right", True, "Returning home does not undo the movement history."),
                  ("Yes, if e1 and the rook square look normal", False, "Castling rights depend on whether the king has ever moved.")),
            check("castle-rook", "Only your h1 rook is attacked; e1, f1, and g1 are safe, the path is empty, and rights remain. Is O-O legal?",
                  ("Yes", True, "An attack on the rook alone does not violate a king-path condition."),
                  ("No; every square of both pieces must be unattacked", False, "The special attacked-square restriction applies to the king's start, crossing, and destination.")),
        ),
        ("King two squares toward rook; rook onto the crossed square.", "Rights must remain and the whole gap must be empty.", "Never out of, through, or into check."),
    ),
    "algebraic-notation": guide(
        (28, 34),
        ("Read numbered game scores and the book's principal symbols.", "Replay a short game and explain the final mate.", "Distinguish legal rule practice from deliberately artificial entertainment."),
        (
            section("Decode one move", """
                Standard algebraic notation gives the destination, prefixed by K, Q, R, B, or N for a piece.
                A pawn's quiet move uses only its destination, such as e4. A capture adds x; a pawn capture
                includes its origin file, as in exd5. Check uses + and mate #. Promotion adds the chosen piece,
                for example axb8=Q+; castling uses O-O or O-O-O. The book may print piece figurines instead
                of letters and may show double check with a doubled check symbol; normal modern SAN often
                simply uses +. Long notation, such as e2-e4, also includes the origin. It is readable, but the
                shorter standard form avoids information that the position already makes clear.
            """),
            section("Resolve ambiguity and track turns", """
                If two legal pieces of the same type can reach one destination, the score must identify which
                moves. Rooks on a1 and f1 that can both reach d1 are distinguished as Rad1 and Rfd1.
                Knights on a2 and a4 that can both reach c3 use N2c3 and N4c3 because their shared file
                cannot distinguish them. A piece that is pinned and cannot legally reach the target does not
                create ambiguity. A move number normally contains White's move followed by Black's reply:
                '1. e4 e5 2. Nf3 Nc6'. An isolated black move uses an ellipsis, as in '2...Nc6'. After every
                entry, update the board and switch the player to move before reading onward.
            """),
            section("Read comments and evaluations as guidance", """
                An exclamation mark ! labels a good move and !! an exceptional one; ? marks a mistake and
                ?? a serious blunder. The mixed signs !? and ?! usually suggest an interesting possibility and
                a doubtful choice respectively. These are annotations, not part of the legal move's identity.
                Evaluation signs describe the position: = suggests equality, ± or ∓ a clear advantage for White
                or Black, +− or −+ a decisive advantage, and ∞ uncertainty. Slight-advantage and compensation
                symbols vary with typography, so read the accompanying explanation rather than guessing from
                a blurred character. 'With compensation' means benefits such as activity or attack may offset
                material loss; it does not promise that the sacrifice works. Use the board to test the author's claim.
            """),
            section("Use the short games as complete cause-and-effect stories", """
                Start from the normal position, play every move in order, and pause before the final attack.
                Ask what the last move weakened, which diagonal or file opened, and how the defender could
                have prevented the immediate threat. In the first worked game, moving the f- and g-pawns exposes
                the e1–h4 diagonal; the black queen then mates on h4. In the second, the e7 knight blocks
                Black's king and the knight on d6 gives a check that cannot be blocked. These examples teach
                different mating mechanisms, not opening recipes to repeat blindly. Reviewing a winning miniature
                should include the loser's earlier alternatives; a quick result often reflects several preventable
                errors rather than a generally sound attacking plan.
            """),
            section("Rule puzzles and historical jokes", """
                The entertainment pages reinforce castling, en passant, promotion, discovered checks, confinement,
                and the importance of whose turn it is. Reuse those ideas by explaining the special-rule examples
                in this chapter without looking at their answers, then deliberately changing one condition and
                predicting the result. Some historical puzzles are jokes: a half-completed castling move is not
                a separate legal turn, ten enemy kings cannot occur in a game, and an impossible position may
                be presented expressly for amusement. Do not learn those exceptions as ordinary rules. Two useful
                geometric challenges remain eight mutually nonattacking queens and thirty-two nonattacking knights
                on all squares of one color. The knight color-change rule explains the latter. Longer composed
                lines are optional enrichment; understanding each rule and verifying the final position comes first.
            """),
        ),
        (example("Read the complete shortest mate", chess.STARTING_FEN, ("f3", "e5", "g4", "Qh4#"), (
            "Start with all pieces in their normal places. Read one move at a time; the bad white pawn moves are warnings, not recommendations.",
            "White moves f2–f3, clearing f2 on the diagonal leading from h4 toward e1.",
            "Black's e-pawn leaves e7, opening the queen's route d8–e7–f6–g5–h4.",
            "White moves g2–g4, so g3 is empty too. The e1–f2–g3–h4 diagonal is now exposed.",
            "The queen checks on that diagonal. White cannot capture her, block on f2 or g3, or move the boxed-in king to a safe square: mate.",
        )), example("A knight gives smothered mate", after(("e4", "c5", "Nf3", "Nc6", "d4", "cxd4", "Nxd4", "e5", "Nf5")), ("Nge7", "Nd6#"), (
            "Black to move. The white knight on f5 can jump to d6; inspect the black king's own surrounding pieces.",
            "Black develops the g8 knight to e7, occupying a square the king might otherwise need and failing to meet the threat.",
            "Nd6 checks by a jump. No black piece can capture the protected knight, the check cannot be blocked, and Black's own pieces confine the king: smothered mate.",
        ))),
        ("The + or # must describe the actual result; writing a suffix cannot create check or mate.",
         "Move-quality marks such as ! and ? comment on a move; they do not alter its movement rule.",
         "A deliberately impossible joke diagram is not evidence that extra kings or half-turn castling are legal."),
        (
            check("notation-pawn", "What does exd8=N+ record?",
                  ("An e-file pawn captures on d8, promotes to a knight, and gives check", True, "The origin file, x, destination, promotion piece, and + each supply one part of the move."),
                  ("A knight on the e-file moves to d8 without a capture", False, "A knight move begins with N; ex records a pawn capture, and =N records promotion.")),
            check("notation-rank", "Two legal knights on a2 and a4 can both move to c3. How do you identify the a4 knight?",
                  ("N4c3", True, "The origin rank distinguishes the knights because both share the a-file."),
                  ("Nac3", False, "Both knights stand on the a-file, so that file alone does not resolve the ambiguity.")),
            check("notation-number", "In '1. e4 e5 2. Nf3 Nc6', which is Black's second move?",
                  ("Nc6", True, "Each numbered pair contains White's move and then Black's reply."),
                  ("Nf3", False, "Nf3 is White's second move, the first entry after move number 2.")),
        ),
        ("Decode destination, capture, check, promotion, and ambiguity.", "Replay every turn and verify the final position.", "Read annotations critically and distinguish rule practice from jokes."),
    ),

}
