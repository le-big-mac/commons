"""Evidence for the missing statement, exact arithmetic.  usage: tests2.py mprime | half
mprime: statement M: n even, N = n/2, B <-> (E, D) on Z_N, both nonempty, not both singletons, not both exceptional
        pairs on Z_N: is there a good signing of B in which S_E or S_D alone has no root of even order dividing N?
half:   odd n: the least share of good signings over all multisets containing 0 with m elements."""
import sys, itertools, random
import numpy as np
from lib import *

def evengood_all(N, els):
    """for all signings (not fixing the first sign) of the multiset els on Z_N: no even d | N with Phi_d | mask"""
    signs = all_signs(len(els), fix_first=False)
    ok = np.ones(len(signs), bool); idx = [x % N for x in els]
    for d in divisors(N):
        if d % 2 == 0: ok &= np.any(signs @ table(d, N)[idx], axis=1)
    return signs, ok

def t_mprime():
    cnt = 0; fails = []; twopairs = 0
    for n, M in ((4, 8), (8, 7), (16, 5), (12, 6), (24, 5), (20, 5), (40, 4), (36, 4), (48, 4), (60, 4), (28, 5), (72, 4)):
        N = n // 2; c0 = cnt
        for m in range(3, M + 1):
            for rest in itertools.combinations_with_replacement(range(n), m - 1):
                els = [0] + list(rest)
                iE = [i for i, x in enumerate(els) if x % 2 == 0]; iD = [i for i, x in enumerate(els) if x % 2 == 1]
                if not iD: continue
                E = [els[i] // 2 for i in iE]; D = [(els[i] - 1) // 2 for i in iD]
                if exceptional_pair(N, E) and exceptional_pair(N, D): twopairs += 1; continue
                signs, good = good_signings(n, els, fix_first=False)
                sE, okE = evengood_all(N, E); sD, okD = evengood_all(N, D)
                # index of the restriction of each signing to E and to D
                wE = 2 ** np.arange(len(iE) - 1, -1, -1); wD = 2 ** np.arange(len(iD) - 1, -1, -1)
                rE = ((1 - signs[:, iE]) // 2) @ wE; rD = ((1 - signs[:, iD]) // 2) @ wD
                if not (good & (okE[rE] | okD[rD])).any(): fails.append((n, els, bool(good.any())))
                cnt += 1
        print(f'n={n}: multisets with 0, 3..{M} elements, both halves occupied: {cnt - c0} tested; failures of M so far: {len(fails)}', flush=True)
    print('total', cnt, 'tested;', twopairs, 'with two exceptional halves left out; failures of M:', len(fails), fails[:20])

def t_half():
    from fractions import Fraction
    for n, M in ((3, 9), (5, 8), (7, 7), (9, 8), (15, 6), (21, 5), (27, 5), (45, 4), (105, 4)):
        for m in range(3, M + 1):
            least = None; arg = None; cnt = 0
            for rest in itertools.combinations_with_replacement(range(n), m - 1):
                els = [0] + list(rest)
                _, g = good_signings(n, els); fr = Fraction(int(g.sum()), len(g)); cnt += 1
                if least is None or fr < least: least, arg = fr, els
            print(f'odd n={n} m={m}: {cnt} multisets with 0; least share of good signings {least} = {float(least):.4f} at {arg}', flush=True)

if __name__ == '__main__':
    {'mprime': t_mprime, 'half': t_half}[sys.argv[1]]()
