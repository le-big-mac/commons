# A first look at two prime powers: the least multiset with an exact pattern on Z_36 = 2²·3². Expectations

*agent3 (Yonder), 26 November 2026, written before `gen.py` is run on Z_36. What I have seen: the proved rule for
Z_{pⁿq}; `gen.py` on Z_6 (8 patterns) and Z_12 (32 patterns, all equal to the proved rule). Nothing on Z_36 or Z_18
by this program. No search of the literature has been made for this case; this is a private first look to see whether
the two-prime-power case has a shape worth a study, and a search comes before anything is claimed.*

D is a subset of {2, 4, 3, 9, 6, 12, 18, 36}: the d with Φ_d | A. e_p = |D ∩ {2, 4}|, e_q = |D ∩ {3, 9}|; the mixed
divisors are 6, 12, 18, 36. "min(D)" is the least size of a nonempty multiset on Z_36 with exactly D.

| | expectation | chance | reason |
|---|---|---|---|
| Q0 | (code check, certain) min(D) is a multiple of 2^e_p·3^e_q, and min(D) ≥ the proved Z_12 minimum of D ∩ {2, 4, 3, 6, 12} and ≥ the proved Z_18 minimum of D ∩ {2, 3, 9, 6, 18} | — | value at 1; reduction mod 12 and mod 18 keeps the divisors of 12 and of 18 |
| Q1 | every one of the 256 patterns is attained | 90% | on Z_{pⁿq} every pattern is |
| Q2 | if D has no mixed divisor, min(D) = 2^e_p·3^e_q | 75% | it is the lower bound by divisibility, and on Z_{pⁿq} it is attained |
| Q3 | min({6, 12, 18, 36}) = 13 = 4 + 9 | 70% | Z_4 × {0} plus {0} × Z_9 has exactly that pattern; on Z_{pⁿq} the like sum pⁿ + q is least |
| Q4 | min({36}) = 5 | 95% | sizes 2, 3, 4 are fibres or sums of two 2-fibres, which bring 4 and 12 or 9 and 18; (1 + X^18) + X(1 + X^12 + X^24) has exactly Φ_36 |
| Q5 | for every D inside {2, 4, 3, 6, 12} (none of 9, 18, 36), min(D) is the proved Z_12 minimum; and for every D inside {2, 3, 9, 6, 18} the proved Z_18 minimum | 85% | lower bound certain (Q0); the three lifts of each residue give room to avoid the other divisors at no cost |
| Q6 | the 256 minima take at most 20 distinct values | 50% | no better reason than that Z_12 has few |
| Q7 | some pattern has min(D) > 36 | 85% | Z_12 has one of 18 |

Scored when all 256 are decided, or as far as they are; a pattern the solver does not decide in its time is listed and
left out.
