"""Z_{p^n q}, the case Phi_q | A: which patterns with 0 in F and E not inside F have D+ >= k = p^e q?  (agent3 / Yonder)
Those are the ones no dual bound excludes; a structural argument is needed for them."""
import sys, itertools
sys.path.insert(0, "/srv/commons/agent2-pdtile/flat")
from lp import Setup
def run(p, n, q):
    M = p ** n * q; S = Setup(M); out = []
    for E in itertools.chain.from_iterable(itertools.combinations(range(1, n + 1), r) for r in range(n + 1)):
        for Fp in itertools.chain.from_iterable(itertools.combinations(range(1, n + 1), r) for r in range(n + 1)):
            if set(E) <= set(Fp): continue                      # T2 holds
            Z = [p ** a for a in E] + [q] + [p ** a * q for a in Fp]
            d = S.Dplus(Z)[0]; k = p ** len(E) * q
            if d >= k: out.append((E, Fp, d, k))
    return out
for p, n, q in [(2, 3, 3), (2, 3, 5), (3, 3, 2), (3, 3, 5), (5, 3, 2), (5, 3, 3), (2, 4, 3), (2, 4, 5), (3, 4, 2), (5, 3, 7), (3, 3, 11)]:
    out = run(p, n, q)
    print(f"p={p} n={n} q={q}: patterns with Phi_q, E not in F, D+ >= k: {len(out)}")
    for E, Fp, d, k in out: print(f"     E={list(E)} F=[0]+{list(Fp)}  E\\F={sorted(set(E) - set(Fp))} F\\E={sorted(set(Fp) - set(E))}  D+={d} k={k}")
