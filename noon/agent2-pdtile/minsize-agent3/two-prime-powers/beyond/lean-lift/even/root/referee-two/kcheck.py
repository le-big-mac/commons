# Referee's recomputation of the constants K of section 6 of two/result.md (data, not used in a proof).
# Brief's definition: h copies of 0 and a decoration D; K_same(D) = the expected number of distinct integers v of
# the parity of h (h even here, the decorations have an even number of elements) among the values -Q(zeta),
# zeta^n = 1, Q the signed mask of D.  -Q(zeta) = v for the roots zeta of order d  <=>  Phi_d divides v + Q(X):
# with R_d the matrix of X^j mod Phi_d, the first coordinate of R_d Q must be -v and the others 0.
# Decorations made of pairs: each pair has signed sum -2, 0, 2 with weights 1, 2, 1.
# With "pp" only d = 1 and the prime powers are counted.
import sys, itertools
import numpy as np
from fractions import Fraction as F

def divisors(n): return [d for d in range(1, n + 1) if n % d == 0]
def pdiv(num, den):
    num = num[:]; q = [0] * (len(num) - len(den) + 1)
    for i in range(len(q) - 1, -1, -1):
        t = num[i + len(den) - 1]; q[i] = t
        for j, dj in enumerate(den): num[i + j] -= t * dj
    assert not any(num)
    return q
_cy = {}
def cyclo(d):
    if d not in _cy:
        num = [-1] + [0] * (d - 1) + [1]
        for e in divisors(d):
            if e < d: num = pdiv(num, cyclo(e))
        _cy[d] = num
    return _cy[d]
def redmat(d):
    ph = cyclo(d); k = len(ph) - 1
    cols = []; cur = [1] + [0] * (k - 1)
    for j in range(d):
        cols.append(cur[:])
        t = cur[-1]; cur = [0] + cur[:-1]
        if t:
            for i in range(k): cur[i] -= t * ph[i]
    return np.array(cols, dtype=np.int64).T
def isprimepower(d):
    for p in range(3, d + 1, 2):
        if d % p == 0:
            while d % p == 0: d //= p
            return d == 1
    return False

def K(n, pairs, only_pp=False):
    k = len(pairs)
    V = np.array(list(itertools.product((-2, 0, 2), repeat=k)), dtype=np.int64)      # pair sums
    W = np.array([1 if x else 2 for x in (-2, 0, 2)], dtype=np.int64)[(V // 2) + 1].prod(axis=1)
    vals = []        # for each d: the integer v (or a sentinel) for each outcome
    for d in divisors(n):
        if only_pp and d > 1 and not isprimepower(d): continue
        R = redmat(d); Q = V @ R[:, [b % d for b in pairs]].T               # (outcomes, phi)
        ok = ~(Q[:, 1:] != 0).any(axis=1) if Q.shape[1] > 1 else np.ones(len(V), dtype=bool)
        vals.append(np.where(ok & (Q[:, 0] % 2 == 0), -Q[:, 0], 10**6 + len(vals)))
    A = np.sort(np.stack(vals, axis=1), axis=1)
    distinct = (A < 10**6).sum(axis=1) - ((np.diff(A, axis=1) == 0) & (A[:, 1:] < 10**6)).sum(axis=1)
    return F(int((distinct * W).sum()), 4 ** k)

cases = [
    ("Z_3: pairs at 1, 2", 3, [1, 2]),
    ("Z_9: pairs at 1, 2, 3, 6", 9, [1, 2, 3, 6]),
    ("Z_27: pairs at 1, 2, 3, 6, 9, 18", 27, [1, 2, 3, 6, 9, 18]),
    ("Z_81: pairs at 1, 2, 3, 6, 9, 18, 27, 54", 81, [1, 2, 3, 6, 9, 18, 27, 54]),
    ("Z_45: pairs at 5, 10, 15, 30 and 9, 18, 27, 36", 45, [5, 10, 15, 30, 9, 18, 27, 36]),
    ("Z_135: pairs at 5, 10, 15, 30, 45, 90 and 27, 54, 81, 108", 135, [5, 10, 15, 30, 45, 90, 27, 54, 81, 108]),
]
for name, n, pairs in cases:
    k_all = K(n, pairs); k_pp = K(n, pairs, True)
    print(f"{name}: K = {k_all} = {float(k_all):.6f} (times sqrt(2/pi): {float(k_all)*0.7978845608:.6f}); counting d = 1 and prime powers only: {k_pp}; difference {k_all - k_pp}", flush=True)
