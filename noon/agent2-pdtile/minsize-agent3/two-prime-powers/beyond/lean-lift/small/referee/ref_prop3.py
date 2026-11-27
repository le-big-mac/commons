"""Referee's test of section 3 / Proposition 3 of small-multisets.md: contract levels (of any tree) as long as some level
is contractible.  Checked for each multiset B of m elements on Z_n:
  - the process ends on Z_nflat with nflat dividing n'_m = product over odd primes p <= m of p^floor((m-1)/(p-1));
  - at the end no level of any tree is contractible, i.e. at every level some group has all p subclasses occupied;
  - EVERY signing that is good for the last multiset is good for B (all 2^(m-1) signings, exact);
  - whether the last group depends on the order in which levels are contracted (two orders are tried: lowest prime and
    lowest level first; highest prime and highest level first).
usage: ref_prop3.py SEED COUNT"""
import sys, random
import numpy as np
from reflib import *


def nprime(m):
    out = 1
    for p in range(3, m + 1):
        if all(p % d for d in range(2, int(p ** 0.5) + 1)):
            out *= p ** ((m - 1) // (p - 1))
    return out


def full_contract(el, n, order):
    steps = []
    while True:
        f = factor(n)
        cand = [(p, t) for p in sorted(f) for t in range(1, f[p] + 1) if contractible(el, p, f[p], t)]
        if not cand:
            return el, n, steps
        p, t = cand[0] if order == 0 else cand[-1]
        el = contract(el, n, p, f[p], t); n //= p
        steps.append((p, t))


if __name__ == '__main__':
    rng = random.Random(int(sys.argv[1])); count = int(sys.argv[2])
    shapes = [45, 135, 405, 225, 675, 315, 945, 1575, 525, 1155, 3465, 189, 441, 1323, 243, 729, 375, 875, 2835, 2475, 2025]
    tot = dict(multisets=0, signings=0, bad_B=0, good_flat=0, viol=0, conv=0, order_differs=0, uncontracted=0, steps=0)
    worst = None
    for _ in range(count):
        n = rng.choice(shapes); f = factor(n); m = rng.randint(2, 9)
        kind = rng.randrange(5)
        if kind == 0:
            el = [rng.randrange(n) for _ in range(m)]
        elif kind == 1:
            d = rng.choice([x for x in divisors(n) if x > 1]); c = rng.randrange(n)
            el = [(c + (n // d) * rng.randrange(d)) % n for _ in range(m)]
        elif kind == 2 or kind == 3:
            el = []
            while len(el) < m:
                q = rng.choice(list(f)); i = rng.randrange(f[q]); c = rng.randrange(n)
                step = q ** i * (n // q ** f[q]) if kind == 2 else n // q
                if len(el) + q <= m and rng.random() < 0.85:
                    el += [(c + step * j) % n for j in range(q)]
                else:
                    el.append(rng.choice(el) if el and rng.random() < 0.3 else rng.randrange(n))
        else:                                       # a 'caterpillar' in the 3-tree: one full group at every level
            a = f.get(3, 0); el = [0]
            for i in range(a):
                if len(el) + 2 <= m: el += [3 ** i * (n // 3 ** a) % n, 2 * 3 ** i * (n // 3 ** a) % n]
            while len(el) < m: el.append(rng.randrange(n))
            c = rng.randrange(n); el = [(x + c) % n for x in el]
        fl, nf, steps = full_contract(el, n, 0)
        fl2, nf2, steps2 = full_contract(el, n, 1)
        assert nprime(m) % nf == 0 and nprime(m) % nf2 == 0, ('n-flat does not divide n\'_m', n, el, nf, nf2)
        for p, a in factor(nf).items():             # no contractible level left = some group full at every level
            for t in range(1, a + 1):
                occ = {}
                for x in fl:
                    u = x % p ** a
                    occ.setdefault(u % p ** (t - 1), set()).add((u // p ** (t - 1)) % p)
                assert any(len(v) == p for v in occ.values())
        g = good_all(n, el); gf = good_all(nf, fl); gf2 = good_all(nf2, fl2)
        v = int((gf & ~g).sum()) + int((gf2 & ~g).sum())
        if v:
            print('VIOLATION of Proposition 3:', n, el, steps, nf, fl); sys.exit(1)
        tot['multisets'] += 1; tot['signings'] += len(g); tot['bad_B'] += int((~g).sum()); tot['good_flat'] += int(gf.sum())
        tot['conv'] += int((g & ~gf).sum()); tot['order_differs'] += (nf != nf2); tot['uncontracted'] += (nf == n)
        tot['steps'] += len(steps)
        if worst is None or nf > worst[0]: worst = (nf, n, m, el)
    print(f'Proposition 3 (seed {sys.argv[1]}): {tot["multisets"]} multisets of 2..9 elements on the groups {shapes}')
    print(f'   signings {tot["signings"]}, bad for B {tot["bad_B"]}, good for the last multiset {tot["good_flat"]} (each of them good for B: '
          f'violations {tot["viol"]}), good for B and bad for the last multiset {tot["conv"]}')
    print(f'   contractions made {tot["steps"]}; multisets with nothing to contract {tot["uncontracted"]}; '
          f'multisets where the two orders end on groups of different order: {tot["order_differs"]}')
    print(f'   every last group order divides n\'_m; the largest last group: Z_{worst[0]} from Z_{worst[1]}, m = {worst[2]}, B = {worst[3]}')
