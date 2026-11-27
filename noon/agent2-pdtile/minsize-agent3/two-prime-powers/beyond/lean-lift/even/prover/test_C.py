"""Theorem C (n = 2^k p^a): test of every step of the count, all signings, exact arithmetic.
 (1) step-down S1: if level i of the p-tree has no full group, a signing bad at 2^j p^i is bad at 2^j p^(i-1);
 (2) e = 1: no signing is bad at any 2^j if m is odd; for m even the share of signings bad at some 2^j is at most
     1/2 + [a = 2^d] * prod over the occupied classes C modulo 2^d of c_|C|   (a = least i with sum_x C(u_x, i) odd);
 (3) e = p^i with a full group at level i: the share of signings bad at some 2^j p^i (j = 0..k) is at most
     (1 + g) 2^(-D),  D = sum over the occupied groups at level i of min(occupied subclasses, p - 1),
     g = phi(p^i)/ord_{p^i}(2) the number of primes above 2;
 (4) the share of signings bad somewhere is at most the sum of these bounds."""
import sys, itertools, random
from math import comb
from fractions import Fraction
import numpy as np
from lib import *

def cc(r): return Fraction(comb(r, r // 2), 2 ** r)
def ordmod(q):
    t, x = 1, 2 % q
    while x != 1: x = x * 2 % q; t += 1
    return t

def check(p, k, a_, els, st):
    q = 2 ** k; P = p ** a_; n = q * P; m = len(els)
    signs = all_signs(m, fix_first=True); idx = [x % n for x in els]
    bad = {d: ~np.any(signs @ table(d, n)[idx], axis=1) for d in divisors(n)}
    tot = len(signs); bound = Fraction(0)
    # (1)
    full = {}
    for i in range(1, a_ + 1):
        groups = {}
        for x in els: groups.setdefault(x % p ** (i - 1), set()).add(x % p ** i)
        full[i] = any(len(s) == p for s in groups.values())
        D = sum(min(len(s), p - 1) for s in groups.values())
        anyj = np.zeros(tot, bool)
        for j in range(k + 1):
            anyj |= bad[2 ** j * p ** i]
            if not full[i]:
                assert not (bad[2 ** j * p ** i] & ~bad[2 ** j * p ** (i - 1)]).any(), ('S1', n, els, i, j); st['s1'] += 1
        if full[i]:
            g = (p - 1) * p ** (i - 1) // ordmod(p ** i)
            b = Fraction(1 + g, 2 ** D); sh = Fraction(int(anyj.sum()), tot)
            assert sh <= b, ('level', n, els, i, sh, b); st['levels'] += 1
            st['maxratio'] = max(st['maxratio'], float(sh / b)); bound += b
    # (2)
    any1 = np.zeros(tot, bool)
    for j in range(k + 1): any1 |= bad[2 ** j]
    sh1 = Fraction(int(any1.sum()), tot)
    if m % 2 == 1:
        assert sh1 == 0
    else:
        beta = [sum(comb(x % q, i) for x in els) for i in range(q)]
        a = next((i for i in range(q) if beta[i] % 2), None)
        b1 = Fraction(1, 2)
        if a is not None and a & (a - 1) == 0:
            d = a.bit_length() - 1; cls = {}
            for x in els: cls[x % 2 ** d] = cls.get(x % 2 ** d, 0) + 1
            pr = Fraction(1)
            for s in cls.values(): assert s % 2 == 0; pr *= cc(s)
            b1 += pr; st['special1'] += 1
        assert sh1 <= b1, ('e=1', n, els, sh1, b1); st['max1'] = max(st['max1'], float(sh1)); bound += b1
    # (4)
    allbad = np.zeros(tot, bool)
    for d in bad: allbad |= bad[d]
    sh = Fraction(int(allbad.sum()), tot)
    assert sh <= bound, ('total', n, els, sh, bound)
    if bound < 1: st['closed'] += 1
    if sh == 1: assert exceptional_pair(n, els); st['exceptional'] += 1
    st['n'] += 1

def main():
    random.seed(23)
    st = dict(n=0, s1=0, levels=0, maxratio=0.0, special1=0, max1=0.0, closed=0, exceptional=0)
    for p, k, a_ in ((3, 1, 1), (3, 2, 1), (3, 3, 1), (3, 1, 2), (3, 2, 2), (3, 2, 3), (5, 1, 1), (5, 2, 1), (5, 3, 1), (5, 2, 2), (7, 1, 1), (7, 2, 1), (7, 3, 1), (11, 2, 1)):
        q = 2 ** k; P = p ** a_; n = q * P
        # exhaustive small
        M = 4 if n > 40 else 5
        if n <= 24:
            for m in range(1, M + 1):
                for rest in itertools.combinations_with_replacement(range(n), m - 1): check(p, k, a_, [0] + list(rest), st)
        for trial in range(500):
            kind = trial % 5; m = random.randint(3, 11)
            if kind == 0: els = [random.randrange(n) for _ in range(m)]
            elif kind == 1:
                half = [random.randrange(n // 2) for _ in range(m // 2)]; els = half + [x + n // 2 for x in half]
            elif kind == 2:   # full p-tree levels: one element in each class modulo p, the rest in few classes
                els = [next(x for x in range(random.randrange(n), 10 * n) if x % p == r) % n for r in range(p)][:11]
                while len(els) < m: els.append(random.choice(els) + P * random.randrange(q))
                els = [x % n for x in els]
            elif kind == 3:   # union of cosets
                step = random.choice([d for d in divisors(n) if 1 < d < n]); els = []
                while len(els) < m:
                    c = random.randrange(step); els += [(c + t * step) % n for t in range(n // step)]
                els = els[:11]
            else:             # an interval
                s = random.randrange(n); els = [(s + t) % n for t in range(m)]
            check(p, k, a_, els, st)
        print(f'p={p} k={k} a={a_} (n={n}) done; totals {st}', flush=True)

if __name__ == '__main__':
    main()
