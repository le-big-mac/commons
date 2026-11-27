# sizes_eq_two, sizes_eq_odd, sizes_eq_mul against the censuses (census/M*.json, complete for sizes 1..S).
# For a pair (N, s), M = N * s, and every finite set P of divisors of N (hP), the Lean statement says L(P) = R(P) where
#   L(P) = { t > 0 : some multiset of size t on Z_M has, for every d | M, d != 1:  Phi_d | mask  <=>  d in P }
#   R(P) = { t > 0 : some multiset of size t on Z_N has, for every d | N, d != 1:  Phi_d | mask  <=>  d in P }.
# Whether 1 is in P makes no difference (d = 1 is skipped), so P runs over the subsets of the divisors > 1 of N.
# Both are computed for t <= S = min of the two census bounds, and compared for every P (a P that occurs in neither census has
# both sets empty up to S).  The census holds only the multisets containing 0; every multiset has such a translate, with the same
# size and the same divisor set.
# Also checked for every divisor set D seen on Z_M at size t: the set D restricted to the divisors of N is seen on Z_N at size t
# (what reduction modulo N would give).
# A pair is an instance of
#   two: s = 2 and the odd part of N has at most two prime factors            (sizes_eq_two)
#   odd: s odd                                                                (sizes_eq_odd; s = 1 says nothing and is left out)
#   mul: N = p^n q for primes p != q, n >= 0                                  (sizes_eq_mul, every s >= 2 tried)
# Pairs with s even, s > 2 that are not of the form `mul` are listed as "none" (no Lean statement covers them): a control.
import sys, os, json, math
from core import divisors

HERE = os.path.dirname(os.path.abspath(__file__))


def load(M):
    p = os.path.join(HERE, 'census', f'M{M}.json')
    return json.load(open(p)) if os.path.exists(p) else None


def primes_of(n):
    return [p for p in range(2, n + 1) if n % p == 0 and all(p % k for k in range(2, int(p ** 0.5) + 1))]


def is_pnq(N):
    """N = p^n * q with primes p != q, n >= 0 ?"""
    pr = primes_of(N)
    if len(pr) == 1:
        return N == pr[0]                    # n = 0: N = q
    if len(pr) == 2:
        a, b = pr
        ea = 0
        while N % a ** (ea + 1) == 0:
            ea += 1
        eb = 0
        while N % b ** (eb + 1) == 0:
            eb += 1
        return ea == 1 or eb == 1
    return False


def kinds(N, s):
    k = []
    odd = N
    while odd % 2 == 0:
        odd //= 2
    if s == 2 and len(primes_of(odd)) <= 2:
        k.append('two')
    if s % 2 == 1:
        k.append('odd')
    if is_pnq(N):
        k.append('mul')
    return k


def compare(N, s, cN, cM):
    S = min(cN['S'], cM['S'])
    divN = set(divisors(N))
    R = {}
    for pat in cN['patterns']:
        P = frozenset(pat['divs']) - {1}
        sz = {t for t in pat['sizes'] if t <= S}
        if sz:
            R[P] = sz
    L = {}
    red_bad = 0
    for pat in cM['patterns']:
        D = frozenset(pat['divs']) - {1}
        sz = {t for t in pat['sizes'] if t <= S}
        if not sz:
            continue
        if D <= divN:
            L[D] = sz
        if not sz <= R.get(frozenset(D & divN), set()):
            red_bad += 1
    keys = set(L) | set(R)
    mism = [P for P in keys if L.get(P, set()) != R.get(P, set())]
    nN = math.comb(N + S - 1, S - 1)
    nM = math.comb(N * s + S - 1, S - 1)
    return S, len(keys), 1 << (len(divN) - 1), mism, red_bad, nN, nM, L, R


if __name__ == '__main__':
    have = sorted(int(f[1:-5]) for f in os.listdir(os.path.join(HERE, 'census')) if f.startswith('M'))
    cs = {M: load(M) for M in have}
    tot = {'two': [0, 0, 0, 0], 'odd': [0, 0, 0, 0], 'mul': [0, 0, 0, 0], 'none': [0, 0, 0, 0]}
    allmis = 0
    allred = 0
    seen_groups = set()
    for N in have:
        for M in have:
            if M % N or M == N:
                continue
            s = M // N
            k = kinds(N, s) or ['none']
            S, nP, nAll, mism, red_bad, nN, nM, L, R = compare(N, s, cs[N], cs[M])
            allmis += len(mism)
            allred += red_bad
            for kk in k:
                tot[kk][0] += 1
                tot[kk][1] += nP
                tot[kk][2] += len(mism)
                tot[kk][3] += nM
            print(f"N={N:3d} s={s:3d} M={M:3d} {'+'.join(k):11s} S={S:2d} multisets: {nN} on Z_N, {nM} on Z_M; "
                  f"sets P with a nonempty side: {nP:4d} of {nAll:5d}; P where the two sets differ: {len(mism)}; "
                  f"reduction inconsistencies: {red_bad}", flush=True)
            for P in mism[:5]:
                print(f"      DIFFER  P={sorted(P)}  on Z_M: {sorted(L.get(P, []))}  on Z_N: {sorted(R.get(P, []))}")
    print()
    for kk in ['two', 'odd', 'mul', 'none']:
        a = tot[kk]
        print(f"{kk:5s}: pairs (N, s) = {a[0]:4d}; sets P compared (nonempty on a side) = {a[1]:6d}; differing = {a[2]}; "
              f"multisets on the larger groups, summed over pairs = {a[3]}")
    print(f"all pairs: differing sets {allmis}; reduction inconsistencies {allred}")
