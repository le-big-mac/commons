#!/usr/bin/env python
"""Which different classes (under shift, reversal, mirror) share a diameter to 1e-7?"""
import json, math, sys
from collections import defaultdict

def main():
    rows = json.load(open(sys.argv[1]))['rows']
    home = {(r['inc'], r['ang']): r for r in rows if r['home']}
    cls = {}
    for key in home:
        if key in cls: continue
        i, a = key; q = 360 // math.gcd(i, 360)
        for j in range(q):
            for k in ((i, (a + j * i) % 360), (i, (-a + j * i) % 360), ((-i) % 360, (-a + j * i) % 360), ((-i) % 360, (a + j * i) % 360)):
                cls[k] = key
    bydiam = defaultdict(set)
    for key, r in home.items():
        bydiam[round(r['diam'], 7)].add(cls[key])
    n = 0
    for d, s in sorted(bydiam.items()):
        if len(s) > 1:
            n += 1
            print(d, [(k, home[k]['n0'], repr(home[k]['diam'])) for k in sorted(s)])
    print('diameters shared by more than one class:', n, '; classes', len(set(cls.values())))

if __name__ == '__main__':
    main()
