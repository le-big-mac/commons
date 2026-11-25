r"""Z_{p^n q}: solver tests of Lemma L and Claim T in groups too large for brute force (agent3 / Yonder).
HiGHS through scipy; Phi_d | A as integer linear equations (residues of X^i mod Phi_d); any set returned is re-verified
exactly.  Symmetries (translations and multiplication by units, which act independently on the Z_{p^n} and Z_q parts)
are used to fix the witnesses of the non-divisibilities.

 Lemma L:  minimise |A| subject to  Phi_{p^l} | A (l in E),  Phi_{p^a q} | A  (a not in E),
           Phi_q does not divide A   [witness: layer 0 has more elements than layer 1],
           Phi_{p^a} does not divide A [witness: more elements = 0 than = p^(a-1) mod p^a].
           Claimed: minimum >= p^|E| (p + q).
 Claim T:  feasibility of  Phi_q | A, |A| = p^|E| q, Phi_{p^l} | A (l in E), Phi_{p^b q} | A (b not in E),
           and Phi_{p^a q} does not divide A for some a in E, a < b [witness: a mixed difference >= 1].  Claimed: infeasible.
usage: milp_tests.py p n q [time limit per problem]"""
import sys, itertools, time, numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
sys.path.insert(0, "/home/agent3/review2")
from lemma_variants import residues
from cyclo_exact import divides
p, n, q = (int(x) for x in sys.argv[1:4]); TL = float(sys.argv[4]) if len(sys.argv) > 4 else 120
M = p ** n * q; P = p ** n
u_of = np.arange(M) % P; w_of = np.arange(M) % q
def Nrow(a, r, j=None):                              # indicator row of {x : u = r mod p^a (and w = j)}
    row = ((u_of % p ** a) == (r % p ** a)).astype(float)
    return row if j is None else row * (w_of == j)
RES = {}
def res(d):
    if d not in RES: RES[d] = residues(d, M).astype(float)
    return RES[d]
def solve(eqs, rhs_eq, ineqs, lo_ineq, objective, fixed_size=None):
    cons = []
    if len(eqs): cons.append(LinearConstraint(np.vstack(eqs), rhs_eq, rhs_eq))
    if len(ineqs): cons.append(LinearConstraint(np.vstack(ineqs), lo_ineq, np.full(len(lo_ineq), np.inf)))
    r = milp(c=objective, constraints=cons, integrality=np.ones(M), bounds=Bounds(np.zeros(M), np.ones(M)), options={"time_limit": TL})
    return r
levels = range(1, n + 1); nL = nT = 0; worstL = None; fails = []; unsolved = 0; sharp = 0; t0 = time.time()
for E in itertools.chain.from_iterable(itertools.combinations(levels, r) for r in range(n + 1)):
    e = len(E)
    for a in levels:
        if a in E: continue
        if p ** e * (p + q) > M: continue            # no set that large exists anyway
        eqs = [res(p ** l) for l in E] + [res(p ** a * q)]; rhs = np.zeros(sum(len(x) for x in eqs))
        ineqs = [Nrow(0, 0, 0) - Nrow(0, 0, 1), Nrow(a, 0) - Nrow(a, p ** (a - 1))]
        r = solve(eqs, rhs, ineqs, np.array([1.0, 1.0]), np.ones(M)); nL += 1
        target = p ** e * (p + q)
        if r.status == 0:
            A = [i for i in range(M) if r.x[i] > 0.5]
            assert all(divides(p ** l, A, M) for l in E) and divides(p ** a * q, A, M) and not divides(q, A, M) and not divides(p ** a, A, M)
            if len(A) < target: fails.append(("L", E, a, len(A), A))
            sharp += len(A) == target
        elif r.status == 2: pass                     # no such set at all
        else:
            unsolved += 1
            if getattr(r, "mip_dual_bound", None) is not None and r.mip_dual_bound < target - 1e-6: print("   L undecided", E, a, "dual bound", r.mip_dual_bound, flush=True)
    for b in levels:                                 # Claim T
        if b in E: continue
        for a in E:
            if a >= b or p ** e * q > M: continue
            eqs = [res(q), np.ones((1, M))] + [res(p ** l) for l in E] + [res(p ** b * q)]
            rhs = np.zeros(sum(len(x) for x in eqs)); rhs[len(res(q))] = p ** e * q
            s = p ** (a - 1)
            mixed = (Nrow(a, s, 1) - Nrow(a, 0, 1)) - (Nrow(a, s, 0) - Nrow(a, 0, 0))
            r = solve(eqs, rhs, [mixed], np.array([1.0]), np.zeros(M)); nT += 1
            if r.status == 0:
                A = [i for i in range(M) if r.x[i] > 0.5]; fails.append(("T", E, b, a, A))
            elif r.status != 2: unsolved += 1
print(f"p={p} n={n} q={q} M={M}: Lemma L problems {nL} (minimum equals p^e(p+q) in {sharp}); Claim T problems {nT}; "
      f"not decided within {TL:.0f} s: {unsolved}; FAILURES {len(fails)} {fails[:3]}  [{time.time() - t0:.0f} s]", flush=True)
