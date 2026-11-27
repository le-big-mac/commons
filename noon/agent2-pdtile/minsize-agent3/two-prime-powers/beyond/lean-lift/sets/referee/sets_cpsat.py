"""Corollary 21 and the remark after it, by a complete solver (CP-SAT, exact integers), with a model of my own:
one 0/1 variable per element of Z_L (or 0..cap for multisets); for each divisor d > 1 of L the remainder of the mask
modulo Phi_d is the integer vector  sum_y x_y * REM_d[y mod d]  (cyc.rem_table);  d in D: every coordinate is 0;
d not in D: some coordinate is >= 1 or <= -1.  Every answer 'found' is checked again by exact division (cyc.pattern).

modes
  sets L p q n TLIM [min]   for every pattern D of Z_{p^n q} (p^n q | L): is there a SET on Z_L with exactly m elements
                            (m = Theorem 1) whose pattern among the divisors > 1 of L is exactly D?  with 'min': also the
                            least size of such a set, by minimisation (a proof only if the solver ends OPTIMAL).
  cap p q n CAP TLIM        for every pattern D of Z_{p^n q}: is there a multiset with m elements, exactly the pattern D
                            and every multiplicity <= CAP?"""
import sys, time
from ortools.sat.python import cp_model
from cyc import divisors, rem_table, pattern
from thm import theorem_m, D_of, all_patterns


def build(L, D, cap, size=None, minimise=False):
    m = cp_model.CpModel()
    x = [m.NewIntVar(0, cap, f'x{y}') for y in range(L)]
    m.Add(x[0] >= 1)
    for d in divisors(L):
        if d == 1:
            continue
        T = rem_table(d)
        deg = len(T[0])
        # group the variables by residue modulo d
        cls = [sum(x[y] for y in range(c, L, d)) for c in range(d)]
        exprs = [sum(T[c][i] * cls[c] for c in range(d) if T[c][i]) for i in range(deg)]
        if d in D:
            for e in exprs:
                m.Add(e == 0)
        else:
            lits = []
            for i, e in enumerate(exprs):
                bp = m.NewBoolVar(f'p{d}_{i}')
                bn = m.NewBoolVar(f'n{d}_{i}')
                m.Add(e >= 1).OnlyEnforceIf(bp)
                m.Add(e <= -1).OnlyEnforceIf(bn)
                lits += [bp, bn]
            m.AddBoolOr(lits)
    if size is not None:
        m.Add(sum(x) == size)
    if minimise:
        m.Minimize(sum(x))
    return m, x


def solve(L, D, cap, size=None, minimise=False, tlim=60.0, workers=2):
    m, x = build(L, D, cap, size, minimise)
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = tlim
    s.parameters.num_search_workers = workers
    st = s.Solve(m)
    name = s.StatusName(st)
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        mult = {y: s.Value(v) for y, v in enumerate(x) if s.Value(v)}
        assert pattern(mult, L) == frozenset(D), 'solver answer fails the exact check'
        assert max(mult.values()) <= cap and (size is None or sum(mult.values()) == size)
        return name, mult
    return name, None


def fmt(mult):
    return ' '.join(f'{y}' if w == 1 else f'{y}^{w}' for y, w in sorted(mult.items()))


if __name__ == '__main__':
    mode = sys.argv[1]
    t0 = time.time()
    if mode == 'sets':
        L, p, q, n, tlim = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), float(sys.argv[6])
        domin = len(sys.argv) > 7 and sys.argv[7] == 'min'
        M = p ** n * q
        assert L % M == 0
        s_ = L // M
        found = nofound = und = 0
        minok = minund = minbad = 0
        lines = []
        for E, F, bal in all_patterns(p, q, n):
            mm = theorem_m(p, q, n, E, F, bal)
            D = D_of(p, q, n, E, F, bal)
            if mm > L:
                nofound += 1
                lines.append(f'  m = {mm} > {L}: no set can have m elements: D = {sorted(D)}')
                continue
            st, mult = solve(L, D, 1, size=mm, tlim=tlim)
            if mult is not None:
                found += 1
                lines.append(f'  D = {sorted(D)} m = {mm}: set {fmt(mult)}')
            elif st == 'INFEASIBLE':
                nofound += 1
                lines.append(f'  NO SET of m = {mm} elements (solver: infeasible): D = {sorted(D)}')
            else:
                und += 1
                lines.append(f'  undecided in {tlim:.0f} s: D = {sorted(D)} m = {mm}')
            if domin:
                st2, mult2 = solve(L, D, 1, minimise=True, tlim=tlim)
                if st2 == 'OPTIMAL':
                    v = sum(mult2.values())
                    if v == mm: minok += 1
                    else:
                        minbad += 1
                        lines.append(f'    least set by minimisation: {v} (m = {mm}) D = {sorted(D)}')
                elif st2 == 'INFEASIBLE':
                    lines.append(f'    minimisation: no set at all with this pattern: D = {sorted(D)}')
                else:
                    minund += 1
        print(f'Z_{L} = Z_({p}^{n}*{q}) * {s_}: patterns of Z_{M}: {2 ** (2 * n + 1)}; a SET of exactly m elements with pattern exactly D '
              f'among the divisors of {L}: found (and checked by exact division) for {found}; none exists for {nofound}; '
              f'undecided in {tlim:.0f} s: {und}' +
              (f'; least set size by minimisation, proved by the solver: equal to m for {minok}, different for {minbad}, not proved in time for {minund}' if domin else '') +
              f'   [{time.time() - t0:.0f} s]')
        for l in lines:
            print(l)
    elif mode == 'cap':
        p, q, n, cap, tlim = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), float(sys.argv[6])
        M = p ** n * q
        found = no = und = 0
        lines = []
        for E, F, bal in all_patterns(p, q, n):
            mm = theorem_m(p, q, n, E, F, bal)
            D = D_of(p, q, n, E, F, bal)
            st, mult = solve(M, D, cap, size=mm, tlim=tlim)
            if mult is not None:
                found += 1
            elif st == 'INFEASIBLE':
                no += 1
                lines.append(f'  NONE with multiplicities <= {cap} (solver: infeasible): E={E} F={F} balanced={bal} m={mm}')
            else:
                und += 1
                lines.append(f'  undecided in {tlim:.0f} s: E={E} F={F} balanced={bal} m={mm}')
        print(f'Z_{M} (p={p}, q={q}, n={n}): patterns {2 ** (2 * n + 1)}; a multiset of m elements with exactly the pattern and every '
              f'multiplicity <= {cap}: found (checked by exact division) for {found}; none for {no}; undecided in {tlim:.0f} s: {und}'
              f'   [{time.time() - t0:.0f} s]')
        for l in lines:
            print(l)
