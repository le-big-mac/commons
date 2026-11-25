"""Referee: for each of the 34 pairs, do the patterns of categories T (and R, U) violate (T2)?  (If every T pattern violates
(T2), the proof of Proposition G shows that no weak tile has a pattern outside L2 and a, hence P(p^3 q^2) for that pair.)"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'orig'))
import exact
a, b = 3, 2
for pq in sys.argv[1:]:
    p, q = map(int, pq.split(','))
    cnt, hard = exact.classify(p, a, q, b); out = {}
    for Z, c in exact.CAT.items():
        if c not in ('T', 'U', 'R', 'H'): continue
        Ep = [l for l in range(1, a + 1) if (l, 0) in Z]; Eq = [m for m in range(1, b + 1) if (0, m) in Z]
        t2 = all((l, m) in Z for l in Ep for m in Eq)
        out[(c, 'T2' if t2 else 'not T2')] = out.get((c, 'T2' if t2 else 'not T2'), 0) + 1
    print(f"({p}, {q}):", dict(sorted(out.items())), flush=True)
