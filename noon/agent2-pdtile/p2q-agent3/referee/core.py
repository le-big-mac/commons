"""Referee's own helpers (written from scratch; nothing imported from the author's scripts).

- cyclotomic polynomials over Z by exact division
- residues of X^i mod Phi_d  (integer vectors)  ->  exact zero sets
- Ramanujan sums / exact Delsarte LP for step functions on Z_M (vertex enumeration over Q)
  and the same LP in floating point via scipy.optimize.linprog
"""
from fractions import Fraction
from itertools import combinations
from math import gcd
import numpy as np


def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def polydiv_exact(num, den):
    """num / den for integer coefficient lists (low -> high), den monic; asserts zero remainder."""
    num = list(num)
    out = [0] * (len(num) - len(den) + 1)
    for i in range(len(out) - 1, -1, -1):
        c = num[i + len(den) - 1]
        out[i] = c
        if c:
            for j, dj in enumerate(den):
                num[i + j] -= c * dj
    assert all(v == 0 for v in num), "non-zero remainder"
    return out


_cyc = {}


def cyclo(n):
    if n not in _cyc:
        num = [-1] + [0] * (n - 1) + [1]
        for d in divisors(n):
            if d < n:
                num = polydiv_exact(num, cyclo(d))
        _cyc[n] = num
    return _cyc[n]


def residues(M, d):
    """R[i] = coefficient vector of X^i mod Phi_d(X), i = 0..M-1 (exact integers)."""
    phi = cyclo(d)
    deg = len(phi) - 1
    R = np.zeros((M, deg), dtype=np.int64)
    cur = [0] * deg
    cur[0] = 1
    for i in range(M):
        R[i] = cur
        top = cur[-1]
        cur = [0] + cur[:-1]
        if top:
            cur = [c - top * phi[j] for j, c in enumerate(cur)]
    return R


_res_cache = {}


def res(M, d):
    if (M, d) not in _res_cache:
        _res_cache[(M, d)] = residues(M, d)
    return _res_cache[(M, d)]


def divides(M, d, A):
    """Phi_d | A(X) for a set/multiset A of residues mod M (exact)."""
    R = res(M, d)
    v = np.zeros(R.shape[1], dtype=np.int64)
    for x in A:
        v += R[x % M]
    return not v.any()


def zero_set(M, A):
    return frozenset(d for d in divisors(M) if d > 1 and divides(M, d, A))


def order(x, M):
    return M // gcd(x % M, M)


def phi_euler(n):
    return sum(1 for y in range(1, n + 1) if gcd(y, n) == 1)


def char_sum(M, d, e):
    """sum over x of order d of exp(2 pi i x xi / M), xi any element of order e. Exact integer
    (Ramanujan sum c_d(M/e)), computed by brute force and rounded, then checked against the
    Moebius-type closed form."""
    xi = M // e
    s = 0.0
    for x in range(M):
        if order(x, M) == d:
            s += np.cos(2 * np.pi * ((x * xi) % M) / M)
    r = int(round(s))
    assert abs(s - r) < 1e-6
    return r


_cs_cache = {}


def char_table(M):
    if M not in _cs_cache:
        D = divisors(M)
        _cs_cache[M] = {(d, e): char_sum(M, d, e) for d in D for e in D}
    return _cs_cache[M]


def solve_frac(Arows, b):
    """Solve square system exactly; return None if singular."""
    n = len(Arows)
    A = [[Fraction(v) for v in row] + [Fraction(bb)] for row, bb in zip(Arows, b)]
    for col in range(n):
        piv = None
        for r in range(col, n):
            if A[r][col] != 0:
                piv = r
                break
        if piv is None:
            return None
        A[col], A[piv] = A[piv], A[col]
        pv = A[col][col]
        A[col] = [v / pv for v in A[col]]
        for r in range(n):
            if r != col and A[r][col] != 0:
                f = A[r][col]
                A[r] = [vr - f * vc for vr, vc in zip(A[r], A[col])]
    return [A[r][n] for r in range(n)]


def dplus_exact(M, Z):
    """Exact D+(Z): maximise sum_x h(x) over step functions h, h(0)=1, h>=0 supported on orders in Z,
    Fourier transform >= 0.  Vertex enumeration over Q (the feasible set is a non-empty polytope:
    h = delta_0 is feasible, and h(x) <= h(0) for positive-definite h)."""
    Z = sorted(Z)
    D = divisors(M)
    T = char_table(M)
    k = len(Z)
    if k == 0:
        return Fraction(1)
    # inequalities  g . h >= c   (h indexed by Z)
    ineq = []
    for i in range(k):
        row = [0] * k
        row[i] = 1
        ineq.append((row, 0))
    for e in D:
        row = [T[(d, e)] for d in Z]
        ineq.append((row, -1))  # 1 + sum h_d C(d,e) >= 0
    obj = [phi_euler(d) for d in Z]
    best = None
    for comb in combinations(range(len(ineq)), k):
        rows = [ineq[i][0] for i in comb]
        rhs = [ineq[i][1] for i in comb]
        sol = solve_frac(rows, rhs)
        if sol is None:
            continue
        ok = all(sum(Fraction(r) * s for r, s in zip(row, sol)) >= c for row, c in ineq)
        if ok:
            val = 1 + sum(o * s for o, s in zip(obj, sol))
            if best is None or val > best:
                best = val
    assert best is not None
    return best


def dplus_float(M, Z):
    from scipy.optimize import linprog
    Z = sorted(Z)
    if not Z:
        return 1.0
    D = divisors(M)
    T = char_table(M)
    c = [-phi_euler(d) for d in Z]
    A_ub = [[-T[(d, e)] for d in Z] for e in D]
    b_ub = [1.0] * len(D)
    r = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=[(0, None)] * len(Z), method="highs")
    assert r.status == 0, r.message
    return 1.0 - r.fun


def crt_pair(u, w, m1, m2):
    """x mod m1*m2 with x = u mod m1, x = w mod m2."""
    for x in range(u % m1, m1 * m2, m1):
        if x % m2 == w % m2:
            return x
    raise ValueError
