"""Second pass: the balanced lift, tested hard.
(1) What the derivation of algebra3.py for {3, 9, 15, 75} on Z_225 (cost 9, not realised) is, and what nine elements it builds on Z_75.
(2) The note's example: nine elements of Z_75 with pattern {3, 15, 75}; balanced lift to Z_225; which divisors come in.  Two kinds of
    nine elements: the three cosets of 25Z_75 all in one class modulo 5, and in different classes modulo 5.
(3) Random test of the move on Z_N for N in several groups: the pattern on the divisors of K = N/r is kept, r^j comes in; how often
    another divisor r^j d' comes in; and the criterion for d' = a prime s: Phi_{r^j s} comes in exactly when every cell
    (class modulo r^(j-1), class modulo s) is spread evenly over its r lifts.
usage: balanced.py [seed]"""
import sys, random, collections, itertools
sys.path.insert(0, '/home/agent3/pq2/rule/reader'); sys.path.insert(1, '/home/agent3/pq2/rule'); sys.dont_write_bytecode = True
from pat import pattern, divisors
random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 5)
def vec(els, N):
    v = [0] * N
    for x in els: v[x % N] += 1
    return v
def pat(els, N): return pattern(vec(els, N), N, routes=2)
def balanced_lift(B, K, r, j, how='random'):
    """B a list of elements of Z_K, K = N / r, r^(j-1) exactly dividing K.  Each class modulo r^(j-1) is spread evenly over its r lifts modulo r^j."""
    N = K * r; rj1 = r ** (j - 1); out = []
    cls = collections.defaultdict(list)
    for x in B: cls[x % rj1].append(x)
    for rho, xs in cls.items():
        assert len(xs) % r == 0
        xs = xs[:]; random.shuffle(xs)
        tg = list(range(r)) * (len(xs) // r)
        if how == 'random': random.shuffle(tg)
        for x, t in zip(xs, tg):
            y = next(x + K * i for i in range(r) if (x + K * i) % (rj1 * r) == rho + rj1 * t); out.append(y)
    return out
# ---- (1) the derivation in the note's program
from algebra3 import Calc
C = Calc(3, 5)
def show(N, P, s, how=None, depth=0, seen=None):
    h = how if how is not None else (C.how[P] if N == C.M else C.S[N][P][s])
    print('      ' + '   ' * depth + f'on Z_{N}: pattern {sorted(P)}, size {s}: {h[0]} {[sorted(t) if isinstance(t, frozenset) else t for t in h[1:]]}')
    k = h[0]
    if k == 'lift': show(h[1], h[2], h[3], depth=depth + 1)
    elif k == 'L': show(N, h[2], h[3], depth=depth + 1)
    elif k in ('+', 'x'): show(N, h[1], h[2], depth=depth + 1); show(N, h[3], h[4], depth=depth + 1)
    elif k == 'dil': show(h[2], h[3], h[4], depth=depth + 1)
    elif k == 'stack':
        for T in h[3]: show(h[2], T, h[4], depth=depth + 1)
    elif k == 'bal': show(h[3], h[4], h[5], depth=depth + 1)
for D in (frozenset({3, 9, 15, 75}), frozenset({5, 15, 25, 45})):
    print(f'(1) the derivation recorded for {sorted(D)} on Z_225, cost {C.U[D]}:'); show(225, D, C.U[D])
# ---- (2) the note's example
print('(2) nine elements of Z_75 with pattern {3, 15, 75} = three cosets of 25 Z_75; balanced lift to Z_225 (r = 3, j = 2), 300 random lifts each')
for name, xs in (('three cosets in ONE class modulo 5 (x = 0, 5, 10)', (0, 5, 10)), ('the same coset three times (x = 0, 0, 0)', (0, 0, 0)), ('three cosets in three classes modulo 5 (x = 0, 1, 2)', (0, 1, 2)),
                 ('two classes modulo 5 (x = 0, 5, 1)', (0, 5, 1))):
    B = [(x + 25 * i) % 75 for x in xs for i in range(3)]
    assert pat(B, 75) == [3, 15, 75]
    got = collections.Counter(tuple(pat(balanced_lift(B, 75, 3, 2), 225)) for _ in range(300))
    print(f'    {name}: patterns of the lifted nine elements: {dict(got)}')
# an explicit nine-element multiset of Z_225 with pattern exactly {3, 9, 15, 75}, if the lift gives one
B = [(x + 25 * i) % 75 for x in (0, 1, 2) for i in range(3)]
for _ in range(200):
    L = balanced_lift(B, 75, 3, 2)
    if pat(L, 225) == [3, 9, 15, 75]: print('    nine elements of Z_225 with pattern exactly {3, 9, 15, 75}, made by a balanced lift:', sorted(L)); break
# ---- (3) random test of the move
def rnd(K):
    els = []
    for _ in range(random.randint(1, 3)):
        c = random.choice(divisors(K)); x = random.randrange(K); els += [(x + c * i) % K for i in range(K // c)]
    if random.random() < 0.3: els.append(random.randrange(K))
    return els
cnt = collections.Counter(); crit = collections.Counter()
CASES = [(225, 3), (225, 5), (36, 2), (36, 3), (100, 2), (100, 5), (45, 3), (75, 5), (12, 2), (18, 3), (20, 2), (50, 5), (9, 3), (25, 5), (4, 2)]
tried = 0
while tried < 3000:
    N, r = random.choice(CASES); j = 0
    while N % r ** (j + 1) == 0: j += 1
    K = N // r; B = rnd(K); pB = pat(B, K)
    if not all(r ** i in pB for i in range(1, j)) or len(B) % r ** j: continue
    tried += 1
    L = balanced_lift(B, K, r, j); pL = pat(L, N)
    assert [d for d in pL if K % d == 0] == pB, 'the pattern on the divisors of K changed'
    assert r ** j in pL, 'r^j did not come in'
    assert vec(L, K) == vec(B, K) and len(L) == len(B)
    extra = [d for d in pL if K % d and d != r ** j]
    cnt['lifts tried'] += 1; cnt['another divisor r^j d\' came in'] += bool(extra)
    # the criterion for d = r^j s, s the other prime
    for s in [t for t in divisors(N // r ** j) if t > 1 and all(t % u for u in range(2, t))]:
        cells = collections.defaultdict(collections.Counter)
        for y in L: cells[(y % r ** (j - 1), y % s)][y % r ** j] += 1
        even = all(len(set(c[rho + r ** (j - 1) * t] for t in range(r))) == 1 for (rho, _), c in cells.items())
        crit[(even, (r ** j * s) in pL)] += 1
for k, v in cnt.items(): print(f'(3) {k}: {v}')
print('(3) for d = r^j s (s the other prime): (every cell spread evenly, Phi_d divides):', dict(crit))
