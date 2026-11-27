"""The first-order bound with the dangerous levels only, for a multiset F on Z_{n'} with an odd number of elements:
W = its support, W2 = the points of odd multiplicity (|W2| odd).
R_d(W2, W) = sum over e > 1, e | n', live for W and dangerous for W2 (sum_{w in W2} eta_e^w in 2 Z[eta_e]) of 2^(1 - D_e(W)).
Random pairs and a local search over pairs; prints the largest value found.  usage: ranksum2.py n1 trials steps seed"""
import sys, random
from fractions import Fraction
import numpy as np
from lib import *
from test_D import primes_of, rank2

def Rd(n1, W2, W):
    tot = Fraction(0)
    for e in divisors(n1):
        if e == 1: continue
        T = table(e, n1)
        if np.any(T[list(W2)].sum(axis=0) % 2): continue          # not dangerous
        ok = True
        for p in primes_of(e):
            i = 0
            while e % p ** (i + 1) == 0: i += 1
            groups = {}
            for x in W: groups.setdefault(x % p ** (i - 1), set()).add(x % p ** i)
            if not any(len(s) == p for s in groups.values()): ok = False; break
        if ok: tot += Fraction(2, 2 ** rank2([T[x] for x in W]))
    return tot

def main(n1, trials, steps, seed):
    random.seed(seed); best = (Fraction(0), None, None)
    for t in range(trials):
        W = set(random.sample(range(n1), random.randint(3, 12)))
        k2 = random.randrange(1, len(W) + 1, 2); W2 = set(random.sample(sorted(W), k2))
        r = Rd(n1, sorted(W2), sorted(W))
        for _ in range(steps):
            V, V2 = set(W), set(W2); mv = random.random()
            if mv < 0.25 and len(V) < 14: V.add(random.randrange(n1))
            elif mv < 0.5 and len(V - V2) > 0: V.discard(random.choice(sorted(V - V2)))
            elif mv < 0.75:                                           # move one point of W2 (keeps |W2| odd)
                x = random.choice(sorted(V2)); y = random.randrange(n1)
                V2.discard(x); V.discard(x); V2.add(y); V.add(y)
                if len(V2) % 2 == 0: continue
            else:                                                     # toggle two points of W in or out of W2
                for x in random.sample(sorted(V), min(2, len(V))): V2 ^= {x}
                if len(V2) % 2 == 0 or not V2: continue
            r2 = Rd(n1, sorted(V2), sorted(V))
            if r2 >= r: W, W2, r = V, V2, r2
        if r > best[0]: best = (r, sorted(W2), sorted(W))
    print(f"n'={n1}: {trials} starts x {steps} steps over pairs (W2 in W, |W2| odd): largest R_d = {best[0]} = {float(best[0]):.5f} at W2 = {best[1]}, W = {best[2]}", flush=True)

if __name__ == '__main__':
    main(*map(int, sys.argv[1:5]))
