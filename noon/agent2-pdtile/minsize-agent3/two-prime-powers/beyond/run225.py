"""Z_225 = 3^2 5^2: the least size of a multiset with exactly a given pattern, with the referee's programme (cuboid forms, HiGHS).
The size is bounded above by the sheet's prediction where there is one (so 'infeasible' means: the least size is larger than
predicted, or no multiset at all), and by 2M = 450 otherwise.  Each multiset returned is checked by exact division (sympy).
usage: run225.py K J tlimit     (patterns number J mod K, in the order of predictions-225.json)"""
import sys, json, time
sys.path.insert(0, '/home/agent3/pq2/referee/two-powers')
from milp import least
from sympy import Poly, cyclotomic_poly, symbols, ZZ
X = symbols('X'); M = 225
K, J, tl = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3])
dv = [d for d in range(2, M + 1) if M % d == 0]
PHI = {d: Poly(cyclotomic_poly(d, X), X, domain=ZZ) for d in dv}
def exact_pattern(v):
    A = Poly(sum(int(w) * X**i for i, w in enumerate(v)), X, domain=ZZ)
    return [d for d in dv if A.rem(PHI[d]).is_zero]
P = json.load(open('/home/agent3/pq2/rule/predictions-225.json'))
for i, (key, o) in enumerate(P.items()):
    if i % K != J: continue
    D = [int(t) for t in key.split(',') if t]
    ub = o['predicted'] if o['predicted'] is not None else 2 * M
    t0 = time.time()
    st, sz, v = least(M, D, [d for d in dv if d not in D] or [1], ub=ub, solver='highs', tlimit=tl)
    ok = None
    if v is not None: ok = (exact_pattern(v) == sorted(D)) and sum(v) == sz and min(v) >= 0
    print(json.dumps(dict(M=M, D=D, cls=o['cls'], predicted=o['predicted'], upper_bound_given=ub, status=st, size=sz, exact_pattern_ok=ok,
                          multiset=' '.join(f'{a}^{c}' if c > 1 else str(a) for a, c in enumerate(v) if c) if v is not None else None, seconds=round(time.time() - t0, 1))), flush=True)
