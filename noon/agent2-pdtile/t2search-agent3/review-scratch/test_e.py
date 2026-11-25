"""(e) exactlp.lp against (1) HiGHS and (2) an independent exact method (enumeration of all basic solutions in rational arithmetic
for the optimum value / feasibility; exact unboundedness test through a recession-direction programme solved by vertex enumeration too).
Families: degenerate (many zero right-hand sides, repeated/dependent rows, zero rows, zero columns, duplicate columns),
redundant-but-consistent and redundant-and-inconsistent systems, fractional data, and programmes of the same shape as the scripts'
(f(0) = 1, integer 'transform' rows = 0, objective = +-class sizes)."""
import sys, random, itertools, time
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import linprog
sys.dont_write_bytecode = True
sys.path.insert(0, "/home/agent3/t2search")
from exactlp import lp

def solve_square(Bm, rhs):
    """exact Gaussian elimination; returns the unique solution or None if singular"""
    n = len(Bm); T = [list(map(Fr, row)) + [Fr(r)] for row, r in zip(Bm, rhs)]
    for c in range(n):
        pr = next((r for r in range(c, n) if T[r][c] != 0), None)
        if pr is None: return None
        T[c], T[pr] = T[pr], T[c]; pv = T[c][c]; T[c] = [v / pv for v in T[c]]
        for r in range(n):
            if r != c and T[r][c] != 0:
                f = T[r][c]; T[r] = [x - f * y for x, y in zip(T[r], T[c])]
    return [T[r][n] for r in range(n)]

def rank_rows(A, b):
    """row-reduce [A | b]; return (independent rows of A, their b) or None if inconsistent"""
    rows = [list(map(Fr, r)) + [Fr(v)] for r, v in zip(A, b)]; n = len(A[0]); out = []; piv = []
    for r in rows:
        r = r[:]
        for (pr, pc) in zip(out, piv):
            if r[pc] != 0:
                f = r[pc] / pr[pc]; r = [x - f * y for x, y in zip(r, pr)]
        pc = next((j for j in range(n) if r[j] != 0), None)
        if pc is None:
            if r[n] != 0: return None
            continue
        out.append(r); piv.append(pc)
    return [r[:n] for r in out], [r[n] for r in out]

def vertices(A, b):
    """all basic feasible solutions of A x = b, x >= 0 (exact).  None if the system A x = b is inconsistent."""
    rr = rank_rows(A, b)
    if rr is None: return None
    A2, b2 = rr; m = len(A2); n = len(A[0]); out = []
    if m == 0: return [[Fr(0)] * n]
    for cols in itertools.combinations(range(n), m):
        sol = solve_square([[A2[i][j] for j in cols] for i in range(m)], b2)
        if sol is None or any(v < 0 for v in sol): continue
        x = [Fr(0)] * n
        for j, v in zip(cols, sol): x[j] = v
        out.append(x)
    return out

def exact_reference(A, b, c):
    """('infeasible' | 'unbounded' | 'optimal', value) by vertex enumeration.  Unbounded iff feasible and there is d >= 0, A d = 0, c d < 0;
       normalise sum d = 1 and enumerate the vertices of that polytope."""
    V = vertices(A, b)
    if not V: return "infeasible", None
    n = len(A[0])
    R = vertices([list(r) for r in A] + [[1] * n], [0] * len(A) + [1])
    if R and min(sum(Fr(ci) * di for ci, di in zip(c, d)) for d in R) < 0: return "unbounded", None
    return "optimal", min(sum(Fr(ci) * xi for ci, xi in zip(c, x)) for x in V)

def gen(kind, rnd):
    if kind == "degenerate":
        m, n = rnd.randint(1, 5), rnd.randint(2, 8)
        A = [[rnd.choice([0, 0, 0, 1, -1, 2, -2]) for _ in range(n)] for _ in range(m)]
        b = [rnd.choice([0, 0, 0, 1, 2]) for _ in range(m)]; c = [rnd.randint(-3, 3) for _ in range(n)]
    elif kind == "redundant":
        m0, n = rnd.randint(1, 3), rnd.randint(2, 8)
        A = [[rnd.randint(-3, 3) for _ in range(n)] for _ in range(m0)]; x0 = [rnd.choice([0, 0, 1, 2, 3]) for _ in range(n)]
        b = [sum(a * x for a, x in zip(r, x0)) for r in A]                         # feasible by construction
        for _ in range(rnd.randint(1, 3)):                                           # dependent rows (consistent, sometimes inconsistent), zero rows
            co = [rnd.randint(-2, 2) for _ in range(len(A))]
            A.append([sum(k * r[j] for k, r in zip(co, A)) for j in range(n)]); b.append(sum(k * v for k, v in zip(co, b)) + (rnd.choice([0, 0, 0, 0, 1, -1])))
        if rnd.random() < 0.3: A.append([0] * n); b.append(rnd.choice([0, 0, 0, 1]))
        if rnd.random() < 0.3:
            j = rnd.randrange(n)
            for r in A: r[j] = 0                                                     # a zero column
        if rnd.random() < 0.3 and n >= 2:
            j, l = rnd.sample(range(n), 2)
            for r in A: r[l] = r[j]                                                  # duplicate columns
        order = list(range(len(A))); rnd.shuffle(order); A = [A[i] for i in order]; b = [b[i] for i in order]
        c = [rnd.randint(-3, 3) for _ in range(n)]
    elif kind == "fractional":
        m, n = rnd.randint(1, 4), rnd.randint(2, 7)
        A = [[Fr(rnd.randint(-5, 5), rnd.randint(1, 4)) for _ in range(n)] for _ in range(m)]
        b = [Fr(rnd.randint(-4, 6), rnd.randint(1, 3)) for _ in range(m)]; c = [Fr(rnd.randint(-5, 5), rnd.randint(1, 3)) for _ in range(n)]
    elif kind == "scriptlike":                                                         # first row: one variable = 1; other rows integer, rhs 0; cost = +-positive sizes
        n = rnd.randint(3, 9); m = rnd.randint(1, 6)
        A = [[int(j == n - 1) for j in range(n)]] + [[rnd.choice([-6, -3, -2, -1, -1, 0, 1, 1, 2, 3, 6]) for _ in range(n)] for _ in range(m)]
        if rnd.random() < 0.5 and m >= 2: A[-1] = [x + y for x, y in zip(A[1], A[2] if m >= 3 else A[1])]
        b = [1] + [0] * m; sz = [rnd.randint(1, 24) for _ in range(n - 1)] + [1]; sg = rnd.choice([1, -1]); c = [sg * v for v in sz]
    return A, b, c

if __name__ == "__main__":
    rnd = random.Random(20261120); t0 = time.time()
    for kind, ntr in [("degenerate", 2500), ("redundant", 2500), ("fractional", 1500), ("scriptlike", 2500)]:
        kinds = {}; bad_h = bad_x = 0; nred = 0
        for trial in range(ntr):
            A, b, c = gen(kind, rnd)
            st, val, x = lp(A, b, c)
            if st == "optimal":
                assert all(v >= 0 for v in x) and all(sum(Fr(a) * v for a, v in zip(row, x)) == Fr(bi) for row, bi in zip(A, b)), "returned point is not feasible"
                assert val == sum(Fr(ci) * xi for ci, xi in zip(c, x))
            rs, rv = exact_reference(A, b, c)
            okx = (st == rs) and (st != "optimal" or val == rv)
            r = linprog([float(v) for v in c], A_eq=np.array([[float(v) for v in row] for row in A]), b_eq=[float(v) for v in b], bounds=[(0, None)] * len(c), method="highs")
            hs = {0: "optimal", 2: "infeasible", 3: "unbounded"}.get(r.status, f"status {r.status}")
            okh = (st == hs) and (st != "optimal" or abs(float(val) - r.fun) < 1e-7)
            kinds[st] = kinds.get(st, 0) + 1; bad_x += not okx; bad_h += not okh
            rr = rank_rows(A, b); nred += (rr is not None and len(rr[0]) < len(A))
            if not okx: print("DISAGREE with exact reference:", kind, st, val, rs, rv, A, b, c)
            if not okh and okx: print("   (HiGHS differs from both exact methods:", kind, st, val, hs, r.fun, ")")
        print(f"{kind:11s}: {ntr} programmes ({nred} consistent with redundant rows): {kinds};  disagreements with exact vertex enumeration: {bad_x};  with HiGHS: {bad_h}", flush=True)
    print(f"{time.time() - t0:.0f} s")
