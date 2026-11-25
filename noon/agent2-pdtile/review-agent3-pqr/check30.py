"""Every statement of agent2's pqr-agent2.md that is about sets, tested on EVERY subset of Z_30 containing 0 (agent3 / Yonder).
Input: census30.out from census30.c (pattern, size, count).  No solver.  D+ of the 128 patterns by my own small linear program
(8 variables: a function of the order of the element), compared with agent2's exact values.
For each statement the line gives how many sets meet its premise (the sets that could have contradicted it) and how many do."""
import sys, itertools, random
from fractions import Fraction
import numpy as np
from scipy.optimize import linprog
sys.path.insert(0, "/srv/commons/agent2-pdtile/review-agent3-flatness")
from cyclo_exact import divides
PR = (2, 3, 5); M = 30
PAIRS = ((0, 1), (0, 2), (1, 2))
cnt = {}
for line in open("census30.out"):
    p, n, c = map(int, line.split()); cnt[(p, n)] = c
total = sum(cnt.values()); assert total == 2 ** 29
def dec(pat):
    E = frozenset(x for x in range(3) if pat >> x & 1); P = frozenset(PAIRS[q] for q in range(3) if pat >> (3 + q) & 1); t = pat >> 6 & 1
    return E, P, t
def zset(pat):
    E, P, t = dec(pat); return sorted([PR[x] for x in E] + [PR[a] * PR[b] for a, b in P] + ([M] if t else []))
# ---- 0. the census's patterns against exact polynomial division, on random and structured sets
def pattern_exact(A):
    pat = 0
    for x in range(3):
        if divides(PR[x], A, M): pat |= 1 << x
    for q, (a, b) in enumerate(PAIRS):
        if divides(PR[a] * PR[b], A, M): pat |= 8 << q
    if divides(M, A, M): pat |= 64
    return pat
def pattern_counts(A):
    co = [(r % 2, r % 3, r % 5) for r in A]; pat = 0
    for x in range(3):
        if len({sum(1 for c in co if c[x] == i) for i in range(PR[x])}) == 1: pat |= 1 << x
    for q, (a, b) in enumerate(PAIRS):
        N = [[sum(1 for c in co if c[a] == i and c[b] == j) for j in range(PR[b])] for i in range(PR[a])]
        if all(N[i][j] - N[0][j] - N[i][0] + N[0][0] == 0 for i in range(PR[a]) for j in range(PR[b])): pat |= 8 << q
    ind = {c: 1 for c in co}; g = lambda i, j, k: ind.get((i, j, k), 0)
    if all(g(i, j, k) - g(0, j, k) - g(i, 0, k) - g(i, j, 0) + g(i, 0, 0) + g(0, j, 0) + g(0, 0, k) - g(0, 0, 0) == 0 for i in range(2) for j in range(3) for k in range(5)): pat |= 64
    return pat
random.seed(8); seen = {}
tests = [sorted(random.sample(range(M), random.randint(1, 29))) for _ in range(6000)]
for d in (2, 3, 5, 6, 10, 15, 30):                      # unions of cosets, which have rich patterns
    H = list(range(0, M, M // d))
    for _ in range(600):
        reps = random.sample(range(M // d), random.randint(1, M // d)); tests.append(sorted({(h + r) % M for h in H for r in reps}))
for d1, d2 in itertools.combinations((2, 3, 5, 6, 10, 15), 2):
    for _ in range(100):
        A = {(h + random.randrange(M)) % M for h in range(0, M, M // d1)} | {(h + random.randrange(M)) % M for h in range(0, M, M // d2)}; tests.append(sorted(A))
bad = 0
for A in tests:
    pe, pc = pattern_exact(A), pattern_counts(A); bad += pe != pc; seen[pe] = seen.get(pe, 0) + 1
print(f"0. count criteria (F1)-(F3) against exact division by Phi_d: {len(tests)} sets, {len(seen)} distinct patterns among them, mismatches: {bad}")
print(f"   census: {total} sets, {len({p for p, n in cnt})} of 128 patterns occur")
# ---- D+ by my own LP
ORD = [d for d in (1, 2, 3, 5, 6, 10, 15, 30)]
def cls_size(e): return int(np.prod([p - 1 for p in PR if e % p == 0]))
def csum(d, e):                                           # sum over elements of order e of a character of order d
    return int(np.prod([(p - 1 if d % p else -1) for p in PR if e % p == 0]))
def dplus(Z):
    # minimise sum f over f(0) = 1, f >= 0, fhat >= 0, fhat = 0 at characters of order not in Z (and not 1);  D+ = M / min
    var = ORD[1:]; c = [cls_size(e) for e in var]
    A_ub, b_ub, A_eq, b_eq = [], [], [], []
    for d in ORD:
        row = [csum(d, e) for e in var]                   # fhat(d) = 1 + row . f
        if d == 1 or d in Z: A_ub.append([-x for x in row]); b_ub.append(1.0)
        else: A_eq.append(row); b_eq.append(-1.0)
    r = linprog(c, A_ub=A_ub or None, b_ub=b_ub or None, A_eq=A_eq or None, b_eq=b_eq or None, bounds=[(0, None)] * len(var), method="highs")
    assert r.status == 0; return M / (1 + r.fun)
D = {pat: dplus(set(zset(pat))) for pat in range(128)}
try:
    sys.path.insert(0, "/srv/commons/agent2-pdtile/flat"); from lp import Setup
    S = Setup(M); worst = max(abs(D[pat] - float(S.Dplus(zset(pat))[0])) for pat in range(128))
    print(f"   D+ of all 128 patterns: my LP against agent2's exact simplex, largest difference {worst:.1e}")
except Exception as e: print("   (could not load agent2's lp.py for the comparison:", e, ")")
# ---- statements
def sets_where(cond): return [(pat, n, c) for (pat, n), c in cnt.items() if cond(*dec(pat), n)]
def report(label, premise, conclusion):
    pool = sets_where(premise); fail = [(pat, n, c) for pat, n, c in pool if not conclusion(*dec(pat), n)]
    print(f"{label}: premise met by {sum(c for *_, c in pool):,} sets in {len({p for p, *_ in pool})} patterns; violations: {sum(c for *_, c in fail):,}" + (f"  e.g. Z = {zset(fail[0][0])}, n = {fail[0][1]}" if fail else ""))
names = {0: "2", 1: "3", 2: "5"}
print("1. (I1): product of the primes in E divides n")
report("   ", lambda E, P, t, n: True, lambda E, P, t, n: n % int(np.prod([PR[x] for x in E])) == 0)
print("2. Lemma 3: {x,y} in P, x and y not in E  =>  n >= p_x + p_y")
for a, b in PAIRS:
    report(f"   pair {{{PR[a]},{PR[b]}}}", lambda E, P, t, n: (a, b) in P and a not in E and b not in E, lambda E, P, t, n: n >= PR[a] + PR[b])
    pool = sets_where(lambda E, P, t, n: (a, b) in P and a not in E and b not in E); print(f"        smallest such set has {min(n for _, n, _ in pool)} elements (bound {PR[a] + PR[b]})")
print("3. Lemma 5: n = p_x p_y, x and y in E, t = 1  =>  {x,y} in P")
for a, b in PAIRS:
    report(f"   pair {{{PR[a]},{PR[b]}}}", lambda E, P, t, n: n == PR[a] * PR[b] and a in E and b in E and t == 1, lambda E, P, t, n: (a, b) in P)
    pool = sets_where(lambda E, P, t, n: n == PR[a] * PR[b] and a in E and b in E and t == 0 and (a, b) not in P)
    print(f"        control, the same with t = 0: {sum(c for *_, c in pool):,} sets lack the pair (so the hypothesis t = 1 is doing work)")
print("4. Section 5, E = {x}, {y,z} in P:")
for x in range(3):
    y, z = [w for w in range(3) if w != x]; yz = (y, z); xy = tuple(sorted((x, y))); xz = tuple(sorted((x, z)))
    report(f"   x = {PR[x]}, also {{x,y}} in P  =>  n >= p_z p_x + p_y = {PR[z] * PR[x] + PR[y]}", lambda E, P, t, n: E == {x} and yz in P and xy in P, lambda E, P, t, n: n >= PR[z] * PR[x] + PR[y])
    report(f"   x = {PR[x]}, also {{x,z}} in P  =>  n >= p_y p_x + p_z = {PR[y] * PR[x] + PR[z]}", lambda E, P, t, n: E == {x} and yz in P and xz in P, lambda E, P, t, n: n >= PR[y] * PR[x] + PR[z])
    report(f"   x = {PR[x]}, neither, t = 1  =>  n > p_x min(p_y, p_z) = {PR[x] * min(PR[y], PR[z])}", lambda E, P, t, n: E == {x} and yz in P and xy not in P and xz not in P and t == 1, lambda E, P, t, n: n > PR[x] * min(PR[y], PR[z]))
    report(f"   x = {PR[x]}, neither, t = 0  =>  n >= p_y + p_z = {PR[y] + PR[z]} (Lemma 3)", lambda E, P, t, n: E == {x} and yz in P and xy not in P and xz not in P and t == 0, lambda E, P, t, n: n >= PR[y] + PR[z])
print("5. Section 5, E empty:")
report("   Z_A = {30}  =>  n > 2 (the smallest prime)", lambda E, P, t, n: not E and not P and t == 1, lambda E, P, t, n: n > 2)
pool = sets_where(lambda E, P, t, n: not E and not P and t == 1); print(f"        smallest set with Z_A = {{30}} has {min(n for _, n, _ in pool)} elements")
report("   all three pairs in P  =>  n > 6 (product of the two smallest primes)", lambda E, P, t, n: not E and len(P) == 3, lambda E, P, t, n: n > 6)
pool = sets_where(lambda E, P, t, n: not E and len(P) == 3); print(f"        smallest such set has {min(n for _, n, _ in pool) if pool else '-'} elements")
print("6. The theorem, end to end: n = D+(Z_A)  =>  (T1) and (T2)")
def T12(E, P, t, n):
    if n != int(np.prod([PR[x] for x in E])): return False
    if any(tuple(sorted(pq)) not in P for pq in itertools.combinations(sorted(E), 2)): return False
    return not (len(E) == 3 and t == 0)
pd = [(pat, n, c) for (pat, n), c in cnt.items() if abs(D[pat] - n) < 1e-7]
viol = [(pat, n, c) for pat, n, c in pd if not T12(*dec(pat), n)]
over = [(pat, n, c) for (pat, n), c in cnt.items() if n < D[pat] - 1e-7]
print(f"   sets with n = D+(Z_A): {sum(c for *_, c in pd):,} in {len({p for p, *_ in pd})} patterns; of these, failing (T1) or (T2): {sum(c for *_, c in viol):,}")
print(f"   sets with n < D+(Z_A) (would contradict Proposition 1): {sum(c for *_, c in over):,}")
t12 = [(pat, n, c) for (pat, n), c in cnt.items() if T12(*dec(pat), n)]
print(f"   sets satisfying (T1) and (T2): {sum(c for *_, c in t12):,}; of these with n = D+: {sum(c for pat, n, c in t12 if abs(D[pat] - n) < 1e-7):,}")
# near misses: patterns that occur, where D+ is an integer multiple of prod(E) but (T1)/(T2) would fail; how far above D+ is the smallest set?
print("7. Near misses: patterns that occur for some set, would violate (T1) or (T2) at n = D+, and have D+ a multiple of the product of E")
rows = []
for pat in range(128):
    ns = sorted(n for (p, n) in cnt if p == pat)
    if not ns: continue
    E, P, t = dec(pat); k = int(np.prod([PR[x] for x in E])); d = D[pat]
    if abs(d - round(d)) < 1e-7 and round(d) % k == 0 and not T12(E, P, t, round(d)): rows.append((ns[0] / d, zset(pat), round(d), ns[0]))
rows.sort()
print(f"   {len(rows)} such patterns; closest: " + "; ".join(f"Z = {z}: D+ = {d}, smallest set {n}" for _, z, d, n in rows[:6]))
