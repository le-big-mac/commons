"""Mixed sets of Z_M, M = p^3 q^2, small cases by exhaustion.  (Noon = agent2, 21 November 2026; exploration)
A set A with M a zero meets every coset of K = P + Q in a union of cosets of P or of cosets of Q (Lemma E.5).  If A is
neither a union of cosets of P nor one of cosets of Q it is 'mixed': i >= 1 cosets of P and j >= 1 cosets of Q, lying in
different cosets of K, |A| = i p + j q.  This script lists, for a given size, every mixed set, computes its exact zero set
and reports those whose zero set is one of the patterns left open by classify2.py (category H).
usage: mixed72.py p q        (M = p^3 q^2)"""
import sys, itertools, cmath, math
import numpy as np
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from classify2 import run
p, q = int(sys.argv[1]), int(sys.argv[2]); a, b = 3, 2; M = p**a * q**b
cnt, hard, _ = run(p, a, q, b)
ORD = [(l, m) for l in range(a + 1) for m in range(b + 1) if (l, m) != (0, 0)]
val = lambda o: p**o[0] * q**o[1]
H = {}
for Z, ratio, size, top, t2, orph in hard: H.setdefault(size, set()).add(frozenset(map(tuple, Z)))
print(f"Z_{M}: open patterns by size:", {s: len(v) for s, v in H.items()})
Plines = [tuple(sorted((x + t * (M // p)) % M for t in range(p))) for x in range(M // p)]
Qlines = [tuple(sorted((y + t * (M // q)) % M for t in range(q))) for y in range(M // q)]
Kc = lambda line: line[0] % (M // (p * q))                       # the coset of K containing the line
FT = lambda line: np.array([sum(cmath.exp(2j * cmath.pi * x / val(o)) for x in line) for o in ORD])
TP = np.array([FT(l) for l in Plines]); TQ = np.array([FT(l) for l in Qlines]); KP = np.array([Kc(l) for l in Plines]); KQ = np.array([Kc(l) for l in Qlines])
for size in sorted(H):
    splits = [(i, (size - i * p) // q) for i in range(1, size // p + 1) if (size - i * p) % q == 0 and (size - i * p) // q >= 1]
    if not splits: print(f"  size {size}: not of the form i p + j q with i, j >= 1, so no mixed set: {len(H[size])} patterns excluded"); continue
    hits = 0; nsets = 0; seen_patterns = set()
    for i, j in splits:
        Qc = list(itertools.combinations(range(len(Qlines)), j))
        SQ = np.array([TQ[list(c)].sum(0) for c in Qc]); QK = [set(KQ[list(c)]) for c in Qc]
        for cp in itertools.combinations(range(len(Plines)), i):
            kp = set(KP[list(cp)]); sp = TP[list(cp)].sum(0)
            ok = np.array([not (kp & kq) for kq in QK])
            if not ok.any(): continue
            tot = SQ[ok] + sp; zero = np.abs(tot) < 1e-8; nsets += int(ok.sum())
            for row in np.unique(zero, axis=0):
                Zs = frozenset(o for o, zz in zip(ORD, row) if zz); seen_patterns.add(Zs)
                if Zs in H[size]: hits += 1; print("    MIXED SET WITH AN OPEN PATTERN:", sorted(val(o) for o in Zs))
    print(f"  size {size}: splits (i, j) = {splits}; {nsets:,} mixed sets, {len(seen_patterns)} distinct zero sets among them; "
          f"with one of the {len(H[size])} open patterns: {hits}")
