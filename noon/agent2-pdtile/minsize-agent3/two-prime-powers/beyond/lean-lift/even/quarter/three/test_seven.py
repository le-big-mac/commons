# Test of Remark 3.3 of result.md (added after the referee's report): on powers of 3,
#  (1) for SEVEN elements every signing that is bad at some 3^i has signs adding up to +3 or -3
#      (all multisets containing 0 on Z_9 and on Z_27 as far as the time allows, random ones on Z_81, Z_243);
#  (2) two classes modulo 3 of sizes 7 and 3 (ten elements): P(X) <= E3(7)*E3(3)/2 = 5/256, X = bad at some 3^i, i >= 1,
#      and not at 1 (targeted multisets on Z_27, Z_81, Z_243);
#  (3) ten elements: P(X) <= 19/512 (all multisets containing 0 on Z_9; random and targeted ones on Z_27, Z_81, Z_243);
#  (4) the terms of the recursion for m = 10 with the exception extended to sizes 3, 5, 7 (exact), and the example.
# bounds.py is NOT changed: E3(10) stays 5/128 there.
# usage: test_seven.py seconds seed
import sys, time, random
from fractions import Fraction as F
from itertools import combinations_with_replacement
import numpy as np
from badlib import configs, bad_mask_at, divisors
import bounds
from bounds import c, E3, g3

bounds.build3(9)

def analyse(n, B):
    """returns (W, total sum of signs per configuration, mask bad at 1, mask bad at some 3^i with i >= 1, m)"""
    cnt = {}
    for b in B:
        cnt[b % n] = cnt.get(b % n, 0) + 1
    residues = sorted(cnt)
    mults = [cnt[r] for r in residues]
    C, W = configs(mults)
    tot = C.sum(axis=1)
    b1 = bad_mask_at(1, residues, C)
    hi = np.zeros(C.shape[0], dtype=bool)
    for d in divisors(n):
        if d > 1:
            hi |= bad_mask_at(d, residues, C)
    return W, tot, b1, hi, sum(mults)

def pX(n, B):
    W, tot, b1, hi, m = analyse(n, B)
    return F(int(W[hi & ~b1].sum()), 2 ** m)

def tree_elem(n, rng):
    b = 0; pw = 1
    while pw < n:
        b += pw * (rng.choice((0, 0, 1, 2)) if rng.random() < 0.8 else rng.randrange(3)); pw *= 3
    return b

def main():
    secs = float(sys.argv[1]); rng = random.Random(int(sys.argv[2]))
    t0 = time.time()
    if len(sys.argv) > 3 and sys.argv[3] == 'z27only':
        # only part (1) on Z_27, with the whole time: all multisets of seven elements containing 0
        n27 = 0; ne27 = 0; complete = True
        for rest in combinations_with_replacement(range(27), 6):
            if time.time() - t0 > secs:
                complete = False
                break
            W, tot, b1, hi, m = analyse(27, (0,) + rest)
            assert not b1.any()
            assert (np.abs(tot[hi]) == 3).all(), ('SEVEN FAILS', 27, rest)
            ne27 += int(hi.any()); n27 += 1
        print('(1) seven elements, Z_27, multisets containing 0 in lexicographic order: %d checked (%s), every bad signing '
              'has sum +3 or -3 (%d multisets have one)' % (n27, 'ALL of them' if complete else 'NOT all: stopped by the clock', ne27))
        return
    # (4) the recursion terms for m = 10
    print('(4) terms of the recursion for m = 10 with the exception for sizes 3, 5, 7:')
    best = F(0)
    for r1 in range(1, 6):
        r0 = 10 - r1
        if r0 in (3, 5, 7) and r1 in (3, 5, 7):
            val = E3[r0] * E3[r1] / 2
        else:
            val = c(r0) * E3[r1] + c(r1) * E3[r0] + E3[r0] * E3[r1]
        best = max(best, val)
        print('    two classes (%d, %d): %s' % (r0, r1, val))
    for r2 in range(1, 4):
        for r1 in range(r2, (10 - r2) // 2 + 1):
            r0 = 10 - r1 - r2
            val = g3(r0, r1, r2) + (c(r0) + E3[r0]) * (c(r1) + E3[r1]) * (c(r2) + E3[r2]) - c(r0) * c(r1) * c(r2)
            best = max(best, val)
            print('    three classes (%d, %d, %d): %s' % (r0, r1, r2), val) if False else print('    three classes (%d, %d, %d): %s' % (r0, r1, r2, val))
    print('    largest: %s   (19/512: %s)' % (best, best == F(19, 512)))
    assert best == F(19, 512)
    ex = (0, 0, 1, 1, 2, 2, 3, 3, 6, 6)
    W, tot, b1, hi, m = analyse(9, ex)
    print('    example %s on Z_9: P(X) = %s, bad share = %s' % (ex, F(int(W[hi & ~b1].sum()), 2 ** m), F(int(W[hi | b1].sum()), 2 ** m)))

    # (1) seven elements
    def check7(n, B):
        W, tot, b1, hi, m = analyse(n, B)
        assert not b1.any()
        bad = hi
        assert (np.abs(tot[bad]) == 3).all(), ('SEVEN FAILS', n, B)
        return int(bad.any())
    n9 = 0; ne9 = 0
    for rest in combinations_with_replacement(range(9), 6):
        ne9 += check7(9, (0,) + rest); n9 += 1
    print('(1) seven elements, Z_9, all %d multisets containing 0: every bad signing has sum +3 or -3 (%d multisets have one)' % (n9, ne9), flush=True)
    n27 = 0; ne27 = 0; complete = True
    budget27 = 0.55 * secs
    for rest in combinations_with_replacement(range(27), 6):
        if time.time() - t0 > budget27:
            complete = False
            break
        ne27 += check7(27, (0,) + rest); n27 += 1
    print('    Z_27, multisets containing 0 in lexicographic order: %d checked (%s), no failure (%d have a bad signing)'
          % (n27, 'ALL of them' if complete else 'NOT all: stopped by the clock', ne27), flush=True)
    nr = 0; ner = 0
    t1 = time.time()
    while time.time() - t1 < 0.1 * secs:
        n = rng.choice((27, 81, 243))
        if rng.random() < 0.7:
            B = [tree_elem(n, rng) for _ in range(7)]
        else:
            pool = [rng.randrange(n) for _ in range(rng.randint(2, 5))]
            B = [rng.choice(pool) for _ in range(7)]
        ner += check7(n, B); nr += 1
    print('    random on Z_27, Z_81, Z_243: %d multisets, no failure (%d have a bad signing)' % (nr, ner), flush=True)

    # (2) two classes of sizes 7 and 3
    bd73 = E3[7] * E3[3] / 2
    n73 = 0; pos73 = 0; eq73 = 0; big = F(0)
    t1 = time.time()
    while time.time() - t1 < 0.15 * secs:
        n = rng.choice((27, 81, 243))
        k = n // 3
        mode = rng.random()
        if mode < 0.6:
            # class 0: heavy class and two single elements at some level; class 1: three elements in one group
            lv = rng.choice([p for p in (1, 3, 9, 27) if p * 3 <= k])
            h = rng.randrange(k)
            A = [h] * 5 + [(h + lv) % k, (h + 2 * lv) % k]
            if rng.random() < 0.4:
                A[rng.randrange(5)] = (h + 3 * lv * rng.randrange(3)) % k
            lv2 = rng.choice([p for p in (1, 3, 9, 27) if p * 3 <= k])
            h2 = rng.randrange(k)
            A2 = [h2, (h2 + lv2) % k, (h2 + 2 * lv2) % k]
        else:
            A = [tree_elem(k, rng) for _ in range(7)]
            A2 = [tree_elem(k, rng) for _ in range(3)]
        t = rng.randrange(3); u = (t + rng.choice((1, 2))) % 3
        B = [t + 3 * a for a in A] + [u + 3 * a for a in A2]
        p = pX(n, B)
        assert p <= bd73, ('(7,3) FAILS', n, B, p)
        n73 += 1; pos73 += p > 0; eq73 += p == bd73; big = max(big, p)
    print('(2) classes (7, 3): %d multisets, P(X) <= %s every time; P(X) > 0 in %d, equal to the bound in %d, largest %s'
          % (n73, bd73, pos73, eq73, big), flush=True)

    # (3) ten elements
    n10 = 0; mx = F(0); cnt_eq = 0
    for rest in combinations_with_replacement(range(9), 9):
        p = pX(9, (0,) + rest)
        assert p <= F(19, 512), ('TEN FAILS', 9, rest, p)
        n10 += 1; mx = max(mx, p); cnt_eq += p == F(19, 512)
    print('(3) ten elements, Z_9, all %d multisets containing 0: P(X) <= 19/512; largest %s, attained by %d' % (n10, mx, cnt_eq), flush=True)
    nr10 = 0; mx = F(0)
    while time.time() - t0 < secs:
        n = rng.choice((27, 81, 243))
        if rng.random() < 0.7:
            B = [tree_elem(n, rng) for _ in range(10)]
        else:
            pool = [rng.randrange(n) for _ in range(rng.randint(2, 6))]
            B = [rng.choice(pool) for _ in range(10)]
        p = pX(n, B)
        assert p <= F(19, 512), ('TEN FAILS', n, B, p)
        nr10 += 1; mx = max(mx, p)
    print('    random on Z_27, Z_81, Z_243: %d multisets, P(X) <= 19/512; largest %s' % (nr10, mx))

main()
