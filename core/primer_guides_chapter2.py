"""Original teaching guides mapped to printed pages of the user's primer.

Examples are connected legal lines, not an assertion that the defender has only
one reply. Notes distinguish a forced move from a representative legal reply.
"""

from core.primer_build import custom


def _section(title, body):
    return {"title": title, "body": " ".join(body.split())}


def _example(title, pieces, start_note, line, turn="w"):
    return {
        "title": title,
        "fen": custom(pieces, turn=turn),
        "moves": tuple(san for san, _ in line),
        "notes": (start_note,) + tuple(note for _, note in line),
    }


def _check(check_id, prompt, answer, why, wrong_a, why_a, wrong_b, why_b):
    return {
        "id": check_id, "prompt": prompt,
        "options": (
            {"text": answer, "correct": True, "explanation": why},
            {"text": wrong_a, "correct": False, "explanation": why_a},
            {"text": wrong_b, "correct": False, "explanation": why_b},
        ),
    }


def _guide(pages, goals, sections, examples, pitfalls, checks, recap):
    return dict(pages=pages, goals=goals, sections=sections, examples=examples,
                pitfalls=pitfalls, checks=checks, recap=recap)


GUIDES = {
    "mate-on-the-edge": _guide(
        (35, 38),
        ("Explain why the edge helps the attacker.", "Account for every escape in a mating net."),
        (
            _section("The board removes escape squares", """
Imagine an otherwise empty board and count the squares next to a king. In the middle there are eight. Along an edge there are five, and in a corner there are three. A defending king cannot retreat beyond the board. This is why the chapter's first mating pictures repeatedly put the defender on an outside rank or file. You still have work to do: an edge king with even one safe flight is not mated. Think of the boundary as part of your net, then identify which friendly piece or enemy blocker removes each remaining route. This counting habit is more reliable than recognizing a familiar-looking picture.
"""),
            _section("Give each piece a job", """
In the worked position Black stands on g8. White's king on g6 does not check him: kings cannot attack one another across an empty rank. Instead it forbids f7, g7 and h7. The queen's job is to give check along the eighth rank, also covering f8 and h8. Those two jobs complement each other. Moving the white king away would leave a hole; moving the queen to a different checking diagonal could leave sideways flights. Say the jobs aloud before you choose a move. This also explains why a stronger piece alone is not the same as a completed mating net.
"""),
            _section("Verify rather than guess", """
After a candidate check, inspect three kinds of reply. Can the king move to a safe square? Can he or another piece capture the checker? Can a piece block the checking line? Our simple example has no defending piece that could capture or block, but normal games often do. A knight check cannot be blocked; a distant rook or queen check sometimes can. The defender's own pawns can help the attacker by occupying escape squares, as the chapter's back-rank pictures show. Practice both with and without those blockers, and include positions where an apparently similar check leaves one flight. The important result is being able to explain why mate is forced.
"""),
        ),
        (_example("A distant queen check completes the net", {"g8":"k","g6":"K","d1":"Q"},
                  "Black has five neighboring board squares; Kg6 already forbids the three on rank seven.",
                  (("Qd8#", "The queen checks g8 along rank eight and covers f8 and h8. No capture, block or flight exists."),)),),
        ("The edge reduces mobility; it does not automatically make a check mate.",
         "Name the controller of every flight instead of assuming your queen covers everything."),
        (
            _check("edge-flights", "How many neighboring board squares does a king in a corner have?", "Three", "Two orthogonal neighbors and one diagonal neighbor remain on the board.", "Five", "Five is the count on a non-corner edge.", "Eight", "Eight applies to an interior square."),
            _check("edge-jobs", "After Qd8#, why can Black not move to h7?", "Kg6 controls h7", "The supporting king closes that forward flight.", "The board has no h7 square", "h7 exists; h9 would be beyond the board.", "Every queen check is mate", "Other queen checks leave legal flights."),
        ),
        ("Drive the defender toward a boundary.", "Assign a piece or blocker to every remaining flight.", "Check captures and blocks before declaring mate."),
    ),
    "queen-mates": _guide(
        (37, 39),
        ("Recognize distant and protected-adjacent queen mates.", "Distinguish a protected queen from a capturable queen."),
        (
            _section("Two finishes to recognize", """
The queen combines rook lines with bishop diagonals, so she can deliver mate in several shapes. Start with two useful pictures against a bare king. In a distant edge mate, the queen checks along the edge while her own king controls the squares in front of the defender. In a protected-adjacent mate, the queen checks from a neighboring square and her king prevents capture. The chapter illustrates both close cooperation and distant control. Memorize the relationship of the pieces, then test it on another file or with colors reversed. Memorizing only the destination d8 would miss a perfectly valid mate on g7 in our practice position.
"""),
            _section("Why a king cannot take a protected queen", """
The king moves only one square and may capture an enemy piece only if the destination is not attacked. With White Kg6 and Qg7 against Black Kg8, taking the queen would place the black king on a square attacked by Kg6. That capture is illegal even though the queen is next door. Without the supporting white king, the same apparent mating check could simply lose the queen. Before playing a close check, locate the defender of the queen explicitly. Protection by a pinned piece or by a king that is too far away needs careful thought in more complicated positions; here Kg6's control is direct.
"""),
            _section("Several correct moves may exist", """
From the exercise position both Qd8 and Qg7 mate. One works from a distance; the other uses direct protection. A task that asks for any checkmate must accept both. Checkmate is a fact about the resulting position, not a preferred style of move. Compare Qd5: it gives check, but the defender can move to f8 or h8, so it is not mate. Use the same check-capture-block-flight routine for all three candidates. Then set up a similar queen position with the white king one square farther away and ask which mating picture survives. This comparison reveals what the supporting king actually contributes and helps prevent accidental queen losses.
"""),
        ),
        (
            _example("A protected queen finishes at close range", {"g8":"k","g6":"K","d4":"Q"},
                     "White can choose either mating pattern. This line uses the queen beside the king.",
                     (("Qg7#", "Qg7 checks Kg8; Kg6 protects g7 and covers f7 and h7, while the queen covers f8 and h8."),)),
            _example("The same position also permits distant mate", {"g8":"k","g6":"K","d4":"Q"},
                     "The pieces have not changed. A different correct finish is available.",
                     (("Qd8#", "The eighth-rank check seals f8 and h8 while Kg6 seals the seventh-rank flights."),)),
        ),
        ("A neighboring queen is safe only if the king cannot legally capture her.",
         "A different mating square is still correct when the task asks for any mate."),
        (
            _check("queen-protection", "What makes Qg7# safe from Kxg7?", "White's king attacks g7", "Kings cannot capture onto attacked squares.", "Queens cannot be captured", "Queens can be captured like other pieces when the capture is legal.", "A checking piece is immune", "Capturing the checking piece is a standard way to escape check."),
            _check("queen-alternatives", "If two legal moves both checkmate, how should an any-mate task treat them?", "Accept both", "Both satisfy the stated objective.", "Accept only the first listed move", "A whitelist would reject a genuine mate.", "Accept only the closer queen move", "Distance does not determine whether the position is mate."),
        ),
        ("Use the distant edge pattern.", "Use the protected-adjacent pattern.", "Verify the board result, including alternative mates."),
    ),
    "rook-mates": _guide(
        (35, 36),
        ("Explain the supporting king's role in rook mate.", "Check whether an apparently unprotected rook is actually capturable."),
        (
            _section("A rook needs help with the front", """
A rook attacks along its rank and file. It does not attack the diagonally neighboring squares that a queen would cover. When a bare king is on the eighth rank, a rook checking along that rank removes sideways movement, but the seventh rank may remain available. The attacking king supplies that missing control. In our corner example Kg6 controls g7 and h7, and Ra8 checks Kh8 from a distance. Neither white piece is doing the entire job alone. The chapter also shows positions where the defender's own pieces block some flights; always inspect what fills each square rather than assuming the supporting piece must be a king.
"""),
            _section("Distance can keep the rook safe", """
An unprotected piece is not automatically lost. From h8 a king can reach g8, g7 or h7 in one move, not a8. A rook checking from a8 is therefore safe from an immediate king capture despite having no white piece defend a8. If the king later walks toward that rook, relocate it to a safe distance. This is a practical habit throughout rook endings. Check the king's actual one-square reach and the destination's protection. Statements such as 'the rook is on his rank, so he can take it' ignore the distance that makes the standard rook mate work in the first place.
"""),
            _section("Distinguish a barrier from the final check", """
Ra7 in the exercise is a useful kind of barrier, but it is not checkmate because Kh8 is not checked and can still move along the eighth rank. The final Ra8 turns the rook's control into a checking line while Kg6 prevents descent to the seventh. Before moving, list g8, g7 and h7. After Ra8, g8 is on the rook's line; g7 and h7 are controlled by the white king. There is no other black piece to block or capture. That short explanation is the proof of mate. Later, the complete rook-method lesson shows how to create this kind of arrangement from a defender in the center rather than starting one move before the finish.
"""),
        ),
        (_example("Rook and king divide the escape squares", {"h8":"k","g6":"K","a4":"R"},
                  "The rook's route to a8 is clear, and Kg6 already controls g7 and h7.",
                  (("Ra8#", "The rook checks horizontally. Black cannot reach a8, cannot stay on rank eight, and cannot escape to rank seven."),)),),
        ("Rooks have no diagonal control; count the front flights separately.",
         "Unprotected and capturable mean different things when the enemy king is far away."),
        (
            _check("rook-front", "Which piece prevents Kh7 after Ra8# in this example?", "The white king on g6", "Kg6 attacks h7 directly.", "The rook on a8", "Ra8 attacks rank eight and the a-file, not h7.", "The black king's own pawn", "There is no black pawn in this position."),
            _check("rook-distance", "Can Kh8 capture a rook on a8 immediately?", "No, the rook is far beyond one king step", "The king moves only one square.", "Yes, because both are on rank eight", "Sharing a rank does not give a king rook-like movement.", "Yes, because the rook is unprotected", "Lack of protection does not change the king's movement rule."),
        ),
        ("The rook controls the checking rank or file.", "The king controls the front flights.", "Keep the rook outside the defender's actual capture range."),
    ),
    "two-rook-mates": _guide(
        (35, 40),
        ("Execute the alternating rook barrier and check.", "Relocate a rook when the king approaches it.", "Explain each rook's separate job at mate."),
        (
            _section("Build a staircase of barriers", """
Two rooks can drive a lone king to an edge while their own king stays out of the operation. One rook cuts off a rank. The other checks on the rank above it, so the defender must retreat instead of crossing the barrier. Next the rooks exchange jobs. Think in terms of a staircase: each check takes away a strip of board and moves the defender closer to the boundary. This is often called the ladder method. The same basic cooperation works along files, and a queen and rook can use a similar pattern. Learn the alternating jobs rather than one memorized board orientation.
"""),
            _section("Safety comes before another check", """
The defender does not have to walk straight backward. He may head toward an exposed rook. In our full example the black king goes to c7 and then b7, bringing a6 into capture range. White moves the rooks sideways to h5 and g6 before resuming the checks. Those quiet moves are part of the method, not wasted time. A rook's checking power is useless after it is captured. Keep a safe distance, make sure the other rook still forms a barrier, and then continue the climb. The worked replies illustrate one route; a different legal defence requires the same checks of distance, barrier and remaining flights.
"""),
            _section("Understand the final position", """
In the separate one-move exercise Ra7 covers the entire seventh rank, including g7 and h7. Rb8 then checks Kh8 along the eighth rank. The rook on a7 does not protect b8; that would require a diagonal attack, which rooks do not have. Rb8 is safe because Kh8 cannot travel six files in one king move. If you instead play Ra8, you remove the seventh-rank barrier and leave forward escapes. If you play Rg1, you may close every flight without giving check and stalemate. For each candidate, check the resulting board instead of saying vaguely that the rooks are supporting one another. Cooperation means complementary jobs, not necessarily direct protection.
"""),
        ),
        (_example("A full ladder, including safe sideways moves", {"f4":"k","h1":"K","a2":"R","b3":"R"},
                  "The defender is central. White's king will remain on h1 throughout the demonstration.", (
                      ("Ra4+", "The a-rook checks on rank four; Rb3 prevents the king dropping to rank three."),
                      ("Ke5", "Black retreats one rank. This is a representative reply, not the only legal one."),
                      ("Rb5+", "The b-rook takes over checking while Ra4 closes rank four."),
                      ("Kd6", "Black retreats again and starts moving toward the a-rook."),
                      ("Ra6+", "The a-rook climbs to rank six; Rb5 provides the lower barrier."),
                      ("Kc7", "Black moves toward a6. Rook safety will soon matter more than immediate checking."),
                      ("Rh5", "The b-rook shifts to a distant file while still controlling rank five."),
                      ("Kb7", "Black now attacks the rook on a6, so White must move that rook."),
                      ("Rg6", "The threatened rook escapes to g6, preserving the rank-six barrier."),
                      ("Kc7", "Black remains above that barrier and cannot break back through rank six."),
                      ("Rh7+", "The h-rook resumes the ladder, checking on rank seven."),
                      ("Kd8", "The defender reaches the edge; rank seven is still closed."),
                      ("Rg8#", "The g-rook checks on rank eight and Rh7 covers every downward flight. The distant white king was unnecessary."),
                  )),),
        ("A rook does not protect a diagonally neighboring rook.",
         "Move a threatened rook before continuing the ladder.",
         "A non-check that removes every move is stalemate, even with two rooks."),
        (
            _check("ladder-king", "Must your king join the two-rook ladder against a lone king?", "No, the rooks can supply both barriers", "Their rank and file control can force mate without the king.", "Yes, every mate needs king support", "Queen and rook or two rooks can mate independently.", "Only if the defender starts in the center", "The ladder is designed to drive a central king to the edge."),
            _check("ladder-jobs", "What does Ra7 contribute when Rb8 mates Kh8?", "It covers g7 and h7", "Those forward flights are closed by the seventh-rank barrier.", "It protects b8 diagonally", "Rooks have no diagonal attack.", "It checks the king on h8", "Ra7 does not attack h8; Rb8 gives the check."),
        ),
        ("Alternate barrier and checking rook.", "Relocate safely when the king approaches.", "Verify the edge check and the lower barrier at the finish."),
    ),
    "minor-piece-and-pawn-mates": _guide(
        (37, 38),
        ("Recognize bishop, knight and pawn delivered mates.", "Separate the checking piece from the pieces closing flights.", "Identify smothered mate and quiet stalemate."),
        (
            _section("Who checks and who closes the exits?", """
A piece can deliver mate even when it could not force mate with only its king for company. A bishop attacks one square color, so another piece must close any surviving flights on the other color. A knight jumps to give check while other pieces or blockers cover the king's destinations. The chapter's patterns deliberately divide these jobs. Do not confuse the piece that gives the final check with the entire force responsible for mate. In the practice net Nc7 checks a8, Ba7 controls b8, and Kb6 closes a7 and b7. All three contributions matter; removing one can change the result.
"""),
            _section("Blockers can belong to either side", """
A smothered mate occurs when a knight checks a king whose own men occupy the escape squares. The knight can jump over those blockers, and its check cannot be interposed against. In the example Kh8 is hemmed in by Rg8 and pawns on g7 and h7. Nf7 gives mate despite being far from White's king. Those black pieces are not protecting their king effectively; they are occupying the very squares he needs. This is why counting material alone cannot tell you whether a mating attack exists. Inspect the king's space and which pieces are free to capture the checker or move out of its attack.
"""),
            _section("Pawns can checkmate before promotion", """
A pawn gives check diagonally, not forward. It can therefore deliver a final mate without becoming a queen when the other flights are already closed. Our pawn example uses two white pawns and a supporting king; b7 checks c8 while Pc7 and Kc6 cover the exits. Promotion is unnecessary because the game ends at once. By contrast, a quiet move can remove all mobility without checking and produce stalemate. In the knight practice position Nd6 and Na3 do exactly that. The bishop remains on dark squares a7 and b8; calling those light squares would obscure the color restriction that makes bishop cooperation important. Check the board's square colors as well as the attacking lines.
"""),
        ),
        (
            _example("A bishop delivers the check", {"a8":"k","b6":"K","d6":"B","c4":"B"},
                     "Bd6 controls b8 and Kb6 closes a7 and b7; the other bishop can deliver the diagonal check.",
                     (("Bd5#", "The bishop on d5 checks a8. Bd6 covers b8 and Kb6 controls the remaining flights."),)),
            _example("A smothered knight mate", {"h8":"k","g8":"r","g7":"p","h7":"p","g5":"N","a1":"K"},
                     "Black's own pieces occupy g8, g7 and h7. White only needs an unanswerable knight check.",
                     (("Nf7#", "The knight attacks h8. No blocker can stop a knight check, and the king has no free destination."),)),
            _example("A pawn mates without promoting", {"c8":"k","c6":"K","c7":"P","b6":"P","a5":"p"},
                     "Pc7 covers b8 and d8 while Kc6 covers b7, c7 and d7.",
                     (("b7#", "The b-pawn checks c8 diagonally. Every flight is occupied or attacked; no queen is needed."),)),
        ),
        ("A bishop or knight can deliver mate with extra help even though one minor piece cannot mate a bare king.",
         "A pawn attacks diagonally and can mate without promotion.",
         "Quiet knight moves in the practice position stalemate; the king does not escape."),
        (
            _check("minor-smothered", "What makes the example a smothered mate?", "Black's own pieces block the king's flights", "The knight jumps in while the king is hemmed in.", "A bishop covers every square color", "A bishop always remains on one color.", "The knight moves like a queen", "The knight still uses its ordinary jump."),
            _check("minor-pawn", "Does a pawn have to promote to give checkmate?", "No, its diagonal check can complete a mating net", "Other pieces can close the remaining flights first.", "Yes, pawns never give check", "Pawns attack diagonally and can check kings.", "Only if it moves backward", "Pawns cannot move backward."),
        ),
        ("Find the checker and the exit guards separately.", "Look for own-piece blockers around the king.", "Distinguish a checking finish from quiet stalemate."),
    ),
    "mating-method-queen": _guide(
        (38, 39),
        ("Restrict a central king with a useful queen barrier.", "Bring your king forward without causing stalemate.", "Complete the method through a verified mate."),
        (
            _section("First reduce space", """
A queen ending is won by making the defender's useful space smaller while keeping the queen safe. You do not need to check on every move. In this example Qd7 is a quiet move that takes away rank seven and keeps the black king below it. The queen also controls the d-file and helpful diagonals. A beginner often chases with unrelated checks; the king keeps changing direction and no stable progress results. Instead identify the boundary you have created, and avoid moving the queen so carelessly that the defender crosses it. The exact best move can vary with the starting position; this line teaches a reliable coordinated plan, not a claim that only one move wins.
"""),
            _section("Next bring the king into contact", """
Once the queen has limited the defender, White improves the king from e1 to f2, f3 and f4. Black's moves in the line are representative legal replies; they help you see how the method adapts as the kings approach. The king supports the final net and makes nearby squares unavailable. Keep the kings from becoming adjacent, since a king may never enter the other king's attack. The queen's long range lets her maintain the boundary while her partner travels. This is the moment to be patient: a useful king move can do more than another check. There is no requirement to make the white king capture anything or reach a particular memorized file.
"""),
            _section("At the edge, count legal replies", """
After Qe7 and Kh6, White has Kf4 and Black is nearly out of room. Qf7 would cover h7, g7, g6, g5 and h5 without checking h6: stalemate. White instead plays Kf5. That king move deliberately leaves Kh5 available and brings support closer. Allowing one safe reply is not a failure; it is how the attacker keeps the game alive while arranging the final check. The worked example then ends with Qh7 mate, and Qg5 would also mate. Both are correct because both satisfy the board conditions. Before every tight quiet queen move, ask what the opponent will legally play next, rather than merely asking how many squares your queen attacks.
"""),
            _section("Practice the method, not only the finish", """
Replay the entire line once while reading each note, then reset and explain the job of every white move before advancing. On a third pass, try a different legal black reply at an earlier point and preserve the same priorities: safe queen, smaller space, useful king, legal defender move until the final check. Do not conclude that a different black reply refutes the method simply because it leaves the displayed line. At the final checkpoint use the full mate test: check, no safe flight, no capture, no block. Later practice should start from several central king positions so that recognizing the process becomes easier than recalling this particular sequence of squares.
"""),
        ),
        (
            _example("From the center to a queen mate", {"e5":"k","e1":"K","d2":"Q"},
                     "White has a winning queen ending, but the black king is central. Start by making a useful barrier.", (
                         ("Qd7", "A useful quiet move: the queen cuts off rank seven and begins restricting the defender's region."),
                         ("Ke4", "Black approaches the white king. This legal reply illustrates why White must coordinate, not chase checks."),
                         ("Kf2", "White brings the king closer while keeping clear of Ke4's attacked squares."),
                         ("Ke5", "Black returns toward the center but remains below the queen's seventh-rank barrier."),
                         ("Kf3", "The supporting king advances another safe step and begins controlling central flights."),
                         ("Kf6", "Black moves toward the upper-right part of the available region."),
                         ("Kf4", "White's king gains control of e5, f5 and g5, helping drive the defender toward the edge."),
                         ("Kg6", "Black moves rightward rather than staying opposite the white king."),
                         ("Qe7", "The queen adjusts the boundary and controls the e-file while maintaining seventh-rank control."),
                         ("Kh6", "The defender reaches the edge. Care is now needed because a quiet queen move can stalemate."),
                         ("Kf5", "White improves the king and deliberately leaves Kh5 legal. Qf7 here instead would stalemate."),
                         ("Kh5", "Black uses the remaining flight. White now has the king support for a final check."),
                         ("Qh7#", "The queen checks down the h-file while Kf5 controls g4, g5 and g6. No defence remains; Qg5# also works."),
                     )),
            _example("The tempting quiet move that draws", {"h6":"k","f4":"K","e7":"Q"},
                     "The defender has almost no space. A move that removes every flight must check, or the game will draw.",
                     (("Qf7", "Black is not checked on h6, but h7, g7, g6, g5 and h5 are all attacked. This is stalemate."),)),
        ),
        ("Useful quiet queen moves can be better than checks.",
         "Do not place the queen beside the king without protection.",
         "Leave a legal reply while arranging the finish; remove it with check."),
        (
            _check("queen-method-quiet", "Why is the first move Qd7 useful even though it does not check?", "It builds a barrier and limits the king's space", "Restriction can make progress without check.", "Every quiet move forces the king to pass", "Black still makes a normal legal move.", "It immediately checkmates", "The defender still has many legal replies."),
            _check("queen-method-stalemate", "Why prefer Kf5 to Qf7 with Kf4, Qe7 and Kh6?", "Kf5 leaves Kh5 legal and prepares mate", "White improves support without ending the game in stalemate.", "Kings must move before queens", "There is no such move-order rule.", "Qf7 loses the queen to Kxf7", "The problem is stalemate, not a legal king capture."),
        ),
        ("Fence off space safely.", "Bring the king while preserving a legal defender move.", "Finish with a check that closes every exit."),
    ),
    "mating-method-rook": _guide(
        (38, 39),
        ("Use opposition to make a rook check force retreat.", "Use a waiting move when the defender avoids opposition.", "Follow a complete safe method to mate."),
        (
            _section("Why the king must help", """
A rook checking a central king often lets him step forward again. The attacker needs the supporting king to close those forward squares before the rook checks. When kings face each other with one empty square between them, their opposition creates a three-square barrier: the attacking king controls the three squares directly in front. A rook check across the defender's rank then forces him backward. The opening position has White Kd4 and Black Kd6. Ra6 checks from a safe distance, and Black cannot come to c5, d5 or e5. This explains the progress; the check alone does not explain it. The method works on files as well as ranks.
"""),
            _section("Follow, then force another retreat", """
After the first check the defender may sidestep rather than stand opposite the white king again. White follows with useful king moves, controlling the next strip of board. This may look slow, but the defender cannot freely regain all the space that has been cut off. In the long line, the kings eventually reach Kg5 and Kg7 in opposition. Ra7 then sends Black onto rank eight. Do not move your king adjacent to the enemy king; opposition includes an empty square. Also do not interpret the displayed black replies as compulsory at every turn. They illustrate how the attacker keeps the same relationship when the defender heads in a different direction.
"""),
            _section("The waiting move is part of the technique", """
On the last rank the defender can keep stepping sideways to avoid a convenient opposition picture. White can move the rook sideways on its barrier rank instead of destroying the barrier with an impatient check. In the example Rh7 preserves the seventh-rank fence and lets Black choose a king square; White then follows until the opposition is achieved. This is a waiting move with a concrete purpose, not a random shuffle. Keep the rook safely distant, because a nearby unprotected rook can be captured. An unprotected rook four files away cannot be captured immediately. Always inspect the actual king move and destination rather than assuming that sharing a rank makes the rook vulnerable.
"""),
            _section("Two complete examples, then independent practice", """
The long line is deliberately easy to explain rather than optimized for the fewest moves. It shows opposition, a retreating check, king pursuit, a waiting rook move and the final edge mate. The second line gives a shorter finish from a later position, showing how a rook fence and an advancing king can cooperate efficiently. Replay both and name the controlled flights before each check. Then reset a central king position and ask which barrier you will preserve while your king approaches. Your success criterion is a legal, safe progress toward mate, not matching a memorized move count. The lesson's final exercise asks for actual mate, so any genuine mating move should be accepted.
"""),
        ),
        (
            _example("A complete rook method with a waiting move", {"d6":"k","d4":"K","a2":"R"},
                     "The kings are in opposition. The rook can check from a safe distance and force a retreat.", (
                         ("Ra6+", "The rook removes rank six; Kd4 closes c5, d5 and e5, so Black must retreat."),
                         ("Kd7", "Black moves back one rank. Other replies require the same barrier-and-king reasoning."),
                         ("Kc5", "White approaches; if Black returns to c7, another rank check would drive him back."),
                         ("Ke7", "Black sidesteps to avoid facing White's king directly."),
                         ("Kd5", "White follows, controlling the squares in front of the defender."),
                         ("Kf7", "Black keeps moving sideways on the seventh rank."),
                         ("Ke5", "White continues the pursuit without giving an unhelpful rook check."),
                         ("Kg7", "Black moves toward the right-hand edge."),
                         ("Kf5", "The white king maintains its approach and controls g6."),
                         ("Kh7", "Black reaches the h-file but still has sideways room."),
                         ("Kg5", "White prepares opposition if Black returns to g7."),
                         ("Kg7", "The kings now face one another with g6 between them."),
                         ("Ra7+", "The rook checks on rank seven while Kg5 closes the forward sixth-rank squares."),
                         ("Kf8", "Black is driven onto the last rank."),
                         ("Kf6", "White approaches the edge king while the rook keeps rank seven closed."),
                         ("Ke8", "Black sidesteps to avoid immediate opposition."),
                         ("Rh7", "A waiting move preserves the barrier and leaves Black to choose a king square."),
                         ("Kd8", "Black moves left along the edge; rank seven is still forbidden."),
                         ("Ke6", "White follows, keeping the kings legally separated."),
                         ("Kc8", "Black continues along the edge."),
                         ("Kd6", "White continues to cover the forward strip."),
                         ("Kb8", "Black has fewer files left before reaching the corner."),
                         ("Kc6", "White stays close enough to meet the next sidestep."),
                         ("Ka8", "The defender reaches the corner but can still move back to b8."),
                         ("Kb6", "White takes the supporting position needed if Black moves to b8."),
                         ("Kb8", "Opposition is achieved: Kb6 closes a7, b7 and c7."),
                         ("Rh8#", "The rook checks across rank eight; the white king covers all rank-seven flights. No capture or block exists."),
                     )),
            _example("A shorter rook finish", {"h7":"k","f5":"K","a6":"R"},
                     "The defender is already near the edge, so White can build a closer fence.", (
                         ("Rg6", "The rook cuts off the g-file below the black king, while staying out of capture range."),
                         ("Kh8", "Black retreats into the corner; this is a representative defence."),
                         ("Kf6", "White approaches while Rg6 keeps the g-file closed."),
                         ("Kh7", "Black moves down the h-file but cannot cross the rook's fence."),
                         ("Kf7", "White now controls g7 and g8, preparing a check on the h-file."),
                         ("Kh8", "Black returns to the corner and has no way around the white king."),
                         ("Rh6#", "The rook checks along the h-file; Kf7 covers both g7 and g8. The method ends in checkmate."),
                     )),
        ),
        ("A check without king support may let the defender return forward.",
         "Waiting rook moves can preserve progress when an immediate check would not.",
         "Do not confuse an unprotected rook with one the king can actually reach."),
        (
            _check("rook-method-opposition", "Why does Ra6+ force retreat with Kd4 facing Kd6?", "Kd4 controls c5, d5 and e5", "The supporting king closes every forward flight from the checked rank.", "A rook check always forces backward movement", "Without those controls a king can often step forward.", "Black must move two squares when checked", "A king still moves one square."),
            _check("rook-method-wait", "What is the purpose of Rh7 in the long worked line?", "Keep the seventh-rank barrier while waiting for a useful king arrangement", "White preserves the fence and lets Black commit to a square.", "Give check immediately", "Rh7 is deliberately a non-check.", "Sacrifice the rook", "The rook remains safely distant from the king."),
        ),
        ("Use the king to close forward flights.", "Preserve the rook's barrier and wait when useful.", "Give the final distant check only after the edge flights are covered."),
    ),
    "mating-method-two-bishops": _guide(
        (40, 41),
        ("Coordinate bishops on opposite colors as diagonal barriers.", "Bring the king while avoiding stalemate.", "Recognize the final corner net."),
        (
            _section("Two colors, one shrinking region", """
Two bishops on opposite colors can work like two diagonal fences. One controls dark squares and the other light squares, so the defender cannot simply slip onto the other color and escape. Their own king helps close the gaps and pushes the enemy king into a corner. This differs from a single bishop ending, where half the board's square colors remain outside the bishop's reach. It also assumes bishops on opposite colors: two promoted bishops restricted to the same color do not supply this same mating force against a bare king. In the demonstration, watch the controlled diagonals as they change, rather than watching only the distance from bishop to king.
"""),
            _section("Regroup before pushing farther", """
The bishops begin on b8 and h5. Bf3, Be5 and Be4 bring them into a coordinated formation, while the defender travels toward c1. The king then approaches through e3. Ke2 would be a mistake at that moment: the king would not be checked, but every flight would be covered, making stalemate. This is a useful lesson in coordinated endings. More control is not always better if it removes the defender's last legal move without check. Keep one escape while improving your king, then close it with the final forcing sequence. The opponent's listed replies illustrate a route; they are not all the only legal replies.
"""),
            _section("Take away the escape route, then check", """
Later Bf5 helps restrict the h-file escape route and Kg3 brings the king close enough to control h2 and g2. The bishops then check in succession, directing the defender to h1. Be4 supplies the last diagonal check. At the finish Bd4 controls g1, Kg3 controls g2 and h2, and Be4 attacks h1. Those are all the corner king's possible neighboring squares. This diagonal advance resembles the two-rook ladder, but the bishops must coordinate across two square colors. Replay the line and point to the specific exit each move prevents. The chapter gives this complete two-bishop method but postpones bishop-and-knight technique until later, so do not assume this line teaches that harder ending too.
"""),
        ),
        (_example("Diagonal barriers to a complete corner mate", {"d4":"k","f2":"K","b8":"B","h5":"B"},
                  "The bishops will regroup, then the king will join. Keep checking for stalemate as the available region shrinks.", (
                      ("Bf3", "The h5 bishop moves onto the a8-h1 diagonal and begins closing the defender's route rightward."),
                      ("Kd3", "Black steps down the board within the available region."),
                      ("Be5", "The b8 bishop adds control of neighboring diagonals, coordinating with Bf3."),
                      ("Kd2", "Black continues toward the bottom edge."),
                      ("Be4", "The bishops regroup on e4 and e5, controlling complementary diagonals."),
                      ("Kc1", "Black reaches the edge. Ke2 would now stalemate, so White needs a careful king route."),
                      ("Ke3", "White approaches while leaving d1 available; the game remains alive."),
                      ("Kd1", "Black uses the remaining route along the edge."),
                      ("Bb2", "The e5 bishop relocates, controlling c1 and preventing a return to the left."),
                      ("Ke1", "Black moves rightward instead of returning to c1."),
                      ("Bc2", "The other bishop adjusts the diagonal barrier while the king continues to assist."),
                      ("Kf1", "Black is confined farther toward the h1 corner."),
                      ("Kf3", "White brings the king closer, controlling e2, f2 and g2."),
                      ("Kg1", "Black moves toward the corner rather than stepping back toward e1."),
                      ("Bf5", "The c2 bishop shifts to control h3, limiting an escape up the h-file."),
                      ("Kf1", "Black returns along the first rank; the bishops keep the broader escape routes closed."),
                      ("Bc3", "The b2 bishop adjusts its diagonal control and prepares the final coordinated checks."),
                      ("Kg1", "Black stays near the corner; White can now improve the king again."),
                      ("Kg3", "The king now directly controls g2 and h2, essential flights in the final net."),
                      ("Kf1", "Black steps back, but cannot cross the bishops' barrier into open space."),
                      ("Bd3+", "The f5 bishop checks along the d3-e2-f1 diagonal."),
                      ("Kg1", "Black is forced toward the corner by the checking diagonal and king control."),
                      ("Bd4+", "The c3 bishop checks g1 along the d4-e3-f2-g1 diagonal."),
                      ("Kh1", "The corner is the defender's remaining legal destination."),
                      ("Be4#", "The other bishop checks h1; Bd4 covers g1 and Kg3 covers g2 and h2. The net is complete."),
                  )),),
        ("The method needs bishops on opposite colors.",
         "Ke2 at the early c1 position would stalemate; the safe king route is e3.",
         "Bishop-and-knight mate is a different method, not a substitute for this one."),
        (
            _check("bishops-colors", "Why do opposite-colored bishops cooperate well here?", "They control complementary square colors", "Together they can close routes unavailable to one bishop alone.", "Each bishop changes color after moving", "A bishop always remains on its original square color.", "They can jump over the king", "Bishops cannot jump over occupied squares."),
            _check("bishops-finish", "At the final Be4#, what closes h2?", "White's king on g3", "Kg3 directly attacks h2.", "The edge removes h2", "h2 is a real square and must be controlled.", "The bishop on d4 alone", "Bd4 does not attack h2."),
        ),
        ("Coordinate opposite-colored diagonal barriers.", "Approach with the king while leaving a legal reply.", "Use the final bishop checks to close the corner net."),
    ),
    "avoid-stalemate": _guide(
        (39, 43),
        ("Distinguish no legal moves with check from no legal moves without check.", "Predict stalemate before a quiet restricting move."),
        (
            _section("Two questions determine the result", """
When the side to move has no legal move, ask whether its king is in check. If yes, the position is checkmate and that side loses. If no, it is stalemate and the game is drawn. Material does not change that rule. A queen and king can stalemate a bare king, and rooks can do it too. If the defender has other pieces, include every legal move by those pieces; a king with no move is not stalemated if a pawn can still move. The chapter presents both accidental stalemates by the attacker and deliberate defensive efforts to reach them. Start by applying the two questions to simple bare-king positions.
"""),
            _section("Inspect the opponent's next turn", """
Before a quiet move that takes away space, imagine the resulting position with your opponent to move. In the practice position Ka8 has only a7, b7 and b8 as neighboring squares. White Ka6 already controls a7 and b7. Qb6 would add control of b8 without checking a8, so it ends the game in a draw. Qe5 has the same unwanted effect: its diagonal reaches b8 while the king still closes the other exits. Counting the flights before moving is faster than discovering the draw afterward. A single remaining legal move is sometimes exactly what you need while bringing your king into the correct mating position.
"""),
            _section("A mating check removes the last reply legally", """
Qa7 solves the exercise because it attacks a8 and is protected by Ka6. Qc8 and Qf8 also give distant rank mates: the queen covers the eighth rank while Ka6 closes a7 and b7. The exercise accepts all genuine checkmates played on the board, rather than pretending only one square works. Compare each mate with Qb6 and say which feature changes: the defender is now in check. That one fact changes the result from draw to loss when no move exists. For practice, rotate the position, swap colors, or replace the queen with a rook where appropriate. Always verify the exact flights; similar pictures can have different outcomes when a king or blocker moves one square.
"""),
        ),
        (
            _example("A quiet move throws away the win", {"a8":"k","a6":"K","c5":"Q"},
                     "Ka6 already covers a7 and b7. Removing b8 without check will stalemate.",
                     (("Qb6", "Black is not checked, but a7, b7 and b8 are forbidden. The game is a draw by stalemate."),)),
            _example("The same net completed with check", {"a8":"k","a6":"K","c5":"Q"},
                     "Instead of a quiet restriction, give a protected adjacent check.",
                     (("Qa7#", "Qa7 attacks a8 and is protected by Ka6. No flight, capture or block is legal."),)),
        ),
        ("No king moves is not enough if another defending piece can move.",
         "Stalemate is an immediate draw, not a delayed form of checkmate.",
         "An alternative genuine mate remains correct even if not listed on a button."),
        (
            _check("stalemate-rule", "A side has no legal move and its king is not in check. What happens?", "The game is drawn by stalemate", "No legal move without check is the definition of stalemate.", "That side loses for having fewer pieces", "Material count does not override stalemate.", "It must pass its turn", "Chess has no voluntary pass in this situation."),
            _check("stalemate-count", "If the king cannot move but a pawn can, is it stalemate?", "No, that pawn move is a legal move", "All of the side's pieces must lack a legal move.", "Yes, only king moves matter", "The definition includes every piece.", "Only if the pawn is passed", "Whether the pawn is passed is irrelevant to this rule."),
        ),
        ("Count every legal defender move.", "No move plus no check means draw.", "Close the final flight with a real checking move."),
    ),
    "two-knights-draw": _guide(
        (42, 42),
        ("Distinguish possible mate from forceable mate.", "Choose the safe defensive escape from a corner trap."),
        (
            _section("Possible does not mean forced", """
King and two knights against a bare king is a theoretical draw against correct defence. Yet checkmate positions with those pieces do exist. The attacker may arrange a trap, but cannot compel a careful defender to enter it from a normal drawn position. This is different from king and a single knight against king, where no legal mating position exists at all. Keep those two ideas separate: material that cannot possibly mate, and material that can form a mate only after defensive mistakes. The distinction matters when deciding whether to keep trying, how to defend, and whether a position has already ended as a dead draw.
"""),
            _section("The actual defensive choice", """
White's king is on g8 and is checked by a knight on h6. The other black knight is on e5, supported by the black king on g6. White has two legal escapes: f8 and h8. Kh8 walks into the corner and permits Nef7 mate. Kf8 avoids the trap and retains the drawn ending. You should be able to see why the mating picture after Kh8 works, rather than accepting the statement that two knights cannot force mate as permission to make any move. A theoretical draw still requires avoiding immediate blunders. Here the question tests a real defensive difference, not an arbitrary choice between moves with identical results.
"""),
            _section("Read the two-knight notation carefully", """
After Kh8, both knights can move to f7. SAN therefore includes the origin file: Nef7 means the knight from the e-file, while Nhf7 means the knight from the h-file. Keeping Nh6 in place is essential to the displayed mate because it controls g8. The knight arriving from e5 checks h8 and covers h6 and g5 among its other squares; Kg6 controls h7 and g7. Black's two knights and king together leave no escape. A careless defender stepping into that net loses despite the theoretical draw. Practice by replaying both king choices and accounting for all three corner flights. Later positions with additional pawns can have different outcomes, so the statement here is specifically about a bare defending king.
"""),
        ),
        (
            _example("Avoid the corner trap", {"g8":"K","g6":"k","h6":"n","e5":"n"},
                     "White is checked by Nh6 and must choose between the corner and an open escape.",
                     (("Kf8", "The king stays out of the mating corner. Correct continued defence holds this two-knight ending."),)),
            _example("The corner mistake permits mate", {"g8":"K","g6":"k","h6":"n","e5":"n"},
                     "Compare the other legal escape. The result changes because a concrete mating reply becomes available.", (
                         ("Kh8", "White enters the trap. The king has only g8, g7 and h7 as possible neighboring board squares."),
                         ("Nef7#", "The e5 knight checks h8, Nh6 controls g8, and Kg6 controls g7 and h7. Every corner flight is closed."),
                     )),
        ),
        ("Two knights can form a mate, so do not call their material automatically dead.",
         "Unable to force mate does not mean every defensive move is safe.",
         "The statement concerns a lone defending king; additional pawns can change the ending."),
        (
            _check("knights-force", "Which statement is accurate about king and two knights against a bare king?", "Mate is possible but cannot be forced against correct defence", "The defender can avoid the necessary corner trap.", "No mating position can ever exist", "The example Nef7# is a legal mating position.", "Mate can always be forced", "Correct defence prevents the attacker from compelling that position."),
            _check("knights-escape", "In the g8 check position, which escape avoids the immediate mating trap?", "Kf8", "This stays out of the corner net.", "Kh8", "Nef7# follows.", "Pass the turn", "A checked player must make a legal move resolving the check."),
        ),
        ("Separate possible mate from forced mate.", "Avoid the displayed corner trap with Kf8.", "Check the concrete replies even in a theoretically drawn ending."),
    ),
    "drawn-material": _guide(
        (38, 43),
        ("Recognize basic dead positions immediately.", "Distinguish dead material from the two-knight theoretical draw.", "Predict the consequence of a minor-piece promotion."),
        (
            _section("No legal mate means the game is drawn", """
A bare king cannot mate another bare king. King and one bishop against king cannot produce mate, because the defender can never have every flight removed in a legal mating arrangement with that material. King and one knight against king also cannot mate. These are dead positions: no possible legal continuation can end in checkmate, so the game has already ended as a draw. There is no need to make an improving king move or ask the opponent to agree. Learning these basic cases prevents both unnecessary resignation and pointless attempts to find a mate that the pieces cannot create. It also helps you recognize the effect of an exchange before making it.
"""),
            _section("Some drawn endings still contain mating positions", """
Do not put every theoretical draw into the same category. Two knights against a lone king cannot force mate against correct defence, but a legal mating picture is possible if the defender goes wrong. That ending is therefore not one of the simple dead-material cases just described. Other positions can be drawn for positional reasons despite having more material, as with a wrong bishop and rook pawn. The reason for a draw matters: insufficient mating possibility, a defendable blockade, stalemate, or another rule are different explanations. Start by naming the material, then ask whether any legal mating position can exist and whether the current position has a concrete drawing feature.
"""),
            _section("Promotion can reveal the material rule", """
The classification exercise begins with a pawn on e7, a distant white king and a lone black king on h8. Promoting to a bishop leaves king and bishop against king, which is immediately dead. Promoting to a knight does the same for king and knight. Promoting to a queen or rook instead retains a forced win with correct technique. Normally you would choose the winning promotion; this particular task deliberately asks you to demonstrate a dead draw so you can see the distinction. A legal move is not automatically a good practical move, and a correct answer depends on the stated task. Before trading or promoting in a real game, identify which mating force remains afterward.
"""),
        ),
        (_example("A promotion immediately creates a dead position", {"h8":"k","a1":"K","e7":"P"},
                  "The pawn can choose any promotion. This demonstration deliberately selects a piece that cannot mate a bare king.",
                  (("e8=B", "King and bishop against king has no possible legal mating continuation. The game ends in a draw now."),)),),
        ("King and one bishop or knight against king is already drawn; no offer is needed.",
         "Two knights are not dead material merely because they cannot force mate.",
         "Do not promote to a minor piece in a winning bare-king ending unless you intend the draw or another concrete reason applies."),
        (
            _check("material-dead", "Which resulting material is a basic dead position?", "King and one bishop against a bare king", "No legal mating position can exist with only that material.", "King and queen against a bare king", "The queen and king can force mate.", "King and rook against a bare king", "The rook and king can force mate."),
            _check("material-promotion", "Why does e8=N draw against a lone king here?", "A king and one knight cannot mate a bare king", "Promotion leaves insufficient mating possibility.", "Promotions must always be queens", "A pawn may legally promote to queen, rook, bishop or knight.", "The black king can take e8 immediately", "Kh8 is three files away and cannot capture e8 in one move."),
        ),
        ("Recognize basic dead material immediately.", "Keep two knights distinct from one-knight dead material.", "Consider the resulting mating force before exchanging or promoting."),
    ),
    "active-stalemate": _guide(
        (42, 43),
        ("Find a move that actively forces a drawing stalemate.", "Use a corner blockade instead of chasing material.", "Recognize wrong-bishop and knight-pawn defensive ideas."),
        (
            _section("The defender can create the draw", """
The stronger side is not the only player who can influence stalemate. Sometimes the weaker king can deliberately remove every move from the opponent and save the game. With Black Ka1 and Pa2, the pawn's promotion square is occupied by its own king. White Kc2 can play Kc1, controlling b1 and b2. The black king is not checked, cannot leave a1, and cannot move the blocked pawn. This is immediate stalemate. The white king has achieved the draw by choosing the right square, despite having no material of its own. Look for this resource before resigning a pawn ending that appears hopeless.
"""),
            _section("Extra material may not break a fortress", """
The chapter also shows a black knight added to the a1 corner prison. With White Kc2 and Black Ka1, Pa2 and Nc4, the side to move matters. When Black moves first, White can keep matching the knight's square color by shuttling between c1 and c2. Even an offered knight should not distract White from the blockade. The worked line Nd2, Kc1, Nc4, Kc2 shows that refusal to chase material. If White instead has to move first from the original arrangement, Black can change the timing and force the king away. This is a precise fortress, not a claim that every knight and rook pawn draws.
"""),
            _section("The wrong bishop cannot remove the corner king", """
A bishop controlling the wrong color for a rook pawn's promotion corner may fail to win despite the extra pawn and piece. In the example White Ka1 blocks a black a-pawn, while Black's bishop on d3 stays on light squares and cannot attack the dark corner a1. The black king cannot force the white king out without giving it a usable escape or producing stalemate. Pushing the pawn to a2 in the displayed position immediately stalemates White. The important ingredients are the rook pawn, the defender established in the promotion corner, and a bishop unable to control that corner. Do not generalize the result to a defender still far from the corner.
"""),
            _section("Choose the drawing job over a tempting capture", """
In these examples the king's main job is control of a small set of squares, not material gain. A capture that leaves the corner or breaks the required move timing can release the enemy king and allow promotion. Before taking something, compare the resulting legal moves with those in the fortress. This is an early example of thinking about the opponent's plan: your king should remain where it prevents that plan. Practice with both sides to move and say explicitly why a pawn is blocked, why the king cannot move, and why the king is not in check. Those details distinguish a proven stalemate from an optimistic wish for one.
"""),
        ),
        (
            _example("The weaker king forces stalemate", {"a1":"k","a2":"p","c2":"K"},
                     "Black is one square from promotion but blocks its own pawn. White can close the king's exits.",
                     (("Kc1", "White controls b1 and b2. Black has no legal king or pawn move and is not checked: stalemate."),)),
            _example("Ignore the offered knight and hold the blockade", {"a1":"k","a2":"p","c4":"n","c2":"K"},
                     "Black moves first. White preserves the fortress by matching the knight's square color rather than capturing it.", (
                         ("Nd2", "Black offers a knight that White could capture, trying to lure the king away from the blockade."),
                         ("Kc1", "White declines, moving to a dark square like the knight on d2 and keeping b1 controlled."),
                         ("Nc4", "Black returns the knight to a light square without freeing the corner king."),
                         ("Kc2", "White matches the light square again and restores the original defensive arrangement."),
                     ), turn="b"),
            _example("Wrong bishop plus rook pawn produces stalemate", {"a1":"K","b3":"k","a3":"p","d3":"b"},
                     "The bishop cannot control a1. White's king is already established in the promotion corner.",
                     (("a2", "The pawn now blocks a2; Kb3 controls b2 and Bd3 controls b1. White is not checked and has no move: stalemate."),), turn="b"),
        ),
        ("The promotion square may be blocked by the attacker's own king.",
         "Do not abandon a drawing fortress for a tempting knight capture.",
         "A wrong-bishop rook-pawn draw requires the defender to reach the relevant corner."),
        (
            _check("active-draw", "Why does Kc1 draw against Ka1 and Pa2?", "It leaves Black no legal move without giving check", "The pawn is blocked and the king's exits are controlled.", "It captures the pawn", "The pawn remains on a2.", "White wins by checkmate", "Black is not checked, so the result is stalemate and a draw."),
            _check("wrong-bishop", "What does 'wrong bishop' refer to in this rook-pawn fortress?", "The bishop cannot control the promotion corner's color", "It cannot force the established corner king out by attacking that corner.", "The bishop is legally allowed to change color", "Bishops never change their square color.", "Any bishop with any pawn always draws", "Many bishop-and-pawn positions win; the corner conditions matter."),
        ),
        ("Look for an active stalemate resource before resigning.", "Keep the king on the square that maintains the blockade.", "Check corner color and side to move in material-rich fortresses."),
    ),
    "queening-a-pawn": _guide(
        (44, 47),
        ("Follow the promotion sequence with both sides moving.", "Choose material that preserves a win against a bare king.", "Check the promotion square and stalemate risk."),
        (
            _section("Promotion is a choice with consequences", """
A pawn reaching the last rank must become a queen, rook, bishop or knight of the same color as part of that move. It cannot remain a pawn or become a king. The notation includes the new piece, such as e8=Q. Against a lone king, queen or rook usually preserves a forced win with correct technique and king support. A single bishop or knight instead leaves a dead drawn position. The queen is normally the most convenient practical choice, but it is inaccurate to say that only a queen wins when a rook would also suffice. Your goal is the resulting position, not promotion for its own sake.
"""),
            _section("Count the defender's turns too", """
From e6 the pawn needs e7 and e8, but Black moves between those white turns. The worked line includes Kg7 so that you see the real alternating sequence. Black is too far from e8 to capture the new piece on arrival. A pawn that looks close to promotion can fail if the defending king reaches the promotion square in time, or if the pawn must advance onto an undefended square. Before pushing, check its next square and the square where it will promote. If the enemy king is close enough to interfere, the king-escort and opposition lessons are essential; a simple race is not the same problem as a contested pawn ending.
"""),
            _section("Inspect the board after the new piece appears", """
Promotion can give check, cause stalemate, lose the new piece immediately, or leave material that cannot mate. In this exercise both e8=Q+ and e8=R+ check safely and retain a win. e8=N does not check and leaves insufficient material. Bishop promotion has the same material problem against a bare king here. In other positions underpromotion can be the best move, so do not turn this result into a rule that minor-piece promotions are always wrong. First state the task: here it is to retain a forced win against this lone king. Then inspect what the specific promotion does. The chapter's central message is that an extra pawn wins only if it can be conducted safely into useful promoted material.
"""),
        ),
        (
            _example("Two pawn moves, with a defender reply", {"h8":"k","a1":"K","e6":"P"},
                     "The pawn has two advances left. Black cannot arrive at the e-file quickly enough.", (
                         ("e7", "The pawn reaches the seventh rank. Its route to e8 is clear."),
                         ("Kg7", "Black uses its intervening turn, but still cannot capture a piece on e8 next move."),
                         ("e8=Q", "The pawn becomes a queen. This particular king square makes the promotion a non-check, but the queen is safe and wins."),
                     )),
            _example("A rook promotion also keeps a win", {"h8":"k","a1":"K","e7":"P"},
                     "The promotion square is safe and the opposing king is on the eighth rank.",
                     (("e8=R+", "The new rook checks along rank eight and can force mate with its king. Choosing a queen is stronger, not uniquely winning."),)),
        ),
        ("Promotion does not by itself prove the ending is won.",
         "A rook promotion also wins against the lone king in this exercise.",
         "Include the defender's intervening move when counting a pawn race."),
        (
            _check("promotion-wins", "Which promotions retain a forced win in the e7 versus Kh8 exercise?", "Queen and rook", "Each can force mate with king support against a bare king.", "Queen only", "The rook is also sufficient mating material.", "Any piece equally", "One bishop or knight cannot mate a bare king."),
            _check("promotion-safety", "What must you check besides whether the pawn can reach the last rank?", "Whether the new piece is safe and the resulting position achieves the goal", "Capture, stalemate and remaining mating material can change the result.", "Whether the pawn used a capture earlier", "A pawn may promote after straight advances or captures.", "Whether a previously captured queen is available", "A promotion is not limited by the original pieces that were captured."),
        ),
        ("Count both sides' moves to the promotion square.", "Check the safety and result of the chosen promotion.", "Use a queen or rook here to retain mating force."),
    ),
    "king-helps-the-pawn": _guide(
        (44, 46),
        ("Protect the pawn's route, including the promotion square.", "Avoid retreating from a winning escort position.", "Explain the necessary king move before promotion."),
        (
            _section("Defending today's pawn is only the beginning", """
In a contested pawn ending, the attacking king should control the squares the pawn will need, not merely defend the square it already occupies. A king beside or ahead of the pawn can keep the opposing king out of its route. A king following far behind may be unable to prevent a blockade. Here White Kd6 and Pe6 face Black Ke8. Kd6 protects e7, so e7 is safe even though the black king also attacks that square. Kings cannot capture a pawn onto a square controlled by the enemy king. This simple fact explains the first advance and why the advanced king is such a valuable escort.
"""),
            _section("The next king move makes promotion safe", """
After e7 Black's only legal move is Kf7. The pawn attacks d8 and f8, while White's king controls d7 and e7, leaving Black no other escape. Do not automatically promote now. A new queen on e8 would be attacked by Kf7 and is not protected by Kd6. White instead plays Kd7, which controls e8. Black must then move and the pawn can promote under protection. This is the important sequence: protect the seventh-rank advance, react to the defender, then protect the promotion square. Seeing only the first safe push would miss the reason the ending actually wins. Say what changed after Black's reply before choosing White's next move.
"""),
            _section("Backward king moves can surrender the win", """
In the quiz, Ke5 or Kc5 lets Black answer Ke7 and establish a drawn blockade. White has given up the advanced king position without making useful pawn progress. A king move is not good merely because it is legal or seems active. Compare the squares it controls before and after moving. In a different ending the correct choice may indeed be a king move before a pawn move; the opposition lessons show precisely that. Here e7 is correct because the king already protects the needed advance and has a follow-up route to d7. Practice the whole line, then reverse colors and explain the same escort principle for a black pawn approaching its first rank.
"""),
        ),
        (_example("Escort the pawn, then guard the new queen", {"e8":"k","d6":"K","e6":"P"},
                  "The pawn's next square e7 is defended by Kd6. Its promotion square e8 is not yet defended.", (
                      ("e7", "The pawn advances safely because Kd6 forbids Kxe7."),
                      ("Kf7", "Black's only legal reply moves the king into capture range of e8."),
                      ("Kd7", "White protects e8 before promoting. Immediate e8=Q+ instead would allow Kxe8."),
                      ("Kf6", "Black steps away; it cannot move onto e8 because White's king now controls that square."),
                      ("e8=Q", "The pawn promotes safely, with Kd7 protecting the queen. The new mating material retains the win."),
                  )),),
        ("A protected pawn on e7 does not imply a protected new queen on e8.",
         "Do not retreat the king from an advanced escort square without checking the blockade it allows.",
         "Choose the correct move for this position; not every pawn ending calls for an immediate push."),
        (
            _check("escort-capture", "Why is Kxe7 illegal after White plays e7?", "Kd6 attacks e7", "The black king may not capture onto an attacked square.", "Kings cannot capture pawns", "A king may capture an undefended pawn when otherwise legal.", "The pawn attacks its own square", "A pawn does not defend its own square."),
            _check("escort-promotion", "After e7 Kf7, why play Kd7 before promoting?", "Kd7 protects the promotion square e8", "Without that protection the king could capture the new queen.", "Pawns must wait one turn before promotion", "There is no such waiting rule.", "Kd7 gives check", "Kd7 does not check Kf7; it improves control of e8."),
        ),
        ("Guard the next advance.", "Reassess after the defender's reply.", "Guard the promotion square before creating the new piece."),
    ),
    "pawn-opposition": _guide(
        (44, 45),
        ("Use opposition to defend a sixth-rank pawn ending.", "Compare a checking seventh-rank advance with a winning non-checking one.", "Identify the unique drawing retreat."),
        (
            _section("Opposition controls entry squares", """
Kings cannot stand next to each other. When they face each other with one empty square between them, the player who must move often has to step aside. The other king may then enter on the opposite side. This relationship is opposition. It matters because the invading king wants to control the pawn's route, while the defender wants to stay directly in front. Opposition is not a complete evaluation rule by itself: pawn location, side to move and the board edge also matter. The chapter introduces these simple cases before the fuller calculation discussion later. Work through the actual moves so you can explain which square the king gains or loses.
"""),
            _section("The defender retreats straight back", """
With White Kc5 and Pc6 against Black Kc7, Black must choose among b8, c8 and d8. Kc8 is the only drawing retreat. It keeps the king directly in front of the pawn and retains a reply on either side. If White comes to b6, Black chooses b8; if White comes to d6, Black chooses d8. A premature Kb8 allows Kd6, while Kd8 allows Kb6. In each case White approaches on the opposite side and gains control of the promotion route. This is a useful defensive pattern to learn actively. The weaker side is not merely waiting to lose; its correct king placement changes the result from win to draw.
"""),
            _section("Understand the seventh-rank comparison precisely", """
In the chapter's simple sixth-rank setup with the supporting king alongside the pawn, a seventh-rank push with check can let the defender blockade the promotion square and draw by stalemate. A comparable push without check can force the defender away while the attacking king takes control of promotion. This is a rule for the pictured family of positions, not a universal rule that checking pawn moves never win. Rook pawns and knight pawns add edge exceptions, and other king placements can change everything. Compare the two worked lines square by square. Then change only whose turn it is and ask how the opposition changes. Learning both win and draw cases is more useful than remembering the slogan without its conditions.
"""),
        ),
        (
            _example("Defend straight in front, then take opposition", {"c7":"k","c5":"K","c6":"P"},
                     "Black must retreat. Staying on the c-file preserves the drawing replies on both sides.", (
                         ("Kc8", "The unique drawing retreat keeps the king directly in front of the pawn."),
                         ("Kb6", "White tries to enter from the left."),
                         ("Kb8", "Black takes direct opposition against Kb6 and prevents the king reaching b7."),
                         ("c7+", "The pawn advances with check, allowing Black to blockade directly on its promotion file."),
                         ("Kc8", "Black occupies the promotion square and cannot be driven away."),
                         ("Kc6", "White approaches but leaves Black unchecked with no move: stalemate."),
                     ), turn="b"),
            _example("A seventh-rank advance without check can win", {"c8":"k","b6":"K","c6":"P"},
                     "Here White can advance without checking. This changes which square the defending king must use.", (
                         ("c7", "The pawn does not check c8; b8 and d8 are attacked, so Black must step to d7."),
                         ("Kd7", "The only legal reply leaves the promotion square."),
                         ("Kb7", "White's king takes control of c8, ensuring the promoted piece cannot be captured."),
                         ("Kd6", "Black uses one legal retreat; other available retreats also fail to stop promotion."),
                         ("c8=Q", "The pawn promotes safely under Kb7's protection, preserving a winning queen ending."),
                     )),
            _example("Checking advance reaches the drawn blockade", {"c8":"k","c6":"K","d6":"P"},
                     "This similar-looking position has the pawn on d6. The checking advance does not force a win.", (
                         ("d7+", "The pawn checks c8, allowing the defender onto d8."),
                         ("Kd8", "Black stands directly in front of the pawn."),
                         ("Kd6", "White cannot force the king away; this approach is stalemate because Black has no legal reply."),
                     )),
        ),
        ("Opposition is a means to control entry, not a universal declaration of win or draw.",
         "The with-check versus without-check rule has specific sixth-rank conditions and edge exceptions.",
         "Defending straight in front of the pawn can be the only drawing move."),
        (
            _check("opposition-retreat", "With Kc5 and Pc6 against Kc7, where should Black retreat to draw?", "c8", "It preserves the defensive reply on either side.", "b8", "White enters from the opposite side with Kd6.", "d8", "White enters from the opposite side with Kb6."),
            _check("opposition-rule-scope", "Does every seventh-rank pawn push with check fail to win?", "No, the chapter's rule concerns a particular family of simple positions", "King placement and edge cases must still be checked.", "Yes, checking a king always helps the defender", "Many checking pawn moves win in other positions.", "Only rook pawns can give check", "Any pawn can check diagonally when an enemy king occupies an attacked square."),
        ),
        ("Use opposition to deny the invading king entry.", "Defend directly in front before choosing a side.", "Compare exact positions and whose turn it is."),
    ),
    "pawn-fifth-rank": _guide(
        (45, 47),
        ("Use an unspent pawn move as a reserve tempo.", "Take opposition with the king before a premature push.", "Compare a winning fifth-rank setup with its drawn successor."),
        (
            _section("A spare pawn move can change who must move", """
With a pawn on the fifth rank and its king securely ahead on the sixth, the pawn often retains a useful waiting move. Advancing it later can transfer the move to the defender at exactly the moment when opposition matters. This is why two positions that look nearly identical can have different results. The pawn is not only potential promotion material; its remaining legal move is a reserve tempo. In the chapter's examples a non-rook pawn with the king properly in front can win whichever side moves first. Learn the specific arrangement rather than assuming any king somewhere ahead of any pawn guarantees a win.
"""),
            _section("Put the king on the right square first", """
The quiz begins with White Kd6 and Pc5 against Black Kc8. Kc6 takes opposition. Black has to move to b8 or d8, and White's king goes to the other side, entering b7 or d7 when appropriate to protect the pawn's route. An immediate c6 instead lets Black play Kd8. White's king is then alongside the pawn with no reserve pawn move left before the critical checking advance. The defender can reach the drawn blockade from the previous lesson. A pawn push is therefore not automatically progress. It may use up the very move that made the original ending winning. Compare the two displayed lines rather than evaluating only how close the pawn is to promotion.
"""),
            _section("Spend the tempo when it forces a concession", """
A different position has White Kd6 and Pc5 against Black Kd8, with White to move. Here c6 is useful: the kings already face one another, and the pawn move makes Black move away. White then advances under the king's protection and clears the promotion square. The same written move c6 is good in one arrangement and draws in another, because the black king starts on a different square. This is the point of studying the connected examples. After each move ask whose turn it is, which king squares are forbidden, and whether the pawn's next step is safe. Practice the mirrored f-pawn version and both sides to move to strengthen the idea beyond memorizing the c-file example.
"""),
        ),
        (
            _example("Take opposition before using the pawn", {"c8":"k","d6":"K","c5":"P"},
                     "White must improve the king first. The pawn's spare move is still available.", (
                         ("Kc6", "White takes opposition and forces the defender to choose a side."),
                         ("Kd8", "Black chooses the right. White should enter from the left."),
                         ("Kb7", "The king controls c6, c7 and c8, the pawn's entire remaining route."),
                         ("Ke7", "Black retreats away from the protected route."),
                         ("c6", "The pawn now advances safely with its king already in the correct position."),
                         ("Kd6", "Black approaches but cannot capture c6, which Kb7 defends."),
                         ("c7", "The next advance remains protected by Kb7."),
                         ("Kd7", "Black attacks the pawn's region but cannot capture its protected squares."),
                         ("c8=Q+", "Promotion is safe because Kb7 protects c8. The new queen checks Kd7."),
                     )),
            _example("The premature push throws away the win", {"c8":"k","d6":"K","c5":"P"},
                     "Compare the same starting position with the pawn pushed before the king takes opposition.", (
                         ("c6", "White spends the spare move too early."),
                         ("Kd8", "Black takes opposition against Kd6 and keeps the promotion blockade available."),
                         ("c7+", "The pawn's next step checks the king, allowing the direct blockade."),
                         ("Kc8", "Black occupies c8 in front of the pawn."),
                         ("Kc6", "White's approach produces stalemate, demonstrating the lost win."),
                     )),
            _example("Spend the spare move after opposition is established", {"d8":"k","d6":"K","c5":"P"},
                     "The defending king starts on d8 this time. White's pawn move now forces Black to give way.", (
                         ("c6", "The reserve tempo transfers the move while the kings already face each other."),
                         ("Kc8", "Black steps left; Ke8 is another legal defence requiring the same escort logic."),
                         ("c7", "The pawn advances without check, while Kd6 protects it."),
                         ("Kb7", "Black must leave the promotion square's neighborhood on this side."),
                         ("Kd7", "White now protects c8 before promoting."),
                         ("Kb6", "Black cannot attack the protected promotion square in time."),
                         ("c8=Q", "The pawn becomes a safe queen. The extra tempo was used at the right moment."),
                     )),
        ),
        ("Do not push merely because the pawn moves closer to the last rank.",
         "The same pawn move can win or draw depending on the kings' squares and the move order.",
         "Rook pawns require their own edge exception."),
        (
            _check("fifth-first", "Why is Kc6 better than c6 in the quiz position?", "It takes opposition before spending the spare pawn move", "Black must step aside and allow king entry.", "Kings always move before pawns in an ending", "There is no such rule; the useful order depends on the position.", "c6 is illegal", "c6 is legal but permits a drawing defence."),
            _check("fifth-tempo", "What is a reserve pawn tempo useful for here?", "Making the defender move while preserving a useful king arrangement", "The pawn move can force the opponent to give up opposition.", "Moving twice in one turn", "Players still alternate normally.", "Skipping the defender's reply", "The defender always gets a legal turn unless the game ends."),
        ),
        ("Secure king entry before pushing.", "Keep a useful pawn move in reserve when needed.", "Check the exact king positions before spending that tempo."),
    ),
    "rook-pawn-draw": _guide(
        (43, 47),
        ("Recognize the promotion-corner draw for an edge pawn.", "Choose the unique drawing corner retreat.", "Explain why central-pawn technique does not transfer unchanged."),
        (
            _section("The edge changes the geometry", """
A rook pawn is an a-pawn or h-pawn, named for the file on which a rook begins. A king defending the corner immediately in front of that pawn may be impossible to dislodge. With a central pawn, the attacking king can sometimes go around on either side. At the edge one of those routes does not exist. The attacker can cover the remaining exits but may then stalemate the defender instead of forcing promotion. This is why the chapter explicitly separates rook-pawn cases from the ordinary central-pawn rules. A king standing impressively in front of an edge pawn does not guarantee that the pawn can be conducted through the corner.
"""),
            _section("Head for the correct corner", """
In the quiz White has Kg6 and Ph6, and Black's king on g8 must move. Kh8 reaches the drawing promotion corner. Kf8 instead lets White advance h7, approach with Kg7 and promote safely. The result changes because Black chooses whether to occupy the destination the pawn needs. Do not describe both retreats as equally adequate just because the defender is near the last rank. Count the actual route and the white king's control. From h8 the defender cannot be driven out by White's king alone, since the kings may not approach adjacent squares. The only attempt to eliminate every available king move without check produces a draw.
"""),
            _section("Recognize the stalemate endpoint", """
After Black plays Kh8, the immediate white push h7 is stalemate. The pawn on h7 controls g8, Kg6 controls g7 and h7, and the black king on h8 is not in check. Black has no other piece to move. White can choose other moves instead of stalemating immediately, but cannot force a win from this established corner defence. In real play a defender who has not yet reached the corner may lose, so do not stop calculating merely because the pawn is on an edge file. Learn the drawing destination and get there in time. The second worked line illustrates how retreating away from that destination can allow the king escort that makes promotion possible.
"""),
        ),
        (
            _example("Enter the corner and the push only stalemates", {"g8":"k","g6":"K","h6":"P"},
                     "Black must choose a retreat. The promotion corner is the saving square.", (
                         ("Kh8", "Black reaches the square the h-pawn needs and establishes the drawing corner defence."),
                         ("h7", "The pawn controls g8 and Kg6 covers g7 and h7. Black is not checked and has no move: stalemate."),
                     ), turn="b"),
            _example("Retreating away allows a protected promotion", {"g8":"k","g6":"K","h6":"P"},
                     "Compare the other king retreat, which gives up the drawing corner.", (
                         ("Kf8", "Black moves away from h8 and permits the escort plan."),
                         ("h7", "The pawn advances while Kg6 protects h7."),
                         ("Ke7", "Black cannot reach h8 now; this legal retreat illustrates the loss of the corner blockade."),
                         ("Kg7", "White's king controls h8, so the new queen will be safe."),
                         ("Ke6", "Black remains too far away to prevent promotion."),
                         ("h8=Q", "Promotion is protected by Kg7. The position is a winning queen ending rather than a corner draw."),
                     ), turn="b"),
        ),
        ("Rook pawn refers to the a- or h-file, not a pawn that promotes to a rook.",
         "The defender must reach the relevant promotion corner in time.",
         "Do not apply central-pawn opposition rules without checking the missing edge route."),
        (
            _check("rookpawn-corner", "Which move draws for Kg8 against Kg6 and Ph6?", "Kh8", "It occupies the pawn's promotion corner.", "Kf8", "This allows h7 and a king escort to g7.", "Stay on g8 without moving", "Black must make a legal move on its turn."),
            _check("rookpawn-push", "After Kh8 h7, why is the result a draw?", "Black is stalemated", "The king is not checked and all three neighboring squares are forbidden.", "The pawn gives checkmate", "A pawn on h7 attacks g8, not h8.", "The pawn promotes on h7", "A white pawn promotes on rank eight."),
        ),
        ("Get the defending king to the promotion corner.", "Recognize the edge's missing route.", "Verify the stalemate instead of assuming the extra pawn wins."),
    ),
    "knight-pawn-stalemate": _guide(
        (45, 47),
        ("Preserve the win in the near-edge pawn exception.", "Avoid both the premature checking push and the quiet stalemate push.", "Reposition the king before advancing."),
        (
            _section("A g-pawn is close enough to the edge to need care", """
A knight pawn means a b-pawn or g-pawn, named for the starting knight file. It does not move like a knight. Unlike a rook pawn it can often win with the king in front, but the nearby edge introduces additional stalemate dangers. Here White Kf6 and Pg5 face Black Kh7. The natural g6+ allows Kh8 and reaches a drawn sixth-rank setup. The win requires Kf7 first. This is a precise result-changing move, not merely a preference for improving the king. Compare the positions after the two choices and observe how much useful pawn tempo remains and which squares the white king can still use.
"""),
            _section("Do not use the pawn's spare move yet", """
After Kf7 Kh8, White has Kf7 and Pg5 against Kh8. Now g6 without check would stalemate. The pawn would attack h7, Kf7 would cover g8 and g7, and the black king would have no square beyond the h-file. White must leave a legal reply instead. Kg6 permits Kg8; Kh6 then permits Kh8. The king has changed its route around the pawn so that g6 can be played while Black still has Kg8 available. These quiet king moves are how the attacker avoids the edge trap. More attacks and fewer defender moves are not automatically better when the king is not in check.
"""),
            _section("Finish under protection, not on autopilot", """
The chapter's maneuver continues g6, Kg8, g7, after which the position is winning. Our connected line goes farther to show the last escort detail. Black's Kf7 attacks the promotion square g8, so White plays Kh7 before promoting, just as the king-escort lesson required protection of e8. After the next black king move, g8=Q is safe because Kh7 guards g8. This avoids the mistake of treating a winning seventh-rank pawn as an automatic instruction to promote immediately. Learn the full chain: keep the spare move, avoid stalemate, create a legal defender reply, advance safely, and guard the promotion square. The same logic applies to the mirrored b-pawn case, with the board directions reversed.
"""),
        ),
        (
            _example("The complete near-edge king maneuver", {"h7":"k","f6":"K","g5":"P"},
                     "White wins only with careful king preparation. A checking pawn advance now would surrender the win.", (
                         ("Kf7", "White keeps the pawn on g5 and prepares to rearrange the king before pushing."),
                         ("Kh8", "Black heads for the corner. The immediate g6 would now stalemate."),
                         ("Kg6", "White moves the king so that Black can legally step to g8 instead of being trapped."),
                         ("Kg8", "Black uses that legal escape, allowing White's next maneuver."),
                         ("Kh6", "White's king changes sides and leaves the pawn's advance available."),
                         ("Kh8", "Black returns to the corner, but the king geometry is now different."),
                         ("g6", "This is safe now: Black still has Kg8, so the move does not stalemate."),
                         ("Kg8", "The defender is forced out of the corner and cannot stop the next protected advance."),
                         ("g7", "The pawn reaches the seventh rank under Kh6's protection."),
                         ("Kf7", "Black's only legal move attacks g8. Do not promote onto an undefended square."),
                         ("Kh7", "The king protects g8 before promotion."),
                         ("Kf6", "Black steps away but cannot prevent a safe new queen."),
                         ("g8=Q", "Promotion is protected by Kh7, completing the conversion to a winning queen ending."),
                     )),
            _example("The tempting push that immediately draws", {"h8":"k","f7":"K","g5":"P"},
                     "The white king has reached f7, but the king maneuver has not yet been completed.",
                     (("g6", "Black is not checked. Pg6 covers h7 and Kf7 covers g7 and g8, so Black is stalemated."),)),
            _example("The earlier checking push loses the forced win", {"h7":"k","f6":"K","g5":"P"},
                     "This is the original position. Compare the premature checking advance with Kf7.", (
                         ("g6+", "White uses the pawn's spare move before arranging the king."),
                         ("Kh8", "Black reaches the known drawn sixth-rank knight-pawn setup. Correct defence holds."),
                     )),
        ),
        ("Knight pawn means a b- or g-pawn; it still uses ordinary pawn movement.",
         "g6+ too early draws; g6 after Kf7 Kh8 stalemates. The exact timing matters.",
         "Even a winning seventh-rank pawn may need one more king move to guard promotion."),
        (
            _check("knightpawn-first", "From Kf6 and Pg5 against Kh7, which move preserves the win?", "Kf7", "It preserves the pawn tempo and starts the necessary king maneuver.", "g6+", "Kh8 establishes the drawn setup.", "Ke6", "The king abandons the winning route and Black can draw."),
            _check("knightpawn-trap", "Why does g6 draw immediately with Kf7, Pg5 and Kh8?", "It stalemates Black", "h7 is attacked by the pawn, g7 and g8 by the king, and Kh8 is not checked.", "It gives checkmate", "Pg6 does not attack h8.", "The pawn is captured immediately", "The game ends by stalemate before another move is played."),
        ),
        ("Preserve the spare pawn move.", "Reposition the king to avoid the edge stalemate.", "Protect the promotion square before the final push."),
    ),
    "outside-pawn": _guide(
        (44, 47),
        ("Count a simple unassisted pawn race correctly.", "Distinguish this supplement from the chapter's contested-pawn theory."),
        (
            _section("An explicitly supplementary illustration", """
The chapter's pawn pages focus on conducting a pawn past a nearby defending king, including opposition and edge exceptions. This additional example shows the simpler case where the defending king is far away. It is a supplement to those ideas, not a claim that the chapter separately teaches an outside passed pawn distraction strategy. The pawn on a4 is passed: no opposing pawn ahead on its file or either adjacent file can stop it by normal pawn play. That description alone does not prove it promotes, because an enemy king or piece could still intercept it. Here the board is sparse enough that we can count the route directly.
"""),
            _section("Count squares and alternating turns", """
The pawn needs four white moves: a5, a6, a7 and a8 with promotion. Black's king begins on h8 and gets a move between consecutive white pushes, but cannot cross the board quickly enough to reach the pawn's route. The worked line shows a sensible attempt to approach via g7 and f6 rather than pretending the defender stands still. With each turn, compare the distance to the next interception square, not just to the pawn's old square. A king moving toward a pawn can still be too late. Once promotion is safe, choose a queen or rook if you want enough material to force mate against the remaining bare king.
"""),
            _section("Do not invent a lost win where none exists", """
In this particular position White can also make a king move and still win. Kg3 or Kg1 is not a blunder that throws away the pawn or lets Black catch it. The practical exercise specifically asks for a pawn advance, so those king moves do not perform the requested action, but their feedback says plainly that they retain a win. This distinction matters for honest teaching: a task-specific move is not automatically the only objectively good move. The conceptual questions test why the pawn can race successfully. When you return to a contested pawn position, do not reuse the advice to push automatically; first inspect the enemy king's distance, the next square's safety, the supporting king and the possible stalemate endpoint.
"""),
        ),
        (_example("A passed pawn outruns a distant king", {"h8":"k","h2":"K","a4":"P"},
                  "White needs four pawn moves. Black's king is too far from the a-file to intercept the route.", (
                      ("a5", "The pawn advances toward a8; no capture or king support is needed on this square."),
                      ("Kg7", "Black starts approaching, but remains many files from the pawn."),
                      ("a6", "White continues the direct race while the route stays clear."),
                      ("Kf6", "Black approaches again but cannot reach a7 or a8 in time."),
                      ("a7", "Only promotion remains; the black king cannot capture the pawn or occupy a8."),
                      ("Ke5", "Black still cannot interfere with the promotion square."),
                      ("a8=Q", "The pawn becomes a queen safely. White can now use the queen mating method."),
                  )),),
        ("This race supplements the source pawn theory; it does not replace opposition and escorting.",
         "Passed does not automatically mean unstoppable; count the defending king's route.",
         "The other listed king moves also win here, even though the exercise asks for a pawn move."),
        (
            _check("race-turns", "How many white moves does the a4 pawn need to promote on an empty route?", "Four", "The sequence is a5, a6, a7 and a8 with promotion.", "Two", "A pawn can move two squares only from its starting rank, not from a4.", "Seven", "Seven is unrelated to the four ranks remaining from a4."),
            _check("race-passed", "Does being passed by itself guarantee promotion?", "No, a king or another piece may still stop the pawn", "Passed describes the opposing pawns, not every possible defender.", "Yes, passed pawns cannot be captured", "They remain ordinary capturable pawns.", "Only if it is on the a-file", "An a-pawn can still be blocked or caught in other positions."),
        ),
        ("Treat this as a simple extra race example.", "Count the defender's moves as well as the pawn's.", "Use king escort and opposition when the route is contested."),
    ),
}
