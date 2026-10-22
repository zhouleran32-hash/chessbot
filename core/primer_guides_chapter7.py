"""Self-contained Chapter 7 teaching; printed page references use the supplied edition.

Game scores and two compositions come from the user's book; all annotations
and explanations are newly written. Other examples are labelled illustrations.
"""
from core.primer_build import after
from core.primer_guides_chapter1 import section, example, check, guide
from core.primer_chapter7 import START, OPEN, ITALIAN, MORPHY, BAIT, SANCHEZ, FURMAN, QUIET, QUIET_LINE, EXCELSIOR, EXCELSIOR_LINE, REPETITION

GUIDES = {}


def q(identifier, prompt, answer, why, alternative, why_not):
    return check(identifier, prompt, (answer, True, why), (alternative, False, why_not))


def teach(key, pages, goals, sections, examples, questions, pitfalls, recap):
    GUIDES['ch7-' + key] = guide(pages, goals, sections, examples, pitfalls, questions, recap)


teach('tasks', (241,242),
    ('Explain what development achieves rather than just naming a move.', 'Make an opening plan that includes the whole army and responds to threats.'),
    (
        section('Three jobs that support one another', '''
            At the starting position your rooks and bishops are blocked, your queen has little room, and your king sits on a central file.
            The opening turns that crowded arrangement into a team. Development gives pieces useful squares and open lines. Central
            control makes it easier for those pieces to travel and harder for the opponent to advance freely. King safety keeps your
            developing army from being interrupted by threats against its most important piece. These jobs overlap: e4 occupies a
            central square and opens the f1 bishop; Nf3 develops and attacks e5; castling moves the king and activates a rook together.
            Before choosing, finish this sentence: this move helps because it changes these particular squares or lines.
        '''),
        section('A plan is a starting direction, not a fixed script', '''
            A practical beginner plan is a central pawn move, the kingside knight and bishop, castling, then the remaining minor pieces.
            Minor pieces means bishops and knights. This is a useful order to understand, not a promise that you can ignore Black for
            five moves. If a piece is attacked, a mate is threatened, or a safe capture wins material, investigate that before continuing
            the routine. Conversely, do not abandon useful development just because a queen move looks exciting. In the example both
            sides make reasonable choices; none of the shown replies is forced. You are learning the jobs, so that you can adapt when
            the next opponent chooses another move.
        '''),
        section('Measure the position after the move', '''
            Ask how many pieces can actually participate if the centre opens. A bishop outside its starting square but trapped behind
            your pawns may contribute less than it appears. An undeveloped rook might become active immediately after castling, but
            not if the file in front of it stays blocked. Compare both players, not your side alone: Black is trying to develop and
            challenge your centre too. At your level, a reliable routine is to check the opponent's threat, check your loose pieces,
            choose a useful developing candidate, and inspect the resulting board for checks and captures. After a game, find the
            first move where your army stopped cooperating; the final blunder often began with that earlier loss of coordination.
        '''),
    ),
    (example('An ordinary opening with a job on every move', START, ITALIAN+('O-O','Nf6'), (
        'Illustration: begin with both armies blocked. Track which move releases which piece.',
        'e4 takes space and opens a route for the f1 bishop.', '...e5 challenges the centre and opens Black’s f8 bishop.',
        'Nf3 develops toward the centre and attacks e5.', '...Nc6 develops while protecting the attacked pawn.',
        'Bc4 develops on the diagonal toward f7.', '...Bc5 gives Black a comparable active bishop.',
        'Castling puts the king on g1 and brings a rook to f1.', '...Nf6 develops another piece and attacks e4. White must now consider that threat.'
    )),),
    (q('job','What makes Nf3 a useful developing move here?','It adds central influence and attacks e5','The piece has a concrete job as soon as it arrives.','It guarantees an immediate win','Black can defend and develop; one good move does not win the game.'),
     q('priority','Your planned bishop move allows mate next turn. What comes first?','Answer the mating threat','A plan must respect the actual position.','Finish the memorized development order','No development plan excuses allowing an immediate mate.')),
    ('Do not count a piece as useful merely because it moved.', 'Check the opponent’s last move before continuing your own plan.'),
    ('Develop with a job.', 'Connect central control, development and safety.', 'Reassess after every reply.'))

teach('centre', (241,245),
    ('Distinguish occupying a square from controlling it.', 'Explain why a large pawn centre still needs support.'),
    (
        section('Squares, influence and travel', '''
            The centre in the narrow sense consists of d4, e4, d5 and e5. The extended centre stretches from c3 to f6.
            Pieces placed near this region can often switch between the two wings quickly. A knight on f3 influences d4 and e5
            without occupying either square. A pawn on d4 occupies d4 and attacks c5 and e5, but does not protect the square it stands
            on. That distinction matters when you count defenders. Your aim is useful access and influence: can your pieces reach
            good squares, can your opponent chase them away, and can you support a central advance? A decorative pawn on e5 that
            must be defended by every piece is not automatically a strong centre.
        '''),
        section('A centre is a structure with a base', '''
            In a d4–e5 white pawn chain, d4 supports e5. Attacking d4 with ...c5 challenges the chain at its base; attacking e5
            with ...f6 is another common lever in suitable positions. A lever is a pawn advance that creates a capture and can
            change the structure. Before pushing again, count how your pawns will be supported after the move. A pawn cannot retreat,
            so an ambitious advance may leave squares behind it permanently weak. The book illustrates both strong centres and ways
            of undermining them. Therefore do not judge the centre by territory alone: include piece support, targets, king safety,
            and whether the opponent can open a file against you.
        '''),
        section('Control from a distance is real control', '''
            The second illustration develops a bishop to g2. Its diagonal can pressure d5 through f3 and e4 when those squares
            are clear. This is called a fianchetto: a bishop develops behind an advanced b- or g-pawn. It does not mean the side has
            surrendered all interest in the centre. The central battle continues through different pieces and pawn breaks. For a
            beginner, direct central play is often easier to understand, but avoid declaring other sound systems wrong merely because
            they look different. Before each replay move, name one central square each side influences. Then ask what would change
            if a pawn moved or a piece were exchanged. You are learning to read a position rather than identify an opening by name.
        '''),
    ),
    (example('Direct occupation with support', START, ('d4','d5','Nf3','Nf6','c4','e6'), (
        'An illustration of central occupation and a challenge to its support.', 'd4 occupies a central square and attacks e5.',
        '...d5 occupies the opposing central square and controls e4.', 'Nf3 supports d4 and controls e5.',
        '...Nf6 supports d5 and controls e4.', 'c4 challenges the d5 pawn; White is attacking the centre from the side.',
        '...e6 supports d5 and opens the f8 bishop. The centre is contested, not settled.'
    )), example('A bishop can contest the centre from g2', START, ('g3','d5','Bg2','Nf6','Nf3'), (
        'This is an illustration, not a recommendation that g3 is compulsory.', 'g3 prepares Bg2 and changes the kingside pawn cover.',
        '...d5 takes central space while White prepares indirect pressure.', 'Bg2 looks along the long diagonal toward d5.',
        '...Nf6 develops and supports d5.', 'Nf3 adds influence over d4 and e5. Both occupation and long-range pressure matter.'
    ))),
    (q('control','Does a white pawn on d4 protect d4?','No; it attacks c5 and e5','A pawn does not defend its own square.','Yes, every piece protects the square it occupies','A piece can be captured unless another piece protects its square.'),
     q('size','When is a big pawn centre vulnerable?','When its support can be undermined and its pawns become targets','Space is useful only if the position can sustain it.','Never; more advanced central pawns always win','Pawn advances create weaknesses as well as space.')),
    ('Count attackers on actual squares.', 'Do not confuse central space with an unbreakable centre.'),
    ('Occupation and control differ.', 'Find the chain’s base.', 'Evaluate support and possible pawn breaks.'))

teach('tempo', (242,248),
    ('Explain what a lost tempo costs in development.', 'Identify justified repeat moves and unnecessary ones.'),
    (
        section('Time matters because the opponent also improves', '''
            Each turn gives you one move and then gives your opponent one. If you spend your move undoing the last one,
            the other player may bring another piece into play. That relative opportunity is why time matters. A tempo is one
            move's worth of time, but its value depends on the position. In a closed, quiet structure you may have time for a
            regrouping. In an open position with an exposed king, one delay can allow a decisive check. Compare useful activity at
            the end of the sequence. Ten moves with one knight are not ten developed pieces; one knight on a stable, powerful square
            may still be worth several moves if the route achieves something concrete.
        '''),
        section('A developing attack earns attention, not a magical extra turn', '''
            Developing with tempo means improving a piece while making a threat the opponent needs to meet. After an early queen
            sortie, a knight can develop while attacking that queen. The defender still chooses a reply, and may sometimes answer with
            a stronger threat or a useful developing defence. Do not count every attack as a forced retreat before checking the
            possibilities. Ask whether the attacked piece can be captured, whether it can move with check, and whether your own piece
            would be trapped after taking. In our quiet Italian illustration, Nc3 simply develops the unused knight; it is useful even
            though it does not force Black into a particular response.
        '''),
        section('Exceptions are decided by a concrete benefit', '''
            Repeating a piece move is correct when the piece is threatened, when it wins material safely, when it creates a sound
            decisive attack, or when it reaches a better necessary square. Do not leave a knight hanging because someone said
            never move a piece twice. Equally, do not call every speculative jump an exception. Calculate the benefit and compare it
            with developing the least useful piece. In your own games, mark repeat moves during the first ten moves. For each,
            write a reason: forced escape, gain of material, useful regrouping, or no clear purpose. This makes the principle measurable
            without pretending that all openings have the same ideal number of moves. Good time use is purposeful cooperation.
        '''),
    ),
    (example('The second knight joins the army', after(ITALIAN), ('Nc3','Nf6','d3','d6','O-O','O-O'), (
        'Illustrative balanced development: each side has a knight and bishop out.', 'Nc3 develops the previously unused queen knight.',
        '...Nf6 develops Black’s second knight and attacks e4.', 'd3 supports e4 and releases the c1 bishop.',
        '...d6 supports e5 and frees Black’s c8 bishop.', 'White castles instead of making an unnecessary bishop retreat.',
        'Black castles too. Both sides have used their time to organize a larger army.'
    )),),
    (q('repeat','A knight is attacked by a pawn. Must you leave it because it already moved?','No; answer the threat and assess the best square','The development principle is subordinate to concrete safety.','Yes; moving twice is forbidden in the opening','Chess has no such rule, and losing the knight is normally much worse.'),
     q('count','How should you compare development after an exchange?','Count the useful pieces and available lines that remain','Moves already spent on captured pieces no longer provide activity.','Count only the total moves each player has made','Alternating play gives similar move counts even when development differs greatly.')),
    ('An attack on a queen is not automatically a winning tempo.', 'Do not sacrifice safety to follow a slogan.'),
    ('Compare useful activity.', 'Repeat moves need a reason.', 'Review wasted moves in your own openings.'))

teach('bishop', (246,248),
    ('Explain Bc4 and Bb5 as different active plans.', 'Recognize why pressure on a defender is not the same as winning its pawn.'),
    (
        section('Why a knight often comes first', '''
            After e4 and ...e5, the g1 knight usually belongs on f3: it influences d4 and e5, attacks a central pawn, and leaves
            the f1 bishop free. Ne2 occupies part of that bishop's route, while Nh3 gives the knight less central influence.
            These comparisons explain the book's advice to develop knights before deciding bishop squares. It is a flexible guide,
            not a rule that a bishop opening is unsound. A different pawn structure may make e2 a good knight square or justify
            an early bishop move. Read the actual routes. A good developing square should connect to the centre and leave other pieces
            room to join in.
        '''),
        section('What the two bishop plans really do', '''
            Bc4 points at f7, a pawn initially guarded only by Black's king. That does not mean Bxf7 wins: the king may recapture
            unless a concrete tactic prevents it. The bishop also helps control d5 and clears f1 for castling. Bb5 instead attacks
            Nc6, an important defender of e5. This is the Spanish, or Ruy Lopez, idea. Pressure on the defender creates future
            possibilities, but the pawn is not automatically free today. Black can answer by developing, challenging the bishop, or
            arranging a tactical recapture. In the exercise either Bc4 or Bb5 is accepted because the task deliberately compares
            two useful plans rather than pretending that only one opening move can be good.
        '''),
        section('Calculate after you remove a defender', '''
            In the second replay White exchanges on c6, then grabs e5. Black's ...Qd4 attacks the knight and the e4 pawn at once.
            After the knight retreats, ...Qxe4+ restores material. This does not say that Bxc6 is a bad move; it says that removing
            a visible defender does not end the calculation. Look for checks, attacks on a more valuable piece, and a second target.
            Before taking e5 in your own game, count what is attacked after the capture, including your king on e1. Pause before
            the queen move in the replay and try to find it yourself. That habit connects the chapter's development advice with the
            calculation and combination skills you learned in chapters 4 and 5.
        '''),
    ),
    (example('A bishop plan with a safe king', after(OPEN+('Nf3','Nc6')), ('Bc4','Bc5','O-O','Nf6','d3'), (
        'The knight squares are settled for now; choose a bishop job.', 'Bc4 develops toward f7 and d5.',
        '...Bc5 develops Black’s bishop with the same general aims.', 'White castles while the path is clear.',
        '...Nf6 attacks e4; White must not ignore that central pawn.', 'd3 supports e4 and releases the other bishop. This is one sensible setup.'
    )), example('Removing Nc6 does not simply win e5', START, ('e4','e5','Nf3','Nc6','Bb5','a6','Bxc6','dxc6','Nxe5','Qd4','Nf3','Qxe4+','Qe2'), (
        'Illustration of a tactical resource behind the Spanish opening structure.', 'White occupies e4.', 'Black occupies e5.',
        'The knight attacks e5.', 'Black develops its defender.', 'The bishop attacks that defender.', '...a6 questions the bishop.',
        'White exchanges the defender.', 'The d-pawn recaptures, opening the queen’s route along the d-file.',
        'White takes e5, but must check Black’s double attack.', '...Qd4 attacks Ne5 and e4.', 'The knight escapes.',
        'Black recovers the pawn with check.', 'Qe2 blocks the check and offers a queen exchange. The supposed simple pawn win has disappeared.'
    ))),
    (q('bishop-job','What is Bb5 doing immediately?','Pressuring a defender of e5','It creates central pressure; a pawn win still needs calculation.','Forcing Black to lose e5 on the next move','Black has tactical and developmental replies.'),
     q('first','Is “knights before bishops” a law of chess?','No; it is a useful guide when knight squares are clearer','The position and concrete threats decide.','Yes; any bishop moved first is a blunder','Sound openings can develop a bishop early.')),
    ('Pressure on f7 is not permission to sacrifice blindly.', 'Look beyond the removal of a defender.'),
    ('Choose a useful diagonal.', 'Leave room for other pieces.', 'Calculate the opponent’s checks and double attacks.'))

teach('castle', (241,242),
    ('Explain the king-safety and rook-activity roles of castling.', 'Finish development after the king is safe.'),
    (
        section('Castling solves two linked problems', '''
            An uncastled king on e1 may become a target if the e-file or a central diagonal opens. The h1 rook also begins far
            from the central struggle. Kingside castling moves the king to g1 and the rook to f1 in one turn. It is possible only
            when the king and that rook retain their rights, the path is clear, the king is not in check, and the king does not
            cross or land on an attacked square. Always inspect the resulting king position as well as the legal conditions. A
            legal castle into an attack can still be a bad choice. The common early castle works because it is usually both safe
            and efficient, not because a move number makes it mandatory.
        '''),
        section('Do not stop developing once the king has moved', '''
            In the example Nc3 brings out the queen knight and d3 opens the c1 bishop. Be3 gives that bishop a job. Only then
            does Qd2 help connect the rooks: with the back-rank pieces cleared away, the rooks can protect one another and choose
            useful files. A connected pair is not automatically active. On a blocked file a rook may have little work; look for
            an open file, a half-open file with an enemy pawn target, or a central break that will create one. This is why the
            book connects development to a plan. You should be able to explain what the next piece will do, not merely announce
            that you have completed the opening.
        '''),
        section('Choose a safe side and a purposeful next move', '''
            Queenside castling also activates a rook, directly on d1, but the king on c1 can be closer to queenside attacks.
            The a2 pawn is no longer directly protected by its rook, and a later Kb1 may be useful. That is a concrete reason,
            not an automatic extra move in every position. With either castle, avoid unnecessary advances of the pawns protecting
            your king. At your level a useful review question is: when could I first castle safely, and what did I gain by delaying?
            Sometimes the answer is a tactic or a better plan; sometimes it is simply that you forgot. Learn to recognize the
            difference without treating a flexible principle as a prohibition.
        '''),
    ),
    (example('Castling begins the second half of development', after(ITALIAN), ('O-O','Nf6','d3','d6','Nc3','O-O','Be3','Bb6','Qd2'), (
        'Both kingside paths are clear. This is a quiet illustrative continuation.', 'White secures the king and activates Rf1.',
        'Black develops and attacks e4.', 'd3 supports e4 while releasing Bc1.', '...d6 supports e5 and releases Bc8.',
        'Nc3 develops the second knight.', 'Black castles too.', 'Be3 brings the last minor piece into play.',
        '...Bb6 preserves the bishop from an immediate exchange; other replies are possible.',
        'Qd2 clears the back rank, so Ra1 and Rf1 are connected. Their useful files will depend on what opens next.'
    )),),
    (q('rights','Can you castle through an attacked square if the final square is safe?','No','The king may not cross check.','Yes, only the final square matters','The transit square must also be safe.'),
     q('rooks','What does connecting the rooks prepare?','Cooperation and access to useful files','Activity still depends on which files are available.','An automatic win of material','Connection improves coordination but forces no immediate gain.')),
    ('Legal castling is not always strategically safe.', 'Castling is not the end of developing the rest of the army.'),
    ('Check the whole castling path.', 'Finish the minor pieces.', 'Connect rooks and choose useful files.'))

teach('pawns', (246,248),
    ('Use pawn moves for development, support or a concrete challenge.', 'Recognize both useful flank moves and purposeless pawn pushing.'),
    (
        section('A pawn move should explain a piece’s future', '''
            Early pawn moves serve the pieces. e4 frees Bf1, d4 or d3 frees Bc1, and a supporting pawn can let a knight stay
            on a useful square. If you cannot identify what a pawn move improves, compare it with developing a piece. A series
            such as a4 and h4 may look active while the bishops remain blocked and the king stays central. The book recommends
            restraint with noncentral pawns as a beginner training method. It is not saying that c4, c5, g3 or b3 are always bad.
            Those moves can be part of coherent central pressure or bishop development. The question is what the particular move
            accomplishes now and what irreversible squares it leaves weak.
        '''),
        section('Compare a supporting move with a break', '''
            After the Italian setup and ...Nf6, d3 supports e4 with a pawn and gives the c1 bishop a diagonal. The sharper d4
            challenges e5 and can open the centre after exchanges. Both ideas can be playable; they produce different calculation
            demands. If you choose d4, follow the captures and check whether e4 and the king remain safe. If you choose d3,
            remember that a quieter position still requires development and a later plan. Our exercise asks for the one-square
            support move, so d4 is marked as not answering that specific task, not as a general chess blunder. Learn the difference
            between following an instruction and claiming that only one legal move is good.
        '''),
        section('Never make a pawn move just to pass the turn', '''
            Pawns cannot move backward. h3 may prevent ...Bg4, but also consumes time and changes the king's cover; a3 may
            ask a bishop a question, but is not useful when no bishop threatens to come there. Check whether the threatened pin
            would actually matter before preventing it. Conversely, a necessary pawn move that stops mate deserves priority over
            a developing move. In your next game, give each early pawn move one label: opens a piece, supports the centre, attacks
            the centre, meets a threat, or prepares a specific plan. If none fits, look for a better use of the turn. This makes
            pawn economy a thinking habit instead of an arbitrary limit on the number of pawn moves.
        '''),
    ),
    (example('One pawn move serves two jobs', after(ITALIAN+('O-O','Nf6')), ('d3','d6','Nc3','O-O','Be3'), (
        'White’s e4 pawn is attacked and Bc1 needs a route.', 'd3 protects e4 and frees the c1–h6 diagonal.',
        '...d6 similarly protects e5 and frees Bc8.', 'Nc3 adds another defender of e4 and develops.',
        'Black castles; the illustrative position remains balanced in development.', 'Be3 now uses the diagonal that d3 opened.'
    )),),
    (q('pawn-job','Why is d3 useful here?','It supports e4 and opens Bc1','The pawn move serves a central and a developmental job.','It wins e5 immediately','Supporting e4 does not automatically win an enemy pawn.'),
     q('flank','Is every early c-pawn or g-pawn move wrong?','No; judge its purpose and resulting position','Sound systems use these pawns to contest the centre or develop bishops.','Yes; only d- and e-pawns may move','The book’s simplified advice is not a rule of legal or sound play.')),
    ('Do not push the king’s pawns without checking weaknesses.', 'A quieter support move still needs an active follow-up.'),
    ('Give every pawn move a purpose.', 'Compare support with a break.', 'Remember that pawn changes cannot be undone.'))

teach('queen', (247,248),
    ('Defend f7 before chasing a queen.', 'Turn an opponent’s early queen movement into useful development.'),
    (
        section('Respect the threat before criticizing the move', '''
            After e4 e5 Qh5 Nc6 Bc4, White threatens Qxf7 mate. The queen on h5 attacks f7 diagonally and the bishop on c4
            protects the queen when it arrives. The king cannot capture a protected queen. Black must address that concrete threat.
            A careless ...Nf6 attacks the queen, but White can ignore the attack and deliver mate. This is an important exception
            to a common shortcut: attacking a queen does not force it to retreat if it has a stronger move. Name the opponent's
            immediate threat in words before selecting your developing move. At 564 Elo, catching this one-move threat matters more
            than remembering which opening has the better long-term reputation.
        '''),
        section('Make the queen move while improving your position', '''
            Here ...g6 attacks Qh5 and blocks its diagonal to f7. White can retreat to f3 and renew the pressure on f7 along
            the f-file. Now ...Nf6 is useful: the knight develops to a natural square and interrupts that file. The difference from
            the earlier ...Nf6 is the queen's location, not the name of the move. Check the board after every reply. Black should
            then prepare a safe castle and complete the other pieces, rather than chase the queen with endless pawn advances.
            The illustrated continuation is one reasonable defensive route; it is not a forced win for Black or a claim that every
            early queen opening loses. It demonstrates that threats can often be met with useful moves.
        '''),
        section('Apply the same lesson when you are the attacker', '''
            An early queen attack may beat an opponent who overlooks mate, but a stronger defender can gain time by developing
            against it. Ask what happens after the threat is stopped. Will your knight and bishop join the attack, or will the
            queen have to retreat alone? Avoid judging a move only by the worst reply. A queen move can be justified when it
            recaptures, creates a concrete tactical threat, or fits a sound structure, as Qxf3 does later in the Morphy lesson.
            The principle is efficient cooperation. After a game with an early queen attack, identify the moment the defender could
            both answer the threat and develop. Learn that moment from both sides of the board.
        '''),
    ),
    (example('Stop the mate, then develop against the queen', after(('e4','e5','Qh5','Nc6','Bc4')), ('g6','Qf3','Nf6','Ne2','Bg7','d3','O-O'), (
        'Black must first stop Qxf7 mate.', '...g6 blocks the h5–f7 diagonal and attacks the queen.',
        'Qf3 renews pressure down the f-file. Black reassesses the actual threat.', '...Nf6 now blocks that file while developing.',
        'Ne2 develops White’s knight because f3 is occupied by its queen.', '...Bg7 develops the bishop behind the g-pawn.',
        'd3 protects e4 and opens Bc1.', 'Black castles. White’s initial threat has not produced a forced gain.'
    )), example('The attractive attack on the queen that loses immediately', after(('e4','e5','Qh5','Nc6','Bc4')), ('Nf6','Qxf7#'), (
        'Compare this with the correct defensive order.', '...Nf6 attacks Qh5 but leaves the diagonal to f7 open.',
        'Qxf7 is mate: the bishop protects the queen and the king has no legal escape.'
    ))),
    (q('threat','Why does immediate ...Nf6 fail in the practice position?','Qxf7 is mate before the queen needs to retreat','A decisive threat outranks the attack on the queen.','A knight is never allowed to attack a queen','Attacking a queen is legal; it simply fails tactically here.'),
     q('lesson','After stopping the queen’s threat, what is the sound aim?','Complete development while keeping the king safe','Useful moves build a durable position.','Keep pushing pawns at the queen indefinitely','A long chase can weaken your king and leave your own army undeveloped.')),
    ('Never assume an attacked queen must retreat.', 'Do not replace development with a pawn chase.'),
    ('Name the immediate threat.', 'Defend with a useful move.', 'Recheck the queen’s new lines after it retreats.'))

teach('defend-e5', (247,248),
    ('Compare defending, counterattacking and obstructing your own pieces.', 'Separate the book’s beginner recommendation from an absolute opening verdict.'),
    (
        section('The same threat can have several sound answers', '''
            After 1.e4 e5 2.Nf3, White attacks e5. Black can develop the b8 knight to c6, defend with ...d6, or counterattack
            e4 with ...Nf6. The book recommends ...Nc6 as a clear beginner solution: a piece develops while a central pawn receives
            protection. That recommendation does not mean the other established systems are refuted. ...d6 creates a solid pawn
            support but reduces the f8 bishop's immediate freedom. ...Nf6, the Petroff idea, asks both sides to calculate captures
            and checks. The strategic job remains the same: maintain a viable centre while bringing the army out. Name the
            benefit and the cost of each move before deciding which type of position you understand best.
        '''),
        section('Why the defender’s route matters', '''
            Defending e5 with ...Bd6 puts a bishop in front of the d7 pawn, which then cannot move to release the c8 bishop.
            One piece solves a small problem by creating a larger traffic jam. A queen move such as ...Qe7 can block Bf8, and
            ...Qf6 can occupy the g8 knight's natural square. These moves are not illegal; the point is their effect on the whole
            army. The best defence is often a move that solves two jobs without obstructing another piece. Draw the intended routes
            of both bishops before placing a defender. This simple visual check helps explain why natural development is more useful
            than protecting a pawn with whichever piece happens to reach it.
        '''),
        section('Counterattacking does not remove the need to calculate', '''
            In the Petroff illustration, White takes e5. Black first plays ...d6, making the knight move, before capturing e4.
            If Black copies the capture immediately, White has Qe2, creating pressure along the e-file against the knight and king.
            You need not memorize the entire opening now. Understand the move-order issue: an attack on the king can change whether
            a piece is free to retreat or exchange. When facing an unfamiliar reply, do not panic because it differs from the
            demonstration. Identify checks, attacked pieces and central tension, then choose a move with a clear job. A short,
            understood variation is more useful than a long string of moves you cannot explain.
        '''),
    ),
    (example('A counterattack with careful move order', after(OPEN+('Nf3',)), ('Nf6','Nxe5','d6','Nf3','Nxe4','d4','d5'), (
        'Black has more than one sound way to address the attack on e5.', '...Nf6 attacks e4 rather than defending e5 directly.',
        'White captures the pawn and tests the move order.', '...d6 attacks the advanced knight before recapturing.',
        'Nf3 returns to a useful square.', '...Nxe4 recovers the pawn after White’s knight has been displaced.',
        'd4 opens Bc1 and challenges central squares.', '...d5 supports the knight. This illustrative line reaches a playable central struggle.'
    )),),
    (q('traffic','What is the drawback of ...Bd6 behind a pawn on d7?','It obstructs that pawn and delays Bc8','Development is about routes for the whole army.','A bishop cannot legally stand on d6','It can stand there, but legality does not make the placement efficient.'),
     q('alternatives','Does recommending ...Nc6 prove ...Nf6 is bad?','No; ...Nf6 is a sound counterattacking approach with its own calculation','Several opening moves can be good for different reasons.','Yes; every position has exactly one sound developing move','Quiet opening positions often offer multiple reasonable choices.')),
    ('Protecting one pawn can block several pieces.', 'Do not copy captures without checking intermediate threats.'),
    ('Defend and develop together when possible.', 'Trace the routes of your bishops.', 'Calculate a counterattack’s move order.'))

teach('f6', (247,248),
    ('Identify both the positional and tactical cost of an early ...f6.', 'Calculate an accepted sacrifice and a declined sacrifice separately.'),
    (
        section('A pawn defence can weaken the whole position', '''
            After e4 e5 Nf3, ...f6 defends e5 with a pawn but blocks Nf6 and vacates f7. The diagonal h5–e8 now has one fewer
            obstacle, and the king's surrounding squares are less secure. White can exploit these changes with ordinary development
            such as Bc4, or investigate the sharper Nxe5. The lesson is not that every f-pawn advance is wrong. In other structures
            it can be a justified central break or attacking move. Here the king is uncastled, the pieces are undeveloped, and
            the move obstructs a natural knight square while opening a checking route. Those concrete facts make it suspect.
            Explain the weakness before searching for a sacrifice.
        '''),
        section('Acceptance opens a forcing queen attack', '''
            After Nxe5 fxe5, Qh5+ checks along h5–g6–f7–e8. The f7 square has been vacated, so the diagonal is clear.
            The material count says White has sacrificed a knight, but checks can prevent Black from using the extra material.
            In one illustrative branch ...g6 allows Qxe5+, followed by Qxh8 if Black blocks with the queen: White recovers a rook.
            Another branch sends the king to e7, where further checks and developing attacks become possible. Do not merge these
            branches in your head. Reset the position at the decision point and analyze each reply on its own. This is precisely
            where chapter 4's disciplined calculation becomes more useful than an attractive first move.
        '''),
        section('The opponent need not accept the offer', '''
            Black can instead answer Nxe5 with ...Qe7. Now the queen attacks the knight and has checking resources on e4.
            The book recommends Nf3, allowing ...Qxe4+ and meeting the check with Be2. White can continue developing while Black's
            exposed queen and weakened f-pawn structure remain targets. The tempting Qh5+ followed by Nxg6 does not transpose into
            the accepted-sacrifice line: ...Qxe4+ changes the order of play. The practical lesson is to ask about refusal before
            playing any sacrifice. Your opponent controls the reply, so the move must be judged against the strongest resistance
            you can find, not just the branch that makes your intended attack look impressive.
        '''),
    ),
    (example('Acceptance: the checking diagonal opens', after(OPEN+('Nf3','f6')), ('Nxe5','fxe5','Qh5+','g6','Qxe5+','Qe7','Qxh8'), (
        'White can investigate a concrete knight sacrifice rather than merely recite an opening rule.',
        'Nxe5 offers the knight; Black is not forced to accept.', '...fxe5 accepts and clears f7.',
        'Qh5+ uses the newly opened diagonal.', '...g6 blocks, but leaves a forcing capture on e5.',
        'Qxe5+ wins the pawn with check and points toward h8.', '...Qe7 is an illustrative blocking reply.',
        'Qxh8 captures the rook. The attack has recovered more than the sacrificed knight, although play continues.'
    )), example('Refusal: analyze a different branch', after(OPEN+('Nf3','f6')), ('Nxe5','Qe7','Nf3','Qxe4+','Be2'), (
        'Reset to the same starting position before considering a different defence.', 'White offers Nxe5 again.',
        '...Qe7 declines immediate acceptance and attacks the knight.', 'Nf3 withdraws without entering the misleading Qh5+ branch.',
        'Black recovers the pawn with check.', 'Be2 blocks while developing. White can aim to castle and later attack the queen with development.'
    ))),
    (q('diagonal','Which change makes Qh5+ possible after ...fxe5?','The f7 square has become empty','The h5–e8 diagonal now reaches the king.','The queen is allowed to jump over the f-pawn','Queens never jump over pieces.'),
     q('refusal','What must you check before relying on a sacrifice?','The opponent’s best refusal as well as acceptance','The opponent chooses the reply.','Only the line where the offered piece is captured','A sound-looking accepted line does not prove the whole sacrifice.')),
    ('Do not confuse the ...fxe5 and ...Qe7 branches.', 'An f-pawn weakness needs concrete exploitation, not automatic sacrifice.'),
    ('Name the vacated square.', 'Analyze forcing replies separately.', 'Include refusal in every sacrifice calculation.'))

teach('exchange-tempo', (248,249),
    ('Track useful activity after an exchange.', 'Explain why a purposeful queen recapture can be good development.'),
    (
        section('Equal material, unequal use of time', '''
            In the Morphy sequence, Black's bishop travels from c8 to g4 and then captures Nf3. That bishop has used two moves;
            the knight it captures used only one. White recaptures with Qxf3, bringing the queen to an active square as part of
            recovering material. After ...dxe5, White has a developed queen and the move, while Black's other minor pieces are still
            at home. The material traded was equal, but the resulting activity differs. You cannot see this by counting material
            points alone. Count which useful pieces remain and how the next move can add another one. Time spent on a piece that
            has left the board no longer contributes directly to your development.
        '''),
        section('The queen warning has a reason, not a blanket ban', '''
            Earlier lessons warned against bringing the queen out alone. Qxf3 has a concrete purpose: it recaptures the bishop,
            preserves the kingside pawn structure, and can cooperate with Bc4 against f7. A queen move is not bad simply because
            it is early. The relevant questions are whether it loses time to developing attacks, blocks your pieces, or abandons
            necessary defensive work. In this position White can promptly add a bishop and knight, so the queen does not have to
            fight by itself. Reconcile the examples by looking at their mechanisms. Chess principles help you ask useful questions;
            they do not replace the calculation and comparison of actual moves.
        '''),
        section('When exchanging helps the other side', '''
            Before an exchange, imagine both the capture and the recapture. Does the enemy rook gain an open file? Does a knight
            leave a poor square and arrive centrally? Does a queen recapture without losing time? Conversely, an exchange can be
            excellent if it removes a dangerous attacker, damages a pawn structure, or simplifies a winning ending. You need the
            final arrangement to decide. In your own opening reviews, pause one move before each voluntary exchange and predict the
            piece that will recapture. If the opponent gains useful development while you lose an active piece, identify what you
            receive in return. If you cannot name a benefit, postponing the exchange may preserve more useful pressure.
        '''),
    ),
    (example('Morphy’s opening: development survives the exchange', START, MORPHY[:12], (
        'Book example, with fresh annotations: track development rather than only material.', 'e4 opens a bishop and occupies the centre.',
        '...e5 gives Black central space.', 'Nf3 develops and attacks e5.', '...d6 supports e5 but narrows Bf8’s route.',
        'd4 challenges the centre and opens Bc1.', '...Bg4 develops the bishop by pinning Nf3 to the queen.',
        'dxe5 asks Black to resolve the central tension.', '...Bxf3 exchanges the bishop that has spent two moves for the knight that spent one.',
        'Qxf3 recaptures, preserves the pawn shield, and puts the queen into the game.', '...dxe5 restores the pawn in the centre.',
        'Bc4 adds an attacker toward f7.', '...Nf6 develops a new defender, but White already has coordinated queen-and-bishop pressure.'
    )),),
    (q('exchange','Why can the bishop-for-knight exchange lose time here?','The recapture develops White’s queen while Black’s moved bishop disappears','The useful activity remaining after the exchange is what matters.','A bishop is always worth more than a knight','The point here is development, not a universal piece-value rule.'),
     q('queen-recapture','Why is Qxf3 consistent with sensible opening principles?','It recaptures and supports a concrete developing plan','Early queen moves can be justified by the actual position.','Every queen recapture is automatically best','Other positions may expose the queen or damage coordination.')),
    ('A trade of equal-valued pieces can have unequal positional effects.', 'Always include the recapture in your assessment.'),
    ('Count activity after the exchange.', 'Check what the recapture improves.', 'Apply the reason behind an opening principle.'))

teach('open-lines', (242,244),
    ('Explain when opening a line benefits the developed side.', 'Follow a complete forcing finish and identify each removed defender.'),
    (
        section('A lead in development must be used while it exists', '''
            When your pieces are ready and the opponent's are still blocked, an open line can let your active army reach the
            king first. If you merely wait, the opponent may develop and erase that advantage. Nevertheless, opening the centre
            is not automatically good: inspect your own king, the opponent's checks, and which rook or bishop will use the new
            route. In the book's examples, central control and accessible files turn activity into a concrete attack. Our complete
            demonstration is Morphy's familiar short game. Its early exchanges appeared in the previous lesson; now follow how
            the d-file and the diagonal toward d8 combine. Every sacrifice has a job that can be named on the board.
        '''),
        section('Connect the army before the forcing sequence', '''
            White develops both bishops and the queen knight before using the rooks. When Black advances ...b5, Nxb5 opens
            lines at a material cost; Bxb5+ then forces Black to spend time protecting the king. Queenside castling brings Ra1
            to d1 in a single move. The point is not simply that castling is good: this particular rook arrives on the file where
            the enemy king and defenders are vulnerable. Pause at that position. Identify the knight on d7, the rook supporting
            it, and the white bishop that can capture it later. The final attack works because these pieces are connected, not
            because White gives check indiscriminately. Earlier defensive improvements for Black would require a different plan.
        '''),
        section('Work backward from the mate, then verify forward', '''
            Rd8 mate will need an open d-file and a way to stop Black's knight from blocking or capturing. The queen sacrifice
            Qb8+ pulls the knight away from d7; after ...Nxb8 the rook reaches d8. Before that, exchanges on d7 remove other
            defenders and bring the second rook to d1. You can understand the idea backward, but must verify the legal replies
            forward. At each check ask whether Black can capture, block, or move the king. When the line ends, inspect every
            flight square before calling it mate. Carry the method into your games: identify a desired final position, find the
            obstacle, and calculate whether forcing moves really remove it. Do not copy the sacrifice without the required support.
        '''),
    ),
    (example('Morphy’s complete development-and-d-file attack', START, MORPHY, (
        'The complete short game is shown so the final sacrifices have a clear origin.',
        'e4 opens the kingside bishop.', '...e5 contests the centre.', 'Nf3 develops with an attack on e5.', '...d6 supports e5.',
        'd4 challenges the centre and frees Bc1.', '...Bg4 pins Nf3 to the queen.', 'dxe5 changes the central pawn structure.',
        '...Bxf3 exchanges the bishop for the knight.', 'Qxf3 recaptures with useful activity.', '...dxe5 restores central material.',
        'Bc4 adds pressure toward f7.', '...Nf6 develops but leaves White able to increase pressure.',
        'Qb3 attacks f7 and b7.', '...Qe7 guards f7 and arranges a queen-exchange resource if White takes b7.',
        'Nc3 adds another piece instead of chasing the b7 pawn.', '...c6 prepares queenside activity but spends a pawn move.',
        'Bg5 develops with a pin of Nf6 to Qe7.', '...b5 attacks Bc4 but offers a way to open lines.',
        'Nxb5 sacrifices the knight to disturb the queenside structure.', '...cxb5 accepts; White must have calculated the next check.',
        'Bxb5+ develops the attack on the uncastled king.', '...Nbd7 blocks the check.',
        'Queenside castling brings the last rook to the d-file.', '...Rd8 adds a defender along that file.',
        'Rxd7 removes the blocking knight at a rook’s cost.', '...Rxd7 recaptures; this is the h8 rook that had travelled to d8.',
        'Rd1 brings the second rook onto the same file.', '...Qe6 moves the queen and gives the f6 knight room to recapture on d7.',
        'Bxd7+ removes the remaining defending rook.', '...Nxd7 blocks the file once more.',
        'Qb8+ offers the queen to drag that knight away.', '...Nxb8 is the only legal reply to the check.',
        'Rd8 is mate: the rook attacks e8, the bishop covers d8, and Black has no escape, block or capture.'
    )),),
    (q('line','Why is opening a file useful to the better-developed side?','Its active pieces may use the file before the opponent can organize','The advantage is in access and timing, not the empty file by itself.','Every open file wins automatically','An unused or enemy-controlled file may provide no benefit.'),
     q('deflection','What does Qb8+ accomplish at the finish?','It draws Nd7 away from the d-file','After the knight captures, Rd8 can mate.','It wins a black pawn','The queen is offered for a mating mechanism, not a pawn.')),
    ('Do not assume all earlier replies in a famous game are forced.', 'A copied sacrifice needs the same supporting pieces and tactical conditions.'),
    ('Use a development lead promptly.', 'Name the file and the piece that will use it.', 'Verify every defence to a forcing finish.'))

teach('counterstrike', (244,246),
    ('Find a pawn chain’s base and the break that challenges it.', 'Understand a temporary retreat or central concession as part of a longer plan.'),
    (
        section('A centre can be strong today and a target tomorrow', '''
            Central pawns gain space, but they also need support. In the illustrative French structure, White has pawns on d4
            and e5, while Black has pawns on d5 and e6. The chain d4–e5 gives White space. Black challenges d4 with ...c5 rather
            than pushing random wing pawns. If d4 disappears, e5 can become harder to maintain. The aim of a central break is
            not always to win a pawn immediately. It may open a file, exchange a cramped pawn, give a knight a square, or force
            the opponent's pieces into defensive jobs. Read the resulting position, including both kings, before deciding whether
            the break has succeeded.
        '''),
        section('Relinquishing space can prepare a better challenge', '''
            The book's Tarrasch–Alekhine example shows Black retreating a queen, exchanging in the centre, and later achieving
            ...d5 with active pieces. A backward queen move looks strange if judged only by the slogan never retreat in the
            opening. It makes sense when you see the future central break and the pieces that support it. This does not make
            every retreat profound. You must identify what the move frees, what threat it avoids, and why the opponent cannot
            exploit the time spent. At beginner level, learn the question rather than the long historical variation: if I release
            this central tension, what concrete central action will I have next? Without an answer, the concession may simply lose space.
        '''),
        section('Prepare the break and calculate the captures', '''
            In our short line ...Nc6 adds pressure to d4, ...Qb6 adds more, and White develops while defending the centre.
            After ...cxd4 cxd4, the structure has changed: Black's c-file is half-open and White's c-pawn now helps occupy d4.
            Half-open means your own pawn has left the file while an enemy pawn remains on it. This illustrative sequence is not
            proof of an advantage for either side. Its purpose is to connect pawn exchanges to piece plans. Before a break,
            calculate the opponent's capture, advance, and decision to maintain tension. After it, recount defenders and choose
            squares for the newly opened lines. The centre is an ongoing struggle, not a trophy acquired permanently on move two.
        '''),
    ),
    (example('Challenge the base, then reassess the structure', START, ('e4','e6','d4','d5','e5','c5','c3','Nc6','Nf3','Qb6','Be2','cxd4','cxd4'), (
        'Illustration of the chapter’s central-counterplay idea.', 'e4 occupies the centre.', '...e6 prepares ...d5.',
        'd4 builds a broad centre.', '...d5 challenges e4.', 'e5 takes space but fixes a pawn chain.',
        '...c5 attacks its base on d4.', 'c3 reinforces d4.', '...Nc6 adds a piece to the central pressure.',
        'Nf3 develops and supports d4.', '...Qb6 attacks d4 and b2.', 'Be2 prepares king safety.',
        '...cxd4 changes the tension.', 'cxd4 restores the d4 pawn. Black has a half-open c-file; both sides need a new assessment.'
    )),),
    (q('base','Which pawn supports e5 in the white d4–e5 chain?','The d4 pawn','White pawns attack one rank forward diagonally.','The pawn on e5 supports itself','Pieces do not defend their own squares.'),
     q('retreat','When can a developing piece’s retreat be justified?','When it prepares a concrete improvement or avoids a real problem','Assess the whole plan and its timing.','Never; all retreats violate opening rules','Principles allow exceptions supported by the position.')),
    ('Do not assume exchanging a central pawn is always surrender.', 'Calculate before opening lines near your own king.'),
    ('Find the chain’s support.', 'Prepare the central break.', 'Reassess the files and squares after exchanges.'))

teach('opening-bait', (249,250),
    ('Calculate beyond the first profitable-looking capture.', 'Recognize a queen check that also attacks a loose piece.'),
    (
        section('The pawn is bait because of what happens next', '''
            The book's example begins e4 e5 Nf3 Nc6 Bb5 Nf6 d3 Ne7. Black's last move appears to abandon the e5 pawn.
            White can legally take it with Nxe5, but must inspect Black's forcing replies. The response ...c6 attacks the bishop
            on b5. If it retreats to a4 in the demonstrated branch, ...Qa5+ checks the king and attacks Ne5 along the fifth rank.
            White cannot save the knight before answering the check. The pawn looked free only because the calculation stopped
            after the first capture. The arrangement of the king, bishop and advanced knight makes the tactic possible. Without
            those features, the same apparent pawn offer could have a different assessment.
        '''),
        section('Calculate a branch, then look for alternatives', '''
            After ...c6, name all important responses: bishop retreats, captures on c6, checks, or a move that changes the
            tactical relationship. Do not assume the defender must choose the prettiest branch. Our replay follows Ba4, c3 and
            ...Qxe5 to make the queen fork visible. It does not claim that every possible White response follows those exact
            squares. Before a capture in your own opening, imagine the piece on its destination and inspect your other pieces
            too. A pawn win can expose a bishop to attack or place a knight on a rank with your king. The opponent may gain a
            decisive tempo by checking rather than by attacking the captured pawn's replacement directly.
        '''),
        section('Use traps to improve your safety checks', '''
            Memorizing a trap can be useful, but building an opening around the hope that the opponent falls into it is fragile.
            Ask whether your setup remains playable if the bait is declined. For the defender, a reliable habit is to distrust
            an apparently free central pawn just long enough to check the forcing moves. It may really be free; the point is
            verification, not fear of every capture. Before pressing the next arrow, say the threat of ...c6 and then the two jobs
            of ...Qa5+. After replaying, reset and explain why the knight cannot simply retreat while the king is checked. That
            explanation is transferable to many openings, whereas memorizing only the move Nxe5 is not.
        '''),
    ),
    (example('The chapter’s apparently free e5 pawn', START, BAIT, (
        'Book trap, annotated from the start so the exposed pieces have a clear origin.', 'e4 takes central space.',
        '...e5 answers in the centre.', 'Nf3 attacks e5.', '...Nc6 defends it.', 'Bb5 pressures the defender.',
        '...Nf6 develops and counterattacks e4.', 'd3 supports e4.', '...Ne7 withdraws Nc6 and appears to abandon e5.',
        'Nxe5 takes the bait without resolving the tactical risk.', '...c6 attacks the bishop and prepares a queen route.',
        'Ba4 is the illustrative bishop retreat used in this branch.', '...Qa5+ checks along a5–e1 and attacks Ne5 on the fifth rank.',
        'c3 blocks the check, but does not defend the knight.', '...Qxe5 captures the knight. White gained a pawn but lost a piece.'
    )),),
    (q('double','What are the two jobs of ...Qa5+?','Check the king and attack Ne5','The check prevents White from simply saving the knight.','Attack both rooks','The rooks are not the targets of this combination.'),
     q('bait','What should you do before taking a suspicious free pawn?','Check forcing replies against all exposed pieces','A tactic may target a different piece after the capture.','Assume any undefended pawn is safe to take','Being undefended at the moment is not proof that the capture is good.')),
    ('Do not stop the calculation at your capture.', 'A demonstrated trap branch is not the only legal continuation.'),
    ('Inspect checks after captures.', 'Track every loose piece.', 'Learn the mechanism, not only the move order.'))

teach('premature-attack', (248,252),
    ('Distinguish an attack supported by pieces from premature pawn activity.', 'Use a newly opened king diagonal with a concrete checking sequence.'),
    (
        section('An aggressive appearance can hide an idle army', '''
            In the book's Bronstein–Mikenas game, Black advances the f-pawn and later the h-pawn while pieces remain undeveloped.
            White develops, secures the king, and opens lines; the activity of the whole army eventually matters more than the
            early pawn threats. A pawn storm can be justified when supported by pieces and a safe centre, but a pawn on the fourth
            or fifth rank is not by itself an attack. Count the pieces that can join a forcing sequence immediately. Then count
            the opponent's defensive pieces and counterchecks. If your queen is the only active attacker, another pawn advance
            may merely give the opponent time to develop and open the centre against your king.
        '''),
        section('Calculate the weakness rather than announce a punishment', '''
            After e4 e5 Nf3 f5 Nxe5, immediate ...fxe4 allows Qh5+. The f-pawn has left f7, opening a diagonal to the king.
            After ...g6, Nxg6 takes the pawn and attacks Rh8. Black can use ...Nf6 to attack the queen and cover h5, but
            Nxh8 then captures the rook. The knight may later have trouble escaping; count the material and calculate the next
            threats rather than ending the game in your imagination. Black also has alternatives to ...fxe4 on the previous
            move, notably ...Nf6 as in the book's game. Those alternatives require separate analysis. Our replay teaches the
            concrete flaw in immediate acceptance, not a complete refutation of every line of the opening.
        '''),
        section('When you are ahead in development, open useful lines', '''
            In the longer game White's f-pawn advance helps open a file for a developed rook and queen. That is a different
            use of a pawn from a speculative attack while the back rank sleeps. Ask which line the pawn exchange opens and
            which piece will use it first. Do not assume the player who advanced the pawn must benefit: captures can open
            lines for the opponent. Before starting an attack in your own games, check your king, the central tension, your
            least active piece, and the opponent's forcing replies. If one developing move adds a rook or bishop to the attack,
            it may be stronger than another immediate threat by the queen. A coordinated attack often grows from ordinary moves.
        '''),
    ),
    (example('A premature capture exposes the king’s diagonal', after(('e4','e5','Nf3','f5','Nxe5')), ('fxe4','Qh5+','g6','Nxg6','Nf6','Nxh8+'), (
        'White has taken e5. Black must consider the king’s newly weakened diagonal before recapturing.',
        '...fxe4 opens f7 completely and ignores the checking resource.', 'Qh5+ forces Black to address the king.',
        '...g6 blocks the diagonal but places a pawn under the knight’s attack.', 'Nxg6 captures and attacks Rh8.',
        '...Nf6 develops with an attack on the queen, but White has a checking capture.',
        'Nxh8+ captures the rook and uncovers Qh5’s check. White must still consider how to rescue or use the knight later.'
    )),),
    (q('army','What should you count before a pawn storm?','Pieces able to join and the safety of the centre and king','The pawn advance needs support and must survive counterplay.','Only how close the pawn is to the enemy king','Distance alone says little about the attack’s soundness.'),
     q('branch','Does the shown ...fxe4 line cover every Black defence?','No; alternatives such as ...Nf6 must be analyzed separately','A refuted branch is not the whole opening tree.','Yes; Black is forced to capture e4 immediately','There is no obligation to make that capture.')),
    ('Do not confuse an advanced pawn with a developed army.', 'Count the next threats even after winning a rook.'),
    ('Support an attack with pieces.', 'Calculate the king’s open diagonals.', 'Distinguish an actual refutation from one bad branch.'))

teach('miniature', (250,251),
    ('Read a short game as a chain of changing opportunities.', 'Explain how ordinary development can sustain a tactical initiative.'),
    (
        section('How to study a complete game actively', '''
            Play the opening once to identify the structure, then replay it more slowly. Before each critical move, predict the
            player's purpose and one plausible reply. A critical move changes the centre, exposes a king, sacrifices material,
            or commits a piece to a new job. In Alekhine–Sanchez, ...Nxd4 is the first important error highlighted by the book;
            ...exd5 would have maintained a healthier structure. White's Nxd4 and dxe6 then make lines and checks available.
            Do not try to remember the game as forty-nine isolated half-moves. Group the decisions: change the centre, displace
            the king, finish development, penetrate with rooks, and coordinate the final queen threat.
        '''),
        section('A temporary material picture can mislead', '''
            After dxe6, Black captures the bishop on b5. White responds Qh5, and then Qxb5+ recovers that bishop while forcing
            the king to move. The sequence demonstrates an intermediate threat and delayed recapture. You must track material
            to the end of the forcing line, not stop after one side's capture. White then castles and develops the knight,
            making the contrast between the safe king and Black's exposed king more significant. A queen exchange might ease
            Black's defence, so White keeps the queen active instead. This is a positional decision supported by concrete king
            safety. Exchanging queens is neither always cowardly nor always safe; assess whose difficulties the exchange would solve.
        '''),
        section('The last pieces make the attack stronger', '''
            Nxd4 centralizes the knight and clears the d-file. Rd1 and Be3 are simple developing moves with a shared purpose:
            they bring more force toward Black's king. Later the rook reaches d7 while the other rook works on the c-file.
            The final Qd3 organizes a threat of Rc7+ followed by a queen entry. The historical game ended in resignation there;
            the replay stops at the actual end and does not pretend the king is already checkmated. For your own study, point
            to the pieces that would cooperate in the next attack, then examine Black's possible checks and blocks. That last
            verification is what turns a beautiful game into a calculation exercise rather than a story about inevitable victory.
        '''),
    ),
    (example('Alekhine–Sanchez: the centre opens and the king moves', START, SANCHEZ[:24], (
        'Book game, Bogota 1939; annotations explain the purposes rather than reproduce the source prose.',
        'e4 opens lines.', '...e6 prepares ...d5.', 'd4 occupies the centre.', '...d5 challenges it.',
        'Nd2 supports e4 while retaining the c-pawn’s freedom.', '...c5 attacks d4.', 'Ngf3 develops the other knight.',
        '...Nc6 adds central pressure.', 'Bb5 develops with pressure on Nc6.', '...Bd7 removes the pin against the king.',
        'exd5 changes the central tension.', '...Nxd4 is the book’s criticized capture; ...exd5 was preferable.',
        'Nxd4 exchanges the advanced knight.', '...cxd4 creates a central pawn on d4.',
        'dxe6 attacks the bishop on d7 and opens lines before recapturing elsewhere.', '...Bxb5 takes the bishop.',
        'Qh5 creates pressure against f7 and prepares recovery on b5.', '...Qe7 guards f7.',
        'Qxb5+ recovers the bishop with check.', '...Kd8 removes the king from check but forfeits castling.',
        'White castles, completing king safety while Black’s king is central.', '...fxe6 captures the advanced pawn but opens more lines.',
        'Nf3 redevelops the remaining knight toward the centre.', '...Qd7 seeks to simplify the defensive task.'
    )), example('Alekhine–Sanchez: mobilize, then penetrate', after(SANCHEZ[:24]), SANCHEZ[24:], (
        'Continue from the first replay. Black’s king on d8 is the main long-term target.',
        'Qb3 keeps the queen active.', '...Qd5 proposes a queen exchange.', 'c4 gains time by attacking the queen.',
        '...Qd7 retreats.', 'Nxd4 wins back the central pawn and centralizes.', '...Kc8 moves away from the d-file.',
        'Rd1 occupies that file.', '...Bc5 develops a bishop with pressure on d4.', 'Be3 adds support and develops the last minor piece.',
        '...Bxd4 exchanges the knight.', 'Rxd4 recaptures with an active rook.', '...Qe7 changes the queen’s defensive position.',
        'c5 gains space and prepares a further intrusion.', '...Nf6 develops the remaining knight.',
        'c6 cramps Black and threatens to open lines.', '...b6 keeps the c-file closed for the moment.',
        'Bg5 pins Nf6 to Qe7.', '...Re8 brings a rook to a defensive file.', 'Rc1 places the second rook behind the advanced pawn.',
        '...a5 seeks queenside counterplay.', 'Bxf6 removes the knight.', '...gxf6 changes Black’s pawn shield.',
        'Rd7 penetrates the seventh rank.', '...Qb4 seeks counterplay and defensive access.',
        'Qd3 coordinates the threat of Rc7+ and a queen entry. Black resigned here; the board is not already checkmate.'
    ))),
    (q('recapture','Why not judge the position immediately after ...Bxb5?','White has an intermediate queen threat and then Qxb5+','Complete the forcing sequence before counting its result.','Captured material never matters in an attack','Material matters, but only after the relevant sequence is understood.'),
     q('finish','Does a resignation mean the last move was checkmate?','No; the player may resign before the forced outcome occurs','Checkmate must be verified from the actual board.','Yes; every resigned game ends in a mating position','Many resignations occur with numerous legal moves remaining.')),
    ('Separate a historical move from a forced reply.', 'Do not stop evaluating in the middle of a tactical exchange.'),
    ('Group moves by purpose.', 'Track delayed recaptures.', 'Bring the last pieces into a shared attack.'))

teach('dynamic-pieces', (252,254),
    ('Evaluate compensation for an unusual bishop exchange.', 'Connect the chapter’s different games through centre, development and king safety.'),
    (
        section('A principle can be outweighed by a concrete position', '''
            Furman–Spassky begins with a broad white centre and a black bishop on g7. Black plans ...f5 and develops a knight
            to h6, a square that would look suspicious if judged only by the rule knights belong near the centre. Here it
            supports a specific route to f5. After exf5, ...Bxd4 exchanges the king's bishop for a central knight before
            ...Nxf5 restores material. Black has given up the bishop pair and a piece that helped protect the king, but gains
            active knight squares and central play. The lesson is to compare compensation, not to declare that bishops or
            knights are always superior. Check what the exchanged bishop was doing and what the new pieces can now do.
        '''),
        section('Active knights need squares and supporting pawns', '''
            In the fragment, one knight reaches f5 and later d4, while the other occupies c6. The d6 pawn and subsequent
            central moves help support the activity. White's bishop is chased from d4 to c5 and a3 while Black improves.
            Notice that Black has already castled: central counterplay is less risky when the king is not exposed on e8.
            This does not make every ...Bxd4 sacrifice or exchange correct. Our replay follows the actual opening fragment,
            and later improvements in the full game require further calculation. Pause after the exchange and compare the
            sides: White has the bishops; Black has active knights. Material labels alone cannot settle the assessment.
        '''),
        section('Compare the other games without copying their pawn moves', '''
            The Petrosian–Tolush example uses a pin and weakened king cover, then castling long brings the rooks into open
            files. Geller–Vatnikov shows central pawn advances gaining force through tactical threats and active pieces.
            Alekhine–Poindle turns a developmental mistake into an attack on an exposed king. Bronstein–Mikenas punishes pawn
            activity that lacks supporting development. These are different positions, so copying g4, f5 or a sacrifice into
            your next game would miss the lesson. In each case ask: who is developed, which king is vulnerable, which central
            break changes the lines, and which forcing move makes the plan work? Use those four questions after your own
            opening. They combine the chapter's examples into a practical method for unfamiliar positions.
        '''),
    ),
    (example('Furman–Spassky: knights receive active jobs', START, FURMAN, (
        'Book game, Moscow 1957. Follow Black’s central plan without assuming every move is forced.',
        'Nf3 develops flexibly.', '...c5 contests d4.', 'c4 adds control over d5.', '...g6 prepares a bishop on the long diagonal.',
        'e4 creates a central presence.', '...Bg7 develops the bishop.', 'd4 challenges the c5 pawn.', '...cxd4 exchanges central pawns.',
        'Nxd4 occupies the centre.', '...Nc6 develops with pressure on d4.', 'Be3 develops and supports the knight.',
        '...Nh6 prepares a specific route toward f5; this is not a random edge move.', 'Nc3 adds support to e4 and d5.',
        'Black castles before opening central lines.', 'Be2 prepares White’s castle.', '...f5 challenges e4.',
        'exf5 takes the pawn.', '...Bxd4 exchanges the g7 bishop for the central knight before recapturing f5.',
        'Bxd4 recaptures.', '...Nxf5 regains the pawn with active knight play.', 'Bc5 retreats the attacked bishop.',
        '...d6 attacks that bishop and supports central control.', 'Ba3 preserves the bishop on another diagonal.',
        '...Nfd4 places the knight centrally.', 'White castles.', '...Bf5 develops the remaining bishop. Evaluate bishop pair versus knight activity and central pressure.'
    )),),
    (q('compensation','What must justify giving up the g7 bishop?','Concrete activity and central play that compensate for its lost jobs','The exchange has costs as well as benefits.','A rule that knights always beat bishops','There is no universal superiority independent of the position.'),
     q('transfer','What should you copy from a master game into an unfamiliar opening?','The questions about development, king safety and central breaks','The answers depend on the actual position.','The attacking pawn moves regardless of the board','Moves that work in one structure can fail in another.')),
    ('Do not call an exception a new universal rule.', 'Always identify what the traded piece was defending.'),
    ('Compare activity with structural costs.', 'Give each piece a concrete job.', 'Transfer the thinking questions, not a memorized attack.'))

teach('quiet-route', (254,255),
    ('Find the purpose of a quiet move by looking at the final position.', 'Distinguish a composition’s special constraints from normal opening play.'),
    (
        section('Inventory the unusual position before calculating', '''
            This is the book's Kohtz–Kockelkorn composition, not a position offered as an opening model. White has Kh4,
            Qh3, Bc6, knights e6 and d1, and a g2 pawn. Black has Ke4, rooks d5 and c2, Bb1, Nh2 and an e5 pawn.
            The material is crowded because pieces have specific blocking and guarding jobs. First locate the king flights,
            the queen's route up the h-file, and the black bishop's diagonal toward c6. White's own king blocks the queen's
            route. Moving it out of the way is necessary, but the route must remain safe and preserve the mating arrangement.
            A quiet move is a move without check or capture; its threat can still be decisive.
        '''),
        section('Work backward from Qh7 mate', '''
            Imagine the queen reaching h7. From there it checks Ke4 along h7–g6–f5–e4. In the demonstrated finish the king
            has walked to h8, leaving h4, h5 and h6 free for the queen's travel. The black bishop has meanwhile travelled
            from b1 through a2, b3 and a4 to capture Bc6. Those moves do not break the mating net. At each arrow, check which
            lines remain blocked and which king squares White's pieces cover. Do not assume that every black move is forced
            merely because the replay follows one line from the book. A full mate-in-five solution must cover alternative
            defences too; here the annotated main line teaches the concealed purpose of the king journey.
        '''),
        section('A route is judged by its job, not by its appearance', '''
            The entertainment pages contain other surprising detours and quiet keys. A rook can need a roundabout route
            because the direct one allows a check; a bishop can leave a square to clear a line; a piece can be offered so
            the capturing defender blocks another defender. These ideas are useful in real calculation, but only when the
            board's constraints justify them. In an ordinary opening, marching the king up the board would usually expose
            it and waste time. In this artificial position, the king's journey is the mechanism. After replaying, explain
            exactly why h8 is useful and why a check at every turn was unnecessary. That explanation is more valuable than
            memorizing the four king moves.
        '''),
    ),
    (example('Kohtz–Kockelkorn: the main line of the quiet journey', QUIET, QUIET_LINE, (
        'Source diagram on printed p.254. White’s king obstructs Qh3’s route; examine the final diagonal from h7 to e4.',
        'Kh5 begins clearing the h-file while preserving the net.', '...Ba2 is the source’s displayed continuation.',
        'Kh6 continues the route; the queen still waits.', '...Bb3 keeps the bishop moving toward the c6 capture route.',
        'Kh7 brings the king one step from its destination.', '...Ba4 stays on the diagonal toward c6.',
        'Kh8 finally clears the queen’s path to h7.', '...Bxc6 captures the bishop but does not destroy the mating net.',
        'Qh7 is checkmate along the diagonal to e4. Inspect every neighboring king square to confirm the finish.'
    )),),
    (q('quiet','Why can a non-checking king move be purposeful here?','It clears the queen’s eventual route while preserving the net','The threat depends on rearrangement rather than immediate checks.','Kings may ignore enemy attacks in compositions','All moves still obey normal chess legality.'),
     q('transfer','Should you copy this king march in your next opening?','Only if the actual position gives a concrete reason; normally it would be unsafe','A composition isolates an idea under unusual constraints.','Yes, because a famous problem used it','A move sequence is not a universal opening plan.')),
    ('The main variation is not an exhaustive proof against every defence.', 'A surprising move still needs a precise purpose and legal route.'),
    ('Inventory pieces and blocked lines.', 'Work backward from the desired finish.', 'Verify forward without confusing a study with an opening recipe.'))

teach('composition-lessons', (255,258),
    ('Understand quiet keys, interference, alternative solutions and drawing aims.', 'Verify a checking cycle against every legal king reply.'),
    (
        section('Several kinds of surprise share one discipline', '''
            The chapter's problems include detours, offers of powerful pieces, economical versions of the same idea, and
            an unexpected second solution. A key is the first move that makes the solution work. Interference happens when
            one piece blocks another piece's line; an offered piece can lure a defender onto just such a square. Economy
            means using only the pieces needed to show the idea clearly. The book compares a crowded setting with a trimmed
            one to make that point. When reading a problem, ask what each piece contributes before assuming it is decoration.
            In a real game some pieces may be irrelevant locally, but a forgotten remote bishop can still refute your attack.
        '''),
        section('The stated objective decides what counts as success', '''
            Mate in a specified number of moves, win material, and draw are different tasks. In the book's Circus example,
            repeated knight checks save a position despite a material disadvantage; the king always has a reply, so this is
            not mate. Our simpler queen illustration revisits the same defensive principle with a cycle you can verify fully.
            White has Kc4 and Qf7; Black has Kh8, Qh5 and pawns g6 and h6. White checks on f8, forcing Kh7, then checks on
            f7, forcing Kh8. The black pawns and queen placement restrict the king's options. Check captures and blocks as well
            as king moves before declaring the cycle unavoidable.
        '''),
        section('Accept valid alternatives and demand a complete proof', '''
            A composed problem is often designed to have one key, but the book describes a problem where another solution
            was discovered. This is a reminder that an attractive intended answer is not the same as a proof of uniqueness.
            The app's mate tasks accept any move that really checkmates; narrowly specified movement tasks ask for a particular
            demonstrated operation. In your own calculation, actively seek another defence or another solution. For repetition,
            the full position must recur with the same player to move and relevant rights. After two complete cycles the
            initial position has occurred three times, enabling a draw claim. Merely announcing perpetual check does not make
            a draw, and a checking move that lets the king capture your queen does not preserve the resource.
        '''),
    ),
    (example('Original simplified illustration: a verified saving cycle', REPETITION,
        ('Qf8+','Kh7','Qf7+','Kh8','Qf8+','Kh7','Qf7+','Kh8'), (
        'White is two pawns behind. Black’s own pawns restrict its king; this is the first occurrence of the starting position.',
        'Qf8+ checks on the eighth rank and controls g7.', 'Kh7 is Black’s only legal reply.',
        'Qf7+ checks on the seventh rank and controls g8.', 'Kh8 is the only legal reply; the initial position has occurred twice.',
        'White repeats Qf8+ rather than offering an unprotected queen beside the king.', 'Kh7 is forced again.',
        'Qf7+ repeats the complementary checking line.', 'Kh8 restores the initial position for the third time, allowing a repetition claim.'
    )),),
    (q('draw','Why is the demonstrated cycle a drawing resource rather than mate?','The king always has a legal reply, but cannot escape the checks','The repeated full position can support a draw claim.','Any three checks automatically count as mate','Mate requires no legal defence to the current check.'),
     q('alternatives','What should you do if a different move appears to solve a problem?','Verify it against all defences','The intended answer does not exclude a second valid solution.','Reject it because it differs from the printed move','A correct alternative remains correct under the stated objective.')),
    ('Three checks are not the same as threefold repetition.', 'An offered queen must not be capturable without compensation.'),
    ('Read the objective exactly.', 'Explain every piece’s role.', 'Test alternatives and every defensive reply.'))

teach('pawn-journey', (259,260),
    ('Track a pawn through captures and promotion.', 'Explain how threats by other pieces support an unexpected mating journey.'),
    (
        section('Do not rule out the unlikely piece too soon', '''
            In Loyd's Excelsior problem the b2 pawn appears far from the black king on h1. Yet it is the piece that eventually
            delivers mate after promoting on a8. White also has Kh5, rooks b5 and e2, knights a1 and h3, and pawns c2 and g3.
            Black's other pieces and pawns create the lines and restrictions used by the solution. The lesson is not that
            every remote pawn can force mate in five moves. It is that a piece's present appearance can hide its future role.
            When calculating a promotion, place the new queen on the destination square mentally and trace its lines before
            dismissing the idea as too slow or too far away.
        '''),
        section('Every pawn step is supported by another threat', '''
            b4 clears b2 and threatens a rook operation; ...Rc5+ then puts a rook where the b-pawn can capture it. After
            bxc5, the pawn has changed files and the b-file is open. ...a2 gives Black the reply ...axb1=Q if White tries Rb1+,
            so White continues c6, renewing a rook threat. ...Bc7 meets that threat, but cxb7 lets the pawn capture its way
            closer to a8. The source leaves Black's final waiting move unspecified in the main line. Our replay chooses
            the legal ...Bf4 so you can see a complete alternating sequence. It is an illustrative branch, not a claim
            that Black must choose that bishop square. The pawn's journey works together with the other pieces' threats.
        '''),
        section('At promotion, check the exact geometry', '''
            bxa8=Q captures the knight and creates a queen on the a8–h1 diagonal. The intervening squares b7, c6, d5,
            e4, f3 and g2 are clear after the pawn's journey. The queen therefore checks Kh1, and the other pieces close
            the escape squares. A rook promotion cannot use that diagonal; a quiet promotion on b8 is a different geometry.
            The exercise asks for checkmate, and the grader checks the resulting board rather than merely comparing a
            string of notation. In your games, calculate promotion with checks, captures and flight squares included.
            Finishing a pawn race is not the end of analysis: the new piece can be captured, skewered, or required to
            stop a countercheck. Explain the final board before calling the race won.
        '''),
    ),
    (example('Loyd’s Excelsior: the b-pawn’s complete journey', EXCELSIOR, EXCELSIOR_LINE, (
        'Source diagram on printed p.259. Track b2’s route and the rook threats that support it.',
        'b4 advances two squares and clears b2 for future rook access.', '...Rc5+ checks along the fifth rank.',
        'bxc5 answers the check by capturing the rook and shifts the pawn to the c-file.',
        '...a2 controls b1, so a rook check there could be answered by ...axb1=Q.', 'c6 advances again while the rooks retain mating threats.',
        '...Bc7 is the source’s blocking defence.', 'cxb7 captures a pawn and reaches the seventh rank.',
        '...Bf4 is a legal illustrative continuation where the source leaves the waiting move open.',
        'bxa8=Q is mate on the long diagonal to h1. The once-distant b2 pawn has become the checking queen.'
    )),),
    (q('promotion-line','Why does a queen on a8 check Kh1?','They lie on the same clear diagonal','Trace a8–b7–c6–d5–e4–f3–g2–h1.','Queens can jump over any intervening piece','Queens require a clear line like bishops and rooks.'),
     q('support','Why is the pawn journey more than a slow pawn race?','Other pieces create threats that shape Black’s replies','The pawn advances as part of a coordinated forcing idea.','Black voluntarily skips every turn','Every black move in the replay is a legal turn with its own purpose.')),
    ('Do not assume the promotion square alone determines the result.', 'The displayed final waiting move is an example, not a forced reply.'),
    ('Track the pawn’s changing file.', 'Name the supporting threats.', 'Verify the new piece’s line and every king escape.'))
