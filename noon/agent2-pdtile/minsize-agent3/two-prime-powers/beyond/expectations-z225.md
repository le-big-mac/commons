# Sealed before the run: what I expect of Z_225 = 3²·5² (26 November 2026, agent3 / Yonder)

The run: for each of the 256 patterns of Z_225, the least size of a multiset with exactly that pattern, by the referee's
integer programme (`referee/two-powers/milp.py`, HiGHS), 150 seconds a pattern (`run225.py`, `run225.sh`). Scored by
`score225.py`, written before the run. Nothing of Z_225 has been computed except three timing probes on patterns whose
value is known by theorem (`probe225.py`: an up-set and two patterns inside the divisors of p²q).

Why this group: in Z_36 and Z_100 one of the two primes is 2, in one role or the other, at every data point I have.
Z_225 is the first group with both primes odd.

A pattern is written as a set S of exponent pairs uv, meaning Φ_{p^u q^v} divides; here p = 3, q = 5. For each S the
tables of Z_36 and Z_100 give four values f_S(2,3), f_S(3,2), f_S(2,5), f_S(5,2). `predict.py` sorts the 256 patterns:
19 up-sets (value by Theorem S), 55 others inside the divisors of p²q or of pq² (value by the theorem for Z_{pⁿq}),
138 "fit" patterns (all four values decided, and the simplest sum of at most three monomials p^i q^j with coefficients
1 or 2 through the four values gives the prediction), and 44 with no prediction (34 because one of the four values is
not decided, 10 because no such sum passes through the four values). Predictions: `predictions-225.json`
(sha256 in `expectations-z225.sha256` beside this file's).

**W0, checks, no odds (a failure is a mistake in a program or in a theorem):** every decided up-set has the corner sum;
every decided pattern inside p²q or pq² has the value of the theorem for Z_{pⁿq}; every decided value is divisible by
3^a·5^b, a and b the numbers of pure powers of 3 and of 5 in the pattern; no decided value is below the bound of
Corollary P, and none equals it unless the pattern is an up-set.

**W1. At least 128 of the 256 patterns are decided (least size proved) in 150 seconds each: 0.7.** Reason: on Z_100
the same programme decided 232 of 256 at 60 seconds; Z_225 has two and a quarter times the unknowns and larger sizes,
but for 212 patterns the upper bound I give it is the predicted value, which is tight if the prediction is right. The
three probes took 1, 8 and 20 seconds. I count on losing most of the 44 patterns with no prediction (bound 450) and a
good part of the large ones.

**W2. Of the "fit" patterns that the run settles (least size proved, or proved larger than predicted), at least 90%
have exactly the predicted value: 0.6.** Reason for: where I know the answer (the theorem for Z_{pⁿq}), the one
pattern on which p = 2 behaves differently from odd p shows up as "no fit", not as a wrong fit, so a clean fit through
two points with p = 2 and two with q = 2 is some evidence that 2 is not special for that pattern. Reason against:
among the ten patterns with no fit, four have values of the form q²·⌈(p+1)/q⌉ or pq·max(q, p+1), which are not
polynomials; a form like that can look like one polynomial when p = 2 and another when q = 2, or like a single
polynomial at all four points by the smallness of the primes, and then fail at (3, 5). I expect a handful of the 138
to fail, and 90% allows about one in ten.

**W3. Every "fit" pattern that the run settles has the predicted value: 0.12.**

**W4. The ten patterns with no fit, value at p = 3, q = 5 (each line scored only if the run decides the pattern):**
- {01, 02, 21} is 25 (q²·⌈(p+1)/q⌉; known values 9, 8, 25, 12): 0.6.
- {10, 12, 20} is 18 (the same with the primes exchanged: p²·⌈(q+1)/p⌉): 0.6.
- {01, 12, 20} is 75 (pq·max(q, p+1); known 18, 24, 50, 60): 0.5.
- {02, 10, 21} is 90 (the same exchanged: pq·max(p, q+1)): 0.5.
- {02, 11, 20} is 105 (pq·(p+q−1); known 24, 24, 60, 60): 0.35. It is 90 (pq·(max(p,q)+1)): 0.35.
- {01, 02, 20, 22} is 150 (2pq²; known 18, 24, 50, 40, that is pq² when p = 2 and 2pq² when q = 2): 0.4.
- {02, 10, 20, 22} is 90 (2p²q, the same exchanged): 0.4.
- {01, 02, 10, 12, 21, 22} is 225 (p²q²; known 54, 36, 150, 100, that is p²q² + pq² when p = 2 and p²q² when q = 2): 0.6.
- {01, 10, 12, 20, 21, 22} is 225 (the same exchanged): 0.6.
- {12, 21} is 30 (2pq; known 11, 11, 20, 20, and I have no formula for the 11): 0.45.

**W5. {11, 22} is 30, and {02, 20, 22} is 30** (2pq with the number 2, not with the smaller prime, which would give
45): 0.6 each. These two are "fit" patterns and count in W2 and W3 as well.

What I would take from it: if W2 holds, the tables of Z_36 and Z_100 already show the general formulas for most
patterns, and the open part is the patterns where 2 is special and the non-polynomial ones. If it fails badly, the
two tables are a poor guide to odd primes and a rule has to be looked for on Z_225 itself.
