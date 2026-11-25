"""The one programme my (T2) search left undecided at Z_392: size 28 with zeros 7, 8, 98, 196.  A hand argument, and
solver checks of each of its steps.

Write Z_392 = Z_8 x Z_49 and let F_y be the fibre of A over y in Z_49 (a subset of Z_8), c_j(y) the number of its
elements congruent to j mod 4.
 1. The zeros 98 = 2*49 and 196 = 4*49 say: for the character of order 2 and those of order 4 of Z_8, the transform
    of F_y, as a function of y, has no frequency of order 49; so it is unchanged by y -> y + 7.  Hence
    (c0 + c2) - (c1 + c3),  c0 - c2  and  c1 - c3  depend only on y mod 7.
 2. The zero 7 says: the seven fibres over a class of y mod 7 hold 4 elements together.  So at least three of them
    are empty, and by 1 all seven have c0 = c2, c1 = c3 and c0 + c2 = c1 + c3: every fibre has 4c elements, c in
    each class mod 4.  So over each class mod 7 exactly one fibre is non-empty, with one element in each class mod 4.
 3. There are then exactly 7 non-empty fibres, each holding exactly one of j, j + 4 for each j.  The zero 8 says the
    number of elements with first coordinate j equals the number with j + 4.  Their sum is 7.  Contradiction.
So no set of 28 elements of Z_392 has the zeros 7, 8, 98 and 196, whatever its other zeros.

Checks below, each a 0/1 programme with zeros 7, 98, 196 and 28 elements (NOT the zero 8) plus one extra condition
that step 2 says is impossible.  Translations in y and in x preserve the zeros, so the extra condition may be put on
the fibre over y = 0 and on the class j = 0.
usage: hand392.py [seconds per programme]
"""
import os
import sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lemma_variants import residues
from ortools.sat.python import cp_model

TL = float(sys.argv[1]) if len(sys.argv) > 1 else 300.0
M = 392
# x in Z_392 <-> (x mod 8, x mod 49)
fib0 = [x for x in range(M) if x % 49 == 0]                       # the fibre over y = 0: eight elements, one per residue mod 8


def run(name, extra, zeros=(7, 98, 196)):
    m = cp_model.CpModel()
    v = [m.NewBoolVar(f'x{i}') for i in range(M)]
    m.Add(sum(v) == 28)
    for d in zeros:
        Rm = residues(d, M)
        for row in np.asarray(Rm):
            coef = [int(round(c)) for c in row]
            m.Add(sum(c * v[i] for i, c in enumerate(coef) if c) == 0)
    extra(m, v)
    s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = TL; s.parameters.num_workers = int(os.environ.get('T2_WORKERS', '4'))
    st = s.Solve(m)
    word = {cp_model.INFEASIBLE: 'INFEASIBLE', cp_model.OPTIMAL: 'FEASIBLE', cp_model.FEASIBLE: 'FEASIBLE'}.get(st, 'undecided')
    print(f'{name}: {word}  ({s.WallTime():.1f} s)', flush=True)
    if word == 'FEASIBLE':
        A = [i for i in range(M) if s.Value(v[i])]
        print('   set:', A)
    return word


size0 = lambda v: sum(v[x] for x in fib0)
cls0 = lambda v, j: sum(v[x] for x in fib0 if x % 4 == j)
res = []
res.append(run('control: zeros 7, 98, 196, 28 elements, nothing else', lambda m, v: None))
for k in (1, 2, 3, 5, 6, 7, 8):
    res.append(run(f'fibre over 0 has {k} elements', lambda m, v, k=k: m.Add(size0(v) == k)))
res.append(run('fibre over 0 has 4 elements and none congruent to 0 mod 4', lambda m, v: (m.Add(size0(v) == 4), m.Add(cls0(v, 0) == 0))))
res.append(run('fibre over 0 has 4 elements and two congruent to 0 mod 4', lambda m, v: (m.Add(size0(v) == 4), m.Add(cls0(v, 0) == 2))))
# and the conclusion itself with the structure of step 2 imposed, which the solver should now refute at once
def structured(m, v):
    for y in range(49):
        f = [x for x in range(M) if x % 49 == y]
        b = m.NewBoolVar(f'b{y}')
        for j in range(4):
            m.Add(sum(v[x] for x in f if x % 4 == j) == b)
res.append(run('zeros 7, 8, 98, 196 with every fibre empty or one-per-class (step 3)', structured, zeros=(7, 8, 98, 196)))
print('all as the argument says' if res[0] == 'FEASIBLE' and all(r == 'INFEASIBLE' for r in res[1:]) else 'NOT all settled')
