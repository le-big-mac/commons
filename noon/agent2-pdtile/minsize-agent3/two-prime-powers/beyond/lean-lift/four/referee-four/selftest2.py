# selftest2.py -- rfast.py against rlib.py (table on Z_n, matrix product) and against the grid count.
import random
import numpy as np
from rlib import *
from rfast import *

rng = random.Random(7)
cnt = 0
for trial in range(600):
    n = rng.choice([3, 9, 15, 21, 25, 27, 35, 45, 63, 75, 81, 105, 135, 225, 315])
    m = rng.randint(1, 11)
    kind = rng.random()
    if kind < 0.35:
        B = [rng.randrange(n) for _ in range(m)]
    elif kind < 0.7:
        pool = [rng.randrange(n) for _ in range(rng.randint(1, 4))]
        B = [rng.choice(pool) for _ in range(m)]
    else:
        g = rng.choice([d for d in divisors(n) if d > 1])
        B = [(rng.randrange(g) * (n // g) + rng.choice([0, 0, 0, 1])) % n for _ in range(m)]
    slow = bad_all(B, n)
    for d in divisors(n):
        v = bad_fast(B, d)
        assert (v == slow[d]).all(), (n, B, d)
        cnt += 1
    counts, ngood, anybad = bad_counts_fast(B, n)
    assert ngood == int(good_vector(B, n).sum())
print("bad_fast equals bad_at for %d pairs (multiset, d), all signings" % cnt)
cnt = 0
for trial in range(40):
    n = rng.choice([9, 15, 27, 45])
    m = rng.randint(12, 18)
    pool = [rng.randrange(n) for _ in range(rng.randint(2, 5))]
    B = [rng.choice(pool) for _ in range(m)]
    counts, ngood, anybad = bad_counts_fast(B, n)
    g2, tot = good_count_grid(B, n)
    assert g2 == ngood and tot == 1 << m, (n, B)
    cnt += 1
print("good counts by doubling equal the grid counts for %d multisets of 12 to 18 elements" % cnt)
