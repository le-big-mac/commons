# Referee, second look: Remark 3.3 by brute force (all signings, remainders modulo Phi_d; my library bf.py).
#  (1) seven elements on powers of 3: every bad signing has sum of signs +3 or -3;
#  (2) classes (7,3) modulo 3: P(X) <= 5/256;   (3) ten elements: P(X) <= 19/512.
# usage: seven_bf.py part seconds
import sys, time, random, itertools
import numpy as np
from fractions import Fraction as Fr
from bf import *
part = sys.argv[1]; secs = float(sys.argv[2]); t0 = time.time(); rng = random.Random(20261128)

def events(n, Bs):
    ev = bad_events(n, Bs)
    hi = np.zeros_like(ev[1])
    for d in ev:
        if d > 1: hi |= ev[d]
    return ev[1], hi

def tree_elem(n):
    b = 0; pw = 1
    while pw < n:
        b += pw * rng.choice((0, 0, 0, 1, 1, 2, rng.randrange(3))); pw *= 3
    return b

def batchsize(n, m): return max(4, min(4000, 25000000 // (2 ** (m - 1) * (n - n // 3))))

if part == '1':
    m = 7; ssum = np.abs(signs(m).sum(axis=1))
    for n in (9, 27):
        it = itertools.combinations_with_replacement(range(n), m - 1); tot = 0; withbad = 0; fails = 0; done = True
        while True:
            chunk = list(itertools.islice(it, 4000))
            if not chunk: break
            b1, hi = events(n, np.array([(0,) + x for x in chunk]))
            assert not b1.any()
            ks, ss = np.nonzero(hi)
            if (ssum[ss] != 3).any(): fails += 1; print('FAIL seven', n)
            tot += len(chunk); withbad += int(hi.any(axis=1).sum())
            if time.time() - t0 > secs: done = False; break
        print('(1) seven elements, Z_%d, multisets containing 0: %d (%s); with a bad signing: %d; every bad signing has sum +-3: %s' % (n, tot, 'ALL' if done else 'not all', withbad, fails == 0), flush=True)
    for n in (81, 243):
        tot = 0; withbad = 0; fails = 0; t1 = time.time()
        while time.time() - t1 < 25:
            K = batchsize(n, m)
            Bs = np.array([[tree_elem(n) for _ in range(m)] if rng.random() < 0.7 else [rng.choice(p) for _ in range(m)] for p in [[rng.randrange(n) for _ in range(rng.randint(2, 5))] for _ in range(K)]])
            b1, hi = events(n, Bs)
            ks, ss = np.nonzero(hi)
            if (ssum[ss] != 3).any(): fails += 1; print('FAIL seven', n)
            tot += K; withbad += int(hi.any(axis=1).sum())
        print('(1) seven elements, Z_%d, random: %d; with a bad signing: %d; failures %d' % (n, tot, withbad, fails), flush=True)
if part == '2':
    m = 10; half = 2 ** (m - 1)
    for n in (27, 81):
        k = n // 3; tot = 0; pos = 0; eq = 0; fails = 0; big = 0; t1 = time.time()
        lvls = [p for p in (1, 3, 9) if p * 3 <= k]
        while time.time() - t1 < secs / 2:
            K = batchsize(n, m); Bs = []
            for _ in range(K):
                if rng.random() < 0.6:
                    lv = rng.choice(lvls); h = rng.randrange(k)
                    A = [h] * 5 + [(h + lv) % k, (h + 2 * lv) % k]
                    if rng.random() < 0.4: A[rng.randrange(5)] = (h + 3 * lv * rng.randrange(3)) % k
                    if rng.random() < 0.3: A = [h] * 3 + [(h + lv) % k] * 3 + [(h + 2 * lv) % k]      # (3,3,1) inside
                    lv2 = rng.choice(lvls); h2 = rng.randrange(k)
                    A2 = [h2, (h2 + lv2) % k, (h2 + 2 * lv2) % k]
                else:
                    A = [tree_elem(k) for _ in range(7)]; A2 = [tree_elem(k) for _ in range(3)]
                t = rng.randrange(3); u = (t + rng.choice((1, 2))) % 3
                Bs.append([t + 3 * a for a in A] + [u + 3 * a for a in A2])
            b1, hi = events(n, np.array(Bs))
            nX = (hi & ~b1).sum(axis=1)
            tot += K; pos += int((nX > 0).sum()); eq += int((nX * 256 == 5 * half).sum()); big = max(big, int(nX.max()))
            if (nX * 256 > 5 * half).any(): fails += 1; print('FAIL (7,3)', n)
        print('(2) classes (7,3) on Z_%d: %d multisets; P(X) > 0 in %d; equal to 5/256 in %d; largest %s; failures %d' % (n, tot, pos, eq, Fr(big, half), fails), flush=True)
if part == '3':
    m = 10; half = 2 ** (m - 1)
    it = itertools.combinations_with_replacement(range(9), m - 1); tot = 0; eq = 0; fails = 0; big = 0; nb = 0
    while True:
        chunk = list(itertools.islice(it, 2000))
        if not chunk: break
        b1, hi = events(9, np.array([(0,) + x for x in chunk]))
        nX = (hi & ~b1).sum(axis=1); bad = (hi | b1).sum(axis=1)
        tot += len(chunk); eq += int((nX * 512 == 19 * half).sum()); big = max(big, int(nX.max())); nb = max(nb, int(bad.max()))
        if (nX * 512 > 19 * half).any(): fails += 1; print('FAIL ten Z_9')
    print('(3) ten elements, Z_9, ALL %d multisets containing 0: largest P(X) %s, attained by %d; largest bad share %s; failures %d' % (tot, Fr(big, half), eq, Fr(nb, half), fails), flush=True)
    for n in (27, 81, 243):
        tot = 0; fails = 0; big = 0; t1 = time.time()
        while time.time() - t1 < secs / 3:
            K = batchsize(n, m)
            Bs = np.array([[tree_elem(n) for _ in range(m)] if rng.random() < 0.7 else [rng.choice(p) for _ in range(m)] for p in [[rng.randrange(n) for _ in range(rng.randint(2, 6))] for _ in range(K)]])
            b1, hi = events(n, Bs)
            nX = (hi & ~b1).sum(axis=1); tot += K; big = max(big, int(nX.max()))
            if (nX * 512 > 19 * half).any(): fails += 1; print('FAIL ten', n)
        print('(3) ten elements, Z_%d, random: %d multisets; largest P(X) %s; failures %d' % (n, tot, Fr(big, half), fails), flush=True)
