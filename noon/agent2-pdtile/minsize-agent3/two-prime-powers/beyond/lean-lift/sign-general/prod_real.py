# prod_real.py -- test of the statement (Prod): for every nonzero integer function w on a box with sides >= 3
# there are sign patterns sigma_i on the coordinates such that (sigma_1 x ... x sigma_k) * w has every
# ANOVA component nonzero (every level has a nonzero cube sum).  Exact integer arithmetic (int64).
import itertools, sys, numpy as np
def setup(sides):
    k = len(sides); cells = list(itertools.product(*[range(s) for s in sides]))
    T = np.zeros((len(cells), len(cells)), dtype=np.int64)   # I = T w ; rows j, columns x
    for a, j in enumerate(cells):
        for b, x in enumerate(cells):
            c = 1
            for i in range(k):
                if j[i] >= 1: c *= 1 if x[i] == j[i] else (-1 if x[i] == 0 else 0)
            T[a, b] = c
    lev = np.array([sum(1 << i for i in range(k) if j[i] >= 1) for j in cells])
    sig = []
    for s in itertools.product(*[list(itertools.product([1, -1], repeat=n - 1)) for n in sides]):
        # first value of every coordinate has sign + (a global sign per coordinate changes nothing)
        full = [(1,) + t for t in s]
        sig.append(np.array([np.prod([full[i][x[i]] for i in range(k)]) for x in cells], dtype=np.int64))
    return cells, T, lev, sig
def test(sides, W, name):
    cells, T, lev, sig = setup(sides)
    k = len(sides)
    ok = np.zeros(len(W), dtype=bool)
    ngood = np.zeros(len(W), dtype=np.int64)
    for s in sig:
        I = (W * s) @ T.T
        g = np.ones(len(W), dtype=bool)
        for L in range(1 << k):
            g &= np.any(I[:, lev == L] != 0, axis=1)
        ok |= g; ngood += g
    nz = np.any(W != 0, axis=1)
    bad = np.where(nz & ~ok)[0]
    frac = ngood[nz].min() / len(sig)
    print("%s, box %s: %d nonzero functions, %d without a good product pattern; least fraction of good patterns %.4f"
          % (name, sides, nz.sum(), len(bad), frac))
    for b in bad[:3]: print("   FAILS:", W[b].tolist())
    w = W[nz][np.argmin(ngood[nz])]
    print("   least at w =", w.tolist())
    sys.stdout.flush()
if __name__ == "__main__":
    rng = np.random.default_rng(1)
    which = sys.argv[1]
    if which == "a":
        W = np.array(list(itertools.product(range(-1, 2), repeat=9)), dtype=np.int64); test([3, 3], W, "all w in {-1,0,1}")
        W = np.array(list(itertools.product(range(-2, 3), repeat=9)), dtype=np.int64); test([3, 3], W, "all w in {-2..2}")
    if which == "b":
        test([3, 4], rng.integers(-2, 3, size=(400000, 12)), "random w in {-2..2}")
        test([3, 5], rng.integers(-1, 2, size=(200000, 15)), "random w in {-1,0,1}")
        test([4, 4], rng.integers(-1, 2, size=(100000, 16)), "random w in {-1,0,1}")
    if which == "c":
        test([3, 3, 3], rng.integers(-1, 2, size=(60000, 27)), "random w in {-1,0,1}")
        # sparse and low-rank ones
        W = rng.integers(-2, 3, size=(60000, 27)) * (rng.random((60000, 27)) < 0.3); test([3, 3, 3], W, "sparse random w in {-2..2}")
        f = rng.integers(-2, 3, size=(30000, 2, 3, 3))
        W = np.zeros((30000, 27), dtype=np.int64)
        for t in range(2):
            a = rng.integers(-2, 3, size=(30000, 3)); b = rng.integers(-2, 3, size=(30000, 3)); c = rng.integers(-2, 3, size=(30000, 3))
            W += np.einsum('ni,nj,nk->nijk', a, b, c).reshape(30000, 27)
        test([3, 3, 3], W, "sums of two product functions")
