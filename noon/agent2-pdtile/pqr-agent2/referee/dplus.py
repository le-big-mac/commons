"""Referee's own exact computation of D+(Z) for Z a set of divisors > 1 of M = p0 p1 p2 (squarefree).

Divisors are indexed by nonempty subsets s of {0,1,2} (bitmask 1..7).  Patterns are 7-bit masks in the
convention of enum.c: bit 0,1,2 = p0,p1,p2 ; bit 3 = p0p1, bit 4 = p0p2, bit 5 = p1p2 ; bit 6 = M.

D+(Z) = max sum_x h(x) over real h on Z_M with h(0) = 1, h >= 0, h = 0 off {0} u {elements of order d, d in Z},
hat h >= 0.  Averaging over the units of Z_M (which preserves all constraints and the objective) one may take
h constant on the elements of each order: h = sum_s h_s 1_{order = d_s}.  Then
   hat h (xi) = 1 + sum_s h_s * prod_{w in s} (p_w - 1 if xi_w = 0 else -1),
which only depends on the support e of xi.  So D+(Z) is an LP in at most 7 variables with integer data,
solved here exactly with a rational simplex (Bland's rule).
"""
from fractions import Fraction as Fr
from itertools import combinations

BIT2SUB = [0b001, 0b010, 0b100, 0b011, 0b101, 0b110, 0b111]
SUB2BIT = {s: b for b, s in enumerate(BIT2SUB)}


def simplex_max(c, A, b):
    """maximise c.x subject to A x <= b, x >= 0, with b >= 0.  Exact (Fractions).  Returns (value, x)."""
    m, n = len(A), len(c)
    assert all(bi >= 0 for bi in b)
    # tableau: rows = constraints with slack basis
    T = [[Fr(A[i][j]) for j in range(n)] + [Fr(int(i == k)) for k in range(m)] + [Fr(b[i])] for i in range(m)]
    z = [Fr(-cj) for cj in c] + [Fr(0)] * m + [Fr(0)]
    basis = [n + i for i in range(m)]
    while True:
        # Bland: entering variable = smallest index with negative reduced cost
        ent = next((j for j in range(n + m) if z[j] < 0), None)
        if ent is None:
            break
        best = None
        for i in range(m):
            if T[i][ent] > 0:
                ratio = T[i][-1] / T[i][ent]
                if best is None or ratio < best[0] or (ratio == best[0] and basis[i] < basis[best[1]]):
                    best = (ratio, i)
        if best is None:
            raise ValueError("unbounded")
        r = best[1]
        piv = T[r][ent]
        T[r] = [v / piv for v in T[r]]
        for i in range(m):
            if i != r and T[i][ent] != 0:
                f = T[i][ent]
                T[i] = [vi - f * vr for vi, vr in zip(T[i], T[r])]
        f = z[ent]
        z = [vi - f * vr for vi, vr in zip(z, T[r])]
        basis[r] = ent
    x = [Fr(0)] * n
    for i, bv in enumerate(basis):
        if bv < n:
            x[bv] = T[i][-1]
    return z[-1], x


def kernel(p, s, e):
    """sum over x with support exactly s of chi_xi(x), xi with support e."""
    v = 1
    for w in range(3):
        if s >> w & 1:
            v *= (p[w] - 1) if not (e >> w & 1) else -1
    return v


def dplus(p, mask, want_h=False):
    subs = [BIT2SUB[b] for b in range(7) if mask >> b & 1]
    if not subs:
        return (Fr(1), {}) if want_h else Fr(1)
    c = [kernel(p, s, 0) for s in subs]                       # number of elements of order d_s
    A = [[-kernel(p, s, e) for s in subs] for e in range(8)]  # -sum h_s K(s,e) <= 1
    b = [1] * 8
    val, x = simplex_max(c, A, b)
    # exact verification of primal feasibility and objective
    assert all(xi >= 0 for xi in x)
    for e in range(8):
        assert 1 + sum(xi * kernel(p, s, e) for xi, s in zip(x, subs)) >= 0
    assert val == sum(ci * xi for ci, xi in zip(c, x))
    if want_h:
        return 1 + val, dict(zip(subs, x))
    return 1 + val


def dplus_bruteforce(p, mask):
    """independent exact check: enumerate the vertices of the feasible polytope."""
    subs = [BIT2SUB[b] for b in range(7) if mask >> b & 1]
    k = len(subs)
    if k == 0:
        return Fr(1)
    cons = []   # each: (coeffs, rhs) meaning coeffs.x >= rhs
    for i in range(k):
        cons.append(([Fr(int(i == j)) for j in range(k)], Fr(0)))
    for e in range(8):
        cons.append(([Fr(kernel(p, s, e)) for s in subs], Fr(-1)))
    c = [Fr(kernel(p, s, 0)) for s in subs]
    best = None
    for idx in combinations(range(len(cons)), k):
        Mx = [cons[i][0][:] + [cons[i][1]] for i in idx]
        # gaussian elimination
        ok = True
        for col in range(k):
            piv = next((r for r in range(col, k) if Mx[r][col] != 0), None)
            if piv is None:
                ok = False
                break
            Mx[col], Mx[piv] = Mx[piv], Mx[col]
            pv = Mx[col][col]
            Mx[col] = [v / pv for v in Mx[col]]
            for r in range(k):
                if r != col and Mx[r][col] != 0:
                    f = Mx[r][col]
                    Mx[r] = [a - f * b for a, b in zip(Mx[r], Mx[col])]
        if not ok:
            continue
        x = [Mx[r][k] for r in range(k)]
        if all(sum(a * xi for a, xi in zip(co, x)) >= rhs for co, rhs in cons):
            v = sum(ci * xi for ci, xi in zip(c, x))
            if best is None or v > best:
                best = v
    return 1 + best


def describe(p, mask):
    names = ["p0", "p1", "p2", "p0p1", "p0p2", "p1p2", "M"]
    vals = [p[0], p[1], p[2], p[0] * p[1], p[0] * p[2], p[1] * p[2], p[0] * p[1] * p[2]]
    return "{" + ",".join(str(vals[b]) for b in range(7) if mask >> b & 1) + "}"


if __name__ == "__main__":
    import sys
    p = tuple(int(a) for a in sys.argv[1:4]) if len(sys.argv) >= 4 else (2, 3, 5)
    for mask in range(128):
        d = dplus(p, mask)
        print(mask, describe(p, mask), d)
