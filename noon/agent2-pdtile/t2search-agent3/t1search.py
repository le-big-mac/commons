r"""Is there a weak tile of Z_M, M = p^a q^b, that violates (T1)?  The companion of t2search.py.  (agent3 / Yonder)
(T1): |A| = product of Phi_s(1) over the prime powers s that are zeros of A, i.e. p^(number of p-power zeros) * q^(number of q-power zeros).
For every set S of prime powers (the exact prime-power zeros) and every pattern Z of orders whose prime powers are exactly S:
  the rational linear programme of t2search.py gives the sizes k the pattern allows; for each k different from the (T1) value of S and each
  minimal such pattern, CP-SAT looks for a set A with |A| = k, Phi_d | A for d in Z, and Phi_s not dividing A for every prime power s not in S
  (for s = r^e: two classes modulo r^e inside one class modulo r^(e-1) hold different numbers of elements; a disjunction, stated as such).
A weak tile violating (T1) has its exact zero set as a pattern allowing its size, hence some minimal pattern with the same prime powers below it.
Any set returned is re-verified exactly, as in t2search.py.   usage: t1search.py p a q b [time limit, s] [--control]
(--control: sizes EQUAL to the (T1) value, where tiles exist and must be found)"""
import sys, itertools, time, numpy as np
from fractions import Fraction
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))     # lemma_variants.py, cyclo_exact.py, exactlp.py sit beside this file
from lemma_variants import residues
from cyclo_exact import divides
from exactlp import lp as exact_lp
from ortools.sat.python import cp_model
p, a, q, b = (int(x) for x in sys.argv[1:5]); TL = float(sys.argv[5]) if len(sys.argv) > 5 and not sys.argv[5].startswith("-") else 300.0
control = "--control" in sys.argv
M = p ** a * q ** b; X = list(range(M))
vp = lambda x, r, cap: next(e for e in range(cap, -1, -1) if x % r ** e == 0)
cls = [(vp(x, p, a), vp(x, q, b)) for x in X]
G = [(i, j) for i in range(a + 1) for j in range(b + 1)]; gi = {g: n for n, g in enumerate(G)}
size = [sum(1 for c in cls if c == g) for g in G]
ORD = [(l, m) for l in range(a + 1) for m in range(b + 1) if (l, m) != (0, 0)]; val = lambda o: p ** o[0] * q ** o[1]
PP = [o for o in ORD if o[0] == 0 or o[1] == 0]; MIX = [o for o in ORD if o not in PP]
Tm = {}
for o in ORD:
    xi = M // val(o); row = np.zeros(len(G)); c = np.cos(2 * np.pi * ((np.arange(M) * xi) % M) / M)
    for x in X: row[gi[cls[x]]] += c[x]
    assert np.allclose(row, np.round(row), atol=1e-6); Tm[o] = [int(v) for v in np.round(row)]
unit0 = [int(g == (a, b)) for g in G]
def sizes_allowed(Z):
    rows = [unit0] + [Tm[o] for o in ORD if o not in Z]; rhs = [1] + [0] * (len(rows) - 1)
    st, lo, _ = exact_lp(rows, rhs, size)
    if st == "infeasible": return []
    st2, hi, _ = exact_lp(rows, rhs, [-v for v in size]); hi = None if st2 == "unbounded" else -hi
    return [k for k in range(1, M + 1) if lo * k <= M and (hi is None or M <= hi * k)]
RES = {}
def res(o):
    if o not in RES: RES[o] = residues(val(o), M)
    return RES[o]
def find(k, Z, nonzero):
    m = cp_model.CpModel(); x = [m.NewBoolVar(f"x{t}") for t in X]
    m.Add(sum(x) == k)
    for o in sorted(Z):
        for row in res(o): m.Add(sum(int(c) * x[t] for t, c in enumerate(row) if c) == 0)
    for o in nonzero:
        r, e = (p, o[0]) if o[1] == 0 else (q, o[1]); re_, rl = r ** e, r ** (e - 1); lits = []
        cnt = {c: sum(x[t] for t in X if t % re_ == c) for c in range(re_)}
        for c1 in range(re_):
            for c2 in range(re_):
                if c1 != c2 and c1 % rl == c2 % rl:
                    y = m.NewBoolVar(f"w{o}_{c1}_{c2}"); m.Add(cnt[c1] >= cnt[c2] + 1).OnlyEnforceIf(y); lits.append(y)
        m.AddBoolOr(lits)
    sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = TL; sv.parameters.num_workers = int(os.environ.get('T2_WORKERS', '8'))   # 8 in every run before 21 Nov 04:50 UTC
    st = sv.Solve(m)
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE): return 0, [t for t in X if sv.Value(x[t])]
    return (2, None) if st == cp_model.INFEASIBLE else (9, None)
def exact_complement(A):
    ZA = {o for o in ORD if divides(val(o), A, M)}
    rows = [unit0] + [Tm[o] for o in ORD if o not in ZA] + [size]; rhs = [1] + [0] * (len(rows) - 2) + [Fraction(M, len(A))]
    st, _, f = exact_lp(rows, rhs, [0] * len(G))
    if st != "optimal": return None, ZA
    fx = [f[gi[cls[x]]] for x in X]; ok = all(sum(fx[(y - x) % M] for x in A) == 1 for y in X) and all(v >= 0 for v in f) and f[gi[(a, b)]] == 1   # last two checks added after review
    return (f if ok else None), ZA
t0 = time.time(); nprog = ninf = nund = 0; found = []; npat = 0
print(f"Z_{M} = Z_({p}^{a} {q}^{b}); (T1) search" + (" CONTROL (sizes equal to the (T1) value)" if control else "") + f"; rational pattern programmes, sets by CP-SAT, {TL:g} s limit")
for r in range(len(PP) + 1):
    for S in itertools.combinations(PP, r):
        S = frozenset(S); t1 = p ** sum(1 for o in S if o[1] == 0) * q ** sum(1 for o in S if o[0] == 0)
        allowed = {}
        for r2 in range(len(MIX) + 1):
            for mix in itertools.combinations(MIX, r2):
                Z = S | frozenset(mix); npat += 1
                for k in sizes_allowed(Z):
                    if (k == t1) == control: allowed.setdefault(k, []).append(Z)
        todo = [(k, Z) for k, Zs in sorted(allowed.items()) for Z in Zs if not any(Y < Z for Y in Zs)]
        if not todo: continue
        nz = [o for o in PP if o not in S]; here = 0
        for k, Z in todo:
            st, A = find(k, Z, nz); nprog += 1
            if st == 0:
                assert len(A) == k and all(divides(val(o), A, M) for o in Z) and not any(divides(val(o), A, M) for o in nz), "not a solution"
                f, ZA = exact_complement(A); found.append((sorted(val(o) for o in S), k, t1, A, f is not None)); here += 1
                if not control or here <= 1: print(f"   prime-power zeros {sorted(val(o) for o in S)} ((T1) value {t1}), size {k}: SET {A}; zeros {sorted(val(o) for o in ZA)}; exact weak complement: {'YES' if f is not None else 'no'}", flush=True)
            elif st == 2: ninf += 1
            else: nund += 1; print(f"   prime-power zeros {sorted(val(o) for o in S)}, size {k}, pattern {sorted(val(o) for o in Z)}: not decided", flush=True)
bad = [x for x in found if x[4]]
print(f"\n{npat} patterns, {nprog} programmes: {ninf} infeasible, {len(found)} with a set ({len(bad)} of them weak tiles by exact check), {nund} undecided; {time.time() - t0:.0f} s")
if control: print(f"CONTROL: {len(bad)} weak tiles found at the (T1) size")
elif found: print(f"SETS RETURNED: {len(found)}; with an exact complement checked point by point: {len(bad)}.")
else: print("WEAK TILES VIOLATING (T1): none found (no programme returned a set)" + ("" if nund == 0 else f"   ({nund} undecided: not a clean negative)"))
