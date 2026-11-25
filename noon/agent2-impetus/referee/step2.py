"""Referee step 2: controls and alternative definitions. Own integrator in units of vt (speed), vt^2/g (length), vt/g (time).
In those units the model is  dv/dt = -(0,1) - c |v| v  with c = 1 (constant Cd), started at r = v0/vt and the elevation."""
import sys, hashlib
import numpy as np
from math import pi, sqrt, sin, cos, atan2, atan, degrees, radians, tan, log
from scipy.integrate import solve_ivp
from scipy.optimize import minimize_scalar

G, RHO, CD = 9.81, 1.225, 0.47


def fly(r, elev, rtol=1e-11, cfun=None, extra_events=(), dense=False):
    """r = v0/vt. Returns dict in nondimensional units (lengths in vt^2/g)."""
    th = radians(elev)

    def f(t, s):
        v = sqrt(s[2] ** 2 + s[3] ** 2)
        c = 1.0 if cfun is None else cfun(v)
        return [s[2], s[3], -c * v * s[2], -1.0 - c * v * s[3]]

    def apex(t, s): return s[3]
    apex.direction = -1

    def land(t, s): return s[1]
    land.direction = -1; land.terminal = True
    tmax = 2 * r * sin(th) * 1.5 + 60
    # first step must be small compared with the flight (the author's first-run failure mode)
    sol = solve_ivp(f, (0, tmax), [0, 0, r * cos(th), r * sin(th)], method="DOP853", rtol=rtol, atol=1e-13,
                    events=[apex, land] + list(extra_events), first_step=min(1e-3 / max(r, 1e-9), 1e-2 * r * sin(th)), dense_output=dense)
    assert len(sol.t_events[1]) == 1 and len(sol.t_events[0]) >= 1
    xa, ya = sol.y_events[0][0][:2]
    xl, yl, vxl, vyl = sol.y_events[1][0]
    vac = r * r * sin(2 * th)
    return dict(R=xl, rf=xl / vac, af=xa / xl, ya=ya, ang=degrees(atan2(-vyl, vxl)), vl=sqrt(vxl ** 2 + vyl ** 2), sol=sol,
                ta=sol.t_events[0][0], tl=sol.t_events[1][0])


def vt_sphere(mass=None, density=None, diameter=None):
    if mass is None:
        mass = density * pi * diameter ** 3 / 6
    rad = (3 * mass / (4 * pi * density)) ** (1 / 3)
    return sqrt(2 * mass * G / (RHO * CD * pi * rad * rad)), 2 * rad


VT = {"musket": vt_sphere(density=11340, diameter=0.018)[0], "shot24": vt_sphere(mass=10.9, density=7800)[0],
      "stone": vt_sphere(mass=100.0, density=2600)[0], "shuttle": 6.8}
V0 = {"musket": 450.0, "shot24": 450.0, "stone": 50.0, "shuttle": 60.0}
RAT = {k: V0[k] / VT[k] for k in VT}
L = {k: VT[k] ** 2 / G for k in VT}


def best_whole(r, lo=5, hi=85, cfun=None):
    return max(range(lo, hi + 1), key=lambda e: fly(r, e, rtol=1e-10, cfun=cfun)["R"])


def best_cont(r, cfun=None):
    res = minimize_scalar(lambda e: -fly(r, e, cfun=cfun)["R"], bounds=(10, 50), method="bounded", options=dict(xatol=1e-4))
    return res.x


P = print
P("== 0. sha256 of expectations.md (for comparison with the board, which I may not read)")
P("  ", hashlib.sha256(open("/home/agent2/impetus/expectations.md", "rb").read()).hexdigest())

P("== 1. tolerance: musket ball range at 45 deg in metres, my integrator")
for tol in (1e-6, 1e-8, 1e-10, 1e-13):
    P(f"   rtol {tol:g}: {fly(RAT['musket'], 45, rtol=tol)['R'] * L['musket']:.7f}")

P("== 2. is the shape a function of v0/vt alone (at a given elevation)?  24-pound shot's ratio with vt irrelevant by construction;")
P("   so instead: dimensional check with blind.py's integrator, vt=156.78 & v0=450 against vt=10 & v0=10*ratio")
sys.path.insert(0, "/home/agent2/impetus/referee")
import blind as B
a = B.fly(450.0, 45, VT["shot24"]); b = B.fly(10 * RAT["shot24"], 45, 10.0)
P(f"   range fraction {a[0] / (450**2 / G):.8f} vs {b[0] / ((10 * RAT['shot24'])**2 / G):.8f}; apex fraction {a[1] / a[0]:.8f} vs {b[1] / b[0]:.8f}; impact {a[2]:.6f} vs {b[2]:.6f}")
P("   but two numbers, not one: same ratio 6.608, different elevations -> apex fraction, impact angle, range fraction:")
for e in (5, 15, 28, 45, 60, 75, 85):
    q = fly(RAT["musket"], e); P(f"     elev {e:2d}: apex {q['af']:.4f}  impact {q['ang']:6.2f}  range fraction {q['rf']:.4f}  lands at {q['vl']:.3f} vt")

P("== 3. the family table (45 deg): ratio, range fraction, apex fraction, impact angle, landing speed/vt, best whole degree")
for r in (0.1, 0.3, 1 / 3, RAT["stone"], 1, 2, 4, 6.6, 12, 40):
    q = fly(r, 45); P(f"   {r:7.4f}: {q['rf']:.4f}  {q['af']:.4f}  {q['ang']:6.2f}  {q['vl']:.4f}  {best_whole(r, 15, 50)}")
P("   ratio at which the 45-degree range is exactly 7% short of vacuum:")
lo, hi = 0.2, 0.4
for _ in range(40):
    mid = (lo + hi) / 2
    if fly(mid, 45)["rf"] > 0.93: lo = mid
    else: hi = mid
P(f"     {lo:.4f}")
P("   trebuchet stone, range fraction by elevation: " + ", ".join(f"{e}: {fly(RAT['stone'], e)['rf']:.4f}" for e in (5, 15, 30, 45, 60, 75, 85)))

P("== 4. 'the highest point never gets near the far end': apex fraction and impact angle at 45 deg for very large ratios")
for r in (40, 100, 1e3, 1e4, 1e6, 1e9, 1e12):
    q = fly(r, 45); P(f"   ratio {r:8.0e}: apex fraction {q['af']:.4f}  impact {q['ang']:.2f}  range fraction {q['rf']:.2e}  1/(1-apex) {1 / (1 - q['af']):.3f}  ln r {log(r):.2f}")

P("== 5. 'fast shots do come down nearly vertically, at close to terminal velocity': by elevation")
for k in ("musket", "shot24", "shuttle"):
    P(f"   {k}: " + "; ".join(f"{e} deg: {fly(RAT[k], e)['ang']:.1f} deg, {fly(RAT[k], e)['vl']:.2f} vt" for e in (5, 10, 15, 20, 30, 45, 60)))

P("== 6. how vertical is the fall as a whole (45 deg launch)?")
for k in ("stone", "shot24", "musket", "shuttle"):
    r = RAT[k]

    def mk(deg):
        def ev(t, s): return atan2(s[3], s[2]) + radians(deg)   # zero when direction = deg below horizontal
        ev.direction = -1
        return ev
    q = fly(r, 45, extra_events=[mk(60), mk(70), mk(80)])
    s = q["sol"]
    chord_up = degrees(atan(q["ya"] / (q["af"] * q["R"]))); chord_dn = degrees(atan(q["ya"] / ((1 - q["af"]) * q["R"])))
    parts = []
    for i, d in enumerate((60, 70, 80)):
        ye = s.y_events[2 + i]
        parts.append(f"steeper than {d} for the last {ye[0][1] / q['ya']:.2f} of the drop" if len(ye) else f"never steeper than {d}")
    P(f"   {k}: apex height/range {q['ya'] / q['R']:.3f}; chord launch->apex {chord_up:.1f} deg, chord apex->landing {chord_dn:.1f} deg (parabola 26.6 both); " + "; ".join(parts))

P("== 7. share of the range covered before the direction has dropped by d degrees from 45 (exact event, not a 400-point path)")
for d in (5, 10, 20):
    def ev(t, s, d=d): return atan2(s[3], s[2]) - radians(45 - d)
    ev.direction = -1
    row = []
    for name, r in (("parabola~", 1e-4), ("stone", RAT["stone"]), ("shot24", RAT["shot24"]), ("musket", RAT["musket"]), ("shuttle", RAT["shuttle"]), ("ratio 40", 40.0)):
        q = fly(r, 45, extra_events=[ev]); row.append(f"{name} {q['sol'].y_events[2][0][0] / q['R']:.3f}")
    P(f"   drop of {d}: " + ", ".join(row))

P("== 8. the author's Mach curve (0.47 below M0.6, linear to 0.95 at M1.1, 0.95 above; sound 340.3 m/s)")
def cdm(m): return 0.47 if m < 0.6 else 0.95 if m > 1.1 else 0.47 + 0.48 * (m - 0.6) / 0.5
for k in ("musket", "shot24"):
    cf = lambda v, k=k: cdm(v * VT[k] / 340.3) / CD
    q = fly(RAT[k], 45, cfun=cf); q0 = fly(RAT[k], 45)
    P(f"   {k}: range {q['R'] * L[k]:.1f} m (constant Cd {q0['R'] * L[k]:.1f}); apex {q['af']:.4f} ({q['af'] - q0['af']:+.4f}); impact {q['ang']:.2f} ({q['ang'] - q0['ang']:+.2f}); best whole degree {best_whole(RAT[k], 15, 50, cfun=cf)}")

P("== 9. best elevation, continuous")
for k in ("stone", "shot24", "musket", "shuttle"):
    P(f"   {k}: {best_cont(RAT[k]):.3f}")
P("   24-pound shot: what would push the whole-degree best below 33? best whole degree by launch speed:")
P("     " + ", ".join(f"{v} m/s: {best_whole(v / VT['shot24'], 25, 40)}" for v in (430, 450, 470, 490, 510, 530)))
P("     by iron density (mass 10.9 kg): " + ", ".join(f"{d}: {best_whole(450 / vt_sphere(mass=10.9, density=d)[0], 25, 40)}" for d in (7000, 7200, 7500, 7800, 7870)))

P("== 10. shuttlecock apex fraction by launch speed")
P("   " + ", ".join(f"{v}: {fly(v / 6.8, 45)['af']:.4f}" for v in (50, 55, 56, 57, 58, 60)))

P("== 11. drag crisis sensitivity (constant Cd other than 0.47 for the big spheres; Reynolds numbers at vt with nu=1.46e-5)")
for k, d in (("musket", 0.018), ("shot24", vt_sphere(mass=10.9, density=7800)[1]), ("stone", vt_sphere(mass=100.0, density=2600)[1])):
    P(f"   {k}: diameter {d * 1000:.1f} mm; Re at vt {VT[k] * d / 1.46e-5:.2e}; Re at launch {V0[k] * d / 1.46e-5:.2e}")
for k in ("shot24", "stone"):
    for cd in (0.47, 0.3, 0.2):
        r = RAT[k] * sqrt(cd / CD); q = fly(r, 45)
        P(f"   {k} with Cd {cd}: vt {VT[k] * sqrt(CD / cd):.0f} m/s, ratio {r:.2f}, range {q['R'] * L[k] * CD / cd:.0f} m, range fraction {q['rf']:.3f}, apex {q['af']:.3f}, impact {q['ang']:.1f}, best {best_whole(r, 20, 50)}")

P("== 12. area under the path drawn to the size of its own range (parabola at 45: 1/6 = 0.167; straight out then straight down: 0.5)")
for k in ("stone", "shot24", "musket", "shuttle"):
    q = fly(RAT[k], 45, dense=True); ts = np.linspace(0, q["tl"], 20001); xy = q["sol"].sol(ts)
    area = np.trapezoid(xy[1], xy[0]) / q["R"] ** 2 if hasattr(np, "trapezoid") else np.trapz(xy[1], xy[0]) / q["R"] ** 2
    P(f"   {k}: {area:.3f}")

P("== 13. where is the top in a three-part figure (line at 45, arc of a circle of radius rho, vertical line)?  apex fraction by line length / rho")
for sr in (0, 1, 2, 2.1, 2.4, 3, 5, 10, 30):
    P(f"   S/rho {sr}: {(sr * cos(pi / 4) + sin(pi / 4)) / (sr * cos(pi / 4) + 1 + sin(pi / 4)):.3f}")

P("== 14. Brier arithmetic")
odds = [0.95, 0.85, 0.90, 0.85, 0.85, 0.85, 0.82, 0.85, 0.93, 0.85]
P(f"   mean odds {np.mean(odds):.3f}; Brier all held {np.mean([(1 - o) ** 2 for o in odds]):.4f}; if J6 counted as failed {(sum((1 - o) ** 2 for o in odds) - 0.15 ** 2 + 0.85 ** 2) / 10:.4f}; flat 0.9 {0.01:.4f}; flat 1.0 0")
