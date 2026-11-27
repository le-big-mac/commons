"""The parts S0, S1, S2 (a), S2 (b), S2, "occupied classes", S3, S4, S5 as stated in Lean, tested on families e with EVERY
signing, in exact integer arithmetic.

For a family e (a list of natural numbers, not reduced modulo anything) and a modulus n used only to pick the levels:
for every divisor D > 1 of n and every prime p | D, with i = v_p(D), d = D / p^i (so p does not divide d):
  S0   every signing bad at D has equal class sums on the p classes of every group at level i of p.  The class sum
       sum_{e_k % p^i = r} sg_k eta^{e_k}, eta a primitive d-th root of unity, is computed in Z[X]/(Phi_d) (eta = the
       class of X): two elements of Z[eta] are equal iff their remainders modulo Phi_d are equal, whichever primitive
       root eta is.  The converse (flat on every group => bad at D) is recorded too; it is not a statement of the
       skeleton, only a check that the class sums computed here are the right objects.
  S1   if level i of p is not live: bad at D => bad at p^(i-1) d.
  S2a  for every pivot set J (IsPivot literally, all subsets J when m <= 9; the largest pivot set by the formula
       "occupied classes minus full groups" otherwise): #bad(D) * 2^|J| <= 2^m.
  S2b  if level i of p is live: some pivot set has at least (p-1) rank e p i elements.
  S2   if level i of p is live: #bad(D) * 2^((p-1) rank e p i) <= 2^m.
and for every prime p | n (and p = 2, 3, 5, 7) and every level j = 0..5:
  OCC  (p-1) rank e p j + 1 <= number of occupied classes modulo p^j;   S3  (p-1) rank e p j + 1 <= m.
S4: bad at 1 iff the signs add up to 0; the number is C(m, m/2) or 0.
S5: m >= 7, level i of 3 live, rank e 3 i = 1  =>  #bad(3^i) * 16 <= 3 * 2^m   (for every i with 3^i | n).
usage: t1_parts.py SEED COUNT MAXM [KIND]"""
import os
import random
import sys
from collections import Counter
from itertools import combinations
from math import comb
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import core

MODULI = [4, 8, 16, 32, 9, 27, 81, 25, 125, 49, 6, 12, 18, 24, 36, 54, 72, 108, 10, 20, 50, 100, 14, 28, 98, 15, 45, 75, 135,
          225, 21, 63, 147, 35, 175, 245, 30, 60, 90, 150, 42, 84, 126, 70, 140, 105, 315, 210, 33, 99, 55, 77, 66, 165,
          343, 64, 243, 11, 121, 22, 13, 39, 3, 5, 7, 2]


def gen_family(rng, n, maxm, kind=None):
    f = core.factor(n)
    m = rng.randint(1, maxm)
    k = rng.random() if kind is None else kind
    if k < 0.2:                                           # random residues
        e = [rng.randrange(n) for _ in range(m)]
    elif k < 0.45:                                        # unions of cosets of subgroups of prime order of Z_D, D | n
        e = []
        while len(e) < m:
            D = rng.choice([d for d in core.divisors(n) if d > 1])
            q = rng.choice(list(core.factor(D)))
            a = rng.randrange(n)
            e += [(a + t * (D // q)) % n for t in range(q)]
        if rng.random() < 0.5:
            e = e[:m]
    elif k < 0.65:                                        # clustered: few base points, digits of one prime varied
        base = [rng.randrange(n) for _ in range(rng.randint(1, 3))]
        q = rng.choice(list(f))
        e = [(rng.choice(base) + rng.randrange(q) * (n // q ** rng.randint(1, f[q]))) % n for _ in range(m)]
    elif k < 0.8:                                         # an interval or an arithmetic progression
        s = rng.choice([1, 1, 2, 3, 5, 7, 9]); a = rng.randrange(n)
        e = [(a + s * j) % n for j in range(m)]
    elif k < 0.9:                                         # a caterpillar for one prime (every level live, few classes)
        q = rng.choice(list(f)); L = rng.randint(1, f[q])
        e = [0] + [t * q ** (j - 1) for j in range(1, L + 1) for t in range(1, q)]
        u = rng.choice([x for x in range(1, n) if all(x % r for r in f)] or [1])
        a = rng.randrange(n)
        e = [(a + u * x) % n for x in e]
        while len(e) < m and rng.random() < 0.6:
            e.append(rng.choice(e) if rng.random() < 0.5 else rng.randrange(n))
    else:                                                 # repeated elements
        base = [rng.randrange(n) for _ in range(rng.randint(1, 4))]
        e = [rng.choice(base) for _ in range(m)]
    e = e[:16]
    # exponents are natural numbers, not residues: push some of them up by multiples of n
    if rng.random() < 0.5:
        e = [x + n * rng.randrange(3) for x in e]
    rng.shuffle(e)
    return e


def max_pivot_formula(e, p, i):
    q = p ** (i - 1); M = p ** i
    occ = {x % M for x in e}
    groups = Counter(r % q for r in occ)
    return len(occ) - sum(1 for c, k in groups.items() if k == p)


def max_pivot_literal(e, p, i):
    m = len(e)
    best = 0
    for size in range(m, -1, -1):
        for J in combinations(range(m), size):
            if core.is_pivot(e, p, i, J):
                return size
    return best


def check(n, e, st, viol):
    m = len(e)
    S = core.signs(m)
    ea = np.array(e, dtype=np.int64)
    f = core.factor(n)
    badv = {}
    for D in core.divisors(n):
        badv[D] = core.bad(e, D)
    # S4
    st['S4 families'] += 1
    zero = S.sum(axis=1) == 0
    if not np.array_equal(zero, badv[1]):
        viol.append(('S4 iff', n, e))
    if int(badv[1].sum()) != (comb(m, m // 2) if m % 2 == 0 else 0):
        viol.append(('S4 count', n, e))
    # OCC, S3 for the primes of n and for 2, 3, 5, 7
    for p in sorted(set(f) | {2, 3, 5, 7}):
        for j in range(0, 6):
            r = core.rank(e, p, j)
            N = len({x % p ** j for x in e})
            st['OCC'] += 1
            if (p - 1) * r + 1 > N:
                viol.append(('OCC', e, p, j))
            if (p - 1) * r + 1 == N:
                st['OCC equality'] += 1
            st['S3'] += 1
            if (p - 1) * r + 1 > m:
                viol.append(('S3', e, p, j))
            if (p - 1) * r + 1 == m:
                st['S3 equality'] += 1
    piv = {}
    for D in core.divisors(n):
        if D == 1:
            continue
        bD = badv[D]
        cnt = int(bD.sum())
        for p, i in core.factor(D).items():
            d = D // p ** i
            q = p ** (i - 1); M = p ** i
            key = 'p=2' if p == 2 else 'p odd'
            # --- S0 ---
            T = core.xtab(d)[ea % d]
            cls = ea % M
            occ = sorted(set(int(r) for r in cls))
            CS = {}
            for r in occ:
                idx = np.nonzero(cls == r)[0]
                CS[r] = S[:, idx] @ T[idx]
            zero_cs = np.zeros((S.shape[0], T.shape[1]), dtype=np.int64)
            flat = np.ones(S.shape[0], dtype=bool)
            for c in sorted(set(r % q for r in occ)):
                first = CS.get(c, zero_cs)
                for t in range(1, p):
                    flat &= np.all(CS.get(c + t * q, zero_cs) == first, axis=1)
            st['S0 instances ' + key] += 1
            if cnt:
                st['S0 instances with a bad signing ' + key] += 1
                st['S0 bad signings checked'] += cnt
                st['S0 with a bad signing, p = %d, i = %d' % (p, i)] += 1
                if d > 1:
                    st['S0 with a bad signing, d > 1'] += 1
                if len(core.factor(d)) >= 2:
                    st['S0 with a bad signing, d of two or more primes'] += 1
            if np.any(bD & ~flat):
                viol.append(('S0', e, D, p, i, d))
            if np.any(flat & ~bD):
                viol.append(('S0 converse', e, D, p, i, d))
            # --- S1 ---
            lv = core.live(e, p, i)
            if not lv:
                st['S1 instances ' + key] += 1
                lower = badv[D // p]
                if cnt:
                    st['S1 instances with a bad signing ' + key] += 1
                    st['S1 with a bad signing, i = %d' % i] += 1
                    if len(core.factor(d)) >= 2:
                        st['S1 with a bad signing, d of two or more primes'] += 1
                if np.any(bD & ~lower):
                    viol.append(('S1', e, D, p, i, d))
            # --- pivots ---
            if (p, i) not in piv:
                fm = max_pivot_formula(e, p, i)
                if m <= 9:
                    lit = max_pivot_literal(e, p, i)
                    st['pivot sets: literal maximum compared with the formula'] += 1
                    if lit != fm:
                        viol.append(('pivot formula', e, p, i, lit, fm))
                piv[(p, i)] = fm
            J = piv[(p, i)]
            st['S2a instances ' + key] += 1
            if cnt * 2 ** J > 2 ** m:
                viol.append(('S2a', e, D, p, i, d, cnt, J))
            if cnt and cnt * 2 ** J == 2 ** m:
                st['S2a equality ' + key] += 1
            if lv:
                rk = core.rank(e, p, i)
                st['S2b instances ' + key] += 1
                if J < (p - 1) * rk:
                    viol.append(('S2b', e, p, i, J, rk))
                if J == (p - 1) * rk:
                    st['S2b equality ' + key] += 1
                st['S2 instances ' + key] += 1
                if d > 1 and len(core.factor(d)) >= 2:
                    st['S2 instances with d of two or more primes'] += 1
                if cnt:
                    st['S2 instances with a bad signing ' + key] += 1
                if cnt * 2 ** ((p - 1) * rk) > 2 ** m:
                    viol.append(('S2', e, D, p, i, d, cnt, rk))
                if cnt * 2 ** ((p - 1) * rk) == 2 ** m:
                    st['S2 equality ' + key] += 1
                    st['S2 equality at level i=%d' % i] += 1
            else:                                          # level not live: outside S2 (b) and S2; recorded only
                rk = core.rank(e, p, i)
                st['S2, S2b without hlive (level not live): instances'] += 1
                if cnt * 2 ** ((p - 1) * rk) > 2 ** m:
                    st['S2 without hlive: inequality fails'] += 1
                if J < (p - 1) * rk:
                    st['S2b without hlive: no pivot set that large'] += 1
    # --- S5 ---
    for i in range(1, f.get(3, 0) + 1):
        if core.live(e, 3, i):
            cnt = int(badv[3 ** i].sum())
            rk = core.rank(e, 3, i)
            if m >= 7 and rk == 1:
                st['S5 instances'] += 1
                if cnt:
                    st['S5 instances with a bad signing'] += 1
                if cnt * 16 > 3 * 2 ** m:
                    viol.append(('S5', e, i, cnt))
                if cnt * 16 == 3 * 2 ** m:
                    st['S5 equality'] += 1
            elif rk == 1:                                  # m < 7: outside the statement; recorded only
                st['S5 without hm (m < 7): instances'] += 1
                if cnt * 16 > 3 * 2 ** m:
                    st['S5 without hm: inequality fails'] += 1
                    st['S5 without hm: inequality fails at m=%d' % m] += 1
            elif m >= 7:                                   # rank >= 2: outside the statement; recorded only
                st['S5 without hrank (rank >= 2): instances'] += 1
                if cnt * 16 > 3 * 2 ** m:
                    st['S5 without hrank: inequality fails'] += 1
        elif m >= 7 and core.rank(e, 3, i) == 1:           # level not live: outside the statement; recorded only
            cnt = int(badv[3 ** i].sum())
            st['S5 without hlive (level not live, rank 1): instances'] += 1
            if cnt * 16 > 3 * 2 ** m:
                st['S5 without hlive: inequality fails'] += 1


if __name__ == '__main__':
    seed, count, maxm = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    kind = float(sys.argv[4]) if len(sys.argv) > 4 else None
    rng = random.Random(seed)
    st = Counter(); viol = []
    sizes = Counter()
    for _ in range(count):
        n = rng.choice(MODULI)
        e = gen_family(rng, n, maxm, kind)
        sizes[len(e)] += 1
        check(n, e, st, viol)
    print('seed', seed, 'families', count, 'sizes', dict(sorted(sizes.items())))
    for k in sorted(st):
        print('   %-60s %d' % (k, st[k]))
    print('   VIOLATIONS', len(viol))
    for v in viol[:20]:
        print('      ', v)
