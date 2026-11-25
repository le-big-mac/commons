"""Afterwards: the closed form of the tilted ring, and what is lowest where the ring ends.   usage: python sliver.py"""
import sys, math, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import floating as F
from scipy.optimize import minimize, minimize_scalar

def tilt_dir(theta, phi):
    return np.array([math.cos(theta), math.sin(theta) * math.cos(phi), math.sin(theta) * math.sin(phi)])

# ---- the ring in closed form.  Under water: a square column of height d with a slanted top of slope tan(theta).
# h = [tan^2/(24 d) + (1 - d)/2] / sqrt(1 + tan^2), least at tan^2 = 12 d (1 - d) - 2, whichever way the slope faces,
# for as long as the water plane misses the bottom face: tan(theta) (|cos phi| + |sin phi|) <= 2 d.
print("the ring in closed form: tan^2(tilt) = 12 d (1 - d) - 2;  h = (1 - d - 1/(12 d)) / sqrt(12 d (1 - d) - 1)")
for d in (0.212, 0.215, 0.22, 0.225, 0.2265):
    s = 12 * d * (1 - d) - 2; th = math.atan(math.sqrt(s)); hf = (1 - d - 1 / (12 * d)) / math.sqrt(12 * d * (1 - d) - 1)
    num = minimize_scalar(lambda t: F.height(tilt_dir(t, 0.3), d), bounds=(0.0, math.pi / 6), method='bounded', options=dict(xatol=1e-13))
    print(f"   d = {d}: formula tilt {math.degrees(th):.3f} deg, h {hf:.9f};  search at azimuth 17 deg: tilt {math.degrees(num.x):.3f} deg, h {num.fun:.9f}")
end = (3 - math.sqrt(2)) / 7
print(f"the ring stays whole until the water plane reaches a bottom corner when tilting towards an edge: 7 d^2 - 6 d + 1 = 0, d = (3 - sqrt 2)/7 = {end:.6f}")
print(f"tilting towards a face it would reach the bottom edge only at tan = 2 d: 12 d (1 - d) - 2 = 4 d^2, d = {(3 - 1) / 8:.4f}")

# ---- what is lowest from there on: a fine scan
corner = F.canon(np.array([1.0, 1, 1]))
def lowest(d):
    best = None
    grid = [(t, p) for t in np.radians(np.arange(0.5, 60.01, 1.5)) for p in np.radians(np.arange(0, 45.01, 3.0))]
    vals = sorted((F.height(tilt_dir(t, p), d), t, p) for t, p in grid)
    for _, t, p in vals[:6]:
        r = minimize(lambda x: F.height(tilt_dir(x[0], x[1]), d), [t, p], method='Nelder-Mead', options=dict(xatol=1e-10, fatol=1e-14, maxiter=4000))
        if best is None or r.fun < best[0]: best = (r.fun, r.x[0], r.x[1])
    return best
print("fine scan: the lowest attitude found; tilt from a face normal and azimuth (0 = towards a face, 45 = towards an edge); h minus corner up's and minus the ring formula's, in millionths")
for d in [0.2262, 0.2264, 0.2265, 0.2266, 0.2267, 0.2268, 0.22685, 0.2269, 0.22695, 0.2270, 0.2272, 0.2275, 0.228]:
    h, t, p = lowest(d); w = F.canon(tilt_dir(t, p)); hc = F.height(corner, d); hr = (1 - d - 1 / (12 * d)) / math.sqrt(12 * d * (1 - d) - 1)
    pd = math.degrees(p) % 90; pd = min(pd, 90 - pd)
    print(f"   d = {d:.5f}: {F.kind(w):32s} tilt {math.degrees(t):6.2f}, azimuth {pd:5.1f};  minus corner up {1e6 * (h - hc):+8.2f};  minus ring {1e6 * (h - hr):+8.3f}")

def low_tilted(d):                                 # the lowest attitude short of corner up: tilts under 40 degrees, any azimuth
    best = 9.0
    for p in np.radians(np.arange(0, 45.01, 2.5)):
        r = minimize_scalar(lambda t: F.height(tilt_dir(t, p), d), bounds=(0.0, math.radians(40)), method='bounded', options=dict(xatol=1e-13))
        best = min(best, r.fun)
    return best
lo, hi = 0.2262, 0.2285
for _ in range(40):
    mid = (lo + hi) / 2
    lo, hi = (mid, hi) if low_tilted(mid) < F.height(corner, mid) else (lo, mid)
print(f"corner up becomes lower than every tilted attitude (tilt under 40 degrees, azimuths every 2.5 degrees) at d = {(lo + hi) / 2:.5f}")
