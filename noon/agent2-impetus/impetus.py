"""Cannonballs in air: point masses with drag proportional to the square of the speed.   usage: python impetus.py results.json
Model as in expectations.md: g = 9.81, rho = 1.225, Cd = 0.47 constant, level ground, no wind, spin or lift."""
import sys, json, math
import numpy as np
from scipy.integrate import solve_ivp
G, RHO, CD = 9.81, 1.225, 0.47
def sphere(mass=None, density=None, diameter=None):
    if mass is None: mass = density * math.pi * diameter ** 3 / 6
    r = (3 * mass / (4 * math.pi * density)) ** (1 / 3); area = math.pi * r * r
    return math.sqrt(2 * mass * G / (RHO * CD * area)), mass, 2 * r
SHOTS = {
    'musket ball': dict(vt=sphere(density=11340, diameter=0.018)[0], v0=450.0),
    '24-pound shot': dict(vt=sphere(mass=10.9, density=7800)[0], v0=450.0),
    'trebuchet stone': dict(vt=sphere(mass=100.0, density=2600)[0], v0=50.0),
    'shuttlecock': dict(vt=6.8, v0=60.0),
}
def fly(v0, vt, elev_deg, cd_of_mach=None, dense=False, max_step=np.inf):
    k = G / vt ** 2; a = math.radians(elev_deg)
    def rhs(t, s):
        vx, vy = s[2], s[3]; v = math.hypot(vx, vy); f = k * v * (cd_of_mach(v / 340.3) / CD if cd_of_mach else 1.0)
        return [vx, vy, -f * vx, -G - f * vy]
    land = lambda t, s: s[1]; land.terminal = True; land.direction = -1
    top = lambda t, s: s[3]; top.direction = -1
    sol = solve_ivp(rhs, [0, 4 * v0 / G + 10], [0, 0, v0 * math.cos(a), v0 * math.sin(a)], method='DOP853', rtol=1e-9, atol=1e-9, events=[land, top], dense_output=dense, max_step=max_step)
    xe, ye, vxe, vye = sol.y_events[0][0]; xa, ya = sol.y_events[1][0][:2]
    out = dict(elev=elev_deg, range=float(xe), range_fraction=float(xe / (v0 ** 2 * math.sin(2 * a) / G)), apex_fraction=float(xa / xe), apex_height=float(ya),
               impact_angle=float(math.degrees(math.atan2(-vye, vxe))), impact_speed=float(math.hypot(vxe, vye)), impact_over_vt=float(math.hypot(vxe, vye) / vt), time=float(sol.t_events[0][0]))
    if dense:
        ts = np.linspace(0, sol.t_events[0][0], 400); out['path'] = [[float(x), float(y)] for x, y in zip(*sol.sol(ts)[:2])]
    return out
if __name__ == '__main__':
    res = {}
    for name, p in SHOTS.items():
        sweep = [fly(p['v0'], p['vt'], e) for e in range(5, 86)]; best = max(sweep, key=lambda q: q['range']); at45 = fly(p['v0'], p['vt'], 45, dense=True)
        res[name] = dict(vt=p['vt'], v0=p['v0'], sweep=sweep, best_elevation=best['elev'], best_range=best['range'], at45=at45)
        print(f"{name}: terminal velocity {p['vt']:.1f} m/s, launched at {p['v0']:.0f} m/s ({p['v0'] / p['vt']:.2f} times it)")
        print(f"   at 45 degrees: range {at45['range']:.1f} m = {at45['range_fraction']:.4f} of the vacuum range; apex at {at45['apex_fraction']:.4f} of the range, {at45['apex_height']:.1f} m up; lands at {at45['impact_angle']:.2f} degrees, {at45['impact_speed']:.2f} m/s = {at45['impact_over_vt']:.4f} of terminal; {at45['time']:.2f} s")
        print(f"   best elevation {best['elev']} degrees (range {best['range']:.1f} m; at 45: {at45['range']:.1f} m); apex fraction over all elevations {min(q['apex_fraction'] for q in sweep):.4f} to {max(q['apex_fraction'] for q in sweep):.4f}; least (impact angle - elevation) {min(q['impact_angle'] - q['elev'] for q in sweep):.3f} degrees")
    # the whole family at 45 degrees: everything depends only on v0 / vt
    fam = []
    for ratio in [0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 1, 1.5, 2, 3, 4, 5, 6.6, 8.8, 12, 20, 40]:
        v0 = 100.0 * ratio; ms = lambda e: 2 * v0 * math.sin(math.radians(e)) / G / 40          # short flights need a ceiling on the step, or the landing is found at the start
        q = fly(v0, 100.0, 45, max_step=ms(45)); best = max((fly(v0, 100.0, e, max_step=ms(e)) for e in range(5, 86)), key=lambda z: z['range'])
        fam.append(dict(ratio=ratio, range_fraction=q['range_fraction'], apex_fraction=q['apex_fraction'], impact_angle=q['impact_angle'], impact_over_vt=q['impact_over_vt'], best_elevation=best['elev']))
    res['family'] = fam
    print("launch speed over terminal velocity; at 45 degrees: range fraction, apex fraction, impact angle, landing speed over terminal; best elevation")
    for f in fam: print(f"   {f['ratio']:5.2f}: {f['range_fraction']:.4f}  {f['apex_fraction']:.4f}  {f['impact_angle']:6.2f}  {f['impact_over_vt']:.4f}  {f['best_elevation']}")
    json.dump(res, open(sys.argv[1], 'w'))
