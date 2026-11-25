"""A third method for the ringed loads: exact matching of Bessel functions across every edge, with no grid.
The skin is a set of rings, each of even mass per area; in each ring the radial shape is a J_m + b Y_m, and the value and the slope are
carried across each edge.  A mode is a frequency at which the shape vanishes at the rim.
usage: python bessel3.py pieces2-1.43.json pieces2-2.79.json pieces2-12.json chain-free-down.json chain-free-up.json     (unregistered)"""
import sys, json, math
import numpy as np
from scipy.special import jv, yv, jvp, yvp
from scipy.optimize import brentq
NINE = [(0, 1), (1, 1), (2, 1), (0, 2), (3, 1), (1, 2), (4, 1), (2, 2), (0, 3)]; TARGET = [1, 2, 3, 3, 4, 4, 5, 5, 5]
def rim(w, m, edges, rho):
    """the shape's value at the rim; edges are the outer radii of the rings, the last being 1; rho their mass per area"""
    k = w * math.sqrt(rho[0]); R, dR = jv(m, k * edges[0]), k * jvp(m, k * edges[0])
    for e0, e1, p in zip(edges[:-1], edges[1:], rho[1:]):
        k = w * math.sqrt(p); J, Y, dJ, dY = jv(m, k * e0), yv(m, k * e0), k * jvp(m, k * e0), k * yvp(m, k * e0); det = J * dY - Y * dJ; a, b = (R * dY - Y * dR) / det, (J * dR - R * dJ) / det
        R, dR = a * jv(m, k * e1) + b * yv(m, k * e1), k * (a * jvp(m, k * e1) + b * yvp(m, k * e1))
    return R
def modes(edges, rho, wmax=14.0, step=0.002):
    need = {}; out = {}
    for m, n in NINE: need[m] = max(need.get(m, 0), n)
    for m, cnt in need.items():
        roots = []; w = 0.02; f0 = rim(w, m, edges, rho)
        while len(roots) < cnt and w < wmax:
            f1 = rim(w + step, m, edges, rho)
            if f0 * f1 < 0: roots.append(brentq(rim, w, w + step, args=(m, edges, rho), xtol=1e-13))
            w += step; f0 = f1
        out[m] = roots
    return np.array([out[m][n - 1] for m, n in NINE])
def report(name, edges, rho, other):
    w = modes(edges, rho); r = w / w[0]; t = max(abs(r[i] / TARGET[i] - 1) for i in range(1, 9)); print(f"{name}: largest miss {100 * t:.4f}% by exact matching ({other}); ratios " + ", ".join(f"{x:.4f}" for x in r), flush=True)
print("a check of the method on the best even disc (drum.py gives 3.157% at s = 9.938, k = 0.4004):"); report("   one even disc", [0.4004, 1.0], [9.938, 1.0], "drum.py: 3.157%")
for f in sys.argv[1:4]:
    P = json.load(open(f)); r1, r2, r3, r4, r5 = P['radii']; L = P['loads']
    report(f"three even pieces, added mass {P['weight']:g}", [r1, r2, r3, r4, r5, 1.0], [1 + L[0], 1.0, 1 + L[1], 1.0, 1 + L[2], 1.0], f"finite differences: {100 * P['miss']:.4f}% with 800 cells, {100 * P['miss4000']:.4f}% with 4,000")
rows = {}
for f in sys.argv[4:6]:
    for r in json.load(open(f)):
        if r['weight'] not in rows or r['miss'] < rows[r['weight']]['miss']: rows[r['weight']] = r
for M in (1.43, 2.79, 12.0):
    a = np.array(rows[M]['a']); n = int(np.max(np.nonzero(a > 1e-9)[0])) + 1; report(f"the 40-ring load, added mass {M:g}", [(j + 1) / 40 for j in range(n)] + [1.0], [1 + x for x in a[:n]] + [1.0], f"finite differences: {100 * rows[M]['miss']:.4f}% with 2,000 cells")
