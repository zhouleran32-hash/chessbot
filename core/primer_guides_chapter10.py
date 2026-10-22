"""Detailed original teaching of Chapter10 (printed pp.369–376).

Historical game branches illustrate the book's reasoning; they are not claims
about current opening popularity or exhaustive best-play verdicts.
"""
import chess
from core.primer_build import after, custom
from core.primer_guides_chapter1 import section, example, check, guide

GUIDES = {}
EXERCISES = []


def position_inventory(fen):
    board = chess.Board(fen)
    armies = []
    for color, label in ((chess.WHITE, 'White'), (chess.BLACK, 'Black')):
        groups = []
        for piece_type in (chess.KING, chess.QUEEN, chess.ROOK, chess.BISHOP, chess.KNIGHT, chess.PAWN):
            squares = board.pieces(piece_type, color)
            if squares:
                name = chess.piece_name(piece_type) + ('s' if len(squares) > 1 else '')
                groups.append(name + ' on ' + ', '.join(chess.square_name(s) for s in squares))
        armies.append(label + ' has ' + '; '.join(groups))
    return ('White' if board.turn else 'Black') + ' to move. ' + '. '.join(armies) + '.'


def add(key, title, pages, summary, goals, sections, examples, prompt, choices,
        checks, pitfalls, recap, *, quiz_fen=None, objective=None):
    identifier = 'ch10-' + key
    practice_fen = quiz_fen or examples[0]['fen']
    GUIDES[identifier] = guide(pages, goals, sections, examples, pitfalls, checks, recap)
    EXERCISES.append(dict(id=identifier, title=title, summary=summary,
                         fen=practice_fen,
                         inventory=(examples[0]['notes'][0] if practice_fen == examples[0]['fen']
                                    else position_inventory(practice_fen)), prompt=prompt,
                         choices=choices, objective=objective))


def q(key, prompt, correct, why, wrong, correction):
    return check(key, prompt, (correct, True, why), (wrong, False, correction))


B0='e4 c5 Nf3 d6 d4 cxd4 Qxd4 Nc6 Bb5 Bd7 Bxc6 bxc6 Nc3 Nf6 Bg5'.split()
B1='Rb8 e5 dxe5 Nxe5 Rxb2 Bxf6 gxf6 Nxd7 Qxd7 Qxd7+ Kxd7 O-O-O+'.split()
Y0='e4 c5 c3 d5 exd5 Qxd5 d4 Nc6 Nf3 Bg4 Be2 O-O-O dxc5 Qxc5 Qa4 Bxf3 Bxf3 Nd4'.split()
Y1='cxd4 Qxc1+ Ke2 Qxb2+ Nd2 Qxd4 Qc2+ Kb8 Rhc1 Qd7 Rab1 b6 Nc4 Rc8 Qe4 Qe6 Ne5 Qxa2+ Kf1'.split()
A='d4 d5 Nf3 e6 c4 a6 c5 Nc6 Bf4 Nge7 Nc3 Ng6 Be3 b6 cxb6 cxb6 h4 Bd6 h5 Nge7 h6 g6 Bg5 O-O Bf6'.split()
L0='e4 e5 Nf3 Nc6 Bb5 a6 Ba4 Nf6 O-O Nxe4 d4 b5 Bb3 d5 dxe5 Be6'.split()
L1='Qe2 Be7 Rd1 Nc5 Bxd5 Bxd5 Nc3 Bc4 Rxd8+ Rxd8 Qe3 b4 b3'.split()
L2='Be6 Ne4 Rd1+ Ne1 Nd4 Bb2 Nxc2 Qe2 Rxa1 Bxa1 Nxa1 Nxc5 Bxc5 Nd3 Bb6 Nxb4 O-O Nc6 f6 h4'.split()
L3='Kh8 Kh2 Bd7 exf6 Bxc6 Qe7 Rg8 fxg7+ Rxg7 Qf8+ Rg8 Qf6+ Rg7 h5 Kg8 Qxc6 Rf7 Qc3'.split()
H=custom({'a8':'r','b8':'n','d8':'q','f8':'r','g8':'k','a7':'p','b7':'p','f7':'p','g7':'b','h7':'p','c6':'p','d6':'p','e6':'b','f6':'n','g6':'p','c4':'P','d4':'B','e4':'P','f4':'N','c3':'N','f3':'P','a2':'P','b2':'P','d2':'Q','g2':'P','h2':'P','a1':'R','e1':'K','f1':'B','h1':'R'},turn='b',castle='KQ')
H1='c5 Be3 Nc6 O-O-O Nd4 h4 h5 Qf2 Nd7'.split()
H = H.rsplit(' ', 1)[0] + ' 10'

add('understand-system', 'Understand a system: moves, structure, and future jobs', (369, 370),
    'Opening knowledge connects the first moves to the kind of position you want to play. Learn the reason for a setup, what the opponent is trying to do, and which changes would make you choose another plan.',
    ('Explain a move through its effect on squares and pieces.', 'Connect an opening exchange to the next phase of the game.'),
    (
        section('General principles are the starting tools', '''Development, central influence, and king safety apply beyond beginner chess. They are useful because undeveloped pieces cannot help, a weak centre allows invasion, and an exposed king consumes defensive moves. Yet those principles do not select one universal move in every position. A system is a recurring arrangement of pawns and pieces with typical plans. To understand it, identify what each piece is meant to do, which pawn advance creates contact, and which exchanges change the character of the position. A named opening is a convenient label for those relationships, not an extra rule of chess.'''),
        section('Follow an exchange all the way to its consequences', '''Our opening example begins with e4 c5, the Sicilian Defence. White occupies the centre; Black's c-pawn attacks d4 from the side. After Nf3 d6 d4 cxd4, White's c- and e-pawns have not vanished: it is the d-pawn that was exchanged for Black's c-pawn. Nxd4 develops the knight while recovering that pawn. The c-file is now partly open for Black, and White has a central knight and e4 pawn. These features help explain later plans. You should be able to describe the position without relying on the opening's name.'''),
        section('Ask a question of each candidate', '''Before the recapture, compare Nxd4 with Qxd4. Both are legal and restore the immediate pawn count. The knight capture develops a minor piece, whereas the queen capture exposes a valuable piece to attacks that may help Black develop. That is a reason to prefer a developing recapture in a basic repertoire, not a proof that every early queen capture loses. The book's next game deliberately uses Qxd4 and then shows Black failing to exploit it. One imperfect move does not excuse the opponent's later mistakes. Evaluate what is actually on the board after every reply.'''),
        section('Make the knowledge usable at your rating', '''For each opening position you study, answer four questions: which piece needs a job, where can the centre change, how will each king become safe, and what is threatened now? At 564, a short line you can explain is worth more than a long sequence you cannot reconstruct. Play the example, reset it, and explain the pawn exchange and the knight's destination aloud. Then change Black's next move and repeat the questions. Learning a system should increase your ability to choose a legal, safe move when memory ends; it should not make an unfamiliar reply feel like the end of your preparation.'''),
    ),
    (example('Opening illustration: a recapture that develops', after(('e4','c5','Nf3','d6')), ('d4','cxd4','Nxd4','Nf6','Nc3'), (
        'White has a pawn on e4 and knight f3; Black has pawns c5/d6. Both kings still need development and shelter.',
        'd4 challenges the centre and opens the c1 bishop. Calculate the possible pawn exchange before pushing.',
        '...cxd4 exchanges Black’s c-pawn for White’s d-pawn and removes the c-file pawn obstruction.',
        'Nxd4 recaptures while putting a knight in the centre. Qxd4 was also legal, but gives the queen an early defensive burden.',
        '...Nf6 develops and attacks e4. It gives White a concrete question to answer.',
        'Nc3 develops while defending e4. This sample continuation explains jobs rather than promising a forced advantage.',
    )),),
    'After d4 cxd4, recapture with the f3 knight to develop it onto d4.',
    (('Nxd4',True,'The knight recaptures and occupies the central square.'),('Qxd4',False,'This legal queen recapture does not perform the specified knight development.'),('Bc4',False,'This develops a bishop but leaves the offered central pawn unrecovered.')),
    (q('system','What does understanding a system include?','Typical pawn changes, piece jobs, and the opponent’s plans','The moves are connected by purposes.','Only a list of move names','A list does not tell you how to react to a new move.'),
     q('judgment','Does Qxd4 automatically lose?','No; its drawbacks must be tested in the actual position','General principles guide the comparison without replacing calculation.','Yes; an early queen move is forbidden','It is legal and sometimes playable; the issue is concrete cost.')),
    ('Do not use an opening name as a substitute for inspecting the board.',),
    ('Name the structural change.', 'Give every move a job.', 'Answer threats before following a setup.'),
    quiz_fen=after(('e4','c5','Nf3','d6','d4','cxd4')))

add('centre-plan', 'The centre matters more than an attractive side target', (370, 370),
    'In Borbely–Kovacs, Black sees a pawn on b2 and sends a rook toward it. The neglected central situation explains why that pawn is expensive. Compare the tempting raid with a central response before following the game.',
    ('Assess both sides before starting a pawn raid.', 'Explain why the central break e5 becomes dangerous.'),
    (
        section('Reconstruct the opening rather than trust the result', '''The game begins e4 c5 Nf3 d6 d4 cxd4 Qxd4. White has recaptured with the queen instead of the knight. Black develops Nc6 with an attack on that queen, and White answers Bb5, pinning the knight to the king. After Bd7 Bxc6 bxc6, Black has a central pawn mass and the bishop pair, while White has exchanged a bishop for a knight. Neither label decides the game. The pawn recapture strengthens Black's central influence but spends a move that could have developed the d7 bishop by Bxc6. Compare both the structural benefit and the development cost.'''),
        section('Inventory the position after Bg5', '''White's queen is on d4, knights on c3 and f3, and bishop on g5. Black's king remains on e8, bishop on f8, knight on f6, and bishop on d7; the queenside rook is still on a8. White can consider e5 to challenge the d6 pawn and the f6 knight. Black's b-file is open because the b-pawn captured on c6, and White's b2 pawn looks reachable. The file explains why Rb8 is tempting. It does not explain whether Black has time to use it. The safety of the king and the possible opening of central lines decide that question.'''),
        section('Compare plans at the decision point', '''The book recommends e5 for Black: the d6 pawn stays behind an advanced e-pawn and White's queen on d4 is attacked. Black combines central restraint with a tempo against the queen. Our alternative line shows Qd3 as one legal retreat, followed by Be7 and castling preparations. It is an illustration of the plan, not a complete best-play verdict. In the historical game Rb8 instead leaves White time for e5. After dxe5 Nxe5, White's developed pieces gain central access while Black's king and f8 bishop still need attention.'''),
        section('Use a two-question test for pawn grabs', '''Before chasing a distant pawn, ask what the opponent can open in the centre and how your least developed pieces will join the defence. A rook moving along an open file can be active in the wrong place. A pawn gain is valuable when you can consolidate it, but not when the rook's excursion leaves your king and central pieces unable to meet forcing moves. Reset the diagram before Rb8, name White's e5 idea, and then explain why Black's own e5 changes the timing. In your games, perform this comparison before you see the continuation; afterward it is easy to call a tempting pawn obviously poisonous.'''),
    ),
    (example('Borbely–Kovacs: development reaches a decision', chess.STARTING_FEN, B0, (
        'Both armies begin at home. Track the queen’s route and Black’s undeveloped kingside.',
        'e4 occupies the centre.', '...c5 challenges d4 from the flank.', 'Nf3 develops and supports d4.', '...d6 supports a central setup and opens the c8 bishop.',
        'd4 challenges Black’s c-pawn.', '...cxd4 opens the c-file.', 'Qxd4 recaptures with the queen.', '...Nc6 develops with a queen attack.',
        'Bb5 pins the c6 knight to the e8 king.', '...Bd7 interrupts the pin and develops a defender.', 'Bxc6 exchanges the bishop for that knight.',
        '...bxc6 reinforces the centre and opens the b-file, while the f8 bishop remains at home.', 'Nc3 develops and supports e4.', '...Nf6 attacks e4 and develops.',
        'Bg5 adds pressure on f6. Stop here and compare a central response with the b2 pawn raid.',
    )),example('Central alternative: make the queen answer first',after(B0),('e5','Qd3','Be7'),(
        'Black to move. White threatens to use e5; Black must decide whether a rook raid is timely.',
        '...e5 occupies the central square and attacks the queen d4.',
        'Qd3 is an illustrative legal retreat. It is not asserted to be White’s only choice.',
        '...Be7 brings the last kingside minor piece into play and clears the castling route.',
    ))),
    'Play the e-pawn to e5, taking central space and attacking the queen on d4.',
    (('e5',True,'The pawn gains central space with a tempo against the queen.'),('Rb8',False,'This is the historical side raid; it does not address the specified central task.'),('h6',False,'A bishop question does not make the requested central advance.')),
    (q('recapture','What does bxc6 change?','It reinforces central pawns and opens the b-file','A structural benefit can coexist with a development cost.','It completes Black’s kingside development','The f8 bishop and e8 king still need attention.'),
     q('raid','What must you check before Rb8 and Rxb2?','The opponent’s central breaks and forcing replies','A distant pawn is useful only if your position survives.','Only whether b2 is defended','Tactics and development can outweigh the pawn’s immediate defence.')),
    ('Do not infer that the game winner handled every earlier move perfectly.',),
    ('Compare structure and time together.', 'A central move can gain a tempo.', 'Look for the opponent’s break.'),quiz_fen=after(B0))

add('pawn-raid', 'Why the rook on b2 becomes a target', (370, 370),
    'Follow the complete central sequence from the rook raid to castling with check. The combination ends by using two different pieces at once: the rook checks the king while the castled king attacks the invading rook.',
    ('Track which piece makes each capture.', 'Explain the final castling move through its two simultaneous effects.'),
    (
        section('White uses the time Black spends on pawns', '''After the position from the previous lesson, Black plays Rb8. White advances e5, attacking the f6 knight and creating contact with the d6 pawn. The game continues dxe5 Nxe5 Rxb2. The rook has won a pawn, but White's queen, bishop, and knights are working in the centre while Black's f8 bishop remains undeveloped. Count the threats before deciding whether that extra pawn is real progress. The source also gives the quieter Rd1 followed by castling as a way to use central pressure. The spectacular continuation is not the only way to punish a development deficit.'''),
        section('Read the exchanges one piece at a time', '''White plays Bxf6, and the game follows gxf6. The bishop has taken the f6 knight; the g-pawn has then taken that bishop. White's knight on e5 captures Black's d7 bishop with Nxd7. Black's queen recaptures on d7, and White's queen takes that queen with check. Black's king captures the white queen on d7. Each capture changes the checking lines and which pieces remain. Do not continue imagining the bishop on g5 or the knight on e5 after they have disappeared. The point of this exchange order becomes visible only when the king reaches d7.'''),
        section('Castling is an attacking move here', '''O-O-O+ moves White's king from e1 to c1 and rook from a1 to d1. The d-file is clear, so the rook checks the king on d7. At the same time the white king on c1 attacks Black's rook on b2. Black must answer the check and cannot simultaneously rescue that rook. In this exact position every legal reply is a king move, after which Kxb2 is legal. This is why the book ends the game with resignation, not with a checkmate symbol. Castling has coordinated king and rook in a tactical double attack.'''),
        section('Keep the defensive alternatives visible', '''The historical line includes Black's mistakes; it is not a claim that the whole sequence was forced from Rb8. After Nxe5, the book examines Rb7 as more resistant than taking b2, and after Bxf6 it points to exf6 as a way to complicate the position. Those alternatives must be considered before choosing a line in a game. Here the learning task is narrower: understand why the displayed captures let White castle with check and win the rook. Replay slowly, explain the change after every capture, then reset and compare the same final move when the black king has not been drawn to d7.'''),
    ),
    (example('Borbely–Kovacs: the pawn raid meets a central combination',after(B0),B1,(
        'Black’s king is e8, rook a8, and bishops d7/f8. White’s queen d4 and developed pieces are ready to use the centre.',
        '...Rb8 heads for b2 before Black has finished kingside development.', 'e5 attacks the knight f6 and challenges d6.',
        '...dxe5 accepts the central exchange.', 'Nxe5 recaptures with the f3 knight and attacks d7.',
        '...Rxb2 takes the pawn. Rb7 was a more resistant source alternative.', 'Bxf6 captures the remaining black knight.',
        '...gxf6 is the game reply; exf6 is a separate defensive possibility.', 'Nxd7 captures the bishop with the knight first.',
        '...Qxd7 takes that knight.', 'Qxd7+ exchanges queens with check.', '...Kxd7 puts the king on the open d-file.',
        'O-O-O+ checks with the rook d1 and attacks b2 with king c1. Black resigned because the rook is lost.',
    )),),
    'Castle queenside with check, placing your king on c1 where it attacks the rook on b2.',
    (('O-O-O+',True,'The rook checks down the d-file while the king attacks b2.'),('O-O',False,'Kingside castling does not create that two-piece attack.'),('Kd2',False,'This does not move the rook to d1 or attack b2 with the king.')),
    (q('checker','Which piece gives check after O-O-O+?','The rook on d1','The king has moved to c1 and attacks the separate target b2.','The king on c1','The kings are not adjacent; the d-file rook delivers check.'),
     q('result','Why is the final move marked + rather than #?','Black can answer check, but then loses the rook','A winning double attack need not be immediate mate.','The book forgot to mark checkmate','Several king replies are legal.')),
    ('Track the knight-first capture order; the next lesson tests the tempting reversal.',),
    ('Update the board after every exchange.', 'A castle moves two useful pieces.', 'Resignation is not checkmate.'),
    quiz_fen=after(B0+B1[:-1]))

add('capture-order', 'A check is not automatically the best capture order', (370, 370),
    'Compare Nxd7 with the tempting Qxd7+ in the same tactical position. The check looks more forcing, but it leaves different pieces on the board and changes Black’s available reply.',
    ('Compare variations by their final positions.', 'Explain why the order of captures changes the next threat.'),
    (
        section('Start from the same board each time', '''The position arises after the rook raid and Bxf6 gxf6. White has king e1, queen d4, rooks a1/h1, and knights c3/e5; Black has king e8, queen d8, rook b2/h8, and bishops d7/f8. White wants to remove the d7 bishop. Both the queen and the e5 knight can capture it. When comparing candidates, reset mentally to this exact inventory. If you leave a captured piece on the imagined board, the apparent forcingness of the line may be entirely fictional. The source uses this moment to warn against careless play even in an advantageous position.'''),
        section('The knight-first line creates a checking castle', '''Nxd7 Qxd7 Qxd7+ Kxd7 leaves Black's king on d7 and White's original king and a1 rook unmoved. Castling queenside is legal and checks along the newly open d-file. The c1 king also attacks the invading b2 rook, so Black loses it after answering check. The calculation is about the final king placement, not just the fact that bishops and queens were exchanged. Describe the endpoint before choosing the first capture: I want the enemy king on the d-file while my own king still has queenside castling available.'''),
        section('The queen-first line changes who recaptures', '''If White instead begins Qxd7+, Black replies Qxd7 and White follows Nxd7. White has traded queens, but Black's king remains on e8. Black now has time for Rxc2, capturing White's c2 pawn with the invading rook. There is no equivalent checking castle that forces the rook to stay on b2. White's knight has reached d7, so the position may still contain useful opportunities, but the immediate rook-winning mechanism has gone. The book does not use this branch to prove White is lost; it shows why a superficially more forcing check is an inferior route to the intended goal.'''),
        section('Use forcing moves as candidates, not as a verdict', '''Checks deserve early attention because the opponent must answer them. That does not mean a check is stronger than every noncheck. Compare what each sequence leaves behind: king squares, remaining attackers, open lines, and whose turn it is. Pause before the first capture and state both endpoints without advancing the arrows. Then replay each branch to correct your mental board. In your own games, whenever two pieces can capture the same target, examine both orders if the position is tactical. A move can be more forcing immediately and still fail to force the result you actually need.'''),
    ),
    (example('Queen first: the rook gets a free move',after(B0+B1[:7]),('Qxd7+','Qxd7','Nxd7','Rxc2'),(
        'White can take d7 with queen or knight. Compare the resulting king position, not just the first check.',
        'Qxd7+ captures the bishop with check.', '...Qxd7 takes White’s queen while Black’s king stays on e8.',
        'Nxd7 recaptures the queen with the e5 knight.', '...Rxc2 takes another pawn; Black was not forced to move its king at all.',
    )),example('Knight first: retain the checking castle',after(B0+B1[:7]),('Nxd7','Qxd7','Qxd7+','Kxd7','O-O-O+'),(
        'Reset to the same board. This time remove the d7 bishop with the knight.', 'Nxd7 starts the intended exchange order.',
        '...Qxd7 takes the knight.', 'Qxd7+ exchanges queens with check.', '...Kxd7 puts the king on the d-file.',
        'O-O-O+ wins time to take the rook b2 with the king after Black answers check.',
    ))),
    'Capture the d7 bishop with the e5 knight first, preserving the queen capture that will draw the king to d7.',
    (('Nxd7',True,'This is the knight-first sequence that prepares castling with check.'),('Qxd7+',False,'The checking queen-first sequence leaves Black’s king on e8 and permits Rxc2.'),('Nxc6',False,'This captures a different target and does not arrange the demonstrated king attraction.')),
    (q('order','Why does the capture order matter?','It determines which black piece occupies d7 at the end','The checking castle needs the king there.','It changes how the knight is allowed to move','The legal movement rules stay unchanged.'),
     q('checks','Are checks automatically better than nonchecks?','No; compare the resulting positions','Forcingness helps calculation, but the result decides.','Yes; a check always gains a useful tempo','The forced response can improve the opponent’s position.')),
    ('Do not call the queen-first branch a forced loss; it loses the intended tactical mechanism.',),
    ('Reset before comparing candidates.', 'Track who recaptures.', 'Judge the endpoint.'),quiz_fen=after(B0+B1[:7]))

add('development-compensation', 'Count the pieces that can actually fight', (371, 371),
    'In Yudovich’s game, Black wins pawns while leaving the kingside army at home. White gives up a bishop to gain time and open routes. The point is coordinated activity, not a general licence to sacrifice material.',
    ('Distinguish material count from useful participation.', 'Calculate the opponent’s captures before accepting a sacrifice.'),
    (
        section('What compensation means', '''Compensation is something useful received in return for material: initiative, exposed targets, open lines, better coordination, or lasting positional gains. It must be shown on the board. Saying I have an attack is not enough if the opponent can exchange queens, return some material, and finish development safely. Conversely, a player may have more points on the board but fewer pieces participating in the immediate fight. In this game the c8 king and roaming queen become targets while Black's f8 bishop, g8 knight and h8 rook remain at home. White tries to make that delay matter before those pieces can join.'''),
        section('Understand how the unusual position arose', '''The opening begins e4 c5 c3 d5 exd5 Qxd5 d4 Nc6 Nf3 Bg4 Be2 O-O-O. Black castles long early, putting the king behind a c-file whose pawn has advanced. White's dxc5 is premature in the book's analysis; Be3 would have developed. Black's Qxc5 also spends queen time instead of using the more active Qe4 idea. After Qa4 Bxf3 Bxf3 Nd4, Black's knight attacks the bishop f3 and threatens to exploit the c-file. Both players made choices that helped create the tactic. The lesson is to recognize the resulting position, not to memorize all preceding choices as an ideal opening.'''),
        section('A pawn capture changes the entire operation', '''White plays cxd4, taking the advanced knight and clearing c3 from the c-file. Black answers Qxc1+, capturing White's bishop on c1 with check. White does not try to hide the fact that material has changed: the knight was exchanged for a bishop, and further pawn captures are coming. Ke2 answers the check, after which Qxb2+ Nd2 Qxd4 takes two pawns. White's reply Qc2+ gains a forcing move for the queen, Kb8 steps aside, and Rhc1 brings a rook onto the open file. The queen and rook cooperate against the castled king while Black's kingside remains dormant.'''),
        section('Why this example needs careful boundaries', '''The king move Ke2 is unusual and would be dangerous in many other openings. Here it supports a concrete line of activity; it is not a replacement for learning to castle. Before playing cxd4, calculate the queen check, your answer, and how the rook enters. Then count the pieces that can give useful threats on the next move for both sides. If the defender can bring a bishop or knight into the fight with tempo, the sacrifice may cease to work. At your level, the transferable habit is to compare participating forces and forcing replies, rather than judging every position by the number of pawns alone.'''),
    ),
    (example('Yudovich–N.N.: the route to the tactical decision',chess.STARTING_FEN,Y0,(
        'Follow how the open c-file and Black’s long castling place a king and queen on the same wing.',
        'e4 occupies the centre.', '...c5 contests d4.', 'c3 prepares a pawn recapture on d4.', '...d5 immediately challenges e4.',
        'exd5 exchanges the e-pawn.', '...Qxd5 recaptures with the queen.', 'd4 builds central contact.', '...Nc6 develops.',
        'Nf3 develops toward the centre.', '...Bg4 pins the knight to the queen d1.', 'Be2 interrupts that pin and prepares castling.',
        '...O-O-O puts Black’s king on c8 and rook d8.', 'dxc5 takes a pawn; the book prefers developing Be3 here.',
        '...Qxc5 recaptures; the source considers Qe4 more active.', 'Qa4 brings the queen to the wing near Black’s king.',
        '...Bxf3 trades the bishop for the knight.', 'Bxf3 recaptures with White’s e2 bishop.', '...Nd4 advances the knight, inviting the critical c-pawn capture.',
    )),example('Material versus development: the c-file becomes useful',after(Y0),Y1[:9],(
        'White’s queen a4, bishop f3 and rooks can cooperate; Black’s king is c8 and kingside pieces remain at home.',
        'cxd4 captures the knight and empties c3. Calculate the queen’s checking capture on c1.',
        '...Qxc1+ takes the bishop and gives check down the first rank.', 'Ke2 answers the check without abandoning the attacking plan.',
        '...Qxb2+ takes a pawn and checks along b2–e2.', 'Nd2 develops with a block to that check.',
        '...Qxd4 takes a second pawn.', 'Qc2+ uses the open file to give check.', '...Kb8 is the game’s king retreat.',
        'Rhc1 activates the h-rook. White’s queen, rook, bishop and knight can join the attack while Black’s kingside is undeveloped.',
    ))),
    'Capture the advanced d4 knight with the c3 pawn, as in the demonstrated compensation line.',
    (('cxd4',True,'The pawn takes the knight and clears the c-file for later activity.'),('Qxd4',False,'The task asks for the c-pawn capture; the queen capture changes the tactical geometry.'),('O-O',False,'Castling is legal here but does not make the specified capture.')),
    (q('forces','What should accompany a material count?','Which pieces can take part in the immediate fight','An undeveloped piece may not help meet an urgent threat.','The number of impressive-looking moves already played','Past activity matters only through the present position.'),
     q('sacrifice','What justifies accepting the risks of cxd4?','A calculated route through the checks to coordinated activity','Compensation must survive the opponent’s forcing responses.','A rule that activity always beats two extra pawns','There is no universal exchange rate between time and material.')),
    ('Do not imitate the exposed king move without the same concrete tactical support.',),
    ('Count active forces as well as material.', 'Calculate checks against your own king.', 'Convert opened lines into entry routes.'),quiz_fen=after(Y0))

add('mobilize-reserves', 'Bring the last attackers into the game', (371, 371),
    'An attack becomes stronger when new pieces join it. Continue Yudovich’s game and see the second rook and knight become active while Black keeps using the queen to collect material.',
    ('Give the least active attacker a concrete route.', 'Separate a resignation from a demonstrated checkmate.'),
    (
        section('Do not ask one piece to do everything', '''After White's Rhc1, the first rook and queen use the c-file, but the a1 rook and knight d2 can still improve. Black has two extra pawns, yet its bishop f8 and knight g8 do not help the king on b8. An attack often stalls when the active pieces repeat threats while the reserves stay idle. Look for a route that adds a new kind of pressure: a second file, a defended entry square, or a knight jump that attacks a pawn shield. The new unit should have a specific job rather than merely move toward the king.'''),
        section('Coordinate the rooks with the knight', '''The game continues Qd7 Rab1 b6 Nc4 Rc8. Rab1 puts the second rook on the b-file, aligned with the enemy king; b6 blocks that file but also creates a target near the king. Nc4 brings the knight toward b6 and e5, and Black replies Rc8 to contest the c-file. The defensive rook is finally active, but Black still has not completed kingside development. White then plays Qe4 and Ne5, increasing pressure and centralizing the knight. Trace each route on the board and explain which target or entry square becomes available after the move.'''),
        section('Answer the check without losing the thread', '''After Qe6 Ne5, Black plays Qxa2+, taking yet another pawn with check. White answers Kf1. That king retreat is important: an attacking plan does not allow you to ignore a legal check. The historical game ends with Black resigning, and the book judges the position overwhelming for White. The displayed endpoint is not checkmate; Black still has legal moves. Our replay therefore stops at the recorded conclusion and teaches the coordination that led to it, rather than inventing a supposedly forced final mating line. A result label and a chess-rule ending are different pieces of information.'''),
        section('Transfer the method without copying the risks', '''At your own board, locate the attacker doing the least work and find a safe route to a useful square. Ask what the defender can exchange, block or threaten while you bring it up. An attacking move that leaves your queen hanging or permits mate at home is not justified by a promising long-term plan. The opponent's best defensive idea may be to return a pawn, exchange an active rook, or develop with tempo. Use the replay as a calculation exercise: before Rab1 and Nc4, name their intended targets; before Kf1, identify the checking line and confirm the destination is safe.'''),
    ),
    (example('Yudovich–N.N.: coordinate the remaining forces',after(Y0+Y1[:9]),Y1[9:],(
        'White’s rook c1 and queen c2 are active; rook a1 and knight d2 are the reserves. Black’s king is b8.',
        '...Qd7 moves the queen toward defence.', 'Rab1 adds pressure down the b-file toward the king.',
        '...b6 blocks the file but creates a pawn target.', 'Nc4 brings the knight toward b6 and e5.',
        '...Rc8 contests the c-file with Black’s developed rook.', 'Qe4 centralizes the queen and supports further threats.',
        '...Qe6 is the game’s defensive queen placement.', 'Ne5 improves the knight’s central attacking position.',
        '...Qxa2+ takes another pawn, but Black still has to deal with White’s coordinated pieces.',
        'Kf1 answers check. Black resigned in the source game; this position is not itself checkmate.',
    )),),
    'After Black’s Qd7, bring the a1 rook to b1 to add pressure on the king’s file.',
    (('Rab1',True,'The a-rook joins the attack on a new file while the c-rook keeps its job.'),('Rcb1',False,'This moves the already active c-rook and leaves the a1 rook unmobilized.'),('Qd3',False,'A queen move does not bring the specified reserve into play.')),
    (q('reserve','Why choose the a-rook for b1?','It activates a reserve while retaining c-file pressure','The two rooks acquire separate, useful jobs.','The c-rook is unable to move legally','Both rook moves are legal; their practical effects differ.'),
     q('resignation','Does Kf1 end this replay in checkmate?','No; resignation is the recorded game result','A king can resign while legal moves remain.','Yes; every winning game score ends in mate','A recorded result does not change the legal position.')),
    ('A long attack still requires answering every check against your own king.',),
    ('Mobilize reserves with a purpose.', 'Keep existing pressure when adding a new target.', 'Verify the actual ending condition.'),quiz_fen=after(Y0+Y1[:10]))

add('opening-to-middlegame', 'Choose development that supports the coming plan', (372, 373),
    'Hukel–Yudovich shows why completing development is not a separate chore before planning. Black accepts a potentially weak pawn to gain active central play against White’s intended attack.',
    ('Describe the opponent’s intended plan before choosing a move.', 'Balance a structural weakness against concrete activity.'),
    (
        section('Read the position as a contest of plans', '''White has king e1, queen d2, bishops d4/f1, knights c3/f4, and pawns c4/e4/f3 among the remaining army. Black has king g8, queen d8, bishops e6/g7, knights b8/f6, and pawns c6/d6/g6. White wants to castle long, pressure d6, and perhaps advance the kingside pawns against Black's king. Merely saying Black should develop the b8 knight misses the most important question: onto which route can that knight oppose White's plan? The source contrasts a routine Nbd7 setup with the more purposeful central arrangement chosen in the game.'''),
        section('A weakness is one factor in the whole assessment', '''Black plays c5, gaining a tempo against White's bishop d4 and clearing c6 for the b8 knight. After Be3 Nc6 O-O-O, Black continues Nd4. With the c-pawn now on c5, the d6 pawn is backward and may become a target; Black has obtained an active knight on d4 in return. The old c6 pawn did not directly defend d6: black pawns attack one rank downward, so c6 attacked b5 and d5. That knight interrupts White's central coordination and creates tactical possibilities. Do not declare a position bad merely because you can name a backward pawn. Ask whether the opponent can actually attack it safely, whether the defender has counterplay, and what must be exchanged before the weakness can be reached.'''),
        section('Test the tempting simplification', '''White might try Bxd4 cxd4 Qxd4, apparently removing the active knight and winning the new d4 pawn. Black has Nd5: the f6 knight moves with an attack on White's f4 knight while uncovering the g7 bishop's diagonal toward the queen d4. That is a concrete reason why the simple pawn grab is dangerous. The lesson does not require calling every move of the game forced. It requires seeing that an apparently weakened structure can be supported by piece coordination and tactical details. Trace g7–f6–e5–d4 before judging the capture sequence.'''),
        section('Planning begins before castling is complete', '''The main line instead continues h4 h5 Qf2 Nd7. White starts the intended wing play, Black slows the pawn advance, and both sides continue organizing their pieces. The position remains a fight; the source's assessment of counterplay should not be mistaken for a simple forced win. At your level, state one plan for each side before playing a developing move. Then ask whether your candidate makes the opponent's plan easier or harder. An opening is successful when it produces pieces with useful middlegame work, not when you have moved every minor piece once and only then begin to think.'''),
    ),
    (example('Hukel–Yudovich: central counterplay against a planned attack',H,H1,(
        'Black to move on move10. White plans long castling and pressure on d6; Black’s b8 knight needs a useful route.',
        '...c5 attacks the d4 bishop and clears c6 for a knight.', 'Be3 moves the bishop to a central defensive square.',
        '...Nc6 develops toward d4.', 'O-O-O puts White’s king on c1 and rook d1, increasing central pressure.',
        '...Nd4 occupies the useful central square; its tactical support matters more than its appearance alone.',
        'h4 begins White’s kingside pawn play.', '...h5 restrains that pawn route.', 'Qf2 reorganizes the queen behind the attack.',
        '...Nd7 continues Black’s regrouping. Both sides have plans and counterplay.',
    )),example('Test the pawn grab before approving it',after(H1[:5],H),('Bxd4','cxd4','Qxd4','Nd5'),(
        'White considers exchanging the d4 knight and taking the pawn that replaces it.', 'Bxd4 removes the active knight with the bishop.',
        '...cxd4 recaptures toward the centre.', 'Qxd4 takes that pawn, placing the queen on the g7 bishop’s diagonal.',
        '...Nd5 uncovers the bishop’s attack on d4 and attacks the f4 knight. White must respond to the changed tactical situation.',
    ))),
    'After c5 Be3 Nc6 O-O-O, move the c6 knight into the central square d4.',
    (('Nd4',True,'The knight reaches the square around which Black’s central counterplay is organized.'),('Na5',False,'This is a legal knight move but does not occupy the requested central square.'),('Nd7',False,'This moves the f6 knight to d7 rather than occupying d4 with the c6 knight.')),
    (q('weakness','Does a backward d6 pawn automatically decide the game?','No; assess access, activity, and tactical support','The opponent must be able to exploit a weakness.','Yes; one backward pawn always loses','Structural labels do not replace analysis.'),
     q('plan','When should you think about middlegame plans?','While choosing the opening moves','Development squares should support the intended struggle.','Only after every piece has moved','Early choices already shape later possibilities.')),
    ('Inspect the queen’s diagonal before capturing the central pawn.',),
    ('Name both plans.', 'Develop toward useful operations.', 'Balance weaknesses with counterplay.'),quiz_fen=after(H1[:4],H))

add('principle-exceptions', 'When repeated moves serve a concrete purpose', (373, 373),
    'Alekhine’s unusual opening against Rubinstein includes repeated pawn and bishop moves. The lesson is to explain the concrete reason for the exception, then calculate its risks, rather than treating a principle as either an absolute rule or something to ignore.',
    ('Explain why h4–h5 fits this particular position.', 'Distinguish a purposeful repeated move from lost time.'),
    (
        section('Count the moves, then ask what they accomplished', '''In the source game White moves the c-pawn three times, the h-pawn three times, and the c1 bishop four times within thirteen moves. That sounds like a direct violation of efficient development. Yet Black has also spent time on a6 and a knight route e7–g6, while the centre has become relatively fixed. A development count is a clue, not a verdict. The important question is whether the repeated moves attack something important, gain space that can be maintained, or force the opponent to spend comparable time answering them.'''),
        section('The flank push responds to the centre', '''After c5, White's c-pawn gains queenside space; Black challenges that structure with b6. White exchanges on b6, and Black recaptures with the c-pawn. Meanwhile the black knight on g6 eyes useful central squares. White plays h4 and h5, attacking that knight and driving it back to e7 in the game. The push is not just a wish to attack the king: it challenges a piece that contributes to Black's central ambitions. Before copying the pawn march, check whether the centre can open against your own uncastled king and whether the advanced pawns can be captured.'''),
        section('Explain the final arrangement honestly', '''After h6 g6 Bg5 O-O Bf6, White's bishop occupies f6 and the pawn h6 cramps Black's king area. The black g-pawn has moved to g6, so the h6 pawn is not simply capturable by it; pawn direction matters. White's bishop on f6 and pawn h6 restrict important squares. The source regards White's position as highly favorable, but the replay is an opening fragment, not a complete proof of a forced win. White still has a king on e1 and undeveloped kingside pieces, so continued accurate play is required. Advantage does not suspend the need to finish the army's work.'''),
        section('Make an exception earn its place', '''Before moving the same pawn or piece again, finish the sentence: the position requires this because the opponent threatens or permits this specific thing. Then calculate a serious reply. If your reason is only that you remember a famous player doing it, return to the normal development plan. In this example, identify the knight on g6 before h5 and the resulting retreat after it. Compare the concrete gains with White's delayed development. The general principle remains valuable precisely because it gives you a default; an exception is justified by the board's details, not by a dislike of rules.'''),
    ),
    (example('Alekhine–Rubinstein: repeated moves with connected jobs',chess.STARTING_FEN,A,(
        'Track the c-pawn, h-pawn and c1 bishop, then compare their gains with the time spent.',
        'd4 occupies the centre.', '...d5 meets it directly.', 'Nf3 develops.', '...e6 supports d5 and opens the f8 bishop.',
        'c4 challenges d5.', '...a6 prepares queenside space but uses a tempo.', 'c5 gains space and fixes the pawn contact.',
        '...Nc6 develops behind the pawn chain.', 'Bf4 develops outside the e-pawn.', '...Nge7 starts Black’s knight route.',
        'Nc3 develops toward the centre.', '...Ng6 attacks f4 and supports central ambitions.', 'Be3 preserves the bishop and supports the central structure.',
        '...b6 challenges the advanced c5 pawn.', 'cxb6 captures and changes the pawn structure.', '...cxb6 recaptures toward b6.',
        'h4 starts a specific operation against the g6 knight.', '...Bd6 develops the bishop toward the centre.', 'h5 attacks the knight.',
        '...Nge7 is the game’s retreat.', 'h6 gains space beside the black king area.', '...g6 leaves the h6 pawn in place and changes the pawn shield.',
        'Bg5 activates the bishop on a new diagonal.', '...O-O castles into the restricted kingside.', 'Bf6 occupies a strong advanced square. This is the source’s favorable opening endpoint, not checkmate.',
    )),),
    'After h4 Bd6, advance h5 to attack the black knight on g6.',
    (('h5',True,'The pawn attacks the knight, giving the repeated advance a concrete purpose.'),('g3',False,'This does not attack the g6 knight as requested.'),('a3',False,'This queenside move does not carry out the stated h-pawn operation.')),
    (q('exception','What justifies departing from a development guideline?','A concrete benefit that survives the opponent’s reply','Calculate the position instead of using the rule mechanically.','The fact that a famous player once did it','The supporting conditions must also match.'),
     q('remaining','Is White finished developing at Bf6?','No; the king and kingside pieces still require attention','A favorable position still needs accurate continuation.','Yes; an advanced bishop makes all other pieces irrelevant','The whole army remains important.')),
    ('Do not turn an exceptional h-pawn march into a routine plan in every opening.',),
    ('Identify the opponent’s specific idea.', 'Make repeated moves earn time or space.', 'Reassess unfinished development.'),quiz_fen=after(A[:18]))

add('symmetry', 'Copying a move is not the same as answering it', (371, 371),
    'The book warns against mechanical symmetry. Learn the difference between a sound symmetrical opening and copying without checking what White’s extra move makes possible.',
    ('Recognize the tactical cost of copying automatically.', 'Apply the warning without rejecting sound symmetrical positions.'),
    (
        section('White moves first; the position is never perfectly simultaneous', '''When both players put corresponding pieces on matching squares, the board may look balanced. But White has had the first move, and one player must act before the other. If White captures something with a threat, Black cannot assume that the matching capture solves the problem. A move has to answer the actual position after the opponent's move, not the position that existed before it. The book's warning is about initiative and timing: equal-looking arrangements can conceal unequal immediate obligations.'''),
        section('An original example makes the difference concrete', '''After e4 e5 Nf3 Nf6, each knight attacks the opponent's e-pawn. White captures Nxe5. If Black immediately copies with Nxe4, White can play Qe2, attacking the knight on e4 down the e-file. In the sample line Nf6 Nc6+ is a discovered check from the queen on e2 and a knight attack on Black's queen d8. The d7 pawn cannot simply take the knight because that would not answer the check on e8. This particular copying sequence has created a tactical problem, even though the two sides initially appeared to be doing the same thing.'''),
        section('An appropriate answer need not preserve the picture', '''The contrasting replay uses d6 before Black recaptures on e4. The pawn attacks White's knight on e5, and after Nf3, Black plays Nxe4. White no longer has the knight on e5 that produced the discovered-check combination. This is a concrete move-order explanation; it is more useful than a vague claim that symmetry is bad. The Petroff opening begins with symmetrical pawn and knight moves, so the very example also shows why the book's historical warning must not become a prohibition against e5 or d5.'''),
        section('Use a threat check instead of a mirroring habit', '''Before making a matching move, ask whether the opponent has given check, attacked a more valuable piece, opened a line, or created a threat that your move ignores. Then look at their strongest forcing reply. If you can meet it and your move has a useful purpose, a symmetrical setup may be entirely reasonable. At your rating, this check matters much more than choosing an opening solely to avoid symmetry. The exercise asks you to reproduce the pawn move that challenges the advanced knight; it does not claim that every other legal move loses.'''),
    ),
    (example('Original illustration: copying creates a discovered attack',after(('e4','e5','Nf3','Nf6','Nxe5')),('Nxe4','Qe2','Nf6','Nc6+'),(
        'Black to move. White’s knight e5 has captured the e-pawn; compare an immediate matching capture with a challenge to that knight.',
        '...Nxe4 immediately copies the capture.', 'Qe2 attacks the e4 knight along the open e-file.',
        '...Nf6 is the illustrative retreat. White now has a forcing discovered attack.',
        'Nc6+ opens the queen’s check on e8 while the knight attacks queen d8. Black must answer the check.',
    )),example('Original contrast: challenge the knight first',after(('e4','e5','Nf3','Nf6','Nxe5')),('d6','Nf3','Nxe4','d4'),(
        'The starting position is the same. This time Black changes the move order.',
        '...d6 attacks the advanced knight before recapturing.', 'Nf3 retreats and removes the knight from the discovered-attack square e5.',
        '...Nxe4 now recaptures with a different tactical arrangement.', 'd4 claims central space. The game continues; this is not a forced verdict.',
    ))),
    'Challenge White’s e5 knight with the d-pawn before recapturing on e4.',
    (('d6',True,'The pawn attacks e5 and changes the timing of the recapture.'),('Nxe4',False,'This is the immediate copying move in the contrasting example.'),('Nc6',False,'Developing this knight does not make the specified d-pawn challenge.')),
    (q('symmetry','Are all symmetrical openings unsound?','No; concrete timing and threats decide','A useful warning against copying is not a ban on symmetrical development.','Yes; Black must never answer e4 with e5','That turns a contextual warning into a false rule.'),
     q('discovery','What gives check after Nc6+ in the first replay?','The queen on e2 through the cleared e-file','The moving knight simultaneously attacks the queen d8.','The knight on c6 attacks the king e8','A c6 knight does not attack e8; trace the queen’s file.')),
    ('Do not confuse a superficially similar board with identical tactical duties.',),
    ('Read the threat after every move.', 'Check the opponent’s forcing reply.', 'Preserve sound principles, not visual symmetry.'),quiz_fen=after(('e4','e5','Nf3','Nf6','Nxe5')))

add('choose-repertoire', 'Choose a small repertoire you can explain', (373, 376),
    'A repertoire is a manageable set of opening choices and plans. Build one around positions you can understand and review, while keeping tactical awareness more important than remembering an exact move order.',
    ('Distinguish opening family labels from actual pawn structure.', 'Choose a practical scope for opening study.'),
    (
        section('Translate the traditional labels', '''In traditional classification, open games begin e4 e5; semi-open games begin e4 followed by a different Black reply; other first-move families are commonly grouped among closed or flank openings. These names describe families, not a guarantee about the later board. An e4 e5 game can have a blocked centre, and a d4 game can open rapidly after exchanges. An open position, in the structural sense, has accessible lines and relatively little central pawn obstruction. Keep those two meanings separate when deciding which kind of play you want to learn.'''),
        section('Use taste as a starting point, not an excuse', '''The source suggests choosing openings that fit the kind of struggle you enjoy, while giving less experienced players practice in open games with relatively clear development and central ideas. An attacker still has to defend, and a player who enjoys manoeuvring still has to calculate. Avoid choosing a system only because you hope the opponent will fall into a trap. Instead, choose positions whose normal plans you can describe even when the trap is unavailable. Familiarity should help you notice danger rather than make you play the same moves regardless of what the opponent does.'''),
        section('Make the repertoire small enough to revisit', '''For a beginner, a useful study unit is one White starting approach and a simple response plan to each common first-move family as Black. Expand gradually when your own games expose a recurring gap. The book recommends limiting the number of openings under active study and playing them repeatedly to gain experience. That is a study method, not a demand to learn every branch before playing. Record the main central break, the usual development squares, the king-safety plan, and one tactical warning for each setup. A page of explanations is more usable than pages of unexplained moves.'''),
        section('Practise a normal position before a clever exception', '''The original replay uses an Italian-style development: e4 e5 Nf3 Nc6 Bc4 Bc5 d3 Nf6 O-O. Both sides develop and White chooses a supported centre before castling. There are other good plans and other move orders. Here the task is to explain what each move does and what still needs work: White's b1 knight and c1 bishop, Black's king safety, and possible future central changes. If Black chooses something unfamiliar, return to those jobs and to the immediate threats. Do not force a remembered setup onto a board where its assumptions have changed.'''),
    ),
    (example('Original study model: develop, support the centre, and castle',chess.STARTING_FEN,('e4','e5','Nf3','Nc6','Bc4','Bc5','d3','Nf6','O-O'),(
        'Use this short line to practise explaining jobs, not to memorize a compulsory sequence.',
        'e4 occupies the centre and opens the f1 bishop.', '...e5 does the corresponding central work.',
        'Nf3 develops with an attack on e5.', '...Nc6 develops while defending e5.', 'Bc4 develops toward f7.',
        '...Bc5 develops toward f2.', 'd3 supports e4 and opens the c1 bishop’s route.', '...Nf6 develops with pressure on e4.',
        'O-O places the king behind its kingside pawns and activates the rook toward central files.',
    )),),
    'After the displayed development, castle kingside to carry out White’s king-safety plan.',
    (('O-O',True,'The king leaves the centre and the h-rook joins the inner files.'),('h3',False,'This legal pawn move does not carry out the requested castle.'),('Nc3',False,'This develops a knight but postpones the specific king-safety operation.')),
    (q('labels','Does the label open game guarantee an open centre forever?','No; later pawn choices determine the actual structure','Family names and structural descriptions are related but distinct.','Yes; e4 e5 prevents blocked pawn chains','Subsequent pawn moves can close central lines.'),
     q('scope','What makes a small repertoire useful?','Repeated experience with plans you can explain','Review reveals typical problems and exceptions.','Never thinking after the opponent’s first move','The actual position still controls every decision.')),
    ('Do not judge an opening solely by a trap or by who currently plays it.',),
    ('Choose positions you want to understand.', 'Keep the initial scope manageable.', 'Review your own unfamiliar replies.'),quiz_fen=after(('e4','e5','Nf3','Nc6','Bc4','Bc5','d3','Nf6')))

add('changing-theory', 'Opening evaluations are arguments that can be improved', (374, 374),
    'The French Defence example shows how a persuasive-looking criticism can be revised. Learn to test an evaluation against the whole position and concrete replies, rather than treating a book’s verdict as permanent.',
    ('Explain the purpose of Bb4 in the French structure.', 'Distinguish a historical assessment from a timeless rule.'),
    (
        section('Understand the position before its reputation', '''After e4 e6 d4 d5 Nc3, Black's d5 pawn attacks e4 and White's c3 knight helps defend that pawn. Bb4 develops the bishop and pins the knight to the king e1 along b4–c3–d2–e1. The pin has a purpose: it can make the support of e4 less secure and may allow Black to damage the queenside pawns by exchanging on c3. It also gives White choices about the centre and the bishop pair. These concrete features are the substance of the position, whatever reputation a particular era assigned to the move.'''),
        section('A reasonable criticism can still be incomplete', '''The source describes an early assessment that called Bb4 weak because White could exchange on d5 and develop Bd3, after which the black bishop might lose time or give up the bishop pair. Those are real factors to inspect. But a verdict based on only those factors can omit Black's development, central play, and the possibility that the resulting position is playable. The chapter uses later practical experience to show that the original dismissal was too confident. We are studying that change in reasoning, not presenting an unverified claim about the most fashionable line today.'''),
        section('Compare two structures rather than two slogans', '''In the exchange illustration, exd5 exd5 removes the e-pawns and leaves central d-pawns opposed. Bd3 and Nf6 then develop normally. In the advance illustration, e5 gains space and creates a d4/e5 chain; c5 attacks its base on d4. These positions require different plans even though both began with the same three moves. Look at open lines, central breaks, and the role of each bishop. The replay does not prove either side has a forced advantage. It shows why an evaluation must say which structure and which continuation it is discussing.'''),
        section('Be precise when disagreeing with an authority', '''If a book says White is better, ask what feature creates the advantage and what Black's best defensive idea might be. A move being legal does not refute the book, and a short engine number does not explain the position. Try a concrete alternative, follow the strongest response, and compare the endpoint. Keep a note of what changed in the reasoning: perhaps a development tempo was recovered, a pawn break was overlooked, or a bishop found a useful new diagonal. Intellectual independence means checking carefully, not automatically taking the opposite side of every published verdict.'''),
    ),
    (example('French illustration: exchange changes the central problem',after(('e4','e6','d4','d5','Nc3')),('Bb4','exd5','exd5','Bd3','Nf6'),(
        'Black to move. White’s c3 knight helps e4, and the king remains e1.',
        '...Bb4 pins the c3 knight along the diagonal to the king.', 'exd5 chooses a central exchange.',
        '...exd5 recaptures and opens the c8 bishop’s diagonal.', 'Bd3 develops toward the kingside.',
        '...Nf6 develops. Assess the resulting whole position rather than assuming Bb4 has already been refuted.',
    )),example('French contrast: a pawn chain calls for a different plan',after(('e4','e6','d4','d5','Nc3','Bb4')),('e5','c5','a3','Bxc3+','bxc3'),(
        'White can choose space instead of exchanging on d5.', 'e5 establishes the advanced end of White’s central pawn chain.',
        '...c5 attacks the chain’s base on d4.', 'a3 asks the b4 bishop to decide.', '...Bxc3+ trades bishop for knight with check.',
        'bxc3 recaptures. White keeps two bishops but has altered queenside pawns; both features matter.',
    ))),
    'After the French setup e4 e6 d4 d5 Nc3, pin the c3 knight with the bishop.',
    (('Bb4',True,'The bishop develops on the diagonal through c3 toward king e1.'),('Nf6',False,'This develops a knight but does not make the specified bishop pin.'),('c5',False,'This challenges the centre without making the requested pin.')),
    (q('evaluation','What should support a positional verdict?','Concrete features and tested replies','A label alone does not explain why one side is preferable.','The age or fame of the printed sentence','Authority can guide study but cannot replace the position.'),
     q('structure','Why compare exd5 with e5?','They produce different central structures and plans','The same opening name can lead to different strategic problems.','They leave every pawn on the same square','One exchanges central pawns; the other fixes an advanced chain.')),
    ('Historical discussion of a line’s reputation is not a current opening ranking.',),
    ('Find the move’s concrete purpose.', 'Compare structures at the endpoint.', 'Treat evaluations as reasoned, revisable claims.'),quiz_fen=after(('e4','e6','d4','d5','Nc3')))

add('ruy-centre', 'The Open Ruy Lopez: the centre explains the variation', (374, 375),
    'Before following the chapter’s long theoretical debate, reconstruct its starting position. The central exchanges and the d-file explain why Qe2, Rd1, and c4 belong to one connected idea.',
    ('Track which central pawns have been exchanged.', 'Explain the purpose of the Qe2–Rd1–c4 plan.'),
    (
        section('Build the position without losing track of the pawns', '''After e4 e5 Nf3 Nc6 Bb5 a6 Ba4 Nf6 O-O Nxe4, Black has taken White's e-pawn. White plays d4, challenging the centre instead of immediately chasing the knight. Following b5 Bb3 d5 dxe5 Be6, White's original d-pawn now stands on e5 and Black's original e-pawn has disappeared. Black's d-pawn stands on d5, supported by pieces. Saying White has a pawn on e5 is not enough: knowing which pawn it is explains why the d-file has become available for a rook.'''),
        section('Compare a structural move with a piece plan', '''The source first mentions c3, which controls d4 and gives the b3 bishop a retreat on c2. It then explores Qe2, preparing Rd1. Moving the queen off d1 makes room for the rook to pressure the central d-pawn and the queen behind it. The plan is not a mysterious sequence: the exchanged white d-pawn has cleared the file, and White wants to use that file before Black completes development. Black must therefore consider both central defence and the speed with which the f8 bishop and king can become active and safe.'''),
        section('The bishop exchange creates a new pawn lever', '''In the illustrative source branch Qe2 Nc5 Rd1 Nxb3 axb3 Be7 c4, Black exchanges the c5 knight for White's bishop b3. White's a-pawn recaptures onto b3, so it can support a later pawn on c4. The c2 pawn then advances to c4, challenging the d5 pawn. If that pawn moves, the d-file pressure changes; if it remains, the centre becomes a focus of contact. Each move changes the conditions for the next. The point is not that accepting doubled b-pawns always helps, but that structural changes can support an active operation.'''),
        section('Keep the opponent in the explanation', '''Black's knight attack on b3 is a useful idea, yet the timing of Nc5 matters because Black also needs to finish development. The next lesson compares Be7 first, after which a different exchange sequence appears. Stop this replay after c4 and name both sides' tasks rather than declaring the entire opening solved. White seeks active central files; Black seeks consolidation and counterplay. At 564, following these relationships accurately is the essential achievement. Memorizing a long branch before you can identify the d5 target will make the later tactical debate harder to understand.'''),
    ),
    (example('Open Ruy Lopez: how the central starting position arises',chess.STARTING_FEN,L0,(
        'Track White’s d-pawn and the two e-pawns as the central structure changes.',
        'e4 occupies the centre.', '...e5 answers centrally.', 'Nf3 attacks e5.', '...Nc6 defends e5 and develops.',
        'Bb5 pressures the defender c6.', '...a6 asks the bishop to decide.', 'Ba4 preserves the bishop.', '...Nf6 attacks e4.',
        'O-O secures the king before the central exchanges.', '...Nxe4 takes the e-pawn.', 'd4 challenges the centre and opens the c1 bishop.',
        '...b5 gains queenside space with an attack on the bishop.', 'Bb3 retreats to an active diagonal.', '...d5 supports central occupation.',
        'dxe5 exchanges White’s d-pawn for Black’s e-pawn.', '...Be6 develops and supports d5. White’s d-file is now available for a rook plan.',
    )),example('Source branch: use the d-file and then challenge d5',after(L0),('Qe2','Nc5','Rd1','Nxb3','axb3','Be7','c4'),(
        'White has pawn e5 and an open path on the d-file; Black has pawn d5 and knight e4.',
        'Qe2 clears d1 for the rook.', '...Nc5 attacks the b3 bishop.', 'Rd1 pressures the central file.',
        '...Nxb3 exchanges for the bishop.', 'axb3 changes the queenside structure and supports c4.',
        '...Be7 develops the kingside bishop.', 'c4 challenges d5. This endpoint illustrates the central plan, not a forced final verdict.',
    ))),
    'From the Open Ruy Lopez starting position, clear d1 for a rook by placing the queen on e2.',
    (('Qe2',True,'The queen vacates the square needed for Rd1.'),('c3',False,'This is a sensible different source plan, but does not make the requested queen move.'),('a3',False,'This does not clear d1 or carry out the demonstrated central piece plan.')),
    (q('pawn','Which white pawn occupies e5 after dxe5?','The pawn that began on d2','White’s original e-pawn was taken by the knight.','White’s original e-pawn','Track the preceding Nxe4 and dxe5 captures.'),
     q('lever','What is c4 trying to challenge?','Black’s pawn on d5','The central contact connects to the rook’s d-file pressure.','A black pawn on h7','The operation is central rather than a direct kingside pawn attack.')),
    ('Do not recite the variation without reconstructing its pawn changes.',),
    ('Track the origin of exchanged pawns.', 'Connect queen and rook development.', 'Identify the central lever.'),quiz_fen=after(L0))
add('move-order', 'The same idea can change when development comes first', (374, 375),
    'Compare Black’s immediate Nc5 with Be7 first. The source uses this adjustment to show that opening investigation is a sequence of problems and improvements, rather than a fixed string of moves.',
    ('Identify why developing before exchanging can matter.', 'Follow the central exchange into a new middlegame problem.'),
    (
        section('A move order is a set of temporary permissions', '''Two variations may contain many of the same moves but allow different replies between them. After Qe2 in the Open Ruy Lopez, immediate Nc5 attacks the bishop b3 but leaves Black's f8 bishop at home. The earlier lesson showed a branch where White exchanges on b3 and challenges d5 with c4. Playing Be7 first attends to development and clears the king's castling route. It does not magically solve every central problem. It changes what Black has already achieved when White starts the next operation.'''),
        section('Why the bishop can take d5', '''After Qe2 Be7 Rd1 Nc5, White plays Bxd5. The bishop from b3 travels through c4 to capture the pawn d5. In the displayed line Black answers Bxd5 with the bishop from e6. White develops Nc3, attacking that bishop on d5. The sequence exchanges a central pawn and an attacking bishop for a new development tempo. Follow both bishops carefully: White's b3 bishop is gone, and Black's e6 bishop is now d5. If you imagine the original pieces still in place, the later manoeuvres will make little sense.'''),
        section('The endpoint is a new question, not a finished opening', '''At the position after Nc3, Black has the bishop d5 under attack, knights c5 and c6, and an uncastled king e8. White has rook d1, queen e2, and knights c3 and f3. The source now compares active replies such as Nb4 and Bc4. These are not interchangeable. A bishop retreat, a knight operation, and a rook exchange create different threats against White's back rank. Opening study becomes useful when you can stop here and describe those possibilities instead of relying on an evaluation symbol at the end of a printed line.'''),
        section('Study the difference one tempo at a time', '''Place the earlier position and this one on the board in turn. Ask which piece has developed, which pawn disappeared, and whose valuable piece is attacked now. Then calculate the next forcing reply. A development move can be an improvement because it prepares castling or makes a later capture possible, but you should name the actual mechanism rather than calling every developing move automatically good. The exercise deliberately asks for Be7's specific job. It does not certify that a single response settles the theoretical evaluation of the whole opening.'''),
    ),
    (example('Source improvement: develop before the knight operation',after(L0),L1[:7],(
        'White to move after Be6. Compare this development-first branch with the earlier immediate Nc5 line.',
        'Qe2 prepares the d-file rook.', '...Be7 develops the bishop and clears f8 for castling.',
        'Rd1 occupies the central file.', '...Nc5 attacks the bishop b3.', 'Bxd5 captures the d5 pawn with that bishop.',
        '...Bxd5 recaptures with the e6 bishop.', 'Nc3 develops with an attack on d5. The position requires a fresh calculation.',
    )),),
    'After Qe2, develop the f8 bishop to e7 before beginning the Nc5 operation.',
    (('Be7',True,'The bishop develops and clears a square needed for castling.'),('Nc5',False,'This is the earlier immediate knight operation, not the development-first move.'),('h6',False,'This does not develop the f8 bishop.')),
    (q('order','Why can exchanging the order of two moves matter?','The opponent gets a reply between them','Temporary threats and permissions can change the continuation.','The position ignores all intermediate moves','Only the actual sequence determines which replies were available.'),
     q('endpoint','What does Nc3 attack at the end of this replay?','The black bishop on d5','The e6 bishop recaptured there after White’s Bxd5.','A white bishop still on b3','That bishop has already been exchanged.')),
    ('Rebuild the board after every capture; do not retain pieces mentally after they are gone.',),
    ('Name the benefit of the extra development.', 'Track the exchanged bishops.', 'Reassess at the new critical position.'),quiz_fen=after(L0+['Qe2']))

add('active-defence', 'Defend first when a tempting attack ignores a threat', (375, 375),
    'After Black’s Nb4, the natural a3 attacks the knight but can allow a dangerous initiative. Compare it with Ne1, which prepares the back rank before White asks the knight to move.',
    ('Recognize a defensive move with an active future purpose.', 'Compare the consequences of a3 before and after preparation.'),
    (
        section('Locate the forces behind the threat', '''Start after Qe2 Be7 Rd1 Nc5 Bxd5 Bxd5 Nc3, and let Black play Nb4 with the c6 knight. White's queen is on e2, king on g1, rook on d1, and other rook on a1 behind a bishop c1. Black's bishop d5 can reach c4 with an attack on the queen e2. The black queen remains d8. The important relationships are the d-file exchanges and the accessibility of White's back rank. An attacked knight on b4 is only one feature of this position.'''),
        section('Why attacking the knight may be premature', '''In the source's warning branch, a3 Bc4 Rxd8+ Rxd8 leaves Black's rook on the open d-file, a knight on b4, and the bishop c4 attacking White's queen. The a3 pawn has spent a move on a knight question while Black has generated a more urgent sequence. This is an example of initiative: one side's threats force the other to respond before carrying out the original plan. The replay stops at a position the source judges dangerous for White. It does not claim that an immediate mate has been demonstrated or that every reply was forced.'''),
        section('Prepare the king’s back rank before gaining space', '''The source's improved line is Ne1, using the f3 knight, followed by c6 a3. The knight on e1 helps meet pressure on the back rank and changes the tactical conditions under which White can challenge b4. Moving a developed knight backward may look passive, but a retreat can be useful if it removes a tactical obstacle to the next plan. Compare the two boards after a3: the white knight and Black's c-pawn are on different squares, so the superficially identical pawn move occurs in a different position.'''),
        section('Make a quiet move explainable', '''Before a quiet defensive move, say what forcing continuation worried you and how the move changes it. Do not justify a retreat only by saying the book recommends it. Here you should identify the bishop's route to c4, the pressure on queen e2, and the d-file. Then replay the prepared a3 line and describe the new defensive arrangement. In your own games, a threat against one enemy piece is not enough if the opponent can ignore it with check, a queen attack, or a stronger tactical threat. Choose the order that leaves your own position able to withstand the reply.'''),
    ),
    (example('Source defence: prepare before challenging the knight',after(L0+L1[:7]),('Nb4','Ne1','c6','a3'),(
        'Black to move after Nc3. The bishop d5 is attacked, and the d-file is tactically important.',
        '...Nb4 brings the c6 knight toward White’s queenside and central entry squares.',
        'Ne1 moves the f3 knight back to prepare against back-rank pressure.',
        '...c6 supports Black’s central arrangement.', 'a3 now challenges b4 after the defensive preparation. Assess this board separately from the immediate-a3 branch.',
    )),example('Source warning: the immediate pawn question is not the whole story',after(L0+L1[:7]),('Nb4','a3','Bc4','Rxd8+','Rxd8'),(
        'Reset to the same position so that the move-order comparison is fair.',
        '...Nb4 makes the knight look like a convenient pawn target.', 'a3 attacks that knight immediately.',
        '...Bc4 attacks queen e2 and preserves active threats.', 'Rxd8+ takes Black’s queen with check.',
        '...Rxd8 recaptures with the a8 rook. Black has an active initiative; this is an assessment point, not a mate endpoint.',
    ))),
    'After Nb4, make the source’s preparatory knight retreat to e1 before playing a3.',
    (('Ne1',True,'The f3 knight repositions before the pawn challenge.'),('a3',False,'This is the premature order examined in the warning branch.'),('h3',False,'This legal pawn move does not perform the requested defensive regrouping.')),
    (q('priority','Why can attacking the b4 knight fail to settle the position?','Black may create a stronger threat against the queen or king','Compare forcing replies before assuming the knight must retreat.','An attacked knight is legally required to move','Only check imposes a compulsory obligation to protect the king.'),
     q('retreat','Can moving a developed piece backward help an active plan?','Yes, when it removes a concrete tactical problem','A useful retreat can make the next operation possible.','No, every backward move wastes a tempo','Direction alone does not determine usefulness.')),
    ('The displayed defensive line is representative analysis, not a claim that Black has only one reply.',),
    ('Inspect threats against your queen and king.', 'Prepare the back rank.', 'Compare endpoints, not just move names.'),quiz_fen=after(L0+L1[:7]+['Nb4']))

add('creative-defence', 'A threat can be answered by changing the whole position', (375, 375),
    'The surprising b3 answers an attack on the c3 knight without moving it. Learn the exact defensive and attacking changes that make the idea intelligible.',
    ('Explain the b3–Ba3 idea through concrete squares.', 'Distinguish a counter-threat from ignoring a threat without calculation.'),
    (
        section('Why the obvious retreat is not the only candidate', '''The source reaches Qe3 b4 after the d-file exchanges. Black's pawn b4 attacks White's knight c3, and the rook d8 has access toward d1. White's bishop c1 blocks the a1 rook from protecting d1 along the first rank. The immediate retreat Ne4 seems natural, but the source examines Rd1+ Ne1 Nd4 as an active reply. Instead of deciding that an attacked knight must move, White looks for a way to alter the threats and the back-rank arrangement at the same time.'''),
        section('Read b3 as more than a pawn move', '''White plays b3. The b-pawn attacks Black's bishop c4 and vacates b2, opening a route from c1 to a3 for the white bishop. Black's pawn on b4 can still take the knight on c3; b3 has not physically defended it. The point is the continuation after that capture. A counter-threat is justified only if the resulting position supplies enough concrete activity or recovery. The book's line gives a way to see the mechanism rather than asking you to trust the appearance of a clever move.'''),
        section('After the capture, name the two separate attackers', '''If Black plays bxc3, White answers Ba3. The white bishop on a3 attacks the black knight c5 along a3–b4–c5. Separately, White's pawn b3 still attacks the black bishop c4. These are two attacks by two different pieces; the a3 bishop does not attack both targets by itself. Moving the bishop away from c1 also clears the a1 rook's line to d1. That is why the back-rank invasion no longer has the same force. The change in defence is as important as the visible attacks.'''),
        section('A good defence can make the opponent change plans', '''The historical continuation does not accept the knight with bxc3. Black instead retreats the attacked bishop to e6, and the struggle develops through another sharp branch. This is a useful lesson about successful defensive ideas: their effect may be to prevent a tempting continuation, not to force the opponent into it. When studying b3, replay the capture branch to understand the threat and then the bishop-retreat branch to see the actual resistance. In your own games, consider a counter-threat only after calculating the capture you appear to permit and checking your king's safety throughout.'''),
    ),
    (example('Source idea: b3 opens a route and creates a threat',after(L0+L1[:11]),('b4','b3','bxc3','Ba3'),(
        'Black to move after Qe3. White’s bishop c1 obstructs the a1 rook along the first rank.',
        '...b4 attacks the c3 knight.', 'b3 attacks bishop c4 and clears b2 for the bishop’s route.',
        '...bxc3 accepts the knight. This is the illustrative capture branch, not the later game continuation.',
        'Ba3 attacks knight c5, while pawn b3 attacks bishop c4. Vacating c1 also lets rook a1 protect d1.',
    )),example('Source resistance: decline the knight and preserve the bishop',after(L0+L1[:-1]),('b3','Be6','Ne4'),(
        'White to move after b4. The knight c3 is attacked.', 'b3 poses a new question to the bishop c4.',
        '...Be6 preserves that bishop instead of taking the knight.', 'Ne4 repositions the knight. The following lesson examines the sharp continuation.',
    ))),
    'After Black’s b4 attacks the knight, play b3 to attack the c4 bishop and clear b2.',
    (('b3',True,'This move creates a counter-threat and prepares the Ba3 resource.'),('Ne4',False,'This is the immediate retreat contrasted with the requested resource.'),('a3',False,'This does not attack bishop c4 with the b-pawn or clear b2.')),
    (q('two-targets','After bxc3 Ba3, which pieces attack the two targets?','Bishop a3 attacks knight c5; pawn b3 attacks bishop c4','Trace each attacker’s own movement rather than giving the bishop an impossible diagonal.','The a3 bishop attacks both c5 and c4','The square c4 is not on a diagonal from a3.'),
     q('rank','Why does moving the c1 bishop help the back rank?','It clears the a1 rook’s line toward d1','The rook gains defensive access along a1–b1–c1–d1.','It makes the white king immune to checks','The king is never exempt from the normal check rules.')),
    ('An undefended knight is not safe merely because you have a counter-threat; verify the continuation.',),
    ('Look for a change to the whole arrangement.', 'Name each actual attacker.', 'Include the new defensive line in your explanation.'),quiz_fen=after(L0+L1[:-1]))

add('compensation', 'Evaluate a queen imbalance by counting and coordinating', (375, 376),
    'The source’s queen-for-pieces struggle is an advanced example of objective evaluation. Track the exchanges carefully, then compare activity, king safety, and targets instead of letting the queen’s presence decide the result.',
    ('Reconstruct the material after a long exchange sequence.', 'Separate numerical material from usable coordination.'),
    (
        section('Do not carry an old material count into a new position', '''Earlier, Black allowed White's rook to capture the queen on d8. That does not mean White now has an extra queen without cost. Black's rook and minor pieces generate threats against White's remaining pieces. From the position after b3, the game continues Be6 Ne4 Rd1+ Ne1 Nd4 Bb2 Nxc2 Qe2 Rxa1 Bxa1 Nxa1. White loses the a1 rook and the bishop that recaptures there, while Black's invading rook is exchanged. Pause after each capture and remove the piece mentally as well as visually.'''),
        section('Follow the remaining exchanges to a stable inventory', '''Next comes Nxc5 Bxc5: White's knight from e4 captures Black's c5 knight, and the black e7 bishop recaptures. White's remaining knight travels from e1 to d3, attacks the c5 bishop, then captures b4 after the bishop retreats to b6. Following castling, Nc6 f6 h4, White has queen and knight, while Black has rook, two bishops, and knight. White has six pawns to Black's five. The shared knight can be set aside for a rough comparison, leaving queen against rook and two bishops, with White an extra pawn. Such arithmetic is a starting inventory, not an evaluation by itself.'''),
        section('Ask how the pieces can work together', '''A queen is especially effective when she can combine checks with attacks on exposed pieces or pawns. A rook and bishops can be very strong when they coordinate, keep the king safe, and avoid loose targets. In this position Black's knight on a1 is far from the kingside struggle, while the bishops and rook have active possibilities. White's queen needs access and the knight c6 helps create pressure. Count not only the nominal value but the routes, targets, and immediate tactical obligations. The book presents this as a disputed analytical position, so a confident verdict based only on piece values would miss the lesson.'''),
        section('Make the practical task smaller than the whole theory', '''At 564, your first goal is to finish the replay with the correct inventory and explain why the material is unusual. Your second is to identify one active plan for each side. White can use queen checks and the advanced e-pawn; Black can coordinate the rook and bishops and challenge that pawn with f6. The final h4 prepares a later advance, whose significance appears in the next lesson. You are not expected to solve the entire queen-versus-pieces position in one exercise. Accurate reconstruction and concrete candidate moves are the foundations that make deeper analysis possible.'''),
    ),
    (example('Boleslavsky–Karaklajic: count every exchange before judging',after(L0+L1),L2,(
        'Black to move after b3. Black’s queen is already gone, but the active pieces threaten White’s first rank.',
        '...Be6 saves the attacked bishop.', 'Ne4 repositions the c3 knight.', '...Rd1+ invades with check.',
        'Ne1 blocks the check with the f3 knight.', '...Nd4 brings the c6 knight into the attack.',
        'Bb2 develops the c1 bishop and opens the first rank.', '...Nxc2 attacks the rook a1 while taking a pawn.',
        'Qe2 repositions the queen.', '...Rxa1 takes the rook.', 'Bxa1 recaptures with the b2 bishop.',
        '...Nxa1 takes that bishop. Update both sides’ material before continuing.', 'Nxc5 takes Black’s c5 knight with the e4 knight.',
        '...Bxc5 recaptures with the e7 bishop.', 'Nd3 activates the remaining white knight with an attack on that bishop.',
        '...Bb6 preserves the bishop.', 'Nxb4 removes the advanced b-pawn.', '...O-O secures the king and places the remaining rook on f8.',
        'Nc6 improves the knight’s activity.', '...f6 challenges White’s e5 pawn.',
        'h4 is the game’s refinement. White has Q+N and six pawns; Black has R+two bishops+N and five pawns.',
    )),),
    'After Bxc5, activate White’s remaining e1 knight by moving it to d3 with an attack on the bishop.',
    (('Nd3',True,'The knight leaves the back rank and attacks bishop c5.'),('Nf3',False,'This activates the knight but does not make the specified attack on c5.'),('h3',False,'This pawn move leaves the knight on e1.')),
    (q('inventory','At the replay’s final h4 position, what does Black have besides pawns and king?','A rook, two bishops, and a knight','The queen and one rook were exchanged; both bishops and the a1 knight remain.','Only a rook and one bishop','That count misses a bishop and the knight on a1.'),
     q('value','Does having the queen alone prove White is winning?','No; compare the full material and its activity','Coordination, targets, king safety, and concrete tactics all matter.','Yes; a queen always defeats any group of pieces','Several coordinated pieces can provide substantial compensation.')),
    ('The book’s disputed position cannot be reduced to a single piece-value slogan.',),
    ('Update the count after every capture.', 'Locate pieces that are far from the action.', 'Evaluate coordination and king safety.'),quiz_fen=after(L0+L1+L2[:13]))

add('refine-analysis', 'An improvement starts another investigation', (376, 376),
    'The h4 improvement and Black’s later defensive revision show how theory develops. One successful game establishes an idea worth studying, but does not prove that every defence has been refuted.',
    ('Explain how h4 prepares a later useful tempo.', 'Compare a successful game continuation with a different defensive branch.'),
    (
        section('Why one pawn square may matter several moves later', '''At the position after Nc6 f6, earlier games had used h3. Boleslavsky chose h4. The point is not simply that advancing farther is stronger. In the later game sequence the pawn reaches h5, where it helps White's attacking arrangement while the queen maintains threats. Starting on h4 makes that further advance available in one move. A small opening refinement can therefore be justified by a much later position, but you must follow the connection rather than assume that every extra pawn tempo improves a king attack.'''),
        section('Follow the successful game with the defence still visible', '''The game proceeds Kh8 Kh2 Bd7 exf6 Bxc6 Qe7 Rg8 fxg7+ Rxg7 Qf8+ Rg8 Qf6+ Rg7 h5 Kg8 Qxc6 Rf7 Qc3. White uses queen checks and pawn pressure before recovering the bishop on c6. The final position is not checkmate; the source reports that White won later. It also identifies Bg8 rather than Bd7 as a defensive improvement earlier in the line. That qualification matters: a successful demonstration against one continuation is evidence of an idea, not proof that all Black's play was unavoidable.'''),
        section('A later game asks a different question', '''The source then gives Suetin–Geller, where Black answers h4 immediately with fxe5. After Nxe5 Rf6 g4 Bxf2+ Kh1 Bxh4, the players eventually drew. The replay ends at the opening of a new struggle, not at a position with an immediate draw claim. Black has chosen a different way to coordinate and capture pawns, so the earlier winning continuation cannot simply be pasted onto this board. To compare the branches, identify which white pawn was exchanged, where the knight stands, and which bishop now attacks on the kingside.'''),
        section('Use uncertainty productively', '''When two plausible lines produce different practical results, write down what you know and what still needs analysis. You can know that h4 has a concrete future purpose without knowing the final best-play verdict of the whole variation. You can also know that a defensive alternative deserves attention without claiming it forces a draw. This is the habit the chapter wants to teach: propose, test, revise, and test again. In your own games, choose one critical opening decision to investigate carefully, include the opponent's strongest reply, and stop with a clear positional explanation rather than a false declaration that the opening has been solved.'''),
    ),
    (example('Boleslavsky–Karaklajic: the h-pawn’s later job',after(L0+L1+L2),L3,(
        'Black to move after h4. Keep track of the white e-pawn, knight c6, and the h-pawn’s next advance.',
        '...Kh8 steps off the first checking lines.', 'Kh2 improves the white king’s position.',
        '...Bd7 is the game move; the source prefers Bg8 as an improvement.', 'exf6 captures the f6 pawn with White’s e-pawn.',
        '...Bxc6 takes the knight with the d7 bishop.', 'Qe7 activates the queen against Black’s defensive arrangement.',
        '...Rg8 reorganizes the rook.', 'fxg7+ captures with check.', '...Rxg7 removes that pawn.',
        'Qf8+ forces a king-safety response.', '...Rg8 blocks the check.', 'Qf6+ gives another check.',
        '...Rg7 again interposes.', 'h5 makes use of the earlier h4 tempo.', '...Kg8 is the game’s king move.',
        'Qxc6 recovers the bishop on c6.', '...Rf7 repositions the rook.',
        'Qc3 centralizes along the diagonal. White won later in the source game; this position itself is not mate.',
    )),example('Suetin–Geller: a different defence keeps the inquiry open',after(L0+L1+L2),('fxe5','Nxe5','Rf6','g4','Bxf2+','Kh1','Bxh4'),(
        'Reset to the same h4 position. Black now challenges the centre immediately.',
        '...fxe5 removes the e5 pawn.', 'Nxe5 recaptures and changes the knight’s attacking route.',
        '...Rf6 activates the rook on the sixth rank.', 'g4 gains space but creates new tactical contact.',
        '...Bxf2+ takes a pawn with check.', 'Kh1 answers the check.',
        '...Bxh4 takes the h-pawn. The source game eventually drew; there is no immediate draw claim here.',
    ))),
    'At the position before h4, advance the h-pawn two squares to prepare the later h5 idea.',
    (('h4',True,'The pawn reaches h4 in one move, preparing h5 in the later line.'),('h3',False,'This was the earlier version; it needs another move to reach h4.'),('a3',False,'This does not prepare the stated kingside pawn advance.')),
    (q('proof','Does White’s win prove the whole Black opening is refuted?','No; alternative defensive moves must be tested','The source itself proposes improvements and shows another game.','Yes; one loss settles every variation','A result belongs to the moves actually played.'),
     q('draw','What does the eventual draw in the second game establish here?','That the historical game was drawn after further play','The displayed endpoint is not automatically a claimable draw.','That the current board has insufficient material','Both sides have ample mating material; the game continued.')),
    ('Keep a game result distinct from an immediate legal ending or a proven best-play verdict.',),
    ('Explain the later purpose of a refinement.', 'Search for stronger defensive choices.', 'Separate known facts from unresolved evaluation.'),quiz_fen=after(L0+L1+L2[:-1]))

add('study-method', 'Turn an opening line into understanding you can use', (376, 376),
    'Finish the chapter with a repeatable study routine: reconstruct the position, explain the moves, test an alternative, and connect the result to your own games. Opening knowledge grows from careful comparison and practical experience.',
    ('Study a short variation with reasons and an endpoint assessment.', 'Use one game mistake to choose the next focused review.'),
    (
        section('Study one meaningful position slowly', '''Choose a position that has appeared in your games or belongs to a small opening repertoire you are building. Put it on the board and identify material, king safety, central pawns, active pieces, and immediate threats. Play a short continuation, stopping after each move to explain its purpose and the opponent's next question. The source warns against racing through opening after opening. Fast familiarity with the move names can feel like progress while leaving you unable to explain the first unfamiliar reply.'''),
        section('Test the explanation with an alternative', '''Return to a critical point and ask what happens if the opponent chooses another sensible move. Prefer a forcing response or a direct challenge to your stated plan. If the intended move no longer works, identify the condition that failed. In the original French illustration, White's e5 fixes a pawn chain based on d4, and Black's c5 attacks that base. After c3, Nc6 increases pressure on d4. White then develops Nf3. These are understandable jobs; the line is a study model, not an assertion that those are the only legal or best moves.'''),
        section('Write an endpoint assessment in ordinary language', '''Instead of copying a symbol that says White is better, explain where each side can play. In our example White has space on e5 and a supported d4 pawn, while Black attacks the centre with c5 and Nc6 and still needs kingside development. White must finish development and protect the centre; Black must increase pressure without neglecting king safety. A useful assessment includes both sides' resources, the important weakness or target, and the next operation. If you cannot explain the verdict, that is the place to study more, not a reason to memorize a longer branch.'''),
        section('Bring the lesson back to your own games', '''After playing, find the first move where your understanding stopped helping. Was a piece left undefended, a central break overlooked, or a plan followed after its conditions changed? Reconstruct that decision and write one correction with a short supporting line. Review it again after a few days without seeing the answer. Over time, the notebook becomes a collection of reasons connected to actual experience. At 564, finishing development, answering threats, and keeping pieces safe remain essential even inside a familiar opening. The aim of this chapter is independent, accurate thinking—not an obligation to reproduce advanced historical analysis from memory.'''),
    ),
    (example('Original review drill: explain a pawn-chain attack',after(('e4','e6','d4','d5','e5')),('c5','c3','Nc6','Nf3'),(
        'Black to move. White has a pawn chain d4–e5, so identify its base before choosing a break.',
        '...c5 attacks the base d4 and creates central contact.', 'c3 supports d4 with another pawn.',
        '...Nc6 develops with additional pressure on d4.', 'Nf3 develops and helps defend d4. Stop and describe both sides’ next jobs.',
    )),),
    'Against the white d4–e5 pawn chain, advance the c-pawn to c5 to attack its base.',
    (('c5',True,'The pawn challenges d4, the base of the chain.'),('a6',False,'This does not make the specified central challenge.'),('h6',False,'This flank move does not attack d4.')),
    (q('endpoint','What belongs in a useful endpoint assessment?','Both sides’ resources, targets, and next plans','An explanation should help you choose a move after memory ends.','Only a copied advantage symbol','A symbol does not tell you how to continue.'),
     q('review','What is a useful response to an unfamiliar opening move?','Inspect threats and apply the position’s principles','Understanding lets you adapt rather than freeze.','Continue the memorized moves regardless of the board','A changed position may invalidate the remembered plan.')),
    ('Do not use advanced opening study to avoid reviewing simple tactical mistakes in your own games.',),
    ('Reconstruct and explain.', 'Test one serious alternative.', 'Review the lesson through your own games.'),quiz_fen=after(('e4','e6','d4','d5','e5')))
