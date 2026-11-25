"""Referee: the property P(M') -- every weak tile of Z_{M'} has (T1), (T2) and no orphan -- tested in small groups with a
constraint solver.  It is what categories R and T of Proposition G take from Z_{p^2 q^2} and Z_{p^3 q}; for Z_{p^2 q^2} it is
NOT part of the machine-checked Theorem C (which says 'tiles').
For every zero pattern Z of Z_{p^a q^b} that violates (T2) or has an orphan:  is there a set A, 0 in A, with |A| = D^w(Z)
and Z(A) = Z exactly?   (A weak tile has |A| = D^w(Z(A)); patterns with D^w(Z) not a multiple of k are skipped: no weak tile.)
Expected: INFEASIBLE for all.     usage: cpsat_P.py p a q b [timelimit] [workers]"""
import sys, time
from collections import Counter
from ortools.sat.python import cp_model
from lemmatests import Grp
p, a, q, b = (int(v) for v in sys.argv[1:5]); TL = float(sys.argv[5]) if len(sys.argv) > 5 else 60.0; NW = int(sys.argv[6]) if len(sys.argv) > 6 else 2
G = Grp(p, a, q, b); M = G.M; ords = G.ords; val = G.val
res = Counter(); t0 = time.time()
for mask in range(1 << len(ords)):
    Z = frozenset(o for t, o in enumerate(ords) if mask >> t & 1)
    Ep, Eq, k, t2, orphan = G.pattern(Z)
    if t2 and not orphan: res['(T2) and no orphan: not examined'] += 1; continue
    D = G.Dw(Z)[0]
    if D % k != 0: res['D^w not a multiple of k: no weak tile'] += 1; continue
    n = int(D)
    m = cp_model.CpModel(); A = [m.NewBoolVar(f"a{z}") for z in range(M)]
    m.Add(A[0] == 1); m.Add(sum(A) == n)
    for o in ords:
        l, mm = o; d = val(o); N = [sum(A[z] for z in range(c, M, d)) for c in range(d)]
        if l and mm: cs = [N[c] - N[(c + d // p) % d] - N[(c + d // q) % d] + N[(c + d // p + d // q) % d] for c in range(d)]
        elif l: cs = [N[c] - N[(c + d // p) % d] for c in range(d)]
        else: cs = [N[c] - N[(c + d // q) % d] for c in range(d)]
        if o in Z:
            for e in cs: m.Add(e == 0)
        else:
            lits = []
            for t, e in enumerate(cs):
                pos = m.NewBoolVar(f"p{o}{t}"); neg = m.NewBoolVar(f"n{o}{t}")
                m.Add(e >= 1).OnlyEnforceIf(pos); m.Add(e <= -1).OnlyEnforceIf(neg); lits += [pos, neg]
            m.AddBoolOr(lits)
    s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = TL; s.parameters.num_workers = NW
    st = s.StatusName(s.Solve(m)); res[st] += 1
    if st != 'INFEASIBLE':
        S = [z for z in range(M) if s.Value(A[z])] if st in ('OPTIMAL', 'FEASIBLE') else None
        print(f"  {st}: size {n}, zeros {sorted(val(o) for o in Z)}, T2 {t2}, orphan {orphan}, A = {S}", flush=True)
print(f"Z_{M} = Z_({p}^{a} {q}^{b}): {1 << len(ords)} patterns: {dict(res)}; {time.time() - t0:.0f}s", flush=True)
