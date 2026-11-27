# Instances of the least-size statements whose Lean value V lies beyond both censuses (t4_open.json): an integer programme.
# Model on Z_M0 (M0 = p^n q): w_y >= 0 integers, y in [0, M0); for each d | M0, d > 1, the remainder of the mask modulo Phi_d is
# the integer vector  sum_y w_y * (X^y mod Phi_d)  (rows of core.Grp, exact integers).  "Phi_d | mask": the vector is 0.
# "Phi_d does not divide the mask": some coordinate is >= 1 or <= -1 (one Boolean for each of the two, at least one true).
# w_0 >= 1 (translation).  Solver: CP-SAT (exact integer arithmetic).
#   (a) with the size fixed to V: a member of size V on Z_M0, checked by long division against the transcribed clauses;
#   (b) minimise the size (time limit): accepted as "least = V on Z_M0" only if the solver reports a proved optimum equal to V;
#   (c) for every s asked for: the member is lifted to Z_{M0 s} by random lifts until the clauses of the statement on
#       Z_{p^n q s} hold (no new divisor), again checked by long division.
# usage: t5_cpsat.py <time limit per solve, seconds> <max M0 | min-max M0> [p q n]
import sys, os, json, time, random
from ortools.sat.python import cp_model
from core import Grp, divisors, pattern_slow
from t4_minsize import holds, find_lift

HERE = os.path.dirname(os.path.abspath(__file__))


def base_pattern(kind, p, q, n, Es, Fs):
    """the divisors d > 1 of p^n q that must / must not divide, read off the clauses with s = 1 by trying each single d"""
    M0 = p ** n * q
    need, forbid = [], []
    lv = range(1, n + 1)
    if kind == 'U':
        forbid.append(q)
    else:
        need.append(q)
    for l in lv:
        (need if l in Es else forbid).append(p ** l)
        if kind == 'A' or l in Fs:
            need.append(p ** l * q)
        else:
            forbid.append(p ** l * q)
    assert sorted(need + forbid) == [d for d in divisors(M0) if d > 1]
    assert holds(kind, p, q, n, 1, set(Es), None if Fs is None else set(Fs), set(need))
    return need, forbid


def solve(M, need, forbid, size, ub, tlimit, workers=4):
    G = Grp(M)
    m = cp_model.CpModel()
    w = [m.NewIntVar(0, ub, f"w{y}") for y in range(M)]
    m.Add(w[0] >= 1)
    tot = sum(w)
    if size is not None:
        m.Add(tot == size)
    else:
        m.Add(tot <= ub)
        m.Minimize(tot)
    for d in need + forbid:
        i = G.divs.index(d)
        cols = range(int(G.off[i]), int(G.off[i + 1]))
        forms = []
        for j in cols:
            forms.append(sum(int(G.C[y, j]) * w[y] for y in range(M) if G.C[y, j] != 0))
        if d in need:
            for f in forms:
                m.Add(f == 0)
        else:
            lits = []
            for k, f in enumerate(forms):
                bp = m.NewBoolVar(f"p{d}_{k}")
                bn = m.NewBoolVar(f"n{d}_{k}")
                m.Add(f >= 1).OnlyEnforceIf(bp)
                m.Add(f <= -1).OnlyEnforceIf(bn)
                lits += [bp, bn]
            m.AddBoolOr(lits)
    sol = cp_model.CpSolver()
    sol.parameters.max_time_in_seconds = tlimit
    sol.parameters.num_workers = workers
    st = sol.Solve(m)
    name = sol.StatusName(st)
    el = None
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        el = []
        for y in range(M):
            el += [y] * sol.Value(w[y])
    bound = int(round(sol.BestObjectiveBound())) if size is None else None
    return name, el, bound


if __name__ == '__main__':
    tlimit = float(sys.argv[1])
    minM0, maxM0 = ((int(x) for x in sys.argv[2].split('-')) if '-' in sys.argv[2] else (0, int(sys.argv[2])))
    only = tuple(int(x) for x in sys.argv[3:6]) if len(sys.argv) >= 6 else None
    inst = json.load(open(os.path.join(HERE, 't4_open.json')))
    rng = random.Random(1126)
    groups = {}
    for it in inst:
        key = (it['kind'], it['p'], it['q'], it['n'], tuple(it['Es']), None if it['Fs'] is None else tuple(it['Fs']), it['a0'], it['V'])
        groups.setdefault(key, []).append(it['s'])
    res = dict(base=0, member=0, optimal=0, notproved=0, lifts=0, liftfail=0, bad=0)
    t00 = time.time()
    for key in sorted(groups, key=lambda k: (k[1] ** k[3] * k[2], k[1], k[7], k[0], k[4], k[5] or (), k[6] or 0)):
        kind, p, q, n, Es, Fs, a0, V = key
        M0 = p ** n * q
        if M0 > maxM0 or M0 < minM0 or (only and (p, q, n) != only):
            continue
        Es_, Fs_ = set(Es), (None if Fs is None else set(Fs))
        need, forbid = base_pattern(kind, p, q, n, Es_, Fs_)
        name = f"{kind} p={p} q={q} n={n} Es={list(Es)}" + ("" if kind == 'A' else f" Fs={list(Fs)}") + (f" a0={a0}" if kind == 'B' else "")
        res['base'] += 1
        t0 = time.time()
        st, el, _ = solve(M0, need, forbid, V, V, tlimit)
        line = f"{name}: Lean {V}; "
        if el is None:
            line += f"member of size {V} on Z_{M0}: {st} (none found); "
            if st == 'INFEASIBLE':
                res['bad'] += 1
                line += "DISAGREE; "
            print(line, flush=True)
            continue
        assert len(el) == V and holds(kind, p, q, n, 1, Es_, Fs_, pattern_slow(el, M0))
        res['member'] += 1
        line += f"member on Z_{M0} found and checked [{time.time() - t0:.0f}s]; "
        t0 = time.time()
        st2, el2, bound = solve(M0, need, forbid, None, V, tlimit)
        if st2 == 'OPTIMAL' and len(el2) == V:
            res['optimal'] += 1
            line += f"least on Z_{M0} = {V} proved by the solver [{time.time() - t0:.0f}s]; "
        elif st2 == 'OPTIMAL' or (el2 is not None and len(el2) < V):
            res['bad'] += 1
            line += f"DISAGREE: a member of size {len(el2)} on Z_{M0}: {el2}; "
        else:
            res['notproved'] += 1
            line += f"least on Z_{M0} not proved in {tlimit:.0f}s (solver's lower bound {bound}); "
        ok_s, bad_s = [], []
        for s in sorted(set(groups[key])):
            if s == 1:
                continue
            G = Grp(M0 * s)
            lifted, k = find_lift(el, M0, s, G, kind, p, q, n, Es_, Fs_, rng)
            if lifted is None:
                bad_s.append(s)
                res['liftfail'] += 1
            else:
                assert len(lifted) == V
                ok_s.append(s)
                res['lifts'] += 1
        line += f"lifted with no new divisor to Z_(M0*s) for s in {ok_s}" + (f"; NO LIFT FOUND for s in {bad_s}" if bad_s else "")
        print(line, flush=True)
    print(f"TOTAL {res} [{time.time() - t00:.0f}s]")
