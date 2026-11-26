"""The twelve patterns of Z_36 that the author's solver had not decided when the referee looked: is there a multiset with
exactly that pattern and FEWER elements than the author's value?  The referee's model (cuboid forms) given to CP-SAT, which
works in exact integers; 'infeasible' is a proof that there is none.   usage: cpsat12.py J K tlimit [first index]"""
import sys, json, time
from lib import divisors
from milp import least
J, K, tl = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]); START = int(sys.argv[4]) if len(sys.argv) > 4 else 0
todo = [([2, 9, 12], 24), ([2, 3, 4, 18], 24), ([4, 6, 9, 12], 30), ([4, 6, 9], 24), ([2, 3, 12, 18], 42), ([4, 6, 9, 18], 30), ([2, 6, 9, 12], 30),
        ([3, 4, 6, 18], 30), ([2, 3, 4, 12, 18], 36), ([4, 6, 18], 22), ([6, 9, 12], 21), ([2, 3, 9, 12, 18], 54)]
dv = [d for d in divisors(36) if d > 1]
for i, (D, val) in enumerate(todo):
    if i < START or i % K != J: continue
    t0 = time.time(); st, sz, v = least(36, D, [d for d in dv if d not in D], ub=val - 1, solver='cpsat', tlimit=tl, workers=2)
    print(json.dumps(dict(M=36, D=D, author_value=val, question=f'a multiset with at most {val - 1} elements?', cpsat_status=st, size=sz, seconds=round(time.time() - t0, 1))), flush=True)
