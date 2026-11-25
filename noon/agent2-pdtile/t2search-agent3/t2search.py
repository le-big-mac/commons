r"""Is there a weak tile of Z_M, M = p^a q^b, that violates (T2)?  A search, set by set, with a solver.  (agent3 / Yonder)

A weak tile is a set A in Z_M with a function f >= 0, f(0) = 1, 1_A * f = 1 (so sum f = M / |A|).  Equivalently: at every order d > 1,
A(X) has a zero (Phi_d | A) or the transform of f vanishes.  f may be taken constant on the classes {x : gcd(x, M) = g} (average over units).
(T2) at (i, j): Phi_{p^i} | A and Phi_{q^j} | A imply Phi_{p^i q^j} | A.   Noon's (L1) is the case i = 1 or j = 1.

For each (i, j), 1 <= i <= a, 1 <= j <= b, the search looks for A with  p^i, q^j zeros,  p^i q^j not a zero,  and a weak complement:
  1. PATTERNS.  For every set Z of orders containing p^i, q^j and not p^i q^j: the linear programme
        f_g >= 0,  f at 0 = 1,  transform of f = 0 at every order not in Z,
     gives the interval of sum f it allows (two LPs), hence the sizes k = |A| with M / k in it.
  2. For each size k, only the MINIMAL patterns allowing k matter (a set whose zeros contain Z has a complement if Z allows one).
  3. SETS.  For each minimal pattern and size: a 0/1 programme (HiGHS through scipy)
        |A| = k,  Phi_d | A for d in Z (integer residues of X^x mod Phi_d),  and  Phi_{p^i q^j} does not divide A,
     the last as one inequality: N(0,0) - N(p^(i-1),0) - N(0,q^(j-1)) + N(p^(i-1),q^(j-1)) >= 1 for the counts N of A modulo p^i q^j
     (Phi_{p^i q^j} divides A exactly when every such cuboid sum, over all base points, vanishes; the sums add to zero over the base points,
     so a nonzero one implies a positive one, and a translation, which preserves everything else, moves it to the origin.  [Reason corrected
     after review: the first version invoked multiplication by units, which is not needed and does not change the sign.])
  Any set returned is re-verified exactly (polynomial division; then an exact rational complement) and printed.
"infeasible" is the solver's word.  With --cpsat the 0/1 programmes are solved by OR-tools CP-SAT (integer arithmetic throughout) instead of HiGHS.
With --exact the pattern programmes of step 1 are solved in rational arithmetic (exactlp.py) instead of floating point.
usage: t2search.py p a q b [time limit per 0/1 programme, s] [--control] [--cpsat] [--exact]"""
import sys, itertools, time, numpy as np
from fractions import Fraction
from scipy.optimize import milp, linprog, LinearConstraint, Bounds
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))     # lemma_variants.py, cyclo_exact.py, exactlp.py sit beside this file
from lemma_variants import residues
from cyclo_exact import divides
ONLY = {tuple(int(v) for v in t.split(',')) for t in os.environ.get('T2_ONLY', '').split(';') if t}
p, a, q, b = (int(x) for x in sys.argv[1:5]); TL = float(sys.argv[5]) if len(sys.argv) > 5 and not sys.argv[5].startswith("-") else 300.0
M = p ** a * q ** b; X = np.arange(M)
vp = lambda x, r, cap: next(e for e in range(cap, -1, -1) if x % r ** e == 0)
cls = [(vp(int(x), p, a), vp(int(x), q, b)) for x in X]                      # class of x: (i, j) with gcd(x, M) = p^i q^j
G = [(i, j) for i in range(a + 1) for j in range(b + 1)]; gi = {g: n for n, g in enumerate(G)}
size = np.array([sum(1 for c in cls if c == g) for g in G], dtype=float)
ORD = [(l, m) for l in range(a + 1) for m in range(b + 1) if (l, m) != (0, 0)]  # orders d = p^l q^m > 1
val = lambda o: p ** o[0] * q ** o[1]
Tm = {}                                                                       # transform of the indicator of class g at a frequency of order d (an integer)
for o in ORD:
    xi = M // val(o); row = np.zeros(len(G))
    c = np.cos(2 * np.pi * (X * xi % M) / M)
    for x in X: row[gi[cls[x]]] += c[x]
    assert np.allclose(row, np.round(row), atol=1e-6); Tm[o] = np.round(row)
exact = "--exact" in sys.argv
if exact: from exactlp import lp as exact_lp
def sumf_range(Z):
    """interval of sum f allowed by the pattern Z, or None"""
    if exact:
        rowsx = [[int(v) for v in np.eye(len(G))[gi[(a, b)]]]] + [[int(v) for v in Tm[o]] for o in ORD if o not in Z]; rhsx = [1] + [0] * (len(rowsx) - 1)
        sz = [int(v) for v in size]
        st, lo, _ = exact_lp(rowsx, rhsx, sz)
        if st == "infeasible": return None
        st2, hi, _ = exact_lp(rowsx, rhsx, [-v for v in sz])
        return lo, (None if st2 == "unbounded" else -hi)
    rows = [np.eye(len(G))[gi[(a, b)]]] + [Tm[o] for o in ORD if o not in Z]; rhs = [1.0] + [0.0] * (len(rows) - 1)
    out = []
    for sgn in (1, -1):
        r = linprog(sgn * size, A_eq=np.vstack(rows), b_eq=rhs, bounds=[(0, None)] * len(G), method="highs")
        if r.status == 2: return None
        if r.status == 3: out.append(np.inf if sgn == -1 else -np.inf); continue
        assert r.status == 0, r.message
        out.append(sgn * r.fun)
    return out[0], out[1]
RES = {}
def res(o):
    if o not in RES: RES[o] = residues(val(o), M).astype(float)
    return RES[o]
def exact_complement(A):
    """exact weak complement of A constant on gcd classes, or None: rational linear programme (exactlp.py), then checked point by point.
    [After review: the first version rounded a floating-point vertex, which could fail on a genuine weak tile.]"""
    from exactlp import lp as _lp
    ZA = {o for o in ORD if divides(val(o), A, M)}
    rows = [[int(v) for v in np.eye(len(G))[gi[(a, b)]]]] + [[int(v) for v in Tm[o]] for o in ORD if o not in ZA] + [[int(v) for v in size]]
    rhs = [1] + [0] * (len(rows) - 2) + [Fraction(M, len(A))]
    st, _, f = _lp(rows, rhs, [0] * len(G))
    if st != "optimal": return None, ZA
    fx = [f[gi[cls[x]]] for x in X]; ok = all(sum(fx[(y - x) % M] for x in A) == 1 for y in X) and all(v >= 0 for v in f) and f[gi[(a, b)]] == 1
    return (f if ok else None), ZA
t0 = time.time(); found = []; nlp = nmilp = ninf = ntl = 0
control = "--control" in sys.argv; cpsat = "--cpsat" in sys.argv
def solve01(Am, rhs, wit):
    """(status, x): status 0 = set found, 2 = infeasible, anything else = undecided"""
    if not cpsat:
        cons = [LinearConstraint(Am, rhs, rhs)] + ([] if wit is None else [LinearConstraint(wit.reshape(1, -1), 1, np.inf)])
        r = milp(c=np.zeros(M), constraints=cons, integrality=np.ones(M), bounds=Bounds(np.zeros(M), np.ones(M)), options={"time_limit": TL})
        return (0, r.x) if (r.status == 0 and r.x is not None) else ((2, None) if r.status == 2 else (r.status if r.status else 9, None))
    from ortools.sat.python import cp_model
    m = cp_model.CpModel(); x = [m.NewBoolVar(f"x{t}") for t in range(M)]
    Ai = np.round(Am).astype(np.int64); assert np.abs(Ai - Am).max() == 0
    for row, r0 in zip(Ai, np.round(rhs).astype(np.int64)): m.Add(sum(int(c) * x[t] for t, c in enumerate(row) if c) == int(r0))
    if wit is not None: m.Add(sum(int(c) * x[t] for t, c in enumerate(np.round(wit).astype(np.int64)) if c) >= 1)
    sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = TL; sv.parameters.num_workers = int(os.environ.get('T2_WORKERS', '8'))   # 8 in every run before 21 Nov 04:50 UTC
    st = sv.Solve(m)
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE): return 0, np.array([sv.Value(v) for v in x], dtype=float)
    return (2, None) if st == cp_model.INFEASIBLE else (9, None)
print(f"Z_{M} = Z_({p}^{a} {q}^{b});  {len(ORD)} orders, {len(G)} classes;  patterns in {'rational' if exact else 'floating-point'} arithmetic, sets by {'CP-SAT' if cpsat else 'HiGHS'}, time limit {TL:g} s per 0/1 programme" + ("   CONTROL: looking for sets that SATISFY (T2) at (i, j) instead" if control else ""))
for i in range(1, a + 1):
    for j in range(1, b + 1):
        if ONLY and (i, j) not in ONLY: continue                              # T2_ONLY="1,2;2,1" restricts the run to those (i, j) (added 21 Nov, to keep runs bounded)
        need = {(i, 0), (0, j)}; d0 = (i, j); free = [o for o in ORD if o not in need and o != d0]
        allowed = {}                                                          # size k -> list of patterns allowing it
        for r in range(len(free) + 1):
            for extra in itertools.combinations(free, r):
                Z = frozenset(need | set(extra) | ({d0} if control else set())); nlp += 1
                rg = sumf_range(Z)
                if rg is None: continue
                lo, hi = rg
                for k in range(2, M):
                    if exact:
                        if lo * k <= M and (hi is None or M <= hi * k): allowed.setdefault(k, []).append(Z)
                    elif lo - 1e-7 <= M / k <= hi + 1e-7: allowed.setdefault(k, []).append(Z)
        todo = []
        for k, Zs in sorted(allowed.items()):
            mins = [Z for Z in Zs if not any(Y < Z for Y in Zs)]
            todo += [(k, Z) for Z in mins]
        line = f"(i, j) = ({i}, {j}): p^{i} = {p**i}, q^{j} = {q**j} zeros, {val(d0)} " + ("a zero too" if control else "not") + f";  sizes allowed by some pattern: {sorted(allowed)};  minimal (size, pattern) pairs: {len(todo)}"
        print(line, flush=True)
        ui = X % p ** i; vj = X % q ** j
        N = lambda u, v: ((ui == u % p ** i) & (vj == v % q ** j)).astype(float)
        wit = N(0, 0) - N(p ** (i - 1), 0) - N(0, q ** (j - 1)) + N(p ** (i - 1), q ** (j - 1))
        for k, Z in todo:
            eqs = [np.ones((1, M))] + [res(o) for o in sorted(Z)]; Am = np.vstack(eqs); rhs = np.zeros(Am.shape[0]); rhs[0] = k
            st, xs = solve01(Am, rhs, None if control else wit); nmilp += 1
            if st == 0:
                A = [int(x) for x in X if xs[x] > 0.5]
                assert len(A) == k and all(divides(val(o), A, M) for o in Z), "the solver returned something that is not a solution"
                f, ZA = exact_complement(A)
                viol = [(ii, jj) for ii in range(1, a + 1) for jj in range(1, b + 1) if (ii, 0) in ZA and (0, jj) in ZA and (ii, jj) not in ZA]
                found.append((i, j, k, A, sorted(val(o) for o in ZA), f is not None, viol))
                print(f"   SET, size {k}: {A}\n      zeros (exact): {sorted(val(o) for o in ZA)};  exact weak complement: {'YES' if f is not None else 'no'};  (T2) violated at {viol if viol else 'nowhere'}", flush=True)
                if f is not None: print("      complement by class (i, j) -> value: " + ", ".join(f"{g}: {v}" for g, v in zip(G, f) if v), flush=True)
            elif st == 2: ninf += 1
            else: ntl += 1; print(f"   size {k}, pattern {sorted(val(o) for o in Z)}: not decided (status {st})", flush=True)
bad = [x for x in found if x[5] and x[6]]
print(f"\n{nlp} patterns examined, {nmilp} 0/1 programmes: {ninf} infeasible, {len(found)} with a set, {ntl} undecided;  {time.time() - t0:.0f} s")
if control: print(f"CONTROL: {len(found)} sets found, of which {sum(1 for x in found if x[5])} are weak tiles by exact check")
elif found: print(f"SETS RETURNED: {len(found)}.  Each has the zeros of a pattern that allows its size and lacks the zero p^i q^j, so each is a weak tile violating (T2) if the pattern stage is right; with an exact complement checked point by point: {len(bad)}.   [After review: a returned set can no longer be reported as none found.]")
else: print("WEAK TILES VIOLATING (T2): none found (no programme returned a set)" + ("" if ntl == 0 else f"   ({ntl} programmes undecided: not a clean negative)"))
