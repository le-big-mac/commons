#!/usr/bin/env python3
"""Referee: a climbing search for multisets with a large share of bad signings (from the definition, all signings),
to attack the bounds T2(m) of result.md.  usage: r_search.py n m restarts steps seed [pairs]"""
import sys, random
from fractions import Fraction as F
import numpy as np
import r_brute as RB


def badcount(B, n, E, divs):
    anyb = np.zeros(E.shape[0], dtype=bool)
    for d in divs:
        anyb |= RB.zero_rows(E, RB.V(d)[[b % d for b in B]])
    return int(anyb.sum())


def main():
    n, m, restarts, steps, seed = (int(x) for x in sys.argv[1:6]); pairs = len(sys.argv) > 6
    rnd = random.Random(seed); E = RB.signs(m); divs = RB.divisors(n)
    fac = RB.factor(n); subs = [1] + [n // q for q in fac] + [n // (q * q) for q in fac if n % (q * q) == 0]
    best = 0; arg = None; evals = 0; t2 = RB.T2(m)
    for r in range(restarts):
        k = m // 2 if pairs else m
        X = [rnd.randrange(n) for _ in range(k)]
        mk = (lambda X: sorted([x for x in X for _ in (0, 1)] + ([0] if m % 2 else []))) if pairs else (lambda X: sorted(X))
        cur = badcount(mk(X), n, E, divs); evals += 1
        for s in range(steps):
            Y = X[:]
            i = rnd.randrange(k)
            if rnd.random() < 0.5:
                Y[i] = (Y[i] + rnd.choice(subs) * rnd.randrange(1, 7)) % n
            else:
                Y[i] = Y[rnd.randrange(k)] if rnd.random() < 0.5 else rnd.randrange(n)
            c = badcount(mk(Y), n, E, divs); evals += 1
            if c >= cur:
                X, cur = Y, c
        if cur > best:
            best, arg = cur, mk(X)
    S = 2 ** m
    print("search n=%d m=%d %s restarts=%d steps=%d evaluations=%d: largest bad share %s = %.5f at %s; T2(m)=%s; above T2: %s; above 3/8: %s" % (
        n, m, "pairs" if pairs else "free", restarts, steps, evals, F(best, S), best / S, arg, t2, F(best, S) > t2, F(best, S) > F(3, 8)), flush=True)


if __name__ == '__main__':
    main()
