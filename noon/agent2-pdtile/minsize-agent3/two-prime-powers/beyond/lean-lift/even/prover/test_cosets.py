"""Corollary N, directly, for every odd e | n' (several primes above 2 included): over all signings of a multiset that are
bad at 2^j e for some j, the vector lambda_e(N) = sum_{x in N} X^{w_x} mod (2, Phi_e) takes at most TWO values; and at
most one level j has a value different from the others' (the special level).  All signings, exact."""
import sys, itertools, random
import numpy as np
from lib import *
from test_D import gen

def check(n, els, st):
    k, n1 = two_part(n); m = len(els)
    signs = all_signs(m, fix_first=False); idx = [x % n for x in els]
    neg = (signs == -1).astype(np.int64)
    for e in divisors(n1):
        lam = (neg @ table(e, n)[idx]) % 2                      # one row per signing: lambda_e(N) as a vector over F_2
        per_level = {}
        for j in range(k + 1):
            badm = ~np.any(signs @ table(2 ** j * e, n)[idx], axis=1)
            vals = {tuple(r) for r in lam[badm]}
            assert len(vals) <= 1, ('two values at one level', n, els, e, j)
            if vals: per_level[j] = next(iter(vals))
        distinct = set(per_level.values())
        assert len(distinct) <= 2, ('more than two cosets', n, els, e)
        if len(distinct) == 2:
            # one of the two values occurs at exactly one level
            counts = sorted(sum(1 for v in per_level.values() if v == d) for d in distinct)
            assert counts[0] == 1, ('no single special level', n, els, e, per_level); st['two'] += 1
        elif len(distinct) == 1: st['one'] += 1
        else: st['none'] += 1
    st['n'] += 1

random.seed(71)
st = dict(n=0, none=0, one=0, two=0)
for n in (6, 12, 24, 30, 60, 120, 42, 84, 70, 140, 90, 210, 126, 330, 14, 28, 56, 62, 124, 146):
    if n <= 30:
        for m in range(1, (5 if n <= 12 else 4) + 1):
            for rest in itertools.combinations_with_replacement(range(n), m - 1): check(n, [0] + list(rest), st)
    for trial in range(240):
        els = gen(n, random.randint(3, 10), trial % 6)
        if els: check(n, els[:10], st)
    print(f'n={n} done; totals {st}', flush=True)
