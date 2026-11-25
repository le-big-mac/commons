"""A second pass over the leave-one-out controls, because some had few searches in agreement: each case is searched again from the
answers of all the other cases of its weight and from four shakes of its own best.  The better of the two passes is kept.
usage: python -u leaveout3.py 1|2 WEIGHT OUT.json      (1: leaveout.py's cases, the lowest mode as the note; 2: leaveout2.py's)"""
import sys, json, time
import numpy as np
import libfree as F
L = F.L; kind, M = sys.argv[1], float(sys.argv[2]); rng = np.random.default_rng(900 + int(10 * M) + int(kind)); out = {}
old = json.load(open(f"leaveout{'' if kind == '1' else '2'}-{M:g}.json"))
def exact2(a, modes):
    r = L.exact_ratios(np.asarray(a, float), list(modes)); T = np.array([L.target(m, n) for m, n in modes]); return float(np.abs(2 * r[1:] / T[1:] - 1).max())
for name, o in old.items():
    if kind == '1':
        drop = tuple(int(x) for x in name.split(",")); modes = [mn for mn in L.NINE if mn != drop]; sk = L.Skin(40, modes); ex = lambda a: L.exact_miss(a, modes)
    else:
        drop = None if name == "nothing" else tuple(int(x) for x in name.strip("()").split(",")); modes = [(1, 1), (0, 1)] + [mn for mn in F.FIVE[1:] if mn != drop]; sk = F.FreeSkin(40, modes); ex = lambda a: exact2(a, modes)
    t0 = time.time(); mine = np.array(o['a']); starts = [np.array(v['a']) for k, v in old.items() if k != name] + [mine * np.exp(0.3 * rng.standard_normal(40)) for _ in range(4)]
    ends = [L.slp(sk, a0, M) for a0 in starts]; a, f = min(ends, key=lambda z: z[1]); better = f < o['miss'] - 1e-7
    if not better: a, f = mine, o['miss']
    out[name] = dict(miss=float(f), exact=ex(a), first=o['miss'], lowered=float(o['miss'] - f), agree=sum(e[1] < f + 2e-5 for e in ends), n=len(ends), a=np.asarray(a).tolist())
    print(f"{M:g} skins, {name} left out: first pass {100 * o['miss']:.4f}%; second pass {100 * min(e[1] for e in ends):.4f}% at best; kept {100 * f:.4f}% ({100 * out[name]['exact']:.4f}% exact); {out[name]['agree']} of {len(ends)} second-pass searches within 0.002 points of the kept one; {time.time() - t0:.0f} s", flush=True)
    json.dump(out, open(sys.argv[3], "w"))
