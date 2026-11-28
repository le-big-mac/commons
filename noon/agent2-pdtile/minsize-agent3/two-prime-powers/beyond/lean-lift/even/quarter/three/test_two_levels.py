# Two live levels of 5 at once (m = 9, 10, 11, 12 on 25 * 3^a): the heavy class modulo 5 holds a full group modulo 25.
# For every such multiset: for each live level i of 5, P(bad at some d = 5^i * 3^j) <= the level bound of every full
# group at that level (Proposition 5), and the bad share is <= BB(m) (Theorem 6).
# usage: test_two_levels.py seconds seed
import sys, time, random
from fractions import Fraction as F
import numpy as np
from badlib import factor
import bounds
from bounds import BB, level_bound
from test_lemmas import masks, share, groups_at      # builds the table up to m = 12

def crt(n, parts):
    x = 0
    for q, r in parts:
        cc = n // q
        x += r * cc * pow(cc, -1, q)
    return x % n

def main():
    secs = float(sys.argv[1]); rng = random.Random(int(sys.argv[2]))
    t0 = time.time(); ntest = 0; both = 0; seen = {}
    while time.time() - t0 < secs:
        m = rng.choice((9, 10, 10, 11, 12))
        a = rng.choice((1, 1, 2))
        n = 25 * 3 ** a
        res25 = [0, 5, 10, 15, 20] + [1 + 5 * rng.randrange(5), 2 + 5 * rng.randrange(5), 3 + 5 * rng.randrange(5),
                                      4 + 5 * rng.randrange(5)]
        while len(res25) < m:
            res25.append(rng.choice(res25) if rng.random() < 0.7 else rng.randrange(25))
        q3 = 3 ** a
        base = rng.randrange(q3); j = rng.randint(1, a)
        pool = [base, (base + 3 ** (j - 1)) % q3, (base + 2 * 3 ** (j - 1)) % q3]
        if rng.random() < 0.4:
            pool.append(rng.randrange(q3))
        res3 = [rng.choice(pool) if rng.random() < 0.9 else rng.randrange(q3) for _ in range(m)]
        B = [crt(n, ((q3, res3[k]), (25, res25[k]))) for k in range(m)]
        mk, W, _ = masks(n, B)
        ntest += 1
        nonempty = 0
        allbad = np.zeros_like(mk[1])
        for d in mk:
            allbad |= mk[d]
        for i in (1, 2):
            full = [G for G in groups_at(B, 5, i).values() if len(G) == 5]
            assert full, (n, B, i)
            ev = np.zeros_like(mk[1])
            for d in mk:
                f = factor(d)
                if d > 1 and max(f) == 5 and f[5] == i:
                    ev |= mk[d]
            p_ev = share(ev, W, m); p_not1 = share(ev & ~mk[1], W, m)
            nonempty += p_ev > 0
            for G in full:
                sizes = tuple(sorted((len(v) for v in G.values()), reverse=True))
                R = m - sum(sizes)
                val = p_not1 if bounds.beyond1(sizes, R) else p_ev
                bd = level_bound(sizes, R)
                assert val <= bd, ('PROP 5 FAILS', n, B, i, sizes, R, val, bd)
                key = (i, sizes, R)
                seen[key] = max(seen.get(key, F(0)), val)
        both += nonempty == 2
        assert share(allbad, W, m) <= BB[m], ('THEOREM 6 FAILS', n, B)
    print(f'{ntest} multisets (m = 9..12) on 75 and 225 with BOTH levels of 5 live: no failure; '
          f'both level events nonempty in {both} of them')
    for key in sorted(seen, key=lambda k: (k[0], sum(k[1]) + k[2], k[1])):
        i, sizes, R = key
        print(f'  level {i}: {sizes} +{R}: largest share met {seen[key]} / bound {level_bound(sizes, R)}')

main()
