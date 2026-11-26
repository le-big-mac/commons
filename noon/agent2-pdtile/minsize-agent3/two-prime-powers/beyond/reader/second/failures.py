"""Second pass: why the 17 derivations of algebra3.py fail.  The reader's own builder follows the recorded derivation (random lifts and
translates, as realise3.py does) and reports, for each pattern that realise3.py could not build: what the built multiset's pattern is
against the claimed one over 40 tries; and at every balanced lift inside the derivation, whether each class modulo r^(j-1) of the
multiset being lifted lies in one class modulo the other prime s (then Phi_{r^j s} cannot be kept out), and whether Phi_{r^j s} came in.
usage: failures.py"""
import sys, random, collections
sys.path.insert(0, '/home/agent3/pq2/rule/reader'); sys.path.insert(1, '/home/agent3/pq2/rule'); sys.dont_write_bytecode = True
from pat import pattern, divisors
from algebra3 import Calc
random.seed(3)
def pat(els, N):
    v = [0] * N
    for x in els: v[x % N] += 1
    return frozenset(pattern(v, N, routes=2))
def lift(els, N1, N): return [(x % N1 + N1 * random.randrange(N // N1)) % N for x in els]
LOG = []
def build(C, N, P, s, how=None):
    h = how if how is not None else (C.how[P] if N == C.M else C.S[N][P][s]); k = h[0]
    if k == 'atom':
        N1, c = h[1], h[2]; x0 = random.randrange(N1); return lift([(x0 + c * j) % N1 for j in range(N1 // c)], N1, N)
    if k == 'lift': return lift(build(C, h[1], h[2], h[3]), h[1], N)
    if k == 'L': return lift(build(C, N, h[2], h[3]), h[1], N)
    if k in ('+', 'x'):
        A, B = build(C, N, h[1], h[2]), build(C, N, h[3], h[4])
        if k == 'x': return [(a + b) % N for a in A for b in B]
        t = random.randrange(N); return A + [(b + t) % N for b in B]
    if k == 'dil':
        c, K, T, w = h[1:]; t = random.randrange(N); return [(c * b + t) % N for b in build(C, K, T, w)]
    if k == 'stack':
        c, K, membs, w = h[1:]; out = []
        order = list(membs) + [random.choice(membs) for _ in range(c - len(membs))]; random.shuffle(order)
        for r, T in enumerate(order):
            t = random.randrange(K); out += [(r + c * ((b + t) % K)) % N for b in build(C, K, T, w)]
        return out
    if k == 'bal':
        r, j, K, P0, s0 = h[1:]; B = build(C, K, P0, s0); rj1 = r ** (j - 1); out = []
        cls = collections.defaultdict(list)
        for x in B: cls[x % rj1].append(x)
        for rho, xs in cls.items():
            tg = list(range(r)) * (len(xs) // r); random.shuffle(tg)
            for x, t in zip(xs, tg): out.append(next(x + K * i for i in range(r) if (x + K * i) % (rj1 * r) == rho + rj1 * t))
        s = C.q if r == C.p else C.p
        if (N // r ** j) % s == 0:
            one_cell = all(len({x % s for x in xs}) == 1 for xs in cls.values())
            LOG.append((N, r, j, tuple(sorted(P0)), s0, one_cell, pat(B, K) == P0, (r ** j * s) in pat(out, N)))
        return out
    raise ValueError(h)
FAILS = {36: [[2, 4, 6], [6, 12, 18], [2, 4, 6, 9], [2, 4, 6, 18], [3, 6, 9, 12], [2, 4, 6, 9, 18], [2, 4, 6, 12, 18], [2, 3, 4, 6, 12, 18]],
         100: [[2, 4, 10], [10, 20, 50], [2, 4, 10, 25], [2, 4, 10, 50], [2, 4, 10, 20, 50], [2, 4, 10, 25, 50], [2, 4, 5, 10, 20, 50]],
         225: [[3, 9, 15, 75], [5, 15, 25, 45]]}
tot = collections.Counter()
for M, p, q in ((36, 2, 3), (100, 2, 5), (225, 3, 5)):
    C = Calc(p, q)
    for D in FAILS[M]:
        P = frozenset(D); got = collections.Counter(); LOG.clear(); balstat = collections.Counter()
        for _ in range(40):
            els = build(C, M, P, C.U[P]); pp = pat(els, M)
            got[(tuple(sorted(pp - P)), tuple(sorted(P - pp)))] += 1
        for (N, r, j, P0, s0, one_cell, inputok, came) in LOG: balstat[(f'bal Z_{N // r}->Z_{N} of {list(P0)} size {s0}', 'input in one class mod s per class' if one_cell else 'input in several', 'r^j s came in' if came else 'r^j s kept out')] += 1
        nbal = len({k[0] for k in balstat})
        print(f'Z_{M} {D} cost {C.U[P]} (last move {C.how[P][0]}): (divisors too many, divisors missing) over 40 builds: {dict(got)}')
        for k, v in sorted(balstat.items()): print('      ', v, k)
        tot['derivations'] += 1; tot['with a balanced lift inside'] += (nbal > 0)
        tot['where the pattern was right in some build'] += ((), ()) in got
        tot['where every build had a divisor too many and none missing'] += all(a and not b for (a, b) in got)
        tot['where every balanced lift had its input in one class mod s and r^j s came in every time'] += (nbal > 0 and all(k[1].startswith('input in one') and k[2].startswith('r^j s came') for k in balstat))
print(dict(tot))
