"""Do the fixed parts give A' ?  The plan's argument for A', step by step, on families with every signing.

n prime to 3, n = 2^k n'', e a family of m >= 3 exponents.  Live := the t | n'', t > 1, such that for every prime p of t
the level v_p(t) of p is live; t* := prod p^(rank e p v_p(t)).
 (i)   [S1' only]  every signing 3-bad at d = 2^j d' (d' | n'') is 3-bad at 2^j or at 2^j t for some t in Live, t | d'.
 (ii)  [S2' with the rank, finished rank_lt_card and injectivity]  t -> t* is injective on Live; t* > 1 is prime to 6;
       #bad3(t) * 2^mu(t*) <= 2^m for the best prime (and so for mu(t*)); Live is empty when m <= 4.
 (iii) [L, E1, N1']  #(signings 3-bad somewhere) <= sum over t in {1} + Live of #(3-bad at 2^j t for some j <= k)
       <= 2 #bad3(1) + 2 sum over Live of #bad3(t) <= 2 (2^m + 2)/3 + 2 * 2^m * sum 2^(-mu(t*)), the last sum < 1/8,
       and the total is < 2^m  (m = 3, 4: 2 #bad3(1) < 2^m).
usage: t7_fit.py SEED COUNT
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import random
import time
from fractions import Fraction
from math import gcd
import numpy as np
from ecore import *


def gen(n, m):
    f = factor(n)
    kind = random.random()
    if kind < 0.25:
        return [random.randrange(0, n) for _ in range(m)]
    if kind < 0.6:
        # a full set of residues modulo a prime power level of an odd prime of n, the rest repeated or random
        ps = [p for p in f if p > 2]
        if not ps:
            return [random.randrange(0, n) for _ in range(m)]
        p = random.choice(ps)
        i = random.randint(1, f[p])
        r = random.randrange(0, n)
        e = [(r + t * (n // p ** i) * random.choice([1, 1, 2 if p > 2 else 1])) % n for t in range(p)]
        if random.random() < 0.5:
            e = [(r + t * p ** (i - 1) + random.randrange(0, n // p ** i) * p ** i * random.choice([0, 1])) % n
                 for t in range(p)]
        e = e[:m]
        while len(e) < m:
            e.append(random.choice(e) if random.random() < 0.6 else random.randrange(0, n))
        return e
    if kind < 0.8:
        # few residues modulo the power of 2, any residues modulo the odd part
        k2 = 2 ** f.get(2, 0)
        cl = [random.randrange(0, k2) for _ in range(2)]
        return [(random.choice(cl) + k2 * random.randrange(0, n // k2)) % n for _ in range(m)]
    base = [random.randrange(0, n) for _ in range(random.randint(2, 3))]
    return [random.choice(base) for _ in range(m)]


def main():
    seed, count = int(sys.argv[1]), int(sys.argv[2])
    random.seed(seed)
    t0 = time.time()
    ns = [2, 4, 8, 16, 5, 10, 20, 40, 80, 25, 50, 100, 7, 14, 28, 56, 35, 70, 140, 280, 175, 55, 110, 220, 49, 98]
    st = dict(fam=0, i_checks=0, i_viol=0, live_levels=0, fam_with_live=0, inj_viol=0, star_viol=0, s2_viol=0,
              small_live=0, cover_viol=0, L_viol=0, sum_viol=0, final_viol=0, e1_viol=0, s2_eq=0)
    max_share = Fraction(0)
    max_ex = None
    max_sum = Fraction(0)
    by_m = {}
    for trial in range(count):
        n = random.choice(ns)
        m = random.randint(3, 10 if n <= 140 else 9)
        e = gen(n, m)
        f = factor(n)
        k = f.get(2, 0)
        n2 = n // 2 ** k
        st['fam'] += 1
        B = {d: bad3(e, d) for d in divisors(n)}
        Live = [t for t in divisors(n2) if t > 1 and all(live(e, p, a) for p, a in factor(t).items())]
        stars = {}
        for t in Live:
            s = 1
            for p, a in factor(t).items():
                s *= p ** rank(e, p, a)
            stars[t] = s
        if Live:
            st['fam_with_live'] += 1
            st['live_levels'] += len(Live)
            if m <= 4:
                st['small_live'] += 1
        # (i)
        for d in divisors(n):
            j = factor(d).get(2, 0)
            dp = d // 2 ** j
            cover = B[2 ** j].copy()
            for t in Live:
                if dp % t == 0:
                    cover |= B[2 ** j * t]
            st['i_checks'] += 1
            if np.any(B[d] & ~cover):
                st['i_viol'] += 1
                print("  (i) VIOLATION", n, e, d)
        # (ii)
        if len(set(stars.values())) != len(stars):
            st['inj_viol'] += 1
            print("  injectivity VIOLATION", n, e, stars)
        for t, s in stars.items():
            if not (s > 1 and gcd(s, 6) == 1):
                st['star_viol'] += 1
            nb = int(B[t].sum())
            if nb * 2 ** mu(s) > 2 ** m:
                st['s2_viol'] += 1
                print("  S2 VIOLATION", n, e, t, s)
            if nb * 2 ** mu(s) == 2 ** m:
                st['s2_eq'] += 1
        # (iii)
        U = np.zeros(1 << m, dtype=bool)
        for d in divisors(n):
            U |= B[d]
        nU = int(U.sum())
        ladder = {}
        for t in [1] + Live:
            acc = np.zeros(1 << m, dtype=bool)
            for j in range(k + 1):
                acc |= B[2 ** j * t]
            ladder[t] = int(acc.sum())
            if ladder[t] > 2 * int(B[t].sum()):
                st['L_viol'] += 1
                print("  L VIOLATION", n, e, t)
        if nU > sum(ladder.values()):
            st['cover_viol'] += 1
            print("  cover VIOLATION", n, e)
        b1 = int(B[1].sum())
        if 3 * b1 + (0 if m % 2 == 0 else 2) != 2 ** m + (2 if m % 2 == 0 else 0):
            st['e1_viol'] += 1
        ssum = sum(Fraction(1, 2 ** mu(s)) for s in stars.values())
        max_sum = max(max_sum, ssum)
        if not ssum < Fraction(1, 8):
            st['sum_viol'] += 1
            print("  N1' VIOLATION", n, e, stars)
        bound = 2 * b1 + 2 * sum(Fraction(2 ** m, 2 ** mu(s)) for s in stars.values())
        if not (nU <= bound < 2 ** m):
            st['final_viol'] += 1
            print("  final VIOLATION", n, e, nU, bound)
        share = Fraction(nU, 2 ** m)
        by_m.setdefault(m, Fraction(0))
        if share > by_m[m]:
            by_m[m] = share
        if share > max_share:
            max_share = share
            max_ex = (n, e)
        if time.time() - t0 > 250:
            print("  (stopped by the clock)")
            break
    print(f"fit seed {seed}: families {st['fam']} (n in {ns}, m = 3..10), with a live t {st['fam_with_live']} "
          f"({st['live_levels']} live t in all)")
    print(f"  (i) checks (family, d) {st['i_checks']}, violations {st['i_viol']}")
    print(f"  (ii) t -> t* not injective: {st['inj_viol']}; t* not > 1 or not prime to 6: {st['star_viol']}; "
          f"#bad3(t) 2^mu(t*) > 2^m: {st['s2_viol']} (equality {st['s2_eq']}); families with m <= 4 and a live t: "
          f"{st['small_live']}")
    print(f"  (iii) union not covered by the ladders: {st['cover_viol']}; ladder > 2 #bad3(t): {st['L_viol']}; E1 count "
          f"wrong: {st['e1_viol']}; sum of 2^(-mu(t*)) >= 1/8: {st['sum_viol']} (largest sum met {max_sum} = "
          f"{float(max_sum):.5f}); final bound not < 2^m or below the true count: {st['final_viol']}")
    print(f"  largest share of signings 3-bad somewhere: {max_share} at {max_ex}; by m: "
          f"{ {mm: str(v) for mm, v in sorted(by_m.items())} }")
    print(f"  ({time.time() - t0:.0f} s)")


main()
