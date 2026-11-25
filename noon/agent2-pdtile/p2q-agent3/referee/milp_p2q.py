"""MILP (HiGHS via scipy.optimize.milp) probes of the counting claims of p2q-agent3.md for prime pairs
that cannot be enumerated (and a few that can, as a cross-check of this script against enum_p2q.py).

Divisibility Phi_d | A: exact integer equalities  sum_i x_i * (X^i mod Phi_d) = 0.
Non-divisibility: by Facts 1/2 plus the affine symmetries of Z_{p^2} x Z_q (which preserve zero sets) it is
enough to impose one strict inequality between two counts:
   Phi_p   not| A :  N10(0) >= N10(1) + 1
   Phi_q   not| A :  N01(0) >= N01(1) + 1
   Phi_p^2 not| A :  N20(0) >= N20(p) + 1
   Phi_pq  not| A :  N11(0,0) - N11(0,1) - N11(1,0) + N11(1,1) >= 1
(only one condition per coordinate is ever normalised at a time, except T6a/T6b which are run separately).
A solver's "infeasible" is the solver's word, not a certificate.
Usage: milp_p2q.py p,q [p,q ...]
"""
import sys
import time
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
import core


def run(p, q):
    M = p * p * q
    P_, P2, Q_, PQ, P2Q = p, p * p, q, p * q, p * p * q
    xs = np.arange(M)

    def div_rows(d):
        return core.res(M, d).T.astype(float)        # (phi(d), M)

    def ind(cond):
        return np.array([1.0 if cond(x) else 0.0 for x in range(M)])

    nd = {
        P_: ind(lambda x: x % p == 0) - ind(lambda x: x % p == 1),
        Q_: ind(lambda x: x % q == 0) - ind(lambda x: x % q == 1),
        P2: ind(lambda x: x % P2 == 0) - ind(lambda x: x % P2 == p),
        PQ: ind(lambda x: x % p == 0 and x % q == 0) - ind(lambda x: x % p == 0 and x % q == 1)
            - ind(lambda x: x % p == 1 and x % q == 0) + ind(lambda x: x % p == 1 and x % q == 1),
    }

    def solve(divs, nondivs, ub, size=None, tl=60):
        cons = []
        for d in divs:
            R = div_rows(d)
            cons.append(LinearConstraint(R, 0, 0))
        for d in nondivs:
            cons.append(LinearConstraint(nd[d][None, :], 1, np.inf))
        if size is not None:
            cons.append(LinearConstraint(np.ones((1, M)), size, size))
        else:
            cons.append(LinearConstraint(np.ones((1, M)), 1, np.inf))
        r = milp(c=np.ones(M), constraints=cons, integrality=np.ones(M), bounds=Bounds(0, ub),
                 options={"time_limit": tl})
        if r.status == 0:
            x = np.round(r.x).astype(int)
            # re-verify the returned (multi)set exactly
            A = [i for i in range(M) for _ in range(x[i])]
            Z = core.zero_set(M, A)
            assert all(d in Z for d in divs), "returned set fails a divisibility"
            assert all(d not in Z for d in nondivs), "returned set fails a non-divisibility"
            return int(x.sum()), sorted(Z)
        if r.status == 2:
            return "infeasible", None
        return f"status {r.status} ({r.message})", None

    t0 = time.time()
    out = []

    def rep(name, expect, got):
        out.append(f"   {name}: {got[0]}" + (f"  zero set {got[1]}" if got[1] else "") + f"   [expected: {expect}]")

    UBM = 2 * p * q   # multiplicity cap for multisets (any feasible multiset of minimal size has entries below this)
    rep("T1  sets  min n | pq in Z; p,q not", f"p+q = {p+q} (claim >= p+q)", solve([PQ], [P_, Q_], 1))
    rep("T2  sets  min n | p2q in Z; p2,q not", f"p+q = {p+q} (claim >= p+q)", solve([P2Q], [P2, Q_], 1))
    rep("T3  sets  n = pq, p,p2q in Z, pq not", "infeasible (Lemma 3(c))", solve([P_, P2Q], [PQ], 1, size=p * q))
    rep("T3m msets n = pq, p,p2q in Z, pq not", "infeasible (Lemma 3(c))", solve([P_, P2Q], [PQ], UBM, size=p * q))
    rep("T4  sets  min n | pq,p2 in Z; p,q not", f"infeasible for sets (referee's remark); note's claim n >= pq+p = {p*q+p}",
        solve([PQ, P2], [P_, Q_], 1))
    rep("T4m msets min n | pq,p2 in Z; p,q not", f"pq+p^2 = {p*q+p*p} (note's claim: >= pq+p = {p*q+p})",
        solve([PQ, P2], [P_, Q_], UBM))
    rep("T5  sets  min n | p,p2q in Z; p2,q not", f"infeasible for sets (referee's remark); note's claim n > p*min(p,q) = {p*min(p,q)}",
        solve([P_, P2Q], [P2, Q_], 1))
    rep("T5m msets min n | p,p2q in Z; p2,q not", f"p(p+q) = {p*(p+q)} (note's claim: > {p*min(p,q)})",
        solve([P_, P2Q], [P2, Q_], UBM))
    rep("T6a sets  pq,p2q in Z; q not, p not", "infeasible for sets (referee's remark)", solve([PQ, P2Q], [Q_, P_], 1))
    rep("T6b sets  pq,p2q in Z; q not, p2 not", "infeasible for sets (referee's remark)", solve([PQ, P2Q], [Q_, P2], 1))
    rep("T6m msets min n | pq,p2q in Z; q,p not", "feasible for multisets", solve([PQ, P2Q], [Q_, P_], UBM))
    print(f"(p,q)=({p},{q}) M={M}   [{time.time()-t0:.1f}s]")
    print("\n".join(out))
    sys.stdout.flush()


for a in sys.argv[1:]:
    p, q = map(int, a.split(","))
    run(p, q)
