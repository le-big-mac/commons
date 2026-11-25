"""After the referee: its controls redone with my code.   usage: python after2.py > after2.out"""
import sys, os, json, math, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import impetus as I
R = json.load(open('results.json')); V = json.load(open('verdicts.json'))
ms = lambda v0, e: 2 * v0 * math.sin(math.radians(e)) / I.G / 40
print("1. Very fast shots at 45 degrees: launch speed over terminal velocity; apex fraction; impact angle")
for ratio in (40, 100, 1000, 10000):
    q = I.fly(100.0 * ratio, 100.0, 45, max_step=ms(100.0 * ratio, 45) if ratio < 100 else np.inf); print(f"   {ratio:6d}: {q['apex_fraction']:.4f}  {q['impact_angle']:.2f}")
print("2. The fall as a whole, and other elevations")
for name in ('musket ball', '24-pound shot'):
    p = I.SHOTS[name]; q = I.fly(p['v0'], p['vt'], 45, dense=True); P = np.array(q['path']); it = int(np.argmax(P[:, 1]))
    chord = math.degrees(math.atan2(P[it, 1], q['range'] - P[it, 0])); d = np.degrees(np.arctan2(-np.gradient(P[:, 1]), np.gradient(P[:, 0]))); steep = P[it:, 1][d[it:] > 80]
    print(f"   {name} at 45: the straight line from the top to the landing slopes at {chord:.0f} degrees; the path is steeper than 80 degrees for the last {100 * (steep.max() / P[it, 1] if len(steep) else 0):.0f}% of the drop")
    b = I.fly(p['v0'], p['vt'], R[name]['best_elevation']); print(f"   {name} at its best elevation ({R[name]['best_elevation']}): lands at {b['impact_angle']:.0f} degrees and {b['impact_over_vt']:.2f} of terminal velocity")
    for e in (5, 10): b = I.fly(p['v0'], p['vt'], e); print(f"   {name} at {e} degrees: lands at {b['impact_angle']:.0f} degrees and {b['impact_over_vt']:.2f} of terminal velocity; range fraction {b['range_fraction']:.3f}")
print("3. One measure of which picture a path is nearer: the area under it, drawn to its own range (a parabola at 45 degrees: 1/6 = 0.167; straight out at 45 degrees and straight down: 0.5)")
def area(v0, vt):
    q = I.fly(v0, vt, 45, dense=True); P = np.array(q['path']) / q['range']; return float(np.sum((P[1:, 0] - P[:-1, 0]) * (P[1:, 1] + P[:-1, 1]) / 2))
for name, p in I.SHOTS.items(): a = area(p['v0'], p['vt']); print(f"   {name}: {a:.3f}  ({(a - 1 / 6) / (0.5 - 1 / 6):.2f} of the way from the parabola to the other)")
print("4. Keeping its line (direction 10 degrees below the launch), on a fine path, as a share of the range and in metres")
def kept(v0, vt, n=20000):
    q = I.fly(v0, vt, 45, dense=True); k = I.G / vt ** 2
    from scipy.integrate import solve_ivp
    def rhs(t, s): v = math.hypot(s[2], s[3]); return [s[2], s[3], -k * v * s[2], -I.G - k * v * s[3]]
    ev = lambda t, s: s[3] - math.tan(math.radians(35)) * s[2]; ev.terminal = True; ev.direction = -1
    sol = solve_ivp(rhs, [0, q['time']], [0, 0, v0 * math.cos(math.pi / 4), v0 * math.sin(math.pi / 4)], method='DOP853', rtol=1e-10, atol=1e-10, events=[ev]); x = sol.y_events[0][0][0]
    return x / q['range'], x
for name, p in I.SHOTS.items(): s, x = kept(p['v0'], p['vt']); print(f"   {name}: {s:.3f} of the range, {x:.0f} m (in a vacuum at the same speed: {0.15 * p['v0'] ** 2 / I.G:.0f} m)")
print("5. Reynolds numbers at terminal velocity (speed x diameter / 1.5e-5), and ranges at 45 degrees with a smaller drag coefficient")
for name, dens, mass, diam in (('musket ball', 11340, None, 0.018), ('24-pound shot', 7800, 10.9, None), ('trebuchet stone', 2600, 100.0, None)):
    vt, m, d = I.sphere(mass=mass, density=dens, diameter=diam); print(f"   {name}: diameter {d:.3f} m, Reynolds number {vt * d / 1.5e-5:,.0f} at terminal velocity, {I.SHOTS[name]['v0'] * d / 1.5e-5:,.0f} at launch")
for name in ('24-pound shot', 'trebuchet stone'):
    p = I.SHOTS[name]
    for cd in (0.3, 0.2):
        vt = p['vt'] * math.sqrt(I.CD / cd); q = I.fly(p['v0'], vt, 45); best = max((I.fly(p['v0'], vt, e) for e in range(20, 50)), key=lambda z: z['range'])
        print(f"   {name} with Cd = {cd}: range {q['range']:.0f} m ({q['range_fraction']:.3f}), best elevation {best['elev']}")
print("6. A three-part figure (a straight line at 45 degrees of length S, an arc of radius r, a vertical line) has its top at (S + r) / (S + 2.414 r) of its range")
print("   " + ", ".join(f"S = {s} r: {(s + 1) / (s + 1 + math.sqrt(2)):.2f}" for s in (1, 2, 2.4, 5, 10)))
print("7. The scorecard read the other way")
text = open('expectations.md').read(); odds = {m.group(1): float(m.group(2)) for m in re.finditer(r"^(J\d+)\..*?odds (0\.\d+)\s*$", text, re.M | re.S)}
ids = sorted(odds, key=lambda k: int(k[1:])); o = np.array([odds[k] for k in ids]); y = np.ones(10); y2 = y.copy(); y2[ids.index('J6')] = 0
print(f"   Brier score with J6 held {((o - y) ** 2).mean():.4f}; with J6 failed {((o - y2) ** 2).mean():.4f}; the product of my ten odds {np.prod(o):.2f}")
p = I.SHOTS['musket ball']; print("   musket ball, range at 27 and 28 degrees: " + ", ".join(f"{I.fly(p['v0'], p['vt'], e)['range']:.3f} m" for e in (27, 28)))
