"""Referee's own CP-SAT model (written from scratch) of subsets of Z_{p0 p1 p2} in coordinates, used to test the
counting statements of the note, and some sharper ones found while refereeing, on prime triples beyond the
reach of exhaustive enumeration.  Every 'expect INFEASIBLE' question has a control (one hypothesis dropped
or a bound relaxed) that is expected FEASIBLE.  A solver's INFEASIBLE is evidence, not a certificate.
usage: cpsat.py p0 p1 p2 [timelimit]
"""
import sys, itertools, time
from ortools.sat.python import cp_model

p = tuple(int(a) for a in sys.argv[1:4]); M = p[0]*p[1]*p[2]
TL = float(sys.argv[4]) if len(sys.argv) > 4 else 120.0

class Q:
    def __init__(self, hi=1):
        self.m = cp_model.CpModel()
        self.a = {}
        for c in itertools.product(range(p[0]), range(p[1]), range(p[2])):
            self.a[c] = self.m.NewIntVar(0, hi, f"a{c}")
        self.n = sum(self.a.values())
        # translation symmetry: we may assume the origin is in A (only used when hi == 1)
        if hi == 1: self.m.Add(self.a[(0, 0, 0)] == 1)
    def N1(self, x, i): return sum(v for c, v in self.a.items() if c[x] == i)
    def N2(self, x, y, i, j): return sum(v for c, v in self.a.items() if c[x] == i and c[y] == j)
    def _disj(self, exprs, bound):
        """at least one of the integer expressions is nonzero (|expr| <= bound)."""
        lits = []
        for k, e in enumerate(exprs):
            bp = self.m.NewBoolVar(""); bn = self.m.NewBoolVar("")
            self.m.Add(e >= 1).OnlyEnforceIf(bp); self.m.Add(e <= -1).OnlyEnforceIf(bn)
            lits += [bp, bn]
        self.m.AddBoolOr(lits)
    def inE(self, x):
        for i in range(1, p[x]): self.m.Add(self.N1(x, i) == self.N1(x, 0))
    def notE(self, x):
        self._disj([self.N1(x, i) - self.N1(x, 0) for i in range(1, p[x])], M)
    def _d2(self, x, y):
        return [self.N2(x, y, i, j) - self.N2(x, y, i, 0) - self.N2(x, y, 0, j) + self.N2(x, y, 0, 0)
                for i in range(1, p[x]) for j in range(1, p[y])]
    def inP(self, x, y):
        for e in self._d2(x, y): self.m.Add(e == 0)
    def notP(self, x, y): self._disj(self._d2(x, y), M)
    def _d3(self):
        out = []
        for i in range(1, p[0]):
            for j in range(1, p[1]):
                for k in range(1, p[2]):
                    e = 0
                    for s in itertools.product((0, 1), repeat=3):
                        c = (i*s[0], j*s[1], k*s[2])
                        e += (1 if sum(s) % 2 == 1 else -1) * self.a[c]
                    out.append(e)
        return out
    def t1(self):
        for e in self._d3(): self.m.Add(e == 0)
    def t0(self): self._disj(self._d3(), 8)
    def size(self, lo, hi):
        self.m.Add(self.n >= lo); self.m.Add(self.n <= hi)
    def solve(self):
        s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = TL; s.parameters.num_workers = 4
        r = s.Solve(self.m)
        return {cp_model.INFEASIBLE: "INFEASIBLE", cp_model.OPTIMAL: "FEASIBLE", cp_model.FEASIBLE: "FEASIBLE"}.get(r, "UNKNOWN")

results = []
MODE = sys.argv[5] if len(sys.argv) > 5 else "all"     # "note": only the note's own statements and their controls
def ask(name, build, expect, hi=1):
    if MODE == "note" and "sharper" in name: return
    if MODE == "sharper" and "sharper" not in name: return
    q = Q(hi); build(q); t0 = time.time(); r = q.solve()
    ok = (r == expect)
    results.append((name, expect, r, ok))
    print(f"{'ok ' if ok else '***'} {name:100s} expect {expect:10s} got {r:10s} {time.time()-t0:6.1f}s", flush=True)

pm = min(range(3), key=lambda w: p[w])
for (x, y, z) in itertools.permutations(range(3)):
    tag = f"[x,y,z={p[x]},{p[y]},{p[z]}]"
    if x < y:
        ask(f"L3 {tag}: {{x,y}} in P, x,y not in E, n <= p_x+p_y-1",
            lambda q: (q.inP(x, y), q.notE(x), q.notE(y), q.size(1, p[x] + p[y] - 1)), "INFEASIBLE")
        ask(f"L3 control {tag}: same with n = p_x+p_y",
            lambda q: (q.inP(x, y), q.notE(x), q.notE(y), q.size(p[x] + p[y], p[x] + p[y])), "FEASIBLE")
        ask(f"L5 {tag}: n = p_x p_y, x,y in E, t=1, {{x,y}} not in P",
            lambda q: (q.inE(x), q.inE(y), q.t1(), q.notP(x, y), q.size(p[x]*p[y], p[x]*p[y])), "INFEASIBLE")
        ask(f"L5 control {tag}: same without t=1",
            lambda q: (q.inE(x), q.inE(y), q.notP(x, y), q.size(p[x]*p[y], p[x]*p[y])), "FEASIBLE")
        ask(f"L5 sharper {tag}: x,y in E, t=1, {{x,y}} not in P, ANY size",
            lambda q: (q.inE(x), q.inE(y), q.t1(), q.notP(x, y)), "INFEASIBLE")
        ask(f"L5 multiset {tag}: multiset of p_x p_y elements, x,y in E, t=1, {{x,y}} not in P",
            lambda q: (q.inE(x), q.inE(y), q.t1(), q.notP(x, y), q.size(p[x]*p[y], p[x]*p[y])), "INFEASIBLE", hi=p[x]*p[y])
        ask(f"L5 multiset control {tag}: multiset of 2 p_x p_y p_z elements (so the mean of N_xy is 2 p_z), same hypotheses",
            lambda q: (q.inE(x), q.inE(y), q.t1(), q.notP(x, y), q.size(2*M, 2*M)), "FEASIBLE", hi=2*M)
    # Section 5, E = {x}, a second pair
    ask(f"S5 second pair {tag}: x in E, y,z not in E, {{y,z}},{{x,y}} in P, n <= p_x p_z + p_y - 1",
        lambda q: (q.inE(x), q.notE(y), q.notE(z), q.inP(y, z), q.inP(x, y), q.size(1, p[x]*p[z] + p[y] - 1)), "INFEASIBLE")
    ask(f"S5 second pair sharper {tag}: x in E, y,z not in E, {{y,z}},{{x,y}} in P, ANY size",
        lambda q: (q.inE(x), q.notE(y), q.notE(z), q.inP(y, z), q.inP(x, y)), "INFEASIBLE")
    ask(f"S5 second pair control {tag}: x in E, y not in E, {{y,z}},{{x,y}} in P (z in E allowed)",
        lambda q: (q.inE(x), q.notE(y), q.inP(y, z), q.inP(x, y)), "FEASIBLE")
    if y < z:
        mn = min(p[y], p[z]); w = y if p[y] < p[z] else z
        ask(f"S5 t=1 {tag}: x in E, {{y,z}} in P, t=1, n <= p_x min(p_y,p_z) - 1",
            lambda q: (q.inE(x), q.inP(y, z), q.t1(), q.size(1, p[x]*mn - 1)), "INFEASIBLE")
        ask(f"S5 t=1 {tag}: x in E, {{y,z}} in P, t=1, n = p_x min(p_y,p_z), smaller of y,z not in E",
            lambda q: (q.inE(x), q.inP(y, z), q.t1(), q.size(p[x]*mn, p[x]*mn), q.notE(w)), "INFEASIBLE")
        ask(f"S5 t=1 control {tag}: x in E, {{y,z}} in P, t=1, n = p_x min(p_y,p_z)",
            lambda q: (q.inE(x), q.inP(y, z), q.t1(), q.size(p[x]*mn, p[x]*mn)), "FEASIBLE")
        ask(f"S5 t=1 sharper {tag}: x in E, {{y,z}} in P, t=1, y and z not in E, ANY size",
            lambda q: (q.inE(x), q.inP(y, z), q.t1(), q.notE(y), q.notE(z)), "INFEASIBLE")
        ask(f"S5 t=1 control2 {tag}: x in E, {{y,z}} in P, t=0, y and z not in E",
            lambda q: (q.inE(x), q.inP(y, z), q.t0(), q.notE(y), q.notE(z)), "FEASIBLE")
        # three pairs / two pairs through x
        ask(f"S5 two pairs through x, sharper {tag}: {{x,y}},{{x,z}} in P, x not in E, y not in E, ANY size",
            lambda q: (q.inP(x, y), q.inP(x, z), q.notE(x), q.notE(y)), "INFEASIBLE")
        ask(f"S5 two pairs through x, sharper {tag}: {{x,y}},{{x,z}} in P, x not in E, z not in E, ANY size",
            lambda q: (q.inP(x, y), q.inP(x, z), q.notE(x), q.notE(z)), "INFEASIBLE")
        ask(f"S5 two pairs through x, control {tag}: {{x,y}},{{x,z}} in P, x not in E",
            lambda q: (q.inP(x, y), q.inP(x, z), q.notE(x)), "FEASIBLE")
s = sorted(p)
ask(f"S5 three pairs: E empty, all three pairs in P, n <= pi = {s[0]*s[1]}",
    lambda q: (q.notE(0), q.notE(1), q.notE(2), q.inP(0, 1), q.inP(0, 2), q.inP(1, 2), q.size(1, s[0]*s[1])), "INFEASIBLE")
ask(f"S5 three pairs control: all three pairs in P, n <= pi",
    lambda q: (q.inP(0, 1), q.inP(0, 2), q.inP(1, 2), q.size(1, s[0]*s[1])), "FEASIBLE")
ask(f"S5 Z_A={{M}}: t=1, n <= smallest prime, smallest prime not in E",
    lambda q: (q.t1(), q.size(1, p[pm]), q.notE(pm)), "INFEASIBLE")
ask(f"S5 Z_A={{M}} control: t=1, n <= smallest prime (a coset of the subgroup of that order)",
    lambda q: (q.t1(), q.size(1, p[pm])), "FEASIBLE")
ask(f"S5 Z_A={{M}} control: Z_A = {{M}} exactly, any size (the pattern is realised)",
    lambda q: (q.t1(), q.notE(0), q.notE(1), q.notE(2), q.notP(0, 1), q.notP(0, 2), q.notP(1, 2)), "FEASIBLE")
ask(f"S5 Z_A={{M}} sharper: t=1, n < largest prime, pair of the two smaller primes not in P",
    lambda q: (q.t1(), q.size(1, max(p) - 1), q.notP(*[w for w in range(3) if p[w] != max(p)])), "INFEASIBLE")
bad = [r for r in results if not r[3]]
print(f"\n{p}: {len(results)} questions, {len(results) - len(bad)} as expected, {len(bad)} not as expected")
for r in bad: print("   NOT AS EXPECTED:", r)
