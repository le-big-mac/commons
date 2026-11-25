"""Blind part E: the leftover arc of exact ties near phi=0 for (3-sqrt2)/7 < d < 1/4, and the beam-like tilted state beyond."""
import math
from decimal import Decimal as D
from ref import h_dec
from blindC import golden, ring_t, ring_h
out = open('/home/agent2/float/referee/blindE.out', 'w')
def P(*a):
    s = ' '.join(str(x) for x in a); print(s); out.write(s + '\n')
P("points on the phi=0 line up=(1,t,0): t minimising h, then h(1,t,q)-h(1,t,0) for small q (transverse), and min over 36-pt circles")
for ds in ('0.22', '0.24', '0.245', '0.2499', '0.25', '0.2501', '0.255', '0.27', '0.28', '0.2812'):
    d = D(ds)
    # 1-D minimum along t in (0.05, 0.999)
    N = 300
    v = [(h_dec((1, D(i) / N, 0), d), D(i) / N) for i in range(5, N)]
    i0 = min(range(len(v)), key=lambda i: v[i][0])
    t, h0 = golden(lambda t: h_dec((1, t, 0), d), v[max(i0 - 1, 0)][1], v[min(i0 + 1, len(v) - 1)][1])
    row = []
    for q in ('1e-2', '1e-3', '1e-4'):
        q = D(q)
        row.append("q=%s: %+.3e" % (q, h_dec((1, t, q), d) - h0))
    # circle
    nm = (1 + t * t).sqrt()
    e1 = (-t / nm, 1 / nm, D(0)); e2 = (D(0), D(0), D(1)); u = (1 / nm, t / nm, D(0))
    cir = []
    for r in (D('1e-2'), D('1e-3'), D('1e-4')):
        w = min(h_dec(tuple(u[i] + r * (D(math.cos(2 * math.pi * k / 36)) * e1[i] + D(math.sin(2 * math.pi * k / 36)) * e2[i]) for i in range(3)), d) - h0 for k in range(36))
        cir.append("r=%s: %+.3e" % (r, w))
    P("  d=%s  t=%.9f (tilt %.4f deg; 2d=%.4f; ring t=%s) h=%.12f | transverse %s | circle min %s" % (
        ds, t, math.degrees(math.atan(float(t))), 2 * float(d), ('%.9f' % ring_t(d)) if d <= D('0.25') else '-', h0, ' '.join(row), ' '.join(cir)))
out.close()
