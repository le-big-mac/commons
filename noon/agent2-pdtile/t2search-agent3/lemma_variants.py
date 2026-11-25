"""Which hypotheses of Lemma A can go?  (agent3 / Yonder, for the review of flatness.md.)
M = p^4 q^2, |A| = p^2 q, 0 in A.  For a list of divisors Z: is there a set with Phi_d | A(X) for all d in Z?
Mixed-integer feasibility with HiGHS through scipy (not CP-SAT, not agent2's models): x in {0,1}^M, and
Phi_d | A stated as  sum_i x_i (X^i mod Phi_d) = 0  with my own integer residues.  Any set returned is
re-verified by exact polynomial division; an "infeasible" is a solver's word and nothing more."""
import sys, time, numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from cyclo_exact import cyclo, polydivmod, divides

def residues(d, M):
    P = cyclo(d); k = len(P) - 1; R = np.zeros((k, M), dtype=np.int64); v = [1] + [0] * (k - 1)
    for i in range(M):
        R[:, i] = v
        top = v[-1]; v = [0] + v[:-1]
        if top: v = [a - top * b for a, b in zip(v, P[:k])]
    return R

def exists(p, q, Z, limit=600):
    M, n = p ** 4 * q ** 2, p * p * q
    rows = [np.ones((1, M), dtype=np.int64)] + [residues(d, M) for d in Z]
    Amat = np.vstack(rows).astype(float); rhs = np.zeros(Amat.shape[0]); rhs[0] = n
    lb = np.zeros(M); lb[0] = 1
    t0 = time.time()
    res = milp(c=np.zeros(M), constraints=LinearConstraint(Amat, rhs, rhs), integrality=np.ones(M), bounds=Bounds(lb, np.ones(M)), options={"time_limit": limit})
    dt = time.time() - t0
    if res.status == 0 and res.x is not None:
        A = [i for i in range(M) if res.x[i] > 0.5]
        assert len(A) == n and all(divides(d, A, M) for d in Z), "solver returned something that is not a solution"
        return "SET (verified exactly)", A, dt
    return {2: "infeasible", 1: "time limit"}.get(res.status, f"status {res.status}"), None, dt

if __name__ == "__main__":
    for p, q in [tuple(map(int, a.split(","))) for a in sys.argv[1:]] or [(2, 3)]:
        names = {q: "q", p**4: "p^4", p**4*q: "p^4q", p**3*q: "p^3q", p**3*q*q: "p^3q^2", p*p*q*q: "p^2q^2"}
        full = list(names)
        cases = [("all six", full)] + [(f"without {names[d]}", [e for e in full if e != d]) for d in full] \
              + [("without p^4q and p^3q", [e for e in full if e not in (p**4*q, p**3*q)])]
        print(f"p={p} q={q} M={p**4*q*q} |A|={p*p*q}")
        for label, Z in cases:
            st, A, dt = exists(p, q, Z)
            print(f"   {label:24s} {st:22s} {dt:6.1f} s  {A if A else ''}", flush=True)
