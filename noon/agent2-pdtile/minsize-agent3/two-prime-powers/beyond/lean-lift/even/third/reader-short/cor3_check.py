#!/usr/bin/env python3
"""A reader's exact spot check of Corollary 3 of theorem-twice.md and of the steps of its proof.

Written from the statements (theorem-twice.md sections 1 and 4; even-result-2.md section 1), not from any program
of the folder.  Exact integer arithmetic: the remainder of the signed mask S_eps(X) = sum eps_b X^b modulo Phi_d
is the signed sum of the remainders of X^b modulo Phi_d (integer vectors).

  bad at d    : the remainder modulo Phi_d is 0                          (d | n)
  3-bad at d  : every coefficient of the remainder is divisible by 3     (d | n_3, n = 3^a n_3)
  good        : bad at no d | n ;   3-good : 3-bad at no d | n_3

For every multiset containing 0 of m elements of Z_n and all 2^m signings:
  (i)    m >= 3: some signing is good.  m = 2, B = {0, b}: some signing is good iff 2^k | b.  m = 1: good.
  (ii)   m >= 3: share of 3-good signings >= 1/2 (m = 3), 1/4 (m = 4), > p_(m-1) - 0.2372 (m >= 5)
  (iii)  Lemma M: every 3-good signing is good
  (iv)   inequality (2): for e'' | n'':  #(3-bad at 2^j e'' for some j <= k) <= 2 #(3-bad at e'')
  (v)    Lemma S3 for p = 2, both directions, with V = Z[x]/3, x of order e'', value x^b, position b mod 2^k:
         3-bad at 2^j e''  iff  level j is bad (class sums computed apart, modulo Phi_e'' and 3);
         and Theorem T': #(level j bad) = #F_(j-1),  #(some level bad) <= 2 #(level 0 bad) - #F_k
  (vi)   Lemma L3 (a) for every prime q != 3 (2 included): level v_q(d) of q not live => 3-bad at d implies 3-bad at d/q
         Lemma L3 (c) with c = 2^j: 3-bad at 2^j e'' => 3-bad at 2^j or at 2^j e' for a live e' > 1
         the shares 3-bad at the live e' > 1 add up to less than 0.118569; each is at most 2^(-mu(e'*))
  (vii)  #(not 3-good) <= 2 (#(3-bad at 1) + sum over live e' > 1 of #(3-bad at e')),  #(3-bad at 1) = p_m 2^m
False variants that must fail somewhere (counted):
  (Y1) (iv) with the factor 1 in place of 2
  (Y2) (ii) with 5/8 for m = 3, 3/8 for m = 4, p_(m-1) for m >= 5
  (Y3) m = 2: a good signing for every pair
  (Y4) (vi) L3 (a) without "not live"

usage: cor3_check.py self
       cor3_check.py exh <n> <m_from> <m_to>
       cor3_check.py live <n> <m> <number> <seed>     random multisets with a full group at every level of every
                                                      prime >= 5 dividing n (as far as m allows), and a random rest
"""
import os
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
import sys
import itertools
import random
import cmath
from fractions import Fraction
from math import comb
import numpy as np

W_NO3 = Fraction(118569, 1000000)
C2372 = Fraction(2372, 10000)


def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def prime_factors(n):
    out = {}
    p = 2
    while p * p <= n:
        while n % p == 0:
            out[p] = out.get(p, 0) + 1
            n //= p
        p += 1
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


def poly_div_exact(a, b):
    """a / b for b monic; asserts that the division is exact."""
    a = a[:]
    db = len(b) - 1
    q = [0] * (len(a) - db)
    for i in range(len(a) - db - 1, -1, -1):
        c = a[i + db]
        q[i] = c
        if c:
            for j, bj in enumerate(b):
                a[i + j] -= c * bj
    assert not any(a), "division not exact"
    return q


def poly_rem(a, b):
    """remainder of a modulo the monic b, by long division (used only in the self-test)."""
    a = a[:]
    db = len(b) - 1
    for i in range(len(a) - 1, db - 1, -1):
        c = a[i]
        if c:
            for j, bj in enumerate(b):
                a[i - db + j] -= c * bj
    return a[:db]


def cyclotomics(n):
    Phi = {}
    for d in divisors(n):
        p = [-1] + [0] * (d - 1) + [1]
        for e in divisors(d):
            if e < d:
                p = poly_div_exact(p, Phi[e])
        Phi[d] = p
    return Phi


def power_table(n, phi):
    """rows x = 0..n-1: the coefficients of X^x modulo the monic phi."""
    D = len(phi) - 1
    cur = [1] + [0] * (D - 1)
    rows = []
    for _ in range(n):
        rows.append(cur[:])
        top = cur[-1]
        cur = [0] + cur[:-1]
        if top:
            for j in range(D):
                cur[j] -= top * phi[j]
    assert cur == [1] + [0] * (D - 1), "X^n is not 1 modulo Phi_d"
    return rows


def p_r(r):
    p = Fraction(1)
    for _ in range(r):
        p = (1 - p) / 2
    return p


def bound(m):
    if m == 3:
        return Fraction(1, 2), False
    if m == 4:
        return Fraction(1, 4), False
    return p_r(m - 1) - C2372, True          # strict


def false_bound(m):
    if m == 3:
        return Fraction(5, 8)
    if m == 4:
        return Fraction(3, 8)
    return p_r(m - 1)


class Setting:
    def __init__(self, n):
        self.n = n
        f = prime_factors(n)
        self.k = f.get(2, 0)
        self.a = f.get(3, 0)
        self.n3 = n // 3 ** self.a
        self.npp = self.n3 // 2 ** self.k
        self.divs = divisors(n)
        self.Phi = cyclotomics(n)
        self.off = {}
        T = np.zeros((n, n), dtype=np.int16)
        o = 0
        for d in self.divs:
            tab = power_table(n, self.Phi[d])
            D = len(self.Phi[d]) - 1
            T[:, o:o + D] = np.array(tab, dtype=np.int16).reshape(n, D)
            self.off[d] = (o, o + D)
            o += D
        assert o == n
        self.T = T
        self.qs = sorted(q for q in prime_factors(self.n3))          # the primes other than 3 (2 included)
        self.vq = prime_factors(self.n3)
        self.epp = divisors(self.npp)


def signed_sums(V):
    """V: (c, m, w) integers.  Returns (c, 2^m, w): row s is sum_j eps_j V[:, j], eps_j = -1 iff bit j of s is set."""
    m = V.shape[1]
    res = np.stack([V[:, 0, :], -V[:, 0, :]], axis=1)
    for j in range(1, m):
        vj = V[:, j, None, :]
        res = np.concatenate([res + vj, res - vj], axis=1)
    return res


class Tally:
    def __init__(self):
        self.c = {}
        self.first = {}

    def add(self, name, k, what=None):
        k = int(k)
        self.c[name] = self.c.get(name, 0) + k
        if k and what is not None and name not in self.first:
            self.first[name] = what

    def get(self, name):
        return self.c.get(name, 0)


TRUE = ["i", "ii", "iii", "iv", "v-S3", "v-E", "v-Q", "vi-a", "vi-c", "vi-W", "vi-mu", "vii", "vii-p"]
FALSE = ["Y1", "Y2", "Y3", "Y4"]


def check_chunk(st, idx, m, tal, stats):
    """idx: (c, m) int array of elements of Z_n."""
    n, k = st.n, st.k
    c = idx.shape[0]
    nsig = 1 << m
    V = st.T[idx]                                    # (c, m, n)
    assert int(np.abs(st.T).max()) * m < 30000
    res = signed_sums(V)                             # (c, 2^m, n)
    bad = {}
    bad3 = {}
    for d in st.divs:
        o0, o1 = st.off[d]
        blk = res[:, :, o0:o1]
        bad[d] = ~blk.any(axis=2)
        if st.n3 % d == 0:
            bad3[d] = ~(blk % 3).any(axis=2)
    del res
    anybad = np.zeros((c, nsig), dtype=bool)
    for d in st.divs:
        anybad |= bad[d]
    good = ~anybad
    any3 = np.zeros((c, nsig), dtype=bool)
    for d in bad3:
        any3 |= bad3[d]
    good3 = ~any3
    ngood = good.sum(axis=1)
    ngood3 = good3.sum(axis=1)

    def ex(rowmask):
        r = int(np.argmax(rowmask))
        return "B=%s" % (list(map(int, idx[r])),)

    # (i), (Y3)
    if m >= 3 or m == 1:
        v = ngood == 0
        tal.add("i", v.sum(), ex(v) if v.any() else None)
    else:
        exceptional = (idx[:, 1] - idx[:, 0]) % (1 << k) != 0
        v = (ngood > 0) == exceptional
        tal.add("i", v.sum(), ex(v) if v.any() else None)
        w = ngood == 0
        tal.add("Y3", w.sum(), ex(w) if w.any() else None)
    # (ii), (Y2)
    if m >= 3:
        b, strict = bound(m)
        lim = b * nsig
        v = (ngood3 <= float(lim)) if strict else (ngood3 < float(lim))
        # exact recheck of the rows flagged or near
        v = np.array([(Fraction(int(x)) <= lim) if strict else (Fraction(int(x)) < lim) for x in ngood3]) \
            if v.any() else v
        tal.add("ii", v.sum(), ex(v) if v.any() else None)
        fb = false_bound(m) * nsig
        w = ngood3 < float(fb) - 1e-9
        tal.add("Y2", w.sum(), ex(w) if w.any() else None)
    r = int(np.argmin(ngood3))
    if stats.get("min3") is None or int(ngood3[r]) < stats["min3"][0]:
        stats["min3"] = (int(ngood3[r]), list(map(int, idx[r])))
    r = int(np.argmin(ngood))
    if stats.get("min") is None or int(ngood[r]) < stats["min"][0]:
        stats["min"] = (int(ngood[r]), list(map(int, idx[r])))
    # (iii)
    v = (good3 & ~good).any(axis=1)
    tal.add("iii", v.sum(), ex(v) if v.any() else None)

    # live levels
    live = {}
    for q in st.qs:
        for i in range(1, st.vq[q] + 1):
            qi = q ** i
            occ = (idx[:, :, None] % qi == np.arange(qi)[None, None, :]).any(axis=1)     # (c, q^i)
            # subclass t = r + s q^(i-1) of the class r modulo q^(i-1)
            full = occ.reshape(c, q, qi // q).all(axis=1)                                # (c, q^(i-1))
            live[(q, i)] = full.any(axis=1)
    live_e = {}
    mu_star = {}
    for e in st.epp:
        if e == 1:
            continue
        fe = prime_factors(e)
        lv = np.ones(c, dtype=bool)
        mu = np.zeros(c, dtype=np.int64)
        for q, i in fe.items():
            lv &= live[(q, i)]
            lq = np.zeros(c, dtype=np.int64)
            for i2 in range(1, i + 1):
                lq += live[(q, i2)]
            mu = np.maximum(mu, lq * (q - 1))
        live_e[e] = lv
        mu_star[e] = mu

    # (iv), (Y1)
    for e in st.epp:
        U = np.zeros((c, nsig), dtype=bool)
        for j in range(k + 1):
            U |= bad3[(1 << j) * e]
        nu = U.sum(axis=1)
        nz = bad3[e].sum(axis=1)
        v = nu > 2 * nz
        tal.add("iv", v.sum(), (ex(v) + " e''=%d" % e) if v.any() else None)
        w = nu > nz
        tal.add("Y1", w.sum(), (ex(w) + " e''=%d" % e) if w.any() else None)
        tal.add("tests-iv", c)
        eq = (nu == 2 * nz) & (nz > 0)
        tal.add("iv-equal", eq.sum())

    # (v)
    for e in st.epp:
        o0, o1 = st.off[e]
        vals = (st.T[:, o0:o1] % 3).astype(np.int16)          # x^b in Z[x]/3, x of order e
        Ve = vals[idx]                                        # (c, m, phi(e))
        S = {}
        for d in range(k + 1):
            for r in range(1 << d):
                mask = (idx % (1 << d)) == r                  # position b mod 2^k lies in the class r mod 2^d
                S[(d, r)] = signed_sums(Ve * mask[:, :, None]) % 3
        lev = [~S[(0, 0)].any(axis=2)]
        for j in range(1, k + 1):
            ok = np.ones((c, nsig), dtype=bool)
            for r in range(1 << (j - 1)):
                ok &= ~((S[(j, r)] - S[(j, r + (1 << (j - 1)))]) % 3).any(axis=2)
            lev.append(ok)
        F = []
        for d in range(k + 1):
            ok = np.ones((c, nsig), dtype=bool)
            for r in range(1 << d):
                ok &= ~S[(d, r)].any(axis=2)
            F.append(ok)
        U = np.zeros((c, nsig), dtype=bool)
        for j in range(k + 1):
            v = (lev[j] != bad3[(1 << j) * e]).any(axis=1)
            tal.add("v-S3", v.sum(), (ex(v) + " e''=%d j=%d" % (e, j)) if v.any() else None)
            U |= lev[j]
            if j >= 1:
                v = lev[j].sum(axis=1) != F[j - 1].sum(axis=1)
                tal.add("v-E", v.sum(), (ex(v) + " e''=%d j=%d" % (e, j)) if v.any() else None)
        v = U.sum(axis=1) > 2 * lev[0].sum(axis=1) - F[k].sum(axis=1)
        tal.add("v-Q", v.sum(), (ex(v) + " e''=%d" % e) if v.any() else None)
        del S

    # (vi) L3 (a), (Y4)
    for d in bad3:
        for q, i in prime_factors(d).items():
            viol = bad3[d] & ~bad3[d // q]
            v = (viol & ~live[(q, i)][:, None]).any(axis=1)
            tal.add("vi-a", v.sum(), (ex(v) + " d=%d q=%d" % (d, q)) if v.any() else None)
            w = viol.any(axis=1)
            tal.add("Y4", w.sum(), (ex(w) + " d=%d q=%d" % (d, q)) if w.any() else None)
    # (vi) L3 (c) with c = 2^j
    for j in range(k + 1):
        cj = 1 << j
        cover = bad3[cj].copy()
        for e in live_e:
            cover |= bad3[cj * e] & live_e[e][:, None]
        for e in st.epp:
            v = (bad3[cj * e] & ~cover).any(axis=1)
            tal.add("vi-c", v.sum(), (ex(v) + " c=%d e''=%d" % (cj, e)) if v.any() else None)
    # (vi) the sum over the live e' > 1, and each share against 2^(-mu(e'*))
    nlive = np.zeros(c, dtype=np.int64)
    anylive = np.zeros(c, dtype=bool)
    for e in live_e:
        cnt = bad3[e].sum(axis=1) * live_e[e]
        nlive += cnt
        anylive |= live_e[e]
        # cnt / 2^m <= 2^(-mu)   <=>   cnt * 2^mu <= 2^m
        v = live_e[e] & (cnt.astype(object) * (2 ** mu_star[e].astype(object)) > nsig)
        v = v.astype(bool)
        tal.add("vi-mu", v.sum(), (ex(v) + " e'=%d" % e) if v.any() else None)
    v = nlive * W_NO3.denominator >= W_NO3.numerator * nsig
    tal.add("vi-W", v.sum(), ex(v) if v.any() else None)
    tal.add("with-live", anylive.sum())
    mx = int(nlive.max())
    if mx > stats.get("maxlive", (0, None))[0]:
        stats["maxlive"] = (mx, list(map(int, idx[int(np.argmax(nlive))])))
    # (vii)
    n1 = bad3[1].sum(axis=1)
    v = (nsig - ngood3) > 2 * (n1 + nlive)
    tal.add("vii", v.sum(), ex(v) if v.any() else None)
    pm = p_r(m) * nsig
    assert pm.denominator == 1
    v = n1 != int(pm)
    tal.add("vii-p", v.sum(), ex(v) if v.any() else None)
    tal.add("multisets", c)


def report(st, m, tal, stats, head):
    nsig = 1 << m
    print(head)
    print("  n = %d = 2^%d * 3^%d * %d ; m = %d ; multisets: %d ; with a live e' > 1: %d"
          % (st.n, st.k, st.a, st.npp, m, tal.get("multisets"), tal.get("with-live")))
    for name in TRUE:
        print("  true statement (%s): failures %d%s"
              % (name, tal.get(name), ("   FIRST: " + tal.first[name]) if name in tal.first else ""))
    for name in FALSE:
        print("  false variant (%s): failures %d%s"
              % (name, tal.get(name), ("   first: " + tal.first[name]) if name in tal.first else ""))
    print("  tests of (2) (multiset, e''): %d ; with equality and z > 0: %d" % (tal.get("tests-iv"), tal.get("iv-equal")))
    g3, B3 = stats["min3"]
    g, B = stats["min"]
    print("  least share of 3-good signings: %s at B=%s" % (Fraction(g3, nsig), B3))
    print("  least share of good signings:   %s at B=%s" % (Fraction(g, nsig), B))
    if m >= 3:
        b, strict = bound(m)
        print("  bound of Corollary 3 for m = %d: %s %s (%.6f)" % (m, ">" if strict else ">=", b, float(b)))
    if "maxlive" in stats:
        mx, Bl = stats["maxlive"]
        print("  largest sum of the shares 3-bad at the live e' > 1: %s (%.6f) at B=%s"
              % (Fraction(mx, nsig), mx / nsig, Bl))
    ok = all(tal.get(nm) == 0 for nm in TRUE)
    print("  RESULT: %s" % ("no true statement failed" if ok else "A TRUE STATEMENT FAILED"))
    sys.stdout.flush()


def run_exh(n, m_from, m_to):
    st = Setting(n)
    for m in range(m_from, m_to + 1):
        tal = Tally()
        stats = {}
        total = comb(n + m - 2, m - 1)
        chunk = max(200, min(20000, 12_000_000 // ((1 << m) * n)))
        it = itertools.combinations_with_replacement(range(n), m - 1)
        done = 0
        while True:
            part = list(itertools.islice(it, chunk))
            if not part:
                break
            idx = np.zeros((len(part), m), dtype=np.int64)
            if m > 1:
                idx[:, 1:] = np.array(part, dtype=np.int64).reshape(len(part), m - 1)
            check_chunk(st, idx, m, tal, stats)
            done += len(part)
        assert done == total
        report(st, m, tal, stats, "EXHAUSTIVE: every multiset containing 0 of %d elements of Z_%d, all signings" % (m, n))


def run_live(n, m, number, seed):
    st = Setting(n)
    rng = random.Random(seed)
    tal = Tally()
    stats = {}
    qs = [q for q in st.qs if q >= 5]
    rows = []
    for _ in range(number):
        B = [0]
        # choose which primes to make live at every level, as the size allows
        want = [q for q in qs if rng.random() < 0.85]
        rng.shuffle(want)
        for q in want:
            # make every level of q hold a full group: a caterpillar through a random spine
            spine = rng.randrange(q ** st.vq[q])
            for i in range(1, st.vq[q] + 1):
                r = spine % (q ** (i - 1))
                for s in range(q):
                    t = r + s * q ** (i - 1)          # a residue modulo q^i
                    if any(b % (q ** i) == t for b in B):
                        continue
                    if len(B) >= m:
                        break
                    # a random element with this residue modulo q^i; reuse the other residues of an old element
                    # half of the time, so that the 2-tree has few classes
                    while True:
                        x = rng.randrange(n)
                        if rng.random() < 0.5:
                            y = rng.choice(B)
                            x = y + (n // (q ** st.vq[q])) * rng.randrange(q ** st.vq[q])
                            x %= n
                        if x % (q ** i) == t:
                            break
                    B.append(x)
        while len(B) < m:
            B.append(rng.choice(B) if rng.random() < 0.3 else rng.randrange(n))
        rows.append(sorted(B[:m]))
    chunk = max(100, min(20000, 12_000_000 // ((1 << m) * n)))
    for o in range(0, number, chunk):
        idx = np.array(rows[o:o + chunk], dtype=np.int64)
        check_chunk(st, idx, m, tal, stats)
    report(st, m, tal, stats, "LIVE: %d random multisets (seed %d) of %d elements of Z_%d built to have live levels, "
                              "all signings" % (number, seed, m, n))


def run_self():
    """The instrument against other ways of computing the same things."""
    # cyclotomic polynomials known by heart
    Phi = cyclotomics(60)
    assert Phi[1] == [-1, 1] and Phi[2] == [1, 1] and Phi[3] == [1, 1, 1] and Phi[4] == [1, 0, 1]
    assert Phi[5] == [1, 1, 1, 1, 1] and Phi[6] == [1, -1, 1] and Phi[10] == [1, -1, 1, -1, 1]
    assert Phi[12] == [1, 0, -1, 0, 1] and Phi[15] == [1, -1, 0, 1, -1, 1, 0, -1, 1]
    assert Phi[20] == [1, 0, -1, 0, 1, 0, -1, 0, 1]
    assert len(Phi[60]) - 1 == 16 and Phi[30] == [1, 1, 0, -1, -1, -1, 0, 1, 1]
    rng = random.Random(5)
    for n in (12, 20, 60, 28, 40):
        st = Setting(n)
        for _ in range(300):
            m = rng.randint(1, 6)
            B = [rng.randrange(n) for _ in range(m)]
            idx = np.array([B], dtype=np.int64)
            res = signed_sums(st.T[idx])[0]                 # (2^m, n)
            for s in range(1 << m):
                eps = [(-1 if (s >> j) & 1 else 1) for j in range(m)]
                S = [0] * n
                for b, e in zip(B, eps):
                    S[b] += e
                for d in st.divs:
                    o0, o1 = st.off[d]
                    rem = poly_rem(S, st.Phi[d])            # long division of the mask itself
                    assert rem == [int(x) for x in res[s, o0:o1]], (n, B, s, d)
                    z = cmath.exp(2j * cmath.pi / d)        # numerical value at a root of unity of order d
                    val = sum(e * z ** b for b, e in zip(B, eps))
                    assert (abs(val) < 1e-9) == (not any(rem)), (n, B, s, d)
    # hand cases: {0,1,2} on Z_12: exactly half of the signings good; {0,0,0,1} on Z_2 and Z_12: a quarter
    for n, B, share in ((12, [0, 1, 2], Fraction(1, 2)), (2, [0, 0, 0, 1], Fraction(1, 4)),
                        (12, [0, 0, 0, 1], Fraction(1, 4)), (6, [0, 1, 2], Fraction(1, 2))):
        st = Setting(n)
        tal = Tally()
        stats = {}
        check_chunk(st, np.array([B], dtype=np.int64), len(B), tal, stats)
        assert Fraction(stats["min"][0], 1 << len(B)) == share, (n, B, stats)
    # five elements, one in each class modulo 5, on Z_5: bad at 5 iff all signs equal (2 of 32)
    st = Setting(5)
    res = signed_sums(st.T[np.array([[0, 1, 2, 3, 4]])])[0]
    o0, o1 = st.off[5]
    assert int((~res[:, o0:o1].any(axis=1)).sum()) == 2
    print("self-test of the instrument: passed")


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "self":
        run_self()
    elif mode == "exh":
        run_exh(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
    elif mode == "live":
        run_live(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]))
