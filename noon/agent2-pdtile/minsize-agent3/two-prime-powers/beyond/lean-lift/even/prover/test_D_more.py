"""More moduli for test_D.py (same checks): several odd primes other than 3, higher powers of 2, and a few with 3."""
import random, sys
from test_D import check, gen
random.seed(47)
st = dict(n=0, levels=0, maxratio=0.0, max1=0.0, closed=0, exceptional=0, worst_bound_3free=0.0)
for n in (280, 770, 130, 260, 98, 250, 160, 112, 350, 120, 126, 210):
    for trial in range(360):
        m = random.randint(4, 11); els = gen(n, m, trial % 6)
        if els: check(n, els, st)
    print(f'n={n} done; totals {st}', flush=True)
