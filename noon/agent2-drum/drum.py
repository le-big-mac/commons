"""A round membrane with a heavier disc at its centre: modes by exact matching of Bessel functions.
usage: python drum.py modes results.json | python drum.py check
Radius 1, even tension, fixed rim; mass per area s for r < k and 1 beyond.  w is the wavenumber outside (frequency in units where tension = 1)."""
import sys, json, math
import numpy as np
from scipy.special import jv, yv, jvp, yvp
from scipy.optimize import brentq, minimize
NINE = [(0, 1), (1, 1), (2, 1), (0, 2), (3, 1), (1, 2), (4, 1), (2, 2), (0, 3)]; TARGET = [1, 2, 3, 3, 4, 4, 5, 5, 5]; NEXT = [(5, 1), (3, 2), (1, 3)]
def F(w, m, s, k):
    """zero when w is a mode: inside J_m(sqrt(s) w r); outside the combination of J_m and Y_m that vanishes at the rim; value and slope matched at r = k"""
    a, b = math.sqrt(s) * w * k, w * k
    phi = jv(m, b) * yv(m, w) - yv(m, b) * jv(m, w); dphi = jvp(m, b) * yv(m, w) - yvp(m, b) * jv(m, w)
    return (math.sqrt(s) * jvp(m, a) * phi - jv(m, a) * dphi) * b          # times b: keeps the size even when w k is small
def roots(m, s, k, count, wmax=40.0):
    out = []; step = 0.01 / max(1.0, math.sqrt(s) * k); w = 0.05 + 0.3 * m; f0 = F(w, m, s, k)
    while len(out) < count and w < wmax:
        w1 = w + step; f1 = F(w1, m, s, k)
        if f0 == 0 or f0 * f1 < 0: out.append(brentq(F, w, w1, args=(m, s, k), xtol=1e-12))
        w, f0 = w1, f1
    return out
def modes(s, k, which=NINE):
    need = {}
    for m, n in which: need[m] = max(need.get(m, 0), n)
    r = {m: roots(m, s, k, c) for m, c in need.items()}; return [r[m][n - 1] for m, n in which]
def miss(s, k):
    w = modes(s, k); return max(abs(w[i] / w[0] / TARGET[i] - 1) for i in range(1, 9))
def fd(m, s, k, count, N=4000):
    """a second method: finite differences on the radial equation -(r R')'/r + m^2 R / r^2 = w^2 rho R, R(1) = 0"""
    from scipy.linalg import eigh_tridiagonal
    h = 1.0 / N; r = (np.arange(N) + 0.5) * h; rho = np.where(r < k, s, 1.0); re = np.arange(N + 1) * h          # cell centres and edges
    d = (re[:-1] + re[1:]) / (h * h * r) + m * m / r ** 2; d[-1] += re[-1] / (h * h * r[-1])                        # ghost cell beyond the rim: R = -R
    off = -re[1:-1] / (h * h)                                                                                       # symmetric after scaling by sqrt(r rho)
    sc = np.sqrt(r * rho); dd = d * r / sc ** 2; oo = off / (sc[:-1] * sc[1:])
    ev = eigh_tridiagonal(dd, oo, select='i', select_range=(0, count - 1))[0]; return np.sqrt(ev)
if __name__ == "__main__":
    if sys.argv[1] == "check":
        print("unloaded, the nine modes (exact zeros of Bessel functions are 2.4048, 3.8317, 5.1356, 5.5201, 6.3802, 7.0156, 7.5883, 8.4172, 8.6537):")
        print("   " + " ".join(f"{w:.4f}" for w in modes(1.0, 0.4)))
        for s, k in ((4.0, 0.3), (10.0, 0.4), (25.0, 0.6)):
            a = modes(s, k); b = []
            for (m, n) in NINE: b.append(fd(m, s, k, n)[n - 1])
            print(f"s = {s}, k = {k}: largest difference between the two methods over the nine modes: {max(abs(x - y) / x for x, y in zip(a, b)):.1e}")
        sys.exit()
    R = {}
    w1 = modes(1.0, 0.5); r1 = [w / w1[0] for w in w1]; print("1. unloaded: " + ", ".join(f"{x:.4f}" for x in r1)); R['unloaded'] = r1
    print("2. s = 4, the ratio of (1,1) by k: " + ", ".join(f"k = {k:.1f}: {modes(4.0, k)[1] / modes(4.0, k)[0]:.4f}" for k in (0.1, 0.2, 0.3, 0.4, 0.5, 0.6))); R['d4'] = [modes(4.0, k)[1] / modes(4.0, k)[0] for k in (0.1, 0.2, 0.3, 0.4, 0.5, 0.6)]
    best = (9, None)
    for k in np.arange(0.05, 0.951, 0.025):
        for s in np.concatenate([np.arange(1.0, 10.0, 0.5), np.arange(10.0, 40.01, 1.0)]):
            v = miss(float(s), float(k))
            if v < best[0]: best = (v, (float(s), float(k)))
    print(f"3. coarse search: largest miss {100 * best[0]:.2f}% at s = {best[1][0]:.2f}, k = {best[1][1]:.3f}")
    res = minimize(lambda x: miss(min(40.0, max(1.0, x[0])), min(0.95, max(0.05, x[1]))), best[1], method="Nelder-Mead", options=dict(xatol=1e-4, fatol=1e-7))
    s, k = float(min(40.0, max(1.0, res.x[0]))), float(min(0.95, max(0.05, res.x[1]))); w = modes(s, k); ratios = [x / w[0] for x in w]; nx = [x / w[0] for x in modes(s, k, NEXT)]
    print(f"   refined: s = {s:.3f}, k = {k:.4f}; largest miss {100 * miss(s, k):.3f}%")
    print("   mode    ratio   target   miss")
    for (m, n), x, t in zip(NINE, ratios, TARGET): print(f"   ({m},{n})   {x:.4f}   {t}     {100 * (x / t - 1):+.2f}%")
    print(f"   (2,1) and (0,2) differ by {100 * abs(ratios[2] / ratios[3] - 1):.2f}%; (3,1) and (1,2) by {100 * abs(ratios[4] / ratios[5] - 1):.2f}%")
    print("   the next three, against 6: " + ", ".join(f"({m},{n}) {x:.4f} ({100 * (x / 6 - 1):+.2f}%)" for (m, n), x in zip(NEXT, nx)))
    R.update(best_s=s, best_k=k, best_miss=miss(s, k), ratios=ratios, next=nx, w0=w[0]); json.dump(R, open(sys.argv[2], "w"), indent=1)
