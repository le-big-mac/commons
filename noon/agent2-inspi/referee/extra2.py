#!/usr/bin/env python
"""More from inspi_ref_out.json: the five widest and five narrowest classes with their members;
a check of the widest by a second formula; the '360-step loop' trap count."""
import json, math, sys, cmath
from collections import defaultdict

def main():
    d = json.load(open(sys.argv[1])); rows = d['rows']
    home = [r for r in rows if r['home']]
    groups = defaultdict(list)
    for r in home:
        groups[round(r['diam'], 7)].append(r)
    keys = sorted(groups)
    def show(k):
        g = groups[k]
        byinc = defaultdict(list)
        for r in g:
            byinc[r['inc']].append(r['ang'])
        s = '; '.join('INC %d: ANGLE %s' % (i, ','.join(map(str, sorted(a))) if len(a) <= 16 else '%d values from %d' % (len(a), min(a))) for i, a in sorted(byinc.items()))
        print('  %.7f  steps %s  pairs %d  %s' % (k, sorted(set(r['n0'] for r in g)), len(g), s))
    print('five widest:')
    for k in keys[-5:][::-1]: show(k)
    print('five narrowest:')
    for k in keys[:5]: show(k)
    print('2cos(15 deg) =', 2 * math.cos(math.radians(15)), ' 2cos(9 deg) =', 2 * math.cos(math.radians(9)))
    # widest by centre formula: INC 135 ANGLE 22: loop q=8, T = 8*22+180*3*7
    inc, ang = 135, 22
    q = 360 // math.gcd(inc, 360); p = inc // math.gcd(inc, 360)
    T = (q * ang + 180 * p * (q - 1)) % 360
    P = [0j]; h = 0; a = ang
    for k in range(q):
        P.append(P[-1] + cmath.exp(-1j * math.radians(h))); h += a; a += inc
    D = P[q]; c = D / (1 - cmath.exp(-1j * math.radians(T)))
    print('INC 135 ANGLE 22: q', q, 'T mod 360', T, '|D|', abs(D), 'radius of skeleton circle', abs(c),
          ' 2*max|P_k - c| =', 2 * max(abs(z - c) for z in P[:q]))
    # the 360-step-loop trap
    trap = [r for r in home if r['inc'] % 2 == 0 and 360 % r['n0'] == 0]
    print('home-coming pairs with INC even and home time dividing 360 (a 360-step "loop" with total turning 0 that closes):', len(trap))
    evenhome = [r for r in home if r['inc'] % 2 == 0]
    print('   home-coming pairs with INC even:', len(evenhome), '; their home times:', sorted(set(r['n0'] for r in evenhome))[-5:])
    odd = [r for r in rows if r['inc'] % 2 == 1]
    print('   pairs with INC odd:', len(odd), 'all come home:', all(r['home'] for r in odd), '; home times', sorted(set(r['n0'] for r in odd)))
    print('share never home: %d / %d = %.4f' % (len(rows) - len(home), len(rows), (len(rows) - len(home)) / len(rows)))

if __name__ == '__main__':
    main()
