"""A control on the reading "the lowest mode is the costly one": keep the lowest mode as the base and leave out one of the eight
overtones instead, so that seven misses are made least as with the lowest mode free. 40 rings.
usage: python -u leaveout.py WEIGHT OUT.json"""
import sys, json
import numpy as np
import libfree as F
L = F.L; M = float(sys.argv[1]); rng = np.random.default_rng(55 + int(10 * M)); out = {}
nine = np.array(json.load(open(f"../drum/rings2-free-{M:g}.json"))['rings']['40']['a']); free = np.array(json.load(open(f"s-five-{M:g}.json"))['rings']['40']['a'])
for drop in L.NINE[1:]:
    modes = [mn for mn in L.NINE if mn != drop]; sk = L.Skin(40, modes); starts = [nine, free, L.disc(sk, M / 0.16, 0.4), L.disc(sk, M / 0.25, 0.5)] + [nine * np.exp(0.4 * rng.standard_normal(40)) for _ in range(4)] + [rng.uniform(0, 20, 40) * (sk.E[:-1] < rng.uniform(0.3, 0.9)) for _ in range(4)]
    ends = [L.slp(sk, a0, M) for a0 in starts]; a, f = min(ends, key=lambda z: z[1]); full = L.Skin(40, L.NINE); c = full.solve(a, grad=False); where = float(c[L.NINE.index(drop) - 1])
    out[f"{drop[0]},{drop[1]}"] = dict(miss=f, exact=L.exact_miss(a, modes), left=where, agree=sum(e[1] < f + 2e-5 for e in ends), n=len(ends), a=a.tolist())
    print(f"{M:g} skins, ({drop[0]},{drop[1]}) left out: least largest miss of the other seven {100 * f:.4f}% ({100 * out[f'{drop[0]},{drop[1]}']['exact']:.4f}% exact); the mode left out ends {100 * where:+.2f}% from its harmonic; {out[f'{drop[0]},{drop[1]}']['agree']} of {len(ends)} searches within 0.002 points", flush=True)
json.dump(out, open(sys.argv[2], "w"))
