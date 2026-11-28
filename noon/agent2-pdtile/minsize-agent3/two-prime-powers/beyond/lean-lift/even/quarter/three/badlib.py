# Exact count of bad signings of a multiset B on Z_n, n odd.
# Method: for each distinct residue r with multiplicity k_r only the signed sum s_r in {-k_r, -k_r+2, .., k_r}
# matters (weight C(k_r, (k_r+s_r)/2)).  A configuration s is bad at d | n iff sum_r s_r zeta_d^r = 0.
# Z[zeta_d] is the tensor product of the Z[zeta_{p^a}], p^a || d, with zeta_d := product of the zeta_{p^a};
# then zeta_d^r = tensor of zeta_{p^a}^(r mod p^a), and zeta_{p^a}^s is written in the basis 1, z, .., z^(phi-1)
# with integer coefficients.  So "bad at d" is: an integer matrix times s is the zero vector.  Exact arithmetic
# (int64; entries are tiny).  A random integer projection is used only as a prefilter; every configuration that
# passes it is checked against the whole matrix, so the answer is exact.
import numpy as np
from fractions import Fraction
from math import comb
from itertools import product

def factor(n):
    f = {}
    p = 2
    while p * p <= n:
        while n % p == 0:
            f[p] = f.get(p, 0) + 1
            n //= p
        p += 1
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f

def divisors(n):
    ds = [1]
    for p, a in factor(n).items():
        ds = [d * p ** i for d in ds for i in range(a + 1)]
    return sorted(ds)

_RP = {}
def red_pp(p, a):
    """matrix (p^a x phi(p^a)): row s = coefficients of X^s mod Phi_{p^a}."""
    key = (p, a)
    if key in _RP:
        return _RP[key]
    q = p ** a
    step = p ** (a - 1)
    phi = (p - 1) * step
    R = np.zeros((q, phi), dtype=np.int64)
    for s in range(q):
        if s < phi:
            R[s, s] = 1
        else:
            u = s - phi
            for j in range(p - 1):
                R[s, u + j * step] = -1
    _RP[key] = R
    return R

def mat_d(d, residues):
    """D x phi(d) integer matrix: row for residue r = coordinates of zeta_d^r."""
    D = len(residues)
    M = np.ones((D, 1), dtype=np.int64)
    for p, a in factor(d).items():
        q = p ** a
        R = red_pp(p, a)
        rows = R[[r % q for r in residues]]            # D x phi(q)
        M = (M[:, :, None] * rows[:, None, :]).reshape(D, -1)
    return M

_rng = np.random.default_rng(12345)

def configs(mults):
    """all configurations of signed sums, and their weights (python ints as int64; fine up to m = 60)."""
    axes = [np.arange(-k, k + 1, 2, dtype=np.int64) for k in mults]
    wax = [np.array([comb(k, j) for j in range(k + 1)], dtype=np.int64) for k in mults]
    C = np.stack(np.meshgrid(*axes, indexing='ij'), axis=-1).reshape(-1, len(mults))
    W = np.ones(1, dtype=np.int64)
    for w in wax:
        W = (W[:, None] * w[None, :]).reshape(-1)
    return C, W

def bad_mask_at(d, residues, C):
    M = mat_d(d, residues)
    if M.shape[1] <= 8:
        return ~((C @ M).any(axis=1))
    w = _rng.integers(-30000, 30001, size=M.shape[1], dtype=np.int64)
    h = M @ w
    cand = np.nonzero((C @ h) == 0)[0]
    mask = np.zeros(C.shape[0], dtype=bool)
    for i in range(0, len(cand), 4096):
        idx = cand[i:i + 4096]
        ok = ~((C[idx] @ M).any(axis=1))
        mask[idx[ok]] = True
    return mask

def bad_count(n, B, divs=None, per_d=False):
    """B: iterable of residues (a multiset).  Returns (number of bad signings, m) [and dict d -> count at d]."""
    cnt = {}
    for b in B:
        cnt[b % n] = cnt.get(b % n, 0) + 1
    residues = sorted(cnt)
    mults = [cnt[r] for r in residues]
    m = sum(mults)
    C, W = configs(mults)
    if divs is None:
        divs = divisors(n)
    bad = np.zeros(C.shape[0], dtype=bool)
    perd = {}
    for d in divs:
        md = bad_mask_at(d, residues, C)
        if per_d:
            perd[d] = int(W[md].sum())
        bad |= md
    tot = int(W[bad].sum())
    if per_d:
        return tot, m, perd
    return tot, m

def bad_share(n, B):
    t, m = bad_count(n, B)
    return Fraction(t, 2 ** m)

# independent slow check: all signings, polynomial remainder modulo Phi_d by exact integer division
def cyclo(d):
    # Phi_d as list of ints (low degree first)
    def polymul(a, b):
        r = [0] * (len(a) + len(b) - 1)
        for i, x in enumerate(a):
            for j, y in enumerate(b):
                r[i + j] += x * y
        return r
    def polydiv(a, b):
        a = a[:]
        q = [0] * (len(a) - len(b) + 1)
        for i in range(len(a) - len(b), -1, -1):
            q[i] = a[i + len(b) - 1] // b[-1]
            for j, y in enumerate(b):
                a[i + j] -= q[i] * y
        assert not any(a)
        return q
    num = [-1] + [0] * (d - 1) + [1]
    for e in divisors(d):
        if e < d:
            num = polydiv(num, cyclo(e))
    return num

def polyrem(a, b):
    a = a[:]
    for i in range(len(a) - len(b), -1, -1):
        c = a[i + len(b) - 1]
        if c:
            for j, y in enumerate(b):
                a[i + j] -= c * y
    return a[:len(b) - 1]

def bad_count_slow(n, B):
    B = [b % n for b in B]
    m = len(B)
    phis = {d: cyclo(d) for d in divisors(n)}
    tot = 0
    for eps in product((1, -1), repeat=m):
        S = [0] * n
        for e, b in zip(eps, B):
            S[b] += e
        for d, ph in phis.items():
            if not any(polyrem(S, ph)):
                tot += 1
                break
    return tot, m

if __name__ == '__main__':
    import random
    random.seed(1)
    nt = 0
    for n in (3, 5, 9, 15, 21, 27, 45, 105, 63, 75):
        for _ in range(12):
            m = random.randint(2, 9)
            if random.random() < 0.5:
                pool = random.sample(range(n), min(n, random.randint(1, 4)))
                B = [random.choice(pool) for _ in range(m)]
            else:
                B = [random.randrange(n) for _ in range(m)]
            a = bad_count(n, B)
            b = bad_count_slow(n, B)
            assert a == b, (n, B, a, b)
            nt += 1
    print('fast = slow on', nt, 'multisets')
    # known values
    print(bad_share(3, [0, 1, 2]), bad_share(3, [0, 0, 1, 2]), bad_share(15, [0, 0, 0, 10, 5]),
          bad_share(105, [0, 0, 0, 0, 0, 70, 35]))
