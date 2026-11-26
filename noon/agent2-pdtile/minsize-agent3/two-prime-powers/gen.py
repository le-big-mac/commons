"""The least size of a nonempty multiset on Z_M whose mask polynomial is divisible by exactly a given set D of the cyclotomic
polynomials Phi_d, d | M, d > 1.  Any M.  CP-SAT minimises the size directly; "Phi_d | A" is "A(X) mod Phi_d(X) = 0" coefficient
by coefficient, and "Phi_d does not divide A" is "some coefficient of the remainder is not zero".  A witness is checked by a
second route: the complex value A(zeta_d).
usage: gen.py M [--only d1,d2,...] [--tlimit SEC] [--workers W] [--cap C]      one line of JSON per pattern
The multiset is translated so that 0 is in it (the pattern does not change under translation)."""
import sys, json, time, cmath, math, itertools
from ortools.sat.python import cp_model

def cyclotomic(d, _c={}):
    if d in _c: return _c[d]
    num = [-1] + [0] * (d - 1) + [1]
    for e in range(1, d):
        if d % e == 0:
            den = cyclotomic(e); quo = [0] * (len(num) - len(den) + 1); num = num[:]
            for k in range(len(quo) - 1, -1, -1):
                c = num[k + len(den) - 1]; quo[k] = c
                for t, dc in enumerate(den): num[k + t] -= c * dc
            assert not any(num); num = quo
    _c[d] = num; return num

def remainder_rows(M, d):
    """row j = coefficients (over x = 0..M-1) of X^j in (X^x mod Phi_d)"""
    phi = cyclotomic(d); deg = len(phi) - 1; rows = [[0] * M for _ in range(deg)]; cur = [0] * deg; cur[0] = 1
    for x in range(M):
        for j in range(deg): rows[j][x] = cur[j]
        top = cur[-1]; cur = [0] + cur[:-1]
        if top:
            for t in range(deg): cur[t] -= top * phi[t]
    return rows

def divides(M, d, x, tol=1e-9):
    z = cmath.exp(2j * math.pi / d); return abs(sum(w * z ** k for k, w in enumerate(x) if w)) < tol * max(1, sum(x))

def minimum(M, divs, D, tlimit, workers, cap):
    m = cp_model.CpModel(); x = [m.NewIntVar(0, cap, f'x{i}') for i in range(M)]; m.Add(x[0] >= 1)
    for d in divs:
        rows = remainder_rows(M, d)
        if d in D:
            for r in rows: m.Add(sum(c * x[i] for i, c in enumerate(r) if c) == 0)
        else:
            bs = []
            for k, r in enumerate(rows):
                e = sum(c * x[i] for i, c in enumerate(r) if c); bp = m.NewBoolVar(f'p{d}_{k}'); bn = m.NewBoolVar(f'n{d}_{k}')
                m.Add(e >= 1).OnlyEnforceIf(bp); m.Add(e <= -1).OnlyEnforceIf(bn); bs += [bp, bn]
            m.AddBoolOr(bs)
    m.Minimize(sum(x)); s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = tlimit; s.parameters.num_search_workers = workers
    st = s.Solve(m)
    if st == cp_model.OPTIMAL or st == cp_model.FEASIBLE:
        v = [s.Value(t) for t in x]
        got = sorted(d for d in divs if divides(M, d, v)); assert got == sorted(D), ('witness fails the second check', D, got, v)
        return sum(v), v, st == cp_model.OPTIMAL
    return None, None, st == cp_model.INFEASIBLE

if __name__ == '__main__':
    a = sys.argv[1:]; M = int(a[0]); opt = dict(zip(a[1::2], a[2::2]))
    tl = float(opt.get('--tlimit', 120)); W = int(opt.get('--workers', 4)); cap = int(opt.get('--cap', M))
    divs = [d for d in range(2, M + 1) if M % d == 0]
    pats = [sorted(int(t) for t in opt['--only'].split(',') if t)] if '--only' in opt else [list(c) for k in range(len(divs) + 1) for c in itertools.combinations(divs, k)]
    print(f'# M={M} divisors={divs} patterns={len(pats)} cap={cap} tlimit={tl}', flush=True)
    for D in pats:
        t0 = time.time(); sz, v, proved = minimum(M, divs, set(D), tl, W, cap)
        wit = '' if v is None else ' '.join(f'{i}' + (f'^{w}' if w > 1 else '') for i, w in enumerate(v) if w)
        print(json.dumps(dict(M=M, D=D, min=sz, proved=proved, witness=wit, seconds=round(time.time() - t0, 1))), flush=True)
