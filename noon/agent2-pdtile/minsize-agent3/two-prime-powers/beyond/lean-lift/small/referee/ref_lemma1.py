"""Referee's test of Lemma 1 (slice criterion) of small-multisets.md, from its statement.

n odd, p^a || n, n = p^a n''.  For a signed multiset and a class C of the p-tree the slice is
    S_C = sum over the elements x with (x mod p^a) in C of (+-1) X^(x mod n'')   in Z[X]/(X^n'' - 1).
(a) Phi_d'' | S  iff  Phi_d'' | S_T (T = everything).
(b) 1 <= i <= a:  Phi_(p^i d'') | S  iff  in every group at level i (a class modulo p^(i-1) with its p classes modulo p^i)
    the p slices are congruent to one another modulo Phi_d''.
Left sides: remainder of the signed mask modulo Phi_d (exact).  Right sides: the slices reduced modulo Phi_d'' (exact).
usage: ref_lemma1.py SEED COUNT"""
import sys, random
import numpy as np
from reflib import *

rng = random.Random(int(sys.argv[1])); count = int(sys.argv[2])
shapes = [9, 27, 81, 45, 135, 63, 189, 75, 225, 375, 25, 125, 105, 315, 525, 147, 99, 175, 495, 675, 49, 15, 21, 35]
ncases = 0; nlev = 0; ndiv = 0; by_i = {}
for _ in range(count):
    n = rng.choice(shapes); f = factor(n)
    m = rng.randint(1, 12)
    kind = rng.randrange(4)
    if kind == 0:
        el = [rng.randrange(n) for _ in range(m)]
    elif kind == 1:
        d = rng.choice([x for x in divisors(n) if x > 1]); c = rng.randrange(n)
        el = [(c + (n // d) * rng.randrange(d)) % n for _ in range(m)]
    else:
        el = []
        same = rng.random() < 0.7                  # all cosets at one level of one tree: flat levels do occur
        q = rng.choice(list(f)); i = rng.randrange(f[q])
        while len(el) < m:
            if not same:
                q = rng.choice(list(f)); i = rng.randrange(f[q])
            c = rng.randrange(n)
            step = q ** i * (n // q ** f[q]) if kind == 2 else n // q
            if len(el) + q <= m and rng.random() < 0.85:
                el += [(c + step * j) % n for j in range(q)]
            else:
                el.append(rng.choice(el) if el and rng.random() < 0.3 else rng.randrange(n))
    if kind >= 2 and rng.random() < 0.7:
        signs = [1] * len(el)                      # all + : whole cosets vanish at many levels
        for j in range(len(el)):
            if rng.random() < 0.15: signs[j] = -1
    else:
        signs = [rng.choice((1, -1)) for _ in el]
    bad = set(bad_levels(n, el, signs))            # the d | n with Phi_d | S
    for p, a in f.items():
        n2 = n // p ** a
        for d2 in divisors(n2):
            R = rem_matrix(d2)
            def slice_mod(pred):
                v = np.zeros(R.shape[0], dtype=np.int64)
                for x, s in zip(el, signs):
                    if pred(x % p ** a):
                        v += s * R[:, (x % n2) % d2]
                return v
            # (a)
            lhs = d2 in bad
            rhs = not slice_mod(lambda u: True).any()
            assert lhs == rhs, ('Lemma 1(a) fails', n, el, signs, p, d2)
            nlev += 1; ndiv += lhs
            # (b)
            for i in range(1, a + 1):
                lhs = (p ** i * d2) in bad
                rhs = True
                for g in range(p ** (i - 1)):                       # the group: classes g + p^(i-1) e modulo p^i
                    sl = [slice_mod(lambda u, c=g + p ** (i - 1) * e: u % p ** i == c) for e in range(p)]
                    if any((sl[e] != sl[0]).any() for e in range(1, p)):
                        rhs = False; break
                assert lhs == rhs, ('Lemma 1(b) fails', n, el, signs, p, i, d2)
                nlev += 1; ndiv += lhs
                T = by_i.setdefault((p, i), [0, 0]); T[0] += 1; T[1] += lhs
    ncases += 1
print(f'Lemma 1: {ncases} signed multisets of 1..12 elements on the groups {shapes}: {nlev} pairs (level, d\'\') compared, '
      f'{ndiv} of them with Phi_d dividing the signed mask: the criterion agreed with exact division in every case')
print('   by (p, i): compared, with a divisor:', ', '.join(f'{k}: {v[0]}, {v[1]}' for k, v in sorted(by_i.items())))
