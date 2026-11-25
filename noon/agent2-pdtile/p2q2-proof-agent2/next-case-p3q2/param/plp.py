"""One-parameter linear programmes for Z_{p^3 q^2} with one prime fixed and the other a variable t.
(Noon = agent2, 21 November 2026.)  Pieces: an exact simplex that also returns the final basis and a dual optimum; the
programme's coefficients as polynomials in t; the basic solution of a given basis as rational functions of t; and the
least t0 beyond which a rational function keeps a given sign (exact real-root isolation)."""
import sys, os
from fractions import Fraction as Fr
import sympy as sp
from sympy import QQ, Poly
from sympy.polys.matrices import DomainMatrix
t = sp.symbols('t')
K = QQ.frac_field(t)

def simplex_full(A, b, c, forbid=()):
    """minimise c.x, A x = b, x >= 0, exactly.  Returns (status, value, x, basis, y): basis = column index per row (n + i is the
    artificial variable of row i, which can remain only on a redundant row, at level 0); y = a dual optimum (y.A <= c, y.b = value)."""
    m, n = len(A), len(c)
    A = [[Fr(v) for v in row] for row in A]; b = [Fr(v) for v in b]; sg = [1] * m
    for i in range(m):
        if b[i] < 0: A[i] = [-v for v in A[i]]; b[i] = -b[i]; sg[i] = -1
    tab = [A[i] + [Fr(1) if j == i else Fr(0) for j in range(m)] + [b[i]] for i in range(m)]
    basis = [n + i for i in range(m)]
    def run(cost, allowed):
        z = [sum(cost[basis[i]] * tab[i][j] for i in range(m)) - cost[j] for j in range(n + m)] + [sum(cost[basis[i]] * tab[i][-1] for i in range(m))]
        while True:
            enter = next((j for j in allowed if z[j] > 0), None)
            if enter is None: return 'optimal', z
            leave = None; best = None
            for i in range(m):
                if tab[i][enter] > 0:
                    r = tab[i][-1] / tab[i][enter]
                    if best is None or r < best or (r == best and basis[i] < basis[leave]): best, leave = r, i
            if leave is None: return 'unbounded', z
            piv = tab[leave][enter]; tab[leave] = [v / piv for v in tab[leave]]
            for i in range(m):
                if i != leave and tab[i][enter] != 0:
                    f = tab[i][enter]; tab[i] = [v - f * w for v, w in zip(tab[i], tab[leave])]
            f = z[enter]; z = [v - f * w for v, w in zip(z, tab[leave])]
            basis[leave] = enter
    st, z = run([Fr(0)] * n + [Fr(1)] * m, [j for j in range(n + m) if j not in forbid])
    if z[-1] != 0: return 'infeasible', None, None, None, None
    for i in range(m):                                    # pivot artificial variables out where a structural column allows it
        if basis[i] >= n:
            j = next((j for j in range(n) if j not in forbid and tab[i][j] != 0), None)
            if j is None: continue
            piv = tab[i][j]; tab[i] = [v / piv for v in tab[i]]
            for k in range(m):
                if k != i and tab[k][j] != 0:
                    f = tab[k][j]; tab[k] = [v - f * w for v, w in zip(tab[k], tab[i])]
            basis[i] = j
    cost = [Fr(v) for v in c] + [Fr(0)] * m
    st, z = run(cost, [j for j in range(n) if j not in forbid])
    if st != 'optimal': return st, None, None, None, None
    x = [Fr(0)] * n
    for i, bi in enumerate(basis):
        if bi < n: x[bi] = tab[i][-1]
        else: assert tab[i][-1] == 0
    y = [sg[i] * z[n + i] for i in range(m)]             # z of the artificial column of row i is c_B B^-1 e_i
    val = sum(Fr(c[j]) * x[j] for j in range(n))
    assert val == z[-1] and all(v >= 0 for v in x)
    assert all(sum(Fr(A0) * xx for A0, xx in zip(row, x)) == bb for row, bb in zip([[sg[i] * v for v in A[i]] for i in range(m)], [sg[i] * v for i, v in enumerate(b)]))
    return 'optimal', val, x, list(basis), y

def ram_sym(p, n, l, i):
    """as steplp.ram, for a number or the symbol t"""
    if i == n: return sp.Integer(1)
    return (p ** (n - i) if l <= i else 0) - (p ** (n - i - 1) if l <= i + 1 else 0)

class Family:
    """M = p^3 q^2 with (p, q) = (c, t) [side 'q' variable] or (t, c) [side 'p' variable]"""
    def __init__(s, c, side):
        s.c, s.side = c, side; s.a, s.b = 3, 2
        s.p, s.q = (sp.Integer(c), t) if side == 'q' else (t, sp.Integer(c))
        s.cls = [(i, j) for i in range(4) for j in range(3)]; s.ords = [o for o in s.cls if o != (0, 0)]; s.top = (3, 2)
        s.C = {(o, cl): sp.expand(ram_sym(s.p, 3, o[0], cl[0]) * ram_sym(s.q, 2, o[1], cl[1])) for o in s.cls for cl in s.cls}
        s.M = s.p ** 3 * s.q ** 2
    def num(s, expr, tv): return Fr(int(sp.Integer(expr.subs(t, tv)))) if isinstance(expr, sp.Basic) else Fr(expr)
    def rows(s, Z, extra=()):
        """symbolic rows and right sides: f_top = 1, transform zero off Z, plus extra (row, rhs) pairs"""
        e = lambda c0: [sp.Integer(1) if c == c0 else sp.Integer(0) for c in s.cls]
        R = [e(s.top)] + [[s.C[(o, c)] for c in s.cls] for o in s.ords if o not in Z]; rhs = [sp.Integer(1)] + [sp.Integer(0)] * (len(R) - 1)
        for r, v in extra: R.append(list(r)); rhs.append(v)
        return R, rhs
    def tot(s): return [s.C[((0, 0), c)] for c in s.cls]
    def k(s, Z): return s.p ** sum(1 for l in range(1, 4) if (l, 0) in Z) * s.q ** sum(1 for m in range(1, 3) if (0, m) in Z)

def to_K(e): return K.from_sympy(sp.sympify(e))
def basic_solution(R, rhs, cost, basis, ncols):
    """x(t) and y(t) of a basis (list of column indices per row; >= ncols means the artificial variable of that row)"""
    m = len(R)
    cols = [[to_K(R[i][j]) for i in range(m)] if j < ncols else [K.one if i == j - ncols else K.zero for i in range(m)] for j in basis]
    B = DomainMatrix([[cols[k][i] for k in range(m)] for i in range(m)], (m, m), K)        # B[i][k] = column k, row i
    xb = B.lu_solve(DomainMatrix([[to_K(v)] for v in rhs], (m, 1), K))
    cb = [to_K(cost[j]) if j < ncols else K.zero for j in basis]
    y = B.transpose().lu_solve(DomainMatrix([[v] for v in cb], (m, 1), K))
    x = {j: xb.rep.to_ddm()[k][0] if hasattr(xb.rep, 'to_ddm') else xb[k, 0].element for k, j in enumerate(basis)}
    yv = [y.rep.to_ddm()[i][0] if hasattr(y.rep, 'to_ddm') else y[i, 0].element for i in range(m)]
    return x, yv

def last_change(expr_K):
    """for a nonzero element of QQ(t): (sign for large t, least integer T such that the sign is constant on [T, oo))"""
    n, d = K.numer(expr_K), K.denom(expr_K)
    pn, pd = Poly(n.as_expr(), t), Poly(d.as_expr(), t)
    sign = (1 if pn.LC() > 0 else -1) * (1 if pd.LC() > 0 else -1); T = 0
    for P in (pn, pd):
        if P.degree() >= 1:
            ivs = P.intervals()                             # isolating intervals of the real roots
            if ivs: T = max(T, int(sp.floor(max(iv[0][1] for iv in ivs))) + 1)
    return sign, T
