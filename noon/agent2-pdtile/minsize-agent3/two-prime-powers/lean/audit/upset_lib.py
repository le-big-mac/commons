"""Library for the audit of Pnq/Upset.lean: a translation of the Lean text into a program.

Nothing here comes from the Lean proof.  Two layers:

* a SLOW, LITERAL layer in pure Python integers (no numpy): the definitions exactly as the Lean text has them
  (`IsUpSet`, `corners`, `maskW`, divisibility by a cyclotomic polynomial by long division in Z[X], the
  existence of the family g by exhaustive search);
* a FAST layer in numpy integer arithmetic (int64, exact; no floating point) for bulk enumeration, checked
  against the slow layer in selftest.py.

Lean text translated here
-------------------------
def IsUpSet (M : N) (D : Finset N) : Prop :=
  (forall d in D, d | M and d != 1) and forall d in D, forall e, d | e -> e | M -> e in D
def corners (M : N) (D : Finset N) : Finset N :=
  (M.divisors \\ D).filter (fun c => forall e in M.divisors \\ D, c | e -> e = c)
def maskW (w : ZMod M -> N) : Polynomial Z := sum over a : ZMod M of C (w a) * X ^ a.val
Nat.divisors n = {d in Ico 1 (n + 1) | d | n}
"""
import itertools
from math import comb

import numpy as np

# ----------------------------------------------------------------------------------------------------------
# slow, literal layer
# ----------------------------------------------------------------------------------------------------------

def nat_dvd(a, b):
    """a | b in the natural numbers, as Lean has it: exists c, b = a * c  (so 0 | b iff b = 0)"""
    if a == 0:
        return b == 0
    return b % a == 0


def nat_divisors(n):
    """Nat.divisors n = {d in Ico 1 (n + 1) | d | n}   (empty for n = 0)"""
    return [d for d in range(1, n + 1) if nat_dvd(d, n)]


def is_upset_lean(M, D):
    """IsUpSet M D, read literally.  The quantifier over e is over all naturals; e | M with M > 0 forces
    e <= M, so e is run over 0 .. M (for M = 0 this function is not meant to be used)."""
    assert M > 0
    D = set(D)
    first = all(nat_dvd(d, M) and d != 1 for d in D)
    second = all((not nat_dvd(d, e)) or (not nat_dvd(e, M)) or (e in D) for d in D for e in range(0, M + 1))
    return first and second


def corners_lean(M, D):
    """corners M D, read literally"""
    D = set(D)
    base = [d for d in nat_divisors(M) if d not in D]            # M.divisors \ D
    return sorted(c for c in base if all((not nat_dvd(c, e)) or e == c for e in base))


def all_upsets(M):
    """every subset of the divisors of M that IsUpSet accepts (subsets with a non-divisor are rejected by the
    first clause of IsUpSet, so nothing is lost by starting from the divisors)"""
    dv = nat_divisors(M)
    out = []
    for k in range(len(dv) + 1):
        for D in itertools.combinations(dv, k):
            if is_upset_lean(M, D):
                out.append(tuple(D))
    return out


# --- polynomials over Z as lists of Python ints, lowest degree first -----------------------------------------

def ptrim(a):
    a = list(a)
    while a and a[-1] == 0:
        a.pop()
    return a


def pmul(a, b):
    if not a or not b:
        return []
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                out[i + j] += x * y
    return ptrim(out)


def pdivmod_monic(a, b):
    """long division of a by the MONIC polynomial b in Z[X]: a = q * b + r, deg r < deg b"""
    b = ptrim(b)
    assert b and b[-1] == 1
    r = list(a) + [0] * max(0, len(b) - len(a))
    q = [0] * max(1, len(r) - len(b) + 1)
    for k in range(len(r) - len(b), -1, -1):
        c = r[k + len(b) - 1]
        if c:
            q[k] = c
            for j, y in enumerate(b):
                r[k + j] -= c * y
    return ptrim(q), ptrim(r[:len(b) - 1])


_cyc = {}


def cyclotomic(n):
    """Phi_n by its defining identity: the product of Phi_d over the divisors d of n is X^n - 1
    (Mathlib: Polynomial.prod_cyclotomic_eq_X_pow_sub_one).  n >= 1."""
    assert n >= 1
    if n not in _cyc:
        num = [-1] + [0] * (n - 1) + [1]
        for d in nat_divisors(n):
            if d < n:
                num, rem = pdivmod_monic(num, cyclotomic(d))
                assert rem == []
        _cyc[n] = num
    return _cyc[n]


def mask(w):
    """maskW w: the coefficient of X^a is w(a), a = 0 .. M - 1  (a.val is the representative in [0, M))"""
    return ptrim([int(x) for x in w])


def cyc_divides_mask(d, w):
    """Polynomial.cyclotomic d Z | maskW w, by long division in Z[X] (Phi_d is monic, so divisibility in Z[X]
    holds exactly when the remainder is 0).  Phi_0 = 1 in Mathlib."""
    if d == 0:
        return True
    return pdivmod_monic(mask(w), cyclotomic(d))[1] == []


def orbits_add(M, c):
    """the classes of x ~ x + (c : ZMod M); (c : ZMod M) is c mod M.  g (x + c) = g x for all x says exactly
    that g is constant on these classes."""
    seen = [False] * M
    out = []
    for x in range(M):
        if not seen[x]:
            orb = []
            y = x
            while not seen[y]:
                seen[y] = True
                orb.append(y)
                y = (y + c) % M
            out.append(sorted(orb))
    return out


def periodic(g, M, c):
    """forall x, g (x + c) = g x"""
    return all(g[(x + c) % M] == g[x] for x in range(M))


def exists_g(w, M, cs):
    """the right-hand side of structure_iff, by exhaustive search: is there a family g_c (c in cs), each with
    values in N and periodic under adding c, with w = sum of the g_c?  Returns a family or None.
    (g is indexed by all naturals in Lean; only its values at the corners occur.)"""
    w = [int(x) for x in w]
    if not cs:
        return {} if all(x == 0 for x in w) else None
    c = cs[0]
    if len(cs) == 1:
        return {c: list(w)} if periodic(w, M, c) else None
    orbs = orbits_add(M, c)
    caps = [min(w[x] for x in orb) for orb in orbs]
    for vals in itertools.product(*[range(k + 1) for k in caps]):
        g = [0] * M
        for orb, v in zip(orbs, vals):
            for x in orb:
                g[x] = v
        rest = [a - b for a, b in zip(w, g)]
        sub = exists_g(rest, M, cs[1:])
        if sub is not None:
            sub = dict(sub)
            sub[c] = g
            return sub
    return None


def lhs_structure(w, D):
    """forall d in D, Phi_d | maskW w"""
    return all(cyc_divides_mask(d, w) for d in D)


def hyp_corners(w, cs):
    """forall c in corners, not (Phi_c | maskW w)"""
    return all(not cyc_divides_mask(c, w) for c in cs)


def exact_pattern(w, M, D):
    """forall d, d | M -> d != 1 -> (Phi_d | maskW w <-> d in D)"""
    D = set(D)
    return all(cyc_divides_mask(d, w) == (d in D) for d in nat_divisors(M) if d != 1)


def corner_sum(M, cs):
    """sum over the corners of M / c (natural-number division)"""
    return sum(M // c for c in cs)


# ----------------------------------------------------------------------------------------------------------
# fast layer (numpy, integers only)
# ----------------------------------------------------------------------------------------------------------

def enum_le(k, S, dtype=np.uint8):
    """all vectors of N^k with sum <= S, as rows; there are comb(k + S, k) of them"""
    rows = np.zeros((1, 0), dtype=dtype)
    sums = np.zeros(1, dtype=np.int64)
    for _ in range(k):
        cnt = S - sums + 1                        # number of values for the new coordinate
        idx = np.repeat(np.arange(len(rows)), cnt)
        start = np.cumsum(cnt) - cnt
        v = np.arange(len(idx)) - np.repeat(start, cnt)
        rows = np.concatenate([rows[idx], v[:, None].astype(dtype)], axis=1)
        sums = sums[idx] + v
    assert len(rows) == comb(k + S, k)
    return rows


def enum_le_chunks(k, S, chunk=2_000_000, dtype=np.uint8):
    """the same vectors in chunks: fix a prefix of j coordinates, extend each block of prefixes"""
    if comb(k + S, k) <= chunk or k <= 2:
        yield enum_le(k, S, dtype)
        return
    # the largest block is the one of the prefix 0…0, with comb(k - j + S, k - j) rows: take the prefix long
    # enough for that block to fit in `chunk` (a shorter prefix once gave a block of 86 million rows)
    j = 1
    while j < k - 1 and comb(k - j + S, k - j) > chunk:
        j += 1
    pre = enum_le(j, S, dtype)
    psum = pre.sum(axis=1).astype(np.int64)
    # group prefixes so that each group gives at most about `chunk` rows
    sizes = np.array([comb(k - j + S - int(s), k - j) for s in psum], dtype=object)
    start = 0
    while start < len(pre):
        end = start
        tot = 0
        while end < len(pre) and (tot == 0 or tot + sizes[end] <= chunk):
            tot += sizes[end]
            end += 1
        rows = pre[start:end]
        sums = psum[start:end].copy()
        for _ in range(k - j):
            cnt = S - sums + 1
            idx = np.repeat(np.arange(len(rows)), cnt)
            st = np.cumsum(cnt) - cnt
            v = np.arange(len(idx)) - np.repeat(st, cnt)
            rows = np.concatenate([rows[idx], v[:, None].astype(dtype)], axis=1)
            sums = sums[idx] + v
        assert len(rows) == tot and len(rows) <= max(chunk, S + 1), 'a chunk is larger than asked for'
        yield rows
        start = end


def rem_matrix(M, d):
    """integer matrix whose row a is X^a mod Phi_d (a = 0 .. M - 1); the remainder of the mask of w modulo
    Phi_d is then w @ rem_matrix (the map w -> remainder is linear over Z)"""
    phi = cyclotomic(d)
    deg = len(phi) - 1
    R = np.zeros((M, deg), dtype=np.int64)
    for a in range(M):
        r = pdivmod_monic([0] * a + [1], phi)[1]
        R[a, :len(r)] = r
    return R


def div_flags(W, M, ds):
    """for every row w of W and every d in ds: does Phi_d divide the mask of w?  (exact integer arithmetic)"""
    W64 = W.astype(np.int64)
    out = {}
    for d in ds:
        R = rem_matrix(M, d)
        out[d] = ~np.any(W64 @ R, axis=1) if R.shape[1] else np.ones(len(W), dtype=bool)
    return out


def lattice_T(M, D):
    """For P = product of Phi_d (d in D), monic of degree M - r with P(0) = +-1: every w whose mask is
    divisible by P is q(X) P(X) with deg q < r, hence determined by its first r coefficients.  Returns
    (r, T) with T an integer r x (M - r) matrix such that w[r:] = w[:r] @ T on that lattice."""
    P = [1]
    for d in D:
        P = pmul(P, cyclotomic(d))
    r = M - (len(P) - 1)
    assert r >= 1 and abs(P[0]) == 1 and P[-1] == 1
    B = np.zeros((r, M), dtype=object)
    for i in range(r):
        for j, c in enumerate(P):
            B[i, i + j] = c
    # head = q @ H with H = B[:, :r] upper triangular, diagonal P[0] = +-1; invert it over Z by back-substitution
    H = B[:, :r]
    Hinv = np.zeros((r, r), dtype=object)
    for i in range(r):                    # solve x @ H = e_i
        x = [0] * r
        for j in range(r):                # column j of H involves x_0 .. x_j
            s = sum(x[t] * H[t, j] for t in range(j))
            x[j] = ((1 if j == i else 0) - s) * H[j, j]          # H[j, j] = +-1 is its own inverse
        Hinv[i, :] = x
    assert np.array_equal(Hinv.dot(H), np.eye(r, dtype=object))
    T = Hinv.dot(B[:, r:])
    return r, np.array(T.tolist(), dtype=np.int64).reshape(r, M - r)


def solutions_lattice(M, D, S, chunk=2_000_000):
    """all w in N^M with sum <= S whose mask is divisible by Phi_d for every d in D, through the lattice:
    run over the first r coordinates, compute the others, keep the non-negative ones.  The other coordinates
    are computed two at a time and the heads with a negative one dropped at once (only for speed)."""
    D = tuple(D)
    if not D:
        return np.concatenate(list(enum_le_chunks(M, S, chunk)), axis=0)
    r, T = lattice_T(M, D)
    assert int(np.abs(T).max()) * S * r < 2 ** 31            # int32 arithmetic below is exact
    T32 = T.astype(np.int32)
    keep = []
    for head in enum_le_chunks(r, S, chunk):
        h = head.astype(np.int32)
        idx = np.arange(len(h))
        for a in range(0, M - r, 2):
            part = h[idx] @ T32[:, a:a + 2]
            idx = idx[(part >= 0).all(axis=1)]
            if len(idx) == 0:
                break
        if len(idx):
            hh = h[idx]
            rest = hh @ T32
            assert (rest >= 0).all()
            ok = (hh.sum(axis=1) + rest.sum(axis=1)) <= S
            if ok.any():
                keep.append(np.concatenate([hh[ok], rest[ok]], axis=1).astype(np.uint8))
    if not keep:
        return np.zeros((0, M), dtype=np.uint8)
    return np.concatenate(keep, axis=0)


def sums_of_periodic(M, cs, S):
    """all w in N^M with sum <= S that are a sum over c in cs of functions with values in N periodic under
    adding c: every such function is a combination, with coefficients in N, of the indicators of the classes
    of x ~ x + c, so the set is generated by adding indicators.  Rows are distinct."""
    W = np.zeros((1, M), dtype=np.uint8)
    sums = np.zeros(1, dtype=np.int64)
    for ci, c in enumerate(cs):
        for orb in orbits_add(M, c):
            size = len(orb)
            ind = np.zeros(M, dtype=np.uint8)
            ind[orb] = 1
            cnt = (S - sums) // size + 1
            idx = np.repeat(np.arange(len(W)), cnt)
            st = np.cumsum(cnt) - cnt
            k = (np.arange(len(idx)) - np.repeat(st, cnt))
            W = W[idx] + (k[:, None].astype(np.uint8) * ind[None, :])
            sums = sums[idx] + k * size
        if ci > 0:                              # duplicates can only arise from the second corner on
            W = np.unique(W, axis=0)
            sums = W.sum(axis=1, dtype=np.int64)
    return W


def same_rows(A, B):
    """do the two arrays have the same set of rows?"""
    A = np.unique(A, axis=0)
    B = np.unique(B, axis=0)
    return A.shape == B.shape and bool(np.array_equal(A, B))
