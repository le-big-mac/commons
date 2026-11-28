# Cross-check of tree.py (count by class sums and masks) against the definition (all signings, division by Phi_d)
# on random small multisets with repeated elements, on Z_9, Z_27, Z_81, Z_25, Z_125, Z_49.
import sys, random, itertools
from fractions import Fraction as F
import tree

def divisors(n): return [d for d in range(1, n + 1) if n % d == 0]
def pdiv(num, den):
    num = num[:]; q = [0] * (len(num) - len(den) + 1)
    for i in range(len(q) - 1, -1, -1):
        t = num[i + len(den) - 1]; q[i] = t
        for j, dj in enumerate(den): num[i + j] -= t * dj
    return q, num
_cy = {}
def cyclo(d):
    if d not in _cy:
        num = [-1] + [0] * (d - 1) + [1]
        for e in divisors(d):
            if e < d: num, rem = pdiv(num, cyclo(e)); assert not any(rem)
        _cy[d] = num
    return _cy[d]
def bad_at(S, d):       # S: list of coefficients of the signed mask, degree < n
    if len(S) < len(cyclo(d)): return not any(S)
    q, rem = pdiv(S, cyclo(d)); return not any(rem)

rng = random.Random(int(sys.argv[1])); count = int(sys.argv[2]); n_ok = 0; nx = 0
for _ in range(count):
    p, v = rng.choice([(3, 2), (3, 3), (3, 4), (5, 2), (5, 3), (7, 2)])
    n = p ** v
    items = tree.rand_items(p, v, rng, "mid")
    # cut down to at most 13 elements
    lst = [b for b, mu in items.items() for _ in range(mu)]
    rng.shuffle(lst); lst = lst[:rng.randint(2, 13)]
    if rng.random() < 0.5:   # make a full group likely
        i = rng.randrange(v); base = rng.randrange(p ** i)
        lst = ([(base + t * p ** i) % n for t in range(p)] + lst)[:13]
    items = {}
    for b in lst: items[b] = items.get(b, 0) + 1
    m, f0, x = tree.analyse(p, v, items)
    cnt_pp = 0; cnt_x = 0
    for eps in itertools.product((1, -1), repeat=m - 1):
        S = [0] * n; S[lst[0]] += 1
        for b, e in zip(lst[1:], eps): S[b] += e
        b1 = bad_at(S, 1); bp = any(bad_at(S, p ** i) for i in range(1, v + 1))
        cnt_pp += b1 or bp; cnt_x += bp and not b1
    assert F(cnt_pp, 1 << (m - 1)) == f0 + x and F(cnt_x, 1 << (m - 1)) == x, (p, v, lst)
    n_ok += 1; nx += x > 0
print(f"seed {sys.argv[1]}: {n_ok} multisets (2 to 13 elements; X_p nonempty in {nx}): tree count = count from the definition every time")
