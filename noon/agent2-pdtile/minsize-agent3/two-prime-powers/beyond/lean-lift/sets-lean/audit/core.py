# core.py -- exact integer arithmetic for the cyclotomic divisors of mask polynomials of sets and multisets on Z_G.
# Nothing here is taken from the Lean proofs or from the programs of the earlier audits.
#
# Phi_d is computed by exact long division of X^d - 1 by the Phi_e, e | d, e < d (Python integers).
# For a group Z_G the table R has one row per residue y in [0, G): the remainders of X^y modulo Phi_d for every divisor d
# of G, one block per divisor (block of d has length phi(d); the blocks together have length G).  For a multiset with
# multiplicities m(y), Phi_d divides sum m(y) X^y exactly when the block of d of sum m(y) R[y] is zero.
import numpy as np
from numba import njit


def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def poly_divmod_monic(a, b):
    """a, b: lists of Python ints, lowest degree first, b monic.  Returns (quotient, remainder)."""
    a = list(a)
    db = len(b) - 1
    assert b[-1] == 1
    q = [0] * max(1, len(a) - db)
    for i in range(len(a) - 1, db - 1, -1):
        c = a[i]
        if c:
            q[i - db] = c
            for k in range(db + 1):
                a[i - db + k] -= c * b[k]
    return q, a[:db]


_CYC = {}


def cyclotomic(d):
    """coefficients of Phi_d, lowest degree first"""
    if d in _CYC:
        return _CYC[d]
    num = [-1] + [0] * (d - 1) + [1]
    for e in divisors(d):
        if e < d:
            num, rem = poly_divmod_monic(num, cyclotomic(e))
            assert not any(rem)
    while len(num) > 1 and num[-1] == 0:
        num.pop()
    _CYC[d] = num
    return num


def rem_rows(G, d):
    """list of G rows: coefficients of X^y mod Phi_d, y = 0..G-1"""
    phi = cyclotomic(d)
    k = len(phi) - 1
    cur = [1] + [0] * (k - 1)
    rows = []
    for _ in range(G):
        rows.append(cur)
        top = cur[-1]
        nxt = [0] + cur[:-1]
        if top:
            nxt = [nxt[i] - top * phi[i] for i in range(k)]
        cur = nxt
    return rows


class Group:
    """Z_G with its remainder table.  divs: all divisors (1 included).  dgt1: the divisors > 1, in increasing order;
    bit i of a 'mask' stands for dgt1[i]."""

    def __init__(self, G):
        self.G = G
        self.divs = divisors(G)
        self.dgt1 = [d for d in self.divs if d > 1]
        blocks = []
        self.off = {}
        pos = 0
        for d in self.divs:
            rows = rem_rows(G, d)
            blocks.append(np.array(rows, dtype=np.int64).reshape(G, -1))
            self.off[d] = (pos, pos + blocks[-1].shape[1])
            pos += blocks[-1].shape[1]
        assert pos == G
        self.R = np.ascontiguousarray(np.concatenate(blocks, axis=1))
        assert np.abs(self.R).max() < 2 ** 20
        # block boundaries for the divisors > 1 (for the compiled enumerators)
        self.bstart = np.array([self.off[d][0] for d in self.dgt1], dtype=np.int64)
        self.bend = np.array([self.off[d][1] for d in self.dgt1], dtype=np.int64)

    def vec(self, mult):
        """mult: sequence of G multiplicities -> the vector of all remainders"""
        return np.asarray(mult, dtype=np.int64) @ self.R

    def divides(self, v, d):
        a, b = self.off[d]
        return not v[a:b].any()

    def pattern(self, mult, with_one=False):
        """the set of divisors d of G (d > 1 unless with_one) with Phi_d | sum mult[y] X^y"""
        v = self.vec(mult)
        return frozenset(d for d in (self.divs if with_one else self.dgt1) if self.divides(v, d))

    def pattern_of_set(self, elems, with_one=False):
        v = self.R[list(elems)].sum(axis=0) if len(elems) else np.zeros(self.G, dtype=np.int64)
        return frozenset(d for d in (self.divs if with_one else self.dgt1) if self.divides(v, d))

    def mask_to_set(self, mask):
        return frozenset(d for i, d in enumerate(self.dgt1) if (mask >> i) & 1)

    def set_to_mask(self, s):
        m = 0
        for i, d in enumerate(self.dgt1):
            if d in s:
                m |= 1 << i
        return m


def divides_longdiv(G, mult, d):
    """literal check: build sum mult[y] X^y and divide by Phi_d (independent of the table R)"""
    a = [int(x) for x in mult]
    assert len(a) == G
    if d - 1 >= 0 and len(cyclotomic(d)) - 1 > len(a) - 1:
        return not any(a)
    _, rem = poly_divmod_monic(a, cyclotomic(d))
    return not any(rem)


@njit(cache=True)
def _enum(G, R, bstart, bend, T, rep, counts, first_lo, first_hi):
    """All sequences 0 = y1 (<= or <) y2 ... of length t <= T (rep: repetitions allowed, i.e. multisets containing 0;
    otherwise sets containing 0).  counts[t, mask] += 1, mask = the divisors > 1 whose block of the sum is zero.
    Only the sequences whose second element lies in [first_lo, first_hi) are visited beyond length 1 (to split a run);
    the sequence (0) alone is counted when first_lo == 0."""
    nb = bstart.shape[0]
    S = np.zeros((T + 1, G), dtype=np.int64)
    idx = np.zeros(T + 1, dtype=np.int64)
    # level 1: the element 0
    for i in range(G):
        S[1, i] = R[0, i]
    if first_lo == 0:
        mask = 0
        for b in range(nb):
            z = True
            for i in range(bstart[b], bend[b]):
                if S[1, i] != 0:
                    z = False
                    break
            if z:
                mask |= 1 << b
        counts[1, mask] += 1
    if T == 1:
        return
    k = 2
    idx[1] = 0
    start2 = first_lo
    if not rep and start2 < 1:
        start2 = 1
    idx[2] = start2
    while k >= 2:
        y = idx[k]
        lim = G
        if k == 2:
            lim = first_hi
        if y >= lim:
            k -= 1
            if k >= 2:
                idx[k] += 1
            continue
        if k == T:
            # leaf level: do not store the sum; test each block with early exit
            Sp = S[k - 1]
            while y < lim:
                mask = 0
                for b in range(nb):
                    z = True
                    for i in range(bstart[b], bend[b]):
                        if Sp[i] + R[y, i] != 0:
                            z = False
                            break
                    if z:
                        mask |= 1 << b
                counts[k, mask] += 1
                y += 1
            k -= 1
            if k >= 2:
                idx[k] += 1
            continue
        for i in range(G):
            S[k, i] = S[k - 1, i] + R[y, i]
        mask = 0
        for b in range(nb):
            z = True
            for i in range(bstart[b], bend[b]):
                if S[k, i] != 0:
                    z = False
                    break
            if z:
                mask |= 1 << b
        counts[k, mask] += 1
        k += 1
        idx[k] = y if rep else y + 1


def census(grp, T, rep, first_lo=0, first_hi=None):
    """counts[t][mask] for every (multi)set containing 0 with t <= T elements; see _enum"""
    if first_hi is None:
        first_hi = grp.G
    counts = np.zeros((T + 1, 1 << len(grp.dgt1)), dtype=np.int64)
    _enum(grp.G, grp.R, grp.bstart, grp.bend, T, rep, counts, first_lo, first_hi)
    return counts


def patterns_by_size(grp, counts):
    """{t: {frozenset of divisors > 1: number of (multi)sets containing 0}}"""
    out = {}
    for t in range(1, counts.shape[0]):
        row = counts[t]
        nz = np.nonzero(row)[0]
        out[t] = {grp.mask_to_set(int(m)): int(row[m]) for m in nz}
    return out
