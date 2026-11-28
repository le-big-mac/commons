# Statements 1 and 2 once more, with numbers that are not all rational multiples of one another in a plane:
# nonzero vectors of Z^n (n = 2..5).  Real (and complex) numbers linearly independent over Q, say 1, sqrt 2, sqrt 3,
# sqrt 5, sqrt 7, make Z^n a set of real numbers, with a signed sum equal to v exactly when the vectors agree; so
# the largest multiplicity of a value among the signed sums of m nonzero vectors must not exceed C(m, m//2).
# Also: roots of unity of order d <= 60 as vectors modulo Phi_d, every value v (not only 0).
# usage: python lo2.py SECONDS
import os, sys, random, time, itertools
from collections import Counter
from math import comb
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))   # the interpreter runs isolated (-I)
import bad


def maxmult(vecs):
    t = Counter({tuple([0] * len(vecs[0])) if vecs else (): 1})
    for x in vecs:
        u = Counter()
        for s, c in t.items():
            u[tuple(a + b for a, b in zip(s, x))] += c
            u[tuple(a - b for a, b in zip(s, x))] += c
        t = u
    return max(t.values())


def main():
    budget = float(sys.argv[1])
    rng = random.Random(12)
    best = {}
    n = 0
    t0 = time.time()
    while time.time() - t0 < budget / 2:
        dim = rng.randint(2, 5)
        m = rng.randint(0, 12)
        R = rng.choice([1, 1, 2, 5])
        pool = None
        if rng.random() < 0.5:      # few different vectors, repeated
            pool = []
            while len(pool) < rng.randint(1, 4):
                z = tuple(rng.randint(-R, R) for _ in range(dim))
                if any(z):
                    pool.append(z)
        vecs = []
        while len(vecs) < m:
            z = rng.choice(pool) if pool else tuple(rng.randint(-R, R) for _ in range(dim))
            if any(z):
                vecs.append(z)
        c = maxmult(vecs)
        n += 1
        if c > comb(m, m // 2):
            print("VIOLATION", vecs, c)
            sys.exit(1)
        best[("Z^n", m)] = max(best.get(("Z^n", m), 0), c)
    print("nonzero vectors of Z^n, n = 2..5: %d lists, no value taken more than C(m, m//2) times" % n)
    n2 = 0
    t0 = time.time()
    while time.time() - t0 < budget / 2:
        d = rng.randint(1, 60)
        m = rng.randint(0, 12)
        e = bad.gen_exps(d, m, rng)
        if m == 0:
            c = 1
        else:
            V = bad.redtable(d)[np.asarray(e) % d]
            Rm = bad.signs(m) @ V
            c = int(np.unique(Rm, axis=0, return_counts=True)[1].max())
        n2 += 1
        if c > comb(m, m // 2):
            print("VIOLATION", e, d, c)
            sys.exit(1)
        best[("roots", m)] = max(best.get(("roots", m), 0), c)
    print("roots of unity of order d <= 60 (the numbers zeta^(e_k)), every value: %d lists, none above C(m, m//2)" % n2)
    print()
    print(" m  C(m,m//2)  largest multiplicity: vectors of Z^n   roots of unity")
    for m in range(13):
        print("%2d %8d %20d %20d" % (m, comb(m, m // 2), best.get(("Z^n", m), 0), best.get(("roots", m), 0)))


main()
