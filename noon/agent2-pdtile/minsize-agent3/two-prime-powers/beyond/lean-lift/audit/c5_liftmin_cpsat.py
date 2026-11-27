# Part 3(d), integer programming: the least size in the set of each theorem of Pnq/LiftMin.lean, by CP-SAT (exact integer
# arithmetic), against the value Lean gives by #eval.
#   variables  w[y] in [0, U], y in [0, M);  minimise sum w  subject to sum w <= U and, for each d the Lean clauses speak of,
#   "Phi_d | mask":      every coefficient of (mask mod Phi_d) is 0        (linear equalities)
#   "not Phi_d | mask":  some coefficient of (mask mod Phi_d) is >= 1 or <= -1   (a disjunction, with indicator booleans)
# U = (Lean value) + 2, so a least size one or two above the Lean value would show as such, not as "infeasible".
# The list of (d, must divide / must not divide) is derived from the clauses and then checked, over EVERY subset D of the
# divisors of M, to describe the same sets D as the membership tests of liftmin_conditions.py (used by the exhaustive run).
# Every optimal multiset returned is re-checked by long division.  No symmetry is broken unless --fix0 is given.
import sys, time, itertools
sys.path.insert(0, '/home/agent3/lean/lift-audit')
from core import *
from liftmin_conditions import *
from ortools.sat.python import cp_model

def spec_of(label, p, q, n, r):
    """{d: True (Phi_d must divide) / False (must not)} from the Lean clauses; and whether 0 < s is asked"""
    N = p ** n * q; M = N * r
    kind = label[0]; Es = set(label[1]); spec = {}
    def put(d, b):
        assert spec.get(d, b) == b, "contradictory clauses"
        spec[d] = b
    put(q, kind != "U")                                   # ¬ Φ_q ∣ maskW w   /   Φ_q ∣ maskW w
    for l in range(1, n + 1):
        put(p ** l, l in Es)                              # Φ_{p^ℓ} ∣ maskW w ↔ ℓ ∈ Es
        if kind == "A": put(p ** l * q, True)             # Φ_{p^ℓ q} ∣ maskW w
        else: put(p ** l * q, l in set(label[2]))         # Φ_{p^ℓ q} ∣ maskW w ↔ ℓ ∈ Fs
    for d in divisors(M):
        if N % d != 0: put(d, False)                      # d ∣ M → ¬ d ∣ N → ¬ Φ_d ∣ maskW w
    return spec, (kind == "A")

def check_spec(spec, need_pos, member, M):
    divs = divisors(M)
    for k in range(len(divs) + 1):
        for c in itertools.combinations(divs, k):
            D = frozenset(c)
            a = all((d in D) == b for d, b in spec.items())
            for s in (0, 1):
                assert (a and (s > 0 or not need_pos)) == member(D, s), ("spec and membership test differ", D, s)

_tab = {}
def solve(M, spec, need_pos, U, tl, workers, fix0):
    m = cp_model.CpModel()
    w = [m.NewIntVar(0, U, f"w{y}") for y in range(M)]
    total = sum(w)
    m.Add(total <= U)
    if need_pos: m.Add(total >= 1)
    if fix0: m.Add(w[0] >= 1)
    for d, must in sorted(spec.items()):
        if (M, d) not in _tab: _tab[(M, d)] = rem_table(M, d)
        T = _tab[(M, d)]
        lits = []
        for j in range(T.shape[1]):
            terms = [(int(T[y][j]), w[y]) for y in range(M) if T[y][j] != 0]
            assert terms
            e = sum(c * v for c, v in terms)
            if must:
                m.Add(e == 0)
            else:
                bp = m.NewBoolVar(f"p{d}_{j}"); bn = m.NewBoolVar(f"n{d}_{j}")
                m.Add(e >= 1).OnlyEnforceIf(bp); m.Add(e <= -1).OnlyEnforceIf(bn)
                lits += [bp, bn]
        if not must:
            m.AddBoolOr(lits)
    m.Minimize(total)
    sv = cp_model.CpSolver()
    sv.parameters.max_time_in_seconds = tl
    sv.parameters.num_search_workers = workers
    st = sv.Solve(m)
    name = sv.StatusName(st)
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return name, int(round(sv.ObjectiveValue())), [sv.Value(v) for v in w], int(round(sv.BestObjectiveBound()))
    return name, None, None, None

if __name__ == "__main__":
    p, q, n, r = (int(x) for x in sys.argv[1:5])
    vmin = int(sys.argv[5])            # only instances whose Lean value is >= vmin
    tl = float(sys.argv[6])            # seconds per instance
    fix0 = "--fix0" in sys.argv
    budget = float(sys.argv[7])        # stop starting new instances after this many seconds
    N = p ** n * q; M = N * r
    val = lean_values()
    G = Group(M)
    t0 = time.time(); ok = 0; notok = 0; unfinished = 0; skipped = 0
    insts = [i for i in instances(p, q, n, r, val) if i[2] >= vmin]
    # --skip FILE ... : leave out the instances that an earlier run of this program (its output FILE) already settled
    done = set()
    if "--skip" in sys.argv:
        for f in sys.argv[sys.argv.index("--skip") + 1:]:
            for line in open(f):
                if "  AGREES" in line: done.add(line.split(" Lean ")[0].strip())
    insts = [i for i in insts if str(i[0]) not in done]
    print(f"p={p} q={q} n={n} r={r}  Z_{M} (N={N}); {len(insts)} instances with Lean value >= {vmin}; {tl:.0f} s each; fix0={fix0}", flush=True)
    for (label, member, v) in sorted(insts, key=lambda i: i[2]):
        if time.time() - t0 > budget:
            skipped += 1; continue
        spec, need_pos = spec_of(label, p, q, n, r)
        check_spec(spec, need_pos, member, M)
        t1 = time.time()
        name, obj, sol, bound = solve(M, spec, need_pos, v + 2, tl, 4, fix0)
        dt = time.time() - t1
        verdict = "?"
        if name == "OPTIMAL":
            D = G.divset(sol)                      # long division
            good = member(D, sum(sol)) and sum(sol) == obj
            if obj == v and good: verdict = "AGREES"; ok += 1
            else: verdict = f"DISAGREES (witness check {good})"; notok += 1
        elif name == "INFEASIBLE":
            verdict = "DISAGREES: no multiset of size <= value + 2"; notok += 1
        else:
            unfinished += 1
            if sol is None:
                verdict = "UNFINISHED (nothing found in the time)"
            else:
                D = G.divset(sol)                  # long division
                good = member(D, sum(sol)) and sum(sol) == obj
                verdict = f"UNFINISHED (a member of size {obj} found, checked by long division: {good}; least size proved >= {bound})"
                if obj < v and good: verdict += " DISAGREES: a smaller member than the Lean value"; notok += 1
        pat = "".join(f"{'+' if b else '-'}{d} " for d, b in sorted(spec.items()))
        wit = "" if sol is None else " witness " + str([y for y, c in enumerate(sol) for _ in range(c)])
        print(f"  {str(label):34s} Lean {v:3d}  CP-SAT {name} {obj}  {dt:6.1f}s  {verdict}   [{pat.strip()}]{wit}", flush=True)
    print(f"summary p={p} q={q} n={n} r={r} Z_{M}: agree {ok}, disagree {notok}, unfinished {unfinished}, not started {skipped};  {time.time()-t0:.0f} s", flush=True)
