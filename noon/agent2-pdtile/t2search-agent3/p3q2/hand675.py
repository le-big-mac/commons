"""Programmes my (T2) search left undecided at Z_675 = Z_(3^3 5^2).  Hand arguments, and solver checks of their steps.

P = {0, 225, 450} is the subgroup of order 3, Q the subgroup of order 5, K = P + Q.  Write Z_675 = Z_27 x Z_25.

(a) 75 elements with zeros 3, 5, 25, 27, 135, 675.  (Only 3, 27, 135 and 675 are used.)
 1. 27 and 135 = 27 * 5 are zeros: the counts R_t(x) of A on Z_27 x Z_5 have, for every t, no frequency of order 27
    in x (the two zeros give all five characters of Z_5), so R_t(x + 9) = R_t(x): the counts modulo 135 are unchanged
    by adding 225.
 2. 675 is a zero, the top order: on every coset of K, a 3 x 5 array, A is a union of rows (cosets of P) or a union
    of columns (cosets of Q).  A union of columns whose column counts are equal by 1 is everything or nothing.  So on
    every coset of K the set is a union of cosets of P: A + P = A.
 3. 3 is a zero: each class modulo 3 holds 25 elements.  A coset of P lies in one class modulo 3 and has 3 elements.
    25 is not a multiple of 3.  Contradiction.
So no set of 75 elements of Z_675 has the zeros 3, 27, 135 and 675.

(b) 25 elements with zeros 5, 27, 75, 225.   Let F_y be the fibre over y in Z_25, a subset of Z_27.
 1. 75 = 3 * 25 and 225 = 9 * 25 are zeros: for the characters of order 3 and of order 9 of Z_27 the transform of
    F_y, as a function of y, has no frequency of order 25, so it is unchanged by y -> y + 5.  For order 3 this says:
    the counts of F_y modulo 3 change, from y to y + 5, by the same amount in all three classes; so the sizes of the
    five fibres over a class of y modulo 5 are congruent modulo 3.
 2. 5 is a zero: those five sizes add to 5.  Congruent modulo 3 and adding to 5, they are 1, 1, 1, 1, 1.  So every
    fibre has exactly one element, x(y); by 1 for order 3, x(y) mod 3 is the same for the five y of a class, and
    then by 1 for order 9, x(y) mod 9 is the same (a difference of two unit vectors on a class modulo 3 that is
    constant on that class is zero).
 3. 27 is a zero: for each residue s modulo 9 the three values x = s, s + 9, s + 18 are taken equally often.  They
    are taken, together, by 5 m values of y, where m is the number of classes modulo 5 with that residue.  So 3
    divides every m; but the m add up to 5.  Contradiction.
So no set of 25 elements of Z_675 has the zeros 5, 27, 75 and 225.

(c) From the (T1) search: 15 elements whose prime-power zeros are exactly {5}, with the zeros 5 and 225.
    Claim: 15 elements with the zeros 5 and 225 always have the zero 9 as well, so no such set exists.
 1. 225 = 9 * 25 is a zero: for the characters of order 9 of Z_27 the transform of F_y is unchanged by y -> y + 5,
    that is, the counts of F_y modulo 9 change, from y to y + 5, by amounts that depend only on the class modulo 3.
 2. 5 is a zero: the five fibres over a class of y modulo 5 hold 3 elements, so at least two of them are empty, and by
    1 every fibre has counts modulo 9 that are constant on the classes modulo 3: it holds 0 elements, or 3 that are
    congruent modulo 3 and different modulo 9.
 3. Adding up over the fibres, the counts of A modulo 9 are constant on the classes modulo 3: 9 is a zero.

(d) From the (T1) search: 45 elements whose prime-power zeros are exactly {3, 5}, with the zeros 3, 5, 45, 75, 675.
    Claim: 45 elements with the zeros 5 and 675 always have the zero 27 as well, so no such set exists.
 1. 675 is a zero, the top order: on every coset of K the set is a union of cosets of P (3 points, at one y) or a
    union of cosets of Q (5 points, at one x).
 2. 5 is a zero: each class of y modulo 5 holds 9 elements.  A class is nine cosets of K, and its 9 elements are 3 a
    + 5 b for a cosets of P and b cosets of Q; so b = 0.  Hence A is a union of cosets of P: A + P = A.
 3. A character of order 27 is not trivial on P, so it sums to zero over A: 27 is a zero.

usage: hand675.py [seconds per programme]
"""
import os
import sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lemma_variants import residues
from ortools.sat.python import cp_model

TL = float(sys.argv[1]) if len(sys.argv) > 1 else 300.0
M = 675


def run(name, zeros, extra, k):
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


def p_invariant(m, v):
    for x in range(225):
        m.Add(v[x] == v[x + 225]); m.Add(v[x] == v[x + 450])


print('(a) 75 elements, zeros 27, 135, 675 (and then 3)')
res = [run('control: zeros 27, 135, 675, nothing else', (27, 135, 675), lambda m, v: None, 75)]
res.append(run('0 in A and 225 not in A (A is not a union of cosets of P)', (27, 135, 675), lambda m, v: (m.Add(v[0] == 1), m.Add(v[225] == 0)), 75))
res.append(run('zeros 3, 27, 135, 675 with A + P = A imposed (step 3)', (3, 27, 135, 675), p_invariant, 75))
ok = res[0] == 'FEASIBLE' and all(r == 'INFEASIBLE' for r in res[1:])
print('  all as the argument says' if ok else '  NOT all settled')


fib = lambda y: [z for z in range(M) if z % 25 == y]
print('(b) 25 elements, zeros 5, 75, 225 (and then 27)')
Z = (5, 75, 225)
res = [run('control: zeros 5, 75, 225, nothing else', Z, lambda m, v: None, 25)]
res.append(run('the fibre over y = 0 is empty', Z, lambda m, v: m.Add(sum(v[z] for z in fib(0)) == 0), 25))
res.append(run('the fibre over y = 0 has two or more elements', Z, lambda m, v: m.Add(sum(v[z] for z in fib(0)) >= 2), 25))
# x(0) is 0 mod 9 (a translation in x arranges it) and x(5) is not
res.append(run('x(0) = 0 mod 9 and x(5) is not 0 mod 9', Z, lambda m, v: (m.Add(sum(v[z] for z in fib(0) if z % 27 % 9 == 0) == 1),
                                                                        m.Add(sum(v[z] for z in fib(5) if z % 27 % 9 == 0) == 0)), 25))
def structure(m, v):
    # The structure of step 2, written with named counts so that a solver that is poor at divisibility can use them.
    # g[t][r] = 1 if x(y) = r mod 9 on the class t of y mod 5; mm[r] = number of classes with residue r; bb[r] = how
    # often x = r is taken, which the zero 27 (imposed separately, through its residues) makes equal for r, r + 9, r + 18.
    # None of these lines is the conclusion (which is: 3 bb[r] = 5 mm[r] for every r, and the mm add to 5).
    g = [[m.NewBoolVar(f'g{t}_{r}') for r in range(9)] for t in range(5)]
    for t in range(5):
        m.Add(sum(g[t]) == 1)
        for y in range(t, 25, 5):
            for r in range(9):
                m.Add(sum(v[z] for z in fib(y) if z % 27 % 9 == r) == g[t][r])
    mm = [m.NewIntVar(0, 5, f'm{r}') for r in range(9)]
    bb = [m.NewIntVar(0, 25, f'b{r}') for r in range(9)]
    for r in range(9):
        m.Add(sum(g[t][r] for t in range(5)) == mm[r])
        for x in (r, r + 9, r + 18):
            m.Add(sum(v[z] for z in range(M) if z % 27 == x) == bb[r])
# Step 3 uses only the structure of step 2 and the zero 27, so it is checked in that form.  (With the residue conditions
# of 5, 75 and 225 left in as well, which the structure already implies, the solver did not finish in 300 s.)
res.append(run('the zero 27 with one element per fibre and x(y) mod 9 constant on classes of y mod 5 (step 3)', (27,), structure, 25))
okb = res[0] == 'FEASIBLE' and all(r == 'INFEASIBLE' for r in res[1:])
print('  all as the argument says' if okb else '  NOT all settled')
print('(c) 15 elements, zeros 5, 225; the zero 9 follows')
Zc = (5, 225)
f0 = fib(0)
r9 = lambda v, r: sum(v[z] for z in f0 if z % 27 % 9 == r)
res = [run('control: zeros 5, 225, nothing else', Zc, lambda m, v: None, 15)]
res.append(run('the fibre over y = 0 has one element', Zc, lambda m, v: m.Add(sum(v[z] for z in f0) == 1), 15))
res.append(run('the fibre over y = 0 has two elements', Zc, lambda m, v: m.Add(sum(v[z] for z in f0) == 2), 15))
res.append(run('the fibre over y = 0 has four or more elements', Zc, lambda m, v: m.Add(sum(v[z] for z in f0) >= 4), 15))
res.append(run('the fibre over y = 0 has two elements that are 0 mod 9', Zc, lambda m, v: m.Add(r9(v, 0) >= 2), 15))
res.append(run('the fibre over y = 0 has an element 0 mod 9 and none 3 mod 9', Zc, lambda m, v: (m.Add(r9(v, 0) >= 1), m.Add(r9(v, 3) == 0)), 15))
# 9 is not a zero: some two residues modulo 9 in one class modulo 3 are taken unequally often; by a translation in x
# and the reflection x -> -x (both keep the zeros) they may be taken to be 0 and 3, with 0 the commoner
n9 = lambda v, r: sum(v[z] for z in range(M) if z % 27 % 9 == r)
res.append(run('more elements are 0 mod 9 than 3 mod 9 (so 9 is not a zero)', Zc, lambda m, v: m.Add(n9(v, 0) >= n9(v, 3) + 1), 15))
okc = res[0] == 'FEASIBLE' and all(r == 'INFEASIBLE' for r in res[1:])
print('  all as the argument says' if okc else '  NOT all settled')
print('(d) 45 elements, zeros 5, 675; the zero 27 follows')
Zd = (5, 675)
res = [run('control: zeros 5, 675, nothing else', Zd, lambda m, v: None, 45)]
res.append(run('0 in A and 225 not in A (A is not a union of cosets of P)', Zd, lambda m, v: (m.Add(v[0] == 1), m.Add(v[225] == 0)), 45))
# 27 is not a zero: two values of x that differ by a multiple of 9 are taken unequally often; by a translation in x and
# the reflection x -> -x they may be taken to be 0 and 9, with 0 the commoner
n27 = lambda v, x: sum(v[z] for z in range(M) if z % 27 == x)
res.append(run('x = 0 is taken more often than x = 9 (so 27 is not a zero)', Zd, lambda m, v: m.Add(n27(v, 0) >= n27(v, 9) + 1), 45))
okd = res[0] == 'FEASIBLE' and all(r == 'INFEASIBLE' for r in res[1:])
print('  all as the argument says' if okd else '  NOT all settled')
print('ALL FOUR SETTLED' if ok and okb and okc and okd else 'SOMETHING IS NOT SETTLED')
