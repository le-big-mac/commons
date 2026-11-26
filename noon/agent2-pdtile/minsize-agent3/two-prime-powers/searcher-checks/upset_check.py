"""SEALED (belongs to sealed-derivations.md).  Exact least sizes for up-set patterns, by CP-SAT.

For M and each up-set D of the divisor lattice of M (1 never in D), find the least |A| of a nonempty
multiset A on Z_M with Phi_d | A(X) exactly for d in D (d | M, d > 1), and compare it with
    formula(D) = sum of M/c over the maximal divisors c of M that are not in D.
With --sets the multiplicities are 0/1.  With --weak the non-divisibility is required only at the
maximal non-members c (the hypothesis the proof in the sealed file uses).

usage: python -I upset_check.py M [--sets] [--weak] [--time SECONDS] [--all] [--only d1,d2,...]
(--all: every pattern, not only up-sets; --only: one pattern)
"""
import sys, itertools
from ortools.sat.python import cp_model

def cyclotomic(n, cache={}):
    # integer coefficient list (low degree first) of Phi_n, by dividing X^n - 1 by Phi_d, d | n, d < n
    if n in cache: return cache[n]
    num = [-1] + [0] * (n - 1) + [1]
    for d in range(1, n):
        if n % d == 0:
            den = cyclotomic(d)
            q = [0] * (len(num) - len(den) + 1)
            num = num[:]
            for i in range(len(q) - 1, -1, -1):
                q[i] = num[i + len(den) - 1]          # den is monic
                for j, c in enumerate(den): num[i + j] -= q[i] * c
            assert not any(num)
            num = q
    cache[n] = num
    return num

def residues(M, d):
    # rows r_k = coefficients of X^k mod Phi_d, k = 0..M-1
    phi = cyclotomic(d); deg = len(phi) - 1
    r = [1] + [0] * (deg - 1) if deg > 0 else []
    rows = []
    for k in range(M):
        rows.append(r[:])
        top = r[-1]
        r = [0] + r[:-1]
        if top:
            for j in range(deg): r[j] -= top * phi[j]
    return rows

def pattern_of(M, A):
    out = []
    for d in range(2, M + 1):
        if M % d: continue
        rows = residues(M, d)
        if all(sum(A[k] * rows[k][i] for k in range(M)) == 0 for i in range(len(rows[0]))): out.append(d)
    return out

def solve(M, D, sets, weak, tlim, cap):
    divs = [d for d in range(2, M + 1) if M % d == 0]
    comp = [c for c in [1] + divs if c not in D]
    mx = [c for c in comp if not any(e != c and e % c == 0 for e in comp)]
    m = cp_model.CpModel()
    hi = 1 if sets else cap
    A = [m.NewIntVar(0, hi, f'a{k}') for k in range(M)]
    m.Add(sum(A) >= 1)
    for d in divs:
        rows = residues(M, d); deg = len(rows[0])
        exprs = [sum(rows[k][i] * A[k] for k in range(M) if rows[k][i]) for i in range(deg)]
        if d in D:
            for e in exprs: m.Add(e == 0)
        elif (not weak) or d in mx:
            bs = []
            for i, e in enumerate(exprs):
                bp = m.NewBoolVar(f'p{d}_{i}'); bn = m.NewBoolVar(f'n{d}_{i}')
                m.Add(e >= 1).OnlyEnforceIf(bp); m.Add(e <= -1).OnlyEnforceIf(bn)
                bs += [bp, bn]
            m.AddBoolOr(bs)
    m.Minimize(sum(A))
    s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = tlim; s.parameters.num_search_workers = 8
    st = s.Solve(m)
    name = s.StatusName(st)
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        a = [s.Value(x) for x in A]
        return name, sum(a), int(round(s.BestObjectiveBound())), a, mx
    return name, None, None, None, mx

def main():
    M = int(sys.argv[1]); sets = '--sets' in sys.argv; weak = '--weak' in sys.argv; allp = '--all' in sys.argv
    tlim = float(sys.argv[sys.argv.index('--time') + 1]) if '--time' in sys.argv else 60.0
    divs = [d for d in range(2, M + 1) if M % d == 0]
    def is_up(D): return all(e in D for d in D for e in divs if e % d == 0)
    pats = []
    for r in range(len(divs) + 1):
        for D in itertools.combinations(divs, r):
            D = frozenset(D)
            if allp or is_up(D): pats.append(D)
    if '--only' in sys.argv:                       # --only d1,d2,... : that single pattern ('' for the empty one)
        pats = [frozenset(int(x) for x in sys.argv[sys.argv.index('--only') + 1].split(',') if x)]
    print(f'M = {M}; {"sets" if sets else "multisets"}; {"non-divisors only at maximal c" if weak else "exact pattern"}; '
          f'{len(pats)} patterns; time limit {tlim:g} s each')
    agree = 0; total = 0; viol = []
    for D in pats:
        comp = [c for c in [1] + divs if c not in D]
        mx = [c for c in comp if not any(e != c and e % c == 0 for e in comp)]
        f = sum(M // c for c in mx)
        up = is_up(D)
        if not up:
            # general lower bound: U = the largest up-set inside D; LB = sum of M/c over the maximal non-members of U
            U = frozenset(d for d in D if all(e in D for e in divs if e % d == 0))
            compU = [c for c in [1] + divs if c not in U]
            mxU = [c for c in compU if not any(e != c and e % c == 0 for e in compU)]
            lb = sum(M // c for c in mxU)
        name, val, bound, a, mx = solve(M, D, sets, weak, tlim, max(f, 1) if up else 3 * M)
        total += 1
        ok = ''
        if a is not None:
            pat = pattern_of(M, a)
            if not weak: assert sorted(pat) == sorted(D), (sorted(D), pat)
            if up:
                ok = 'AGREES' if (name == 'OPTIMAL' and val == f) else ('differs' if name == 'OPTIMAL' else 'not proved')
                if ok == 'AGREES': agree += 1
            else:
                ok = ('LB-ok' if val >= lb else 'LB-VIOLATED') + ('' if name == 'OPTIMAL' else ' not proved')
                if val < lb: viol.append(sorted(D))
        if up:
            print(f'D={sorted(D)} up-set maxc={mx} formula={f} status={name} least={val} bound={bound} {ok}'
                  + (f' A={[k for k in range(M) for _ in range(a[k])]}' if a is not None and (ok != "AGREES") else ''), flush=True)
        else:
            print(f'D={sorted(D)} not-up-set up-interior={sorted(U)} LB={lb} status={name} least={val} bound={bound} {ok}', flush=True)
    print(f'up-sets that agree with the formula and are proved optimal: {agree} of {sum(1 for D in pats if is_up(D))}; '
          f'patterns in all: {total}; lower bound violated: {len(viol)} {viol}')

main()
