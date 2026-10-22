"""Additional original teaching for Chapter 3's previously omitted topics.

Printed page references match the supplied Maizelis edition. PDF pages are
one greater. The worked positions are teaching illustrations; a displayed
reply is not claimed forced unless its note explicitly says so.
"""

from core.primer_build import after, custom
from core.primer_guides_chapter1 import check, example, guide, section


GUIDES = {
    "bishop-vs-knight": guide(
        (66, 69),
        ("Compare the actual jobs available to a bishop and a knight.", "Identify a supported knight post and the pawn breaks that could challenge it."),
        (
            section("Equal average value does not mean equal usefulness", """
                Bishops and knights have roughly similar average material value, but they solve different problems.
                A bishop can cross the board quickly along an open diagonal, making it useful when targets lie
                on both wings. It remains limited to one square color. A knight takes several jumps to travel far,
                but can eventually reach both colors and can jump over a blocked pawn structure. Do not decide
                an exchange merely by saying 'both are worth about three'. Look at the actual diagonals, entry
                squares, king safety, and targets in this position. An active bishop can outperform a passive
                knight, while a firmly supported central knight can dominate a bishop trapped behind its own pawns.
            """),
            section("Find a job and a stable square", """
                A useful knight post lets the knight attack meaningful targets without being easily chased away.
                In the example, c4 supports d5 diagonally, while the knight on d5 attacks the black pawn on f6.
                Black's bishop on g7 is initially hemmed in by its own pawns on f6 and h6, so its long-range
                advantage has little immediate use. Nd5 therefore improves the knight and creates a concrete
                threat at the same time. Supporting a square is not the whole analysis: check whether an enemy
                pawn can advance to challenge the knight, whether a bishop can exchange it, and what happens
                after the knight captures. A post is valuable because of its available work, not simply because
                it occupies a central coordinate.
            """),
            section("The pawn structure can change the comparison", """
                A blocked bishop is not sentenced to remain bad forever. A pawn advance or capture may open
                a new diagonal, and a bishop retreat may put it outside its own pawn chain. Equally, a knight
                can become stranded after a supporting pawn disappears. Before trading bishop for knight or
                vice versa, imagine the remaining pawns and the likely next several moves. If play opens on
                both wings, the bishop's range may become more important; if the center stays locked and
                targets are nearby, the knight's jumping may matter more. The worked bishop retreat is one
                illustrative response, not proof that every defence loses immediately. Explain why the knight
                improves, then look for the defender's best resistance instead of turning an instructive example
                into an absolute rule about all closed positions.
            """),
        ),
        (example("A supported knight attacks behind a pawn wall", custom({"g1": "K", "f4": "N", "c4": "P", "h8": "k", "g7": "b", "f6": "p", "h6": "p"}), ("Nd5", "Bf8", "Nxf6"), (
            "White's c4 pawn supports d5. The bishop on g7 has little scope because f6 and h6 block its downward diagonals.",
            "Nd5 occupies the supported post and attacks f6. The move creates useful work rather than centralizing for appearance alone.",
            "Black retreats the bishop to f8. This is one legal response; Black may also investigate king moves and other defensive plans.",
            "The knight captures the pawn on f6. Its jump bypasses the pawn wall that restricted the bishop; no check is given to h8.",
        )),),
        ("A supported central square is not automatically permanent; inspect pawn challenges and exchanges.",
         "Closed positions often favor knights, but a concrete pawn break can change the comparison."),
        (
            check("compare-open", "Why can a bishop be useful when weak pawns lie on opposite wings?",
                  ("Its open diagonals let it switch targets over long distances", True, "Range can matter more than short-distance jumping when the board is open."),
                  ("It can change square color whenever needed", False, "A bishop permanently remains on its original square color.")),
            check("compare-post", "What should you ask before calling d5 a permanent knight outpost?",
                  ("Whether enemy pawns or exchanges can challenge it", True, "Support and central location do not by themselves guarantee lasting occupation."),
                  ("Only whether d5 is near the center", False, "An easily expelled knight may accomplish little despite its central square.")),
        ),
        ("Compare concrete jobs, not only point values.", "Support a knight post and inspect challenges.", "Reassess bishop and knight activity when pawns change."),
    ),
    "queen-vs-pawn": guide(
        (62, 65),
        ("Recognize stalemate shelters beside an advanced rook pawn.", "Check the defender's legal moves before bringing a distant king closer."),
        (
            section("An exceptional pawn can challenge an enormous material lead", """
                A queen is normally much stronger than a single pawn, but a pawn one step from promotion
                demands precise handling. Its promotion threat can force the queen to keep checking instead of
                allowing time for the attacking king to approach. Rook pawns and bishop pawns on the seventh
                rank have special stalemate resources when their king is nearby and the enemy king is far away.
                These are geometric exceptions, not a revision that makes any pawn equal to a queen. Identify
                the pawn's file, promotion square, king position, and available checks before deciding the result.
                A queen-versus-pawn ending can change completely when the stronger king begins only a few squares nearer.
            """),
            section("The king can block its own pawn to create a shelter", """
                In the example Black's h2 pawn wants to promote on h1, while its king is checked on g1 by
                White's queen on g3. Black can play Kh1. The king is now out of check, and the pawn cannot
                advance because its own king occupies h1. The queen controls g1 and g2, so the king has no
                move either. It is White's turn, so the position is not already stalemate. But an ordinary distant
                white king move leaves Black to move with no legal action and no check: the game is drawn.
                The defender's own obstruction, normally a disadvantage, becomes the resource that prevents
                the queen side from casually gaining a free tempo for king improvement.
            """),
            section("Do not confuse prevention with progress", """
                Giving more queen checks may prevent immediate promotion, yet prevention alone does not prove
                that the stronger side can make progress. Each time the defender reaches its shelter, inspect
                whether a waiting move is possible without stalemate. Capturing the pawn is useful only if that
                capture is legal and does not lose the queen; moving the queen away may instead allow promotion.
                This is why a distant king matters: it cannot help in the critical area without spending turns
                that the queen may be unable to spare. Practice the defending side as well as the attacking side.
                Look for a safe king square that removes all future legal moves, and explain why the pawn
                cannot move. In other arrangements the queen does win, so retain the exact conditions rather
                than memorizing 'queen versus rook pawn is always drawn'.
            """),
        ),
        (example("A distant king move concedes stalemate", custom({"a1": "K", "g3": "Q", "g1": "k", "h2": "p"}, turn="b"), ("Kh1", "Ka2"), (
            "Black is checked along the g-file. Its advanced h-pawn and corner provide a possible shelter.",
            "Kh1 escapes check and blocks the pawn's promotion square. Black now has no legal move if White leaves this confinement intact.",
            "White tries to bring its distant king closer. Black is not checked and cannot move king or pawn, so the game immediately ends as stalemate. The white move is an instructive error.",
        )),),
        ("A position with no black moves is not stalemate while White still has the turn.",
         "A near-promotion rook pawn is not always a draw; the attacking king's distance and exact queen geometry matter."),
        (
            check("qp-block", "After Black Kh1 beside its own h2 pawn, why can the pawn not advance?",
                  ("Its promotion square h1 is occupied by its own king", True, "A pawn cannot move onto a friendly piece, even to promote."),
                  ("Pawns cannot promote on the h-file", False, "Rook pawns promote normally when the last-rank square is legally available.")),
            check("qp-wait", "Why can an ordinary distant king move fail for the queen side?",
                  ("It may give the defender a turn with no legal move and no check", True, "The attempted improvement then ends the game in stalemate."),
                  ("The queen side must always keep its king on the first rank", False, "There is no such movement restriction; the issue is the resulting legal moves.")),
        ),
        ("Locate the promotion square and the king shelter.", "Check every defending piece's legal moves after a waiting move.", "A huge material advantage still needs a method that avoids stalemate."),
    ),
    "relative-pin": guide(
        (77, 80),
        ("Distinguish an absolute pin from a relative pin.", "Unpin safely while keeping the formerly pinned piece defended."),
        (
            section("Name what stands behind the blocker", """
                A line piece can attack a valuable target through an intervening enemy piece. If the hidden
                target is the king, moving the blocker off that line would expose check and is illegal: an
                absolute pin. If the hidden target is a queen, rook, or other valuable unit, exposing it is legal
                but may lose material: a relative pin. In the example Black's bishop on b4 looks through the
                white knight on c3 toward the queen on e1. The king is on g1, away from that diagonal, so
                the knight is not legally frozen. Its problem is the expensive queen it would leave behind.
            """),
            section("Legal does not mean affordable", """
                White can play Nd5, but then Black can capture the queen with Bxe1. Before obeying a pin,
                however, calculate any forcing opportunity: a pinned piece might move with mate, a decisive
                check, or a greater material gain. The word 'relative' means you must compare consequences,
                not that the pin is irrelevant. Also inspect the attacker's safety and the target's defenders.
                A bishop pointing at a queen does not win her if the queen can move with a stronger threat
                or if capturing her exposes a mating attack. Use the alignment as a clue to search for tactics,
                then calculate the actual moves. A motif's name describes a relationship; it cannot replace
                verifying the resulting position.
            """),
            section("Release the piece without giving it away", """
                One method is to move the valuable rear target off the line. Qe2 removes White's queen from
                the bishop's b4–c3–d2–e1 diagonal. The knight may now move without exposing her. Another
                method may be to block the line with a different piece, attack or exchange the pinning bishop,
                or defend the rear target sufficiently for a tactical break. Whichever method you choose, inspect
                whether the knight itself remains protected. Here b2 still supports c3, so if Black exchanges
                bishop for knight, bxc3 recaptures. Unpinning and defending are different jobs: removing the
                queen from danger does not automatically stop Bxc3. The worked line shows both the release
                and the real recapture, so that the learner accounts for the whole exchange rather than just
                declaring the pin gone.
            """),
        ),
        (example("Release the queen and preserve the recapture", custom({"g1": "K", "e1": "Q", "c3": "N", "b2": "P", "b4": "b", "g8": "k"}), ("Qe2", "Bxc3", "bxc3"), (
            "The knight on c3 shields the queen, not the king. Moving it is legal but would open the bishop's line to e1.",
            "Qe2 steps off that diagonal. The b2 pawn still protects the knight on c3.",
            "Black exchanges bishop for knight. This is an illustrative response, not a forced one; unpinning did not make the knight immune to capture.",
            "White recaptures with the pawn, so the bishop was not won for nothing. White's queen remains safe from the original line.",
        )),),
        ("A relative pin may be broken legally; calculate the loss or gain behind it.",
         "Moving the queen off the line does not by itself defend the knight that was shielding her."),
        (
            check("relative-law", "A knight shields its queen from a bishop, but its king is elsewhere. May the knight move?",
                  ("Yes, legally; the exposed queen may make it costly", True, "Only a pin to the king creates a direct king-safety prohibition."),
                  ("No; every pinned piece is forbidden to move", False, "Relative pins are material relationships, not an absolute movement ban.")),
            check("relative-release", "After unpinning a knight, what should you still inspect?",
                  ("Whether an enemy can capture it and whether you can legally recapture", True, "Removing the pin does not remove attacks on the knight itself."),
                  ("Nothing; an unpinned piece cannot be taken", False, "A piece's freedom to move and its protection are separate questions.")),
        ),
        ("Identify the rear target before naming the pin.", "Relative pins are legal to break but may be costly.", "Release the line and verify the former blocker's safety."),
    ),
    "overloaded-defender": guide(
        (75, 77),
        ("Identify two incompatible defensive duties.", "Calculate the defender's new lines after a forcing exchange."),
        (
            section("Two apparent defences may share one resource", """
                A defender is overloaded when it cannot meet two important duties after a forcing sequence.
                Looking at each target separately may suggest that both are protected. The attacker links them:
                fulfilling one duty pulls the defender away from the other. In the example Black's queen on
                d8 protects a rook on c8 along rank 8 and another rook on g5 along the diagonal d8–e7–f6–g5.
                White can capture c8 with its rook and attack g5 with its bishop. Name both exact duties before
                calculating. 'The queen defends many things' is not a tactic until a concrete sequence shows
                that one cannot be saved without conceding something else.
            """),
            section("Recalculate from the defender's new square", """
                White begins Rxc8. If Black replies Qxc8, the queen no longer stands on the diagonal toward
                g5, and White can play Bxg5. White loses one rook while Black loses two. The queen on c8
                cannot recapture a bishop on g5: their file and rank differences do not form a rank, file,
                or diagonal. That last check is essential. If the second rook were instead on f8 and White
                captured it with a queen, Qc8 would still defend f8 along rank 8 and could recapture again.
                The same motif label would then conceal a losing material calculation. After every capture,
                redraw the surviving defender's actual lines instead of assuming that moving it must have
                removed all its former duties.
            """),
            section("A forced loss is not the same as a forced recapture", """
                Black is not literally compelled to play Qxc8. Declining the recapture leaves the first rook lost,
                but Black may prefer that to entering the displayed continuation. A stronger countercheck or
                mating threat elsewhere could also change the assessment, so inspect forcing replies before
                claiming a clean gain. Overloading is closely related to deflection: the attacker exploits the
                defender's limited ability to maintain several jobs, then draws it to a square where one job
                fails. Use material accounting through the final capture and note which pieces remain. A clear
                beginner explanation should say 'if the queen recaptures, this second target falls', rather than
                describing an optional recapture as compulsory. That distinction prepares you to assess real
                opponents who choose the least damaging response rather than cooperate with your favorite line.
            """),
        ),
        (example("The queen cannot keep both rook defences", custom({"h1": "K", "g1": "N", "b4": "Q", "c1": "R", "f4": "B", "h7": "k", "d8": "q", "c8": "r", "g5": "r"}), ("Rxc8", "Qxc8", "Bxg5"), (
            "The queen on d8 defends c8 horizontally and g5 diagonally. White's bishop on f4 attacks g5, while the rook has a clear c-file.",
            "White captures the first rook. Black must assess whether recapturing is better than accepting that loss or finding a counter-threat.",
            "Black chooses to recapture with the queen. Its new square c8 no longer protects g5.",
            "The bishop captures the second rook. Qc8 cannot recapture on g5, so the full sequence gains two rooks for one rather than losing the attacking queen.",
        )),),
        ("A defender moving does not automatically abandon a target; recompute its new lines.",
         "The opponent may decline a recapture when that is the least costly defence."),
        (
            check("overload-proof", "What proves that a defender is overloaded?",
                  ("A concrete sequence makes its important duties incompatible", True, "The attacker must show that answering one threat concedes another meaningful loss."),
                  ("It protects at least two pieces", False, "A piece may safely defend several targets if no forcing sequence exploits their relationship.")),
            check("overload-recalc", "After the queen recaptures on c8, what should you verify before taking another target?",
                  ("Whether the queen from c8 can still recapture there or create a stronger threat", True, "The new geometry and all forcing replies decide the tactic."),
                  ("Only that the queen moved away from d8", False, "Changing squares does not necessarily remove its defence of the second target.")),
        ),
        ("Name both defensive duties.", "Calculate the defender's new geometry after it moves.", "Distinguish an optional recapture from an unavoidable material concession."),
    ),
    "skewer": guide(
        (87, 90),
        ("Recognize a valuable front piece hiding a target behind it.", "Verify the forcing reply and the final capture."),
        (
            section("Reverse the familiar pin picture", """
                A pin attacks a shielding piece whose movement would expose something more valuable behind it.
                A skewer puts the more valuable or urgent target in front, so its movement exposes a rear target.
                The front piece is often the king: check forces the defender to answer before the rear queen
                or rook can simply move away. Rooks, bishops, and queens create these line attacks, so inspect
                ranks, files, and diagonals for alignments. The attacker need not already occupy the relevant
                line. In the example White's rook starts on a1 but can reach a7 with check against a king
                on d7, revealing the black rook farther along the same rank on h7.
            """),
            section("Show why the rear piece cannot escape first", """
                After Ra7+, Black must resolve the attack on its king. Moving the h7 rook to an unrelated
                square would leave the king checked and is illegal. Could that rook instead capture the checker
                or block between a7 and d7? Its own king on d7 obstructs its route to the squares on that
                side of the king, so it cannot perform those defences here. The king must leave the seventh
                rank, after which Rxh7 is available. The displayed king move is one legal reply; other king
                exits should be checked for their effect on the rear rook's protection. A skewer is successful
                only if the attacker can legally make the payoff capture after the forcing response.
            """),
            section("Check the capture's consequences", """
                Not every visual alignment wins material. Another piece may capture the checking rook, interpose
                on the line, defend the rear target, or create a countercheck when the king moves. If the front
                target is a queen rather than a king, it may move with a stronger threat instead of submitting
                to the skewer's intended sequence. Calculate the opponent's best response, then count what both
                sides lose after the rear target is taken. In the small worked position there are no extra
                defenders, and the king cannot both leave the checking line and protect h7 from a nearby square.
                This makes the mechanism easy to see. In a full game, look for the same alignment, but earn
                the conclusion by verifying all legal responses rather than labeling the picture and stopping.
            """),
        ),
        (example("Check the king, then take the rook behind it", custom({"g1": "K", "a1": "R", "d7": "k", "h7": "r"}), ("Ra7+", "Kc6", "Rxh7"), (
            "Black's king and rook share rank 7. White can place its rook on that rank with check.",
            "Ra7+ attacks the front king. The h7 rook cannot cross its own king to interpose between a7 and d7.",
            "Black leaves the line with Kc6. This is one legal king response, opening the rook's clear path along rank 7.",
            "White captures the rear rook on h7. The black king on c6 cannot recapture, so White retains a rook against a lone king.",
        )),),
        ("A skewer needs a usable forcing line, not just two pieces somewhere on the same rank.",
         "After the front piece moves, verify that the rear capture is safe and still legal."),
        (
            check("skewer-front", "In the common king-and-rook skewer, which piece stands nearer the checking attacker?",
                  ("The king", True, "The urgent front target must move first, exposing the rook behind it."),
                  ("The rook shielding the king", False, "That arrangement is typically a pin rather than a skewer.")),
            check("skewer-reply", "After a checking skewer, may the defender move the rear rook away while leaving the king in check?",
                  ("No", True, "Every reply must resolve the check on the king."),
                  ("Yes; saving a rook is more valuable than moving the king", False, "Material value never permits an unanswered check.")),
        ),
        ("Find the alignment and the valuable front target.", "Prove that the checking reply exposes the rear piece.", "Verify the final capture and any recapture."),
    ),
    "discovered-attack": guide(
        (84, 92),
        ("Identify the moved piece and the newly revealed attacker separately.", "Use a discovered check to combine two useful jobs in one move."),
        (
            section("Look behind the piece that moves", """
                A discovered attack happens when one piece moves out of another friendly piece's line, revealing
                an attack that the blocker previously prevented. The moving piece need not attack the newly
                exposed target itself. In the example White's bishop on e4 stands between its rook on e1 and
                the black king on e8. Moving the bishop away opens the rook's e-file. The bishop can choose
                a destination that accomplishes another useful task at the same time. Name both pieces and
                both jobs before calculating: 'the bishop captures the queen, while the rook gives check' is
                more precise and easier to verify than simply announcing that a discovery wins something.
            """),
            section("Discovered check constrains the reply", """
                When the revealed attack reaches the king, the discovery is especially forcing. Black must
                answer that check before doing an unrelated job, such as saving another attacked piece.
                Bxb7+ captures Black's queen and uncovers the rook's check; the bishop on b7 does not itself
                attack the king on e8. If both the moved piece and the revealed piece check, the result is
                double check, requiring a legal king move. An ordinary discovered attack on a queen or rook
                is less compulsory because the opponent may choose a stronger counter-threat. In either case,
                the apparent gain must survive the actual reply. A checking discovery can still fail if the
                opponent captures its checker or moves the king with a decisive counterattack.
            """),
            section("Choose the best useful departure square", """
                Several bishop moves may uncover the same rook check. Bf3+ reveals the line but leaves the
                queen on b7 alive; Bxb7+ performs the profitable capture as well. This illustrates why you
                should compare candidate discoveries instead of selecting the first checking move you see.
                Inspect the departing piece's safety, the rook's new path, and your own king. A blocker pinned
                to its own king may not be able to move legally, and opening one friendly line may also open
                an enemy line. After the forcing reply, reconsider whether the moved bishop should remain
                exposed or return to a useful diagonal. The worked withdrawal is one illustrative continuation,
                not a claim that every enemy king reply is forced. Coordinating two tasks is powerful only
                when all the resulting lines and captures have been checked.
            """),
        ),
        (example("The bishop captures while the rook checks", custom({"g1": "K", "e1": "R", "e4": "B", "e8": "k", "b7": "q"}), ("Bxb7+", "Kf7", "Be4"), (
            "The bishop blocks the rook's e-file. The black queen on b7 also lies on the bishop's e4–d5–c6–b7 diagonal.",
            "The bishop captures the queen and clears the e-file. The rook, not the bishop, now checks the king on e8.",
            "Black moves the king off the file to f7. This is one legal response, and it does not recover the lost queen.",
            "White returns the bishop to a central diagonal. This blocks the rook's e-file again, but Black's king has already left it and the queen remains captured.",
        )),),
        ("The piece that moved need not be the piece giving check.",
         "Several moves can reveal the same attack; compare what each departure square achieves."),
        (
            check("discovery-checker", "White moves a bishop off the e-file and a rook on e1 now attacks the king on e8. Which piece gives the discovered check?",
                  ("The rook", True, "The bishop's departure reveals the rook's previously blocked line."),
                  ("The bishop automatically", False, "A moved piece can uncover another attack without checking the king itself.")),
            check("discovery-choice", "Two bishop moves reveal the same safe rook check, but one also captures an undefended queen. What should you compare?",
                  ("The full consequences of both moves, including the extra capture", True, "The discovered line is only one job; the moving piece can achieve another."),
                  ("Only whether each move has a plus sign", False, "Equal checking status does not imply equal value.")),
        ),
        ("Name the blocker and the attacker behind it.", "Check whether the discovery forces a king response.", "Choose a departure square that performs a second useful job safely."),
    ),
    "underpromotion": guide(
        (96, 98),
        ("Choose the promoted piece by the resulting legal moves.", "Explain a rook underpromotion that preserves a forced mate."),
        (
            section("Promotion strength depends on the task", """
                On the last rank a pawn must become a queen, rook, bishop, or knight immediately. A queen
                is normally strongest, but promotion is a decision about the resulting position, not a contest
                to select the largest nominal value. A rook may avoid a queen's unwanted diagonal control;
                a knight may give a unique check or fork. A bishop may have a similarly precise composed
                purpose. Choosing a piece other than a queen is underpromotion. First identify the problem
                that makes a queen fail, then show how the alternative solves it. Selecting an unusual piece
                without a concrete reason does not improve a position, and avoiding stalemate alone does not
                prove that the remaining material can win.
            """),
            section("A queen removes one square too many", """
                White has a king on c6 and pawn on c7; Black's king is on a7. After c8=Q, Black is not
                checked, but has no legal move. The queen covers a8 and b8 along rank 8 and a6 along
                the c8–b7–a6 diagonal. White's king controls b5, b6, and b7. The queen's extra diagonal
                has therefore destroyed the win by causing stalemate. A rook on c8 still controls a8 and b8,
                but does not attack a6. Black retains exactly that move. Naming a6 is the key explanation:
                the rook is better here because it permits an enemy move that the queen forbids, not because
                a rook is generally stronger than a queen.
            """),
            section("Show the payoff after the weaker promotion", """
                After c8=R, Black must play Ka6. White then gives Ra8#, checking down the a-file. The white
                king covers b5, b6, and b7, while the rook covers the a-file flights. Black cannot reach and
                capture the rook on a8, and has no piece to interpose. The underpromotion thus preserves
                a concrete forced mate instead of merely postponing the ending. A knight promotion on c8
                would even give check to a7, but king and knight against a lone king cannot produce mate:
                the checking suffix would not make it the winning choice. The book places underpromotion
                beside other powerful promotion threats to teach the same habit throughout: calculate the
                opponent's actual reply, then evaluate the whole continuation rather than stopping when the
                pawn becomes a piece.
            """),
        ),
        (example("The rook leaves a move, then gives mate", custom({"c6": "K", "c7": "P", "a7": "k"}), ("c8=R", "Ka6", "Ra8#"), (
            "A queen promotion would stalemate Black by also controlling a6. White must choose a piece that preserves a winning continuation.",
            "The rook controls rank 8 but leaves a6 unattacked. Black's other king destinations remain unavailable.",
            "Ka6 is forced. The white king still controls b5, b6, and b7.",
            "Ra8 checks down the a-file. The king cannot escape to a5 or a7, enter the b-file squares controlled by White's king, capture the distant rook, or block: mate.",
        )),),
        ("The strongest promotion can be wrong if it ends the game as stalemate.",
         "A checking knight promotion is not automatically better than a quiet rook promotion."),
        (
            check("under-queen", "Why does c8=Q fail with White Kc6/Pc7 and Black Ka7?",
                  ("It creates stalemate by also controlling a6", True, "Black is not checked and every legal king destination disappears."),
                  ("A second queen is illegal", False, "Extra queens are legal; the problem is the resulting draw.")),
            check("under-check", "A knight promotion gives check but leaves only king and knight versus king. Has that check proved a win?",
                  ("No; that material cannot produce a legal mate against a lone king", True, "Giving check does not override the limits of the remaining material."),
                  ("Yes; every promotion with check wins", False, "Check may be answered, and the ending may be drawn.")),
        ),
        ("Find the concrete reason a queen would fail.", "Count the defender's legal replies after replacement.", "Verify the weaker piece's full winning continuation."),
    ),
    "bishop-knight-mate": guide(
        (100, 104),
        ("Assign the king, bishop, and knight distinct squares to control.", "Recognize the correct corner and a coordinated barrier.", "Replay one complete illustrative transfer from a distant wing to mate."),
        (
            section("Start with the final corner pattern", """
                King, bishop, and knight can force mate against a lone king, but all three pieces must cooperate.
                The standard method drives the king to a corner of the bishop's color. A dark-squared bishop
                targets a1 or h8; a light-squared bishop targets a8 or h1. In the first example Nh6+ forces
                the king to h8 and controls g8. White's king on g6 controls g7 and h7, while Bf6 then checks
                along the dark diagonal into h8. Each unit has a separate job. Removing the knight gives an
                escape on g8; removing the supporting king releases forward squares. Learn these jobs before
                trying to memorize a long succession of checks.
            """),
            section("Build barriers and transfer the king", """
                The defender tries to remain central, then heads toward a corner the bishop cannot use for
                the standard forced mate. Repeated random checks do not reliably solve this problem. In the
                longer example a light-squared bishop and knight gradually steer the king toward a8. After
                Nd7 and Bd3, the knight controls dark b6 and c5 while the bishop controls light b5 and a6.
                Together they form a barrier across complementary colors, allowing the attacking king to
                approach without the defender escaping past it. Inspect the controlled squares at this pause.
                The point of the maneuver is the combined fence, not merely the fact that the knight traced
                an attractive shape. Preserve the barrier until another coordinated arrangement can replace it.
            """),
            section("Practice stages, then combine them", """
                First solve final mates in two or three moves, then practice confining a king on an edge,
                transferring it from the less useful wing, and reaching the starting arrangement from a more
                open board. The long replay shows one chosen defensive branch from the book's teaching
                sequence, not every legal reply or a promise that only those moves work. Explain why each
                quiet move keeps control before moving forward. Reset and try an alternative king defence,
                checking whether the barrier still holds. This ending can require many accurate moves, so
                the fifty-move rule makes aimless shuffling costly. Knowing one corner pattern is a foundation,
                not mastery of the entire ending. The worked transfer supplies a route to study in stages
                while retaining the distinct king, bishop, and knight responsibilities that make the route succeed.
            """),
        ),
        (example("The final dark-corner pattern", custom({"g6": "K", "f5": "N", "e7": "B", "g8": "k"}), ("Nh6+", "Kh8", "Bf6#"), (
            "The dark-squared bishop will deliver the final check on h8, while the knight must first deny g8.",
            "Nh6+ attacks g8. The white king controls f7, g7, and h7, and the bishop controls f8.",
            "Kh8 is forced. The knight on h6 prevents the king's return to g8.",
            "Bf6 checks along f6–g7–h8. The king and knight remove all flights, completing mate.",
        )), example("A coordinated transfer to the light a8 corner", "5k2/5N2/5K2/5B2/8/8/8/8 w - - 0 1", ("Bh7", "Ke8", "Ne5", "Kd8", "Ke6", "Kc7", "Nd7", "Kc6", "Bd3", "Kb7", "Kd6", "Kc8", "Nc5", "Kb8", "Kd7", "Ka7", "Kc7", "Ka8", "Kb6", "Kb8", "Ba6", "Ka8", "Bb7+", "Kb8", "Na6#"), (
            "White has a light-squared bishop. Study this one illustrative defensive branch toward a8; it is not the only legal variation.",
            "Bh7 controls g8, limiting a retreat toward the less useful h8 wing while keeping the bishop safe.",
            "Black chooses Ke8 rather than another legal defence. The king seeks room along the back ranks.",
            "Ne5 centralizes the knight and prepares support of the approaching king and barrier squares.",
            "Black retreats to d8, continuing toward the queenside.",
            "Ke6 brings the attacking king closer while denying d7 and e7, so the defender cannot simply come forward there.",
            "Black chooses Kc7, apparently finding an exit from the edge. White must build a new barrier rather than chase blindly.",
            "Nd7 controls b6 and c5, two dark squares on the defender's possible escape route.",
            "Black steps to c6, but cannot cross to b6 or c5 because the knight controls them.",
            "Bd3 adds control of light b5 and a6. Pause: bishop and knight now seal complementary squares across the route.",
            "Black chooses Kb7, staying on the far side of the coordinated barrier.",
            "Kd6 advances the supporting king while maintaining the minor-piece restrictions.",
            "Black returns to c8. The defender remains near the edge rather than breaking through the barrier.",
            "Nc5 changes the knight's job, controlling b7 and supporting the approach without losing control of key exits.",
            "Black retreats to b8, still avoiding direct approach to White's king.",
            "Kd7 takes control of c8, c7, and c6, pushing the black king farther toward the corner.",
            "Black chooses Ka7. White's pieces must keep the king from slipping down the a-file.",
            "Kc7 strengthens control of b8, b7, and b6 while the knight controls a6.",
            "Black retreats to a8, the corner matching the light-squared bishop.",
            "Kb6 brings the attacking king into its final supporting neighborhood, including a7 and b7.",
            "Black returns to b8, trying to postpone confinement while remaining away from White's king.",
            "Ba6 controls b7 and prepares a checking move from b7, preserving the net without rushing a check.",
            "Black chooses Ka8. White now has the coordinated pieces for a short final sequence.",
            "Bb7+ checks the corner. White's king protects the bishop; Black cannot capture it.",
            "Kb8 is forced. The king leaves the checking diagonal but remains confined against the edge.",
            "Na6# checks b8. The bishop and king control the remaining flights and protect the mating arrangement.",
        ))),
        ("The standard forced target corner matches the bishop's color; the defender seeks the other corner.",
         "A list of checks is not a method; identify the combined barrier and safe king approach.",
         "One chosen legal continuation does not establish that every defensive reply is forced."),
        (
            check("bn-corner", "Which corner is a standard target for a light-squared bishop and knight?",
                  ("a8 or h1", True, "Those corners are light, matching the bishop's permanent square color."),
                  ("a1 or h8", False, "Those dark corners are the defender's preferred alternative in the usual forcing method.")),
            check("bn-barrier", "Why combine Nd7 and Bd3 in the transfer example?",
                  ("They restrict complementary dark and light escape squares", True, "The knight covers b6/c5 while the bishop covers b5/a6, creating a joint barrier."),
                  ("The knight can then change into a bishop", False, "Only pawns promote; the pieces cooperate without changing type.")),
        ),
        ("Match the target corner to the bishop's color.", "Coordinate complementary escape-square control.", "Learn final patterns, barriers, transfer, and king approach as connected stages."),
    ),
    "triangulation": guide(
        (116, 118),
        ("Recognize a return to the same placement with the other side to move.", "Explain why the defender's restricted waiting moves make the triangle useful."),
        (
            section("Lose a move to improve the position", """
                In some endings the obligation to move is a disadvantage. If the same pieces could remain
                where they are while the opponent moved instead, that opponent would have to yield a key
                square. Triangulation achieves that change legally. One king follows a three-move route while
                the other makes two useful replies, returning to the same piece placement with the opposite
                player to move. White has not passed or taken two turns together: it has used a different-length
                route. The effect matters only when the starting arrangement is sensitive to whose turn it is.
                A triangle without a reason to alter the move is merely a king walk that may waste valuable time.
            """),
            section("The pawns restrict useful waiting routes", """
                White has Ke5, Pf5, and Pg6 against Black Ke7 and Pg7. The advanced pawns restrict Black's
                king and threaten to create a passer if the wrong route is chosen. The illustrated triangle is
                Ke5–d5–e4–e5, while Black follows Ke7–f6–e7. After those five individual turns the board's
                piece placement is exactly restored, but Black must move. The halfmove counter and move
                number have naturally changed; the relevant point is the placement and the side's obligation,
                not literal identity of every computer record field. Count the three white turns and two black
                replies aloud. Then inspect what Black can do from the final arrangement rather than assuming
                the word 'triangulation' alone proves a win.
            """),
            section("Convert the changed move into a concrete result", """
                The long worked continuation shows one defensive branch after the triangle. White uses opposition
                to escort the king toward the kingside, then chooses a pawn break at the moment when a
                careless further king move could stalemate. The sacrifice f6 draws the g7 pawn away, freeing
                White's g-pawn. The supporting king then makes promotion safe and helps finish the mate.
                This demonstrates why the changed move is useful instead of ending the lesson at a repeated
                diagram. Other black replies require their own analysis; the selected branch is illustrative,
                not a claim that every displayed move is the only legal defence. When considering a triangle
                in your games, check whether the opponent can escape, capture a pawn, create a counter-passer,
                or use a pawn waiting move. Restricted useful routes, not the geometric shape itself, supply the gain.
            """),
        ),
        (example("Change the turn, then convert one defensive branch", custom({"e5": "K", "g6": "P", "f5": "P", "e7": "k", "g7": "p"}), ("Kd5", "Kf6", "Ke4", "Ke7", "Ke5", "Kf8", "Kd6", "Ke8", "Ke6", "Kf8", "Kd7", "Kg8", "Ke7", "Kh8", "f6", "gxf6", "Kf7", "f5", "g7+", "Kh7", "g8=Q+", "Kh6", "Qg6#"), (
            "White to move. This is a mirrored version of the book's pawn-triangulation geometry; follow one legal defensive branch.",
            "Kd5 begins the king triangle without spending a pawn move or changing the structure.",
            "Black chooses Kf6, remaining near the pawns instead of abandoning them along the back rank immediately.",
            "Ke4 uses the third corner. White remains ready to return to e5 rather than pushing a pawn prematurely.",
            "Black returns to e7. Its two king turns contrast with White's three-move route.",
            "Ke5 restores the starting placement, now with Black to move. Pause and compare both kings and every pawn with the opening frame.",
            "Black chooses Kf8. The defender must now concede space; this is one branch of the resulting play.",
            "Kd6 takes diagonal opposition, preparing to answer a central retreat by approaching directly.",
            "Black steps to e8, attempting to keep White's king from penetrating.",
            "Ke6 takes direct opposition with the defender on e8 and controls the forward approach squares.",
            "Black returns to f8, yielding the central route.",
            "Kd7 advances farther while the pawns continue limiting the defender's kingside options.",
            "Black retreats to g8, staying near the promotion area.",
            "Ke7 supports the next approach and controls f8 and f7.",
            "Black reaches h8. Do not assume another king advance is best; inspect stalemate before continuing.",
            "f6 offers a pawn to remove the g7 blocker and create a passed g-pawn.",
            "Black chooses gxf6, accepting the sacrifice. White's g-file is now clear of enemy pawns ahead.",
            "Kf7 approaches to support the passed pawn while restricting the black king.",
            "Black advances its own pawn, a legal waiting move that does not stop White's promotion plan.",
            "g7+ advances with check, forcing the king away from h8 while White's king protects the pawn.",
            "Black must play Kh7. Other nearby squares are controlled by the supporting king or checking pawn.",
            "g8=Q+ promotes with check. The queen acts immediately, and Black must answer before advancing its own pawn.",
            "Black chooses Kh6, one legal check response, still close enough for White to finish at once.",
            "Qg6# is protected by Kf7. The queen and king cover every flight, proving the payoff in this branch.",
        )),),
        ("Walking a triangle is useful only if changing the side to move has a concrete benefit.",
         "A king maneuver must allow every opponent reply; extra pawn waiting moves can defeat a naive triangulation claim."),
        (
            check("triangle-count", "White makes three king moves while Black makes two, returning to the same placement. What has changed?",
                  ("The other player now has the turn", True, "The odd number of individual turns changes the side to move without changing placement."),
                  ("White has illegally taken two consecutive turns", False, "The turns alternated normally; the kings used routes of different lengths.")),
            check("triangle-reason", "Why might a king triangle fail to gain anything in another position?",
                  ("The opponent may have a useful escape, capture, or pawn waiting move", True, "The restricted useful replies are what make triangulation effective."),
                  ("Kings are never allowed to return to an earlier square", False, "Returning is legal; the question is whether it improves the resulting position.")),
        ),
        ("Find the position where moving is harmful.", "Count a three-versus-two route accurately.", "Calculate the gain after the turn changes, including stalemate risks."),
    ),
    "purposeful-exchanges": guide(
        (92, 96),
        ("Predict structural and activity changes after a trade.", "Compare an exchange with a reasonable retreat instead of trading automatically."),
        (
            section("Equal points can produce unequal positions", """
                Trading a bishop for a knight may leave the approximate material count unchanged while altering
                nearly everything about the position's character. An exchange can remove a defender, damage
                pawn structure, open a file, eliminate an active enemy piece, or simplify an ending. It can
                also help the opponent develop or activate a previously blocked bishop. Before taking, name
                your intended benefit and the cost you accept. A sacrifice deliberately gives more material
                than it immediately receives; an ordinary equal trade has different accounting, but both require
                evaluating the remaining position. 'I can capture' and 'the pieces have equal values' are not
                enough to explain why this particular trade belongs in your plan.
            """),
            section("Read both sides of a structural change", """
                In the opening example White can exchange the bishop on b5 for the knight on c6. After
                ...dxc6 Black has two pawns on the c-file and no d-pawn. That creates potential targets and
                changes which pawn breaks are available, but Black keeps both bishops. Vacating d7 opens
                the d-file for the queen and the c8 bishop's diagonal, giving activity as compensation for
                the structural change. The c6 pawn may also perform useful central control despite being
                doubled. Do not conclude that doubled pawns always lose or that giving up a bishop is
                automatically bad. Describe the resulting weaknesses and active resources together, then judge
                whether your remaining pieces can actually exploit the weaknesses you have created.
            """),
            section("Calculate the immediate tactics before the long-term verdict", """
                Removing the c6 knight might appear to leave e5 undefended, yet Nxe5 is not automatically
                a free pawn. Black's newly available queen activity can create tactical replies, and a natural
                ...Bd6 can defend e5 again. Long-term structural reasoning must therefore survive a short-term
                calculation. In the worked line White castles and Black develops the bishop rather than
                cooperating with a pawn grab. Compare the original Bxc6 decision with Ba4, a normal retreat
                that preserves the bishop and maintains different pressure. The exercise asks for the exchange
                to study its consequences; it does not declare every retreat wrong in a real game. A sound
                explanation ends with what changed and how each side might use it, rather than awarding a
                victory simply because one pawn file now contains two pawns.
            """),
        ),
        (example("Trade, recapture, then use the new position", after(("e4", "e5", "Nf3", "Nc6", "Bb5", "a6")), ("Bxc6", "dxc6", "O-O", "Bd6"), (
            "White's bishop is attacked by a6 and can retreat or exchange. The example chooses the structural trade, not an automatic best move in every game.",
            "White captures the c6 knight with the bishop. The material result is not final until Black replies.",
            "Black recaptures with the d-pawn, creating doubled c-pawns but retaining the bishop pair and opening lines from d7.",
            "White castles, improving king safety and rook development instead of assuming the e5 pawn is immediately free.",
            "Black develops the f8 bishop to d6, defending e5 and using the newly shaped position actively. Both structural liabilities and piece activity matter.",
        )),),
        ("Doubled pawns are a structural feature, not an automatic losing verdict.",
         "Removing a defender does not prove a pawn is free; check tactical replies and new defences."),
        (
            check("trade-purpose", "What should you identify before choosing an equal exchange?",
                  ("The concrete change in structure, activity, defence, or ending", True, "Equal material can lead to very different practical positions."),
                  ("Only that both pieces have the same point value", False, "The point count omits why either side benefits from the new arrangement.")),
            check("trade-bishops", "After Bxc6 dxc6, why is 'Black has doubled pawns, so White has won' incomplete?",
                  ("Black retains active resources, including two bishops and opened lines", True, "The weaknesses must be assessed alongside the opponent's compensation and tactics."),
                  ("Doubled pawns are illegal", False, "Two friendly pawns may legally occupy one file after a capture.")),
        ),
        ("State the purpose before exchanging.", "Account for both the weakness and the activity created.", "Check immediate tactics before trusting a long-term structural gain."),
    ),
    "chapter3-practice": guide(
        (120, 126),
        ("Search an unfamiliar position before choosing a tactical label.", "Calculate the defender's best reply and verify the final result.", "Compare a familiar mating pattern with a small but decisive defensive change."),
        (
            section("Begin with questions, not a motif name", """
                In a real game the position does not announce that a fork, pin, or sacrifice is available.
                First identify whose turn it is, whether either king is checked, and what the opponent's
                previous move threatened. Then list your forcing candidates: checks, significant captures,
                promotion threats, and serious threats against the king or material. Inspect loose pieces,
                overloaded defenders, alignments, blocked lines, and restricted flight squares as clues.
                The clue suggests where to calculate; it does not prove a move works. Choose a small set
                of candidates and compare actual replies rather than trying to attach every theme you have
                learned to every square on the board. Naming the successful mechanism comes after verifying it.
            """),
            section("Calculate from the opponent's point of view", """
                After each candidate, switch sides and search for the strongest legal answer. For a check,
                test capture, block, and safe king movement. For a sacrifice, count the recapture and inspect
                counterchecks before claiming compensation. For promotion, replace the pawn and count the
                defender's legal moves to avoid stalemate. Keep the board updated: remove captured pieces,
                open lines that lost blockers, and allow one reply after every move. If several moves achieve
                the same objective, compare them rather than treating the first remembered solution as unique.
                If your calculation ends in a material gain, also ask whether that gain changes a lost game
                to a draw or actually leaves a winning army. A precise result is more useful than an impressive
                phrase such as 'decisive combination' without a demonstrated ending.
            """),
            section("Test the pattern by changing one condition", """
                In the first replay Black attacks White's queen with ...Nf6, but White can ignore that attack
                because Qxf7 is immediate mate. The bishop on c4 protects the queen, while Black's own
                pieces obstruct the king. This combines coordination, a forcing capture, and king restriction.
                In the comparison Black instead plays ...g6 before the capture. The pawn on g6 blocks the
                queen's route from h5 to f7; the same remembered move is now unavailable. White retreats
                and Black develops to meet the renewed pressure. Explain the precise changed square, not
                merely 'the pattern no longer works'. Work slowly through a few mixed positions, record
                your candidate and predicted reply before revealing the next frame, then revisit errors later.
                The end-chapter assessment applies the chapter's ideas together; memorizing one quick-mate
                opening is not a substitute for this independent calculation habit.
            """),
        ),
        (example("A queen threat loses to an immediate mate", after(("e4", "e5", "Bc4", "Nc6")), ("Qh5", "Nf6", "Qxf7#"), (
            "White to move. The c4 bishop attacks f7, but needs another attacker and a protected checking destination.",
            "The queen joins the attack on f7 from h5. This creates a threat, but a sound defender can still answer it.",
            "Black attacks the queen with the knight instead of meeting the immediate mating threat. This is an instructive blunder, not forced play.",
            "White captures f7 with mate. The c4 bishop protects the queen, the king has no safe flight, and the adjacent check cannot be blocked.",
        )), example("One defensive pawn changes the calculation", after(("e4", "e5", "Bc4", "Nc6")), ("Qh5", "g6", "Qf3", "Nf6"), (
            "Reset the same position and investigate Black's defence rather than assuming the opponent repeats the blunder.",
            "White again threatens f7. Look at the queen's exact diagonal route through g6.",
            "Black's g-pawn occupies g6 and attacks the queen. It also blocks h5–g6–f7, so Qxf7 is no longer a legal queen move.",
            "White retreats to f3, preserving the queen and renewing pressure along the f-file.",
            "Black develops to f6, blocking that file and meeting the renewed pressure. The familiar mating picture has changed, so White needs a new plan.",
        ))),
        ("A familiar diagram is a clue, not permission to skip the opponent's strongest reply.",
         "A threat to your queen can be ignored only when the calculated consequence is stronger, such as immediate mate.",
         "A tiny blocker change can make a remembered move illegal rather than merely less effective."),
        (
            check("mixed-queen", "Your queen is attacked, but you have a legal checkmate immediately. What should you play?",
                  ("The verified checkmate", True, "Mate ends the game before the opponent gets a turn to capture the queen."),
                  ("Always retreat the queen first", False, "Material safety is secondary to an immediate legal game-ending mate.")),
            check("mixed-change", "A pawn now blocks the queen's h5–f7 diagonal. How should you respond to the familiar pattern?",
                  ("Recalculate the legal moves and the defender's replies", True, "The changed blocker may invalidate the old combination entirely."),
                  ("Play the memorized capture anyway", False, "A line piece cannot jump over the new blocker just because the old pattern was winning.")),
        ),
        ("Inspect the position before naming the theme.", "Calculate the opponent's best legal replies.", "Verify the result and retest the idea when one condition changes."),
    ),

}
