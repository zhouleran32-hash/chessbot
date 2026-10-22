"""Chapter 7: opening decisions and the chapter's composed-study themes."""
import chess
from core.primer_build import after, custom, lesson, step

START = chess.STARTING_FEN
OPEN = ('e4', 'e5')
ITALIAN = OPEN + ('Nf3', 'Nc6', 'Bc4', 'Bc5')
MORPHY = ('e4','e5','Nf3','d6','d4','Bg4','dxe5','Bxf3','Qxf3','dxe5','Bc4','Nf6','Qb3','Qe7','Nc3','c6','Bg5','b5','Nxb5','cxb5','Bxb5+','Nbd7','O-O-O','Rd8','Rxd7','Rxd7','Rd1','Qe6','Bxd7+','Nxd7','Qb8+','Nxb8','Rd8#')
BAIT = ('e4','e5','Nf3','Nc6','Bb5','Nf6','d3','Ne7','Nxe5','c6','Ba4','Qa5+','c3','Qxe5')
SANCHEZ = ('e4','e6','d4','d5','Nd2','c5','Ngf3','Nc6','Bb5','Bd7','exd5','Nxd4','Nxd4','cxd4','dxe6','Bxb5','Qh5','Qe7','Qxb5+','Kd8','O-O','fxe6','Nf3','Qd7','Qb3','Qd5','c4','Qd7','Nxd4','Kc8','Rd1','Bc5','Be3','Bxd4','Rxd4','Qe7','c5','Nf6','c6','b6','Bg5','Re8','Rc1','a5','Bxf6','gxf6','Rd7','Qb4','Qd3')
FURMAN = ('Nf3','c5','c4','g6','e4','Bg7','d4','cxd4','Nxd4','Nc6','Be3','Nh6','Nc3','O-O','Be2','f5','exf5','Bxd4','Bxd4','Nxf5','Bc5','d6','Ba3','Nfd4','O-O','Bf5')
QUIET = custom({'h4':'K','h3':'Q','c6':'B','e6':'N','d1':'N','g2':'P','e4':'k','d5':'r','c2':'r','b1':'b','h2':'n','e5':'p'})
QUIET_LINE = ('Kh5','Ba2','Kh6','Bb3','Kh7','Ba4','Kh8','Bxc6','Qh7#')
EXCELSIOR = custom({'h5':'K','b5':'R','e2':'R','a1':'N','h3':'N','b2':'P','c2':'P','g3':'P','h1':'k','a8':'n','c8':'r','d8':'b','b7':'p','b6':'p','f7':'p','h7':'p','a3':'p','e3':'p'})
EXCELSIOR_LINE = ('b4','Rc5+','bxc5','a2','c6','Bc7','cxb7','Bf4','bxa8=Q#')
REPETITION = custom({'c4':'K','f7':'Q','h8':'k','h5':'q','g6':'p','h6':'p'})


def opening_lesson(key, title, explanation, prefix, prompt, choices, *, start=START, objective=None):
    quiz = after(prefix, start) if prefix else start
    return lesson(7, 'ch7-' + key, title, explanation, [
        step(start, 'Identify the side to move, both kings, and the pieces needed for this lesson.'),
        step(quiz, 'This is your decision position. Read the specific task before choosing a legal move.'),
    ], prompt, choices, objective=objective)


LESSONS = [
    opening_lesson('tasks', 'The opening is a job for the whole army',
        'Development means bringing a piece to a useful working square. In the opening, combine central influence, efficient development and king safety. A move should do an identifiable job; merely moving a piece does not guarantee that it is well placed. Begin with a central pawn, develop supporting pieces, and keep checking the opponent’s threats.',
        OPEN, 'Develop the g1 knight to the central square where it also attacks e5.',
        [('Nf3',True,'Nf3 develops, controls d4 and e5, and attacks the e5 pawn.'),('Nh3',False,'This develops to the edge and does not attack e5. The task is Nf3.'),('a4',False,'This moves a flank pawn rather than mobilizing the knight.')]),
    opening_lesson('centre', 'Occupy the centre or control it from a distance',
        'The four central squares are d4, e4, d5 and e5. Occupation means placing something there; control means attacking the squares. You need useful influence, not four pawns marching forward without protection. The extended centre includes c3 through f6, where pieces can support or challenge the central battle.',
        (), 'Advance the d-pawn two squares to occupy d4 and attack e5.',
        [('d4',True,'The pawn occupies d4 and attacks c5 and e5, while opening the c1 bishop.'),('e4',False,'e4 is a good opening move, but this exercise specifically asks for d4 and control of e5.'),('h4',False,'h4 does not contest the central squares named in the task.')]),
    opening_lesson('tempo', 'Spend a move on a new useful piece',
        'A tempo is a unit of time measured in moves. Compare the pieces doing useful work, rather than simply counting how many moves have been played. Moving a threatened piece again may be necessary; moving the same piece aimlessly while the rest wait costs development. Choose a new working piece when there is no urgent reason to repeat one.',
        ITALIAN, 'Develop the b1 knight to c3, adding central support without moving an active piece again.',
        [('Nc3',True,'The second knight joins the game and protects e4 and d5.'),('Ng1',False,'The active knight retreats to its starting square without necessity.'),('Bb3',False,'The bishop is safe on c4; this task asks you to develop the unused queen knight.')]),
    opening_lesson('bishop', 'Choose bishop squares after seeing the position',
        'A knight often has a natural early central square, while a bishop may choose among several diagonals. After 1.e4 e5 2.Nf3 Nc6, Bc4 eyes f7 and Bb5 pressures the defender of e5. Neither move wins anything by itself. Choose a square that fits the pawn structure and plan, and understand its job.',
        OPEN+('Nf3','Nc6'), 'Develop the f1 bishop to either c4 or b5, the two active plans compared in this lesson.',
        [('Bc4',True,'Bc4 develops toward f7 and clears the way to castle.'),('Bb5',True,'Bb5 develops with pressure on Nc6, which guards e5.'),('Bd3',False,'Bd3 obstructs the d2 pawn and is not one of the two plans requested here.')]),
    opening_lesson('castle', 'Make the king safe, then connect the rooks',
        'Castling usually moves the king out of the centre and brings a rook closer to the action. First clear the path, verify the castling rules, and check the resulting king position. Afterwards, finish the other minor pieces and move the queen to a useful safe square so that the rooks can cooperate.',
        ITALIAN, 'Castle kingside now that the f1 bishop and g1 knight have developed.',
        [('O-O',True,'The legal castle puts Kg1 and Rf1 in place together.'),('Ke2',False,'Ke2 leaves the king in the centre and permanently gives up castling.'),('h4',False,'A flank pawn move does not complete the king-safety job.')]),
    opening_lesson('pawns', 'Use pawn moves to make pieces work',
        'Pawn moves are useful when they claim or challenge central squares, open a route for a piece, or answer a concrete threat. Too many pawn moves can leave the army asleep. The book’s beginner advice to favour the d- and e-pawns is a training guideline, not a ban on other opening pawn moves.',
        ITALIAN+('O-O','Nf6'), 'Advance the d-pawn one square to support e4 and open the c1 bishop.',
        [('d3',True,'d3 protects e4 and clears d2 for the bishop’s diagonal.'),('d4',False,'d4 is another playable plan, but it opens a sharper central confrontation rather than the one-square support task.'),('a4',False,'a4 does not support e4 or release the c1 bishop.')]),
    opening_lesson('queen', 'Meet an early queen attack without panic',
        'An early queen is powerful but can be chased by smaller developing pieces. You still have to answer its threats. Against Qh5 and Bc4, f7 is attacked twice: a careless developing move can allow mate. Defend first, then use the exposed queen as a target while your other pieces improve.',
        ('e4','e5','Qh5','Nc6','Bc4'), 'Block the queen’s diagonal to f7 and attack the queen with the g-pawn.',
        [('g6',True,'g6 interrupts h5–f7 and attacks Qh5. White must change the plan.'),('Nf6',False,'This attacks Qh5 but allows Qxf7#: always answer the immediate mating threat.'),('a6',False,'a6 leaves the queen-and-bishop attack on f7 intact.')]),
    opening_lesson('defend-e5', 'Compare three sensible answers to Nf3',
        'After 1.e4 e5 2.Nf3, Black should notice the attack on e5. Nc6 develops and defends; d6 defends with a pawn but reduces the f8 bishop’s scope; Nf6 counterattacks e4 and requires concrete knowledge of the exchanges. A sound opening can have several good moves. Judge each by its consequences.',
        OPEN+('Nf3',), 'Develop the b8 knight while directly protecting e5.',
        [('Nc6',True,'Nc6 develops and protects e5 in one move.'),('d6',False,'d6 is a legitimate defence, but it does not develop the b8 knight requested here.'),('Nf6',False,'Nf6 is a sound counterattacking system, but it attacks e4 rather than directly defending e5.')]),
    opening_lesson('f6', 'Why an early ...f6 can expose the king',
        'Defending e5 with ...f6 blocks the g8 knight’s natural square and weakens diagonals around the king. White can continue developing or investigate Nxe5. The sacrifice is instructive only if you calculate Black’s alternatives: accepting it with ...fxe5 is dangerous, but ...Qe7 is a different branch that must be checked.',
        OPEN+('Nf3','f6'), 'Play the knight sacrifice on e5 whose acceptance opens the h5–e8 checking diagonal.',
        [('Nxe5',True,'After ...fxe5, Qh5+ exploits the vacated f7 square. Also calculate ...Qe7 instead of acceptance.'),('Bc4',False,'Bc4 is sensible development, but this task specifically asks for the knight sacrifice.'),('Nh4',False,'This moves the knight to the edge without exposing the e8 king.')]),
    opening_lesson('exchange-tempo', 'An exchange can quietly lose development time',
        'A bishop that spends two moves exchanging a knight that moved once can help the opponent develop on the recapture. The material balance may be equal while the useful pieces left on the board are not. In the Morphy example, Qxf3 is a purposeful queen move because it recaptures and prepares pressure with Bc4.',
        MORPHY[:8], 'Recapture the bishop on f3 with the queen, keeping the kingside pawns intact.',
        [('Qxf3',True,'The queen recaptures without changing the pawn shield and can cooperate with Bc4.'),('gxf3',False,'This also recaptures legally, but changes the pawn structure; the task asks for the queen recapture.'),('Nc3',False,'Black’s bishop on f3 has captured a knight. Finish the specified recapture first.')]),
    opening_lesson('open-lines', 'Turn a development lead into open lines',
        'A development lead is temporary. Open a line only after identifying which active pieces will use it and how the opponent can defend. Morphy’s famous short game brings the last rook into the attack, sacrifices to remove defenders, and ends with a mating rook. The lesson is coordination and calculation, not automatic sacrifice.',
        MORPHY[:22], 'Castle queenside to bring the a1 rook onto the open d-file in the demonstrated game.',
        [('O-O-O',True,'The king reaches c1 and the rook reaches d1, joining the central attack.'),('O-O',False,'Kinging safely on the other wing is legal, but does not bring Ra1 to d1 as requested.'),('a3',False,'The attack needs the a1 rook; a3 does not activate it.')]),
    opening_lesson('counterstrike', 'A pawn centre can be challenged',
        'Owning more central space does not end the struggle. Attack the base of a pawn chain, arrange your pieces for the resulting files, and calculate the timing. Relinquishing a central pawn square can be sensible if it prepares a later central break. Never confuse a broad pawn centre with an invulnerable one.',
        ('e4','e6','d4','d5','e5'), 'Challenge White’s d4 pawn with the c-pawn, attacking the base of the chain.',
        [('c5',True,'The c-pawn attacks d4, the support under White’s e5 pawn.'),('h5',False,'This does not challenge the base of White’s central chain.'),('a6',False,'a6 can have uses in other positions, but it is not the central break requested.')]),
    opening_lesson('opening-bait', 'Ask what happens after the apparently free pawn',
        'Before taking opening bait, calculate forcing replies against every exposed piece, including checks that attack another target. In the book’s trap, Nxe5 is followed by ...c6, driving the bishop, and ...Qa5+, attacking the knight with check. The first capture looks profitable only if you stop calculating too early.',
        BAIT[:11], 'Give the queen check on a5 that simultaneously attacks the knight on e5.',
        [('Qa5+',True,'The checking diagonal gains time while the queen attacks Ne5 along rank five.'),('Qc7',False,'Qc7 does not create the same check-and-knight attack.'),('d5',False,'This contests the centre but does not execute the specific queen fork.')]),
    opening_lesson('premature-attack', 'Do not let a pawn raid replace development',
        'An aggressive pawn move is not an attack by an army. In the early ...f5 example, Black must account for the opening of the king’s diagonal and White’s forcing checks. Diagnose the weakness and calculate; do not play a memorized punishment if the opponent chooses a different defence.',
        ('e4','e5','Nf3','f5','Nxe5','fxe4'), 'Give the queen check made possible by the early f-pawn advance.',
        [('Qh5+',True,'The diagonal h5–e8 is now open because the f-pawn has left f7.'),('Bc4',False,'Bc4 develops, but the task is the immediate queen check.'),('Ng4',False,'This spends another knight move without exploiting the king’s diagonal.')]),
    opening_lesson('miniature', 'Study a whole opening as connected decisions',
        'A miniature is a short game, often decided by a development error and a tactical sequence. In Alekhine–Sanchez, a knight capture changes the centre, White uses checks to displace the king, and ordinary developing moves make the attack stronger. Follow the changes in the position instead of memorizing move numbers.',
        SANCHEZ[:28], 'Capture the d4 pawn with the f3 knight, centralizing it and uncovering the d-file.',
        [('Nxd4',True,'Nxd4 restores an active central piece and prepares Rd1.'),('Kh1',False,'A king sidestep does not take the central pawn or develop the initiative.'),('h3',False,'This does not carry out the centralizing capture requested.')]),
    opening_lesson('dynamic-pieces', 'Judge an unusual exchange by the resulting activity',
        'The bishop pair is valuable, and a castled king normally likes its bishop shield. Nevertheless, a concrete position can justify trading that bishop for a central knight. Furman–Spassky shows Black using active knights and central counterplay. Explain the compensation and the risk before treating an exception as a rule.',
        FURMAN[:17], 'Before recapturing on f5, use the g7 bishop to capture the knight on d4.',
        [('Bxd4',True,'The bishop captures Nd4 through f6 and e5, before the knight recaptures on f5.'),('Nxf5',False,'This recaptures directly; the exercise asks for the bishop exchange first.'),('gxf5',False,'This changes the king’s pawn cover rather than exchanging the central knight.')]),
    opening_lesson('quiet-route', 'A quiet king journey prepares the finish',
        'The entertainment pages train imagination as well as opening play. In this composition, White’s king walks out of the queen’s way while Black’s pieces have tightly restricted jobs. Work backward from the final mating line, then check the safe route. This artificial position teaches calculation, not an opening king march.',
        QUIET_LINE[:8], 'Complete the demonstrated king journey with checkmate.',
        [('Qh7#',True,'The h-file is clear, so Qh7 checks along h7–e4 while the escape squares remain covered.'),('Qg3',False,'Qg3 does not checkmate. The final route was built for the h-file queen check.'),('g3',False,'A pawn move does not deliver the available mating check.')], start=QUIET, objective='checkmate'),
    opening_lesson('composition-lessons', 'Read composed problems without importing bad habits',
        'A composition can reward a quiet key, an indirect route, a deliberately offered piece, or repeated checks that save a lost position. Its task must be read exactly: mate and draw are different goals. The same calculation skills help real games, but the special arrangement is not a recipe for normal opening play.',
        (), 'Begin the f8–f7 checking cycle that forces the king between h8 and h7.',
        [('Qf8+',True,'Qf8+ forces Kh7; Qf7+ then forces Kh8, creating a repeatable cycle.'),('Qh7+',False,'Black can capture the unprotected queen with Kxh7.'),('Qe7',False,'This is not check and lets Black choose a plan rather than forcing the cycle.')], start=REPETITION),
    opening_lesson('pawn-journey', 'Follow the unexpected pawn all the way to promotion',
        'Loyd’s Excelsior composition challenges the assumption that only an already powerful piece can give mate. The b-pawn advances, changes files by capturing, and promotes on a8. Its journey is supported by threats from other pieces: count moves, keep the destination in mind, and re-evaluate the board after each capture.',
        EXCELSIOR_LINE[:8], 'Promote by capturing on a8 and deliver checkmate.',
        [('bxa8=Q#',True,'The pawn becomes a queen on a8; the diagonal a8–h1 delivers mate.'),('bxa8=R',False,'A rook on a8 cannot check Kh1 along a diagonal.'),('b8=Q',False,'A queen on b8 does not deliver the required checkmate.')], start=EXCELSIOR, objective='checkmate'),
]
