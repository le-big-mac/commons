"""Referee's tests of sections 1-5 of result.md (the tree of 3), written from the text.

A multiset on Z_(3^a) up to the automorphisms of the ternary tree is a nested sorted triple ("shape").  For a shape the
joint law of (sum of signs, set of levels i in 1..a with E_i) is computed exactly by convolution over the children;
the events themselves are compared with division by Phi_(3^i) on explicit multisets, all signings (mode def).

usage: ref_tree3.py shapes A MMAX     every shape of depth A with 1..MMAX elements: Lemmas 1, 2 (i)(a)(b)(c), X <= xi
       ref_tree3.py def SEED COUNT    tree events against polynomial division, random multisets on Z_9 .. Z_243
       ref_tree3.py big SEED COUNT MLO MHI   structured shapes with many elements
"""
import sys, random, itertools
from fractions import Fraction as Fr
from math import comb
from functools import lru_cache


def pi(v, r):
    if abs(v) > r or (r + v) % 2:
        return Fr(0)
    return Fr(comb(r, (r + v) // 2), 2 ** r)


def cc(r):
    return Fr(comb(r, r // 2), 2 ** r)


def A_of(r0, r1, r2):
    top = min(r0, r1, r2)
    return sum(pi(v, r0) * pi(v, r1) * pi(v, r2) for v in range(-top, top + 1) if v != 0)


def xi_table(M):
    xi = [Fr(0), Fr(0)]
    for m in range(2, M + 1):
        best = Fr(0)
        for r2 in range(0, m // 3 + 1):
            for r1 in range(max(1, r2), m):
                r0 = m - r1 - r2
                if r0 < r1:
                    break
                gs = [(cc(r) if r % 2 == 0 else 0) + xi[r] for r in (r0, r1, r2)]
                rules = [gs[0] * gs[1] * gs[2]]
                if r0 % 2 == 0 and r1 % 2 == 0 and r2 % 2 == 0:
                    rules.append(gs[0] * gs[1] * gs[2] - cc(r0) * cc(r1) * cc(r2))
                if r2 == 0 and r0 % 2 and r1 % 2 and r0 <= 7:
                    rules.append(xi[r0] * xi[r1] / 2)
                best = max(best, A_of(r0, r1, r2) + min(rules))
        xi.append(best)
    return xi


def size(s):
    return s if isinstance(s, int) else sum(size(t) for t in s)


def depth(s):
    return 0 if isinstance(s, int) else 1 + depth(s[0])


@lru_cache(maxsize=None)
def law(s):
    """dict (sigma, mask) -> number of signings; bit (i-1) of mask set iff E_i holds (i = 1 at the root)"""
    if isinstance(s, int):
        return {(v, 0): comb(s, (s + v) // 2) for v in range(-s, s + 1, 2)}
    L0, L1, L2 = law(s[0]), law(s[1]), law(s[2])
    out = {}
    for (v0, k0), n0 in L0.items():
        for (v1, k1), n1 in L1.items():
            for (v2, k2), n2 in L2.items():
                e1 = 1 if (v0 == v1 == v2) else 0
                key = (v0 + v1 + v2, e1 | ((k0 & k1 & k2) << 1))
                out[key] = out.get(key, 0) + n0 * n1 * n2
    return out


def numbers(s):
    """shares for the multiset s: X, P(U), z = P(U and sigma = 0), P(bad), P(E1 and sigma != 0), P(H), P(H and sigma != 0)"""
    m = size(s); T = 2 ** m; L = law(s)
    f = lambda cond: Fr(sum(n for (v, k), n in L.items() if cond(v, k)), T)
    return dict(X=f(lambda v, k: k and v), U=f(lambda v, k: k), z=f(lambda v, k: k and v == 0), bad=f(lambda v, k: k or v == 0),
                E1X=f(lambda v, k: (k & 1) and v), H=f(lambda v, k: k >> 1), HX=f(lambda v, k: (k >> 1) and v))


@lru_cache(maxsize=None)
def all_shapes(a, m):
    if a == 0:
        return (m,)
    out = []
    for r0 in range(m, -1, -1):
        for r1 in range(min(r0, m - r0), -1, -1):
            r2 = m - r0 - r1
            if r2 > r1:
                continue
            S0, S1, S2 = all_shapes(a - 1, r0), all_shapes(a - 1, r1), all_shapes(a - 1, r2)
            for i0, s0 in enumerate(S0):
                for i1, s1 in enumerate(S1):
                    if r1 == r0 and i1 > i0:
                        continue
                    for i2, s2 in enumerate(S2):
                        if r2 == r1 and i2 > i1:
                            continue
                        out.append((s0, s1, s2))
    return tuple(out)


def check_shape(s, xi, cnt):
    """all the statements of sections 2, 3 for the shape s (root at depth a >= 1); returns X, bad share"""
    m = size(s); nb = numbers(s)
    assert nb['X'] <= xi[m], ("X > xi", s)
    kids = [numbers(t) for t in s]; rs = [size(t) for t in s]
    occ = [t for t in range(3) if rs[t]]
    if len(occ) <= 1:
        if occ:
            t = occ[0]
            assert nb['X'] == kids[t]['X'] and nb['bad'] == kids[t]['bad'], ("Lemma 1", s)
            cnt['L1'] += 1
        return nb['X'], nb['bad']
    A = A_of(*rs)
    assert nb['E1X'] == A, ("Lemma 2 (i)", s); cnt['i'] += 1
    assert nb['X'] <= A + nb['HX'], ("Lemma 2 head", s)
    assert nb['HX'] <= kids[0]['U'] * kids[1]['U'] * kids[2]['U'], ("Lemma 2 (a) first", s)
    for t in range(3):
        cap = Fr(1) if rs[t] == 0 else (cc(rs[t]) if rs[t] % 2 == 0 else 0) + kids[t]['X']
        assert kids[t]['U'] <= cap, ("Lemma 2 (a) second", s)
    cnt['a'] += 1
    if all(r % 2 == 0 for r in rs):
        zs = [k['z'] for k in kids]; Xs = [k['X'] for k in kids]
        assert all(zs[t] <= cc(rs[t]) for t in range(3)), ("Lemma 2 (b) z", s)
        assert all(kids[t]['U'] == zs[t] + Xs[t] for t in range(3))
        rhs = (zs[0] + Xs[0]) * (zs[1] + Xs[1]) * (zs[2] + Xs[2]) - zs[0] * zs[1] * zs[2]
        assert nb['HX'] <= rhs, ("Lemma 2 (b)", s)
        rhs2 = 1
        for t in range(3):
            rhs2 *= cc(rs[t]) + Xs[t]
        rhs2 -= cc(rs[0]) * cc(rs[1]) * cc(rs[2])
        assert rhs <= rhs2, ("Lemma 2 (b) monotone", s)
        cnt['b'] += 1
    srt = sorted(range(3), key=lambda t: -rs[t])
    if rs[srt[2]] == 0 and rs[srt[0]] % 2 and rs[srt[1]] % 2 and rs[srt[0]] <= 7:
        assert nb['HX'] == nb['H'] / 2, ("Lemma 2 (c) equality", s)
        assert nb['H'] <= kids[srt[0]]['X'] * kids[srt[1]]['X'], ("Lemma 2 (c) inequality", s)
        cnt['c'] += 1
    # the same statement (c) without the bound 7 is recorded, not asserted
    if rs[srt[2]] == 0 and rs[srt[0]] % 2 and rs[srt[1]] % 2 and rs[srt[0]] > 7:
        cnt['c_over7'] += 1
        if nb['HX'] != nb['H'] / 2:
            cnt['c_over7_fails'] += 1
    return nb['X'], nb['bad']


def run_shapes(a, mmax):
    xi = xi_table(mmax)
    print(f"depth {a} (Z_{3 ** a}): every shape with 1..{mmax} elements")
    total = 0
    for m in range(1, mmax + 1):
        cnt = dict(L1=0, i=0, a=0, b=0, c=0, c_over7=0, c_over7_fails=0)
        bx = Fr(0); bb = Fr(0); ex = None
        S = all_shapes(a, m)
        for s in S:
            X, bad = check_shape(s, xi, cnt)
            if X > bx:
                bx = X; ex = s
            bb = max(bb, bad)
        total += len(S)
        tb = (cc(m) if m % 2 == 0 else 0) + xi[m]
        print(f"m = {m:2d}: {len(S):7d} shapes; largest X = {bx} (xi = {xi[m]}, equal: {bx == xi[m]}); largest bad share = {bb} (tbar = {tb}, equal: {bb == tb}); checks {cnt}", flush=True)
        if ex is not None and m % 2 == 0:
            print(f"        X largest at {ex}", flush=True)
        law.cache_clear()
    print(f"{total} shapes, no failure")


# ---------- the definition
def run_def(seed, count):
    import numpy as np
    from cyc import signs, bad_at
    rnd = random.Random(seed); nsign = 0

    def shape_of(a, elems):
        if a == 0:
            return len(elems)
        return tuple(shape_of(a - 1, [b // 3 for b in elems if b % 3 == t]) for t in range(3))

    for _ in range(count):
        a = rnd.choice([1, 2, 2, 3, 3, 4, 5]); n = 3 ** a; m = rnd.randint(1, 11)
        st = rnd.randint(0, 4)
        if st == 0:
            B = [rnd.randrange(n) for _ in range(m)]
        elif st == 1:
            pool = [rnd.randrange(n) for _ in range(rnd.randint(1, 4))]; B = [rnd.choice(pool) for _ in range(m)]
        elif st == 2:
            pool = [rnd.randrange(n) for _ in range((m + 1) // 2)]; B = (pool + pool)[:m]
        elif st == 3:
            x = rnd.randrange(n); B = [x] * max(m - 2, 0) + [(x + rnd.choice([1, 2, 3, 6, 9, 18]) ) % n for _ in range(min(m, 2))]
        else:
            step = 3 ** rnd.randint(0, a - 1); B = [(rnd.randrange(3) * step + rnd.randrange(3) * step * 3) % n for _ in range(m)]
        E = signs(m)
        sig = E.sum(axis=1)
        mask = np.zeros(2 ** m, dtype=np.int64)
        for i in range(1, a + 1):
            mask |= bad_at(n, B, 3 ** i, E).astype(np.int64) << (i - 1)
        assert np.array_equal(bad_at(n, B, 1, E), sig == 0)
        D = {}
        for v, k in zip(sig.tolist(), mask.tolist()):
            D[(v, k)] = D.get((v, k), 0) + 1
        L = {k: v for k, v in law(shape_of(a, B)).items() if v}
        assert D == L, ("tree events differ from division by Phi", n, B)
        nsign += 2 ** m
    print(f"seed {seed}: {count} multisets on Z_3 .. Z_243, 1 to 11 elements, {nsign} signings: the law of (sum, levels 3^i dividing) by polynomial division equals the tree law; no failure")


# ---------- many elements
def rand_shape(rnd, a, m, style):
    if a == 0:
        return m
    if m == 0:
        return (rand_shape(rnd, a - 1, 0, style),) * 3
    st = style if style is not None else rnd.randint(0, 6)
    if st == 0:
        p = [m, 0, 0]
    elif st == 1:                                   # heavy and two small
        x = rnd.randint(1, 3); y = rnd.randint(0, 3)
        x = min(x, m); y = min(y, m - x); p = [m - x - y, x, y]
    elif st == 2:                                   # all even if m even
        x = 2 * rnd.randint(0, m // 4); y = 2 * rnd.randint(0, (m - x) // 4); p = [m - x - y, x, y]
    elif st == 3:                                   # (r, 6, 6), (r, 6, 2), (r, 2, 2): where the recursion peaks
        x, y = rnd.choice([(6, 6), (6, 2), (2, 2), (6, 4), (4, 4), (3, 3), (5, 5), (7, 7), (3, 0), (5, 0), (7, 0)])
        if x + y > m:
            x, y = min(m, 2), 0
        p = [m - x - y, x, y]
    elif st == 4:
        p = [m // 3, (m + 1) // 3, m - m // 3 - (m + 1) // 3]
    elif st == 5:                                   # odd, odd, 0
        x = rnd.choice([1, 3, 5, 7, 9]); x = min(x, m); p = [m - x, x, 0]
    else:
        x = rnd.randint(0, m); y = rnd.randint(0, m - x); p = [x, y, m - x - y]
    sub = None if rnd.random() < 0.5 else st
    return tuple(rand_shape(rnd, a - 1, r, sub) for r in p)


def run_big(seed, count, mlo, mhi):
    rnd = random.Random(seed); xi = xi_table(mhi)
    best = {}; cnt = dict(L1=0, i=0, a=0, b=0, c=0, c_over7=0, c_over7_fails=0)
    for _ in range(count):
        a = rnd.randint(1, 5); m = rnd.randint(mlo, mhi)
        s = rand_shape(rnd, a, m, None)
        X, bad = check_shape(s, xi, cnt)
        tb = (cc(m) if m % 2 == 0 else 0) + xi[m]
        assert bad <= tb and bad <= Fr(3, 8)
        if X > best.get(m, (Fr(-1),))[0]:
            best[m] = (X, s)
        law.cache_clear()
    print(f"seed {seed}: {count} structured shapes of depth 1..5 with {mlo}..{mhi} elements: all statements hold; checks {cnt}")
    for m in sorted(best):
        print(f"  m = {m}: largest X = {best[m][0]} = {float(best[m][0]):.6f}, xi = {float(xi[m]):.6f}, equal: {best[m][0] == xi[m]}")


if __name__ == '__main__':
    if sys.argv[1] == 'shapes':
        run_shapes(int(sys.argv[2]), int(sys.argv[3]))
    elif sys.argv[1] == 'def':
        run_def(int(sys.argv[2]), int(sys.argv[3]))
    else:
        run_big(*[int(x) for x in sys.argv[2:6]])
