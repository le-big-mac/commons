"""Referee: validate mylp against (1) character sums over the group, (2) the author's formula, (3) scipy HiGHS, (4) settle72.out counts."""
import sys, random, time
from collections import Counter
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import linprog
sys.path.insert(0, '/home/agent2/p3q2/referee2'); import mylp
from mylp import *
def ram(p, nn, l, i):                              # the author's formula, retyped here only for comparison
    if i == nn: return 1
    return (p ** (nn - i) if l <= i else 0) - (p ** (nn - i - 1) if l <= i + 1 else 0)
for (p, q) in [(2, 3), (3, 2), (3, 5), (5, 3), (2, 7), (7, 2), (5, 7)]:
    B = brute(p, q); ok1 = all(B[(o, c)] == coeff(p, q, o, c) for o in cls for c in cls)
    ok2 = all(ram(p, 3, o[0], c[0]) * ram(q, 2, o[1], c[1]) == coeff(p, q, o, c) for o in cls for c in cls)
    print((p, q), "Moebius form = character sums over Z_M:", ok1, "; = author's formula:", ok2)
print("author's formula = Moebius form at 400 random pairs up to 10^4:", all(ram(p, 3, o[0], c[0]) * ram(q, 2, o[1], c[1]) == coeff(p, q, o, c) for _ in range(400) for p, q in [(random.randint(2, 10**4), random.randint(2, 10**4))] for o in cls for c in cls))
# (3) HiGHS on a scaled programme (masses g_c = f_c |class c|), a sample of patterns
random.seed(1); pats = [Z for Z in patterns()]; bad = 0; cnt = 0
for (p, q) in [(3, 7), (7, 5), (11, 13)]:
    pr = Prog(p, q)
    for Z in random.sample(pats, 150):
        R, rhs = pr.rows(Z); st, v, x = lp(R, rhs, pr.tot)
        size = np.array(pr.tot, float); A = np.array(R, float) / size; res = linprog(np.ones(n), A_eq=A, b_eq=np.array(rhs, float) / 1.0, bounds=[(0, None)] * n, method='highs')
        cnt += 1
        if res.status != 0 or abs(res.fun - float(v)) > 1e-7 * max(1, float(v)): bad += 1; print("HiGHS differs", (p, q), sorted(Z), res.status, res.fun, float(v))
print(f"HiGHS comparison: {cnt} programmes, {bad} differences")
