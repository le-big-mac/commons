"""Q5 by the geometric (second) method, and thresholds one step off; where the 36-circles sit."""
import math
import numpy as np
import sys
sys.path.insert(0, "/home/agent2/referee-gasket-27")
from check_geo import run, tangent

if __name__ == '__main__':
    M = 1800
    for q, f in [((-4, 5, 20, 21), 'out/g_-4_5_20_21_1e6.bin'), ((-3, 5, 8, 8), 'out/g_-3_5_8_8_1e6.bin')]:
        circles, worst, nq = run(q, M)
        ks = sorted(c[0] for c in circles)
        cc = np.fromfile(f, dtype=np.uint32)[:M + 1].astype(np.int64)
        for T in (674.2, 788.5, 874.2, 1685.7):
            t = math.floor(T)
            geo = sum(1 for k in ks if k <= T)
            cfile = int(cc[:t + 1].sum()) + 1
            sq = {}
            for k in ks:
                if 0 < k <= T and math.isqrt(k) ** 2 == k:
                    sq[k] = sq.get(k, 0) + 1
            print(q, 'T=%s' % T, 'geometric count', geo, '| C count', cfile, '| at T-1:', sum(1 for k in ks if k <= t - 1),
                  'at T+1:', sum(1 for k in ks if k <= t + 1), '| circles with curvature exactly floor(T):', int(cc[t]),
                  '| square curvatures (curvature: circles):', sq)
        if q == (-4, 5, 20, 21):
            for c in circles:
                if c[0] in (36, 144, 1296):
                    tn = sorted(d[0] for d in circles if d is not c and tangent(c, d) * max(abs(c[0]), abs(d[0])) < 1e-3)
                    print('  circle of curvature', c[0], 'centre (%.5f, %.5f)' % (c[1] / c[0], c[2] / c[0]),
                          'is tangent to circles of curvature (<=%d):' % M, tn[:12])
