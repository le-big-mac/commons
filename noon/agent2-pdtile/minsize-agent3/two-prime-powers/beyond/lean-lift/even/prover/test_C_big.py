"""(a) n = 2^k: the share of good signings is 1 for m odd and at least 1/2 - c_m for even m >= 4 (Theorem A', by Lemma N
at e = 1); exhaustive on small cases.  (b) n = 2^k p^a, larger cases, random signings tested exactly: is a good signing
found, and how many of the tried signings are good (Theorem C promises a positive share for p >= 5, and for p = 3, m odd)."""
import sys, itertools, random
from math import comb
from fractions import Fraction
import numpy as np
from lib import *

def part_a():
    for k, M in ((1, 10), (2, 9), (3, 7), (4, 6)):
        n = 2 ** k
        for m in range(1, M + 1):
            least = None; arg = None
            for rest in itertools.combinations_with_replacement(range(n), m - 1):
                els = [0] + list(rest)
                if exceptional_pair(n, els): continue
                _, g = good_signings(n, els); fr = Fraction(int(g.sum()), len(g))
                if least is None or fr < least: least, arg = fr, els
            lb = Fraction(1) if m % 2 else (Fraction(1, 2) - Fraction(comb(m, m // 2), 2 ** m))
            assert m == 2 or least >= lb, (n, m, least, lb)
            print(f'n={n} m={m}: least share of good signings (exceptional pairs left out) {least} at {arg}; bound of Theorem A\': {lb if m != 2 else "-"}', flush=True)

def part_b():
    random.seed(31); rows = []
    for p, k, a_ in ((5, 3, 1), (5, 4, 2), (5, 6, 1), (7, 3, 1), (7, 5, 1), (11, 3, 1), (13, 4, 1), (3, 3, 2), (3, 5, 3), (3, 6, 1)):
        n = 2 ** k * p ** a_
        for kind in ('random', 'closed', 'cosets', 'interval', 'fullp'):
            for m in ((7, 12, 13, 20, 31) if p != 3 else (7, 12, 13, 20, 31)):
                if kind == 'random': els = [random.randrange(n) for _ in range(m)]
                elif kind == 'closed':
                    half = random.sample(range(n // 2), min(m // 2, n // 2)); els = half + [x + n // 2 for x in half]
                elif kind == 'cosets':
                    step = random.choice([d for d in divisors(n) if 1 < d < n and n // d <= m]); els = []
                    cs = random.sample(range(step), min(step, m))
                    for c in cs:
                        els += [(c + t * step) % n for t in range(n // step)]
                        if len(els) >= m: break
                    els = els[:m]
                elif kind == 'interval':
                    s = random.randrange(n); els = [(s + t) % n for t in range(m)]
                else:
                    els = [(r + p * random.randrange(n // p)) % n for r in range(p)]
                    while len(els) < m: els.append((random.choice(els) + p ** a_ * random.randrange(2 ** k)) % n)
                    els = els[:max(m, p)]
                good = 0; T = 40
                for _ in range(T):
                    sg = [random.choice((1, -1)) for _ in els]
                    good += is_good(mask(n, els, sg), n)
                rows.append((p, n, kind, len(els), good, T))
                assert good > 0 or exceptional_pair(n, els), (n, els)
        sub = [r for r in rows if r[1] == n]
        print(f'n={n} (p={p}): {len(sub)} multisets (random, closed under +n/2, cosets, intervals, full p-levels; 7 to 31 elements), 40 random signings each: '
              f'least number good {min(r[4] for r in sub)}, at odd m {min(r[4] for r in sub if r[3] % 2)}, at even m {min(r[4] for r in sub if r[3] % 2 == 0)}', flush=True)

if __name__ == '__main__':
    part_a() if sys.argv[1] == 'a' else part_b()
