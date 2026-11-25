"""Which way up does a uniform square beam or cube float?   usage: python floating.py results.json
For an "up" direction n (unit vector in the body's frame) and relative density d, the water plane cuts off the share d of
the unit box below it.  h(n) = height of the centre of gravity above the centre of buoyancy; stable attitudes are the
local minima of h over directions.  For a box the cut-off volume has a closed form:
    V(t) = sum over subsets S of the nonzero components of (-1)^|S| max(0, t - sum_S |n_i|)^k / (k! prod |n_i|)
with k the number of nonzero components, and the integral of V has the same form with k + 1."""
import sys, json, itertools, math
import numpy as np
from scipy.optimize import minimize

TINY = 1e-4                                         # a component this small is treated as zero (h is even in it, so the error is ~1e-8)

def height(n, d):
    w = np.abs(np.asarray(n, float)); w = w / np.linalg.norm(w)
    w = w[w > TINY]; w = w / np.linalg.norm(w)      # renormalise after dropping components that are zero to working accuracy
    k = len(w); sums = np.array([sum(c) for r in range(k + 1) for c in itertools.combinations(w, r)]); sign = np.array([(-1) ** r for r in range(k + 1) for _ in itertools.combinations(w, r)])
    pw = np.prod(w)
    V = lambda t: float((sign * np.maximum(0.0, t - sums) ** k).sum() / (math.factorial(k) * pw))
    J = lambda t: float((sign * np.maximum(0.0, t - sums) ** (k + 1)).sum() / (math.factorial(k + 1) * pw))
    lo, hi = 0.0, float(w.sum())
    for _ in range(50):                             # the water plane: bisect on the cut-off volume
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if V(mid) < d else (lo, mid)
    t = (lo + hi) / 2
    return w.sum() / 2 - (t - J(t) / d)             # n.G - n.B

def canon(n):
    w = np.sort(np.abs(n))[::-1]
    return w / np.linalg.norm(w)

def kind(w, tol=3e-3):
    a, b, c = w
    if b < tol: return 'face up'
    if c < tol and abs(a - b) < tol: return 'edge up'
    if abs(a - b) < tol and abs(b - c) < tol: return 'corner up'
    if c < tol: return 'tilted, one edge direction level'
    if abs(a - b) < tol or abs(b - c) < tol: return 'tilted, in a diagonal plane'
    return 'lopsided'

def is_local_min(n, d, r=0.01, dim=3):
    n = np.asarray(n, float) / np.linalg.norm(n); h0 = height(n, d)
    if dim == 2:
        t = np.array([-n[1], n[0]])
        return all(height(n * math.cos(s) + t * math.sin(s), d) > h0 + 1e-12 for s in (r, -r))
    u = np.cross(n, [1.0, 0.3, 0.2]); u /= np.linalg.norm(u); v = np.cross(n, u)
    return all(height(n * math.cos(r) + (u * math.cos(p) + v * math.sin(p)) * math.sin(r), d) > h0 + 1e-12 for p in np.linspace(0, 2 * math.pi, 36, endpoint=False))

def sph(x):
    return np.array([math.sin(x[0]) * math.cos(x[1]), math.sin(x[0]) * math.sin(x[1]), math.cos(x[0])])

STARTS = [(th, ph) for th in np.linspace(0.08, 1.5, 6) for ph in np.linspace(0.05, 1.5, 6)]
SPECIAL = {'face up': (1, 0, 0), 'edge up': (1, 1, 0), 'corner up': (1, 1, 1)}

def cube_minima(d):
    found = []
    for x0 in STARTS:
        res = minimize(lambda x: height(sph(x), d), x0, method='Nelder-Mead', options=dict(xatol=1e-9, fatol=1e-13, maxiter=4000))
        w = canon(sph(res.x))
        for name, s in SPECIAL.items():             # snap to a symmetric attitude if the search ended on it
            s = canon(np.array(s, float))
            if np.abs(w - s).max() < 3e-3 and height(s, d) <= res.fun + 1e-9:
                w = s
        if is_local_min(w, d) and not any(np.abs(w - f[0]).max() < 2e-3 for f in found):
            found.append((w, height(w, d)))
    for name, s in SPECIAL.items():
        s = canon(np.array(s, float))
        if is_local_min(s, d) and not any(np.abs(s - f[0]).max() < 2e-3 for f in found):
            found.append((s, height(s, d)))
    return sorted(found, key=lambda f: f[1])

if __name__ == '__main__':
    rng = np.random.default_rng(0)
    # ---- the formula against brute force
    pts = rng.random((2_000_000, 3)); worst = 0
    for _ in range(6):
        n = rng.normal(size=3); n /= np.linalg.norm(n); d = rng.uniform(0.1, 0.9)
        s = pts @ np.abs(n); t = np.quantile(s, d); below = s <= t
        brute = np.abs(n).sum() / 2 - s[below].mean()
        worst = max(worst, abs(brute - height(n, d)))
    print(f"closed form against two million random points, six random attitudes and densities: largest difference in h {worst:.5f}")
    print(f"symmetry check: h at density 0.3 and at 0.7 for one attitude differ by a constant times d: {height([0.5, 0.3, 0.8], 0.3) * 0.3:.9f} and {height([0.5, 0.3, 0.8], 0.7) * 0.7:.9f}")
    # ---- the square beam
    def beam_state(d):
        ang = np.linspace(0, math.pi / 4, 2001); hs = np.array([height([math.cos(a), math.sin(a)], d) for a in ang])
        return float(np.degrees(ang[int(np.argmin(hs))]))
    def threshold(test, lo, hi):
        for _ in range(40):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if test(mid) else (lo, mid)
        return (lo + hi) / 2
    f1 = threshold(lambda d: is_local_min([1, 0], d, dim=2), 0.05, 0.4)
    f2 = threshold(lambda d: not is_local_min([1, 1], d, dim=2), 0.05, 0.5)
    grid = [round(0.02 + 0.005 * i, 3) for i in range(97)]
    flat_grid = [d for d in grid if is_local_min([1, 0], d, dim=2)]; corner_grid = [d for d in grid if is_local_min([1, 1], d, dim=2)]
    tilt = [(d, beam_state(d)) for d in grid]
    print(f"F1  square beam: flat is stable up to a density of {f1:.5f} (literature {(3 - math.sqrt(3)) / 6:.5f}); on the grid, stable at {flat_grid[0]} to {flat_grid[-1]}")
    print(f"F2  square beam: corner up is stable from {f2:.5f} (literature {9 / 32:.5f}); on the grid, from {corner_grid[0]}; tilt of the lowest state between: " + ", ".join(f"{d}: {a:.1f}" for d, a in tilt if 0.205 <= d <= 0.29))
    mono = all(b[1] >= a[1] - 1e-9 for a, b in zip(tilt, tilt[1:]))
    print(f"    the tilt never decreases with density: {mono}; largest jump between neighbouring densities {max(b[1] - a[1] for a, b in zip(tilt, tilt[1:])):.1f} degrees")
    # ---- the cube
    out = []
    for d in grid:
        mins = cube_minima(d)
        out.append(dict(d=d, minima=[dict(up=[float(x) for x in w], h=float(h), kind=kind(w)) for w, h in mins]))
        w, h = mins[0]
        print(f"cube d = {d:.3f}: lowest {kind(w):34s} up = ({w[0]:.4f}, {w[1]:.4f}, {w[2]:.4f})  h = {h:.6f}" + ("   also stable: " + "; ".join(f"{kind(x)} (+{hh - h:.5f})" for x, hh in mins[1:]) if len(mins) > 1 else ""))
    json.dump(dict(beam=dict(flat_threshold=f1, corner_threshold=f2, tilt=tilt), cube=out), open(sys.argv[1], 'w'))
