"""Referee's test of Lemma 4 (divisors) of small-multisets.md: B0 on Z_n0, k odd, n = k n0, B = k * B0 on Z_n.
Claim: a signing that is good for B on Z_n is good for B0 on Z_n0.  All signings, exact.   usage: ref_lemma4.py SEED COUNT"""
import sys, random
from reflib import *
rng = random.Random(int(sys.argv[1])); count = int(sys.argv[2])
tot = [0, 0, 0, 0, 0]
for _ in range(count):
    n0 = rng.choice([1, 3, 5, 9, 15, 21, 25, 27, 45, 63, 75, 105]); k = rng.choice([3, 5, 7, 9, 15, 21, 25]); n = n0 * k
    m = rng.randint(1, 9); f0 = factor(n0)
    if n0 > 1 and rng.random() < 0.6:
        el0 = []
        while len(el0) < m:
            q = rng.choice(list(f0)); c = rng.randrange(n0)
            if len(el0) + q <= m and rng.random() < 0.85: el0 += [(c + (n0 // q) * j) % n0 for j in range(q)]
            else: el0.append(rng.choice(el0) if el0 and rng.random() < 0.4 else rng.randrange(n0))
    else:
        el0 = [rng.randrange(n0) for _ in range(m)]
    g0 = good_all(n0, el0); g = good_all(n, [k * x for x in el0])
    assert not (g & ~g0).any(), ('Lemma 4 fails', n0, k, el0)
    tot[0] += 1; tot[1] += len(g); tot[2] += int((~g0).sum()); tot[3] += int(g.sum()); tot[4] += int((g0 & ~g).sum())
print(f'Lemma 4: {tot[0]} multisets of 1..9 elements, {tot[1]} signings; bad on Z_n0: {tot[2]}; good for k*B0 on Z_(k n0): {tot[3]}, '
      f'each of them good for B0 (asserted); good for B0 and bad for k*B0: {tot[4]}')
