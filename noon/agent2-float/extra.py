"""Afterwards: the tilted family, and where each state takes over.   usage: python extra.py"""
import sys, math, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import floating as F
from scipy.optimize import minimize_scalar
def tilt_dir(theta, phi):
    """up direction tilted by theta from a face normal, towards azimuth phi (0 = towards a face, 45 degrees = towards an edge)"""
    return [math.cos(theta), math.sin(theta) * math.cos(phi), math.sin(theta) * math.sin(phi)]
def best_tilt(d, phi):
    r = minimize_scalar(lambda th: F.height(tilt_dir(th, phi), d), bounds=(0.0, math.pi / 3), method='bounded', options=dict(xatol=1e-13))
    return r.fun, math.degrees(r.x)
print("the lowest tilt at each azimuth (0 = tilting towards a face, 45 = towards an edge): tilt angle, and h minus h at azimuth 0, in billionths")
for d in (0.212, 0.215, 0.22, 0.225, 0.2265, 0.24):
    h0, t0 = best_tilt(d, 0.0)
    print(f"   d = {d}: tilt {t0:.3f} deg at azimuth 0; " + "; ".join(f"{a}: {best_tilt(d, math.radians(a))[1]:.3f} deg, {1e9 * (best_tilt(d, math.radians(a))[0] - h0):+.1f}" for a in (5, 15, 25, 35, 45)))
def thr(test, lo, hi):
    for _ in range(45):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if test(mid) else (lo, mid)
    return (lo + hi) / 2
corner = F.canon(np.array([1.0, 1, 1])); face = F.canon(np.array([1.0, 0, 0]))
def tilted_low(d):                                 # the tilted family proper: tilts of under 30 degrees, towards a face
    return minimize_scalar(lambda th: F.height(tilt_dir(th, 0.0), d), bounds=(0.0, math.pi / 6), method='bounded', options=dict(xatol=1e-13)).fun
x = thr(lambda d: tilted_low(d) < F.height(corner, d), 0.215, 0.24)
print(f"corner up becomes lower than the tilted family at d = {x:.5f}; lower than face up at {thr(lambda d: F.height(face, d) < F.height(corner, d), 0.1, 0.4):.5f}")
print(f"corner up is a local minimum from d = {thr(lambda d: not F.is_local_min([1, 1, 1], d), 0.05, 0.3):.5f}; face up until {thr(lambda d: F.is_local_min([1, 0, 0], d), 0.05, 0.4):.5f} = (3 - sqrt 3)/6 = {(3 - math.sqrt(3)) / 6:.5f}")
grid = [round(0.02 + 0.005 * i, 3) for i in range(97)]
print("edge up is a local minimum at these densities of the grid:", [d for d in grid if F.is_local_min([1, 1, 0], d)])
print("edge up at d = 0.5: h on a small circle round it, minus h at edge up, in millionths:", [round(1e6 * (F.height(np.array([1, 1, 0]) / math.sqrt(2) * math.cos(0.02) + np.array(v) * math.sin(0.02), 0.5) - F.height([1, 1, 0], 0.5)), 2)
                                                                                                       for v in ([0, 0, 1.0], [1 / math.sqrt(2), -1 / math.sqrt(2), 0])])
for d in (0.3, 0.5):
    w = np.abs(corner); t_lo, t_hi = 0.0, w.sum()
    print(f"corner up at d = {d}: h = {F.height(corner, d):.6f}; the water plane is a {'hexagon' if 1/6 < d < 5/6 else 'triangle'}")

print("how far round the family is exactly level: largest azimuth (degrees from a face direction) at which the lowest tilt is still as low as at azimuth 0, to a billionth")
for d in (0.212, 0.215, 0.22, 0.225, 0.2265):
    h0 = best_tilt(d, 0.0)[0]
    ok = [a for a in range(0, 46) if abs(best_tilt(d, math.radians(a))[0] - h0) < 1e-9]
    print(f"   d = {d}: level out to {max(ok)} degrees" + (" (all the way round)" if max(ok) == 45 else ""))
