"""Corollary 21 by complete enumeration, no solver.  For a group Z_L: every SET of at most K elements that contains 0
(a translate has the same pattern), its exact pattern among ALL divisors d > 1 of L by the exact integer remainder
(cyc.rem_table, int16 sums: at most K terms of size <= 2, no overflow).  For each pattern met: the least size.

Then, for every way L = p^n q * s (p != q primes, n >= 0... here n >= 1) and every pattern D of Z_{p^n q}: the theorem's m
(thm.theorem_m) beside the least size of a set on Z_L with pattern exactly D among the divisors of L.

usage: sets_enum.py L K"""
import sys, itertools
import numpy as np
from cyc import divisors, rem_table, cyclo
from thm import theorem_m, D_of, all_patterns


def enumerate_sets(L, K, chunk=200000):
    divs = [d for d in divisors(L) if d > 1]
    T = {}
    for d in divs:
        R = np.array(rem_table(d), dtype=np.int16)            # d x phi(d)
        assert np.abs(R).max() * K < 30000
        T[d] = R[np.arange(L) % d]                            # L x phi(d)
    best = {}                                                  # code -> (size, witness)
    counts = {}
    for k in range(1, K + 1):
        it = itertools.combinations(range(1, L), k - 1)
        n_k = 0
        while True:
            if k == 1:
                idx = np.zeros((1, 0), dtype=np.int16)
            else:
                flat = np.fromiter(itertools.chain.from_iterable(itertools.islice(it, chunk)), dtype=np.int16)
                if flat.size == 0:
                    break
                idx = flat.reshape(-1, k - 1)
            n = idx.shape[0]
            n_k += n
            code = np.zeros(n, dtype=np.int64)
            for b, d in enumerate(divs):
                R = np.broadcast_to(T[d][0], (n, T[d].shape[1])).copy()
                for c in range(k - 1):
                    R += T[d][idx[:, c]]
                code |= (~R.any(axis=1)).astype(np.int64) << b
            u, first = np.unique(code, return_index=True)
            for cval, i in zip(u.tolist(), first.tolist()):
                if cval not in best:
                    best[cval] = (k, (0,) + tuple(int(v) for v in idx[i]))
            if k == 1:
                break
        counts[k] = n_k
    out = {}
    for cval, (k, wit) in best.items():
        out[frozenset(d for b, d in enumerate(divs) if cval >> b & 1)] = (k, wit)
    return out, counts


def primes(n):
    return [p for p in range(2, n + 1) if n % p == 0 and all(p % t for t in range(2, int(p ** 0.5) + 1))]


def readings(L):
    """all (p, q, n, s) with p != q primes, n >= 1, p^n q s = L"""
    out = []
    for p in primes(L):
        for q in primes(L):
            if p == q:
                continue
            n = 1
            while L % (p ** n * q) == 0:
                out.append((p, q, n, L // (p ** n * q)))
                n += 1
    return out


if __name__ == '__main__':
    L, K = int(sys.argv[1]), int(sys.argv[2])
    best, counts = enumerate_sets(L, K)
    print(f'Z_{L}: every set of at most {K} elements that contains 0: {sum(counts.values())} sets '
          f'({", ".join(f"{k}: {v}" for k, v in counts.items())}); different exact patterns met: {len(best)}')
    for (p, q, n, s) in readings(L):
        M = p ** n * q
        odd = [r for r in primes(s) if r != 2]
        eq = more = less = big = 0
        lines = []
        cor = cor_ok = 0
        for E, F, bal in all_patterns(p, q, n):
            m = theorem_m(p, q, n, E, F, bal)
            D = D_of(p, q, n, E, F, bal)
            got = best.get(D)
            # does Corollary 21 apply as stated?  some odd prime power r^j | s with r^j > m
            applies = False
            for r in odd:
                j = 1
                while s % r ** j == 0:
                    if r ** j > m:
                        applies = True
                    j += 1
            if applies:
                cor += 1
            if m > K:
                big += 1
                assert got is None, ('a set smaller than the theorem allows', L, p, q, n, sorted(D), got)
                if applies:
                    lines.append(f'    (Corollary applies but m = {m} > K: not reached) D = {sorted(D)}')
                continue
            if got is None:
                more += 1
                lines.append(f'    NO SET OF SIZE <= {K}: D = {sorted(D)}, m = {m}, Corollary 21 applies as stated: {applies}')
            elif got[0] == m:
                eq += 1
                if applies:
                    cor_ok += 1
            elif got[0] > m:
                more += 1
                lines.append(f'    LEAST SET {got[0]} > m = {m}: D = {sorted(D)}, e.g. {got[1]}, Corollary 21 applies as stated: {applies}')
            else:
                less += 1
                lines.append(f'    !! SET SMALLER THAN m: D = {sorted(D)}, m = {m}, set {got}')
        print(f'  as Z_({p}^{n}*{q}) * {s} [Z_{M}, s = {s}; odd prime factors of s: {odd}]: patterns of Z_{M}: {2 ** (2 * n + 1)}; '
              f'with m <= {K}: {eq + more + less}; least set size = m: {eq}; least set size > m (or none up to {K}): {more}; '
              f'smaller than m: {less}; m > {K} (no set that small, as it must be): {big}; '
              f'patterns to which Corollary 21 applies as stated (an odd prime power r^j | s, r^j > m): {cor}, '
              f'of them confirmed least set = m: {cor_ok}')
        for l in lines:
            print(l)
