#!/usr/bin/env python
"""One step off the whole-degree grid: INC = p/q of a turn, ANGLE = u/v of a turn, with q and v
that need not divide 360.  The rule is stepped literally with turning kept as whole numbers of
1/L turn (L = lcm(v, 2q)); positions in double precision, tolerance 1e-9.
Compared with the pencil result: home first at q*r steps, r = denominator of
T/360 = q*u/v + p*(q-1)/2, unless that is a whole number, when it never comes home and each
q steps move it sqrt(q)."""
import math, cmath, sys
from fractions import Fraction

TOL = 1e-9


def run(p, q, u, v, cap):
    L = math.lcm(v, 2 * q)
    a0 = (u * L // v) % L
    inc = (p * L // q) % L
    U = [cmath.exp(-2j * math.pi * h / L) for h in range(L)]
    a, h, pos = a0, 0, 0j
    Pq = None; mind = 9e9; q6 = 0; early = 0
    for n in range(1, cap + 1):
        pos += U[h]
        h = (h + a) % L
        a = (a + inc) % L
        if n == q:
            Pq = pos
        d = abs(pos)
        if d < TOL and h == 0 and a == a0:
            return n, Pq, mind, q6, early
        if d < TOL:
            early += 1
            if h == 0:
                q6 += 1
        mind = min(mind, d)
    return None, Pq, mind, q6, early


def main():
    cases = 0; bad = 0; never = 0; maxdev = 0.0; q6tot = 0; nevervisit = 0
    closest = (9e9, None); q6list = []
    for q in list(range(1, 17)) + [25, 27, 32]:
        for p in range(0, q):
            if math.gcd(p, q) != 1:
                continue
            for v in range(1, 17):
                for u in range(v):
                    cases += 1
                    T = Fraction(q * u, v) + Fraction(p * (q - 1), 2)
                    pred = None if T.denominator == 1 else q * T.denominator
                    cap = 40 * q if pred is None else 2 * pred + 5
                    got, Pq, mind, q6, early = run(p, q, u, v, cap)
                    if q6:
                        q6tot += 1; q6list.append((p, q, u, v))
                    if pred is None:
                        never += 1
                        if got is not None:
                            bad += 1
                        maxdev = max(maxdev, abs(abs(Pq) - math.sqrt(q)))
                        if early:
                            nevervisit += 1
                        if mind < closest[0]:
                            closest = (mind, (p, q, u, v))
                    elif got != pred:
                        bad += 1
    print('cases', cases, '; disagreements with pencil formula', bad)
    print('never-home cases', never, '; max | |P_q| - sqrt(q) |', maxdev)
    print('never-home cases that stand on the start again within 40 loops:', nevervisit,
          '; closest approach', closest)
    print('cases at start with first heading but a different next turn (question 6):', q6tot, q6list[:10])


if __name__ == '__main__':
    main()
