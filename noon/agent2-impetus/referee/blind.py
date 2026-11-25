"""Referee's blind computation. Own integrator: scipy DOP853 with events, cross-checked
against a hand-written fixed-step RK4 with a linear/Hermite landing solve, and against vacuum."""
import numpy as np
from math import pi, sqrt, sin, cos, atan2, degrees, radians
from scipy.integrate import solve_ivp

G = 9.81
RHO = 1.225
CD = 0.47


def vt_sphere(mass, density):
    r = (3 * mass / (4 * pi * density)) ** (1 / 3)
    A = pi * r * r
    return sqrt(2 * mass * G / (RHO * CD * A)), r, A


def projectiles():
    out = {}
    # musket ball
    d = 0.018
    r = d / 2
    m = 11340 * 4 / 3 * pi * r ** 3
    A = pi * r * r
    out["musket"] = (sqrt(2 * m * G / (RHO * CD * A)), 450.0, m, r)
    vt, r, A = vt_sphere(10.9, 7800)
    out["shot24"] = (vt, 450.0, 10.9, r)
    vt, r, A = vt_sphere(100.0, 2600)
    out["trebuchet"] = (vt, 50.0, 100.0, r)
    out["shuttle"] = (6.8, 60.0, None, None)
    return out


def fly(v0, elev_deg, vt, rtol=1e-11):
    """returns range, x_apex, impact angle (deg below horizontal), landing speed, flight time"""
    k = 0.0 if vt is None else G / vt ** 2  # a_drag = k v^2
    th = radians(elev_deg)

    def f(t, s):
        x, y, vx, vy = s
        v = sqrt(vx * vx + vy * vy)
        return [vx, vy, -k * v * vx, -G - k * v * vy]

    def apex(t, s):
        return s[3]
    apex.direction = -1
    apex.terminal = False

    def land(t, s):
        return s[1]
    land.direction = -1
    land.terminal = True

    tmax = 2 * v0 * sin(th) / G * 1.5 + 10
    sol = solve_ivp(f, (0, tmax), [0, 0, v0 * cos(th), v0 * sin(th)], method="DOP853",
                    rtol=rtol, atol=1e-12, events=[apex, land])
    assert len(sol.t_events[1]) == 1, "no landing"
    assert len(sol.t_events[0]) >= 1, "no apex"
    xa = sol.y_events[0][0][0]
    xl, yl, vxl, vyl = sol.y_events[1][0]
    ang = degrees(atan2(-vyl, vxl))
    return xl, xa, ang, sqrt(vxl ** 2 + vyl ** 2), sol.t_events[1][0]


def fly_rk4(v0, elev_deg, vt, dt):
    """independent fixed-step RK4; landing and apex by linear interpolation within the last step."""
    k = 0.0 if vt is None else G / vt ** 2
    th = radians(elev_deg)
    s = np.array([0.0, 0.0, v0 * cos(th), v0 * sin(th)])

    def f(s):
        v = sqrt(s[2] ** 2 + s[3] ** 2)
        return np.array([s[2], s[3], -k * v * s[2], -G - k * v * s[3]])

    xa = None
    while True:
        k1 = f(s); k2 = f(s + 0.5 * dt * k1); k3 = f(s + 0.5 * dt * k2); k4 = f(s + dt * k3)
        n = s + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        if xa is None and n[3] <= 0:
            fr = s[3] / (s[3] - n[3])
            xa = s[0] + fr * (n[0] - s[0])
        if n[1] < 0:
            fr = s[1] / (s[1] - n[1])
            e = s + fr * (n - s)
            return e[0], xa, degrees(atan2(-e[3], e[2])), sqrt(e[2] ** 2 + e[3] ** 2)
        s = n


if __name__ == "__main__":
    lines = []
    P = projectiles()
    lines.append("REFEREE BLIND NUMBERS (own code, scipy DOP853 rtol 1e-11 with events; g=9.81, rho=1.225, Cd=0.47)")
    lines.append("")
    lines.append("Vacuum check at 45 deg, v0=450: ")
    R, xa, ang, vl, T = fly(450.0, 45, None)
    lines.append(f"  range {R:.6f} (formula {450**2/G:.6f}), apex frac {xa/R:.9f}, impact angle {ang:.9f}, landing speed {vl:.6f}")
    R, xa, ang, vl, T = fly(50.0, 30, None)
    lines.append(f"  v0=50 at 30 deg: range {R:.6f} (formula {50**2*sin(radians(60))/G:.6f}), apex frac {xa/R:.9f}, impact angle {ang:.9f}")
    lines.append("")
    lines.append("Terminal velocities, mass, radius:")
    for name, (vt, v0, m, r) in P.items():
        if m is None:
            lines.append(f"  {name:10s} vt = {vt:.4f} m/s (set)  v0 = {v0}  v0/vt = {v0/vt:.4f}")
        else:
            lines.append(f"  {name:10s} vt = {vt:.4f} m/s  mass = {m:.6f} kg  diameter = {2*r*1000:.3f} mm  v0 = {v0}  v0/vt = {v0/vt:.4f}")
    lines.append("")
    lines.append("At 45 degrees:")
    lines.append(f"  {'name':10s} {'range m':>12s} {'vac range':>12s} {'range frac':>11s} {'apex frac':>10s} {'impact deg':>11s} {'vland/vt':>9s} {'best elev':>9s} {'range@best':>11s}")
    minapex = (9, None, None)
    minexcess = (999, None, None)
    alltab = {}
    for name, (vt, v0, m, r) in P.items():
        best = (-1, None)
        tab = []
        for e in range(5, 86):
            R, xa, ang, vl, T = fly(v0, e, vt)
            tab.append((e, R, xa / R, ang, vl / vt))
            if R > best[0]:
                best = (R, e)
            if xa / R < minapex[0]:
                minapex = (xa / R, name, e)
            if ang - e < minexcess[0]:
                minexcess = (ang - e, name, e)
        alltab[name] = tab
        e, R, af, ang, vr = tab[45 - 5]
        vac = v0 ** 2 / G
        lines.append(f"  {name:10s} {R:12.4f} {vac:12.4f} {R/vac:11.6f} {af:10.6f} {ang:11.5f} {vr:9.5f} {best[1]:9d} {best[0]:11.4f}")
    lines.append("")
    lines.append(f"Least apex fraction over all four and 5..85: {minapex[0]:.6f} ({minapex[1]} at {minapex[2]} deg)")
    lines.append(f"Least (impact angle - elevation): {minexcess[0]:.6f} deg ({minexcess[1]} at {minexcess[2]} deg)")
    lines.append("")
    lines.append("Ranges near the best elevation (to see how flat the top is):")
    for name, tab in alltab.items():
        bi = max(range(len(tab)), key=lambda i: tab[i][1])
        seg = tab[max(0, bi - 2): bi + 3]
        lines.append(f"  {name:10s} " + "  ".join(f"{e}:{R:.4f}" for e, R, *_ in seg))
    lines.append("")
    lines.append("Cross-check with hand-written fixed-step RK4 (dt chosen small), 45 deg:")
    for name, (vt, v0, m, r) in P.items():
        dt = 2e-4 if name != "shuttle" else 2e-5
        R, xa, ang, vl = fly_rk4(v0, 45, vt, dt)
        lines.append(f"  {name:10s} range {R:.4f}  apex frac {xa/R:.6f}  impact {ang:.5f}  vland/vt {vl/vt:.5f}")
    out = "\n".join(lines) + "\n"
    print(out)
    with open("/home/agent2/impetus/referee/blind.out", "w") as fh:
        fh.write(out)
