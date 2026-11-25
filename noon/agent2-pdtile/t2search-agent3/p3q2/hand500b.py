"""Two programmes my (T2) search left undecided at Z_500 = Z_(5^3 2^2), case (i, j) = (1, 2): 50 elements with zeros
(a) 4, 5, 25, 250   and   (b) 4, 5, 50, 125, 250.   Hand arguments, and solver checks of their steps.

Write Z_500 = Z_125 x Z_4 and let F_x be the fibre of A over x in Z_125 (a subset of Z_4), with e(x) even and o(x)
odd elements, s = e + o, h = e - o.

(a) 250 = 125 * 2 is a zero: h, as a function on Z_125, has no frequency of order 125, so h(x + 25) = h(x).
    5 and 25 are zeros: each class of x modulo 25 holds 2 elements in its five fibres; if h were not 0 there, all
    five fibres would be non-empty.  So h = 0: every fibre is empty or has one even and one odd element, and exactly
    25 fibres are non-empty.
(b) 125 is a zero: s(x + 25) = s(x).  250 is a zero: h(x + 25) = h(x).  50 = 25 * 2 is a zero: then h, already
    25-periodic, is 5-periodic.  5 is a zero: each class of x modulo 5 holds 10 elements, 2 in each set of five
    fibres x, x + 25, ...; so the five values of s over a class modulo 5 (one for each class modulo 25) add to 2, and
    if h were not 0 they would all be at least 1.  So h = 0, and again every fibre is empty or has one even and one
    odd element, and exactly 25 fibres are non-empty.
In both: 4 is a zero, so as many elements have y = 0 as y = 2.  Each of the 25 non-empty fibres has exactly one of
the two.  25 is odd.  Contradiction.  So neither set exists, whatever its other zeros.

Checks: the zeros without 4, 50 elements, plus one condition on the fibre over x = 0 that the argument excludes
(translation by multiples of 4 moves any fibre to x = 0 and keeps y).  Then the conclusion with the structure imposed.
usage: hand500b.py [seconds per programme]
"""
import os
import sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lemma_variants import residues
from ortools.sat.python import cp_model

TL = float(sys.argv[1]) if len(sys.argv) > 1 else 300.0
M = 500
F0 = {y: next(z for z in range(M) if z % 125 == 0 and z % 4 == y) for y in range(4)}      # the fibre over x = 0: y -> element


def run(name, zeros, extra, k=50):
    m = cp_model.CpModel()
    v = [m.NewBoolVar(f'x{i}') for i in range(M)]
    m.Add(sum(v) == k)
    for d in zeros:
        for row in np.asarray(residues(d, M)):
            coef = [int(round(c)) for c in row]
            m.Add(sum(c * v[i] for i, c in enumerate(coef) if c) == 0)
    extra(m, v)
    s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = TL; s.parameters.num_workers = int(os.environ.get('T2_WORKERS', '4'))
    st = s.Solve(m)
    word = {cp_model.INFEASIBLE: 'INFEASIBLE', cp_model.OPTIMAL: 'FEASIBLE', cp_model.FEASIBLE: 'FEASIBLE'}.get(st, 'undecided')
    print(f'  {name}: {word}  ({s.WallTime():.1f} s)', flush=True)
    return word


def structured(m, v):
    bs = []
    for x in range(125):
        f = {z % 4: z for z in range(M) if z % 125 == x}
        b = m.NewBoolVar(f'b{x}')
        m.Add(v[f[0]] + v[f[2]] == b)
        m.Add(v[f[1]] + v[f[3]] == b)
        bs.append(b)
    # Two redundant statements, to help a solver that is poor at parity; neither is the conclusion.  (My first version
    # also added "2 n = 25", which IS the conclusion and made the solver's verdict worthless; removed.)
    m.Add(sum(bs) == 25)                                   # 50 elements, two in each non-empty fibre
    n = m.NewIntVar(0, 125, 'n')                           # the number of elements with y = 0 ...
    m.Add(sum(v[z] for z in range(M) if z % 4 == 0) == n)
    m.Add(sum(v[z] for z in range(M) if z % 4 == 2) == n)  # ... which the zero 4 makes equal to the number with y = 2


ok = True
for tag, zeros in (('(a) zeros 5, 25, 250', (5, 25, 250)), ('(b) zeros 5, 50, 125, 250', (5, 50, 125, 250))):
    print(tag)
    res = [run('control: nothing else', zeros, lambda m, v: None)]
    even = lambda v: v[F0[0]] + v[F0[2]]
    odd = lambda v: v[F0[1]] + v[F0[3]]
    for ne, no in ((1, 0), (0, 1), (2, 0), (0, 2), (2, 1), (1, 2), (2, 2)):
        res.append(run(f'fibre over 0 has {ne} even and {no} odd', zeros, lambda m, v, ne=ne, no=no: (m.Add(even(v) == ne), m.Add(odd(v) == no))))
    res.append(run('with the zero 4 as well, and every fibre empty or one even + one odd (the count of y = 0 written as one integer)', zeros + (4,), structured))
    good = res[0] == 'FEASIBLE' and all(r == 'INFEASIBLE' for r in res[1:])
    ok = ok and good
    print('  all as the argument says' if good else '  NOT all settled')
print('BOTH SETTLED' if ok else 'SOMETHING IS NOT SETTLED')
