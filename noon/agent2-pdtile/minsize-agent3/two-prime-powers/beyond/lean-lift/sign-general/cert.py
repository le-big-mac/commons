# cert.py -- do the BAD product patterns (as tensors sigma_1 x ... x sigma_k) span a proper subspace of R^X ?
# If they do, some nonzero g has <g, sigma> = 0 for every bad sigma, and then at least 2^-k of the patterns are good.
import itertools, sys, numpy as np
from prod_real import setup
def run(sides, W, name):
    cells, T, lev, sig = setup(sides); k = len(sides); S = np.array(sig)      # patterns x cells
    full = 0; maxrank = 0; worst = None; minfrac = 1.0
    for w in W:
        if not np.any(w): continue
        I = (S * w) @ T.T
        g = np.ones(len(S), dtype=bool)
        for L in range(1 << k): g &= np.any(I[:, lev == L] != 0, axis=1)
        bad = S[~g]
        r = np.linalg.matrix_rank(bad.astype(float)) if len(bad) else 0
        if r > maxrank: maxrank = r; worst = w
        if r == len(cells): full += 1
        minfrac = min(minfrac, g.mean())
    print("%s, box %s: %d functions; largest rank of the bad patterns %d of %d; functions whose bad patterns span everything: %d; least good fraction %.4f"
          % (name, sides, len(W), maxrank, len(cells), full, minfrac))
    if full: print("   e.g. w =", worst.tolist())
    sys.stdout.flush()
rng = np.random.default_rng(2)
run([3, 3], np.array(list(itertools.product(range(-1, 2), repeat=9))), "all w in {-1,0,1}")
run([3, 3], rng.integers(-3, 4, size=(20000, 9)), "random w in {-3..3}")
run([3, 5], rng.integers(-1, 2, size=(5000, 15)), "random w in {-1,0,1}")
run([3, 5], rng.integers(0, 2, size=(5000, 15)), "random 0/1 w")
run([3, 3, 3], rng.integers(-1, 2, size=(3000, 27)), "random w in {-1,0,1}")
run([3, 3, 3], rng.integers(-1, 2, size=(3000, 27)) * (rng.random((3000, 27)) < 0.3), "sparse w in {-1,0,1}")
