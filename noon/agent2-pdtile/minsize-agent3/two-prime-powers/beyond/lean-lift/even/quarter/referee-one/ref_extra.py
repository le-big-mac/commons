"""Referee: the intermediate statements of the paragraphs "beta(6) = 11/32" and "beta(7)", and the remark on eight
elements, tested as stated (all signings, by the definition).

(a) six elements, some level j of 5 live:
    - if the full group holds only five of them: no signing is bad at any 3^i 5^j';
    - if it holds all six (sizes (2,1,1,1,1)): at most two signings are bad at some 3^i 5^j, they have sum of
      signs +-2 and are bad at one i only, i >= 1; if there are any, the signings bad at a power of 3 are exactly
      those with sum 0 (share 5/16); in every case the bad share is at most 11/32.
(b) eight elements: no signing is 3-bad at a live 5^j 7^k; bad share at most 45/128.
usage: ref_extra.py SEED COUNT
"""
import sys, random, itertools
from fractions import Fraction as Fr
import numpy as np
from cyc import divisors, signs, bad_at, three_bad_at, factor, live_levels
from ref_odd import crt_elem, share

seed, count = int(sys.argv[1]), int(sys.argv[2])
rnd = random.Random(seed)

# ---- (a)
st = dict(five=0, six=0, six_with_bad=0, none=0)
for _ in range(count):
    n = rnd.choice([15, 45, 135, 405, 75, 225, 675, 105, 315])
    f = factor(n); a3 = f[3]; P3 = 3 ** a3; v5 = f[5]; Q = 5 ** v5
    lvl = rnd.randint(1, v5); base = rnd.randrange(5 ** (lvl - 1))
    full = [(base + t * 5 ** (lvl - 1) + (rnd.randrange(Q // 5 ** lvl) * 5 ** lvl if lvl < v5 else 0)) % Q for t in range(5)]
    mode = rnd.randint(0, 3)
    if mode == 0:
        r5 = full + [rnd.choice(full)]                      # sixth inside the full group, same subclass at level lvl
    elif mode == 1:
        r5 = full + [rnd.randrange(Q)]
    elif mode == 2:
        r5 = [rnd.randrange(Q) for _ in range(6)]
    else:
        r5 = full + [(full[0] + rnd.randrange(Q // 5 ** lvl) * 5 ** lvl) % Q]
    k = rnd.randint(0, 3)
    if k == 0:                                               # the shape of the proof: (4,1,1) at some level of 3
        i = rnd.randint(1, a3); c0 = rnd.randrange(3 ** (i - 1))
        r3 = [(c0 + t * 3 ** (i - 1) + (rnd.randrange(P3 // 3 ** i) * 3 ** i if i < a3 else 0)) % P3 for t in (0, 0, 0, 0, 1, 2)]
        # put the two odd ones on the pair if there is one
        cnt = {}
        for x in r5:
            cnt[x % 5 ** lvl] = cnt.get(x % 5 ** lvl, 0) + 1
        pair = [j for j, x in enumerate(r5) if cnt[x % 5 ** lvl] == 2]
        if len(pair) == 2:
            order = [j for j in range(6) if j not in pair] + pair
            r3n = [0] * 6
            for pos, j in enumerate(order):
                r3n[j] = r3[pos]
            r3 = r3n
    elif k == 1:
        r3 = [rnd.randrange(P3) for _ in range(6)]
    elif k == 2:
        pool = [rnd.randrange(P3) for _ in range(3)]; r3 = [rnd.choice(pool) for _ in range(6)]
    else:
        r3 = [x % P3 for x in (0, 0, 1, 1, 2, 2)]; rnd.shuffle(r3)
    res = [{P3: u, Q: v} for u, v in zip(r3, r5)]
    if 7 in f:
        for r in res:
            r[7] = rnd.randrange(7)
    B = [crt_elem(n, r) for r in res]
    E = signs(6); sig = E.sum(axis=1)
    badd = {d: bad_at(n, B, d, E) for d in divisors(n)}
    bad = np.zeros(64, dtype=bool)
    for v in badd.values():
        bad |= v
    bad3 = np.zeros(64, dtype=bool)
    for i in range(a3 + 1):
        bad3 |= badd[3 ** i]
    assert share(bad) <= Fr(11, 32), ("beta(6)", n, B)
    live = live_levels(B, 5, v5)
    if not live:
        assert not np.any(bad & ~bad3), ("no live level", n, B); st['none'] += 1
        continue
    assert len(live) == 1
    j = live[0]
    groups = {}
    for b in B:
        groups.setdefault(b % 5 ** (j - 1), []).append(b % 5 ** j)
    fullsize = max(len(g) for g in groups.values() if len(set(g)) == 5)
    at35 = {i: badd[3 ** i * 5 ** j] for i in range(a3 + 1)}
    any35 = np.zeros(64, dtype=bool)
    for v in at35.values():
        any35 |= v
    if fullsize == 5:
        st['five'] += 1
        assert not any35.any(), ("five in the full group", n, B)
        assert not np.any(bad & ~bad3)
    else:
        st['six'] += 1
        assert int(any35.sum()) <= 2, ("more than two", n, B)
        if any35.any():
            st['six_with_bad'] += 1
            assert int(any35.sum()) == 2 and set(np.abs(sig[any35]).tolist()) == {2}
            assert sum(1 for v in at35.values() if v.any()) == 1 and not at35[0].any()
            assert np.array_equal(bad3, sig == 0), ("X(B) = 0", n, B)
            assert share(bad) == Fr(11, 32)
print(f"(a) six elements, seed {seed}: {count} multisets on Z_15 .. Z_675, Z_105, Z_315: {st}; every statement holds")

# ---- (b)
st = dict(both_live=0, total=0); best = Fr(0)
E = signs(8)
for _ in range(count):
    n = rnd.choice([105, 315, 525, 735, 35, 175, 245])
    f = factor(n); a3 = f.get(3, 0); P3 = 3 ** a3
    res = [dict() for _ in range(8)]
    for q in (5, 7):
        Q = q ** f[q]; lvl = rnd.randint(1, f[q]); base = rnd.randrange(q ** (lvl - 1))
        full = [(base + t * q ** (lvl - 1)) % Q for t in range(q)]
        rq = full + [rnd.choice(full) if rnd.random() < .7 else rnd.randrange(Q) for _ in range(8 - q)]
        rnd.shuffle(rq)
        for r, v in zip(res, rq):
            r[Q] = v
    if a3:
        k = rnd.randint(0, 2)
        r3 = [0, 0, 0, 0, 1, 1, 2, 2] if k == 0 else ([rnd.randrange(P3) for _ in range(8)] if k == 1 else [0, 0, 1, 1, 2, 2, 3 % P3, 3 % P3])
        rnd.shuffle(r3)
        for r, v in zip(res, r3):
            r[P3] = v
    B = [crt_elem(n, r) for r in res]
    bad = np.zeros(256, dtype=bool)
    for d in divisors(n):
        bad |= bad_at(n, B, d, E)
    assert share(bad) <= Fr(45, 128), ("45/128", n, B, share(bad))
    best = max(best, share(bad)); st['total'] += 1
    l5 = live_levels(B, 5, f[5]); l7 = live_levels(B, 7, f[7])
    for j in l5:
        for k in l7:
            st['both_live'] += 1
            assert not three_bad_at(n, B, 5 ** j * 7 ** k, E).any(), ("3-bad at a live 5^j 7^k", n, B)
print(f"(b) eight elements, seed {seed}: {st}; no signing 3-bad at a live 5^j 7^k; bad share <= 45/128 always; largest {best}")
