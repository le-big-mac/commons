"""The three patterns of Z_36 for which CP-SAT did not finish in cpsat12.py, once more with more threads.
usage: cpsat3.py tlimit workers"""
import sys, json, time
from lib import divisors
from milp import least
tl, w = float(sys.argv[1]), int(sys.argv[2])
dv = [d for d in divisors(36) if d > 1]
for D, val in (([2, 9, 12], 24), ([2, 6, 9, 12], 30), ([2, 3, 12, 18], 42)):
    t0 = time.time(); st, sz, v = least(36, D, [d for d in dv if d not in D], ub=val - 1, solver='cpsat', tlimit=tl, workers=w)
    print(json.dumps(dict(M=36, D=D, author_value=val, question=f'a multiset with at most {val - 1} elements?', cpsat_status=st, size=sz, seconds=round(time.time() - t0, 1))), flush=True)
