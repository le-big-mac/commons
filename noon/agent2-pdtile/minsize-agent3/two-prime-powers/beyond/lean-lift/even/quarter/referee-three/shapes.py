# Referee: the three shapes (S-a), (S-b), (S-c) of result.md section 4, tested as stated on powers of 3.
# usage: shapes.py n m mode(ex|rnd) [count]
import sys, itertools, random, time
import numpy as np
from bf import *
n, m, mode = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
count = int(sys.argv[4]) if len(sys.argv) > 4 else 0
a = vp(n, 3); assert 3 ** a == n
rng = random.Random(n * 100 + m); t0 = time.time()
half = 2 ** (m - 1)
stat = dict(Sa=0, Sb1=0, Sb2=0, Sc=0, fails=0, tot=0, maxXc=0)

def classify(B):
    out = []
    for j in range(1, a + 1):
        groups = {}
        for b in B:
            groups.setdefault(b % 3 ** (j - 1), {}).setdefault(b % 3 ** j, 0)
            groups[b % 3 ** (j - 1)][b % 3 ** j] += 1
        gs = [sorted(g.values(), reverse=True) + [0] * (3 - len(g)) for g in groups.values()]
        def as_in_Sa(sz): return 1 in sz and len(set(x % 2 for x in sz)) > 1
        if len(gs) == 1:
            if as_in_Sa(gs[0]): out.append('Sa')
            if m == 8 and gs[0] == [3, 3, 2]: out.append('Sc')
        if len(gs) == 2:
            for g1, g2 in ((gs[0], gs[1]), (gs[1], gs[0])):
                if as_in_Sa(g1) and g2 == [2, 0, 0]: out.append('Sb1')
                if g1 == [1, 1, 1] and g2[1] == 0 and g2[0] % 2 == 1: out.append('Sb2')
    return out

def process(Bs):
    Bs = np.array(Bs); ev = bad_events(n, Bs)
    X = np.zeros_like(ev[1])
    for d in ev:
        if d > 1: X |= ev[d]
    X &= ~ev[1]
    nX = X.sum(axis=1)
    for k in range(len(Bs)):
        cl = classify(Bs[k].tolist()); stat['tot'] += 1
        for s in cl:
            stat[s] += 1
            if s == 'Sc':
                stat['maxXc'] = max(stat['maxXc'], int(nX[k]))
                if nX[k] * 256 > 4 * half: stat['fails'] += 1; print('FAIL S-c', Bs[k].tolist(), nX[k])
            elif nX[k] > 0: stat['fails'] += 1; print('FAIL', s, Bs[k].tolist(), nX[k])

def gen():
    j = rng.randint(1, a); base = rng.randrange(3 ** (j - 1)) if j > 1 else 0
    def el(t, grp=None):
        g = base if grp is None else grp
        return (g + t * 3 ** (j - 1) + 3 ** j * rng.choice([0, 0, rng.randrange(3 ** (a - j))])) % n
    kind = rng.random(); B = []
    if kind < 0.35:      # S-a like
        B = [el(0)] + [el(rng.choice([1, 1, 2, 2, 0])) for _ in range(m - 1)]
    elif kind < 0.6 and j > 1:   # S-b first kind
        g2 = (base + 3 ** rng.randrange(j - 1) * rng.randint(1, 2)) % 3 ** (j - 1)
        e = el(rng.randrange(3), g2)
        B = [el(0)] + [el(rng.choice([1, 1, 2])) for _ in range(m - 3)] + [e, e if rng.random() < 0.5 else (e + 3 ** j * rng.randrange(3 ** (a - j))) % n]
    elif kind < 0.8 and j > 1 and m >= 4:   # S-b second kind
        g2 = (base + 3 ** rng.randrange(j - 1) * rng.randint(1, 2)) % 3 ** (j - 1)
        t = rng.randrange(3)
        B = [el(0), el(1), el(2)] + [el(t, g2) for _ in range(m - 3)]
    elif m == 8:         # S-c
        B = [el(0) for _ in range(3)] + [el(1) for _ in range(3)] + [el(2) for _ in range(2)]
    else:
        B = [rng.randrange(n) for _ in range(m)]
    return B

if mode == 'ex':
    it = itertools.combinations_with_replacement(range(n), m - 1)
    while time.time() - t0 < 300:
        chunk = list(itertools.islice(it, 4000))
        if not chunk: break
        process([(0,) + c for c in chunk])
else:
    left = count
    while left > 0 and time.time() - t0 < 120:
        process([gen() for _ in range(2000)]); left -= 2000
print('shapes n=%d m=%d %s: multisets %d; with shape (S-a) %d, (S-b) first kind %d, second kind %d, (S-c) %d (largest number of X signings with first sign + : %d, allowed %d); failures %d  [%.0fs]' % (n, m, mode, stat['tot'], stat['Sa'], stat['Sb1'], stat['Sb2'], stat['Sc'], stat['maxXc'], 4 * half // 256 if m == 8 else 0, stat['fails'], time.time() - t0))
