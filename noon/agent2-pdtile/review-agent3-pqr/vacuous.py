"""Two sub-cases in Section 5 of agent2's pqr-agent2.md that, by a short argument, no SET can be in at all (agent3 / Yonder).
  V1: x in E, y and z not in E, {y,z} in P, {x,y} in P.     (argument: p_x divides alpha_j, so some entry of N_yz is >= p_x + 1 > p_x)
  V2: x in E, y and z not in E, {y,z} in P, t = 1.          (argument: every x-slice is a union of full lines of one direction)
Checked here by integer programming (HiGHS through scipy), any size, for several triples and every assignment of roles.
'y not in E' is imposed as N_y(0) >= N_y(1) + 1, which loses nothing: translations and multiplication by units of Z_{p_y} preserve
the pattern and can move any unequal pair of counts to positions 0 and 1 in that order.  Controls: each question with one hypothesis dropped."""
import sys, itertools, time
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
def ask(pr, x, y, z, hyp):
    P = [pr[x], pr[y], pr[z]]; n = P[0] * P[1] * P[2]                  # coordinates ordered (x, y, z)
    idx = lambda i, j, k: (i * P[1] + j) * P[2] + k
    rows, lo, hi = [], [], []
    def add(coefs, a, b):
        r = np.zeros(n)
        for v, c in coefs: r[v] += c
        rows.append(r); lo.append(a); hi.append(b)
    cells = list(itertools.product(range(P[0]), range(P[1]), range(P[2])))
    def N1(axis, val): return [(idx(*c), 1) for c in cells if c[axis] == val]
    def N2(ax1, v1, ax2, v2): return [(idx(*c), 1) for c in cells if c[ax1] == v1 and c[ax2] == v2]
    neg = lambda L: [(v, -c) for v, c in L]
    if "xE" in hyp:
        for i in range(1, P[0]): add(N1(0, i) + neg(N1(0, 0)), 0, 0)
    if "y!E" in hyp: add(N1(1, 0) + neg(N1(1, 1)), 1, np.inf)
    if "z!E" in hyp: add(N1(2, 0) + neg(N1(2, 1)), 1, np.inf)
    def additive(a, b):
        for u in range(1, P[a]):
            for v in range(1, P[b]): add(N2(a, u, b, v) + neg(N2(a, 0, b, v)) + neg(N2(a, u, b, 0)) + N2(a, 0, b, 0), 0, 0)
    if "yzP" in hyp: additive(1, 2)
    if "xyP" in hyp: additive(0, 1)
    if "t" in hyp:
        for i in range(1, P[0]):
            for j in range(1, P[1]):
                for k in range(1, P[2]):
                    add([(idx(i, j, k), 1), (idx(0, j, k), -1), (idx(i, 0, k), -1), (idx(i, j, 0), -1), (idx(i, 0, 0), 1), (idx(0, j, 0), 1), (idx(0, 0, k), 1), (idx(0, 0, 0), -1)], 0, 0)
    add([(v, 1) for v in range(n)], 1, n - 1)                          # nonempty, not everything
    r = milp(np.zeros(n), constraints=LinearConstraint(np.array(rows), lo, hi), integrality=np.ones(n), bounds=Bounds(0, 1), options={"time_limit": 300})
    return {0: "set found", 2: "infeasible"}.get(r.status, f"status {r.status}")
triples = [(2, 3, 5), (2, 3, 7), (2, 5, 7), (3, 5, 7), (2, 3, 11), (3, 5, 11)]
V1 = ("xE", "y!E", "z!E", "yzP", "xyP"); V2 = ("xE", "y!E", "z!E", "yzP", "t")
tally = {}
t0 = time.time()
for pr in triples:
    for x, y, z in itertools.permutations(range(3)):
        for name, H in (("V1", V1), ("V2", V2)):
            res = ask(pr, x, y, z, H); tally[(name, "full", res)] = tally.get((name, "full", res), 0) + 1
            if res not in ("infeasible",): print(f"   NOTE {name} full question at {pr}, roles x,y,z = {pr[x]},{pr[y]},{pr[z]}: {res}", flush=True)
            for drop in H:
                res = ask(pr, x, y, z, tuple(h for h in H if h != drop)); tally[(name, "without " + drop, res)] = tally.get((name, "without " + drop, res), 0) + 1
    print(f"{pr} done, {time.time() - t0:.0f} s", flush=True)
print(f"{len(triples)} triples x 6 role assignments = {len(triples) * 6} questions per line")
for k in sorted(tally): print(f"  {k[0]}  {k[1]:14s} {k[2]:12s} {tally[k]}")
