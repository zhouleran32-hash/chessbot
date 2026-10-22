"""Original warm-ups explaining the appendix's problem-solving language.

These deliberately simple illustrations are not numbered book compositions.
Several have alternate solutions; their purpose is to make the logic visible.
"""
from core.primer_build import after, custom
from core.primer_guides_chapter1 import section, example, check, guide
from core.primer_guides_chapter10 import position_inventory

GUIDES = {}
EXERCISES = []
A = custom({'f6': 'K', 'f5': 'Q', 'h8': 'k'})
B = custom({'f6': 'K', 'e5': 'Q', 'g8': 'k'})
C = custom({'f6': 'K', 'g6': 'Q', 'h8': 'k'})
D = custom({'f7': 'K', 'g6': 'P', 'h8': 'k'})


def q(key, prompt, correct, reason, wrong, correction):
    return check(key, prompt, (correct, True, reason), (wrong, False, correction))


def add(key, title, pages, summary, sections, examples, prompt, choices, checks,
        pitfalls, recap, goals, *, fen=None, objective=None):
    identifier = 'app-' + key
    GUIDES[identifier] = guide(pages, goals, sections, examples, pitfalls, checks, recap)
    position = fen or examples[0]['fen']
    EXERCISES.append(dict(id=identifier, title=title, summary=summary, fen=position,
                         inventory=position_inventory(position), prompt=prompt,
                         choices=choices, objective=objective))


add('introduction', 'Start here: what a composition asks you to prove', (377, 378),
    'A composition is a carefully arranged chess puzzle. Read its task before deciding what counts as success: checkmate within a move limit, a forced win, or a forced draw.',
    (
        section('A position can be a work of art', '''A composer chooses a position to express an idea: perhaps a queen retreats to a corner, a rook is offered to an enemy pawn, or a king walks toward apparent danger. The material balance may look completely unlike your games. That does not make the puzzle pointless. The challenge is to explain the surprising move and the exact cooperation of the pieces. In practical chess you seek the best result; in a direct-mate problem you also have to meet a specified deadline. A winning position is not automatically a solved mate-in-two problem.'''),
        section('Read the stipulation literally', '''The stipulation is the task printed beside the diagram. White to play and mate in two means White can force checkmate by White's second move, whatever legal defence Black chooses. The normal longest line is White's key, Black's reply, White's mate: three half-moves. It does not mean any two moves in total. An immediate mate also meets this warm-up's “within two” task; a composed two-mover is normally designed to require the second White move. A sound two-mover cannot be dismissed merely by showing a slower win. In the warm-up, Qd7 is quiet, then ...Kg8 allows Qg7 mate. Count White's moves, not the number of arrows you click.'''),
        section('Studies ask a different question', '''A winning study asks for a forced winning result, often by promotion, material gain, or a mating net. A drawing study asks the weaker-looking side to secure a draw against winning attempts. Neither normally sets a fixed number of moves. You must still explain why the endpoint is won or drawn: having a new queen is not enough if it is immediately lost, and being far behind does not prevent stalemate. Later lessons develop these distinctions with the actual studies from the book.'''),
        section('How these lessons work', '''Start by locating both kings and naming whose turn it is. Read the explanation, but try to propose a candidate before opening every continuation. Replay slowly and say what changed after each move. The numbered lessons preserve the book's collection and problem number; these introductory boards are simpler original demonstrations. The mate-in-two practice checker tests every legal defence, so it accepts alternate valid keys in an illustration. For longer problems and studies, read the precise practice task: a selected move or mechanism is one checkpoint, not a substitute for explaining the entire solution.'''),
    ),
    (example('Original warm-up: a quiet key, then mate', A, ('Qd7', 'Kg8', 'Qg7#'), (
        position_inventory(A) + ' This is an illustration with more than one winning key.',
        'The queen retreats to d7. It covers h7 along the seventh rank while the king covers g7.',
        'Black has only this legal move. The king goes to g8; it has not been forced there by a check.',
        'The queen gives check on the g-file. White’s king protects g7 and f7; the queen covers f8 and h8. Black has no legal reply.',
    )),),
    'White to move: force checkmate within two of your moves. Any move that meets the task is accepted.',
    (('Qd7', True, 'The quiet key leaves only ...Kg8, followed by Qg7 mate.'),
     ('Qh5+', False, 'After ...Kg8, White cannot checkmate on the next move. A check is not automatically the right key.')),
    (q('deadline', 'How long is a full mate-in-two line?', 'White, Black, White: up to three half-moves.', 'The limit counts the attacker’s moves; Black gets a reply between them.', 'Two half-moves altogether.', 'Black’s first reply does not use up White’s second move.'),
     q('study-task', 'What must a drawing study establish?', 'A way to draw despite the opponent’s best winning attempts.', 'The opponent must be treated as a determined adversary, not a cooperative partner.', 'One sequence in which the opponent accidentally draws.', 'A helpful mistake by the stronger side does not prove a forced draw.')),
    ('Do not substitute a material win for a required mate.', 'Do not read a single displayed line as proof against every defence.'),
    ('State the task first.', 'Count the attacking side’s moves.', 'Make the defender try to refute your idea.'),
    ('Distinguish direct-mate problems from studies.', 'Read the move limit and judge the endpoint.'), objective='mate_in_2')

add('keys-and-tries', 'Keys, threats, tries, and refutations', (377, 378),
    'A good candidate is a hypothesis. A key solves the task; a try looks convincing until a precise defence refutes it.',
    (
        section('Name the roles of the moves', '''The key is the first move that solves the problem. A threat is what the attacker intends if Black does not prevent it. A variation is the continuation after a particular defence. A try is a tempting candidate that fails to one or more replies. These terms help organize your thinking: write the candidate, its intended mate, and Black's strongest objection. A memorable solution is often understandable only after you have seen why the obvious move fails.'''),
        section('Why a checking move can be too crude', '''Checks deserve attention because Black must answer them, but they can move the king away from the mating net. In our original warm-up, Qh5 checks along the h-file. Black escapes to g8. White still has a winning queen, but cannot finish on White's second move. Do not call the move losing: it fails this problem's deadline, which is a different claim. By contrast, Qd7 covers h7 without checking, so Black has no choice but ...Kg8 while the queen remains ready for Qg7 mate.'''),
        section('A beautiful-looking trap can simply be stalemate', '''Qg6 seems attractive because the queen approaches the black king. But after that move, Black on h8 is not checked, and g8, g7 and h7 are unavailable. With no other black piece to move, the game ends immediately in stalemate. There is no later Qg7 mate because Black never gets a legal turn to make. Always perform a legal-move check after a quiet candidate. Empty space around a king is not the same as a legal escape square.'''),
        section('Use failure as a clue', '''When a try fails, identify the exact cause rather than just crossing out its notation. Did the queen abandon a square? Did a defender gain a capture? Did Black have no move at all? The refutation tells you what the real key must preserve or change. The book values unexpected keys, but a quiet first move is an artistic preference, not a law of chess: some of its own historical problems begin with check. Calculate before rejecting a move for looking too obvious.'''),
    ),
    (example('A checking try misses the deadline', A, ('Qh5+', 'Kg8'), (
        position_inventory(A), 'The queen checks, but gives the king the g8 escape.',
        'Black takes that escape. Inspect all White checks: none is checkmate on this turn. White is still winning in ordinary play.')),
     example('A quiet-looking try ends the game incorrectly', A, ('Qg6',), (
        position_inventory(A), 'Black is not in check and has no legal move: stalemate. This cannot be the key to a mating task.'))),
    'Find a move that forces mate within two White moves; avoid both the checking try and stalemate.',
    (('Qd7', True, 'The key changes the queen’s coverage while preserving a legal black reply.'),
     ('Qg6', False, 'This is stalemate, so the required mate cannot happen.')),
    (q('try-result', 'If a try wins eventually but misses the move limit, what do we conclude?', 'It fails the problem’s task, without necessarily losing a real game.', 'Always separate the problem deadline from the position’s practical result.', 'It is a losing chess move.', 'Failure to force mate in two is not evidence of a lost position.'),
     q('quiet-rule', 'Must every valid composition start with a quiet move?', 'No; quiet keys are an aesthetic preference in many problems.', 'Studies and some historical direct-mate problems use checks, captures or promotions as their first move.', 'Yes; a checking key is illegal.', 'The rules of legal chess do not ban checking on the first move.')),
    ('Never praise a key before checking stalemate.', 'A threat is not a guarantee that Black will ignore it.'),
    ('Record the strongest refutation of a try.', 'Separate practical result from problem success.', 'Check quiet moves as carefully as forcing ones.'),
    ('Use the terms key, try and refutation.', 'Explain why a plausible move fails.'), fen=A, objective='mate_in_2')

add('defence-tree', 'Prove the solution: one answer for every defence', (377, 378),
    'You choose one key, Black chooses any legal reply, and then you choose the right continuation. The order of these choices matters.',
    (
        section('The attacker and defender have different jobs', '''To prove a two-move mate, you need one first move that works against all replies. You do not need the same mating move against all replies. Imagine a branching tree: the key is the trunk, Black's replies are the branches, and a checked mating position must finish every branch. Finding one attractive line proves only that line. Black is free to choose the branch you hoped they would overlook.'''),
        section('Build the tree in a reliable order', '''After your candidate, first list king moves, captures of important attacking pieces, checks against your king, blocks of mating lines, and moves that guard the intended mating square. These categories guide attention; they do not replace listing every legal reply in a small problem. A seemingly irrelevant pawn move can block an escape square or uncover a bishop. For each defence, rebuild the position and find a legal mate. Avoid carrying an attacker or defender from a previous branch into the next one.'''),
        section('Our two branches need different answers', '''With White king f6 and queen e5 against Black king g8, Qc7 is a quiet key. Black can choose h8 or f8. After ...Kh8, Qg7 mates because the white king protects the queen and the queen seals the edge. After ...Kf8, Qd8 is one mating finish: the queen controls the eighth rank while the white king covers e7, f7 and g7. Do not play Qg7 mechanically in the second branch. The mating move responds to the king's actual square.'''),
        section('What completion should mean', '''After studying a composition, hide the notes and explain the key plus the answer to each important defence. Then revisit a different branch first. If you remember only the sequence that happened to be displayed, you have memorized a path but have not reconstructed the proof. The simple board here has alternate keys and several mates in one branch; this is intentional in an illustration. The numbered compositions are checked separately for their stated tasks.'''),
    ),
    (example('Defence one: the king goes right', B, ('Qc7', 'Kh8', 'Qg7#'), (
        position_inventory(B), 'The queen moves to c7 and covers the seventh rank.',
        'Black chooses h8. Keep the other variation separate.', 'Qg7 is protected by the king and covers every escape.')),
     example('Defence two: the king goes left', B, ('Qc7', 'Kf8', 'Qd8#'), (
        position_inventory(B), 'The same key must work against a different reply.',
        'Black chooses f8 instead.', 'The queen seals the eighth rank. White’s king on f6 covers e7, f7 and g7, so there is no exit.'))),
    'Find a key that forces mate within two White moves against BOTH legal king replies.',
    (('Qc7', True, 'After ...Kh8 use Qg7 mate; after ...Kf8, Qd8 is one mating finish.'),
     ('Qe6+', False, 'This checking move does not force mate within the required deadline.')),
    (q('branches', 'Does a sound key need one identical mating move against every reply?', 'No; different defences can require different mates.', 'The requirement is a successful answer on every branch.', 'Yes; otherwise the solution is inconsistent.', 'A variation is precisely a different continuation after a different defence.'),
     q('proof', 'You found a beautiful mate after one black move. What remains?', 'Check every other legal defence.', 'Black chooses their reply, so one successful branch is insufficient.', 'The problem is solved.', 'The defender may have a reply that avoids your mating idea.')),
    ('Reset the board between branches.', 'Do not confuse “some reply loses” with “every reply loses”.'),
    ('One key, every defence, an appropriate answer.', 'Verify the final board is checkmate.', 'Reconstruct the solution without notes.'),
    ('Build a complete defensive tree.', 'Explain why different replies require different mates.'), objective='mate_in_2')

add('model-mate', 'Pure, economical, and model mates', (377, 378),
    'A composition can be judged both for correctness and for the economy of its final mating picture. Learn those ideas by inspecting actual squares.',
    (
        section('Correctness comes before appearance', '''First establish ordinary checkmate: the king is in check, cannot escape, cannot capture the checking piece, and cannot block or remove the check. Only then ask about the artistic arrangement. A position with elegant geometry but a legal defence is not checkmate. Likewise, a correct mate does not become invalid merely because it lacks the economy a composer prefers.'''),
        section('Pure mate: account for each flight square', '''In the book's elementary description, a pure mate denies every square beside the mated king for just one reason. A square may be occupied by a black piece, or controlled by one white unit. At the edge, squares outside the board are simply absent. After Qg7 mate in our example, Black's king on h8 has three neighboring board squares: g8, g7 and h7. The queen controls g8 and h7. White's king on f6 protects g7, so Black cannot capture the queen. State each reason separately instead of saying only that the king is trapped.'''),
        section('Economical and model mates', '''An economical mate uses all White's pieces in the mating arrangement, with the traditional exceptions for king and pawns described in the book. A model mate combines purity and economy. In this small illustration the queen performs the checking and seals two flights; the king protects the mating queen. Adding an idle white rook far away would not improve the artistic economy. Adding another attack to an already controlled flight could spoil purity without changing the game's result.'''),
        section('Turn the aesthetic lesson into calculation', '''You need not become a problem-composition judge to benefit. Counting the job of each piece is an excellent blunder check: which piece protects the mating square, which seals the escape, and what happens if it moves? Do not turn the book's taste for non-checking keys or minimal forces into a rule for real games. If you have a sound mate in one, play it. A composition's beauty invites closer observation; it does not override the rules or the result.'''),
    ),
    (example('Original illustration: identify every mating job', C, ('Qg7#',), (
        position_inventory(C), 'The queen checks h8 and controls g8 and h7. The king on f6 protects the queen on g7, completing the mate.')) ,),
    'White to move: give checkmate now, then account for g8, g7 and h7.',
    (('Qg7#', True, 'All three neighboring squares are accounted for, and the checking queen is protected.'),
     ('Qf7', False, 'The king is not in check. With no legal move this is stalemate, not a model mate.')),
    (q('protection', 'What prevents ...Kxg7 after Qg7 mate?', 'White’s king on f6 protects g7.', 'The queen’s proximity alone does not make it safe; the king supplies the protection.', 'A king may never capture a queen.', 'A king may capture an undefended enemy queen if the destination is safe.'),
     q('model', 'What does model mate combine?', 'Purity and economy.', 'It is an artistic classification of a correctly checkmated position.', 'A large material advantage and a check.', 'Those features do not establish either checkmate or the required artistic qualities.')),
    ('Do not count the queen as protecting its own square.', 'Do not confuse beautiful placement with proof of mate.'),
    ('Verify checkmate first.', 'Give each neighboring square a reason.', 'Identify every participating piece’s job.'),
    ('Distinguish pure, economical and model mate.', 'Explain the mating net square by square.'), objective='checkmate')

add('winning-task', 'Winning studies: justify the position you reach', (377, 388),
    'A winning study is finished when the win is established against proper defence, not merely when an attractive sacrifice or promotion has appeared.',
    (
        section('Replace the move deadline with an outcome', '''A study may take several moves to reveal its point. White may first give material away, allow the enemy pawn to queen, or approach a checking rook. Your job is to establish the stipulated result, not to keep the material count favorable at every step. Ask what the final position gives you: forced mate, a safe extra queen, a standard winning pawn ending, or another position whose winning method you can explain.'''),
        section('Promotion is a means, not a verdict', '''The original warm-up starts with White king f7, pawn g6, and Black king h8. The white king protects the pawn's advance and promotion square. After g7 check, Black has only ...Kh7. Promotion to a queen gives check; after ...Kh6, Qg6 mates. Here we can follow the claim all the way to checkmate. In harder studies, stop before saying promotion wins: check whether the new piece can be captured, whether the opponent has a perpetual check, or whether promotion has caused stalemate.'''),
        section('Why underpromotion appears so often', '''A queen is strongest in most positions, but its extra attacks can be harmful when they remove the opponent's last legal move. A knight promotion can give a check a queen cannot, or create a fork. A rook can preserve a needed escape square and avoid stalemate. The appendix's Saavedra and other studies make these mechanisms concrete. Compare resulting boards instead of using “always queen” or “always look for a trick” as a substitute for calculation.'''),
        section('Continue past the spectacular move', '''The key sacrifice is often only the entrance to the solution. Count the remaining material, identify the new side to move, and name the winning plan. If the explanation ends at an advantage rather than mate, describe the conversion and the defender's remaining resource. You do not need to calculate every future move of a routine king-and-queen win, but you do need to know it is that routine win and that no immediate exception undermines it.'''),
    ),
    (example('Original warm-up: protected promotion, then a verified mate', D,
             ('g7+', 'Kh7', 'g8=Q+', 'Kh6', 'Qg6#'), (
        position_inventory(D), 'The pawn advances with check on h8. White’s king protects g7.',
        'The only legal reply is Kh7; g8 is controlled by White’s king.',
        'Promotion gives check on the g8–h7 diagonal. The new queen is protected by the king.',
        'Kh6 is the only legal escape from this check.',
        'The queen gives mate from g6, protected by the king on f7. We have proved the outcome rather than stopping at promotion.')) ,),
    'Promote White’s pawn. Choose any legal promotion; then compare the resulting piece’s job with the demonstrated queen line.',
    (('g8=Q+', True, 'Promotion to a queen gives check and supports the displayed mating finish.'),
     ('Kf8', False, 'The king move is legal, but it does not carry out this promotion exercise.')),
    (q('verdict', 'Why continue analyzing after promotion?', 'The new piece may be lost, stalemate may occur, or counterplay may change the result.', 'A promotion is an event; the study’s result still needs a concrete justification.', 'Every promotion automatically wins.', 'The board after promotion matters more than the name of the new piece.'),
     q('underpromotion', 'When should you seriously consider a knight promotion?', 'When its check or fork does a job a queen cannot.', 'Different movement patterns can make the lower-valued piece the right choice.', 'Whenever the position is a study, regardless of the board.', 'The artistic setting does not make an underpromotion useful by itself.')),
    ('Do not stop the explanation at the sacrifice.', 'Check all four promotion choices when their differences matter.'),
    ('Name the resulting winning method.', 'Check immediate counterplay.', 'Distinguish a verified finish from an illustrative continuation.'),
    ('Explain what proves a winning endpoint.', 'Treat promotion choice as a concrete decision.'), fen=after(('g7+', 'Kh7'), D), objective='promotion')

add('drawing-task', 'Drawing studies: save the game by changing the objective', (377, 393),
    'When winning is impossible, look for the exact mechanism that prevents defeat: stalemate, repetition, sufficient exchanges, or a position the stronger side cannot break.',
    (
        section('The weaker side still has an objective', '''A drawing study deliberately puts White in danger. White may have to give up the last rook or block their own pawn to eliminate every legal move. That can be the right decision because the objective is a draw. A material count alone cannot tell you the result. Before sacrificing, state the mechanism: “If Black captures, I have no legal move and am not checked,” or “Black cannot escape repeated checks without losing the extra material.”'''),
        section('Stalemate has two separate conditions', '''The side to move must have no legal move, and its king must not be in check. Both are essential. Test all its pieces and pawns, not just the king. A forgotten pawn advance destroys many imagined stalemate ideas. In our simple demonstration, White plays Qf7 from g6 with king f6 against Black king h8. The queen covers g8 and h7; the white king covers g7. Black is not checked and has no other unit to move. The result is therefore stalemate.'''),
        section('A demonstration is not a drawing proof', '''In that demonstration, White voluntarily throws away a win; Black has not forced it. The numbered drawing studies are more demanding: the weaker side must arrange a mechanism that survives the stronger side's best alternative. If a rook is offered, ask what happens when Black declines it. If a checking sequence is shown, ask whether the king can leave the checking zone. A study's attractive finale is only decisive when the defender can force it or meet every attempt to avoid it.'''),
        section('Other ways to survive', '''Repeated checking can prevent progress, but a game becomes drawn by the applicable repetition rule or agreement, not just because several checks have been played. A fortress is a position whose defensive structure cannot be broken by the available forces; explain why invasion and pawn breaks fail. Sometimes an exchange leaves only non-mating material. Sometimes king geometry reaches a known drawn pawn ending. Learn which mechanism applies and its conditions, rather than labeling every uncomfortable position a fortress.'''),
    ),
    (example('Original rule demonstration: deliberately stalemating the weaker side', C, ('Qf7',), (
        position_inventory(C) + ' White is winning; the following is a deliberate error to demonstrate the rule.',
        'Black is not checked, g8 and h7 are covered by the queen, and g7 by the king. There are no other black moves, so this is stalemate.')) ,),
    'Rule demonstration: deliberately stalemate Black. This tests the draw condition, not the best way for White to win.',
    (('Qf7', True, 'Black has no legal move and is not in check: exactly the condition for stalemate.'),
     ('Qg7#', False, 'That is checkmate. It wins the game but does not meet this deliberately different task.')),
    (q('stalemate', 'A king has no moves, but its pawn can advance. Is the position stalemate?', 'No; the side still has a legal move.', 'Stalemate concerns the entire army, not only the king.', 'Yes; only king moves count.', 'Every legal piece or pawn move must be considered.'),
     q('sacrifice', 'A rook offer causes stalemate if accepted. What still needs checking?', 'Whether declining the rook lets the opponent win.', 'A forced drawing mechanism must answer the stronger side’s alternatives.', 'Nothing; showing the capture proves a draw.', 'The opponent is not required to accept your offered material.')),
    ('Check whether the king is in check before calling a position stalemate.', 'A repeated-check illustration does not automatically establish a repetition claim.'),
    ('Name the drawing mechanism.', 'Test refusal of sacrifices.', 'Inspect every unit for a remaining legal move.'),
    ('Distinguish checkmate from stalemate.', 'Explain why one cooperative drawing line is insufficient.'), objective='stalemate')

add('soundness', 'Soundness, economy, and alternative solutions', (377, 378),
    'A composed position has a chess task and an artistic intention. Learn to distinguish a correct result, a unique key, and a well-constructed position.',
    (
        section('Legal position is a starting requirement', '''The book requires a composition to be reachable from the ordinary starting position by legal play. That includes mundane details such as whether the kings could both be in check, whether a pawn can stand on a last rank without promoting, and whether a claimed en-passant capture has a possible preceding move. Software can detect many basic inconsistencies, but a board that passes ordinary validity checks is not automatically a complete proof of historical reachability. For practical solving, pay attention to the side to move and any special-move rights actually specified.'''),
        section('One key and later alternatives are different', '''A traditional direct-mate composition aims for a unique first move. A second solving key is commonly called a cook. Several successful continuations after one defence are called duals. These are related artistic issues, but not identical: uniqueness of the key does not imply that every later mating move is unique. Our introductory illustration intentionally has several keys, including Qd7 and Qg5. It teaches the mate-in-two logic without pretending to be a prize problem.'''),
        section('Why pieces should have jobs', '''Economy asks whether the forces used are necessary for the intended construction. A pawn might prevent an unwanted king flight, stop an alternative solution, or permit a precise defensive resource. Such a pawn is not redundant just because it never moves in the displayed main line. To understand a composition, ask what would change if each unit vanished. Do not actually delete pieces and then assume the altered position is the same problem; the exercise is to recognize their roles.'''),
        section('Respect evidence when a source is imperfect', '''Historical texts, diagrams and scanned notation can contain mistakes. If a line seems illegal, first reconstruct the board and check the square, piece and move number. If an alternative appears to solve the task, test all replies before declaring the problem defective. A corrected reading of a blurred symbol is different from changing the chess position. In these lessons, source positions are checked against the diagrams, and material limitations or alternate endings are identified where they matter. The purpose is understanding the chess, not defending a printed answer at any cost.'''),
    ),
    (example('A second valid key in an original teaching illustration', A, ('Qg5', 'Kh7', 'Qg7#'), (
        position_inventory(A) + ' Compare this with Qd7 in the introduction.',
        'The queen controls g8 along the g-file and leaves h7 as Black’s only legal king move.',
        'Black is forced to h7. The new mating target follows the king’s actual position.',
        'Qg7 checks on the seventh rank. White’s king protects g7 and g6; the queen covers the remaining flights.')) ,),
    'Find any move that forces mate within two White moves. This illustration intentionally accepts more than one key.',
    (('Qg5', True, 'This is a second valid key in the original demonstration; it leaves ...Kh7 and Qg7 mate.'),
     ('Qg6', False, 'This candidate stalemates Black immediately.')),
    (q('dual', 'A unique key permits two different mates after one defence. What does that mean?', 'There is a dual in that variation, not necessarily a second key.', 'The first move and later continuation are different stages of the solution.', 'The first move is automatically not unique.', 'A second mating finish does not supply a different solving first move.'),
     q('idle-piece', 'A pawn never moves in the main line. Must it be redundant?', 'No; it may stop a flight, cook, or defensive resource.', 'A stationary unit can be essential to the construction.', 'Yes; only moving pieces contribute.', 'Control and obstruction can matter without a move being played.')),
    ('Do not call an illustration a unique composition without checking it.', 'Basic board validity is not a full retrograde proof.'),
    ('Separate keys from continuations.', 'Ask what each unit prevents.', 'Resolve notation mistakes against the source diagram.'),
    ('Understand cooks and duals.', 'Identify useful stationary pieces.'), objective='mate_in_2')

add('study-method', 'A solving routine you can carry into your games', (377, 388),
    'Use the appendix as deliberate practice: calculate, explain the resistance, test yourself later, and transfer the useful thinking habits to real play.',
    (
        section('Make a position inventory before calculating', '''Say whose move it is, where the kings stand, which pieces are loose, and what the stipulation demands. Name the king's escape squares and the defenders of your proposed mating square. At your current level, a slow accurate inventory is more valuable than an instant spectacular guess. You can use the board to test a candidate after trying to picture it; the goal is gradually to see the consequences before moving the pieces.'''),
        section('Use staged help', '''Try a few sensible candidates and write their purpose in words. If stuck, reveal the first explanation rather than the whole line. Ask whether the theme is clearance, blocking a line, diversion, king geometry, a waiting move, or promotion choice. Then try again. After seeing the solution, close it and reconstruct it. Struggling for a few attentive minutes and then learning the missing idea is useful; staring without a plan is less useful. The book explicitly encourages returning to a study over several days.'''),
        section('Review the failure, not just the answer', '''For each wrong attempt, record one concrete missed detail: an escape square, a capture, a check, a blocked diagonal, or a pawn's last legal move. Review that detail the next day. A remembered move such as Qd7 has little value if you cannot explain why ...Kg8 is forced. Passing a board task plus the concept checks is a progress checkpoint. To deepen retention, explain the idea again after a delay and solve a different position using the same mechanism.'''),
        section('Transfer the method with judgment', '''Your games will rarely reproduce an elaborate composition. The transferable habits are to calculate the opponent's best defence, notice every piece's job, reassess after a sacrifice, and check the final position. In a practical game, a simple safe win is usually sufficient; you do not need the prettiest move or a unique key. Before using a composition pattern, confirm the same conditions exist. One extra pawn move, a different king square, or a missing defender can reverse the result.'''),
    ),
    (example('Reconstruct a known idea without skipping the defence', A, ('Qd7', 'Kg8', 'Qg7#'), (
        position_inventory(A) + ' Before advancing, predict the key and its purpose.',
        'Name the queen’s new control of h7. Then list Black’s legal moves yourself.',
        'Only Kg8 survives the legality check. Predict White’s mate before advancing again.',
        'Explain every black king flight and the protection of the queen. That explanation is the part to remember.')) ,),
    'Reconstruct a mate within two moves, then explain why the defender cannot escape.',
    (('Qd7', True, 'The useful memory is the coverage of h7 and the protected mating square g7.'),
     ('Qh5+', False, 'Check the escape to g8; this check does not meet the two-move deadline.')),
    (q('retention', 'What is a stronger test of understanding than remembering a move?', 'Reconstruct the idea later and answer the defender’s alternatives.', 'That tests the mechanism and the proof rather than recognition alone.', 'Recognize the lesson title.', 'Recognition can feel familiar without producing the solution.'),
     q('transfer', 'Before using a study idea in a game, what should you check?', 'Whether its essential defenders, escapes, and timing still match.', 'A similar-looking board can differ in a decisive detail.', 'Whether the same sacrifice looks impressive.', 'Appearance does not establish that the tactical conditions are present.')),
    ('Do not equate one correct click with permanent mastery.', 'Do not force artistic moves when a simple practical win is available.'),
    ('Inventory, candidates, resistance, endpoint.', 'Revisit the missed detail after a delay.', 'Transfer the mechanism only when its conditions hold.'),
    ('Use staged hints and delayed recall.', 'Apply composition habits to practical games.'), objective='mate_in_2')
