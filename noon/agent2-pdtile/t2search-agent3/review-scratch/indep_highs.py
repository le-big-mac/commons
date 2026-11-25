"""(T1) search re-solved with a second solver: HiGHS (floating point branch and bound), disjunctions by big-M binaries,
count encoding of divisibility as in indep.py (whose definitions are reused; its search loop is not run).
usage: indep_highs.py p a q b [time limit per programme]"""
import sys, time, itertools, numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
TLH = float(sys.argv[5]) if len(sys.argv) > 5 else 60
src = open("/tmp/rev_t2/indep.py").read(); cut = src.index("t0 = time.time(); nprog = ninf = nund = nset = nwt = 0")
argv = sys.argv; sys.argv = argv[:5] + ["T1", "1"]; ns = {"__name__": "indep_defs"}; exec(compile(src[:cut], "indep_defs", "exec"), ns); sys.argv = argv
p, a, q, b, M, PP, MIX, D = (ns[n] for n in ("p", "a", "q", "b", "M", "PP", "MIX", "D")); allows, minimal, exps = ns["allows"], ns["minimal"], ns["exps"]
X = np.arange(M)
def cntvec(d, c): return (X % d == c).astype(float)
def eq_rows(Z):
    rows = []
    for d in Z:
        if d in PP:
            r = p if d % p == 0 else q
            for c in range(d): rows.append(cntvec(d, c) - cntvec(d, (c + d // r) % d))
        else:
            i, j = exps(d); P, Q = p ** i, q ** j; s1, s2 = p ** (i - 1), q ** (j - 1)
            N = lambda u, v: ((X % P == u % P) & (X % Q == v % Q)).astype(float)
            for u in range(P):
                for v in range(Q): rows.append(N(u, v) - N(u + s1, v) - N(u, v + s2) + N(u + s1, v + s2))
    return rows
def solve(k, Z, nonpp):
    lits = [(d, c) for d in nonpp for c in range(d)]; nv = M + len(lits); BIG = k + 1
    E = [np.concatenate([np.ones(M), np.zeros(len(lits))])] + [np.concatenate([r, np.zeros(len(lits))]) for r in eq_rows(Z)]
    rhs = np.zeros(len(E)); rhs[0] = k; cons = [LinearConstraint(np.array(E), rhs, rhs)]
    G = []; lo = []
    for n, (d, c) in enumerate(lits):                                   # y = 1  =>  cnt(c) - cnt(c + d/r) >= 1
        r = p if d % p == 0 else q; row = np.zeros(nv); row[:M] = cntvec(d, c) - cntvec(d, (c + d // r) % d); row[M + n] = -BIG; G.append(row); lo.append(1 - BIG)
    for d in nonpp:
        row = np.zeros(nv)
        for n, (dd, c) in enumerate(lits):
            if dd == d: row[M + n] = 1
        G.append(row); lo.append(1)
    if G: cons.append(LinearConstraint(np.array(G), np.array(lo), np.inf))
    lb = np.zeros(nv); lb[0] = 1                                         # 0 in A (translation invariance)
    r = milp(c=np.zeros(nv), constraints=cons, integrality=np.ones(nv), bounds=Bounds(lb, np.ones(nv)), options={"time_limit": TLH})
    if r.status == 2: return "infeasible", None
    if r.x is not None: return "set", [x for x in range(M) if r.x[x] > 0.5]
    return "undecided", None
t0 = time.time(); nprog = ninf = nund = nset = 0; slow = []
for r in range(len(PP) + 1):
    for S in itertools.combinations(PP, r):
        S = frozenset(S); t1 = p ** sum(1 for d in S if d % p == 0) * q ** sum(1 for d in S if d % q == 0)
        fam = [S | frozenset(mx) for r2 in range(len(MIX) + 1) for mx in itertools.combinations(MIX, r2)]; todo = []
        for k in range(1, M + 1):
            if k != t1: todo += [(k, Z) for Z in minimal([Z for Z in fam if allows(Z, k)])]
        for k, Z in todo:
            t1_ = time.time(); st, A = solve(k, sorted(Z), [d for d in PP if d not in S]); nprog += 1; dt = time.time() - t1_
            if dt > 20: slow.append((k, sorted(Z), round(dt)))
            if st == "set":
                nset += 1; ZA = ns["zeros_exact"](A, M); print("   SET", k, A, sorted(ZA), "full LP weak tile:", ns["wt"].full_lp(A, M)[0], flush=True)
            elif st == "infeasible": ninf += 1
            else: nund += 1; print("   undecided", k, sorted(Z), sorted(S), flush=True)
print(f"Z_{M} (T1) search with HiGHS (big-M): {nprog} programmes, {ninf} infeasible, {nset} with a set, {nund} undecided; {time.time() - t0:.0f} s; programmes over 20 s: {slow}")
