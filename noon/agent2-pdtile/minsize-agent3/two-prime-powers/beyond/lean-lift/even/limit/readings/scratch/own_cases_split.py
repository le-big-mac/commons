"""How many of the cases (multiset, d, x) of the author's test of Lemma 1 have an occupied class (a >= 1)?
Same loops as test_two_factors.py, without the signings.  Only counts classes."""
import itertools
from collections import Counter
tot = occ = 0
for n, mmax in ((3, 10), (5, 8), (7, 7), (9, 8), (15, 6), (21, 5), (25, 5), (27, 5), (45, 4), (105, 3)):
    divs = [d for d in range(2, n + 1) if n % d == 0]
    for m in range(2, mmax + 1):
        for rest in itertools.combinations_with_replacement(range(n), m - 1):
            xs = (0,) + rest
            for d in divs:
                cnt = Counter(b % d for b in xs)
                full = 1 if len(cnt) == 1 else 0          # one class holds all m: that x is skipped
                tot += d - full
                occ += len(cnt) - full
print('cases', tot, '; with an occupied class (a >= 1):', occ, '; with a = 0:', tot - occ)
