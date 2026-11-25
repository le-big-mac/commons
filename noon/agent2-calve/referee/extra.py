# Peaks of the first 40 units; friction needed to be caught by the lean at e = 0.74; two times to roll.
import sys, math
sys.dont_write_bytecode = True
sys.path.insert(0, '/home/agent2/calve/referee')
import numpy as np
from scipy.integrate import solve_ivp
import blind as B
def go(e, a0, T, fric=0.0):
    M = e; I = M * (e * e + 1) / 12.0; th0 = math.radians(a0); y0 = B.float_at(e, th0)[0]
    def rhs(t, s):
        A, cx, cy = B.sub(e, s[1], s[0]); return [s[2], s[3], (A / B.D - M) / M - fric * s[2], cx * A / B.D / I - fric * s[3]]
    sol = solve_ivp(rhs, (0, T), [y0, th0, 0, 0], method='DOP853', rtol=1e-10, atol=1e-12, dense_output=True, max_step=0.05)
    ts = np.linspace(0, T, int(T * 200) + 1); S = sol.sol(ts); return ts, np.degrees(S[1]), S
ts, deg, S = go(0.5, 1.0, 40.0)
pk = [(round(float(ts[i]), 2), round(float(deg[i]), 1)) for i in range(1, len(ts) - 1) if (deg[i] - deg[i - 1]) * (deg[i + 1] - deg[i]) < 0]
print('turning points of the tilt, e = 0.5 from 1 deg, first 40 units (t, tilt):', pk)
i = int(np.argmax(deg >= 90)); print('at the first passing of 90 deg (t = %.2f) it is turning at %.3f rad per unit (%.1f deg per unit)' % (ts[i], S[3, i], math.degrees(S[3, i])))
for e in (0.74, 0.738):
    for fr in (0.22, 0.05, 0.02, 0.01, 0.005):
        ts, deg, S = go(e, 3.0, 400.0, fr); print('e = %.3f from 3 deg, friction %.3f: greatest tilt %.1f, tilt at t = 400: %.2f' % (e, fr, deg.max(), deg[-1]))
for e in (0.2, 0.73):
    ts, deg, S = go(e, 1.0, 60.0); print('e = %.2f from 1 deg: 90 deg at t = %.2f' % (e, ts[np.argmax(deg >= 90)]))
