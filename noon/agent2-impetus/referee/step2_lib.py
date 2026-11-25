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


