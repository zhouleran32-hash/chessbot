"""Original beginner teaching for all twenty three-movers and fifteen more-movers.

Positions were read from the uploaded book's diagrams (printed pp.381–387).
The solution references are printed pp.396–398. Every displayed line is legal;
short forcing claims were also checked by exhaustive legal-move search. Longer
engine checks and the limits of the seventeen-move analysis are recorded in the
appendix audit. This module does not require an engine at runtime.
"""
import chess
from core.primer_guides_chapter1 import section, example, check, guide

GUIDES = {}
EXERCISES = []


def _inventory(fen):
    board = chess.Board(fen)
    armies = []
    for color, label in ((chess.WHITE, 'White'), (chess.BLACK, 'Black')):
        groups = []
        for kind in (chess.KING, chess.QUEEN, chess.ROOK, chess.BISHOP, chess.KNIGHT, chess.PAWN):
            squares = board.pieces(kind, color)
            if squares:
                groups.append(chess.piece_name(kind) + ('s' if len(squares) > 1 else '') + ' on ' + ', '.join(chess.square_name(s) for s in squares))
        armies.append(label + ' has ' + '; '.join(groups))
    return 'White to move. ' + '. '.join(armies) + '.'


def _add(identifier, title, author, page, mate, fen, paragraphs, moves, notes, concept,
         defence_check, pitfalls, *, extra=()):
    inventory = _inventory(fen)
    key = moves[0]
    examples = [example('The source idea, played to checkmate', fen, moves, (inventory, *notes))]
    examples.extend(extra)
    q1, right1, why1, wrong1, correction1 = concept
    q2, right2, why2, wrong2, correction2 = defence_check
    sections = (
        section('Read the diagram and the task', f'{author}. Source problem {identifier.rsplit("-", 1)[1]}, printed page {page}; White is to mate in {mate} moves. {inventory} {paragraphs[0]}'),
        section('Understand the first move', paragraphs[1]),
        section('Calculate the defence', paragraphs[2]),
        section('Make the lesson useful in your games', paragraphs[3]),
    )
    GUIDES[identifier] = guide((page, 398 if identifier.startswith('app-more') else 397),
        (right1, right2), sections, examples, pitfalls,
        (check(identifier + '-idea', q1, (right1, True, why1), (wrong1, False, correction1)),
         check(identifier + '-defence', q2, (right2, True, why2), (wrong2, False, correction2))),
        (why1, why2, 'Reset the board and explain the key before replaying the mating line.'))
    # Practice explicitly asks for this source plan; a different legal move is
    # not automatically described as a losing move or an independently disproved key.
    board = chess.Board(fen)
    alternatives = [board.san(m) for m in board.legal_moves if board.san(m) != key][:2]
    choices = ((key, True, paragraphs[1]),) + tuple((san, False,
        f'{san} is legal, but it does not start the source plan taught here. {why1}') for san in alternatives)
    EXERCISES.append(dict(id=identifier, title=title,
        summary=f'{author}: mate in {mate}. {why1}', fen=fen, inventory=inventory,
        prompt=f'Find the first move of the source plan explained in this lesson (mate in {mate}).',
        choices=choices, objective=None))


# Data and teaching are kept together so every claim can be traced to its board.

_add(
    'app-three-01',
    'A checking key opens a bishop diagonal',
    'Ercole del Rio, 1750',
    381,
    3,
    '5N1k/6p1/5n1p/8/4Q3/2q5/6B1/7K w - - 0 1',
    ("The queen and bishop point toward the black king, but the knight on f6 interrupts the bishop's long "
 "diagonal. White also has a knight waiting on f8. Look for a way to change both knights' jobs. The enemy "
 'queen is far away; its material value matters less than whether it can answer the checks near h8.',
 'The key is Qh7+: White offers the queen with check. Black must use Nxh7, pulling the f6 knight away from the '
 "bishop's diagonal. Now Ng6+ puts White's knight on a square that attacks h8 while protecting h8's "
 'neighboring area. The sacrifice is payment for time and access, not a mistaken exchange of a queen for a '
 'knight. This is an explicit exception to the historical preference for quiet problem keys.',
 'After Qh7+ the knight capture is the only legal reply. After Ng6+ the king must go to g8. Only then does '
 'Bd5# finish: the bishop attacks g8 along d5–e6–f7–g8, and the knight removes h8. Black cannot capture the '
 'nearby knight with the king, nor can the distant queen solve this adjacent network. Check the empty '
 'intervening squares rather than assuming a bishop can jump.',
 'Practice by finding the obstruction before looking for checks: f6 is occupied by a defender. Then explain '
 "what changes after each sacrifice and why the king's next square is forced. In an ordinary game, use this "
 'thinking to search for deflection when a defender performs one essential job. Do not conclude that every '
 "queen sacrifice works; here each checking move sharply limits Black's legal choices."),
    ['Qh7+', 'Nxh7', 'Ng6+', 'Kg8', 'Bd5#'],
    ['Offer the queen on h7 with check, forcing the defender on f6 to leave its post.',
 'The black knight captures the queen and vacates the important f6 square.',
 'The white knight checks from g6 and forces the king away from h8.',
 'g8 is the only legal king destination.',
 'The bishop reaches d5 and checks along the now usable diagonal. The king has no legal reply.'],
    ('Why offer the queen on h7?',
 'To pull the f6 knight away and force the king route',
 'The queen sacrifice changes the defensive arrangement with tempo.',
 'To win a knight for free',
 'White gives up a queen; the compensation is a forced mate.'),
    ('Does a composition key have to be quiet?',
 'No; this key gives check',
 'Quiet keys are an aesthetic preference, not a chess rule.',
 'Yes; checking keys are illegal in problems',
 'Qh7+ is legal and is the source solution.'),
    ('Do not stop after the queen is captured; calculate the forced continuation.',
 'The bishop must have a clear path on its mating diagonal.')
)

_add(
    'app-three-02',
    'The Indian theme: block your bishop to let the king move',
    'G. Lawday, 1845; simplified by L. Kubbel',
    382,
    3,
    '8/1p6/7B/1K2p3/4k1P1/5n2/5PB1/3R4 w - - 0 1',
    ("Black's king is very restricted, but an immobile king is not necessarily mated. White must preserve a useful "
 'black move until a checking finish is ready. Study the bishop on h6 and the rook on d1 together. They will '
 'briefly interfere with one another, and that interference is the point of the combination.',
 'Bc1 retreats the bishop along h6–g5–f4–e3–d2–c1. It crosses d2 before the rook arrives there. After Black '
 "spends a pawn move, Rd2 blocks this bishop's diagonal. The temporary blockage releases f4 for the black "
 'king. This arrangement is called the Indian theme: an attacker first crosses a critical square, another '
 'attacker blocks it, and a later move reopens the line.',
 "The illustrated reply is ...b6. Then Rd2 leaves ...Kf4 as Black's only legal move. Rd4# both checks along "
 "the fourth rank and vacates d2, reopening the bishop's diagonal toward f4. Black's knight on f3 cannot "
 'simply leave: moving it would expose the king to the g2 bishop. The b-pawn cannot advance two squares '
 'initially because White’s king occupies b5; its only available advance is to b6.',
 'At your board, pause after Rd2 and name the square White has deliberately stopped attacking. Then move the '
 'king and ask what two jobs Rd4 performs. This is useful training in avoiding stalemate and coordinating line '
 'pieces. The lesson is not that blocking your bishop is normally good; it is that a temporary obstruction can '
 'make the opponent supply exactly the move your final attack needs.'),
    ['Bc1', 'b6', 'Rd2', 'Kf4', 'Rd4#'],
    ['Cross d2 with the bishop and prepare a deliberate temporary blockage.',
 'The b-pawn spends a move; the black king is still confined.',
 'The rook blocks its own bishop on d2, freeing f4 for the king.',
 'The king uses the newly available square; the f3 knight remains pinned.',
 'The rook leaves d2 and checks from d4. Reopened bishop support completes the mate.'],
    ('Why does the bishop retreat all the way to c1?',
 'To cross d2 before the rook blocks the diagonal',
 'The move order creates the temporary interference needed for the king route.',
 'Because bishops attack only from the back rank',
 'Bishops can attack from any clear diagonal.'),
    ('What is the purpose of Rd2?',
 'To release f4 temporarily',
 'Black must get a legal move before White can finish the mating construction.',
 'To win the f3 knight immediately',
 'There is no immediate capture; the knight is a pinned blocker.'),
    ('A king with no move is not automatically checkmated.',
 'Do not replace Bc1 with a bishop move that has not crossed d2.')
)

_add(
    'app-three-03',
    'Feed two knights to a pawn and open the a-file',
    'J. Tolosa y Carreras, 1892',
    382,
    3,
    '7k/Q6P/8/8/8/2pN4/2N1K3/1B6 w - - 0 1',
    ("The black king is trapped at h8, while White's h7 pawn cuts off g8. The queen on a7 is powerful but lacks "
 'the right checking diagonal. The black pawn on c3 is the only movable defender. White can exploit that '
 'limited choice by giving it a carefully ordered pair of captures.',
 "Nb2 offers the knight from d3. Black's king cannot move and its pawn must capture on b2. Then Na1 offers the "
 'other knight, from c2, to the same pawn. This is not random generosity: the pawn must arrive on a1, and both '
 "knights must disappear from the queen's route. White is arranging the final position before delivering any "
 'check.',
 'After ...bxa1=Q, Qxa1# brings the queen down the now open a-file. From a1 she checks along '
 'a1–b2–c3–d4–e5–f6–g7–h8. The former pawn has cleared b2 and c3 by moving and promoting. Black may promote to '
 'a rook, bishop, or knight instead; White still captures that new piece on a1 with the same mate. Promotion '
 'is compulsory, but choosing a queen is not.',
 "Replay the sequence using a different promotion piece and verify that the queen's final diagonal remains "
 'clear. This trains a useful habit: after a pawn capture, remove the pawn from its old square as well as '
 'removing the captured piece. A long diagonal can change in several places during a short combination. In '
 'games, examine forced pawn captures whenever a blocked queen or bishop needs a route.'),
    ['Nb2', 'cxb2', 'Na1', 'bxa1=Q', 'Qxa1#'],
    ['Offer the d3 knight on b2; the black king still has no safe move.',
 'The pawn captures and leaves c3, clearing one square of the future mating diagonal.',
 'Offer the c2 knight on a1 and clear the queen’s a-file route.',
 'The pawn captures and promotes; any promotion type permits the same finish.',
 'The queen captures on a1 and checks the king on h8 along the fully cleared diagonal.'],
    ('What does the pawn journey c3–b2–a1 accomplish?',
 'It clears the queen’s final diagonal',
 'Both c3 and b2 become empty before Qxa1#.',
 'It protects the black king permanently',
 'The new piece is captured and cannot stop mate.'),
    ('Would promoting to a knight avoid the shown finish?',
 'No; Qxa1# still captures it',
 'All four promotions put a capturable piece on the same square.',
 'Yes; only queen promotion allows a capture',
 'A queen can capture any enemy non-king piece on her line.'),
    ('Nb2 is a knight move, not a queen move.', 'Remember to promote the black pawn before White captures it.')
)

_add(
    'app-three-04',
    'A rook clears the queen’s route through promotion',
    'P. Daly, 1935',
    382,
    3,
    'kb5Q/p7/P7/8/1p6/1R6/1P4p1/6K1 w - - 0 1',
    ("The black king on a8 has almost no freedom: its own bishop and pawn fill nearby squares, and White's a6 pawn "
 "restricts b7. White's queen on h8 would like a clear attacking line from the lower corner. The white rook "
 'must travel without giving Black a useful escape or leaving its own king exposed.',
 'Rh3 sends the rook across the third rank. It is a preparatory move: after ...b3 the rook can reach h1. '
 'Moving directly toward the final capture would ignore the need to place a white unit where the g2 pawn can '
 "take it. The rook is used as an invitation, bringing that pawn to h1 and clearing g2 for the queen's later "
 'diagonal.',
 "The complete line is Rh3 b3 Rh1 gxh1=Q+ Qxh1#. Black's promotion gives check to the white king on g1, but "
 "White removes the checking piece while delivering mate. The queen's new line is h1–g2–f3–e4–d5–c6–b7–a8. "
 'Black can choose a different promotion, and White still captures it. A check is urgent, but it does not '
 'guarantee that the checking side is safe.',
 'Before the final capture, trace every square from h1 to a8 and explain why g2 is now empty. Then verify that '
 "Qxh1 answers the check on White's king. This combines two beginner skills: keeping track of promotion and "
 "checking the legality of a countercheck. In practical play, an opponent's forcing move may help you if the "
 'required response simultaneously reaches your own goal.'),
    ['Rh3', 'b3', 'Rh1', 'gxh1=Q+', 'Qxh1#'],
    ['The rook prepares to reach h1 while preserving the intended pawn reply.',
 'The b-pawn moves down one square; the black king remains boxed in.',
 'Offer the rook on h1 to the g2 pawn.',
 'Black captures and promotes with check against the white king.',
 'Capture the promoted piece, remove the check, and mate along h1–a8.'],
    ('Why is the g2 pawn encouraged to capture on h1?',
 'To clear g2 for the queen’s diagonal',
 'The pawn’s capture opens h1–a8.',
 'Because promotions cannot give check',
 'A promoted piece can give check immediately.'),
    ('How does White answer the promotion check?',
 'Qxh1# captures the checker and mates',
 'One legal move can defend the king and deliver mate.',
 'White may ignore the check because mate is threatened',
 'Every move must leave White’s king safe.'),
    ('A promotion check must still be answered legally.',
 'Do not leave the g2 pawn on the board after it promotes.')
)

_add(
    'app-three-05',
    'Sacrifice the queen to build a bishop mate',
    'W. Shinkman, 1890',
    382,
    3,
    '8/4K3/2k5/5Q1B/bp6/8/7B/8 w - - 0 1',
    ('White has a queen and two bishops against a king, bishop, and pawn. Material superiority does not tell you '
 "the three-move solution. Focus on the two bishops' different square colors and the black king's access to b6 "
 'or b7. White needs a way to cover a flight square while bringing the king onto a mating diagonal.',
 'Be2 redeploys the h5 bishop. The move leaves the queen free to sacrifice herself after either principal king '
 'retreat. After ...Kb6, Qa5+ offers the queen on a5; after ...Kb7, Qc8+ offers her on c8. The queen chooses '
 "the king's destination. The bishops then provide the check and the support needed to finish.",
 'In the main line ...Kxa5 is the only answer to Qa5+. Bc7# follows, moving the h2 bishop along '
 'g3–f4–e5–d6–c7. The bishop on e2 controls b5; the bishop on c7 checks along b6–a5. Thus the final net is '
 'constructed from two diagonals, not from a surviving queen. Against ...Kb7, Qc8+ Kxc8 Ba6# gives the '
 'corresponding second pattern.',
 'Set up both final positions and name which bishop covers each escape. The queen sacrifice should feel less '
 'mysterious once you can see its exact destination. In a normal game, consider whether a checking sacrifice '
 'can draw a king into a net formed by quieter pieces. Always calculate the capture and the refusal; here the '
 'checking offers force the relevant king captures.'),
    ['Be2', 'Kb6', 'Qa5+', 'Kxa5', 'Bc7#'],
    ['Redeploy the h5 bishop to e2 to prepare the bishop net.',
 'The king chooses b6, entering the first of the two main patterns.',
 'Offer the queen with check on a5 and control the remaining flights.',
 'The king must capture the queen on a5.',
 'The h2 bishop reaches c7, checks a5, and works with the e2 bishop to deny every escape.'],
    ('What is the queen sacrifice buying?',
 'A precise destination for the black king',
 'The bishops can mate once the king is drawn onto their net.',
 'A favorable material exchange',
 'White sacrifices the strongest piece to mate.'),
    ('After the king captures on a5, which move mates?',
 'Bc7#',
 'The h2 bishop checks along c7–b6–a5 while the other bishop covers b5.',
 'Bf3',
 'That move does not reproduce the required checking geometry.'),
    ('The two bishops have different jobs and different square colors.',
 'Use Qc8+ against ...Kb7, rather than copying the a5 route blindly.')
)

_add(
    'app-three-06',
    'A bishop retreats so the queen can answer a checking capture',
    'A. Galitsky, 1890; corrected 1903',
    382,
    3,
    'Q7/8/4P3/1p6/p1B2P2/2B3Pp/1P5K/krbR4 w - - 0 1',
    ("Black's king is in the a1 corner behind its rook and bishop. White has several active pieces, but the b2 "
 'pawn can be captured in two different ways. The important distinction is whether the capturing piece checks '
 "White's king. Label those captures before trying to memorize a single mating line.",
 'Bh8 moves the bishop from c3 along d4–e5–f6–g7–h8. This long retreat clears c3 and keeps useful pressure on '
 'the long diagonal. It prepares different answers to ...Bxb2 and ...Rxb2+. The correct key must work against '
 'both, including the reply that gives check. A solution that handles only the quiet capture is incomplete.',
 'Against ...Bxb2, Rh1 creates the mating threat on the first rank; the illustrated ...a3 is answered by '
 'Qxa3#. The queen checks along a3–a2–a1 while the bishop on c4 protects a2. Against ...Rxb2+, White must '
 "first answer check: Qg2 blocks on the second rank. If ...hxg2 follows, Rxc1# removes the corner king's "
 'remaining screen. These branches use different attackers because different black pieces have moved.',
 'Replay each capture from the original position. State aloud whether White is in check before choosing a '
 'response. Then compare the two final mating pictures and identify the newly vacant line. This is practical '
 'calculation training: two captures on the same square can have completely different consequences. The '
 'destination alone is not enough; track which piece moved, what it uncovered, and whether it gave check.'),
    ['Bh8', 'Bxb2', 'Rh1', 'a3', 'Qxa3#'],
    ['The bishop retreats from c3 to h8, preparing the two distinct capture branches.',
 'The bishop, rather than the rook, captures b2 without checking White’s king.',
 'The rook reaches h1 and creates a mating threat along the first rank.',
 'Black tries to move the a-pawn and alter the corner position.',
 'The queen captures on a3; the c4 bishop guards a2 and the corner king is mated.'],
    ('Why distinguish ...Bxb2 from ...Rxb2+?',
 'The rook capture gives check and requires a different answer',
 'White must answer ...Rxb2+ with a legal check response such as Qg2.',
 'All captures on b2 create the same position',
 'The capturing piece and the line it vacates both matter.'),
    ('What does Qg2 do against ...Rxb2+?',
 'It blocks the checking line on the second rank',
 'The queen meets the check before White completes the mating threat.',
 'It ignores check to attack the king',
 'Ignoring a check is illegal.'),
    ('Rh1 is the bishop-capture branch; it does not answer a rook check on the second rank.',
 'Keep the identities of the two b2 capturers separate.')
)

_add(
    'app-three-07',
    'One discovered queen check, four king routes',
    'S. Loyd, 1857',
    382,
    3,
    '6R1/2K5/8/8/5p2/6p1/1Q3Nk1/8 w - - 0 1',
    ("The black king is exposed on g2, but White cannot assume it will walk into the same mate every time. White's "
 'queen, rook, and knight must coordinate around several different king exits. The pawns on f4 and g3 both '
 'restrict Black and provide potential defensive moves.',
 'Ng4+ moves the knight off f2, opening the queen’s line from b2 to the black king on g2. The queen gives '
 'the discovered check; the knight on g4 does not attack g2. The key is a check, another reminder that quiet keys are a '
 'preference rather than a legal requirement. After the check, examine each legal king destination. The source '
 'highlights h1, h3, f3, and f1. Each location changes which white piece can finish and which square must '
 'first be controlled.',
 'The main line uses ...Kh1 Qh2+ gxh2 Nf2#. White gives the queen so that the g3 pawn moves to h2, where it '
 'blocks its own king. The knight then returns to f2 and checks h1. Against ...Kh3, Nh2 prepares a different '
 'net. Against ...Kf3, Qc2 is the quiet continuation; against ...Kf1, Ra8 prepares a rook finish. These are '
 'separate calculations, not interchangeable second moves.',
 'Start by solving the h1 branch until you can explain why the pawn is a useful blocker. Then reset and choose '
 'another king reply. This trains branching without requiring you to remember every move at once. In your own '
 'games, a forcing check is valuable because it narrows the options, but several legal answers may remain. '
 'Enumerate them before calling a combination forced.'),
    ['Ng4+', 'Kh1', 'Qh2+', 'gxh2', 'Nf2#'],
    ['The knight leaves f2 for g4, uncovering the queen’s check along b2–c2–d2–e2–f2–g2.',
 'The king chooses h1; a different second move is needed against other destinations.',
 'Sacrifice the queen with check on h2.',
 'The g3 pawn must capture, blocking h2 beside its own king.',
 'The knight returns to f2 with check; the pawn on h2 prevents the corner escape.'],
    ('Why does White want ...gxh2?',
 'The black pawn blocks h2 beside its own king',
 'A defender’s own piece can help complete a mating net.',
 'It wins White’s queen back',
 'The queen is sacrificed and does not return.'),
    ('Can White copy Qh2+ after every king reply?',
 'No; each king destination needs its own continuation',
 'The source uses Nh2, Qc2, and Ra8 in other branches.',
 'Yes; a checking key always has one fixed continuation',
 'Checks can leave several legal responses.'),
    ('Do not count only the king reply you hoped to see.',
 'A return to the knight’s original square can be the point of the combination.')
)

_add(
    'app-three-08',
    'The Steinitz Gambit: walk into checks and answer with mate',
    'S. Loyd, 1903, “Steinitz Gambit”',
    383,
    3,
    '4r1b1/1p4B1/pN2pR2/RB2k3/1P2N2p/2p3b1/n2P1p1r/5K1n w - - 0 1',
    ("This crowded position rewards patience. White's rooks, bishops, and knights already form a net around the "
 'king on e5. Black has many pieces, including a pawn one step from promotion. Count the lines around e5 '
 'rather than comparing material. The apparently exposed white king will become part of the mating '
 'construction.',
 'Ke2 permits ...f1=Q+. Instead of taking the new queen, White plays Ke3. The king steps into a forest of '
 'possible checks while controlling d4 and f4, squares the black king might otherwise use. That control makes '
 "Black's checking replies vulnerable to captures or blocks that simultaneously give mate. The quiet king move "
 'is safe only because every legal checking resource has an adequate answer.',
 'In the displayed branch Black tries ...Bf2+, and Rxf2# answers check by capturing the bishop and revealing '
 "the bishop g7's diagonal toward e5. Other checks need other replies: ...Qd3+ permits Bxd3#, ...Re2+ permits "
 'Bxe2#, and ...Qg1+ permits Rf2#. If Black promotes to a knight with check on move one, Rf2+ is the source '
 'response. The queen-promotion main line must not be applied blindly to that underpromotion.',
 'At 564, treat this as a guided calculation exercise rather than a model for exposing your king in every '
 "game. First check the white king's legality; then identify the line that opens when a checking piece is "
 'captured. Reset after each branch. This position also illustrates why a short engine search can overlook a '
 'quiet mating construction: the legal reply tree, not an unexplained evaluation number, establishes the '
 'tactic.'),
    ['Ke2', 'f1=Q+', 'Ke3', 'Bf2+', 'Rxf2#'],
    ['The king deliberately allows the f-pawn to promote with check.',
 'Black promotes to a queen and attacks the king on e2.',
 'The king advances to e3 and controls important flight squares around e5.',
 'Black chooses a bishop check from f2.',
 'The rook captures the checking bishop; moving it also uncovers the g7 bishop’s attack on e5, and Black is '
 'mated.'],
    ('What is White’s king doing on e3?',
 'Controlling escape squares while the other pieces supply mate',
 'The king’s control of nearby squares is essential to the construction.',
 'Ignoring the opponent’s checks',
 'Every move in the line legally answers the current check.'),
    ('Should White always answer promotion with Ke3?',
 'No; knight promotion gives a different check',
 'The source answers ...f1=N+ with Rf2+.',
 'Yes; the promotion piece never matters',
 'Different promoted pieces attack different squares.'),
    ('Do not mistake the f6 rook’s discovered attack for a direct rook check on e5.',
 'This unusual safe king walk depends on the exact diagram, not a general rule.')
)

_add(
    'app-three-09',
    'Remove a pawn shield to expose the king',
    'T. Herbeck, 1923',
    383,
    3,
    'Q5rk/4K1pp/6P1/5N2/4B3/8/8/8 w - - 0 1',
    ("The black rook sits on g8, next to the king on h8. White's g6 pawn is close to promotion but blocks some "
 'lines, and the knight on f5 can reach h6. The objective is not to promote the pawn. White needs the black '
 'king on a square that the queen can attack from the distant corner.',
 'Nh6 offers the knight to the g7 pawn. After ...gxh6, g7+ advances the white pawn with check. The pawn now '
 'attacks h8, so Black must address the check. The rook on g8 appears able to capture the pawn on g7, but it '
 'is pinned on the eighth rank by the queen on a8. Moving that rook would uncover a queen check on h8. Kxg7 is '
 'therefore the forced legal response.',
 'After ...Kxg7, Qa1# checks along a1–b2–c3–d4–e5–f6–g7. The bishop on e4 controls useful flight squares and '
 'supports the net. The knight and pawn sacrifices removed the original g7 pawn and drew the king onto g7. The '
 'black rook remains on g8; it is not the capturing piece in the main line. This distinction is easy to lose '
 'when reading a dense printed solution.',
 "Replay the position slowly and distinguish a piece's movement ability from its legal freedom. A rook "
 'normally moves down a file, but a pinned rook may not leave its rank if that exposes its king. Then trace '
 "the queen's final diagonal and test the king's neighboring squares. The practical lesson is to combine "
 'deflection with a pin, rather than considering each attacking move in isolation.'),
    ['Nh6', 'gxh6', 'g7+', 'Kxg7', 'Qa1#'],
    ['Offer the knight on h6 to pull the g7 pawn away.',
 'Black captures the knight, removing the original shield on g7.',
 'Advance the white pawn with check and invite the king onto g7.',
 'The king captures; the g8 rook is constrained by the queen’s line across the eighth rank.',
 'The queen reaches a1 and checks the king on g7 along the long diagonal, with bishop support.'],
    ('Why does the g8 rook not simply take the pawn on g7?',
 'Leaving the eighth rank would expose the king to the queen',
 'The rook is pinned while the king remains on h8.',
 'Rooks cannot capture pawns',
 'They can, provided the move does not expose their king.'),
    ('Which piece captures on g7 in the shown line?',
 'The black king',
 'Kxg7 puts the king on the queen’s final diagonal.',
 'The black rook',
 'That move would not legally answer the position’s pin and check.'),
    ('The defender on g8 is a rook, and Kxg7 is a king capture.',
 'The white pawn is sacrificed; promotion is not the objective.')
)

_add(
    'app-three-10',
    'Meet a pawn threat with a queen sacrifice',
    'I. Kers, 1932',
    383,
    3,
    'N7/5p2/pR3P2/Bpkp2p1/3pp3/1b5R/1P5K/nQ6 w - - 0 1',
    ("Black's king is surrounded by pawns, but some are shields rather than permanent walls. White's queen on b1 "
 "and rook on h3 can attack different lines. Before moving, notice Black's g-pawn: an advance may threaten a "
 'check against the white king on h2. A good mating plan must survive that counterthreat.',
 "Qd3 centralizes the queen and prepares mating play while keeping track of ...g4. Black's pawn advance "
 'threatens ...g3+, so White cannot assume every second move is harmless. Qc4+ changes the race by giving a '
 'forcing check and offering the queen to the d5 pawn. The pawn must leave d5, clearing the fifth rank for the '
 "h3 rook's eventual check.",
 'After ...dxc4, Rh5# attacks the king along h5–g5–f5–e5–d5–c5. The g-pawn has already vacated g5, and the '
 'd-pawn has vacated d5; both events matter. The source also answers ...Nc2 with Qxb3, removing the bishop, '
 "while many other first replies allow Rh8. The main line is chosen to show why Black's apparent counterthreat "
 "helps open the rook's route.",
 'List the occupied squares between h5 and c5 before the key, then list them after the queen sacrifice. This '
 'makes the combination understandable without memorizing the whole diagram. In games, a pawn threat can '
 'sometimes be met by a forcing attack that exploits the squares the pawn abandoned. Do not ignore the threat '
 'on principle; calculate why your checks arrive first.'),
    ['Qd3', 'g4', 'Qc4+', 'dxc4', 'Rh5#'],
    ['The queen moves to d3 and prepares responses to Black’s different defensive choices.',
 'The pawn leaves g5 and threatens a check from g3.',
 'Offer the queen with check, compelling the d5 pawn to change files.',
 'The pawn captures and vacates d5, opening the rook’s future fifth-rank line.',
 'The rook checks from h5 across the cleared rank. Black’s king has no legal defence.'],
    ('Which two pawn departures help Rh5#?',
 'The g-pawn leaves g5 and the d-pawn leaves d5',
 'Both squares lie on the rook’s checking rank.',
 'Only the g-pawn matters',
 'The d5 pawn would also block the rook’s path.'),
    ('Why can White answer ...g4 with Qc4+?',
 'The forcing check makes Black respond immediately',
 'The sacrifice creates the mate before ...g3+ can occur.',
 'Pawn checks may be ignored in compositions',
 'The line works through legal forcing moves, not an exception.'),
    ('Do not forget the counterthreat ...g3+.',
 'A rook cannot attack through the d5 pawn until that pawn has moved.')
)

_add(
    'app-three-11',
    'Invite a bishop check, then block with a sacrifice',
    'F. Palitsch, 1930',
    383,
    3,
    '3b4/8/7R/8/8/R7/7P/5K1k w - - 0 1',
    ("Black's king is trapped beside the h2 pawn, and its bishop is the only active defender. White's two rooks "
 'seem overwhelming, yet an immediate check is not the whole solution. Notice how a capture from h2 onto g3 '
 'would vacate the h-file and uncover a check by the rook on h6. White must arrange a black piece on that '
 'square at the right moment.',
 'Kf2 improves the king and allows the bishop to check from h4. White then responds with Rg3, moving the a3 '
 "rook across the third rank to block the bishop's line h4–g3–f2. The rook is offered for capture. This is a "
 "defensive interposition with an attacking purpose: it places a black bishop where White's h-pawn can capture "
 'it.',
 'After ...Bxg3+, hxg3# answers the new check and opens the h-file for the rook on h6. The pawn itself now '
 'stands on g3, while the rook delivers the discovered check down to h1. The white king on f2 controls g1 and '
 'g2, so Black cannot escape sideways. Other bishop moves after Kf2 permit corresponding rook mates; the '
 'checking move is the most instructive defence to calculate.',
 'Practice the three legal answers to a check: move the king, capture the checker, or block the line. Here '
 'blocking is best because it improves the final attack. After the pawn capture, do not identify the checking '
 'piece by habit: hxg3# is a pawn move, but the rook on h6 supplies the actual check. Discovering which line '
 'opens is more useful than memorizing the symbol at the end.'),
    ['Kf2', 'Bh4+', 'Rg3', 'Bxg3+', 'hxg3#'],
    ['The king reaches f2 and controls the corner king’s future escape squares.',
 'The bishop checks along h4–g3–f2.',
 'The a3 rook blocks on g3 and invites capture.',
 'The bishop captures the interposed rook and checks again.',
 'The h-pawn captures the bishop, answers check, and opens the h6 rook’s mating line.'],
    ('Why block with Rg3?',
 'To put the bishop on g3 for the h-pawn to capture',
 'The defensive block prepares a discovered rook mate.',
 'Because the king may remain in check for one move',
 'Rg3 legally interrupts the bishop’s line immediately.'),
    ('Which piece gives the final check after hxg3#?',
 'The rook on h6',
 'The pawn vacates h2 and opens the h-file.',
 'The pawn on g3',
 'That pawn attacks f4 and h4, not h1.'),
    ('A move marked # need not give check with the piece that moved.',
 'Keep the king on f2: its control of g1 and g2 matters.')
)

_add(
    'app-three-12',
    'Place the queen to meet a bishop’s changing diagonal',
    'S. Loyd, 1869',
    383,
    3,
    '5N1k/5Ppp/8/8/2Q3p1/8/8/b6K w - - 0 1',
    ("The black bishop on a1 can move along a long diagonal, while the pawns near h8 shelter the king. White's f7 "
 'pawn and f8 knight are already close to the corner. The queen needs a flexible starting square from which '
 "she can attack either the bishop or h7, depending on Black's choice.",
 'Qf1 is a quiet key. It keeps several useful queen routes available without releasing the mating net. Against '
 "...Bb2, Qb1 attacks the bishop and h7 along the first-rank queen's diagonal. Against ...Bc3 or ...Bd4, Qd3 "
 'performs the analogous job; against ...Be5 or ...Bf6, Qf5 is the matching queen move. Follow the geometry '
 'rather than treating these as unrelated memorized answers.',
 'The displayed line uses ...Bb2 Qb1 g3 Qxh7#. The knight on f8 protects h7, so the king cannot capture the '
 'checking queen. If the bishop stays exposed, White can instead capture it with mate in the appropriate '
 'branch. The source also gives Qb1 against ...h6 and Ng6+ against ...g3. A pawn move changes the correct '
 'response just as a bishop move does.',
 'Reset the board and choose three bishop destinations. For each, find the queen square that attacks that '
 'bishop while maintaining a mating threat. This is a small lesson in double attacks: the target need not be '
 'valuable material if capturing it ends the game. At your rating, train the shared pattern first, then check '
 "the exact diagonal and the king's available squares in each variation."),
    ['Qf1', 'Bb2', 'Qb1', 'g3', 'Qxh7#'],
    ['The queen chooses a flexible central starting point on f1.',
 'The bishop chooses b2 on its long diagonal.',
 'The queen attacks b2 and h7 from b1, creating two mating possibilities.',
 'Black moves the g-pawn but cannot stop the h7 finish.',
 'The queen captures h7 with check, protected by the f8 knight, and mates.'],
    ('Why do Qb1, Qd3, and Qf5 appear in different branches?',
 'They match the bishop’s chosen square',
 'Each queen move combines pressure on the bishop with a mating threat.',
 'Any queen move wins in exactly the same way',
 'The required lines depend on where Black’s bishop moved.'),
    ('What protects the queen after Qxh7#?',
 'The knight on f8',
 'A knight on f8 attacks h7.',
 'The pawn on f7',
 'The f7 pawn attacks e8 and g8.'),
    ('A bishop move to a new square changes the queen’s best route.',
 'Do not overlook the g-pawn’s different continuation.')
)

_add(
    'app-three-13',
    'Move a bishop away, then retreat the knight',
    'S. Loyd, 1876',
    383,
    3,
    '8/6p1/6Qp/3N1p1P/2P5/5k2/2P1p3/4K1B1 w - - 0 1',
    ("Black's king is far from its own pawns, yet the e2 pawn is close to promotion and the white king must remain "
 "safe. White's queen is active on g6, with a knight on d5 and bishop on g1. Identify which squares the knight "
 'controls now and which squares would become available if it moved.',
 'Ba7 sends the bishop to the far end of its diagonal. After ...f4, Nb6 retreats the knight from d5. This '
 "apparently quiet retreat is the center of the plan: it changes the net and makes e3 the king's compelled "
 "destination. The bishop's long-range support remains useful even though it looks far from the black king. "
 "Distance alone does not measure an attacker's contribution.",
 "The main continuation is ...Ke3 Qd3#. The queen checks at close range and is protected by White's c2 pawn. "
 'The white king on e1 helps control d2, e2, and f2, while the c4 pawn controls d5. If Black instead moves the '
 'king to e4 immediately after Ba7, the source uses Qg3, threatening a different close-range mate. The knight '
 'retreat belongs to the ...f4 branch, not every reply.',
 'On the final board, test whether the king could capture the queen: the c2 pawn prevents it. Then return to '
 "the position before Nb6 and compare the king's legal choices. This trains you to view a retreat as a change "
 'in square control rather than as a loss of attacking spirit. In practical games, a distant bishop or a '
 'backward knight move may coordinate better than the most aggressive-looking advance.'),
    ['Ba7', 'f4', 'Nb6', 'Ke3', 'Qd3#'],
    ['The bishop reaches a7 and preserves long-range control while preparing the net.',
 'The f-pawn advances, changing the king’s available squares.',
 'The knight retreats to b6 and reorganizes the mating net.',
 'The king is driven onto e3 in this branch.',
 'The queen checks from d3, protected by the c2 pawn; every escape is covered.'],
    ('Why is Qd3# safe from the king’s capture?',
 'The c2 pawn protects d3',
 'A queen next to a king still needs protection.',
 'Queens cannot be captured by kings',
 'A king may capture an undefended queen if the destination is safe.'),
    ('Is Nb6 meant for every first reply?',
 'No; the immediate ...Ke4 branch uses Qg3',
 'The second move depends on the defender’s choice.',
 'Yes; only the first move matters',
 'A correct key still needs accurate continuations.'),
    ('The retreat is Nb6, a knight move, not a bishop or queen move.',
 'Account for the c2 pawn when judging the final queen sacrifice risk.')
)

_add(
    'app-three-14',
    'A bishop retreat prepares a safe king capture',
    'J. Kohtz and C. Kockelkorn, 1903',
    384,
    3,
    '8/6Q1/2B5/5p2/5k2/6p1/2N5/6K1 w - - 0 1',
    ("White's queen is near the black king, but the black g3 pawn stands close to the white king on g1. The bishop "
 'on c6 can retreat all the way to h1. Before calculating, trace that diagonal and note that a bishop may move '
 'backward as freely as forward when the route is clear.',
 'Bh1 is the quiet key. After ...g2, Kxg2 removes the advanced pawn and activates the white king. The bishop '
 'has preserved its diagonal toward the center while making this king maneuver possible. White does not rush a '
 'queen check: first the arrangement of the king, bishop, and knight must make the final close-range queen '
 'move safe.',
 'Black then has ...Ke4, and Qd4# finishes. The knight on c2 protects d4, so the black king cannot capture the '
 'checking queen. The queen also attacks the nearby escape squares, with the bishop and king completing the '
 "net. The full line has only one capture, but it changes the white king's role from a potentially threatened "
 'piece into an active supporter.',
 "Practice by identifying the protector of the final queen before moving her. Then explain why the bishop's "
 'retreat did not remove it from the battle: its diagonal still matters after the king and pawn move. In a '
 'game, a quiet preparatory move can be useful when an immediate attack leaves a flight square or an unsafe '
 'checking piece. Work backward from the final mate to determine which support is missing.'),
    ['Bh1', 'g2', 'Kxg2', 'Ke4', 'Qd4#'],
    ['The bishop retreats to h1, preserving its useful diagonal while preparing the king maneuver.',
 'The pawn advances to g2 near White’s king.',
 'The king captures the pawn and reaches an active supporting square.',
 'The black king moves to e4, the destination the net allows.',
 'The queen checks from d4, protected by the c2 knight, and mates.'],
    ('What protects the queen on d4?',
 'The knight on c2',
 'The knight attacks d4 and makes the king’s capture illegal.',
 'The queen protects herself',
 'A queen cannot protect her own square from capture.'),
    ('What is the value of Kxg2?',
 'It removes the pawn and activates the king',
 'King participation helps complete the mating net.',
 'It allows White to ignore king safety',
 'The capture is legal only because g2 is safe.'),
    ('Bh1 is the bishop key; Qh1 is not the source move.',
 'Verify the knight’s protection before placing the queen next to the king.')
)

_add(
    'app-three-15',
    'Lure a rook away, then return the queen as bait',
    'P. Orlimont, 1907',
    384,
    3,
    '8/2p5/N1P5/1bQ5/kPr5/8/1K1B4/8 w - - 0 1',
    ("The black rook on c4 helps confine the white pieces, and the white pawn on c6 blocks the c-file. White's "
 'queen stands on c5 beside a knight on a6. The final mating unit will be the knight, but first White must '
 'arrange a black rook on the square that knight can capture.',
 'Qf5 moves the queen away from c5. After ...Rxc6, the pawn on c6 disappears and the rook leaves c4. Now Qc5 '
 'offers the queen on her original square. This return has a new purpose because the position has changed: the '
 "rook can capture on c5 and become the knight's final target. The queen's trip is a deliberate lure, not a "
 'meaningless loss of time.',
 "The line continues ...Rxc5 Nxc5#. The knight from a6 gives check to the king on a4. White's b4 pawn blocks "
 "b4 and controls a5; the king on b2 controls a3 and b3. Black's bishop on b5 also occupies a square the king "
 'might otherwise want. Replacing the final knight capture with a queen capture would produce a different '
 'position and does not give this mating check.',
 'Replay the position twice: first following the queen, then following only the black rook. The second view '
 "reveals the mechanism more clearly: c4–c6–c5 is a forced itinerary ending on the knight's capture square. In "
 'games, a sacrifice often works because it relocates a defender, not merely because it removes material. '
 "Track the defender's changing job after each capture."),
    ['Qf5', 'Rxc6', 'Qc5', 'Rxc5', 'Nxc5#'],
    ['The queen vacates c5 and invites the rook to take c6.',
 'The rook captures the c6 pawn and leaves its original defensive square.',
 'The queen returns to c5 as a second sacrifice.',
 'The rook captures the queen and lands on the knight’s target square.',
 'The a6 knight captures on c5 with check; White’s king and pawn complete the net.'],
    ('Why return the queen to c5?',
 'To lure the rook onto the knight’s capture square',
 'The position changed after ...Rxc6, giving Qc5 a new purpose.',
 'To repeat the position for a draw',
 'The pawn has vanished and the rook has moved; it is not the same position.'),
    ('Which piece delivers the final mate?',
 'The knight from a6',
 'Nxc5# checks a4 and fits the surrounding square control.',
 'The queen from f5',
 'The queen has been sacrificed on c5.'),
    ('Qc5 is the second white move; Nxc5# is the third.',
 'Do not confuse the queen’s return with a repetition of the whole position.')
)

_add(
    'app-three-16',
    'The Bristol theme: clear a path for the queen',
    'F. Healey, 1861',
    384,
    3,
    '8/1n3Np1/1N4Q1/1bkP4/p1p2p2/P1P2R2/3P2PK/B2R4 w - - 0 1',
    ("White's queen needs to reach the first rank, but the rook on d1 obstructs her eventual route. Another rook "
 'on f3 and the minor pieces already restrain the king on c5. Look for a way to move the obstructing rook '
 'beyond the square the queen will later need, while preserving all important controls.',
 'Rh1 clears d1 and the rest of the route from b1 to g1. This is a line-clearance idea called the Bristol '
 'theme: one line piece travels ahead so another can follow along the same line. The rook does not need to '
 'capture anything. After ...Be8, Qb1 takes the queen to the entry point of the cleared first rank.',
 "The queen now threatens Qb4#. Black's bishop can return to b5 to answer that threat, but Qg1# then checks "
 "the king along g1–f2–e3–d4–c5. The rook is safely beyond the queen's destination on h1, so it no longer "
 'blocks the route. A first move by the black knight permits Qd6# instead. The main bishop shuttle shows the '
 'clearance mechanism most clearly.',
 "Trace both routes separately: first the queen's horizontal travel b1–g1, then her checking diagonal g1–c5. A "
 'piece can obstruct a route even when it is helping the attack elsewhere. In your games, before choosing a '
 "complicated sacrifice, ask whether one friendly piece simply needs to get out of another's way. The needed "
 'move may be a quiet retreat to an apparently inactive square.'),
    ['Rh1', 'Be8', 'Qb1', 'Bb5', 'Qg1#'],
    ['The d1 rook runs ahead to h1, clearing the queen’s future first-rank route.',
 'The bishop moves to e8 and keeps defensive control in the center.',
 'The queen reaches b1 and threatens Qb4#.',
 'The bishop returns to b5 to meet that threat.',
 'The queen crosses the cleared first rank to g1 and mates along the diagonal to c5.'],
    ('Why put the rook on h1?',
 'To clear the queen’s route while staying beyond g1',
 'The rook must move far enough that the queen can follow.',
 'Because the rook itself will deliver mate',
 'The final checking piece is the queen.'),
    ('What changes after ...Bb5?',
 'Qb4 is defended but Qg1# becomes the finish',
 'Black can answer one threat without stopping the second route.',
 'White has no mating move because b4 is covered',
 'The clearance prepared an alternative queen path.'),
    ('A rook left on an intermediate first-rank square would still obstruct the queen.',
 'Do not confuse the queen’s travel line with her final checking diagonal.')
)

_add(
    'app-three-17',
    'Sacrifice the rook to free a promotion square',
    'J. Møller, 1918',
    384,
    3,
    'R7/P6b/6p1/8/8/8/2p5/k1K5 w - - 0 1',
    ("White's pawn on a7 is ready to promote, but its own rook occupies a8. Black's king on a1 is boxed in by the "
 'white king on c1 and a black pawn on c2. The rook must leave the promotion square in a way that also deals '
 'with the bishop on h7.',
 'Rg8 offers the rook to that bishop. After ...Bxg8, a8=Q+ promotes with check. The sacrifice has cleared a8 '
 "and moved the bishop onto a diagonal from which it must return to interfere with the queen's a-file check. "
 'White gains time through check precisely when the new queen arrives.',
 'Black answers the promotion check with ...Ba2, placing the bishop between a8 and a1. Qh8# then checks along '
 "h8–g7–f6–e5–d4–c3–b2–a1. The bishop's block on a2 cannot stop this diagonal. If Black chooses ...Ka2 instead "
 'of capturing the rook on move one, the source uses Rb8, preserving a different mating setup. The promotion '
 'branch is the main illustration, not the only legal defence.',
 'Practice by asking two separate questions about the rook move: does it free a8, and does it influence '
 "Black's next move? Merely clearing a promotion square is not enough if the defender gets a useful tempo. In "
 'games, promotions with check are especially powerful because the opponent must respond immediately. Always '
 'select the promoted piece explicitly and verify which line gives the check.'),
    ['Rg8', 'Bxg8', 'a8=Q+', 'Ba2', 'Qh8#'],
    ['Clear a8 and offer the rook to the h7 bishop.',
 'The bishop captures on g8, entering the diagonal that will later block the a-file.',
 'Promote to a queen with check down the a-file.',
 'The bishop blocks on a2, the available defence to the promotion check.',
 'The new queen switches to h8 and mates along the long diagonal to a1.'],
    ('What two things does Rg8 achieve?',
 'It clears a8 and draws the bishop to g8',
 'The promotion and the later interference belong to one plan.',
 'It wins Black’s bishop immediately',
 'White offers the rook and then promotes.'),
    ('Why does Qh8# beat the block on a2?',
 'It uses a different checking diagonal',
 'The a2 bishop blocks the file, not h8–a1.',
 'Bishops cannot block queen checks',
 'They can block an appropriate line, as ...Ba2 does.'),
    ('The pawn cannot promote while its own rook occupies a8.', 'The ...Ka2 branch needs a different continuation.')
)

_add(
    'app-three-18',
    'Unpin a pawn so your rook can change files',
    'N. Heeg, 1906',
    384,
    3,
    '5b1k/4pBp1/1P2P3/5pN1/5P1P/P3Qp1R/1B1P4/5K2 w - - 0 1',
    ("The position is crowded, but focus first on the rook's intended route across the third rank. White's own "
 "queen on e3 and Black's pawn on f3 both obstruct its path from h3 to c3. The queen must move away, and the "
 "pawn must leave f3, before the rook can cross. This is clearance involving both sides' pieces.",
 "Qb3 is a quiet queen relocation. Black's ...f2 vacates f3, while White's rook travels from h3 to c3. The "
 'rook does not attack the king yet. Its purpose is to reach the eighth rank by an open file while the black '
 'king remains restricted. The queen move establishes the controls that make this rook transfer work.',
 'In the main line ...g6 is followed by Rc8#. Leaving c3 uncovers the b2 bishop’s long diagonal to h8, which '
 'gives the actual check. The rook on c8 pins the f8 bishop, preventing it from blocking with ...Bg7. White’s '
 'f7 bishop controls g8 and the g5 knight covers h7. The rook’s two jobs are therefore to uncover one bishop '
 'and pin the other.',
 "At your level, reduce the diagram to the traveling rook and the king's nearby squares. Trace h3–c3–c8, "
 'stopping to check whether an occupied square blocks either leg. Then add back the bishops and explain why '
 '...Bg7 cannot legally block the discovered check. A successful rook transfer can uncover an attack while '
 'simultaneously restraining a defender.'),
    ['Qb3', 'f2', 'Rc3', 'g6', 'Rc8#'],
    ['The queen moves to b3 and prepares the rook transfer while preserving the needed net.',
 'The f-pawn advances from f3 to f2, changing the third-rank obstruction.',
 'The rook crosses from h3 to c3 and prepares to enter the eighth rank.',
 'The g-pawn advances; the king remains confined by White’s supporting pieces.',
 'The rook leaves c3 to uncover the b2 bishop’s check, and on c8 it pins the f8 bishop so ...Bg7 cannot block.'],
    ('What is the rook’s route in the source line?',
 'h3–c3–c8',
 'It changes files, then uncovers the b2 bishop while pinning the defender on f8.',
 'h3–h8',
 'The direct file route does not express this construction.'),
    ('What must be checked before a rook transfer works?',
 'Both its travel path and the king’s escape squares',
 'A clear route alone does not establish checkmate.',
 'Only whether the rook reaches the back rank',
 'A back-rank rook check can still allow a legal defence.'),
    ('Do not invent a king pin merely because pieces share a rank.',
 'The quiet rook move Rc3 is preparation; it is not already check.')
)

_add(
    'app-three-19',
    'One queen key supports two different sacrifices',
    'N. Malakhov, 1924',
    384,
    3,
    '1K6/6p1/4ppbp/Q1p2k2/2pp4/b3RNP1/4PN2/8 w - - 0 1',
    ('The black king stands in a dense central formation. White has a queen, rook, and two knights, so several '
 'attractive checks are available. The challenge is to choose a quiet first move that supports the right '
 "second move after the defender changes the position. Pay special attention to Black's f6 and d4 pawns.",
 'Qd8 places the queen on useful lines without checking. After ...Bh7, Re5+ offers the rook to the f6 pawn. '
 "Once ...fxe5 occurs, Nh4# from f3 gives the final knight check. The queen's placement and the other knight "
 "help keep the king inside the net. The rook sacrifice is designed to alter the defender's pawn structure "
 'before the knight arrives.',
 'The source also gives ...Bf7 Nh4+, beginning a different continuation. More surprisingly, after ...dxe3, Qd2 '
 'offers the queen to the pawn now on e3. If ...exd2 follows, e4# is a pawn mate. The same first move supports '
 'both a rook sacrifice and a queen sacrifice, depending on what Black does. These are distinct branches; do '
 'not combine their captures into one imaginary line.',
 'Practice by naming the pawn that captures in each branch: f6 goes to e5 in the main line, while d4 goes to '
 'e3 and then d2 in the other. Update the board after every capture. This is especially valuable when many '
 'pieces cluster around a king, because a single forgotten pawn changes which checks are legal and which '
 'escape squares remain covered.'),
    ['Qd8', 'Bh7', 'Re5+', 'fxe5', 'Nh4#'],
    ['The queen quietly reaches d8, supporting several different attacking continuations.',
 'The bishop chooses h7 and changes the defensive arrangement.',
 'The rook checks from e5 and invites the f6 pawn to capture.',
 'The pawn leaves f6 and captures the offered rook on e5.',
 'The f3 knight jumps to h4 with check and completes the net around f5.'],
    ('What is the purpose of Re5+?',
 'To draw the f6 pawn onto e5 before the knight mate',
 'The rook is sacrificed to change the king’s surrounding position.',
 'To win the bishop on h7',
 'The main line does not capture that bishop.'),
    ('Does the ...dxe3 branch use the same sacrifice?',
 'No; Qd2 offers the queen before e4#',
 'The first move prepares more than one mechanism.',
 'Yes; Re5+ must always be played',
 'Different defensive pawn moves require different replies.'),
    ('The final main-line move is Nh4#, not Qh4.', 'Reset between branches so captured pieces do not reappear.')
)

_add(
    'app-three-20',
    'Promotions change which piece must finish',
    'S. Kriuchkov, 1927; developing Galitsky’s theme',
    385,
    3,
    '8/1p6/8/7K/p4pQN/5B2/4pp2/2b2k2 w - - 0 1',
    ("Black has two pawns on the second rank, a bishop on c1, and a king on f1. White's queen and knight are "
 'active near the kingside, but the bishop on f3 needs a new role. Promotion is an immediate defensive '
 'resource, so the attacking plan must distinguish the type of piece Black creates.',
 'Bc6 offers the bishop to the b7 pawn. After ...bxc6, Nf3 moves the knight from h4 and threatens Qh3#. Black '
 'can promote the e2 pawn to a queen, but that changes the position in a way that permits Nh2#. The knight '
 'travels h4–f3–h2, and its final check attacks f1. The queen remains on g4 throughout this main line.',
 'An immediate ...e1=Q after the key is answered by Bg2+, while immediate knight promotion is answered by '
 'Bb5+. If Black moves the king to e1 instead, Nf3+ drives it toward d1 and Bxa4# finishes. These alternatives '
 "matter because a queen, knight, and king create different checks and obstructions. The source's branching "
 'solution is a lesson in responding to the actual promoted piece.',
 'Practice the bishop-sacrifice branch first, then repeat with Black promoting immediately. Announce the '
 "promoted piece before choosing White's move. This prevents a common beginner error: assuming all promotions "
 'act like queens. Also distinguish a threat from a check. Nf3 is quiet in the main line and threatens Qh3; '
 'the later Nh2 is the move that actually checks and mates.'),
    ['Bc6', 'bxc6', 'Nf3', 'e1=Q', 'Nh2#'],
    ['Offer the bishop on c6 and prepare different answers to captures and promotions.',
 'The b7 pawn captures the bishop and changes the queenside structure.',
 'The knight moves to f3, threatening a queen mate on h3.',
 'Black promotes the e-pawn to a queen, trying to gain defensive power.',
 'The knight checks from h2 and mates the king on f1; the promoted queen cannot save it.'],
    ('Which white piece moves to f3 after ...bxc6?',
 'The knight from h4',
 'Nf3 threatens Qh3# while keeping a knight finish available.',
 'The queen from g4',
 'The queen stays on g4 in the main line.'),
    ('Why study queen and knight promotions separately?',
 'They attack different squares and need different replies',
 'The source uses Bg2+ against a queen and Bb5+ against a knight.',
 'All promoted pieces move like queens for one turn',
 'A promoted piece immediately uses its own normal movement.'),
    ('Do not confuse the quiet threat Nf3 with the later checking move Nh2#.',
 'An immediate promotion is a separate branch from ...bxc6.')
)

_add(
    'app-more-01',
    'A rook sacrifice sets up a knight capture mate',
    'A. Petrov, 1845',
    385,
    5,
    'R7/3p1K1k/6p1/5n1p/3bN2P/8/8/8 w - - 0 1',
    ("White has a rook and knight near the black king, while Black's bishop and knight defend a compact kingside "
 'position. The five-move task is longer than the preceding problems, but much of the route is forced. Start '
 "with the king's legal responses to a knight check, then follow the jobs of the two black defenders.",
 "Ng5+ forces ...Kh6. Rh8+ then offers the rook to the bishop on d4, which captures along e5–f6–g7–h8. White's "
 'king follows with Kg8. The rook sacrifice has placed the bishop on a square the white king can later '
 'capture. White is building a knight mate and using the king actively; there is no need to preserve the rook '
 'once its forcing job is done.',
 "The source continues ...Nd6 Kxh8 Nf7+ Nxf7#. Black's knight checks White's king on h8, but White's knight "
 'captures that checker and simultaneously attacks the black king on h6. The h4 pawn controls g5, and the '
 'white king restricts g7. Check each capture on the board: the bishop vanishes on h8, then the black knight '
 "vanishes on f7. Black's last check creates the final capture square.",
 'Work through this in two stages: first the rook-and-bishop exchange, then the knight finish. Before the last '
 'move, ask how White can answer the check on h8. Capturing a checker is especially valuable when the '
 "capturing piece also gives mate. In games, calculate beyond an opponent's check rather than assuming it "
 'refutes your attack; the check must be strong enough to change the outcome.'),
    ['Ng5+', 'Kh6', 'Rh8+', 'Bxh8', 'Kg8', 'Nd6', 'Kxh8', 'Nf7+', 'Nxf7#'],
    ['Check from g5 and restrict the black king’s destination.',
 'The king is forced to h6.',
 'Offer the rook on h8 with check.',
 'The bishop takes the rook and is drawn onto h8.',
 'Bring the king to g8, preparing to remove that bishop.',
 'The black knight moves to d6, preparing its defensive check.',
 'The king captures the bishop on h8.',
 'The knight checks from f7, trying to gain a tempo.',
 'The white knight captures the checker and mates the king on h6.'],
    ('Why sacrifice the rook on h8?',
 'To draw the bishop onto the king’s capture square',
 'The rook forces the defender into a position useful for the later knight mate.',
 'To exchange equal-valued pieces',
 'The material count is secondary to the forcing net.'),
    ('How does White answer ...Nf7+?',
 'Nxf7# captures the checker and mates',
 'The answer to a check can itself be checkmate.',
 'White must move the king',
 'Capturing a checker is also a legal response when it removes the check.'),
    ('Do not stop calculating when Black gives check.', 'After Kxh8 the black bishop is gone; it cannot defend f7.')
)

_add(
    'app-more-02',
    'Two heavy-piece sacrifices create a smothered mate',
    'J. Kling, 1850',
    385,
    4,
    'r4q1k/7p/n6N/B2Q4/bR6/8/8/K7 w - - 0 1',
    ("The black king sits on h8 with a pawn on h7 and a rook on a8. White's knight on h6 is close to a familiar "
 'mating square, f7, but the defenders must first be rearranged. The queen, rook, and bishop are the tools '
 'used to produce the final confinement.',
 'Rb8 sacrifices the rook along the eighth rank. After ...Rxb8, Bc3+ checks the king on the long diagonal '
 'c3–d4–e5–f6–g7–h8. Black blocks with ...Qg7. White then plays Qg8+, offering a second heavy piece. Each '
 'check or threat moves a defender closer to its own king, turning defensive pieces into obstacles.',
 'After ...Rxg8, Nf7# attacks h8. The king cannot capture its own rook on g8 or pawn on h7, and the queen on '
 'g7 fills another nearby square. A knight check cannot be blocked, so the rook and queen cannot interpose. '
 "The black king's defenders now form its prison. Verify that the f7 knight itself cannot be captured legally "
 'before calling this smothered mate.',
 'Set up the final position first and count the occupied squares around h8. Then reverse the sacrifices and '
 'explain how each defender reached its blocking square. This is an accessible way to study a long '
 'combination: find the final pattern and reconstruct the forced arrivals. In games, look for smothered mates '
 'when the enemy king has little room and your knight can reach a checking square.'),
    ['Rb8', 'Rxb8', 'Bc3+', 'Qg7', 'Qg8+', 'Rxg8', 'Nf7#'],
    ['Offer the rook on b8, drawing Black’s rook away from a8.',
 'Black captures and puts its rook on b8.',
 'The bishop checks along the diagonal to h8.',
 'The queen blocks on g7, occupying a flight square beside the king.',
 'Offer the queen with check on g8.',
 'The rook captures and blocks g8 beside its own king.',
 'The knight checks from f7; the king is smothered by its own pieces.'],
    ('What do the sacrifices do to Black’s defenders?',
 'They turn them into blockers around their own king',
 'The final knight mate depends on occupied escape squares.',
 'They remove every black piece',
 'Several black pieces remain and help trap the king.'),
    ('Can Black block the final knight check?',
 'No; a knight check cannot be interposed against',
 'The defender must capture the knight or move the king, and neither works.',
 'Yes; the queen can stand between f7 and h8',
 'A knight jumps, so there is no intervening line to block.'),
    ('Smothered mate depends on the exact squares occupied around the king.',
 'The rook sacrifice comes before the bishop check.')
)

_add(
    'app-more-03',
    'A pawn ending becomes a four-move mate',
    'A. Galitsky, 1900',
    385,
    4,
    '8/8/6pp/6pk/7P/6K1/7P/8 w - - 0 1',
    ('Only kings and pawns remain. White has two h-pawns, an unusual arrangement that can arise after captures. '
 'The black king on h5 is hemmed in by its own pawns. Do not dismiss a pawn-only position as harmless: a small '
 'change in pawn squares can create a complete mating net.',
 'h3 moves the rear pawn from h2, leaving the h4 pawn available for capture. Black must play ...gxh4+, which '
 "gives check to the white king on g3. Kf4 answers the check and begins the king's approach. The black pawn's "
 'capture is useful to White because it changes which squares the black king can use and clears the g-file '
 "pawn's old square.",
 'Black continues ...g5+, and Kf5 again steps forward while legally answering check. After ...g4, hxg4# '
 'captures with the pawn that originally stood on h2. The new pawn on g4 attacks h5. The white king on f5 '
 "controls g4, g5, and g6, while Black's own pawns occupy h4 and h6. The king is boxed in by both friendly and "
 'enemy units.',
 'Track the two white h-pawns separately. One is sacrificed on h4; the other moves h2–h3–g4 and gives mate. '
 'This is excellent practice in avoiding a common calculation error: mentally moving the wrong pawn after a '
 'capture. In endgames, king activity and precise pawn timing can matter more than a simple pawn count. Check '
 "the king's legal route after every pawn check."),
    ['h3', 'gxh4+', 'Kf4', 'g5+', 'Kf5', 'g4', 'hxg4#'],
    ['Advance the rear h-pawn one square and preserve the intended capture on h4.',
 'Black captures the front h-pawn with check.',
 'The king answers check by moving to f4.',
 'The remaining g-pawn advances with another check.',
 'The king moves to f5 and controls key g-file escape squares.',
 'The pawn advances to g4, entering the rear h-pawn’s capture square.',
 'The h3 pawn captures on g4 and gives mate to the king on h5.'],
    ('Which white pawn delivers mate?',
 'The pawn that began on h2',
 'It moves to h3 and then captures on g4.',
 'The pawn that began on h4',
 'That pawn was captured on Black’s first move.'),
    ('Why is Kf5 important?',
 'It controls the king’s escape squares on the g-file',
 'The final pawn check needs the king’s support.',
 'It promotes the pawn automatically',
 'Promotion occurs only when a pawn reaches its last rank.'),
    ('Keep the two h-pawns distinct throughout the calculation.',
 'Black’s checking moves do not prevent the white king from advancing legally.')
)

_add(
    'app-more-04',
    'Sacrifice a bishop to bring the king into the net',
    'A. Anderssen, 1842',
    385,
    4,
    '3BB2K/7p/7k/8/8/5P1p/7P/8 w - - 0 1',
    ("White has two bishops, two pawns, and a king close to Black's king. Black's own h-pawns restrict its "
 'movement. The bishops operate on opposite colors, so identify which one can reach h5. The task is to lure '
 "the black king forward, then use White's king to complete a discovered mating net.",
 "Bh5 offers the e8 bishop on h5. Black's king captures it, and White plays Kg7. The remaining bishop on d8 "
 "still controls an important diagonal. White's king must approach by the correct route, preserving the "
 'supporting squares without allowing the black king to escape. The sacrificed bishop has bought a precise '
 'king destination, not material compensation.',
 'After ...h6, Kf6 is the quiet but essential next step. Black is forced to ...Kh4, and Kg6# follows. The '
 "king's move opens the d8 bishop's diagonal through e7–f6–g5–h4: the bishop supplies the check, while White's "
 'king controls g5 and h5. Thus a king move is marked as mate even though kings may never move next to one '
 'another to give direct check.',
 "Pause before Kg6 and trace the bishop's blocked line. Then move the king off f6 and observe the discovered "
 "check. This is a useful correction to a beginner's habit of looking only at the piece that moved. A quiet "
 'king move can reveal an attack by another piece. In games, always inspect which lines your own king is '
 'blocking before moving it in a tactical ending.'),
    ['Bh5', 'Kxh5', 'Kg7', 'h6', 'Kf6', 'Kh4', 'Kg6#'],
    ['Offer the e8 bishop on h5 to lure the black king forward.',
 'The king captures the offered bishop.',
 'White’s king approaches via g7 while preserving the net.',
 'The h-pawn advances, occupying another square near its king.',
 'The king moves to f6, temporarily blocking its own bishop’s diagonal.',
 'The black king is forced to h4.',
 'The king leaves f6 for g6, uncovering the d8 bishop’s mating diagonal.'],
    ('Which piece gives check after Kg6#?',
 'The bishop on d8',
 'The king vacates f6 and opens the diagonal to h4.',
 'White’s king directly attacks h4',
 'Kings cannot attack each other directly in a legal position.'),
    ('Why give up the bishop on h5?',
 'To draw the black king into the planned route',
 'The lure enables White’s king and remaining bishop to form the net.',
 'Because bishops are worthless in endings',
 'The remaining bishop delivers the final check.'),
    ('The final check is discovered, not a direct king check.',
 'Kf6 is preparation for opening the bishop’s diagonal next move.')
)

_add(
    'app-more-05',
    'Give up a rook to force the final pawn capture',
    'P. Homma, 1939',
    386,
    4,
    '8/2BR4/4p3/8/4k1P1/5p2/2PK1P2/8 w - - 0 1',
    ("White's rook is active on d7, but the final mating unit will be a pawn. Black's king on e4 is restricted by "
 "White's bishop, pawns, and king. The black e6 pawn can still move, giving the defender spare time. White's "
 'king must reach the correct square before that pawn is forced into a useful capture.',
 'Kc3 prepares to meet ...e5 with Rd4+. The rook checks and offers itself to the e5 pawn. After ...exd4+, '
 "White's king moves to c4. The exchange is deliberately unfavorable in material: White gives up a rook to "
 "bring a black pawn onto the d-file and make it advance into the c2 pawn's capture square.",
 "Black must continue ...d3, after which cxd3# checks the king on e4. The pawn on d3 attacks e4, and White's "
 'king on c4 controls d3, d4, and d5. The bishop on c7 and the other pawns deny the remaining flights. The '
 'black f3 pawn stays on the board as part of the confinement. Removing that pawn in your mental picture would '
 'change the mating geometry.',
 "Follow the black pawn's full journey e6–e5–d4–d3 before following White's c-pawn. This makes the rook "
 'sacrifice easier to understand: it is a way to place a target, not an attempt to win material. In practical '
 'play, a sacrifice can force a pawn to leave a defensive line or create a new capture. Always verify that '
 'your king can safely answer any check produced by the capture.'),
    ['Kc3', 'e5', 'Rd4+', 'exd4+', 'Kc4', 'd3', 'cxd3#'],
    ['The king moves to c3, preparing the rook sacrifice and the later approach.',
 'The e-pawn advances and becomes available for the forced capture.',
 'The rook checks from d4 and offers itself to the pawn.',
 'The pawn captures the rook with check, changing from the e-file to the d-file.',
 'The king answers check on c4 and controls the final net’s central squares.',
 'The pawn advances to d3, where White’s c-pawn can capture it.',
 'The c2 pawn captures on d3 with check and mate.'],
    ('Why sacrifice the rook on d4?',
 'To bring the e-pawn onto the d-file',
 'The pawn must reach d3 for White’s final c-pawn capture.',
 'To promote the rook',
 'Rooks do not promote; the sacrifice is about pawn placement.'),
    ('What makes cxd3 a checking move?',
 'A white pawn on d3 attacks e4',
 'The black king stands on one of the pawn’s two attacking squares.',
 'Pawns attack straight ahead',
 'Pawns move forward but capture and attack diagonally.'),
    ('The rook capture gives check; Kc4 must answer it legally.', 'Keep the black f3 pawn in the final position.')
)

_add(
    'app-more-06',
    'Use the opponent’s spare pawn moves to redeploy king and rook',
    'S. Loyd, 1859',
    386,
    5,
    '8/8/8/p7/8/8/R6p/2K2Rbk w - - 0 1',
    ('The black king on h1 is trapped by its own bishop and pawn. The a5 pawn is far away, but its available moves '
 'determine the timing. White has two rooks and must move them with precise identities: one begins on a2, the '
 'other on f1. Rook notation will distinguish them when either could reach f2.',
 "Raf2 moves the a2 rook to f2. After ...a4, Kd2 clears c1 and prepares the king's return to e1. Black spends "
 'another pawn move with ...a3, and Ra1 transfers the original f1 rook to a1. That rook blocks the advancing '
 "a-pawn's eventual promotion square and opens the f-file arrangement needed for the final discovered mate.",
 'After ...a2, Ke1 leaves Black with ...Bxf2+. Kxf2# captures the bishop and vacates e1, uncovering the a1 '
 "rook's line along the first rank to h1. The black a-pawn cannot advance because a1 is occupied. Its earlier "
 'spare moves have run out. The apparent king capture mate is really a discovered rook check, with the king '
 'helping restrict g1 and g2.',
 'Replay while naming each rook by its starting square. This prevents accidentally moving the f2 rook back to '
 "a1. Then count Black's useful waiting moves before and after ...a2. In endgames, a distant pawn can decide a "
 'local zugzwang by supplying or exhausting spare moves. The exact timing matters even when that pawn never '
 'reaches the fight around the king.'),
    ['Raf2', 'a4', 'Kd2', 'a3', 'Ra1', 'a2', 'Ke1', 'Bxf2+', 'Kxf2#'],
    ['The a2 rook goes to f2; the notation identifies which rook moves.',
 'The distant pawn spends one available move.',
 'The king leaves c1 so the other rook can later cross the first rank.',
 'The pawn spends another move, reaching a3.',
 'The f1 rook reaches a1, blocking the pawn’s eventual promotion square.',
 'The pawn reaches a2 and has no further advance.',
 'The king reaches e1 and leaves Black the forced bishop capture.',
 'The bishop captures on f2 with check.',
 'The king captures the bishop and vacates e1, opening the a1 rook’s mating line.'],
    ('Why is Ra1 played before the a-pawn promotes?',
 'To occupy and block the promotion square',
 'The pawn’s spare moves then run out.',
 'To capture the pawn immediately',
 'The pawn remains on a2 in the final position.'),
    ('Which piece gives check after Kxf2#?',
 'The rook on a1',
 'The king leaves e1 and uncovers the first rank.',
 'The capturing king directly attacks h1',
 'A king on f2 does not directly attack h1.'),
    ('Raf2 uses the a2 rook; Ra1 later uses the rook that began on f1.',
 'The a2 pawn cannot advance onto the occupied a1 square.')
)

_add(
    'app-more-07',
    'Force a bishop to block, then leave the block behind',
    'S. Loyd, 1877',
    386,
    4,
    '8/8/7K/4P2p/6bk/7p/5R1P/B7 w - - 0 1',
    ("The black king is boxed in on h4 by pawns and White's nearby king. Its bishop on g4 is an active defender. "
 "White's rook and bishop must coordinate without loosening the net. The e5 pawn and h2 pawn are not "
 "decoration; they help restrict the king's options during the maneuver.",
 "Rb2 prepares a rook check from b4. Black's bishop can make several moves; the source illustrates ...Be2. "
 'Rb4+ then checks across the fourth rank, compelling ...Bg4 to block beside the king. White has used a check '
 'to force the defender back to a known square. Now Bd4 places the white bishop where Bf2 will give the '
 'finishing check.',
 'Black must move the bishop again, and Bf2# follows. In the shown line it returns to e2, but the precise '
 "destination is not the main mechanism. Once the defender leaves g4, White's bishop checks along f2–g3–h4, "
 'and the rook on b4 helps keep the king confined. Black cannot keep a useful block on every relevant line at '
 'once.',
 'Study the sequence as a change in duties: the black bishop first moves freely, then is forced to block, then '
 'cannot maintain the whole defence. In games, this is a useful way to recognize overloaded defenders. A piece '
 'may appear to guard many squares, but a forcing check can make it abandon one duty. Name the duty it loses '
 'before deciding that a sacrifice or quiet move works.'),
    ['Rb2', 'Be2', 'Rb4+', 'Bg4', 'Bd4', 'Be2', 'Bf2#'],
    ['The rook prepares to check along the fourth rank.',
 'The bishop chooses e2 as an illustrative waiting move.',
 'The rook checks from b4 and forces the defender to interpose.',
 'The bishop blocks on g4 beside its king.',
 'The white bishop reaches d4, preparing Bf2#.',
 'Black moves the bishop again and cannot preserve the needed defence.',
 'The bishop checks from f2 and completes the net with the rook and king.'],
    ('What does Rb4+ force?',
 'The bishop block ...Bg4',
 'The checking line fixes the defender on a known square.',
 'The immediate capture of the black king',
 'Kings are never captured; mate is established by legal restrictions.'),
    ('Why does Bd4 help?',
 'It prepares Bf2# while Black must move',
 'The white bishop changes diagonal to complete the net.',
 'It gives check immediately',
 'Bd4 is a quiet preparatory move in the shown line.'),
    ('Do not label Bd4 as a check.', 'The bishop’s first waiting move can vary; identify the shared forced block.')
)

_add(
    'app-more-08',
    'A knight makes a round trip and draws the king forward',
    'P. Orlimont, 1939',
    386,
    4,
    '8/8/4p3/4P3/8/1p2p1p1/pP2Q1pk/K3N2b w - - 0 1',
    ("White's king is confined on a1, far from Black's king on h2. The queen on e2 and knight on e1 must do the "
 "attacking work. Black's pawns heavily restrict its own king, but they also make the position look dangerous "
 "for White. Focus on the knight's route and the king squares it controls.",
 "Nd3 begins the maneuver. Black's strongest delaying reply is ...Kg1; other moves allow a quicker mate. Nf4 "
 'then forces the king back toward h2. The knight is not merely checking at every opportunity. It uses quiet '
 "moves to control the right squares and prepare a sacrifice that changes the black king's location.",
 'After ...Kh2, Nh3 offers the knight. The king captures with ...Kxh3, and Qh5# checks down the h-file. The '
 "queen controls h2, h4, and g4, while Black's own pawns occupy g2 and g3. Those are all the neighboring "
 'squares available to a king on h3. The important final change is that the king has been drawn from h2 to h3, '
 'where the queen can finish.',
 'Draw the knight route e1–d3–f4–h3 and check each L-shaped jump. Then replay without looking at the move '
 'list, explaining what each destination achieves. This trains quiet calculation and piece routing. In your '
 'games, a knight may need several moves to reach a decisive square, but that is only feasible if the '
 "opponent's replies are constrained enough to give you the time."),
    ['Nd3', 'Kg1', 'Nf4', 'Kh2', 'Nh3', 'Kxh3', 'Qh5#'],
    ['The knight begins its route to d3 and creates a mating threat.',
 'The king chooses g1, the delaying defence.',
 'The knight reaches f4 and changes the available king squares.',
 'The king returns to h2.',
 'Offer the knight on h3 to draw the king forward.',
 'The king captures the knight on h3.',
 'The queen checks from h5 and mates the exposed king.'],
    ('Why is the knight sacrificed on h3?',
 'To draw the king onto the queen’s mating line',
 'The final queen move works after the king changes squares.',
 'To promote the knight into a queen',
 'Knights do not promote.'),
    ('Must every move in a forcing combination give check?',
 'No; quiet moves can create unavoidable threats',
 'Nd3, Nf4, and Nh3 organize the net without continuous checks.',
 'Yes; a quiet move lets Black do anything',
 'Black’s legal replies may still be tightly restricted.'),
    ('Count knight jumps exactly; they do not slide along a diagonal.',
 'The queen mates after the king captures, not before the knight reaches h3.')
)

_add(
    'app-more-09',
    'Clear the diagonal before a chain of rook sacrifices',
    'E. Zepler, 1936',
    386,
    5,
    '3r3k/R4P1p/3p1K1N/4P3/8/1qp3R1/8/8 w - - 0 1',
    ("White's f7 pawn is close to promotion and the knight on h6 eyes f7. Black's rook on d8 and queen on b3 "
 'defend the king. White has two rooks, but the attack depends on their order of sacrifice and on the e5 pawn '
 'moving out of a diagonal. Start by imagining the final knight on f7.',
 "Ra8 offers the a7 rook. After ...Rxa8, e6 is the essential quiet move: the pawn blocks the black queen's "
 'diagonal b3–c4–d5–e6–f7, preventing her from capturing a future mating knight on f7. White also threatens '
 'Rg8+. White must not rush the second rook sacrifice before this pawn move. The position after a capture is a '
 'new calculation, not an automatic continuation.',
 'In the source line Black defends with ...Qb8. Rg8+ Qxg8 fxg8=Q+ Rxg8 Nf7# follows. The new white queen is '
 'sacrificed immediately, forcing the rook to g8 and smothering its king. Black can resist differently, '
 'including ...Qxe6+ after e6; White then captures with the king and uses a different mating continuation. The '
 'displayed chain illustrates the source theme without pretending that every black reply is identical.',
 'Track the f-pawn through promotion and remove the promoted queen when the rook captures it. Then examine the '
 'final knight check: the rook on g8 and pawn on h7 block their own king. In games, a promotion is sometimes a '
 'forcing intermediate step rather than a permanent material gain. Look for what the promotion check compels '
 'before celebrating the new queen.'),
    ['Ra8', 'Rxa8', 'e6', 'Qb8', 'Rg8+', 'Qxg8', 'fxg8=Q+', 'Rxg8', 'Nf7#'],
    ['Offer the a7 rook on a8 and pull Black’s rook away from d8.',
 'Black captures and places its rook on a8.',
 'Advance e6 before the next sacrifice; the new position threatens Rg8+.',
 'The queen comes to b8 to defend along the eighth rank.',
 'Sacrifice the second rook with check on g8.',
 'The queen captures the rook and occupies g8.',
 'The pawn captures the queen and promotes with check.',
 'Black’s rook captures the new queen and blocks g8.',
 'The knight jumps to f7 and delivers the smothered mate.'],
    ('Why is the new queen on g8 allowed to be captured?',
 'Its checking arrival forces the rook onto a blocking square',
 'The final objective is the knight mate, not keeping a queen.',
 'A promoted queen has no value',
 'It has normal queen power, which creates the forcing check.'),
    ('What is the final mating piece?',
 'The knight from h6',
 'Nf7# attacks h8 while Black’s own pieces block escapes.',
 'The pawn that promoted',
 'That pawn became a queen and was then captured.'),
    ('Do not omit the quiet e6 move from the sequence.',
 'The ...Qxe6+ defence requires its own continuation, rather than the displayed promotion chain.')
)

_add(
    'app-more-10',
    'Retreat a bishop step by step to distract a rook',
    'H. Hindre, 1952',
    386,
    6,
    'k1K5/p1b4p/p6r/1B6/8/1P6/7B/8 w - - 0 1',
    ("White's king on c8 restricts the black king on a8, and the bishop on b5 would like to capture a6 before "
 "mating on b7. The black rook on h6 can interfere. White's other bishop on h2 is a potential target for that "
 'rook. This six-move problem is about arranging where the defender stands before the final bishop attack.',
 'Bc4 begins a measured retreat: after ...Rh5, Bd3, then ...Rh4, Be2, then ...Rh3, Bf1. The bishop travels one '
 'square at a time rather than jumping directly to f1. Each move induces a corresponding rook move. The source '
 'warns that immediate Bf1 permits ...Rg6, and that an early Bxa6 after ...Rh5 permits ...Rb5, keeping a '
 'useful defence against the b7 mate.',
 'After Bf1, the source illustrates ...Rxh2, taking the second bishop. Now Bxa6 removes the a6 pawn and '
 'threatens Bb7#. Black can spend a move with ...h6, but Bb7# follows. The rook has been drawn away from the '
 'useful defensive rank. Other rook replies require their own mating continuation; the stepwise retreat is '
 'what preserves the six-move solution against resistance.',
 'Compare the tempting shortcut with the full retreat using the actual board. Ask where the rook would stand '
 'when White finally captures a6. This is a useful introduction to timing: the same white move can succeed or '
 "fail depending on the defender's square. In games, do not call a sequence a waste of time until you have "
 'checked whether it forces an opposing piece onto a worse line.'),
    ['Bc4', 'Rh5', 'Bd3', 'Rh4', 'Be2', 'Rh3', 'Bf1', 'Rxh2', 'Bxa6', 'h6', 'Bb7#'],
    ['Begin the bishop’s staged retreat instead of jumping directly to f1.',
 'The rook moves to h5, retaining a potential fifth-rank defence.',
 'Continue to d3 and make the rook adjust again.',
 'The rook reaches h4.',
 'Retreat to e2, preserving the intended timing.',
 'The rook reaches h3 near the h2 bishop.',
 'Complete the bishop’s route to f1.',
 'Black captures the h2 bishop and leaves the useful defensive ranks.',
 'The remaining bishop captures a6 and threatens Bb7#.',
 'The pawn move cannot prevent the mating threat.',
 'The bishop checks from b7, supported by the king on c8, and mates.'],
    ('Why not rush Bxa6 after ...Rh5?',
 'The rook can defend with ...Rb5',
 'The defender’s rank determines whether the b7 finish works.',
 'Bishops cannot capture backward',
 'Bishops can move in either direction along clear diagonals.'),
    ('What is the point of the staged retreat?',
 'To make the rook change squares before the final attack',
 'The sequence changes the defender’s geometry, not just White’s bishop position.',
 'To repeat moves until Black agrees to lose',
 'The solution relies on concrete threats and defences.'),
    ('The rook’s destination matters more than how many squares the bishop retreats.',
 'After ...Rxh2, remove the captured bishop before continuing.')
)

_add(
    'app-more-11',
    'A seventeen-move king walk with two published finishes',
    'A. Guliaev, 1950; alternative by A. Studenetsky, 1953',
    387,
    17,
    '6K1/1p6/4B3/2R5/8/pp4P1/pk6/b7 w - - 0 1',
    ('This is a guided long composition, not an expectation that a beginner calculate seventeen moves unaided. '
 "White's king starts far from the trapped black king. The rook and bishop can keep the defender confined "
 'while the king travels across the board. The source line and its acknowledged alternative are both shown; '
 'the lesson does not claim a unique solution.',
 'Kh7 begins the source plan. After ...b6, Rc6 ...b5, Kh6 ...b4, Bg8 brings the bishop toward h7. Then ...Kb1 '
 "Bh7+ forces ...Kb2. The bishop can now check along h7–g6–f5–e4–d3–c2–b1. White's king repeatedly blocks this "
 'diagonal and steps off it again, allowing Black to shuttle between b1 and b2 while White advances safely.',
 "The king route is g6, g5, f5, f4, e4, e3, d3, d2. Moves onto the diagonal stop the bishop's check; moves off "
 'it uncover check again. After the king reaches d2, Rg6 temporarily blocks the same diagonal. Rd6+ then '
 'moves the rook off g6, uncovering the bishop’s check on b1; Rd3 blocks the diagonal again before Rxb3#. The '
 'alternative Rg4+ also uncovers a bishop check, then Bc2 allows ...bxc2 and Rxb4#. Both lines are legal mates in seventeen; the '
 'long illustrated branch alone is not an exhaustive proof against every earlier black deviation.',
 'Study one cycle first: king blocks the bishop, Black moves to b1, king uncovers check, Black returns to b2. '
 'Then repeat that idea as the king approaches. The practical skill is keeping a stable constraint while '
 "improving your worst-placed piece. The source's long move count and alternative finish should encourage "
 'patient analysis, not the belief that one memorized sequence is the only possible way to win.'),
    ['Kh7',
 'b6',
 'Rc6',
 'b5',
 'Kh6',
 'b4',
 'Bg8',
 'Kb1',
 'Bh7+',
 'Kb2',
 'Kg6',
 'Kb1',
 'Kg5+',
 'Kb2',
 'Kf5',
 'Kb1',
 'Kf4+',
 'Kb2',
 'Ke4',
 'Kb1',
 'Ke3+',
 'Kb2',
 'Kd3',
 'Kb1',
 'Kd2+',
 'Kb2',
 'Rg6',
 'Kb1',
 'Rd6+',
 'Kb2',
 'Rd3',
 'Kb1',
 'Rxb3#'],
    ['The king begins its approach on h7.',
 'The b-pawn supplies a waiting move.',
 'The rook reaches c6, maintaining the confinement.',
 'The b-pawn advances again.',
 'The king moves to h6, preparing the bishop maneuver.',
 'The pawn reaches b4 and has used its forward moves in this line.',
 'The bishop heads for h7 via g8.',
 'The black king moves to b1.',
 'The bishop checks along the long diagonal from h7.',
 'The king returns to b2.',
 'White’s king blocks the bishop’s diagonal on g6.',
 'With the diagonal blocked, the king can return to b1.',
 'The king steps off the diagonal on g5, uncovering check.',
 'The king must return to b2 in this cycle.',
 'The king blocks the diagonal on f5, one stage nearer the queenside.',
 'The king returns to b1.',
 'The king steps off on f4, uncovering bishop check.',
 'The king returns to b2.',
 'The king blocks the diagonal on e4.',
 'The king returns to b1.',
 'The king steps off on e3, uncovering check.',
 'The king returns to b2.',
 'The king blocks the diagonal on d3, close to its destination.',
 'The king returns to b1.',
 'The king reaches d2 and uncovers the bishop check again.',
 'The king returns to b2.',
 'The rook blocks the bishop’s diagonal on g6, allowing ...Kb1 and preparing the finishing maneuver.',
 'The king returns to b1.',
 'Rd6+ vacates g6, uncovering the h7 bishop’s check on b1. The rook itself does not check the king.',
 'The king returns to b2.',
 'Rd3 blocks the bishop’s diagonal again, allowing ...Kb1 before the rook captures b3 across the third rank.',
 'The king returns to b1.',
 'The rook captures b3 and checks down the b-file; White’s king and bishop complete the mate.'],
    ('What repeats during the king walk?',
 'The king blocks and then uncovers the bishop’s diagonal',
 'This keeps Black’s king shuttling while White improves its king.',
 'The king gives direct checks to the other king',
 'The bishop gives the discovered checks; the kings stay legally separated.'),
    ('Does the book claim only one finish?',
 'No; it records an alternative finishing plan',
 'The alternative Rg4+ and Bc2 ends with Rxb4#.',
 'Yes; every long composition has a unique continuation',
 'The source explicitly acknowledges another solution.'),
    ('Do not treat a demonstrated long branch as an exhaustive proof of every alternative.',
 'A move onto the bishop’s diagonal blocks its check; a move off that line uncovers it.')
)

_add(
    'app-more-12',
    'Walk away from checks to prepare a queen sacrifice',
    'P. Orlimont, 1906',
    387,
    4,
    '6b1/8/8/8/3p2N1/2pQpB2/6r1/4KNrk w - - 0 1',
    ("Black's king is trapped on h1 behind rooks, while White's queen and two knights are ready to attack. Black "
 'also has dangerous advanced pawns and a bishop on g8. The white king on e1 must choose a route that answers '
 "the defender's checks without disrupting the mating pieces.",
 'Kd1 is the quiet key. It allows ...Bb3+, a long bishop check, but Kc1 steps out of it. After ...Bc2, Qd1 '
 "offers the queen on the bishop's diagonal. The purpose is to draw the bishop to d1 and make the knight jump "
 "to g3 decisive. White's king has deliberately moved away from the squares where the sacrifice and check will "
 'occur.',
 'After ...Bxd1, Ng3# checks the king on h1. The knight from f1 is the mating piece; the knight on g4 and '
 "bishop on f3 help restrict the net. Black's rooks occupy g1 and g2 and cannot block a knight check. The "
 'source also considers immediate ...c2+ after Kd1, answered by Kc1, and ...e2+, answered by Qxe2. Each '
 'checking pawn move must be answered on its own terms.',
 'Play the main line while naming the piece giving every check. Then reset and test the two pawn checks. This '
 'trains disciplined calculation under pressure: first ensure your own king is safe, then continue the attack. '
 'A powerful queen can be sacrificed if the remaining pieces already control the relevant squares. Do not '
 'evaluate Qd1 solely by the material it offers.'),
    ['Kd1', 'Bb3+', 'Kc1', 'Bc2', 'Qd1', 'Bxd1', 'Ng3#'],
    ['The king moves to d1, inviting the defender’s checking attempts.',
 'The bishop checks along b3–c2–d1.',
 'The king steps to c1 and keeps the attacking pieces in place.',
 'The bishop reaches c2, approaching the queen’s planned sacrifice square.',
 'Offer the queen on d1 to the bishop.',
 'The bishop captures the queen and is drawn onto d1.',
 'The f1 knight jumps to g3, checking h1 and delivering mate.'],
    ('Why does the king travel to c1?',
 'To answer checks while preserving the attacking arrangement',
 'The king gets clear before the queen sacrifice and knight finish.',
 'To castle with a rook on the kingside',
 'This is an ordinary king walk, not castling.'),
    ('Why can the rooks not block Ng3#?',
 'A knight check cannot be blocked',
 'Their own occupied squares also confine the king.',
 'A rook is never allowed to defend a king',
 'Rooks can defend, but no legal defence works here.'),
    ('The f1 knight, not the g4 knight, gives the final check.',
 'Do not apply the bishop-check continuation blindly to a pawn check.')
)

_add(
    'app-more-13',
    'A pawn staircase ends in knight underpromotion',
    'L. Kubbel, 1939',
    387,
    7,
    '7b/Kp4q1/1p2bp1n/p1B2pp1/7p/5r1k/6RP/7Q w - - 0 1',
    ("White's h2 pawn faces a remarkable row of possible captures. Black's king is on h3, with many defenders "
 'nearby. The queen on h1 and rook on g2 are restricted by their own pawn. The seven-move task is to make that '
 'pawn travel diagonally up the board, repeatedly opening checking lines.',
 "Rg1 moves the rook behind the future pawn route. Black's ...Rg3 offers a rook where the h-pawn can capture. "
 "After hxg3+, the king goes to g4, and gxh4+ starts the staircase. Each capture changes the pawn's file and "
 'exposes another line. The pawn is not simply collecting material: the checks force the king to remain '
 'vulnerable while the attack advances.',
 'The source main line continues ...Kh5 hxg5+ Kg6 gxh6+ Kh7 hxg7+ Kg8 gxh8=N#. The last capture opens the '
 'g-file for the rook on g1 to check g8. Promotion to a knight is essential because a knight on h8 controls '
 "f7, the king's otherwise available escape. A queen promotion gives check but allows a defence, so the piece "
 'choice must be checked. The source also gives king deviations at f4 and f7 with separate queen '
 'continuations.',
 "Replay the pawn's squares aloud: h2, g3, h4, g5, h6, g7, h8. After each capture, remove the captured unit "
 'and identify the actual checking line. At promotion, test every legal defender response rather than assuming '
 'a queen is automatically best. Underpromotion is rare in practical games, but the habit behind it is '
 "universal: choose the move that meets the position's needs, not the most valuable piece by default."),
    ['Rg1', 'Rg3', 'hxg3+', 'Kg4', 'gxh4+', 'Kh5', 'hxg5+', 'Kg6', 'gxh6+', 'Kh7', 'hxg7+', 'Kg8', 'gxh8=N#'],
    ['The rook moves to g1, preparing the checking lines behind the pawn.',
 'Black’s rook reaches g3 and becomes the pawn’s first target.',
 'The h-pawn captures the rook and opens a checking line.',
 'The king moves to g4.',
 'The pawn captures on h4 with check.',
 'The king reaches h5.',
 'The pawn captures on g5 and checks again.',
 'The king moves to g6.',
 'The pawn captures the knight on h6 with check.',
 'The king moves to h7 in the source main line.',
 'The pawn captures the queen on g7 with check.',
 'The king moves to g8.',
 'The pawn captures the bishop on h8 and promotes to a knight, giving the required mating geometry.'],
    ('Why study the final promotion choice carefully?',
 'Different promoted pieces allow different defensive replies',
 'The source requires a knight promotion for its mating finish.',
 'A pawn must always become a queen',
 'A pawn may promote to queen, rook, bishop, or knight.'),
    ('What makes the pawn staircase forcing?',
 'The captures repeatedly give check by changing open lines',
 'Black must respond to the checks as the pawn advances.',
 'Black is required to keep every piece en prise',
 'The line follows legal checks, not a rule requiring bad captures.'),
    ('The pawn alternates files; it does not move straight up the h-file.',
 'The final promotion is to a knight, not automatically to a queen.')
)

_add(
    'app-more-14',
    'Make two defenders interfere with each other',
    'S. Loyd, 1886',
    387,
    5,
    'b7/8/7B/7p/8/2p3r1/2P1P1pp/4K1kq w - - 0 1',
    ("Black's king on g1 is almost surrounded by its own army. White has only a bishop and two pawns besides the "
 "king, so the attack depends on the defender's congestion. The bishop on h6 needs a route to a decisive "
 "diagonal, but Black's bishop and rook can initially interfere with that route.",
 'Bc1 retreats the bishop across the board. After ...h4, Bf4 offers a flexible route toward b8 and then a7. '
 "Black's bishop may choose different squares on its long diagonal: the source pairs ...Bb7 with Bb8, ...Bc6 "
 'with Bc7, ...Bd5 with Bd6, and ...Be4 with Be5. White follows the defender by moving onto the next useful '
 'diagonal, keeping the final a7 idea available.',
 "The shown line uses ...Bb7 Bb8 Re3 Ba7 Bd5 Bxe3#. The rook on e3 blocks the black bishop's route, and "
 "White's bishop can finally capture it with mate along e3–f2–g1. Other defences produce different fifth-move "
 'finishes; Ba7 may give check in some branches and be a quiet threat in others. The lesson is the '
 'interference between defenders, not a claim that one final capture answers everything.',
 "At each stage, trace the black bishop's long diagonal and the black rook's possible blocking squares. Then "
 "identify where White's bishop must stand to exploit their interference. In a game, cramped defenders often "
 'obstruct each other, especially near a king with few flights. A quiet bishop maneuver can exploit that '
 'congestion more effectively than a premature check that lets the defenders reorganize.'),
    ['Bc1', 'h4', 'Bf4', 'Bb7', 'Bb8', 'Re3', 'Ba7', 'Bd5', 'Bxe3#'],
    ['The bishop retreats to c1, preparing a flexible route through f4.',
 'The h-pawn advances and changes the cramped kingside structure.',
 'The bishop reaches f4 and prepares to follow Black’s bishop placement.',
 'The black bishop chooses b7 on its long diagonal.',
 'The white bishop moves to b8, preparing Ba7.',
 'The rook moves to e3, creating an interference opportunity.',
 'The bishop reaches a7 and threatens the decisive diagonal.',
 'The black bishop tries d5 but cannot restore the whole defence.',
 'The white bishop captures the rook on e3 and mates along the diagonal to g1.'],
    ('Why are Bb8, Bc7, Bd6, and Be5 different responses?',
 'They match the black bishop’s chosen diagonal square',
 'White adapts its route to the defender’s placement.',
 'Bishops can change square color in problems',
 'Bishops always remain on their original color.'),
    ('What does the rook on e3 enable in the main line?',
 'Bxe3# along e3–f2–g1',
 'The rook becomes a capturable obstruction in the final diagonal attack.',
 'An immediate pawn promotion',
 'No white pawn promotes in this line.'),
    ('Ba7 is not automatically check in every branch.', 'The fifth move depends on Black’s defensive arrangement.')
)

_add(
    'app-more-15',
    'Use a waiting queen move to create zugzwang',
    'A. Nemtsov, 1947',
    387,
    4,
    '8/1p4p1/1P4P1/3N1P2/p1k1p3/p3B1pQ/Pp4P1/1K6 w - - 0 1',
    ("Black's king can move, but many pawns are locked or block useful squares. White's queen begins on h3, and "
 'its route through h7 and h8 is a timing maneuver. The white pawn on f5 controls e6 and g6; that support will '
 'make a queen check from e6 safe in one of the main branches.',
 'Qh7 is the correct first move. After ...Kd3, Qh8 puts Black in zugzwang: any legal king move worsens the '
 'position. The tempting immediate Qh8 fails to reproduce this timing, because ...Kd3 would leave White '
 'needing to move in the wrong version of the position. The extra queen step is useful precisely because it '
 'changes whose turn it is at the critical moment.',
 'After Qh7 Kd3 Qh8, ...Ke2 is answered by Qh1, followed in the shown line by ...Kd3 Qf1#. If Black instead '
 'returns to c4, Qe8 prepares the mate; ...Kxd5 is then met by Qe6#. The source also considers an immediate '
 "...Kxd5, answered by Qg8+, and ...Kb5, answered by Qxg7. The queen's destination depends on which king route "
 'Black chooses.',
 'Place the same pieces on the board with the opposite side to move and compare the options. This is the heart '
 'of zugzwang: having to move can be a disadvantage. At your rating, begin with the two main king replies and '
 "explain the queen's different follow-up squares. Avoid calling every quiet waiting move zugzwang; here the "
 'claim depends on the defender having no satisfactory legal move.'),
    ['Qh7', 'Kd3', 'Qh8', 'Ke2', 'Qh1', 'Kd3', 'Qf1#'],
    ['The queen moves to h7 to establish the correct move order.',
 'The king chooses d3, entering the key timing position.',
 'The queen reaches h8 and leaves Black to move in zugzwang.',
 'The king chooses e2, requiring the h-file queen response.',
 'The queen reaches h1 and prepares the final checking line.',
 'The king returns to d3 in this branch.',
 'The queen checks from f1 along f1–e2–d3 and mates.'],
    ('Why play Qh7 before Qh8?',
 'To reach the critical position with Black to move',
 'The timing creates zugzwang.',
 'Because a queen cannot move from h3 to h8',
 'That move is legal, but its timing does not solve the problem in four.'),
    ('What does zugzwang mean here?',
 'Black must move and every legal choice worsens its defence',
 'The obligation to move lets White choose the corresponding mating plan.',
 'Black is in check before making its move',
 'Zugzwang can occur without a check.'),
    ('The f5 pawn protects a queen on e6 in the relevant mating branch.',
 'Qh1 answers ...Ke2; Qe8 is the response to ...Kc4.')
)

# Additional defensive branches and the published alternative long finish.
GUIDES['app-three-05']['examples'] += (example('The king chooses b7 instead', '8/4K3/2k5/5Q1B/bp6/8/7B/8 w - - 0 1', ('Be2', 'Kb7', 'Qc8+', 'Kxc8', 'Ba6#'), (_inventory('8/4K3/2k5/5Q1B/bp6/8/7B/8 w - - 0 1'), *('Prepare the bishops’ complementary control.', 'The king chooses the other principal route.', 'Sacrifice the queen on c8 with check.', 'The king must accept the queen.', 'The e2 bishop checks from a6, supported by the h2 bishop’s control of b8.'))),)
GUIDES['app-three-06']['examples'] += (example('Answer the checking rook capture', 'Q7/8/4P3/1p6/p1B2P2/2B3Pp/1P5K/krbR4 w - - 0 1', ('Bh8', 'Rxb2+', 'Qg2', 'hxg2', 'Rxc1#'), (_inventory('Q7/8/4P3/1p6/p1B2P2/2B3Pp/1P5K/krbR4 w - - 0 1'), *('Clear c3 with the bishop’s long retreat.', 'The rook captures b2 with check along the second rank.', 'Block the check on g2 and offer the queen to the h-pawn.', 'The pawn captures the queen, leaving its old defensive square.', 'The rook captures c1 and checks the corner king at close range.'))),)
GUIDES['app-three-07']['examples'] += (example('King route through h3', '6R1/2K5/8/8/5p2/6p1/1Q3Nk1/8 w - - 0 1', ('Ng4+', 'Kh3', 'Nh2', 'Kh4', 'Qh8#'), (_inventory('6R1/2K5/8/8/5p2/6p1/1Q3Nk1/8 w - - 0 1'), *('Ng4+ uncovers the b2 queen’s check by clearing f2; the knight is not the checking piece.', 'The king chooses h3.', 'The knight reaches h2 and controls g4, leaving the intended king route.', 'The king moves to h4.', 'The queen checks down the h-file and mates.'))),)
GUIDES['app-three-07']['examples'] += (example('King route through f3', '6R1/2K5/8/8/5p2/6p1/1Q3Nk1/8 w - - 0 1', ('Ng4+', 'Kf3', 'Qc2', 'g2', 'Qd3#'), (_inventory('6R1/2K5/8/8/5p2/6p1/1Q3Nk1/8 w - - 0 1'), *('The knight moves to g4 and uncovers the queen’s check along the second rank.', 'The king chooses f3.', 'The queen quietly prepares a close-range checking net.', 'The pawn advances but cannot stop the net.', 'The queen checks from d3, protected by the knight on g4.'))),)
GUIDES['app-three-07']['examples'] += (example('King route through f1', '6R1/2K5/8/8/5p2/6p1/1Q3Nk1/8 w - - 0 1', ('Ng4+', 'Kf1', 'Ra8', 'Kg1', 'Ra1#'), (_inventory('6R1/2K5/8/8/5p2/6p1/1Q3Nk1/8 w - - 0 1'), *('The discovered queen check forces Black to choose a king reply.', 'The king chooses f1.', 'The rook prepares to enter the first rank while preserving the other controls.', 'The king goes to g1.', 'The rook checks across the first rank and mates.'))),)
GUIDES['app-three-08']['examples'] += (example('Underpromotion gives a different check', '4r1b1/1p4B1/pN2pR2/RB2k3/1P2N2p/2p3b1/n2P1p1r/5K1n w - - 0 1', ('Ke2', 'f1=N+', 'Rf2+', 'Kxe4', 'Bd3#'), (_inventory('4r1b1/1p4B1/pN2pR2/RB2k3/1P2N2p/2p3b1/n2P1p1r/5K1n w - - 0 1'), *('The king permits a promotion but must distinguish the new piece.', 'Black promotes to a knight; vacating f2 uncovers the h2 rook’s check along the second rank.', 'The rook blocks the second-rank check on f2 and uncovers bishop check on e5.', 'The king captures the e4 knight in this branch.', 'The bishop checks from d3, protected by the white king on e2, and mates.'))),)
GUIDES['app-three-12']['examples'] += (example('A bishop on e5 needs a different queen square', '5N1k/5Ppp/8/8/2Q3p1/8/8/b6K w - - 0 1', ('Qf1', 'Be5', 'Qf5', 'g6', 'Qxe5#'), (_inventory('5N1k/5Ppp/8/8/2Q3p1/8/8/b6K w - - 0 1'), *('The queen chooses the flexible key square.', 'The bishop chooses e5.', 'The queen attacks the bishop while maintaining the corner threat.', 'The g-pawn advances to meet part of the pressure.', 'The queen captures e5 and mates along the long diagonal to h8.'))),)
GUIDES['app-three-13']['examples'] += (example('The king moves before the pawn', '8/6p1/6Qp/3N1p1P/2P5/5k2/2P1p3/4K1B1 w - - 0 1', ('Ba7', 'Ke4', 'Qg3', 'g5', 'Qe3#'), (_inventory('8/6p1/6Qp/3N1p1P/2P5/5k2/2P1p3/4K1B1 w - - 0 1'), *('The bishop’s retreat begins the source plan.', 'The king immediately chooses e4.', 'The queen prepares the close-range e3 mate.', 'The g-pawn advances but does not stop the mating square.', 'The queen checks from e3, protected by the knight on d5; the white king controls nearby second-rank squares.'))),)
GUIDES['app-three-19']['examples'] += (example('The d-pawn capture invites a queen sacrifice', '1K6/6p1/4ppbp/Q1p2k2/2pp4/b3RNP1/4PN2/8 w - - 0 1', ('Qd8', 'dxe3', 'Qd2', 'exd2', 'e4#'), (_inventory('1K6/6p1/4ppbp/Q1p2k2/2pp4/b3RNP1/4PN2/8 w - - 0 1'), *('The queen’s key supports more than one sacrifice.', 'The d4 pawn captures the rook on e3.', 'Offer the queen on d2 to that same pawn.', 'The pawn captures and clears e3.', 'The e2 pawn advances two squares and checks the king on f5, completing the net.'))),)
GUIDES['app-three-20']['examples'] += (example('Immediate queen promotion', '8/1p6/8/7K/p4pQN/5B2/4pp2/2b2k2 w - - 0 1', ('Bc6', 'e1=Q', 'Bg2+', 'Kg1', 'Nf3#'), (_inventory('8/1p6/8/7K/p4pQN/5B2/4pp2/2b2k2 w - - 0 1'), *('The bishop key keeps replies ready against promotion.', 'Black promotes immediately to a queen.', 'The bishop checks from g2.', 'The king moves to g1.', 'The knight reaches f3 and mates by opening the queen’s g-file attack while covering escape squares.'))),)
GUIDES['app-three-20']['examples'] += (example('Immediate knight promotion', '8/1p6/8/7K/p4pQN/5B2/4pp2/2b2k2 w - - 0 1', ('Bc6', 'e1=N', 'Bb5+', 'Nd3', 'Qd1#'), (_inventory('8/1p6/8/7K/p4pQN/5B2/4pp2/2b2k2 w - - 0 1'), *('The bishop key prepares a different response to a knight.', 'Black chooses a knight promotion.', 'The bishop checks along the diagonal from b5 to f1.', 'The new knight interposes on d3.', 'The queen reaches d1 and checks along the first rank with mate.'))),)
GUIDES['app-three-20']['examples'] += (example('The king advances to e1', '8/1p6/8/7K/p4pQN/5B2/4pp2/2b2k2 w - - 0 1', ('Bc6', 'Ke1', 'Nf3+', 'Kd1', 'Bxa4#'), (_inventory('8/1p6/8/7K/p4pQN/5B2/4pp2/2b2k2 w - - 0 1'), *('The bishop key begins the attack.', 'The king chooses e1 instead of promoting.', 'The knight checks from f3.', 'The king moves to d1.', 'The bishop captures a4 and mates along a4–b3–c2–d1.'))),)
GUIDES['app-more-09']['examples'] += (example('The queen captures the blocking pawn', '3r3k/R4P1p/3p1K1N/4P3/8/1qp3R1/8/8 w - - 0 1', ('Ra8', 'Rxa8', 'e6', 'Qxe6+', 'Kxe6', 'c2', 'Rg8+', 'Rxg8', 'fxg8=Q#'), (_inventory('3r3k/R4P1p/3p1K1N/4P3/8/1qp3R1/8/8 w - - 0 1'), *('Draw the rook onto a8.', 'The rook captures the offered attacker.', 'The pawn blocks the queen’s line toward f7 and creates a threat.', 'The queen removes the pawn with check.', 'The king captures the checking queen, eliminating that defender.', 'The c-pawn advances in this illustrative continuation.', 'The remaining rook checks on g8.', 'Black’s rook captures on g8.', 'The pawn recaptures and promotes to a queen with mate.'))),)
GUIDES['app-more-13']['examples'] += (example('The king escapes toward f4', '7b/Kp4q1/1p2bp1n/p1B2pp1/7p/5r1k/6RP/7Q w - - 0 1', ('Rg1', 'Rg3', 'hxg3+', 'Kg4', 'gxh4+', 'Kf4', 'Bd6+', 'Ke3', 'Rg3+', 'Kd4', 'Qd1+', 'Kc4', 'Qd3#'), (_inventory('7b/Kp4q1/1p2bp1n/p1B2pp1/7p/5r1k/6RP/7Q w - - 0 1'), *('Prepare the rook behind the pawn route.', 'Black offers the rook on g3.', 'The pawn captures and opens check.', 'The king moves to g4.', 'The pawn captures h4 with check.', 'The king chooses f4, leaving the main staircase.', 'The bishop checks from d6.', 'The king goes to e3.', 'The rook checks along the third rank.', 'The king moves to d4.', 'The queen checks on the d-file.', 'The king moves to c4.', 'The queen checks from d3 and completes the mating net.'))),)
GUIDES['app-more-15']['examples'] += (example('Zugzwang sends the king back to c4', '8/1p4p1/1P4P1/3N1P2/p1k1p3/p3B1pQ/Pp4P1/1K6 w - - 0 1', ('Qh7', 'Kd3', 'Qh8', 'Kc4', 'Qe8', 'Kxd5', 'Qe6#'), (_inventory('8/1p4p1/1P4P1/3N1P2/p1k1p3/p3B1pQ/Pp4P1/1K6 w - - 0 1'), *('Use the intermediate queen move to establish the timing.', 'The king reaches d3.', 'Put Black to move in the critical position.', 'The king returns to c4.', 'The queen chooses e8, the correct response to this route.', 'The king captures the knight on d5.', 'The queen checks from e6, protected by the f5 pawn, and mates.'))),)
GUIDES['app-more-11']['examples'] += (example('Studenetsky’s published alternative finish', '6K1/1p6/4B3/2R5/8/pp4P1/pk6/b7 w - - 0 1', ('Kh7', 'b6', 'Rc6', 'b5', 'Kh6', 'b4', 'Bg8', 'Kb1', 'Bh7+', 'Kb2', 'Kg6', 'Kb1', 'Kg5+', 'Kb2', 'Kf5', 'Kb1', 'Kf4+', 'Kb2', 'Ke4', 'Kb1', 'Ke3+', 'Kb2', 'Kd3', 'Kb1', 'Kd2+', 'Kb2', 'Rg6', 'Kb1', 'Rg4+', 'Kb2', 'Bc2', 'bxc2', 'Rxb4#'), (_inventory('6K1/1p6/4B3/2R5/8/pp4P1/pk6/b7 w - - 0 1'), *('The king begins its approach on h7.', 'The b-pawn supplies a waiting move.', 'The rook reaches c6, maintaining the confinement.', 'The b-pawn advances again.', 'The king moves to h6, preparing the bishop maneuver.', 'The pawn reaches b4 and has used its forward moves in this line.', 'The bishop heads for h7 via g8.', 'The black king moves to b1.', 'The bishop checks along the long diagonal from h7.', 'The king returns to b2.', 'White’s king blocks the bishop’s diagonal on g6.', 'With the diagonal blocked, the king can return to b1.', 'The king steps off the diagonal on g5, uncovering check.', 'The king must return to b2 in this cycle.', 'The king blocks the diagonal on f5, one stage nearer the queenside.', 'The king returns to b1.', 'The king steps off on f4, uncovering bishop check.', 'The king returns to b2.', 'The king blocks the diagonal on e4.', 'The king returns to b1.', 'The king steps off on e3, uncovering check.', 'The king returns to b2.', 'The king blocks the diagonal on d3, close to its destination.', 'The king returns to b1.', 'The king reaches d2 and uncovers the bishop check again.', 'The king returns to b2.', 'The rook blocks the bishop’s diagonal on g6, allowing ...Kb1 and preparing the finishing maneuver.', 'The king returns to b1.', 'Rg4+ leaves g6 and uncovers the h7 bishop’s check on b1, while preparing the rook’s fourth-rank finish.', 'The king returns to b2.', 'The bishop is offered on c2 to the b3 pawn.', 'The b3 pawn captures the bishop, clearing b3 and occupying c2.', 'The rook captures b4 and checks down the b-file; the changed pawn structure completes the alternative mate.'))),)
