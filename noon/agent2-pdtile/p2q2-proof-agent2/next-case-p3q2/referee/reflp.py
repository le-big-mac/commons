"""Referee's own exact LP solver (rational arithmetic) with certificate verification.
min c.x  s.t.  A x = b, x >= 0.
Returns ('optimal', value, x, y)  where y is a dual solution; before returning, the pair (x, y) is verified exactly:
   A x = b, x >= 0, c - A^T y >= 0, c.x = b.y      (LP duality: this PROVES optimality, whatever the pivoting did)
or ('infeasible', None, None, y) with a Farkas vector y:  A^T y <= 0, b.y > 0   (verified exactly)
or ('unbounded', None, None, None).
Written from scratch by the referee; it does not share code with exact.py."""
from fractions import Fraction as Fr


def _independent_rows(A, b):
    """indices of a maximal independent set of rows of A; raises Inconsistent if a dependent row has a wrong rhs.
    Also returns, for the inconsistency case, nothing (handled by phase 1 instead)."""
    n = len(A[0]) if A else 0
    red, keep = [], []
    for i, row in enumerate(A):
        r = [Fr(v) for v in row]
        for pc, rr in red:
            if r[pc] != 0:
                f = r[pc]
                r = [u - f * w for u, w in zip(r, rr)]
        pc = next((j for j in range(n) if r[j] != 0), None)
        if pc is None:
            continue
        piv = r[pc]
        red.append((pc, [u / piv for u in r]))
        keep.append(i)
    return keep


def _solve_square(Bm, rhs):
    """solve Bm z = rhs exactly (Bm square, nonsingular)"""
    m = len(Bm)
    T = [[Fr(v) for v in Bm[i]] + [Fr(rhs[i])] for i in range(m)]
    for col in range(m):
        piv = next(r for r in range(col, m) if T[r][col] != 0)
        T[col], T[piv] = T[piv], T[col]
        pv = T[col][col]
        T[col] = [v / pv for v in T[col]]
        for r in range(m):
            if r != col and T[r][col] != 0:
                f = T[r][col]
                T[r] = [u - f * w for u, w in zip(T[r], T[col])]
    return [T[i][m] for i in range(m)]


def solve_lp(A, b, c):
    m0, n = len(A), len(c)
    A0 = [[Fr(v) for v in row] for row in A]
    b0 = [Fr(v) for v in b]
    c0 = [Fr(v) for v in c]
    # ---------- phase 1 on ALL rows (so that infeasibility of a dependent row is seen), dictionary form
    # variables 0..n-1 structural, n..n+m0-1 artificial
    sgn = [(-1 if b0[i] < 0 else 1) for i in range(m0)]
    T = [[sgn[i] * v for v in A0[i]] + [Fr(1) if k == i else Fr(0) for k in range(m0)] + [sgn[i] * b0[i]] for i in range(m0)]
    basis = [n + i for i in range(m0)]
    N = n + m0

    def pivot(r, col):
        pv = T[r][col]
        T[r] = [v / pv for v in T[r]]
        for i in range(m0):
            if i != r and T[i][col] != 0:
                f = T[i][col]
                T[i] = [u - f * w for u, w in zip(T[i], T[r])]
        basis[r] = col

    def iterate(cost, allowed):
        """primal simplex with Bland's rule on columns in `allowed`; reduced costs recomputed from scratch each time
        (slow but simple and independent of any running z-row)."""
        while True:
            # reduced cost d_j = cost_j - sum_i cost[basis[i]] * T[i][j]
            cb = [cost[basis[i]] for i in range(m0)]
            enter = None
            for j in allowed:
                if j in basis:
                    continue
                d = cost[j] - sum(cb[i] * T[i][j] for i in range(m0) if cb[i] != 0 and T[i][j] != 0)
                if d < 0:
                    enter = j
                    break
            if enter is None:
                return 'optimal'
            best = None
            leave = None
            for i in range(m0):
                if T[i][enter] > 0:
                    ratio = T[i][-1] / T[i][enter]
                    if best is None or ratio < best or (ratio == best and basis[i] < basis[leave]):
                        best, leave = ratio, i
            if leave is None:
                return 'unbounded'
            pivot(leave, enter)

    cost1 = [Fr(0)] * n + [Fr(1)] * m0
    st = iterate(cost1, list(range(N)))
    assert st == 'optimal'
    val1 = sum(T[i][-1] for i in range(m0) if basis[i] >= n)
    if val1 != 0:
        # Farkas certificate from the phase-1 duals: y_i = (cost of basis) B^{-1}; the artificial columns hold B^{-1}
        y = [sgn[k] * sum(cost1[basis[i]] * T[i][n + k] for i in range(m0)) for k in range(m0)]
        # check: A^T y <= 0 and b.y > 0
        assert all(sum(y[i] * A0[i][j] for i in range(m0)) <= 0 for j in range(n)), "Farkas check failed"
        assert sum(y[i] * b0[i] for i in range(m0)) > 0, "Farkas check failed"
        return ('infeasible', None, None, y)
    # drive artificials out where possible; rows where impossible are redundant (all structural entries zero)
    for i in range(m0):
        if basis[i] >= n:
            j = next((j for j in range(n) if T[i][j] != 0), None)
            if j is not None:
                pivot(i, j)
    cost2 = c0 + [Fr(0)] * m0
    st = iterate(cost2, list(range(n)))
    if st == 'unbounded':
        return ('unbounded', None, None, None)
    x = [Fr(0)] * n
    for i in range(m0):
        if basis[i] < n:
            x[basis[i]] = T[i][-1]
        else:
            assert T[i][-1] == 0
    # ---------- dual solution, computed independently of the tableau: solve B^T y = c_B on independent rows
    keep = _independent_rows(A0, b0)
    bcols = [basis[i] for i in range(m0) if basis[i] < n]
    assert len(bcols) == len(keep), (len(bcols), len(keep))
    BT = [[A0[i][j] for i in keep] for j in bcols]          # rows: basic columns; cols: kept rows
    ysub = _solve_square(BT, [c0[j] for j in bcols])
    y = [Fr(0)] * m0
    for t, i in enumerate(keep):
        y[i] = ysub[t]
    # ---------- certificate
    assert all(v >= 0 for v in x), "x >= 0 failed"
    assert all(sum(A0[i][j] * x[j] for j in range(n)) == b0[i] for i in range(m0)), "A x = b failed"
    red = [c0[j] - sum(y[i] * A0[i][j] for i in range(m0)) for j in range(n)]
    assert all(r >= 0 for r in red), "dual feasibility failed"
    val = sum(c0[j] * x[j] for j in range(n))
    assert val == sum(y[i] * b0[i] for i in range(m0)), "duality gap"
    return ('optimal', val, x, y)


if __name__ == '__main__':
    # self-test against scipy on random small problems
    import random
    import numpy as np
    from scipy.optimize import linprog
    random.seed(7)
    nt = bad = 0
    stat = {}
    for _ in range(3000):
        m = random.randint(1, 6)
        n = random.randint(1, 8)
        A = [[random.randint(-3, 3) for _ in range(n)] for _ in range(m)]
        if random.random() < 0.3 and m >= 2:                 # a dependent row
            A[-1] = [A[0][j] + A[1 % m][j] for j in range(n)]
        if random.random() < 0.7:
            x0 = [random.randint(0, 3) for _ in range(n)]
            b = [sum(A[i][j] * x0[j] for j in range(n)) for i in range(m)]
        else:
            b = [random.randint(-3, 3) for _ in range(m)]
        c = [random.randint(-2, 5) for _ in range(n)]
        r = solve_lp(A, b, c)
        s = linprog(c, A_eq=np.array(A, float), b_eq=np.array(b, float), bounds=[(0, None)] * n, method='highs')
        nt += 1
        stat[r[0]] = stat.get(r[0], 0) + 1
        if r[0] == 'optimal':
            if s.status != 0 or abs(s.fun - float(r[1])) > 1e-6:
                bad += 1
                print('MISMATCH', A, b, c, r[:2], s.status, s.fun)
        elif r[0] == 'infeasible':
            if s.status != 2:
                bad += 1
                print('MISMATCH inf', A, b, c, s.status)
        else:
            if s.status != 3:
                bad += 1
                print('MISMATCH unb', A, b, c, s.status)
    print(f"self-test: {nt} random LPs, statuses {stat}, mismatches with scipy/HiGHS: {bad}")
