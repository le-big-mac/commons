import sys; sys.path.insert(0, "/home/agent2/drum12/referee")
import numpy as np, time
from scipy.optimize import minimize
import sol
F = int(sys.argv[1]) if len(sys.argv) > 1 else 6
modes = sol.fam_modes(F)
def miss(s, k, exact=False, p=120):
    c = sol.misses(np.array([k, 1.0]), np.array([s, 1.0]), modes, p, exact)
    return np.abs(c).max()
t0 = time.time()
S = np.arange(1, 60.01, 0.5); K = np.arange(0.05, 0.9501, 0.01)
G = np.array([[miss(s, k) for k in K] for s in S])
print("# grid %dx%d done in %.0fs; grid min %.4f%%" % (len(S), len(K), time.time() - t0, 100 * G.min()))
cand = []
for i in range(len(S)):
    for j in range(len(K)):
        nb = G[max(i - 1, 0):i + 2, max(j - 1, 0):j + 2]
        if G[i, j] <= nb.min(): cand.append((G[i, j], S[i], K[j]))
cand.sort()
print("# grid local minima (miss%, s, k):", [(round(100 * g, 3), s, round(k, 2)) for g, s, k in cand[:8]])
out = []
for g, s, k in cand[:6]:
    fun = lambda x: miss(x[0], x[1], True, 300) if (1 <= x[0] <= 60 and 0.05 <= x[1] <= 0.95) else 9.0
    r = minimize(fun, [s, k], method='Nelder-Mead', options=dict(xatol=1e-5, fatol=1e-9, initial_simplex=[[s, k], [min(s + 0.3, 60), k], [s, k + 0.005]]))
    out.append((r.fun, r.x[0], r.x[1]))
    print("refined: miss %.4f%% at s=%.4f k=%.5f (added mass %.3f)" % (100 * r.fun, r.x[0], r.x[1], (r.x[0] - 1) * r.x[1]**2), flush=True)
out.sort(); f, s, k = out[0]
c = sol.misses(np.array([k, 1.0]), np.array([s, 1.0]), modes, 400, True)
print("BEST DISC F=%d: miss %.4f%% at s=%.4f k=%.5f added mass %.3f" % (F, 100 * f, s, k, (s - 1) * k * k))
print("misses %:", " ".join("(%d,%d)%+.3f" % (m, n, 100 * ci) for (m, n, _), ci in zip(modes[1:], c)))
print("# time %.0fs" % (time.time() - t0))
