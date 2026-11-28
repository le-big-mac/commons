# Referee's test of the theorem and of the intermediate statements of result.md, brute force.
# usage: test_theorem.py MODE n m [count seed]
#   MODE = ex  : every multiset of m elements of Z_n containing 0
#   MODE = rnd : `count` structured random multisets
import sys, time, random, itertools
import numpy as np
from fractions import Fraction as Fr
from math import comb
from bf import *
sys.path.insert(0, '.')
import importlib

mode, n, m = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
count = int(sys.argv[4]) if len(sys.argv) > 4 else 0
seed = int(sys.argv[5]) if len(sys.argv) > 5 else 1
tlimit = float(sys.argv[6]) if len(sys.argv) > 6 else 540.0
rng = random.Random(seed)
t0 = time.time()

# ---- the text's numbers, typed in from result.md (not from its programs) ----
def c(r): return Fr(comb(r, r // 2), 2 ** r) if r % 2 == 0 else Fr(0)
E3 = {1: 0, 2: 0, 3: Fr(1, 4), 4: Fr(0), 5: Fr(3, 16), 6: Fr(1, 32), 7: Fr(5, 32), 8: Fr(1, 32), 9: Fr(35, 256), 10: Fr(5, 128),
      11: Fr(63, 512), 12: Fr(9, 256), 13: Fr(231, 2048), 14: Fr(309, 8192), 15: Fr(429, 4096), 16: Fr(297, 8192)}
BB = {1: Fr(0), 2: Fr(1, 2), 3: Fr(1, 4), 4: Fr(3, 8), 5: Fr(1, 4), 6: Fr(3, 8), 7: Fr(7, 32), 8: Fr(11, 32), 9: Fr(31, 128),
      10: Fr(91, 256), 11: Fr(331, 1024), 12: Fr(679, 2048)}
# sharpest claims of the text: exact values for m <= 8, Remark 6.1 for 9..12, Theorem 7 beyond
BETA = {3: Fr(1, 4), 4: Fr(3, 8), 5: Fr(1, 4), 6: Fr(11, 32), 7: Fr(7, 32), 8: Fr(39, 128), 9: Fr(25, 128), 10: Fr(83, 256),
        11: Fr(235, 1024), 12: Fr(615, 2048), 13: Fr(469, 2048), 14: Fr(2977, 8192), 15: Fr(905, 4096), 16: Fr(11431, 32768)}

def omega(R): return Fr(1) if R == 0 else (Fr(0) if R == 1 else Fr(1, 2))
def pairings(idx, npairs):
    if npairs == 0:
        yield []; return
    if len(idx) < 2 * npairs: return
    a = idx[0]
    for p in pairings(idx[1:], npairs): yield p
    for j in range(1, len(idx)):
        for p in pairings(idx[1:j] + idx[j + 1:], npairs - 1): yield [(a, idx[j])] + p
def lam(sizes, R, q):
    """returns (bound, beyond1) : beyond1 = True if the bound is for the event minus 'bad at 1'"""
    k = sum(1 for r in sizes if r == 1)
    if k >= 1:
        v = Fr(1, 2 ** (k - 1))
        for r in sizes:
            if r >= 2: v *= BB[r + 1]
        return v * omega(R), False
    best = min(np.prod([BB[sizes[a] + sizes[b]] for a, b in p]) for p in pairings(list(range(q)), q // 2))
    sz = tuple(sorted(sizes, reverse=True))
    if q == 5:
        if sz == (2, 2, 2, 2, 2):
            if R == 0: return Fr(2, 1024), True
            if R >= 2: return Fr(34, 1024) * omega(R), False
        if sz == (4, 2, 2, 2, 2) and R == 0:
            return Fr(2, 1024) + (BB[6] - c(6)) / 8, True
        if sz == (3, 3, 2, 2, 2):
            return min(best, BB[5] ** 2 / 2) * omega(R), False
    return best * omega(R), False

fac = factor(n)
divs = divisors(n)
pow3 = [d for d in divs if d > 1 and set(factor(d)) == {3}]
bigq = [q for q in fac if q >= 5]
half = 2 ** (m - 1)

stats = dict(multisets=0, maxbad=Fr(0), maxbad_B=None, maxX=Fr(0), maxX_B=None, max3=Fr(0), fails=0, livelevels=0,
             Lnonempty=0, prop5_tight=0, twolevels=0, m8_L5=0, m8_L7=0, m6_L5=0, maxL={})
failures = []
def fail(msg):
    stats['fails'] += 1
    if len(failures) < 30: failures.append(msg)
    print('FAIL', msg, flush=True)

def process(Bs):
    Bs = np.asarray(Bs, dtype=np.int64)
    ev = bad_events(n, Bs)
    K = Bs.shape[0]
    bad = np.zeros((K, half), dtype=bool)
    for d in divs: bad |= ev[d]
    bad1 = ev[1]
    b3 = bad1.copy()
    for d in pow3: b3 |= ev[d]
    X = b3 & ~bad1
    L = {}
    for d in divs:
        q = largest_prime(d)
        if q >= 5:
            key = (q, vp(d, q))
            if key in L: L[key] = L[key] | ev[d]
            else: L[key] = ev[d].copy()
    nb = bad.sum(axis=1); nX = X.sum(axis=1); n3 = b3.sum(axis=1)
    stats['multisets'] += K
    # bad at 1 has share exactly c(m)
    if not (bad1.sum(axis=1) * 2 ** m == comb(m, m // 2) * half * (1 - m % 2)).all(): fail('bad at 1 share')
    i = int(nb.argmax()); v = Fr(int(nb[i]), half)
    if v > stats['maxbad']: stats['maxbad'], stats['maxbad_B'] = v, Bs[i].tolist()
    i = int(nX.argmax()); v = Fr(int(nX[i]), half)
    if v > stats['maxX']: stats['maxX'], stats['maxX_B'] = v, Bs[i].tolist()
    v = Fr(int(n3.max()), half)
    if v > stats['max3']: stats['max3'] = v
    # the theorem with the sharpest claimed bound, and Theorem 6 / Proposition 3
    if m in BETA:
        for i in np.nonzero(nb * BETA[m].denominator > BETA[m].numerator * half)[0]:
            fail('bad share %s > claimed %s  n=%d B=%s' % (Fr(int(nb[i]), half), BETA[m], n, Bs[i].tolist()))
    for i in np.nonzero(nX * E3[m].denominator > E3[m].numerator * half)[0] if m in E3 else []:
        fail('P(X) %s > E3 %s n=%d B=%s' % (Fr(int(nX[i]), half), E3[m], n, Bs[i].tolist()))
    # multisets where some L is nonempty: tree analysis
    anyL = np.zeros(K, dtype=bool)
    Lcount = {key: arr.sum(axis=1) for key, arr in L.items()}
    for key in L: anyL |= Lcount[key] > 0
    # Lemma P needs live status; a signing bad, not at a power of 3, must be in a live L
    rest = bad & ~b3
    need = anyL | rest.any(axis=1)
    for i in np.nonzero(need)[0]:
        B = Bs[i].tolist()
        cover = np.zeros(half, dtype=bool)
        liveL = {}
        for q in bigq:
            tl = tree_levels(n, B, q)
            live = [lv for lv in tl if any(full for (_, full) in tl[lv])]
            # (F3)
            if len(live) > (m - 1) // (q - 1): fail('F3 n=%d B=%s q=%d' % (n, B, q))
            for lv in live:
                stats['livelevels'] += 1
                ev_L = L[(q, lv)][i]
                cover |= ev_L
                pL = Fr(int(ev_L.sum()), half)
                liveL[(q, lv)] = pL
                if pL > 0: stats['Lnonempty'] += 1
                for (sizes, full) in tl[lv]:
                    if not full: continue
                    R = m - sum(sizes)
                    if m <= 12:
                        bound, beyond = lam(sizes, R, q)
                        val = Fr(int((ev_L & ~bad1[i]).sum()), half) if beyond else pL
                        keyS = (q, sizes, R)
                        if val > stats['maxL'].get(keyS, (Fr(-1),))[0]: stats['maxL'][keyS] = (val, bound)
                        if val > bound: fail('Prop 5: P(L)=%s > lambda=%s n=%d B=%s q=%d level=%d sizes=%s R=%d' % (val, bound, n, B, q, lv, sizes, R))
                        if val == bound and bound > 0: stats['prop5_tight'] += 1
            # Remark 6.1
            if len(live) >= 2:
                stats['twolevels'] += 1
                for lv in live[1:]:
                    if L[(q, lv)][i].any() and m < 3 * q - 2:
                        fail('Remark 6.1: n=%d B=%s q=%d deeper level %d nonempty with m=%d' % (n, B, q, lv, m))
        if (rest[i] & ~cover).any(): fail('Lemma P: n=%d B=%s' % (n, B))
        # the case analyses for six and eight elements
        if m == 6:
            l5 = [p for (q, lv), p in liveL.items() if q == 5 and p > 0]
            if l5:
                stats['m6_L5'] += 1
                if nX[i] > 0: fail('m=6: L5 nonempty and X nonempty n=%d B=%s' % (n, B))
                if l5[0] > Fr(1, 32): fail('m=6: P(L5) > 1/32')
        if m == 8:
            l5 = [((q, lv), p) for (q, lv), p in liveL.items() if q == 5 and p > 0]
            l7 = [((q, lv), p) for (q, lv), p in liveL.items() if q == 7 and p > 0]
            un = X[i].copy()
            for (key, p) in l5 + l7: un |= L[key][i]
            if Fr(int(un.sum()), half) > Fr(8, 256): fail('m=8: P(X u L5 u L7) > 8/256 n=%d B=%s' % (n, B))
            if l7:
                stats['m8_L7'] += 1
                if l7[0][1] > Fr(2, 256): fail('m=8: P(L7) > 2/256 n=%d B=%s' % (n, B))
                if nX[i] > 0: fail('m=8: L7 nonempty and X nonempty n=%d B=%s' % (n, B))
            if l5:
                stats['m8_L5'] += 1
                if l5[0][1] > Fr(6, 256): fail('m=8: P(L5) > 6/256 n=%d B=%s' % (n, B))
                tl = tree_levels(n, B, 5)
                fullsizes = [s for (s, full) in tl[l5[0][0][1]] if full]
                if nX[i] > 0:
                    if fullsizes != [(2, 2, 2, 1, 1)]: fail('m=8: L5 nonempty, X nonempty, sizes %s n=%d B=%s' % (fullsizes, n, B))
                    elif Fr(int(nX[i]), half) > Fr(4, 256): fail('m=8: (2,2,2,1,1) P(X) > 4/256 n=%d B=%s' % (n, B))

def gen_structured():
    # palettes per prime power with tree structure; skewed multiplicities
    comps = []
    for p, a in fac.items():
        pa = p ** a
        npal = rng.randint(1, min(pa, p + 2))
        pal = set()
        base = rng.randrange(pa)
        while len(pal) < npal:
            kind = rng.random()
            if kind < 0.5:
                lvl = rng.randrange(a)       # differ from base at one digit
                pal.add((base + rng.randrange(p) * p ** lvl) % pa)
            elif kind < 0.8 and pal:
                b2 = rng.choice(sorted(pal)); lvl = rng.randrange(a)
                pal.add((b2 + rng.randrange(p) * p ** lvl) % pa)
            else:
                pal.add(rng.randrange(pa))
        pal = sorted(pal)
        w = [rng.choice([1, 1, 1, 2, 4, 8]) for _ in pal]
        comps.append((pa, pal, w))
    B = []
    style = rng.random()
    for _ in range(m):
        x = 0; mod = 1
        for (pa, pal, w) in comps:
            r = rng.choices(pal, w)[0]
            # CRT
            while x % pa != r: x += mod
            mod *= pa
        B.append(x % n)
    if style < 0.3:
        # repeat some elements
        for _ in range(rng.randint(1, max(1, m // 2))):
            B[rng.randrange(m)] = B[rng.randrange(m)]
    elif style < 0.4:
        B = [rng.randrange(n) for _ in range(m)]
    return B


def parts5(total, k, mx=None):
    if mx is None: mx = total
    if k == 0:
        if total == 0: yield ()
        return
    for f in range(min(mx, total - k + 1), 0, -1):
        if f * k < total: break
        for rest in parts5(total - f, k - 1, f): yield (f,) + rest

E5 = fac.get(5, 0); A3 = fac.get(3, 0); E7 = fac.get(7, 0)
STRUCTS = []
for R in range(0, m - 5 + 1):
    if R == 1 or (R > 0 and E5 < 2): continue
    for sz in parts5(m - R, 5): STRUCTS.append((sz, R))
WANT = None
if len(sys.argv) > 7:
    WANT = [tuple(int(x) for x in s.split(',')) for s in sys.argv[7].split('/')]   # e.g. 2,2,2,2,2,0/4,2,2,2,2,0  (last = R)
    STRUCTS = [(w[:-1], w[-1]) for w in WANT]

def crt(res):
    x = 0; mod = 1
    for pa, r in res:
        while x % pa != r % pa: x += mod
        mod *= pa
    return x

def gen_targeted():
    sizes, R = rng.choice(STRUCTS)
    # 5-parts
    c5 = []
    kind = rng.random()
    if E5 == 1:
        for t, s in enumerate(sizes): c5 += [t] * s
    elif R == 0 and kind < 0.4:
        ks = [rng.randrange(5) if rng.random() < 0.3 else 0 for _ in range(5)]
        for t, s in enumerate(sizes): c5 += [t + 5 * ks[t]] * s
    else:
        c0 = rng.randrange(5)
        for t, s in enumerate(sizes): c5 += [c0 + 5 * t] * s
        c1 = (c0 + rng.randrange(1, 5)) % 5; u = rng.randrange(5)
        for _ in range(R):
            if rng.random() < 0.8: c5.append(c1 + 5 * u)
            else: c5.append((c0 + rng.randrange(1, 5)) % 5 + 5 * rng.randrange(5))
    single = [False] * m
    pos = 0
    for s in sizes:
        if s == 1: single[pos] = True
        pos += s
    # 7-parts
    c7 = [0] * m
    if E7:
        k7 = rng.random()
        if k7 < 0.3 and m >= 7:
            perm = list(range(m)); rng.shuffle(perm)
            for idx, e in enumerate(perm): c7[e] = idx if idx < 7 else rng.choice([0, 0, 0, rng.randrange(7)])
        elif k7 < 0.45:
            c7 = [rng.randrange(7) for _ in range(m)]
        if E7 == 2: c7 = [x + 7 * rng.choice([0, 0, 0, rng.randrange(7)]) for x in c7]
    # 3-parts
    c3 = [0] * m
    if A3:
        pa = 3 ** A3
        a0 = rng.randrange(pa); j = rng.randint(1, A3)
        k3 = rng.random()
        for e in range(m):
            if k3 < 0.1:
                d = 0
            else:
                w = [6, 1, 1] if single[e] else [2, 2, 2]
                d = rng.choices([0, 1, 2], w)[0] * 3 ** (j - 1)
            if rng.random() < 0.2 and j < A3: d += 3 ** j * rng.randrange(3 ** (A3 - j))
            if rng.random() < 0.05: d = rng.randrange(pa)
            c3[e] = (a0 + d) % pa
    B = []
    for e in range(m):
        res = []
        if A3: res.append((3 ** A3, c3[e]))
        if E5: res.append((5 ** E5, c5[e]))
        if E7: res.append((7 ** E7, c7[e]))
        for p, a in fac.items():
            if p not in (3, 5, 7): res.append((p ** a, 0 if rng.random() < 0.7 else rng.randrange(p ** a)))
        B.append(crt(res) % n)
    return B

def gen_seven():
    # eight elements; the 7-tree has a full group with sizes (2,1,1,1,1,1,1); 3-parts aligned so that the six single
    # elements are congruent modulo 3^j and the pair sits in the two other subclasses of their group at level j
    perm = list(range(m)); rng.shuffle(perm)
    c7 = [0] * m
    for idx, e in enumerate(perm): c7[e] = idx if idx < 7 else 0
    pair = [perm[0], perm[7]] if m == 8 else [perm[0]]
    if E7 == 2:
        k = rng.randrange(7); c7 = [7 * x + k for x in c7]
    c3 = [0] * m
    if A3:
        pa = 3 ** A3; a0 = rng.randrange(pa); j = rng.randint(1, A3); u = rng.choice([1, 2])
        for e in range(m):
            d = 0
            if rng.random() < 0.25 and j < A3: d = 3 ** j * rng.randrange(3 ** (A3 - j))
            if rng.random() < 0.06: d = rng.randrange(pa)
            c3[e] = (a0 + d) % pa
        if rng.random() < 0.8 and len(pair) == 2:
            c3[pair[0]] = (c3[pair[0]] + u * 3 ** (j - 1)) % pa; c3[pair[1]] = (c3[pair[1]] + 2 * u * 3 ** (j - 1)) % pa
    c5 = [0] * m
    if E5:
        k5 = rng.random()
        if k5 < 0.45:
            v = rng.randrange(5 ** E5); c5 = [v] * m
        elif k5 < 0.85:
            sizes = rng.choice([(4, 1, 1, 1, 1), (3, 2, 1, 1, 1), (2, 2, 2, 1, 1)])
            lab = []
            for t, s in enumerate(sizes): lab += [t] * s
            rng.shuffle(lab); c5 = lab
        else:
            c5 = [rng.randrange(5 ** E5) for _ in range(m)]
    B = []
    for e in range(m):
        res = [(7 ** E7, c7[e])]
        if A3: res.append((3 ** A3, c3[e]))
        if E5: res.append((5 ** E5, c5[e]))
        B.append(crt(res) % n)
    return B

BATCH = max(4, min(4000, (1 << 22) // (half * m), 25000000 // (half * max(len(cyclo(d)) - 1 for d in divs))))
if mode == 'ex':
    buf = []
    done = True
    for comb_ in itertools.combinations_with_replacement(range(n), m - 1):
        buf.append((0,) + comb_)
        if len(buf) == BATCH:
            process(buf); buf = []
            if time.time() - t0 > tlimit:
                done = False; break
    if buf and done: process(buf)
    print('exhaustive n=%d m=%d: %s' % (n, m, 'COMPLETE' if done else 'STOPPED EARLY (time)'))
else:
    left = count
    while left > 0 and time.time() - t0 < tlimit:
        k = min(BATCH, left)
        process([gen_seven() for _ in range(k)]); left -= k
    print('%s n=%d m=%d seed=%d %s' % ('targeted (full group (2,1,1,1,1,1,1) of 7, aligned 3-parts)', n, m, seed, sys.argv[7] if len(sys.argv) > 7 else ''))
print('  multisets %d  largest bad share %s (claimed bound %s) at %s' % (stats['multisets'], stats['maxbad'], BETA.get(m), stats['maxbad_B']))
print('  largest P(X) %s (E3 = %s) at %s ; largest share bad at a power of 3: %s (c+E3 = %s)' % (stats['maxX'], E3.get(m), stats['maxX_B'], stats['max3'], c(m) + E3[m] if m in E3 else None))
print('  live levels of primes >= 5 looked at (only where some L nonempty or needed): %d ; L nonempty: %d ; Prop 5 bound attained: %d ; two live levels: %d' % (stats['livelevels'], stats['Lnonempty'], stats['prop5_tight'], stats['twolevels']))
if m == 8: print('  m=8: L5 nonempty in %d, L7 nonempty in %d' % (stats['m8_L5'], stats['m8_L7']))
if m == 6: print('  m=6: L5 nonempty in %d' % stats['m6_L5'])
for k in sorted(stats['maxL'], key=str): print('    structure q=%d sizes=%s R=%d : largest %s  bound %s' % (k[0], k[1], k[2], stats['maxL'][k][0], stats['maxL'][k][1]))
print('  FAILURES: %d   time %.1fs' % (stats['fails'], time.time() - t0))
