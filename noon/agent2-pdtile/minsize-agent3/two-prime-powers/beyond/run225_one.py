"""One pattern of Z_225, the same call as run225.py.   usage: run225_one.py KEY tlimit     (KEY as in predictions-225.json, e.g. 3,45)"""
import sys, json, time
sys.path.insert(0, '/home/agent3/pq2/referee/two-powers')
from milp import least
from sympy import Poly, cyclotomic_poly, symbols, ZZ
X = symbols('X'); M = 225
key, tl = sys.argv[1], float(sys.argv[2])
dv = [d for d in range(2, M + 1) if M % d == 0]
PHI = {d: Poly(cyclotomic_poly(d, X), X, domain=ZZ) for d in dv}
def exact_pattern(v):
    A = Poly(sum(int(w) * X**i for i, w in enumerate(v)), X, domain=ZZ)
    return [d for d in dv if A.rem(PHI[d]).is_zero]
o = json.load(open('/home/agent3/pq2/rule/predictions-225.json'))[key]
D = [int(t) for t in key.split(',') if t]
ub = o['predicted'] if o['predicted'] is not None else 2 * M
t0 = time.time()
st, sz, v = least(M, D, [d for d in dv if d not in D] or [1], ub=ub, solver='highs', tlimit=tl)
ok = None
if v is not None: ok = (exact_pattern(v) == sorted(D)) and sum(v) == sz and min(v) >= 0
print(json.dumps(dict(M=M, D=D, cls=o['cls'], predicted=o['predicted'], upper_bound_given=ub, status=st, size=sz, exact_pattern_ok=ok,
                      multiset=' '.join(f'{a}^{c}' if c > 1 else str(a) for a, c in enumerate(v) if c) if v is not None else None, seconds=round(time.time() - t0, 1))), flush=True)
