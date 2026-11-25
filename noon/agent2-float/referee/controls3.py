"""Step 2: corner-up curvature against the referee's algebra below 1/6, and the size of the corner-up hollow just above 1/6."""
import math
from decimal import Decimal as D
from ref import h_dec
S2, S3, S6 = D(2).sqrt(), D(3).sqrt(), D(6).sqrt()
C = (1/S3, 1/S3, 1/S3); E1 = (1/S2, -1/S2, D(0)); E2 = (1/S6, 1/S6, -2/S6)
def circ(d, r, m=36):
    h0 = h_dec((1,1,1), d); w = None
    for k in range(m):
        a = 2*math.pi*k/m; c, s = D(math.cos(a)), D(math.sin(a))
        dh = h_dec(tuple(C[i] + r*(c*E1[i] + s*E2[i]) for i in range(3)), d) - h0
        w = dh if w is None or dh < w else w
    return w
print("corner up: min over circle of 2*dh/r^2 at r=1e-7 vs algebra (sqrt3/2)((6d)^(1/3)-1) valid for d<=1/6")
for ds in ('0.05', '0.10', '0.15', '0.166', '0.1667', '0.17', '0.20'):
    d = D(ds); r = D('1e-7')
    print("   d=%s numeric %+.6f  algebra(tetra regime) %+.6f" % (ds, 2*circ(d, r)/(r*r), float(S3)/2*((6*float(d))**(1/3)-1)))
print("size of the corner-up hollow just above 1/6: lowest dh on circles of radius r (rad); negative = some direction is lower")
for ds in ('0.1667', '0.1670', '0.1675', '0.1680', '0.1700'):
    d = D(ds)
    print("   d=%s: " % ds + "  ".join("r=%s: %+.2e" % (r, circ(d, D(r))) for r in ('1e-4', '3e-4', '1e-3', '3e-3', '1e-2', '2e-2', '5e-2')))
