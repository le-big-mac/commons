"""Exploration (27 November 2026): for EVEN n, which multisets on Z_n have NO signing whose signed mask is divisible by no
Phi_d, d | n?  (For odd n every nonempty multiset has one: Theorem 4.)  Every multiset containing 0 (every multiset
has such a translate, and translation changes no divisibility), every signing, exact arithmetic modulo Phi_d.
usage: explore.py N MAXSIZE   -> prints, for each size, the number of multisets and the bad ones (as sorted tuples),
with their heaps: the residues modulo 2^k, 2^k the power of 2 in N."""
import sys, itertools
import numpy as np
sys.path.insert(0, '/home/agent3/lean/lift-check/four-mine')
from plan_check import divisors, powers_mod
def run(n, maxsize):
    k2 = 1
    while n % (2 * k2) == 0: k2 *= 2
    ds = divisors(n); T = {d: powers_mod(d, n) for d in ds}
    out = {}
    for m in range(1, maxsize + 1):
        signs = np.array(list(itertools.product((1, -1), repeat=m)), dtype=np.int64)
        signs = signs[signs[:, 0] == 1]                      # a signing and its negative are bad at the same d
        nb = 0; bad = []
        for rest in itertools.combinations_with_replacement(range(n), m - 1):
            e = (0,) + rest; nb += 1
            good = np.ones(len(signs), bool)
            for d in ds:
                good &= np.any(signs @ T[d][list(e)], axis=1)
                if not good.any(): break
            if not good.any(): bad.append(e)
        out[m] = (nb, bad)
        heaps = lambda e: tuple(sorted(sum(1 for x in e if x % k2 == h) for h in range(k2)))
        print(f'n={n} m={m}: {nb} multisets containing 0, {len(bad)} with no good signing', flush=True)
        for e in bad[:40]: print('    ', e, ' heap sizes', heaps(e))
        if len(bad) > 40: print('     ... and', len(bad) - 40, 'more')
    return out
if __name__ == '__main__':
    run(int(sys.argv[1]), int(sys.argv[2]))
