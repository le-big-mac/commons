"""For Z_225 (p = 3, q = 5): the lower bound LB (lowerbound.py) and the upper bound U (algebra.py) for every pattern, and how they sit
against the two theorems where a theorem gives the value.  Uses nothing of the Z_225 run.   usage: bounds225.py"""
import json, sys
sys.path.insert(0, '/home/agent3/pq2/rule')
from lowerbound import LB
from algebra import closure, expr
P = json.load(open('predictions-225.json'))
for (p, q) in ((2, 3), (3, 2), (2, 5), (5, 2), (3, 5), (5, 3)):
    divs, mask, U, how = closure(p, q)
    n_th = eq = 0; n_sand = 0; diff = []
    for key, o in P.items():
        S = [tuple(t) for t in o['S']]; D = [p ** u * q ** v for u, v in S]
        u_ = U[mask(D)]; lb, _ = LB(D, p, q)
        if lb == u_: n_sand += 1
        if o['cls'].startswith('theorem'):
            n_th += 1
            # the theorem's value at (p, q): for these patterns LB already contains it (restriction or corner sum), so compare U with LB
            if u_ == lb: eq += 1
            else: diff.append((' '.join(f'{a}{b}' for a, b in S), lb, u_))
    print(f'(p, q) = ({p}, {q}): LB = U for {n_sand} of 256 patterns; among the {n_th} theorem patterns U equals the theorem value for {eq}; others (pattern, theorem, U): {diff}')
divs, mask, U, how = closure(3, 5)
out = {}
for key, o in P.items():
    D = [int(t) for t in key.split(',') if t]; lb, parts = LB(D, 3, 5)
    out[key] = dict(S=o['S'], LB=lb, U=U[mask(D)], expression=expr(mask(D), how, divs))
json.dump(out, open('bounds-225.json', 'w'), indent=0)
print('agreement of U with the fit predictions of predictions-225.json:', sum(1 for k, o in P.items() if o['cls'] == 'fit' and o['predicted'] == out[k]['U']), 'of', sum(1 for o in P.values() if o['cls'] == 'fit'))
print('   fit patterns where U differs from the fit prediction:', [(' '.join(f'{a}{b}' for a, b in o['S']), o['predicted'], out[k]['U'], out[k]['LB']) for k, o in P.items() if o['cls'] == 'fit' and o['predicted'] != out[k]['U']])
print('   LB = U at (3,5):', sum(1 for o in out.values() if o['LB'] == o['U']))
