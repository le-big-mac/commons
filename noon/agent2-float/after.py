"""After the referee: the checks it proposed, redone with my own code.   usage: python after.py > after.out"""
import sys, math, os, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import floating as F
from scipy.optimize import minimize_scalar

def thr(test, lo, hi, n=45):
    for _ in range(n):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if test(mid) else (lo, mid)
    return (lo + hi) / 2
def tilt_dir(theta, phi):
    return np.array([math.cos(theta), math.sin(theta) * math.cos(phi), math.sin(theta) * math.sin(phi)])
def circle(n, r, m):
    n = np.asarray(n, float) / np.linalg.norm(n); u = np.cross(n, [1.0, 0.3, 0.2]); u /= np.linalg.norm(u); v = np.cross(n, u)
    return [n * math.cos(r) + (u * math.cos(p) + v * math.sin(p)) * math.sin(r) for p in np.linspace(0, 2 * math.pi, m, endpoint=False)]
def is_min(n, d, r, m=36):
    h0 = F.height(n, d); return all(F.height(x, d) > h0 + 1e-13 for x in circle(n, r, m))
corner = np.ones(3) / math.sqrt(3); face = np.array([1.0, 0, 0]); edge = np.array([1.0, 1, 0]) / math.sqrt(2)
ring_h = lambda d: (1 - d - 1 / (12 * d)) / math.sqrt(12 * d * (1 - d) - 1)
lean = lambda d: math.atan(math.sqrt(12 * d * (1 - d) - 2))

print("1. Corner up: the density from which it passes the local-minimum test, by the radius of the test circle (radians)")
for r in (0.02, 0.01, 0.003, 0.001, 0.0003, 0.0001):
    print(f"   radius {r}: from {thr(lambda d: not is_min(corner, d, r), 0.12, 0.25):.5f}" + (f"   (the same for face up: until {thr(lambda d: is_min(face, d, r), 0.1, 0.3):.6f})" if r >= 0.001 else "   (face up: differences too small for the test at this radius)"))
print(f"   1/6 = {1 / 6:.5f}: where the corner-up water line reaches three vertices and turns from a triangle into a hexagon")
print("2. How wide the hollow round corner up is: the smallest angle from it at which some direction is lower")
for d in (0.168, 0.17, 0.18, 0.19, 0.20, 0.21, 0.22):
    h0 = F.height(corner, d); w = next((r for r in np.arange(0.002, 0.7, 0.002) if any(F.height(x, d) < h0 for x in circle(corner, r, 72))), None)
    print(f"   d = {d}: " + (f"{math.degrees(w):.1f} degrees" if w else "none within 40 degrees"))

print("3. The sliver: how much lower the tilt towards an edge is than the ring formula, in trillionths (1e-12 of the side)")
def diag_low(d):
    return minimize_scalar(lambda t: F.height(tilt_dir(t, math.pi / 4), d), bounds=(0.2, 0.5), method='bounded', options=dict(xatol=1e-14)).fun
take = thr(lambda d: diag_low(d) < F.height(corner, d), 0.2262, 0.2285)
for d in (0.2266, 0.2267, 0.2268, 0.22685, take):
    print(f"   d = {d:.6f}: {1e12 * (diag_low(d) - ring_h(d)):+.1f}")
print(f"   corner up overtakes the tilt towards an edge at d = {take:.6f}")

print("4. After the takeover: the tilt towards an edge as a separate stable attitude")
def diag_min(d):                                   # an interior local minimum of h along the diagonal plane, tilt under 45 degrees
    ths = np.radians(np.arange(8, 45.001, 0.05)); hs = np.array([F.height(tilt_dir(t, math.pi / 4), d) for t in ths])
    i = [k for k in range(1, len(ths) - 1) if hs[k] < hs[k - 1] and hs[k] < hs[k + 1]]
    if not i: return None
    r = minimize_scalar(lambda t: F.height(tilt_dir(t, math.pi / 4), d), bounds=(ths[i[0] - 1], ths[i[0] + 1]), method='bounded', options=dict(xatol=1e-13))
    return math.degrees(r.x), r.fun
endd = thr(lambda d: diag_min(d) is not None, 0.23, 0.25, 30)
for d in (0.2268, 0.228, 0.23, 0.235, 0.2375):
    t, h = diag_min(d); n = tilt_dir(math.radians(t), math.pi / 4)
    print(f"   d = {d}: tilt {t:.2f} degrees, h = {h:.9f}, {1e6 * (h - F.height(corner, d)):+.0f} millionths above corner up; passes the test at radius 0.003 with 360 points: {is_min(n, d, 0.003, 360)}; curvature across the diagonal plane {2 * (F.height(tilt_dir(math.radians(t), math.pi / 4 + 0.01), d) - h) / (0.01 * math.sin(math.radians(t))) ** 2:+.5f} per radian squared")
print(f"   it exists up to d = {endd:.5f} (tilt {diag_min(endd - 1e-5)[0]:.1f} degrees there)")
print("5. What is left of the ring after 0.2265: an arc round each towards-a-face direction where the formula still holds, tan(tilt) (cos phi + sin phi) <= 2 d")
for d in (0.2265, 0.23, 0.235, 0.24, 0.245, 0.2499):
    x = 2 * d / math.tan(lean(d)) / math.sqrt(2); half = 45 - math.degrees(math.acos(min(1.0, x)))
    inside = minimize_scalar(lambda t: F.height(tilt_dir(t, math.radians(max(half - 1, 0) * 0.9)), d), bounds=(0.05, 0.6), method='bounded', options=dict(xatol=1e-14)).fun
    beyond = minimize_scalar(lambda t: F.height(tilt_dir(t, math.radians(half + 3)), d), bounds=(0.05, 0.6), method='bounded', options=dict(xatol=1e-14)).fun
    print(f"   d = {d}: half-width {half:5.1f} degrees; inside the arc h minus formula {1e12 * (inside - ring_h(d)):+.2f} trillionths; 3 degrees beyond its end {1e9 * (beyond - ring_h(d)):+.1f} billionths")
print("   the arc closes at 12 d (1 - d) - 2 = 4 d^2, d = 1/4")

print("6. Edge up: curvature of h towards a face (rolling) and towards a corner, per radian squared, from second differences at 0.003 rad")
both = []
for d in [round(0.02 + 0.001 * i, 3) for i in range(481)]:
    h0 = F.height(edge, d); r = 0.003
    roll = (F.height(edge * math.cos(r) + np.array([1, -1, 0]) / math.sqrt(2) * math.sin(r), d) + F.height(edge * math.cos(r) - np.array([1, -1, 0]) / math.sqrt(2) * math.sin(r), d) - 2 * h0) / r ** 2
    tip = 2 * (F.height(edge * math.cos(r) + np.array([0, 0, 1.0]) * math.sin(r), d) - h0) / r ** 2
    if roll > 0 and tip > 0: both.append(d)
    if d in (0.05, 0.1, 0.125, 0.15, 0.2, 0.25, 0.28, 0.285, 0.3, 0.4, 0.45, 0.49, 0.5): print(f"   d = {d}: rolling {roll:+.4f}, towards a corner {tip:+.4f}")
print(f"   densities from 0.020 to 0.500 in steps of 0.001 at which both are positive: {both}")
print("   at 0.5, towards a corner: (h - h at edge up) / angle^3 = " + ", ".join(f"{(F.height(edge * math.cos(t) + np.array([0, 0, 1.0]) * math.sin(t), 0.5) - F.height(edge, 0.5)) / t ** 3:.5f} at {t}" for t in (0.01, 0.02, 0.05)) + f"   (-1/48 = {-1 / 48:.5f})")
low = [k for k, x in enumerate(circle(edge, 0.01, 3600)) if F.height(x, 0.5) < F.height(edge, 0.5)]
print(f"   at 0.5 on a circle of 0.01 rad round edge up, h is lower on {len(low) / 10:.1f} of 360 degrees; the registered 36-point test sees it: {not F.is_local_min(edge, 0.5)}")

print("7. The square beam's tilt between its thresholds: search against tan^2 = 12 d (1 - d) - 2 (to 1/4) and sin 2 tilt = 16 d / (9 - 16 d) (from 1/4)")
for d in (0.212, 0.215, 0.22, 0.24, 0.25, 0.26, 0.27, 0.28, 0.281):
    ang = np.linspace(0, math.pi / 4, 20001); hs = [F.height([math.cos(a), math.sin(a)], d) for a in ang]; num = math.degrees(ang[int(np.argmin(hs))])
    form = math.degrees(lean(d)) if d <= 0.25 else math.degrees(math.asin(16 * d / (9 - 16 * d)) / 2)
    print(f"   d = {d}: search {num:.2f} degrees, formula {form:.2f}")

print("8. Corner up: the sides of the water line")
V = np.array(list(itertools.product([0.0, 1.0], repeat=3)))
def section(n, d):
    w = np.abs(n); lo, hi = 0.0, w.sum()
    def vol(t):
        sums = np.array([sum(c) for r in range(4) for c in itertools.combinations(w, r)]); sign = np.array([(-1) ** r for r in range(4) for _ in itertools.combinations(w, r)])
        return (sign * np.maximum(0, t - sums) ** 3).sum() / (6 * np.prod(w))
    for _ in range(60):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if vol(mid) < d else (lo, mid)
    t = (lo + hi) / 2; pts = []
    for a, b in itertools.combinations(range(8), 2):
        if np.abs(V[a] - V[b]).sum() == 1 and (V[a] @ n - t) * (V[b] @ n - t) < 0:
            s = (t - V[a] @ n) / ((V[b] - V[a]) @ n); pts.append(V[a] + s * (V[b] - V[a]))
    pts = np.array(pts); c = pts.mean(0); e1 = np.cross(n, [1, 0, 0.0]); e1 /= np.linalg.norm(e1); e2 = np.cross(n, e1)
    o = np.argsort(np.arctan2((pts - c) @ e2, (pts - c) @ e1)); pts = pts[o]
    return [float(np.linalg.norm(pts[i] - pts[(i + 1) % len(pts)])) for i in range(len(pts))]
for d in (0.1, 0.2, 0.3, 0.5):
    print(f"   d = {d}: " + ", ".join(f"{x:.4f}" for x in section(corner, d)))

print("9. Margins at d = 0.22, in units of the side")
print(f"   the ring is {F.height(face, 0.22) - ring_h(0.22):.6f} below face up and {F.height(corner, 0.22) - ring_h(0.22):.6f} below corner up")
print(f"   at d = 0.3 corner up is {F.height(face, 0.3) - F.height(corner, 0.3):.4f} below face up; at 0.5, {F.height(face, 0.5) - F.height(corner, 0.5):.4f}; edge up at 0.5 is {F.height(edge, 0.5) - F.height(corner, 0.5):.4f} above corner up")
print("10. The shortcut TINY: h at 0.22 on the ring, at azimuths either side of the cut-off, minus the formula, in billionths")
for comp in (0.5e-4, 0.9e-4, 1.1e-4, 2e-4, 1e-3):
    t = lean(0.22); n = np.array([math.cos(t), math.sqrt(math.sin(t) ** 2 - comp ** 2), comp])
    print(f"   smallest component {comp:.1e}: {1e9 * (F.height(n, 0.22) - ring_h(0.22)):+.3f}")
