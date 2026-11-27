"""functions of spread_lift.py (the part above its main loop)"""
import sys, random, json, collections
from sympy import Poly, cyclotomic_poly, symbols, ZZ
X = symbols('X'); random.seed(5); CY = {}
def pattern(mult, M):
    A = Poly(sum(w * X**i for i, w in mult.items() if w), X, domain=ZZ); out = set()
    for d in range(1, M + 1):
        if M % d == 0:
            if d not in CY: CY[d] = Poly(cyclotomic_poly(d, X), X, domain=ZZ)
            if A.rem(CY[d]).is_zero: out.add(d)
    return frozenset(out)
def even_split(m, r, same_ends=True):
    a, rho = divmod(m, r); s = [a] * r
    if rho == r - 1:
        for t in range(r): s[t] += 1
        s[1] -= 1
    else:
        for t in range(1, 1 + rho): s[t] += 1          # rho <= r-2 middle slots
    assert sum(s) == m and s[0] == s[r - 1]; return s
def step(mult, N, r, i):
    """one lift along r; mult: dict x -> multiplicity on Z_N, all <= r^i and not all = r^i; returns dict on Z_{N r}"""
    assert max(mult.values()) <= r ** i and not all(m == r ** i for m in mult.values())
    k = 0
    while N % r ** (k + 1) == 0: k += 1
    cand = [x for x in sorted(mult) if mult[x] % r] or [x for x in sorted(mult) if mult[x] < r ** i]
    x1 = cand[0]; c1 = x1 % r ** k; out = {}
    for x, m in mult.items():
        if x == x1:
            a, rho = divmod(m, r)
            if rho > 0:
                s = [a] * r; s[0] += 1
                for t in range(1, rho): s[t] += 1          # rho - 1 <= r - 2 middle slots
            else:
                s = [a] * r; s[0] += 1; s[r - 1] -= 1
            assert sum(s) == m and s[0] != s[r - 1] and min(s) >= 0
        else: s = even_split(m, r)
        for j in range(r):
            y = x + N * j; t = (y % r ** (k + 1)) // r ** k
            if s[t]: out[y] = s[t]
    return out
def lift_to_set(mult, N, r):
    j = 0
    while not (max(mult.values()) <= r ** j and not all(m == r ** j for m in mult.values())): j += 1
    M = N
    for i in range(j, 0, -1): mult = step(mult, M, r, i); M *= r
    assert max(mult.values()) == 1
    return mult, M, j
