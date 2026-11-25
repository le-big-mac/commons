"""Z_{p^2 q}: for each pattern Z (set of orders among p, p2, q, pq, p2q), D+(Z) against k(Z), over many prime pairs.
T1-dangerous: D+(Z) >= 2 k(Z)  (a set with exactly these zeros and D+ elements would violate T1)
T2-dangerous: Z not T2-closed and D+(Z) >= k(Z)."""
import sys, itertools
from fractions import Fraction as Fr
sys.path.insert(0, "/srv/commons/agent2-pdtile/flat")
from lp import Setup
NAMES = ["p", "p2", "q", "pq", "p2q"]
def orders(p, q): return dict(zip(NAMES, [p, p * p, q, p * q, p * p * q]))
pairs = [(p, q) for p in (2, 3, 5, 7, 11, 13) for q in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 53, 127) if p != q]
table = {}
for p, q in pairs:
    S = Setup(p * p * q); o = orders(p, q)
    for r in range(6):
        for Z in itertools.combinations(NAMES, r):
            table[(Z, p, q)] = S.Dplus([o[z] for z in Z])[0]
import pickle; pickle.dump(table, open("table.pkl", "wb"))
def k(Z, p, q): return (p if "p" in Z else 1) * (p if "p2" in Z else 1) * (q if "q" in Z else 1)
def closed(Z): return (not ("p" in Z and "q" in Z) or "pq" in Z) and (not ("p2" in Z and "q" in Z) or "p2q" in Z)
for r in range(6):
    for Z in itertools.combinations(NAMES, r):
        t1 = [(p, q, table[(Z, p, q)]) for p, q in pairs if table[(Z, p, q)] >= 2 * k(Z, p, q)]
        t1int = [(p, q, v) for p, q, v in t1 if v.denominator == 1 and v % k(Z, p, q) == 0]
        t2 = [] if closed(Z) else [(p, q, table[(Z, p, q)]) for p, q in pairs if table[(Z, p, q)] >= k(Z, p, q)]
        t2int = [(p, q, v) for p, q, v in t2 if v.denominator == 1 and v % k(Z, p, q) == 0]
        eq = sum(table[(Z, p, q)] == k(Z, p, q) for p, q in pairs)
        print(f"{{{','.join(Z)}}}: D+=k for {eq}/{len(pairs)}; T1-dangerous {len(t1)} (integer multiple of k: {len(t1int)}) {[(p, q, str(v)) for p, q, v in t1int[:6]]}"
              + ("" if closed(Z) else f"; NOT T2-closed, D+>=k for {len(t2)} (integer multiple: {len(t2int)}) {[(p, q, str(v)) for p, q, v in t2int[:6]]}"), flush=True)
