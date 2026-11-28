"""Exact tools written by the referee: cyclotomic polynomials by integer division, remainders of X^k modulo Phi_d,
all signings as a matrix.  A signing is bad at d iff the remainder of its signed mask modulo Phi_d is 0."""
import cmath
import numpy as np

_phi = {}


def cyclotomic(d):
    """coefficients (low degree first) of Phi_d, from X^d - 1 = product of Phi_e over e | d"""
    if d in _phi:
        return _phi[d]
    num = [-1] + [0] * (d - 1) + [1]
    for e in range(1, d):
        if d % e == 0:
            den = cyclotomic(e)
            # exact long division num / den (den monic)
            num = num[:]
            quo = [0] * (len(num) - len(den) + 1)
            for i in range(len(quo) - 1, -1, -1):
                t = num[i + len(den) - 1]
                quo[i] = t
                if t:
                    for j, y in enumerate(den):
                        num[i + j] -= t * y
            assert not any(num), "division not exact"
            num = quo
    # sanity: vanishes at a primitive d-th root of unity, monic, degree = Euler phi
    z = cmath.exp(2j * cmath.pi / d)
    assert abs(sum(c * z ** k for k, c in enumerate(num))) < 1e-7
    assert num[-1] == 1 and len(num) - 1 == sum(1 for k in range(1, d + 1) if np.gcd(k, d) == 1)
    _phi[d] = num
    return num


_rm = {}


def rem_matrix(n, d):
    """integer array (n, phi(d)): row k = coefficients of X^k modulo Phi_d"""
    if (n, d) in _rm:
        return _rm[(n, d)]
    ph = cyclotomic(d); deg = len(ph) - 1
    rows = []
    cur = [0] * deg
    if deg:
        cur[0] = 1
    for k in range(n):
        rows.append(cur[:])
        top = cur[-1] if deg else 0
        cur = [0] + cur[:-1]
        if top:
            for j in range(deg):
                cur[j] -= top * ph[j]
    out = np.array(rows, dtype=np.int64).reshape(n, deg)
    _rm[(n, d)] = out
    return out


def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


_sg = {}


def signs(m):
    """(2^m, m) matrix of all sign vectors"""
    if m not in _sg:
        idx = np.arange(2 ** m, dtype=np.int64)[:, None]
        _sg[m] = 1 - 2 * ((idx >> np.arange(m, dtype=np.int64)[None, :]) & 1)
    return _sg[m]


def bad_at(n, B, d, E=None):
    """boolean vector over all signings: Phi_d divides the signed mask"""
    if E is None:
        E = signs(len(B))
    R = E @ rem_matrix(n, d)[B]
    return ~np.any(R != 0, axis=1)


def three_bad_at(n, B, d, E=None):
    """boolean vector: the remainder modulo Phi_d has all coefficients divisible by 3"""
    if E is None:
        E = signs(len(B))
    R = E @ rem_matrix(n, d)[B]
    return ~np.any(R % 3 != 0, axis=1)


def factor(n):
    f = {}
    p = 2
    while n > 1:
        while n % p == 0:
            f[p] = f.get(p, 0) + 1; n //= p
        p += 1
    return f


def live_levels(B, q, vq):
    """levels j in 1..vq of the q-tree of B at which some class modulo q^(j-1) has all q subclasses occupied"""
    out = []
    for j in range(1, vq + 1):
        occ = {}
        for b in B:
            occ.setdefault(b % q ** (j - 1), set()).add(b % q ** j)
        if any(len(s) == q for s in occ.values()):
            out.append(j)
    return out
