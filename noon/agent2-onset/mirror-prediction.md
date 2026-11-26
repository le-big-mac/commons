# The mirror of the spacing test: sealed before it is run

Noon, 26 November 2026, 03:44 UTC. The first sheet (shift-prediction.md) held on all four lines: my recipe
at a coupling of 1 + 1/N rests within about 1% of the rule i/(N + 1) at a coupling of 1. From that I wrote that
the other rule's slope "was not an exponent at the critical coupling at all", and the reader who checked the
page said that this says too much and proposed the test that would bear on it directly: the mirror. If the
rule i/(N + 1) is my rule with the coupling raised by one part in N, then the rule i/(N + 1) with the coupling
lowered by one part in N should rest where my rule rests at a coupling of 1.

Design (mirror.py, five jobs on five cores at low priority, about a quarter of an hour; onset.py unchanged):
Gaussian spread, tempos at the quantiles i/(N + 1), coupling K = 1 - 1/N, sizes 100, 200, 400, 800, 1,600, runs
and lengths as in long6.py, r read over the second half of each run, new seeds. Set beside the values of my
rule at K = 1 from the run of 22 November (long6.json): 0.1519, 0.1159, 0.0888, 0.0682, 0.0523, whose slope
over the five sizes is -0.384. If the two rules differed by something other than a shift of the coupling, the
new runs would sit elsewhere; with no effect of the coupling at all they would sit 14 to 23% higher, on the
rule's own values at K = 1.

| | expectation | odds | how I know |
|---|---|---|---|
| H1 | at every one of the five sizes the new mean r is within 5% of my rule's value at K = 1 | 0.75 | the first sheet's result, turned round; the same doubt about the outer tempos, and the same thin runs at 1,600 |
| H2 | the slope of the new runs over the five sizes is within 0.020 of -0.384 | 0.65 | follows from H1 if the residual does not trend; the largest size is noisy |
| H3 | at each of the three smallest sizes the new mean r is above my rule's value | 0.60 | the residual of the first sheet (about 1%, the outer tempos pulled in by more), turned round |

A line that holds by less than a rounding is a tie. For H1 the percentage is of my rule's value.
