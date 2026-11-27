# t2_census.py -- complete census of the sets (kind = set) or multisets (kind = multi) containing 0 on Z_G, up to T
# elements: for every size t and every set D of divisors > 1 of G, the number of (multi)sets containing 0, of t elements,
# whose mask is divisible by Phi_d (d | G, d > 1) exactly for d in D.  Every (multi)set has a translate containing 0 with
# the same divisors (checked in t0_selftest.py), so a pattern that occurs at a size occurs here.
# usage: python t2_census.py kind G T [lo hi]      (lo, hi: range of the second element, to split a long run)
# Output: census/<kind>_<G>_T<T>[_lo_hi].json  with {"G":..,"T":..,"kind":..,"count":{t:{"d1,d2,..":number}}}
import sys, json, time, os
from math import comb
from core import *

kind = sys.argv[1]
G = int(sys.argv[2])
T = int(sys.argv[3])
rep = (kind == 'multi')
lo, hi = 0, G
tag = ''
if len(sys.argv) > 4:
    lo, hi = int(sys.argv[4]), int(sys.argv[5])
    tag = '_%d_%d' % (lo, hi)
if rep:
    est = sum(comb(G + t - 2, t - 1) for t in range(1, T + 1))
else:
    est = sum(comb(G - 1, t - 1) for t in range(1, T + 1))
print("census %s G=%d T=%d: %d (multi)sets containing 0 (whole range)" % (kind, G, T, est), flush=True)
grp = Group(G)
t0 = time.time()
cnt = census(grp, T, rep, lo, hi)
el = time.time() - t0
pb = patterns_by_size(grp, cnt)
tot = int(cnt.sum())
if lo == 0 and hi == G:
    assert tot == est, (tot, est)
out = {"G": G, "T": T, "kind": kind, "lo": lo, "hi": hi, "visited": tot, "seconds": round(el, 1),
       "count": {str(t): {",".join(str(d) for d in sorted(D)): c for D, c in sorted(pb[t].items(), key=lambda kv: sorted(kv[0]))}
                 for t in pb}}
os.makedirs('census', exist_ok=True)
fn = 'census/%s_%d_T%d%s.json' % (kind, G, T, tag)
json.dump(out, open(fn, 'w'))
print("visited %d in %.1f s; patterns per size: %s; wrote %s" % (tot, el, {t: len(pb[t]) for t in pb}, fn), flush=True)
