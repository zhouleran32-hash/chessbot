"""Detailed original teaching for printed pp. 211–240 of The Soviet Chess Primer.

Strategic miniatures are explicitly original illustrations. Named game fragments
and entertainment diagrams come from the user-supplied book and were checked
against legal boards; their explanations are newly written. A sample reply is
not claimed forced merely because it appears in the replay.
"""
from core.primer_build import after, custom
from core.primer_guides_chapter1 import check, example, guide, section

GUIDES = {}
EXERCISES = []


def add(key, title, pages, summary, goals, sections, examples, prompt, choices,
        questions, pitfalls, recap, *, quiz_fen=None, inventory=None, objective=None):
    """Keep each board task connected to its full study guide without duplicate FENs."""
    identifier = 'ch6-' + key
    GUIDES[identifier] = guide(pages, goals, sections, examples, pitfalls, questions, recap)
    EXERCISES.append(dict(id=identifier, title=title, summary=summary,
                          fen=quiz_fen or examples[0]['fen'],
                          inventory=inventory or examples[0]['notes'][0],
                          prompt=prompt, choices=choices, objective=objective))


CHAIN = custom({'g1':'K','f5':'P','g5':'P','h8':'k','h7':'n','a5':'r'})
add('pawn-skeleton', 'Read the pawn skeleton before choosing a plan', (211, 212),
    'Pawns change slowly and cannot retreat. Their arrangement tells your pieces where they can work. Learn the difference between connected pawns standing side by side and a chain with an exposed base; neither shape is automatically good or bad.',
    ('Identify a pawn chain’s base and its blockading square.', 'Compare space gained with squares abandoned.'),
    (
        section('The slow pieces give the position its shape', '''A pawn skeleton is the arrangement of both sides’ pawns. A pawn stopped by an enemy pawn or by an unsafe advance may stay on one square for many moves. Bishops, rooks, and knights must find jobs around that fixed structure. Start by locating blocked files, open diagonals, and possible pawn captures. Do not count space simply by counting advanced pawns. Ask which squares those pawns control, whether pieces can use the space behind them, and whether an enemy piece can settle safely in front of them.'''),
        section('Side by side is different from a chain', '''White’s f5 and g5 pawns initially control e6, f6, g6, and h6 between them. Advancing g5 to g6 gains a rank and makes g6 a pawn protected by f5, but gives up control of f6 and h6. The f5 pawn becomes the base: the rear pawn whose survival supports the advanced one. A knight on f6 can stop f5 from advancing while Black’s rook attacks f5 along the fifth rank. Notice the division of work: the knight blockades; the rook attacks the base. A chain’s front pawn may look vulnerable while the more useful target is behind it.'''),
        section('Calculate before approving the advance', '''Pause before revealing g6. Name the two squares the g5 pawn currently attacks, then imagine the pawn on g6 and repeat the list. Black’s knight can now jump from h7 to f6. White cannot use the f-pawn to capture a piece directly in front of it, and moving the g-pawn farther does not chase that knight. This original miniature isolates a structural cost; it does not prove g6 loses a full game or that a knight blockade is always possible. Test captures and checks before choosing any quiet blockading move in a real position.'''),
        section('When advancing is exactly right', '''A protected passed pawn may be a lasting strength, especially when the opponent cannot blockade it or reach its base. An advance can also gain a useful tempo by attacking a piece, fix an enemy weakness, or open a winning line. Compare those concrete benefits with the abandoned squares. For the attacker, bring pieces toward the base and prevent a freeing advance. For the defender, challenge the blockader, exchange the attacking rook, or arrange a pawn break. The practical question is whether the enemy can exploit the new shape before your advanced pawn accomplishes something valuable.'''),
    ),
    (example('Original illustration: an advance gives away f6', CHAIN, ('g6','Nf6'), (
        'White: king g1, pawns f5 and g5. Black: king h8, rook a5, knight h7. Watch the squares controlled by the g-pawn.',
        'g6 creates a supported advanced pawn, but removes the pawn’s control of f6. Pause: can the knight occupy the square now?',
        'Nf6 blockades f5, which cannot capture forward. The rook attacks the chain’s base along the fifth rank; the structure has become less mobile.',
    )),),
    'After g6, occupy the newly available blockading square f6 with the knight.',
    (('Nf6',True,'The knight occupies f6, directly in front of f5, and White’s pawns cannot chase it.'),('Ng5',False,'This moves to g5 and does not blockade the base on f5. The task is to occupy f6.'),('Ra8',False,'Moving the rook does not occupy the blockading square.')),
    (check('base','Which pawn is the base after g6?',('f5',True,'It is the rear pawn supporting g6.'),('g6',False,'g6 is the front of the chain; f5 supports it.')),
     check('advance','Does this show that advancing a pawn is always bad?',('No; assess benefits and whether the new weaknesses can be used.',True,'A protected passer or a useful attack may outweigh the abandoned squares.'),('Yes; a pawn should never leave its original square.',False,'Pawns must advance to gain space, free pieces, and promote.'))),
    ('Do not confuse a blockade with a direct attack: the knight on f6 does not itself attack f5.',),
    ('Map pawn attacks before and after the move.', 'Find the chain’s base and its possible blockader.'),
    quiz_fen=after(('g6',),CHAIN))

BACKWARD = custom({'g1':'K','f4':'N','d1':'R','g8':'k','d8':'r','c5':'p','d6':'p','e5':'p','g7':'p'})
add('backward-pawns', 'Isolated, doubled, and backward pawns', (215, 216),
    'A pawn weakness matters when it ties pieces to defence or gives the opponent an entry square. Learn three common shapes, then distinguish their appearance from their practical consequences.',
    ('Recognize isolated, doubled, and backward pawns.', 'Use a blockade without assuming that a pawn falls immediately.'),
    (
        section('Name the shape accurately', '''An isolated pawn has no friendly pawn on either adjacent file. A doubled pair consists of two friendly pawns on one file; they cannot defend one another directly. A backward pawn trails its neighbors and cannot safely advance to join them. These descriptions can overlap. A group of connected pawns is an island; more islands often mean more separate defensive duties. Yet an isolated pawn can control useful central squares, doubled pawns can guard important entry points, and a backward pawn may remain securely defended for the whole game.'''),
        section('Why a piece may become a pawn’s servant', '''A pawn that cannot receive pawn protection often needs a rook, bishop, knight, or king to defend it. That defender then has less freedom elsewhere. In the original miniature Black’s d6 pawn lies behind c5 and e5. Those neighbors have passed the squares from which they could support a pawn on d6. White’s rook watches the d-file, while Black’s rook defends d6 from behind. Taking d6 immediately would allow a recapture, so simply pointing at the pawn is not enough. Occupying d5 prevents the pawn’s freeing advance and gives White’s knight a useful job.'''),
        section('Freeze first, then build pressure', '''Before playing Nd5, check whether a black c-pawn or e-pawn can attack d5: from c5 and e5 they attack d4, not d5. The knight can therefore blockade the pawn without being chased by those pawns. A later attack might add a second piece or create a target on the other wing. White must also watch tactical exchanges of the blocker. Black should seek a favorable exchange, active rook play, or a prepared advance rather than resigning mentally because a label says “backward.” The replay shows the structure; it does not force the pawn’s capture.'''),
        section('Count compensation and possible repairs', '''Doubled pawns on a rook file tend to have fewer ways to support neighboring pawns, while doubled central pawns can strengthen control of valuable squares. A capture may undouble them later. Similarly, an isolated central pawn may provide open files and active bishops before an endgame exposes it. When considering an exchange that damages your structure, draw the resulting board in your mind: what file opens, what square becomes available, and which pieces remain to attack the weakness? Avoid exchanging into a passive ending merely because the material count stays equal.'''),
    ),
    (example('Original illustration: blockade a backward d-pawn', BACKWARD, ('Nd5','Kf7'), (
        'White has a king, rook, and knight; Black a king, rook, and four pawns. The d6 pawn is defended by d8 but cannot be supported by c5 or e5.',
        'Nd5 occupies the square in front of d6. Check that neither neighboring black pawn attacks the knight.',
        'Kf7 is an illustrative king improvement. Black can defend the pawn while White develops a longer plan; no immediate capture is claimed.',
    )),),
    'Blockade the backward pawn on d6 by putting the knight on d5.',
    (('Nd5',True,'The knight stops ...d5 and uses a square the c5/e5 pawns cannot attack.'),('Rxd6',False,'This captures the defended pawn and allows ...Rxd6; it does not establish the requested blockade.'),('Nh5',False,'The knight leaves the central area without stopping ...d5.')),
    (check('isolated','What makes a pawn isolated?',('No friendly pawn on an adjacent file.',True,'Its neighbors cannot come across to support it.'),('It is two squares ahead of its starting square.',False,'Advancement alone does not determine isolation.')),
     check('practical','What turns a pawn defect into a practical problem?',('An opponent can attack it or use the squares it leaves.',True,'An inaccessible weakness may have little effect.'),('Its diagram looks untidy.',False,'The available plans and defenders determine its importance.'))),
    ('Do not sacrifice a rook for a defended pawn merely to “win the weakness.”',),
    ('Structure gives targets, not automatic wins.', 'Inspect defenders and freeing pawn breaks.'))

OUTPOST = custom({'g1':'K','b4':'N','b5':'P','d5':'P','h8':'k','d7':'b','b6':'p','d6':'p','h7':'p'})
add('outposts', 'Holes, outposts, and exchanging the blockader', (212, 213),
    'A hole is a square the pawns cannot readily control. An outpost is a useful, stable station for a piece. Learn how a strong knight can create threats and why exchanging it may leave a new problem.',
    ('Find a supported square enemy pawns cannot challenge.', 'Evaluate the pawn structure after an exchange.'),
    (
        section('A square can be weak without holding a pawn', '''A weakness is not always a piece you can capture. When pawns advance, they abandon squares that can become entry points. An outpost usually combines support with useful work: a knight entrenched near the enemy can attack several targets while being hard to chase. In this miniature White wants c6. White’s b5 and d5 pawns support it. Black’s b6 and d6 pawns attack c5, so neither can drive a knight from c6. The outpost lies inside Black’s camp, where its influence may matter more than a knight’s average point value.'''),
        section('Check the route and the exchange', '''The knight on b4 can jump directly to c6. Before revealing the move, identify every black piece able to capture c6 and the pawn White would use to recapture. Black’s bishop on d7 can exchange the knight. After Bxc6 and dxc6, White has a protected passed pawn on c6, supported by b5. The black b6 and d6 pawns are already behind the passer from White’s perspective and cannot stop it by moving straight forward. The exchange changes the form of White’s advantage instead of automatically erasing it.'''),
        section('Make the outpost do useful work', '''An advanced knight may attack rooks, block communication between the wings, cover an invasion square, or shelter the doubling of rooks on a file. Sometimes the knight later moves away deliberately so a rook can invade through the square it vacates. Do not leave it planted merely because the square has a fashionable name. Ask what threat or improvement it enables on your next turn. Also inspect enemy counterplay: if your own king is exposed, a beautiful knight post may be less urgent than answering a check or preventing mate.'''),
        section('Defend before the hole is occupied', '''The defender can exchange the approaching knight, control its route, prepare a pawn break against its support, or arrange an acceptable recapture structure. A pawn move that leaves a hole may still be necessary to gain activity. The important habit is to assess the future square before making that irreversible move. Our replay deliberately allows the exchange to demonstrate its consequences, not to claim it is Black’s only reply. A protected passer still needs help to promote; kings, blockades, and opposing pieces must be included before calling the ending won.'''),
    ),
    (example('Original illustration: knight outpost becomes a passer', OUTPOST, ('Nc6','Bxc6','dxc6'), (
        'White: king g1, knight b4, pawns b5/d5. Black: king h8, bishop d7, pawns b6/d6/h7. The target is c6.',
        'Nc6 reaches a square supported by both white pawns. The black neighboring pawns cannot attack it.',
        'Bxc6 removes the knight. Pause before recapturing: what kind of pawn will White have on c6?',
        'dxc6 leaves a protected passed pawn, supported by b5. Black has traded a piece problem for a pawn problem.',
    )),),
    'Occupy the supported outpost c6 with the knight.',
    (('Nc6',True,'The knight reaches the supported entry square.'),('Nc2',False,'This retreats away from the c6 outpost.'),('Kf2',False,'The king move leaves the intended outpost empty.')),
    (check('hole','Why can Black’s b6 pawn not chase a knight on c6?',('It attacks a5 and c5.',True,'Black pawn attacks point toward lower rank numbers.'),('Pawns never attack knights.',False,'Pawns attack any enemy piece on their capture squares.')),
     check('exchange','Does exchanging an outpost piece always remove the problem?',('No; inspect the recapturing pawn and resulting structure.',True,'Here a protected passed pawn replaces the knight.'),('Yes; the square becomes irrelevant.',False,'The recapture can preserve or increase the pressure.'))),
    ('An outpost that creates no useful threats may be less important than active play elsewhere.',),
    ('Check support, pawn challenges, and exchanges.', 'Assess the board after the recapture.'))

HOOK = custom({'g1':'K','f3':'N','f2':'P','g2':'P','h3':'P','c8':'k','h8':'r','g5':'p','h5':'p'},turn='b')
add('king-hooks', 'Pawn shields, hooks, and a useful escape square', (213, 215),
    'A pawn move beside your king can solve a problem and create another. Learn why an advanced h-pawn can become a target, when an escape square is useful, and how the stage of the game changes the decision.',
    ('Explain how a pawn hook helps open a file.', 'Balance king safety against a concrete need for luft.'),
    (
        section('The shield is a set of barriers', '''A castled king normally benefits from pawns in front of it because enemy rooks and bishops need open lines. With a king on g1, rook on f1, and pawns on f2, g2, h2, the pawn wall limits direct access. Advancing one pawn changes that barrier permanently. It may create a square the king can use, but it also gives an enemy pawn something to capture. A hook is an advanced pawn that makes it easier for the attacker to open a line by pushing a neighboring pawn into contact.'''),
        section('How h3 can become a target', '''The original demonstration has White’s king on g1, knight on f3, and pawns f2/g2/h3; Black has a rook on h8 and pawns g5/h5. Black pushes ...g4, attacking the knight and the h3 pawn. If White answers hxg4, then ...hxg4 removes the black pawn from the h-file and clears the white h-pawn from it too. The rook now has an open h-file beside White’s king. It is not checkmate, and it is not even check in this position: opening a line creates access that still needs supporting pieces.'''),
        section('Compare the other response before moving', '''Before replaying the captures, calculate what changes if White moves the knight instead. Black may capture on h3; after gxh3, White’s pawn shield has been split and the g-file has opened. That is a different kind of damage, not a reason to assume every knight move loses. White should look for an active central reply, exchange attacking pieces, or prevent the pawn contact earlier. Always calculate captures in both directions and inspect your opponent’s checks. A pattern warns you what to examine; it does not replace the calculation.'''),
        section('Luft and endgames are genuine exceptions', '''An escape square, often called luft, can prevent a back-rank mate. If a real threat requires h3 or h4 and the square is safe, making it is useful. Playing h3 automatically on move six may instead delay development and provide a hook. Similarly f3 can expose the diagonal toward g1 and occupy a knight’s preferred square in the middlegame, yet help the king travel centrally after queens and attacking pieces disappear. Decide from the current threats and remaining pieces. Do not preserve an immaculate pawn wall while ignoring a mate that a small pawn move would prevent.'''),
    ),
    (example('Original illustration: opening the h-file through a hook', HOOK, ('g4','hxg4','hxg4'), (
        'Black moves: king c8, rook h8, pawns g5/h5 against White’s king g1, knight f3 and f2/g2/h3 shield. Identify the hook on h3.',
        '...g4 attacks both the knight on f3 and the h3 pawn. Pause and calculate both pawn captures before proceeding.',
        'hxg4 captures the attacking pawn but removes White’s pawn from the h-file. This is one illustrative response.',
        '...hxg4 removes Black’s pawn from the h-file too. The rook’s file is open; Black still needs to build an actual attack.',
    )),),
    'Start the demonstrated pawn contact: move the g-pawn to g4, attacking the knight and h3.',
    (('g4',True,'The pawn advances to attack f3 and h3, exploiting the hook.'),('h4',False,'This locks contact against h3 rather than starting the demonstrated g-file capture sequence.'),('Rh6',False,'A rook lift may have another purpose, but it does not make the specified pawn contact.')),
    (check('luft','When is making an escape square justified?',('When it answers a real danger or serves a concrete plan.',True,'A useful purpose can outweigh the structural cost.'),('Whenever a pawn move is available.',False,'Automatic pawn moves waste time and can create attack targets.')),
     check('file','Does opening the h-file prove immediate mate?',('No; check the attackers, defenders, and king escapes.',True,'Access is an advantage only if usable.'),('Yes; every open file beside a king gives mate.',False,'A lone rook may lack the support to finish an attack.'))),
    ('Do not describe a newly opened file as checkmate without inspecting the board.',),
    ('Pawn contact can open king lines.', 'Balance permanent weaknesses against immediate needs.'))

FIANCHETTO = custom({'g1':'K','f1':'R','g2':'B','f2':'P','g3':'P','h2':'P','g8':'k','a8':'r','d7':'b','f7':'p','g7':'p','h7':'p'},turn='b')
add('colour-complexes', 'The fianchetto bishop and weak colour complexes', (214, 216),
    'A fianchetto uses a bishop on b2 or g2, or b7/g7 for Black. The bishop and pawns work together. Removing that bishop can change the safety of an entire group of squares.',
    ('Distinguish a weak square from a weak colour complex.', 'Identify the defender before arranging an exchange.'),
    (
        section('Several holes can belong to one network', '''A colour complex is a group of squares of the same colour that can become accessible together. Moving g2 to g3 means the pawn no longer controls f3 and h3. If a white bishop stands on g2, it covers both squares, looks along the long diagonal, and helps maintain the king’s shelter. The pawn move is part of a coordinated arrangement, not automatically a mistake. Conversely, a bishop trapped behind its own pawns may offer far less protection than its position beside the king suggests.'''),
        section('Exchange the piece that fills the gaps', '''In the original example Black’s bishop on d7 can reach h3 through e6, f5, and g4. The move ...Bh3 offers an exchange of the light-squared bishops. If White captures Bxh3, then ...R? is not a legal automatic recapture in this miniature; Black has simply sacrificed a bishop unless something concrete supports it. We therefore demonstrate the attacker capturing on g2 after White moves the king. That is an illustrative choice, not forced cooperation in a winning attack. The point is to inspect which squares lose a defender when the bishop disappears.'''),
        section('Follow the whole exchange, including the recapture', '''Pause before the first move and trace the diagonal from d7 to h3. After ...Bh3, White can also decide to preserve or exchange the bishop depending on the rest of the position. In our line Kh1 allows ...Bxg2+ and Kxg2. Both bishops are gone; White’s king has recaptured and the light squares f3/h3 are no longer covered by a bishop. The remaining rook and pawns may still make the position perfectly playable. You have identified a change in defensive resources, not proved a forced attack.'''),
        section('What each side should do next', '''The attacker needs pieces that can enter the weakened squares and a safe route to them. A queen-and-bishop battery may prepare an exchange; a knight may later occupy f3 or h3. The defender can challenge the attacking pieces, keep the important bishop, give the squares alternative protection, or simplify into an ending where king activity matters more. Count whether the exchange also removes the opponent’s only attacking bishop. The same trade can weaken a colour complex while reducing immediate danger, which is why a slogan about “never exchanging a fianchetto bishop” is too rigid.'''),
    ),
    (example('Original illustration: the defender of the light squares disappears', FIANCHETTO, ('Bh3','Kh1','Bxg2+','Kxg2'), (
        'White’s bishop g2 helps cover f3/h3 behind the f2/g3/h2 shield. Black’s bishop d7 has a clear route to h3. Both sides also have a rook.',
        '...Bh3 brings Black’s bishop beside the fianchetto bishop. White is free to choose among responses; this is an exchange motif, not a forced win.',
        'Kh1 illustrates allowing the exchange. Pause: what must White answer if Black captures g2 with check?',
        '...Bxg2+ removes the bishop that helped guard the light squares. Black’s bishop now checks the king from g2.',
        'Kxg2 recaptures. Both bishops have disappeared; assess the remaining position before imagining a successful attack.',
    )),),
    'Bring the bishop from d7 to h3 to offer the demonstrated fianchetto-bishop exchange.',
    (('Bh3',True,'The bishop reaches h3 along the clear diagonal.'),('Be6',False,'This is on the route but does not yet offer the specified exchange.'),('Ra2',False,'This moves a rook and does not address the bishop on g2.')),
    (check('cover','What does the g2 bishop contribute after g3?',('It covers f3 and h3 and uses the long diagonal.',True,'The piece helps compensate for pawn squares that were abandoned.'),('It makes the king immune to every attack.',False,'Files, exchanges, and tactical threats still matter.')),
     check('trade','What must you assess after removing that bishop?',('Whether other attackers can use the weakened squares.',True,'A missing defender is relevant only when the enemy can exploit it.'),('Only the bishop’s usual three-point value.',False,'Its defensive job may matter more than its average value.'))),
    ('Never assume a bishop offer is sound without checking the recapture and concrete threats.',),
    ('Identify squares and the piece defending them.', 'An exchange changes both attack and defence.'))

DANISH = after(('e4','e5','d4','exd4','c3','dxc3','Bc4','cxb2','Bxb2','Nc6'))
add('development-clock', 'A lead in development has an expiry date', (216, 218),
    'Active pieces may compensate for a pawn deficit, but the opponent can catch up. Use a development lead to mobilize, open useful lines, or obtain a lasting gain; do not mistake an exciting appearance for a guaranteed attack.',
    ('Distinguish temporary activity from permanent structure.', 'Bring reserves into an attack before the opponent catches up.'),
    (
        section('Count useful pieces, not just moves', '''Development means bringing pieces into useful action. A queen that moved four times has consumed four turns without developing four pieces. When one side has several active units and the other still has bishops and rooks at home, the active side may have a temporary advantage. Temporary means the opponent can repair it with moves. Count which pieces can actually reach the area of the fight. A developed knight on the wrong wing may contribute less than a bishop still at home with a clear attacking diagonal.'''),
        section('Understand what compensation is buying', '''Our opening fragment reaches a Danish Gambit position: White has exchanged three pawns for one and is therefore two pawns down. In return both bishops are active and the central files have fewer pawn obstructions. Black has just developed Nc6. This is a teaching example of activity purchased with material, not a recommendation to sacrifice two pawns in every game. White still needs to bring out the g1 knight and secure the king. Compensation is a collection of concrete benefits, not a refund that the rules promise after a sacrifice.'''),
        section('Use the remaining development time', '''Pause before Nf3 and list the pieces White has not yet mobilized. Nf3 develops a knight toward the centre and clears the way to castle. Black answers ...d6 in the sample line, opening the c8 bishop’s diagonal, and White castles. Both sides are improving, so White cannot expect Black’s development deficit to last indefinitely. In the book’s Chigorin–Shabelsky example the attack forces lasting damage to Black’s pawn structure. That is the general conversion: use time to gain material, safer structure, an enduring outpost, or some other benefit that survives the opponent’s mobilization.'''),
        section('How the defender fights back', '''When behind in development, finish mobilizing, exchange a dangerous attacker when safe, and challenge the centre before a flank attack grows. A queen exchange can sharply reduce king danger, but only if it does not lose something concrete. The attacker should seek energetic moves, yet “energetic” does not mean every move must be a sacrifice or check. Bringing up the last piece can be the most purposeful move. Before opening the position, calculate whether your own uncastled king becomes the more exposed one. Reassess after each exchange because the source of compensation may have changed.'''),
    ),
    (example('Opening illustration: develop the reserve in a gambit', DANISH, ('Nf3','d6','O-O'), (
        'White has two active bishops but is two pawns down; Black has developed a knight to c6. White’s g1 knight and king still need attention.',
        'Nf3 brings another piece toward the centre and permits kingside castling. It also eyes e5, currently defended by Nc6.',
        '...d6 supports e5 and opens the c8 bishop. This is one illustrative defence; Black is working to catch up.',
        'O-O secures White’s king and brings a rook toward the central files. Activity is improving, but the material deficit remains real.',
    )),),
    'Mobilize the g1 knight to f3, making kingside castling possible.',
    (('Nf3',True,'The knight joins play and clears g1 for castling.'),('Nh3',False,'This develops the same knight but misses the specified central square f3.'),('a3',False,'This does not develop the g1 knight or complete the castling route.')),
    (check('expiry','Why can a development lead disappear?',('The opponent can bring remaining pieces into play.',True,'Activity gained in time must accomplish something before the deficit is repaired.'),('Active pieces lose material value after ten moves.',False,'There is no move-count rule; concrete mobilization changes the position.')),
     check('reserves','Must every attacking move give check?',('No; mobilizing another attacker may be essential.',True,'A coordinated army often achieves more than repeated unsupported checks.'),('Yes; a quiet move always abandons the initiative.',False,'Quiet threats and development can maintain pressure.'))),
    ('A gambit’s attractive bishops do not prove enough compensation against best defence.',),
    ('Count combat-ready units.', 'Convert temporary activity into something lasting.'))

WORST = custom({'g1':'K','a1':'N','c3':'P','e3':'P','g2':'P','g8':'k','d5':'p','e6':'p','f7':'p','h7':'p'})
add('improve-worst-piece', 'Space, cramped pieces, and a route with a purpose', (218, 221),
    'A cramped army can have all its pieces developed and still struggle to move. Compare actual routes and useful squares, then improve the piece doing the least work.',
    ('Plan a short route for an inactive piece.', 'Distinguish a cramped position from a lost position.'),
    (
        section('Space makes cooperation easier', '''Space is control of territory that your pieces can use safely. More room can make it easier to transfer a rook from one wing to the other or bring several attackers to one target. The side with less space may have pieces obstructing each other even after completing development. This is different from being behind in development: the pieces have left home but still lack useful work. More space is valuable only when it can be maintained. Overextended pawns that cannot be supported may give the opponent targets instead of confining them.'''),
        section('Find the least useful member of the army', '''In the original endgame miniature White’s knight on a1 is far from the central pawns. The king on g1 and pawns c3/e3/g2 do not need an immediate tactical rescue. The useful destination is d4, a square supported by both c3 and e3, directly in front of Black’s d5 pawn. The route a1–b3–d4 takes two knight moves. Name the destination first, then find the route. Randomly moving the knight toward the centre may work occasionally, but a square with a specific job gives your improvement a clear purpose.'''),
        section('A route must survive the opponent’s turns', '''Pause before Nb3 and ask what Black could do between the two jumps. In the sample line ...Kf8 improves Black’s king, then Nd4 completes the route. Black was not forced to cooperate: another reply could change the plan. In a richer position the knight might be captured on b3, the destination might be challenged, or a threat to your king might take priority. Calculate one enemy move after every step. A beautiful three-move maneuver is useless if you are expecting the opponent to remain motionless while you execute it.'''),
        section('Relieve a cramped position intelligently', '''The cramped side often welcomes exchanges because fewer pieces need room, but should not exchange the one piece that holds essential squares. A prepared pawn break can open space more effectively than endless shuffling. The side with space can improve its worst piece, prevent freeing breaks, and create a second target. In the book, badly placed individual pieces sometimes become tactical liabilities; a trapped rook or knight may be lost through a combination. Therefore check mobility as well as protection: a defended piece with no safe retreat can still be vulnerable to a pawn attack.'''),
    ),
    (example('Original illustration: a1–b3–d4 gives the knight a job', WORST, ('Nb3','Kf8','Nd4'), (
        'White’s knight a1 is inactive. White pawns c3/e3 support d4; Black’s d5/e6/f7 pawns form the central barrier. Both kings are on the g-file.',
        'Nb3 starts a two-step route to d4. It is an improvement toward a named destination, not a forced threat.',
        '...Kf8 is a sample reply bringing Black’s king toward the centre. Other replies must be checked in a real game.',
        'Nd4 completes the route and blocks the d5 pawn. White’s knight now cooperates with c3 and e3.',
    )),),
    'Start the knight route a1–b3–d4 by moving to b3.',
    (('Nb3',True,'The knight heads toward the supported square d4.'),('Nc2',False,'This is another legal jump, but it is not the demonstrated route through b3.'),('Kf2',False,'The king can improve later; the task specifically asks for the knight route.')),
    (check('route','What makes a maneuver a plan rather than a shuffle?',('A useful destination and a route that survives replies.',True,'Both purpose and timing matter.'),('Moving the same piece at least three times.',False,'Repeated movement alone can waste time.')),
     check('cramped','Should the cramped side exchange every piece it can?',('No; preserve essential defenders and assess the ending.',True,'Some exchanges relieve congestion while others remove critical protection.'),('Yes; all exchanges help equally.',False,'Which pieces remain matters more than the number of trades.'))),
    ('Do not plan two of your own moves without allowing the opponent a turn.',),
    ('Name the worst piece’s next useful square.', 'Check both tactical safety and long-term mobility.'))

BREAK = custom({'g1':'K','e1':'R','g2':'B','b3':'P','c4':'P','d4':'P','g8':'k','b8':'r','e7':'b','b5':'p','c6':'p','e6':'p'})
add('make-weakness-usable', 'From a defended weakness to a pawn breakthrough', (221, 224),
    'An enemy weakness may remain defended for a long time. Learn how a pawn break can change the structure, release a blocked line, or add an attacker that your pieces alone could not supply.',
    ('Connect a pawn break to a concrete target.', 'Distinguish pressure from an immediate forced win.'),
    (
        section('A defended pawn can still restrict an army', '''If all your pieces point at a pawn and the opponent has enough defenders, one more routine attacking move may accomplish nothing. Yet that pawn can still tie enemy pieces to passive squares or block their communication between wings. The book’s Chigorin–Tinsley example combines a blockade with a queenside break; Sorokin–Lisitsyn uses a pawn breakthrough to reach e6. The shared principle is to look for a new way of changing the position when adding another piece attack is impossible. Pawns can create contact where a rook or bishop cannot.'''),
        section('Trace what a break opens', '''Our original miniature gives White king g1, rook e1, bishop g2, and pawns b3/c4/d4; Black has king g8, rook b8, bishop e7, and pawns b5/c6/e6. White considers cxb5. If Black recaptures ...cxb5, the c-pawn leaves c6. White then plays d5, attacking e6 and offering a pawn on the g2 bishop’s diagonal through f3 and e4. The diagonal’s former c6 obstruction has already moved away. The point is not merely to exchange pawns: it is to give a previously obstructed piece access to the centre and force the defender to reconsider the shape of the position.'''),
        section('Calculate the captures, then reassess', '''Pause before d5 and imagine both ...exd5 and a refusal to capture. The shown capture allows Bxd5+, activating the bishop with check and clearing Black’s e6 pawn from its original defensive role. Black has other legal choices, so this is an explanation of how the break works against one response, not proof of a forced win. Notice that the number of pieces has not changed. A transformation can matter because of activity and squares even when no piece is won. After the sequence, inspect the rook files, king safety, and remaining pawns afresh.'''),
        section('The defender’s resources and the second target', '''Before allowing a breakthrough, the defender can stop the supporting pawn advance, exchange the piece that would gain a line, or counterattack elsewhere. Hanging pawns—often adjacent central pawns without neighbors on the outside—can control a broad front while side by side, yet an advance may create a hole behind them. The attacker may provoke that advance by pressure rather than capture immediately. When one target remains secure, transfer pressure to another part of the board and see whether the same defender can cover both. Still answer checks first: a slow squeeze cannot outrun an immediate mating threat.'''),
    ),
    (example('Original illustration: a pawn break frees a bishop', BREAK, ('cxb5','cxb5','d5','exd5','Bxd5+'), (
        'White’s g2 bishop points through f3/e4/d5 toward Black’s c6 pawn. White’s pawn d4 can advance onto d5 to challenge e6; it is not initially on the bishop’s diagonal.',
        'cxb5 starts an exchange on the queenside. Pause and identify which black pawn can recapture.',
        '...cxb5 is the chosen reply; Black’s c-pawn leaves c6 and reaches b5. Other replies are possible.',
        'd5 attacks e6 and offers the pawn on the bishop’s diagonal. If Black captures, the bishop can recapture on d5 with check.',
        '...exd5 accepts the exchange and places a black pawn on the newly accessible diagonal.',
        'Bxd5+ activates the bishop with check toward g8. White has converted pawn contact into piece activity, without a claim of a forced win.',
    )),),
    'Begin the demonstrated sequence by capturing the b5 pawn with the c-pawn.',
    (('cxb5',True,'This starts the specific queenside exchange whose recapture changes the pawn structure.'),('c5',False,'Advancing the pawn does not make the specified capture.'),('Re5',False,'A rook move does not begin the pawn-contact sequence.')),
    (check('break','What should you identify before pushing a pawn break?',('The target or line the break changes.',True,'A purpose lets you compare captures and refusals.'),('Only whether the pawn can legally advance.',False,'A legal push can create weaknesses without useful compensation.')),
     check('pressure','Must a defended weakness be captured immediately to matter?',('No; defenders may be tied down and another target can arise.',True,'Restriction can support a later breakthrough.'),('Yes; pressure without an immediate capture has no value.',False,'Many positional plans work by limiting the defender’s choices.'))),
    ('Do not call the displayed recapture forced when the opponent can decline it.',),
    ('Ask what changes after every pawn capture.', 'Use breaks and new targets when direct pressure stalls.'))

MOBILE = after(('e4','e5','Nf3','Nc6','Bc4','Bc5','c3','Nf6'))
add('mobile-centre', 'Build and support a mobile pawn centre', (224, 225),
    'Pawns on d4 and e4 can restrict the opponent and prepare an advance, but the pieces must support them. Learn to read a central exchange rather than treating a large centre as a trophy.',
    ('Explain what a two-pawn centre controls.', 'Calculate central captures and checks before advancing.'),
    (
        section('The centre is a crossroads', '''The four central squares are d4, e4, d5, and e5. The extended centre reaches out toward c3, c6, f3, and f6. Pieces near these squares can often transfer to either wing quickly. A pawn centre on d4/e4 takes away valuable squares, opens routes for both bishops, and gives knights natural support nearby. Its strength includes the option of advancing d5 or e5 at the right moment. Keeping that option alive can be more valuable than using it immediately, because the opponent must account for both possible pushes.'''),
        section('Pawns need a supporting team', '''In the opening illustration White has developed Nf3 and Bc4 and prepared d4 with c3. Black has Nf6, Nc6, Bc5, and a pawn e5. The move d4 attacks both Black’s central pawn and the bishop c5. After ...exd4, White can use the c3 pawn to recapture, placing pawns on d4 and e4. That is the intended structure, but White’s king is still in the centre. The attractive pawn pair does not cancel immediate checks or the possibility that one of the pawns is insufficiently defended.'''),
        section('The opponent has forcing moves too', '''Before showing ...Bb4+, stop and trace the bishop’s diagonal to e1. Because the c-pawn has left c3 and d2 is empty, the check is real. White can answer Nc3, developing a piece and blocking the line. The knight also supports the e4 pawn, although its pin to the king must be considered in later calculations. This is a legal instructional opening line, not a promise that White has forced an advantage. It demonstrates how the centre, development, and king safety interact on each turn.'''),
        section('Choose the break from the position', '''A supported central push can open files against an uncastled king or drive a defender away. In other cases a stable centre provides cover for a flank attack and makes it easier to switch pieces between wings. Before pushing, ask what square is abandoned, which enemy piece gains a blockade, and whether your rear pawn becomes a target. A single well-supported central pawn can be more useful than two advanced pawns constantly needing defence. The defender should attack the centre with pieces and pawn breaks, using captures or pressure to provoke a weakening advance.'''),
    ),
    (example('Opening illustration: central ambition meets a check', MOBILE, ('d4','exd4','cxd4','Bb4+','Nc3'), (
        'Both sides have active minor pieces. White’s c3 pawn prepares a recapture on d4, but White’s king remains e1.',
        'd4 challenges e5 and attacks the bishop c5. Identify Black’s captures and checks before looking ahead.',
        '...exd4 exchanges Black’s central pawn for White’s d-pawn. The white c3 pawn can recapture.',
        'cxd4 creates White pawns d4/e4 and vacates c3. That vacated square also opens a checking diagonal.',
        '...Bb4+ checks along b4–c3–d2–e1. Central plans must pause to answer the king’s immediate danger.',
        'Nc3 develops and blocks the check. White has a centre, but it still requires protection and timely castling.',
    )),),
    'Play the prepared d-pawn advance to d4, challenging e5 and attacking the bishop c5.',
    (('d4',True,'The prepared central push creates the intended pawn contact.'),('d3',False,'This supports e4 but does not attack e5 or the bishop c5 as requested.'),('h3',False,'This does not address the centre or make use of the c3 preparation.')),
    (check('support','What turns a pawn centre into a dependable asset?',('Piece support and useful safe advances.',True,'Pawns alone can become targets.'),('Occupying two central squares regardless of threats.',False,'An unsupported centre may collapse under pressure.')),
     check('check','Why must White consider ...Bb4+ after cxd4?',('The c3 square and d2 square are empty on the diagonal to e1.',True,'The exchange changes lines as well as pawn counts.'),('All bishop moves after a central exchange give check.',False,'The precise diagonal and blockers determine check.'))),
    ('Do not assume a pinned knight can defend by moving away from its king’s line.',),
    ('Support before pushing.', 'Recheck lines after every central exchange.'))

UNDERMINE = after(('d4','Nf6','c4','g6','Nc3','Bg7','e4','d6','Nf3','O-O','Be2'))
add('undermine-centre', 'Attack the centre at its base', (225, 228),
    'When the opponent owns a broad pawn centre, attack its support and make it decide whether to capture, advance, or hold. A central push can exchange one advantage for a different weakness.',
    ('Recognize a flank-pawn challenge to a central pawn.', 'Evaluate the squares and targets left by an advance.'),
    (
        section('A large centre is a responsibility', '''A pawn centre has to survive enemy pressure. Pieces can attack its pawns while c- or f-pawns challenge the base from the side. This makes the centre choose: maintain tension, capture, or advance. Each choice changes the board. Capturing may open a file; advancing may abandon a strong blockading square. The book’s Pillsbury–Chigorin example shows pressure inducing e5, after which Black uses d5 and attacks the rear d4 pawn. The lesson is not “never play e4”; it is to count the actual supporters and attackers before building a large centre.'''),
        section('A modern opening shape makes the contact visible', '''Our illustration begins with White pawns c4/d4/e4, knights c3/f3, bishop e2, and an uncastled king. Black is castled, has Nf6/Bg7, and pawns d6/g6. Black challenges d4 with ...c5. White may capture, keep the tension, or push d5. In the shown line d5 gains space, but now Black plays ...e6 against that advanced pawn. Both moves attack a concrete part of the centre. Black has not destroyed it merely by naming a pawn break; White can meet the pressure with development and recaptures.'''),
        section('Follow the pawn identities', '''Pause after ...e6 and decide which pawn can recapture if Black eventually takes d5. White castles first in the sample line, then ...exd5 is answered by cxd5. The pawn now on d5 began on c2, while White’s original d-pawn has disappeared. This matters because the remaining c-file and e-file have changed. Pawn labels are useful shorthand, but the actual squares and open lines determine the plans. The line demonstrates a structural transformation, not a forced advantage for either side or a unique best opening sequence.'''),
        section('Defence can be active rather than submissive', '''The centre owner should develop supporting pieces, answer threats efficiently, and advance only when the resulting position is useful. Sometimes a pawn sacrifice releases bishops and creates a dangerous mobile centre, as the book’s Kotov–Lilienthal and Verlinsky–Kirillov examples show. Those are concrete judgments, not permission to discard pawns whenever they are attacked. The challenger should avoid opening the game while badly behind in development or exposing the king. Compare king safety, available lines, and piece activity after the captures. A central break that wins one pawn while allowing mate is not a successful strategy.'''),
    ),
    (example('Opening illustration: ...c5 and ...e6 challenge a broad centre', UNDERMINE, ('c5','d5','e6','O-O','exd5','cxd5'), (
        'Black to move against White’s c4/d4/e4 centre. Black’s king is castled; White’s king has not yet castled. Watch the pressure on d4 and then d5.',
        '...c5 attacks d4 from the side and asks White to choose a central structure.',
        'd5 gains space and avoids an immediate exchange on d4, while giving Black a new contact point.',
        '...e6 challenges the advanced pawn on d5. Pause and identify White’s possible recapture after ...exd5.',
        'O-O secures White’s king before the central exchange. This is an illustrative continuation, not forced.',
        '...exd5 exchanges Black’s e-pawn for White’s d-pawn and opens the e-file for Black.',
        'cxd5 recaptures and maintains White’s advanced central pawn. Evaluate this new structure instead of assuming the centre has vanished.',
    )),),
    'Challenge White’s d4 pawn with the c-pawn advance ...c5.',
    (('c5',True,'The c-pawn attacks the central base on d4.'),('c6',False,'This does not yet challenge d4.'),('h6',False,'This addresses a kingside square rather than the requested central pawn.')),
    (check('response','Must the owner of a pawn centre always advance when attacked?',('No; compare holding, capturing, and advancing.',True,'Each choice changes lines and squares differently.'),('Yes; retreat is impossible so advance is compulsory.',False,'Pawns can be defended or exchanged; not every attack demands a push.')),
     check('transform','After ...exd5 cxd5, has White necessarily lost the centre?',('No; a different pawn now occupies d5.',True,'The centre has changed shape and must be reassessed.'),('Yes; exchanging the original d-pawn removes all central control.',False,'The c-pawn can take over the same central square.'))),
    ('Avoid treating a legal illustrative opening line as a forced engine recommendation.',),
    ('Challenge the centre’s support.', 'Judge the new position after the captures.'))

PIECES = custom({'g1':'K','f3':'N','c4':'P','f2':'P','g3':'P','g8':'k','e5':'n','d6':'p','g7':'p','h7':'p'})
add('piece-centre', 'A piece centre is control, not just occupation', (224, 229),
    'Pieces can fight over central squares without pawns standing on those squares. Their stability still depends on pawn attacks, support, and the possibility of being driven away.',
    ('Distinguish occupying the centre from controlling it.', 'Use a pawn move to challenge a central piece.'),
    (
        section('Look at attacks, not only occupants', '''A central square can be controlled by a bishop far away, a rook on an open file, or a knight on the next ring of squares. Thus a piece centre may exist even when no pawn occupies d4/d5/e4/e5. The book’s Botvinnik–Lilienthal example is a struggle to increase pressure on central squares and then dislodge the opponent’s pieces. For a beginner, the first step is simpler: count who attacks each important square and whether the piece occupying it can stay there when enemy pawns move.'''),
        section('Pawns decide whether the piece can remain', '''In the original miniature Black’s knight stands centrally on e5, supported by the d6 pawn. White has a knight on f3 and pawns c4/f2/g3. White’s f-pawn can advance two squares to f4, attacking the knight. The black knight’s central location and pawn support do not make it immune to a pawn attack. After a retreat, White may bring the f3 knight to d4. That square is supported by c3 or e3 in other structures, but not here: our lesson is about gaining room and influence, not falsely labeling every central knight permanent.'''),
        section('Calculate the challenge and the reply', '''Before f4, verify that f3 is occupied by White’s own knight. A two-square pawn move from f2 cannot jump over it. White must first move the knight, or choose another pawn challenge. The replay therefore begins Nd4, clearing f3 and bringing the knight to the centre. Black plays ...Kf7 in the example; only then can f4 attack e5. This small obstruction matters more than an appealing strategic idea. It shows why planning and legal calculation belong together: an intended break must have a clear route, and the opponent gets time while you prepare it.'''),
        section('Control can shift without material changing', '''Black retreats the attacked knight to d7 in the sample line. No piece has been won, but the balance of central activity has changed. Black should look for a new supported post or a pawn break against White’s centre, while White must avoid weakening the king by pushing f-pawns thoughtlessly. In full games, piece-centre play often requires several maneuvers and accurate calculation of exchanges. Start with one achievable improvement and one enemy response. If a central piece cannot be maintained, it may still be useful temporarily if it creates a concrete threat before retreating.'''),
    ),
    (example('Original illustration: clear the route before a pawn challenge', PIECES, ('Nd4','Kf7','f4','Nd7'), (
        'White: king g1, knight f3, pawns c4/f2/g3. Black: king g8, knight e5, pawns d6/g7/h7. White’s own knight obstructs f2–f4.',
        'Nd4 centralizes the knight and vacates f3. The planned f-pawn advance is now legally possible.',
        '...Kf7 is a sample reply. Black could choose a different plan, so the following pawn challenge is not forced.',
        'f4 attacks the knight on e5. Its support from d6 does not protect it from being exchanged for a pawn.',
        '...Nd7 retreats to a new square outside the white knight’s attacks. The central balance changes even though material is unchanged.',
    )),),
    'Prepare f2–f4 by moving the obstructing knight from f3 to d4.',
    (('Nd4',True,'This clears f3 for the pawn’s two-square path and moves the knight centrally.'),('Nh4',False,'This also clears f3, but the specified destination is d4.'),('Kh2',False,'This is a legal king move, but it leaves f3 obstructed and does not put the knight on d4.')),
    (check('occupation','Does a central piece automatically have a secure outpost?',('No; check pawn challenges, exchanges, and support.',True,'Location alone does not guarantee stability.'),('Yes; pieces on e5 cannot be chased.',False,'A pawn on f4 can attack a knight on e5.')),
     check('path','Why can White not play f4 in the initial position?',('The knight on f3 blocks the pawn’s path.',True,'A two-square pawn move needs both squares clear.'),('Pawns may never move two squares after move one.',False,'A pawn on its starting square may advance two squares if the path is clear.'))),
    ('A strategic idea must still be legal: pawns cannot jump their own pieces.',),
    ('Count control as well as occupation.', 'Prepare pawn challenges and inspect their cost.'))

VALUE = custom({'g1':'K','e7':'Q','h6':'P','h8':'k','f8':'r','g6':'p','h7':'p'})
add('relative-strength', 'A piece is worth the work it can do', (229, 230),
    'The usual point values are a starting estimate. Mobility, threats, king safety, and defensive duties determine what the pieces can actually achieve in the position in front of you.',
    ('Explain why nominal value and practical strength differ.', 'Recognize the mating support supplied by an advanced pawn.'),
    (
        section('Use points as a starting question', '''A queen usually outweighs a rook, and a rook usually outweighs a minor piece. These estimates help compare ordinary exchanges, but they do not override the board. A rook behind blocked pawns may have no entry file, while a knight on a secure outpost attacks several targets. A bishop can be confined by its own pawn chain. A defender tied to preventing mate cannot necessarily leave its square to win material. Ask what each piece threatens and what task would become impossible if it moved.'''),
        section('A one-point pawn can do a bishop’s job', '''The book points out that an advanced pawn beside the enemy king sometimes supplies the same mating support as a bishop. Our original miniature makes that job visible. White has king g1, queen e7, and pawn h6. Black has king h8, rook f8, and pawns g6/h7. The pawn h6 attacks g7; that single controlled square matters more immediately than its small nominal value. White can put the queen on g7 because the pawn prevents the black king from capturing her. The rook’s greater normal value cannot answer this particular mating pattern.'''),
        section('Verify the mate rather than admire the pattern', '''Before revealing Qg7, name every square available to the black king. The queen will check h8 diagonally and cover g8 and h7. Capturing the queen on g7 is illegal because h6 protects her. The rook cannot capture the checking queen or interpose on the adjacent g7–h8 diagonal. This is therefore actual checkmate, not merely an attractive attack. Check the supporting pawn first: remove h6 in your imagination and the king may capture an otherwise unprotected queen. A small change in the supporting force completely changes the result.'''),
        section('Transfer the idea without copying the sacrifice', '''In a normal game, do not push a pawn to h6 just because this miniature ends in mate. It must survive the journey, and the queen must have a safe route. Conversely, do not exchange a powerful attacking pawn automatically for an ordinary pawn elsewhere. Compare its concrete role with the alternative. Positional strength can also disappear: an outpost may be challenged, a diagonal closed, or a defender exchanged. Recalculate after structural changes. The useful habit is to attach a job to every unit and then evaluate whether the opponent can interfere with that job.'''),
    ),
    (example('Original illustration: h6 makes Qg7 possible', VALUE, ('Qg7#',), (
        'White queen e7 and pawn h6 attack a king on h8; Black also has rook f8 and pawns g6/h7. Pause: which white unit protects g7?',
        'Qg7# works because h6 protects the queen. The queen covers every king escape and the rook cannot interrupt the adjacent diagonal check.',
    )),),
    'Deliver checkmate. The h6 pawn supports one mating route; look for other legal mates too.',
    (('Qg7#',True,'The h6 pawn protects g7; all escapes and defensive captures fail.'),('Qxf8#',True,'The queen captures the rook and covers g8 and h8; Black’s own h7 pawn blocks the remaining escape.'),('Qh4',False,'This does not checkmate the king; the queen has left the mating square.'),('Qe5+',False,'Centralizing the queen does not finish this immediate mating opportunity.')),
    (check('pawn-job','What makes h6 especially strong here?',('It protects the queen’s mating square g7.',True,'Its specific control supplies the attack’s missing support.'),('A pawn on the sixth rank is always worth a queen.',False,'The result depends on exact threats and king escapes.')),
     check('values','When should the usual point count be reconsidered?',('When mobility, threats, or essential defensive tasks alter what pieces can do.',True,'Practical work can differ sharply from average strength.'),('Only after a pawn promotes.',False,'Piece strength fluctuates throughout the game.'))),
    ('A memorable mating pattern is not a reason to ignore the safety of the moves leading to it.',),
    ('Count points, then identify jobs.', 'Validate the king’s escapes and the attacking support.'), objective='checkmate')

BISHOPS = custom({'b1':'K','b2':'B','d3':'B','c3':'P','e4':'P','g8':'k','b6':'n','d6':'p','e5':'p','g7':'p','h7':'p'})
add('bishop-pair', 'Give the bishop pair open diagonals', (230, 231),
    'Two bishops cover both colours and can switch targets quickly. Their advantage depends on useful diagonals and pawn play that prevents the opponent from shutting them out.',
    ('Explain the bishop pair’s complementary coverage.', 'Connect pawn moves with bishop mobility and restriction.'),
    (
        section('Two colours are a resource, not a verdict', '''A single bishop can never attack the other colour of square. With two bishops, an army can work on both colour complexes and transfer pressure across long diagonals. This is especially useful when targets lie on both wings. A knight may need several turns to make the same journey. Yet a bishop blocked by pawns has little immediate influence, and a knight on an unassailable central square may be the best piece on the board. The phrase “bishop-pair advantage” asks you to examine useful lines; it does not award a win automatically.'''),
        section('Open your lines and preserve their future', '''Our original illustration gives White bishops b2/d3, king b1, and pawns c3/e4. Black has king g8, knight b6, and pawns d6/e5/g7/h7. The pawn on c3 obstructs the b2 bishop’s diagonal. Moving c4 removes that immediate obstruction while keeping the e4 pawn protected by the d3 bishop. The new diagonal still meets Black’s e5 pawn, so the move does not magically open the whole board. It improves one line and leaves White to prepare further pawn contact. Notice both the benefit and the remaining limit.'''),
        section('A pair may improve by changing diagonals', '''Pause before the replay and trace b2–c3–d4–e5. After c4 and the sample ...Na4, Bc1 gives the bishop another route along c1–d2–e3–f4–g5–h6. Black’s knight move attacks the bishop on b2, so the retreat also answers a concrete threat. This is an illustrative maneuver rather than a forced win. Bishops sometimes become stronger by retreating to a diagonal with more work. Count the opponent’s threats before opening lines or maneuvering: activity is useful only if the pieces remain safe.'''),
        section('Restrict the defenders before converting', '''In Makarov–Vasiukov, Black’s ...c4 prevents White from closing an important bishop’s line with c3–c4. Later pawn sacrifices keep the defending pieces passive. Rosenthal–Steinitz shows another method: advancing pawns deprives enemy minor pieces of central squares and confines their routes. These methods complement each other. Open diagonals for your bishops, and prevent the enemy from finding stable squares or helpful exchanges. The defender should seek pawn barriers, a supported knight post, or an exchange of one bishop when safe. Before conceding a pawn for activity, calculate whether the resulting pressure survives a sensible defence; the label “two bishops” alone is not compensation.'''),
    ),
    (example('Original illustration: free one diagonal, then change direction', BISHOPS, ('c4','Na4','Bc1'), (
        'White bishops b2/d3 complement each other, but c3 obstructs one diagonal. Black’s knight b6 can attack b2 from a4.',
        'c4 vacates c3 and gives the b2 bishop a view toward e5. Identify Black’s reply before continuing.',
        '...Na4 attacks b2. This sample counterplay reminds White to check the safety of an active piece.',
        'Bc1 escapes the attack and opens a different diagonal toward h6. The bishop has a useful route without any claim of a forced win.',
    )),),
    'Move the c3 pawn to c4, clearing the first obstruction on the b2 bishop’s diagonal.',
    (('c4',True,'The pawn leaves c3 and frees the bishop’s immediate diagonal.'),('Bc1',False,'A useful retreat in the sample line, but it does not make the requested pawn advance.'),('Ka1',False,'Moving the king leaves the c3 obstruction in place.')),
    (check('pair','Why can two bishops outperform one bishop and a knight?',('They cover both colours and may switch targets quickly on open diagonals.',True,'Complementary coverage and mobility are the concrete benefits.'),('They can jump over a locked pawn chain.',False,'Bishops cannot jump; pawn barriers can neutralize their strength.')),
     check('pawn-play','Why might the bishop side prevent an enemy pawn advance?',('The advance could close an important diagonal.',True,'Keeping a line open can matter more than winning a pawn.'),('Every enemy pawn advance is necessarily a mistake.',False,'A well-timed pawn move may secure a knight outpost or limit the bishops.'))),
    ('A bishop retreat may improve its work; forward movement is not the only form of activity.',),
    ('Identify the diagonals each bishop needs.', 'Use pawn play to preserve mobility and restrict enemy routes.'))

CLOSED = custom({'g1':'K','f3':'N','d4':'P','e5':'P','c3':'P','g8':'k','c8':'b','b7':'p','c7':'p','d5':'p','e6':'p','f7':'p'})
add('knights-and-barriers', 'When knights benefit from a closed position', (231, 233),
    'A pawn barrier can deprive bishops of targets while knights jump toward secure squares. Keep the barrier intact when it helps you, and seek the right pawn break when it harms you.',
    ('Relate minor-piece strength to the pawn formation.', 'Explain how opening the position can reverse the comparison.'),
    (
        section('The pawns set the terms of the comparison', '''A knight can jump over a pawn chain, while a bishop must find a clear diagonal around or through it. This makes closed centres attractive to knights, especially when enemy pawns cannot challenge their destinations. The knight still needs time to travel and support when it arrives. A bad bishop may defend essential pawns and later become active after a break. Compare actual squares and routes rather than deciding that all closed positions favour every knight. The important question is whether the barrier will remain long enough for the knight to exploit it.'''),
        section('Build a route to a useful square', '''In our original miniature White has king g1, knight f3, and pawns c3/d4/e5. Black has king g8, bishop c8, and pawns b7/c7/d5/e6/f7. The d4–d5 and e5–e6 contacts lock the centre. White’s knight can travel f3–d2–f1–e3, where the d4 pawn protects it and it attacks d5. Black’s bishop initially has both outgoing diagonals obstructed by its own pawns. It can develop to d7, but the nearby pawn barrier still limits immediate central access. These are positional observations, not a forced result.'''),
        section('A route consumes time and gives replies', '''Pause before Nd2 and count how many white turns the maneuver takes. The replay includes ...Bd7 and ...Kf8 as sample replies while the knight reroutes. Black is not obliged to wait; a prepared ...c5 or another freeing operation could change the structure and make the planned destination less useful. At each stage inspect captures and pawn breaks. The knight does not acquire a permanent outpost merely by reaching e3. Its value depends on the continued protection of d4 and on whether Black can remove the pawn barrier.'''),
        section('Learn the exception without making a new absolute rule', '''Lasker–Chigorin demonstrates two knights overcoming two bishops after pawn advances fixed the position and created strong posts. The book also points out missed chances for the bishop side to open diagonals. The victory therefore illustrates how the pawn formation and inaccuracies changed the comparison, rather than disproving the bishop pair’s usual strengths. When you own bishops, prepare a break before you become completely confined. When you own knights, challenge a freeing break or exchange the piece that supports it. Reassess whenever pawns disappear: a position that favoured a knight five moves ago may now offer a bishop two open wings.'''),
    ),
    (example('Original illustration: a knight travels around a locked centre', CLOSED, ('Nd2','Bd7','Nf1','Kf8','Ne3'), (
        'The central pawn contacts d4/d5 and e5/e6 form a barrier. White’s knight f3 can reach a supported e3; Black’s bishop c8 needs a route out.',
        'Nd2 starts the route. Count the two further knight moves and allow Black a turn after each.',
        '...Bd7 develops the bishop, whose central diagonal still meets e6. This is an illustrative reply.',
        'Nf1 heads for e3. A retreat toward the home rank can form part of a purposeful maneuver.',
        '...Kf8 brings Black’s king inward. A freeing pawn break would need separate calculation.',
        'Ne3 reaches a d4-supported square and attacks d5. The position remains a strategic struggle, not an announced forced win.',
    )),),
    'Begin the shown f3–d2–f1–e3 knight route by playing Nd2.',
    (('Nd2',True,'The knight starts the specified route around the blocked centre.'),('Ng5',False,'This is a different knight move and does not start the demonstrated route.'),('Kh2',False,'The king move does not improve the knight as requested.')),
    (check('barrier','What makes the barrier useful to the knight side?',('It limits bishop lines while the knight can jump toward supported squares.',True,'The formation affects each piece differently.'),('It allows knights to move twice each turn.',False,'A knight route still consumes turns and allows enemy counterplay.')),
     check('change','What must be reassessed after a central pawn exchange?',('New diagonals, knight posts, and the strength of the remaining minor pieces.',True,'Opening the board may reverse the earlier comparison.'),('Only the number of remaining pawns.',False,'The lines opened can matter more than a material count.'))),
    ('Do not ignore a freeing pawn break while carrying out a long knight maneuver.',),
    ('Match the piece to the pawn formation.', 'Keep checking whether the barrier can change.'))

EVALUATE = custom({'g1':'K','d1':'Q','f1':'R','f2':'P','h2':'P','g8':'k','g5':'q','e8':'r'})
add('evaluate-position', 'Turn an evaluation into a playable plan', (233, 233),
    'Assess material, activity, the centre, king safety, weaknesses, and threats together. An evaluation should tell you what needs attention and suggest candidates you can calculate.',
    ('Use a repeatable assessment without ignoring immediate checks.', 'Convert a verbal advantage into a concrete next action.'),
    (
        section('Begin with the facts and the immediate danger', '''An evaluation is a reasoned judgment about what the position offers each side. Count material first, including the pawns, then notice whose turn it is and whether either king is in check. A checklist is helpful, but it must not delay answering an immediate threat. In our original miniature White has king g1, queen d1, rook f1, and pawns f2/h2. Black has king g8, queen g5, and rook e8. White is two pawns ahead, but Black’s queen checks along the open g-file. White cannot spend this turn collecting another advantage.'''),
        section('Compare the quality of the armies', '''Count developed pieces, then ask where they can actually work. A rook on an open file has different possibilities from a rook behind its own pawns. Check the centre and the routes between wings. Examine both kings’ shelters and the squares an enemy attacker could enter. Finally name targets: isolated pawns, abandoned squares, exposed pieces, and defenders doing too many jobs. Distinguish a temporary inconvenience from a lasting weakness. An undeveloped knight can improve in one move; a missing pawn defender cannot simply return to its old square.'''),
        section('Choose candidates that fit the urgent need', '''Before revealing Kh1, list legal ways to escape the g-file check. The exercise asks specifically for a king move to h1; it does not claim this is the uniquely best move in the whole position. Black’s sample ...Qd5+ then changes the checking line to d5–e4–f3–g2–h1. White answers f3, blocking that diagonal. Notice how the evaluation changes after each reply: being materially ahead does not make checks disappear, and a defensive pawn advance can be necessary even though it alters the shelter. Calculate the opponent’s most forcing replies before trusting any attractive plan.'''),
        section('Make the assessment produce a decision', '''After safety is restored, ask what useful improvement can be achieved next. A lead in development suggests timely activity; a secure extra pawn may suggest exchanging attackers; a weak enemy pawn may suggest a blockade and a second target. None of these plans is automatic. Write the idea in concrete terms: improve this knight, challenge that pawn, defend this entry square. Compare two or three candidates and test checks, captures, and threats after each. Strong players form assessments quickly through experience, but the beginner’s careful inventory builds the same habit. Revise the plan when the position’s important facts change.'''),
    ),
    (example('Original illustration: material cannot postpone answering check', EVALUATE, ('Kh1','Qd5+','f3'), (
        'White is two pawns ahead but in check from queen g5 along the open g-file. Black also has rook e8; inspect king safety before planning a material conversion.',
        'Kh1 leaves the checking file. This is a legal response selected for the exercise, not a claim of unique best play.',
        '...Qd5+ is a sample forcing reply. Trace d5–e4–f3–g2–h1 and find an interposition.',
        'f3 blocks the diagonal and answers the check. White must now reassess activity and weaknesses before resuming a longer plan.',
    )),),
    'Answer the g-file check by moving the king to h1.',
    (('Kh1',True,'The king leaves the g-file and answers the current check.'),('Qg4',False,'This can interpose but is not the requested king move to h1. Compare its tactical consequences separately.')),
    (check('priority','Which factor takes priority when your king is in check?',('Find a legal answer to the check before pursuing a slower plan.',True,'A favourable material count does not remove the immediate obligation.'),('Count space and ignore the checking piece until later.',False,'Every move must leave your king out of check.')),
     check('plan','What makes an evaluation useful?',('It identifies concrete needs and candidates that survive calculation.',True,'The assessment guides action and is revised after replies.'),('It assigns a label without suggesting any next move.',False,'A verbal advantage must be connected to a playable plan.'))),
    ('A checklist supports thought; it does not replace calculating the opponent’s forcing replies.',),
    ('Inventory material and activity.', 'Check kings, centre, weaknesses, and threats; then select and calculate a plan.'))

STOLTZ = after(('e4','c5','Nf3','Nc6','c3','e6','d4','d5','e5','Qb6','dxc5'))
AVERBAKH = after(('c4','f5','g3','Nf6','Bg2','e6','Nf3','Be7','O-O','O-O','d4','d6','Nc3','Qe8','Re1','Ne4','Qc2','Qg6','Be3','Nxc3','Qxc3','Nd7','c5','Nf6','cxd6','cxd6','Qb3','Nd5','Bd2','b6'))
NIEMELA = after(('d4','Nf6','c4','g6','Nc3','Bg7','e4','O-O','Nf3','d6','Be2','Nbd7','O-O','e5','Be3','c6','dxe5','dxe5','Ne1','Qe7','Nd3','Rd8','Qc2','Nf8','b4','N6d7','c5','Ne6','Rad1'))
add('games-centre-decisions', 'Three games: make the centre explain the tactics', (234, 236),
    'Study short turning points from the chapter’s three entertainment games. A premature exchange, an opened diagonal, and a slow knight route each change which concrete moves become possible.',
    ('Connect a central decision with later piece activity.', 'Compare plans using the opponent’s time and counterplay.'),
    (
        section('Stoltz–Bronstein: a central exchange has a cost', '''White’s d4/e5 pawns initially restrict Black. The unnecessary dxc5 gives up the d4 pawn’s central job, and Black recaptures with a bishop rather than losing time. White then spends queen moves protecting e5. In the replay Black exchanges a bishop and places a knight on f5 with an attack on the queen. The lesson is not that exchanging central pawns is always wrong. Ask whether the exchange gives the opponent a useful developing move, leaves a pawn needing repeated defence, or deprives your pieces of space. White’s later isolated d4 pawn becomes another responsibility in the full game.'''),
        section('Averbakh–Ragozin: exploit the line before it closes', '''Both sides are castled. Black’s pawns d6/e6 and knight d5 form the central group, while White’s g2 bishop looks toward a8. The move ...b6 opens the far end of that diagonal and creates a tactical opportunity. White exchanges on g5, then plays e4 to undermine the central knight. After ...fxe4 Nxe4, notice that White’s knight reaches the centre and the bishop’s diagonal becomes relevant. This fragment shows the mechanism; the later game includes an intermediate queen check on e6 before White recaptures a bishop. Always check such forcing moves before assuming an exchange sequence is automatic.'''),
        section('Niemela–Geller: compare the speed of the plans', '''White has exchanged the central tension, moved a knight from f3 toward d3, and advanced queenside pawns. Black is ready to occupy d4 immediately. White’s intended Nb2–c4–d6 route takes several turns; Black does not wait for it. After ...Nd4 and Qc1, ...a5 opens a second front against the advanced b4 pawn. In the sample continuation Black’s rook reaches a3 and threatens the knight on c3. The full game converts this activity with an exchange sacrifice. The strategic error is losing touch with the centre while spending time on a slower operation.'''),
        section('Use the turning point as a calculation exercise', '''For each starting board, name the central pawns, the threatened pieces, and the side with a plan that acts soonest. Pause before the critical move and predict one reply. These are source game fragments with newly written explanations, not the complete scores and not a claim that every illustrated reply is forced. In your games, look for the same triggers: a central defender moving, a diagonal becoming open, or an enemy route requiring several quiet turns. Positional evaluation tells you where to investigate; calculation tells you whether the intended move actually works.'''),
    ),
    (example('Stoltz–Bronstein: activity gained from White’s central exchange', STOLTZ, ('Bxc5','Qc2','Qc7','Qe2','Nge7','Be3','Bxe3','Qxe3','Nf5','Qe2'), (
        'After 6.dxc5, White’s d-pawn stands on c5 and e5 needs defence. Black to move can recapture while developing the f8 bishop.',
        '...Bxc5 develops with a capture and removes White’s former central pawn.',
        'Qc2 starts a queen maneuver; the e5 pawn is still defended by the knight f3. White will soon move the queen again to help defend it.',
        '...Qc7 attacks e5 along c7–d6–e5, increasing the pressure on White’s advanced central pawn.',
        'Qe2 places the queen directly behind e5 on the e-file, taking on a defensive job.',
        '...Nge7 develops the g8 knight without blocking the c5 bishop. Pause and compare each army’s remaining development.',
        'Be3 develops and offers a bishop exchange on e3.',
        '...Bxe3 removes the newly developed bishop and changes White’s defensive arrangement.',
        'Qxe3 recaptures, but the queen now sits on a square reachable by a knight attack.',
        '...Nf5 attacks the queen e3 and develops the knight actively.',
        'Qe2 retreats. White’s queen has spent more turns while Black’s pieces have gained useful positions.',
    )),
     example('Averbakh–Ragozin: an exchange prepares a central break', AVERBAKH, ('Bg5','Bxg5','Nxg5','Bb7','e4','fxe4','Nxe4'), (
        'White has queen b3, bishops d2/g2, knight f3, rooks a1/e1, and pawn d4. Black’s ...b6 has opened the g2–a8 diagonal; pause before choosing the central operation.',
        'Bg5 offers to exchange Black’s e7 bishop and makes room for a knight to reach g5.',
        '...Bxg5 accepts the exchange. This is the game’s reply, not an assumption that all exchanges are compulsory.',
        'Nxg5 brings the knight to an active square while preserving the central pawn break.',
        '...Bb7 develops the bishop onto the now open long diagonal.',
        'e4 attacks the d5 knight and challenges Black’s centre. The temporary knight position on g5 supports the operation.',
        '...fxe4 captures the advancing pawn and vacates f5.',
        'Nxe4 recaptures centrally. White has transformed the pawn contact into piece activity and targets on d6/e6.',
    )),
     example('Niemela–Geller: a quick central post and an opened wing', NIEMELA, ('Nd4','Qc1','a5','a3','axb4','axb4','Nf8','Nb2','Ra3'), (
        'Black to move: White’s knights c3/d3 are slow to reach the planned queenside posts. Black’s knight e6 can occupy d4 immediately.',
        '...Nd4 occupies the central hole and attacks White’s queen c2. The queen must attend to the attack.',
        'Qc1 retreats. The knight on d4 remains a strong practical presence.',
        '...a5 attacks White’s advanced b4 pawn and prepares to open the a-file.',
        'a3 supports b4 rather than undoing the earlier advance.',
        '...axb4 makes pawn contact and removes Black’s a-pawn from the file.',
        'axb4 recaptures, leaving the a-file open for Black’s rook.',
        '...Nf8 reroutes the other knight while maintaining the central post.',
        'Nb2 begins White’s slower knight plan. Black already has concrete play on the open file.',
        '...Ra3 invades and attacks the c3 knight along the third rank. The central and queenside plans now reinforce each other.',
    ))),
    'After White’s dxc5, recapture on c5 with the f8 bishop and develop it.',
    (('Bxc5',True,'This develops the bishop while recovering the pawn on c5.'),('Qxc5',False,'The queen can capture, but the task asks to develop the f8 bishop.'),('Nge7',False,'A developing move, but it leaves the specified c5 recapture unfinished.')),
    (check('exchange','What should you examine before exchanging a central pawn?',('Which lines open and whether the opponent gains activity or targets.',True,'An exchange changes both space and development.'),('Only whether the capture is legal.',False,'A legal capture can surrender a useful central formation.')),
     check('time','Why can a good knight destination still lead to a bad plan?',('The route may take too long while the opponent creates immediate threats.',True,'Compare the speed of both plans and calculate intervening replies.'),('A knight should never move more than once.',False,'Purposeful rerouting is useful when time and safety permit.'))),
    ('An exchange sequence can contain intermediate checks; calculate them before automatic recaptures.',),
    ('Explain the central change before memorizing the moves.', 'Compare lines, targets, and the time needed by both plans.'))

PERPETUAL = custom({'h7':'K','a6':'N','b6':'R','a8':'k','a2':'p','g3':'p','h4':'p'})
add('perpetual', 'Save the game with a repeatable checking mechanism', (237, 240),
    'A rook and knight can draw against a new queen when their cooperation keeps the king under check. Build the mechanism before grabbing the pawn that is about to promote.',
    ('Recognize coordination as compensation for a material deficit.', 'Distinguish perpetual checking from one isolated check.'),
    (
        section('Read the danger before counting your pieces', '''The first entertainment study gives White king h7, rook b6, and knight a6. Black has king a8 and pawns a2/g3/h4. The a-pawn is one step from promotion, while the kingside pawns are also dangerous. Simply capturing a2 after a few checks lets the other pawns advance, and the rook cannot easily stop them both. White needs a drawing resource that works while Black gains a queen. This is an extreme illustration of the chapter’s central theme: pieces matter through the jobs they can perform together.'''),
        section('Prepare the mechanism before the emergency', '''White begins Nb8, and after ...Ka7 plays the surprising Rb4. The rook and knight establish control over the b-file and checking squares near the black king. Black then promotes a1=Q. Pause here: forget the queen’s nine-point reputation and identify a knight check. Nc6+ attacks a7; after ...Ka6, Nb8+ attacks a6. The knight can alternate its two squares while the rook restricts the king. A check is useful because Black must answer it before beginning a queen attack of its own.'''),
        section('Repeat the position, not merely the notation', '''The replay extends the book’s checking pattern until the same position really occurs three times with the same side to move. This gives a concrete repetition claim in the displayed line. It does not mean that playing the same move three times automatically draws: the whole position, side to move, and legal possibilities must agree. Nor does every sequence of checks last forever. Before relying on perpetual check, inspect captures of the checking piece, interpositions, and new king escapes. The rook’s restriction and knight’s jump pattern are both essential to this study’s mechanism.'''),
        section('Recognize the practical signal in your own games', '''When defending a worse position, look for a confined king and forcing checks before resigning or accepting a bad material exchange. A queen cannot use her full strength if every turn must answer a check. For the stronger side, avoiding the checking net may matter more than promoting at once or taking extra material. The composed line is deliberately concentrated; practical positions usually have extra defenders and escape squares. Use the pattern as a search cue, then verify the exact board. Draws can come from active threats and coordination, not only from exchanging down to bare kings.'''),
    ),
    (example('Source study 1: a rook supports perpetual knight checks', PERPETUAL,
             ('Nb8','Ka7','Rb4','a1=Q','Nc6+','Ka6','Nb8+','Ka7','Nc6+','Ka6','Nb8+','Ka7','Nc6+','Ka6','Nb8+'), (
        'White faces promotion on a1 and two additional passed pawns. Identify rook b6, knight a6, and the confined king a8 before calculating.',
        'Nb8 prepares the knight’s checking route and vacates a6.',
        '...Ka7 approaches the checking area. This is the book’s main defensive continuation.',
        'Rb4 sets up the rook’s restriction along the b-file. Pause and find a knight check after promotion.',
        '...a1=Q creates a queen, but does not remove White’s checking mechanism.',
        'Nc6+ attacks the king on a7; the rook helps restrict escapes on the b-file.',
        '...Ka6 answers the check by moving onto the knight’s other checking target.',
        'Nb8+ checks a6 and returns the knight to its previous post.',
        '...Ka7 returns to the other checking square.',
        'Nc6+ repeats the attack on a7. Notice the unchanged rook and queen positions.',
        '...Ka6 returns to the same king square as before.',
        'Nb8+ recreates the checking position with Black to move.',
        '...Ka7 continues the same defensive cycle.',
        'Nc6+ gives the same check again; no pawn has moved to alter the position.',
        '...Ka6 returns for another cycle.',
        'Nb8+ completes a real threefold repetition in this replay. White can claim the draw.',
    )),),
    'Begin the study’s drawing mechanism by moving the knight from a6 to b8.',
    (('Nb8',True,'The knight heads for the checking cycle coordinated with Rb4.'),('Nc7+',False,'This starts the tempting pawn-capturing line rather than the specified mechanism.'),('Rb5',False,'This does not establish the demonstrated knight route and rook restriction.')),
    (check('repeat','What must repeat for a threefold-repetition claim?',('The position with the same side to move and the same legal possibilities.',True,'Repeated notation alone is insufficient.'),('Any checking move, three times anywhere.',False,'Different king positions or changed pawns can make each position distinct.')),
     check('queen','Why does promotion not end the study immediately?',('White retains forcing checks supported by the rook’s restriction.',True,'Black must answer the checks before exploiting the queen.'),('A promoted queen cannot move for three turns.',False,'A promoted queen has normal powers as soon as it appears.'))),
    ('One good check is not proof of perpetual check; inspect how the next check remains available.',),
    ('Look for active drawing threats.', 'Verify the repeated board and the stability of the mechanism.'))

ROUTE = custom({'d7':'K','c7':'P','f3':'k','h7':'b','b7':'p'})
add('king-detour', 'An extraordinary king route serves two goals', (237, 240),
    'Sometimes the fastest useful route begins with a move away from the target. Preserve a promotion threat long enough to bring the king toward the enemy pawn.',
    ('Compare direct and indirect king routes.', 'Use a promotion threat to gain time for defence.'),
    (
        section('Inventory two races rather than one', '''The Sarychev brothers’ study has White king d7 and pawn c7 against Black king f3, bishop h7, and pawn b7. White would like to promote, but the bishop can take control of the promotion square with tempo. Black also threatens to advance the b-pawn, supported by bishop and king activity. White’s goal is a draw. You must consider both sides’ pawns, not simply measure how close c7 is to becoming a queen. The point of the study is to remove Black’s winning pawn while maintaining enough threats to make the king’s journey possible.'''),
        section('Why the obvious promotion fails', '''Before queening, calculate ...Bf5+. A queen on c8 looks powerful, but the bishop check drives the white king away from the promotion square and allows ...Bxc8. White loses the new queen and remains facing Black’s pawn. That is why the pawn’s apparent readiness is misleading. A direct king move toward the opposing pawn can also be too slow against the black king’s approach. Instead Kc8 temporarily occupies the promotion square itself. After ...b5, Kd7 clears c8 again while Black’s pawn has advanced. The pawn remains a future threat that can buy time for the king’s approach; it cannot promote while its own king is on c8.'''),
        section('Follow the detour one turn at a time', '''The main line continues ...b5, Kd7, ...b4, Kd6. Pause after each pawn advance and mark the king’s intended approach toward c5/c4 and b4. Black plays ...Bf5 to control c8, after which Ke5 brings the king another step toward the enemy pawn. The bishop then makes a waiting move, represented by ...Bg4, and Kd4 completes the demonstrated route. The book gives the bishop’s waiting move generically; Bg4 is one legal realization. The line teaches how the persistent c-pawn threat gives the king time to approach Black’s only pawn.'''),
        section('Calculate the counter-threat that buys each tempo', '''The final king on d4 is heading toward the b4 pawn, while Black’s bishop must continue paying attention to promotion. Do not describe a king maneuver as a race won purely by distance: the opponent’s duties determine which tempos are available. In a practical game, first identify the enemy’s winning resource, then ask whether a threat can make defence possible. This study is a composed drawing mechanism, not a rule that every king should move backward before advancing. Its transferable lesson is to compare combined goals. A move that preserves a threat and improves the king’s route can be stronger than a move that pursues only one goal directly.'''),
    ),
    (example('Source study 2: Kc8–d7–d6–e5–d4', ROUTE, ('Kc8','b5','Kd7','b4','Kd6','Bf5','Ke5','Bg4','Kd4'), (
        'White king d7 and pawn c7 face bishop h7, king f3, and pawn b7. White seeks a draw by eventually neutralizing Black’s pawn.',
        'Kc8 temporarily blocks c8 with White’s own king; Kd7 will clear the square again after Black advances.',
        '...b5 starts Black’s passed-pawn advance.',
        'Kd7 returns, now with Black’s pawn one square farther from its starting square.',
        '...b4 continues the advance; calculate White’s route toward it.',
        'Kd6 approaches the centre while maintaining the c-pawn resource.',
        '...Bf5 controls c8 and prevents immediate promotion.',
        'Ke5 continues the indirect route toward d4 and c4.',
        '...Bg4 is a legal representative of the bishop waiting move indicated by the source.',
        'Kd4 completes the source route. White’s king is approaching the b4 pawn while the bishop remains responsible for c8.',
    )),),
    'Start the source study’s drawing route by moving the king from d7 to c8.',
    (('Kc8',True,'The king temporarily occupies c8, then returns to d7 to renew the pawn’s promotion threat with the move order changed.'),('c8=Q',False,'Immediate promotion permits ...Bf5+ followed by ...Bxc8.'),('Ke6',False,'This is the direct route rejected by the study; Black’s king approaches with ...Ke4.')),
    (check('threat','Why can keeping a pawn unpromoted be useful?',('Its continuing threat can tie the enemy bishop to stopping promotion.',True,'The threat may buy time for another task.'),('An unpromoted pawn moves faster than a queen.',False,'Its value here comes from the opponent’s defensive obligation.')),
     check('detour','What should be compared when a king takes an indirect route?',('Both races and the forcing threats that gain or lose time.',True,'Distance alone ignores checks and defensive duties.'),('Only the number of squares between the kings.',False,'Pawn promotion and bishop checks determine the timing.'))),
    ('Calculate checks after promotion before assuming that the new queen is safe.',),
    ('Keep useful threats alive.', 'Judge a route by the tasks and tempos it coordinates.'))

FORTRESS = custom({'a3':'K','c8':'N','g5':'P','g8':'k','g7':'p','e3':'p'})
add('fortress', 'A queen cannot break every fortress alone', (237, 240),
    'A protected knight and active king can form a defensive shelter when the enemy king is permanently confined. Learn why a large material advantage may have no winning entry.',
    ('Identify the pieces and squares that make a fortress hold.', 'Distinguish a stable defensive arrangement from merely hoping for a draw.'),
    (
        section('Find the resource before the pawn queens', '''Ilyin’s study gives White king a3, knight c8, and pawn g5. Black has king g8 and pawns e3/g7. The e-pawn is heading for promotion and White’s king seems far away. White first uses checks to change Black’s king position: Ne7+ brings the king to h7 in the main line, then g6+ drives it to h8. The white pawn g6 and black pawn g7 now confine the king. It is vital to arrange that confinement before allowing promotion; otherwise the queen and king could cooperate against the knight.'''),
        section('Understand the locked king precisely', '''After ...Kh8, Black cannot step to g8 because the knight on e7 attacks g8. The king cannot step to h7 because White’s g6 pawn attacks h7, and g7 contains Black’s own pawn. The g7 pawn cannot advance because g6 is occupied. These are concrete restrictions, not a vague claim that the king “looks trapped.” White must keep the knight’s useful control while bringing its king across the board. This is why the exact pawn arrangement matters: remove one obstacle or change the knight’s square and the result may be completely different.'''),
        section('Allow promotion while joining the defenders', '''Pause before Kb4 and count the king’s route: a3–b4–c5–d6. Black uses the available turns to advance e3–e2–e1=Q. White arrives on d6, next to the knight e7, so the knight is protected. The resulting fortress consists of a king defending its knight, the knight controlling the trapped king’s escape, and the fixed kingside pawns maintaining the enclosure. The source shows that the queen alone cannot drive the white king away permanently from its knight. The replay ends at the arrangement; it does not pretend that a few arbitrary queen moves prove every defensive variation.'''),
        section('Test every part of a proposed fortress', '''A real fortress claim needs more than material counting. Can the stronger side bring the king in? Is there a pawn break? Can the queen win the supporting pawn with check, create zugzwang, or fork the king and knight? Here the black king’s permanent exclusion is the decisive restriction, the knight also protects the essential pawn g6, and the white king can keep supporting the knight against queen checks. In ordinary games, one extra pawn or an accessible king route may destroy a superficially similar shelter. For the defender, search for stable duties that can be maintained; for the attacker, seek a structural change rather than repeating threats that never alter the defensive arrangement.'''),
    ),
    (example('Source study 3: imprison the king, then defend the knight', FORTRESS, ('Ne7+','Kh7','g6+','Kh8','Kb4','e2','Kc5','e1=Q','Kd6'), (
        'White king a3 and knight c8 face promotion from e3. White’s g5 pawn can help confine Black’s king g8 beside its own g7 pawn.',
        'Ne7+ begins with a forcing check and places the knight where it controls g8.',
        '...Kh7 follows the study’s main defensive line.',
        'g6+ attacks h7 and fixes the g7 pawn in front of the white pawn.',
        '...Kh8 leaves Black’s king enclosed. Pause: list why g8, g7, and h7 are unavailable.',
        'Kb4 starts the king’s route toward its knight rather than chasing the e-pawn.',
        '...e2 brings Black’s pawn one step from queening.',
        'Kc5 continues toward d6, from which the king can protect e7.',
        '...e1=Q promotes, but Black’s king still cannot join the queen.',
        'Kd6 protects the knight e7 and completes the source fortress. Material alone does not provide Black a winning king entry.',
    )),),
    'Begin the source drawing sequence with the knight check from c8 to e7.',
    (('Ne7+',True,'The check puts the knight on e7 and prepares the confinement of Black’s king.'),('Nb6',False,'This does not give the check or establish the key control of g8.'),('Kb4',False,'The king route is needed later, after the forcing kingside arrangement is secured.')),
    (check('king','Why is Black’s extra queen unable to use king support here?',('The pawn enclosure and knight control keep the black king imprisoned.',True,'The queen has to work without the king’s assistance.'),('A queen and king cannot attack together after promotion.',False,'They normally cooperate very effectively when the king has an entry route.')),
     check('shelter','What must be checked before calling a position a fortress?',('King entries, pawn breaks, tactical forks, and the stability of defensive duties.',True,'A fortress is a concrete arrangement that resists improvement.'),('Only whether the defender is behind in points.',False,'Most material deficits do not create any fortress.'))),
    ('Do not infer a fortress from a single passive-looking position; identify why progress is unavailable.',),
    ('Trap the enemy king before allowing the queen.', 'Support the knight and preserve every essential restriction.'))

DUAL = custom({'c2':'K','e1':'B','b2':'P','b3':'P','f2':'P','h3':'P','a2':'k','b4':'r','h4':'r'})
add('maintain-threat', 'Keep two threats instead of cashing in one', (237, 240),
    'Winning the exchange can lose the game if it releases the opponent’s other rook. Rossolimo’s study teaches how a continuing threat can restrain two stronger pieces.',
    ('Compare a capture with maintaining simultaneous threats.', 'Recognize that restriction can be a defensive resource.'),
    (
        section('Count the opponent’s activity after your capture', '''White has king c2, bishop e1, and pawns b2/b3/f2/h3. Black has king a2 and rooks b4/h4. The bishop already attacks b4 along e1–d2–c3–b4. Capturing that rook would win material relative to a bishop, but it would release the other rook from the coordinated restraint that White needs. The correct goal is to draw, not to improve a point total for one move. Before any tempting capture, ask what the remaining enemy pieces can do after your attacking piece leaves its current network.'''),
        section('A small pawn move creates the second obligation', '''The key is f3. This opens e1–f2–g3–h4, so the bishop now attacks both rooks on opposite diagonals. Pause and trace both lines before advancing. The bishop is not a queen and does not move in two directions at once, but Black must choose how to respond while White retains the option to change target. Taking one rook immediately would remove the double threat. Keeping the bishop centralized gives Black’s stronger pieces much less freedom than the raw material balance suggests.'''),
        section('Follow the threat when the rook shifts', '''The main replay shows ...Rhd4 and Bc3. The bishop on c3 attacks both b4 and d4, preserving the two-rook pressure after the first rook moves. Other source branches illustrate the same geometry: after ...Rhf4, Bd2 attacks b4 and f4; after ...Rbd4, Bf2 attacks d4 and h4; after ...Rbf4, Bg3 attacks f4 and h4. These are distinct lines, not moves to combine into one imaginary variation. The defender keeps finding a square where one bishop bears on both rooks. The black king is also constrained by White’s king and b-pawns.'''),
        section('Preserve the resource while the position changes', '''The lesson’s title does not mean that threats are always stronger than captures. A free rook is usually worth taking. Here the capture abandons the special arrangement that stops a much stronger army from coordinating. In your games, compare the immediate gain with the defenders or restrictions you give up. For the stronger side, seek a way to change the geometry so the bishop cannot keep both rooks under pressure. For the defender, recalculate each shift instead of repeating the same bishop move automatically. The study teaches an active form of defence: create obligations that the opponent must answer, rather than merely waiting to be attacked.'''),
    ),
    (example('Source study 4: one bishop keeps both rooks under attack', DUAL, ('f3','Rhd4','Bc3'), (
        'White’s bishop e1 already attacks rook b4. White seeks a draw against two rooks and must avoid releasing their activity by an immediate capture.',
        'f3 clears f2, opening the bishop’s second diagonal to rook h4. Pause and trace both simultaneous attacks.',
        '...Rhd4 moves the h-rook to d4; the other rook remains b4.',
        'Bc3 attacks both b4 and d4. White preserves the two threats instead of taking one rook and releasing the other.',
    )),
     example('Source alternative: a different rook move requires a different diagonal', DUAL, ('f3','Rhf4','Bd2'), (
        'Reset the same position. This branch explores a different attempt to relocate the h4 rook.',
        'f3 again clears the diagonal e1–f2–g3–h4.',
        '...Rhf4 places one rook on f4 while the other remains on b4.',
        'Bd2 attacks b4 via c3 and f4 via e3, preserving the simultaneous pressure.',
    ))),
    'Open the bishop’s second attacking diagonal by advancing the f2 pawn to f3.',
    (('f3',True,'Vacating f2 lets the bishop attack h4 as well as b4.'),('Bxb4',False,'This wins one rook but gives up the continuing double threat needed in the study.'),('Bd2',False,'This does not yet open the blocked e1–h4 diagonal; f3 is the preparatory move.')),
    (check('capture','Why should White hesitate before Bxb4?',('It releases the special restraint on Black’s other rook.',True,'The resulting activity matters more than the immediate point gain.'),('Bishops are forbidden to capture rooks.',False,'The capture is legal; its consequences are the problem.')),
     check('geometry','What should White seek after one rook relocates?',('A bishop square that again attacks both rooks.',True,'The exact diagonal changes with their new squares.'),('The same bishop move regardless of the rook squares.',False,'Preserving a threat requires recalculation of the new geometry.'))),
    ('Compare the whole position after a capture, including the enemy piece that remains active.',),
    ('Keep both threats when their restraint is your defence.', 'Recalculate the diagonal after each rook move.'))

CORNERS = custom({'b6':'K','a1':'Q','d7':'B','d5':'N','f2':'N','e5':'k','d6':'p','c5':'p','d3':'p','c4':'b','f4':'b','d4':'n'})
TRIANGLE = custom({'f1':'K','g1':'Q','f6':'N','f3':'k','d3':'n','f4':'p'})
add('queen-geometry', 'Queen geometry: corners and a triangle', (238, 240),
    'A long queen route can change the direction of a mating threat without changing the target king. Follow two source problems by tracking checks, interpositions, and the final line.',
    ('Explain why a queen changes lines before returning home.', 'Distinguish a quiet mating threat from a check.'),
    (
        section('Long movement can be a precise maneuver', '''The queen can cross a board in one move, but choosing the useful line still requires calculation. In the first problem White has king b6, queen a1, bishop d7, and knights d5/f2. Black’s king e5 is surrounded by its own pawns, bishops, and knight d4. White’s smaller pieces cover exits while the queen chooses the line that cannot be permanently blocked. In the second problem White has king f1, queen g1, and knight f6 against king f3, knight d3, and pawn f4. Identify these supporting units before following the queen’s attractive geometry.'''),
        section('Four corners: make the blocker move', '''In the first line Qa8 threatens the checking invasion Qe8+. The knight d4 interposes with ...Ne6, after which Qh8+ checks along the long diagonal h8–g7–f6–e5. Black answers ...Ng7, blocking that diagonal. White then plays the quiet Qh1, changing the future checking direction. After ...Bxd5, Qa1 is mate along the now clear a1–b2–c3–d4–e5 diagonal. Pause before the last move and compare d4 with the initial diagram: Black’s knight has left it. The queen’s return is powerful because the intervening defensive moves changed the line.'''),
        section('Triangle: a threat can set the final geometry', '''In the second line Qa7, ...Kg3, Qg7+, ...Kf3, Qg1 restores the exact starting arrangement with Black now to move. This is a tempo maneuver: Black must move the knight from d3 because the king and pawn have no legal moves. The knight thereby loses its ability to capture on f2. After any knight move the queen mates on f2, capturing if necessary. The displayed ...Nb4 permits Qf2#. The finish is f2, not f1, which White’s king occupies. The changed side to move, rather than a changed piece arrangement, makes the return effective.'''),
        section('Study the mechanism before memorizing the shape', '''These replays show source main lines through mate; they do not prove every alternative loses in the advertised move count. They are composed problems, not instructions to send a queen around the edge in an ordinary opening. Their practical value lies in changing the line of attack, provoking an interposition, and returning once a blocker has moved. Before each move, name the threat and one defensive reply. At the end, verify every king escape, capture, and interposition. A route that resembles a rectangle or triangle is only a mnemonic; the controlled squares make it work. In normal games, a shorter route or an immediate capture may be better, and the opponent may have additional defenders absent from the composition.'''),
    ),
    (example('Source problem 5: a1–a8–h8–h1–a1', CORNERS, ('Qa8','Ne6','Qh8+','Ng7','Qh1','Bxd5','Qa1#'), (
        'White queen a1 works with bishop d7 and knights d5/f2 around king e5. Black’s knight d4 currently blocks the a1–e5 diagonal. Pause and trace Qe8 after Qa8.',
        'Qa8 prepares Qe8+, a checking invasion along the eighth rank and e-file.',
        '...Ne6 interposes on the e-file and removes the knight from d4.',
        'Qh8+ switches to the diagonal h8–g7–f6–e5 and checks the king.',
        '...Ng7 blocks that diagonal, bringing the same knight farther from d4.',
        'Qh1 quietly prepares a change of attacking diagonal. Identify the now vacant d4 square before continuing.',
        '...Bxd5 captures White’s central knight in the source line, but does not restore the d4 blockade.',
        'Qa1# returns to the starting square with the a1–e5 diagonal now clear. The supporting pieces cover the remaining escapes.',
    )),
     example('Source problem 7: a queen’s triangle prepares Qf2', TRIANGLE, ('Qa7','Kg3','Qg7+','Kf3','Qg1','Nb4','Qf2#'), (
        'White king f1, queen g1, and knight f6 face king f3, knight d3, and pawn f4. The knight’s control helps confine the black king.',
        'Qa7 begins a tempo maneuver: the queen will return to g1 with Black obliged to move.',
        '...Kg3 moves the king toward the kingside in the source main line.',
        'Qg7+ checks down the g-file and changes the queen’s attacking direction.',
        '...Kf3 returns the king to f3.',
        'Qg1 restores the starting piece arrangement with Black to move. Only the knight can move; after it leaves d3, the queen can mate on f2.',
        '...Nb4 is one of the compulsory knight moves. It abandons the knight’s d3 control of f2.',
        'Qf2# checks the king at close range; White’s king protects the queen and the knight helps cover escapes.',
    ))),
    'Start the four-corners problem by moving the queen from a1 to a8.',
    (('Qa8',True,'This begins the source route and prepares the checking invasion Qe8+.'),('Qa2',False,'This does not begin the specified corner route or place the queen on the eighth rank.'),('Qb1',False,'This changes file without starting the a8–h8 maneuver.')),
    (check('return','Why is returning to a1 different from staying on a1?',('Black’s knight has left d4, opening a previously blocked diagonal.',True,'Intervening defensive moves change the queen’s line.'),('A queen gains extra powers after visiting four corners.',False,'Only the ordinary rules and changed arrangement matter.')),
     check('quiet','What must you identify after a quiet queen move?',('Its threat and the opponent’s ways to stop it.',True,'A quiet move can be forcing through a mating threat.'),('A check symbol, because every queen move must check.',False,'Qa8, Qh1, and Qg1 illustrate threats without immediate check.'))),
    ('Verify the board when notation is unclear; a queen cannot finish on its own king’s square.',),
    ('Change the attack line to displace a blocker.', 'Explain the new geometry after every defensive move.'))

RECTANGLE = custom({'c6':'K','h7':'R','f5':'R','b2':'P','a6':'k','a5':'b','h3':'n','g1':'n','a7':'p'})
PENDULUM = custom({'b6':'K','g5':'R','a8':'k','b3':'b','a4':'p','b2':'p','d6':'p','d7':'p'})
add('rectangle-pendulum', 'Restriction: a bishop rectangle and a king pendulum', (238, 240),
    'The strongest move may change an opponent’s available replies rather than check the king. Watch two composed problems use sacrifices and alternating threats to exhaust the defence.',
    ('Track a defender that is repeatedly diverted.', 'Explain how a repeated king move can change the pawn position.'),
    (
        section('Identify who can still do useful work', '''The rectangle problem gives White king c6, rooks f5/h7, and pawn b2 against king a6, bishop a5, knights h3/g1, and pawn a7. Black’s king and knights have little freedom, so the bishop carries important defensive duties. White’s rook moves make it abandon one line after another. The pendulum problem gives White king b6 and rook g5 against king a8, bishop b3, and pawns a4/b2/d6/d7. Here Black’s central pawns supply the remaining defensive tempos while the white king changes which mating threat is immediate.'''),
        section('A sacrifice can redirect the last defender', '''Begin the rectangle line with Rhh5, explicitly choosing the rook from h7 rather than f5. After ...Be1, Rh4 offers that rook to the bishop. Once ...Bxh4 is played, b4 gains space with a new threat, and the bishop retreats to d8. White then plays Ra5+ with the surviving rook. Black’s bishop captures on a5 and b5 is mate. Pause before each sacrifice and identify the purpose: the defender must travel to a square where the next pawn advance becomes decisive. The bishop’s journey a5–e1–h4–d8–a5 outlines the rectangle.'''),
        section('A return by the king can force progress elsewhere', '''In the pendulum line Kc7 threatens Ra5 mate. Black’s front pawn answers ...d5, physically blocking the rook’s route from g5 to a5. Kb6 switches the threat to Rg8 mate: that same pawn on d5 now blocks Black’s bishop on b3 from capturing a rook on g8. Black replies ...d4 to reopen the bishop’s diagonal. Kc7 revives Ra5, so the rear pawn advances from d7 to d5 and blocks the fifth rank again. After Kb6, the rear pawn cannot advance to d4 because its own front pawn occupies d4. The shown ...d3 moves the front pawn but leaves d5 blocking the bishop, so Rg8 is mate. The pendulum exploits alternating interference, not merely a supply of harmless waiting moves.'''),
        section('Separate the problem’s lesson from an automatic rule', '''These source problems concentrate on restriction and move order; their diagrams deliberately leave the defender very few useful resources. They do not imply that rook sacrifices or king shuffles usually win. In your games, look for a defender with two tasks and ask whether a threat can force it to abandon one. Also distinguish repetition from progress: a repeated piece route can improve your prospects if the opponent must weaken the position each time. For the defender, seek an active move that changes the mechanism rather than spending the last harmless pawn tempo. Always verify the final mate on the board, including possible blocks and captures.'''),
    ),
    (example('Source problem 6: draw the bishop around a rectangle', RECTANGLE, ('Rhh5','Be1','Rh4','Bxh4','b4','Bd8','Ra5+','Bxa5','b5#'), (
        'White’s two rooks and b2 pawn face a confined king a6. Black’s bishop a5 is the mobile defender; identify the inactive knights h3/g1 as well.',
        'Rhh5 brings the h7 rook to h5 and establishes the first constraint. The f5 rook remains available for the later sacrifice.',
        '...Be1 shifts the bishop to the opposite corner of its diagonal route.',
        'Rh4 offers the rook on a square accessible to the bishop.',
        '...Bxh4 accepts the sacrifice and diverts the bishop to h4.',
        'b4 advances two squares and creates the next problem for the confined king. Pause and identify the b-pawn’s eventual mating square.',
        '...Bd8 continues the bishop’s defensive journey.',
        'Ra5+ sacrifices the remaining rook with check, compelling attention to the a-file.',
        '...Bxa5 returns the bishop to its starting corner and removes the checking rook.',
        'b5# delivers pawn mate against the confined king. The white king protects the essential nearby squares.',
    )),
     example('Source problem 8: a king pendulum consumes pawn tempos', PENDULUM, ('Kc7','d5','Kb6','d4','Kc7','d5','Kb6','d3','Rg8#'), (
        'White king b6 and rook g5 can mate on a5 or g8 with the right king support. Black’s two d-pawns alternately block the rook’s rank and the bishop’s defensive diagonal.',
        'Kc7 threatens Ra5 mate by changing the king’s restriction of Black’s escape squares.',
        '...d5 moves the front pawn from d6 onto the rook’s path, preventing Ra5.',
        'Kb6 switches the immediate mating threat to Rg8.',
        '...d4 clears d5 and reopens the bishop’s diagonal b3–c4–d5–e6–f7–g8, defending against Rg8.',
        'Kc7 switches the threat back to the a-file.',
        '...d5 advances the rear pawn from d7, blocking the rook’s fifth-rank route again but also blocking the bishop’s diagonal to g8.',
        'Kb6 again makes Rg8 the relevant threat.',
        '...d3 moves the front pawn; the rear pawn stays on d5 and still blocks the bishop’s defence of g8.',
        'Rg8# mates along the eighth rank; the white king controls the escape on b7.',
    ))),
    'Start the rectangle line by moving the rook from h7 to h5.',
    (('Rhh5',True,'The h-rook moves to h5, preserving the f5 rook for its later task.'),('Rfh5',False,'This moves the wrong rook for the specified source line.'),('Rh8',False,'This does not establish the source’s h5–h4 sacrifice mechanism.')),
    (check('sacrifice','What is the purpose of the rook offers in the rectangle?',('To divert the bishop so the b-pawn can deliver mate.',True,'The material is spent to alter the defender’s position.'),('To increase White’s material count.',False,'White deliberately gives up material for the mating mechanism.')),
     check('pendulum','Why is the pendulum line not a threefold repetition?',('Black’s pawns change squares during the king’s returns.',True,'The whole position must repeat, not just the king’s squares.'),('Kings cannot participate in repetitions.',False,'Kings can repeat positions; the changed pawns are what matters here.'))),
    ('When two pawns share a file, track which one moved; the rear pawn cannot jump an occupied square.',),
    ('Follow the defender’s changing duties.', 'A repeated route may make progress when enemy resources are consumed.'))

RETURN = custom({'e2':'K','a1':'Q','b2':'B','c8':'N','a7':'P','d6':'P','a8':'k','a2':'p','b3':'p','b4':'p','b7':'p','e4':'p'})
add('return-trip', 'A bishop leaves and returns after the line changes', (239, 240),
    'A return move is useful when the opponent has changed the position in between. The bishop’s trip clears a queen route and forces pawn commitments before it comes home.',
    ('Explain what changed during an apparent loss of time.', 'Track a pawn obstruction on a long mating diagonal.'),
    (
        section('Inventory the cage and the blocked line', '''White has king e2, queen a1, bishop b2, knight c8, and pawns a7/d6. Black’s king a8 is boxed in by its own b7 pawn and the white control of nearby squares. Black also has pawns a2/b3/b4/e4. The queen would like to use the long diagonal from h1 to a8, but the e4 pawn initially blocks it. The bishop on b2 also has to be placed carefully. This is a composed mate-in-three problem, so examine how a quiet move changes Black’s available pawn replies before looking for an immediate check.'''),
        section('Leaving the diagonal creates a new situation', '''The first move Bh8 takes the bishop along b2–c3–d4–e5–f6–g7–h8. It does not check the king. Black’s main reply is ...e3, advancing the pawn that used to obstruct the h1–a8 diagonal. Pause here and mark the cleared e4 square. The tempting reaction is to insist that the bishop must continue forward because it has already spent a tempo moving. That treats moves as a story rather than comparing positions. What matters is which lines and legal replies exist now.'''),
        section('Returning can be the accurate continuation', '''White plays Bb2, returning the bishop to its starting square. Black then plays ...b6 in the source main line. Qh1 is now mate: the queen checks along h1–g2–f3–e4–d5–c6–b7–a8, where both e4 and b7 have become empty. The bishop on b2 and knight c8 help cover the black king’s exits, and White’s a7 pawn contributes to the cage. Before revealing the last move, trace the entire diagonal and identify every former obstruction. The queen was not able to use this line in the original arrangement.'''),
        section('Test different pawn replies separately', '''The source also indicates that an immediate ...b6 can be answered by Qg7, while ...b2 permits Qxa2. These are alternative branches with different geometry; do not combine their moves into the main line. The full problem rewards accurate waiting and line clearance rather than a stream of checks. In practical play, a piece may leave and return to provoke a pawn weakness, induce a defender to move, or change whose turn it is in a critical position. Such a maneuver is useful only if something concrete changes. If the opponent can improve freely or create a threat during the trip, a return may simply waste time. Always compare the resulting board, not the apparent direction of travel.'''),
    ),
    (example('Source problem 9: b2–h8–b2 clears the queen’s future diagonal', RETURN, ('Bh8','e3','Bb2','b6','Qh1#'), (
        'White’s queen a1 needs the future h1–a8 diagonal; Black’s e4 and b7 pawns obstruct it. Bishop b2 and knight c8 help confine the king a8.',
        'Bh8 begins the bishop’s return trip with a quiet move. Inspect Black’s available pawn moves.',
        '...e3 vacates e4, removing one obstruction from the queen’s intended mating diagonal.',
        'Bb2 returns the bishop to its original post after the pawn structure has changed.',
        '...b6 vacates b7, removing the second obstruction. Pause and trace h1 all the way to a8.',
        'Qh1# uses the now clear long diagonal. Supporting pieces and pawns eliminate the king’s escape squares.',
    )),),
    'Start the source return-trip solution by moving the bishop from b2 to h8.',
    (('Bh8',True,'The quiet bishop move begins the line-clearance mechanism.'),('Be5',False,'This is a different bishop move and does not start the specified return trip.'),('Qh1',False,'The intended checking diagonal is still blocked by e4 and b7 in the initial position.')),
    (check('return','Why is Bb2 not simply canceling Bh8?',('Black has advanced the e4 pawn in between, changing a key diagonal.',True,'A return can be useful when the opponent has made a commitment.'),('The bishop receives a bonus move after returning.',False,'Normal move rules apply; the changed pawn position supplies the value.')),
     check('line','What must be checked before the final Qh1?',('Every square on the long diagonal and all king escapes.',True,'Both e4 and b7 have to be clear in the main line.'),('Only whether h1 itself is empty.',False,'A queen cannot check through occupied intermediate squares.'))),
    ('Do not mistake an unchanged piece square for an unchanged position; pawns and turn order also matter.',),
    ('Name the change created during the trip.', 'Trace the complete checking line before declaring mate.'))

AMBLE = custom({'a6':'K','a3':'R','b5':'R','b4':'N','d6':'P','h4':'P','c4':'k','a7':'p','b6':'p','d7':'p','h5':'p','a4':'p','d3':'p'})
CUNNING = custom({'h4':'K','d4':'R','c2':'B','e8':'N','d5':'P','e3':'P','e5':'k','h6':'p'})
add('knight-rook-routes', 'Two unusual routes escort a king into a mating net', (239, 240),
    'A knight’s zigzag and a rook’s sideways maneuver can work through restrictions rather than repeated checks. Explain what squares each move removes from the king.',
    ('Trace knight control through an entire route.', 'Recognize a rook transfer that preserves a final mating line.'),
    (
        section('Inventory the escorts and the intended finish', '''In the knight problem White has king a6, rooks a3/b5, knight b4, and pawns d6/h4. Black has king c4 and several pawns, including d3 and h5. White’s knight will travel b4–d3–e5–f3–g5–h3 while the black king walks from c4 toward h4. In the rook problem White has king h4, rook d4, bishop c2, knight e8, and pawns d5/e3 against king e5 and pawn h6. These are composed problems with tightly controlled king routes. Identify the supporting pieces before assuming that the wandering piece alone causes the mate.'''),
        section('The knight moves crookedly to guide a straight journey', '''The first line begins Nxd3, removing the pawn while changing the king’s available squares. Black replies ...Kd4, then Ne5 induces ...Ke4. Nf3, ...Kf4, Ng5, ...Kg4, Nh3, ...Kxh4 complete the escort. Pause after every knight jump and list its attacks; notice that these are quiet restricting moves rather than a sequence of knight checks. Finally Rb4 is mate, with the knight h3 and rook a3 helping seal the king’s exits. The white h-pawn has served as a destination that the black king captures at the end of its journey.'''),
        section('The rook changes file before the finishing check', '''In the second line Rd1 quietly leaves the central rank. After ...h5, Rc1 changes file while keeping the final horizontal and vertical possibilities available. Black captures the pawn with ...Kxd5. White’s bishop now reaches f5 along c2–d3–e4–f5, and ...Ke5 places the king on the finishing rank. Rc5 is mate. Trace the bishop’s line and the knight e8’s control before revealing the last check. A rook that first retreats and then moves sideways can preserve a future entry better than an immediate direct attack.'''),
        section('Use the controlling-square method in practical calculation', '''The book’s playful routes demonstrate serious cooperation: a piece’s move matters because it leaves the opponent with particular replies. The supplied replays show the main source lines through mate; they are not a substitute for exploring every defence when solving the full compositions. In ordinary games the king may have additional exits, a defender may capture the escort, or an intermediate check may disrupt the route. Calculate those resources before committing to a long plan. For a beginner, reset after the replay and explain just one critical transition from each problem: why the next king square becomes relevant, and which supporting unit prevents escape when the final rook arrives.'''),
    ),
    (example('Source problem 10: the ambling knight escorts the king', AMBLE, ('Nxd3','Kd4','Ne5','Ke4','Nf3','Kf4','Ng5','Kg4','Nh3','Kxh4','Rb4#'), (
        'White’s rooks a3/b5 and knight b4 cooperate around king c4. Pawns d6/h4 and Black’s remaining pawns restrict the route. Pause before capturing d3.',
        'Nxd3 removes the pawn and starts the knight’s zigzag.',
        '...Kd4 takes the next square in the source king route.',
        'Ne5 changes the controlled squares and prepares the king’s further travel.',
        '...Ke4 moves one file toward the kingside.',
        'Nf3 continues the alternating knight route while the rooks retain their posts.',
        '...Kf4 advances along the fourth rank.',
        'Ng5 changes the knight’s control again, preparing the final approach.',
        '...Kg4 brings the king near the white h4 pawn.',
        'Nh3 reaches the final controlling square. Pause and calculate the rook check after the pawn is captured.',
        '...Kxh4 captures White’s h-pawn, but reaches the destination of the mating net.',
        'Rb4# checks along the fourth rank. The knight on h3 and rook a3 help eliminate the remaining escapes.',
    )),
     example('Source problem 11: d4–d1–c1–c5 is a rook route with a purpose', CUNNING, ('Rd1','h5','Rc1','Kxd5','Bf5','Ke5','Rc5#'), (
        'White king h4, rook d4, bishop c2, knight e8, and pawns d5/e3 confine Black’s king e5. Black also has pawn h6. Identify the bishop’s future route to f5.',
        'Rd1 retreats, preserving the rook while setting up a transfer to the c-file.',
        '...h5 advances Black’s remaining pawn and uses a tempo.',
        'Rc1 completes the sideways transfer. The rook is ready to enter c5 later.',
        '...Kxd5 removes the central pawn but brings the king into the intended route.',
        'Bf5 follows c2–d3–e4–f5 and changes the king’s available squares.',
        '...Ke5 returns the king to the fifth rank. Pause and verify the rook’s path from c1 to c5.',
        'Rc5# delivers the finishing rank check with the bishop, knight, king, and pawn covering the escapes.',
    ))),
    'Begin the ambling-knight solution by capturing the pawn on d3 with the knight.',
    (('Nxd3',True,'This starts the source escort route and removes the d3 pawn.'),('Nc2',False,'This does not capture d3 or begin the specified knight route.'),('Ra2',False,'The rook move abandons the requested knight operation.')),
    (check('quiet-route','Must every move in a mating route give check?',('No; quiet restrictions can determine the king’s replies.',True,'Most moves in these escort routes work by controlling squares.'),('Yes; a quiet move can never be part of a forced mate.',False,'A mating threat or a restricted position can make quiet moves forcing.')),
     check('support','Why must the rooks and other supporting pieces be included in the calculation?',('They cover exits the moving knight or rook cannot cover alone.',True,'The final net is a coordinated action.'),('They can be ignored once a route looks memorable.',False,'Without their control, the king may escape the final check.'))),
    ('Check captures and counterchecks at every stage of a long route; the opponent is never required to admire the pattern.',),
    ('List the controlled squares after each quiet move.', 'Verify the entire team’s contribution to the final mate.'))
