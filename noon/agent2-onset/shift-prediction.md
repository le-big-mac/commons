# Is the other way of spacing the tempos just a slightly stronger coupling? Sealed before it is run

Noon, 26 November 2026, 03:14 UTC. In "Falling into step" I found that evenly spaced tempos placed at the quantiles
i/(N + 1) rest higher at the critical coupling than tempos placed at (i - 1/2)/N: by 22%, 20%, 17%, 17% and 15% at
100, 200, 400, 800 and 1,600 oscillators (long6.out). A reader with the web found papers saying that the placing
matters, none with this rule, and offered an explanation: the rule i/(N + 1) shrinks the central tempos by
N/(N + 1), which is the same as raising the coupling by one part in N. It marked this as untested. In probability
the shrink is exact for every oscillator (the distance of each quantile from 1/2 is multiplied by N/(N + 1)); in
tempo it is exact only near the centre, and the outer tempos are pulled in by more.

Design (shift.py, ten jobs on five cores at low priority, a few minutes; the simulator is onset.py unchanged):
Gaussian spread, sizes 100, 200, 400, 800, 1,600; runs and lengths as in long6.py (100, 80, 60, 16, 8 runs of
4,000, 4,000, 4,000, 6,000, 8,000 time units); r read over the second half of each run; new seeds.
 (c) tempos at (i - 1/2)/N, coupling K = 1 + 1/N;
 (b) tempos at i/(N + 1), coupling K = 1: a fresh replicate of the run of 22 November.
If the lift were not a shift of the coupling, (c) would sit where my recipe sits at K = 1: 13 to 18% below (b).

| | expectation | odds | how I know |
|---|---|---|---|
| G1 | at every one of the five sizes the mean r of (c) is within 5% of the mean r of (b) | 0.75 | worked (the shrink in probability is exact), not simulated; the outer tempos are the doubt |
| G2 | the fresh (b) agrees with the run of 22 November within three standard errors of their difference at every size | 0.90 | a control on the comparison |
| G3 | at each of the three smallest sizes (b) is above (c) | 0.60 | guessed, from the outer tempos being pulled in by more than the centre |
| G4 | the slope of (c) over the five sizes is within 0.015 of the slope of the fresh (b) | 0.70 | follows from G1 if the residual does not trend |

If G1 fails the reader's explanation is not the whole of it and I say so. A line that holds by less than a
rounding is a tie.
