"""The referee's controls, redone here with my own code.   usage: python -u after3.py SECTIONS   (for example 12 or 3 or 45)
Finite differences as before, but a cell that a disc's edge cuts takes the average of the two loads, so that the largest miss changes
smoothly with a radius (the referee found that my 600-cell searches were walking on a staircase)."""
import math, json, sys
SEC = sys.argv[1] if len(sys.argv) > 1 else '12345'
import numpy as np
from scipy.linalg import eigh_tridiagonal
from scipy.optimize import differential_evolution, minimize_scalar, minimize
import drum
NINE, TARGET = drum.NINE, np.array(drum.TARGET, float)
def modes(rho_cells, N):
    h = 1.0 / N; r = (np.arange(N) + 0.5) * h; re = np.arange(N + 1) * h; rho = rho_cells; sc = np.sqrt(r * rho); need = {0: 3, 1: 2, 2: 2, 3: 1, 4: 1}; ev = {}
    for m, cnt in need.items():
        d = (re[:-1] + re[1:]) / (h * h * r) + m * m / r ** 2; d[-1] += re[-1] / (h * h * r[-1]); off = -re[1:-1] / (h * h)
        ev[m] = np.sqrt(eigh_tridiagonal(d * r / sc ** 2, off / (sc[:-1] * sc[1:]), select='i', select_range=(0, cnt - 1))[0])
    return np.array([ev[m][n - 1] for m, n in NINE])
def discs(loads, radii, N):
    """mass per area in each cell: 1 plus each load times the share of the cell's area inside that disc's radius"""
    re = np.arange(N + 1) / N; rho = np.ones(N)
    for a, k in zip(loads, radii): rho += a * np.clip((np.minimum(k, re[1:]) ** 2 - re[:-1] ** 2) / (re[1:] ** 2 - re[:-1] ** 2), 0, 1)
    return rho
tied = lambda w: float(np.max(np.abs(w[1:] / w[0] / TARGET[1:] - 1)))
f2 = lambda x, N=800: tied(modes(discs([x[0], x[1]], [max(x[2], x[3]), min(x[2], x[3])], N), N))
if '1' in SEC:
    print("1. Two layers inside the sealed range (loads 0 to 40, radii 0.05 to 0.95), by differential evolution, two seeds")
    for seed in (1, 2):
        r = differential_evolution(f2, [(0, 40), (0, 40), (0.05, 0.95), (0.05, 0.95)], seed=seed, tol=1e-7, maxiter=150, popsize=12, polish=True); x = r.x; ko, ki = max(x[2], x[3]), min(x[2], x[3]); ao, ai = x[0], x[1]      # the first load always goes with the wider radius, as in f2
        print(f"   seed {seed}: largest miss {100 * r.fun:.3f}% (800 cells; {100 * f2(x, 6000):.3f}% with 6,000): +{ao:.2f} inside {ko:.4f} and +{ai:.2f} inside {ki:.4f}; added mass {ao * ko * ko + ai * ki * ki:.2f} skins")
if '2' in SEC:
    print("2. Two layers with the outer load fixed beyond the sealed cap (the rest refitted)")
    for ao in (40, 80, 160, 640):
        r = differential_evolution(lambda y: f2([ao, y[0], y[1], y[2]]), [(0, 2 * ao), (0.3, 0.6), (0.1, 0.4)], seed=3, tol=1e-7, maxiter=120, popsize=12); print(f"   outer load {ao:4d}: largest miss {100 * r.fun:.3f}%; inner +{r.x[0]:.1f}; radii {max(r.x[1], r.x[2]):.4f} and {min(r.x[1], r.x[2]):.4f}")
if '3' in SEC:
    print("3. Two layers at a fixed added mass (in bare skins); the even disc adds 1.43")
    def fixed(M):
        def g(y):
            ko, ki, share = max(y[0], y[1]), min(y[0], y[1]), y[2]; return tied(modes(discs([share * M / ko ** 2, (1 - share) * M / ki ** 2], [ko, ki], 800), 800))
        r = differential_evolution(g, [(0.2, 0.7), (0.08, 0.5), (0.0, 1.0)], seed=4, tol=1e-7, maxiter=120, popsize=15); return r.fun, r.x
    for M in (1.433, 1.5, 1.6, 2.0, 2.79, 4.6, 9.6):
        v, x = fixed(M); print(f"   added mass {M:5.2f}: largest miss {100 * v:.2f}%  (radii {max(x[0], x[1]):.3f} and {min(x[0], x[1]):.3f}; {100 * x[2]:.0f}% of the mass in the wider disc)")
if '4' in SEC:
    print("4. The parabola at a fixed added mass, (s - 1) k^2 / 2")
    def para(M):
        def g(k):
            s = 1 + 2 * M / k ** 2; N = 2000; r = (np.arange(N) + 0.5) / N; return tied(modes(np.where(r < k, 1 + (s - 1) * (1 - (r / k) ** 2), 1.0), N))
        r = minimize_scalar(g, bounds=(0.2, 0.95), method="bounded", options=dict(xatol=1e-5)); return r.fun, r.x, 1 + 2 * M / r.x ** 2
    for M in (1.433, 2.0, 3.0, 4.0):
        v, k, s = para(M); print(f"   added mass {M:5.2f}: largest miss {100 * v:.2f}% (peak {s:.1f} over {k:.3f})")
if '5' in SEC:
    print("5. Heavier even discs with the radius refitted (exact Bessel matching)")
    for s in (9.94, 12, 14, 20, 30, 40):
        r = minimize_scalar(lambda k: drum.miss(float(s), float(k)), bounds=(0.30, 0.55), method="bounded", options=dict(xatol=1e-5)); print(f"   s = {s:5.2f}: best k = {r.x:.3f}; largest miss {100 * r.fun:.2f}%")
    R = json.load(open("results.json")); c = [1200 * math.log2(x / t) for x, t in zip(R['ratios'], drum.TARGET)]
    print(f"6. The best even disc in cents: (2,1) and (0,2) are {c[3] - c[2]:.0f} apart; (3,1) and (1,2) {c[5] - c[4]:.0f}; the three aimed at 5 span {max(c[6:9]) - min(c[6:9]):.0f}")
    u = np.array(json.load(open("after.json"))['unloaded_w']); u = u / u[0]; print("7. The plain skin's overtones against the nearest whole multiple: " + ", ".join(f"{x:.3f} ({100 * (x / round(x) - 1):+.1f}%)" for x in u[1:]))
