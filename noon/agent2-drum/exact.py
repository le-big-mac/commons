"""A patch of any radial shape: the lightest load, in 40 rings, that puts the nine modes on their harmonics.
usage: python -u exact.py exact.json
Finite differences (2,000 cells, 50 to a ring; the answer checked with 8,000). Gradient search (SLSQP) with the exact derivative of
each frequency with respect to each ring's load.  Sealed measure: the largest of |ratio/target - 1| over the eight ratios."""
import sys, json, math
import numpy as np
from scipy.linalg import eigh_tridiagonal
from scipy.optimize import minimize
NINE = [(0, 1), (1, 1), (2, 1), (0, 2), (3, 1), (1, 2), (4, 1), (2, 2), (0, 3)]; TARGET = np.array([1, 2, 3, 3, 4, 4, 5, 5, 5], float); NEXT = [(5, 1), (3, 2), (1, 3)]
RINGS = 40; EDGE = np.arange(RINGS + 1) / RINGS; AREA = EDGE[1:] ** 2 - EDGE[:-1] ** 2; MAXMASS = 12.0
def solve(a, N=2000, which=NINE, grad=True):
    """frequencies of the modes and, for each, the derivative of ln(frequency) with respect to each ring's load"""
    per = N // RINGS; h = 1.0 / N; r = (np.arange(N) + 0.5) * h; re = np.arange(N + 1) * h; rho = 1.0 + np.repeat(a, per); sc = np.sqrt(r * rho); need = {}
    for m, n in which: need[m] = max(need.get(m, 0), n)
    w = {}; g = {}
    for m, cnt in need.items():
        d = (re[:-1] + re[1:]) / (h * h) + m * m / r; d[-1] += re[-1] / (h * h); off = -re[1:-1] / (h * h)
        ev, vec = eigh_tridiagonal(d / sc ** 2, off / (sc[:-1] * sc[1:]), select='i', select_range=(0, cnt - 1))
        for n in range(cnt):
            w[(m, n + 1)] = math.sqrt(ev[n])
            if grad: g[(m, n + 1)] = -0.5 * (vec[:, n] ** 2 / rho).reshape(RINGS, per).sum(axis=1)          # d ln w / d a_j
    W = np.array([w[k] for k in which]); return (W, np.array([g[k] for k in which])) if grad else W
def misses(a, N=2000): W = solve(a, N, grad=False); return W[1:] / W[0] / TARGET[1:] - 1
mass = lambda a: float(a @ AREA)
cache = {}
def cons(a):
    key = a.tobytes()
    if key not in cache:
        cache.clear(); W, G = solve(a); c = np.log(W[1:] / W[0]) - np.log(TARGET[1:]); J = G[1:] - G[0]; cache[key] = (c, J)
    return cache[key]
def minimax(a0, monotone=False, iters=400):
    """least largest miss: variables (a, t); |c_i| <= t"""
    x0 = np.concatenate([a0, [np.abs(cons(a0)[0]).max() * 1.05]])
    cs = [dict(type='ineq', fun=lambda x: x[-1] - cons(x[:-1])[0], jac=lambda x: np.hstack([-cons(x[:-1])[1], np.ones((8, 1))])),
          dict(type='ineq', fun=lambda x: x[-1] + cons(x[:-1])[0], jac=lambda x: np.hstack([cons(x[:-1])[1], np.ones((8, 1))])),
          dict(type='ineq', fun=lambda x: MAXMASS - x[:-1] @ AREA, jac=lambda x: np.concatenate([-AREA, [0.0]]))]
    if monotone:
        D = np.zeros((RINGS - 1, RINGS + 1)); D[np.arange(RINGS - 1), np.arange(RINGS - 1)] = 1; D[np.arange(RINGS - 1), np.arange(1, RINGS)] = -1
        cs.append(dict(type='ineq', fun=lambda x: D @ x, jac=lambda x: D))
    r = minimize(lambda x: x[-1], x0, jac=lambda x: np.concatenate([np.zeros(RINGS), [1.0]]), bounds=[(0, None)] * RINGS + [(0, None)], constraints=cs, method='SLSQP', options=dict(maxiter=iters, ftol=1e-12))
    return np.maximum(r.x[:-1], 0.0)
def lightest(a0, iters=600):
    """least added mass with the eight ratios exact"""
    r = minimize(lambda a: a @ AREA, a0, jac=lambda a: AREA, bounds=[(0, None)] * RINGS, constraints=[dict(type='eq', fun=lambda a: cons(a)[0], jac=lambda a: cons(a)[1])], method='SLSQP', options=dict(maxiter=iters, ftol=1e-13))
    return np.maximum(r.x, 0.0)
def discs(loads, radii): return sum(l * np.clip((np.minimum(k, EDGE[1:]) ** 2 - EDGE[:-1] ** 2) / AREA, 0, 1) for l, k in zip(loads, radii))
rng = np.random.default_rng(40)
starts = [("two discs", discs([12.94, 5.63], [0.438, 0.234])), ("one disc", discs([8.94], [0.4004]))]
for i in range(10):
    k = rng.uniform(0.3, 0.6); a = rng.uniform(3, 14) * np.clip(1 - (EDGE[:-1] / k) ** rng.uniform(1, 6), 0, None) + rng.uniform(0, 1.5, RINGS) * (rng.random(RINGS) < 0.3); starts.append((f"random {i + 1}", a))
out = dict(runs=[]); best = None
print("start        least miss found   then the lightest exact patch: added mass, largest miss (2,000 cells), heaviest ring, share of mass beyond 0.6", flush=True)
for name, a0 in starts:
    a1 = minimax(a0); t1 = float(np.abs(misses(a1)).max()); line = f"{name:11s}  {100 * t1:8.4f}%"
    if t1 <= 5e-4 * 4:
        a2 = lightest(a1); t2 = float(np.abs(misses(a2)).max())
        if t2 > 5e-4: a2 = lightest(minimax(a2), iters=1000); t2 = float(np.abs(misses(a2)).max())
        j = int(np.argmax(a2)); beyond = float(a2[EDGE[:-1] >= 0.6 - 1e-9] @ AREA[EDGE[:-1] >= 0.6 - 1e-9]) / max(mass(a2), 1e-12)
        line += f"          {mass(a2):6.3f} skins, {100 * t2:.4f}%, ring {j + 1} (from {EDGE[j]:.3f}), {100 * beyond:.0f}%"
        out['runs'].append(dict(start=name, miss1=t1, mass=mass(a2), miss=t2, a=a2.tolist()))
        if t2 <= 5e-4 and (best is None or mass(a2) < best[0]): best = (mass(a2), a2, name)
    else: out['runs'].append(dict(start=name, miss1=t1))
    print(line, flush=True)
if best:
    m, a, name = best; W = solve(a, 8000, NINE + NEXT, grad=False); r = W / W[0]; j = int(np.argmax(a)); sel = EDGE[:-1] >= 0.6 - 1e-9
    print(f"\nthe lightest exact patch found (from the start '{name}'): added mass {m:.3f} skins; largest miss {100 * np.abs(misses(a)).max():.4f}% with 2,000 cells and {100 * np.abs(r[1:9] / TARGET[1:] - 1).max():.4f}% with 8,000")
    print("   ratios (8,000 cells): " + ", ".join(f"{x:.4f}" for x in r[:9]) + "; the next three: " + ", ".join(f"{x:.3f}" for x in r[9:]))
    print("   load by ring, from the centre (40 rings): " + " ".join(f"{x:.2f}" for x in a))
    print(f"   heaviest ring: {j + 1} (from {EDGE[j]:.3f} to {EDGE[j + 1]:.3f}), load {a[j]:.2f}; share of the added mass beyond 0.6 of the radius: {100 * float(a[sel] @ AREA[sel]) / m:.1f}%; rings with any load: {int((a > 1e-6).sum())}")
    out.update(best=dict(mass=m, a=a.tolist(), start=name, ratios=r.tolist()))
print("\nloads that may not increase outward (discs piled on discs): the least largest miss found, within 12 skins", flush=True)
mono = []
for name, a0 in starts:
    a0m = np.maximum.accumulate(a0[::-1])[::-1]; a1 = minimax(a0m, monotone=True, iters=600); t = float(np.abs(misses(a1)).max()); mono.append((t, name, a1)); print(f"   {name:11s} {100 * t:.4f}%   (added mass {mass(a1):.2f}; steps of more than 0.05 in the load: {int((np.abs(np.diff(a1)) > 0.05).sum())})", flush=True)
t, name, a = min(mono, key=lambda z: z[0]); W = solve(a, 8000, NINE, grad=False); print(f"   least: {100 * t:.4f}% from '{name}' ({100 * np.abs(W[1:] / W[0] / TARGET[1:] - 1).max():.4f}% with 8,000 cells); load by ring: " + " ".join(f"{x:.2f}" for x in a))
out.update(monotone=dict(miss=t, a=a.tolist(), start=name)); json.dump(out, open(sys.argv[1], "w"))
