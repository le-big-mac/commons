"""Referee: search for counterexamples to Lemma M (M2, M3, M4 as STATED in the note) with a constraint solver (OR-tools CP-SAT).
Unknowns: X in Z_M/P, Y in Z_M/Q (0/1); A = (X + P) u (Y + Q); cosets in different cosets of K; i, j >= 1; |A| = p^2 q.
Zeros are imposed on A itself (cuboid sums of the counts of A modulo d), not through the dictionary.
  M3  (p < q):  q a zero                                              -> lemma says INFEASIBLE
  M4:           q and p q^2 zeros                                     -> lemma says INFEASIBLE
  M2:           p, p^3 q, p^2 q^2 zeros and A not invariant under K   -> lemma says INFEASIBLE
                (by translation: the coset K itself is met by A and not contained in A)
controls (must be FEASIBLE, to show the model is not vacuous):
  C0: no zeros imposed;  C2: the zeros of M2 without the last condition;  C3 (p > q): q a zero;  C4: p q^2 a zero alone
usage: cpsat_lemmaM.py p q [timelimit]"""
import sys, time
from ortools.sat.python import cp_model
p, q = int(sys.argv[1]), int(sys.argv[2]); TL = float(sys.argv[3]) if len(sys.argv) > 3 else 120.0
a, b = 3, 2; M = p**a * q**b; MX = M // p; MY = M // q; G = M // (p * q)
val = lambda o: p**o[0] * q**o[1]

def build(zeros, partialK=False):
    m = cp_model.CpModel()
    X = [m.NewBoolVar(f"x{t}") for t in range(MX)]; Y = [m.NewBoolVar(f"y{t}") for t in range(MY)]
    for g in range(G):
        bx = m.NewBoolVar(f"bx{g}"); by = m.NewBoolVar(f"by{g}")
        for x in range(g, MX, G): m.AddImplication(X[x], bx)
        for y in range(g, MY, G): m.AddImplication(Y[y], by)
        m.AddBoolOr([bx.Not(), by.Not()])
    m.Add(sum(X) >= 1); m.Add(sum(Y) >= 1); m.Add(p * sum(X) + q * sum(Y) == p * p * q)
    A = [X[z % MX] + Y[z % MY] for z in range(M)]
    for o in zeros:
        l, mm = o; d = val(o)
        N = [sum(A[z] for z in range(c, M, d)) for c in range(d)]
        for c in range(d):
            if l and mm: m.Add(N[c] - N[(c + d // p) % d] - N[(c + d // q) % d] + N[(c + d // p + d // q) % d] == 0)
            elif l: m.Add(N[c] == N[(c + d // p) % d])
            else: m.Add(N[c] == N[(c + d // q) % d])
    if partialK:
        s = sum(A[z] for z in range(0, M, G)); m.Add(s >= 1); m.Add(s <= p * q - 1)
    return m, X, Y

def run(name, zeros, expect, partialK=False):
    m, X, Y = build(zeros, partialK); s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = TL; s.parameters.num_workers = 4
    t = time.time(); st = s.Solve(m); st = s.StatusName(st)
    verdict = "as the lemma says" if st == expect else ("UNDECIDED (time limit)" if st == 'UNKNOWN' else "*** CONTRADICTS THE EXPECTATION ***")
    extra = ""
    if st in ('OPTIMAL', 'FEASIBLE'):
        xs = [t_ for t_ in range(MX) if s.Value(X[t_])]; ys = [t_ for t_ in range(MY) if s.Value(Y[t_])]; extra = f"  X = {xs}  Y = {ys}"
    print(f"  {name:4s} zeros {sorted(val(o) for o in zeros)}{' + K met but not contained' if partialK else ''}: {st} in {time.time() - t:.1f}s (expected {expect}) {verdict}{extra if expect == 'INFEASIBLE' else ''}", flush=True)

print(f"Z_{M} (p = {p}, q = {q}), |A| = p^2 q = {p * p * q}", flush=True)
run("C0", [], 'OPTIMAL')
run("C2", [(1, 0), (3, 1), (2, 2)], 'OPTIMAL')
run("C4", [(1, 2)], 'OPTIMAL')
if p > q: run("C3", [(0, 1)], 'OPTIMAL')
if p < q: run("M3", [(0, 1)], 'INFEASIBLE')
run("M4", [(0, 1), (1, 2)], 'INFEASIBLE')
run("M2", [(1, 0), (3, 1), (2, 2)], 'INFEASIBLE', partialK=True)
