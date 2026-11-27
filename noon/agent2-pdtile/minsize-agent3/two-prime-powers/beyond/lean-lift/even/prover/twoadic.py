"""Lemma N (the levels of 2 are nested): test.  n = 2^k n', x <-> (u, w) = (x mod 2^k, x mod n').  For e | n' and a
monic factor g of Phi_e modulo 4 that is irreducible modulo 2 (Phi_e itself when 2 is a primitive root modulo e):
O/4 = (Z/4)[X]/(g), kappa = F_2[X]/(g).   beta_i = sum_x C(u_x, i) X^{w_x}  (mod 4),  a = least i with beta_i != 0 mod 2,
c = (beta_0 / 2) mod 2 (when a >= 1),  c' = c + beta_a mod 2,  lambda(N) = sum_{x in N} X^{w_x} mod 2 (N = the elements
with sign -).   Claim: if Phi_{2^j e} | S then  a >= 1 (j = 0) resp. a >= 2^(j-1) (j >= 1), and
lambda(N) = c' if j >= 1 and 2^(j-1) = a, and lambda(N) = c otherwise."""
import sys, itertools, random
from math import comb
import numpy as np
from lib import *

def polymod4(vec, g):
    """reduce an integer polynomial (list, low first) modulo monic g and modulo 4"""
    v = [c % 4 for c in vec]; f = len(g) - 1
    for i in range(len(v) - 1, f - 1, -1):
        c = v[i]
        if c:
            for j in range(f + 1): v[i - f + j] = (v[i - f + j] - c * g[j]) % 4
    return tuple(v[:f] + [0] * max(0, f - len(v)))

FACT = {1: [[-1, 1]], 3: [cyclo(3)], 5: [cyclo(5)], 9: [cyclo(9)], 11: [cyclo(11)], 13: [cyclo(13)], 25: [cyclo(25)], 27: [cyclo(27)],
        7: [[3, 1, 2, 1], [3, 2, 3, 1]]}   # x^3+2x^2+x+3 and x^3+3x^2+2x+3 modulo 4
def check_fact():
    p = polymul(FACT[7][0], FACT[7][1]); assert [c % 4 for c in p] == [1] * 7
check_fact()

def check(n, els, stats):
    k, n1 = two_part(n); q = 2 ** k
    signs, _ = good_signings(n, els, fix_first=False)
    idx = [x % n for x in els]
    data = {}
    for e in divisors(n1):
        if e not in FACT: continue
        for g in FACT[e]:
            f = len(g) - 1
            pw = [polymod4([0] * (x % n1) + [1], g) for x in els]
            beta = []
            for i in range(q):
                s = [0] * f
                for x, p in zip(els, pw):
                    c = comb(x % q, i) % 4
                    if c: s = [(a_ + c * b_) % 4 for a_, b_ in zip(s, p)]
                beta.append(s)
            a = next((i for i in range(q) if any(c % 2 for c in beta[i])), None)   # None: beta = 0 mod 2
            cc = tuple((c // 2) % 2 for c in beta[0]) if (a is None or a >= 1) else None
            cp = tuple((x_ + y_) % 2 for x_, y_ in zip(cc, beta[a])) if (cc is not None and a is not None) else None
            data[(e, tuple(g))] = (a, cc, cp, pw)
    for e in divisors(n1):
        if e not in FACT: continue
        for j in range(k + 1):
            d = 2 ** j * e
            badmask = ~np.any(signs @ table(d, n)[idx], axis=1)
            for g in FACT[e]:
                a, cc, cp, pw = data[(e, tuple(g))]
                free = (a is not None) and (a < (1 if j == 0 else 2 ** (j - 1)))
                if free:
                    assert not badmask.any(), ('free level is bad', n, els, d); stats['free'] += 1
                    continue
                stats['crit'] += 1
                special = (a is not None) and j >= 1 and 2 ** (j - 1) == a
                want = cp if special else cc
                for row in np.nonzero(badmask)[0]:
                    lam = [0] * len(want)
                    for s, p in zip(signs[row], pw):
                        if s == -1: lam = [(x_ + y_) % 2 for x_, y_ in zip(lam, p)]
                    assert tuple(lam) == want, ('coset', n, els, d, signs[row]); stats['badsignings'] += 1
                    stats['special' if special else 'plain'] += 1

def main(which):
    random.seed(11)
    stats = dict(free=0, crit=0, badsignings=0, special=0, plain=0); cnt = 0
    if which == 'exhaust':
        for n, M in ((4, 6), (8, 5), (16, 4), (6, 6), (12, 5), (24, 4), (10, 5), (20, 4), (40, 4), (14, 5), (28, 4), (18, 5), (36, 4), (72, 3), (22, 4), (26, 4)):
            for m in range(1, M + 1):
                for rest in itertools.combinations_with_replacement(range(n), m - 1):
                    check(n, [0] + list(rest), stats); cnt += 1
            print(f'n={n}: all multisets with 0 up to {M} elements done; running totals {cnt} multisets, {stats}', flush=True)
    else:
        for n in (24, 48, 40, 80, 56, 72, 144, 36, 108, 200, 104, 88):
            k, n1 = two_part(n)
            for trial in range(400):
                kind = trial % 4; m = random.randint(4, 11)
                if kind == 0: els = [random.randrange(n) for _ in range(m)]
                elif kind == 1:   # closed under x -> x + n/2
                    half = [random.randrange(n // 2) for _ in range(m // 2)]; els = half + [x + n // 2 for x in half]
                elif kind == 2:   # unions of cosets of a subgroup, truncated
                    step = random.choice([d for d in divisors(n) if 1 < d < n]); els = []
                    while len(els) < m:
                        c = random.randrange(step); els += [(c + t * step) % n for t in range(n // step)]
                    els = els[:11]
                else:             # few classes modulo n', so that the unsigned mask vanishes modulo 2 at many levels
                    ws = [random.randrange(n1) for _ in range(2)]; els = []
                    for _ in range(m // 2):
                        w = random.choice(ws); u1, u2 = random.randrange(2 ** k), random.randrange(2 ** k)
                        for u in (u1, u2):
                            els.append(next(x for x in range(n) if x % n1 == w and x % 2 ** k == u))
                check(n, els, stats); cnt += 1
            print(f'n={n}: 400 random and structured multisets done; running totals {cnt} multisets, {stats}', flush=True)

if __name__ == '__main__':
    main(sys.argv[1])
