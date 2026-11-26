"""Least size of a multiset (or set) on Z_M with prescribed divisors and prescribed non-divisors among the Phi_d.

An integer programme, but not the author's and not the searcher's:
  * "Phi_d | A" is written with the cuboid forms of lib.cuboid_rows (the coefficients of A(X) * prod_{p|d}(1 - X^{d/p}) mod X^d - 1),
    not with remainders modulo Phi_d;
  * "Phi_d does not divide A" is "some cuboid form of scale d is >= 1" (the d forms add up to 0, so not all zero means one is
    positive); for the first non-divisor the position is fixed at 0 by translation;
  * solver: HiGHS through scipy.optimize.milp (branch and bound on a linear programme), or CP-SAT with --solver cpsat (same model).
The answer is accepted only if the solver reports proved optimality (or proved infeasibility); every solution returned is
checked again by lib.pattern (exact).

least(M, need, forbid, binary=False, ub=None, solver='highs', tlimit=120) -> (status, size, A)
   need: divisors d with Phi_d | A;  forbid: d with Phi_d not dividing A (d = 1 means: A is not empty).
"""
import sys, time, json
import numpy as np
from lib import divisors, cuboid_rows, pattern, divides


def build(M, need, forbid, ub):
    """rows of the model: variables x_0..x_{M-1}, then binaries.  Returns (nvar, nbin, eq rows, ge rows)  with rows as (dict, rhs)."""
    eqs, ges = [], []
    nb = 0
    for d in need:
        rows = cuboid_rows(M, d)
        seen = set()
        for r in rows:
            key = tuple(sorted(r.items()))
            if key in seen: continue
            seen.add(key); eqs.append((dict(r), 0))
    forbid = sorted(forbid, reverse=True)
    first = True
    binrows = []
    for d in forbid:
        if d == 1:
            ges.append(({x: 1 for x in range(M)}, 1)); continue
        rows = cuboid_rows(M, d)
        if first:
            ges.append((dict(rows[0]), 1)); first = False; continue
        ids = []
        for t in range(d):
            b = M + nb; nb += 1; ids.append(b)
            r = dict(rows[t]); r[b] = -(ub + 1)                 # E_t - (ub+1) b >= -ub   i.e.  b = 1  =>  E_t >= 1
            ges.append((r, -ub))
        ges.append(({b: 1 for b in ids}, 1))
    ges.append(({x: -1 for x in range(M)}, -ub))                # size <= ub
    return M + nb, nb, eqs, ges


def least(M, need, forbid, binary=False, ub=None, solver='highs', tlimit=120, workers=1):
    if ub is None: ub = M
    nvar, nb, eqs, ges = build(M, need, forbid, ub)
    cap = 1 if binary else ub
    if solver == 'highs':
        from scipy.optimize import milp, LinearConstraint, Bounds
        from scipy.sparse import lil_matrix
        A = lil_matrix((len(eqs) + len(ges), nvar)); lo = []; hi = []
        for i, (r, rhs) in enumerate(eqs):
            for x, c in r.items(): A[i, x] = c
            lo.append(rhs); hi.append(rhs)
        for i, (r, rhs) in enumerate(ges):
            for x, c in r.items(): A[len(eqs) + i, x] = c
            lo.append(rhs); hi.append(np.inf)
        c = np.zeros(nvar); c[:M] = 1
        lb = np.zeros(nvar); ubv = np.ones(nvar); ubv[:M] = cap
        res = milp(c, constraints=LinearConstraint(A.tocsr(), lo, hi), integrality=np.ones(nvar), bounds=Bounds(lb, ubv),
                   options=dict(time_limit=tlimit, mip_rel_gap=0.0, presolve=True))
        if res.status == 0:
            v = [int(round(t)) for t in res.x[:M]]; return 'optimal', sum(v), v
        if res.status == 2: return 'infeasible', None, None
        if res.x is not None:
            v = [int(round(t)) for t in res.x[:M]]; return 'feasible-not-proved', sum(v), v
        return 'unknown', None, None
    else:
        from ortools.sat.python import cp_model
        m = cp_model.CpModel()
        xs = [m.NewIntVar(0, cap, f'x{i}') for i in range(M)] + [m.NewBoolVar(f'b{i}') for i in range(nb)]
        for r, rhs in eqs: m.Add(sum(c * xs[x] for x, c in r.items()) == rhs)
        for r, rhs in ges: m.Add(sum(c * xs[x] for x, c in r.items()) >= rhs)
        m.Minimize(sum(xs[:M])); s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = tlimit; s.parameters.num_search_workers = workers
        st = s.Solve(m)
        if st == cp_model.OPTIMAL:
            v = [s.Value(t) for t in xs[:M]]; return 'optimal', sum(v), v
        if st == cp_model.INFEASIBLE: return 'infeasible', None, None
        if st == cp_model.FEASIBLE:
            v = [s.Value(t) for t in xs[:M]]; return 'feasible-not-proved', sum(v), v
        return 'unknown', None, None


def check(M, need, forbid, v):
    """exact check of a returned solution"""
    for d in need: assert divides(M, d, v), ('solution fails', d)
    for d in forbid: assert not divides(M, d, v), ('solution fails non-divisor', d)


if __name__ == '__main__':
    M = int(sys.argv[1]); need = [int(t) for t in sys.argv[2].split(',') if t]; forbid = [int(t) for t in sys.argv[3].split(',') if t]
    t0 = time.time(); st, sz, v = least(M, need, forbid, solver=sys.argv[4] if len(sys.argv) > 4 else 'highs')
    if v: check(M, need, forbid, v)
    print(st, sz, [f'{i}^{w}' if w > 1 else i for i, w in enumerate(v or []) if w], pattern(M, v) if v else None, round(time.time() - t0, 1))
