"""Does `Pnq.Tiles` (Pnq/Step.lean) say what 1_A * f = 1 says?  (agent3 / Yonder)
Lean proves `step_structure`: a tree with a step complement gamma satisfies (T1) and (T2).  It cannot check that the recursive predicate
`Tiles gamma 0 t 0` is the identity  sum_{a in A} f(v - a) = 1 for all v  when f is the step function
     f(x) = gamma(d, same)   with d = number of low base-p digits of x mod p^n that vanish (d = n if x = 0 mod p^n), same = (x = 0 mod q).
Two tests, both with the recursion transcribed from the Lean source:
 (1) for RANDOM gamma (any sign) and random or exhaustive sets A, the left-hand side that `Tiles` builds at each leaf and layer equals the
     convolution computed directly in Z_M;
 (2) which sets have a step complement at all (a linear program in the 2(n+1) weights), against which sets tile: the hypotheses of
     `step_structure` should be satisfiable exactly for tiles, so the theorem is not about an empty class."""
import sys, random, itertools
import numpy as np
from scipy.optimize import linprog
sys.path.insert(0, ".")
from tree_vs_cyclo import tree, lay, size, E, F
def val(x, p, n):
    d = 0
    while d < n and x % p == 0: x //= p; d += 1
    return d
def direct(A, gam, p, n, q):
    M = p ** n * q
    return {(v % p ** n, v % q): sum(gam[(val((v - a) % p ** n, p, n), (v - a) % q == 0)] for a in A) for v in range(M)}
def tiles_lhs(t, gam, p, n, q):
    """the left-hand sides that `Tiles` requires to equal 1, as {(u, w): value}; transcription of the Lean recursion"""
    out = {}
    def rec(node, d, ext, u, scale):                     # u = residue so far (low digits), scale = p^d
        if d == n:
            tot = sum(node)
            for w in range(q): out[(u, w)] = ext[w] + gam[(d, True)] * node[w] + gam[(d, False)] * (tot - node[w])
            return
        lays = [lay(c, d + 1, n, q) for c in node]; sizes = [sum(l) for l in lays]
        for c in range(p):
            e2 = [ext[w] + sum(gam[(d, True)] * lays[c2][w] + gam[(d, False)] * (sizes[c2] - lays[c2][w]) for c2 in range(p) if c2 != c) for w in range(q)]
            rec(node[c], d + 1, e2, u + c * scale, scale * p)
    rec(t, 0, [0.0] * q, 0, 1)
    return out
random.seed(10); worst = 0.0; ntest = 0
for p, n, q in [(2, 1, 3), (3, 1, 2), (2, 2, 3), (3, 2, 2), (2, 2, 5), (2, 3, 3), (3, 3, 2), (2, 4, 3), (5, 2, 2), (2, 3, 5)]:
    M = p ** n * q
    for _ in range(300):
        A = sorted(random.sample(range(M), random.randint(1, M)))
        gam = {(d, b): random.uniform(-1, 2) for d in range(n + 1) for b in (True, False)}
        a, b = direct(A, gam, p, n, q), tiles_lhs(tree(A, p, n, q), gam, p, n, q)
        worst = max(worst, max(abs(a[k] - b[k]) for k in a)); ntest += 1
print(f"(1) {ntest} random (set, gamma) pairs in 10 groups: largest difference between the Lean recursion and the direct convolution: {worst:.1e}")
def has_step_complement(A, p, n, q):
    M = p ** n * q; keys = [(d, b) for d in range(n + 1) for b in (True, False)]; idx = {k: i for i, k in enumerate(keys)}
    rows = []; rhs = []
    for v in range(M):
        r = [0.0] * len(keys)
        for a in A: r[idx[(val((v - a) % p ** n, p, n), (v - a) % q == 0)]] += 1
        rows.append(r); rhs.append(1.0)
    r = [0.0] * len(keys); r[idx[(n, True)]] = 1.0; rows.append(r); rhs.append(1.0)
    res = linprog([0.0] * len(keys), A_eq=rows, b_eq=rhs, bounds=[(0, None)] * len(keys), method="highs")
    return res.status == 0
def tiles_group(A, M):
    A = sorted(A); n = len(A)
    if M % n: return False
    k = M // n; full = (1 << M) - 1; masks = [sum(1 << ((a + s) % M) for a in A) for s in range(M)]
    def rec(cov, used):
        if cov == full: return True
        v = (~cov & full); v = (v & -v).bit_length() - 1
        return any(rec(cov | masks[s], used + 1) for s in range(M) if masks[s] >> v & 1 and not masks[s] & cov)
    return rec(0, 0)
def T12(A, p, n, q):
    t = tree(A, p, n, q); Es = [l for l in range(1, n + 1) if E(t, 0, n, q, l)]; F0 = F(t, 0, n, q, 0)
    return len(A) == p ** len(Es) * (q if F0 else 1) and (not F0 or all(F(t, 0, n, q, l) for l in Es))
for p, n, q in [(2, 1, 3), (3, 1, 2), (5, 1, 2), (2, 2, 3), (3, 2, 2)]:
    M = p ** n * q; cnt = dict(step=0, tile=0, t12=0, step_not_tile=0, tile_not_step=0, step_not_t12=0, total=0)
    for m in range(2 ** (M - 1)):
        A = [0] + [i + 1 for i in range(M - 1) if m >> i & 1]
        s = has_step_complement(A, p, n, q); cnt["total"] += 1; cnt["step"] += s
        if s or M % len(A) == 0:
            tl = tiles_group(A, M); t12 = T12(A, p, n, q)
            cnt["tile"] += tl; cnt["t12"] += t12; cnt["step_not_tile"] += s and not tl; cnt["tile_not_step"] += tl and not s; cnt["step_not_t12"] += s and not t12
    print(f"(2) p = {p}, n = {n}, q = {q} (M = {M}): {cnt['total']} sets containing 0; with a step complement {cnt['step']}; tiles {cnt['tile']}; (T1)+(T2) in the Lean definitions {cnt['t12']};"
          f"  step but not tile {cnt['step_not_tile']}, tile but no step complement {cnt['tile_not_step']}, step but not (T1)+(T2) {cnt['step_not_t12']}", flush=True)
