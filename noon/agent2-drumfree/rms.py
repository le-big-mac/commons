"""The measure varied: loads searched to make the root mean square of the misses least, the lowest mode free (seven misses against
half the second mode) and tuned (eight misses against the lowest mode, the first study's measure).  40 rings.
usage (from the study's folder): python -u rms.py WEIGHT OUT.json"""
import sys, json, time
sys.path.insert(0, ".")
import numpy as np
from scipy.optimize import minimize
import libfree as F
L = F.L; M = float(sys.argv[1]); rng = np.random.default_rng(321 + int(10 * M)); out = {}
B = json.load(open("best.json")); free0 = np.array(B[f"five|{M:g}|40"]['a']); tuned0 = np.array(json.load(open(f"../drum/rings2-free-{M:g}.json"))['rings']['40']['a'])
def search(sk, a0):
    def f(a):
        c, J = sk.solve(np.maximum(a, 0)); return float(c @ c) * 1e4, 2e4 * (J.T @ c)
    res = minimize(f, sk.fit(a0, M), jac=True, method='SLSQP', bounds=[(0, None)] * sk.R, constraints=[dict(type='ineq', fun=lambda a: M - a @ sk.A, jac=lambda a: -sk.A)], options=dict(maxiter=3000, ftol=1e-14))
    a = np.maximum(res.x, 0); c = sk.solve(a, grad=False); return a, float(np.sqrt(np.mean(c ** 2))), float(np.abs(c).max())
for name, sk, own, other in (("free", F.FreeSkin(40, F.FIVE), free0, tuned0), ("tuned", L.Skin(40, L.NINE), tuned0, free0)):
    t0 = time.time(); c0 = sk.solve(own, grad=False); starts = [own, other, L.disc(sk, M / 0.16, 0.4), L.disc(sk, M / 0.25, 0.5)] + [own * np.exp(0.3 * rng.standard_normal(40)) for _ in range(4)] + [rng.uniform(0, 20, 40) * (sk.E[:-1] < rng.uniform(0.3, 0.9)) for _ in range(4)]
    ends = [search(sk, a0) for a0 in starts]; a, r, mx = min(ends, key=lambda z: z[1])
    for _ in range(3):
        e = search(sk, a * np.exp(0.2 * rng.standard_normal(40))); ends.append(e)
        if e[1] < r: a, r, mx = e
    out[name] = dict(rms=r, largest=mx, start_rms=float(np.sqrt(np.mean(c0 ** 2))), start_largest=float(np.abs(c0).max()), agree=sum(e[1] < r * 1.02 for e in ends), n=len(ends), used=sk.mass(a), a=a.tolist())
    print(f"{M:g} skins, the lowest mode {name}: least root mean square found {100 * r:.4f}% (its largest miss {100 * mx:.4f}%); the load searched for the largest miss has {100 * out[name]['start_rms']:.4f}% and {100 * out[name]['start_largest']:.4f}%; {out[name]['agree']} of {len(ends)} searches within 2% of the least; used {sk.mass(a):.2f}; {time.time() - t0:.0f} s", flush=True)
json.dump(out, open(sys.argv[2], "w"))
