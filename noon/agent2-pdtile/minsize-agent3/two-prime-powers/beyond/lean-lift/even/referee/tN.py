# Lemma N, Remarks 2 and 3, Corollary N: tested from the statements, for every odd e | n' and every prime of Z[eta_e]
# above 2 (the factors of Phi_e modulo 2), all 2^m signings, bad levels by exact remainders modulo Phi_{2^j e}.
#
# c_p = (beta_0 / 2) mod p is computed WITHOUT lifting the factorisation modulo 4: with u = product of the OTHER
# factors (taken with coefficients 0/1 in Z[Y]), u*beta_0 lies in every prime above 2, hence in 2 Z[eta];
# then c_p = ((u beta_0)/2 mod p) / (u mod p).
#
# usage: tN.py exh n m      every multiset with 0 of m elements on Z_n
#        tN.py rand seed count      random and structured multisets on a list of moduli
import sys, random, itertools
from math import comb
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from rlib import *

INF = 10 ** 9
stats = dict(multisets=0, pairs_e=0, pairs_e_with_bad=0, triples=0, special=0, free_levels=0, split_bad=0,
             diff_a_bad=0, two_values=0, one_value=0, attained=0, remark2=0, special_with_mixed=0)
seen_e = {}

def polymulmod_Z(a, b, P):
    """a*b mod P over Z (lists low first, P monic)"""
    r = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                r[i + j] += x * y
    dp = len(P) - 1
    for i in range(len(r) - 1, dp - 1, -1):
        c = r[i]
        if c:
            for j in range(dp + 1):
                r[i - dp + j] -= c * P[j]
    return r[:dp] + [0] * max(0, dp - len(r))

def check(B, n, bl=None):
    k, npr = split2(n)
    K = 1 << k
    m = len(B)
    u = [x % K for x in B]
    w = [x % npr for x in B]
    if bl is None:
        bl = bad_levels(B, n)
    stats['multisets'] += 1
    for e in divisors(npr):
        stats['pairs_e'] += 1
        badj = [bl[(1 << j) * e] for j in range(k + 1)]
        anybad = np.zeros(1 << m, dtype=bool)
        for bj in badj:
            anybad |= bj
        pw = powers_mod2(e)
        vec = [pw[x % e] for x in w]                  # eta^{w_x} mod 2, as an element of F_2[Y]/(Phi_e)
        De = f2_rank(vec)
        fs = factors_mod2(e)
        # the numbers a_p for every prime, and Remark 2
        a = []
        betas = []
        for f in fs:
            beta = []
            for i in range(K):
                s = 0
                for ux, vx in zip(u, vec):
                    if comb(ux, i) & 1:
                        s ^= vx
                beta.append(f2_mod(s, f))
            ap = next((i for i in range(K) if beta[i]), INF)
            a.append(ap)
            betas.append(beta)
            for d in range(k + 1):                    # Remark 2: a >= 2^d iff every class mod 2^d has its sum in p
                cls = {}
                for ux, vx in zip(u, vec):
                    cls[ux % (1 << d)] = cls.get(ux % (1 << d), 0) ^ vx
                allin = all(f2_mod(s, f) == 0 for s in cls.values())
                assert (ap >= (1 << d)) == allin, ("Remark 2", n, B, e, f, d)
                stats['remark2'] += 1
        amin = min(a)
        # (i): the levels that the lemma calls free
        for j in range(k + 1):
            need = 1 if j == 0 else (1 << (j - 1))
            if amin < need:
                assert not badj[j].any(), ("Lemma N (i)", n, B, e, j, a)
                stats['free_levels'] += 1
        if amin == 0:
            assert not anybad.any()
        if not anybad.any():
            continue
        stats['pairs_e_with_bad'] += 1
        seen_e[e] = seen_e.get(e, 0) + 1
        if len(fs) > 1:
            stats['split_bad'] += 1
        if len(set(a)) > 1:
            stats['diff_a_bad'] += 1
        # c_p, c'_p
        Pe = list(cyclo(e))
        if e == 1:
            beta0 = [m]
        else:
            Te = table(e, e)
            beta0 = [int(v) for v in sum(Te[x % e] for x in w)]
        cs, cps = [], []
        for t, f in enumerate(fs):
            up = [1]
            for g in fs:
                if g != f:
                    gl = [(g >> i) & 1 for i in range(g.bit_length())]
                    up = polymulmod_Z(up, gl, Pe) if e > 1 else [1]
            if e == 1:
                prod = [m]
                umodf = 1
            else:
                prod = polymulmod_Z(up, beta0, Pe)
                umodf = f2_mod(sum(1 << i for i, c in enumerate(up) if c % 2), f)
            assert all(c % 2 == 0 for c in prod), ("u*beta_0 not in 2Z[eta]", n, B, e)
            half = sum(1 << i for i, c in enumerate(prod) if (c // 2) % 2)
            if e == 1:
                c = half & 1                         # F_2: Y = 1, f = Y + 1
            else:
                c = f2_mulmod(f2_mod(half, f), f2_inv(umodf, f), f)
            cs.append(c)
            cps.append(c ^ betas[t][a[t]] if a[t] < INF else None)
        # (ii) for every bad signing, level and prime
        lam_values = {}          # level -> set of values of lambda_e (mod 2)
        for j in range(k + 1):
            idxs = np.nonzero(badj[j])[0]
            for s in idxs:
                s = int(s)
                lam = 0
                for i in range(m):
                    if s >> i & 1:
                        lam ^= vec[i]
                lam_values.setdefault(j, set()).add(lam)
                for t, f in enumerate(fs):
                    lp = f2_mod(lam, f) if e > 1 else (lam & 1)
                    if j >= 1 and a[t] == (1 << (j - 1)):
                        pred = cps[t]
                        stats['special'] += 1
                    else:
                        pred = cs[t]
                    assert lp == pred, ("Lemma N (ii)", n, B, e, j, f, a, lp, pred)
                    stats['triples'] += 1
        # Corollary N / Remark 3
        allv = set().union(*lam_values.values())
        assert len(allv) <= 2, ("Corollary N: more than two values", n, B, e)
        for j, vs in lam_values.items():
            assert len(vs) == 1, ("more than one value at one level", n, B, e, j)
        ispow2 = amin < INF and (amin & (amin - 1)) == 0
        if len(allv) == 2:
            stats['two_values'] += 1
            assert ispow2
            jstar = amin.bit_length()                 # 1 + log2(amin)
            # the value at j* differs from the value at every other level, which all agree
            others = set().union(*[vs for j, vs in lam_values.items() if j != jstar])
            assert len(others) == 1 and jstar in lam_values and lam_values[jstar] != others, ("Remark 3", n, B, e)
            if len(set(a)) > 1:
                stats['special_with_mixed'] += 1
        else:
            stats['one_value'] += 1
        nb = int(anybad.sum())
        bound = 2 ** (m + 1 - De) if ispow2 else 2 ** (m - De)
        assert nb <= bound, ("Corollary N: share", n, B, e, nb, De)
        if nb == 2 ** (m + 1 - De):
            stats['attained'] += 1

def report(head):
    print(head)
    print("  multisets %(multisets)d; pairs (multiset, e) %(pairs_e)d, with a bad signing at some 2^j e: %(pairs_e_with_bad)d"
          " (e with several primes above 2: %(split_bad)d; with different a_p: %(diff_a_bad)d)" % stats)
    print("  Lemma N (i): %(free_levels)d free levels, no bad signing at any;  (ii): %(triples)d (bad signing, level, prime)"
          " all with the predicted value, %(special)d of them c' at the special level" % stats)
    print("  Remark 2 checked %(remark2)d times.  Corollary N: two values %(two_values)d times (the special level j* = 1+log2 a_min"
          " each time; %(special_with_mixed)d of them with different a_p), one value %(one_value)d times;"
          " share <= 2^(1-D_e) always (and <= 2^(-D_e) when a_min is not a power of 2), 2^(1-D_e) attained %(attained)d times" % stats)
    print("  e with bad signings:", dict(sorted(seen_e.items())))

def gen(n, rnd):
    k, npr = split2(n)
    K = 1 << k
    def el(u, w):       # CRT: the element of Z_n with residues u mod 2^k and w mod n'
        for x in range(u % K, n, K):
            if x % npr == w % npr:
                return x
    t = rnd.random()
    es = [e for e in divisors(npr) if e > 1]
    if t < 0.12:
        return [rnd.randrange(n) for _ in range(rnd.randint(3, 10))]
    if t < 0.30:        # twins: every class modulo n' holds an even number of elements
        B = []
        for _ in range(rnd.randint(2, 5)):
            wv = rnd.randrange(npr)
            for _ in range(2):
                B.append(el(rnd.randrange(K), wv))
        return B[:10]
    if t < 0.42:        # closed under x -> x + n/2
        h = [rnd.randrange(n) for _ in range(rnd.randint(2, 5))]
        return h + [(x + n // 2) % n for x in h]
    if t < 0.56:        # union of cosets of a subgroup of order g, cut to 11
        gs = [g for g in divisors(n) if 1 < g <= 9]
        g = rnd.choice(gs)
        B = []
        while len(B) + g <= 11 and (not B or rnd.random() < 0.7):
            r = rnd.randrange(n)
            B += [(r + (n // g) * i) % n for i in range(g)]
        return B
    if t < 0.86:        # blocks (support of a product of factors of Phi_e mod 2, shifted) x (a set U of 2-residues)
        e = rnd.choice(es)
        fs = factors_mod2(e)
        B = []
        for _ in range(rnd.randint(1, 3)):
            g = 1
            for f in rnd.sample(fs, rnd.randint(1, max(1, len(fs) - 1))):
                g = f2_mul(g, f)
            g = f2_mod(g, cyclo_mod2(e)) if e > 1 else g
            if rnd.random() < 0.5:
                g = min(fs, key=lambda f: bin(f).count('1')) if rnd.random() < 0.5 else rnd.choice(fs)
            supp = [i for i in range(g.bit_length()) if g >> i & 1]
            sh = rnd.randrange(npr)
            mult = npr // e
            u0 = rnd.randrange(K)
            step = rnd.choice([1 << i for i in range(k)]) if k else 0
            U = [u0, (u0 + step) % K] if rnd.random() < 0.8 else [(u0 + i * (K // 4 if K >= 4 else 1)) % K for i in range(min(4, K))]
            if len(supp) * len(U) + len(B) > 12:
                continue
            # the residue modulo n' is chosen with w = sh + (index in supp) modulo e, the rest random but equal within the block
            lift = rnd.randrange(mult)
            for uu in U:
                for i in supp:
                    wv = None
                    for cand in range(npr):
                        if cand % e == (sh + i) % e and (cand // 1) % mult == lift % mult:
                            wv = cand
                            break
                    if wv is None:
                        wv = (sh + i) % e
                    B.append(el(uu, wv))
        if rnd.random() < 0.3 and len(B) <= 10:
            x = rnd.randrange(n)
            B += [x, (x + rnd.choice([n // 2, K * rnd.randrange(npr), npr * rnd.randrange(K)])) % n]
        return B if B else [0, 0]
    # one element in every class modulo a prime p | n', the 2-residues from a small set, then twins on top
    p = rnd.choice(list(factorint(npr).keys()))
    if p > 9:
        return [rnd.randrange(n) for _ in range(rnd.randint(4, 9))]
    us = [rnd.randrange(K) for _ in range(2)]
    B = [el(rnd.choice(us), (rnd.randrange(npr // p) * p + r) % npr) for r in range(p)]
    while len(B) < 9 and rnd.random() < 0.6:
        x = rnd.choice(B)
        B.append((x + rnd.choice([n // 2, npr, 2 * npr])) % n)
    return B

if sys.argv[1] == 'exh':
    n, m = int(sys.argv[2]), int(sys.argv[3])
    for B in multisets_with_zero(n, m):
        check(list(B), n)
    report("EXHAUSTIVE n = %d, every multiset with 0 of %d elements, all %d signings" % (n, m, 2 ** m))
else:
    seed, count = int(sys.argv[2]), int(sys.argv[3])
    rnd = random.Random(seed)
    mods = [int(x) for x in sys.argv[4:]] or [14, 28, 56, 30, 60, 120, 42, 84, 62, 124, 146, 292, 70, 90, 126, 102, 34, 46, 170, 210]
    per = {}
    for _ in range(count):
        n = rnd.choice(mods)
        B = gen(n, rnd)
        if len(B) > 12:
            B = B[:12]
        check(B, n)
        per[n] = per.get(n, 0) + 1
    report("RANDOM AND STRUCTURED seed %d: %s" % (seed, dict(sorted(per.items()))))
print("OK")
