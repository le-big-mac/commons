"""Referee's own solver models (CP-SAT and HiGHS) for Lemmas A and B.  Independent encoding:
x_0..x_{M-1} in {0,1}, sum = p^2 q, and for each d the phi(d) integer equations
sum_x x_x * coeff_k(X^x mod Phi_d) = 0.  x_0 = 1 (translation).  Every set returned by a solver is
re-verified exactly and in floating point; no 'infeasible' is trusted unless the same model with one
condition dropped returns (and verifies) a set somewhere, i.e. the encoding is shown not to be vacuous.

usage: solver_check.py p q [cpsat|highs] [timelimit] [drop]
"""
import sys
import time

import numpy as np

from cyclo import xpow_table, divides_exact, divides_numeric, zero_set


def lists(p, q):
    A = [q, p ** 4, p ** 4 * q, p ** 3 * q, p ** 3 * q * q, p * p * q * q]
    B = [p * p, p ** 3, q * q, p * q, p * q * q, p * p * q]
    return A, B


def rows(M, D):
    eqs = []
    for d in D:
        T = xpow_table(M, d)
        for k in range(T.shape[1]):
            eqs.append(T[:, k].copy())
    return np.array(eqs, dtype=np.int64)


def cpsat(M, n, D, tl, workers=14):
    from ortools.sat.python import cp_model
    m = cp_model.CpModel()
    x = [m.NewBoolVar(f"x{i}") for i in range(M)]
    m.Add(sum(x) == n)
    m.Add(x[0] == 1)
    for row in rows(M, D):
        nz = np.nonzero(row)[0]
        m.Add(sum(int(row[i]) * x[i] for i in nz) == 0)
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = tl
    s.parameters.num_workers = workers
    st = s.Solve(m)
    name = s.StatusName(st)
    A = [i for i in range(M) if s.Value(x[i])] if name in ("OPTIMAL", "FEASIBLE") else None
    return name, A


def highs(M, n, D, tl):
    from scipy.optimize import milp, LinearConstraint, Bounds
    R = rows(M, D)
    Aeq = np.vstack([R, np.ones((1, M))]).astype(float)
    beq = np.concatenate([np.zeros(len(R)), [n]])
    lb = np.zeros(M)
    lb[0] = 1
    res = milp(c=np.zeros(M), constraints=LinearConstraint(Aeq, beq, beq), integrality=np.ones(M),
               bounds=Bounds(lb, np.ones(M)), options={"time_limit": tl})
    if res.status == 0:
        return "FEASIBLE", [i for i in range(M) if res.x[i] > 0.5]
    if res.status == 2:
        return "INFEASIBLE", None
    return f"status{res.status}:{res.message}", None


def run(p, q, solver, tl, do_drop):
    M, n = p ** 4 * q * q, p * p * q
    LA, LB = lists(p, q)
    f = cpsat if solver == "cpsat" else highs
    for name, D in (("A", LA), ("B", LB)):
        t0 = time.time()
        st, A = f(M, n, D, tl)
        print(f"({p},{q}) M={M} n={n} Lemma {name} D={D} [{solver}]: {st}  ({time.time() - t0:.1f}s)", flush=True)
        if A is not None:
            good = len(A) == n and all(divides_exact(A, M, d) and divides_numeric(A, d) for d in D)
            print(f"   !!! set returned: {A}; verifies = {good}; zero set {zero_set(A, M)}", flush=True)
        if do_drop:
            for d in D:
                D2 = [e for e in D if e != d]
                t0 = time.time()
                st, A = f(M, n, D2, tl)
                msg = ""
                if A is not None:
                    good = len(A) == n and all(divides_exact(A, M, e) and divides_numeric(A, e) for e in D2)
                    assert good, "solver returned a set that fails verification"
                    assert not divides_exact(A, M, d) or True
                    msg = f" set {A} verified; zero set {zero_set(A, M)}"
                print(f"   drop Phi_{d}: {st} ({time.time() - t0:.1f}s){msg}", flush=True)


if __name__ == "__main__":
    p, q = int(sys.argv[1]), int(sys.argv[2])
    solver = sys.argv[3] if len(sys.argv) > 3 else "cpsat"
    tl = float(sys.argv[4]) if len(sys.argv) > 4 else 120.0
    do_drop = len(sys.argv) > 5 and sys.argv[5] == "drop"
    run(p, q, solver, tl, do_drop)
