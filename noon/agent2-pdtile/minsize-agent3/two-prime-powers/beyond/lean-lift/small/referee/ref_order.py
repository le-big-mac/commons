"""Referee's check of a remark on section 3 of small-multisets.md: the order of the contractions.

Claims checked (the referee's, proved by hand in the report):
  (1) contracting from the top level down in every tree deletes exactly the levels that are contractible for B itself;
      the group left has order  n_td = product over p of p^(r_p), r_p = number of levels of the p-tree of B at which
      some group has all p subclasses occupied;
  (2) every other order ends on a group whose order is a multiple of n_td (a level that has a full group can never be
      deleted; a contractible level can lose that property when a lower level is contracted first).
Orders tried: top-down; bottom-up; 3 random orders.
usage: ref_order.py SEED COUNT"""
import sys, random
from reflib import *

def full_levels(el, n):
    out = 1
    for p, a in factor(n).items():
        for t in range(1, a + 1):
            if not contractible(el, p, a, t):
                out *= p
    return out

def run(el, n, pick):
    while True:
        f = factor(n)
        cand = [(p, t) for p in sorted(f) for t in range(1, f[p] + 1) if contractible(el, p, f[p], t)]
        if not cand:
            return n
        p, t = pick(cand)
        el = contract(el, n, p, f[p], t); n //= p

rng = random.Random(int(sys.argv[1])); count = int(sys.argv[2])
shapes = [81, 243, 729, 2187, 135, 405, 675, 2025, 3375, 945, 1575, 4725, 625, 3125, 1323, 9261, 3465, 10395, 50625, 23625]
differ = 0; worst = None
for _ in range(count):
    n = rng.choice(shapes); f = factor(n); m = rng.randint(2, 14)
    kind = rng.randrange(3)
    if kind == 0:
        el = [rng.randrange(n) for _ in range(m)]
    elif kind == 1:                                  # clustered: shared low digits
        base = rng.randrange(n); el = []
        for _ in range(m):
            q = rng.choice(list(f)); i = rng.randrange(f[q] + 1)
            el.append((base + q ** i * (n // q ** f[q]) * rng.randrange(q ** (f[q] - i) if i < f[q] else 1)) % n)
    else:
        el = []
        while len(el) < m:
            q = rng.choice(list(f)); i = rng.randrange(f[q]); c = rng.choice(el) if el and rng.random() < 0.6 else rng.randrange(n)
            if len(el) + q <= m and rng.random() < 0.85:
                el += [(c + q ** i * (n // q ** f[q]) * j) % n for j in range(q)]
            else:
                el.append(rng.randrange(n))
    target = full_levels(el, n)
    td = run(el, n, lambda c: max(c, key=lambda pt: pt[1]))          # highest level first
    bu = run(el, n, lambda c: min(c, key=lambda pt: pt[1]))          # lowest level first
    rs = [run(el, n, lambda c: rng.choice(c)) for _ in range(3)]
    assert td == target, ('top-down does not end on the full levels', n, el, td, target)
    for other in [bu] + rs:
        assert other % td == 0, ('another order ends on a group that is not a multiple', n, el, td, other)
    if bu != td or any(r != td for r in rs):
        differ += 1
        if worst is None or bu // td > worst[0]:
            worst = (bu // td, n, el, td, bu)
print(f'{count} multisets of 2..14 elements on {shapes}: top-down always ends on the product of p^(number of levels with a full group); '
      f'every other order ends on a multiple of it; some order ended on a larger group for {differ} multisets')
if worst:
    print(f'   largest ratio bottom-up / top-down: {worst[0]}: Z_{worst[1]}, B = {worst[2]}, top-down ends on Z_{worst[3]}, bottom-up on Z_{worst[4]}')
# the smallest example, by hand in the report: Z_9, B = {0, 3, 7} (digits (0,0), (0,1), (1,2))
el = [0, 3, 7]
print('Z_9, B = {0, 3, 7}: level 1 contractible:', contractible(el, 3, 2, 1), '; level 2 contractible:', contractible(el, 3, 2, 2),
      '; level 1 first gives', contract(el, 9, 3, 2, 1), 'on Z_3, contractible:', contractible(contract(el, 9, 3, 2, 1), 3, 1, 1),
      '; level 2 first gives', contract(el, 9, 3, 2, 2), 'on Z_3, contractible:', contractible(contract(el, 9, 3, 2, 2), 3, 1, 1))
