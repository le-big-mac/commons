"""The three-piece model of pieces.py started from the 40-ring answer instead of from scratch: the loaded rings of the best ringed load
fall into three runs (a core, a hoop, a wider ring); make each run even, then let the five edges and the shares of the mass move
(Nelder-Mead, restarted until it stops gaining).   usage: python -u pieces2.py WEIGHT     (unregistered)"""
import sys, json
import numpy as np
from scipy.optimize import minimize
argv = sys.argv; other = __file__.replace("pieces2.py", "pieces.py"); src = open(other).read(); ns = {'__file__': other}; sys.argv = [argv[0], argv[1], "0"]; exec(src[:src.index("r = differential_evolution")], ns)          # the model of pieces.py, without its search
g, shape = ns['g'], ns['shape']; M = float(argv[1]); E = np.arange(41) / 40; A = E[1:] ** 2 - E[:-1] ** 2
rows = [r for w in ("down", "up") for r in json.load(open(f"chain-free-{w}.json")) if abs(r['weight'] - M) < 1e-9]; row = min(rows, key=lambda r: r['miss']); a = np.array(row['a']); on = a > 0.03 * a.max(); runs = []; j = 0
while j < 40:
    if on[j]:
        k = j
        while k < 40 and on[k]: k += 1
        runs.append((j, k)); j = k
    else: j += 1
print(f"added mass {M:g}: the ringed load ({100 * row['miss']:.3f}%) has {len(runs)} runs of loaded rings: " + "; ".join(f"{E[j]:.3f} to {E[k]:.3f} ({float(a[j:k] @ A[j:k]):.2f} skins)" for j, k in runs), flush=True)
if len(runs) == 3 and runs[0][0] == 0:
    m = [float(a[j:k] @ A[j:k]) for j, k in runs]; y = np.array([E[runs[0][1]], E[runs[1][0]], E[runs[1][1]], E[runs[2][0]], E[runs[2][1]], m[0] / sum(m), m[1] / sum(m)]); v = g(y); print(f"   made even, as it stands: {100 * v:.3f}%", flush=True)
    for rnd in range(6):
        r = minimize(g, y, method='Nelder-Mead', options=dict(maxiter=6000, xatol=1e-7, fatol=1e-9, adaptive=True)); gain = v - r.fun; y, v = r.x, r.fun
        if gain < 1e-6: break
    (r1, r2, r3, r4, r5), L = shape(y); print(f"   with edges and shares free: {100 * v:.3f}% ({100 * g(y, 4000):.3f}% with 4,000 cells): a core of +{L[0]:.1f} inside {r1:.3f}; a hoop of +{L[1]:.1f} from {r2:.3f} to {r3:.3f}; a ring of +{L[2]:.1f} from {r4:.3f} to {r5:.3f}", flush=True)
    json.dump(dict(weight=M, miss=float(v), miss4000=float(g(y, 4000)), radii=[float(x) for x in (r1, r2, r3, r4, r5)], loads=[float(x) for x in L]), open(f"pieces2-{M:g}.json", "w"))
