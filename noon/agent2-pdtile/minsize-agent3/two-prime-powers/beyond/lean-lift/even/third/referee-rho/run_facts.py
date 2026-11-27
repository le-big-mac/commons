# (F2), (F3) and the inner claims of (A), (B1), (B2) of lemma-rho.md, signing by signing, on random multisets.
import sys, random, itertools
from collections import Counter
from ref_lib import bad_levels

random.seed(271126)
cnt = Counter(); fail = Counter()


def rand_multiset(k, m):
    kind = random.random()
    N = 1 << k
    if kind < 0.35:
        return [random.randrange(N) for _ in range(m)]
    if kind < 0.7:
        pool = [random.randrange(N) for _ in range(random.randint(1, 4))]
        return [random.choice(pool) for _ in range(m)]
    return random.sample(range(N), min(m, N))


def sgn3(s):  # s mod 3 as -1, 0, 1
    s %= 3
    return -1 if s == 2 else s


# ---- (F2): A a sub-multiset that no class at depth <= D divides
for trial in range(4000):
    k = random.randint(0, 5); m = random.randint(1, 8)
    B = rand_multiset(k, m); m = len(B)
    D = random.randint(0, k)
    # A: a random sub-multiset (possibly empty, possibly all) of one class at depth D
    x = random.choice(B)
    cls = [i for i in range(m) if B[i] % (1 << D) == x % (1 << D)]
    A = [i for i in cls if random.random() < 0.6]
    if random.random() < 0.15:
        A = cls
    rest = [i for i in range(m) if i not in A]
    for eps in itertools.product((1, -1), repeat=m):
        s = sgn3(sum(eps[i] for i in A))
        bad = {j for j in bad_levels(B, k, eps) if j <= D}
        if s == 0:
            B2 = [B[i] for i in rest]; e2 = [eps[i] for i in rest]
            if not B2:
                cnt["(F2) s = 0, B minus A empty"] += 1
                if 0 not in bad:
                    fail["(F2) empty: level 0 bad"] += 1
                if bad != set(range(0, D + 1)):
                    fail["(F2) empty: all levels 0..D bad"] += 1
                continue
            cnt["(F2) s = 0"] += 1
            if bad != {j for j in bad_levels(B2, k, e2) if j <= D}:
                fail["(F2) s = 0"] += 1
        else:
            for a in {B[i] for i in A}:      # every choice of the one element a of A
                B2 = [B[i] for i in rest] + [a]; e2 = [eps[i] for i in rest] + [s]
                cnt["(F2) s = +-1"] += 1
                if bad != {j for j in bad_levels(B2, k, e2) if j <= D}:
                    fail["(F2) s = +-1"] += 1

# ---- (F2) needs its hypothesis: count how often the conclusion fails when A is divided by a class at depth <= D
for trial in range(1500):
    k = random.randint(1, 4); m = random.randint(2, 6)
    B = rand_multiset(k, m); m = len(B)
    D = random.randint(1, k)
    A = random.sample(range(m), random.randint(2, m))
    if len({B[i] % (1 << D) for i in A}) == 1:
        continue
    rest = [i for i in range(m) if i not in A]
    broke = False
    for eps in itertools.product((1, -1), repeat=m):
        s = sgn3(sum(eps[i] for i in A))
        bad = {j for j in bad_levels(B, k, eps) if j <= D}
        if s == 0:
            B2 = [B[i] for i in rest]; e2 = [eps[i] for i in rest]
        else:
            B2 = [B[i] for i in rest] + [B[A[0]]]; e2 = [eps[i] for i in rest] + [s]
        if bad != {j for j in bad_levels(B2, k, e2) if j <= D}:
            broke = True; break
    cnt["(F2) without its hypothesis: instances"] += 1
    if broke:
        cnt["(F2) without its hypothesis: conclusion false"] += 1

# ---- (F3)
for trial in range(4000):
    k = random.randint(1, 5); m = random.randint(1, 8)
    B = rand_multiset(k, m); m = len(B)
    for eps in itertools.product((1, -1), repeat=m):
        bad = bad_levels(B, k, eps)
        for j in range(1, k + 1):
            cl = Counter(b % (1 << (j - 1)) for b in B)
            if 1 in cl.values():
                cnt["(F3) level with a one-element class"] += 1
                if j in bad:
                    fail["(F3)"] += 1

# ---- inner claims of (B1) and (B2), on random sets
for trial in range(6000):
    k = random.randint(1, 5)
    m = random.randint(2, min(8, 1 << k))
    if random.random() < 0.5:
        # force type (B2): pairs at depth r-1
        r = random.randint(1, k)
        nn = random.randint(1, min(4, 1 << (r - 1)))
        low = random.sample(range(1 << (r - 1)), nn)
        B = []
        for c in low:
            hi = random.randrange(1 << (k - r))
            hi2 = random.randrange(1 << (k - r))
            B += [c + (hi << r), c + (1 << (r - 1)) + (hi2 << r)]
    else:
        B = random.sample(range(1 << k), m)
    m = len(B)
    r = next(j for j in range(0, k + 1) if len({b % (1 << j) for b in B}) == m)
    cl = {}
    for i, b in enumerate(B):
        cl.setdefault(b % (1 << (r - 1)), []).append(i)
    pairs = [c for c in cl.values() if len(c) == 2]
    singles = [c for c in cl.values() if len(c) == 1]
    assert pairs and all(len(c) <= 2 for c in cl.values())
    for eps in itertools.product((1, -1), repeat=m):
        bad = bad_levels(B, k, eps)
        if any(j > r for j in bad):
            fail["levels > r not bad"] += 1
        if singles:
            cnt["(B1) signings"] += 1
            if r in bad:
                fail["(B1) level r not bad"] += 1
            (iy, iz) = pairs[0]
            s = sgn3(eps[iy] + eps[iz])
            rest = [i for i in range(m) if i not in (iy, iz)]
            if s == 0:
                B2 = [B[i] for i in rest]; e2 = [eps[i] for i in rest]
            else:
                B2 = [B[i] for i in rest] + [B[iy]]; e2 = [eps[i] for i in rest] + [s]
            # all levels: "no level is bad for B iff none is bad for the smaller set"
            if (not bad) != (not bad_levels(B2, k, e2)):
                fail["(B1) reduction"] += 1
        else:
            cnt["(B2) signings"] += 1
            U = []; eU = []
            for (iy, iz) in pairs:
                s = sgn3(eps[iy] + eps[iz])
                if s != 0:
                    U.append(B[iy]); eU.append(s)
            badU = bad_levels(U, k, eU)      # empty U: every level bad by this code's convention
            if {j for j in bad if j <= r - 1} != {j for j in badU if j <= r - 1}:
                fail["(B2) levels <= r-1 are those of U"] += 1
            if (r in bad) != (len(U) == len(pairs)):
                fail["(B2) level r bad iff U is all"] += 1
            if U and any(j >= r for j in badU):
                fail["(B2) levels >= r not bad for U"] += 1
            # the whole equivalence used for the formula
            if (not bad) != (len(U) < len(pairs) and len(U) > 0 and not badU):
                fail["(B2) good iff U proper, nonempty, good"] += 1
print("counts:", dict(cnt))
print("failures:", dict(fail) if fail else "none")
