"""Bonus (beyond the (2,3) brief): my CP-SAT model at other (p,q), full four-hypothesis lists only.
mode 'set'      : Boolean x_a (A a subset of Z_M)
mode 'multiset' : integer x_a in [0, p^2 q]  (the proofs never use that A is a set)
Usage: cpsat_extra.py p q mode timelimit
"""
import sys, time
from ortools.sat.python import cp_model
from common import residues, phi_divides, zero_set, selftest

def solve(M, size, hyps, timelimit, multiset):
    m = cp_model.CpModel()
    x = [m.NewIntVar(0, size if multiset else 1, f"x{a}") for a in range(M)]
    m.Add(sum(x) == size)
    for d in hyps:
        R = residues(d, M)
        for k in range(len(R[0])):
            m.Add(sum(R[a][k] * x[a] for a in range(M) if R[a][k]) == 0)
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = timelimit
    s.parameters.num_workers = 8
    t0 = time.time()
    st = s.Solve(m)
    A = None
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        A = [a for a in range(M) for _ in range(s.Value(x[a]))]
    return s.StatusName(st), A, time.time() - t0

if __name__ == "__main__":
    selftest()
    p, q, mode, tl = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], float(sys.argv[4])
    M, size = p ** 4 * q ** 2, p * p * q
    for lname, hyps in (("Lemma A", [q, p ** 4, p ** 3 * q ** 2, p ** 2 * q ** 2]),
                        ("Lemma B", [p ** 2, p ** 3, q ** 2, p * q])):
        name, A, dt = solve(M, size, hyps, tl, mode == "multiset")
        print(f"(p,q)=({p},{q}) M={M} size={size} {mode:8s} {lname} hyps={hyps}: {name} ({dt:.1f}s)"
              + (f"  A={A}" if A else ""))
        sys.stdout.flush()
