# irregular polygons with an incircle (radius 1), mirror-symmetric about the x axis; normals at +-(given fractions of pi)
# corners rounded inward by eps (the inner parallel body of such a polygon is a scaled copy). Uses flow.py's solver.
import sys, math, numpy as np, flow5 as flow
fr = [float(s) for s in sys.argv[1].split(',')]; m = int(sys.argv[2]); eps = float(sys.argv[3])
ang = sorted(set([f * math.pi for f in fr] + [-f * math.pi for f in fr if 0 < f < 1]))
V = []
for i in range(len(ang)):
    a = ang[i]; b = ang[(i + 1) % len(ang)]
    if b <= a: b += 2 * math.pi
    assert b - a < math.pi
    V.append(((a + b) / 2, 1 / math.cos((b - a) / 2)))
def p0(shape, th, e):
    P = np.max([r * np.cos(th - c) for c, r in V], axis=0)
    return (1 - e) * P + e, 1
flow.p0 = p0
r = flow.solve('halfdisc', m, eps)
print('poly normals=%-12s m=%4d eps=%-6g steps=%8d A0=%.6f T=%.6f I=%.6f Q=%.5f Qlow=%.5f chk=%.1e' % (sys.argv[1], m, eps, r['steps'], r['A0'], r['T'], r['I'], r['Q'], r['Qlow'], r['chk']), flush=True)
big = np.nonzero(r['R0'] > 10)[0]
print('   Euler %.5f   (3/2) A M(0)/T^2 = %.5f   G on the edges / (2T/3A): %s  at theta/pi = %s' % (r['euler'], r['QM'], np.round(r['ge'][big], 4).tolist(), np.round(big / m, 4).tolist()), flush=True)
