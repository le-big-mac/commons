"""Theorem D (iii) (m odd, n = 2^k 3^a 5^b) and Lemma Q (dangerous levels of one prime), all signings, exact.
For a multiset with an odd number of elements on Z_n:
 (a) an odd e that is not dangerous (sum_x X^{w_x} not 0 modulo (2, Phi_e)) has no bad signing at any 2^j e;
 (b) if p^i is dangerous, level i of p is live, and D_{p^i} >= (p-1) p^(l-1), l = the number of dangerous levels of p up to i;
 (c) share of signings bad somewhere <= sum over the live dangerous e > 1 of 2^(1 - D_e); this sum is printed (largest),
     and is asserted < 1 when n has no prime factor other than 2, 3, 5."""
import sys, itertools, random
from fractions import Fraction
import numpy as np
from lib import *
from test_D import primes_of, rank2, gen

def check(n, els, st):
    k, n1 = two_part(n); m = len(els); assert m % 2 == 1
    signs = all_signs(m, fix_first=True); idx = [x % n for x in els]; tot = len(signs)
    bad = {d: ~np.any(signs @ table(d, n)[idx], axis=1) for d in divisors(n)}
    dang = {e: not np.any(table(e, n)[idx].sum(axis=0) % 2) for e in divisors(n1)}
    assert not dang[1]
    def live_lv(p, i):
        groups = {}
        for x in els: groups.setdefault(x % p ** (i - 1), set()).add(x % p ** i)
        return any(len(s) == p for s in groups.values())
    def live(e):
        for p in primes_of(e):
            i = 0
            while e % p ** (i + 1) == 0: i += 1
            if not live_lv(p, i): return False
        return True
    bound = Fraction(0); allbad = np.zeros(tot, bool)
    for e in divisors(n1):
        anyj = np.zeros(tot, bool)
        for j in range(k + 1): anyj |= bad[2 ** j * e]
        allbad |= anyj
        if not dang[e]:
            assert not anyj.any(), ('not dangerous but bad', n, els, e); st['free'] += 1
            continue
        D = rank2([table(e, n)[x] for x in idx])
        ps = primes_of(e)
        if len(ps) == 1:
            p = ps[0]; i = 0
            while e % p ** (i + 1) == 0: i += 1
            l = sum(1 for t in range(1, i + 1) if dang[p ** t])
            assert live_lv(p, i), ('dangerous prime power not live', n, els, e)
            assert D >= (p - 1) * p ** (l - 1), ('Lemma Q', n, els, e, D, l); st['Q'] += 1
        if live(e): bound += Fraction(2, 2 ** D)
    sh = Fraction(int(allbad.sum()), tot)
    assert sh <= bound, ('total', n, els, sh, bound)
    if all(p in (3, 5) for p in primes_of(n)): assert bound < 1, ('bound', n, els, bound)
    st['max'] = max(st['max'], float(bound)); st['maxtrue'] = max(st['maxtrue'], float(sh)); st['n'] += 1

random.seed(83)
st = dict(n=0, free=0, Q=0, max=0.0, maxtrue=0.0)
for n in (30, 60, 90, 150, 180, 270, 450, 45, 135, 225, 18, 54, 50, 210, 630, 105):
    if n <= 30:
        for m in (1, 3, 5):
            if m == 5 and n > 18: continue
            for rest in itertools.combinations_with_replacement(range(n), m - 1): check(n, [0] + list(rest), st)
    for trial in range(300):
        els = gen(n, random.choice((3, 5, 7, 9, 11)), trial % 6)[:11]
        if len(els) % 2 == 0: els = els[:-1]
        if els: check(n, els, st)
    # sets with one element in every class modulo 9, 15, 25, 27 (many dangerous levels at once)
    for q in (9, 15, 25, 27, 45):
        if n1q := (n % q == 0):
            base = [(r + q * random.randrange(n // q)) % n for r in range(q)]
            for cut in (9, 11):
                els = base[:cut] if cut % 2 else base[:cut - 1]
                check(n, els, st)
            if q <= 11: check(n, base, st)
    print(f'n={n} done; totals {st}', flush=True)
