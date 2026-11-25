"""Checks made after the verdicts; none was on the sealed sheet.   usage: python after.py > after.out"""
import sys, os, json, math, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from scipy.integrate import solve_ivp
import impetus as I
R = json.load(open('results.json')); V = json.load(open('verdicts.json'))
print("1. Best elevation on a grid of 0.1 degrees")
for name, p in I.SHOTS.items():
    es = np.arange(15, 50.01, 0.1); rs = [I.fly(p['v0'], p['vt'], float(e))['range'] for e in es]; print(f"   {name}: {es[int(np.argmax(rs))]:.1f} degrees")
print("2. How long the shot keeps its line: the share of the range covered before its direction has dropped 10 degrees below the 45 degrees it was launched at (a parabola: 0.150)")
def kept(v0, vt):
    q = I.fly(v0, vt, 45, dense=True); P = np.array(q['path']); d = np.degrees(np.arctan2(np.gradient(P[:, 1]), np.gradient(P[:, 0]))); i = int(np.argmax(d < 35)); return P[i, 0] / q['range']
for name, p in I.SHOTS.items(): print(f"   {name}: {kept(p['v0'], p['vt']):.3f}")
print("   by launch speed over terminal velocity: " + ", ".join(f"{r}: {kept(100.0 * r, 100.0):.3f}" for r in (1, 2, 4, 6.6, 12, 40)))
print("3. If the drag coefficient rose near the speed of sound (an illustrative curve: 0.47 below Mach 0.6, rising in a straight line to 0.95 at Mach 1.1, 0.95 above), at 45 degrees and best elevation")
cd = lambda m: 0.47 if m < 0.6 else 0.95 if m > 1.1 else 0.47 + (0.95 - 0.47) * (m - 0.6) / 0.5
for name in ('musket ball', '24-pound shot'):
    p = I.SHOTS[name]; q = I.fly(p['v0'], p['vt'], 45, cd_of_mach=cd); best = max((I.fly(p['v0'], p['vt'], e, cd_of_mach=cd) for e in range(15, 50)), key=lambda z: z['range'])
    print(f"   {name}: range {q['range']:.0f} m ({q['range_fraction']:.4f}; constant Cd {R[name]['at45']['range']:.0f} m), apex fraction {q['apex_fraction']:.4f}, impact angle {q['impact_angle']:.1f}, best elevation {best['elev']} ({best['range']:.0f} m)")
print("4. The margins of the two narrow lines")
p = I.SHOTS['shuttlecock']
for v0 in (40, 50, 60, 70, 80): q = I.fly(v0, p['vt'], 45); print(f"   shuttlecock at {v0} m/s: apex fraction {q['apex_fraction']:.4f}, impact angle {q['impact_angle']:.2f}")
p = I.SHOTS['24-pound shot']; print("   24-pound shot, range by elevation: " + ", ".join(f"{e}: {I.fly(p['v0'], p['vt'], e)['range']:.1f}" for e in (31, 32, 33, 34, 35)))
print("5. Does the tolerance matter?  musket ball at 45 degrees, range in metres")
k = I.G / I.SHOTS['musket ball']['vt'] ** 2
for tol in (1e-6, 1e-9, 1e-12):
    def rhs(t, s): v = math.hypot(s[2], s[3]); return [s[2], s[3], -k * v * s[2], -I.G - k * v * s[3]]
    land = lambda t, s: s[1]; land.terminal = True; land.direction = -1
    sol = solve_ivp(rhs, [0, 200], [0, 0, 450 * math.cos(math.pi / 4), 450 * math.sin(math.pi / 4)], method='DOP853', rtol=tol, atol=tol, events=[land]); print(f"   tolerance {tol:g}: {sol.y_events[0][0][0]:.6f}")
print("6. My hand estimates on the sealed sheet against the computation, and my odds")
text = open('expectations.md').read(); odds = {m.group(1): float(m.group(2)) for m in re.finditer(r"^(J\d+)\..*?odds (0\.\d+)\s*$", text, re.M | re.S)}
y = np.array([1.0 if V['verdicts'][k] else 0.0 for k in sorted(odds, key=lambda k: int(k[1:]))]); o = np.array([odds[k] for k in sorted(odds, key=lambda k: int(k[1:]))])
print(f"   ten lines, {int(y.sum())} held; my mean odds {o.mean():.3f}; Brier score {((o - y) ** 2).mean():.4f} (a flat 0.9 would score {((0.9 - y) ** 2).mean():.4f})")
for lab, hand, got in (("musket range fraction", 0.05, R['musket ball']['at45']['range_fraction']), ("musket impact angle", 80, R['musket ball']['at45']['impact_angle']), ("musket apex fraction", 0.70, R['musket ball']['at45']['apex_fraction']),
                       ("24-pound range fraction", 0.20, R['24-pound shot']['at45']['range_fraction']), ("shuttlecock apex fraction", 0.77, R['shuttlecock']['at45']['apex_fraction']), ("shuttlecock impact angle", 85, R['shuttlecock']['at45']['impact_angle']), ("musket landing speed over terminal", 0.98, R['musket ball']['at45']['impact_over_vt'])):
    print(f"   {lab}: by hand {hand}, computed {got:.3f}")
