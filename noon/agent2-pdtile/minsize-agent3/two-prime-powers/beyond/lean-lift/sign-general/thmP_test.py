# thmP_test.py -- numerical tests of Theorem P (product patterns) and of the steps of its proof.
# Box X = X_1 x ... x X_k; f : X -> F (F = Q or F_q); pattern sigma = (sigma_1..sigma_k), sigma_i : X_i -> {+1,-1};
# sigma f is GOOD if every level has a nonzero cube sum (over F).  Theorem P: if the sides, in some order,
# satisfy n_1 >= 3, n_j >= 2j, then at least 2^-k of all patterns are good, for every nonzero f.
import itertools, sys, numpy as np
def setup(sides):
    k = len(sides); cells = list(itertools.product(*[range(s) for s in sides]))
    T = np.zeros((len(cells), len(cells)), dtype=np.int64)
    for a, j in enumerate(cells):
        for b, x in enumerate(cells):
            c = 1
            for i in range(k):
                if j[i] >= 1: c *= 1 if x[i] == j[i] else (-1 if x[i] == 0 else 0)
            T[a, b] = c
    lev = np.array([sum(1 << i for i in range(k) if j[i] >= 1) for j in cells])
    sig = []
    for s in itertools.product(*[list(itertools.product([1, -1], repeat=n - 1)) for n in sides]):
        full = [(1,) + t for t in s]      # first value of each coordinate +: each class of 2^k patterns once
        sig.append(np.array([int(np.prod([full[i][x[i]] for i in range(k)])) for x in cells], dtype=np.int64))
    return cells, T, lev, np.array(sig)
def good_fraction(sides, W, q, pre=None):
    cells, T, lev, S = pre or setup(sides); k = len(sides)
    out = []
    for w in W:
        I = (S * w) @ T.T
        if q: I %= q
        g = np.ones(len(S), dtype=bool)
        for L in range(1 << k): g &= np.any(I[:, lev == L] != 0, axis=1)
        out.append(g.mean())
    return np.array(out)
rng = np.random.default_rng(5)
def report(sides, W, q, name, pre=None):
    W = np.array([w for w in W if np.any(w % q if q else w)])
    fr = good_fraction(sides, W, q, pre)
    k = len(sides)
    print("box %s over %s, %s: %d nonzero functions, least fraction of good patterns %.5f (bound 2^-%d = %.5f) %s"
          % (sides, "F_%d" % q if q else "Q", name, len(W), fr.min(), k, 2.0 ** -k, "OK" if fr.min() >= 2.0 ** -k else "*** BELOW THE BOUND ***"))
    sys.stdout.flush()
part = sys.argv[1]
if part == "a":
    pre = setup([3, 5])
    report([3, 5], rng.integers(0, 2, size=(4000, 15)), 0, "random 0/1", pre)
    report([3, 5], rng.integers(-2, 3, size=(4000, 15)), 0, "random in -2..2", pre)
    report([3, 5], rng.integers(-1, 2, size=(4000, 15)) * (rng.random((4000, 15)) < 0.35), 0, "sparse", pre)
    for q in (7, 11, 13):
        report([3, 5], rng.integers(0, 2, size=(3000, 15)), q, "random 0/1", pre)
        report([3, 5], rng.integers(0, q, size=(3000, 15)), q, "random residues", pre)
        report([3, 5], rng.integers(0, q, size=(3000, 15)) * (rng.random((3000, 15)) < 0.3), q, "sparse residues", pre)
    pre = setup([5, 5])
    for q in (0, 3, 7):
        report([5, 5], rng.integers(0, 2, size=(1500, 25)), q, "random 0/1", pre)
        report([5, 5], rng.integers(-1, 2, size=(1500, 25)) * (rng.random((1500, 25)) < 0.3), q, "sparse", pre)
    pre = setup([3, 7])
    for q in (0, 5):
        report([3, 7], rng.integers(0, 2, size=(1500, 21)), q, "random 0/1", pre)
        report([3, 7], rng.integers(-1, 2, size=(1500, 21)) * (rng.random((1500, 21)) < 0.3), q, "sparse", pre)
if part == "b":
    pre = setup([3, 5, 7])
    for q in (0, 11):
        report([3, 5, 7], rng.integers(0, 2, size=(150, 105)), q, "random 0/1", pre)
        report([3, 5, 7], rng.integers(0, 2, size=(250, 105)) * (rng.random((250, 105)) < 0.1), q, "sparse 0/1", pre)
        # structured: unions of lines, products
        W = []
        for _ in range(250):
            w = np.zeros((3, 5, 7), dtype=np.int64)
            for _ in range(rng.integers(1, 4)):
                ax = rng.integers(0, 3); idx = [rng.integers(0, n) for n in (3, 5, 7)]; idx[ax] = slice(None)
                w[tuple(idx)] += 1
            for _ in range(rng.integers(0, 3)):
                w[rng.integers(0, 3), rng.integers(0, 5), rng.integers(0, 7)] ^= 1
            W.append((w % 2).reshape(-1))
        report([3, 5, 7], W, q, "unions of lines with a few cells changed", pre)
if part == "c":   # boxes that do NOT satisfy the hypothesis, for comparison
    pre = setup([3, 3]); W = np.array(list(itertools.product(range(-1, 2), repeat=9)))
    for q in (0, 5, 7): report([3, 3], W, q, "all functions with values in -1..1", pre)
    pre = setup([3, 3, 3])
    for q in (0, 5): report([3, 3, 3], rng.integers(-1, 2, size=(1500, 27)) * (rng.random((1500, 27)) < 0.4), q, "sparse", pre)
