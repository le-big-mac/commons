# Turning only, the block held at its floating depth: (i) as in after.py (inertia of turning only); (ii) with the rise that goes with the turning counted in the inertia.
import sys, math
sys.dont_write_bytecode = True
sys.path.insert(0, '/home/agent2/calve/referee')
import numpy as np
from scipy.integrate import solve_ivp
import blind as B
e = 0.5; k2 = (e * e + 1) / 12
def yp(th, dl=1e-5): return (B.float_at(e, th + dl)[0] - B.float_at(e, th - dl)[0]) / (2 * dl)
def ypp(th, dl=1e-4): return (B.float_at(e, th + dl)[0] - 2 * B.float_at(e, th)[0] + B.float_at(e, th - dl)[0]) / dl ** 2
def r1(t, s): return [s[1], B.xb(e, s[0]) / k2]
def r2(t, s):                                   # (k2 + y'^2) th'' + y' y'' th'^2 = xb
    a = yp(s[0]); return [s[1], (B.xb(e, s[0]) - a * ypp(s[0]) * s[1] ** 2) / (k2 + a * a)]
for name, r in (('inertia of turning only', r1), ('with the rise counted', r2)):
    sol = solve_ivp(r, (0, 40), [math.radians(1.0), 0.0], method='DOP853', rtol=1e-9, atol=1e-11, dense_output=True, max_step=0.05)
    ts = np.linspace(0, 40, 8001); deg = np.degrees(sol.sol(ts)[0]); print('%s: 90 deg at t = %.2f; greatest tilt in 40 units %.1f' % (name, ts[np.argmax(deg >= 90)], deg.max()))
