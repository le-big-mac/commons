"""Referee's own linear-programming code for the step-complement programmes of Z_{p^3 q^2} (no code shared with the author's).
- coefficients of the programme from the Moebius form of the transform (not from the author's product formula `ram`);
  brute(p, q) recomputes them from actual character sums over Z_M for small M;
- an exact simplex in Fractions whose answers are never trusted: every 'optimal' is returned only after an exact check of a primal
  feasible x and a dual feasible y with equal objective values, every 'infeasible' only after an exact check of a Farkas vector."""
from fractions import Fraction as Fr
cls = [(i, j) for i in range(4) for j in range(3)]; ords = [o for o in cls if o != (0, 0)]; ci = {c: k for k, c in enumerate(cls)}; n = 12; TOP = (3, 2)

def coeff(p, q, o, c):
    """coefficient of f_c in the transform at order o = (l, m): f = sum_d mu_d 1_{dZ}, transform of 1_{dZ} at order (l, m) is M/d if p^l q^m | d, else 0"""
    (l, m), (i, j) = o, c; t = 0
    for di, dj, sg in ((0, 0, 1), (1, 0, -1), (0, 1, -1), (1, 1, 1)):
        i2, j2 = i + di, j + dj
        if i2 <= 3 and j2 <= 2 and i2 >= l and j2 >= m: t += sg * p**(3 - i2) * q**(2 - j2)
    return t

def brute(p, q):
    """the same table from character sums over the group itself (floating point, rounded); for small M only"""
    import numpy as np
    M = p**3 * q**2; x = np.arange(M)
    def val(x, pr, cap):
        v = np.zeros(M, int); y = x.copy()
        for _ in range(cap):
            d = (y % pr == 0) & (v == _); v[d] += 1; y[d] //= pr
        return v
    x0 = x.copy(); x0[0] = M                      # 0 has valuation capped
    vp = val(x0.copy(), p, 3); vq = val(x0.copy(), q, 2); out = {}
    for o in cls:
        xi = M // (p**o[0] * q**o[1])              # a frequency of order p^l q^m
        ch = np.cos(2 * np.pi * ((x * xi) % M) / M)
        for c in cls: out[(o, c)] = int(round(ch[(vp == c[0]) & (vq == c[1])].sum()))
    return out

def _check_opt(A, b, c, allowed, x, y):
    m = len(A)
    assert all(v >= 0 for v in x) and all(x[j] == 0 for j in range(len(c)) if j not in allowed)
    assert all(sum(A[i][j] * x[j] for j in allowed) == b[i] for i in range(m))
    assert all(sum(y[i] * A[i][j] for i in range(m)) <= c[j] for j in allowed)
    assert sum(c[j] * x[j] for j in allowed) == sum(y[i] * b[i] for i in range(m))

def lp(A, b, c, forbid=()):
    """minimise c.x over A x = b, x >= 0, x_j = 0 for j in forbid.  Returns ('optimal', value, x) or ('infeasible', None, None); certified."""
    m, nn = len(A), len(c); A = [[Fr(v) for v in row] for row in A]; b = [Fr(v) for v in b]; c = [Fr(v) for v in c]
    allowed = [j for j in range(nn) if j not in forbid]; sg = [-1 if b[i] < 0 else 1 for i in range(m)]
    T = [[sg[i] * v for v in A[i]] + [Fr(1) if k == i else Fr(0) for k in range(m)] + [sg[i] * b[i]] for i in range(m)]
    basis = [nn + i for i in range(m)]
    def pivot(r, e):
        pv = T[r][e]; T[r] = [v / pv for v in T[r]]
        for i in range(m):
            if i != r and T[i][e] != 0:
                f = T[i][e]; T[i] = [v - f * w for v, w in zip(T[i], T[r])]
        basis[r] = e
    def optimise(cost):
        while True:
            inb = set(basis); enter = None
            for j in allowed:                                   # Bland: the first column with negative reduced cost
                if j in inb: continue
                if cost[j] - sum(cost[basis[i]] * T[i][j] for i in range(m)) < 0: enter = j; break
            if enter is None: return True
            best = None; leave = None
            for i in range(m):
                if T[i][enter] > 0:
                    ratio = T[i][-1] / T[i][enter]
                    if best is None or ratio < best or (ratio == best and basis[i] < basis[leave]): best, leave = ratio, i
            if leave is None: return False
            pivot(leave, enter)
    dual = lambda cost: [sg[i] * sum(cost[basis[k]] * T[k][nn + i] for k in range(m)) for i in range(m)]
    c1 = [Fr(0)] * nn + [Fr(1)] * m
    assert optimise(c1)
    if sum(T[i][-1] for i in range(m) if basis[i] >= nn) != 0:
        y = dual(c1)                                            # Farkas: y.A_j <= 0 for all allowed j and y.b > 0
        assert all(sum(y[i] * A[i][j] for i in range(m)) <= 0 for j in allowed) and sum(y[i] * b[i] for i in range(m)) > 0
        return 'infeasible', None, None
    for i in range(m):
        if basis[i] >= nn:
            j = next((j for j in allowed if T[i][j] != 0), None)
            if j is not None: pivot(i, j)
    c2 = c + [Fr(0)] * m
    assert optimise(c2), 'unbounded'
    x = [Fr(0)] * nn
    for i in range(m):
        if basis[i] < nn: x[basis[i]] = T[i][-1]
        else: assert T[i][-1] == 0
    y = dual(c2); _check_opt(A, b, c, allowed, x, y)
    return 'optimal', sum(c[j] * x[j] for j in range(nn)), x

def solve_square(B, rhs):
    """exact solution of a square system (Fractions); None if singular"""
    m = len(B); T = [[Fr(v) for v in B[i]] + [Fr(rhs[i])] for i in range(m)]
    for col in range(m):
        piv = next((i for i in range(col, m) if T[i][col] != 0), None)
        if piv is None: return None
        T[col], T[piv] = T[piv], T[col]; pv = T[col][col]; T[col] = [v / pv for v in T[col]]
        for i in range(m):
            if i != col and T[i][col] != 0:
                f = T[i][col]; T[i] = [v - f * w for v, w in zip(T[i], T[col])]
    return [T[i][-1] for i in range(m)]

class Prog:
    """all programmes of one pair (p, q)"""
    def __init__(s, p, q):
        s.p, s.q, s.M = p, q, p**3 * q**2
        s.C = {(o, c): coeff(p, q, o, c) for o in cls for c in cls}; s.tot = [s.C[((0, 0), c)] for c in cls]
        s.e = lambda k0: [1 if k == k0 else 0 for k in range(n)]
        s.Pc, s.Qc = ci[(2, 2)], ci[(3, 1)]                    # P \ 0 = class (2, 2), Q \ 0 = class (3, 1)
        s.outp = [k for k, c in enumerate(cls) if c[0] == 0]; s.outq = [k for k, c in enumerate(cls) if c[1] == 0]
    def rows(s, Z):
        R = [s.e(ci[TOP])] + [[s.C[(o, c)] for c in cls] for o in ords if o not in Z]
        return R, [1] + [0] * (len(R) - 1)
    def k(s, Z): return s.p ** sum(1 for l in range(1, 4) if (l, 0) in Z) * s.q ** sum(1 for m in range(1, 3) if (0, m) in Z)
    def props(s, Z):
        """v and a function prop(name) deciding each property by a certified programme: 'b', 'N', 'Rp', 'Rq', 'TP', 'TQ', 'UP', 'UQ', 'M0', 'M2', 'M4'"""
        R, rhs = s.rows(Z); st, v, x = lp(R, rhs, s.tot); assert st == 'optimal'
        D = Fr(s.M) / v; k = s.k(Z); top = TOP in Z; cache = {}
        def prop(name):
            if name in cache: return cache[name]
            if name == 'b': r = D < k
            elif name == 'N': r = (D / k).denominator != 1
            elif name in ('Rp', 'Rq'):
                st2, v2, _ = lp(R, rhs, s.tot, forbid=s.outp if name == 'Rp' else s.outq); r = st2 == 'optimal' and v2 == v
            elif name in ('TP', 'TQ'):
                if top: r = False
                else:
                    st2, v2, _ = lp(R + [s.e(s.Pc if name == 'TP' else s.Qc)], rhs + [1], s.tot); r = st2 == 'optimal' and v2 == v
            elif name in ('UP', 'UQ'):
                if not top: r = False
                else:
                    st2, v2, _ = lp(R + [s.tot], rhs + [v], [-t for t in s.e(s.Pc if name == 'UP' else s.Qc)]); assert st2 == 'optimal'; r = -v2 > 0
            elif name == 'M0': r = top and D == s.p * s.q
            elif name == 'M2': r = top and D == s.p**2 * s.q and {(1, 0), (3, 1), (2, 2)} <= Z
            elif name == 'M4': r = top and D == s.p**2 * s.q and {(0, 1), (1, 2)} <= Z
            cache[name] = r; return r
        return v, D, k, prop
    def category(s, Z):
        """first category that applies, in the order of the author's exact.py (b, N, R, T, U, H) -- for comparing counts with settle72.out"""
        v, D, k, prop = s.props(Z)
        if prop('b'): return 'b', v, prop
        if prop('N'): return 'N', v, prop
        if prop('Rp') or prop('Rq'): return 'R', v, prop
        if prop('TP') or prop('TQ'): return 'T', v, prop
        if prop('UP') or prop('UQ'): return 'U', v, prop
        if prop('M0'): return 'H:M0', v, prop
        if prop('M2'): return 'H:M2', v, prop
        if prop('M4'): return 'H:M4', v, prop
        return 'LEFT', v, prop

def t2_orph(Z):
    t2 = all((l, m) in Z for l in range(1, 4) for m in range(1, 3) if (l, 0) in Z and (0, m) in Z)
    orph = any((l, 0) not in Z and (0, m) not in Z for (l, m) in Z if l and m)
    return t2, orph
def patterns():
    for mask in range(1 << len(ords)): yield frozenset(o for i, o in enumerate(ords) if mask >> i & 1)
