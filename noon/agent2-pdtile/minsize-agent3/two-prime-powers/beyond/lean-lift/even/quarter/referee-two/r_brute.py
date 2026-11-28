#!/usr/bin/env python3
"""Referee's brute force: every signing, exact integer arithmetic, badness from the DEFINITION (the remainder of the
signed mask modulo the cyclotomic polynomial Phi_d, for every d | n), against the claims of result.md.

modes
  exh n m [cap]      every multiset of m elements of Z_n containing 0 (a random sample of `cap` of them if there are
                     more than cap): share of bad signings <= T2(m) and <= 3/8; share "bad at some p^i, i>=1, not at
                     1" <= U_p(m); reports the largest shares.
  lem n m count seed [l4]   `count` random and shaped multisets: Lemma 1, Lemma 2 (strong form), Lemma 5, the cell
                     values of section 2 (by the actual class sizes, and vf/vnf), Proposition 6, U_p, COMP, Theorem A;
                     with l4 also Lemma 4 (a), (b), (c) class by class.
  lemexh n m [l4]    the same tests on every multiset containing 0.
"""
import sys, random, itertools, time
from math import comb
from fractions import Fraction as F
import numpy as np
import r_tables as RT


def factor(n):
    f = {}; q = 2
    while q * q <= n:
        while n % q == 0:
            f[q] = f.get(q, 0) + 1; n //= q
        q += 1
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f


def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def rad(d):
    r = 1
    for q in factor(d):
        r *= q
    return r


_cyc = {}


def polydiv(num, den):
    num = num[:]; dd = len(den) - 1; q = [0] * (len(num) - dd)
    for i in range(len(num) - 1, dd - 1, -1):
        t = num[i]
        if t:
            q[i - dd] = t
            for j in range(dd + 1):
                num[i - dd + j] -= t * den[j]
    assert not any(num), "inexact division"
    return q


def cyclo(d):
    if d not in _cyc:
        num = [-1] + [0] * (d - 1) + [1]
        for e in divisors(d):
            if e < d:
                num = polydiv(num, cyclo(e))
        _cyc[d] = num
    return _cyc[d]


_V = {}


def V(d):
    """V[r] = coefficients of X^r mod Phi_d, r = 0..d-1"""
    if d not in _V:
        ph = cyclo(d); deg = len(ph) - 1
        out = np.zeros((d, deg), dtype=np.float64)
        v = [0] * deg; v[0] = 1
        for r in range(d):
            out[r] = v
            t = v[-1]
            v = [0] + v[:-1]
            if t:
                for i in range(deg):
                    v[i] -= t * ph[i]
        assert np.abs(out).max() < 2 ** 20
        _V[d] = out
    return _V[d]


_E = {}


def signs(m):
    if m not in _E:
        a = np.arange(2 ** m, dtype=np.int64)
        _E[m] = (1.0 - 2.0 * ((a[:, None] >> np.arange(m)[None, :]) & 1)).astype(np.float64)
    return _E[m]


_rng = np.random.default_rng(12345)


def zero_rows(E, M):
    f = M.shape[1]
    if f <= 64:
        return ~(E @ M).any(axis=1)
    J = _rng.choice(f, 48, replace=False)
    cand = ~(E @ M[:, J]).any(axis=1)
    idx = np.nonzero(cand)[0]
    if len(idx):
        cand[idx] = ~(E[idx] @ M).any(axis=1)
    return cand


_T2 = {}


def U_bound(p, m):
    if p in RT.U_TEXT and m in RT.U_TEXT[p]:
        return F(RT.U_TEXT[p][m])
    if p > m:
        return F(0)
    return RT.PP(p, m)


def T2(m):
    if m not in _T2:
        lvl0 = RT.c(m) if m % 2 == 0 else F(0)
        _T2[m] = lvl0 + sum((U_bound(p, m) for p in RT.primes_upto(m)), F(0)) + RT.COMP(m)[0]
    return _T2[m]


# ------------------------------------------------------------------ exhaustive, batched
def exh(n, m, cap):
    fac = factor(n); divs = divisors(n)
    E = signs(m).astype(np.float32); S = E.shape[0]
    total = comb(n + m - 2, m - 1)
    if total <= cap:
        gen = itertools.combinations_with_replacement(range(n), m - 1); sampled = False
    else:
        rnd = random.Random(n * 1000 + m)
        gen = (tuple(sorted(rnd.randrange(n) for _ in range(m - 1))) for _ in range(cap)); sampled = True
    t2 = T2(m); maxbad = 0; argmax = None; nms = 0
    maxU = {p: 0 for p in fac}
    fails = []
    K = max(1, min(4000, (1 << 22) // S))
    while True:
        chunk = list(itertools.islice(gen, K))
        if not chunk:
            break
        Bs = np.zeros((len(chunk), m), dtype=np.int64)
        Bs[:, 1:] = np.array(chunk, dtype=np.int64).reshape(len(chunk), m - 1)
        nms += len(chunk)
        z = {}
        for d in divs:
            M = V(d).astype(np.float32)[Bs % d]                    # (K, m, f)
            R = np.tensordot(E, M, axes=([1], [1]))                # (S, K, f)
            z[d] = ~R.any(axis=2)
        anyb = np.zeros_like(z[1])
        for d in divs:
            anyb |= z[d]
        cnt = anyb.sum(axis=0)
        i = int(cnt.argmax())
        if cnt[i] > maxbad:
            maxbad = int(cnt[i]); argmax = tuple(int(x) for x in Bs[i])
        for i in np.nonzero(cnt * F(1, S) > t2)[0] if False else np.nonzero(cnt > float(t2) * S + 1e-9)[0]:
            fails.append(("T2", tuple(int(x) for x in Bs[i]), int(cnt[i])))
        for p, a in fac.items():
            ev = np.zeros_like(z[1])
            for i_ in range(1, a + 1):
                ev |= z[p ** i_]
            ev &= ~z[1]
            c2 = ev.sum(axis=0)
            maxU[p] = max(maxU[p], int(c2.max()))
            ub = U_bound(p, m)
            for i in np.nonzero(c2 > float(ub) * S + 1e-9)[0]:
                fails.append(("U_%d" % p, tuple(int(x) for x in Bs[i]), int(c2[i])))
    print("exh n=%d m=%d multisets=%d%s  largest bad share=%s at %s  T2(m)=%s  largest U-share: %s  failures=%d" % (
        n, m, nms, " (random sample)" if sampled else " (all with 0)", F(maxbad, S), argmax, t2,
        " ".join("%d:%s(<=%s)" % (p, F(maxU[p], S), U_bound(p, m)) for p in sorted(fac)), len(fails)), flush=True)
    for f in fails[:10]:
        print("   FAILURE", f, flush=True)
    return len(fails)


# ------------------------------------------------------------------ lemma tests, one multiset at a time
class Stats:
    def __init__(self):
        self.d = {}

    def add(self, k, v=1):
        self.d[k] = self.d.get(k, 0) + v


def lemma_tests(B, n, st, l4=False):
    B = list(B); m = len(B); E = signs(m); S = E.shape[0]
    fac = factor(n); divs = divisors(n)
    fails = []
    bad = {d: zero_rows(E, V(d)[[b % d for b in B]]) for d in divs}
    anyb = np.zeros(S, dtype=bool)
    for d in divs:
        anyb |= bad[d]
    live = {}
    for p, a in fac.items():
        lv = []
        for i in range(1, a + 1):
            groups = {}
            for b in B:
                groups.setdefault(b % p ** (i - 1), set()).add(b % p ** i)
            if any(len(s) == p for s in groups.values()):
                lv.append(i)
        live[p] = lv
    fully = []; share = {}
    for d in divs:
        g = rad(d); d0 = d // g
        cells = {}
        for i, b in enumerate(B):
            cells.setdefault(b % d0, []).append(i)
        cz = {}; ks = {}
        allz = np.ones(S, dtype=bool)
        for c0, idx in cells.items():
            kk = []
            for i in idx:
                x = (B[i] % d) - c0
                assert x % d0 == 0
                kk.append((x // d0) % g)
            ks[c0] = kk
            cz[c0] = zero_rows(E[:, idx], V(g)[kk])
            allz &= cz[c0]
        st.add("Lemma 1: pairs (multiset, d)")
        if not np.array_equal(allz, bad[d]):
            fails.append(("Lemma 1", d))
        share[d] = F(int(bad[d].sum()), S)
        prodc = F(1)
        for c0 in cells:
            prodc *= F(int(cz[c0].sum()), S)
        if prodc != share[d]:
            fails.append(("product over cells", d))
        if d == 1:
            continue
        pr = sorted(factor(d))
        pfull = {}
        for p in pr:
            pfull[p] = [c0 for c0 in cells if len({k % p for k in ks[c0]}) == p]
            if pfull[p] and factor(d)[p] not in live[p]:
                fails.append(("p-full cell but level not live", d, p))
        # cell values through each prime, by the actual sizes and by vf / vnf
        for p in pr:
            g2 = g // p
            for c0, idx in cells.items():
                R = len(idx)
                sizes = {}
                for k in ks[c0]:
                    sizes[k % p] = sizes.get(k % p, 0) + 1
                rs = sorted(sizes.values())
                actual = F(int(cz[c0].sum()), S)
                isfull = len(rs) == p
                if not isfull:
                    b1 = F(1)
                    for r in rs:
                        b1 *= RT.z(r, p)
                    b2 = RT.vnf(p, R)
                else:
                    pz = F(1)
                    for r in rs:
                        pz *= RT.z(r, p)
                    pc = F(1)
                    for r in rs[1:]:
                        pc *= RT.cnz(r)
                    if p == 3 and rs[0] == 1 and 2 in rs:
                        pc = F(0)
                    b1 = pz + pc
                    b2 = RT.vf(p, R)
                st.add("cell values: (multiset, d, p, cell)")
                if actual > b1:
                    fails.append(("cell value by sizes", d, p, c0, rs, actual, b1))
                if b1 > b2:
                    fails.append(("sizes bound above vf/vnf", d, p, rs, b1, b2))
                if actual == b2:
                    st.add("cell values: equality with vf/vnf")
                if l4:
                    cls = {}
                    for i, k in zip(idx, ks[c0]):
                        cls.setdefault(k % p, []).append(k % g2)
                    roots = {tuple(sgn * V(g2)[j]) for j in range(g2) for sgn in (1, -1)}
                    for t, kl in cls.items():
                        r = len(kl)
                        if r > 12:
                            continue
                        vals = signs(r) @ V(g2)[kl]
                        uq, cnts = np.unique(vals, axis=0, return_counts=True)
                        st.add("Lemma 4: classes")
                        zc = 0; mx = 0; mxnz = 0; hitroot = False
                        for row, c_ in zip(uq, cnts):
                            mx = max(mx, int(c_))
                            if not row.any():
                                zc = int(c_)
                            else:
                                mxnz = max(mxnz, int(c_))
                                if tuple(row) in roots:
                                    hitroot = True
                        zb = RT.z(r, 3) if (r == 3 and g2 % 3 != 0) else RT.z(r, 5)
                        if F(mx, 2 ** r) > RT.c(r):
                            fails.append(("Lemma 4a", d, p, kl))
                        if F(zc, 2 ** r) > zb:
                            fails.append(("Lemma 4b", d, p, kl, zc))
                        if F(mxnz, 2 ** r) > RT.cnz(r):
                            fails.append(("Lemma 4c", d, p, kl, mxnz))
                        if r == 2 and g2 % 3 != 0 and hitroot:
                            fails.append(("Lemma 4c pair = root", d, p, kl))
        if all(pfull[p] for p in pr):
            fully.append(d)
            ranks = {p: live[p].index(factor(d)[p]) + 1 for p in pr}
            G = max(1 + (ranks[p] - 1) * (p - 1) for p in pr)
            st.add("Lemma 5: fully live (multiset, d)")
            if len(cells) < G:
                fails.append(("Lemma 5", d, len(cells), G))
            for p in pr:
                st.add("Prop 6: (multiset, fully live d, p)")
                bf = RT.BF(p, G, m)
                if share[d] > bf:
                    fails.append(("Prop 6", d, p, share[d], bf))
                if share[d] == bf:
                    st.add("Prop 6: equality")
    # Lemma 2, strong form: the least d at which a signing is bad is 1 or fully live
    seen = np.zeros(S, dtype=bool)
    for d in divs:
        first = bad[d] & ~seen
        if d > 1 and first.any() and d not in fully:
            fails.append(("Lemma 2", d))
        seen |= bad[d]
    cover = bad[1].copy()
    for d in fully:
        cover |= bad[d]
    if not np.array_equal(cover, anyb):
        fails.append(("Lemma 2 cover",))
    st.add("Lemma 2: multisets")
    # U_p
    for p, a in fac.items():
        ev = np.zeros(S, dtype=bool)
        for i in range(1, a + 1):
            ev |= bad[p ** i]
        ev &= ~bad[1]
        u = F(int(ev.sum()), S); ub = U_bound(p, m)
        if u > ub:
            fails.append(("U_p", p, u, ub))
        if u == ub and ub > 0:
            st.add("U_p attained")
    comp = sum((share[d] for d in fully if len(factor(d)) >= 2), F(0))
    cb = RT.COMP(m)[0]
    if comp > cb:
        fails.append(("COMP", comp, cb))
    if comp == cb and cb > 0:
        st.add("COMP attained")
    tot = F(int(anyb.sum()), S)
    if tot > T2(m) or (m >= 3 and tot > F(3, 8)):
        fails.append(("THEOREM", tot, T2(m)))
    st.add("multisets"); st.add("signings", S)
    return tot, fails


def shaped(n, m, rnd):
    fac = factor(n); ps = sorted(fac)
    kind = rnd.randrange(8)
    if kind == 0:      # few residues with multiplicities
        k = rnd.randint(2, min(m, 6)); res = [rnd.randrange(n) for _ in range(k)]
        return [rnd.choice(res) for _ in range(m)]
    if kind == 1:      # heavy element and a coset of the subgroup of order p
        p = rnd.choice(ps); b = rnd.randrange(n)
        B = [(b + t * (n // p)) % n for t in range(1, p)]
        B = B[:m - 1]
        return B + [b] * (m - len(B))
    if kind == 2:      # all elements in pairs
        k = m // 2; sub = rnd.choice([1] + [n // q for q in ps] + [n // (q * r) for q in ps for r in ps if n % (q * r) == 0])
        res = [(rnd.randrange(n) * sub) % n for _ in range(k)]
        B = [x for x in res for _ in (0, 1)]
        return B + [rnd.randrange(n)] * (m - len(B))
    if kind == 3:      # union of cosets of subgroups of prime order
        B = []
        while len(B) < m:
            p = rnd.choice(ps); b = rnd.randrange(n)
            B += [(b + t * (n // p)) % n for t in range(p)]
        return B[:m]
    if kind == 4:      # a row and a column of a p x q block, with multiplicities
        if len(ps) < 2:
            return [rnd.randrange(n) for _ in range(m)]
        p, q = rnd.sample(ps, 2); b = rnd.randrange(n)
        B = [(b + t * (n // p)) % n for t in range(p)] + [(b + t * (n // q)) % n for t in range(1, q)]
        while len(B) < m:
            B.append(rnd.choice(B))
        rnd.shuffle(B)
        return B[:m]
    if kind == 5:      # everything inside a small subgroup (many levels live for the small primes), in pairs or not
        sub = n // rnd.choice([q ** rnd.randint(1, fac[q]) for q in ps])
        if rnd.random() < 0.5:
            sub = 1
        base = [((rnd.randrange(n)) * sub) % n for _ in range(rnd.randint(2, 5))]
        return [rnd.choice(base) for _ in range(m)]
    if kind == 6:      # CRT product of small residue sets, with multiplicities
        B = []
        choices = {q: rnd.sample(range(q), min(q, rnd.randint(1, 3))) for q in ps}
        for _ in range(m):
            x = 0
            for q in ps:
                r = rnd.choice(choices[q])
                # digit at the top level of q: multiples of n/q
                x += r * (n // q)
            B.append(x % n)
        return B
    return [rnd.randrange(n) for _ in range(m)]


def main():
    mode = sys.argv[1]
    t0 = time.time()
    if mode == 'exh':
        n, m = int(sys.argv[2]), int(sys.argv[3]); cap = int(sys.argv[4]) if len(sys.argv) > 4 else 10 ** 9
        exh(n, m, cap)
    elif mode in ('lem', 'lemexh'):
        st = Stats(); nf = 0; best = F(0); arg = None
        if mode == 'lem':
            n, m, count, seed = (int(x) for x in sys.argv[2:6]); l4 = len(sys.argv) > 6
            rnd = random.Random(seed)
            gen = (shaped(n, m, rnd) for _ in range(count))
        else:
            n, m = int(sys.argv[2]), int(sys.argv[3]); l4 = len(sys.argv) > 4
            gen = ([0] + list(t) for t in itertools.combinations_with_replacement(range(n), m - 1))
        for B in gen:
            tot, fails = lemma_tests(B, n, st, l4)
            if tot > best:
                best = tot; arg = sorted(B)
            if fails:
                nf += 1
                if nf <= 5:
                    print("   FAILURE", sorted(B), fails[:3], flush=True)
        print("%s n=%d m=%d  largest bad share %s (T2=%s) at %s  failures=%d  %.0fs" % (mode, n, m, best, T2(m), arg, nf, time.time() - t0))
        print("   " + "; ".join("%s: %d" % kv for kv in sorted(st.d.items())), flush=True)


if __name__ == '__main__':
    main()
