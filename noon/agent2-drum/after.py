"""Checks made after the first sheet was scored, and the graded patch of the second sheet.   usage: python after.py after.json"""
import sys, json, math
import numpy as np
from scipy.linalg import eigh_tridiagonal
from scipy.optimize import minimize
import drum
NINE, TARGET, NEXT = drum.NINE, np.array(drum.TARGET, float), drum.NEXT; R = json.load(open("results.json")); S, K = R['best_s'], R['best_k']; out = {}
def fd_modes(rho_of_r, which=NINE, N=2000):
    h = 1.0 / N; r = (np.arange(N) + 0.5) * h; rho = rho_of_r(r); re = np.arange(N + 1) * h; need = {}
    for m, n in which: need[m] = max(need.get(m, 0), n)
    ev = {}
    for m, cnt in need.items():
        d = (re[:-1] + re[1:]) / (h * h * r) + m * m / r ** 2; d[-1] += re[-1] / (h * h * r[-1]); off = -re[1:-1] / (h * h); sc = np.sqrt(r * rho)
        ev[m] = np.sqrt(eigh_tridiagonal(d * r / sc ** 2, off / (sc[:-1] * sc[1:]), select='i', select_range=(0, cnt - 1))[0])
    return np.array([ev[m][n - 1] for m, n in which])
disc = lambda s, k: (lambda r: np.where(r < k, s, 1.0)); graded = lambda s, k: (lambda r: np.where(r < k, 1 + (s - 1) * (1 - (r / k) ** 2), 1.0))
tied = lambda w: float(np.max(np.abs(w[1:] / w[0] / TARGET[1:] - 1)))
def free(w): x = w / TARGET; return float((x.max() - x.min()) / (x.max() + x.min()))
ls_tied = lambda w: float(np.sqrt(np.mean((w[1:] / w[0] / TARGET[1:] - 1) ** 2))); ls_free = lambda w: float(np.std(np.log(w / TARGET)))
print("A. The two methods at the best loading, the nine modes and the next three: largest difference "
      + f"{max(abs(a - b) / a for a, b in zip(drum.modes(S, K, NINE + NEXT), fd_modes(disc(S, K), NINE + NEXT, N=4000))):.1e}")
g = [(drum.miss(float(s), float(k)), float(s), float(k)) for k in np.arange(0.380, 0.4201, 0.004) for s in np.arange(9.0, 11.01, 0.1)]; b = min(g)
print(f"B. A fine grid round the best loading (k 0.380 to 0.420, s 9.0 to 11.0; {len(g)} points): smallest largest miss {100 * b[0]:.3f}% at s = {b[1]:.2f}, k = {b[2]:.3f}; the refined answer was {100 * R['best_miss']:.3f}% at s = {S:.3f}, k = {K:.4f}")
print("C. Other lawful measures of 'closest to harmonic', each minimised over the disc's s and k")
for name, f in (("largest miss, ratios to the lowest mode (sealed)", tied), ("largest miss, the base note free", free), ("root mean square miss, ratios to the lowest mode", ls_tied), ("root mean square miss, the base note free", ls_free)):
    best = min(((f(np.array(drum.modes(float(s), float(k)))), float(s), float(k)) for k in np.arange(0.25, 0.551, 0.025) for s in np.arange(4.0, 16.01, 1.0)))
    res = minimize(lambda x: f(np.array(drum.modes(min(40.0, max(1.0, x[0])), min(0.95, max(0.05, x[1]))))), best[1:], method="Nelder-Mead", options=dict(xatol=1e-4, fatol=1e-8)); w = np.array(drum.modes(res.x[0], res.x[1]))
    print(f"   {name:52s} s = {res.x[0]:6.2f}, k = {res.x[1]:.3f}: {100 * res.fun:.2f}%   (by the sealed measure there: {100 * tied(w):.2f}%)"); out[name] = (float(res.x[0]), float(res.x[1]), float(res.fun))
print("D. How sharp is the tuning? The largest miss (sealed measure) away from the best loading")
print("   k = 0.40: " + "; ".join(f"s = {s}: {100 * drum.miss(float(s), 0.40):.1f}%" for s in (4, 6, 8, 10, 12, 14, 20)))
print("   s = 10:   " + "; ".join(f"k = {k}: {100 * drum.miss(10.0, k):.1f}%" for k in (0.2, 0.3, 0.35, 0.4, 0.45, 0.5, 0.6)))
u = np.array(drum.modes(1.0, 0.5)); w = np.array(drum.modes(S, K)); print(f"E. Modes within 2% of a harmonic of the lowest mode (of the eight): unloaded {int((np.abs(u[1:] / u[0] / np.round(u[1:] / u[0]) - 1) <= 0.02).sum())}; best disc {int((np.abs(w[1:] / w[0] / TARGET[1:] - 1) <= 0.02).sum())}; unloaded, the sealed measure against its own targets: {100 * tied(u):.1f}%")
ks = np.arange(0.10, 0.801, 0.02); ss = np.concatenate([np.arange(1.0, 10.0, 0.5), np.arange(10.0, 30.01, 1.0)]); grid = [[tied(fd_modes(disc(float(s), float(k)), N=800)) for k in ks] for s in ss]; out['map'] = dict(k=ks.tolist(), s=ss.tolist(), miss=grid)
print("F. The graded patch (load falling off as a parabola from the centre; second sheet)")
chk = fd_modes(graded(20.0, 0.5)); chk2 = fd_modes(graded(20.0, 0.5), N=4000); print(f"   finite differences with 2,000 and 4,000 cells differ by at most {max(abs(a - b) / a for a, b in zip(chk, chk2)):.1e}")
best = min(((tied(fd_modes(graded(float(s), float(k)), N=800)), float(s), float(k)) for k in np.arange(0.05, 0.951, 0.025) for s in np.concatenate([np.arange(1.0, 20.0, 1.0), np.arange(20.0, 80.01, 2.5)])))
print(f"   coarse search: largest miss {100 * best[0]:.2f}% at s = {best[1]:.1f}, k = {best[2]:.3f}")
res = minimize(lambda x: tied(fd_modes(graded(min(80.0, max(1.0, x[0])), min(0.95, max(0.05, x[1]))))), best[1:], method="Nelder-Mead", options=dict(xatol=1e-3, fatol=1e-7)); gs, gk = float(min(80.0, max(1.0, res.x[0]))), float(min(0.95, max(0.05, res.x[1])))
wg = fd_modes(graded(gs, gk), NINE + NEXT, N=4000); rg = wg / wg[0]
print(f"   refined: peak load s = {gs:.2f}, k = {gk:.4f}; largest miss {100 * tied(wg[:9]):.3f}%; ratios " + ", ".join(f"{x:.3f}" for x in rg[:9]) + "; the next three " + ", ".join(f"{x:.3f}" for x in rg[9:]))
print(f"   the patch's added mass as a share of the bare skin's: disc {(S - 1) * K * K:.2f}; graded {(gs - 1) * gk * gk / 2:.2f}")
print(f"   G1 (below 3.157%): {'held' if tied(wg[:9]) < 0.03157 else 'FAILED'}; G2 (k above 0.45): {'held' if gk > 0.45 else 'FAILED'}; G3 (s above 12): {'held' if gs > 12 else 'FAILED'}")
out.update(graded=dict(s=gs, k=gk, miss=tied(wg[:9]), ratios=rg.tolist()), disc_w=w.tolist(), unloaded_w=u.tolist()); json.dump(out, open(sys.argv[1], "w"))
