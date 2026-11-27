"""S5 (card_badSet_three_pow_mul_le): m >= 7, level i of 3 live, rank e 3 i = 1  =>  #bad(3^i) * 16 <= 3 * 2^m.

(a) one occupied group: every triple of class sizes (k0, k1, k2), all >= 1, with m = k0 + k1 + k2 <= MAXM, at the levels
    i = 1, 2, 3: all signings, exact division by Phi_{3^i}; compared with the closed count
    sum_beta C(k0, (k0+beta)/2) C(k1, (k1+beta)/2) C(k2, (k2+beta)/2).  The inequality is reported for m >= 7 (the
    statement) and for m < 7 (outside it: is the hypothesis 7 <= m needed?).
(b) the closed count for every triple with m <= 150: the largest fraction #bad / 2^m for each m.
(c) two or more occupied groups at level i = 2, 3 (rank still 1): random families, all signings.
usage: t1b_s5.py MAXM COUNT SEED"""
import os
import random
import sys
from collections import Counter
from fractions import Fraction
from math import comb
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import core

MAXM, COUNT, SEED = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
rng = random.Random(SEED)


def closed(ks):
    tot = 0
    for beta in range(-min(ks), min(ks) + 1):
        if all((k + beta) % 2 == 0 for k in ks):
            tot += comb(ks[0], (ks[0] + beta) // 2) * comb(ks[1], (ks[1] + beta) // 2) * comb(ks[2], (ks[2] + beta) // 2)
    return tot


# (a)
st = Counter(); viol = []
worst = {}
for m in range(3, MAXM + 1):
    for k0 in range(1, m - 1):
        for k1 in range(1, m - k0):
            k2 = m - k0 - k1
            if k2 < 1:
                continue
            for i in (1, 2, 3):
                q = 3 ** (i - 1); M = 3 ** i
                c = rng.randrange(q)
                e = []
                for t, k in enumerate((k0, k1, k2)):
                    e += [c + t * q + M * rng.randrange(4) for _ in range(k)]
                rng.shuffle(e)
                assert core.live(e, 3, i) and core.rank(e, 3, i) == 1
                cnt = int(core.bad(e, M).sum())
                if cnt != closed((k0, k1, k2)):
                    viol.append(('closed count', e, i, cnt))
                frac = Fraction(cnt, 2 ** m)
                if m not in worst or frac > worst[m][0]:
                    worst[m] = (frac, (k0, k1, k2))
                if m >= 7:
                    st['(a) instances with m >= 7'] += 1
                    if cnt:
                        st['(a) instances with m >= 7 and a bad signing'] += 1
                    if cnt * 16 > 3 * 2 ** m:
                        viol.append(('S5', e, i, cnt))
                else:
                    st['(a) outside the statement, m = %d: instances' % m] += 1
                    if cnt * 16 > 3 * 2 ** m:
                        st['(a) outside the statement, m = %d: inequality FAILS' % m] += 1
                    if cnt * 16 == 3 * 2 ** m:
                        st['(a) outside the statement, m = %d: equality' % m] += 1
print('(a) one occupied group, all class sizes, m = 3..%d, levels 1, 2, 3, all signings' % MAXM)
for k in sorted(st):
    print('   %-62s %d' % (k, st[k]))
print('   largest fraction of signings bad at 3^i, by m:',
      ', '.join('%d: %s %s' % (m, worst[m][0], worst[m][1]) for m in sorted(worst)))

# (b)
big = {}
for m in range(3, 151):
    best = (Fraction(0), None)
    for k0 in range(1, m - 1):
        for k1 in range(1, min(k0, m - k0 - 1) + 1):
            k2 = m - k0 - k1
            if k2 < 1 or k2 > k1:
                continue
            fr = Fraction(closed((k0, k1, k2)), 2 ** m)
            if fr > best[0]:
                best = (fr, (k0, k1, k2))
    big[m] = best
print('(b) closed count, one occupied group, every triple of sizes: largest fraction for m = 7..150 is %s = %.5f at m = %d, sizes %s; 3/16 = 0.1875'
      % max((big[m][0], float(big[m][0]), m, big[m][1]) for m in range(7, 151)))
print('   all m in 7..150 below or equal 3/16:', all(big[m][0] <= Fraction(3, 16) for m in range(7, 151)),
      '; m in 3..6:', ', '.join('%d: %s %s' % (m, big[m][0], big[m][1]) for m in range(3, 7)))
print('   m >= 14 (where A1 uses S5): largest %.5f at m = %d' % max((float(big[m][0]), m) for m in range(14, 151)))

# (c)
st = Counter()
for _ in range(COUNT):
    i = rng.choice([2, 3])
    q = 3 ** (i - 1); M = 3 ** i
    # occupied classes modulo 3^(i-1) with no live level below i
    while True:
        groups = sorted(set(rng.randrange(q) for _ in range(rng.randint(2, 4))))
        if len(groups) >= 2 and all(not core.live(groups, 3, j) for j in range(1, i)):
            break
    full = rng.choice(groups)
    e = []
    for g in groups:
        kind = 'full' if g == full else rng.choice(['full', 'even', 'even', 'two', 'random'])
        if kind == 'full':                               # three classes, small sizes
            sizes = [rng.choice([1, 1, 2, 3]) for _ in range(3)]
        elif kind == 'even':                             # one class with an even number of elements
            sizes = [0, 0, 0]; sizes[rng.randrange(3)] = rng.choice([2, 2, 4])
        elif kind == 'two':                              # two classes with two elements each
            sizes = [2, 2, 2]; sizes[rng.randrange(3)] = 0
        else:
            sizes = [rng.randint(0, 2) for _ in range(3)]
        for t in range(3):
            e += [g + t * q + M * rng.randrange(3) for _ in range(sizes[t])]
    if not 7 <= len(e) <= 14:
        st['(c) skipped (size)'] += 1
        continue
    rng.shuffle(e)
    m = len(e)
    if not (core.live(e, 3, i) and core.rank(e, 3, i) == 1):
        st['(c) skipped'] += 1
        continue
    cnt = int(core.bad(e, M).sum())
    st['(c) instances'] += 1
    if cnt:
        st['(c) instances with a bad signing'] += 1
    if cnt * 16 > 3 * 2 ** m:
        viol.append(('S5 (c)', e, i, cnt))
    ngroups = len({x % q for x in e})
    st['(c) instances with %s occupied' % ('one group' if ngroups == 1 else 'two or more groups')] += 1
    if ngroups >= 2:                                     # the plan's proof of S5 claims at most 1/8 here
        if cnt * 8 > 2 ** m:
            st['(c) two or more groups occupied and more than 1/8 bad'] += 1
            print('   MORE THAN 1/8 with two groups:', e, i, cnt)
        if cnt * 8 == 2 ** m:
            st['(c) two or more groups occupied and exactly 1/8 bad'] += 1
print('(c) two or more occupied groups, levels 2 and 3, 7 <= m <= 14, all signings')
for k in sorted(st):
    print('   %-62s %d' % (k, st[k]))
print('VIOLATIONS', len(viol))
for v in viol[:10]:
    print('   ', v)
