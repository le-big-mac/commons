"""Independent test of the Claim inside Noon's Lemma 3 (agent3 / Yonder): in Z_{p q^2}, two tiles of the same size whose sets of prime-power zeros
differ (one has q and not q^2, the other q^2 and not q) have NO common weak complement.
By the first lines of the proof the only case not excluded at once by sizes is |A| = q < p with p not a zero.  For such p, q this script
enumerates every A1 containing 0 with q elements, zero at q, no zero at q^2 or p, and every A2 containing 0 with q elements, zero at q^2, no zero at q
or p, and asks a solver (HiGHS) whether some g >= 0 with g(0) = 1 has 1_{A1} * g = 1 and 1_{A2} * g = 1.
Control: each set alone must have a weak complement (it is a tile)."""
import sys, itertools, numpy as np
from scipy.optimize import linprog
def zeros(A, M, ds):
    out = set()
    for d in ds:
        w = np.exp(2j * np.pi * np.array(sorted(A)) * (M // d) / M)
        if abs(w.sum()) < 1e-9: out.add(d)
    return out
def feasible(sets, M):
    rows = []; rhs = []
    for A in sets:
        for v in range(M):
            r = np.zeros(M)
            for a in A: r[(v - a) % M] += 1
            rows.append(r); rhs.append(1.0)
    r = np.zeros(M); r[0] = 1; rows.append(r); rhs.append(1.0)
    res = linprog(np.zeros(M), A_eq=np.array(rows), b_eq=np.array(rhs), bounds=[(0, None)] * M, method="highs")
    return res.status == 0
for p, q in ((3, 2), (5, 2), (7, 2), (5, 3), (7, 3), (11, 2)):
    M = p * q * q; ds = [p, q, q * q]
    cands = [frozenset((0,) + c) for c in itertools.combinations(range(1, M), q - 1)]
    A1 = [A for A in cands if zeros(A, M, ds) == {q}]; A2 = [A for A in cands if zeros(A, M, ds) == {q * q}]
    ctrl = all(feasible([A], M) for A in A1[:40] + A2[:40])
    common = [(sorted(a), sorted(b)) for a in A1 for b in A2 if feasible([a, b], M)]
    print(f"Z_{M} (p = {p}, q = {q}): {len(A1)} sets with S = {{q}}, {len(A2)} sets with S = {{q^2}}; each alone weak-tiles (first 40 of each): {ctrl}; pairs with a common weak complement: {len(common)} of {len(A1) * len(A2)}" + (f"  e.g. {common[0]}" if common else ""))
