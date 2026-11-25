"""Z_{p^2 q}: brute-force check of every step of the proposed proof that pd-tiling sets satisfy (T1) and (T2).
(agent3 / Yonder.)  All subsets of Z_M containing 0, M = 12, 18, 20 (and 28 with 'big').  Exact integer arithmetic for the
zero sets (residues of X^i mod Phi_d); exact D+ from agent2's lp.py.  For each zero pattern that occurs: how many sets,
the smallest set size, D+ of the pattern, and whether any set pd-tiles (|A| = D+(Z_A))."""
import sys, itertools, numpy as np
from fractions import Fraction as Fr
sys.path.insert(0, "/srv/commons/agent2-pdtile/flat"); sys.path.insert(0, "/home/agent3/review2")
from lp import Setup
from lemma_variants import residues
NAMES = ["p", "p2", "q", "pq", "p2q"]
def run(p, q):
    M = p * p * q; o = dict(zip(NAMES, [p, p * p, q, p * q, p * p * q])); S = Setup(M)
    D = {Z: S.Dplus([o[z] for z in Z])[0] for r in range(6) for Z in itertools.combinations(NAMES, r)}
    R = {z: residues(o[z], M) for z in NAMES}                       # phi(d) x M integer matrices
    k = lambda Z: (p if "p" in Z else 1) * (p if "p2" in Z else 1) * (q if "q" in Z else 1)
    U = lambda Z: set(z for z in NAMES if (("p" in Z and z in ("p", "pq")) or ("p2" in Z and z in ("p2", "p2q")) or ("q" in Z and z in ("q", "pq", "p2q"))))
    closed = lambda Z: (not ("p" in Z and "q" in Z) or "pq" in Z) and (not ("p2" in Z and "q" in Z) or "p2q" in Z)
    stats = {}                                                        # pattern -> [count, min size, #pd-tiling, #pd-tiling violating]
    bits = M - 1; chunk = 1 << 16
    for lo in range(0, 1 << bits, chunk):
        idx = np.arange(lo, min(lo + chunk, 1 << bits), dtype=np.int64)
        X = np.ones((len(idx), M), dtype=np.int64)
        for b in range(bits): X[:, b + 1] = (idx >> b) & 1
        n = X.sum(1)
        zero = {z: ~np.any(X @ R[z].T, axis=1) for z in NAMES}
        code = sum(zero[z].astype(np.int64) << i for i, z in enumerate(NAMES))
        for c in np.unique(code):
            Z = tuple(z for i, z in enumerate(NAMES) if c >> i & 1); sel = code == c; ns = n[sel]
            pd = int((ns == int(D[Z])).sum()) if D[Z].denominator == 1 else 0
            viol = pd if (int(D[Z]) != k(Z) or not closed(Z)) else 0
            st = stats.setdefault(Z, [0, 10 ** 9, 0, 0]); st[0] += int(sel.sum()); st[1] = min(st[1], int(ns.min())); st[2] += pd; st[3] += viol
            assert (ns % k(Z) == 0).all() and (ns >= D[Z]).all()      # Prop. 1(i), (iii)
    print(f"p={p} q={q} M={M}: {1 << bits} sets containing 0")
    print("   pattern               sets   min|A|   D+      k   Z in U(P)  closed  pd-tiling sets  of which violating T1/T2")
    for Z in sorted(stats, key=lambda Z: (len(Z), Z)):
        c, mn, pd, viol = stats[Z]
        print(f"   {{{','.join(Z)}}}".ljust(22) + f"{c:8d} {mn:7d}   {str(D[Z]):>5} {k(Z):5d}   {str(set(Z) <= U(Z)):9s} {str(closed(Z)):6s} {pd:10d} {viol:14d}")
    # the inequalities the proof uses
    mn_, mx_ = min(p, q), max(p, q)
    assert D[("p2", "pq", "p2q")] <= p * mn_ and D[("p", "pq", "p2q")] <= p * mn_ and D[("pq",)] <= mn_ and D[("p2q",)] <= mn_
    assert D[("pq", "p2q")] <= min(q, p * p) and D[("p", "q")] <= mx_ and D[("p2", "q", "pq")] <= mx_
    for r in range(4):
        for Sset in itertools.combinations(("p", "p2", "q"), r): assert D[tuple(z for z in NAMES if z in U(Sset))] == k(Sset)
    print("   total pd-tiling sets:", sum(s[2] for s in stats.values()), "; violating:", sum(s[3] for s in stats.values()), flush=True)
for p, q in [(2, 3), (3, 2), (2, 5)] + ([(2, 7)] if "big" in sys.argv else []): run(p, q)
