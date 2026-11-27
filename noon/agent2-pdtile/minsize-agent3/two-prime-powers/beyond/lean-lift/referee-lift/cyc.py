"""Exact tools, written for this refereeing (no sympy): cyclotomic polynomials by exact integer division of X^d - 1,
remainder tables of X^i modulo Phi_d, and the pattern of a multiset on Z_M.  Integer arithmetic only."""
import numpy as np
from math import gcd
_phi = {}
def divisors(n): return [d for d in range(1, n + 1) if n % d == 0]
def polydiv_exact(a, b):
    """a / b for integer coefficient lists (lowest degree first), b monic; asserts zero remainder"""
    a = a[:]; q = [0] * (len(a) - len(b) + 1)
    for i in range(len(a) - len(b), -1, -1):
        c = a[i + len(b) - 1]; q[i] = c
        if c:
            for j, bj in enumerate(b): a[i + j] -= c * bj
    assert not any(a), 'division not exact'
    return q
def cyclotomic(d):
    """Phi_d as a list of integers, lowest degree first"""
    if d not in _phi:
        f = [-1] + [0] * (d - 1) + [1]
        for e in divisors(d):
            if e < d: f = polydiv_exact(f, cyclotomic(e))
        _phi[d] = f
    return _phi[d]
def totient(d): return sum(1 for i in range(1, d + 1) if gcd(i, d) == 1)
def rem_table(d, M):
    """T[i] = coefficients of X^i mod Phi_d, for 0 <= i < M: array M x phi(d), int64"""
    phi = cyclotomic(d); deg = len(phi) - 1
    assert deg == totient(d) and phi[-1] == 1
    T = np.zeros((M, deg), dtype=np.int64)
    cur = [0] * deg
    if deg == 0: raise ValueError
    # X^0 mod Phi_d
    if deg >= 1:
        cur[0] = 1
        if deg == 1 and False: pass
    for i in range(M):
        T[i] = cur
        # multiply by X and reduce
        top = cur[-1]; cur = [0] + cur[:-1]
        if top:
            for j in range(deg): cur[j] -= top * phi[j]
    return T
_tabs = {}
def tables(M):
    """{d: table} for every divisor d of M (d = 1 included: X^i mod (X - 1) = 1)"""
    if M not in _tabs: _tabs[M] = {d: rem_table(d, M) for d in divisors(M)}
    return _tabs[M]
def pattern(elems, M, with_one=False):
    """the set of divisors d of M (d > 1 unless with_one) with Phi_d | sum X^e over the list elems (elements of range(M))"""
    T = tables(M); idx = np.array(sorted(elems), dtype=np.int64)
    out = set()
    for d, t in T.items():
        if d == 1 and not with_one: continue
        if not t[idx].sum(axis=0).any(): out.add(d)
    return frozenset(out)
def selftest():
    # known values
    assert cyclotomic(1) == [-1, 1] and cyclotomic(2) == [1, 1] and cyclotomic(3) == [1, 1, 1] and cyclotomic(4) == [1, 0, 1]
    assert cyclotomic(6) == [1, -1, 1] and cyclotomic(12) == [1, 0, -1, 0, 1] and cyclotomic(9) == [1, 0, 0, 1, 0, 0, 1]
    assert cyclotomic(105).count(-2) == 2          # the famous coefficient -2 (twice) of Phi_105
    # the product of Phi_d over d | n is X^n - 1, degrees are totients
    for n in (30, 36, 54, 72, 105, 108, 225):
        prod = [1]
        for d in divisors(n):
            f = cyclotomic(d); new = [0] * (len(prod) + len(f) - 1)
            for i, a in enumerate(prod):
                for j, b in enumerate(f): new[i + j] += a * b
            prod = new
        assert prod == [-1] + [0] * (n - 1) + [1]
    # pattern against complex evaluation on random multisets
    import cmath, random
    rnd = random.Random(5)
    for M in (12, 18, 30, 36, 45, 54):
        for _ in range(300):
            if rnd.random() < 0.5: el = [rnd.randrange(M) for _ in range(rnd.randint(1, 8))]
            else:
                el = []
                for _ in range(rnd.randint(1, 3)):
                    c = rnd.choice(divisors(M)); x0 = rnd.randrange(M); el += [(x0 + c * j) % M for j in range(M // c)]
            P = pattern(el, M, with_one=True)
            for d in divisors(M):
                z = cmath.exp(2j * cmath.pi / d); val = sum(z ** e for e in el)
                assert (abs(val) < 1e-7) == (d in P), (M, el, d, val)
    return 'cyc.py self-test passed'
if __name__ == '__main__': print(selftest())
