"""Checks made after the sealed sheet was scored; none was registered. All on the table's own loads (best.json).
usage: python -u after.py SECTION OUT.json
I strays; T inexact making; R 160 rings; B the base left free as well; G what the two-disc and piled loads are"""
import sys, json, math, time
import numpy as np
from scipy.linalg import eigh_tridiagonal
import libfree as F
L = F.L; SEC = sys.argv[1]; OUT = sys.argv[2]; A = {}; BEST = json.load(open("best.json")); B = lambda key: np.array(BEST[key]['a'])
def spectrum(a, mmax=30, nmax=10, per=50):
    R = len(a); N = R * per; h = 1.0 / N; r = (np.arange(N) + 0.5) * h; re = np.arange(N + 1) * h; rho = 1 + np.repeat(a, per); sc = np.sqrt(r * rho); out = []
    for m in range(mmax + 1):
        d = (re[:-1] + re[1:]) / (h * h) + m * m / r; d[-1] += re[-1] / (h * h); w = np.sqrt(eigh_tridiagonal(d / sc ** 2, -re[1:-1] / (h * h) / (sc[:-1] * sc[1:]), select='i', select_range=(0, nmax - 1))[0]); out += [(w[j], m, j + 1) for j in range(nmax)]
    base = next(x for x, m, n in out if (m, n) == (1, 1)) / 2; return sorted((x / base, m, n) for x, m, n in out)
if SEC == 'I':
    print("I. Strays: modes that are neither the lowest nor of the set, below the top harmonic plus a half (in units of the base; m up to 30, n up to 10)"); A['strays'] = []
    for key, top in (("five|1.43|40", 5), ("five|4|40", 5), ("five|4|80", 5), ("five|12|40", 5), ("seven|4|40", 7), ("seven|4|80", 7), ("seven|12|40", 7)):
        name = key.split("|")[0]; own = set(F.SETS[name]) | {(0, 1)}; sp = spectrum(B(key)); out = [(float(x), m, n) for x, m, n in sp if x < top + 0.5 and (m, n) not in own]; A['strays'].append(dict(key=key, strays=out))
        print(f"   {key}: " + (", ".join(f"({m},{n}) at {x:.3f}" for x, m, n in out) if out else "none"), flush=True)
if SEC == 'T':
    print("T. Inexact making (400 draws each): every ring's load off by a random share; the whole load moved by one ring"); rng = np.random.default_rng(23); A['tol'] = []
    for key in ("five|1.43|40", "five|4|40", "seven|4|40"):
        name = key.split("|")[0]; a = B(key); sk = F.FreeSkin(40, F.SETS[name]); row = dict(key=key, base=sk.miss(a))
        for eps in (0.01, 0.03): v = np.array([sk.miss(a * (1 + eps * rng.standard_normal(40))) for _ in range(400)]); row[str(eps)] = (float(np.median(v)), float(v.max()))
        row['out'] = sk.miss(np.concatenate([[a[0]], a[:-1]])); row['in'] = sk.miss(np.concatenate([a[1:], [0.0]])); A['tol'].append(row)
        print(f"   {key}: as found {100 * row['base']:.3f}%; each ring off by 1%: median {100 * row['0.01'][0]:.2f}%, worst {100 * row['0.01'][1]:.2f}%; by 3%: median {100 * row['0.03'][0]:.2f}%; moved one ring outward {100 * row['out']:.1f}%, inward {100 * row['in']:.1f}%", flush=True)
    two = json.load(open("shape-two-five-1.43.json")); N = 800; sk = F.FreeSkin(N, F.FIVE, per=1)
    def load(ko, ki, lo, li): e = sk.E; return sum(l * np.clip((np.minimum(k, e[1:]) ** 2 - e[:-1] ** 2) / sk.A, 0, 1) for l, k in ((lo, ko), (li, ki)))
    ko, ki = two['radii']; lo = two['share'] * two['used'] / ko ** 2; li = (1 - two['share']) * two['used'] / ki ** 2; base = sk.miss(load(ko, ki, lo, li)); v = np.array([sk.miss(load(ko * (1 + 0.01 * rng.standard_normal()), ki * (1 + 0.01 * rng.standard_normal()), lo * (1 + 0.01 * rng.standard_normal()), li * (1 + 0.01 * rng.standard_normal()))) for _ in range(400)])
    A['two'] = dict(base=base, median=float(np.median(v)), worst=float(v.max())); print(f"   two discs, 1.43 skins: as found {100 * base:.2f}%; both radii and both loads off by 1%: median {100 * np.median(v):.2f}%, worst {100 * v.max():.2f}%")
if SEC == 'R':
    print("R. 160 rings, from the 80-ring load split in two (four searches each)"); rng = np.random.default_rng(160); A['fine'] = []
    for key in ("five|1.43|80", "five|4|80", "seven|4|80"):
        name, M = key.split("|")[0], float(key.split("|")[1]); sk = F.FreeSkin(160, F.SETS[name]); start = np.repeat(B(key), 2); f0 = sk.miss(start); t0 = time.time()
        ends = [L.slp(sk, start, M)] + [L.slp(sk, start * np.exp(0.2 * rng.standard_normal(160)), M) for _ in range(3)]; a, f = min(ends, key=lambda z: z[1]); ex, pl = F.exact(a, F.SETS[name]); A['fine'].append(dict(key=key, start=f0, miss=f, exact=ex, place=pl, moved=float(np.abs(a - start).max()), ends=[e[1] for e in ends]))
        print(f"   {key}: split in two {100 * f0:.4f}%; after the search {100 * f:.4f}% ({100 * ex:.4f}% exact); the four ended at " + ", ".join(f"{100 * e[1]:.4f}%" for e in ends) + f"; largest change in a ring's load {np.abs(a - start).max():.1f}; place {pl:.4f}; {time.time() - t0:.0f} s", flush=True)
if SEC == 'B':
    print("B. The base left free as well: the eight overtones (the second mode among them) against whole multiples of the best-fitting base; the loads are not searched again"); A['freebase'] = []
    def fitted(r, T):
        best = min(((max(abs(x / (c * t) - 1) for x, t in zip(r, T)), c) for c in np.arange(0.97, 1.0301, 0.00005)), key=lambda z: z[0]); return best
    D = json.load(open("disc.json")); cases = [("the best even disc", D['five']['ratios'], D['five']['miss'])]
    for key in ("five|1.43|40", "five|4|40"):
        rr = L.exact_ratios(B(key), F.FIVE); cases.append((key, (2 * rr).tolist(), BEST[key]['exact']))
    T = [L.target(m, n) for m, n in F.FIVE]
    for name, r, sealed in cases:
        t, c = fitted(r, T); A['freebase'].append(dict(name=name, sealed=sealed, free=float(t), base=float(c))); print(f"   {name}: {100 * sealed:.3f}% with the base at half the second mode; {100 * t:.3f}% with the best-fitting base, which is {c:.4f} of that half")
if SEC == 'G':
    print("G. What the layered loads are")
    for M in ("1.43", "4.0"):
        two = json.load(open(f"shape-two-five-{M}.json")); ko, ki = two['radii']; lo = two['share'] * two['used'] / ko ** 2; li = (1 - two['share']) * two['used'] / ki ** 2
        A[f"two{M}"] = dict(ko=ko, ki=ki, outer=1 + lo, inner=1 + lo + li, used=two['used'], miss=two['miss'], place=two['place']); print(f"   two discs, up to {float(M):g} skins: {1 + lo:.2f} times the skin from {ki:.3f} to {ko:.3f} of the radius and {1 + lo + li:.2f} times inside {ki:.3f}; {two['used']:.2f} skins; overtone miss {100 * two['miss']:.2f}%; the lowest mode's place {two['place']:.3f}")
    for M in ("1.43", "4.0"):
        p = json.load(open(f"shape-piled-five-{M}.json"))['rings']['40']; a = np.array(p['a']); steps = [(j / 40, 1 + a[j]) for j in range(40) if j == 0 or abs(a[j] - a[j - 1]) > 0.02 * a.max()]; A[f"piled{M}"] = steps
        print(f"   piled discs on 40 rings, up to {float(M):g} skins: mass per area, in skins, from each radius outward: " + "; ".join(f"{r:.3f}: {s:.1f}" for r, s in steps))
json.dump(A, open(OUT, "w"))
