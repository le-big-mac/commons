r"""How many sets actually meet the premise of Lemma 4 (so that its conclusion is tested, not vacuous)?  (agent3 / Yonder)
Premise: Phi_q | A, |A| = p^e q, some b >= 1 in F \ E, and some a in E with a < b.   usage: premise_count.py p n q"""
import sys, numpy as np
sys.path.insert(0, "/home/agent3/review2")
from lemma_variants import residues
p, n, q = (int(x) for x in sys.argv[1:4]); M = p ** n * q
orders = [("E", a, p ** a) for a in range(1, n + 1)] + [("F", a, p ** a * q) for a in range(0, n + 1)]
R = [residues(d, M).astype(np.int32) for _, _, d in orders]
hist = {}; bits = M - 1; chunk = 1 << 17
for lo in range(0, 1 << bits, chunk):
    idx = np.arange(lo, min(lo + chunk, 1 << bits), dtype=np.int64)
    X = np.ones((len(idx), M), dtype=np.int32)
    for b in range(bits): X[:, b + 1] = (idx >> b) & 1
    size = X.sum(1); code = np.zeros(len(idx), dtype=np.int64)
    for i, Rd in enumerate(R): code |= (~np.any(X @ Rd.T, axis=1)).astype(np.int64) << i
    u, c = np.unique(code * (M + 1) + size, return_counts=True)
    for kk, cc in zip(u, c): hist[(int(kk) // (M + 1), int(kk) % (M + 1))] = hist.get((int(kk) // (M + 1), int(kk) % (M + 1)), 0) + int(cc)
prem = concl_ok = 0; pats = {}
for (code, s), c in hist.items():
    E = {orders[i][1] for i in range(len(orders)) if code >> i & 1 and orders[i][0] == "E"}
    F = {orders[i][1] for i in range(len(orders)) if code >> i & 1 and orders[i][0] == "F"}
    if 0 in F and s == p ** len(E) * q:
        pairs = [(a, b) for b in F - E - {0} for a in E if a < b]
        if pairs:
            prem += c; ok = all(a in F for a, b in pairs); concl_ok += c * ok
            pats[(tuple(sorted(E)), tuple(sorted(F)))] = c
print(f"p={p} n={n} q={q} M={M}: sets meeting the premise of Lemma 4: {prem}; conclusion holds for {concl_ok}; patterns: {pats}")
