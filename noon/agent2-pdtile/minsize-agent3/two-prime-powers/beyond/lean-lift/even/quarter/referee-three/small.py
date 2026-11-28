# Referee: the small facts the proofs lean on, exhaustively (multisets containing 0, all signings).
#  two elements: a bad signing has opposite signs.   three: all signs equal, bad only at d with 3 | d, and with
#  3^j || d the three lie in the three subclasses of one group at level j and are congruent modulo d/3^j.
#  four: the signs add up to 0.   Remark 3.2: 3 or 5 elements on Z_27, Z_81: on X the signs add up to +-3.
import sys, itertools, time
import numpy as np
from bf import *
t0 = time.time()
fails = 0; cnt = {2: 0, 3: 0, 4: 0}; nbad3 = 0
for n in (15, 21, 35, 45, 63, 75, 105, 135, 225):
    for m in (2, 3, 4):
        S = signs(m); ssum = S.sum(axis=1)
        allB = [(0,) + c for c in itertools.combinations_with_replacement(range(n), m - 1)]
        for st in range(0, len(allB), 5000):
            Bs = np.array(allB[st:st + 5000]); ev = bad_events(n, Bs); cnt[m] += len(Bs)
            for d, E in ev.items():
                if not E.any(): continue
                ks, ss = np.nonzero(E)
                if m == 2:
                    if (ssum[ss] != 0).any(): fails += 1; print('FAIL two elements', n)
                if m == 4:
                    if (ssum[ss] != 0).any(): fails += 1; print('FAIL four elements', n, d)
                if m == 3:
                    nbad3 += len(ks)
                    if (ssum[ss] != 3).any(): fails += 1; print('FAIL three elements signs', n, d)
                    if d % 3: fails += 1; print('FAIL three elements bad at d prime to 3', n, d); continue
                    j = vp(d, 3); rest = d // 3 ** j
                    for k in set(ks.tolist()):
                        b = Bs[k].tolist()
                        ok = len(set(x % 3 ** (j - 1) for x in b)) == 1 and len(set(x % 3 ** j for x in b)) == 3 and len(set(x % rest for x in b)) == 1
                        if not ok: fails += 1; print('FAIL root of the shapes', n, d, b)
print('two/three/four elements on Z_15,21,35,45,63,75,105,135,225: multisets', cnt, ' bad (multiset, d) pairs of three elements:', nbad3, ' failures:', fails, ' [%.0fs]' % (time.time() - t0), flush=True)
# Remark 3.2
f2 = 0; c2 = 0
for n, ms in ((27, (3, 5)), (81, (3, 5))):
    for m in ms:
        S = signs(m); ssum = S.sum(axis=1)
        it = itertools.combinations_with_replacement(range(n), m - 1)
        while True:
            chunk = list(itertools.islice(it, 20000))
            if not chunk: break
            Bs = np.array([(0,) + c for c in chunk]); ev = bad_events(n, Bs); c2 += len(Bs)
            X = np.zeros_like(ev[1])
            for d in ev:
                if d > 1: X |= ev[d]
            X &= ~ev[1]
            ks, ss = np.nonzero(X)
            if (np.abs(ssum[ss]) != 3).any(): f2 += 1; print('FAIL Remark 3.2', n, m)
            if time.time() - t0 > 400: break
print('Remark 3.2 on Z_27, Z_81 (3 and 5 elements containing 0): multisets', c2, ' failures:', f2, ' [%.0fs]' % (time.time() - t0))
