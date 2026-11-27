# Audit of the eight statements: exact integer arithmetic for mask polynomials and divisibility by cyclotomic polynomials.
# Written for this audit; shares nothing with the Lean files.
#
# A multiset on Z_M is given by its elements as representatives in [0, M) (or by its count vector).  Its mask polynomial is
# sum of X^y over its elements, the exponent being the representative (this is Lean's `maskW`: X ^ a.val).
# For d | M, Phi_d divides X^M - 1 and X^d - 1, so  mask mod Phi_d = sum over elements of (X^(y mod d) mod Phi_d).
# The table C of a group has, in row y, the coefficient vectors of X^(y mod d) mod Phi_d for all d | M, one after another
# (lengths phi(d), total M).  Phi_d | mask  <=>  the block of d in the sum of the rows is zero.  All entries are small integers
# and all sums are exact (int64).
import math
import numpy as np
from numba import njit


def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def polydivmod(a, b):
    """quotient and remainder of a by the monic b; lists of Python integers, lowest degree first"""
    assert b[-1] == 1
    a = list(a)
    db = len(b) - 1
    q = [0] * max(len(a) - db, 0)
    for i in range(len(a) - 1, db - 1, -1):
        c = a[i]
        if c:
            q[i - db] = c
            for j in range(db + 1):
                a[i - db + j] -= c * b[j]
    return q, a[:db]


def polymul(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                out[i + j] += x * y
    return out


def mobius(n):
    m, k = 1, 2
    while k * k <= n:
        if n % k == 0:
            n //= k
            if n % k == 0:
                return 0
            m = -m
        k += 1
    if n > 1:
        m = -m
    return m


_phi = {}


def cyclo(d):
    """Phi_d = prod over e | d of (X^e - 1)^mu(d/e): multiply the numerator factors, divide exactly by the others"""
    assert d >= 1
    if d not in _phi:
        num = [1]
        for e in divisors(d):
            if mobius(d // e) == 1:
                num = polymul(num, [-1] + [0] * (e - 1) + [1])
        for e in divisors(d):
            if mobius(d // e) == -1:
                num, rem = polydivmod(num, [-1] + [0] * (e - 1) + [1])
                assert not any(rem)
        assert num[-1] == 1
        _phi[d] = num
    return _phi[d]


def divides_slow(d, coeffs):
    """does Phi_d divide the integer polynomial with this coefficient list?  (long division, Python integers)"""
    _, rem = polydivmod(list(coeffs), cyclo(d))
    return not any(rem)


def counts(elems, M):
    w = [0] * M
    for y in elems:
        w[y % M] += 1
    return w


def pattern_slow(elems, M, signs=None):
    """set of d | M with Phi_d dividing sum of (+-) X^y, y the representatives in [0, M); literal long division"""
    co = [0] * M
    for i, y in enumerate(elems):
        assert 0 <= y < M
        co[y] += 1 if signs is None else signs[i]
    return frozenset(d for d in divisors(M) if divides_slow(d, co))


class Grp:
    def __init__(self, M):
        self.M = M
        self.divs = divisors(M)
        self.nd = len(self.divs)
        self.bit = {d: 1 << i for i, d in enumerate(self.divs)}
        off = [0]
        blocks = []
        for d in self.divs:
            phi = cyclo(d)
            deg = len(phi) - 1
            R = np.zeros((d, deg), dtype=np.int64)
            for r in range(d):
                _, rem = polydivmod([0] * r + [1], phi)
                R[r, :len(rem)] = rem
            blocks.append(R[np.arange(M) % d])
            off.append(off[-1] + deg)
        assert off[-1] == M
        self.C = np.ascontiguousarray(np.concatenate(blocks, axis=1))
        self.off = np.array(off, dtype=np.int64)

    def mask_of(self, ds):
        m = 0
        for d in ds:
            m |= self.bit[d]
        return m

    def decode(self, code):
        return frozenset(d for d in self.divs if code & self.bit[d])

    def pattern(self, elems, signs=None):
        v = np.zeros(self.M, dtype=np.int64)
        for i, y in enumerate(elems):
            v += self.C[y] * (1 if signs is None else signs[i])
        return self.decode(int(code_of(v, self.off, self.nd)))


@njit(cache=True)
def code_of(vec, off, nd):
    code = 0
    for i in range(nd):
        z = True
        for j in range(off[i], off[i + 1]):
            if vec[j] != 0:
                z = False
                break
        if z:
            code |= (1 << i)
    return code


@njit(cache=True)
def census_kernel(C, off, nd, M, S, tally, exsize, ex):
    """Every multiset of size 1..S on Z_M that contains 0 (first element 0, the rest nondecreasing):
    tally[code, size] += 1, where code = set of d | M with Phi_d | mask;  ex[code] = a first example of least size."""
    vecs = np.zeros((S + 1, M), dtype=np.int64)
    el = np.zeros(S + 1, dtype=np.int64)
    nxt = np.zeros(S + 2, dtype=np.int64)
    t = 1
    el[1] = 0
    vecs[1, :] = C[0, :]
    nxt[1] = 0
    code = code_of(vecs[1], off, nd)
    tally[code, 1] += 1
    if exsize[code] == 0 or exsize[code] > 1:
        exsize[code] = 1
        ex[code, 0] = 0
    nodes = 1
    while t >= 1:
        if t < S and nxt[t] < M:
            y = nxt[t]
            nxt[t] += 1
            t += 1
            el[t] = y
            for j in range(M):
                vecs[t, j] = vecs[t - 1, j] + C[y, j]
            nxt[t] = y
            code = code_of(vecs[t], off, nd)
            tally[code, t] += 1
            nodes += 1
            if exsize[code] == 0 or exsize[code] > t:
                exsize[code] = t
                for i in range(t):
                    ex[code, i] = el[i + 1]
        else:
            t -= 1
    return nodes


def census(M, S):
    """returns (G, tally, exsize, ex, nodes).  tally[code, t] = number of multisets of size t containing 0 with exactly the
    divisor set `code` (among all d | M, d = 1 included)."""
    G = Grp(M)
    tally = np.zeros((1 << G.nd, S + 1), dtype=np.int64)
    exsize = np.zeros(1 << G.nd, dtype=np.int64)
    ex = np.zeros((1 << G.nd, S), dtype=np.int64)
    nodes = census_kernel(G.C, G.off, G.nd, M, S, tally, exsize, ex)
    assert nodes == math.comb(M + S - 1, S - 1), (nodes, math.comb(M + S - 1, S - 1))
    for t in range(1, S + 1):
        assert int(tally[:, t].sum()) == math.comb(M + t - 2, t - 1)
    return G, tally, exsize, ex, nodes


def census_nodes(M, S):
    return math.comb(M + S - 1, S - 1)
