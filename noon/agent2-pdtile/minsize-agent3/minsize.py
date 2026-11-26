"""The smallest multiset (or set) on Z_M, M = p^n q, whose cyclotomic divisors among Phi_d, d | M, d > 1,
are EXACTLY those named by E and F:
    E = { a in 1..n : Phi_{p^a} | A },     F = { a in 0..n : Phi_{p^a q} | A }.

Two encodings of "Phi_d divides A", made independently of one another:
  (B) by class counts (used with CP-SAT):
      Phi_{p^a} | A   iff  the counts N(c) of A in the classes c mod p^a are equal on the p lifts of each class mod p^(a-1);
      Phi_{p^a q} | A iff  within each class c0 mod p^(a-1), the p x q array G(i, j) = (count of A at c0 + i p^(a-1)
                           mod p^a and j mod q) has all mixed second differences zero (a = 0: the counts mod q are equal).
  (A) by polynomial remainders (used with HiGHS): A(X) mod Phi_d(X) = 0, coefficient by coefficient.
A witness from either solver is verified by (C): the complex value A(zeta_d), to 1e-9, a third route.

usage: minsize.py p q n [set|multi] [--solver cpsat|highs] [--patterns all|nozero] [--smax S] [--only E:F]
Prints one line per pattern.  Nothing here is imported from, or reads, any downloaded file.
"""
import sys, itertools, json, time, cmath, math
import numpy as np


# ---------- forms: lists of integer vectors v (length M) such that Phi_d | A  iff  v.x = 0 for every v ----------
def forms_B(p, q, n, kind, a):
    """class-count forms.  kind 'P': Phi_{p^a} (a >= 1); kind 'Q': Phi_{p^a q} (a >= 0)."""
    M = p ** n * q
    out = []
    if kind == 'P':
        pa, pb = p ** a, p ** (a - 1)
        for c0 in range(pb):
            for i in range(1, p):
                v = np.zeros(M, dtype=np.int64)
                for x in range(M):
                    r = x % pa
                    if r == c0: v[x] -= 1
                    if r == c0 + i * pb: v[x] += 1
                out.append(v)
    else:
        if a == 0:
            for j in range(1, q):
                v = np.zeros(M, dtype=np.int64)
                for x in range(M):
                    if x % q == 0: v[x] -= 1
                    if x % q == j: v[x] += 1
                out.append(v)
        else:
            pa, pb = p ** a, p ** (a - 1)
            for c0 in range(pb):
                for i in range(1, p):
                    for j in range(1, q):
                        v = np.zeros(M, dtype=np.int64)
                        for x in range(M):
                            r, s = x % pa, x % q
                            if r % pb != c0: continue
                            ii = (r - c0) // pb
                            # G(i,j) - G(0,j) - G(i,0) + G(0,0)
                            if ii == i and s == j: v[x] += 1
                            if ii == 0 and s == j: v[x] -= 1
                            if ii == i and s == 0: v[x] -= 1
                            if ii == 0 and s == 0: v[x] += 1
                        out.append(v)
    return out


def cyclotomic(d, _cache={}):
    """Phi_d as a list of integer coefficients, lowest degree first, by exact division of X^d - 1."""
    if d in _cache: return _cache[d]
    num = [-1] + [0] * (d - 1) + [1]
    for e in range(1, d):
        if d % e == 0:
            den = cyclotomic(e)
            quo = [0] * (len(num) - len(den) + 1)
            num = num[:]
            for k in range(len(quo) - 1, -1, -1):
                c = num[k + len(den) - 1]            # den is monic
                quo[k] = c
                for t, dc in enumerate(den): num[k + t] -= c * dc
            assert not any(num), (d, e)
            num = quo
    _cache[d] = num
    return num


def forms_A(p, q, n, kind, a):
    """polynomial-remainder forms: row j is the coefficient of X^j in (X^x mod Phi_d), for x = 0..M-1."""
    M = p ** n * q
    d = p ** a * (q if kind == 'Q' else 1)
    phi = cyclotomic(d); deg = len(phi) - 1
    R = np.zeros((deg, M), dtype=np.int64)
    cur = [0] * deg; cur[0] = 1                     # X^0   (deg >= 1 since d > 1)
    for x in range(M):
        R[:, x] = cur
        top = cur[-1]; cur = [0] + cur[:-1]          # multiply by X
        if top:
            for t in range(deg): cur[t] -= top * phi[t]
    return [R[j].copy() for j in range(deg)]


def divides_C(p, q, n, kind, a, x, tol=1e-9):
    M = p ** n * q
    d = p ** a * (q if kind == 'Q' else 1)
    z = cmath.exp(2j * math.pi / d)
    return abs(sum(int(w) * z ** k for k, w in enumerate(x) if w)) < tol * max(1, sum(x))


def exact_pattern(p, q, n, x):
    E = tuple(a for a in range(1, n + 1) if divides_C(p, q, n, 'P', a, x))
    F = tuple(a for a in range(0, n + 1) if divides_C(p, q, n, 'Q', a, x))
    return E, F


# ---------- solvers ----------
def feasible_cpsat(p, q, n, E, F, s, is_set, tlimit, workers=4):
    from ortools.sat.python import cp_model
    M = p ** n * q
    m = cp_model.CpModel()
    hi = 1 if is_set else s
    x = [m.NewIntVar(0, hi, f'x{i}') for i in range(M)]
    m.Add(sum(x) == s)
    m.Add(x[0] >= 1)                                  # by translation
    for kind, rng, S in (('P', range(1, n + 1), E), ('Q', range(0, n + 1), F)):
        for a in rng:
            fs = forms_B(p, q, n, kind, a)
            if a in S:
                for v in fs: m.Add(sum(int(c) * x[i] for i, c in enumerate(v) if c) == 0)
            else:
                bs = []
                for k, v in enumerate(fs):
                    expr = sum(int(c) * x[i] for i, c in enumerate(v) if c)
                    bp = m.NewBoolVar(f'{kind}{a}p{k}'); bn = m.NewBoolVar(f'{kind}{a}n{k}')
                    m.Add(expr >= 1).OnlyEnforceIf(bp); m.Add(expr <= -1).OnlyEnforceIf(bn)
                    bs += [bp, bn]
                m.AddBoolOr(bs)
    sol = cp_model.CpSolver()
    sol.parameters.max_time_in_seconds = tlimit; sol.parameters.num_search_workers = workers
    st = sol.Solve(m)
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE): return True, [sol.Value(v) for v in x]
    if st == cp_model.INFEASIBLE: return False, None
    return None, None                                  # time limit


def feasible_highs(p, q, n, E, F, s, is_set, tlimit):
    from scipy.optimize import milp, LinearConstraint, Bounds
    M = p ** n * q
    hi = 1 if is_set else s
    rows, lo, up = [], [], []
    nb = 0; bool_rows = []                              # (form, index of b+, index of b-)
    groups = []
    for kind, rng, S in (('P', range(1, n + 1), E), ('Q', range(0, n + 1), F)):
        for a in rng:
            fs = forms_A(p, q, n, kind, a)
            if a in S:
                for v in fs: rows.append((v, None, None)); lo.append(0); up.append(0)
            else:
                g = []
                for v in fs:
                    bool_rows.append((v, nb, nb + 1)); g += [nb, nb + 1]; nb += 2
                groups.append(g)
    N = M + nb
    Arows, lo2, up2 = [], [], []
    for (v, _, _), l, u in zip(rows, lo, up):
        r = np.zeros(N); r[:M] = v; Arows.append(r); lo2.append(l); up2.append(u)
    for v, ip, im in bool_rows:
        B = int(np.abs(v).sum()) * hi + 1
        r = np.zeros(N); r[:M] = v; r[M + ip] = -(B + 1)           # v.x >= 1 - (B+1)(1 - b+)   i.e.  v.x - (B+1) b+ >= -B
        Arows.append(r); lo2.append(-B); up2.append(np.inf)
        r = np.zeros(N); r[:M] = v; r[M + im] = (B + 1)            # v.x <= -1 + (B+1)(1 - b-)  i.e.  v.x + (B+1) b- <= B
        Arows.append(r); lo2.append(-np.inf); up2.append(B)
    for g in groups:
        r = np.zeros(N); r[[M + k for k in g]] = 1; Arows.append(r); lo2.append(1); up2.append(np.inf)
    r = np.zeros(N); r[:M] = 1; Arows.append(r); lo2.append(s); up2.append(s)
    lb = np.zeros(N); ub = np.concatenate([np.full(M, hi), np.ones(nb)]); lb[0] = 1
    res = milp(c=np.zeros(N), constraints=LinearConstraint(np.array(Arows), lo2, up2), integrality=np.ones(N),
               bounds=Bounds(lb, ub), options=dict(time_limit=tlimit, presolve=True))
    if res.status == 0 and res.x is not None: return True, [int(round(t)) for t in res.x[:M]]
    if res.status == 2: return False, None
    return None, None


def sizes(p, q, n, E, F, smax):
    """sizes allowed by evaluating at 1: p^|E| divides |A|; q divides |A| iff ... only if 0 in F (if 0 not in F nothing is forced)."""
    step = p ** len(E) * (q if 0 in F else 1)
    s = step
    while s <= smax:
        yield s
        s += step


def minimum(p, q, n, E, F, is_set, solver='cpsat', smax=None, tlimit=600):
    M = p ** n * q
    smax = smax or (M if is_set else 4 * M)
    fn = feasible_cpsat if solver == 'cpsat' else feasible_highs
    unknown = []
    for s in sizes(p, q, n, E, F, min(smax, M) if is_set else smax):
        ok, x = fn(p, q, n, E, F, s, is_set, tlimit)
        if ok:
            assert sum(x) == s and x[0] >= 1 and (not is_set or max(x) <= 1)
            assert exact_pattern(p, q, n, x) == (tuple(sorted(E)), tuple(sorted(F))), ('witness fails the third check', E, F, x)
            return s, x, unknown
        if ok is None: unknown.append(s)
    return None, None, unknown


def patterns(n, which):
    for ke in range(n + 1):
        for E in itertools.combinations(range(1, n + 1), ke):
            for kf in range(n + 2):
                for F in itertools.combinations(range(0, n + 1), kf):
                    if which == 'nozero' and 0 in F: continue
                    yield E, F


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    opt = {}
    it = iter(sys.argv[1:])
    for a in it:
        if a.startswith('--'): opt[a[2:]] = next(it)
    p, q, n = int(args[0]), int(args[1]), int(args[2]); is_set = (len(args) > 3 and args[3] == 'set')
    solver = opt.get('solver', 'cpsat'); which = opt.get('patterns', 'all'); smax = int(opt['smax']) if 'smax' in opt else None
    tl = float(opt.get('tlimit', 600))
    pats = list(patterns(n, which))
    if 'only' in opt:
        e, f = opt['only'].split(':')
        pats = [(tuple(int(c) for c in e.split(',') if c), tuple(int(c) for c in f.split(',') if c))]
    M = p ** n * q
    print(f'# p={p} q={q} n={n} M={M} {"sets" if is_set else "multisets"} solver={solver} patterns={len(pats)}', flush=True)
    for E, F in pats:
        t0 = time.time()
        s, x, unk = minimum(p, q, n, E, F, is_set, solver, smax, tl)
        wit = '' if x is None else ' '.join(f'{i}' + (f'^{w}' if w > 1 else '') for i, w in enumerate(x) if w)
        print(json.dumps(dict(p=p, q=q, n=n, E=list(E), F=list(F), kind='set' if is_set else 'multi', min=s, undecided=unk, witness=wit,
                              seconds=round(time.time() - t0, 1), solver=solver)), flush=True)
