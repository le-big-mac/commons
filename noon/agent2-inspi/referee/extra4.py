#!/usr/bin/env python
"""(a) are the 315 'loop ends on the start, heading off' pairs exactly ANGLE = INC with INC not divisible by 8?
   (l) can the pencil comparison fail?  Count disagreements for two deliberately wrong formulas.
   (m) are the five pairs of classes with equal diameter congruent as sets of corners?
       (compare sorted lists of all distances between distinct corners, and of corner counts)"""
import json, math, sys
import numpy as np
sys.path.insert(0, '/home/agent2/inspi/referee')
from inspi_ref import simulate

def main():
    rows = json.load(open(sys.argv[1]))['rows']
    # (a)
    z = []
    for r in rows:
        if not r['home']: continue
        inc, ang = r['inc'], r['ang']; q = 360 // math.gcd(inc, 360)
        H, P = simulate(inc, ang, q)
        if abs(P[q]) < 1e-9: z.append((inc, ang))
    print('(a) pairs', len(z), '; all have ANGLE = INC:', all(i == a for i, a in z),
          '; INC set equals the INC not divisible by 8:', sorted(i for i, a in z) == [i for i in range(1, 360) if i % 8])
    # (l)
    def wrong1(inc, ang):
        g = math.gcd(inc, 360); q = 360 // g
        T = q * ang                                 # drops 180 p (q-1)
        return None if T % 360 == 0 else q * (360 // math.gcd(T % 360, 360))
    def wrong2(inc, ang):
        g = math.gcd(inc, 360); q = 360 // g; p = inc // g
        T = q * ang + 180 * p * (q - 1)
        return None if T % 360 == 0 else 360 // math.gcd(T % 360, 360) * 360   # loop taken as 360 steps
    for name, f in (('T = q ANGLE only', wrong1), ('loop of 360 steps', wrong2)):
        bad = sum(1 for r in rows if (f(r['inc'], r['ang']) is None) != (not r['home'])
                  or (r['home'] and f(r['inc'], r['ang']) != r['n0']))
        print('(l) wrong formula "%s": disagreements %d of %d' % (name, bad, len(rows)))
    # (m)
    def corners(inc, ang, n0):
        H, P = simulate(inc, ang, n0)
        pts = np.unique(np.round(P[1:], 9))
        d = np.abs(pts[:, None] - pts[None, :])
        return len(pts), np.sort(d[np.triu_indices(len(pts), 1)])
    for (a, b, n0) in (((60, 0), (180, 60), 12), ((30, 0), (90, 30), 24), ((45, 15), (75, 0), 48),
                       ((50, 0), (70, 0), 72), ((57, 0), (177, 0), 240)):
        na, da = corners(*a, n0); nb, db = corners(*b, n0)
        same = na == nb and np.max(np.abs(da - db)) < 1e-7
        print('(m)', a, b, 'steps', n0, 'distinct corners', na, nb, '; same list of distances:', bool(same))

if __name__ == '__main__':
    main()
