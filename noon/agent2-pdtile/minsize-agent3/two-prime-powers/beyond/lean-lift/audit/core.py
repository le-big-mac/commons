# Audit helper: exact integer polynomial arithmetic for mask polynomials and cyclotomic divisibility.
# Shares nothing with the Lean proof.  A multiset on Z_M is a list w of M natural numbers, w[y] the multiplicity of the
# residue with representative y in [0, M); its mask polynomial is sum_y w[y] X^y, so its coefficient list is w itself.
import itertools
import numpy as np

def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]

def totient(n):
    from math import gcd
    return sum(1 for k in range(1, n + 1) if gcd(k, n) == 1)

def poly_divmod_monic(a, b):
    """quotient and remainder of a by the monic b; integer coefficient lists, lowest degree first"""
    assert b[-1] == 1
    a = list(a); db = len(b) - 1
    q = [0] * max(len(a) - db, 0)
    for i in range(len(a) - 1, db - 1, -1):
        c = a[i]
        if c:
            q[i - db] = c
            for j in range(db + 1):
                a[i - db + j] -= c * b[j]
    return q, a[:db]

_cyc = {}
def cyclotomic(d):
    """Phi_d over Z: (X^d - 1) divided (exactly) by the Phi_e for the proper divisors e of d"""
    assert d >= 1
    if d not in _cyc:
        num = [-1] + [0] * (d - 1) + [1]
        for e in divisors(d):
            if e < d:
                num, rem = poly_divmod_monic(num, cyclotomic(e))
                assert not any(rem)
        assert num[-1] == 1 and len(num) - 1 == totient(d)
        _cyc[d] = num
    return _cyc[d]

def divides(d, w):
    """does Phi_d divide the polynomial with coefficient list w (in Z[X])?  Phi_d is monic, so: remainder zero"""
    _, rem = poly_divmod_monic(w, cyclotomic(d))
    return not any(rem)

def reduce_mod(w, N):
    """the reduction modulo N of the multiset w on Z_M (N | M): multiplicity of x = number of elements with residue x"""
    out = [0] * N
    for y, c in enumerate(w):
        out[y % N] += c
    return out

def rem_table(M, d):
    """T[y] = coefficients of X^y mod Phi_d, y in [0, M); by long division each time"""
    phi = cyclotomic(d)
    T = np.zeros((M, len(phi) - 1), dtype=np.int32)
    for y in range(M):
        _, rem = poly_divmod_monic([0] * y + [1], phi)
        T[y, :len(rem)] = rem
    return T

def multisets(M, s):
    """all multisets of size s on Z_M as nondecreasing tuples of representatives (a generator; nothing is stored)"""
    return itertools.combinations_with_replacement(range(M), s)

def multiset_chunks(M, s, chunk=200000, lo=0):
    """the same in numpy blocks of shape (k, s); with lo>0 only elements >= lo are used"""
    it = itertools.combinations_with_replacement(range(lo, M), s)
    if s == 0:
        yield np.zeros((1, 0), dtype=np.int16); return
    while True:
        block = np.fromiter(itertools.chain.from_iterable(itertools.islice(it, chunk)), dtype=np.int16)
        if block.size == 0:
            return
        yield block.reshape(-1, s)

def counts_of(t, M):
    w = [0] * M
    for y in t:
        w[y] += 1
    return w

class Group:
    """Z_M with the remainder tables of all Phi_d, d | M"""
    def __init__(self, M):
        self.M = M
        self.divs = divisors(M)
        self.T = {d: rem_table(M, d) for d in self.divs}
        self.bit = {d: 1 << i for i, d in enumerate(self.divs)}
    def divset_block(self, idx, extra=None):
        """for a block of multisets (rows of representatives; extra = a fixed list of further elements in every row):
        the code of the set {d | M : Phi_d divides the mask}, bit i for the i-th divisor"""
        k = idx.shape[0]
        code = np.zeros(k, dtype=np.int64)
        for d in self.divs:
            T = self.T[d]
            rem = np.zeros((k, T.shape[1]), dtype=np.int32)
            for i in range(idx.shape[1]):
                rem += T[idx[:, i]]
            if extra:
                for y in extra:
                    rem += T[y]
            code |= np.where(rem.any(axis=1), 0, self.bit[d])
        return code
    def divset(self, w):
        """slow, literal: the set of d | M with Phi_d dividing the mask of the count vector w (long division)"""
        return frozenset(d for d in self.divs if divides(d, w))
    def decode(self, code):
        return frozenset(d for d in self.divs if code & self.bit[d])

def census(M, S, fix_zero=False, chunk=200000):
    """{divisor-set : set of sizes s <= S at which some multiset of size s on Z_M has exactly that set of d | M
    with Phi_d dividing its mask}.  fix_zero: only multisets containing the residue 0 are enumerated for s >= 1
    (every multiset has a translate containing 0, and translation multiplies the mask by X^t modulo X^M - 1)."""
    G = Group(M)
    out = {}
    n = 0
    for s in range(0, S + 1):
        if fix_zero and s >= 1:
            gen = multiset_chunks(M, s - 1, chunk); extra = [0]
        else:
            gen = multiset_chunks(M, s, chunk); extra = None
        for idx in gen:
            n += idx.shape[0]
            for c in np.unique(G.divset_block(idx, extra)):
                out.setdefault(G.decode(int(c)), set()).add(s)
    return out, n
