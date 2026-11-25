r"""Z_{p^n q}: brute-force test of Lemma L, Claim T and the theorem on every subset containing 0 (agent3 / Yonder).
E = {a >= 1 : Phi_{p^a} | A},  F = {a >= 0 : Phi_{p^a q} | A},  e = |E|.
 Lemma L : Phi_q does not divide A and some a >= 1 lies in F \ E   =>   |A| >= p^e (p + q).
 Claim T : Phi_q | A, |A| = p^e q, b >= 1 in F \ E, a in E, a < b    =>   a in F.
 Theorem : D+(Z_A) = |A|  =>  (0 not in F => F inside E and |A| = p^e) and (0 in F => E inside F and |A| = p^e q).
Exact zero sets (integer residues mod Phi_d); exact D+ from agent2's lp.py.  usage: brute.py p n q"""
import sys, numpy as np
sys.path.insert(0, "/srv/commons/agent2-pdtile/flat"); sys.path.insert(0, "/home/agent3/review2")
from lp import Setup
from lemma_variants import residues
p, n, q = (int(x) for x in sys.argv[1:4]); M = p ** n * q
orders = [("E", a, p ** a) for a in range(1, n + 1)] + [("F", a, p ** a * q) for a in range(0, n + 1)]
S = Setup(M); R = [residues(d, M).astype(np.int32) for _, _, d in orders]
def EF(code):
    return ({orders[i][1] for i in range(len(orders)) if code >> i & 1 and orders[i][0] == "E"},
            {orders[i][1] for i in range(len(orders)) if code >> i & 1 and orders[i][0] == "F"})
hist = {}                                           # pattern code -> {size: count}
bits = M - 1; chunk = 1 << 17
for lo in range(0, 1 << bits, chunk):
    idx = np.arange(lo, min(lo + chunk, 1 << bits), dtype=np.int64)
    X = np.ones((len(idx), M), dtype=np.int32)
    for b in range(bits): X[:, b + 1] = (idx >> b) & 1
    size = X.sum(1); code = np.zeros(len(idx), dtype=np.int64)
    for i, Rd in enumerate(R): code |= (~np.any(X @ Rd.T, axis=1)).astype(np.int64) << i
    key = code * (M + 1) + size
    u, c = np.unique(key, return_counts=True)
    for kk, cc in zip(u, c):
        h = hist.setdefault(int(kk) // (M + 1), {}); s = int(kk) % (M + 1); h[s] = h.get(s, 0) + int(cc)
nL = nT = npd = 0; bad = []
for code, h in hist.items():
    E, F = EF(code); e = len(E); Fp = F - {0}
    for s in h: assert s % (p ** e * (q if 0 in F else 1)) == 0                 # Fact 4
    if 0 not in F and Fp - E:                                                   # Lemma L
        nL += sum(h.values())
        if min(h) < p ** e * (p + q): bad.append(("L", sorted(E), sorted(F), min(h)))
    if 0 in F and h.get(p ** e * q, 0) and any(a < b for a in E - F for b in Fp - E):   # Claim T
        bad.append(("T", sorted(E), sorted(F), h[p ** e * q]))
    if 0 in F: nT += h.get(p ** e * q, 0)
    d = S.Dplus([orders[i][2] for i in range(len(orders)) if code >> i & 1])[0]
    assert min(h) >= d                                                          # Prop. 1(i)
    if d.denominator == 1 and int(d) in h:                                      # pd-tiling sets with this zero set
        npd += h[int(d)]
        ok = (Fp <= E and int(d) == p ** e) if 0 not in F else (E <= F and int(d) == p ** e * q)
        if not ok: bad.append(("theorem", sorted(E), sorted(F), int(d)))
print(f"p={p} n={n} q={q} M={M}: {1 << bits} sets, {len(hist)} zero patterns; Lemma L tested on {nL} sets; "
      f"Claim T on {nT} sets with Phi_q and |A| = p^e q; pd-tiling sets {npd}; FAILURES {len(bad)} {bad[:5]}", flush=True)
