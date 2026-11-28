# Test of the case analysis for eight elements (result.md, section 4, "beta(8) = 39/128").
# For multisets of 8 elements built to make the levels of 5 and 7 live with the 3-part chosen from small pools:
#   X  = bad at some 3^i (i >= 1), not at 1;  L5, L7 = bad at some d with largest prime 5, 7.
# Claims tested: P(L7) <= 2/256; P(L5) <= 6/256; L7 nonempty => X empty; L5 nonempty => X empty, unless the full
# group of 5 has sizes (2,2,2,1,1), and then P(X) <= 4/256; bad share <= 39/128.
# usage: test8.py seconds seed
import sys, time, random
from fractions import Fraction as F
import numpy as np
from badlib import factor
from test_lemmas import masks, share, groups_at

def crt(n, parts):
    x = 0
    for q, r in parts:
        cc = n // q
        x += r * cc * pow(cc, -1, q)
    return x % n

def main():
    secs = float(sys.argv[1]); rng = random.Random(int(sys.argv[2]))
    t0 = time.time()
    pats5 = [(4, 1, 1, 1, 1), (3, 2, 1, 1, 1), (2, 2, 2, 1, 1), (2, 1, 1, 1, 1), (1, 1, 1, 1, 1)]
    ntest = 0; stat = {}
    worst = F(0)
    while time.time() - t0 < secs:
        a = rng.choice((1, 2, 2, 3, 3))
        with7 = rng.random() < 0.3
        lvl2 = (not with7) and rng.random() < 0.4
        m = 8
        if lvl2:
            # the full group sits at level 2 of the 5-tree (class 0 modulo 5), the other elements in class 1 modulo 5
            a = rng.choice((1, 2, 2))
            n = 3 ** a * 25
            P5 = 25
            pat = rng.choice(((2, 1, 1, 1, 1), (1, 1, 1, 1, 1), (3, 1, 1, 1, 1), (2, 2, 1, 1, 1)))
            res5 = []
            for t, r in enumerate(pat):
                res5 += [5 * t] * r
            u = rng.randrange(5)
            while len(res5) < m:
                res5.append(1 + 5 * (u if rng.random() < 0.85 else rng.randrange(5)))
        else:
            n = 3 ** a * 5 * (7 if with7 else 1)
            P5 = 5
            # residues modulo 5
            pat = rng.choice(pats5)
            res5 = []
            for t, r in enumerate(pat):
                res5 += [t] * r
            while len(res5) < m:
                res5.append(rng.choice(res5[-1:] + [rng.randrange(5)]) if rng.random() < 0.8 else rng.randrange(5))
        rng.shuffle(res5)
        # residues modulo 3^a from a small pool (many coincidences); pools made of a base and its translates by 3^(j-1)
        q3 = 3 ** a
        base = rng.randrange(q3)
        j = rng.randint(1, a)
        pool = [base, (base + 3 ** (j - 1)) % q3, (base + 2 * 3 ** (j - 1)) % q3]
        if rng.random() < 0.5:
            pool.append(rng.randrange(q3))
        if rng.random() < 0.3:
            pool.append(rng.randrange(q3))
        res3 = [rng.choice(pool) if rng.random() < 0.9 else rng.randrange(q3) for _ in range(m)]
        if with7:
            if rng.random() < 0.7:
                res7 = list(range(7)) + [rng.randrange(7)]
                rng.shuffle(res7)
            else:
                res7 = [rng.randrange(7) for _ in range(m)]
            B = [crt(n, ((q3, res3[k]), (P5, res5[k]), (7, res7[k]))) for k in range(m)]
        else:
            B = [crt(n, ((q3, res3[k]), (P5, res5[k]))) for k in range(m)]
        mk, W, _ = masks(n, B)
        ntest += 1
        lev5 = 2 if lvl2 else 1
        live5 = any(len(G) == 5 for G in groups_at(B, 5, lev5).values())
        assert not (lvl2 and any(len(G) == 5 for G in groups_at(B, 5, 1).values()))
        live7 = with7 and any(len(G) == 7 for G in groups_at(B, 7, 1).values())
        zero = np.zeros_like(mk[1])
        X = zero.copy(); L5 = zero.copy(); L7 = zero.copy(); allbad = zero.copy()
        for d in mk:
            allbad |= mk[d]
            if d == 1:
                continue
            mx = max(factor(d))
            if mx == 3:
                X |= mk[d]
            elif mx == 5:
                if live5 and factor(d)[5] == lev5:           # L_(q,i) is defined for LIVE levels only (Lemma P); otherwise step-down applies
                    L5 |= mk[d]
            else:
                if live7:
                    L7 |= mk[d]
        X &= ~mk[1]
        assert not (allbad & ~(mk[1] | X | L5 | L7)).any(), ('LEMMA P', n, B)
        pX, p5, p7 = share(X, W, m), share(L5, W, m), share(L7, W, m)
        sh = share(allbad, W, m)
        assert p7 <= F(2, 256), ('L7', n, B, p7)
        assert p5 <= F(6, 256), ('L5', n, B, p5)
        assert sh <= F(39, 128), ('TOTAL', n, B, sh)
        worst = max(worst, sh)
        if p7 > 0:
            assert pX == 0, ('L7 and X', n, B, pX, p7)
            stat['L7 nonempty'] = stat.get('L7 nonempty', 0) + 1
            if p5 > 0:
                stat['L7 and L5 nonempty'] = stat.get('L7 and L5 nonempty', 0) + 1
        if p5 > 0:
            gr = groups_at(B, 5, lev5)
            full = [G for G in gr.values() if len(G) == 5]
            sizes = tuple(sorted((len(v) for v in full[0].values()), reverse=True))
            key = f'L5 nonempty, sizes {sizes} + {m - sum(sizes)}: {p5}'
            stat[key] = stat.get(key, 0) + 1
            if sizes == (2, 2, 2, 1, 1):
                assert pX <= F(4, 256), ('L5 (2,2,2,1,1) and X', n, B, pX)
                if pX > 0:
                    stat['  of these with X nonempty: P(X) = %s' % pX] = stat.get('  of these with X nonempty: P(X) = %s' % pX, 0) + 1
            else:
                assert pX == 0, ('L5 and X', n, B, sizes, pX, p5)
    print(f'{ntest} multisets of 8 elements on 3^a*5, 3^a*5*7 (a <= 3) and 3^a*25 (a <= 2): no failure; largest bad share met {worst}')
    for k in sorted(stat):
        print('  ', k, ':', stat[k])

main()
