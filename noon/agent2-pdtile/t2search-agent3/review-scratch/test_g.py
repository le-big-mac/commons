"""(g) Z_M exhaustive: every candidate orbit representative from enum36 (all sets with A - A != Z_M that pass the support test),
decided directly (full LP, exact certificates), then (T1)/(T2) checked on every weak tile.
usage: test_g.py p a q b candfile [nproc]"""
import sys, time, math
from multiprocessing import Pool
from common import *
import wt
p, a, q, b = (int(v) for v in sys.argv[1:5]); M = p ** a * q ** b
cands = [int(l, 16) for l in open(sys.argv[5]) if l.strip()]
nproc = int(sys.argv[6]) if len(sys.argv) > 6 else 4
def work(mask):
    A = [x for x in range(M) if mask >> x & 1]
    verdict, cert, feas_float = wt.certified(A, M)
    Zx = zeros_exact(A, M); Zn = zeros_numeric(A, M); assert Zx == Zn, (A, Zx, Zn)
    cl = wt.class_lp(A, M, Zx)
    return mask, len(A), verdict, feas_float, sorted(Zx), cl
if __name__ == "__main__":
    t0 = time.time()
    with Pool(nproc) as pool: res = pool.map(work, cands, chunksize=50)
    und = [r for r in res if r[2] == "?"]
    mism_float = [r for r in res if r[2] != "?" and (r[2] == "yes") != r[3]]
    mism_class = [r for r in res if r[2] != "?" and (r[2] == "yes") != r[5]]
    tiles = [r for r in res if r[2] == "yes"]
    print(f"Z_{M}: {len(res)} orbit representatives decided in {time.time() - t0:.0f} s: {len(tiles)} weak tiles (exact rational complement verified), "
          f"{sum(1 for r in res if r[2] == 'no')} not (exact Farkas certificate verified), {len(und)} without an exact certificate")
    print(f"   float full-LP verdict differs from the certified one: {len(mism_float)};  class-constant reduction (a) differs from the certified one: {len(mism_class)}")
    for r in und[:20]: print("   UNCERTIFIED:", [x for x in range(M) if r[0] >> x & 1], "float verdict", r[3], "class verdict", r[5])
    bysize = {}
    badT1 = []; badT2 = []
    pats = {}
    for mask, k, verdict, ff, Z, cl in tiles:
        bysize[k] = bysize.get(k, 0) + 1; Zs = set(Z)
        pats.setdefault((k, tuple(Z)), 0); pats[(k, tuple(Z))] += 1
        if not T1_holds(Zs, k, p, a, q, b): badT1.append((mask, k, Z))
        v = T2_violations(Zs, p, a, q, b)
        if v: badT2.append((mask, k, Z, v))
    print("   weak-tile orbits by size:", dict(sorted(bysize.items())), " (plus the trivial ones: a single point, and Z_M itself)")
    print(f"   distinct (size, exact zero set) among weak tiles: {len(pats)}")
    for (k, Z), n in sorted(pats.items()): print(f"      size {k:2d} zeros {list(Z)}: {n} orbits")
    print(f"   (T1) violated by {len(badT1)} weak-tile orbits, (T2) violated by {len(badT2)} weak-tile orbits")
    for x in badT1[:10]: print("   T1 VIOLATION", [y for y in range(M) if x[0] >> y & 1], x[1:])
    for x in badT2[:10]: print("   T2 VIOLATION", [y for y in range(M) if x[0] >> y & 1], x[1:])
    # how many NON-weak-tiles violate T1 / T2 (shows the properties are not vacuous on this population)
    non = [r for r in res if r[2] == "no"]
    print(f"   for comparison, among the {len(non)} candidates that are not weak tiles: {sum(1 for r in non if not T1_holds(set(r[4]), r[1], p, a, q, b))} violate (T1), "
          f"{sum(1 for r in non if T2_violations(set(r[4]), p, a, q, b))} violate (T2)")
    import pickle; pickle.dump(res, open(f"/tmp/rev_t2/res{M}.pkl", "wb"))
