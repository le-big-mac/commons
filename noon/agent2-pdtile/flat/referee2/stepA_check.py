"""Bonus: test the conclusion of Steps 1-3 of Lemma A at other (p,q) with my own CP-SAT count model.
Counts n(c) on Z_{p^3 q^2} (0 <= n(c) <= p, the number of lifts to Z_M), total p^2 q, with
Phi_q, Phi_{p^3 q^2}, Phi_{p^2 q^2} imposed through exact polynomial remainders.
Claim of Step 3: for each j, N_31(r, j) = 1 on one class r = rho_j mod p and 0 elsewhere.
Given Phi_q (sum_r N_31(r,j) = p^2) the claim fails iff, after a translation,
   (i)  N_31(0,0) >= 2, or
   (ii) N_31(0,0) >= 1 and N_31(r',0) >= 1 for some r' not divisible by p.
Each of these models should be INFEASIBLE.  A feasible base model (no extra constraint) is the control.
Usage: stepA_check.py p q timelimit_per_model
"""
import sys, time
from ortools.sat.python import cp_model
from common import residues, selftest

def model(p, q, extra, tl):
    L = p ** 3 * q ** 2
    size = p * p * q
    m = cp_model.CpModel()
    x = [m.NewIntVar(0, p, f"n{c}") for c in range(L)]
    m.Add(sum(x) == size)
    for d in (q, p ** 3 * q ** 2, p ** 2 * q ** 2):
        R = residues(d, L)
        for k in range(len(R[0])):
            m.Add(sum(R[c][k] * x[c] for c in range(L) if R[c][k]) == 0)
    def N31(r, j):
        return sum(x[c] for c in range(L) if c % p ** 3 == r and c % q == j)
    for (r, j, lo) in extra:
        m.Add(N31(r, j) >= lo)
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = tl
    s.parameters.num_workers = 6
    st = s.Solve(m)
    return s.StatusName(st)

if __name__ == "__main__":
    selftest()
    p, q, tl = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3])
    t0 = time.time()
    print(f"(p,q)=({p},{q}): base model (control, should be feasible): {model(p, q, [], tl)}")
    res = [model(p, q, [(0, 0, 2)], tl)]
    print(f"   (i)  N_31(0,0) >= 2: {res[0]}")
    sys.stdout.flush()
    for r2 in range(1, p ** 3):
        if r2 % p:
            st = model(p, q, [(0, 0, 1), (r2, 0, 1)], tl)
            res.append(st)
            print(f"   (ii) N_31(0,0) >= 1 and N_31({r2},0) >= 1: {st}")
            sys.stdout.flush()
    print(f"   all refutation models infeasible: {all(s == 'INFEASIBLE' for s in res)}   [{time.time()-t0:.1f}s]")
