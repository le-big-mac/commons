"""Referee: end-to-end test of the category table in a small group, by a constraint solver (OR-tools CP-SAT), with no use of
Lemmas A-E or M.   A set A is a weak tile iff |A| = D^w(Z(A)).  The proof of Proposition G implies that NO weak tile has
its exact zero set in a category other than L2, a (b, N: divisibility; H: Lemma M; R, U: the proof gives (T2) and no
orphan, which would put the pattern in a; T: the proof gives (T1), (T2), and every T pattern met violates (T2)).
So for each pattern Z in the chosen categories:  is there a set A, 0 in A, |A| = D^w(Z), with Z(A) = Z EXACTLY?
   zeros d in Z:     all cuboid sums of the counts modulo d vanish
   non-zeros d:      some cuboid sum is >= 1 or <= -1
Expected: INFEASIBLE for every pattern.  A FEASIBLE answer is printed with the set and whether it satisfies (T1), (T2).
usage: cpsat_exact.py p q CATS [timelimit per pattern] [workers]      e.g. cpsat_exact.py 2 3 H,T,U,R 60 4"""
import sys, time
from collections import Counter
from ortools.sat.python import cp_model
import refclassify as rc
p, q = int(sys.argv[1]), int(sys.argv[2]); cats = sys.argv[3].split(','); TL = float(sys.argv[4]) if len(sys.argv) > 4 else 60.0; NW = int(sys.argv[5]) if len(sys.argv) > 5 else 4
a, b = 3, 2; M = p**a * q**b; val = lambda o: p**o[0] * q**o[1]
ORDS = [(l, m) for l in range(a + 1) for m in range(b + 1) if (l, m) != (0, 0)]
CAT, SIZE, cnt, _ = rc.classify(p, q)
def cuboids(A, o):
    l, mm = o; d = val(o); N = [sum(A[z] for z in range(c, M, d)) for c in range(d)]
    if l and mm: return [N[c] - N[(c + d // p) % d] - N[(c + d // q) % d] + N[(c + d // p + d // q) % d] for c in range(d)], 2 * (M // d)
    if l: return [N[c] - N[(c + d // p) % d] for c in range(d)], M // d
    return [N[c] - N[(c + d // q) % d] for c in range(d)], M // d
def zeros_of(S):
    out = set()
    for o in ORDS:
        l, mm = o; d = val(o); N = [0] * d
        for x in S: N[x % d] += 1
        if l and mm: z = all(N[c] - N[(c + d // p) % d] - N[(c + d // q) % d] + N[(c + d // p + d // q) % d] == 0 for c in range(d))
        elif l: z = all(N[c] == N[(c + d // p) % d] for c in range(d))
        else: z = all(N[c] == N[(c + d // q) % d] for c in range(d))
        if z: out.add(o)
    return frozenset(out)
res = Counter(); t0 = time.time(); todo = [Z for Z, c in CAT.items() if c in cats]
print(f"Z_{M} (p = {p}, q = {q}): {len(todo)} patterns in categories {cats}; time limit {TL}s each", flush=True)
for Z in todo:
    if Z in SIZE: n = SIZE[Z]; assert n.denominator == 1; n = int(n)
    else: n = p ** sum(1 for l in range(1, a + 1) if (l, 0) in Z) * q ** sum(1 for mm in range(1, b + 1) if (0, mm) in Z)      # category a (control): |A| = k
    m = cp_model.CpModel(); A = [m.NewBoolVar(f"a{z}") for z in range(M)]
    m.Add(A[0] == 1); m.Add(sum(A) == n)
    for o in ORDS:
        cs, bound = cuboids(A, o)
        if o in Z:
            for e in cs: m.Add(e == 0)
        else:
            lits = []
            for t, e in enumerate(cs):
                pos = m.NewBoolVar(f"p{o}{t}"); neg = m.NewBoolVar(f"n{o}{t}")
                m.Add(e >= 1).OnlyEnforceIf(pos); m.Add(e <= -1).OnlyEnforceIf(neg); lits += [pos, neg]
            m.AddBoolOr(lits)
    s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = TL; s.parameters.num_workers = NW
    st = s.StatusName(s.Solve(m)); res[(CAT[Z], st)] += 1
    if st in ('OPTIMAL', 'FEASIBLE'):
        S = [z for z in range(M) if s.Value(A[z])]; ZZ = zeros_of(S)
        Ep = [l for l in range(1, a + 1) if (l, 0) in ZZ]; Eq = [mm for mm in range(1, b + 1) if (0, mm) in ZZ]
        t1 = p ** len(Ep) * q ** len(Eq) == len(S); t2 = all((l, mm) in ZZ for l in Ep for mm in Eq)
        if CAT[Z] == 'a': res[('a control: T1 and T2', t1 and t2 and ZZ == Z)] += 1; continue
        print(f"  *** FEASIBLE: category {CAT[Z]}, size {n}, zeros {sorted(val(o) for o in Z)}: A = {S}; exact zero set as required: {ZZ == Z}; T1 {t1}, T2 {t2}", flush=True)
    elif st != 'INFEASIBLE':
        print(f"  undecided ({st}): category {CAT[Z]}, size {n}, zeros {sorted(val(o) for o in Z)}", flush=True)
print(f"Z_{M}: results {dict(res)}; {time.time() - t0:.0f}s", flush=True)
