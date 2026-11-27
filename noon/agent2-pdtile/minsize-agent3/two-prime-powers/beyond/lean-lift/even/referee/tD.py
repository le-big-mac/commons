# Proposition P and Theorem D by brute force over ALL signings (exact remainders), written from the statements.
# For every multiset B on Z_n tested:
#   S1 : for every prime p | n (2 included) and every d | n with p^i || d: if level i of the p-tree of B is not
#        live, then every signing bad at d is bad at d/p.   (This is the Lean statement S1, here also for even d.)
#   SD : every signing bad at 2^j e is bad at 2^j e' for some e' | e with e' = 1 or e' live (the step-down as used).
#   CN : for every live e > 1 the share of signings bad at 2^j e for some j is <= 2^(1 - D_e); it is 0 if e is not
#        dangerous.
#   P  : share(bad somewhere) <= P_1 + sum over the live dangerous e > 1 of 2^(1 - D_e);  P_1 = 0 for odd m,
#        P_1 <= 3/4 for even m >= 4.
#   D  : the shares of good signings against the stated lower bounds.
# usage: tD.py exh n m | tD.py rand seed count n1 n2 ... | tD.py adv seed n m starts steps
import sys, random, itertools
from fractions import Fraction as F
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from rlib import *

rec = {}        # (category, n, m) -> [count, min good share, example, max first-order bound]
tot = dict(multisets=0, S1=0, S1_even_d=0, SD=0, CN=0, CN_att=0, notdanger=0, P=0, maxbound_no3_even=F(0), maxbound_no3_odd=F(0))

def live2(U, i):
    occ = set(u % (1 << i) for u in U)
    q = 1 << (i - 1)
    return any((c in occ) and (c + q in occ) for c in range(q))

def analyse(B, n, light=False):
    k, npr = split2(n)
    m = len(B)
    bl = bad_levels(B, n)
    fac = factorint(n)
    W = [x % npr for x in B]
    tot['multisets'] += 1
    live = {}
    for p, a in fac.items():
        for i in range(1, a + 1):
            live[(p, i)] = live2(B, i) if p == 2 else live_level(W, p, i)
    ds = divisors(n)
    if not light:
        # S1
        for d in ds:
            for p, i in factorint(d).items():
                if not live[(p, i)]:
                    assert not (bl[d] & ~bl[d // p]).any(), ("S1", n, B, d, p)
                    tot['S1'] += 1
                    if (d // p ** i) % 2 == 0 and p != 2:
                        tot['S1_even_d'] += 1
    # live e
    def is_live(e):
        return all(live[(p, i)] for p, i in factorint(e).items())
    es = divisors(npr)
    bad_e = {}
    for e in es:
        b = np.zeros(1 << m, dtype=bool)
        for j in range(k + 1):
            b |= bl[(1 << j) * e]
        bad_e[e] = b
    first = F(0)
    for e in es:
        if e == 1:
            continue
        lv = is_live(e)
        if not lv:
            if not light:
                for j in range(k + 1):
                    cover = np.zeros(1 << m, dtype=bool)
                    for e2 in divisors(e):
                        if e2 == 1 or (e2 < e and is_live(e2)):
                            cover |= bl[(1 << j) * e2]
                    assert not (bl[(1 << j) * e] & ~cover).any(), ("step-down", n, B, e, j)
                    tot['SD'] += 1
            continue
        De = D_rank(W, e)
        pw = powers_mod2(e)
        s = 0
        for w in W:
            s ^= pw[w % e]
        dangerous = (s == 0)
        nb = int(bad_e[e].sum())
        assert nb * 2 ** De <= 2 ** (m + 1), ("Corollary N", n, B, e)
        tot['CN'] += 1
        tot['CN_att'] += (nb * 2 ** De == 2 ** (m + 1))
        if not dangerous:
            assert nb == 0, ("not dangerous but bad", n, B, e)
            tot['notdanger'] += 1
        else:
            first += F(2, 2 ** De)
    P1 = F(int(bad_e[1].sum()), 1 << m)
    if m % 2 == 1:
        assert P1 == 0
    elif m >= 4:
        assert P1 <= F(3, 4)
    anyb = np.zeros(1 << m, dtype=bool)
    for d in ds:
        anyb |= bl[d]
    badshare = F(int(anyb.sum()), 1 << m)
    assert badshare <= P1 + first, ("Proposition P", n, B, badshare, P1, first)
    tot['P'] += 1
    good = 1 - badshare
    proofbound = (F(3, 4) if (m % 2 == 0 and m >= 4) else F(0)) + first
    cats = []
    if n % 3 != 0:
        if m % 2 == 1:
            cats.append('3 not| n, m odd (>0.76)')
            assert good > F(76, 100), (n, B, good)
            tot['maxbound_no3_odd'] = max(tot['maxbound_no3_odd'], proofbound)
        elif m >= 4:
            cats.append('3 not| n, m even>=4 (>0.011)')
            assert good > F(11, 1000), (n, B, good)
            tot['maxbound_no3_even'] = max(tot['maxbound_no3_even'], proofbound)
            assert proofbound < 1
    if n % 5 != 0 and m % 2 == 1:
        cats.append('5 not| n, m odd (>0.13)')
        assert good > F(13, 100), (n, B, good)
    if m % 2 == 1 and all(p in (2, 3) for p in fac):
        cats.append('n=2^k 3^a, m odd (>=1/3)')
        assert good >= F(1, 3), (n, B, good)
    if m % 2 == 1 and all(p in (2, 3, 5) for p in fac):
        cats.append('n=2^k 3^a 5^b, m odd (>0.014)')
        assert good > F(14, 1000), (n, B, good)
        assert first < 1
    if n % 3 == 0 and m % 2 == 0 and m >= 6 and n % 2 == 0:
        cats.append('OPEN: n even, 3 | n, m even>=6')
    if n % 2 == 0 and n % 15 == 0 and m % 2 == 1 and m >= 5 and any(p >= 7 for p in fac):
        cats.append('"OPEN": n even, 15 | n, prime>=7, m odd>=5')
    if m == 5:
        cats.append('m = 5, any n (first-order sum < 1 ?)')
        assert first < 1, ("m = 5", n, B, first)
    if not cats:
        cats.append('other')
    for c in cats:
        key = (c, n, m)
        r = rec.get(key)
        if r is None:
            rec[key] = [1, good, tuple(B), first]
        else:
            r[0] += 1
            if good < r[1]:
                r[1] = good; r[2] = tuple(B)
            if first > r[3]:
                r[3] = first
    if is_exceptional_pair(B, n):
        assert good == 0
    else:
        assert good > 0, ("NO GOOD SIGNING", n, B)
    return good

def el(n, u, w):
    k, npr = split2(n)
    K = 1 << k
    for x in range(u % K, n, K):
        if x % npr == w % npr:
            return x

def gen(n, rnd, mmax=11):
    k, npr = split2(n)
    K = 1 << k
    t = rnd.random()
    m = rnd.randint(3, mmax)
    if t < 0.2:
        return [rnd.randrange(n) for _ in range(m)]
    if t < 0.35 and n % 2 == 0:         # closed under + n/2
        h = [rnd.randrange(n) for _ in range(max(1, m // 2))]
        return h + [(x + n // 2) % n for x in h]
    if t < 0.5:                          # union of cosets
        g = rnd.choice([d for d in divisors(n) if 1 < d <= mmax])
        B = []
        while len(B) + g <= mmax and (not B or rnd.random() < 0.7):
            r = rnd.randrange(n)
            B += [(r + (n // g) * i) % n for i in range(g)]
        if rnd.random() < 0.3 and len(B) < mmax:
            B.append(rnd.randrange(n))
        return B
    if t < 0.6:                          # interval
        s = rnd.randrange(n)
        return [(s + i) % n for i in range(m)]
    if t < 0.75 and npr > 1:             # twins in the classes modulo n'
        B = []
        while len(B) + 2 <= m:
            w = rnd.randrange(npr)
            B += [el(n, rnd.randrange(K), w), el(n, rnd.randrange(K), w)]
        if rnd.random() < 0.3:
            B.append(rnd.randrange(n))
        return B
    if t < 0.9 and npr > 1:              # one element in every class modulo a prime (a full level), 2-parts from two values
        p = rnd.choice([q for q in factorint(npr)])
        if p > mmax:
            return [rnd.randrange(n) for _ in range(m)]
        us = [rnd.randrange(K), rnd.randrange(K)]
        B = [el(n, rnd.choice(us), (rnd.randrange(npr // p) * p + r) % npr) for r in range(p)]
        while len(B) < m:
            x = rnd.choice(B)
            B.append((x + rnd.choice([n // 2 if n % 2 == 0 else npr, npr * rnd.randrange(K), K * rnd.randrange(npr)])) % n)
        return B
    # few 2-residues, many repeats
    us = [rnd.randrange(K) for _ in range(2)]
    ws = [rnd.randrange(npr) for _ in range(3)]
    return [el(n, rnd.choice(us), rnd.choice(ws)) for _ in range(m)]

def report():
    print("multisets %(multisets)d; S1 checked %(S1)d times (of these with p odd and d/p^i even: %(S1_even_d)d); step-down %(SD)d;"
          " Corollary N on %(CN)d live e (bound attained %(CN_att)d); live but not dangerous, no bad signing: %(notdanger)d;"
          " Proposition P %(P)d" % tot)
    print("largest proof bound, 3 not| n: even m>=4: %s = %.4f ; odd m: %s = %.4f"
          % (tot['maxbound_no3_even'], float(tot['maxbound_no3_even']), tot['maxbound_no3_odd'], float(tot['maxbound_no3_odd'])))
    agg = {}
    for (c, n, m), r in sorted(rec.items()):
        a = agg.setdefault((c, m), [0, F(2), None, None, F(0)])
        a[0] += r[0]
        if r[1] < a[1]:
            a[1], a[2], a[3] = r[1], n, r[2]
        a[4] = max(a[4], r[3])
    for (c, m), a in sorted(agg.items()):
        print("  %-45s m=%2d: %7d multisets; least share of good signings %s = %.4f (n=%d, %s); largest first-order sum over live dangerous e>1: %s"
              % (c, m, a[0], a[1], float(a[1]), a[2], a[3], a[4]))

mode = sys.argv[1]
if mode == 'exh':
    n, m = int(sys.argv[2]), int(sys.argv[3])
    for B in multisets_with_zero(n, m):
        analyse(list(B), n)
    print("EXHAUSTIVE n = %d, every multiset with 0 of %d elements, all signings" % (n, m))
    report()
elif mode == 'rand':
    seed, count = int(sys.argv[2]), int(sys.argv[3])
    mods = [int(x) for x in sys.argv[4:]]
    rnd = random.Random(seed)
    for _ in range(count):
        n = rnd.choice(mods)
        B = gen(n, rnd)
        if len(B) < 1 or len(B) > 12:
            continue
        analyse(B, n)
    print("RANDOM AND STRUCTURED seed %d on %s" % (seed, mods))
    report()
elif mode == 'adv':
    # local search for a small share of good signings (one element changed at a time)
    seed, n, m, starts, steps = [int(x) for x in sys.argv[2:7]]
    rnd = random.Random(seed)
    best = (F(2), None)
    for s in range(starts):
        B = gen(n, rnd, mmax=m)
        B = (B + [rnd.randrange(n) for _ in range(m)])[:m]
        g = analyse(B, n, light=True)
        for _ in range(steps):
            C = list(B)
            C[rnd.randrange(m)] = rnd.randrange(n)
            if rnd.random() < 0.3:
                C[rnd.randrange(m)] = rnd.randrange(n)
            g2 = analyse(C, n, light=True)
            if g2 <= g:
                B, g = C, g2
        if g < best[0]:
            best = (g, sorted(B))
    print("ADVERSARY n = %d, m = %d, %d starts of %d steps (seed %d): least share of good signings found %s = %.4f at %s"
          % (n, m, starts, steps, seed, best[0], float(best[0]), best[1]))
    report()
print("OK")
