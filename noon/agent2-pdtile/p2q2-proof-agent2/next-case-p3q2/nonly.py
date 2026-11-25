"""Which patterns of Z_{p^3 q^2} are excluded by non-integrality ONLY?  Order of tests here: L2, a, b, R, T, U, then N, then H.
(exploration for a proof for all p, q; Noon, 21 November 2026)"""
import sys
from fractions import Fraction as Fr
from collections import Counter
from exact import simplex_min
from steplp import ram
def run(p, q, a=3, b=2):
    M = p**a * q**b; cls = [(i, j) for i in range(a + 1) for j in range(b + 1)]; ords = [o for o in cls if o != (0, 0)]
    C = {(o, c): ram(p, a, o[0], c[0]) * ram(q, b, o[1], c[1]) for o in cls for c in cls}
    tot = [C[((0, 0), c)] for c in cls]; e = lambda c0: [1 if c == c0 else 0 for c in cls]
    outp = [tot[k] if c[0] == 0 else 0 for k, c in enumerate(cls)]; outq = [tot[k] if c[1] == 0 else 0 for k, c in enumerate(cls)]
    cnt = Counter(); nonly = []
    for mask in range(1 << len(ords)):
        Z = {o for i, o in enumerate(ords) if mask >> i & 1}
        if (1, 0) not in Z and (0, 1) not in Z: cnt['L2'] += 1; continue
        t2 = all((l, m) in Z for l in range(1, a + 1) for m in range(1, b + 1) if (l, 0) in Z and (0, m) in Z)
        orph = any((l, 0) not in Z and (0, m) not in Z for (l, m) in Z if l and m)
        if t2 and not orph: cnt['a'] += 1; continue
        k = p ** sum(1 for l in range(1, a + 1) if (l, 0) in Z) * q ** sum(1 for m in range(1, b + 1) if (0, m) in Z)
        rows = [e((a, b))] + [[C[(o, c)] for c in cls] for o in ords if o not in Z]; rhs = [1] + [0] * (len(rows) - 1)
        v = simplex_min(rows, rhs, tot)[1]; D = Fr(M) / v
        if D < k: cnt['b'] += 1; continue
        rows2 = rows + [tot]; rhs2 = rhs + [v]
        if simplex_min(rows2, rhs2, outp)[1] == 0 or simplex_min(rows2, rhs2, outq)[1] == 0: cnt['R'] += 1; continue
        xmax = -simplex_min(rows2, rhs2, [-t for t in e((a - 1, b))])[1]; ymax = -simplex_min(rows2, rhs2, [-t for t in e((a, b - 1))])[1]
        top = (a, b) in Z
        if not top and (xmax == 1 or ymax == 1): cnt['T'] += 1; continue
        if top and (xmax > 0 or ymax > 0): cnt['U'] += 1; continue
        if (D / k).denominator != 1: cnt['N only'] += 1; nonly.append((sorted(Z), D / k, k, top)); continue
        cnt['H'] += 1
    return cnt, nonly
for pq in sys.argv[1:]:
    p, q = map(int, pq.split(',')); cnt, nonly = run(p, q)
    print(f"(p, q) = ({p}, {q}): " + ", ".join(f"{k} {cnt[k]}" for k in ('L2', 'a', 'b', 'R', 'T', 'U', 'N only', 'H')), flush=True)
    for Z, r, k, top in nonly[:40]: print(f"     N only: D/k = {r}  k = {k}  {'M zero' if top else 'M not zero'}  zeros {Z}")
