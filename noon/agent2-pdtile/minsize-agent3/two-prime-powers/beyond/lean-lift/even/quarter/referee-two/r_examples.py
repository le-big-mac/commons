#!/usr/bin/env python3
"""Referee's recount, from the definition, of the two multisets of result.md section 7 (and any other given on the
command line as n:b1,b2,...)."""
import sys
from fractions import Fraction as F
import numpy as np
import r_brute as RB

cases = ["225:19,19,22,22,36,36,110,110,133,133", "675:17,17,66,66,106,106,384,384,558,558,665,665"] + sys.argv[1:]
for cs in cases:
    n, bs = cs.split(":"); n = int(n); B = [int(x) for x in bs.split(",")]
    m = len(B); E = RB.signs(m); S = E.shape[0]
    anyb = np.zeros(S, dtype=bool); per = {}
    for d in RB.divisors(n):
        z = RB.zero_rows(E, RB.V(d)[[b % d for b in B]])
        per[d] = int(z.sum()); anyb |= z
    print("Z_%d m=%d B=%s: bad %d of %d = %s; T2(m)=%s; bad at d: %s" % (n, m, B, int(anyb.sum()), S, F(int(anyb.sum()), S), RB.T2(m), per))
