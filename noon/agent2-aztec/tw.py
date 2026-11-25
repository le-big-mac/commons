"""The exact law of the frozen depth against the Tracy-Widom distribution.   usage: python tw.py tw.json > tw.out
F(s) = det(I - K_Airy on (s, infinity)), by Gauss-Legendre quadrature (the upper end cut at s + 14, where the Airy function is negligible)."""
import sys, os, json, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'referee'))
import numpy as np
from scipy.special import airy
from ref_Kkraw import K_law
X, Wt = np.polynomial.legendre.leggauss(80)
def F(s, width=14.0):
    global X, Wt
    x = s + (X + 1) * width / 2; w = Wt * width / 2; ai, aip, _, _ = airy(x)
    with np.errstate(divide='ignore', invalid='ignore'):
        Kmat = (ai[:, None] * aip[None, :] - aip[:, None] * ai[None, :]) / (x[:, None] - x[None, :])
    np.fill_diagonal(Kmat, aip ** 2 - x * ai ** 2)
    sw = np.sqrt(w); return float(np.linalg.det(np.eye(len(x)) - sw[:, None] * Kmat * sw[None, :]))
if __name__ == '__main__':
    grid = np.linspace(-9, 6, 3001); cdf = np.array([F(s) for s in grid]); pdf = np.gradient(cdf, grid); tz = lambda y: float(np.sum((y[1:] + y[:-1]) / 2 * np.diff(grid)))
    mean = tz(grid * pdf); var = tz((grid - mean) ** 2 * pdf); skew = tz((grid - mean) ** 3 * pdf) / var ** 1.5
    print(f"Tracy-Widom, computed with 80 nodes: F(-9) = {cdf[0]:.2e}, F(6) = {cdf[-1]:.12f}; mean {mean:.5f}, standard deviation {math.sqrt(var):.5f}, skewness {skew:.5f}")
    X, Wt = np.polynomial.legendre.leggauss(50); c50 = np.array([F(s_) for s_ in grid]); X, Wt = np.polynomial.legendre.leggauss(80)
    print(f"   the same function with 50 nodes differs from it by at most {np.abs(c50 - cdf).max():.1e}; with the upper end at s + 10 instead of s + 14, by at most {np.abs(np.array([F(s_, 10.0) for s_ in grid[::10]]) - cdf[::10]).max():.1e}")
    Fi = lambda s: np.interp(s, grid, cdf, left=0.0, right=1.0)
    a = (1 - 1 / math.sqrt(2)) / 2; b = 2 ** (-11 / 6); out = dict(mean=mean, sd=math.sqrt(var), skew=skew, sizes={})
    for n in (100, 400, 1600, 6400):
        law = K_law(n); surv = law['surv']; ks = np.arange(len(surv)); best = None
        for shift in np.arange(-1, 1.0001, 0.01):
            D = float(np.abs(surv - Fi((a * n - ks + shift) / (b * n ** (1 / 3)))).max())
            if best is None or D < best[0]: best = (D, float(shift))
        D0 = float(np.abs(surv - Fi((a * n - ks - 0.5) / (b * n ** (1 / 3)))).max())
        out['sizes'][n] = dict(D=best[0], shift=best[1], D_half=D0, mean=law['mean'], sd=law['sd'], skew=law['skew'], pmf=law['pmf'].tolist())
        print(f"n = {n:5d}: D = {best[0]:.5f} at shift {best[1]:+.2f}; with the shift fixed at -1/2: {D0:.5f}; exact skewness {law['skew']:+.4f}; standardised: (a n - 1/2 - mean)/(b n^(1/3)) = {(a * n - 0.5 - law['mean']) / (b * n ** (1 / 3)):+.4f}, sd/(b n^(1/3)) = {law['sd'] / (b * n ** (1 / 3)):.4f}", flush=True)
    json.dump(out, open(sys.argv[1], 'w'))
