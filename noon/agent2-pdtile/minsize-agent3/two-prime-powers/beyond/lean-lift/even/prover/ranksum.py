"""How far is the first-order count from closing when 15 | n and m is odd?  For a support W in Z_{n'} (n' odd) the bound
of Proposition P for odd m is  R(W) = sum over the live e > 1 of 2^(1 - D_e(W)),  D_e = rank over F_2 of X^w mod (2, Phi_e).
It depends on W only.  Also R_d(W): the same sum over the live e that are dangerous for the SET W (sum_w eta^w in 2 Z[eta_e]).
Prints the largest values found.  If R(W) < 1 for every W, Conjecture E follows for every multiset with an odd number of
elements and support W; if R_d(W) < 1, for the set W with |W| odd (and every multiset on it with odd multiplicities)."""
import sys, itertools, random
from fractions import Fraction
import numpy as np
from lib import *
from test_D import primes_of, rank2

def R(n1, W):
    tot = Fraction(0); totd = Fraction(0)
    for e in divisors(n1):
        if e == 1: continue
        ok = True
        for p in primes_of(e):
            i = 0
            while e % p ** (i + 1) == 0: i += 1
            groups = {}
            for x in W: groups.setdefault(x % p ** (i - 1), set()).add(x % p ** i)
            if not any(len(s) == p for s in groups.values()): ok = False; break
        if not ok: continue
        T = table(e, n1)
        D = rank2([T[x] for x in W])
        tot += Fraction(2, 2 ** D)
        if not np.any(T[list(W)].sum(axis=0) % 2): totd += Fraction(2, 2 ** D)
    return tot, totd

def main():
    random.seed(61)
    # n' = 15: every W containing 0
    best = (Fraction(0), None); bestd = (Fraction(0), None); cnt = 0
    for bits in range(1, 2 ** 14):
        W = [0] + [x for x in range(1, 15) if bits >> (x - 1) & 1]
        r, rd = R(15, W); cnt += 1
        if r > best[0]: best = (r, W)
        if len(W) % 2 and rd > bestd[0]: bestd = (rd, W)
    print(f"n'=15: all {cnt} supports with 0 and at least 2 elements: largest R = {best[0]} = {float(best[0]):.4f} at {best[1]}; largest R_d over |W| odd = {bestd[0]} = {float(bestd[0]):.4f} at {bestd[1]}", flush=True)
    for n1, trials in ((45, 6000), (105, 4000), (315, 1500), (225, 1500), (135, 2000)):
        best = (Fraction(0), None); bestd = (Fraction(0), None)
        for t in range(trials):
            kind = t % 4; size = random.randint(3, 16)
            if kind == 0: W = random.sample(range(n1), size)
            elif kind == 1:   # an interval
                W = list(range(size))
            elif kind == 2:   # as few elements as possible with many live levels: residues spread by CRT
                W = sorted(set((random.randrange(n1) // 1) for _ in range(size)))
                ps = primes_of(n1); base = random.randrange(n1)
                W = sorted(set((base + r * (n1 // p)) % n1 for p in ps for r in range(p)) | set(W[:max(0, size - 8)]))
            else:             # the first size residues along a generator scaled so that classes fill evenly
                g = random.choice([x for x in range(1, n1) if np.gcd(x, n1) == 1]); W = sorted(set(g * i % n1 for i in range(size)))
            W = sorted(set(W))
            if len(W) < 2: continue
            r, rd = R(n1, W)
            if r > best[0]: best = (r, W)
            if len(W) % 2 and rd > bestd[0]: bestd = (rd, W)
        print(f"n'={n1}: {trials} supports (random, intervals, cosets of the prime subgroups, arithmetic progressions; 2 to 16+ elements): largest R = {float(best[0]):.4f} at {best[1]}; largest R_d over |W| odd = {float(bestd[0]):.4f} at {bestd[1]}", flush=True)

if __name__ == '__main__':
    main()
