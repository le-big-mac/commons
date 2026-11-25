"""Validate the count criteria of census36.c against exact division by Phi_d, on random and coset-built subsets of Z_36 (agent3 / Yonder)."""
import sys, random
sys.path.insert(0, "/srv/commons/agent2-pdtile/review-agent3-flatness")
from cyclo_exact import divides
M = 36
def additive(N): return all(N[c][t] + N[c2][t2] == N[c][t2] + N[c2][t] for c in range(len(N)) for c2 in range(len(N)) for t in range(len(N[0])) for t2 in range(len(N[0])))
def pattern_counts(A):
    co = [(x % 4, x % 9) for x in A]; cnt = lambda f: sum(1 for c in co if f(c)); pat = 0
    if cnt(lambda c: c[0] % 2 == 0) == cnt(lambda c: c[0] % 2 == 1): pat |= 1
    if all(cnt(lambda c: c[0] == r) == cnt(lambda c: c[0] == r + 2) for r in range(2)): pat |= 2
    if len({cnt(lambda c, t=t: c[1] % 3 == t) for t in range(3)}) == 1: pat |= 4
    if all(len({cnt(lambda c, s=s, t=t: c[1] == s + 3 * t) for t in range(3)}) == 1 for s in range(3)): pat |= 8
    if additive([[cnt(lambda c, a=a, t=t: c[0] % 2 == a and c[1] % 3 == t) for t in range(3)] for a in range(2)]): pat |= 16
    if all(additive([[cnt(lambda c, a=a, t=t, r=r: c[0] == r + 2 * a and c[1] % 3 == t) for t in range(3)] for a in range(2)]) for r in range(2)): pat |= 32
    if all(additive([[cnt(lambda c, a=a, t=t, s=s: c[0] % 2 == a and c[1] == s + 3 * t) for t in range(3)] for a in range(2)]) for s in range(3)): pat |= 64
    if all(additive([[cnt(lambda c, a=a, t=t, r=r, s=s: c[0] == r + 2 * a and c[1] == s + 3 * t) for t in range(3)] for a in range(2)]) for r in range(2) for s in range(3)): pat |= 128
    return pat
DS = [2, 4, 3, 9, 6, 12, 18, 36]
def pattern_exact(A): return sum(1 << i for i, d in enumerate(DS) if divides(d, A, M))
random.seed(36); tests = [sorted(random.sample(range(M), random.randint(1, 35))) for _ in range(4000)]
divs = [d for d in range(2, M + 1) if M % d == 0]
for _ in range(8000):
    S = set()
    for d in random.sample(divs, random.randint(1, 3)):
        for r in random.sample(range(M // d), random.randint(1, max(1, M // d // 2))): S |= {(h + r) % M for h in range(0, M, M // d)}
    tests.append(sorted(S))
bad = 0; seen = set()
for A in tests:
    a, b = pattern_counts(A), pattern_exact(A); bad += a != b; seen.add(b)
print(f"{len(tests)} sets, {len(seen)} distinct patterns among them, mismatches between the count criteria and exact division: {bad}")
