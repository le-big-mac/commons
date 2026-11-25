"""Z_{p^n q} exploration (agent3 / Yonder): census of zero patterns of all subsets of Z_M containing 0, with exact D+,
for M = 24 (p=2, n=3, q=3).  Pattern written as E = {a : Phi_{p^a} | A}, F = {a : Phi_{p^a q} | A} (0 in F means Phi_q)."""
import sys, itertools, numpy as np
sys.path.insert(0, "/srv/commons/agent2-pdtile/flat"); sys.path.insert(0, "/home/agent3/review2")
from lp import Setup
from lemma_variants import residues
p, n, q = (int(x) for x in sys.argv[1:4]) if len(sys.argv) > 3 else (2, 3, 3)
M = p ** n * q
orders = [("E", a, p ** a) for a in range(1, n + 1)] + [("F", a, p ** a * q) for a in range(0, n + 1)]
S = Setup(M); R = [residues(d, M) for _, _, d in orders]
Dcache = {}
def D(code):
    if code not in Dcache: Dcache[code] = S.Dplus([orders[i][2] for i in range(len(orders)) if code >> i & 1])[0]
    return Dcache[code]
def EF(code):
    E = [orders[i][1] for i in range(len(orders)) if code >> i & 1 and orders[i][0] == "E"]
    F = [orders[i][1] for i in range(len(orders)) if code >> i & 1 and orders[i][0] == "F"]
    return E, F
stats = {}
bits = M - 1; chunk = 1 << 17
for lo in range(0, 1 << bits, chunk):
    idx = np.arange(lo, min(lo + chunk, 1 << bits), dtype=np.int64)
    X = np.ones((len(idx), M), dtype=np.int32)
    for b in range(bits): X[:, b + 1] = (idx >> b) & 1
    size = X.sum(1); code = np.zeros(len(idx), dtype=np.int64)
    for i, Rd in enumerate(R): code |= (~np.any(X @ Rd.T.astype(np.int32), axis=1)).astype(np.int64) << i
    for c in np.unique(code):
        sel = code == c; ns = size[sel]; d = D(int(c))
        st = stats.setdefault(int(c), [0, 10 ** 9, 0]); st[0] += int(sel.sum()); st[1] = min(st[1], int(ns.min()))
        if d.denominator == 1: st[2] += int((ns == int(d)).sum())
print(f"M={M} (p={p}, n={n}, q={q}): {1 << bits} sets; {len(stats)} zero patterns occur")
print("  E          F            sets   min|A|    D+    k  0inF  F<=E  E<=F  pd-tiling sets")
tot = 0
for c in sorted(stats, key=lambda c: (EF(c)[0], EF(c)[1])):
    E, F = EF(c); cnt, mn, pd = stats[c]; k = p ** len(E) * (q if 0 in F else 1); tot += pd
    Fp = [a for a in F if a > 0]
    flag = "" if pd == 0 else ("  <-- pd-tiling, 0 not in F, F not in E" if (0 not in F and not set(Fp) <= set(E)) else ("  <-- pd-tiling, T2 open" if (0 in F and not set(E) <= set(F)) else ""))
    if pd or (0 not in F and not set(Fp) <= set(E)) or (0 in F and not set(E) <= set(F)):
        print(f"  {str(E):10s} {str(F):12s} {cnt:7d} {mn:6d} {str(D(c)):>6} {k:4d}  {str(0 in F):5s} {str(set(Fp) <= set(E)):5s} {str(set(E) <= set(F)):5s} {pd:8d}{flag}")
print("  total pd-tiling sets containing 0:", tot)
