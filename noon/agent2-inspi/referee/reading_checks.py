#!/usr/bin/env python
"""Referee's recomputation of README figures, from the blind step's own programs."""
import json, math, sys, cmath
import numpy as np
sys.path.insert(0, '/home/agent2/inspi/referee')
from inspi_ref import simulate

def phi(n):
    return sum(1 for k in range(1, n + 1) if math.gcd(k, n) == 1)

def main():
    rows = json.load(open('/home/agent2/inspi/referee/inspi_ref_out.json'))['rows']
    home = [r for r in rows if r['home']]
    # A. figures under 2 across
    u2 = [r for r in home if r['diam'] < 2 - 1e-9]
    print('A. home-coming pairs less than 2 across:', len(u2), '; INCs', sorted(set(r['inc'] for r in u2)),
          '; ANGLEs', sorted(r['ang'] for r in u2), '; distinct widths', len(set(round(r['diam'], 7) for r in u2)))
    e2 = [r for r in home if abs(r['diam'] - 2) < 1e-9]
    print('   exactly 2 across:', [(r['inc'], r['ang'], r['n0']) for r in e2][:20], len(e2))
    w = [r for r in home if r['diam'] > 81.7366306 + 1e-6]
    print('   pairs wider than 81.7366:', len(w))
    # B. the sums
    s40 = sum(q * phi(q) for q in range(1, 361) if 360 % q == 0 or q <= 40)
    s150 = sum(q * phi(q) for q in range(1, 151))
    print('B. sum q phi(q), q | 360 or q <= 40:', s40, ' (README 66,079);  q <= 150:', s150, ' (README 686,733)')
    # C. the family ANGLE = INC/2 (INC = 2 ANGLE mod 360)
    fam = [r for r in rows if (2 * r['ang']) % 360 == r['inc']]
    print('C. pairs with INC = 2 ANGLE mod 360:', len(fam), '; home:', sum(r['home'] for r in fam))
    bad = 0
    for r in fam:
        q = 360 // math.gcd(r['ang'], 360)       # their q: alpha = ANGLE/360 = p/q
        if (q % 4 == 2) != r['home']: bad += 1
    print('   bounded exactly when q = 2 mod 4 fails in', bad)
    # D. lap displacement for every pair; ratio to sqrt q; T of laps ending on start; symmetry of all
    best = (0, None); zero = []; msq = 0.0; symbad = 0; symmax = 0.0
    lapd = {}
    for inc in range(1, 360):
        g = math.gcd(inc, 360); q = 360 // g; p = inc // g
        tot = 0.0
        for ang in range(360):
            H, P = simulate(inc, ang, q)
            b = abs(P[q]); lapd[(inc, ang)] = b; tot += b * b
            T = (q * ang + 180 * p * (q - 1)) % 360
            if b < 1e-9: zero.append((inc, ang, T))
            if T and b / math.sqrt(q) > best[0] + 1e-12: best = (b / math.sqrt(q), (inc, ang, b))
        msq = max(msq, abs(tot / 360 - q))
    print('D. laps ending on the start:', len(zero), '; their T values:', sorted(set(z[2] for z in zero)))
    print('   largest |B|/sqrt(q) among home-coming:', best, '; mean-square departure', msq)
    print('   book turtle (20,2):', lapd[(20, 2)], ' (7,0):', lapd[(7, 0)], ' (101,281):', lapd[(101, 281)], lapd[(259, 79)])
    hs = {(r['inc'], r['ang']) for r in home}
    print('   smallest nonzero lap displacement among home-coming:', min((v, k) for k, v in lapd.items() if v > 1e-9 and k in hs), flush=True)
    # symmetry for every home-coming pair: lap k+1 is lap k turned through T about the centre
    for r in home:
        inc, ang, n0 = r['inc'], r['ang'], r['n0']
        g = math.gcd(inc, 360); q = 360 // g; p = inc // g
        T = (q * ang + 180 * p * (q - 1)) % 360
        H, P = simulate(inc, ang, n0)
        rot = cmath.exp(-1j * math.radians(T)); c = P[q] / (1 - rot)
        dev = np.max(np.abs((P[q:] - c) - rot * (P[:-q] - c)))
        symmax = max(symmax, dev)
        if dev > 1e-8: symbad += 1
    print('   every home-coming pair: each lap is the one before turned through T about the centre; fails in', symbad, 'largest departure', symmax)
    # E. a lap that ends on its start off the whole-degree grid: roots of B(z) on the unit circle
    found = []
    for q in range(2, 41):
        for p in range(1, q):
            if math.gcd(p, q) != 1: continue
            coef = [cmath.exp(2j * math.pi * p * k * (k - 1) / (2 * q)) for k in range(q)]   # B(a) = sum coef_k z^k, z = e(a)
            for z in np.roots(coef[::-1]):
                if abs(abs(z) - 1) < 1e-7:
                    a = (cmath.phase(z) / (2 * math.pi)) % 1.0
                    t = (q * a + p * (q - 1) / 2) % 1.0
                    found.append((q, p, round(a * 360, 6), round(t * 360, 4)))
    ts = sorted(set(f[3] for f in found))
    print('E. q <= 40: first turns (any real number) at which the lap ends on its start:', len(found), '; distinct T (degrees):', ts[:12], '... count', len(ts))
    odd = [f for f in found if abs(f[3] - 180) > 1e-3]
    print('   with T other than half a turn:', len(odd), odd[:8])
    oddq = [f for f in found if f[0] % 2 == 1]
    print('   with q odd:', len(oddq), oddq[:6])

if __name__ == '__main__':
    main()
