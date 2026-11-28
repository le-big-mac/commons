# Tests of the lemmas of result.md by exact arithmetic over all signings.
# usage: test_lemmas.py which seconds seed
#   which = t3   : Proposition 3 (powers of 3): for every multiset tested, Extra(B) <= the bound for its own class sizes
#   which = t5   : Proposition 5 (one live level of a prime q >= 5): for every multiset and every live level (q, i),
#                  P(bad at some d with largest prime q and q^i || d) <= level bound of every full group of that level;
#                  and Lemma P: every bad signing is bad at a power of 3 or at such a d with a full group;
#                  and the whole: bad share <= BB(m)
import sys, time, random
from fractions import Fraction as F
from itertools import combinations_with_replacement
import numpy as np
from badlib import divisors, factor, configs, bad_mask_at
import bounds
from bounds import c, E3, BB, two_class, three_class, level_bound

bounds.build(12)

def masks(n, B):
    cnt = {}
    for b in B:
        cnt[b % n] = cnt.get(b % n, 0) + 1
    residues = sorted(cnt)
    mults = [cnt[r] for r in residues]
    C, W = configs(mults)
    return {d: bad_mask_at(d, residues, C) for d in divisors(n)}, W, sum(mults)

def share(mask, W, m):
    return F(int(W[mask].sum()), 2 ** m)

def strip3(B):
    """shift and divide by 3 while all elements lie in one class modulo 3; returns the three class sizes"""
    B = list(B)
    for _ in range(40):
        cl = [sum(1 for b in B if b % 3 == t) for t in range(3)]
        if sum(1 for x in cl if x) > 1:
            return sorted(cl, reverse=True)
        t = B[0] % 3
        if all(b == B[0] for b in B):
            return None
        B = [(b - t) // 3 for b in B]
    return None

def test3(secs, seed):
    rng = random.Random(seed)
    t0 = time.time()
    n_ex = 0; n_rand = 0; tight = {}; worst = {}
    def check(n, B):
        mk, W, m = masks(n, B)
        ex = np.zeros_like(mk[1])
        for d in mk:
            if d > 1:
                ex |= mk[d]
        ex &= ~mk[1]
        e = share(ex, W, m)
        cl = strip3(B)
        if cl is None:
            assert e == 0, (n, B, e)
            return
        if cl[2] == 0:
            bd = two_class(cl[0], cl[1])
        else:
            bd = three_class(*cl)
        assert e <= bd, ('PROP 3 FAILS', n, B, e, bd, cl)
        assert e <= E3[m]
        if e == E3[m]:
            tight[m] = tight.get(m, 0) + 1
        if e > worst.get(m, (F(-1),))[0]:
            worst[m] = (e, n, sorted(B))
    # exhaustive: Z_9, multisets containing 0, m <= 8; Z_27, m <= 5
    for n, mmax in ((9, 8), (27, 5)):
        for m in range(2, mmax + 1):
            for rest in combinations_with_replacement(range(n), m - 1):
                check(n, (0,) + rest); n_ex += 1
    print(f'exhaustive (Z_9 to m=8, Z_27 to m=5, multisets containing 0): {n_ex} multisets, no failure; '
          f'time {time.time()-t0:.0f}s', flush=True)
    while time.time() - t0 < secs:
        n = rng.choice((27, 27, 81, 81, 243))
        m = rng.randint(6, 11)
        mode = rng.random()
        if mode < 0.4:
            pool = [rng.randrange(n) for _ in range(rng.randint(2, 6))]
            B = [rng.choice(pool) for _ in range(m)]
        elif mode < 0.8:
            # tree-shaped: digits biased to 0
            B = []
            for _ in range(m):
                b = 0; pw = 1
                while pw < n:
                    b += pw * (rng.choice((0, 0, 1, 2)) if rng.random() < 0.8 else rng.randrange(3)); pw *= 3
                B.append(b)
        else:
            B = [rng.randrange(n) for _ in range(m)]
        check(n, B); n_rand += 1
    print(f'random (Z_27, Z_81, Z_243, m = 6..11): {n_rand} multisets, no failure')
    for m in sorted(worst):
        print(f'  m={m}: largest Extra found {worst[m][0]} (bound E3 {E3[m]}) at n={worst[m][1]} B={worst[m][2]}')

def groups_at(B, q, i):
    gr = {}
    for b in B:
        gr.setdefault(b % q ** (i - 1), {}).setdefault(b % q ** i, []).append(b)
    return gr

def test5(secs, seed):
    rng = random.Random(seed)
    t0 = time.time()
    ntest = 0; nlev = 0; tightlev = 0; struct_seen = {}
    worst = {}
    ns = (5, 15, 25, 35, 45, 75, 105, 175, 225, 315, 525, 7, 21, 63, 49 * 3, 385, 125, 375, 1155)
    while time.time() - t0 < secs:
        n = rng.choice(ns)
        m = rng.randint(MLO, MHI)
        fac = factor(n)
        mode = rng.random()
        B = [0] * m
        for p, a in fac.items():
            qq = p ** a
            cc = n // qq
            e = (cc * pow(cc, -1, qq)) % n
            md = rng.random()
            for j in range(m):
                if md < 0.35:
                    r = rng.randrange(qq)
                elif md < 0.7:
                    r = (j % p) * (qq // p) if rng.random() < 0.8 else rng.randrange(qq)   # spread over the classes
                    if a > 1 and rng.random() < 0.5:
                        r = (j % p) + p * rng.randrange(qq // p) if rng.random() < 0.7 else r
                else:
                    r = 0 if rng.random() < 0.6 else rng.randrange(qq)
                B[j] = (B[j] + e * r) % n
        if rng.random() < 0.3:
            j = rng.randrange(m); B[j] = B[rng.randrange(m)]
        mk, W, m = masks(n, B)
        ntest += 1
        allbad = np.zeros_like(mk[1])
        for d in mk:
            allbad |= mk[d]
        pow3 = np.zeros_like(mk[1])
        d = 1
        while n % d == 0:
            pow3 |= mk[d]; d *= 3
        covered = pow3.copy()
        total_bound = F(0)
        for q in sorted(fac):
            if q < 5:
                continue
            for i in range(1, fac[q] + 1):
                ev = np.zeros_like(mk[1])
                for d in mk:
                    f = factor(d)
                    if d > 1 and max(f) == q and f[q] == i:
                        ev |= mk[d]
                gr = groups_at(B, q, i)
                full = [G for G in gr.values() if len(G) == q]
                if not full:
                    # not live: the event must be inside lower events (step-down); checked through 'covered' below
                    continue
                covered |= ev
                nlev += 1
                p_ev = share(ev, W, m)
                p_ev_not1 = share(ev & ~mk[1], W, m)
                best = None
                for G in full:
                    sizes = tuple(sorted((len(v) for v in G.values()), reverse=True))
                    R = m - sum(sizes)
                    bd = level_bound(sizes, R)
                    special = bounds.beyond1(sizes, R)
                    val = p_ev_not1 if special else p_ev
                    assert val <= bd, ('PROP 5 FAILS', n, B, q, i, sizes, R, val, bd)
                    struct_seen[(q, sizes, R)] = max(struct_seen.get((q, sizes, R), F(0)), val)
                    if val == bd and bd > 0:
                        tightlev += 1
                    best = bd if best is None else min(best, bd)
                total_bound += best
        # Lemma P: every bad signing is bad at a power of 3 or at a d whose largest prime q >= 5 has a live top level
        assert not (allbad & ~covered).any(), ('LEMMA P FAILS', n, B)
        sh = share(allbad, W, m)
        assert sh <= BB[m], ('THEOREM 6 FAILS', n, B, sh, BB[m])
        if sh > worst.get(m, (F(-1),))[0]:
            worst[m] = (sh, n, sorted(B))
    print(f'{ntest} multisets (m = {MLO}..{MHI}) on n in {ns}; {nlev} live levels of primes >= 5 tested, no failure; '
          f'level bound attained {tightlev} times')
    for m in sorted(worst):
        print(f'  m={m}: largest bad share met {worst[m][0]} (bound BB {BB[m]}) at n={worst[m][1]} B={worst[m][2]}')
    print('structures met (q, sizes of the full group, elements outside): largest event share met / bound')
    for key in sorted(struct_seen, key=lambda k: (k[0], sum(k[1]) + k[2], k[1])):
        q, sizes, R = key
        print(f'  q={q} {sizes} +{R}: {struct_seen[key]} / {level_bound(sizes, R)}')

if __name__ == '__main__':
    which = sys.argv[1]; secs = float(sys.argv[2]); seed = int(sys.argv[3])
    MLO = int(sys.argv[4]) if len(sys.argv) > 4 else 5
    MHI = int(sys.argv[5]) if len(sys.argv) > 5 else 10
    if which == 't3':
        test3(secs, seed)
    else:
        test5(secs, seed)
