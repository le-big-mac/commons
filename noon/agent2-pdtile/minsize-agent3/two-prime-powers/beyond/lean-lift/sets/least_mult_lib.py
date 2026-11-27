"""functions of least_mult.py (the part above its main loop)"""
import sys, json, collections
sys.path.insert(0, '/home/agent3/minsize')
from minsize import forms_B
from ortools.sat.python import cp_model
from sympy import Poly, cyclotomic_poly, symbols, ZZ
X = symbols('X')
def feasible(p, q, n, E, F, s, cap, tlimit):
    M = p ** n * q; m = cp_model.CpModel()
    x = [m.NewIntVar(0, cap, f'x{i}') for i in range(M)]
    m.Add(sum(x) == s); m.Add(x[0] >= 1)
    for kind, rng, S in (('P', range(1, n + 1), E), ('Q', range(0, n + 1), F)):
        for a in rng:
            fs = forms_B(p, q, n, kind, a)
            if a in S:
                for v in fs: m.Add(sum(int(c) * x[i] for i, c in enumerate(v) if c) == 0)
            else:
                bs = []
                for k, v in enumerate(fs):
                    expr = sum(int(c) * x[i] for i, c in enumerate(v) if c)
                    bp = m.NewBoolVar(f'{kind}{a}p{k}'); bn = m.NewBoolVar(f'{kind}{a}n{k}')
                    m.Add(expr >= 1).OnlyEnforceIf(bp); m.Add(expr <= -1).OnlyEnforceIf(bn); bs += [bp, bn]
                m.AddBoolOr(bs)
    sol = cp_model.CpSolver(); sol.parameters.max_time_in_seconds = tlimit; sol.parameters.num_search_workers = 2
    st = sol.Solve(m)
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE): return True, [sol.Value(v) for v in x]
    return (False, None) if st == cp_model.INFEASIBLE else (None, None)
def exact(p, q, n, x):
    M = p ** n * q; A = Poly(sum(w * X**i for i, w in enumerate(x) if w), X, domain=ZZ)
    dv = lambda d: A.rem(Poly(cyclotomic_poly(d, X), X, domain=ZZ)).is_zero
    return [a for a in range(1, n + 1) if dv(p ** a)], [a for a in range(0, n + 1) if dv(p ** a * q)]
