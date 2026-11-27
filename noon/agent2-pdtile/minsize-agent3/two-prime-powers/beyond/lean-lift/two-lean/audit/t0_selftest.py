# Self-test of core.py: (1) the cyclotomic polynomials against sympy and against the product formula X^d - 1 = prod Phi_e;
# (2) the table method against literal long division, on random multisets and random signed multisets;
# (3) the census kernel against a plain itertools enumeration with long division;
# (4) translation does not change the divisor set (the reason only multisets containing 0 are enumerated).
import sys, random, itertools, math
import numpy as np
import sympy
from core import *

random.seed(20261126)
X = sympy.symbols('X')
bad = 0
for d in range(1, 241):
    ref = [int(c) for c in reversed(sympy.Poly(sympy.cyclotomic_poly(d, X), X).all_coeffs())]
    if ref != cyclo(d):
        bad += 1
    prod = [1]
    for e in divisors(d):
        prod = polymul(prod, cyclo(e))
    if prod != [-1] + [0] * (d - 1) + [1]:
        bad += 1
    assert len(cyclo(d)) - 1 == sum(1 for k in range(1, d + 1) if math.gcd(k, d) == 1)
print("cyclotomic polynomials d = 1..240 against sympy and against the product over divisors: mismatches", bad)

n_t = 0
bad = 0
for M in [1, 2, 3, 4, 6, 8, 9, 12, 15, 18, 20, 24, 30, 36, 45, 48, 60, 72, 90, 105]:
    G = Grp(M)
    # X^y mod Phi_d really is the row used
    for d in G.divs:
        for y in range(M):
            _, rem = polydivmod([0] * y + [1], cyclo(d))
            i = G.divs.index(d)
            row = G.C[y, G.off[i]:G.off[i + 1]]
            if list(row[:len(rem)]) != rem or any(row[len(rem):]):
                bad += 1
    for _ in range(150):
        s = random.randint(1, 14)
        el = [random.randrange(M) for _ in range(s)]
        if random.random() < 0.5:
            # make divisibility likelier: union of cosets of subgroups
            el = []
            for _ in range(random.randint(1, 3)):
                d = random.choice(G.divs)
                t = random.randrange(M)
                el += [(t + j * (M // d)) % M for j in range(d)]
        sg = [random.choice([1, -1]) for _ in el]
        if G.pattern(el) != pattern_slow(el, M):
            bad += 1
        if G.pattern(el, sg) != pattern_slow(el, M, sg):
            bad += 1
        t = random.randrange(M)
        if G.pattern([(y + t) % M for y in el]) != G.pattern(el):
            bad += 1
        n_t += 1
print("table method against long division (unsigned, signed, translated), random multisets:", n_t, "mismatches", bad)

bad = 0
n_c = 0
for M, S in [(1, 6), (2, 6), (3, 6), (4, 6), (6, 6), (9, 5), (12, 5), (18, 4), (30, 3)]:
    G, tally, exsize, ex, nodes = census(M, S)
    ref = {}
    for s in range(1, S + 1):
        for rest in itertools.combinations_with_replacement(range(M), s - 1):
            el = (0,) + rest
            pat = pattern_slow(el, M)
            ref[(G.mask_of(pat), s)] = ref.get((G.mask_of(pat), s), 0) + 1
            n_c += 1
    got = {(c, s): int(tally[c, s]) for c in range(tally.shape[0]) for s in range(S + 1) if tally[c, s]}
    if got != ref:
        bad += 1
    for c in range(tally.shape[0]):
        if exsize[c]:
            el = [int(v) for v in ex[c, :exsize[c]]]
            if G.mask_of(pattern_slow(el, M)) != c:
                bad += 1
            if exsize[c] != min(s for (cc, s) in ref if cc == c):
                bad += 1
print("census kernel against itertools + long division:", n_c, "multisets in 9 groups; mismatching groups/examples", bad)
