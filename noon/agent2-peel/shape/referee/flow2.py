# rounded-triangle family: equilateral triangle (inradius 1) swollen by d; uses flow.py's solver
import sys, math, numpy as np, flow
d = float(sys.argv[1]); m = int(sys.argv[2])
orig = flow.p0
def p0(shape, th, eps):
    if shape == 'rtriangle':
        return 2.0 * np.cos(th - math.pi / 3) + d, 3
    return orig(shape, th, eps)
flow.p0 = p0
r = flow.solve('rtriangle', m, 0.0)
print('rt d=%-5g m=%4d steps=%8d A0=%.6f T=%.6f I=%.6f Q=%.5f Qlow=%.5f chk=%.1e' % (d, m, r['steps'], r['A0'], r['T'], r['I'], r['Q'], r['Qlow'], r['chk']), flush=True)
