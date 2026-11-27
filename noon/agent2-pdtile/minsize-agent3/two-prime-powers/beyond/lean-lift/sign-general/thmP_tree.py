# thmP_tree.py -- Theorem P' (levels with at most one digit of each prime): least fraction of good patterns.
import sys, itertools, numpy as np
sys.argv = [sys.argv[0], 'none']   # thmP_test reads argv[1] at import
from thmP_test import setup
from coverage import cbound
rng = np.random.default_rng(11)
def run(sides, q, W, name):
    cells, T, lev, S = setup(sides); k = len(sides)
    levels = [L for L in range(1 << k) if len({sides[i] for i in range(k) if L >> i & 1}) == bin(L).count("1")]
    fm = {p: sides.count(p) for p in set(sides)}
    c = cbound(fm); least = 1.0
    W = [w for w in W if np.any(w % q if q else w)]
    for w in W:
        I = (S * w) @ T.T
        if q: I %= q
        g = np.ones(len(S), dtype=bool)
        for L in levels: g &= np.any(I[:, lev == L] != 0, axis=1)
        least = min(least, g.mean())
    print("digits %s over %s, %s: %d functions, %d of %d levels; least fraction of good patterns %.5f; bound from the recursion: %s %s"
          % (sides, "F_%d" % q if q else "Q", name, len(W), len(levels), 1 << k, least, c, "OK" if least >= c else "*** BELOW ***"))
    sys.stdout.flush()
W33 = np.array(list(itertools.product(range(-1, 2), repeat=9)))
for q in (0, 5, 7): run([3, 3], q, W33, "all functions with values in -1..1")
for q in (0, 5):
    run([3, 3, 7], q, rng.integers(0, 2, size=(400, 63)), "random 0/1")
    run([3, 3, 7], q, rng.integers(-1, 2, size=(600, 63)) * (rng.random((600, 63)) < 0.12), "sparse")
for q in (0, 7):
    run([3, 3, 5], q, rng.integers(-1, 2, size=(1500, 45)) * (rng.random((1500, 45)) < 0.15), "sparse")
    run([3, 3, 5, 5], q, rng.integers(-1, 2, size=(150, 225)) * (rng.random((150, 225)) < 0.05), "sparse")
