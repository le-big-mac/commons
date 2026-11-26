"""The patterns of Z_100 (or Z_36) on which the referee's programme (referee/two-powers/milp.py: cuboid forms, HiGHS) either found
a smaller multiset than my solver's or did not finish in 60 seconds: run again with that programme and a longer limit, and
this time keep the multiset.  Each multiset returned is checked here by exact division of polynomials (my own check, sympy).
usage: finish100.py M K J tlimit which        which = smaller | undecided
(patterns number J mod K of the chosen list; output: one JSON line for each)"""
import sys, json, glob, time
sys.path.insert(0, '/home/agent3/pq2/referee/two-powers')
from milp import least
from sympy import Poly, cyclotomic_poly, symbols, ZZ
X = symbols('X')
M, K, J, tl, which = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]), sys.argv[5]
dv = [d for d in range(2, M + 1) if M % d == 0]
PHI = {d: Poly(cyclotomic_poly(d, X), X, domain=ZZ) for d in dv}
def exact_pattern(v):
    A = Poly(sum(int(w) * X**i for i, w in enumerate(v)), X, domain=ZZ)
    return [d for d in dv if A.rem(PHI[d]).is_zero]
R = {}
for f in sorted(glob.glob(f'/home/agent3/pq2/referee/two-powers/out/retable-{M}-*.jsonl')):
    for l in open(f):
        if l.startswith('{'):
            r = json.loads(l); R[tuple(r['D'])] = r
if which == 'smaller': todo = [D for D, r in R.items() if r['referee_status'] == 'optimal' and r['referee_least'] != r['author_min']]
else: todo = [D for D, r in R.items() if r['referee_status'] != 'optimal']
todo.sort(key=lambda D: (len(D), D))
for i, D in enumerate(todo):
    if i % K != J: continue
    r = R[D]
    cands = [t for t in (r['author_min'], r['referee_least']) if t is not None]
    ub = min(cands) if cands else 2 * M
    t0 = time.time()
    st, sz, v = least(M, list(D), [d for d in dv if d not in D] or [1], ub=ub, solver='highs', tlimit=tl)
    ok = None
    if v is not None:
        ok = (exact_pattern(v) == sorted(D)) and sum(v) == sz and min(v) >= 0
    print(json.dumps(dict(M=M, D=list(D), upper_bound_given=ub, status=st, size=sz, exact_pattern_ok=ok, A=v, seconds=round(time.time() - t0, 1))), flush=True)
