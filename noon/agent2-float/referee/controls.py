"""Step 2 controls against the author's code (imported read-only; run with python -B)."""
import sys, math
sys.path.insert(0, '/home/agent2/float')
from decimal import Decimal as D
import numpy as np
import floating as F
from ref import h_dec, h_float, clip_h
from blindC import valley, ring_h, ring_t, diag_min, golden
S2 = D(2).sqrt()
def P(*a): print(*a, flush=True)

P("(a) author's height() against referee Decimal closed form")
rng = np.random.default_rng(3); worst = 0
for _ in range(300):
    n = rng.normal(size=3); n /= np.linalg.norm(n); d = rng.uniform(0.02, 0.98)
    if np.abs(n).min() < 2e-3: continue
    worst = max(worst, abs(F.height(n, d) - float(h_dec([D(float(x)) for x in n], D(float(d))))))
P("   300 random directions (all components > 2e-3), densities 0.02-0.98: largest difference %.2e" % worst)
P("   TINY: directions with one component just under / over 1e-4 (after normalising)")
for d in (0.1, 0.22, 0.3, 0.5):
    for base in ((1, 0.3), (1, 1.0), (1, 0.05)):
        row = []
        for c in (0.99e-4, 1.01e-4):
            n = np.array([base[0], base[1], 0.0]); n /= np.linalg.norm(n); n = np.array([n[0], n[1], c]); n /= np.linalg.norm(n)
            row.append(F.height(n, d) - float(h_dec([D(float(x)) for x in n], D(str(d)))))
        P("     d=%.2f up~(%g,%g,c): error with c=0.99e-4: %+.2e ; with c=1.01e-4: %+.2e" % (d, base[0], base[1], row[0], row[1]))
P("   TINY near face up (two small components 0.9e-4, 0.5e-4): error %+.2e" % (F.height([1, 0.9e-4, 0.5e-4], 0.3) - float(h_dec((1, D('0.9e-4'), D('0.5e-4')), D('0.3')))))

P("\n(b) is_local_min: dependence on test radius and on where the 36 points sit")
def ilm(n, d, r=0.01, m=36, off=0.0, aux=(1.0, 0.3, 0.2)):
    n = np.asarray(n, float) / np.linalg.norm(n); h0 = F.height(n, d)
    u = np.cross(n, aux); u /= np.linalg.norm(u); v = np.cross(n, u)
    return all(F.height(n * math.cos(r) + (u * math.cos(p) + v * math.sin(p)) * math.sin(r), d) > h0 + 1e-12 for p in np.linspace(0, 2 * math.pi, m, endpoint=False) + off)
def thr(test, lo, hi):
    for _ in range(40):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if test(mid) else (lo, mid)
    return (lo + hi) / 2
for r in (0.02, 0.01, 0.003, 0.001, 0.0003):
    P("   author's height(), radius %.4f: corner up 'local minimum from' %.6f ; face up 'until' %.6f" % (
        r, thr(lambda d: not ilm([1, 1, 1], d, r), 0.05, 0.3), thr(lambda d: ilm([1, 0, 0], d, r), 0.05, 0.4)))
P("   edge up at d=0.5, author's test as written: is_local_min =", F.is_local_min([1, 1, 0], 0.5))
for off in (0, 1, 2, 3, 4, 5, 6, 7, 8, 9):
    P("     36 points rotated by %d deg: edge up at 0.5 passes as local minimum: %s ; at 0.495: %s ; at 0.49: %s" % (
        off, ilm([1, 1, 0], 0.5, off=math.radians(off)), ilm([1, 1, 0], 0.495, off=math.radians(off)), ilm([1, 1, 0], 0.49, off=math.radians(off))))
grid = [round(0.02 + 0.005 * i, 3) for i in range(97)]
for off in (4, 5, 6):
    P("     rotated by %d deg: grid densities where edge up passes: %s" % (off, [d for d in grid if ilm([1, 1, 0], d, off=math.radians(off))]))
P("     with 360 points instead of 36 (as written otherwise): grid densities where edge up passes:", [d for d in grid if ilm([1, 1, 0], d, m=360)])

P("\n(c) the sliver: advantage of the diagonal-plane tilt over the surviving ties, Decimal 60 digits, and the author's double precision")
for ds in ('0.2266', '0.2267', '0.2268', '0.22685', '0.22689', '0.226892677'):
    d = D(ds); t, h = valley(d, 45); rh = ring_h(d)
    th = math.atan(float(t))
    ha = F.height([math.cos(th), math.sin(th) * math.sqrt(0.5), math.sin(th) * math.sqrt(0.5)], float(d))
    tr = math.atan(float(ring_t(d)))
    hb = F.height([math.cos(tr), math.sin(tr) * math.cos(0.3), math.sin(tr) * math.sin(0.3)], float(d))
    P("   d=%s: diag tilt %.4f deg; referee: h - ring = %+.3e ; author's height(): h(diag) - h(ring point at azimuth 17 deg) = %+.3e ; corner - diag = %+.3e" % (
        ds, math.degrees(th), h - rh, ha - hb, h_dec((1, 1, 1), d) - h))

P("\n(e) water plane at d=0.5 corner up (referee clipping): side lengths of the section polygon")
n = np.ones(3) / math.sqrt(3)
import itertools
verts = np.array(list(itertools.product([-0.5, 0.5], repeat=3)))
def section(L):
    pts = []
    for i in range(8):
        for j in range(i + 1, 8):
            if np.sum(np.abs(verts[i] - verts[j]) > 0) == 1:
                a, b = verts[i] @ n - L, verts[j] @ n - L
                if a * b < 0:
                    pts.append(verts[i] + a / (a - b) * (verts[j] - verts[i]))
    pts = np.array(pts); c = pts.mean(0); e1 = np.cross(n, [1, 0, 0]); e1 /= np.linalg.norm(e1); e2 = np.cross(n, e1)
    ang = np.arctan2((pts - c) @ e2, (pts - c) @ e1); pts = pts[np.argsort(ang)]
    return [float(np.linalg.norm(pts[k] - pts[(k + 1) % len(pts)])) for k in range(len(pts))]
P("   d=0.5 (plane through centre):", [round(x, 6) for x in section(0.0)])
from scipy.optimize import brentq
P("   d=0.3:", [round(x, 4) for x in section(-0.1023)], "(irregular hexagon, level approximate)")
