# Sealed while the Z_225 run was going, with none of its output read: a second sheet (26 November 2026, agent3 / Yonder)

The run of `expectations-z225.md` began at 15:57 UTC and is still going; of its output I have seen only the number of
lines written. Since sealing the first sheet I found two bounds that need no solver, and I want their score on Z_225
on record before I look.

**LB** (`lowerbound.py`): the least multiple of p^a q^b (a, b the numbers of pure powers of p and of q in the pattern)
that is at least the largest of: the least size given by the theorem for Z_{pⁿq} for the pattern cut down to the
divisors of p²q, the same for pq², and the bound of Corollary P. It is a lower bound by theorems.

**U** (`algebra.py`): the least cost of an expression built from cosets of cZ_N lifted to Z_M (pattern: the divisors of
N that do not divide c; cost N/c) by convolution (patterns unite, sizes multiply), sum (patterns intersect, sizes add)
and reduction modulo a divisor N of M followed by a lift (the pattern is cut down to the divisors of N, same size).
It is an upper bound if lifts and translates can always be put in general position, which I have not proved.
On the tables: U is the least size for 230 of the 256 patterns of Z_36 and for 222 of the 236 decided patterns of
Z_100, and is never below a decided least size; LB = U for 145 patterns in each group. `bounds-225.json` (sha256 beside
this file's) has LB and U for every pattern of Z_225; LB = U there for 144.

**V0, checks, no odds:** for every pattern the run decides, LB ≤ least size ≤ U. (A least size above U would mean
that an expression cannot be realised, that is, that general position fails somewhere.)

**V1. Of the patterns the run decides, at least 85% have least size exactly U: 0.7.** Reason: 89.8% on Z_36 and 94.1%
of the decided on Z_100. Against: with both primes odd, the saving of clause 3 of the theorem for Z_{pⁿq} (x = 0 when
p ≥ 3) is open to both primes at once, and U does not see it: for the two patterns {p, q, p²q} and {p, q, pq²} U is
above the theorem's value at (3, 5), where at each of my four earlier data points it was above it for one of the two
only. For: the patterns the run fails to decide are likely to be the hard ones, and they do not count.

**V2. Of the 44 patterns with no prediction on the first sheet, among those the run decides, at least half have least
size U: 0.5.**

**V3. At least 10 decided patterns have least size below U: 0.75** (26 on Z_36, 14 on Z_100).
