"""Z_231 = 3*7*11, D = {231}: the one case tried on the side where S6 says the corner formula is RIGHT (least 21 = 3 + 7 + 11, against
(3-1)(7-1) + 11 - 1 = 22).  Question put to CP-SAT (exact integers) on the referee's model: is there a multiset with pattern exactly
{231} and at most 20 elements?   usage: z231.py tlimit workers"""
import sys, json, time
from lib import divisors
from milp import least
tl, w = float(sys.argv[1]), int(sys.argv[2])
dv = [d for d in divisors(231) if d > 1]
t0 = time.time(); st, sz, v = least(231, [231], [d for d in dv if d != 231], ub=20, solver='cpsat', tlimit=tl, workers=w)
print(json.dumps(dict(M=231, D=[231], question='a multiset with pattern exactly {231} and at most 20 elements?', cpsat_status=st, size=sz, seconds=round(time.time() - t0, 1))))
