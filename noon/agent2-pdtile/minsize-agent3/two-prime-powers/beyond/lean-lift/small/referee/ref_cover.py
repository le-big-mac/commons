"""Are the test groups of ref_thmS.py covered by Theorem 7 (Gamma > 0 for some choice of q, or with no q)?  And by
Theorem 2 (at most two primes) or Theorem 3 (three primes, two of them to the first power)?  Theorem 6 (the digit
recursion c(m) of the second result) cannot hold when some prime p has exponent >= p in m: c(m) <= 2^-(number of digits)
and each step needs c(m/p) > 2^(1-p), so a digit of p must be among the first p - 1 digits taken (referee's remark, by
hand; printed here as 'Theorem 6 excluded by hand' when, for every choice of q, some prime keeps an exponent >= p).
Gamma: ref_gamma.gamma_all (written from section 5 of sign-all-result.md)."""
import math
from ref_gamma import gamma_all
from ref_thmS import GROUPS, fstr
for G, f in GROUPS.items():
    n = math.prod(p ** a for p, a in f.items())
    res = []
    for q in [None] + sorted(f):
        rest = [(p, a) for p, a in sorted(f.items()) if p != q]
        res.append((q, gamma_all(rest)))
    pos = [(q, g) for q, g in res if g > 0]
    t2 = len(f) <= 2
    t3 = len(f) == 3 and sorted(f.values())[:2] == [1, 1]
    t6_excluded = all(any(a >= p for p, a in f.items() if p != q) for q in [None] + sorted(f))
    print(f'group {G}: n = {n} = {fstr(f)} (about {float(n):.3g}): Theorem 2: {t2}; Theorem 3: {t3}; '
          + ('Theorem 6 excluded by hand; ' if t6_excluded else 'Theorem 6 not examined; ')
          + ('Theorem 7: Gamma > 0 for q = ' + ', '.join(f'{q} ({float(g):.3g})' for q, g in pos) if pos else 'Theorem 7: Gamma <= 0 for every q and for no q')
          + ('  => covered by none of Theorems 2, 3, 6, 7' if not (t2 or t3 or pos) and t6_excluded else ''))
