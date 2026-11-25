"""Independent numerical test of Facts 1 and 2 of flatness.md (agent3 / Yonder).
Exact integer arithmetic: Phi_d | A(X) is decided by polynomial remainder, not by floating-point roots."""
import itertools, random
from cyclo_exact import divides
def N(A, pa, qb):
    t = {}
    for x in A: t[(x % pa, x % qb)] = t.get((x % pa, x % qb), 0) + 1
    return t
def fact1(A, p, a):                       # N_{a,0}(r + i p^{a-1}) = N_{a,0}(r)
    pa = p ** a; n = N(A, pa, 1)
    return all(n.get(((r + i * p ** (a - 1)) % pa, 0), 0) == n.get((r, 0), 0) for r in range(pa) for i in range(p))
def fact2(A, p, a, q, b):                 # N(r + i p^{a-1}, t') - N(r, t') the same for all t' in t + q^{b-1} Z
    pa, qb = p ** a, q ** b; n = N(A, pa, qb); g = lambda r, t: n.get((r % pa, t % qb), 0)
    for r in range(pa):
        for i in range(1, p):
            for t in range(q ** (b - 1)):
                if len({g(r + i * p ** (a - 1), t + j * q ** (b - 1)) - g(r, t + j * q ** (b - 1)) for j in range(q)}) > 1: return False
    return True
random.seed(1); tot = pos = 0
# every subset of Z_12 and of Z_18; every relevant divisor
for M, p, q in ((12, 2, 3), (18, 3, 2), (18, 2, 3), (12, 3, 2)):
    al = max(a for a in range(6) if M % p ** a == 0); be = max(b for b in range(6) if M % q ** b == 0)
    for mask in range(1, 1 << M):
        A = [x for x in range(M) if mask >> x & 1]
        for a in range(1, al + 1):
            assert divides(p ** a, A, M) == fact1(A, p, a), (M, A, p, a); tot += 1; pos += fact1(A, p, a)
            for b in range(1, be + 1):
                assert divides(p ** a * q ** b, A, M) == fact2(A, p, a, q, b), (M, A, p, a, q, b); tot += 1; pos += fact2(A, p, a, q, b)
print(f"all subsets of Z_12 and Z_18: {tot} comparisons, {pos} with the condition true, no disagreement")
# Z_36, Z_72, Z_144: random sets (mostly negatives) and sets built block by block to satisfy the count condition (positives)
def built(M, p, a, q, b):
    pa, qb = p ** a, q ** b; K = M // (pa * qb); A = []
    for r0 in range(p ** (a - 1)):
        for t0 in range(q ** (b - 1)):
            kind = random.choice("zorc")                   # zero, one, rows (depends on i), columns (depends on j)
            u = [random.randint(0, 1) for _ in range(p)]; w = [random.randint(0, 1) for _ in range(q)]
            for i in range(p):
                for j in range(q):
                    v = {"z": 0, "o": 1, "r": u[i], "c": w[j]}[kind]
                    if v:
                        r, t = r0 + i * p ** (a - 1), t0 + j * q ** (b - 1)
                        x = next(x for x in range(pa * qb) if x % pa == r and x % qb == t)
                        A.append(x + pa * qb * random.randrange(K))        # one element in that class, anywhere in Z_M
    return sorted(set(A))
tot = pos = 0
for M, p, q in ((36, 2, 3), (72, 2, 3), (144, 2, 3), (144, 3, 2), (100, 2, 5), (225, 3, 5)):
    al = max(a for a in range(8) if M % p ** a == 0); be = max(b for b in range(8) if M % q ** b == 0)
    for trial in range(400):
        a, b = random.randint(1, al), random.randint(1, be)
        A = built(M, p, a, q, b) if trial % 2 else random.sample(range(M), random.randint(1, M - 1))
        if not A: continue
        x, y = divides(p ** a * q ** b, A, M), fact2(A, p, a, q, b); assert x == y, (M, A, p, a, q, b); tot += 1; pos += x
        x, y = divides(p ** a, A, M), fact1(A, p, a); assert x == y; tot += 1; pos += x
print(f"larger moduli, random and constructed sets: {tot} comparisons, {pos} with the condition true, no disagreement")
