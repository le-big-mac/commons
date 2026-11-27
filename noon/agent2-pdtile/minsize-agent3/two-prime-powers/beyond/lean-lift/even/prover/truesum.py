"""Where the count stands when 3 | n: for each multiset (exceptional pairs left out) the TRUE shares
P_e = share of signings bad at 2^j e for some j, summed over e = 1 and the live e > 1 (the union bound over e with
nothing lost inside a level), next to the share of signings bad somewhere.  If the largest sum is < 1 the missing
part is sharper bounds per e; if it reaches 1 the overlaps between different e must be used."""
import sys, itertools, random
from fractions import Fraction
import numpy as np
from lib import *
from test_D import primes_of, gen

def sums(n, els):
    k, n1 = two_part(n); m = len(els)
    signs = all_signs(m, fix_first=True); idx = [x % n for x in els]; tot = len(signs)
    bad = {d: ~np.any(signs @ table(d, n)[idx], axis=1) for d in divisors(n)}
    def live(e):
        for p in primes_of(e):
            i = 0
            while e % p ** (i + 1) == 0: i += 1
            groups = {}
            for x in els: groups.setdefault(x % p ** (i - 1), set()).add(x % p ** i)
            if not any(len(s) == p for s in groups.values()): return False
        return True
    s = Fraction(0); allbad = np.zeros(tot, bool)
    for e in divisors(n1):
        anyj = np.zeros(tot, bool)
        for j in range(k + 1): anyj |= bad[2 ** j * e]
        allbad |= anyj
        if e == 1 or live(e): s += Fraction(int(anyj.sum()), tot)
    return s, Fraction(int(allbad.sum()), tot)

random.seed(53)
for n in (6, 12, 18, 24, 30, 36, 60, 90):
    best = {}
    def see(els):
        if exceptional_pair(n, els): return
        s, b = sums(n, els); par = len(els) % 2
        if par not in best or s > best[par][0]: best[par] = (s, b, els)
    if n <= 30:
        for m in range(1, (6 if n <= 12 else 5 if n <= 18 else 4) + 1):
            for rest in itertools.combinations_with_replacement(range(n), m - 1): see([0] + list(rest))
    for trial in range(600):
        els = gen(n, random.randint(3, 11), trial % 6)
        if els: see(els)
    for par in (1, 0):
        s, b, els = best[par]
        print(f'n={n}, m {"odd" if par else "even"}: largest sum of true shares {s} = {float(s):.4f} (share bad somewhere {float(b):.4f}) at {sorted(els)}', flush=True)
