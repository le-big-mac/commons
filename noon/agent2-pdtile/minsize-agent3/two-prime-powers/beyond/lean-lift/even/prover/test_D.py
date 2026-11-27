"""Theorem D (3 does not divide n) and Proposition P (every n): test of every step of the count, all signings, exact.
For n = 2^k n' and a multiset:
 (1) step-down: a signing bad at some d | n is bad at some 2^j e with e = 1 or e LIVE (for every prime power p^i || e,
     level i of the p-tree has a full group);
 (2) for every live e > 1:  share of signings bad at 2^j e for some j in 0..k  <=  2 * 2^(-D_e),
     D_e = rank over F_2 of the vectors X^w mod (2, Phi_e), w the residues of the elements;  and
     D_e >= max over p | e of (p-1) * (number of live levels of p up to v_p(e));
 (3) e = 1: share of signings bad at some 2^j is 0 for m odd and <= 3/4 for m even >= 4 (exceptional pairs apart);
 (4) share of signings bad somewhere <= (3) + sum over live e > 1 of 2^(1 - D_e)."""
import sys, itertools, random
from fractions import Fraction
import numpy as np
from lib import *

def primes_of(n):
    ps = []; q = 3
    while n % 2 == 0: n //= 2
    while n > 1:
        if n % q == 0:
            ps.append(q)
            while n % q == 0: n //= q
        q += 2
    return ps

def rank2(rows):
    rows = [int(''.join(str(int(c) % 2) for c in r), 2) for r in rows]; rk = 0
    while rows:
        piv = max(rows); rows.remove(piv)
        if piv == 0: continue
        rk += 1; hb = piv.bit_length()
        rows = [r ^ piv if r.bit_length() == hb else r for r in rows]
    return rk

def check(n, els, st):
    k, n1 = two_part(n); m = len(els)
    signs = all_signs(m, fix_first=True); idx = [x % n for x in els]; tot = len(signs)
    bad = {d: ~np.any(signs @ table(d, n)[idx], axis=1) for d in divisors(n)}
    live = {}
    for p in primes_of(n):
        a_ = 0
        while n1 % p ** (a_ + 1) == 0: a_ += 1
        for i in range(1, a_ + 1):
            groups = {}
            for x in els: groups.setdefault(x % p ** (i - 1), set()).add(x % p ** i)
            live[(p, i)] = any(len(s) == p for s in groups.values())
    def is_live(e):
        for p in primes_of(e):
            i = 0
            while e % p ** (i + 1) == 0: i += 1
            if not live[(p, i)]: return False
        return True
    covered = np.zeros(tot, bool); bound = Fraction(0)
    for e in divisors(n1):
        if e > 1 and not is_live(e): continue
        anyj = np.zeros(tot, bool)
        for j in range(k + 1): anyj |= bad[2 ** j * e]
        covered |= anyj; sh = Fraction(int(anyj.sum()), tot)
        if e == 1:
            if m % 2: assert sh == 0
            elif m >= 4: assert sh <= Fraction(3, 4), ('e=1', n, els, sh); st['max1'] = max(st['max1'], float(sh))
            bound += sh if m < 4 else (0 if m % 2 else Fraction(3, 4))
        else:
            D = rank2([table(e, n)[x] for x in idx])
            mu = 0
            for p in primes_of(e):
                i = 0
                while e % p ** (i + 1) == 0: i += 1
                mu = max(mu, (p - 1) * sum(1 for t in range(1, i + 1) if live[(p, t)]))
            assert D >= mu, ('rank', n, els, e, D, mu)
            b = Fraction(2, 2 ** D)
            assert sh <= b, ('level', n, els, e, sh, b); st['levels'] += 1; st['maxratio'] = max(st['maxratio'], float(sh / b))
            bound += b
    allbad = np.zeros(tot, bool)
    for d in bad: allbad |= bad[d]
    assert not (allbad & ~covered).any(), ('step-down', n, els)
    sh = Fraction(int(allbad.sum()), tot)
    assert sh <= bound, ('total', n, els, sh, bound)
    if sh == 1: assert exceptional_pair(n, els); st['exceptional'] += 1
    elif n % 3 and m >= 5: assert bound < 1, ('Theorem D bound not below 1', n, els, bound); st['closed'] += 1
    st['n'] += 1; st['worst_bound_3free'] = max(st['worst_bound_3free'], float(bound)) if (n % 3 and m >= 5) else st['worst_bound_3free']

def gen(n, m, kind):
    k, n1 = two_part(n); q = 2 ** k
    if kind == 0: return [random.randrange(n) for _ in range(m)]
    if kind == 1:
        half = [random.randrange(n // 2) for _ in range(m // 2)]; return half + [x + n // 2 for x in half]
    if kind == 2:
        step = random.choice([d for d in divisors(n) if 1 < d < n]); els = []
        while len(els) < m:
            c = random.randrange(step); els += [(c + t * step) % n for t in range(n // step)]
        return els[:11]
    if kind == 3:
        s = random.randrange(n); return [(s + t) % n for t in range(m)]
    if kind == 4:  # every element with a twin in the same class modulo n' (unsigned mask 0 modulo 2 at every e)
        els = []
        for _ in range(m // 2):
            x = random.randrange(n); els += [x, (x + n1 * random.randrange(q)) % n]
        return els
    # full levels of one odd prime, few classes otherwise
    p = random.choice(primes_of(n)); base = random.randrange(n); els = [(base + r * (n // p)) % n for r in range(p)]
    while len(els) < m: els.append((random.choice(els) + n1 * random.randrange(q)) % n)
    return els[:11]

def main(arg):
    random.seed(41 if arg == 'a' else 43)
    st = dict(n=0, levels=0, maxratio=0.0, max1=0.0, closed=0, exceptional=0, worst_bound_3free=0.0)
    mods = (10, 20, 40, 14, 28, 56, 50, 70, 140, 22, 44, 110) if arg == 'a' else (6, 12, 24, 18, 36, 30, 60, 90, 42, 84, 35, 55, 15, 45, 105)
    for n in mods:
        if n <= 30:
            for m in range(1, (5 if n <= 20 else 4) + 1):
                for rest in itertools.combinations_with_replacement(range(n), m - 1): check(n, [0] + list(rest), st)
        for trial in range(480):
            m = random.randint(3, 11); els = gen(n, m, trial % 6)
            if els: check(n, els, st)
        print(f'n={n} done; totals {st}', flush=True)

if __name__ == '__main__':
    main(sys.argv[1])
