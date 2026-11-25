"""The control of leaveout.py in this study's own units: the note is half the second mode's frequency throughout; the lowest mode is
kept (aimed at 1 times the note) and one of the seven overtones is left out instead, so that seven misses are made least, as with
the lowest mode free.  Also with nothing left out (eight misses).  40 rings.     usage: python -u leaveout2.py WEIGHT OUT.json"""
import sys, json, time
import numpy as np
import libfree as F
L = F.L; M = float(sys.argv[1]); rng = np.random.default_rng(77 + int(10 * M)); out = {}
nine = np.array(json.load(open(f"../drum/rings2-free-{M:g}.json"))['rings']['40']['a']); free = np.array(json.load(open(f"s-five-{M:g}.json"))['rings']['40']['a'])
def exact(a, modes):
    r = L.exact_ratios(np.asarray(a, float), list(modes)); T = np.array([L.target(m, n) for m, n in modes]); return float(np.abs(2 * r[1:] / T[1:] - 1).max())
for drop in [None] + F.FIVE[1:]:
    modes = [(1, 1), (0, 1)] + [mn for mn in F.FIVE[1:] if mn != drop]; sk = F.FreeSkin(40, modes); t0 = time.time()
    starts = [nine, free, L.disc(sk, M / 0.16, 0.4), L.disc(sk, M / 0.25, 0.5)] + [nine * np.exp(0.4 * rng.standard_normal(40)) for _ in range(4)] + [free * np.exp(0.4 * rng.standard_normal(40)) for _ in range(2)] + [rng.uniform(0, 20, 40) * (sk.E[:-1] < rng.uniform(0.3, 0.9)) for _ in range(4)]
    ends = [L.slp(sk, a0, M) for a0 in starts]; a, f = min(ends, key=lambda z: z[1]); name = "nothing" if drop is None else f"({drop[0]},{drop[1]})"
    where = None if drop is None else float(F.FreeSkin(40, [(1, 1), drop]).solve(a, grad=False)[0])
    out[name] = dict(miss=f, exact=exact(a, modes), left=where, agree=sum(e[1] < f + 2e-5 for e in ends), n=len(ends), a=a.tolist(), used=sk.mass(a))
    print(f"{M:g} skins, {name} left out: least largest miss of the {len(modes) - 1} that remain {100 * f:.4f}% ({100 * out[name]['exact']:.4f}% exact)" + ("" if drop is None else f"; the mode left out ends {100 * where:+.2f}% from its harmonic") + f"; {out[name]['agree']} of {len(ends)} searches within 0.002 points; used {sk.mass(a):.2f}; {time.time() - t0:.0f} s", flush=True)
    json.dump(out, open(sys.argv[2], "w"))
