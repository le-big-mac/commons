# tree_box.py -- the one-step lemma for a tree coordinate (Lemma 3T) and the count of good patterns on tree boxes.
# Box T x Y with T = Z_{p^a} (first coordinate), Y = Z_{r^c} (second); F = F_q (q = 0: integers).
# For each test function g:
#   (A) the exact number of good patterns (s, sigma) by the definition (all levels (i, j), sibling cubes), signs
#       enumerated on the active rows and columns only (signs on zero rows/columns do not matter);
#   (B) the same number computed through the slices as in the proof: (s, sigma) is good iff for every level j of Y
#       the vectors x_v = [sigma g_v] in V_j (image of the sibling differences at level j) have s*x with nonzero total
#       and not flat at any level i >= 1;  (A) == (B) is asserted;
#   (C) for every (sigma, j): #{s : total != 0 and s*x flat at some level} <= lambda(p, a) 2^(p^a)   (Lemma T), asserted;
#   (D) the rank of g along T, and the fraction of good patterns against the bound of Lemma 3T.
# usage: python tree_box.py p a r c q N maxrows maxcols [seed]
import sys, random, itertools
from fractions import Fraction
import numpy as np
import tb
from tree_single import lam, flat_masks

def rank_mod(M, q):
    """rank of an integer matrix over F_q (q prime) or over Q (q None), exact."""
    if q is None:
        from sympy import Matrix
        return Matrix(M.tolist()).rank()
    A = [[int(t) % q for t in row] for row in M.tolist()]
    rk = 0; rows = len(A); cols = len(A[0]) if A else 0
    for c in range(cols):
        piv = None
        for r_ in range(rk, rows):
            if A[r_][c]: piv = r_; break
        if piv is None: continue
        A[rk], A[piv] = A[piv], A[rk]
        inv = pow(A[rk][c], q - 2, q)
        A[rk] = [(t * inv) % q for t in A[rk]]
        for r_ in range(rows):
            if r_ != rk and A[r_][c]:
                f = A[r_][c]
                A[r_] = [(u - f * t) % q for u, t in zip(A[r_], A[rk])]
        rk += 1
    return rk

def sparse_signs(n, act):
    S = np.ones((2 ** len(act), n), dtype=np.int64)
    if act: S[:, act] = tb.all_signs(len(act))
    return S

def analyse_box(g, p, a, r, c, q):
    n1, n2 = p ** a, r ** c
    spec = [(p, a), (r, c)]
    rows = [v for v in range(n1) if g[v].any()]
    cols = [y for y in range(n2) if g[:, y].any()]
    S1 = sparse_signs(n1, rows)      # (N1, n1)
    S2 = sparse_signs(n2, cols)      # (N2, n2)
    L = lam(p, a)
    goodA = 0; goodB = 0; maxlost = Fraction(0); lostpairs = 0
    for sg in S2:
        h = g * sg[None, :]
        # (A)
        A = S1[:, :, None] * h[None, :, :]
        goodA += int(tb.good_batch(A, spec, q).sum())
        # (B), (C)
        okB = np.ones(S1.shape[0], dtype=bool)
        for j in range(c + 1):
            x = tb.level_image(h, [(r, c)], (j,), q, first_axis=1)      # (n1, r^j)
            SX = S1[:, :, None] * x[None, :, :]
            tnz, flats = flat_masks(SX, p, a, q)
            anyflat = np.zeros(S1.shape[0], dtype=bool)
            for f in flats: anyflat |= f
            lost = int((tnz & anyflat).sum())
            lostpairs += lost
            fr = Fraction(lost, S1.shape[0])
            maxlost = max(maxlost, fr)
            assert fr <= L, "Lemma T violated"
            okB &= tnz & ~anyflat
        goodB += int(okB.sum())
    assert goodA == goodB, "slices criterion differs from the definition"
    total = S1.shape[0] * S2.shape[0]
    return Fraction(goodA, total), maxlost, Fraction(lostpairs, total)

def make(kind, p, a, r, c, q, rnd, maxrows, maxcols):
    n1, n2 = p ** a, r ** c
    hi = (q - 1) // 2 if q else 2
    g = np.zeros((n1, n2), dtype=np.int64)
    def rows_pick(w):
        t = rnd.randrange(3)
        if t == 0: return rnd.sample(range(n1), min(w, n1))
        if t == 1:   # whole sibling groups of leaves
            out = []
            for D in rnd.sample(range(p ** (a - 1)), max(1, min(w // p, p ** (a - 1)))):
                out += [D + u * p ** (a - 1) for u in range(p)]
            return out[:maxrows]
        i = rnd.randrange(1, a + 1)   # one leaf in each class of one group at level i
        D = rnd.randrange(p ** (i - 1))
        return [D + u * p ** (i - 1) + p ** i * rnd.randrange(p ** (a - i)) for u in range(p)]
    def cols_pick(w):
        t = rnd.randrange(3)
        if t == 0: return rnd.sample(range(n2), min(w, n2))
        if t == 1:
            out = []
            for D in rnd.sample(range(r ** (c - 1)), max(1, min(w // r, r ** (c - 1)))):
                out += [D + u * r ** (c - 1) for u in range(r)]
            return out[:maxcols]
        j = rnd.randrange(1, c + 1)
        D = rnd.randrange(r ** (j - 1))
        return [D + u * r ** (j - 1) + r ** j * rnd.randrange(r ** (c - j)) for u in range(r)]
    R = rows_pick(rnd.randrange(1, maxrows + 1)); C = cols_pick(rnd.randrange(1, maxcols + 1))
    if kind == 0:      # random 0/1 on the chosen rows and columns
        for v in R:
            for y in C:
                if rnd.random() < 0.6: g[v, y] = 1
    elif kind == 1:    # product c (x) h
        cv = {v: rnd.choice([1, 1, -1, 2]) for v in R}; hv = {y: rnd.choice([1, 1, -1, 2]) for y in C}
        for v in R:
            for y in C: g[v, y] = cv[v] * hv[y]
    elif kind == 2:    # "permutation": distinct rows, distinct columns
        m = min(len(R), len(C))
        for v, y in zip(R[:m], C[:m]): g[v, y] = 1
    elif kind == 3:    # all slices equal up to sign (rank one, 0/1 up to sign)
        hv = {y: rnd.choice([0, 1, 1]) for y in C}
        for v in R:
            e = rnd.choice([1, -1])
            for y in C: g[v, y] = e * hv[y]
    elif kind == 4:    # rank two: slices alpha h1 + beta h2
        h1 = {y: rnd.randrange(-1, 2) for y in C}; h2 = {y: rnd.randrange(-1, 2) for y in C}
        for v in R:
            al, be = rnd.randrange(-1, 2), rnd.randrange(-1, 2)
            for y in C: g[v, y] = al * h1[y] + be * h2[y]
    elif kind == 5:    # random values of F_q
        for v in R:
            for y in C: g[v, y] = rnd.randrange(-hi, hi + 1)
    elif kind == 6:    # full 0/1 block
        for v in R:
            for y in C: g[v, y] = 1
    else:              # sum of two blocks on sibling groups
        for _ in range(2):
            R2 = rows_pick(maxrows); C2 = cols_pick(maxcols)
            for v in R2[:maxrows // 2 + 1]:
                for y in C2[:maxcols // 2 + 1]: g[v, y] += 1
    return g

def main():
    p, a, r, c, q, N, maxrows, maxcols = [int(t) for t in sys.argv[1:9]]
    seed = int(sys.argv[9]) if len(sys.argv) > 9 else 1
    q = q or None
    rnd = random.Random(seed)
    n1, n2 = p ** a, r ** c
    L = lam(p, a)
    least = {}; cnt = 0; maxlost = Fraction(0); maxpairs = Fraction(0)
    names = ["random 0/1", "product", "permutation", "slices equal up to sign", "rank two", "random values", "full block", "two blocks"]
    for it in range(N):
        kind = it % 8
        g = make(kind, p, a, r, c, q, rnd, maxrows, maxcols)
        if q:
            if not (g % q).any(): continue
        elif not g.any(): continue
        rows = [v for v in range(n1) if g[v].any()]; cols = [y for y in range(n2) if g[:, y].any()]
        if len(rows) > maxrows or len(cols) > maxcols: continue
        fr, ml, lp = analyse_box(g, p, a, r, c, q)
        rk = rank_mod(g, q)
        cnt += 1
        key = (names[kind], "rank 1" if rk == 1 else "rank >= 2")
        if key not in least or fr < least[key][0]: least[key] = (fr, lp)
        maxlost = max(maxlost, ml); maxpairs = max(maxpairs, lp)
    print("box Z_%d x Z_%d over %s, levels %d: %d functions (<= %d active rows, <= %d active columns)" % (n1, n2, "F_%d" % q if q else "Q", (a + 1) * (c + 1), cnt, maxrows, maxcols))
    print("  definition == slices criterion for every function; Lemma T held for every (sigma, level); largest lost fraction for one (sigma, level): %s (bound %s)" % (maxlost, L))
    print("  largest sum over the levels of Y of the lost fraction: %s (the union bound allows %s)" % (maxpairs, (c + 1) * L))
    for key in sorted(least):
        print("  %-26s %-10s least fraction of good patterns %s" % (key[0], key[1], least[key][0]))
    allmin = min(v[0] for v in least.values())
    print("  least over all: %s" % allmin)

if __name__ == "__main__":
    main()
