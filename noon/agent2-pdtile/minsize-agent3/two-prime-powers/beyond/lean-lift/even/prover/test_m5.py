"""Five elements, every n (the referee's remark, item 1 of its report): with five elements no prime >= 7 has a live
level, so the live e are 3^i 5^i' and the count of Theorem D (iii) applies.  For multisets of five elements on moduli
with further odd primes: (a) every live e > 1 is of the form 3^i 5^i'; (b) the sum over the live dangerous e > 1 of
2^(1 - D_e) is below 1 (and at least the true share of bad signings, all signings, exact); (c) a good signing exists."""
import sys, itertools, random
from fractions import Fraction
import numpy as np
from lib import *
from test_D import primes_of, rank2, gen

def check(n, els, st):
    k, n1 = two_part(n); m = len(els); assert m == 5
    signs = all_signs(m, fix_first=True); idx = [x % n for x in els]; tot = len(signs)
    def live_lv(p, i):
        groups = {}
        for x in els: groups.setdefault(x % p ** (i - 1), set()).add(x % p ** i)
        return any(len(s) == p for s in groups.values())
    bound = Fraction(0); allbad = np.zeros(tot, bool)
    for e in divisors(n1):
        for j in range(k + 1): allbad |= ~np.any(signs @ table(2 ** j * e, n)[idx], axis=1)
        if e == 1: continue
        lv = True
        for p in primes_of(e):
            i = 0
            while e % p ** (i + 1) == 0: i += 1
            if not live_lv(p, i): lv = False; break
        if not lv: continue
        assert all(p in (3, 5) for p in primes_of(e)), ('live e with a prime >= 7', n, els, e)
        T = table(e, n)
        if np.any(T[idx].sum(axis=0) % 2): continue          # not dangerous
        bound += Fraction(2, 2 ** rank2([T[x] for x in idx]))
    sh = Fraction(int(allbad.sum()), tot)
    assert sh <= bound < 1, ('bound', n, els, sh, bound)
    st['n'] += 1; st['maxbound'] = max(st['maxbound'], float(bound)); st['maxbad'] = max(st['maxbad'], float(sh))

random.seed(97)
st = dict(n=0, maxbound=0.0, maxbad=0.0)
for n in (30, 42, 70, 210, 126, 330, 630, 1050, 390, 2310):
    if n <= 42:
        for rest in itertools.combinations_with_replacement(range(n), 4): check(n, [0] + list(rest), st)
    for trial in range(1500):
        kind = trial % 4
        if kind == 0: els = [random.randrange(n) for _ in range(5)]
        elif kind == 1: s = random.randrange(n); els = [(s + t) % n for t in range(5)]
        elif kind == 2:   # one element in every class modulo 5, residues modulo 3 spread, the rest random
            els = [(r + 5 * random.randrange(n // 5)) % n for r in range(5)] if n % 5 == 0 else [random.randrange(n) for _ in range(5)]
        else:             # {0,1,2} modulo 3 scaled, plus two elements
            els = [(t * (n // 3) + random.choice((0, n // 2))) % n for t in range(3)] + [random.randrange(n), random.randrange(n)] if n % 3 == 0 else [random.randrange(n) for _ in range(5)]
        check(n, els, st)
    print(f'n={n} done; totals {st}', flush=True)
