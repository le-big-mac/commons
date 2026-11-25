"""Independent replication of the two searches (reviewer's code; shares only the mathematical reduction with the scripts under review).
Differences from t2search.py / t1search.py:
  * transform matrix from FFTs of the class indicators (wt.class_data), classes indexed by gcd;
  * 'Phi_d | A' is NOT stated through residues of X^x mod Phi_d but through the counts of A modulo d:
        d = r^e      : cnt(c) = cnt(c + r^(e-1))                      for all c mod d
        d = p^i q^j  : N(c) - N(c+e1) - N(c+e2) + N(c+e1+e2) = 0      for all c  (CRT coordinates, e1 = (p^(i-1), 0), e2 = (0, q^(j-1)))
  * 'Phi_{p^i q^j} does not divide A' is a DISJUNCTION over all cuboids and both signs (no normalisation by symmetry is used);
    'Phi_{r^e} does not divide A' is a disjunction over adjacent classes c, c + r^(e-1);
  * 0 in A is imposed (legitimate here because every constraint is translation invariant);  CP-SAT, integer arithmetic.
usage: indep.py p a q b T1|T2 [workers] [time limit]"""
import sys, itertools, time, math
import numpy as np
from scipy.optimize import linprog
from ortools.sat.python import cp_model
from common import *
import wt
p, a, q, b = (int(v) for v in sys.argv[1:5]); mode = sys.argv[5]; workers = int(sys.argv[6]) if len(sys.argv) > 6 else 4; TL = float(sys.argv[7]) if len(sys.argv) > 7 else 300
M = p ** a * q ** b; divs, cls, Tm = wt.class_data(M); D = [d for d in divs if d > 1]
PP = [d for d in D if d % p != 0 or d % q != 0]; MIX = [d for d in D if d not in PP]
size = np.array([len(cls[g]) for g in divs], float); e0 = np.array([1.0 if g == M else 0.0 for g in divs])
_rg = {}
def sum_range(Z):
    Z = frozenset(Z)
    if Z not in _rg:
        rows = np.array([e0] + [Tm[d] for d in D if d not in Z], float); rhs = [1.0] + [0.0] * (len(rows) - 1); out = []
        for sg in (1, -1):
            r = linprog(sg * size, A_eq=rows, b_eq=rhs, bounds=[(0, None)] * len(divs), method="highs")
            if r.status == 2: out = None; break
            if r.status == 3: assert sg == -1; out.append(np.inf); continue
            assert r.status == 0; out.append(sg * r.fun)
        _rg[Z] = out
    return _rg[Z]
def allows(Z, k):
    rg = sum_range(Z)
    return rg is not None and rg[0] - 1e-7 <= M / k <= rg[1] + 1e-7
def exps(d):
    i = 0
    while d % p == 0: d //= p; i += 1
    j = 0
    while d % q == 0: d //= q; j += 1
    return i, j
def build(k, Z, nonpp, nonmix):
    """model: |A| = k, 0 in A, Phi_d | A for d in Z, Phi_s does not divide A for s in nonpp (prime powers) and nonmix (mixed orders)"""
    m = cp_model.CpModel(); x = [m.NewBoolVar(f"x{t}") for t in range(M)]; m.Add(sum(x) == k); m.Add(x[0] == 1)
    def cnt(d): return [sum(x[t] for t in range(M) if t % d == c) for c in range(d)]
    def cubs(d):
        i, j = exps(d); P, Q = p ** i, q ** j; N = {(u, v): sum(x[t] for t in range(M) if t % P == u and t % Q == v) for u in range(P) for v in range(Q)}
        s1, s2 = p ** (i - 1), q ** (j - 1)
        return [N[(u, v)] - N[((u + s1) % P, v)] - N[(u, (v + s2) % Q)] + N[((u + s1) % P, (v + s2) % Q)] for u in range(P) for v in range(Q)]
    for d in Z:
        if d in PP:
            r = p if d % p == 0 else q; c_ = cnt(d)
            for c in range(d): m.Add(c_[c] == c_[(c + d // r) % d])
        else:
            for e in cubs(d): m.Add(e == 0)
    for d in nonpp:
        r = p if d % p == 0 else q; c_ = cnt(d); lits = []
        for c in range(d):
            y = m.NewBoolVar(""); m.Add(c_[c] >= c_[(c + d // r) % d] + 1).OnlyEnforceIf(y); lits.append(y)
        m.AddBoolOr(lits)
    for d in nonmix:
        lits = []
        for e in cubs(d):
            y = m.NewBoolVar(""); m.Add(e >= 1).OnlyEnforceIf(y); lits.append(y)
            y = m.NewBoolVar(""); m.Add(e <= -1).OnlyEnforceIf(y); lits.append(y)
        m.AddBoolOr(lits)
    return m, x
def solve(k, Z, nonpp, nonmix):
    m, x = build(k, Z, nonpp, nonmix); sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = TL; sv.parameters.num_workers = workers
    st = sv.Solve(m)
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE): return "set", [t for t in range(M) if sv.Value(x[t])]
    return ("infeasible" if st == cp_model.INFEASIBLE else "undecided"), None
def minimal(Zs): return [Z for Z in Zs if not any(Y < Z for Y in Zs)]
def report(A, k, Z, tag):
    ZA = zeros_exact(A, M); assert len(A) == k and set(Z) <= ZA
    feas, _ = wt.full_lp(A, M)
    print(f"   SET {tag} size {k}: {A} zeros {sorted(ZA)}; weak tile by the full LP: {feas}; (T1) holds: {T1_holds(ZA, k, p, a, q, b)}; (T2) violations: {T2_violations(ZA, p, a, q, b)}", flush=True)
    return feas
t0 = time.time(); nprog = ninf = nund = nset = nwt = 0
if mode in ("T2", "T2C"):
    for i in range(1, a + 1):
        for j in range(1, b + 1):
            need = {p ** i, q ** j} if mode == "T2" else {p ** i}; d0 = p ** i * q ** j; free = [d for d in D if d not in need and d != d0]; todo = []
            fam = [frozenset(need | set(ex)) for r in range(len(free) + 1) for ex in itertools.combinations(free, r)]
            for k in range(2, M):
                todo += [(k, Z) for Z in minimal([Z for Z in fam if allows(Z, k)])]
            print(f"(i, j) = ({i}, {j}): {len(fam)} patterns, {len(todo)} minimal (size, pattern) pairs", flush=True)
            for k, Z in todo:
                st, A = solve(k, sorted(Z), [], [d0]); nprog += 1
                if st == "set": nset += 1; nwt += report(A, k, Z, f"(T2) at ({i},{j})")
                elif st == "infeasible": ninf += 1
                else: nund += 1; print("   undecided", k, sorted(Z), flush=True)
else:
    for r in range(len(PP) + 1):
        for S in itertools.combinations(PP, r):
            S = frozenset(S); t1 = p ** sum(1 for d in S if d % p == 0) * q ** sum(1 for d in S if d % q == 0)
            fam = [S | frozenset(mx) for r2 in range(len(MIX) + 1) for mx in itertools.combinations(MIX, r2)]; todo = []
            for k in range(1, M + 1):
                if (k != t1) == (mode == "T1"): todo += [(k, Z) for Z in minimal([Z for Z in fam if allows(Z, k)])]
            for k, Z in todo:
                st, A = solve(k, sorted(Z), [d for d in PP if d not in S], []); nprog += 1
                if st == "set": nset += 1; nwt += report(A, k, Z, f"(T1), prime-power zeros {sorted(S)}")
                elif st == "infeasible": ninf += 1
                else: nund += 1; print("   undecided", k, sorted(Z), flush=True)
print(f"Z_{M} independent {mode} search: {nprog} programmes, {ninf} infeasible, {nset} with a set ({nwt} weak tiles by the full LP), {nund} undecided; {time.time() - t0:.0f} s")
