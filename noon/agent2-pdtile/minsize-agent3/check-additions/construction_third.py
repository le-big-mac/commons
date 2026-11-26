"""A fresh reader's check of the sentence "1,700 patterns, none wrong" in the paragraph added to section 3.
The prover's builder (balanced-half/construct_bal.py, function construct) for every pattern with 0 in F, n = 1..4 and
the five pairs of primes of the author's check; the pattern by code of mine (the tree conditions of section 1, exact
integers; nothing of the author's, the prover's or either referee's), the size by the rule written from the words of
section 3 of the note.  Then two placebos: one element added at 0 (spoils the size every time), and one element moved to the next residue
(same size; counts how often the pattern code sees the change).
usage: construction_third.py PATH_TO_balanced-half"""
import sys, itertools, io, contextlib, importlib.util
import numpy as np

def tree_pattern(p, q, n, w):
    P = p ** n; M = P * q
    g = np.zeros((P, q), dtype=np.int64)
    for x in range(M):
        if w[x]: g[x % P, x % q] += w[x]
    E = []; F = []
    if len(set(g.sum(0).tolist())) == 1: F.append(0)
    for a in range(1, n + 1):
        pa = p ** a; pb = p ** (a - 1)
        T = np.zeros((pa, q), dtype=np.int64)
        for c in range(pa): T[c] = g[c::pa].sum(0)                      # class c mod p^a
        ch = T.reshape(p, pb, q)                                         # ch[i, c0] = child i of the class c0 mod p^(a-1)
        tot = ch.sum(2)
        if (tot == tot[0]).all(): E.append(a)
        d = ch - ch[0]                                                   # differences of the children's vectors
        if (d == d[:, :, :1]).all(): F.append(a)
    return tuple(E), tuple(F)

def rule(p, q, n, E, F):
    e = len(E)
    if set(F) == set(range(n + 1)): return q * p ** e
    a0 = min(a for a in range(1, n + 1) if a not in F)
    deeper = sorted(a for a in F if a > a0 and a not in E); k2 = len(deeper)
    c1 = k2 == 0
    c2 = any(a in E for a in range(1, a0))
    c3 = a0 in E and p >= 3
    c4 = (not c1) and a0 in E and p == 2 and any(a in E and a not in F for a in range(a0 + 1, deeper[0]))
    return q * p ** e * (p ** k2 + (0 if (c1 or c2 or c3 or c4) else 1))

folder = sys.argv[1]
sys.path.insert(0, folder)            # the builder imports pat.py and claims.py from its own folder
spec = importlib.util.spec_from_file_location('construct_bal', folder + '/construct_bal.py')
cb = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(cb)

# the tree-pattern code tried first on multisets whose pattern I worked out by hand from the factors of the mask
# polynomial (my first hand values for two of them were wrong, the code was right: 1 + x^3 = (x + 1)(x^2 - x + 1))
assert tree_pattern(2, 3, 1, [1, 1, 1, 1, 1, 1]) == ((1,), (0, 1))
assert tree_pattern(2, 3, 1, [1, 0, 0, 0, 0, 0]) == ((), ())
assert tree_pattern(2, 3, 1, [1, 0, 0, 1, 0, 0]) == ((1,), (1,))          # {0, 3}: Phi_2 Phi_6
assert tree_pattern(2, 3, 1, [1, 0, 1, 0, 1, 0]) == ((), (0, 1))          # {0, 2, 4}: Phi_3 Phi_6
assert tree_pattern(2, 3, 1, [1, 0, 1, 1, 1, 0]) == ((), ())              # {0, 2, 3, 4}: values 2, 1, -1 at the roots of order 2, 3, 6
# and against the values of the mask polynomial at roots of unity, on random multisets
def root_pattern(p, q, n, w):
    M = p ** n * q; w = np.array(w, dtype=float); x = np.arange(M)
    z = lambda d: abs((w * np.exp(2j * np.pi * x / d)).sum()) < 1e-8
    return tuple(a for a in range(1, n + 1) if z(p ** a)), tuple(a for a in range(0, n + 1) if z(p ** a * q))
rng = np.random.default_rng(20261126); agree = 0; seen = set()
for (p, q, n) in ((2, 3, 2), (3, 2, 2), (2, 3, 3), (2, 5, 2), (3, 5, 2), (5, 2, 2), (2, 3, 4), (3, 2, 3)):
    M = p ** n * q
    for trial in range(1500):
        # sums of a few cosets and points, so that many patterns occur
        w = np.zeros(M, dtype=np.int64)
        for _ in range(rng.integers(1, 4)):
            d = [dd for dd in range(1, M + 1) if M % dd == 0][rng.integers(0, len([dd for dd in range(1, M + 1) if M % dd == 0]))]
            w[(rng.integers(0, M) + d * np.arange(M // d)) % M] += 1
        for _ in range(rng.integers(0, 3)): w[rng.integers(0, M)] += 1
        a = tree_pattern(p, q, n, w.tolist()); b = root_pattern(p, q, n, w.tolist())
        assert a == b, (p, q, n, w.tolist(), a, b)
        agree += 1; seen.add((p, q, n) + a)
print(f"tree pattern = pattern by values at roots of unity on {agree} random multisets in 8 groups ({len(seen)} distinct (group, pattern) pairs)")

tot = bad = pl_tot = pl_caught = mv_caught = 0
for (p, q) in ((2, 3), (3, 2), (2, 5), (5, 2), (3, 5)):
    for n in range(1, 5):
        g_bad = 0; g_tot = 0
        lv = range(1, n + 1)
        for E in itertools.chain.from_iterable(itertools.combinations(lv, r) for r in range(n + 1)):
            for F1 in itertools.chain.from_iterable(itertools.combinations(lv, r) for r in range(n + 1)):
                F = (0,) + F1
                w = list(cb.construct(p, q, n, set(E), set(F))[0])
                good = tree_pattern(p, q, n, w) == (E, F) and sum(w) == rule(p, q, n, E, F)
                g_tot += 1; g_bad += (not good)
                w2 = list(w); w2[0] += 1
                pl_tot += 1; pl_caught += not (tree_pattern(p, q, n, w2) == (E, F) and sum(w2) == rule(p, q, n, E, F))
                w3 = list(w); x0 = next(i for i, v in enumerate(w3) if v); w3[x0] -= 1; w3[(x0 + 1) % len(w3)] += 1
                mv_caught += tree_pattern(p, q, n, w3) != (E, F)
        tot += g_tot; bad += g_bad
        print(f"p = {p}, q = {q}, n = {n}, order {p ** n * q}: {g_tot} patterns with 0 in F, {g_bad} with the wrong pattern or size")
print(f"total {tot} patterns, {bad} wrong;  placebo (one element added at 0): caught {pl_caught} of {pl_tot};  placebo (one element moved to the next residue, same size): pattern changed in {mv_caught} of {pl_tot}")
