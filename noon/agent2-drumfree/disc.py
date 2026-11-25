"""One even disc with the lowest mode free, by exact Bessel matching: the least overtone miss for five and for seven families, where the
lowest mode then sits, the same inside the makers' range, and the disc that best fits Raman's measured ratios.
usage: python -u disc.py disc.json"""
import sys, json, math
import numpy as np
from scipy.optimize import minimize
import libfree as F
L = F.L; out = {}
S = np.exp(np.linspace(0, math.log(60), 36)); K = np.arange(0.05, 0.9501, 0.0125)
clip = lambda x: (min(60.0, max(1.0, x[0])), min(0.95, max(0.05, x[1])))
def best(f, label, top=8):
    grid = sorted((f(s, k), float(s), float(k)) for s in S for k in K); res = None
    for t, s, k in grid[:top]:
        r = minimize(lambda x: f(*clip(x)), [s, k], method='Nelder-Mead', options=dict(xatol=1e-6, fatol=1e-10, maxiter=600))
        if res is None or r.fun < res[0]: res = (float(r.fun), *clip(r.x))
    print(f"{label}: grid's best {100 * grid[0][0]:.3f}% at ({grid[0][1]:.2f}, {grid[0][2]:.4f}); the eight best grid points have k from {min(g[2] for g in grid[:top]):.4f} to {max(g[2] for g in grid[:top]):.4f}; polished {100 * res[0]:.4f}% at {res[1]:.3f} times over {res[2]:.4f}", flush=True)
    return res, grid
for name in ("five", "seven"):
    (t, s, k), grid = best(lambda s, k: F.disc_miss(s, k, F.SETS[name])[0], f"{name} families, least overtone miss"); r, pl = F.disc_modes(s, k, F.SETS[name])
    out[name] = dict(miss=t, s=s, k=k, place=pl, ratios=r, mass=(s - 1) * k * k)
    print(f"   {name}: {s:.3f} times the skin over {k:.4f} of the radius (added mass {(s - 1) * k * k:.3f} skins); overtone miss {100 * t:.3f}%; the lowest mode's place {pl:.4f}; ratios to the base " + ", ".join(f"{x:.4f}" for x in r), flush=True)
    if name == "five": out['map'] = dict(s=S.tolist(), k=K.tolist(), miss=[[F.disc_miss(s_, k_, F.FIVE)[0] for k_ in K] for s_ in S])
# inside the makers' range (density ratio 6.25 to 16, edge 0.45 to 0.55)
res = None
for s0 in np.linspace(6.25, 16, 14):
    for k0 in np.linspace(0.45, 0.55, 9):
        t = F.disc_miss(s0, k0, F.FIVE)[0]
        if res is None or t < res[0]: res = (t, float(s0), float(k0))
r = minimize(lambda x: F.disc_miss(min(16, max(6.25, x[0])), min(0.55, max(0.45, x[1])), F.FIVE)[0], res[1:], method='Nelder-Mead', options=dict(xatol=1e-6, fatol=1e-10)); s, k = min(16, max(6.25, r.x[0])), min(0.55, max(0.45, r.x[1])); t, pl = F.disc_miss(s, k, F.FIVE)
out['makers'] = dict(miss=t, s=float(s), k=float(k), place=pl); print(f"inside the makers' range: least overtone miss {100 * t:.3f}% at {s:.2f} times over {k:.4f}; the lowest mode's place {pl:.4f}", flush=True)
# Raman's measured ratios, as arXiv:0809.1320 gives them (the second mode taken as 2)
RAMAN = {(0, 1): 1.03, (2, 1): 3.00, (0, 2): 3.00, (3, 1): 4.00, (1, 2): 4.00, (0, 3): 5.04, (4, 1): 5.03, (2, 2): 5.08}
def fit(s, k):
    r, pl = F.disc_modes(s, k, F.FIVE); model = dict(zip(F.FIVE, r)); model[(0, 1)] = pl; return max(abs(model[mn] / x - 1) for mn, x in RAMAN.items())
(t, s, k), grid = best(fit, "the disc nearest Raman's eight measured ratios"); r, pl = F.disc_modes(s, k, F.FIVE); model = dict(zip(F.FIVE, r)); model[(0, 1)] = pl
out['raman'] = dict(fit=t, s=s, k=k, place=pl, model={f"{m},{n}": model[(m, n)] for m, n in RAMAN}, overtone=F.disc_miss(s, k, F.FIVE)[0])
print(f"   {s:.3f} times over {k:.4f} (added mass {(s - 1) * k * k:.3f}); largest relative difference {100 * t:.3f}%; model against measured: " + ", ".join(f"({m},{n}) {model[(m, n)]:.3f}/{x:.2f}" for (m, n), x in RAMAN.items()), flush=True)
t54 = fit(3.125 ** 2, 0.4); out['raman54'] = t54; print(f"   the 1954 disc (9.77 over 0.4) against the same ratios: largest relative difference {100 * t54:.2f}%")
json.dump(out, open(sys.argv[1], "w"))
