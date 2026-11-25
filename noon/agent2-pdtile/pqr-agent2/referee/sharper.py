"""Pattern-level statements read off the exhaustive histograms (M=30: subsets containing 0; M=42: all subsets).
(I7) check, and the referee's sharper statements G1-G4 (which explain why several bullets of Section 5 have an
empty premise for sets)."""
import sys, itertools
sys.path.insert(0, '/tmp/agent2_referee3')
from dplus import dplus, describe
PB = {frozenset((0, 1)): 3, frozenset((0, 2)): 4, frozenset((1, 2)): 5}
def EPt(mask):
    return ({w for w in range(3) if mask >> w & 1}, {pr for pr, b in PB.items() if mask >> b & 1}, mask >> 6 & 1)
for p, fn in (((2, 3, 5), 'm30_hist.txt'), ((2, 3, 7), 'm42_hist.txt')):
    M = p[0]*p[1]*p[2]
    rows = []
    for line in open(fn):
        if line[0] == '#': continue
        f = line.split(); rows.append((int(f[0]), int(f[1]), int(f[2]), int(f[3]) if len(f) > 3 else None))
    D = {m: dplus(p, m) for m in range(128)}
    def T1T2(m, n):
        E, P, t = EPt(m); k = 1
        for w in E: k *= p[w]
        return n == k and all(frozenset((a, b)) in P for a in E for b in E if a < b) and (len(E) < 3 or t)
    c = sum(cnt for m, n, cnt, tl in rows if T1T2(m, n)); c2 = sum(cnt for m, n, cnt, tl in rows if T1T2(m, n) and D[m] == n)
    c3 = sum(cnt for m, n, cnt, tl in rows if D[m] == n)
    print(f"M={M}: sets with (T1),(T2): {c}; of which |A| = D+(Z_A): {c2}; sets with |A| = D+(Z_A): {c3}" +
          (f"; of the (T1),(T2) sets, tiling by brute force: {sum(tl for m, n, cnt, tl in rows if T1T2(m, n))}" if rows[0][3] is not None else ""))
    def stat(name, prem, concl):
        a = sum(cnt for m, n, cnt, tl in rows if prem(m, n)); b = sum(cnt for m, n, cnt, tl in rows if prem(m, n) and not concl(m, n))
        print(f"   {name:86s} premise sets={a:12d} violations={b}")
    for x, y, z in itertools.permutations(range(3)):
        tag = f"[x,y,z={p[x]},{p[y]},{p[z]}]"
        if x < y:
            stat(f"G1 {tag}: x,y in E, t=1, A != Z_M => {{x,y}} in P", lambda m, n: {x, y} <= EPt(m)[0] and EPt(m)[2] and n < M, lambda m, n: frozenset((x, y)) in EPt(m)[1])
        if y < z:
            stat(f"G2 {tag}: x in E, {{y,z}} in P, t=1 => y in E or z in E", lambda m, n: x in EPt(m)[0] and frozenset((y, z)) in EPt(m)[1] and EPt(m)[2], lambda m, n: y in EPt(m)[0] or z in EPt(m)[0])
            stat(f"G4 {tag}: {{x,y}},{{x,z}} in P, x not in E => y,z in E", lambda m, n: x not in EPt(m)[0] and frozenset((x, y)) in EPt(m)[1] and frozenset((x, z)) in EPt(m)[1], lambda m, n: y in EPt(m)[0] and z in EPt(m)[0])
        stat(f"G3 {tag}: x in E, y not in E, {{x,y}},{{y,z}} in P => z in E", lambda m, n: x in EPt(m)[0] and y not in EPt(m)[0] and frozenset((x, y)) in EPt(m)[1] and frozenset((y, z)) in EPt(m)[1], lambda m, n: z in EPt(m)[0])
