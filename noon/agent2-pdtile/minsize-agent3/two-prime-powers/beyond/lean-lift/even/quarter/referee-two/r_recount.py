#!/usr/bin/env python3
"""Referee: a second, plain recount of single multisets (pure Python integers, one signing at a time, remainder of the
signed mask modulo Phi_d by long division; no numpy, no table of powers).  usage: r_recount.py n:b1,b2,... ..."""
import sys, itertools
from fractions import Fraction as F


def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def rem(num, den):
    num = num[:]; dd = len(den) - 1
    for i in range(len(num) - 1, dd - 1, -1):
        t = num[i]
        if t:
            for j in range(dd + 1):
                num[i - dd + j] -= t * den[j]
    return num[:dd]


def quo(num, den):
    num = num[:]; dd = len(den) - 1; q = [0] * (len(num) - dd)
    for i in range(len(num) - 1, dd - 1, -1):
        t = num[i]; q[i - dd] = t
        for j in range(dd + 1):
            num[i - dd + j] -= t * den[j]
    assert not any(num)
    return q


cyc = {}
def phi(d):
    if d not in cyc:
        p = [-1] + [0] * (d - 1) + [1]
        for e in divisors(d):
            if e < d:
                p = quo(p, phi(e))
        cyc[d] = p
    return cyc[d]


for cs in sys.argv[1:]:
    n, bs = cs.split(":"); n = int(n); B = [int(x) for x in bs.split(",")]; m = len(B)
    divs = divisors(n); bad = 0; per = {d: 0 for d in divs}
    for eps in itertools.product((1, -1), repeat=m - 1):
        eps = (1,) + eps
        S = [0] * n
        for e, b in zip(eps, B):
            S[b % n] += e
        isbad = False
        for d in divs:
            if not any(rem(S, phi(d))):
                per[d] += 2; isbad = True
        bad += 2 * isbad
    print("Z_%d m=%d B=%s: bad %d of %d = %s; bad at d: %s" % (n, m, B, bad, 2 ** m, F(bad, 2 ** m), per), flush=True)
