"""Referee: end-to-end test on the line unions of size p^2 q listed (through signatures) by mixedsig.py.
A set A is a weak tile iff |A| = D^w(Z(A))  (Proposition 4 of the p2q2 note).  For every zero set Z realised by a line
union of size n = p^2 q:  compute D^w(Z) with the referee's certified LP; if D^w(Z) = n the sets are weak tiles, and then
Proposition G says they tile; check that the pattern satisfies (T1) and (T2) -- and report its category.
usage: mixedweak.py p q"""
import sys, os, pickle
from fractions import Fraction as Fr
from collections import Counter
from reflp import solve_lp
import refclassify as rc
p, q = int(sys.argv[1]), int(sys.argv[2]); a, b = 3, 2; M = p**a * q**b
d = pickle.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"mixedsig_{p}_{q}.pkl"), 'rb'))
H, n = d['hist'], d['n']
CAT, SIZE, cnt, _ = rc.classify(p, q)
cls = [(i, j) for i in range(a + 1) for j in range(b + 1)]; ords = [o for o in cls if o != (0, 0)]
C = {(o, c): rc.csum(p, a, o[0], c[0]) * rc.csum(q, b, o[1], c[1]) for o in cls for c in cls}
size = [C[((0, 0), c)] for c in cls]
def Dw(Z):
    rows = [[1 if c == (a, b) else 0 for c in cls]] + [[C[(o, c)] for c in cls] for o in ords if o not in Z]
    st, v, x, y = solve_lp(rows, [1] + [0] * (len(rows) - 1), size); assert st == 'optimal'
    return Fr(M) / v
weak = Counter(); nweak = 0; bad = []
for Z, mult in sorted(H.items(), key=lambda kv: -kv[1]):
    D = Dw(Z)
    if D > n: bad.append(("IMPOSSIBLE: a set of size n with D^w(Z(A)) > n", sorted(Z), D)); continue      # D^w(Z(A)) <= |A| for every set, with equality iff A is a weak tile
    if D != n: continue
    Ep = [l for l in range(1, a + 1) if (l, 0) in Z]; Eq = [m for m in range(1, b + 1) if (0, m) in Z]
    k = p ** len(Ep) * q ** len(Eq)
    t1 = (k == n); t2 = all((l, m) in Z for l in Ep for m in Eq)
    orphan = any(l >= 1 and m >= 1 and l not in Ep and m not in Eq for (l, m) in Z)
    weak[(CAT[Z], 'T1' if t1 else 'not T1', 'T2' if t2 else 'not T2', 'orphan' if orphan else 'no orphan')] += mult; nweak += mult
    if not (t1 and t2): bad.append(("WEAK TILE WITHOUT (T1),(T2)", sorted(Z), mult))
    if CAT[Z] not in ('L2', 'a'): bad.append(("weak tile with a pattern outside L2, a", CAT[Z], sorted(Z), mult))
print(f"Z_{M} (p = {p}, q = {q}): {sum(H.values()):,} line unions of size {n} with i, j >= 1; {len(H)} zero sets; weak tiles among them (|A| = D^w(Z(A))): {nweak:,}")
for k_, v_ in weak.items(): print("    ", k_, f"{v_:,}")
print("   problems:", bad if bad else "none")
