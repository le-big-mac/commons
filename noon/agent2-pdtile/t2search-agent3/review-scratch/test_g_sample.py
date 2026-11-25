"""(g), larger sizes at M = 72 / 108: targeted random samples, each set decided by the full LP on all M unknowns (no pattern logic).
Populations:
  T2V : random sets that VIOLATE (T2) as sets: |A| = k (multiple of pq), Phi_{p^i}, Phi_{q^j} | A, the standard cuboid >= 1, plus 0-3 random extra zeros
  T1V : random sets with prescribed zeros S + mixed and a size k different from the (T1) value of their actual prime-power zero set
  OK  : random sets with a (T1)/(T2)-consistent prescribed zero set and the (T1) size (many are weak tiles: positive population)
  TILE: random tiles built recursively (lifts of tiles of quotients), must come out as weak tiles satisfying (T1), (T2)
  PERT: tiles with one element moved
usage: test_g_sample.py p a q b nper seed"""
import sys, random, time, itertools
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from common import *
import wt
p, a, q, b = (int(v) for v in sys.argv[1:5]); nper = int(sys.argv[5]); seed = int(sys.argv[6])
M = p ** a * q ** b; rnd = random.Random(seed); np.random.seed(seed)
divs = [d for d in divisors(M) if d > 1]; RES = {d: residues(d, M) for d in divs}
PP = [d for d in divs if d % p != 0 or d % q != 0]; MIX = [d for d in divs if d not in PP]
def solve(k, Zreq, wit=None, tl=10):
    rows = [np.ones((1, M))] + [RES[d] for d in Zreq]; Am = np.vstack(rows).astype(float); rhs = np.zeros(Am.shape[0]); rhs[0] = k
    cons = [LinearConstraint(Am, rhs, rhs)] + ([] if wit is None else [LinearConstraint(wit.reshape(1, -1), 1, np.inf)])
    r = milp(c=np.random.randn(M), constraints=cons, integrality=np.ones(M), bounds=Bounds(np.zeros(M), np.ones(M)), options={"time_limit": tl})
    if r.x is None: return None
    A = [x for x in range(M) if r.x[x] > 0.5]
    return A if len(A) == k and all(divides(d, A, M) for d in Zreq) else None
def wit_vec(i, j):
    X = np.arange(M); ui = X % p ** i; vj = X % q ** j
    N = lambda u, v: ((ui == u % p ** i) & (vj == v % q ** j)).astype(float)
    return N(0, 0) - N(p ** (i - 1), 0) - N(0, q ** (j - 1)) + N(p ** (i - 1), q ** (j - 1))
def t1val(Z): return p ** sum(1 for d in Z if d in PP and d % p == 0) * q ** sum(1 for d in Z if d in PP and d % q == 0)
def random_tile(M):
    """a tile A of Z_M (with complement B), built by: pick a prime r | M; either A = lift of a tile of Z_{M/r} with arbitrary lifts (then B periodic),
    or A = (tile of Z_{M/r} lifted arbitrarily... as the periodic factor): A' + (M/r) Z_r."""
    if M == 1: return [0], [0]
    r = rnd.choice([s for s in (p, q) if M % s == 0]); A1, B1 = random_tile(M // r); m = M // r
    if rnd.random() < 0.5: A1, B1 = B1, A1
    A = [(x + m * rnd.randrange(r)) % M for x in A1]; B = sorted({(y + m * t) % M for y in B1 for t in range(r)})
    if rnd.random() < 0.5: A, B = B, A
    return sorted(set(A)), sorted(set(B))
pool = []
# T2V
for i in range(1, a + 1):
    for j in range(1, b + 1):
        d0 = p ** i * q ** j; w = wit_vec(i, j); ks = [k for k in range(p * q, M // 2 + 1, p * q)]
        for rep in range(nper):
            k = rnd.choice(ks); extra = rnd.sample([d for d in divs if d not in (p ** i, q ** j, d0)], rnd.randint(0, 3))
            A = solve(k, [p ** i, q ** j] + extra, w)
            if A is None and extra: A = solve(k, [p ** i, q ** j], w)
            if A is not None: pool.append(("T2V", A))
# T1V and OK
for rep in range(nper * 6):
    S = [d for d in PP if rnd.random() < 0.5]
    if not S: continue
    t1 = t1val(S); mult = (p if any(d % p == 0 for d in S) else 1) * (q if any(d % q == 0 for d in S) else 1)
    closure = [x * y for x in S if x % p == 0 for y in S if y % q == 0]
    mix = list(set(closure) | set(rnd.sample(MIX, rnd.randint(0, 2)))) if rnd.random() < 0.7 else rnd.sample(MIX, rnd.randint(0, 3))
    if rep % 2 == 0:
        ks = [k for k in range(2 * t1, M // 2 + 1, t1)] or [k for k in range(mult, M // 2 + 1, mult) if k != t1]
        if not ks: continue
        A = solve(rnd.choice(ks), S + mix)
        if A is not None: pool.append(("T1V", A))
    elif t1 < M:
        A = solve(t1, S + mix)
        if A is not None: pool.append(("OK", A))
for rep in range(nper * 4):
    A, B = random_tile(M)
    if 1 < len(A) < M:
        chk = sorted((x + y) % M for x in A for y in B); assert chk == list(range(M))
        pool.append(("TILE", A))
        if rep % 2 == 0:
            A2 = set(A); A2.remove(rnd.choice(A)); A2.add(rnd.choice([x for x in range(M) if x not in A2])); pool.append(("PERT", sorted(A2)))
t0 = time.time(); stats = {}
for kind, A in pool:
    s = stats.setdefault(kind, dict(n=0, wt=0, wt_exact=0, no_exact=0, uncert=0, T1viol_sets=0, T2viol_sets=0, wt_T1viol=0, wt_T2viol=0, class_mismatch=0, sizes=set()))
    Z = zeros_exact(A, M); k = len(A); s["n"] += 1; s["sizes"].add(k)
    feas, f = wt.full_lp(A, M)
    cl = wt.class_lp(A, M, Z); s["class_mismatch"] += (cl != feas)
    v1 = not T1_holds(Z, k, p, a, q, b); v2 = bool(T2_violations(Z, p, a, q, b)); s["T1viol_sets"] += v1; s["T2viol_sets"] += v2
    if feas:
        s["wt"] += 1; s["wt_T1viol"] += v1; s["wt_T2viol"] += v2
        fz = np.where(np.abs(f) < 1e-9, 0, f)
        ok = any(wt.verify_f(A, M, fr) for fr in wt.rationalise(fz)); s["wt_exact"] += ok; s["uncert"] += not ok
        if v1 or v2: print("WEAK TILE VIOLATING", "T1" if v1 else "", "T2" if v2 else "", A, sorted(Z), "exact complement verified:", ok)
    else:
        # exact Farkas certificate: restricted LP + rationalisation only (cheap); otherwise the verdict rests on HiGHS
        As = set(A); Dset = {(x - y) % M for x in A for y in A}; T = [t for t in range(M) if t not in Dset]; Ac = [y for y in range(M) if y not in As]; ok = False
        if not T: ok = True      # A - A = Z_M: no weak complement, by the support argument (F1)
        else:
            from scipy.optimize import linprog
            from fractions import Fraction
            C = np.array([[1.0 if (y - t) % M in As else 0.0 for y in Ac] for t in T])
            r = linprog(-np.ones(len(Ac)), A_ub=C, b_ub=np.zeros(len(T)), bounds=[(-1, 1)] * len(Ac), method="highs")
            if r.status == 0 and -r.fun > 1e-7:
                for wr in wt.rationalise(r.x, dens=(1, 2, 3, 4, 6, 12, 60, 2520, 10 ** 5, 10 ** 7)):
                    w = [Fraction(0)] * M
                    for y, v in zip(Ac, wr): w[y] = v
                    for x in A: w[x] = Fraction(-k)
                    if wt.verify_farkas(A, M, (w, Fraction(k * k))): ok = True; break
        s["no_exact"] += ok; s["uncert"] += not ok
print(f"Z_{M} = {p}^{a} {q}^{b}, seed {seed}: {len(pool)} sets decided by the full LP on {M} unknowns in {time.time() - t0:.0f} s")
for kind, s in stats.items():
    print(f"   {kind:5s}: {s['n']:4d} sets (sizes {min(s['sizes'])}..{max(s['sizes'])}; as sets, {s['T1viol_sets']} violate (T1), {s['T2viol_sets']} violate (T2)):  weak tiles {s['wt']} "
          f"({s['wt_exact']} with an exactly verified rational complement), non-weak-tiles with an exactly verified certificate {s['no_exact']}, float-only verdicts {s['uncert']};  "
          f"WEAK TILES VIOLATING (T1): {s['wt_T1viol']}, (T2): {s['wt_T2viol']};  full LP vs class-constant reduction mismatches: {s['class_mismatch']}")
