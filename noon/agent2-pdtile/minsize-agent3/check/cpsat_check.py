"""Referee's own CP-SAT model (written from section 1 of the note: class counts on the tree), used for spot checks that
do not rest on dp.c:  is there a multiset (or set) on Z_{p^n q} of size exactly s with exactly the pattern (E, F)?
usage: cpsat_check.py p q n kind(multi|set) E F s1[,s2,...] [tlimit] [workers]      E, F as comma lists, '-' for empty
Every witness is checked by exact polynomial division (pat.py)."""
import sys, time
sys.path.insert(0, '/home/agent3/minsize/check')
from pat import *
from ortools.sat.python import cp_model


def feasible(p, q, n, E, F, s, is_set, tlimit=600, workers=1):
    m = cp_model.CpModel()
    pn = p ** n
    hi = 1 if is_set else s
    x = [[m.NewIntVar(0, hi, f'x{u}_{j}') for j in range(q)] for u in range(pn)]     # leaf u, layer j
    m.Add(sum(x[u][j] for u in range(pn) for j in range(q)) == s)

    def vec(d, c):      # layer vector of class c mod p^d, as linear expressions
        return [sum(x[u][j] for u in range(c, pn, p ** d)) for j in range(q)]

    def neq_any(exprs, name):
        bs = []
        for i, ex in enumerate(exprs):
            bp = m.NewBoolVar(f'{name}p{i}'); bn = m.NewBoolVar(f'{name}n{i}')
            m.Add(ex >= 1).OnlyEnforceIf(bp); m.Add(ex <= -1).OnlyEnforceIf(bn)
            bs += [bp, bn]
        m.AddBoolOr(bs)

    root = vec(0, 0)
    bal = [root[j] - root[0] for j in range(1, q)]
    if 0 in F:
        for ex in bal: m.Add(ex == 0)
    else:
        neq_any(bal, 'F0')
    for a in range(1, n + 1):
        tot_diffs = []; shape_diffs = []
        for c in range(p ** (a - 1)):
            kids = [vec(a, c + i * p ** (a - 1)) for i in range(p)]
            for i in range(1, p):
                tot_diffs.append(sum(kids[i]) - sum(kids[0]))
                for j in range(1, q):
                    shape_diffs.append((kids[i][j] - kids[0][j]) - (kids[i][0] - kids[0][0]))
        if a in E:
            for ex in tot_diffs: m.Add(ex == 0)
        else:
            neq_any(tot_diffs, f'E{a}')
        if a in F:
            for ex in shape_diffs: m.Add(ex == 0)
        else:
            neq_any(shape_diffs, f'F{a}')
    sol = cp_model.CpSolver()
    sol.parameters.max_time_in_seconds = tlimit
    sol.parameters.num_search_workers = workers
    st = sol.Solve(m)
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        M = pn * q
        w = [0] * M
        for u in range(pn):
            for j in range(q):
                v = sol.Value(x[u][j])
                if v:
                    xx = next(t for t in range(u, M, pn) if t % q == j)
                    w[xx] = v
        assert sum(w) == s and exact_pattern_division(p, q, n, w) == (tuple(sorted(E)), tuple(sorted(F))), 'witness fails exact division'
        return True, w
    if st == cp_model.INFEASIBLE:
        return False, None
    return None, None


if __name__ == '__main__':
    p, q, n = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]); kind = sys.argv[4]
    E = tuple(int(t) for t in sys.argv[5].split(',')) if sys.argv[5] != '-' else ()
    F = tuple(int(t) for t in sys.argv[6].split(',')) if sys.argv[6] != '-' else ()
    sizes = [int(t) for t in sys.argv[7].split(',')]
    tl = float(sys.argv[8]) if len(sys.argv) > 8 else 600
    wk = int(sys.argv[9]) if len(sys.argv) > 9 else 1
    for s in sizes:
        t0 = time.time()
        ok, w = feasible(p, q, n, E, F, s, kind == 'set', tl, wk)
        res = 'EXISTS' if ok else ('NONE (proved infeasible)' if ok is False else 'undecided (time limit)')
        wit = '' if not ok else '  witness (checked by exact division): ' + ' '.join(f'{i}' + (f'^{v}' if v > 1 else '') for i, v in enumerate(w) if v)
        print(f'p={p} q={q} n={n} order {p ** n * q} {kind} E={list(E)} F={list(F)} size {s}: {res}  [{time.time() - t0:.1f} s]{wit}', flush=True)
