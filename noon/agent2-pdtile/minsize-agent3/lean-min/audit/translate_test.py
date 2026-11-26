"""The pattern of a multiset on Z_M does not change when the multiset is translated: checked by long division
on every multiset of small size in small groups, and on random multisets in the larger ones.  (The window
bound of enumB.c rests on this.)"""
import itertools
import random
from math import gcd

from cyc import pattern

random.seed(20261126)


def translate(w, t):
    M = len(w)
    return [w[(a - t) % M] for a in range(M)]


def check(M, w):
    pat = pattern(M, w)
    for t in range(1, M):
        assert pattern(M, translate(w, t)) == pat, (M, w, t)
    return 1


total = 0
for M, smax in [(2, 8), (3, 8), (5, 6), (6, 6), (10, 4), (12, 4), (15, 3), (18, 3), (20, 3), (24, 3)]:
    c = 0
    for s in range(0, smax + 1):
        for comb in itertools.combinations_with_replacement(range(M), s):
            w = [0] * M
            for a in comb:
                w[a] += 1
            c += check(M, w)
    print(f"Z_{M}: every multiset of size <= {smax}: {c} multisets, all {M - 1} translates have the same pattern")
    total += c
for M in [12, 18, 20, 24, 28]:
    c = 0
    for _ in range(3000):
        s = random.randint(1, 40)
        w = [0] * M
        for _ in range(s):
            w[random.randrange(M)] += 1
        c += check(M, w)
    # structured ones, so that large patterns occur: sums of cosets of subgroups
    for _ in range(3000):
        w = [0] * M
        for _ in range(random.randint(1, 4)):
            d = random.choice([d for d in range(2, M + 1) if M % d == 0])
            t = random.randrange(M)
            for i in range(d):
                w[(t + i * (M // d)) % M] += 1
        c += check(M, w)
    print(f"Z_{M}: {c} random multisets (half of them sums of cosets), all translates have the same pattern")
    total += c
print("total multisets checked:", total)
