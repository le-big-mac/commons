# Proposition P (2): the level e = 1.  For every multiset with 0 of m elements (m even, m >= 4) on Z_{2^k}:
# the true P_1 (share of signings bad at some 2^j, by exact remainders), against the bound that the proof of (2)
# gives case by case, against 3/4.  Every sentence of the proof of (2) is asserted on the way.
# P_1 of a multiset on Z_n depends only on its residues modulo 2^k, and is invariant under translation.
# usage: tP1.py K m [m ...]
import sys, itertools
from math import comb
from fractions import Fraction as F
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from rlib import *

def c_(r):
    return F(comb(r, r // 2), 2 ** r)

def dist(r):
    """distribution of a sum of r signs"""
    return {r - 2 * t: F(comb(r, t), 2 ** r) for t in range(r + 1)}

def run(K, m):
    k = K.bit_length() - 1
    S = signmat(m)
    nminus = np.array([bin(i).count('1') for i in range(1 << m)])
    best = F(0); bestB = None; nb = 0
    best_set = F(0); best_setB = None
    cases = {'not a power of 2': 0, 'a=2^d, several classes': 0, 'a=2^d, one class': 0}
    attain = 0
    for B in multisets_with_zero(K, m):
        nb += 1
        bl = bad_levels(list(B), K)
        badj = [bl[1 << j] for j in range(k + 1)]
        anyb = np.zeros(1 << m, dtype=bool)
        for b in badj:
            anyb |= b
        P1 = F(int(anyb.sum()), 1 << m)
        beta = [sum(comb(u, i) for u in B) % 2 for i in range(K)]
        assert beta[0] == 0
        a = next((i for i in range(K) if beta[i]), None)
        cpar = (m // 2) % 2
        if a is None or (a & (a - 1)) != 0:
            cases['not a power of 2'] += 1
            assert (nminus[anyb] % 2 == cpar).all()
            bound = F(1, 2)
        else:
            d = a.bit_length() - 1
            cls = {}
            for u in B:
                cls.setdefault(u % (1 << d), []).append(u)
            assert all(len(v) % 2 == 0 for v in cls.values())
            assert d + 1 <= k
            ch = {}
            for u in B:
                ch[u % (1 << (d + 1))] = ch.get(u % (1 << (d + 1)), 0) + 1
            assert any(v % 2 for v in ch.values())
            for j in range(d + 2, k + 1):
                assert not badj[j].any()
            for j in range(0, k + 1):
                if j != d + 1:
                    assert (nminus[badj[j]] % 2 == cpar).all()
            qprod = F(1)
            for v in cls.values():
                q = c_(len(v))
                assert q <= F(1, 2)
                qprod *= q
            assert F(int(badj[d + 1].sum()), 1 << m) <= qprod       # the product bounds "bad at 2^(d+1)"
            if len(cls) >= 2:
                cases['a=2^d, several classes'] += 1
                bound = F(1, 2) + qprod
                assert bound <= F(3, 4)
            else:
                cases['a=2^d, one class'] += 1
                sizes = sorted(ch.values())
                assert len(sizes) == 2 and sizes[0] % 2 == 1 and sizes[1] % 2 == 1 and sizes[1] >= 3
                r, s = sizes
                dr, ds = dist(r), dist(s)
                bound = sum(dr[x] * (ds.get(x, 0) + ds.get(-x, 0)) for x in dr)
                assert bound <= 2 * c_(max(r, s)) <= F(3, 4)
        assert P1 <= bound <= F(3, 4), (K, B, P1, bound)
        if P1 == F(3, 4):
            attain += 1
        if P1 > best:
            best, bestB = P1, B
        if len(set(B)) == m and P1 > best_set:
            best_set, best_setB = P1, B
    print("Z_%d, m = %d: %d multisets with 0; cases %s; largest P_1 = %s at %s; among sets %s at %s; P_1 = 3/4 for %d multisets"
          % (K, m, nb, cases, best, bestB, best_set, best_setB, attain), flush=True)

K = int(sys.argv[1])
for m in sys.argv[2:]:
    run(K, int(m))
print("OK")
