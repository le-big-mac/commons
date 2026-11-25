"""The ring search of the sealed sheet: the least overtone miss found for five or seven families at one weight, on 40 rings and then 80.
usage: python -u searchfree.py five|seven WEIGHT     → s-SET-WEIGHT.json and two lines     (one thread)"""
import sys, json, time, glob
import numpy as np
import libfree as F
L = F.L; name, M = sys.argv[1], float(sys.argv[2]); modes = F.SETS[name]; rng = np.random.default_rng(int(1000 * M) + len(modes)); out = {}; prev = None
nine = {}
for f in glob.glob("../drum/rings2-free-*.json"):
    d = json.load(open(f)); nine[d['weight']] = d['rings']
near = min(nine, key=lambda w: abs(np.log(w / M))); B12 = json.load(open("../drum12/best.json")); w16 = min((1.0, 1.43, 2.0, 2.79, 4.0, 6.0, 12.0), key=lambda w: abs(np.log(w / M)))
for R in (40, 80):
    sk = F.FreeSkin(R, modes); t0 = time.time()
    starts = [("a disc to 0.4", L.disc(sk, M / 0.16, 0.4)), ("a disc to 0.5", L.disc(sk, M / 0.25, 0.5)), ("two discs", L.disc(sk, 0.9 * M / 0.19, 0.436) + L.disc(sk, 0.1 * M / 0.05, 0.224)),
              ("the nine-mode load of that weight", np.array(nine[near][str(R)]['a']) * min(1.0, M / near)), ("the sixteen-mode load of that weight", np.array(B12[f"sixteen|{w16:g}|{R}"]['a']) * min(1.0, M / w16))]
    if prev is not None: starts.append(("the answer with half as many rings", np.repeat(prev, 2)))
    for i in range({40: 16, 80: 8}[R]):
        if i % 2 == 0:
            a0 = np.zeros(R)
            for _ in range(rng.integers(2, 6)): lo = rng.uniform(0, 0.7); a0 += rng.uniform(2, 40) * ((sk.E[:-1] >= lo) & (sk.E[:-1] < lo + rng.uniform(0.02, 0.25)))
        else: a0 = rng.uniform(0, 20, R) * (sk.E[:-1] < rng.uniform(0.3, 0.95))
        starts.append((f"random {i + 1}", a0))
    ends = []; best = None
    for nm, a0 in starts:
        a, f = L.slp(sk, a0, M); ends.append(f)
        if best is None or f < best[0]: best = (f, a, nm)
    for i in range(3):
        a, f = L.slp(sk, best[1] * np.exp(0.3 * rng.standard_normal(R)), M); ends.append(f)
        if f < best[0]: best = (f, a, f"the best, shaken {i + 1}")
    f, a, nm = best; prev = a; ex, pl = F.exact(a, modes); out[R] = dict(miss=f, exact=ex, place=pl, a=a.tolist(), start=nm, ends=ends, used=sk.mass(a))
    print(f"{name:5s} {M:5.2f} skins, {R} rings: least {100 * f:.4f}% ({100 * ex:.4f}% exact) from '{nm}'; {sum(e < f + 2e-5 for e in ends)} of {len(ends)} within 0.002 points, worst {100 * max(ends):.2f}%; used {sk.mass(a):.2f}; the lowest mode's place {pl:.4f}; {time.time() - t0:.0f} s", flush=True)
    json.dump(dict(set=name, weight=M, rings={str(k): v for k, v in out.items()}), open(f"s-{name}-{M:g}.json", "w"))
