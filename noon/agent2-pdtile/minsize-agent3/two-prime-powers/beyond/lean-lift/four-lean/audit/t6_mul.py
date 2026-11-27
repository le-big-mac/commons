"""sizes_eq_mul_all: for N, s and every set P of divisors of N, the sizes t (0 < t <= S) of the multisets on Z_{Ns}
whose mask is divisible by Phi_d, among the d | Ns with d != 1, exactly for d in P, against the sizes of the multisets
on Z_N whose mask is divisible by Phi_d, among the d | N with d != 1, exactly for d in P.

A complete census of both groups up to size S (multisets that contain 0; the set of cyclotomic divisors does not
change under translation), with the census routine of t4b_sizes.py.  S is the largest size for which the census of
Z_{Ns} stays within BUDGET table cells (multisets x Ns x size), at most 12.
Each line also says whether the pair is outside the earlier audited statements: s even and not 2 (not sizes_eq_odd,
not sizes_eq_two_all alone), N not of the form p^n q (not sizes_eq_mul).
usage: t6_mul.py BUDGET N1,N2,... s1,s2,..."""
import os
import sys
import time
from math import comb
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import core
from t4b_sizes import census


def pick_S(M, budget):
    S = 1
    cost = M
    while S < 12:
        nxt = comb(M + S - 1, S) * M * (S + 1)
        if cost + nxt > budget:
            break
        cost += nxt
        S += 1
    return S


def is_pnq(N):
    f = core.factor(N)
    return (len(f) == 1 and min(f.values()) == 1) or (len(f) == 2 and min(f.values()) == 1)


if __name__ == '__main__':
    budget = int(float(sys.argv[1]))
    Ns = [int(x) for x in sys.argv[2].split(',')]
    ss = [int(x) for x in sys.argv[3].split(',')]
    for N in Ns:
        for s in ss:
            t0 = time.time()
            M = N * s
            S = pick_S(M, budget)
            small, c1 = census(N, S)
            big, c2 = census(M, S)
            divN = set(core.divisors(N))
            left = {P: z for P, z in big.items() if P <= divN}
            outside = {P: z for P, z in big.items() if not P <= divN}
            pats = set(left) | set(small)
            diff = [P for P in pats if left.get(P, set()) != small.get(P, set())]
            both = sum(1 for P in pats if left.get(P) and small.get(P))
            kind = ('s-even-not-2 ' if (s % 2 == 0 and s != 2) else 's-odd-or-2 ') + ('N-pnq' if is_pnq(N) else 'N-not-pnq')
            print('N = %d s = %d S = %d multisets %d and %d patterns-P-with-a-nonempty-side %d nonempty-on-both %d '
                  'DIFFERENT %d %s patterns-with-a-new-divisor %d kind %s (%.0f s)'
                  % (N, s, S, c1, c2, len(pats), both, len(diff),
                     [(sorted(P), sorted(left.get(P, [])), sorted(small.get(P, []))) for P in diff[:2]] if diff else '',
                     len(outside), kind, time.time() - t0), flush=True)
