"""CP-SAT test on the raw definition, written from scratch.

Variables: one Boolean x_a per a in Z_M.   sum x_a = p^2 q.
For each hypothesis d:   sum_a x_a * (X^a mod Phi_d) = 0   (phi(d) integer equations, from exact
polynomial remainders -- Facts 1/2 of the text are NOT used to build the model).

Usage: cpsat_test.py p q [timelimit_seconds]
Runs Lemma A list, Lemma B list, and every drop-one sublist.  Every set returned by the solver
is re-verified by exact integer long division, and its full zero set {d | M : Phi_d | A} printed.
"""
import sys, time
from ortools.sat.python import cp_model
from common import residues, phi_divides, zero_set, selftest


def solve(M, size, hyps, timelimit, fix0=False, seed=1):
    m = cp_model.CpModel()
    x = [m.NewBoolVar(f"x{a}") for a in range(M)]
    m.Add(sum(x) == size)
    for d in hyps:
        assert M % d == 0
        R = residues(d, M)
        for k in range(len(R[0])):
            m.Add(sum(R[a][k] * x[a] for a in range(M) if R[a][k]) == 0)
    if fix0:
        m.Add(x[0] == 1)  # translation invariance of the conditions (optional symmetry break)
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = timelimit
    s.parameters.num_workers = 8
    s.parameters.random_seed = seed
    t0 = time.time()
    st = s.Solve(m)
    dt = time.time() - t0
    name = s.StatusName(st)
    A = None
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        A = [a for a in range(M) if s.Value(x[a])]
    return name, A, dt


def report(label, M, size, hyps, timelimit):
    name, A, dt = solve(M, size, hyps, timelimit)
    line = f"  {label:28s} hyps={hyps!s:22s} -> {name:10s} ({dt:6.1f}s)"
    if A is not None:
        assert len(A) == size and len(set(A)) == size
        ok = all(phi_divides(d, A, M) for d in hyps)
        line += f"  exact recheck of hyps: {'OK' if ok else 'FAILED'}"
        print(line)
        print(f"      A = {A}")
        print(f"      full zero set {{d | M : Phi_d | A}} = {zero_set(A, M)}")
    else:
        print(line)
    sys.stdout.flush()
    return name, A


if __name__ == "__main__":
    selftest()
    p, q = int(sys.argv[1]), int(sys.argv[2])
    tl = float(sys.argv[3]) if len(sys.argv) > 3 else 120.0
    M, size = p ** 4 * q ** 2, p * p * q
    lists = {
        "Lemma A": [q, p ** 4, p ** 3 * q ** 2, p ** 2 * q ** 2],
        "Lemma B": [p ** 2, p ** 3, q ** 2, p * q],
    }
    print(f"(p,q)=({p},{q})  M={M}  |A|={size}")
    for lname, full in lists.items():
        print(f"{lname}: full list {full}")
        name, A = report(f"{lname} (all four)", M, size, full, tl)
        for d in full:
            sub = [e for e in full if e != d]
            name, A = report(f"{lname} minus Phi_{d}", M, size, sub, tl)
            if A is not None:
                print(f"      dropped Phi_{d} divides this A? {phi_divides(d, A, M)}")
