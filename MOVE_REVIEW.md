# Independent move-by-move review

Every move lists each move played by the selected player, preserving its exact
mainline ply, SAN move, starting position and resulting position. It supports
custom PGN positions, either color, promotions and terminal positions.

The board, move selector, table and local explanation use the selected move.
Best/reply continuations are replayed legally before presentation. The line
slider follows the displayed variation, with at most six plies retained. Engine
lines are examples found by the search, not proof that every reply is forced.

## Assessment method

Stockfish examines two candidate moves before the player's move and the actual
position afterward. Each search has a 0.2-second limit. Scores use the player's
perspective consistently. Positive pawn evaluations mean better for the player;
mate distances and terminal mate/draw positions are shown explicitly.

The Stockfish 16 WDL model converts the scores into expected results at the
position's actual ply. Expected result includes draws; it is not a personalized
prediction of a beginner's winning probability. The player's live Chess.com
rating guides vocabulary and coaching, not an invented rating-adjustment formula.

The loss is the nonnegative difference between before/after expectations:

- Excellent: up to 0.02.
- Good: over 0.02 through 0.05.
- Inaccuracy: over 0.05 through 0.10.
- Mistake: over 0.10 through 0.20.
- Blunder: over 0.20.

Exact boundary ties use the less severe band. The engine's top choice is Best;
its loss is treated as zero to avoid contradictory labels caused by differences
between two bounded searches. A position with one legal move is Forced.

Great candidate requires the engine's top move, measured loss no greater than
0.02, expectation below 0.95 beforehand and at least 0.50 afterward, plus a
second-best expectation at least 0.10 worse. Brilliant candidate uses the same
soundness thresholds and requires a legal capture of the offered non-pawn
piece at the start of a reply line of at least three plies. At least two pawn
units of material must remain lost throughout that line. These conservative
rules can miss deserving moves. They are independent candidates, not official
Chess.com awards or exhaustive tactical proofs.

Book and Miss labels are not guessed without supporting opening/opponent-error
evidence. Losing an earlier mating line can supplement a move's explanation.

## Provenance and compatibility

Chess.com's public API supplies game PGN and sometimes overall player accuracy;
it does not document per-move classifications. The displayed overall accuracy
is retained as published and is never calculated from these labels. No external
source code or proprietary evaluation algorithm was copied.

Key mistakes retains the original >1.5-pawn material-loss contract, optional AI
coaching and weekly-plan inputs. Its blunder count can differ from Every move,
which uses expected-result loss. Full review is cached per game and engine
configuration. Replaying/selecting moves or refreshing the live rating does
not rerun Stockfish. A failed upgrade preserves a usable quick review and waits
for an explicit retry. Mock mode is labeled Preview and awards no quality labels.

## Detailed Stockfish view

The separate **Stockfish analysis** view searches every selected-player move at
one second per search. Before the move it requests up to three candidate lines;
after the actual move it searches the reply separately. Each candidate retains
its own evaluation, mate distance, reached depth and up to twelve legal SAN
plies. The entire returned variation is validated even beyond the display cap.
All scores use the selected player's perspective, including when playing Black.

The report compares scored candidates and lets the user replay any candidate or
the played move followed by the engine reply. Board facts explain the opening
move and each reply. Scores describe the searched root position, not an assumed
evaluation of every replayed position. Mate scores remain mate distances rather
than enormous pawn values. Candidates share the one-second MultiPV search
budget, and a deeper search may change rankings. The depth reached is displayed;
a fixed depth is not promised.

The independent review retains its existing labels and search limits. Detailed
Stockfish results have their own session cache keyed by PGN, player color, engine
path and search settings. Generating or retrying a report requires an explicit
click. Failure preserves both the independent review and any prior successful
Stockfish report. Mock preview is not used in this engine-only view. Varying step
descriptions appear below the board navigation to keep the buttons steady.

## Explaining the recommendation

Both review views explain the recommendation's concrete board effects and
annotate each legal ply of the engine sample. Captures, recaptures, checks,
development, and newly opened attacks are checked against the replayed board.
Attack descriptions use legal capture possibilities rather than treating a
pinned piece's attack map as proof of a winning capture. The final summary
describes the displayed material change and activity, without assigning an
unevaluated score to the final board.

Quick review reuses evidence only when position, played move, and recommendation
all match. Otherwise it analyzes that selected position with two bounded
0.5-second searches. The recommendation search is restricted to the stored
move; it does not silently replace the arrow with another move from a deeper
search. The actual-move line is searched separately from the same player's
perspective. Lines and failures are cached, and failed attempts wait for retry.

Implementation references include the official python-chess engine and board
APIs, plus engine-first analysis patterns in ChessBeast and chess-puzzle-maker.
These resources informed the approach; their source code was not copied.

## References

- [Chess.com classification definitions and public loss bands](https://support.chess.com/en/articles/8572705-how-are-moves-classified-what-is-a-blunder-or-brilliant-etc).
- [Chess.com published game/archive schema](https://www.chess.com/news/view/published-data-api#pubapi-endpoint-games-archive).
- [python-chess scores, WDL and engine analysis](https://python-chess.readthedocs.io/en/latest/engine.html#chess.engine.Score.wdl).
- [Lichess explanation of model/depth differences](https://lichess.org/page/accuracy).
- [python-chess root-move restrictions and PV evidence](https://python-chess.readthedocs.io/en/latest/engine.html#chess.engine.Protocol.analyse).
- [python-chess legal board variations](https://python-chess.readthedocs.io/en/latest/core.html#chess.Board.variation_san).
- [ChessBeast engine-first exploration](https://github.com/rlefko/chessbeast#how-it-works).
- [chess-puzzle-maker candidate comparison](https://github.com/linrock/chess-puzzle-maker#how-it-works).
