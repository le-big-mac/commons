# adversary.py seed budget_seconds mlist nlist -- local search for multisets with FEW good signings (exact counts).
# One element is changed at a time; a change is kept if the fraction of good signings does not go up; restarts.
# Counting: through the coefficient vectors when the multiset has few distinct points, otherwise all 2^m signings
# by doubling (rfast.py).  Reports the least fraction found for each (n, m) and the stated bound.
import sys, math, random, time
from fractions import Fraction
import numpy as np
from rlib import divisors, good_count_grid
from rfast import bad_fast

seed = int(sys.argv[1]); budget = float(sys.argv[2])
MS = [int(a) for a in sys.argv[3].split(",")]
NS = [int(a) for a in sys.argv[4].split(",")]
rng = random.Random(seed)
t0 = time.time()
if max(MS) >= 20:
    budget = min(budget, 200.0)
cache = {}


def frac_good(B, n):
    key = (n, tuple(sorted(B)))
    if key not in cache:
        m = len(B)
        mult = {}
        for x in B:
            mult[x] = mult.get(x, 0) + 1
        gridsize = math.prod(c + 1 for c in mult.values())
        if gridsize * 8 <= (1 << m) or m > 20:
            if gridsize > 400_000:
                return None
            g, tot = good_count_grid(B, n)
        else:
            anybad = np.zeros(1 << m, dtype=bool)
            for d in divisors(n):
                anybad |= bad_fast(B, d)
            g, tot = (1 << m) - int(anybad.sum()), 1 << m
        cache[key] = Fraction(g, tot)
    return cache[key]


def start(n, m):
    r = rng.random()
    if r < 0.25:
        return [rng.randrange(n) for _ in range(m)]
    if r < 0.5:
        pool = [rng.randrange(n) for _ in range(rng.randint(2, 6))]
        return [rng.choice(pool) for _ in range(m)]
    if r < 0.75:
        pool = [rng.randrange(n) for _ in range(m // 2)]
        return (pool + pool + [0])[:m]
    g = rng.choice([d for d in divisors(n) if d > 1])
    pts = [j * (n // g) % n for j in range(g)]
    return [pts[k % g] for k in range(m)]


best = {}
evals = 0
budget_each = budget / (len(MS) * len(NS))
for n in NS:
    for m in MS:
        tstart = time.time()
        b = (Fraction(2), None)
        restarts = 0
        while time.time() - tstart < budget_each:
            B = start(n, m)
            f = frac_good(B, n)
            if f is None:
                continue
            restarts += 1
            stall = 0
            while stall < 60 and time.time() - tstart < budget_each:
                C = list(B)
                k = rng.randrange(m)
                r = rng.random()
                if r < 0.4:
                    C[k] = rng.randrange(n)
                elif r < 0.8:
                    C[k] = rng.choice(B)
                else:
                    d = rng.choice([d for d in divisors(n) if d > 1])
                    C[k] = (C[k] + rng.randrange(1, d) * (n // d)) % n
                fc = frac_good(C, n)
                evals += 1
                if fc is not None and fc <= f:
                    stall = 0 if fc < f else stall + 1
                    B, f = C, fc
                else:
                    stall += 1
            if f < b[0]:
                b = (f, sorted(B))
        best[(n, m)] = (b, restarts)
        print("Z_%d, m = %d: least fraction of good signings found %s = %.5f at %s  (%d starts)" % (n, m, b[0], float(b[0]), b[1], restarts))
        sys.stdout.flush()
print("evaluations: %d, distinct multisets counted: %d; least fraction overall: %.5f; seconds %.0f"
      % (evals, len(cache), float(min(v[0][0] for v in best.values())), time.time() - t0))
