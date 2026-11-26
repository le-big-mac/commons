#!/usr/bin/env python
"""Extra counts from inspi_ref_out.json and a fresh simulation with the referee's simulate():
   how many home-coming pairs have the basic loop (first q = 360/gcd steps) end ON the start with the heading off;
   the book's own example; where early visits to the start fall."""
import json, math, sys
import numpy as np
sys.path.insert(0, '/home/agent2/inspi/referee')
from inspi_ref import simulate, reduction_table, exact_zero

def main():
    d = json.load(open(sys.argv[1])); rows = d['rows']
    R = reduction_table()
    book = [r for r in rows if r['inc'] == 20 and r['ang'] == 2][0]
    print('book example ANGLE 2 INC 20:', book)
    zeroD = []; minD = (9e9, None); absDs = []
    for r in rows:
        if not r['home']:
            continue
        inc, ang = r['inc'], r['ang']
        q = 360 // math.gcd(inc, 360)
        H, P = simulate(inc, ang, q)
        a = abs(P[q])
        if a < 1e-9:
            assert exact_zero(R, H[:q] % 360)
            zeroD.append((inc, ang, int(H[q] % 360)))
        else:
            if a < minD[0]:
                minD = (a, (inc, ang))
    print('home-coming pairs whose first q steps end on the start (heading off):', len(zeroD))
    incs = sorted(set(z[0] for z in zeroD))
    print('  INC values:', len(incs), incs[:40])
    print('  examples:', zeroD[:12])
    from collections import Counter
    print('  by q:', sorted(Counter(360 // math.gcd(z[0], 360) for z in zeroD).items()))
    print('  smallest nonzero |P_q| among home-coming pairs:', minD)

if __name__ == '__main__':
    main()
