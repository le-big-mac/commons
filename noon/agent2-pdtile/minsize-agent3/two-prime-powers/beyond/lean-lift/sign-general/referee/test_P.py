# Referee test of Lemma 3 / Theorem P as statements, and of the inner counts of the proof of Lemma 3.
# usage: test_P.py sides(comma) q nfun seed [internals]
import sys, random, itertools, time
import numpy as np
from fractions import Fraction
from boxlib import *

sides = [int(x) for x in sys.argv[1].split(',')]
q = int(sys.argv[2])
nfun = int(sys.argv[3])
random.seed(int(sys.argv[4]))
internals = len(sys.argv) > 5
k = len(sides)
LV = all_levels(k)
t0 = time.time()


def rv(lo=-3, hi=3):
    if q:
        return random.randrange(q)
    return random.randint(lo, hi)


def rvec(n, nz=True):
    while True:
        v = [rv() for _ in range(n)]
        if not nz or any(x % q if q else x for x in v):
            return v


def families():
    shape = tuple(sides)
    # 1 random 0/1
    d = random.random()
    yield 'rand01', (np.random.random(shape) < d).astype(np.int64)
    # 2 random values
    yield 'rand', np.array([rv() for _ in range(int(np.prod(shape)))]).reshape(shape)
    # 3 sparse
    g = np.zeros(shape, dtype=np.int64)
    for _ in range(random.randint(1, 4)):
        g[tuple(random.randrange(n) for n in sides)] = random.choice([1, -1, 2, rv()])
    yield 'sparse', g
    # 4 supported on a line
    i = random.randrange(k)
    idx = [random.randrange(n) for n in sides]
    g = np.zeros(shape, dtype=np.int64)
    v = random.choice([rvec(sides[i]), [random.choice([1, -1]) for _ in range(sides[i])], [1] * sides[i],
                       [1, 1] + [0] * (sides[i] - 2), [1, -1] + [0] * (sides[i] - 2)])
    for a in range(sides[i]):
        idx[i] = a
        g[tuple(idx)] = v[a]
    yield 'line', g
    # 5 products
    vs = []
    for n in sides:
        vs.append(random.choice([rvec(n), [1, 1] + [0] * (n - 2), [1] * n, [random.choice([1, -1]) for _ in range(n)],
                                 [1, -1] + [0] * (n - 2), [1] + [0] * (n - 1)]))
    g = np.array(vs[0])
    for v in vs[1:]:
        g = np.multiply.outer(g, np.array(v))
    yield 'product', g
    # 6 sum of two products
    def prod():
        g = np.array(rvec(sides[0]))
        for n in sides[1:]:
            g = np.multiply.outer(g, np.array(random.choice([rvec(n), [1, 1] + [0] * (n - 2), [1] * n])))
        return g
    yield 'two products', prod() + prod()
    # 7 slices equal up to sign along a random axis
    i = random.randrange(k)
    rest = [n for j, n in enumerate(sides) if j != i]
    u = np.array([rv() for _ in range(int(np.prod(rest)))]).reshape(rest) if rest else np.array(1)
    if random.random() < .5:
        u = (np.random.random(rest) < .5).astype(np.int64)
    eps = np.array([random.choice([1, -1]) for _ in range(sides[i])])
    if random.random() < .3:
        eps = np.array([random.choice([1, -1, 0]) for _ in range(sides[i])])
    g = np.moveaxis(np.multiply.outer(eps, u), 0, i)
    yield 'slices equal up to sign', g
    # 8 dependent slices (rank 2 along a random axis)
    if rest:
        u = np.array([rv() for _ in range(int(np.prod(rest)))]).reshape(rest)
        w = np.array([rv() for _ in range(int(np.prod(rest)))]).reshape(rest)
        c = np.array(rvec(sides[i], False))
        dd = np.array(random.choice([rvec(sides[i], False), [random.choice([1, -1]) for _ in range(sides[i])]]))
        g = np.moveaxis(np.multiply.outer(c, u) + np.multiply.outer(dd, w), 0, i)
        yield 'dependent slices', g
        # 9 slices: sign vector times u plus degenerate perturbations (constants) -- aims at the Claim
        s = np.array([random.choice([1, -1]) for _ in range(sides[i])])
        cst = np.array(rvec(sides[i], False))
        g = np.moveaxis(np.multiply.outer(s, u) + np.multiply.outer(cst, np.ones(rest, dtype=np.int64)), 0, i)
        yield 'sign*u + const', g


np.random.seed(int(sys.argv[4]))
worst = {}
bound = Fraction(1, 2 ** k)
total_pat = 2 ** sum(sides)
stats = dict(caseK0=0, caseKnon=0, lost_total=0, max_lost_ratio=Fraction(0), claim_checks=0, minA_ratio=None)
done = 0
checked_brute = 0
while done < nfun and time.time() - t0 < 85:
    for name, g in families():
        gg = g % q if q else g
        if not gg.any():
            continue
        done += 1
        res, per = good_table(gg, sides, q, LV)
        cnt = int(res.sum())
        fr = Fraction(cnt, total_pat)
        if name not in worst or fr < worst[name][0]:
            worst[name] = (fr, gg.copy())
        if fr < bound:
            print('VIOLATION of Theorem P count', name, fr, gg.tolist())
        # occasional independent check of the fast cube test against brute force on one pattern
        if checked_brute < 40 and k <= 2:
            checked_brute += 1
            sig = [random.randrange(2 ** n) for n in sides]
            sv = [signs(n)[s] for n, s in zip(sides, sig)]
            h = gg.copy()
            for i, s in enumerate(sv):
                sh = [1] * k
                sh[i] = sides[i]
                h = h * s.reshape(sh)
            for P in LV:
                assert brute_cube_good(h, sides, P, q) == bool(per[P][tuple(sig)]), 'fast/brute mismatch'
        if internals:
            # X_1 = axis 0 (size p), Y = the other axes.
            p = sides[0]
            Ys = sides[1:]
            SY = 2 ** sum(Ys)
            L0 = [P for P in LV if 0 not in P]
            L1 = [P for P in LV if 0 in P]
            A = np.ones_like(res)
            for P in L0:
                A &= per[P]
            A2 = A.reshape(2 ** p, SY)
            lostP = {P: (A & ~per[P]).reshape(2 ** p, SY) for P in L1}
            lost = np.zeros_like(A2)
            for P in L1:
                lost |= lostP[P]
            assert ((A2 & ~lost) == res.reshape(2 ** p, SY)).all()
            G = gg.reshape(p, -1)
            rk = rank(G.tolist(), q)
            S = signs(p)
            us = S @ G
            if q:
                us %= q
            inK = ~us.any(axis=1)
            # gamma for Y (true least fraction is not known here; use the proved 2^-(k-1) when Y satisfies Thm P,
            # only as a check of the hypothesis)
            gam = Fraction(1, 2 ** (k - 1))
            for si in range(2 ** p):
                if not inK[si]:
                    r = Fraction(int(A2[si].sum()), SY)
                    if stats['minA_ratio'] is None or r < stats['minA_ratio']:
                        stats['minA_ratio'] = r
            stats['lost_total'] += int(lost.sum())
            if rk < p:
                stats['caseKnon'] += 1
                # K^perp = column space of G^T ... K = {t : t G = 0}, K^perp = column space of G
                inKp = np.array([rank(np.hstack([G, S[si][:, None]]).tolist(), q) == rk for si in range(2 ** p)])
                bad = lost.any(axis=1) & ~inKp
                if bad.any():
                    print('VIOLATION: lost pair with s not in K-perp', gg.tolist())
                if int((inK | inKp).sum()) > 2 ** (p - 1):
                    print('VIOLATION Lemma 2(d)', gg.tolist(), int((inK | inKp).sum()))
                outside = ~(inK | inKp)
                if int(res.reshape(2 ** p, SY)[outside].sum()) != int(A2[outside].sum()):
                    print('VIOLATION: pairs in A with s outside K u Kperp not all good')
            else:
                stats['caseK0'] += 1
                for P in L1:
                    lp = lostP[P]
                    percol = lp.sum(axis=0)
                    if percol.max() > 2:
                        print('VIOLATION: more than two s lost for one (sigma_Y, P)', gg.tolist(), P)
                    for col in np.nonzero(percol == 2)[0][:5]:
                        ss = np.nonzero(lp[:, col])[0]
                        if not (S[ss[0]] == -S[ss[1]]).all():
                            print('VIOLATION: two lost s not opposite', gg.tolist())
                r = Fraction(int(lost.sum()), 2 * len(L1) * SY)
                if r > stats['max_lost_ratio']:
                    stats['max_lost_ratio'] = r
                if int(lost.sum()) > 2 * len(L1) * SY:
                    print('VIOLATION: |Lost| > 2|L1||Sigma_Y|', gg.tolist())
            # the Claim itself on a few lost pairs: class of sigma_Y u_t = <s,t> b, b = class of s_0 sigma_Y g_0, b != 0
            SYs = [signs(n) for n in Ys]
            pairs = np.argwhere(lost)
            for (si, yi) in pairs[np.random.permutation(len(pairs))[:3]] if len(pairs) else []:
                idx = np.unravel_index(yi, [2 ** n for n in Ys])
                sy = np.array(1)
                for a, n in zip(idx, Ys):
                    sy = np.multiply.outer(sy, SYs[Ys.index(n) if Ys.count(n) == 1 else 0][a]) if False else np.multiply.outer(sy, signs(n)[a])
                sy = sy.reshape(Ys)
                s = S[si]
                for P in L1:
                    if not lostP[P][si, yi]:
                        continue
                    Pp = frozenset(i - 1 for i in P if i != 0)
                    b = s[0] * sy * gg[0]
                    if not cube_sums_plain(b, Ys, Pp, q).any():
                        print('VIOLATION: class b is zero', gg.tolist())
                    for v in range(p):
                        if cube_sums_plain(s[v] * sy * gg[v] - b, Ys, Pp, q).any():
                            print('VIOLATION: slices not congruent on a lost pair (Lemma 1(b))')
                    for _ in range(3):
                        t = np.array(rvec(p, False))
                        ut = np.tensordot(t, gg, axes=(0, 0))
                        diff = sy * ut - int(s @ t) * b
                        if cube_sums_plain(diff, Ys, Pp, q).any():
                            print('VIOLATION of the Claim', gg.tolist())
                        stats['claim_checks'] += 1

print('box', sides, 'field', 'Q' if q == 0 else 'F_%d' % q, 'functions', done, 'bound 2^-k =', bound,
      'time %.1fs' % (time.time() - t0))
for name in worst:
    print('  %-26s least fraction %s' % (name, worst[name][0]))
allmin = min(w[0] for w in worst.values())
print('  least over all:', allmin)
if internals:
    print('  internals:', {a: str(b) for a, b in stats.items()})
