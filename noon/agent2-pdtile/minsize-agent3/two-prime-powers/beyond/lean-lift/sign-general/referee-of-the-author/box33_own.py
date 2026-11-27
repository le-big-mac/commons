"""Referee: Remark (3) after Theorem P' says of the box 3 x 3 (outside the hypothesis of Theorem P) that "the conclusion
holds there".  Here: every nonzero function on 3 x 3 over F_5, all four levels, all patterns: least share of good patterns.
(Not part of any proof; it bears only on the wording of the remark and on the conjecture of section 6.)"""
import numpy as np
from fractions import Fraction as Fr
from itertools import product
from boxtools import all_levels, pattern_array, good_batch

sides = (3, 3); fam = all_levels(2); PA, _ = pattern_array(sides); PA = PA.astype(np.int64)
for q in (5,):
    least = PA.shape[0]; nf = 0; nmin = 0
    tail = np.array(list(product(range(q), repeat=6)), dtype=np.int64)
    for head in product(range(q), repeat=3):
        G = np.concatenate([np.tile(np.array(head, dtype=np.int64), (tail.shape[0], 1)), tail], axis=1)
        G = G[G.any(axis=1)].reshape(-1, 3, 3)
        cnt = np.zeros(G.shape[0], dtype=np.int64)
        for i in range(PA.shape[0]):
            cnt += good_batch(G * PA[i][None], fam, q)
        mn = int(cnt.min())
        if mn < least: least = mn; nmin = 0
        if mn == least: nmin += int((cnt == mn).sum())
        nf += G.shape[0]
    print(f'box 3 x 3, all four levels, every nonzero function over F_{q} ({nf}): least share of good patterns {Fr(least, PA.shape[0])} '
          f'(2^-k = 1/4), attained by {nmin} functions')
