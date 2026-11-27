"""Do the parts give A1 in the way of the plan?  The assembly, checked numerically on families e with every signing.

For an odd n and a family e of m >= 1 elements:
  D*   = the d | n, d > 1, such that for every prime p | d the level v_p(d) of p is live;
  flat(d) = prod_{p | d} p^(rank e p (v_p d)),  T = the image of D* under flat.
Checked, exactly:
  (i)   every signing that is bad at some d | n is bad at 1 or at some d in D*          (S1, repeatedly);
  (ii)  flat is injective on D*; every t in T is odd, > 1, and mu t + 1 <= m            (S3: the hypothesis of N1);
        #bad(d) * 2^(mu(flat d)) <= 2^m for d in D*                                     (S2 with the best prime);
        if flat d = 3 and m >= 14 is even: #bad(d) * 16 <= 3 * 2^m                      (S5: flat d = 3 means d = 3^i,
        level i of 3 live, rank e 3 i = 1);
  (iii) #(bad somewhere) <= #bad(1) + sum_{d in D*} #bad(d) <= 2^m * lhsN1 m T < 2^m    (S4, N1),
        so some signing is good.
usage: t5_fit.py SEED COUNT MINM MAXM"""
import os
import random
import sys
from collections import Counter
from fractions import Fraction
from math import comb
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import core
from t1_parts import gen_family

ODD = [9, 27, 81, 15, 45, 75, 135, 225, 21, 63, 147, 35, 175, 245, 105, 315, 33, 99, 55, 77, 165, 25, 125, 49, 3, 5, 7]


def rich_family(rng, n, m):
    """elements chosen so that many levels are live: a caterpillar in every prime, then translates and repeats"""
    f = core.factor(n)
    e = [0]
    for p, a in f.items():
        L = rng.randint(1, a)
        for j in range(1, L + 1):
            for t in range(1, p):
                if len(e) < m:
                    # a number that is t * p^(j-1) modulo p^a and 0 modulo the rest of n
                    rest = n // p ** a
                    x = next(y for y in range(0, n, rest) if y % p ** a == (t * p ** (j - 1)) % p ** a)
                    e.append(x)
    while len(e) < m:
        r = rng.random()
        if r < 0.4:
            p = rng.choice(list(f))
            e.append((rng.choice(e) + rng.randrange(p) * (n // p)) % n)
        elif r < 0.7:
            e.append(rng.choice(e))
        else:
            e.append(rng.randrange(n))
    a = rng.randrange(n)
    return [(x + a) % n for x in e]


def check(n, e, st, viol):
    m = len(e)
    f = core.factor(n)
    ds = core.divisors(n)
    badv = {d: core.bad(e, d) for d in ds}
    lv = {(p, i): core.live(e, p, i) for p, a in f.items() for i in range(1, a + 1)}
    rk = {(p, i): core.rank(e, p, i) for p, a in f.items() for i in range(1, a + 1)}
    Dstar = [d for d in ds if d > 1 and all(lv[(p, i)] for p, i in core.factor(d).items())]
    flat = {}
    for d in Dstar:
        t = 1
        for p, i in core.factor(d).items():
            t *= p ** rk[(p, i)]
        flat[d] = t
    T = set(flat.values())
    st['families'] += 1
    st['families with m = %2d' % m] += 1
    st['levels in D* (total)'] += len(Dstar)
    # (i)
    anybad = np.zeros(2 ** m, dtype=bool)
    for d in ds:
        anybad |= badv[d]
    star = badv[1].copy()
    for d in Dstar:
        star |= badv[d]
    if np.any(anybad & ~star):
        viol.append(('(i)', n, e))
    # (ii)
    if len(T) != len(Dstar):
        viol.append(('flat not injective', n, e))
    for t in T:
        if not (t % 2 == 1 and t > 1 and core.mu(t) + 1 <= m):
            viol.append(('hT', n, e, t))
    total_bound = Fraction(comb(m, m // 2), 2 ** m) if m % 2 == 0 else Fraction(0)
    cnt1 = int(badv[1].sum())
    if Fraction(cnt1, 2 ** m) != total_bound:
        viol.append(('S4', n, e))
    ssum = cnt1
    for d in Dstar:
        c = int(badv[d].sum())
        ssum += c
        mt = core.mu(flat[d])
        if c * 2 ** mt > 2 ** m:
            viol.append(('S2 best prime', n, e, d))
        if flat[d] == 3 and m >= 14 and m % 2 == 0:
            st['uses of S5 (flat d = 3, m >= 14 even)'] += 1
            assert core.factor(d).keys() == {3} and rk[(3, core.factor(d)[3])] == 1 and lv[(3, core.factor(d)[3])]
            if c * 16 > 3 * 2 ** m:
                viol.append(('S5', n, e, d))
    lhs = core.lhsN1(m, T)
    nb = int(anybad.sum())
    # (iii)
    if not (nb <= ssum):
        viol.append(('union', n, e))
    if not (Fraction(ssum, 2 ** m) <= lhs):
        viol.append(('sum <= lhsN1', n, e, ssum, lhs))
    if not lhs < 1:
        viol.append(('N1', n, e, lhs))
    st['largest lhsN1 m T seen (x 10^6)'] = max(st['largest lhsN1 m T seen (x 10^6)'], int(lhs * 10 ** 6))
    st['largest fraction of bad signings seen (x 10^6)'] = max(st['largest fraction of bad signings seen (x 10^6)'],
                                                             nb * 10 ** 6 // 2 ** m)
    if nb == 2 ** m:
        viol.append(('NO GOOD SIGNING', n, e))
    if anybad[-1]:
        st['families for which "all +" is bad'] += 1


if __name__ == '__main__':
    seed, count, minm, maxm = (int(x) for x in sys.argv[1:5])
    rng = random.Random(seed)
    st = Counter(); viol = []
    for _ in range(count):
        n = rng.choice(ODD)
        if rng.random() < 0.5:
            e = rich_family(rng, n, rng.randint(minm, maxm))
        else:
            while True:
                e = gen_family(rng, n, maxm)
                if minm <= len(e) <= maxm:
                    break
        check(n, e, st, viol)
    print('seed', seed, 'count', count, 'sizes', minm, 'to', maxm)
    for k in sorted(st):
        print('   %-55s %d' % (k, st[k]))
    print('   VIOLATIONS', len(viol))
    for v in viol[:10]:
        print('      ', v)
