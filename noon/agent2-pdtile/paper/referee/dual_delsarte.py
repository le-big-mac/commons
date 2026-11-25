"""Referee checks for Remark 'dual' and for Remark 3 of the last section of weak-pqr.tex.

(1) Duality as phrased in Remark 'dual', for every nonempty A in Z_M containing 0 (M small):
      A is a weak tile   <=>   min{ sum G : G >= 0, G(0) >= 1, Ghat = 0 wherever 1_A hat = 0 } = |A|.
    Weak tile is decided by a direct LP on f (no step functions, no Delsarte).
(2) The criterion quoted in Remark 3: weak tile <=> D^w(Z_A) = |A|, pd-tile <=> D^+(Z_A) = |A|.
(3) The numbers D^+({2,3,5,30}) = 120/19, D^w = 15/2 at M = 30 (exact, sympy simplex), and
    'first at M = 30' (floating point scan of all patterns for 2 <= M <= 30).
"""
import itertools, math, sys
import numpy as np
from scipy.optimize import linprog
import sympy as sp

TOL = 1e-7

def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]

def ramanujan(d, x):
    g = math.gcd(d, x)
    return sum(sp.mobius(d // e) * e for e in divisors(g))

def zero_orders(A, M):
    """orders d>1 of frequencies at which 1_A hat vanishes (a union of classes, by Galois)"""
    Z = []
    for d in divisors(M):
        if d == 1:
            continue
        xi = M // d
        s = sum(np.exp(2j * np.pi * a * xi / M) for a in A)
        if abs(s) < 1e-9:
            Z.append(d)
    return Z

def weak_tile_direct(A, M, pd=False):
    """max f(0) s.t. f >= 0, 1_A * f = 1 (and fhat >= 0 if pd). Returns the max."""
    Aeq = np.zeros((M, M))
    for v in range(M):
        for a in A:
            Aeq[v, (v - a) % M] += 1
    c = np.zeros(M); c[0] = -1
    Aub = bub = None
    if pd:
        # fhat real for real even part; impose Re fhat(xi) >= 0 and Im fhat = 0 is not needed: average f with f(-x)
        rows = []
        for xi in range(M):
            rows.append([-math.cos(2 * math.pi * xi * x / M) for x in range(M)])
        Aub = np.array(rows); bub = np.zeros(M)
        # symmetrise: f(x) = f(-x) (wlog, by averaging) so that fhat is real
        E = []
        for x in range(1, M):
            y = (-x) % M
            if x < y:
                r = np.zeros(M); r[x] = 1; r[y] = -1; E.append(r)
        if E:
            Aeq = np.vstack([Aeq, np.array(E)])
    beq = np.concatenate([np.ones(M), np.zeros(Aeq.shape[0] - M)])
    r = linprog(c, A_ub=Aub, b_ub=bub, A_eq=Aeq, b_eq=beq, bounds=[(0, None)] * M, method='highs')
    assert r.status == 0, r.message
    return -r.fun

def dual_min_mass(A, M):
    """min sum G : G >= 0, G(0) >= 1, Ghat(xi) = 0 for every xi with 1_A hat(xi) = 0."""
    Z = zero_orders(A, M)
    rows = []
    for xi in range(1, M):
        if (M // math.gcd(xi, M)) in Z:
            rows.append([math.cos(2 * math.pi * xi * x / M) for x in range(M)])
            rows.append([math.sin(2 * math.pi * xi * x / M) for x in range(M)])
    bounds = [(1, None)] + [(0, None)] * (M - 1)
    if rows:
        r = linprog(np.ones(M), A_eq=np.array(rows), b_eq=np.zeros(len(rows)), bounds=bounds, method='highs')
    else:
        r = linprog(np.ones(M), bounds=bounds, method='highs')
    assert r.status == 0, r.message
    return r.fun

def delsarte(M, Z, plus, exact=False):
    """max 1 + sum_{d in Z} phi(d) h_d  s.t. 1 + sum_d h_d c_d(x) >= 0 for all x; h_d >= 0 if plus."""
    Z = sorted(Z)
    if not Z:
        return sp.Integer(1) if exact else 1.0
    gs = divisors(M)
    if exact:
        hs = sp.symbols('h0:%d' % len(Z), real=True)
        cons = [1 + sum(h * ramanujan(d, g) for h, d in zip(hs, Z)) >= 0 for g in gs]
        if plus:
            cons += [h >= 0 for h in hs]
        else:
            # free variables: write h = u - w
            us = sp.symbols('u0:%d' % len(Z), nonnegative=True)
            ws = sp.symbols('w0:%d' % len(Z), nonnegative=True)
            sub = {h: u - w for h, u, w in zip(hs, us, ws)}
            cons = [c.subs(sub) for c in cons] + [u >= 0 for u in us] + [w >= 0 for w in ws]
            obj = (1 + sum(sp.totient(d) * h for h, d in zip(hs, Z))).subs(sub)
            from sympy.solvers.simplex import lpmax
            return lpmax(obj, cons)[0]
        from sympy.solvers.simplex import lpmax
        return lpmax(1 + sum(sp.totient(d) * h for h, d in zip(hs, Z)), cons)[0]
    c = -np.array([float(sp.totient(d)) for d in Z])
    Aub = -np.array([[float(ramanujan(d, g)) for d in Z] for g in gs])
    bub = np.ones(len(gs))
    r = linprog(c, A_ub=Aub, b_ub=bub, bounds=[(0, None) if plus else (None, None)] * len(Z), method='highs')
    assert r.status == 0, (M, Z, r.message)
    return 1 - r.fun

if __name__ == '__main__':
    # (1), (2)
    for M in [int(s) for s in sys.argv[1:]] or [6, 8, 9, 10, 12, 15]:
        n = weak = bad_dual = bad_dw = pdt = bad_dp = weak_not_pd = 0
        for r in range(0, M):
            for rest in itertools.combinations(range(1, M), r):
                A = (0,) + rest
                n += 1
                w = weak_tile_direct(A, M) > 1 - TOL
                g = dual_min_mass(A, M)
                assert g <= len(A) + TOL          # (1_A * 1_{-A})/|A| is admissible
                if w != (g > len(A) - TOL):
                    bad_dual += 1
                Z = zero_orders(A, M)
                dw = delsarte(M, Z, plus=False)
                if w != (abs(dw - len(A)) < TOL) or dw > len(A) + TOL or abs(dw - g) > 1e-6:
                    bad_dw += 1
                pd = weak_tile_direct(A, M, pd=True) > 1 - TOL
                dp = delsarte(M, Z, plus=True)
                if pd != (abs(dp - len(A)) < TOL):
                    bad_dp += 1
                weak += w; pdt += pd; weak_not_pd += (w and not pd)
        print(f'M={M}: {n} sets containing 0; weak tiles {weak}; pd-tiles {pdt}; weak but not pd {weak_not_pd}; '
              f'duality mismatches {bad_dual}; "weak <=> D^w=|A|" (and D^w = dual min) mismatches {bad_dw}; '
              f'"pd <=> D^+=|A|" mismatches {bad_dp}', flush=True)
    # (3)
    print('exact, M=30, Z={2,3,5,30}:  D^+ =', delsarte(30, [2, 3, 5, 30], True, exact=True),
          '  D^w =', delsarte(30, [2, 3, 5, 30], False, exact=True))
    print('exact, M=30, Z={2,6,10,15}: D^+ =', delsarte(30, [2, 6, 10, 15], True, exact=True),
          '  D^w =', delsarte(30, [2, 6, 10, 15], False, exact=True))
    for M in range(2, 31):
        ds = [d for d in divisors(M) if d > 1]
        diff = []
        for r in range(len(ds) + 1):
            for Z in itertools.combinations(ds, r):
                a, b = delsarte(M, Z, True), delsarte(M, Z, False)
                assert a <= b + 1e-7
                if b - a > 1e-6:
                    diff.append((Z, round(a, 6), round(b, 6)))
        if diff:
            print('M =', M, ': D^w > D^+ on', len(diff), 'of', 2 ** len(ds), 'patterns:', diff)
    print('scan 2..30 done (no line for M means D^w = D^+ on every pattern)')
