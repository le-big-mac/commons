"""Ring loads with air as a spring of fixed strength B: the least largest miss found for all nine modes with the lowest as the note
("tuned"), or the least overtone miss with the lowest mode left free ("free"), at one weight, on 40 rings and then 80.
usage: python -u searchair.py tuned|free B WEIGHT      -> s-KIND-B-WEIGHT.json and two lines      (one thread)"""
import sys, json, time, glob
import numpy as np
import airlib as A
L = A.L; kind, B, M = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]); free = kind == "free"; FIVE = [(1, 1), (2, 1), (0, 2), (3, 1), (1, 2), (4, 1), (2, 2), (0, 3)]
modes = FIVE if free else L.NINE; rng = np.random.default_rng(int(1000 * M) + int(100 * B) + (7 if free else 3)); out = {}; prev = None
def nearest(pattern, key):
    best = None
    for f in glob.glob(pattern):
        d = json.load(open(f)); w = d['weight']
        if best is None or abs(np.log(w / M)) < abs(np.log(best[0] / M)): best = (w, d['rings'])
    return best
def exact(a):
    """the measure by exact matching, and the lowest mode's place with air"""
    e, r = A.load_pieces(a); W = A.with_air(e, r, L.NINE, B); w = [W[q] for q in L.NINE]; T = [L.target(m, n) for m, n in L.NINE]; note = w[1] / 2
    return (max(abs(x / note / t - 1) for x, t in zip(w[2:], T[2:])) if free else max(abs(x / w[0] / t - 1) for x, t in zip(w[1:], T[1:]))), w[0] / note
nine = nearest("../drum/rings2-free-*.json", None); fr = nearest("../drumfree/s-five-*.json", None)
for R in (40, 80):
    sk = A.AirSkin(R, modes, B, free=free); t0 = time.time()
    starts = [("a disc to 0.4", L.disc(sk, M / 0.16, 0.4)), ("a disc to 0.5", L.disc(sk, M / 0.25, 0.5)), ("a disc to 0.3", L.disc(sk, M / 0.09, 0.3)), ("two discs", L.disc(sk, 0.9 * M / 0.19, 0.436) + L.disc(sk, 0.1 * M / 0.05, 0.224)),
              ("the vacuum's tuned load of that weight", np.array(nine[1][str(R)]['a']) * min(1.0, M / nine[0])), ("the vacuum's free load of that weight", np.array(fr[1][str(R)]['a']) * min(1.0, M / fr[0]))]
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
    f, a, nm = best; prev = a; ex, pl = exact(a); out[R] = dict(miss=f, exact=ex, place=pl, a=a.tolist(), start=nm, ends=ends, used=sk.mass(a))
    print(f"{kind:5s} B = {B:g}, {M:5.2f} skins, {R} rings: least {100 * f:.4f}% ({100 * ex:.4f}% exact) from '{nm}'; {sum(e < f + 2e-5 for e in ends)} of {len(ends)} within 0.002 points, worst {100 * max(ends):.2f}%; used {sk.mass(a):.2f}; the lowest mode's place {pl:.4f}; {time.time() - t0:.0f} s", flush=True)
    json.dump(dict(kind=kind, B=B, weight=M, rings={str(k): v for k, v in out.items()}), open(f"s-{kind}-{B:g}-{M:g}.json", "w"))
