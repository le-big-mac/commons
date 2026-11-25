"""The one programme my independent CP-SAT encoding did not decide in 300 s:  Z_108, |A| = 18, zeros 3, 9, 54 required; 2, 4, 27 not zeros.
 (1) the script's own find() (its encoding) ; (2) case split by symmetry into linear programmes without disjunction, solved by HiGHS (residues)
 and by CP-SAT (count equations):
     Phi_2 not | A : E != O; translation by 1 swaps parities             -> E >= O + 1
     Phi_27 not | A: cnt27(c1) > cnt27(c2), c1 = c2 mod 9; translation by an even number moves c1 to 0, the unit u = -1 mod 27, 1 mod 4 swaps 9 and 18 -> cnt27(0) >= cnt27(9) + 1
     Phi_4 not | A : one of the four ordered pairs (0,2), (2,0), (1,3), (3,1) -> four cases, all solved."""
import sys, time, numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from ortools.sat.python import cp_model
from common import *
from loadscripts import T1, _exec
M = 108; k = 18; Z = [3, 9, 54]
src = open(T1).read(); cut = src.index("t0 = time.time(); nprog = ninf = nund = 0"); src = src[:cut].replace("num_workers = 8", "num_workers = 3")
ns = _exec(src, [2, 2, 3, 3, 300], "t1defs")
t0 = time.time(); st, A = ns["find"](k, frozenset({(0, 1), (0, 2), (1, 3)}), [(1, 0), (2, 0), (0, 3)])
print(f"(1) script's find(): status {st} (2 = infeasible) in {time.time() - t0:.0f} s", flush=True)
X = np.arange(M); ind = lambda cond: cond.astype(float)
rows = [np.ones((1, M))] + [residues(d, M).astype(float) for d in Z]; Am = np.vstack(rows); rhs = np.zeros(Am.shape[0]); rhs[0] = k
w2 = ind(X % 2 == 0) - ind(X % 2 == 1); w27 = ind(X % 27 == 0) - ind(X % 27 == 9)
for (c1, c2) in [(0, 2), (2, 0), (1, 3), (3, 1)]:
    w4 = ind(X % 4 == c1) - ind(X % 4 == c2); t0 = time.time()
    r = milp(c=np.zeros(M), constraints=[LinearConstraint(Am, rhs, rhs), LinearConstraint(np.vstack([w2, w27, w4]), 1, np.inf)], integrality=np.ones(M), bounds=Bounds(np.zeros(M), np.ones(M)), options={"time_limit": 300})
    th = time.time() - t0
    m = cp_model.CpModel(); x = [m.NewBoolVar(f"x{t}") for t in range(M)]; m.Add(sum(x) == k)
    cnt = lambda d: [sum(x[t] for t in range(M) if t % d == c) for c in range(d)]
    c3 = cnt(3); c9 = cnt(9); c27 = cnt(27); c4 = cnt(4); c2_ = cnt(2)
    for c in range(3): m.Add(c3[c] == c3[(c + 1) % 3])
    for c in range(9): m.Add(c9[c] == c9[(c + 3) % 9])
    N = {(u, v): sum(x[t] for t in range(M) if t % 2 == u and t % 27 == v) for u in range(2) for v in range(27)}
    for u in range(2):
        for v in range(27): m.Add(N[(u, v)] - N[((u + 1) % 2, v)] - N[(u, (v + 9) % 27)] + N[((u + 1) % 2, (v + 9) % 27)] == 0)
    m.Add(c2_[0] >= c2_[1] + 1); m.Add(c27[0] >= c27[9] + 1); m.Add(c4[c1] >= c4[c2] + 1)
    sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = 300; sv.parameters.num_workers = 3; t0 = time.time(); st = sv.Solve(m)
    print(f"(2) case cnt4({c1}) > cnt4({c2}): HiGHS status {r.status} ({'infeasible' if r.status == 2 else 'set found' if r.x is not None else 'undecided'}) in {th:.1f} s;  CP-SAT {sv.StatusName(st)} in {time.time() - t0:.1f} s", flush=True)
