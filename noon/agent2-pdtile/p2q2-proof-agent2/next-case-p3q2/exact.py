"""Exact (rational) classification of the zero patterns of Z_{p^a q^b} and exact exclusion of mixed sets.
(Noon = agent2, 21 November 2026.)   Categories as in classify2.py; every linear programme is solved by the simplex method
in Fractions (Bland's rule), and zeros of sets are tested on integer counts (no floating point anywhere).
usage: exact.py p a q b [--mixed]"""
import sys, itertools
from fractions import Fraction as Fr
from collections import Counter
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))     # steplp.py sits beside this file
from steplp import ram

def simplex_min(A, b, c):
    """minimise c.x subject to A x = b, x >= 0, exactly.  Returns ('infeasible', None, None), ('unbounded', None, None)
    or ('optimal', value, x).  Two phases, Bland's rule."""
    m, n = len(A), len(c)
    A = [[Fr(v) for v in row] for row in A]; b = [Fr(v) for v in b]
    for i in range(m):
        if b[i] < 0: A[i] = [-v for v in A[i]]; b[i] = -b[i]
    tab = [A[i] + [Fr(1) if j == i else Fr(0) for j in range(m)] + [b[i]] for i in range(m)]
    basis = [n + i for i in range(m)]
    def run(cost, ncol):
        # reduced costs for every column of the tableau and the objective value last, so that the row has the length of a
        # tableau row and is updated in step with it; only the first ncol columns may enter.  (The referee's point A1: in an
        # earlier version the row was shorter in phase 2 and its last entry went stale; that value was never used.)
        nall = n + m
        z = [sum(cost[basis[i]] * tab[i][j] for i in range(m)) - cost[j] for j in range(nall)] + [sum(cost[basis[i]] * tab[i][-1] for i in range(m))]
        while True:
            enter = next((j for j in range(ncol) if z[j] > 0), None)
            if enter is None: return 'optimal', z[-1]
            leave = None; best = None
            for i in range(m):
                if tab[i][enter] > 0:
                    r = tab[i][-1] / tab[i][enter]
                    if best is None or r < best or (r == best and basis[i] < basis[leave]): best, leave = r, i
            if leave is None: return 'unbounded', None
            piv = tab[leave][enter]; tab[leave] = [v / piv for v in tab[leave]]
            for i in range(m):
                if i != leave and tab[i][enter] != 0:
                    f = tab[i][enter]; tab[i] = [v - f * w for v, w in zip(tab[i], tab[leave])]
            f = z[enter]; z = [v - f * w for v, w in zip(z, tab[leave])]
            basis[leave] = enter
    st, val = run([Fr(0)] * n + [Fr(1)] * m, n + m)
    if val != 0: return 'infeasible', None, None
    for i in range(m):                                    # drive artificial variables out of the basis where possible
        if basis[i] >= n:
            j = next((j for j in range(n) if tab[i][j] != 0), None)
            if j is None: continue                        # a redundant row
            piv = tab[i][j]; tab[i] = [v / piv for v in tab[i]]
            for k in range(m):
                if k != i and tab[k][j] != 0:
                    f = tab[k][j]; tab[k] = [v - f * w for v, w in zip(tab[k], tab[i])]
            basis[i] = j
    cost = [Fr(v) for v in c] + [Fr(0)] * m
    for row in tab:                                       # forbid the artificial columns
        for j in range(n, n + m): row[j] = Fr(0)
    st, val = run(cost, n)
    if st != 'optimal': return st, None, None
    x = [Fr(0)] * n
    for i, bi in enumerate(basis):
        if bi < n: x[bi] = tab[i][-1]
    assert all(v >= 0 for v in x) and all(sum(A[i][j] * x[j] for j in range(n)) == b[i] for i in range(m))
    assert val == sum(Fr(c[j]) * x[j] for j in range(n))             # the tableau's objective agrees with the basic solution
    return 'optimal', val, x

CAT = {}; LAST = [None, None]          # after classify(): CAT[frozenset of zeros] = category
def classify(p, a, q, b):
    M = p**a * q**b; cls = [(i, j) for i in range(a + 1) for j in range(b + 1)]; ords = [o for o in cls if o != (0, 0)]
    C = {(o, c): ram(p, a, o[0], c[0]) * ram(q, b, o[1], c[1]) for o in cls for c in cls}
    tot = [C[((0, 0), c)] for c in cls]; e = lambda c0: [1 if c == c0 else 0 for c in cls]
    outp = [tot[k] if c[0] == 0 else 0 for k, c in enumerate(cls)]; outq = [tot[k] if c[1] == 0 else 0 for k, c in enumerate(cls)]
    cnt = Counter(); hard = []; CAT.clear()
    for mask in range(1 << len(ords)):
        Z = {o for i, o in enumerate(ords) if mask >> i & 1}
        if cnt: CAT[LAST[0]] = LAST[1]
        LAST[0] = frozenset(Z); LAST[1] = None
        if (1, 0) not in Z and (0, 1) not in Z: cnt['L2'] += 1; LAST[1] = 'L2'; continue
        t2 = all((l, m) in Z for l in range(1, a + 1) for m in range(1, b + 1) if (l, 0) in Z and (0, m) in Z)
        orph = any((l, 0) not in Z and (0, m) not in Z for (l, m) in Z if l and m)
        if t2 and not orph: cnt['a'] += 1; LAST[1] = 'a'; continue
        k = p ** sum(1 for l in range(1, a + 1) if (l, 0) in Z) * q ** sum(1 for m in range(1, b + 1) if (0, m) in Z)
        rows = [e((a, b))] + [[C[(o, c)] for c in cls] for o in ords if o not in Z]; rhs = [1] + [0] * (len(rows) - 1)
        st, v, _ = simplex_min(rows, rhs, tot); assert st == 'optimal'
        D = Fr(M) / v
        if D < k: cnt['b'] += 1; LAST[1] = 'b'; continue
        if (D / k).denominator != 1: cnt['N'] += 1; LAST[1] = 'N'; continue
        rows2 = rows + [tot]; rhs2 = rhs + [v]            # the optimal face
        mp = simplex_min(rows2, rhs2, outp)[1]; mq = simplex_min(rows2, rhs2, outq)[1]
        if mp == 0 or mq == 0: cnt['R'] += 1; LAST[1] = 'R'; continue
        xmax = -simplex_min(rows2, rhs2, [-t for t in e((a - 1, b))])[1]; ymax = -simplex_min(rows2, rhs2, [-t for t in e((a, b - 1))])[1]
        top = (a, b) in Z
        if not top and (xmax == 1 or ymax == 1): cnt['T'] += 1; LAST[1] = 'T'; continue
        if top and (xmax > 0 or ymax > 0): cnt['U'] += 1; LAST[1] = 'U'; continue
        if not top: cnt['H, M not a zero'] += 1
        cnt['H'] += 1; LAST[1] = 'H'; hard.append((frozenset(Z), int(D)))
    CAT[LAST[0]] = LAST[1]
    return cnt, hard

def mixed(p, q, hard):
    """a = 3, b = 2: every mixed set of each open size, exact zero set by integer cuboid sums"""
    import numpy as np
    a, b = 3, 2; M = p**a * q**b; ords = [(l, m) for l in range(a + 1) for m in range(b + 1) if (l, m) != (0, 0)]; val = lambda o: p**o[0] * q**o[1]
    def cub(o):                                           # integer matrix: counts modulo d -> cuboid sums (zero iff Phi_d | A)
        l, m = o; d = val(o); cntm = np.zeros((d, M), np.int64); cntm[np.arange(M) % d, np.arange(M)] = 1; rows = []
        for c in range(d):
            if l and m: rows.append(cntm[c] - cntm[(c + d // p) % d] - cntm[(c + d // q) % d] + cntm[(c + d // p + d // q) % d])
            elif l: rows.append(cntm[c] - cntm[(c + d // p) % d])
            else: rows.append(cntm[c] - cntm[(c + d // q) % d])
        return np.array(rows)
    L = np.vstack([cub(o) for o in ords]); blocks = np.cumsum([0] + [val(o) for o in ords])
    Pl = [[(x + t * (M // p)) % M for t in range(p)] for x in range(M // p)]; Ql = [[(y + t * (M // q)) % M for t in range(q)] for y in range(M // q)]
    ind = lambda line: np.bincount(line, minlength=M)
    VP = np.array([L @ ind(l) for l in Pl]); VQ = np.array([L @ ind(l) for l in Ql])
    KP = [l[0] % (M // (p * q)) for l in Pl]; KQ = [l[0] % (M // (p * q)) for l in Ql]
    H = {}
    for Z, size in hard: H.setdefault(size, set()).add(Z)
    out = []
    for size in sorted(H):
        splits = [(i, (size - i * p) // q) for i in range(1, size // p + 1) if (size - i * p) % q == 0 and (size - i * p) // q >= 1]
        if not splits: out.append((size, len(H[size]), 'no split', 0, 0)); continue
        nsets = hits = 0
        for i, j in splits:
            Qc = list(itertools.combinations(range(len(Ql)), j)); SQ = np.array([VQ[list(c)].sum(0) for c in Qc]); QK = [frozenset(KQ[t] for t in c) for c in Qc]
            for cp in itertools.combinations(range(len(Pl)), i):
                kp = {KP[t] for t in cp}; ok = np.array([not (kp & kq) for kq in QK])
                if not ok.any(): continue
                tot = SQ[ok] + VP[list(cp)].sum(0); nsets += int(ok.sum())
                zero = np.stack([(tot[:, blocks[t]:blocks[t + 1]] == 0).all(1) for t in range(len(ords))], 1)
                for row in np.unique(zero, axis=0):
                    if frozenset(o for o, zz in zip(ords, row) if zz) in H[size]: hits += 1
        out.append((size, len(H[size]), splits, nsets, hits))
    return out

if __name__ == '__main__':
    p, a, q, b = (int(v) for v in sys.argv[1:5]); M = p**a * q**b
    cnt, hard = classify(p, a, q, b)
    print(f"Z_{M} = Z_({p}^{a} {q}^{b}), exact:  " + ", ".join(f"{k} {cnt[k]}" for k in ('L2', 'a', 'b', 'N', 'R', 'T', 'U', 'H')) + f"   (open patterns with M not a zero: {cnt['H, M not a zero']})")
    print("   open patterns by size:", dict(Counter(s for _, s in hard)))
    if '--mixed' in sys.argv:
        for size, npat, splits, nsets, hits in mixed(p, q, hard):
            print(f"   size {size}: {npat} open patterns; " + ("not of the form i p + j q with i, j >= 1: no mixed set" if splits == 'no split' else f"splits {splits}: {nsets:,} mixed sets, {hits} with an open pattern"))
