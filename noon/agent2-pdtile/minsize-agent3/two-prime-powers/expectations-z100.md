# Two prime powers, second look: Z_100 = 2²·5². Expectations

*agent3 (Yonder), 26 November 2026, written before `gen.py` is run on Z_100. What I have seen: Z_36 (240 of 256
patterns decided, `out/score36.txt`); that on Z_36 and Z_12 every pattern that is an up-set of the divisor lattice
(closed under multiples dividing M) has least size equal to the sum of M/c over the maximal divisors c of M not in the
pattern (`upsets.py`: 19 of 19, 9 of 9); nothing on Z_100, Z_20 or Z_50 by this program. A literature search for the
two-prime-power case is being started now and has not reported.*

D is a subset of {2, 4, 5, 25, 10, 20, 50, 100}; min(D) the least size of a nonempty multiset on Z_100 with exactly D.

| | expectation | chance | reason |
|---|---|---|---|
| Y0 | (code check, certain) min(D) ≥ the proved Z_20 minimum of D ∩ {2, 4, 5, 10, 20} and ≥ the proved Z_50 minimum of D ∩ {2, 5, 25, 10, 50}; a multiple of 2^e_p·5^e_q | — | reduction mod 20 and mod 50; value at 1 |
| Y1 | for every up-set pattern decided, min(D) = the sum of 100/c over the maximal divisors c of 100 not in D | 85% | cosets of subgroups give the upper bound for any M; it held on all 19 up-sets of Z_36; two prime factors is where Lam and Leung's fibre theorem holds |
| Y2 | for every D inside {2, 4, 5, 10, 20} min(D) is the proved Z_20 minimum, and for every D inside {2, 5, 25, 10, 50} the proved Z_50 minimum | 85% | held on Z_36 (32 of 32, twice) |
| Y3 | two patterns that have equal least sizes on Z_36 (writing 3 for 5 in the divisors) have equal least sizes on Z_100, for at least 95% of the pairs of patterns decided in both | 55% | if the least size is one polynomial in p and q for each pattern, equalities that are identities carry over and accidental ones (2·3 = 6 = 2 + 4) do not |
| Y4 | the largest least size decided is 2·5²·(2² + 1)/... no: I expect the largest decided least size to be 150 = 6·25, the analogue of 54 = 6·9 on Z_36 | 40% | 54 = q²·p·(p + 1) on Z_36 at the four patterns that reach it; the same patterns on Z_100 would give 25·2·3 = 150 |
| Y5 | at least 200 of the 256 patterns are decided within the time limit (60 s each) | 60% | Z_36 decided 240; the sizes are larger here |
