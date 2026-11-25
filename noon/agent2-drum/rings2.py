"""The weight table again after the referee: the sealed measure, sequential linear programming, many starts, and 40, 80 (and, if asked,
160) rings.   usage: python -u rings2.py free|piled WEIGHT [160]     → rings2-KIND-WEIGHT.json and one block of lines     (unregistered)"""
import sys, json, time
import numpy as np
import ringlib as L
kind, M = sys.argv[1], float(sys.argv[2]); mono = kind == "piled"; top = 160 if len(sys.argv) > 3 else 80; rng = np.random.default_rng(int(1000 * M) + (7 if mono else 0)); out = {}; prev = None
walk = None
for f in (f"chain-{kind}-down.json", f"chain-{kind}-up.json"):
    for r in json.load(open(f)):
        if abs(r['weight'] - M) < 1e-9 and (walk is None or r['miss'] < walk['miss']): walk = r
for R in (40, 80, 160):
    if R > top: break
    sk = L.Skin(R); t0 = time.time(); starts = [("one disc", L.disc(sk, M / 0.16, 0.4)), ("two discs", L.disc(sk, 0.9 * M / 0.19, 0.436) + L.disc(sk, 0.1 * M / 0.05, 0.224))]
    if walk is not None: starts.append(("the walks' answer", L.split(np.array(walk['a']), R // 40)))
    if prev is not None: starts.append(("the answer with half as many rings", L.split(prev)))
    for i in range({40: 16, 80: 8, 160: 3}[R]):
        if i % 2 == 0:                                     # a few random rings
            a0 = np.zeros(R)
            for _ in range(rng.integers(2, 5)): lo = rng.uniform(0, 0.5); a0 += rng.uniform(2, 60) * ((sk.E[:-1] >= lo) & (sk.E[:-1] < lo + rng.uniform(0.02, 0.2)))
        else: a0 = rng.uniform(0, 30, R) * (sk.E[:-1] < rng.uniform(0.3, 0.8))          # rough loads out to a random radius
        starts.append((f"random {i + 1}", a0))
    ends = []; best = None
    for name, a0 in starts:
        a, f = L.slp(sk, a0, M, monotone=mono); ends.append(f)
        if best is None or f < best[0]: best = (f, a, name)
    # shake the best three times and search again
    for i in range(3):
        a0 = best[1] * np.exp(0.3 * rng.standard_normal(R)); a, f = L.slp(sk, a0, M, monotone=mono); ends.append(f)
        if f < best[0]: best = (f, a, f"the best, shaken {i + 1}")
    f, a, name = best; prev = a; ex = L.exact_miss(a); hv = int(np.argmax(a)); loaded = np.nonzero(a > 1e-6)[0]
    out[R] = dict(miss=f, exact=ex, a=a.tolist(), start=name, ends=ends)
    print(f"{kind:5s} {M:5.2f} skins, {R:3d} rings: least {100 * f:.4f}% ({100 * ex:.4f}% by exact matching) from '{name}'; {sum(e < f + 2e-5 for e in ends)} of {len(ends)} searches ended within 0.002 points of it, the worst at {100 * max(ends):.3f}%; used {sk.mass(a):.2f}; heaviest ring +{a[hv]:.0f} from {sk.E[hv]:.4f} to {sk.E[hv + 1]:.4f}; loaded out to {sk.E[loaded.max() + 1]:.4f}; {time.time() - t0:.0f} s", flush=True)
    json.dump(dict(kind=kind, weight=M, rings={str(k): v for k, v in out.items()}), open(f"rings2-{kind}-{M:g}.json", "w"))
