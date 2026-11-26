"""Z_36, pattern {2, 3, 12, 18}: the one value of the Z_36 table (42) that rested on HiGHS alone.
Phi_2 and Phi_3 divide the mask, so the size is a multiple of 6 (the value at 1 is divisible by Phi_2(1) Phi_3(1) = 6).  A multiset with
this pattern and fewer than 42 elements would therefore have 6, 12, 18, 24, 30 or 36 elements.  Each of the six sizes is given to CP-SAT
(exact integers) as a separate question on the referee's model (cuboid forms, ../milp.py: build): is there a multiset of exactly that
size with exactly that pattern?  'INFEASIBLE' six times is a proof in exact integers that the least size is 42.
usage: cpsat_42.py size tlimit workers"""
import sys, json, time
sys.path.insert(0, '/home/agent3/pq2/referee/two-powers')
from lib import divisors, pattern
from milp import build
from ortools.sat.python import cp_model
M = 36; D = [2, 3, 12, 18]; size, tl, w = int(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3])
dv = [d for d in divisors(M) if d > 1]
nvar, nb, eqs, ges = build(M, D, [d for d in dv if d not in D], size)
m = cp_model.CpModel()
xs = [m.NewIntVar(0, size // 2, f'x{i}') for i in range(M)] + [m.NewBoolVar(f'b{i}') for i in range(nb)]     # a multiplicity is at most half the size (nonempty pattern)
for r, rhs in eqs: m.Add(sum(c * xs[x] for x, c in r.items()) == rhs)
for r, rhs in ges: m.Add(sum(c * xs[x] for x, c in r.items()) >= rhs)
m.Add(sum(xs[:M]) == size)
s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = tl; s.parameters.num_search_workers = w
t0 = time.time(); st = s.Solve(m)
name = {cp_model.OPTIMAL: 'FEASIBLE', cp_model.FEASIBLE: 'FEASIBLE', cp_model.INFEASIBLE: 'INFEASIBLE'}.get(st, 'UNKNOWN')
rec = dict(M=M, D=D, size=size, cpsat=name, seconds=round(time.time() - t0, 1))
if name == 'FEASIBLE':
    v = [s.Value(t) for t in xs[:M]]; rec['multiset'] = v; rec['exact_pattern'] = pattern(M, v)
print(json.dumps(rec), flush=True)
