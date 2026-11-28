# Upper bounds for powers of 3 by the recursion of result.md (Proposition 3).
#   e(m)  >= sup over multisets of m elements on Z_(3^a) of  P(bad at some 3^i, i >= 1, and not bad at 1)
#   c(m)  =  P(the signs add up to 0)  (0 for odd m)
# recursion:  e(1) = e(2) = 0;
#   two classes (r0, r1):      c(r0) e(r1) + c(r1) e(r0) + e(r0) e(r1)
#   three classes (r0,r1,r2):  g(r0,r1,r2) + prod (c(rt) + e(rt)) - prod c(rt),
#       g = sum over v != 0 of prod_t P(S_rt = v)
# exact rationals.
import sys
from fractions import Fraction as F
from math import comb
from functools import lru_cache

def c(r):
    return F(comb(r, r // 2), 2 ** r) if r % 2 == 0 else F(0)

def pv(r, v):
    if (r + v) % 2 or abs(v) > r:
        return F(0)
    return F(comb(r, (r + v) // 2), 2 ** r)

@lru_cache(None)
def g(r0, r1, r2):
    r = min(r0, r1, r2)
    return 2 * sum(pv(r0, v) * pv(r1, v) * pv(r2, v) for v in range(1, r + 1))

E = {1: F(0), 2: F(0)}
ARG = {}
def build(M):
    for m in range(3, M + 1):
        best = F(-1); arg = None
        for r1 in range(1, m // 2 + 1):
            r0 = m - r1
            val = c(r0) * E[r1] + c(r1) * E[r0] + E[r0] * E[r1]
            if val > best:
                best, arg = val, (r0, r1)
        for r2 in range(1, m // 3 + 1):
            for r1 in range(r2, (m - r2) // 2 + 1):
                r0 = m - r1 - r2
                val = g(r0, r1, r2) + (c(r0) + E[r0]) * (c(r1) + E[r1]) * (c(r2) + E[r2]) - c(r0) * c(r1) * c(r2)
                if val > best:
                    best, arg = val, (r0, r1, r2)
        E[m] = best; ARG[m] = arg

if __name__ == '__main__':
    M = int(sys.argv[1]) if len(sys.argv) > 1 else 60
    build(M)
    print('m  e(m)  c(m)+e(m)  [decimal]  attained in the recursion at class sizes')
    for m in range(3, M + 1):
        t = c(m) + E[m]
        if m <= 40 or m % 20 in (0, 1):
            print(m, E[m] if m <= 16 else '', t if m <= 16 else '', f'{float(E[m]):.6f} {float(t):.6f}', ARG[m])
    print('max over odd m in [7, M] of e(m):', max(float(E[m]) for m in range(7, M + 1, 2)))
    print('max over even m in [14, M] of c(m)+e(m):', max(float(c(m) + E[m]) for m in range(14, M + 1, 2)))
    # monotonicity facts used in the tail argument
    print('e(m)*sqrt(m) max over m in [3,M]:', max(float(E[m]) * m ** 0.5 for m in range(3, M + 1)))
    print('(c+e)(m)*sqrt(m) max over m in [3,M]:', max(float(c(m) + E[m]) * m ** 0.5 for m in range(3, M + 1)))
