"""Original teaching of the 32 winning and 11 drawing appendix studies.

Diagrams were transcribed visually from printed pp.388–395; solutions pp.398–400.
Replays distinguish the source's principal defence from a complete game tree.
The explanatory verdicts were checked with finite engine searches, not certified
by exhaustive tablebases. Alternative first moves may also satisfy a study goal.
"""
import chess
from core.primer_guides_chapter1 import section, example, check, guide
from core.primer_build import custom

GUIDES = {}
EXERCISES = []
STUDY_DATA = {}


def _inventory(fen):
    board = chess.Board(fen)
    armies = []
    for color, label in ((chess.WHITE, 'White'), (chess.BLACK, 'Black')):
        groups = []
        for pt in (chess.KING, chess.QUEEN, chess.ROOK, chess.BISHOP, chess.KNIGHT, chess.PAWN):
            squares = board.pieces(pt, color)
            if squares:
                groups.append(chess.piece_name(pt) + ('s' if len(squares) > 1 else '') + ' on ' + ', '.join(chess.square_name(sq) for sq in squares))
        armies.append(label + ' has ' + '; '.join(groups))
    return 'White to move. ' + '. '.join(armies) + '.'


def _replay(title, fen, moves, highlights):
    """Keep an explanatory note for every ply and canonicalize checked source SAN."""
    board = chess.Board(fen)
    notes = [_inventory(fen)]
    canonical = []
    if set(highlights) != set(range(len(moves))):
        raise ValueError(f'Missing purposeful notes: {title}')
    for index, san in enumerate(moves):
        move = board.parse_san(san)
        canonical.append(board.san(move))
        board.push(move)
        notes.append(highlights[index])
    return example(title, fen, canonical, notes)



def _add(identifier, title, page, composer, pieces, moves, intro, mechanism, defence, practice,
         question, answer, reason, misconception, correction, recap, highlights=None, extra=()):
    fen = custom({x[1:]: x[0] for x in pieces.split()})
    kind = 'win' if '-win-' in identifier else 'draw'
    number = int(identifier.rsplit('-', 1)[1])
    line = moves.split()
    ex = _replay(f'{composer}: principal study line', fen, line, highlights or {})
    examples = [ex]
    for heading, branch, branch_notes in extra:
        examples.append(_replay(heading, fen, branch.split(), branch_notes))
    solution_page = 398 if kind == 'win' and number <= 18 else 399 if kind == 'win' or number <= 5 else 400
    solution_label = 'pp.398–399' if identifier == 'app-win-18' else f'p.{solution_page}'
    if identifier == 'app-win-18':
        solution_page = 399
    source = f'{composer}. Printed diagram p.{page}; solution {solution_label}. White to play and {kind}. '
    sections = (
        section('Read the position and the task', source + _inventory(fen) + ' ' + intro),
        section('How the idea works', mechanism),
        section('Defence, traps, and the final assessment', defence),
        section('Practice at the board', practice + ' Reset the diagram after your first attempt. Say the purpose of each White move before revealing the reply, then take Black’s side and look for an improvement. Use the replay arrows only after calculating. A study asks for a result against resistance; memorizing one line is a starting point, not a substitute for checking the opponent’s choices.'),
    )
    quizzes = (
        check(identifier + '-idea', question,
              (answer, True, reason), (misconception, False, correction)),
        check(identifier + '-goal', 'What establishes the requested result in this study?',
              (recap, True, 'Judge the actual final position and the defensive resources described in the lesson.'),
              ('The first impressive move alone proves the result', False, 'A sacrifice, check, or promotion still needs a continuation. Test captures, checks, and defensive alternatives.')),
    )
    GUIDES[identifier] = guide((page, solution_page),
        ('Explain the key mechanism without memorizing the move list.', 'Evaluate the resulting position and the important defence.'),
        sections, examples, (correction, 'The displayed defence is a principal study line; do not assume every black move is forced.'), quizzes,
        (answer, recap, 'Calculate the defender’s choices before accepting the verdict.'))
    board = chess.Board(fen)
    first = board.san(board.parse_san(line[0]))
    # The prompt deliberately tests execution of the named method, not uniqueness.
    alternatives = [board.san(m) for m in board.legal_moves if board.san(m) != first]
    choices = [(first, True, reason)]
    if alternatives:
        choices.append((alternatives[0], False, 'This is legal, but it does not play the requested opening move of the demonstrated method. This choice is not a claim that every alternative loses.'))
    EXERCISES.append(dict(id=identifier, title=f'{"Winning" if kind == "win" else "Drawing"} study {number}: {title}',
        summary=intro, fen=fen, inventory=_inventory(fen),
        prompt=f'Find the first move of the “{title}” method taught in this lesson, then explain its purpose. This practice checks the demonstrated route, not whether every other move loses.',
        choices=tuple(choices)))
    STUDY_DATA[identifier] = dict(composer=composer, diagram_page=page,
        solution_page=solution_page, fen=fen)


_add(
    'app-win-01',
    'Promotion as a king decoy',
    388,
    'W. Steinitz, 1880',
    'kg8 Ke7 Ph6 Pg6 Bh4 rh1',
    'h7+ Kg7 h8=Q+ Kxh8 Kf7 Rf1+ Bf6+ Rxf6+ Kxf6 Kg8 g7',
    "White must win despite Black's rook. The two advanced pawns are more important than their nominal value because they restrict the black king. Do not begin by counting the bishop as merely three points: its checking sacrifice will remove the rook at exactly the right moment.",
    "The h-pawn advances with check and promotes with another check. Black accepts the new queen, bringing the king from g8 through g7 to h8. White then plays Kf7, attacking the rook's routes and preparing to escort g6. The defence Rf1+ seems to drive the king back, but Bf6+ interposes with a countercheck. Black's rook takes that bishop and White's king recaptures. Each sacrifice has exchanged a temporary piece for a useful change in the position: first the king is displaced, then the rook disappears. White is left with a protected passer.",
    "After Kxf6, Black cannot approach the g-pawn effectively. The source uses ...Kg8, when g7 gives a standard winning king-and-pawn position; ...Kh7 instead also permits g7 and king support. The final pawn is a g-pawn, so the familiar stalemate exception for a rook pawn does not apply. Promoting is not the endpoint of the combination: the promoted queen is deliberately expendable. White's precise king advance and bishop interposition establish the win. Do not assume the rook must cooperate before the checking moves have restricted its options.",
    "Stop after Kf7 and locate the bishop's f6 square. Then remove both rooks and bishops from the final board and play the pawn ending, making sure the white king stays close enough to prevent capture.",
    'Why does White allow the promoted queen to be captured?',
    'It draws the black king to h8 and enables the rook-removing sequence',
    'The rook is eliminated and the king escorts the g-pawn to promotion.',
    'The promotion was an accidental loss of material',
    'The queen is a decoy; evaluate the protected g-pawn after the subsequent exchanges.',
    'The rook is eliminated and the king escorts the g-pawn to promotion.',
    highlights={0: 'Advance with check before Black can activate the rook.', 1: 'The king must leave g8; g7 is the source defence.', 2: 'Offer the new queen with check to draw the king to h8.', 3: 'Accepting the decoy moves the king away from the g-pawn.', 4: 'Approach the pawn and prepare to meet a rook check by interposition.', 5: "Check along the f-file to try to drive White's king away.", 6: 'Interpose with countercheck: the bishop both shields the king and attacks h8.', 7: 'Removing the bishop answers check but exposes the rook to capture.', 8: 'The rook disappears; the supported g-pawn now decides.', 9: "The king tries to blockade the pawn's promotion route.", 10: 'Advance under king support; Black cannot prevent the king-and-pawn conversion.'},
    extra=())

_add(
    'app-win-02',
    'Lasker’s descending rook staircase',
    388,
    'Em. Lasker, 1890',
    'Kc8 Rh7 Pc7 ka6 ph2 rc2',
    'Kb8 Rb2+ Ka8 Rc2 Rh6+ Ka5 Kb7 Rb2+ Ka7 Rc2 Rh5+ Ka4 Kb6 Rb2+ Ka6 Rc2 Rh4+ Ka3 Kb6 Rb2+ Ka5 Rc2 Rh3+ Ka2 Rxh2',
    "Both sides have a pawn one step from promotion, but each pawn is restrained. White's king and rook must cooperate to release that restraint safely. The long solution is built from a repeated pattern, so learn the pattern rather than trying to memorize thirteen numbered moves.",
    "Kb8 begins a king journey down the a- and b-files. Black checks from b2 and returns to c2 to watch c7. White answers by giving horizontal rook checks: Rh6+, Rh5+, Rh4+, and Rh3+. In the displayed defence, these checks drive the black king down the a-file one rank at a time; the replay does not enumerate every legal king retreat. White's king repeatedly hides on the a-file so the black rook cannot keep checking along the b-file. At the right moments it steps back to b6 or b7, attacking the rook's working area and renewing the threat to take h2.",
    "The rook cannot simply abandon c7, because c8=Q is immediate. Nor can Black allow Rxh2 under conditions where the c-pawn remains safely protected. At the finale ...Ka2 places Black's king on the second rank. After Rxh2, White’s rook on h2 pins the black rook on c2 to that king along h2–g2–f2–e2–d2–c2–b2–a2. Black can no longer play ...Rxc7, because moving off the second rank would expose its king to check. If ...Rxh2, White promotes on c8; the resulting queen-versus-rook position is winning with the kings positioned as shown. This is a gradual restriction of Black's defensive coordination, not a claim that every rook ending with an advanced pawn wins. White must respect checks throughout the staircase.",
    "Before each white rook check, predict the black king's next square. Compare the opening board with the final board and identify why taking h2 becomes effective only after the king has been driven down.",
    'What does the repeated horizontal check accomplish?',
    'It drives the king downward while the white king escapes the rook checks',
    'The final Rxh2 pins the c2 rook to its king on a2; ...Rxc7 is illegal, while ...Rxh2 releases c8=Q.',
    'It wins a pawn immediately on every turn',
    'The value of the staircase is its cumulative change in king position.',
    'The final Rxh2 pins the c2 rook to its king on a2; ...Rxc7 is illegal, while ...Rxh2 releases c8=Q.',
    highlights={0: 'Step off the c-file to begin the king-and-rook staircase.', 1: 'Check from the b-file while keeping promotion under control.', 2: "Hide on the a-file, outside the rook's checking file.", 3: 'Return to c2 to stop c8=Q.', 4: 'Drive the black king one rank down before moving your own king.', 5: 'The king retreats down the a-file.', 6: 'Step toward the rook and renew the threat against h2.', 7: "The rook checks again to prevent White's immediate capture plan.", 8: 'Hide on the a-file again.', 9: 'The rook returns to its promotion-blockading duty.', 10: 'Repeat the horizontal check one rank lower.', 11: 'The king chooses a4 in the source line. Other legal retreats exist; this is the illustrated staircase defence.', 12: "Approach the rook's working area and threaten Rxh2.", 13: 'Black must spend another tempo checking the king.', 14: 'Escape the b-file check while preserving coordination.', 15: 'Black must again guard c8 from the c-file.', 16: 'The next horizontal check pushes the king toward the second rank.', 17: 'Continue down the a-file; the defensive king is losing useful room.', 18: 'Re-enter b6 to renew the capture threat and make Black check.', 19: 'Checking postpones the attack on h2.', 20: "Step to a5, retaining the rook's next checking route.", 21: 'Return to c2 or allow promotion.', 22: 'The last staircase check is met by ...Ka2 in this line, bringing the king onto the second rank.', 23: 'The king reaches a2, changing the geometry of the rook exchange.', 24: 'Rxh2 pins the c2 rook to its king on a2, so ...Rxc7 is illegal. Exchanging with ...Rxh2 allows c8=Q.'},
    extra=())

_add(
    'app-win-03',
    'A rook sacrifice opens the promotion square',
    388,
    'A. Troitsky, before 1924',
    'Ph6 Rf6 rd2 kc1 Ka1',
    'h7 Rh2 Rf1+ Kd2 Rf2+ Rxf2 h8=Q',
    "White's h-pawn is nearly home, but Black's rook can attack it from the h-file or defend the last rank. White uses the rook to interfere with either defence. Check the black king's proximity to the c- and d-files before choosing which rook checks to use.",
    'After h7, ...Rh2 is met by Rf1+. The black king must move; the illustrative replay chooses ...Kd2. Rf2+ then offers the white rook along the second rank. If Black captures it, the h-file is clear and h8=Q follows. If Black moves the king instead, White can take the rook on h2. The second rook move combines check with a threat against the defender. Against ...Rd8, White changes direction: Rc6+ drives the king away, then Rd6+ attacks the rook from its own file and offers the same kind of exchange.',
    'The two branches must be kept distinct. Rf2 is designed for a rook on h2; Rd6 is designed for a rook on d8. Capturing the sacrificed rook does not end the study with mate: White promotes and obtains queen against rook. That material ending is winning here, but it still requires normal technique and protection from checking tricks. Black is not obliged to capture in either branch; refusing the capture loses the defensive rook or gives up control of promotion. The checks supply the time White needs for this interference.',
    "Reset after h7 and play both rook defences. Before making the second white rook move, point out the defender's line to h8 and explain how capture or refusal changes that line.",
    'Why is the second white rook move made with check?',
    'It attacks the defending rook while preventing a free defensive move',
    'Black cannot keep the rook and stop the h-pawn in the demonstrated branches.',
    'Checks always win queen-versus-rook endings automatically',
    'The check buys a tempo for a concrete deflection; the resulting material still needs conversion.',
    'Black cannot keep the rook and stop the h-pawn in the demonstrated branches.',
    highlights={0: 'Advance the pawn to force the rook to choose a defensive line.', 1: 'Attack the pawn from its own file.', 2: 'Gain a checking tempo before attacking the defender.', 3: 'This legal king retreat illustrates the principal mechanism.', 4: 'Check and attack the h2-rook along the second rank.', 5: 'Accepting the sacrifice abandons the h-file.', 6: 'Promote: White reaches a winning queen-versus-rook position.'},
    extra=(('The other rook defence', 'h7 Rd8 Rc6+ Kd2 Rd6+ Rxd6 h8=Q', {0: 'Advance the pawn to force the rook to choose a defensive line.', 1: 'Guard the promotion rank instead of attacking h7.', 2: 'Gain a checking tempo on the c-file.', 3: 'This legal retreat illustrates the parallel deflection.', 4: "Offer the rook with check on the defending rook's file.", 5: 'Capturing abandons the eighth rank.', 6: 'Promote and reach a winning queen-versus-rook position.'}),))

_add(
    'app-win-04',
    'A queen sacrifice that changes the diagonal',
    388,
    'L. van Vliet, 1888',
    'Ka8 Pb7 qc6 ka6 Qb3',
    'Qb4 Qh1 Qa3+ Kb6 Qb2+ Ka6 Qa2+ Kb6 Qb1+ Qxb1 b8=Q+',
    "White's b-pawn is ready to promote, but the king stands beside the queening square and Black has checking resources. The queen must lead the opposing king through a precise route. A promotion with check matters because it prevents Black from using the next move to rescue the old queen.",
    "Qb4 prepares checking routes without allowing the defender to settle. Against the principal ...Qh1, White plays Qa3+, Qb2+, and Qa2+, steering the black king between a6 and b6. Qb1+ then places the white queen where Black's queen can capture along the h1–b1 rank. After ...Qxb1, b8=Q+ both promotes and checks the black king. The new queen also attacks b1 down the open file. Black must answer the check first, after which White takes the enemy queen. The sacrifice changes the geometry of the queen exchange.",
    'Black has alternative king replies during the checking sequence. For example, after Qa3+ ...Kb5, Qb2+ continues the pursuit; the white king can later step away from a8 so the queen and pawn cooperate. If ...Kc7 follows Qb2+, Qh2+ attacks the queen on h1 and frees the pawn. These branches explain why repeating the principal route blindly is unsafe. The key final feature is the checking promotion and the loose queen on b1, not merely reaching the eighth rank. The replay shows the characteristic branch rather than every legal defence.',
    'Freeze just before Qb1+ and trace the b-file. Then play the capture and promotion, name the piece giving check, and verify that Black cannot move the queen on b1 while its king remains attacked.',
    'Why does b8=Q come with a decisive tempo?',
    'It checks the king while attacking the queen on b1',
    'The checking promotion wins Black’s queen on the next move.',
    'A promoted queen automatically captures the original queen',
    'Promotion creates a new attack; the check forces Black to deal with the king first.',
    'The checking promotion wins Black’s queen on the next move.',
    highlights={0: "Prepare the checking route without releasing Black's defensive queen.", 1: 'The queen takes the long first-rank defensive line.', 2: 'Begin steering the king toward the required diagonal.', 3: 'The king retreats to b6, where the next check changes direction.', 4: 'Continue the pursuit while preserving the b-pawn.', 5: 'Return to a6; White now has the next checking route.', 6: 'Drive the king back to b6 with the queen on a different file.', 7: 'The king returns, enabling the final first-rank sacrifice.', 8: 'Offer the queen with check on the same file as the passed pawn.', 9: 'The black queen is drawn onto b1.', 10: 'Promote with check; after the king moves, the new queen captures b1.'},
    extra=())

_add(
    'app-win-05',
    'Blocking a knight with its own king',
    388,
    'Textbook study',
    'kd8 Nd6 nc5 Pa5 pc4 Kd2',
    'Nb7+ Nxb7 a6 c3+ Kc2 Kc8 a7',
    "White's advanced a-pawn needs two more moves, but Black's knight controls its route. The first move sacrifices the white knight to move the defender onto an awkward square. The black c-pawn then offers a distracting capture that would spoil White's carefully timed promotion.",
    "Nb7+ draws the black knight from c5 to b7. White immediately plays a6, advancing beyond the knight's direct control. Black's counterplay is ...c3+, and the correct king response is Kc2. This leaves c3 occupied, restricting the knight's useful routes while White threatens a7 and a8=Q. After ...Kc8, a7 leaves Black's king and knight unable to establish a blockade in time. The check on the first move is a deflection: it changes where the black knight must stand before the pawn race begins.",
    "The natural Kxc3 is the trap. Once White removes the pawn from c3, ...Nd6 gives the knight a route back toward the promotion squares and holds the game. Winning a pawn is therefore less important than retaining the right tempo and obstruction. Black's king on c8 cannot reach a7 in one move, and its own knight occupies b7. The final diagram is not checkmate; its verdict rests on unavoidable promotion. Do not generalize that a pawn on the seventh always defeats a knight: the king and knight squares decide the race.",
    'Play the good and bad king responses side by side. Count how many moves the knight needs to reach a8 or a7, and notice that capturing c3 changes the available route rather than just the material count.',
    'Why does White decline to capture c3?',
    'Kc2 preserves the promotion mechanism and avoids the ...Nd6 defence',
    'The a-pawn promotes before the knight can build a blockade.',
    'Every pawn capture in an ending is bad',
    'The error is specific: Kxc3 allows the knight to return through d6.',
    'The a-pawn promotes before the knight can build a blockade.',
    highlights={0: 'Sacrifice the knight with check to displace the defender to b7.', 1: 'The knight accepts and becomes awkwardly placed.', 2: "Advance beyond the knight's direct blockade.", 3: 'The countercheck tempts White to remove the c3 obstruction.', 4: 'Decline the pawn; Kxc3 would allow ...Nd6.', 5: 'The king approaches but remains unable to stop a7 in time.', 6: 'The passer reaches the seventh before the knight can establish a blockade.'},
    extra=(('The greedy king loses the tempo', 'Nb7+ Nxb7 a6 c3+ Kxc3 Nd6', {0: 'Sacrifice the knight with check to displace the defender to b7.', 1: 'The knight accepts and becomes awkwardly placed.', 2: "Advance beyond the knight's direct blockade.", 3: 'The countercheck tempts White to remove the c3 obstruction.', 4: 'This tempting capture releases the obstruction and allows the knight to return.', 5: 'The knight reaches the defensive route that saves the game; promotion is no longer forced.'}),))

_add(
    'app-win-06',
    'A pawn sacrifice traps the bishop',
    389,
    'H. Otten, 1892',
    'bg7 kf6 Pg4 Ke4 Pa4',
    'a5 Bf8 Kd5 Bh6 g5+ Bxg5 Ke4 Bh4 Kf3',
    'White has two separated pawns against a bishop. The a-pawn gives the bishop a distant defensive duty, while the g-pawn supplies the tactical lever. The white king must approach with exact timing so Black cannot both stop the passer and keep the bishop safe.',
    "The advance a5 ties the bishop to diagonals that can meet a6 and a7. After ...Bf8, Kd5 improves the king before the decisive sacrifice. Black uses ...Bh6 to keep control, but g5+ forces the bishop to capture on g5 in the principal line. Ke4 now heads toward f3, attacking the bishop's escape routes. After ...Bh4, Kf3 drives the bishop away from useful defence of the a-pawn. The white king has gained access because the g-pawn was removed at a moment when Black had to answer check.",
    "White is not winning simply because opposite-wing pawns are far apart. If the king remains passive, the bishop can switch between diagonals and restrain them. The source sequence illustrates domination: the king approaches while the bishop's responsibility to the a-pawn restricts its freedom. At the endpoint the bishop cannot maintain the required blockade without being lost or allowing a6 and a7. The g-pawn is expendable because the surviving a-pawn is now decisive. Make sure the sacrifice is checking; a casual pawn push could give Black time to rearrange the bishop.",
    "Draw the bishop's diagonals after ...Bf8, ...Bh6, and ...Bh4. For each position, identify the squares it needs to cover against the a-pawn and the squares the white king removes from its retreat options.",
    'What is the purpose of g5+?',
    'To force a bishop placement that the advancing king can exploit',
    'The king disrupts the bishop’s blockade, allowing the a-pawn to decide.',
    'To win the bishop immediately by a pawn fork',
    'The bishop is not forked; it becomes overworked and restricted after the sacrifice.',
    'The king disrupts the bishop’s blockade, allowing the a-pawn to decide.',
    highlights={0: 'Make the bishop commit to stopping the distant a-pawn.', 1: 'The bishop chooses the diagonal that controls a3 and b4 approaches.', 2: 'Improve the king before sacrificing the kingside pawn.', 3: 'The bishop keeps access to the long diagonal toward the a-pawn.', 4: 'Sacrifice with check, forcing a useful displacement of the bishop.', 5: 'The bishop accepts, leaving its former defensive diagonal.', 6: "The king approaches the bishop's retreat squares.", 7: 'The bishop retreats but cannot preserve every duty.', 8: "The king breaks the bishop's effective blockade; the a-pawn will advance."},
    extra=())

_add(
    'app-win-07',
    'Saavedra: the rook that a queen cannot replace',
    389,
    'F. Saavedra, 1895',
    'Pc6 Kb6 rd5 ka1',
    'c7 Rd6+ Kb5 Rd5+ Kb4 Rd4+ Kb3 Rd3+ Kc2 Rd4 c8=R Ra4 Kb3',
    "White's c-pawn appears able to promote, but Black can give a series of checking rook moves. The solution contains two separate tasks: move the king out of the checks, then choose a promotion that preserves winning chances. The strongest piece is not always the correct promotion.",
    "After c7 ...Rd6+, Kb5 begins the king's walk through b4 and b3 to c2. The rook follows down the d-file with checks. When Black plays ...Rd4, White must promote to a rook: c8=R. The new rook threatens Ra8 mate. Black answers ...Ra4 to prevent that immediate threat, but Kb3 attacks the rook while retaining the mating idea. The black king on a1 is crucial: its lack of mobility makes the rook-versus-rook position a tactical win, rather than an ordinary balanced material ending.",
    "Queen promotion falls into ...Rc4+ followed by Qxc4 stalemate. The queen on c4 controls the black king's remaining squares, leaving Black no move after the rook is taken. A rook on c8 does not produce that stalemate pattern and creates a different mating threat. Earlier, choosing Kc5 instead of Kb5 allows ...Rd1 and loses the required coordination. At the main endpoint ...Rb4+ can be met by Kxb4; other rook moves must meet the mate threat. Always inspect stalemate immediately after the last capture, even when promotion looked decisive.",
    'Use the second replay to verify the queen-promotion stalemate square by square. Then return to c8=R and compare the squares a rook does not attack with those the queen attacked. Finish the rook line against an attempted check.',
    'Why is rook promotion stronger than queen promotion here?',
    'It avoids the stalemate defence and introduces a mating threat',
    'Rook promotion avoids stalemate and wins through the combined mate threat and rook attack.',
    'A queen is unable to move along the eighth rank',
    'The queen moves there perfectly well; its extra diagonal control creates the stalemate trap.',
    'Rook promotion avoids stalemate and wins through the combined mate threat and rook attack.',
    highlights={0: 'Advance to within one move of promotion.', 1: 'Check from behind the pawn to gain time.', 2: 'Choose b5; Kc5 would allow the disruptive ...Rd1.', 3: 'Continue checking down the d-file.', 4: 'Keep walking down the b-file toward shelter.', 5: 'The rook follows with another rank check.', 6: 'Approach c2 while keeping the pawn ready to promote.', 7: "Black's checking rook descends to the third rank.", 8: 'Escape the checks and prepare to promote.', 9: 'Set the stalemate trap: queen promotion allows ...Rc4+.', 10: "Promote to a rook, threatening Ra8 mate without the queen's stalemate problem.", 11: 'Stop the immediate mate by interposing along the a-file.', 12: 'Attack the rook while retaining the mating threat; Black cannot meet both.'},
    extra=(('Why queen promotion fails', 'c7 Rd6+ Kb5 Rd5+ Kb4 Rd4+ Kb3 Rd3+ Kc2 Rd4 c8=Q Rc4+ Qxc4', {0: 'Advance to within one move of promotion.', 1: 'Check from behind the pawn to gain time.', 2: 'Choose b5; Kc5 would allow the disruptive ...Rd1.', 3: 'Continue checking down the d-file.', 4: 'Keep walking down the b-file toward shelter.', 5: 'The rook follows with another rank check.', 6: 'Approach c2 while keeping the pawn ready to promote.', 7: "Black's checking rook descends to the third rank.", 8: 'Escape the checks and prepare to promote.', 9: 'Set the stalemate trap: queen promotion allows ...Rc4+.', 10: "Queen promotion allows Black's checking stalemate trick.", 11: 'Offer the rook with check, drawing the queen to c4.', 12: "Capturing leaves Black's king on a1 with no move and no check: stalemate."}),))

_add(
    'app-win-08',
    'A king march clears the rook’s escape',
    389,
    'A. Troitsky, 1896',
    'Ra8 Pa7 Kg4 kg2 ra1',
    'Kf4 Kf2 Ke4 Ke2 Kd4 Kd2 Kc5 Kc3 Rc8 Rxa7 Kb6+',
    "White's rook stands in front of its own a-pawn. Moving it casually allows Black's rook to take the pawn along the file. The king therefore joins the action from the kingside. This study teaches a coordination pattern; the printed first move is not asserted to be the only winning king route.",
    "Kf4 starts a march through e4, d4, and c5. The black king follows on the second and third ranks, seeking counterplay against the white rook's eventual escape. Once the white king reaches c5, Rc8 releases the a-pawn and offers it to ...Rxa7. White then plays Kb6+, uncovering a rook check along the c-file. At the same time the king attacks the black rook on a7. Black must answer the check, so White takes the rook next. This is a discovered check coupled with a king attack.",
    "The endpoint is not a rook exchange or a drawn rook ending: the checking move leaves Black unable to save the attacked rook. White's king was previously blocking the c-file, so stepping to b6 releases the rook's line to the black king on c3. If Black chooses a different king route, White must adapt the timing of Rc8 and the discovered attack. Kf5 and Kg5 are also winning first king moves; the practice asks for the demonstrated Kf4 route rather than claiming that it is unique. The central idea remains the same: improve the king before releasing the rook.",
    'After Rc8 ...Rxa7, identify both attacks created by Kb6+. Play a legal black king reply and capture the rook. Then replay from the start, explaining why the white king cannot remain on g4.',
    'What makes Kb6+ a double attack?',
    'It uncovers the c-file rook check while the king attacks a7',
    'The discovered check wins the black rook while it is attacked by the king.',
    'The king itself checks the king on c3',
    'The kings are not adjacent; the rook supplies the check and the king attacks the rook.',
    'The discovered check wins the black rook while it is attacked by the king.',
    highlights={0: "Begin the king march that will support the rook's eventual escape.", 1: "Black's king follows to seek counterplay against the rook.", 2: 'Approach the centre without releasing the a-pawn.', 3: 'The black king follows along the second rank.', 4: 'Continue toward the queenside while the rooks hold the a-file.', 5: "Stay close enough to challenge the white king's route.", 6: 'Reach the square that can uncover a c-file check later.', 7: 'The king occupies the c-file, making a discovered check possible.', 8: "Release the a-pawn and place the rook on the black king's file.", 9: 'Taking the pawn leaves the rook vulnerable to a king attack.', 10: 'Uncover the rook check while attacking a7 with the king; the rook is lost.'},
    extra=())

_add(
    'app-win-09',
    'Two rooks use a quiet doubling move',
    389,
    'H. Rinck, 1921',
    'rg8 rd8 kh7 Kh5 Re1 Rd1',
    'Re7+ Kh8 Kh6 Rge8 Rdd7 Kg8 Rg7+ Kh8 Rh7+ Kg8 Rdg7+ Kf8 Rh8#',
    "The material is equal, but Black's king is confined to the edge while White's king can support the attack. White must coordinate both rooks without allowing a simplifying exchange. The spectacular finish is prepared by a quiet rook move that removes Black's useful waiting choices.",
    "Re7+ drives the king to h8 in the principal defence, and Kh6 brings White's king close enough to guard the mating squares. After ...Rge8, Rdd7 doubles the white rooks on the seventh rank. This move does not give check, but it prepares Rg7+ and Rh7+ with the other rook joining on g7. The two rooks and king cover one another: the white king denies g7 and g6 as escape squares, and the rook arrangement restricts Black's back rank. The replay continues through ...Kf8 to Rh8 mate.",
    "Black can choose ...Rgf8 instead of ...Rge8. Then Rh7+ forces the king to g8 and Rg1 is mate along the g-file. This branch shows why simply defending another file does not solve the problem. The initial Re7+ also has defensive replies other than ...Kh8, and the diagram's win should not be equated with every black response following the displayed script. In particular, modern analysis finds that White has other winning moves, so this lesson teaches the book's mating mechanism, not a uniqueness proof. Count legal king escapes at the final board.",
    'Pause before Rdd7 and try a forcing check instead. Then compare how the quiet doubling move places both rooks where they can cooperate. Play both defensive file choices and name which rook gives the last check.',
    'Why is Rdd7 valuable even though it is not check?',
    'It coordinates both rooks for the forcing mating sequence',
    'The coordinated rooks and king produce checkmate against the demonstrated defences.',
    'Every quiet rook move wins in this position',
    'The specific seventh-rank arrangement and king support create the threats.',
    'The coordinated rooks and king produce checkmate against the demonstrated defences.',
    highlights={0: 'Gain time with a seventh-rank rook check.', 1: 'The king retreats to the corner in the principal defence.', 2: 'Bring the king close enough to protect the mating squares.', 3: 'Move the g-rook to e8 to defend against the attack.', 4: 'Quietly double on the seventh rank and prepare coordinated checks.', 5: 'The king has no comfortable waiting square.', 6: 'Check under the protection of the white king.', 7: 'The king is driven back to h8.', 8: "Shift the checking rook to prepare the other rook's entry.", 9: 'The king returns to g8, unable to escape the net.', 10: 'Bring the d-rook to g7 while retaining the h-rook for the finish.', 11: 'The remaining king retreat meets a back-rank mate.', 12: 'The h-rook checks along the eighth rank; every defence fails.'},
    extra=(('A file change does not cure the mate', 'Re7+ Kh8 Kh6 Rgf8 Rh7+ Kg8 Rg1#', {0: 'Gain time with a seventh-rank rook check.', 1: 'The king retreats to the corner in the principal defence.', 2: 'Bring the king close enough to protect the mating squares.', 3: 'Move the rook to f8 instead, hoping to defend from another file.', 4: 'Force the king onto the g-file.', 5: "The king's escape squares remain restricted by White's king and rook.", 6: 'The d-rook checks on the g-file; the h7-rook and king complete the mate.'}),))

_add(
    'app-win-10',
    'Giving away a queen to build a mating cage',
    389,
    'A. Troitsky, version 1897',
    'Be8 Ng6 pf6 pf5 pg4 rb4 kh3 pg3 bh2 Qh1 Ke1',
    'Bc6 Rb1+ Ke2 Rxh1 Bg2+ Kxg2 Nf4+ Kg1 Ke1 g2 Ne2#',
    "Black has a rook, bishop, and several advanced pawns, but those pieces can become obstacles to its own king. White's queen is pinned near the corner and looks indispensable. The solution instead sacrifices it, then sacrifices the bishop, to reach a surprising knight mate.",
    "Bc6 clears the bishop's route to g2. The source defence ...Rb1+ sends the white king to e2, after which ...Rxh1 takes the queen. Bg2+ now draws the black king from h3 onto g2. Nf4+ forces it toward g1; White's king returns to e1, controlling f1 and f2. Black's remaining useful pawn move is ...g2, and Ne2 mate follows. The knight checks the king on g1 while Black's own rook on h1, bishop on h2, and pawns deprive the king of escape squares.",
    "The bishop's g2 sacrifice is possible only after it has reached the long diagonal from c6. Saving the queen would miss the study's attacking geometry. The final position must be inspected as checkmate, not described vaguely as a large material gain: White has only king and knight against a substantial army, yet every king escape is blocked or attacked. The source's ...Rxh1 is not forced. The stronger ...Rb2+ meets Kd3, followed by checking and capturing play that wins the rook; the extra replay shows this defence. Against passive rook moves, Bg2 can itself be mate; Black must keep making forcing threats, and White answers those before completing the attack.",
    'At the final board, list all squares adjacent to g1 and identify whether each is occupied or controlled. Then reconstruct why the white king needed to visit e2 and return to e1 instead of wandering away.',
    'How can a lone knight deliver mate here?',
    'The white king and Black’s own pieces eliminate the king’s escapes',
    'The sacrifices produce a verified knight checkmate despite Black’s extra material.',
    'A knight always mates an isolated king by itself',
    'The mating cage depends on the exact blockers and king support; a bare king and knight cannot force mate.',
    'The sacrifices produce a verified knight checkmate despite Black’s extra material.',
    highlights={0: 'Prepare Bg2 on the long diagonal and the mating threats against h3.', 1: 'Check along the first rank before deciding whether to take the queen.', 2: 'Step to e2, retaining access to e1 for the knight-mate pattern.', 3: 'The source accepts the queen; ...Rb2+ is a more resistant alternative.', 4: 'Sacrifice the bishop with check to draw the king onto g2.', 5: "The king accepts the bishop and enters the knight's forcing route.", 6: 'Force the king toward g1 with a knight check.', 7: 'This is the only legal king escape from the check.', 8: "Control f1 and f2, completing the cage while Black's pieces block the other exits.", 9: 'The only legal move advances the pawn and leaves the mating square available.', 10: "The knight checks g1; king support and Black's blockers make this mate."},
    extra=(('Declining the queen capture', 'Bc6 Rb1+ Ke2 Rb2+ Kd3 g2 Nf4+ Kg3 Qe1+ Rf2 Nxg2 f4 Nxf4 Kxf4 Qxf2+', {0: 'Prepare Bg2 on the long diagonal and the mating threats against h3.', 1: 'Check along the first rank before deciding whether to take the queen.', 2: 'Step to e2, retaining access to e1 for the knight-mate pattern.', 3: "Continue checking instead of accepting the queen; this is more resistant than the source's capture.", 4: 'Keep the king active while preparing to break the attack.', 5: "Push the g-pawn, threatening promotion and opening the king's route.", 6: 'Check with the knight before Black can promote.', 7: "The king leaves h3 and enters the queen's checking line.", 8: 'Check along the e1–g3 diagonal.', 9: 'Interpose the rook to stop the diagonal check.', 10: 'Remove the advanced pawn and threaten the exposed defenders.', 11: 'Black attacks the knight while trying to free its pieces.', 12: "Capture the pawn to open the queen's route to f2.", 13: 'Accept the knight, leaving the rook on f2 unprotected.', 14: "Capture the rook with check. White's queen and bishop now have a decisive advantage."}),))

_add(
    'app-win-11',
    'A knight sacrifice decides a promotion race',
    389,
    'H. Rinck, 1904',
    'Kc8 bb8 pa7 Pb6 Na6 pg5 kc3',
    'b7 g4 Nxb8 g3 Nc6 g2 Nd4 Kxd4 b8=Q g1=Q Qxa7+',
    "Both sides have dangerous passed pawns. White can take the bishop, but that capture alone does not settle the race against Black's g-pawn. The knight must continue working after the capture, forcing the black king onto a square where a checking queen move becomes a skewer.",
    'b7 threatens promotion and leaves the bishop short of useful moves. In the principal line ...g4, Nxb8 removes the bishop, and the knight then travels through c6 to d4 while the g-pawn reaches g2. Nd4 offers the knight to the black king. If accepted with ...Kxd4, both pawns promote, and Qxa7+ gives a diagonal check along a7–d4–g1. Once Black moves its king, White captures the queen on g1. The knight sacrifice has put the king between the two queens on precisely the right diagonal.',
    "If Black declines the knight on d4, Ne2+ interrupts the pawn's promotion plan and gives White time to queen. A bishop retreat after b7 also meets a knight move to c7, so Black cannot simply ignore the passer. At the final checking position White has not yet captured the queen; Black still makes a king move before Qxg1. This distinction helps prevent a common calculation error: stopping at simultaneous promotion and assuming equality. The relative king squares matter more than the number of newly promoted queens.",
    'Trace the a7–g1 diagonal after both promotions. Remove the black king temporarily and notice that the queen on a7 directly attacks g1; replace it on d4 to understand why the intermediate check makes the attack decisive.',
    'What is the purpose of Nd4?',
    'It decoys the king onto the future queen-skewer diagonal',
    'A checking queen skewer wins the newly promoted black queen.',
    'It stops the g-pawn by physically occupying g1',
    'The knight does not occupy the promotion square; its sacrifice makes Qxa7+ decisive.',
    'A checking queen skewer wins the newly promoted black queen.',
    highlights={0: 'Threaten promotion while keeping the knight ready to take the bishop.', 1: 'Start the opposing passed-pawn race.', 2: 'Remove the bishop before moving the knight toward the king.', 3: 'Continue the race; Black is counting on simultaneous promotion.', 4: 'Head toward d4, where the knight can force a decisive king placement.', 5: 'Reach the seventh rank, threatening promotion.', 6: 'Offer the knight to draw the king onto the future queen-skewer diagonal.', 7: 'Accepting the knight places the king on d4.', 8: 'Promote first; the coming check will matter more than the temporary material balance.', 9: 'Black also promotes, but its queen stands behind its king on a diagonal.', 10: 'Check along a7–d4–g1; after the king moves, White wins the queen.'},
    extra=())

_add(
    'app-win-12',
    'A promoted queen clears the king’s path',
    390,
    'A. Troitsky, 1895',
    'kf8 ph7 pe7 Pg6 Kd5 Be3',
    'Bh6+ Kg8 g7 Kf7 g8=Q+ Kxg8 Ke6 Kh8 Kf7 e5 Bg7#',
    'White has a bishop and a pawn near promotion, but simply retaining material misses a mating construction. The black h-pawn restricts its own king. White uses the g-pawn first to control king squares, then gives it away so the white king can occupy the crucial approach squares.',
    "Bh6+ sends the black king to g8. After g7 and ...Kf7, g8=Q+ offers the new queen to the king. Once ...Kxg8 is played, Ke6 begins the king's approach. The black king retreats to h8, Kf7 shuts off g8, and Bg7 mate follows after a waiting pawn move such as ...e5. The bishop attacks h8 from g7, White's king protects the bishop and controls g8, and Black's own h7-pawn occupies the remaining edge square. Promotion is a clearance sacrifice that helps build this exact mating net.",
    'Black may push the e-pawn earlier. After g7 ...e5, Ke6 meets the attempt to gain space; after ...e4, Kf6 preserves the mating pressure. Against ...e6+, Kd6 avoids being driven away, and the king returns through e5 toward f6. These pawn checks are important defensive resources, not decorative moves. The principal replay uses a legal waiting move to complete the mate the book states in words. Do not call the position won merely because White promoted: the promoted queen has been captured, and the bishop-and-king geometry supplies the proof.',
    'At the final position, inspect h7, g7, and g8 separately. Then replay the earlier e-pawn check and verify why the white king needs an accurate central square rather than stepping toward the corner immediately.',
    'Why does White sacrifice the new queen on g8?',
    'It draws the king into the corner and clears the white king’s mating route',
    'The white king and bishop deliver mate against the cornered king.',
    'The remaining bishop can force mate against any bare king',
    'A bishop alone cannot force mate; the black pawn and exact king placement are essential.',
    'The white king and bishop deliver mate against the cornered king.',
    highlights={0: 'Drive the king toward the corner before advancing the pawn.', 1: 'The king retreats to g8.', 2: 'Advance with protection from the bishop and restrict the king.', 3: "The king approaches the pawn's promotion square.", 4: 'Offer a checking promotion to displace the king.', 5: "Capture the queen, but allow White's king to approach the mating squares.", 6: 'Enter the centre and prepare Kf7.', 7: 'The king retreats to the corner.', 8: "Control g8 and protect the bishop's future g7 square.", 9: 'A legal waiting pawn move; Black cannot escape the net.', 10: 'The bishop checks h8, protected by the king, while h7 blocks the last edge square.'},
    extra=())

_add(
    'app-win-13',
    'A bishop loses a tempo to keep the king out',
    390,
    'J. Gunst, 1922',
    'kd8 Bc8 Nb8 pd7 pa7 Kd5',
    'Bb7 Kc7 Ba6 Kxb8 Kd6',
    'White has a bishop and a knight against two pawns, but one minor piece is exposed to the black king. The winning method deliberately gives up the knight. White must first place the bishop so the black king is drawn away while the white king obtains a decisive central entry.',
    "Bb7 is the quiet first move. After ...Kc7, Ba6 offers the knight on b8 while placing the bishop on the a6–d3 diagonal. Black takes with ...Kxb8, and Kd6 becomes decisive. The white king attacks the d7-pawn and threatens to advance toward c7, creating mating threats against the king trapped behind a7. In this position the bishop does more than protect a pawn: it controls b7 and c8, removing the black king's useful escape squares. The knight sacrifice buys the king's entry.",
    "Taking d7 immediately fails to ...Kc7, allowing the king to attack the knight without being confined by the bishop. Ba6 immediately is also premature: ...Kc7, Ke5 ...d6+ drives White's king away before ...Kxb8. The order Bb7 and then Ba6 changes the available pawn tempo. After the correct final Kd6, the black king has no useful escape and Black must face mate or lose the pawn under much worse conditions. This is why the study's extra knight is not simply being exchanged for a pawn: position and tempo dominate the material count.",
    "Compare the good line with an immediate Ba6. Mark the square controlled by the bishop after each move and explain how ...d6+ changes the result when White's king has not reached d6 in time.",
    'Why is Bb7 played before Ba6?',
    'It arranges the king entry without allowing the defensive pawn-check tempo',
    'The sacrifice gives the white king a decisive entry against the confined king.',
    'The bishop cannot move directly from c8 to a6',
    'That direct move is legal, but its timing allows ...d6+ to disrupt the king.',
    'The sacrifice gives the white king a decisive entry against the confined king.',
    highlights={0: 'Lose the right bishop tempo before offering the knight.', 1: 'Approach the knight, hoping to win material safely.', 2: 'Place the bishop on the diagonal that restricts the corner king.', 3: 'Accept the knight but leave the king confined behind the a-pawn.', 4: 'Enter d6 and threaten Kc7 followed by the decisive bishop mate.'},
    extra=())

_add(
    'app-win-14',
    'A rook sacrifice changes a pawn-race square',
    390,
    'M. Grinfeld, 1903',
    'pb5 pa5 Pa4 Kh3 kb2 Ra1',
    'Ra3 Kxa3 axb5',
    "White's rook is threatened by the nearby black king, and the a-pawn faces two black pawns. It is tempting to save the rook with check or exchange pawns immediately. The study instead offers the rook on a square that sends the black king farther from the future passed pawn.",
    "Ra3 places the rook directly beside Black's king. If ...Kxa3, axb5 leaves a passed b-pawn, with the black king on a3 instead of a1 or a2. That displacement matters: the pawn can run before the king reaches the required interception square. The white king is distant, so the race must be calculated by exact squares rather than general principles. The rook has not been traded for a pawn by ordinary material accounting; it has bought a decisive king tempo while enabling the pawn capture.",
    "If Black declines the rook and plays ...b4, Rg3 prepares to attack the advanced pawn from the side. After ...b3, Rg5 keeps both the pawn race and rook activity under control. The source warns that immediate axb5 or Ra2+ does not win: the black king captures on a1 or a2, a better starting square for stopping the pawn. At the accepted-sacrifice endpoint, continue b6, b7, and promotion against the king's closest route. The study's conclusion depends on this one-square difference, so do not replace the precise board with a vague rule about passed pawns.",
    "Set up the three possible black king squares a1, a2, and a3 after the pawn exchange. Count the king's route to the b-pawn's promotion square, then compare why the rook sacrifice chooses the favorable square.",
    'What does Ra3 buy in exchange for the rook?',
    'A worse interception square for the black king',
    'The b-pawn outruns the displaced king, while declining the rook leaves White winning.',
    'An immediate checkmate against the king on b2',
    'Ra3 does not check; it alters the pawn race by inviting a specific king capture.',
    'The b-pawn outruns the displaced king, while declining the rook leaves White winning.',
    highlights={0: "Offer the rook on the square that puts Black's king too far from the future passer.", 1: 'Capture the rook, accepting the unfavorable pawn-race geometry.', 2: 'Create a passed b-pawn that outruns the king from a3.'},
    extra=(('Declining the rook', 'Ra3 b4 Rg3 b3 Rg5', {0: "Offer the rook on the square that puts Black's king too far from the future passer.", 1: 'Decline the sacrifice and advance the b-pawn.', 2: 'Activate the rook against the advancing pawn from the side.', 3: 'Continue the pawn race.', 4: "Attack a5 and restrain Black's counterplay; the active rook keeps the win."}),))

_add(
    'app-win-15',
    'Two pawns pull a rook off the back rank',
    390,
    'A. Nimzowitsch, version 1919',
    'rh8 kd8 pf7 Re7 ph6 pe6 Pd6 Pd5 Kb1',
    'Ra7 Re8 d7 Re7 d6 Rxd7 Ra8#',
    "Black's king is near the centre but has very few safe squares. White's rook can threaten mate along the eighth rank, while the doubled d-pawns create successive threats. Their value comes from the way they force the defending rook to leave its protective line.",
    'Ra7 threatens Ra8 mate, so Black brings the rook from h8 to e8. White advances the pawn from d6 to d7, threatening promotion and attacking the defensive arrangement. Black replies ...Re7, retaining control of the seventh rank. The other pawn now moves from d5 to d6. It protects d7 and creates another promotion threat while denying the black king useful squares. If ...Rxd7 captures the leading pawn, the rook leaves the back rank completely, and Ra8 is mate. The pawns operate as successive decoys against the same defender.',
    "Black can try ...Rh7 after Ra7, but dxe6 opens the position and advances another dangerous pawn with a winning continuation. In the principal line the final rook capture is not forced merely because it is a capture; it represents the defensive obligation created by both pawns. Confirm the mate by checking the king's adjacent squares, the white rook's line, and the black rook's inability to interpose in time. The e6- and f7-pawns help restrict Black's king, so their exact locations in the source diagram matter. Avoid treating doubled pawns as automatically weak.",
    'Before every d-pawn advance, identify which pawn moves and which square it protects afterward. At Ra8 mate, try all three kinds of defence: a king move, a capture of the rook, and an interposition.',
    'Why is the second pawn advance d6 so strong?',
    'It renews the promotion threat and overloads the defending rook',
    'The defending rook is drawn away and Ra8 delivers checkmate.',
    'Doubled pawns are always stronger than connected pawns',
    'Their strength here is concrete: the rook cannot meet promotion and back-rank mate together.',
    'The defending rook is drawn away and Ra8 delivers checkmate.',
    highlights={0: 'Threaten Ra8 mate while forcing the rook to take a defensive post.', 1: "Defend the back rank and the king's vicinity.", 2: 'Advance the leading d-pawn and threaten promotion.', 3: 'Shift to the seventh rank to restrain the pawn.', 4: 'Advance the rear pawn, protecting d7 and renewing the pressure.', 5: 'Take the leading pawn, but abandon the back rank.', 6: 'Deliver mate along the eighth rank; the king has no escape or interposition.'},
    extra=())

_add(
    'app-win-16',
    'A bishop shelters the king from rook checks',
    390,
    'A. Troitsky, before 1924',
    'Bd8 Kh7 Pa6 rb5 pg4 ka3',
    'Bc7 Rh5+ Kg7 Rg5+ Kf7 Rh5 a7 Rh8 Bd6+ Kb3 Bf8 Rh7+ Bg7',
    "White's a-pawn is close to promotion, but Black's rook can check from a distance. White needs the bishop on a diagonal that both supports the pawn's progress and eventually interposes against checks. The key move prepares that coordination before moving the pawn.",
    "Bc7 begins the plan. In the principal line ...Rh5+, Kg7 ...Rg5+, Kf7 brings the king toward the bishop. After ...Rh5, a7 forces the rook to h8, where it can watch a8 along the rank. Bd6+ gains time to bring the bishop to f8, and after ...Rh7+, Bg7 blocks the rook's attack on the king. The bishop and king now protect one another while the a-pawn threatens to promote. A piece used for attack earlier in the line becomes the shield that makes the pawn unstoppable.",
    "Black may instead begin with ...Rb1 and check from the first rank. White advances a7, then walks the king through g7, f7, e7, and d7 before Bd6+ restores the bishop's useful checking diagonal. The book prints ...Rg1 with a check symbol in this branch, but the black pawn on g4 blocks that file: canonical notation is Rg1 without check. That detail does not invalidate the legal move or the plan. Different black king replies to Bd6+ require attention; the replay chooses a legal illustrative square. At the endpoint, promotion follows because the rook cannot maintain both duties.",
    "Trace the g-file after ...Rg1 in the second replay and locate the blocker. Then return to the main line and explain why Bg7 is legal and protected, even though it steps directly into the rook's line.",
    'What final job does the bishop perform?',
    'It interposes safely against the rook check so the pawn can promote',
    'The bishop shelters the king while the a-pawn breaks through.',
    'It captures the checking rook immediately',
    'Bg7 blocks the check; promotion pressure, rather than an immediate capture, decides the game.',
    'The bishop shelters the king while the a-pawn breaks through.',
    highlights={0: "Prepare the bishop's checking and shielding diagonal before advancing a6.", 1: 'Use a rank check to try to drive the king away.', 2: 'Approach the bishop and the promotion side.', 3: 'Renew the rank check from the g-file.', 4: 'Step toward the centre while retaining the promotion plan.', 5: 'Return to a position that can restrain the a-pawn.', 6: 'Advance to the seventh, forcing a direct promotion defence.', 7: 'Guard a8 along the eighth rank.', 8: 'Gain a checking tempo to reposition the bishop.', 9: 'This legal retreat illustrates the bishop-shielding plan.', 10: 'Bring the bishop to the diagonal needed for the next interposition.', 11: 'Check the king while keeping the rook active.', 12: 'Interpose under king protection; the a-pawn will promote.'},
    extra=(('Checks from the first rank', 'Bc7 Rb1 a7 Rh1+ Kg7 Rg1 Kf7 Rf1+ Ke7 Re1+ Kd7 Rd1+ Bd6+', {0: "Prepare the bishop's checking and shielding diagonal before advancing a6.", 1: 'Prepare checks from the first rank rather than the fifth.', 2: 'Advance before Black can coordinate the blockade.', 3: 'Check along the h-file.', 4: 'Step toward the centre and keep the bishop route available.', 5: "Move to the g-file. This is not check because Black's g4-pawn blocks the file.", 6: 'Continue the king journey while the pawn remains ready to promote.', 7: 'Renew checking from the first rank.', 8: "Approach the bishop's useful diagonal.", 9: 'Check on the e-file to delay promotion.', 10: 'Step to d7, retaining the bishop-check resource.', 11: "The rook follows the king's file.", 12: 'Gain a bishop check and prepare to shield the king while promoting.'}),))

_add(
    'app-win-17',
    'A rook and pawn form an unavoidable fork',
    390,
    'S. Kozlovsky, 1931',
    'Bh8 kg8 rf8 Rh7 pf7 Pg6 Kf3',
    'Rg7+ Kxh8 Rh7+ Kg8 g7',
    "White's bishop is exposed on h8, and Black's rook protects the back rank. The winning sequence starts by offering the bishop indirectly, then advances the pawn to create a promotion threat combined with an attack on the rook. The final position needs more explanation than simply saying White has an advanced pawn.",
    'Rg7+ forces the black king to deal with the checking rook. In the principal line ...Kxh8 accepts the bishop, drawing the king onto h8. Rh7+ returns the rook to the h-file and drives the king back to g8. Now g7 attacks the rook on f8 and threatens promotion. Moving the black rook away from f8 does not solve the problem: Rh8+ forces the king off its useful square, and the pawn promotes with decisive effect. If Black captures White’s rook with ...Kxh7, gxf8=Q takes the black rook and promotes. The rook on f8 cannot capture g7: that would be a diagonal rook move.',
    "A pawn on the seventh rank does not always win against a rook. Here White's rook supports it and can deliver a checking move on h8, while Black's king has no useful shelter. The bishop sacrifice changed the move order enough to obtain this arrangement. Black's f7-pawn also restricts the king's vicinity and cannot free the position in time. Check the exact threats after g7 before deciding whether a rook retreat or pawn push works. The study ends with a winning mechanism, not immediate mate, and White must execute the follow-up accurately.",
    'After g7, list the squares to which the black rook can move, and test one retreat with Rh8+. Try ...Kxh7 as a separate branch and count the remaining material after gxf8=Q.',
    'Why is g7 decisive after the rook checks?',
    'It attacks the rook and combines promotion with Rh8+',
    'Black cannot avoid losing the rook or allowing a decisive promotion.',
    'Any seventh-rank pawn wins regardless of king placement',
    'The rook support and checking tempo are essential; advanced pawns can otherwise be blockaded.',
    'Black cannot avoid losing the rook or allowing a decisive promotion.',
    highlights={0: 'Check to draw the king toward the bishop on h8.', 1: 'Accept the bishop and move onto the h-file.', 2: 'Check again, driving the king back to g8 under changed conditions.', 3: 'The king returns to g8, but the rook has gained the right arrangement.', 4: 'Attack f8 and threaten promotion; rook retreats meet Rh8+, while ...Kxh7 allows gxf8=Q.'},
    extra=())

_add(
    'app-win-18',
    'A rook loses a tempo to win opposition',
    391,
    'R. Reti, 1922',
    'Ke7 ke5 pd5 Rd4',
    'Rd2 d4 Rd1 Kd5 Kd7 Ke4 Kd6 Ke3 Kc5',
    "White has a rook against a pawn, but the kings' relationship makes casual play dangerous. Black's king can use the pawn as shelter and force White into unhelpful squares. The study begins with a waiting rook move so White can return to the first rank at the correct moment.",
    "Rd2 allows ...d4, then Rd1 establishes the rook behind the pawn with Black to move. The source also accepts Rd3 as the first move; both lose the needed tempo before reaching d1. After ...Kd5, Kd7 approaches from behind. Black's ...Ke4 is met by Kd6, and White next reaches c5 to attack and contain the pawn. The rook limits the pawn's freedom while the king takes over the close work. Moving directly to d1 changes whose turn it is in the critical king arrangement and permits a drawing defence.",
    'The first move is therefore not unique: the book explicitly gives Rd2 or Rd3. A quiz should test the waiting idea without incorrectly condemning the alternative. Against ...Ke4 after Rd1, Kd6 is already available, so Black cannot regain the useful opposition by changing its king route. At the shown endpoint the rook and king will win the d-pawn, after which rook versus king is a routine win. Continue accurately against ...d3 rather than assuming that an extra rook licenses any king move. The point is move order and access, not a mating trick.',
    'Set the rook on d1 twice: once directly, once after Rd2 ...d4 Rd1. Compare whose move it is and the king squares available. Repeat with Rd3 to see that the same waiting principle survives.',
    'Why does White play Rd2 before Rd1?',
    'To reach the critical arrangement with the correct side to move',
    'The waiting rook move lets the king approach and win the d-pawn.',
    'Rd1 is illegal from d4',
    'Rd1 is legal, but the immediate move gives Black a different opposition arrangement.',
    'The waiting rook move lets the king approach and win the d-pawn.',
    highlights={0: 'Wait with the rook; Rd3 is another source-approved waiting move.', 1: 'Advance the pawn, committing the critical king-and-pawn structure.', 2: 'Reach d1 with Black to move, preserving the favorable opposition.', 3: 'The king approaches to support its pawn.', 4: 'Bring the white king closer while the rook restrains the pawn.', 5: "Try to maintain access to the pawn's supporting squares.", 6: 'Take the entry square that the waiting move made available.', 7: "A legal retreat illustrates the pawn's lack of lasting shelter.", 8: 'Approach the pawn from the side and prepare to win it with rook support.'},
    extra=())

_add(
    'app-win-19',
    'A rook sacrifice clears a king shelter',
    391,
    'O. Duras, 1902',
    'Kb8 kd7 Pb7 Pb6 ra3 Rc2',
    'Rd2+ Ke7 Rd6 Kxd6 Kc8 Rc3+ Kd8',
    "White has two b-pawns and an exposed king on the back rank. Black's rook is poised to check from the side, so merely advancing the pawn can fail to coordinate the pieces. The winning method offers White's rook in order to create a safe route for the king and a decisive promotion threat.",
    "Rd2+ first drives the black king to e7 in the principal line. Rd6 then offers the rook. If ...Kxd6, Kc8 steps away from the b-file while keeping the b7-pawn ready to promote. Black checks with ...Rc3+, and Kd8 escapes the check without blocking the pawn. Black can no longer stop promotion without sacrificing the rook, and the queen-versus-rook or queen-versus-king result is winning. The sacrifice is not just a clearance of one file: it improves the white king's access to the shelter squares c8 and d8.",
    "Black may refuse with ...Rc3. White answers Rc6, inviting ...Rxc6, and Ka7 then lets the b-pawn promote under king support. The remaining b6-pawn helps restrict defensive checks and protects the king's position. Modern analysis also finds other winning first moves, so the source's elegant Rd2+ is taught as a method rather than an exclusive solution. At the main endpoint White has not yet promoted; calculate the actual next move against a black king move or rook check. Do not confuse the sacrificed rook with a loss of the promotion threat.",
    'Play both captures of the white rook: one by the king on d6, one by the rook on c6. Identify the different white king square required afterward and explain why the b-pawn remains safe enough to promote.',
    'What is common to the two rook-sacrifice branches?',
    'They create a safe king arrangement for decisive b-pawn promotion',
    'The king reaches shelter and the b-pawn promotes despite the rook’s checks.',
    'They both immediately checkmate the black king',
    'The result is a promotion win; neither sacrifice is itself mate.',
    'The king reaches shelter and the b-pawn promotes despite the rook’s checks.',
    highlights={0: 'Drive the black king away from d7 with a checking rook move.', 1: 'The king retreats to e7 in the principal defence.', 2: 'Offer the rook to create safe king access and promotion threats.', 3: 'Accept the rook but leave White a route to c8.', 4: "Step away from the pawn's file while keeping promotion ready.", 5: 'Check along the c-file to try to dislodge the king.', 6: 'Escape the check without blocking b8; the pawn will promote.'},
    extra=(('The black rook takes over the defence', 'Rd2+ Ke7 Rd6 Rc3 Rc6 Rxc6 Ka7', {0: 'Drive the black king away from d7 with a checking rook move.', 1: 'The king retreats to e7 in the principal defence.', 2: 'Offer the rook to create safe king access and promotion threats.', 3: 'Decline the rook sacrifice and prepare lateral checks.', 4: "Offer the rook on c6 to clear the white king's route.", 5: 'Accept, leaving the b-pawn ready to promote.', 6: 'Approach the pawn and support promotion from a7.'}),))

_add(
    'app-win-20',
    'A king walks toward both promotion races',
    391,
    'B. Horwitz, 1879',
    'Kf8 Ra7 pe5 pg3 pa3 Pg2 kb2',
    'Ke7 a2 Kd6 e4 Kc5 e3 Kb4 e2 Re7 a1=Q Rxe2+ Kb1 Re1+ Kb2 Rxa1',
    "Black has widely separated passed pawns, while White's rook cannot stop both by itself. White's king appears far away on f8, but a diagonal route lets it approach the e-pawn and the queenside at the same time. This is a geometric king-march study, not a simple race calculation.",
    "Ke7 begins the diagonal journey. Against ...a2, Kd6 approaches the e-pawn; after ...e4, Kc5 continues toward b4. When Black advances ...e3, Kb4 supports a rook manoeuvre against both passers. After ...e2, Re7 attacks the e-pawn. Black promotes on a1, but Rxe2+ removes the other pawn with check. The rook then checks on e1 and captures the queen on a1. White's king has reached the square that makes the remaining pawn ending winning if Black takes the rook.",
    "The alternative ...a1=Q before ...e2 is also important. White can play Rxa1, allow ...Kxa1, and use Kc3 followed by Kd2 to stop the e-pawn. At the main endpoint the e-pawn has already disappeared. After ...Kxa1, Kc3 brings White’s king toward the blocked g-pawns before Black’s king can contest them. A rook on the board is not required for the final win. White must calculate the conversion after exchanging for the queen rather than stopping the analysis at equal material. Early rook checks waste the king's essential travel tempo.",
    'Draw the king route f8–e7–d6–c5–b4. At each stop, count its distance from the e-pawn and from a1. Then play the early-promotion branch and verify the king reaches d2 in time.',
    'Why does White’s king travel diagonally toward b4?',
    'The route approaches both passed pawns and supports the final conversion',
    'The diagonal king march enables both passers to be stopped and the pawn ending won.',
    'The king is trying to capture the black king',
    'Kings are never captured; the route coordinates the rook exchange and pawn blockade.',
    'The diagonal king march enables both passers to be stopped and the pawn ending won.',
    highlights={0: 'Begin a diagonal king march that approaches both pawn races.', 1: "Push the distant a-pawn to force the rook's attention.", 2: 'Approach the e-pawn while continuing toward the queenside.', 3: 'Advance the second passer, trying to overload the rook.', 4: 'Continue diagonally instead of choosing only one pawn to chase.', 5: 'Keep the central passer moving.', 6: "Reach the square that supports the rook's final conversion.", 7: 'Threaten a second promotion.', 8: 'Attack the e-pawn while retaining checks on the e-file.', 9: 'Promote, hoping the queen can rescue the other passer.', 10: 'Remove the e-pawn with check, denying Black a free queen move.', 11: 'The king must answer the check.', 12: 'Check on the first rank while attacking a1 along the rank.', 13: "The king leaves the rook's line.", 14: 'Take the queen. If ...Kxa1, the white king wins the remaining pawn race.'},
    extra=())

_add(
    'app-win-21',
    'A king threatens mate while chasing a pawn',
    391,
    'L. Kubbel, 1909',
    'Kg8 ph6 ka6 Pb4 pg3 Pa3 pg2 Bg1',
    'Kf7 h5 Ke6 h4 Kd5 h3 Kc6 h2 Bb6 h1=Q b5#',
    "Black's h-pawn looks much faster than White's king. The king cannot catch it by running straight down the h-file, so it approaches the queenside king instead. White threatens a mating net while keeping a route back toward the advanced pawns if Black changes plans.",
    'Kf7, Ke6, and Kd5 carry the king diagonally toward the opposing king on a6. If Black keeps pushing the h-pawn, Kc6 reaches the critical square. After ...h2, Bb6 prepares b5 mate. Black may promote, but the new queen cannot prevent the immediate pawn mate: the white bishop controls a7 and c7, the king controls b7 and b6, and the a3-pawn supports b4 before its advance. The apparent pawn race is transformed into a race between promotion and checkmate, and mate arrives first.',
    'Black has a more resistant choice than automatic pawn pushing. After Kd5, ...Kb5 avoids the immediate net; White then switches direction with Ke4, heading toward f3 and the g-pawns. This branch wins by collecting pawns and converting the queenside advantage, rather than by following the same mating script. The source line is useful because it exposes the dual purpose of the king march. At the final main-line board, promotion has already happened, but the game ends in mate before the queen can act. Do not assume that every defensive king move loses to b5.',
    "Trace both king routes from d5: c6 against the pawn push, and e4 against ...Kb5. At the mating board, check each escape square around a6 and explain why Black's new queen does not get another turn.",
    'Why does White’s king head toward the queenside?',
    'It creates a mate threat while retaining a route toward the pawns',
    'White either mates the king or switches to a winning pawn-collection plan.',
    'It can catch the h-pawn by ordinary distance alone',
    'The win depends on the mating threat and the alternative central route, not a straight pursuit.',
    'White either mates the king or switches to a winning pawn-collection plan.',
    highlights={0: 'Begin the diagonal route that threatens the black king while retaining a kingside return.', 1: 'Advance the apparent winning passer.', 2: 'Continue toward the centre and the mating squares.', 3: 'Keep pushing the h-pawn.', 4: 'Reach the fork in the plan: c6 against another pawn push, e4 against ...Kb5.', 5: 'Continue the race, allowing White to close the mating net.', 6: 'Approach the black king rather than chase the h-pawn directly.', 7: 'The passer reaches the seventh, but mate is nearer.', 8: 'Prepare b5 mate by controlling a7 and c7.', 9: 'Promote, but the queen cannot stop the immediate mate.', 10: 'The pawn checks a6, while the bishop and king remove all escape squares.'},
    extra=())

_add(
    'app-win-22',
    'A bishop cages a rook while the king walks home',
    391,
    'L. Kubbel, 1909',
    'Bf8 kd8 ra8 Rh7 pa6 Ke1',
    'Bc5 Rc8 Bb6+ Ke8 Bc7 a5 Kd1 a4 Kc1 a3 Kb1 a2+ Ka1',
    "The material favors White, but Black's rook and a-pawn provide practical counterplay. White must restrain the rook before bringing the king to the queenside. A series of bishop moves forces the rook into a cramped position where its own king limits its mobility.",
    'Bc5 forces Black to address the threat along the diagonal. Against ...Rc8, Bb6+ drives the king to e8, and Bc7 restricts the rook on c8. The rook cannot simply capture the bishop because Rh8 would mate along the back rank. While the rook is tied to defending its king, White walks the king through d1, c1, and b1. Black uses the a-pawn to gain tempi, but after ...a2+, Ka1 reaches safety and stops the pawn. White can then resume the attack on the restrained rook and king.',
    "The source also gives ...Rb8 after Bc5: Rh8+ followed by Bd6+ creates a double attack on king and rook. If Black instead plays ...Kc8 immediately, Ba7 restricts the rook on a8. These are separate geometries and should not be blended. At the principal endpoint the position is winning, but it is neither stalemate nor immediate mate: White has an extra bishop and a continuing mating attack, with the passed pawn contained. The king's journey is possible because Black cannot freely activate the rook. Check that interdependence before making a quiet king move.",
    'After Bc7, try ...Rxc7 and find the mate. Then replay the a-pawn advances and explain why White can spend four moves with the king while keeping the rook on h7 in place.',
    'Why can the white king walk toward a1 without losing the attack?',
    'The bishop restriction and mate threat tie down Black’s rook',
    'White contains the passer while preserving the decisive rook-and-bishop attack.',
    'Black has no legal rook moves at all',
    'The rook has legal moves, but critical departures allow decisive threats; legal immobility is not the claim.',
    'White contains the passer while preserving the decisive rook-and-bishop attack.',
    highlights={0: "Prepare bishop checks that tie the rook to its king's defence.", 1: "The rook shifts to c8 to meet the bishop's activity.", 2: 'Check while steering the bishop toward the restrictive c7 square.', 3: 'The king moves to e8, where the back-rank threat remains.', 4: 'Restrict the rook; ...Rxc7 would allow Rh8 mate.', 5: 'Use the a-pawn as a waiting move while the rook is tied down.', 6: 'Start the king journey toward the passed pawn.', 7: 'Gain another pawn tempo on the a-file.', 8: 'Approach the queenside without releasing the rook restriction.', 9: 'Push the passer closer to promotion.', 10: 'Prepare to meet the final pawn check from the corner.', 11: 'Check with the pawn, hoping to displace the king.', 12: 'Contain the pawn while preserving the decisive rook-and-bishop attack.'},
    extra=())

_add(
    'app-win-23',
    'Two sacrifices build a protected passed pawn',
    391,
    'M. Kliatskin, 1924',
    'Rb8 ra8 pa7 kd6 Pc6 nb6 Ka6 Pa5',
    'c7 Kxc7 axb6+ Kxb8 b7',
    "White's rook is attacked and the black knight protects the queenside. A normal exchange would leave Black able to stop the pawns. White instead offers the c-pawn first, using a checking pawn capture to alter the position before the black king takes the rook.",
    "c7 invites ...Kxc7, moving the black king onto c7. White then plays axb6+, capturing the knight with check. That tempo is essential: Black must answer the attack on its king rather than rearrange the rook or capture the pawn at leisure. The source continues ...Kxb8, accepting the white rook. White replies b7, producing a protected pawn one step from promotion. White's king on a6 supports b7 and controls b6, while the black king and rook are confined to the eighth rank. The sacrifices have converted a complicated material position into a concrete promotion win.",
    'At the endpoint Black’s king cannot capture b7 because White’s king protects it. The rook on a8 is not aligned with b7, so it has no direct capture there. Moving the king away allows bxa8=Q if the rook stays on a8, and moving the rook permits b8=Q when the promotion square becomes available. Black may give checks with the rook, so continue with safe king moves rather than assuming the game ends on b7. Immediate Rxa8 is inferior because the knight can recapture and help blockade the remaining pawns. The checking order, not the quantity of sacrificed material, explains the combination.',
    'Play c7 and axb6+ slowly, identifying which black unit disappears on each capture. At b7, test a king capture, a rook capture, and a rook retreat; explain which are illegal and which allow promotion.',
    'Why does axb6 come before saving the rook?',
    'It captures the knight with check and creates the protected passer',
    'The protected b-pawn forces promotion despite the rook and king blockade.',
    'It is the only legal move available to White',
    'Other legal moves exist, but the checking capture preserves the combination’s tempo.',
    'The protected b-pawn forces promotion despite the rook and king blockade.',
    highlights={0: 'Offer the c-pawn to draw the king onto c7.', 1: 'Accept the pawn and enter the checking pawn-capture geometry.', 2: 'Capture the knight with check before Black can reorganize.', 3: 'Accept the rook, leaving the king and rook confined on the back rank.', 4: 'Create a protected seventh-rank pawn; king a6 prevents a direct capture.'},
    extra=())

_add(
    'app-win-24',
    'A knight promotion wins the checking rook',
    392,
    'T. Kok, 1936',
    'Rc8 Pc7 kb6 rh4 Ph3 Kb3 Pb2',
    'Rd8 Rxh3+ Rd3 Rxd3+ Kc2 Rd6 c8=N+',
    "White's c-pawn is ready to promote, but the exposed king allows Black to gain checking tempi. White first changes the rook's location, then sacrifices it to force a favorable geometry. The promotion choice is decided by a fork, not by the usual relative values of queen and knight.",
    "Rd8 prepares the rook interposition against ...Rxh3+. White answers Rd3, offering the rook on the third rank. After ...Rxd3+, Kc2 steps off the b-file while retaining access to the pawn's support squares. Black's strongest thematic defence is ...Rd6, preparing to meet a queen with an exchange on c6. White instead plays c8=N+, forking the king on b6 and rook on d6. The king must answer check, after which Nxd6 wins the rook. White then has a knight and b-pawn against a bare king, with the pawn positioned to convert.",
    "Queen promotion after ...Rd6 is a trap: ...Rc6+ draws the queen onto c6, and ...Kxc6 reaches a drawn pawn ending. Against ...Rd5 instead, queen promotion is effective, because after ...Rc5+ Qxc5+ ...Kxc5, Kc3 obtains the winning king-and-pawn arrangement. The one-rank difference in Black's rook defence changes the correct promotion. Earlier Kc4 after the rook sacrifice allows ...Rd1 and loses the intended coordination. At the main endpoint the knight has only just appeared; complete the fork and examine the remaining b-pawn rather than calling underpromotion itself a win.",
    'Compare ...Rd5 with ...Rd6 after Kc2. In each branch, promote to a queen and calculate the exchange. Then return to ...Rd6 and use the knight fork, naming both attacked pieces.',
    'Why is c8=N+ required against ...Rd6?',
    'It forks the king and rook while avoiding the drawn queen-exchange line',
    'The checking knight promotion wins the rook and leaves a winning minor-piece-and-pawn ending.',
    'A queen cannot give check from c8',
    'The queen can check, but Black’s exchange sequence reaches a drawn pawn ending.',
    'The checking knight promotion wins the rook and leaves a winning minor-piece-and-pawn ending.',
    highlights={0: 'Prepare to interpose on d3 against the coming rook check.', 1: 'Take h3 with check, seeking time against promotion.', 2: 'Offer the rook while interrupting the check.', 3: 'Capture with check, drawing the black rook onto the third rank.', 4: 'Escape to c2; Kc4 would allow the disruptive ...Rd1.', 5: 'Prepare the queen-promotion exchange trap on c6.', 6: 'Underpromote with check, forking king b6 and rook d6.'},
    extra=(('Why a queen fails against the sixth-rank defence', 'Rd8 Rxh3+ Rd3 Rxd3+ Kc2 Rd6 c8=Q Rc6+ Qxc6+ Kxc6', {0: 'Prepare to interpose on d3 against the coming rook check.', 1: 'Take h3 with check, seeking time against promotion.', 2: 'Offer the rook while interrupting the check.', 3: 'Capture with check, drawing the black rook onto the third rank.', 4: 'Escape to c2; Kc4 would allow the disruptive ...Rd1.', 5: 'Prepare the queen-promotion exchange trap on c6.', 6: "Promoting to a queen allows the rook's checking exchange.", 7: 'Check from c6 and offer the rook to the new queen.', 8: 'Taking the rook draws the queen next to the black king.', 9: "Exchange into a drawn b-pawn ending; the king on c6 blocks White's entry."}),))

_add(
    'app-win-25',
    'A bishop sacrifice removes its rival’s long diagonal',
    392,
    'P. Heyeker, 1930',
    'Bb8 Ph6 pe5 kh4 bd4 Kc1',
    'Ba7 Ba1 Kb1 Bc3 Kc2 Ba1 Bd4 Bxd4 Kd3 Bb2 Ke4',
    "White's h-pawn is far advanced, but Black's bishop controls its promotion square. The white king is too far away to attack the bishop directly. The solution maneuvers both bishops before offering an exchange that disrupts the defence of h8.",
    "Ba7 places the white bishop on the diagonal leading to d4. In the source line ...Ba1, Kb1 approaches the centre; ...Bc3 is met by Kc2, and ...Ba1 then allows Bd4. This sacrifice offers the bishop to either the black bishop or the e-pawn. If ...Bxd4, Kd3 gains access, and after ...Bb2, Ke4 attacks the pawn and restricts the bishop's effective retreat. White can now advance h7 and h8=Q because the king has disrupted Black's defensive arrangement. The quiet preliminary king moves make the sacrifice work.",
    "If Black captures with ...exd4 instead, Kd3 is again the answer: the pawn has left e5 and the king can support the decisive advance. Black can choose ...Bc3 earlier, shortening the manoeuvre, but White retains the same Kc2 and Bd4 idea. Rushing the h-pawn before this preparation allows the bishop to remain on a useful diagonal and hold the position. At the endpoint the bishop is still on the board, so White must explain why its blockade fails rather than simply counting the passed pawn. The king's proximity and the bishop's restricted diagonal are the deciding facts.",
    'Play both possible captures of Bd4. Mark the diagonal to h8 before and after each capture, then test whether the black bishop can restore its blockade without allowing the king to win the e-pawn or support promotion.',
    'What does Bd4 achieve?',
    'It changes the pawn-and-bishop arrangement so the king can break the blockade',
    'The prepared bishop sacrifice breaks the defence of the h-pawn’s promotion square.',
    'It immediately captures the black bishop',
    'Bd4 offers the white bishop; its value comes from the resulting king access.',
    'The prepared bishop sacrifice breaks the defence of the h-pawn’s promotion square.',
    highlights={0: 'Place the bishop where it can later sacrifice on d4.', 1: 'Retain the long diagonal to the promotion square.', 2: "Approach the centre while challenging the bishop's working squares.", 3: 'Reposition the bishop while retaining the blockade.', 4: 'Continue the king approach and prepare Bd4.', 5: 'Return to the long diagonal, now vulnerable to the sacrifice.', 6: "Offer the bishop to change either the bishop's or pawn's defensive placement.", 7: 'Accept with the bishop, leaving the original blockade arrangement.', 8: "Enter the centre and prepare to attack e5 and the bishop's routes.", 9: 'Retreat while trying to keep the h-pawn under control.', 10: 'The king disrupts the blockade; the h-pawn can break through.'},
    extra=())

_add(
    'app-win-26',
    'A bishop retreat wins after both sides promote',
    392,
    'A. Troitsky, 1925',
    'Ke8 Ba8 pc5 Pa5 kh2 bc2',
    'a6 c4 a7 c3 Bh1 Ba4+ Kf7 Bc6 Bxc6 c2 a8=Q c1=Q Qa2+ Kg3 Qg2+ Kf4 Qf3+ Kg5 Qg3+ Kf5 Qg6+ Ke5 Qf6#',
    "Both a- and c-pawns are racing toward promotion. White's bishop appears able to stay near the queenside, but its decisive square is h1, on the other side of the board. The study combines promotion, a bishop exchange, and a checking queen sequence against an exposed king.",
    "a6 and a7 force Black to keep advancing the c-pawn. When it reaches c3, Bh1 preserves the long diagonal. Black tries ...Ba4+ to disrupt White's king, but Kf7 maintains the attack. After ...Bc6, Bxc6 removes the defender before both pawns promote. Qa2+ begins a queen pursuit supported by the bishop on c6. The queen checks through g2, f3, and g3, forcing the black king onto vulnerable squares. Qg6+ then wins: ...Ke5 permits Qf6 mate, while ...Kf4 allows a further checking skewer.",
    "Black's queen on c1 gives the appearance of balanced material, but it is unable to supply useful defensive checks while its own king is being chased. The bishop's control of the long diagonal makes the queen checks much stronger than they would be alone. The replay chooses ...Ke5 to show the actual mate; ...Kf4 Qh6+ is another source continuation that wins the queen by the resulting geometry. Earlier ...Kh4 during the chase is met by Qf2+, keeping the attack. Do not stop calculation at simultaneous promotion: assess king exposure and forcing moves.",
    'At Bh1, trace the entire h1–c6 diagonal and explain why the bishop returns to c6 by capture. After both promotions, pause before each check and mark the safe squares left to the black king.',
    'Why does the bishop retreat all the way to h1?',
    'It preserves the diagonal needed for the exchange and later queen attack',
    'The exposed king cannot survive the coordinated queen-and-bishop checks.',
    'It is being removed from the game to save calculation',
    'The bishop returns actively to c6 and supports the decisive checking sequence.',
    'The exposed king cannot survive the coordinated queen-and-bishop checks.',
    highlights={0: 'Start the promotion race while the bishop retains its long diagonal.', 1: 'Advance the opposing passer.', 2: 'Reach the seventh, forcing Black to keep pace.', 3: 'Push to c3, preparing promotion and bishop interference.', 4: 'Retreat to h1 to preserve the diagonal needed against ...Bc6.', 5: "Check to try to disturb White's king placement.", 6: 'Keep the king on the square supporting the eventual queen attack.', 7: 'Interpose on the long diagonal and challenge the white bishop.', 8: 'Remove the defender before both sides promote.', 9: "Continue toward c1 while White's a-pawn is ready.", 10: 'Promote with the bishop already placed on its useful diagonal.', 11: 'Black also promotes, but its king remains exposed.', 12: 'Start the checking pursuit, supported by the bishop on c6.', 13: 'The king steps toward the centre, seeking shelter.', 14: 'Continue checking without giving Black time for its queen.', 15: 'The king moves into the next checking net.', 16: 'Restrict the king with another queen check.', 17: 'The king is driven to g5.', 18: 'Keep the pursuit forcing and deny the black queen a turn.', 19: 'The king moves to f5, where the decisive check is available.', 20: 'Force mate or a queen-winning continuation.', 21: 'This defence allows the direct mating finish.', 22: 'Mate: the queen and bishop cover every escape square.'},
    extra=())

_add(
    'app-win-27',
    'A rook sacrifice creates a pawn mate',
    392,
    'J. Moravets, 1937',
    'Rb8 kd7 pc7 Pb6 rd4 Ka3 Pa2',
    'Rd8+ Kxd8 b7 Rb4 Kxb4 c5+ Kb5 Kc7 Ka6 Kb8 Kb6 c4 a4 c3 a5 c2 a6 c1=Q a7#',
    "White's queenside pawns are advanced, but Black's rook can blockade them while the king approaches. The first move sacrifices the rook with check, forcing the black king to a square that makes the pawn advance effective. A second rook sacrifice by Black creates the study's important king-choice test.",
    "Rd8+ draws the black king to d8. White then plays b7, and Black's ...Rb4 offers its rook to divert the white king. After Kxb4, ...c5+ forces a decision. Kb5 keeps the king close to the b-pawn and blocks the black king's useful approach. The route continues ...Kc7, Ka6 ...Kb8, Kb6. White now advances the a-pawn while Black advances the c-pawn. Even though Black promotes first, a7 is mate: the white king and the two queenside pawns trap the black king on b8.",
    "The tempting first move Rb7 allows ...Kc6, improving Black's king without the required displacement. In the main line, choosing the wrong square after ...c5+ also gives away the mating net, so the king response matters as much as the original sacrifice. The final pawn race is not about which side obtains a queen first. Black's queen on c1 cannot act once the king is checkmated by a7. Verify that the b7-pawn controls a8 and c8, while the white king on b6 controls a7, b7, and c7. Those restrictions explain the finish.",
    'Pause after ...c5+ and compare Kb5 with moving away from the b-pawn. Then complete the pawn race on a board, making both promotions or mating moves in order instead of deciding the result by speed alone.',
    'Why can White allow Black’s c-pawn to promote first?',
    'The next a-pawn move checkmates the confined king',
    'The king and two pawns deliver mate immediately after Black promotes.',
    'A queen promoted on c1 cannot move until two turns later',
    'The queen could move normally if Black received a turn; checkmate ends the game first.',
    'The king and two pawns deliver mate immediately after Black promotes.',
    highlights={0: 'Sacrifice the rook with check to force the king onto d8.', 1: "Accept the rook and leave the b-pawn's blockade vulnerable.", 2: 'Advance to the seventh rank.', 3: "Offer the rook to divert White's king before a pawn check.", 4: 'Accept the rook while keeping close to the b-pawn.', 5: "Check with the pawn to test White's king route.", 6: 'Stay close to the passer and preserve the mating approach.', 7: 'The king approaches the queenside blockade.', 8: 'Take the square that supports entry to b6.', 9: 'The king retreats behind the b-pawn.', 10: 'Occupy b6 and prepare to advance the a-pawn.', 11: 'Start the counter-race with the c-pawn.', 12: 'Advance the pawn that will deliver mate.', 13: 'Continue the race toward promotion.', 14: 'Keep the a-pawn moving under king support.', 15: 'Black is one step from promotion.', 16: 'Prepare the final pawn check from a7.', 17: 'Promote first, but too late to answer the mating move.', 18: 'The a-pawn mates; b7 and the king on b6 cover the escape squares.'},
    extra=())

_add(
    'app-win-28',
    'A knight zigzag wins a queen',
    392,
    'L. Kubbel, 1918',
    'Nb8 pe6 pc6 Pe5 kc5 Bh4 Ka4 Pd3 Pc3 Pg2 qf1',
    'Nd7+ Kd5 Nb6+ Kxe5 Nc4+ Kf4 g3+ Kf3 Nd2+',
    "Black has a queen against two minor pieces, but the central king offers a chain of forcing attacks. White's knight starts far from the action and must use checks to reach a useful fork square. A pawn advance later drives the king onto the diagonal needed for the final tactic.",
    'Nd7+ forces the king away from c5. Against ...Kd5, Nb6+ keeps the initiative and tempts ...Kxe5. Nc4+ then drives the king toward f4 in the source line. White plays g3+, attacking the king with a pawn while the knight prepares a checking fork. After the illustrative ...Kf3, Nd2+ attacks both the king on f3 and the queen on f1. Black must move the king, and Nxf1 follows. The white pieces have used successive checks to prevent the queen from starting its own attack.',
    "After Nb6+, Black can choose ...Kc5 instead. Bf2+ then offers the bishop to the queen. Following ...Qxf2, Nd7+ and Nf6+ create another king-and-queen fork. This branch shows why the bishop is part of the combination even though it remains still in the principal line. The final checking move is not mate: White wins the queen on the next turn and must convert the resulting material advantage. Check the queen's actual square in each branch, because the fork destination differs when the queen moves from f1 to f2.",
    "After each knight check, mark the squares the knight attacks. Play both king replies to Nb6+ and explain how the bishop sacrifice changes the queen's square and therefore the final knight-fork square.",
    'Why do the knight’s apparently indirect jumps work?',
    'Each check gains time to force a king-and-queen fork',
    'A checking knight fork wins the queen in either critical king branch.',
    'Knights can attack any queen regardless of its square',
    'The precise king and queen squares determine the fork; the checks arrange them.',
    'A checking knight fork wins the queen in either critical king branch.',
    highlights={0: 'Begin the forcing knight route with check.', 1: 'Move into the next knight-check geometry.', 2: 'Keep checking and tempt the king to take e5.', 3: "Capture the pawn but allow the knight's return through c4.", 4: 'Drive the king toward the pawn-check square.', 5: 'The source king route allows g3 with check.', 6: 'Use the pawn check to set up a king-and-queen fork.', 7: 'This legal retreat illustrates the final fork.', 8: 'Check the king on f3 and attack the queen on f1.'},
    extra=(('The bishop decoy against another king route', 'Nd7+ Kd5 Nb6+ Kc5 Bf2+ Qxf2 Nd7+ Kd5 Nf6+', {0: 'Begin the forcing knight route with check.', 1: 'Move into the next knight-check geometry.', 2: 'Keep checking and tempt the king to take e5.', 3: "Choose another king route, but allow the bishop's checking decoy.", 4: 'Offer the bishop with check to draw the queen onto f2.', 5: 'Accept the bishop and enter a knight-fork pattern.', 6: 'Check and drive the king back to d5.', 7: "The king steps onto the knight's next checking square.", 8: 'Fork the king and queen with check; White wins the queen next.'}),))

_add(
    'app-win-29',
    'A quiet queen move breaks a defensive pin',
    392,
    'A. Troitsky, 1927',
    'Ke8 ka8 bh7 Pc5 pb5 Bh3 pb3',
    'c6 b2 c7 b1=Q c8=Q+ Ka7 Qc7+ Ka8 Bg2+ Be4 Qh7 Kb8 Bxe4',
    "Both sides can promote, and Black's bishop seems able to interpose against checks. White's bishop on h3 supports a long diagonal attack against the corner king. The winning sequence includes a quiet queen move after several checks, so forcing play alone does not reveal the complete idea.",
    "c6 and c7 keep White's promotion threat moving while Black advances b2 and b1=Q. After c8=Q+, ...Ka7, Qc7+ drives the king back to a8. Bg2+ attacks along the long diagonal, and ...Be4 blocks it. Qh7 is the key change of direction. The queen points down the h7–g6–f5–e4–d3–c2–b1 diagonal, with Black’s bishop on e4 standing between the two queens. In the source king reply ...Kb8, Bxe4 removes the blocker with a decisive queen-and-bishop attack.",
    "The exact reason Qh7 works is tactical, not a general rule that moving a queen to the h-file wins. If ...Bxg2 removes the white bishop, Qxb1 wins Black's queen; the e4-bishop had been shielding the diagonal between h7 and b1. If the king moves to b8 instead, Bxe4 creates strong threats and leaves Black's queen pinned or vulnerable to exchange under unfavorable conditions. Black can also check with ...Bg6+ earlier in the pawn race; the white king steps to d8 and follows the same promotion-and-diagonal plan. Trace blockers carefully before naming a pin.",
    'At Qh7, draw the h7–b1 diagonal and locate the bishop on e4. Compare ...Bxg2 with ...Kb8. In both cases, explain what happens to the black queen before deciding whether the position is won.',
    'What tactical line does Qh7 create?',
    'It points through the bishop on e4 toward the queen on b1',
    'The quiet queen move defeats the bishop interposition and wins decisive material or mate.',
    'It checks the king directly on a8',
    'Qh7 is quiet; its value is the diagonal pressure and the threats after the blocker moves.',
    'The quiet queen move defeats the bishop interposition and wins decisive material or mate.',
    highlights={0: 'Start the race while keeping the bishop ready for a diagonal attack.', 1: 'Push toward promotion rather than defend the corner king.', 2: 'Reach the seventh rank.', 3: "Promote, hoping to match White's new queen.", 4: 'Promote with check and gain the initiative.', 5: 'The king retreats along the edge.', 6: 'Drive the king back to the corner.', 7: 'Return to a8, where the bishop check becomes effective.', 8: 'Check along the long diagonal and force an interposition.', 9: 'Block the diagonal with the bishop.', 10: 'Quietly aim through e4 at the queen on b1; moving the blocker exposes that queen.', 11: 'The king moves rather than remove the white bishop.', 12: 'Remove the blocker and reach a decisive queen-and-bishop attack.'},
    extra=())

_add(
    'app-win-30',
    'A rook and knight build a mating net',
    393,
    'R. Reti, 1923',
    'Rd8 pa7 Nd6 ph4 pb3 Ka3 ph2 kd2',
    'Re8 h1=Q Ne4+ Kc1 Rc8+ Kb1 Nd2+ Ka1 Nxb3+ Kb1 Nd2+ Ka1 Rc2',
    "Black's h-pawn will promote immediately, and another pawn on b3 restricts White's king. White cannot win by simply taking every pawn or checking at random. The rook must first choose a square that cooperates with a series of knight checks and a final mating threat.",
    "Re8 allows ...h1=Q, then Ne4+ starts a forcing pursuit. After ...Kc1, Rc8+ drives the king toward b1. Nd2+ sends it to a1, and Nxb3+ removes the b3-pawn with check. The knight then returns to d2 with another check, forcing the king back to a1. Rc2 completes the net. White's rook controls the second rank, while the knight guards b3 and b1 and can meet checking attempts. Black's new queen has activity, but its king is trapped in the corner and faces a decisive coordinated attack.",
    "The b3-pawn must be removed before the final arrangement; otherwise it interferes with White's king and knight coordination. Black can choose ...Kc2 after Ne4+, but the same rook-check idea drives it toward the corner. At the endpoint Rc2 is not itself checkmate: White has established a winning mating net, and Black can still give queen checks. The replay stops at the source's conclusion, so continue against a checking defence rather than describing the quiet rook move as mate. Finite analysis finds a forced win from this position, but the shown line is not an exhaustive list of checks.",
    'Before Rc2, identify which corner squares the knight covers and which squares the rook will cover. Try a black queen check, then find a knight interposition or countercheck that preserves the net instead of abandoning the rook.',
    'Why does the knight capture b3 with check and then return to d2?',
    'It removes a blocker while forcing the king back into the mating net',
    'The rook and knight establish a decisive mating net against the corner king.',
    'It gains a pawn that is worth more than Black’s queen',
    'The pawn capture matters because of king safety and square control, not material value alone.',
    'The rook and knight establish a decisive mating net against the corner king.',
    highlights={0: "Choose the rook square that supports the knight's forcing route.", 1: 'Promote, but leave the black king exposed to checks.', 2: 'Start the knight pursuit with tempo.', 3: 'Move toward the corner in the principal line.', 4: 'Drive the king onto the first-rank corner route.', 5: 'The king steps to b1 under pressure.', 6: 'Check and force the king toward a1.', 7: 'Enter the corner that the white pieces will surround.', 8: "Remove b3 with check, clearing White's coordination.", 9: 'The king returns to b1.', 10: "Re-establish the knight's useful d2 control with check.", 11: 'The king is forced back to a1.', 12: 'Build the mating net; this is a winning threat, not immediate mate.'},
    extra=())

_add(
    'app-win-31',
    'Successive sacrifices draw a rook onto the wrong square',
    393,
    'G. Kasparian, 1935',
    'Kg8 Bc8 ph6 pf6 Nd6 kh5 pg5 Ph4 Pf4 Pg3 rh2 rf1',
    'Ne8 Kg6 h5+ Rxh5 f5+ Rxf5 g4 Re5 Bf5+ Rxf5 Ng7 Re5 gxh5#',
    "White's bishop and knight are poised to attack a king surrounded by its own pawns. Black has two rooks, but their extra material does not guarantee useful defensive squares. White draws the two rooks onto different squares, then attacks both with one pawn push.",
    'Ne8 threatens Ng7+ followed by Bf5 mate. After ...Kg6, h5+ draws the h2-rook to h5. Next f5+ draws the f1-rook to f5: these are two different rooks. The move g4 forks both rooks. The f5-rook retreats to e5, but Bf5+ offers the bishop to draw that rook back to f5. Ng7 completes the net. In the replay the f-rook returns to e5, and gxh5 captures the other rook with mate. The pawn fork is the bridge between the successive sacrifices and the final mating cage.',
    "The initial threat explains why the quiet knight move is urgent. White is not merely attacking a rook with pawns: the king on g6 lacks safe squares because its own f6-, g5-, and h6-pawns obstruct it, while White's knight and pawns control the remaining exits. After Ng7, other rook moves also fail to the mating threat; the displayed ...Re5 is one legal completion of the source's statement that mate follows. Check which pawn delivers the last check: it is the g-pawn capturing on h5. The bishop has disappeared, but its sacrifice made that arrangement possible.",
    'Label the rooks by their original squares: the h2-rook goes to h5, while the f1-rook goes to f5, e5, and f5. At g4, identify both attacked rooks. Finish by listing every king escape after Ng7.',
    'What connects the pawn and bishop sacrifices?',
    'They draw both rooks into a pawn fork and tighten the king’s cage',
    'The forced rook displacements leave Black unable to prevent mate.',
    'White is trading down to a routine pawn ending',
    'The purpose is immediate mate; the material count alone would favor Black.',
    'The forced rook displacements leave Black unable to prevent mate.',
    highlights={0: 'Threaten Ng7+ followed by Bf5 mate.', 1: 'Move away from the immediate threat but enter the pawn-sacrifice net.', 2: 'Sacrifice with check to draw a rook to h5.', 3: 'The h2-rook captures on h5 and remains there.', 4: 'Offer the f-pawn with check to draw the other rook forward.', 5: 'The f1-rook captures on f5; Black now has rooks on f5 and h5.', 6: 'Fork both rooks with the g-pawn while tightening the king’s cage.', 7: 'Retreat to e5, keeping a defensive rook near the king.', 8: 'Offer the bishop with check to pull the rook back to f5.', 9: 'Accept the bishop and lose the needed defensive flexibility.', 10: "Complete the knight cage; mate follows against the rook's legal moves.", 11: 'One legal rook retreat, illustrating the unavoidable finish.', 12: 'The g-pawn captures the original h2-rook on h5 with mate.'},
    extra=())

_add(
    'app-win-32',
    'A knight retreats to attack a promoted queen',
    393,
    'V. and M. Platov, 1909',
    'ph7 Be7 Ph5 pd5 Kg3 ke3 Pd3 pa2 Ng1',
    'Bf6 d4 Ne2 a1=Q Nc1 Qa5 Bxd4+ Kd2 Nb3+',
    "Black's a-pawn is about to promote, and White cannot stop it directly. The bishop and knight must create threats against the exposed king instead. The surprising retreat to the first rank keeps both a mating threat and a queen fork available.",
    "Bf6 prepares the bishop's attacking diagonal. After ...d4, Ne2 allows Black to promote with ...a1=Q. Nc1 is the central idea: White threatens Bg5 mate, and the knight on c1 can jump to b3 with check if the black king or queen moves into the corresponding geometry. The source defence ...Qa5 tries to interfere with the mating threat, but Bxd4+ forces the king away, and Nb3+ forks king and queen. The knight's retreat is active because it creates a forcing threat and a tactical jumping point.",
    'If Black captures the knight with ...Qxc1, Bg5+ wins the queen by a bishop skewer after the king moves. A king move such as ...Kd2 allows Nb3+ directly. If ...h6 tries to create space, Be5 threatens Bf4 mate. The tempting Bxd4+ immediately after promotion is premature: ...Qxd4, Nxd4 ...Kxd4 reaches a drawn pawn ending after the kings collect d3. The extra retreat therefore preserves the win instead of simplifying into a draw. The lesson turns on the difference between winning the queen by a fork and exchanging all the pieces without a winning pawn ending.',
    'Play the premature exchange branch to its pawn ending and compare it with Nc1. Then test ...Qxc1 and ...Qa5 separately, naming the bishop skewer or knight fork that wins the queen in each case.',
    'Why does White retreat the knight to c1?',
    'It preserves a mating threat and prepares a checking fork on b3',
    'The mating threat forces a queen-losing skewer or knight fork.',
    'It is trying to save the knight from all possible captures',
    'Black can capture it, but that permits Bg5+ and a decisive skewer.',
    'The mating threat forces a queen-losing skewer or knight fork.',
    highlights={0: "Prepare the bishop's mating diagonal before Black promotes.", 1: 'Advance the central pawn to interrupt that diagonal.', 2: 'Bring the knight toward its surprising first-rank retreat.', 3: 'Promote, expecting the queen to dominate the minor pieces.', 4: 'Threaten Bg5 mate and prepare a checking fork on b3.', 5: 'Try to cover the mating attack while keeping the queen active.', 6: 'Remove d4 with check, forcing the king onto a forkable square.', 7: "This king retreat allows the knight's prepared jump.", 8: 'Fork the king and queen with check; White takes the queen next.'},
    extra=(('The premature exchange gives a drawn pawn ending', 'Bf6 d4 Ne2 a1=Q Bxd4+ Qxd4 Nxd4 Kxd4 Kg4 Kxd3', {0: "Prepare the bishop's mating diagonal before Black promotes.", 1: 'Advance the central pawn to interrupt that diagonal.', 2: 'Bring the knight toward its surprising first-rank retreat.', 3: 'Promote, expecting the queen to dominate the minor pieces.', 4: 'This premature check allows Black to exchange all the minor pieces.', 5: 'Capture the bishop while offering a queen exchange for the knight.', 6: 'Take the queen, but lose the knight to the nearby king.', 7: 'Remove the knight and reach a pawn ending.', 8: 'Approach the kingside pawns, hoping to win the race.', 9: 'Take d3. The blocked rook pawns and king placement give a draw, not the intended win.'}),))

_add(
    'app-draw-01',
    'A rook sacrifice seals the king into stalemate',
    393,
    'D. Ponziani, 1769',
    'kh8 Ra7 Ph5 Kf4 pa2 ra1',
    'Kg5 Rg1+ Kh6 a1=Q Ra8+ Qxa8',
    "Black threatens to promote the a-pawn, and White cannot stop it by ordinary capture. The drawing idea is to remove White's last movable piece while keeping the king safe from check. The h-pawn is useful because it helps deprive the white king of legal moves.",
    'Kg5 invites the rook check ...Rg1+, and Kh6 places the king on the edge beside its own h5-pawn. Black promotes with ...a1=Q, apparently gaining an overwhelming material advantage. White replies Ra8+, offering the rook to the new queen. After ...Qxa8, White has only king and pawn. The rook on g1 controls g5, g6, and g7; the black king on h8 controls h7. White’s own pawn occupies h5, and its king on h6 blocks that pawn’s only advance. The pawn has no capture on g6. White therefore has no legal move. The king itself is not checked, so the game is drawn immediately.',
    'The last distinction is essential: if the white king were in check, no legal move would mean mate, not stalemate. Nor is merely sacrificing the rook enough; the king must first reach h6. Black can avoid the displayed capture or choose another defence earlier, so White must retain checking resources rather than assuming the opponent is obliged to accept every gift. The principal line illustrates the stalemate defence against the natural promotion plan. The final board is an actual stalemate, and the result is independent of how much extra material Black has.',
    "After Qxa8, test the king's neighboring squares and the pawn's possible advance or capture. Then move the white king back to g5 in your imagination and see why the same sacrifice would no longer create the same stalemate.",
    'What turns the rook sacrifice into a draw?',
    'White has no legal move and the king is not in check',
    'The accepted rook sacrifice leaves an immediate stalemate.',
    'Any sacrifice against a newly promoted queen draws',
    'The exact king square and coverage of every legal move create stalemate.',
    'The accepted rook sacrifice leaves an immediate stalemate.',
    highlights={0: 'Approach the future stalemate cage before Black promotes.', 1: 'Check along the g-file, driving the king toward the edge.', 2: 'Enter h6, where the black pieces can cover every escape without checking the king.', 3: 'Promote, creating the piece that will accept the rook sacrifice.', 4: "Offer the rook with check on the queen's rank.", 5: 'The queen captures, leaving White no legal move and no check: stalemate.'},
    extra=())

_add(
    'app-draw-02',
    'Promotion is answered by stalemate or capture',
    393,
    'A. Troitsky, before 1910',
    'ph5 be5 Kh4 Ra3 pg2 kb2',
    'Rg3 Bxg3+ Kh3 g1=Q',
    "Black's g-pawn is about to promote, while White's rook cannot simply capture it. White can force a choice between stalemate and a reduced ending that Black cannot win. The white king's exact placement beside the bishop is the key to meeting underpromotion.",
    'Rg3 offers the rook to the bishop. After ...Bxg3+, Kh3 leaves the bishop on g3 beside the white king and the pawn on g2 ready to promote. A queen or rook promotion produces stalemate: the promoted piece controls the escape squares along the g-file, the bishop controls h2 and h4, and the pawn on h5 prevents the remaining king route. White is not in check and has no legal move. The rook sacrifice has removed the only white piece that could otherwise spoil the stalemate by moving.',
    "Black is not restricted to queen promotion. After ...g1=N+, White answers Kxg3, taking the bishop while escaping the knight check. Bishop promotion likewise permits Kxg3. Those reduced endings do not give Black a forced win. If Black delays promotion with a king move, Kxg2 removes the g-pawn, leaving a wrong-bishop rook-pawn ending: the dark-squared bishop cannot control the light promotion square h1, and White heads for that corner. The lesson therefore explains the defensive alternatives rather than treating the book's queen-promotion line as the only legal possibility.",
    'At Kh3, try all four promotions. For queen and rook, verify stalemate. For knight and bishop, play Kxg3 and inspect the remaining material. Finally delay promotion and guide the white king toward h1 after taking g2.',
    'Why does underpromotion not refute the drawing idea?',
    'It allows the king to capture the bishop and reach a drawable reduced ending',
    'Queen or rook promotion stalemates; alternatives allow capture or the wrong-bishop corner defence.',
    'Underpromotion is illegal when a queen would stalemate',
    'Any piece may be chosen; White must answer the actual promotion correctly.',
    'Queen or rook promotion stalemates; alternatives allow capture or the wrong-bishop corner defence.',
    highlights={0: "Offer the rook to remove White's last movable piece.", 1: "Accept with check, placing the bishop beside the white king's destination.", 2: 'Enter the stalemate cage while keeping the bishop capturable after minor-piece promotion.', 3: 'Queen promotion leaves White without a legal move and not in check: stalemate.'},
    extra=(('Knight promotion gives up the bishop', 'Rg3 Bxg3+ Kh3 g1=N+ Kxg3 Ne2+ Kh4 Nf4 Kg5 Kc3 Kxf4 Kd4 Kg5 Ke5 Kxh5', {0: "Offer the rook to remove White's last movable piece.", 1: "Accept with check, placing the bishop beside the white king's destination.", 2: 'Enter the stalemate cage while keeping the bishop capturable after minor-piece promotion.', 3: 'Underpromote with check, but fail to protect the bishop on g3.', 4: 'Escape check by taking the bishop.', 5: 'Check with the knight to try to gain time for the pawn.', 6: 'Keep the king near the h-pawn.', 7: "Defend the pawn from f4, but leave the knight vulnerable to the king's route.", 8: 'Approach both knight and pawn.', 9: 'The distant king cannot protect the knight in time.', 10: 'Remove the knight and reduce the ending to one harmless pawn.', 11: 'Try to support the pawn from a distance.', 12: 'Approach h5 before the black king arrives.', 13: 'The king remains too far away.', 14: 'Take the last pawn: bare kings draw.'}), ('Bishop promotion gives up the bishop', 'Rg3 Bxg3+ Kh3 g1=B Kxg3 Kc3 Kh4 Kd4 Kxh5', {0: "Offer the rook to remove White's last movable piece.", 1: "Accept with check, placing the bishop beside the white king's destination.", 2: 'Enter the stalemate cage while keeping the bishop capturable after minor-piece promotion.', 3: 'Promote to a bishop, but allow White to remove the original bishop.', 4: 'Capture g3; Black has only one bishop and the h-pawn.', 5: 'Bring the king closer, too slowly to save the pawn.', 6: 'Approach h5.', 7: 'Continue the king approach.', 8: 'Remove the pawn, leaving bare king versus bishop and king: insufficient material.'})))

_add(
    'app-draw-03',
    'A rook forces its own capture before the pawn promotes',
    394,
    'A. Troitsky, 1895',
    'kf8 Rd5 Kg4 Ph2 pg2 bd2',
    'Rf5+ Ke7 Re5+ Kd6 Re1 Bxe1 Kh3 g1=Q',
    'White cannot stop the g-pawn by ordinary rook defence because the bishop controls useful squares. The drawing plan relocates the rook to a square where the bishop can take it, then arranges a stalemate cage. The preliminary checks give White time to reach that square.',
    "Rf5+ forces a king response; the source uses ...Ke7. Re5+ gains another tempo, and after a legal king move such as ...Kd6, Re1 offers the rook to the bishop on d2. Black accepts with ...Bxe1. Kh3 then places the white king beside its own h2-pawn, ready for ...g1=Q or ...g1=R to produce stalemate. The h-pawn cannot advance because White's own king occupies h3. The king's remaining squares are covered by the bishop and promoted piece.",
    "Black can underpromote to a knight with check. White answers Kg2; after ...Ne2, Kf1 attacks the knight and prevents Black from coordinating a winning attack. Bishop promotion produces two dark-squared bishops, which do not give the usual two-bishop mating force; White can advance or give up the h-pawn while avoiding a self-blockade. Black may also move the king differently during the rook checks, so the move Re1 must remain safe and purposeful. The replay's knight branch shows a drawable position, not a completed threefold repetition. Correct defence continues after the source's short line.",
    'Verify the stalemate with the king on h3 and pawn on h2. Then try the knight promotion and follow the king route g2–f1. Explain why a check from an underpromoted piece changes the required reply but does not automatically win.',
    'Why must the rook disappear before Kh3?',
    'A surviving rook would still have legal moves and spoil the stalemate',
    'The rook sacrifice enables stalemate, while minor-piece promotions have drawable defensive replies.',
    'White cannot move the king while owning a rook',
    'The issue is availability of moves in the final cage, not a restriction on king movement.',
    'The rook sacrifice enables stalemate, while minor-piece promotions have drawable defensive replies.',
    highlights={0: "Check to gain time for the rook's route to e1.", 1: "The king chooses the source's principal retreat.", 2: 'Gain another checking tempo before offering the rook.', 3: 'This legal king move illustrates the sacrifice mechanism.', 4: 'Offer the rook to the bishop on d2.', 5: "Remove White's rook, leaving only king and h-pawn.", 6: 'Block the h-pawn with the king and prepare the stalemate cage.', 7: 'Queen promotion covers the escape squares without checking the king: stalemate.'},
    extra=(('Underpromotion avoids stalemate but cannot win', 'Rf5+ Ke7 Re5+ Kd6 Re1 Bxe1 Kh3 g1=N+ Kg2 Ne2 Kf1', {0: "Check to gain time for the rook's route to e1.", 1: "The king chooses the source's principal retreat.", 2: 'Gain another checking tempo before offering the rook.', 3: 'This legal king move illustrates the sacrifice mechanism.', 4: 'Offer the rook to the bishop on d2.', 5: "Remove White's rook, leaving only king and h-pawn.", 6: 'Block the h-pawn with the king and prepare the stalemate cage.', 7: 'Promote to a knight with check, avoiding immediate stalemate.', 8: 'Approach the knight and prepare to attack it.', 9: 'The knight moves to a square protecting the bishop.', 10: 'Attack the knight and retain the drawing defence; Black cannot coordinate a winning material gain.'}),))

_add(
    'app-draw-04',
    'A pawn sacrifice builds a stalemate wall',
    394,
    'G. Andersson, 1934',
    'pd7 pb6 Pe5 Ph4 Kf4 pe4 ke1 bb1',
    'e6 dxe6 Ke3 Ba2 h5 e5 h6 Bg8 h7 Bxh7',
    "White has two pawns against a bishop and three pawns. Saving material is not the aim. White needs Black's central pawns on squares that control every possible king exit while leaving the king itself un-attacked. The h-pawn then supplies the final sacrifice.",
    "e6 invites ...dxe6, shifting the d-pawn to e6 and fixing the central structure. Ke3 places the king between the e-pawns' controlled squares. White then advances h5 and h6 while Black's bishop travels to g8 to stop the pawn. h7 offers the pawn on a square where the bishop can capture it. After ...Bxh7, White has only the king. The black king on e1 and pawns on e4 and e5 cover its neighboring squares, while no black unit attacks e3 itself. With no pawn left to move, the result is stalemate.",
    "Keeping the e-pawn or moving the king first lets Black arrange its pieces without creating the required cage. The initial sacrifice is therefore constructive: it changes the pawn attacks that make the final position possible. The black b6-pawn is far away and does not provide White with any move, so its presence does not prevent stalemate. Black may alter the bishop move order, but must still address the h-pawn's advance. The principal line illustrates the full stalemate mechanism. Check the final board rather than assuming that a bare king surrounded by pawns must be mated.",
    'After ...dxe6, mark the squares controlled by the two e-pawns. At the final position, test every king move from e3 and confirm that the king is not in check. Then restore the h-pawn and see why its removal matters.',
    'What is the purpose of the opening e-pawn sacrifice?',
    'It rearranges Black’s pawn control to build a future stalemate cage',
    'The final h-pawn sacrifice leaves the king safely stalemated.',
    'It immediately wins the bishop by a fork',
    'The sacrifice changes the geometry of the king’s legal moves; it does not attack the bishop.',
    'The final h-pawn sacrifice leaves the king safely stalemated.',
    highlights={0: "Sacrifice the e-pawn to rearrange Black's pawn control.", 1: 'Accept the pawn and create the central stalemate wall.', 2: 'Place the king where the black pawns will deny its eventual escape squares.', 3: "Reposition the bishop to meet the h-pawn's advance.", 4: 'Start the final pawn sacrifice route.', 5: "Fix the e-pawn structure that confines White's king.", 6: 'Continue toward h7, inviting a bishop capture.', 7: 'Prepare to capture the pawn along the diagonal.', 8: "Offer White's last pawn and last non-king move.", 9: 'The capture leaves the king on e3 safely stalemated.'},
    extra=())

_add(
    'app-draw-05',
    'A rook attacks two defenders from between them',
    394,
    'S. Kozlovsky, 1930',
    'kc8 Kg7 rh6 ra6 Pe4 Rf1',
    'Rf8+ Kd7 Rf7+ Ke6 Rf5',
    "White is a rook down, but Black's king and rooks are awkwardly placed on the sixth rank. White cannot afford a quiet move that lets them coordinate. The drawing sequence uses checks to place the king where a rook fork becomes possible without exposing White's rook to a king capture.",
    "Rf8+ drives the king away from the back rank. Against ...Kd7, Rf7+ continues the pursuit, and ...Ke6 is met by Rf5. The white rook threatens Rf6, attacking both black rooks along the sixth rank while supported by the white king on g7. Black's king on e6 cannot take a protected rook on f6. Black cannot freely coordinate the rooks while also escaping the checks, and White keeps either the checking sequence or the threat to win one rook.",
    "At Rf5, the pawn on e4 protects the rook, preventing ...Kxf5. The threat Rf6+ then attacks the rooks along the sixth rank. Black's king can retreat, but White resumes checking from f7 or f8; the source's principal defence reaches a perpetual-check or material-recovery mechanism. This is not an immediate capture of both rooks, and Rf5 is not itself a fork of the sixth-rank rooks. The distinction matters for accurate teaching: the threat and the checking cycle secure the draw together. If Black gives up one rook, reassess the reduced ending rather than expecting mate.",
    'After Rf5, identify what protects the white rook and what protects f6. Try a black king retreat and continue the checks. Then test a rook move and see whether the threatened sixth-rank fork wins material.',
    'Why can White play the quiet Rf5 without losing the rook?',
    'The e4-pawn protects f5, and the move threatens a protected sixth-rank fork',
    'The checking cycle and threat to win a rook prevent Black from converting the extra rook.',
    'The rook is directly attacking both sixth-rank rooks from f5',
    'Rf5 threatens Rf6; it does not already attack a6 and h6.',
    'The checking cycle and threat to win a rook prevent Black from converting the extra rook.',
    highlights={0: 'Begin checking before the two black rooks can coordinate.', 1: 'Move away from the back rank check.', 2: 'Continue the pursuit and invite the king onto e6.', 3: 'The king approaches the checking rook.', 4: 'The e4-pawn protects f5; White threatens a protected Rf6 fork and retains the checking cycle.'},
    extra=())

_add(
    'app-draw-06',
    'A sideways king move preserves the right opposition',
    394,
    'N. Grigoriev, 1924',
    'kd8 pf7 Pf6 pe6 Kc5',
    'Kc6 Ke8 Kd6 Kf8 Ke5 Kg8 Kf4 Kh7 Kg5',
    "White has one pawn against two, and the white king must defend the advanced f-pawn while Black's king tries to approach. A direct step toward the pawns looks natural but gives Black the favorable move order. The drawing move first shifts the king sideways.",
    "Kc6 preserves the correct relationship between the kings. After ...Ke8, Kd6 reaches the useful opposition arrangement with Black to move. The source then follows ...Kf8, Ke5 ...Kg8, Kf4 ...Kh7, Kg5. White has transferred the king from the queenside to the kingside without abandoning f6. The pawn on f6 restricts the black king and divides its routes, while White's king approaches along the fifth and fourth ranks. Black cannot force the white king away and win the pawn without allowing a drawing counteraction against the e-pawn.",
    'The tempting Kd6 immediately is met by ...Ke8, and after Ke5, ...Kd7 gives Black the favorable opposition. That one tempo changes which king can make progress. At the correct endpoint Kg5, Black can push ...e5, but Kf5 attacks that pawn while keeping the f-pawn supported. White must continue actively rather than wait on one square forever. The study is a drawn king-and-pawn ending, not stalemate and not an immediate repetition. Exact move order matters more than the general advice to centralize the king or march toward an advanced pawn.',
    'Play the first two king moves in both orders and note whose turn it is when White reaches d6. Continue the good line to g5, then answer ...e5 by attacking the new pawn rather than retreating automatically.',
    'Why is Kc6 better than the direct Kd6?',
    'It preserves the move order needed to hold opposition',
    'Correct opposition lets White defend the f-pawn and counterattack the e-pawn.',
    'It is physically closer to the f-pawn',
    'The sideways move is not the shortest geometric route; its value is the tempo.',
    'Correct opposition lets White defend the f-pawn and counterattack the e-pawn.',
    highlights={0: 'Take the sideways route to preserve the favorable opposition.', 1: 'Try to approach the f-pawn from the back rank.', 2: 'Reach d6 with the right side to move.', 3: 'Shift toward the pawn while avoiding the opposing king.', 4: 'Keep the king active and close to f6.', 5: 'Continue around the restricted king routes.', 6: 'Approach the kingside while maintaining pawn support.', 7: 'The king seeks entry from the edge.', 8: 'Support f6 and prepare Kf5 against ...e5; the ending can be held.'},
    extra=(('The tempting king step loses opposition', 'Kd6 Ke8 Ke5 Kd7', {0: 'The direct approach gives Black the favorable opposition.', 1: 'Take the key defensive square with White to move.', 2: "Approach the pawn, but allow the black king's counter-entry.", 3: 'Black takes the useful opposition and can win the f-pawn; the tempo was lost.'}),))

_add(
    'app-draw-07',
    'Two pawn sacrifices deny the king shelter',
    394,
    'S. Kozlovsky, 1932',
    'kd7 Pc7 ra7 pa6 rh5 Pf4 Pc4 Pa4 Pf3 Kf2 Re1',
    'Re7+ Kc8 Re8+ Kxc7 Re7+ Kb6 c5+ Rxc5 a5+ Rxa5 Re6+ Kc5 Re5+ Kb4 Re4+',
    "Black has an extra rook, and White's advanced c-pawn cannot survive indefinitely. White needs a continuous series of checks. The two queenside pawns are useful because they can sacrifice themselves with check, drawing a rook onto squares that obstruct Black's king.",
    "Re7+ begins the pursuit. After ...Kc8, Re8+ drives the king toward c7, where it captures the pawn. Re7+ then sends it to b6. White plays c5+, forcing a response to the pawn check; the source uses ...Rxc5. The next sacrifice a5+ draws the same rook to a5. Now Re6+ resumes the rook checks, and the king is pushed down through c5 and b4 while Re5+ and Re4+ follow. The black rook on a5 blocks useful shelter squares and cannot simultaneously escape the king's way and stop the checks.",
    "The pawns are not sacrificed to gain material. Their captures change the positions of Black's pieces so the checking rook can continue safely. If the black king chooses another square during the sequence, White must choose the corresponding rank for the next check; the displayed line is one route through the perpetual-check mechanism. The final Re4+ is not a draw by itself under the repetition rule: play must continue until a repetition claim or another draw condition applies. The study's verdict is that Black cannot escape the checking system without giving up the winning advantage.",
    'Compare the board before c5+ with the board after ...Rxa5. Identify which squares around the black king are now blocked by its own rook. Continue checking against one different king retreat instead of memorizing only b4.',
    'Why does White sacrifice both queenside pawns with check?',
    'To draw a rook into the king’s escape route while preserving the initiative',
    'The displaced rook and continuous checks prevent Black from finding safe shelter.',
    'To promote a different pawn immediately',
    'The sacrifices construct a perpetual-check mechanism; no immediate promotion follows.',
    'The displaced rook and continuous checks prevent Black from finding safe shelter.',
    highlights={0: 'Start the perpetual-check construction.', 1: 'Retreat toward the advanced c-pawn.', 2: 'Check again before Black can coordinate its rooks.', 3: 'Capture c7, but step into the next checking route.', 4: 'Continue the pursuit toward the queenside.', 5: 'Seek shelter on b6.', 6: 'Sacrifice a pawn with check to displace a rook.', 7: "Accept and move the rook into the king's route.", 8: 'Sacrifice the second pawn with check, drawing the rook farther aside.', 9: 'The rook on a5 will now obstruct king shelter.', 10: 'Resume rook checks with the defensive pieces awkwardly placed.', 11: 'The king moves down the board seeking an escape.', 12: "Keep the check on the king's rank.", 13: 'Continue downward, still without safe shelter.', 14: 'Maintain the checking mechanism; play must continue before any repetition claim.'},
    extra=())

_add(
    'app-draw-08',
    'A rook offers itself on the only useful file',
    394,
    'A. Herbstmann, 1935',
    'Rg8 Kg6 pg4 rf4 Pd4 kf2',
    'Kg5 Rxd4 Kh4 g3+ Kh3 Rd3 Rg7 Rf3 Rg4 Rf8 Rf4+ Rxf4',
    "White is a pawn behind in a rook ending and faces a dangerous g-pawn. The king cannot remain exposed to checks forever. White deliberately lets the d-pawn go, arranging a position where the black rook's capture of White's rook would leave stalemate.",
    "Kg5 invites ...Rxd4, and Kh4 moves toward the edge. After ...g3+, Kh3 places the king in a narrow cage. Black tries ...Rd3, improving the rook and preparing to support the pawn. Rg7 keeps White's rook on the correct file. Against ...Rf3, Rg4 offers the rook while maintaining the stalemate idea. Black's ...Rf8 is answered by Rf4+, offering the rook with check. Capturing is not forced: a king move instead allows Rxf8, winning Black’s rook. The principal line accepts the sacrifice. After ...Rxf4, White's king on h3 has no legal square, is not in check, and owns no other piece: stalemate.",
    "The attractive Rf8+ at the earlier position is the trap: ...Rf3, Rg8 ...Rf7 lets Black coordinate rook and pawn while avoiding the sacrifice on the right square. The quiet rook placement matters more than giving check immediately. Black can decline some sacrifices and shuffle its rook, but White preserves the drawing setup; for example, ...Rd3 can lead back toward the same arrangement. The endpoint is a real stalemate, while earlier repeated rook moves are a defensive resource rather than an automatic draw claim. Check both the g-pawn's attacks and the black king's control of g2.",
    'At Kh3, mark g2, g3, g4, h2, and h4. Then compare Rg7 with the premature Rf8+. At the final sacrifice, verify why the capturing rook attacks escape squares without checking the king itself.',
    'Why does White choose Rg7 instead of the immediate Rf8+?',
    'It preserves the rook-sacrifice geometry and avoids Black’s coordinating reply',
    'White preserves a stalemate sacrifice or a repeating defensive rook arrangement.',
    'Giving check is illegal in a drawn rook ending',
    'The check is legal but mistimed; ...Rf3 and ...Rf7 defeat that move order.',
    'White preserves a stalemate sacrifice or a repeating defensive rook arrangement.',
    highlights={0: 'Enter the route to the stalemate cage and offer the d-pawn.', 1: 'Take the pawn, leaving White with only king and rook.', 2: 'Move toward the edge where the pawn can restrict the king.', 3: 'Check and push the king into its intended cage.', 4: 'Enter h3, where a future rook sacrifice can stalemate.', 5: 'Improve the rook while supporting the g-pawn.', 6: 'Keep the rook on the correct file for the defensive sacrifice.', 7: 'Try to coordinate the rook and pawn against the trapped king.', 8: 'Offer the rook while preserving stalemate geometry.', 9: 'Avoid the immediate capture but permit a checking sacrifice.', 10: 'Offer the rook with check. A king move declines the sacrifice but allows Rxf8.', 11: "Capturing the rook leaves White's king not checked and without a legal move: stalemate."},
    extra=())

_add(
    'app-draw-09',
    'A bishop hideaway makes the final stalemate possible',
    395,
    'V. and M. Platov, 1907',
    'kg8 Bf8 Rc7 Ph6 pc6 pf5 pa5 Pf4 pb4 Pb3 ph2 Kc1 bb1',
    'h7+ Kh8 Bg7+ Kxh7 Ba1+ Kh6 Rxc6+ Kh5 Kb2 h1=Q Rh6+ Kxh6',
    'Black threatens an h-pawn promotion while White has a rook and bishop that might seem able to attack. The drawing combination must dispose of the rook and immobilize the bishop, so neither piece gives White a legal move in the final position. Several checking moves prepare that unusual arrangement.',
    "h7+ drives the black king to h8. Bg7+ then forces ...Kxh7, removing White's h-pawn. Ba1+ places the bishop in the corner behind the blocked b-pawn structure while continuing to check. After ...Kh6, Rxc6+ removes another black pawn and sends the king toward h5. Kb2 is the quiet move that completes White's future stalemate cage. Black promotes with ...h1=Q, and Rh6+ offers the rook. Once ...Kxh6 is played, White's king, bishop, and pawns have no legal moves, yet the king on b2 is not checked.",
    "The bishop on a1 is not captured; it is blocked by the king on b2 and the surrounding pawn structure. The white pawns on b3 and f4 cannot advance because black pawns occupy b4 and f5. Black's bishop on b1 controls the white king's available diagonal squares. If Black declines the promotion plan, White can threaten Rc1; the source also gives ...Bc2, when Rc8 and Rh8+ maintain the defence. The central lesson is to count all movable units, not just the king. A bishop left on a free diagonal would ruin the stalemate.",
    'At the final board, test the white king, bishop, and both pawns separately. Then return to Ba1+ and explain why that corner square was chosen many moves before the rook sacrifice became available.',
    'Why is the bishop sent to a1?',
    'It can be immobilized there as part of the final stalemate',
    'The rook sacrifice leaves every white unit immobile without checking the king.',
    'A bishop on a1 is automatically unable to move',
    'It is the exact blockers, including the king and pawn structure, that stop the bishop.',
    'The rook sacrifice leaves every white unit immobile without checking the king.',
    highlights={0: 'Force the black king toward the h-file before disposing of the pawn.', 1: 'Retreat to h8 under the pawn check.', 2: 'Check with the bishop and invite the king to take h7.', 3: "Remove the pawn, opening the bishop's route to a1.", 4: 'Hide the bishop in the future stalemate corner while giving check.', 5: 'Move down the h-file to escape the diagonal.', 6: 'Remove c6 with check, changing the future king cage.', 7: 'The king approaches the final rook-sacrifice square.', 8: 'Complete the cage and threaten Rc1 if Black delays promotion.', 9: 'Promote, but allow the prepared rook sacrifice.', 10: 'Offer the rook with check beside the black king.', 11: "Capture the rook; White's king, bishop, and pawns now have no legal move: stalemate."},
    extra=())

_add(
    'app-draw-10',
    'A rook sacrifice reaches the seventh-rank bishop-pawn draw',
    395,
    'V. Chekhover, 1945',
    'Rg7 Kf7 Pf4 pe3 pd3 kc2',
    'Kf8 d2 Rd7 e2 Rxd2+ Kxd2 f5 e1=Q f6 Qe6 f7',
    'Black has two connected passed pawns close to promotion. White cannot stop both while keeping the rook, so the task is to exchange the rook for one pawn with check and run the f-pawn. The drawing destination is a special queen-versus-pawn ending, not equal material.',
    "Kf8 is the precise king move, leaving the f-pawn free to advance and placing the king where it can support f7. Against ...d2, Rd7 attacks the leading pawn while preparing the checking sacrifice. Black continues ...e2, and Rxd2+ draws the king onto d2. White then plays f5 while Black promotes on e1. f6 and f7 reach the known drawing setup: a bishop-file pawn on the seventh rank, with its king nearby and the opposing king too far away. The queen can give checks but cannot force the pawn's capture without allowing stalemate or promotion.",
    'If Black advances ...e2 first, Re7 meets the other move order, and after ...Kd1, f5 begins the same race. The king move Kf8 is essential preparation; the pawn needs nearby support when it reaches f7. A seventh-rank pawn is not always a draw against a queen: central and knight-file pawns often lose, and even a bishop-pawn can lose when the enemy king is close enough to create mating threats. Here the black king has been drawn to d2, far from the promotion corner. The illustrative queen move in the replay simply shows f7 arriving; the defensive principle must continue afterward.',
    "Play the rook capture with check and count the black king's distance from f7. At the final position, try queen checks and use the king to stay near the pawn, watching for the stalemate resource when driven toward h8.",
    'Why is White willing to exchange a rook for one pawn?',
    'It reaches a drawable queen-versus-seventh-rank bishop-pawn position',
    'The supported f-pawn reaches the seventh rank before Black’s king can help the queen.',
    'A rook is always worth exactly one passed pawn',
    'The exact king placement and pawn file make this sacrifice draw; material values alone do not.',
    'The supported f-pawn reaches the seventh rank before Black’s king can help the queen.',
    highlights={0: 'Place the king near f7 before starting the pawn race.', 1: 'Advance the d-pawn, challenging White to stop both passers.', 2: 'Prepare the checking capture of the leading pawn.', 3: 'Advance the second pawn, hoping to force promotion.', 4: 'Give the rook for the d-pawn with check to gain a racing tempo.', 5: 'Accept the rook and draw the black king far from f7.', 6: 'Start the f-pawn race immediately.', 7: 'Promote, but the king is too distant to help stop the f-pawn in time.', 8: 'Advance toward the seventh-rank drawing setup.', 9: 'An illustrative queen move; it does not prevent the supported advance.', 10: 'Reach the bishop-pawn drawing position with the white king nearby.'},
    extra=())

_add(
    'app-draw-11',
    'A knight hides while the king chases the rook',
    395,
    'M. Liburkin, 1946',
    'ka8 Nb7 pe6 rd5 Nf1 Kc1',
    'Ne3 Rd3 Kc2 Rxe3 Nd8 Re2+ Kd3 Re1 Kd2 Re4 Kd3 Re5 Kc3 Rc5+ Kb4 Re5 Kc3',
    "White has two knights against a rook and pawn. One knight is attacked by the black king, but saving that knight is not the point. White offers the other knight, then uses the survivor's protected retreat and the king's activity to deny Black a useful rook position.",
    'Ne3 develops the f1-knight with an attack on the rook. The source continues ...Rd3, and Kc2 attacks the rook on d3 while inviting ...Rxe3. It does not directly protect Nb7: if Black captures that knight with ...Kxb7, Kxd3 takes the rook and removes Black’s winning material advantage. Nd8 then places the surviving knight on a square where it is difficult to attack without allowing a fork or an active king response. Black checks with ...Re2+, and the white king approaches through d3 and d2. After ...Re5, Kc3 starts a small pursuit: ...Rc5+ is met by Kb4, and ...Re5 by Kc3 again. The rook cannot make useful progress without becoming a target.',
    'Black can capture the b7-knight at the beginning, but Nxd5 then removes the rook and reaches a drawable pawn ending after ...exd5. In the main line, a black king move after Nd8 allows White to attack the rook; ...Re5 can then meet a knight fork on c6. The repeated king-and-rook arrangement demonstrates the defensive mechanism, but the replay contains only two occurrences of that position, so it is not yet an automatic threefold claim. White must keep choosing the active king squares instead of retreating passively and allowing the rook to coordinate with its king.',
    'Compare sacrificing the e3-knight with abandoning the b7-knight without compensation. After Nd8, test a black king move and look for a fork. Then play the king chase until the same position occurs three times, keeping track of whose turn it is.',
    'Why does White offer the e3-knight?',
    'It leaves the other knight and king in a coordinated drawing arrangement',
    'The king chase, knight forks, and exchange resources prevent Black from making progress.',
    'Either knight can be sacrificed with no calculation',
    'The surviving knight’s d8 square and the king’s active route are essential.',
    'The king chase, knight forks, and exchange resources prevent Black from making progress.',
    highlights={0: 'Attack the rook with the knight that White is willing to sacrifice.', 1: 'Keep the rook active and invite the king forward.', 2: 'Attack the rook on d3. The b7-knight is protected only indirectly: ...Kxb7 allows Kxd3.', 3: 'Take the offered knight, leaving the other knight a useful retreat.', 4: 'Preserve the knight on d8, with forks and king attacks against rook manoeuvres.', 5: 'Check to try to drive the king away.', 6: 'Approach the rook instead of retreating passively.', 7: "Move out of the king's attack while retaining checking resources.", 8: 'Keep the king ready to challenge the rook.', 9: 'Reposition the rook while trying to support the e-pawn.', 10: 'Continue the active king pursuit.', 11: 'Defend the pawn and seek a stable rook square.', 12: 'Start the small king chase that prevents progress.', 13: 'Check from c5, hoping to push the king away.', 14: 'Attack the rook and keep the active defensive arrangement.', 15: 'Return to e5 rather than lose the rook.', 16: 'Re-establish the same position; this is the second occurrence, so a third is needed for a claim.'},
    extra=())
