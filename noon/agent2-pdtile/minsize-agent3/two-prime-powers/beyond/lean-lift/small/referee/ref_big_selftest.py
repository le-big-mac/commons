"""Self-test of refbig.py against reflib.py on small groups: for random and structured multisets, ALL signings, the
set of divisors d with Phi_d | S found by the split test (both methods, 'ld' and 'psi') must equal the one found by the
remainder of the dense mask modulo Phi_d; and the numeric value |S(zeta_d)| must be < 1e-9 exactly for those d.
usage: ref_big_selftest.py SEED COUNT"""
import sys, random, math
import numpy as np
from reflib import factor, divisors, good_all, bad_levels, sign_matrix, good_plain
from refbig import Tester, Phi, Psi
from reflib import cyclo

rng = random.Random(int(sys.argv[1])); count = int(sys.argv[2])
for r in [1, 3, 5, 15, 21, 105, 165, 1155]:
    assert tuple(int(v) for v in Phi(r)) == cyclo(r)
print('Phi_r for r = 1, 3, 5, 15, 21, 105, 165, 1155: equal to the plain construction')
shapes = [27, 81, 45, 135, 405, 225, 675, 315, 945, 1575, 525, 1155, 189, 441, 243, 375, 2025, 3465]
nsign = 0; nbad = 0; ndiv = 0
for _ in range(count):
    n = rng.choice(shapes); f = factor(n); m = rng.randint(1, 8)
    kind = rng.randrange(4)
    if kind == 0:
        el = [rng.randrange(n) for _ in range(m)]
    elif kind == 1:
        d = rng.choice([x for x in divisors(n) if x > 1]); c = rng.randrange(n)
        el = [(c + (n // d) * rng.randrange(d)) % n for _ in range(m)]
    else:
        el = []
        while len(el) < m:
            q = rng.choice(list(f)); i = rng.randrange(f[q]); c = rng.randrange(n)
            step = q ** i * (n // q ** f[q]) if kind == 2 else n // q
            if len(el) + q <= m and rng.random() < 0.85:
                el += [(c + step * j) % n for j in range(q)]
            else:
                el.append(rng.choice(el) if el and rng.random() < 0.3 else rng.randrange(n))
    T = Tester(f, el)
    sg = sign_matrix(len(el))
    g = good_all(n, el)
    for row, gv in zip(sg, g):
        signs = [int(v) for v in row]
        ref = bad_levels(n, el, signs)
        a = sorted(T.bad_divisors(signs, 'psi'))
        b = sorted(L[0] for L in T.levels if T.divides(L, signs, 'ld'))
        assert a == ref == b, (n, el, signs, ref, a, b)
        assert T.good(signs) == bool(gv)
        nd, nld, ok = T.confirm_by_long_division(signs)
        assert ok == bool(gv)
        for d in divisors(n):                       # numeric check
            v = sum(s * complex(math.cos(2 * math.pi * (x % d) / d), math.sin(2 * math.pi * (x % d) / d)) for x, s in zip(el, signs))
            assert (abs(v) < 1e-9) == (d in ref), (n, el, signs, d, abs(v))
        nsign += 1; nbad += (not gv); ndiv += len(ref)
print(f'split test (both methods) = dense remainder modulo Phi_d = numeric vanishing: {count} multisets of 1..8 elements on {shapes}, '
      f'{nsign} signings ({nbad} bad; {ndiv} pairs (signing, d) with Phi_d | S)')
