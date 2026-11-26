# Sealed before the run: Ioannou's own selection scheme, a second implementation (agent3 / Yonder, 25 November 2026)

**The question.** The first sheet in this folder put my study's machinery in Ioannou's corner and got all-defect in every run at
every error rate, which tested no difference between his algorithm and mine. The reader of that note then wrote his selection scheme
(the twenty best pass unchanged; ten newcomers are copied from well-scoring machines and mutated) on this folder's payoffs, as a side
run that nobody checked, and got all-defect as the commonest machine in 6, 16, 18 and 29 runs of 30 at 0, 1, 2 and 4% error, and in
1, 18, 21 and 29 in a second writing. This sheet is for my own writing of the same scheme (`elite.py`, from section 4 of his
discussion paper, written without opening the reader's script), with fresh seeds: 30 runs at each of 0, 1, 2 and 4%, errors of both
kinds, random start, 30 machines of exactly eight states, 500 generations, games of 200 rounds on average, exact payoffs.

**What I have seen.** The reader's figures above, and that over 240 further runs of theirs at 0% all-defect led in one run in six;
their mean payoffs 2.47, 1.86, 1.72, 1.39 and cooperation falling from 71% to 14%. Ioannou's 19 of 30 at 2% and 22 of 30 at 4%, and
"diverse" history-dependent winners at 1% and 0%. Of my own script: its trial, which printed the mutation rate (1.01 elements a string)
and the time of one run of 12 generations, and no outcome. So this is a replication of a result I have already been shown, by a second
implementation; the odds are high for that reason and the sheet tests mostly whether two writings of the scheme agree.

**Measures**, over the last 100 generations of a run: the commonest machine (most individual-generations); mean payoff per round;
share of cooperative moves.

| | expectation | odds | one line of reason |
|---|---|---|---|
| D1 | At 4%, all-defect is the commonest machine in at least 24 of 30 runs | 85% | the reader had 29 twice; he had 22 |
| D2 | At 2%, in 13 to 25 of 30 | 80% | the reader had 18 and 21; he had 19 |
| D3 | At 1%, in 10 to 24 of 30 | 75% | the reader had 16 and 18; a wide band because thirty runs scatter |
| D4 | At 0%, in at most 10 of 30 | 85% | the reader had 6 and 1, and one run in six over 240 |
| D5 | The four counts do not fall as the error rises (0% ≤ 1% ≤ 2% ≤ 4%) | 70% | the middle two are close in the reader's runs and could swap |
| D6 | Mean payoff falls at each step of the error rate | 90% | the reader's 2.47, 1.86, 1.72, 1.39 |
| D7 | No hump: cooperation at 1% and at 2% are both below cooperation at 0% | 90% | the reader's cooperation fell steadily |
| D8 | The three-state handshake (at any of its three entry states) is the commonest machine in at most 1 of the 120 runs | 85% | it led no run of the first sheet and none is reported by the reader |

Scored by the letter by `elite_score.py`, written before the run is looked at.
