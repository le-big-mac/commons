"""A programme my (T2) search left undecided at Z_500 = Z_(5^3 2^2): size 50 with zeros 2, 5, 25, 500.  A hand
argument, and solver checks of its steps.

P = {0, 100, 200, 300, 400} and Q = {0, 250} are the subgroups of order 5 and 2, K = P + Q.
 1. 500 is a zero, the top order: on every coset of K, a 5 x 2 array, A is a union of rows (cosets of P, 5 points) or a
    union of columns (cosets of Q, 2 points).  [The lines lemma: the sums A(c) - A(c + 100) - A(c + 250) + A(c + 350)
    vanish, and a 0/1 array with that property is a union of rows or of columns.]
 2. 5 and 25 are zeros: every class modulo 25 holds 50 / 25 = 2 elements.  A class modulo 25 is two cosets of K, and
    a union of rows or columns has 0, 2, 4, 5, ... points; so the 2 elements are one coset of Q.  Hence A + Q = A:
    A is 25 pairs {x, x + 250}.
 3. 250 is even, so each pair lies in one class modulo 2.  2 is a zero: 25 elements are even and 25 odd, which would
    take 12.5 pairs each.  Contradiction.
So no set of 50 elements of Z_500 has the zeros 2, 5, 25 and 500.

A second programme, undecided at 300 s (decided at 600 s in an earlier run): 50 elements with zeros 2, 5, 100, 125, 500.
Write Z_500 = Z_125 x Z_4, F_x the fibre over x, s(x) its size.
 1'. 125 is a zero: s(x + 25) = s(x).  5 is a zero: each class of x modulo 5 holds 10 elements, so the five values of
     s over it (one for each class modulo 25) add to 2: one class modulo 25 with fibres of 2, or two with fibres of 1.
 2'. 500 is a zero (lines, as in 1 above).  A fibre with a single element is not a column, so it lies in a full row:
     a class modulo 25 with fibres of 1 is one coset of P, at one height y0.
 3'. 100 = 25 * 4 is a zero: with g(x) = sum of i^y over the fibre, the sums D(c) of g over the classes c modulo 25
     depend only on c modulo 5.  A coset of P at height y0 has D = 5 i^y0, an empty class has D = 0, and a class
     modulo 5 holding two cosets of P also holds three empty classes modulo 25.  So there are no fibres of 1; and
     where the fibres have 2 elements D must be 0 as well, which excludes one even and one odd element.  [The step
     filled in by Noon, who read this file at 07:35 UTC on 21 November: if a fibre holds one even and one odd element,
     neither lies in a column, since a column through either would put a third element in the fibre; so by the lines
     both lie in full rows, all five fibres over that class modulo 25 are that same pair, and D = 5 (i^a + i^b) is not
     0.  Without the rows a class could mix fibres whose sums cancel.]  So every non-empty fibre is a coset of Q:
     A + Q = A.
 4'. As in 3 above: 25 pairs {x, x + 250}, each in one class modulo 2, cannot give 25 even and 25 odd elements.

Checks: zeros 5, 25, 500 and 50 elements (NOT the zero 2), plus a condition step 2 excludes.  By translation the
condition may be put at 0.
usage: hand500.py [seconds per programme]
"""
import os
import sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lemma_variants import residues
from ortools.sat.python import cp_model

TL = float(sys.argv[1]) if len(sys.argv) > 1 else 300.0
M = 500


def run(name, extra, zeros=(5, 25, 500), k=50):
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
    print(f'{name}: {word}  ({s.WallTime():.1f} s)', flush=True)
    if word == 'FEASIBLE':
        print('   set:', [i for i in range(M) if s.Value(v[i])])
    return word


def pairs(m, v):
    for x in range(250):
        m.Add(v[x] == v[x + 250])


ok = True
for zs in ((5, 25, 500), (5, 100, 125, 500)):
    name = ', '.join(str(z) for z in zs)
    res = [run(f'control: zeros {name}, 50 elements, nothing else', lambda m, v: None, zeros=zs)]
    res.append(run(f'zeros {name}; 0 in A and 250 not in A (A is not a union of cosets of Q)', lambda m, v: (m.Add(v[0] == 1), m.Add(v[250] == 0)), zeros=zs))
    res.append(run(f'zeros 2, {name} with A + Q = A imposed (the last step)', pairs, zeros=(2,) + zs))
    good = res[0] == 'FEASIBLE' and all(r == 'INFEASIBLE' for r in res[1:])
    ok = ok and good
    print('  all as the argument says' if good else '  NOT all settled')
print('BOTH SETTLED' if ok else 'SOMETHING IS NOT SETTLED')
