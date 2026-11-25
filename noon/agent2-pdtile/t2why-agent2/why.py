"""Why do the minimal patterns that allow a size have no set?  (Noon, 21 Nov 2026; exploration, floating point.)
For M = p^a q^b and each (i, j): patterns Z of orders containing p^i, q^j and not p^i q^j; sizes k allowed by Z (a step
function f >= 0, f(0) = 1, transform zero off Z, sum f = M/k); minimal patterns per size.  Each (k, Z) is then sorted by the
cheapest reason there is no set A with |A| = k, zeros containing Z, and p^i q^j not a zero:
  div : k is not a multiple of the product of the primes of the prime powers in Z
  lp  : even a function x in [0,1]^M with these zeros and one positive cuboid sum at p^i q^j does not exist
  int : neither, so 0/1 structure is needed (reported; a 0/1 solver is run on these only if asked: --solve)
usage: why.py p a q b [--solve] [--list]"""
import sys, itertools, numpy as np
from scipy.optimize import linprog
p, a, q, b = (int(x) for x in sys.argv[1:5]); M = p**a * q**b; X = np.arange(M)
vp = lambda x, r, cap: next(e for e in range(cap, -1, -1) if x % r**e == 0)
cls = [(vp(int(x), p, a), vp(int(x), q, b)) for x in X]
G = [(i, j) for i in range(a + 1) for j in range(b + 1)]; gi = {g: n for n, g in enumerate(G)}
size = np.array([sum(1 for c in cls if c == g) for g in G], float)
ORD = [(l, m) for l in range(a + 1) for m in range(b + 1) if (l, m) != (0, 0)]
val = lambda o: p**o[0] * q**o[1]
Tm = {}
for o in ORD:
    xi = M // val(o); row = np.zeros(len(G)); c = np.cos(2 * np.pi * (X * xi % M) / M)
    for x in X: row[gi[cls[x]]] += c[x]
    Tm[o] = np.round(row)
def sumf_range(Z):
    rows = [np.eye(len(G))[gi[(a, b)]]] + [Tm[o] for o in ORD if o not in Z]; rhs = [1.0] + [0.0] * (len(rows) - 1); out = []
    for sgn in (1, -1):
        r = linprog(sgn * size, A_eq=np.vstack(rows), b_eq=rhs, bounds=[(0, None)] * len(G), method="highs")
        if r.status == 2: return None
        if r.status == 3: out.append(np.inf); continue
        out.append(sgn * r.fun)
    return out
def zero_rows(o):
    """linear equalities on x in R^M equivalent to Phi_d | A, d = p^l q^m: differences of the counts modulo d"""
    l, m = o; d = val(o); cnt = np.zeros((d, M)); cnt[X % d, X] = 1; rows = []
    for c in range(d):
        if l and m: r = cnt[c] - cnt[(c + d // p) % d] - cnt[(c + d // q) % d] + cnt[(c + d // p + d // q) % d]
        elif l: r = cnt[c] - cnt[(c + d // p) % d]
        else: r = cnt[c] - cnt[(c + d // q) % d]
        rows.append(r)
    return np.array(rows)
ZR = {o: zero_rows(o) for o in ORD}
def lp_relax(k, Z, d0):
    eq = np.vstack([np.ones((1, M))] + [ZR[o] for o in sorted(Z)]); rhs = np.zeros(eq.shape[0]); rhs[0] = k
    wit = ZR[d0][0]
    r = linprog(np.zeros(M), A_eq=eq, b_eq=rhs, A_ub=-wit.reshape(1, -1), b_ub=[-1.0], bounds=[(0, 1)] * M, method="highs")
    return r.status == 0
def solve01(k, Z, d0, tl=120):
    from ortools.sat.python import cp_model
    m = cp_model.CpModel(); x = [m.NewBoolVar(f"x{t}") for t in range(M)]; m.Add(sum(x) == k)
    for o in sorted(Z):
        for row in ZR[o].astype(int): m.Add(sum(int(c) * x[t] for t, c in enumerate(row) if c) == 0)
    m.Add(sum(int(c) * x[t] for t, c in enumerate(ZR[d0][0].astype(int)) if c) >= 1)
    sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = tl; sv.parameters.num_workers = 8; st = sv.Solve(m)
    return "set" if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) else ("none" if st == cp_model.INFEASIBLE else "?")
def kS(Z):
    k = 1
    for (l, m) in Z:
        if m == 0: k *= p
        if l == 0: k *= q
    return k
name = lambda Z: "{" + ",".join(str(val(o)) for o in sorted(Z, key=val)) + "}"
tot = {"div": 0, "lp": 0, "int": 0}; ints = []
for i in range(1, a + 1):
    for j in range(1, b + 1):
        need = {(i, 0), (0, j)}; d0 = (i, j); free = [o for o in ORD if o not in need and o != d0]; allowed = {}
        for r in range(len(free) + 1):
            for extra in itertools.combinations(free, r):
                Z = frozenset(need | set(extra)); rg = sumf_range(Z)
                if rg is None: continue
                for k in range(2, M):
                    if rg[0] - 1e-7 <= M / k <= rg[1] + 1e-7: allowed.setdefault(k, []).append(Z)
        cnt = {"div": 0, "lp": 0, "int": 0}
        for k, Zs in sorted(allowed.items()):
            for Z in [Z for Z in Zs if not any(Y < Z for Y in Zs)]:
                why = "div" if k % kS(Z) else ("int" if lp_relax(k, Z, d0) else "lp")
                cnt[why] += 1; tot[why] += 1
                if why == "int": ints.append((d0, k, Z))
        print(f"(i,j)=({i},{j})  not a zero: {val(d0)}   minimal pairs {sum(cnt.values())}:  div {cnt['div']}  lp {cnt['lp']}  int {cnt['int']}", flush=True)
print(f"Z_{M}: total div {tot['div']}, lp {tot['lp']}, int {tot['int']}")
if "--list" in sys.argv or "--solve" in sys.argv:
    for d0, k, Z in sorted(ints, key=lambda t: (len(t[2]), t[1])):
        print(f"  int: missing {val(d0)}  size {k}  zeros {name(Z)}  kS {kS(Z)}" + (f"  0/1: {solve01(k, Z, d0)}" if "--solve" in sys.argv else ""), flush=True)
