"""A pattern of Z_M whose least size no programme has proved: every size below the smallest multiset known, one size at a time.
The size of a multiset is a multiple of prod Phi_d(1) over the prime-power d of its pattern (the mask is divisible by those Phi_d, and
Phi_{r^k}(1) = r).  Each admissible size below the known one is given to CP-SAT (exact integers) on the referee's model (cuboid forms,
../milp.py: build) as a question: is there a multiset of exactly that size with exactly that pattern?  If every answer is INFEASIBLE,
the known size is least, proved in exact integers.
usage: cpsat_sizes.py M known_size tlimit workers d1,d2,... [lowest]    one JSON line for each size, largest size first; stops at the first
that is not INFEASIBLE; sizes below "lowest" (a bound known without a solver, see bounds_no_solver.py) are not tried"""
import sys, json, time
sys.path.insert(0, '/home/agent3/pq2/referee/two-powers')
from lib import divisors, pattern, prime_factors
from milp import build
from ortools.sat.python import cp_model
M, known, tl, w = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]); D = sorted(int(t) for t in sys.argv[5].split(','))
dv = [d for d in divisors(M) if d > 1]
step = 1
for d in D:
    pf = prime_factors(d)
    if len(pf) == 1: step *= pf[0]
LOW = int(sys.argv[6]) if len(sys.argv) > 6 else 1
sizes = [s for s in range(step, known, step) if s >= LOW][::-1]
print(json.dumps(dict(M=M, D=D, known=known, sizes_are_multiples_of=step, sizes_to_exclude=sizes)), flush=True)
allinf = True
for size in sizes:
    nvar, nb, eqs, ges = build(M, D, [d for d in dv if d not in D], size)
    m = cp_model.CpModel()
    xs = [m.NewIntVar(0, size // 2, f'x{i}') for i in range(M)] + [m.NewBoolVar(f'b{i}') for i in range(nb)]
    for r, rhs in eqs: m.Add(sum(c * xs[x] for x, c in r.items()) == rhs)
    for r, rhs in ges: m.Add(sum(c * xs[x] for x, c in r.items()) >= rhs)
    m.Add(sum(xs[:M]) == size)
    s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = tl; s.parameters.num_search_workers = w
    t0 = time.time(); st = s.Solve(m)
    name = {cp_model.OPTIMAL: 'FEASIBLE', cp_model.FEASIBLE: 'FEASIBLE', cp_model.INFEASIBLE: 'INFEASIBLE'}.get(st, 'UNKNOWN')
    rec = dict(M=M, D=D, size=size, cpsat=name, seconds=round(time.time() - t0, 1))
    if name == 'FEASIBLE':
        v = [s.Value(t) for t in xs[:M]]; rec['multiset'] = v; rec['exact_pattern_ok'] = (pattern(M, v) == D and sum(v) == size)
    print(json.dumps(rec), flush=True)
    if name != 'INFEASIBLE': allinf = False; break
print(json.dumps(dict(M=M, D=D, known=known, every_smaller_admissible_size_infeasible=allinf)), flush=True)
