"""What the complete census of Z_36 says, pattern by pattern (agent3 / Yonder).  Exploratory groundwork for p^2 q^2.
For each zero pattern Z that occurs: the smallest set with exactly that pattern, the weak-tiling bound D^w(Z) and the pd bound D+(Z) (my LP,
~/pnq/weak/dw.py), k(Z) = product of the primes of the prime powers in Z, whether (T1)/(T2) could hold, and 'orphans' = composite d in Z none of
whose exact prime-power parts is in Z."""
import sys, itertools, collections
sys.path.insert(0, "/home/agent3/pnq/weak")
from dw import setup
DS = [2, 4, 3, 9, 6, 12, 18, 36]; M = 36
cnt = collections.defaultdict(dict)
for line in open("census36.out"):
    p, n, c = map(int, line.split()); cnt[p][n] = c
total = sum(sum(v.values()) for v in cnt.values()); print("sets in the census:", total, " (2^35 =", 2 ** 35, ")  patterns that occur:", len(cnt), "of 256")
D, bound = setup(M)
def zs(p): return [d for i, d in enumerate(DS) if p >> i & 1]
def parts(d):   # exact prime-power parts of d
    out = []
    for q in (2, 3):
        e = 1
        while d % (e * q) == 0: e *= q
        if e > 1: out.append(e)
    return out
def kk(Z): return (2 ** sum(1 for d in (2, 4) if d in Z)) * (3 ** sum(1 for d in (3, 9) if d in Z))
def T2(Z): return all(d in Z for d in (6, 12, 18, 36) if all(s in Z for s in parts(d)))
def orphans(Z): return [d for d in Z if d in (6, 12, 18, 36) and not any(s in Z for s in parts(d))]
rows = []
for p in sorted(cnt):
    Z = zs(p); ns = sorted(cnt[p]); dw, dp = bound(set(Z), False), bound(set(Z), True)
    rows.append(dict(Z=Z, nmin=ns[0], nmax=ns[-1], dw=dw, dp=dp, k=kk(Z), T2=T2(Z), orph=orphans(Z), at_min=cnt[p][ns[0]], sizes=ns))
weak = [r for r in rows if abs(r["nmin"] - r["dw"]) < 1e-6]
print(f"patterns whose smallest set attains D^w (weak tiles exist): {len(weak)};  of these with |A| = k and (T2): {sum(1 for r in weak if r['nmin'] == r['k'] and r['T2'])};  violating: {[r['Z'] for r in weak if not (r['nmin'] == r['k'] and r['T2'])]}")
print(f"patterns with nmin < D^w (impossible): {[r['Z'] for r in rows if r['nmin'] < r['dw'] - 1e-6]}")
bad = [r for r in rows if not (r["T2"]) or r["orph"]]
print(f"\npatterns that occur and violate (T2) or have an orphan: {len(bad)}.  For each: Z, k, D^w, D+, smallest set, ratio nmin / D^w")
for r in sorted(bad, key=lambda r: r["nmin"] / r["dw"]):
    print(f"   Z = {str(r['Z']):28s} k = {r['k']:2d}  D^w = {r['dw']:7.3f}  D+ = {r['dp']:7.3f}  nmin = {r['nmin']:2d}  ratio {r['nmin'] / r['dw']:5.2f}   orphans {r['orph']}   T2 {'ok' if r['T2'] else 'fails'}")
good = [r for r in rows if r["T2"] and not r["orph"]]
print(f"\npatterns that occur, satisfy (T2) and have no orphan: {len(good)}.  smallest set against k:")
for r in sorted(good, key=lambda r: (r["nmin"] / r["k"], r["k"])):
    print(f"   Z = {str(r['Z']):28s} k = {r['k']:2d}  D^w = {r['dw']:7.3f}  nmin = {r['nmin']:2d}" + ("   = k: tiles" if r["nmin"] == r["k"] else f"   {r['nmin'] / r['k']:.2f} k"))
