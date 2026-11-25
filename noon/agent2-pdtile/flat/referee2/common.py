"""Referee-2 helpers, written from scratch.  Exact integer arithmetic only.

Polynomials are lists of ints, lowest degree first.
"""
from math import gcd


def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def poly_divmod(num, den):
    """Divide integer polynomial num by MONIC integer polynomial den. Returns (quot, rem)."""
    assert den[-1] == 1
    num = list(num)
    dn = len(den) - 1
    if len(num) - 1 < dn:
        return [0], num + [0] * (dn - len(num))
    quot = [0] * (len(num) - dn)
    for k in range(len(num) - 1, dn - 1, -1):
        c = num[k]
        if c:
            quot[k - dn] = c
            for i, dcoef in enumerate(den):
                num[k - dn + i] -= c * dcoef
    return quot, num[:dn]


_CYC = {}


def cyclotomic(n):
    """Phi_n as integer coefficient list, from X^n - 1 = prod_{d | n} Phi_d."""
    if n in _CYC:
        return _CYC[n]
    num = [-1] + [0] * (n - 1) + [1]
    for d in divisors(n):
        if d < n:
            num, rem = poly_divmod(num, cyclotomic(d))
            assert not any(rem)
            while len(num) > 1 and num[-1] == 0:
                num.pop()
    _CYC[n] = num
    return num


def euler_phi(n):
    return sum(1 for k in range(1, n + 1) if gcd(k, n) == 1)


def residues(d, upto=None):
    """List R with R[a] = coefficient vector (length phi(d)) of X^a mod Phi_d, for a in range(upto)."""
    if upto is None:
        upto = d
    phi = cyclotomic(d)
    deg = len(phi) - 1
    cur = [1] + [0] * (deg - 1) if deg >= 1 else []
    out = []
    for a in range(upto):
        out.append(list(cur))
        # multiply by X and reduce by the monic Phi_d
        top = cur[-1]
        cur = [0] + cur[:-1]
        if top:
            for i in range(deg):
                cur[i] -= top * phi[i]
    return out


def set_poly(A, M):
    co = [0] * M
    for a in A:
        assert 0 <= a < M
        co[a] += 1
    return co


def phi_divides(d, A, M):
    """Exact test: does Phi_d divide A(X) = sum_{a in A} X^a ?  (long division, integers)"""
    _, rem = poly_divmod(set_poly(A, M), cyclotomic(d))
    return not any(rem)


def zero_set(A, M):
    """All d | M, d > 1, with Phi_d | A(X)."""
    return [d for d in divisors(M) if d > 1 and phi_divides(d, A, M)]


def selftest():
    import cmath
    known = {
        1: [-1, 1], 2: [1, 1], 3: [1, 1, 1], 4: [1, 0, 1], 6: [1, -1, 1],
        8: [1, 0, 0, 0, 1], 9: [1, 0, 0, 1, 0, 0, 1],
        16: [1] + [0] * 7 + [1],
        36: [1, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 1],
        72: [1] + [0] * 11 + [-1] + [0] * 11 + [1],
    }
    for n, co in known.items():
        assert cyclotomic(n) == co, (n, cyclotomic(n))
    for n in list(range(1, 150)) + [200, 324, 400]:
        co = cyclotomic(n)
        assert len(co) - 1 == euler_phi(n)
        z = cmath.exp(2j * cmath.pi / n)
        assert abs(sum(c * z ** k for k, c in enumerate(co))) < 1e-7, n
        # X^n = 1 mod Phi_n, and residues really are remainders
        R = residues(n, n + 3)
        assert R[n] == R[0] and R[n + 1] == R[1]
    for d in (3, 16, 36, 72, 4, 8, 9, 6):
        R = residues(d, 144)
        for a in (0, 1, 5, 17, 71, 100, 143):
            mono = [0] * a + [1]
            _, rem = poly_divmod(mono, cyclotomic(d))
            assert rem == R[a], (d, a)
    # Z_144 itself: A = all of Z_144 is divisible by every Phi_d, d>1
    assert zero_set(list(range(144)), 144) == [d for d in divisors(144) if d > 1]
    # a subgroup coset {0,72}: 1+X^72 vanishes exactly at d with 144/gcd... d | 144, d not dividing 72
    assert zero_set([0, 72], 144) == [16, 48, 144]
    return True


if __name__ == "__main__":
    print("selftest:", selftest())
