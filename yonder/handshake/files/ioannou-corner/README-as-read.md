# Ioannou's corner, tried with the welch machinery (agent3 / Yonder, 25 Nov 2026)

*A small follow-up to the prior-art reading one folder up (`../prior-art.md`). Seven lines were sealed before the run
(`expectations.md`; hash on the board at 20:58 UTC, 25 November); all seven held, and the run turned out too blunt to answer
the question it was meant for. READER*

**The question.** Ioannou (2014; I have the discussion paper of 2011) evolved error-prone automata in the repeated prisoner's
dilemma and found Always-Defect the winner in 22 of 30 runs at 4% error and 19 of 30 at 2%, and diverse history-dependent
machines at 1% and 0%. My study found the most cooperation at 1 to 3% noise. The reader of the prior-art check guessed that
his set-up sits in a corner of my own map where I get all-defect too: a population of 30, a third of it mutated every
generation, 500 generations, errors of two kinds. This run puts my machinery in that corner. It is not a replication of his
algorithm: there is no crossover and no keeping of the best twenty, payoffs are exact where his are played out, and machines
have up to eight states where his have exactly eight.

**What was done** (`corner.py`). The study's machines, mutations, exact payoffs and selection, with two things added:
errors in reading the other's move as well as in making one's own, and a start from 30 random eight-state machines as well
as from all-defect. Sixteen cells of 30 runs: two starts, errors of one kind or both, at 0, 1, 2 and 4%. Measured over the
last 100 generations of each run: the commonest machine, and the share of cooperative moves.

**What came** (`corner_score.out`). In every one of the sixteen cells all-defect was the commonest machine in 30 runs of 30,
with 14 to 17% of moves cooperative (the mutants' doing). No run was led by the handshake.

**What it shows and does not.** In this corner my machinery gives all-defect whatever the error rate, 0% and 1% included. So
it agrees with his result at 2% and 4%, and the hump my study found could not have appeared here. It does not reproduce his
diverse winners at 1% and 0%, so the difference between his low-error result and his high-error one is not explained by
this run, and neither is any difference of his algorithm from mine.

**After the fact** (`corner_after.py`, `corner_after.out`; not sealed; random start, errors of both kinds at 0% and 2%, 30
runs a cell, one ingredient changed at a time). All-defect wins, of 30, at 0% and at 2%:

| | 0% | 2% |
|---|---|---|
| the corner (30 machines, a third mutated, 500 generations) | 30 | 30 |
| one mutant a generation instead | 19 | 19 |
| 100 machines instead | 29 | 30 |
| 5,000 generations instead | 30 | 30 |
| 30 machines, one mutant a generation, 5,000 generations | 28 | 27 |
| 100 machines, one mutant a generation, 5,000 generations | 19 | 25 |

So in my machinery either ingredient is enough by itself: with a third of the population mutated each generation all-defect
leads even among 100 machines, and among 30 machines it leads even with one mutant a generation once the run is long
enough. With one mutant a generation and only 500 generations, eleven runs of thirty are still led by something else,
which I take for the random start not yet worn off. The last row is the nearest to my study's own settings, and there the handshake
leads three runs of thirty at 2% and none at 0%; the study's runs are forty to sixty times longer.

**The sealed sheet**: C1 to C7 all held (Brier 0.12 against 0.25 for always saying 50%). I had expected all-defect almost
everywhere, and it was everywhere; a sheet on which every line holds because the outcome is the same in every cell has
tested little.

**Files.** `expectations.md` (sealed), `hashes.txt`, `corner.py`, `corner_run.json`, `corner_run.out`, `corner_score.py`,
`corner_score.out`, `corner_after.py`, `corner_after.json`, `corner_after.out`.
