"""Theorem B, m = 3, with equal elements allowed (the clause as reworded after the referee's report): for every multiset
of three elements at least two of the four signings (first sign +) are good.  Every multiset with 0, every even n <= 100
and some larger; and every odd n <= 45 for completeness.  Exact."""
import itertools
from lib import *
cnt = rep = worst = 0
for n in list(range(2, 101, 2)) + [120, 144, 180, 210] + list(range(1, 46, 2)):
    for rest in itertools.combinations_with_replacement(range(n), 2):
        els = [0] + list(rest)
        _, g = good_signings(n, els); nb = int((~g).sum())
        assert nb <= 2, (n, els, nb)
        cnt += 1; rep += (len(set(els)) < 3); worst = max(worst, nb)
print(f'{cnt} three-element multisets with 0 ({rep} of them with equal elements): never more than {worst} of the 4 signings bad')
