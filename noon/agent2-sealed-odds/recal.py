"""Would a correction learnt from the other studies have improved my odds on each study?   usage: python recal.py lines.csv
logit(p') = a + b logit(p), fitted by maximum likelihood on the settled lines of the other nine studies; p' kept in [0.01, 0.99]."""
import sys, csv
import numpy as np
from scipy.optimize import minimize
R = [r for r in csv.DictReader(open(sys.argv[1])) if r['outcome'] != '']
st = np.array([r['study'] for r in R]); p = np.array([float(r['odds']) for r in R]); y = np.array([float(r['outcome']) for r in R])
fc = np.array([float(r['forecasters']) if r['forecasters'] else np.nan for r in R]); x = np.log(p / (1 - p))
def fit(xx, yy, slope=True):
    def nll(t):
        z = t[0] + (t[1] if slope else 1.0) * xx
        return np.sum(np.logaddexp(0, z) - yy * z)
    best = min((minimize(nll, s, method='Nelder-Mead', options=dict(xatol=1e-9, fatol=1e-12, maxiter=20000)) for s in ([0, 1], [0.5, 1.5], [-0.5, 0.7])), key=lambda r: r.fun)
    return best.x[0], (best.x[1] if slope else 1.0)
def apply(a, b, xx): return np.clip(1 / (1 + np.exp(-(a + b * xx))), 0.01, 0.99)
B = lambda q, yy: float(np.mean((q - yy) ** 2))
studies = list(dict.fromkeys(st))
print(f"{len(R)} settled lines; my sealed odds score {B(p, y):.4f}")
for slope, name in ((True, "shift and slope"), (False, "shift only")):
    a, b = fit(x, y, slope); print(f"\n{name}: fitted to all {len(R)} lines at once: a = {a:+.3f}, b = {b:.3f}; scores {B(apply(a, b, x), y):.4f} (in sample)")
    q = np.empty_like(p)
    print("   leaving each study out in turn:")
    better = 0; worst = None
    for s in studies:
        k = st == s; a, b = fit(x[~k], y[~k], slope); q[k] = apply(a, b, x[k]); d = B(q[k], y[k]) - B(p[k], y[k]); better += round(B(q[k], y[k]), 4) < round(B(p[k], y[k]), 4)
        if worst is None or d > worst[1]: worst = (s, d)
        print(f"   {s:22s} {k.sum():3d} lines; a = {a:+.3f}, b = {b:.3f}; sealed {B(p[k], y[k]):.4f}, corrected {B(q[k], y[k]):.4f}, change {d:+.4f}")
    print(f"   all {len(R)} lines: sealed {B(p, y):.4f}, corrected {B(q, y):.4f}; studies that score better corrected: {better} of {len(studies)}; harmed most: {worst[0]} ({worst[1]:+.4f})")
    k = ~np.isnan(fc); print(f"   the {k.sum()} lines the forecasters priced: sealed {B(p[k], y[k]):.4f}, corrected {B(q[k], y[k]):.4f}, forecasters {B(fc[k], y[k]):.4f}")
    rng = np.random.default_rng(1); d = (q - y) ** 2 - (p - y) ** 2; boot = [d[rng.integers(0, len(d), len(d))].mean() for _ in range(10000)]
    print(f"   corrected minus sealed: {d.mean():+.4f}; resampling the lines as if independent: {np.percentile(boot, 2.5):+.4f} to {np.percentile(boot, 97.5):+.4f}")
    ds = np.array([d[st == s].sum() for s in studies]); boot = [ds[rng.integers(0, len(ds), len(ds))].sum() / len(d) for _ in range(10000)]
    print(f"   resampling whole studies: {np.percentile(boot, 2.5):+.4f} to {np.percentile(boot, 97.5):+.4f} (approximate: studies differ in size)")
