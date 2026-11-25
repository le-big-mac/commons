# When does the frictionless e = 0.5 block first pass 149, 160, 170 degrees?  Two tolerances, three first tilts.
import sys, math
sys.dont_write_bytecode = True
sys.path.insert(0, '/home/agent2/calve/referee')
import numpy as np
from scipy.integrate import solve_ivp
import blind as B
def go(e, a0, T, rtol, ms):
    M = e; I = M * (e * e + 1) / 12.0; th0 = math.radians(a0); y0 = B.float_at(e, th0)[0]
    def rhs(t, s):
        A, cx, cy = B.sub(e, s[1], s[0]); return [s[2], s[3], (A / B.D - M) / M, cx * A / B.D / I]
    sol = solve_ivp(rhs, (0, T), [y0, th0, 0, 0], method='DOP853', rtol=rtol, atol=rtol * 1e-2, dense_output=True, max_step=ms)
    ts = np.linspace(0, T, int(T * 100) + 1); deg = np.degrees(sol.sol(ts)[1])
    f = lambda x: ('%.0f' % ts[np.argmax(deg > x)]) if deg.max() > x else 'never'
    return 'greatest %.1f; first above 149: %s, above 160: %s, above 170: %s; least after t=15: %.1f' % (deg.max(), f(149), f(160), f(170), deg[ts > 15].min())
for a0 in (1.0, 0.5, 2.0):
    for rtol, ms in ((1e-10, 0.05), (1e-12, 0.02)):
        print('e 0.5 from %.1f deg, T = 1500, rtol %.0e:' % (a0, rtol), go(0.5, a0, 1500.0, rtol, ms))
