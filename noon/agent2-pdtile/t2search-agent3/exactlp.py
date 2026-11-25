"""A small exact linear-programming routine (rational arithmetic, Bland's rule), for programmes with a dozen variables.  (agent3 / Yonder)
lp(A, b, c): minimise c.x subject to A x = b, x >= 0, all entries integers or Fractions.
Returns ("infeasible", None, None), ("unbounded", None, None) or ("optimal", value, x) with exact Fractions."""
from fractions import Fraction as Fr
def _pivot(T, basis, r, s):
    piv = T[r][s]; T[r] = [v / piv for v in T[r]]
    for i in range(len(T)):
        if i != r and T[i][s] != 0:
            f = T[i][s]; T[i] = [vi - f * vr for vi, vr in zip(T[i], T[r])]
    basis[r] = s
def _simplex(T, basis, ncols, allowed):
    """T: rows of constraints then the objective row last (reduced costs); minimise.  allowed: columns that may enter."""
    m = len(T) - 1
    while True:
        s = next((j for j in allowed if T[m][j] < 0), None)                      # Bland: smallest index with negative reduced cost
        if s is None: return "optimal"
        best = None
        for i in range(m):
            if T[i][s] > 0:
                ratio = T[i][ncols] / T[i][s]
                if best is None or ratio < best[0] or (ratio == best[0] and basis[i] < basis[best[1]]): best = (ratio, i)
        if best is None: return "unbounded"
        _pivot(T, basis, best[1], s)
def lp(A, b, c):
    m, n = len(A), len(A[0])
    A = [[Fr(v) for v in row] for row in A]; b = [Fr(v) for v in b]; c = [Fr(v) for v in c]
    for i in range(m):
        if b[i] < 0: A[i] = [-v for v in A[i]]; b[i] = -b[i]
    # phase 1: artificial variables n .. n+m-1
    T = [A[i] + [Fr(int(i == k)) for k in range(m)] + [b[i]] for i in range(m)]
    obj = [Fr(0)] * n + [Fr(1)] * m + [Fr(0)]
    for i in range(m): obj = [o - t for o, t in zip(obj, T[i])]                  # reduced costs with the artificial basis
    T.append(obj); basis = [n + i for i in range(m)]
    _simplex(T, basis, n + m, list(range(n + m)))
    if -T[m][n + m] != 0: return "infeasible", None, None
    for i in range(m):                                                           # drive artificial variables out of the basis where possible
        if basis[i] >= n:
            s = next((j for j in range(n) if T[i][j] != 0), None)
            if s is not None: _pivot(T, basis, i, s)
    keep = [i for i in range(m) if basis[i] < n]                                 # rows still artificial are redundant constraints
    T2 = [T[i][:n] + [T[i][n + m]] for i in keep]; basis2 = [basis[i] for i in keep]
    obj = c + [Fr(0)]
    for i, bi in enumerate(basis2):
        if obj[bi] != 0:
            f = obj[bi]; obj = [o - f * t for o, t in zip(obj, T2[i])]
    T2.append(obj)
    st = _simplex(T2, basis2, n, list(range(n)))
    if st == "unbounded": return "unbounded", None, None
    x = [Fr(0)] * n
    for i, bi in enumerate(basis2): x[bi] = T2[i][n]
    return "optimal", sum(ci * xi for ci, xi in zip(c, x)), x
if __name__ == "__main__":
    import random, numpy as np
    from scipy.optimize import linprog
    random.seed(3); agree = 0; kinds = {}
    for trial in range(3000):
        m, n = random.randint(1, 6), random.randint(2, 9)
        A = [[random.randint(-3, 3) for _ in range(n)] for _ in range(m)]; b = [random.randint(-2, 4) for _ in range(m)]; c = [random.randint(-3, 3) for _ in range(n)]
        st, val, x = lp(A, b, c)
        r = linprog(c, A_eq=np.array(A, float), b_eq=np.array(b, float), bounds=[(0, None)] * n, method="highs")
        st2 = {0: "optimal", 2: "infeasible", 3: "unbounded"}.get(r.status, f"status {r.status}")
        ok = (st == st2) and (st != "optimal" or abs(float(val) - r.fun) < 1e-7)
        if st == "optimal": assert all(v >= 0 for v in x) and all(sum(Fr(a) * v for a, v in zip(row, x)) == bi for row, bi in zip(A, b))
        agree += ok; kinds[st] = kinds.get(st, 0) + 1
        if not ok: print("DISAGREE", st, st2, val, r.fun, A, b, c)
    print(f"exact routine against HiGHS on 3000 random small programmes: {agree} agree;  {kinds}")
