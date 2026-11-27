# t0_selftest.py -- checks of core.py:
#  (1) Phi_d against sympy for d <= 240;
#  (2) the remainder table against literal long division, on random multisets and sets;
#  (3) the compiled enumerator against itertools (sets and multisets containing 0), and "containing 0" against all
#      (multi)sets, on small groups;
#  (4) translation does not change the divisors.
import itertools, random, sys
import numpy as np
from core import *

random.seed(12345)
# (1)
import sympy
X = sympy.symbols('X')
bad = 0
for d in range(1, 241):
    c = sympy.Poly(sympy.cyclotomic_poly(d, X), X).all_coeffs()[::-1]
    if [int(x) for x in c] != cyclotomic(d):
        bad += 1
print("(1) Phi_d against sympy, d = 1..240: mismatches", bad)

# (2)
n = 0
bad = 0
for G in [1, 2, 3, 4, 6, 8, 9, 12, 18, 25, 27, 30, 36, 45, 54, 60, 75, 90, 98, 150]:
    grp = Group(G)
    for trial in range(150):
        if trial % 2 == 0:
            mult = [random.choice([0, 0, 0, 1, 1, 2, 3, 7]) for _ in range(G)]
        else:
            mult = [random.choice([0, 1]) for _ in range(G)]
        if trial < 6:
            # some with many divisors: unions of cosets
            mult = [0] * G
            d0 = random.choice(grp.divs)
            for c in range(random.randint(1, 3)):
                s0 = random.randrange(G)
                for k in range(G // d0):
                    mult[(s0 + k * d0) % G] += 1
        pat = grp.pattern(mult, with_one=True)
        for d in grp.divs:
            n += 1
            if (d in pat) != divides_longdiv(G, mult, d):
                bad += 1
print("(2) table against long division:", n, "tests (multiset, d), mismatches", bad)

# (3)
bad = 0
ntot = 0
for G, T in [(6, 6), (8, 5), (9, 5), (12, 5), (18, 4), (10, 5)]:
    grp = Group(G)
    for rep in (False, True):
        cnt = census(grp, T, rep)
        got = patterns_by_size(grp, cnt)
        # split run must give the same
        cnt2 = census(grp, T, rep, 0, G // 2) + census(grp, T, rep, G // 2, G)
        if not (cnt2 == cnt).all():
            bad += 1
            print("split mismatch", G, rep)
        for t in range(1, T + 1):
            exp0 = {}
            expall = set()
            it = (itertools.combinations_with_replacement(range(G), t) if rep else itertools.combinations(range(G), t))
            for comb in it:
                mult = [0] * G
                for y in comb:
                    mult[y] += 1
                pat = frozenset(d for d in grp.dgt1 if divides_longdiv(G, mult, d))
                expall.add(pat)
                ntot += 1
                if comb[0] == 0:
                    exp0[pat] = exp0.get(pat, 0) + 1
            if exp0 != got.get(t, {}):
                bad += 1
                print("mismatch", G, rep, t)
            if set(exp0) != expall:
                bad += 1
                print("containing-0 loses a pattern", G, rep, t)
print("(3) enumerator against itertools + long division:", ntot, "(multi)sets, mismatches", bad)

# (4)
bad = 0
n = 0
for G in [12, 18, 30, 54, 90]:
    grp = Group(G)
    for trial in range(200):
        mult = [random.choice([0, 0, 1, 1, 2]) for _ in range(G)]
        c = random.randrange(G)
        mult2 = [mult[(y - c) % G] for y in range(G)]
        n += 1
        if grp.pattern(mult, True) != grp.pattern(mult2, True):
            bad += 1
print("(4) translation:", n, "tests, mismatches", bad)
