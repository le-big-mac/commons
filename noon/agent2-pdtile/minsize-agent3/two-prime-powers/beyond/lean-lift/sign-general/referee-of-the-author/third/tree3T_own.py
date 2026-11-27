"""Referee, third pass: Lemma 3T and Lemma 3' of sign-all-result.md on two-tree boxes X = T x Y, from the text.

For a function g on T x Y (T the new coordinate) and EVERY pattern (s, sigma_Y) on the active rows and columns
(rows and columns on which g vanishes do not matter: their signs multiply every count by the same power of 2):
  nz[i][j](s, sigma) = "some cube sum of (s, sigma) g at the level (i, j) is not 0"            (the definition; treetools)
  good = all nz;   A = pairs with sigma u_s good on Y = all_j nz[0][j]                          (Lemma 1T(a))
  rank r of the slices.
  r = 1:  g = c (x) h;  check  good(s, sigma) <=> (sc good on T) and (sigma h good on Y);  count >= single(T) single(Y).
  r >= 2: sign vectors in K = {u_s = 0} at most a quarter;
          for every (sigma, level j of Y), with x_v = class of sigma g_v modulo Deg_Y(j):
              |B(x)| = #{s : nz[0][j] and some i >= 1 with not nz[i][j]} <= lam(p, a) 2^(p^a)      (Lemma T as used)
          count of good pairs >= (3/4) single(Y) - L_Y lam(p, a)   (when that is positive);
          and for information: per sigma, the SUM over j and the UNION over j of the sets Lost(sigma, j) (section 6).
  a = 1 (Lemma 3'): for every (sigma, j) at most two s are lost, s and -s; count >= single(Y)/2 if K != 0, >= single(Y) - L_Y 2^(1-p) if K = 0.
usage: tree3T_own.py CASE SEED COUNT
"""
import sys, time
import numpy as np
from fractions import Fraction as Fr
from treetools import level_matrix, all_signs
from treeTS_own import lam, single, make_support

def rank_mod(Mx, q):
    Mx = [[int(x) % q for x in row] for row in Mx]; r = 0
    rows, cols = len(Mx), len(Mx[0])
    for c in range(cols):
        pr = next((i for i in range(r, rows) if Mx[i][c]), None)
        if pr is None: continue
        Mx[r], Mx[pr] = Mx[pr], Mx[r]
        inv = pow(Mx[r][c], -1, q)
        for i in range(r + 1, rows):
            if Mx[i][c]:
                f = Mx[i][c] * inv % q; Mx[i] = [(x - f * y) % q for x, y in zip(Mx[i], Mx[r])]
        r += 1
        if r == rows: break
    return r

def rank_Q(Mx):
    Mx = [[Fr(int(x)) for x in row] for row in Mx]; r = 0
    rows, cols = len(Mx), len(Mx[0])
    for c in range(cols):
        pr = next((i for i in range(r, rows) if Mx[i][c] != 0), None)
        if pr is None: continue
        Mx[r], Mx[pr] = Mx[pr], Mx[r]
        for i in range(r + 1, rows):
            if Mx[i][c] != 0:
                f = Mx[i][c] / Mx[r][c]; Mx[i] = [x - f * y for x, y in zip(Mx[i], Mx[r])]
        r += 1
        if r == rows: break
    return r

def nonzero(A, q):
    return (A != 0) if q is None else (A % q != 0)

def analyse(g, T, Y, q, st):
    p, a = T; r_, c_ = Y; nT, nY = p ** a, r_ ** c_
    gz = nonzero(g, q)
    actT = np.nonzero(gz.any(axis=1))[0]; actY = np.nonzero(gz.any(axis=0))[0]
    ST = np.ones((2 ** len(actT), nT), dtype=np.int64); ST[:, actT] = all_signs(len(actT))
    SY = np.ones((2 ** len(actY), nY), dtype=np.int64); SY[:, actY] = all_signs(len(actY))
    BT, BY = ST.shape[0], SY.shape[0]
    MT = [level_matrix(p, a, i) for i in range(a + 1)]; MY = [level_matrix(r_, c_, j) for j in range(c_ + 1)]
    W = [SY[:, None, :] * MY[j][None, :, :] for j in range(c_ + 1)]            # (BY, rows_j, nY)
    nz = [[None] * (c_ + 1) for _ in range(a + 1)]
    for i in range(a + 1):
        P = (MT[i][None, :, :] * ST[:, None, :]) @ g                           # (BT, rows_i, nY)
        for j in range(c_ + 1):
            R = np.tensordot(P, W[j], axes=([2], [2]))                         # (BT, rows_i, BY, rows_j)
            nz[i][j] = nonzero(R, q).any(axis=(1, 3))                          # (BT, BY)
    good = np.ones((BT, BY), dtype=bool)
    for i in range(a + 1):
        for j in range(c_ + 1): good &= nz[i][j]
    share = Fr(int(good.sum()), BT * BY)
    rk = rank_mod(g[actT][:, actY], q) if q else rank_Q(g[actT][:, actY])
    gamma_Y = single(r_, c_); gamma_T = single(p, a); LY = c_ + 1
    st['functions'] += 1
    st['least'] = min(st['least'], share)
    if rk == 1:
        v0, y0 = np.argwhere(gz)[0]
        cvec = g[:, y0]; h = g[v0]
        gT = np.ones(BT, dtype=bool)
        for i in range(a + 1): gT &= nonzero((ST * cvec[None, :]) @ MT[i].T, q).any(axis=1)
        gY = np.ones(BY, dtype=bool)
        for j in range(c_ + 1): gY &= nonzero((SY * h[None, :]) @ MY[j].T, q).any(axis=1)
        assert (good == (gT[:, None] & gY[None, :])).all(), ('rank one: the factorisation fails', g.tolist(), q)
        assert share >= gamma_T * gamma_Y, ('rank one: count below single(T) single(Y)', g.tolist(), q, share)
        st['rank1'] += 1; st['least1'] = min(st['least1'], share)
    else:
        us = ST @ g
        inK = ~nonzero(us, q).any(axis=1)
        assert Fr(int(inK.sum()), BT) <= Fr(1, 4), ('more than a quarter of the sign vectors in K', g.tolist(), q)
        A = np.ones((BT, BY), dtype=bool)
        for j in range(c_ + 1): A &= nz[0][j]
        assert int(A.sum()) >= Fr(3, 4) * gamma_Y * BT * BY, ('|A| below (3/4) gamma', g.tolist(), q)
        sum_lost = np.zeros(BY, dtype=np.int64); union = np.zeros((BT, BY), dtype=bool)
        for j in range(c_ + 1):
            deg = np.zeros((BT, BY), dtype=bool)
            for i in range(1, a + 1): deg |= ~nz[i][j]
            Bx = nz[0][j] & deg                                # s in B(x) for x = classes of sigma g_v at the level j
            cnt = Bx.sum(axis=0)                               # per sigma
            assert int(cnt.max()) <= lam(p, a) * BT, ('Lemma T fails inside Lemma 3T', g.tolist(), q, j, int(cnt.max()), BT)
            st['maxB'] = max(st['maxB'], Fr(int(cnt.max()), BT))
            lost = A & deg
            sum_lost += lost.sum(axis=0); union |= lost
            if a == 1:
                assert int(lost.sum(axis=0).max()) <= 2, ("Lemma 3': more than two lost sign vectors", g.tolist(), q, j)
                # closed under s -> -s: the sign arrays are listed so that row k and row BT-1-k are negatives on the active rows
                assert (lost == lost[::-1]).all()
        assert (good == (A & ~union)).all()
        st['max_sum'] = max(st['max_sum'], Fr(int(sum_lost.max()), BT))
        st['max_union'] = max(st['max_union'], Fr(int(union.sum(axis=0).max()), BT))
        st['max_lost_all'] = max(st['max_lost_all'], Fr(int(union.sum()), BT * BY))
        bound = Fr(3, 4) * gamma_Y - LY * lam(p, a)
        assert share >= bound, ('rank >= 2: count below (3/4) gamma - L_Y lam', g.tolist(), q, share, bound)
        if a == 1:
            b2 = gamma_Y / 2 if inK.any() else gamma_Y - LY * Fr(2, 2 ** p)
            assert share >= b2, ("Lemma 3': count below its bound", g.tolist(), q, share, b2)
        st['rank2'] += 1; st['least2'] = min(st['least2'], share)

def gen(rng, T, Y, q, kind, wT, wY):
    p, a = T; r_, c_ = Y; nT, nY = p ** a, r_ ** c_
    hi = q if q else 4
    tk = rng.choice(['random', 'whole_groups', 'one_leaf_per_class', 'nested', 'one_class']) if a >= 2 else 'random'
    yk = rng.choice(['random', 'whole_groups', 'one_leaf_per_class', 'nested', 'one_class']) if c_ >= 2 else 'random'
    rows = make_support(rng, p, a, tk, wT) if a >= 2 else rng.permutation(nT)[:rng.integers(1, min(wT, nT) + 1)]
    cols = make_support(rng, r_, c_, yk, wY) if c_ >= 2 else rng.permutation(nY)[:rng.integers(1, min(wY, nY) + 1)]
    rows = rows[:wT]; cols = cols[:wY]
    g = np.zeros((nT, nY), dtype=np.int64)
    def vec(n_, mode=None):
        mode = rng.integers(0, 3) if mode is None else mode
        if mode == 0: return rng.integers(1, hi, size=n_)
        if mode == 1: return np.ones(n_, dtype=np.int64)
        return rng.choice([1, -1], size=n_)
    R, C = len(rows), len(cols)
    if kind == 'zero_one': blk = (rng.random((R, C)) < rng.choice([0.3, 0.6, 0.9])).astype(np.int64)
    elif kind == 'product': blk = np.outer(vec(R), vec(C))
    elif kind == 'full_block': blk = np.ones((R, C), dtype=np.int64)
    elif kind == 'rank2': blk = np.outer(vec(R), vec(C)) + np.outer(vec(R) * (rng.random(R) < 0.5), vec(C) * (rng.random(C) < 0.5))
    elif kind == 'block_plus':      # the example of section 6 (a full block, rank one) with one or two cells changed: rank two
        blk = np.ones((R, C), dtype=np.int64)
        for _ in range(rng.integers(1, 3)): blk[rng.integers(0, R), rng.integers(0, C)] += rng.integers(1, hi)
    elif kind == 'perm':
        blk = np.zeros((R, C), dtype=np.int64)
        for k in range(max(R, C)): blk[k % R, rng.integers(0, C) if R >= C else k % C] = 1
    elif kind == 'random_values': blk = rng.integers(0, hi, size=(R, C)) if q else rng.integers(-2, 3, size=(R, C))
    elif kind == 'two_blocks':
        blk = np.zeros((R, C), dtype=np.int64)
        r1 = rng.integers(1, R + 1); c1 = rng.integers(1, C + 1)
        blk[:r1, :c1] += 1; blk[R - rng.integers(1, R + 1):, C - rng.integers(1, C + 1):] += rng.integers(1, hi)
    g[np.ix_(rows, cols)] = blk
    return g % q if q else g

KINDS = ['zero_one', 'product', 'full_block', 'rank2', 'block_plus', 'perm', 'random_values', 'two_blocks']

CASES = {
    # name: (T, Y, fields, most active rows, most active columns)
    '25x3':  ((5, 2), (3, 1), [7, None], 9, 3),
    '25x9':  ((5, 2), (3, 2), [7, None], 8, 6),
    '49x9':  ((7, 2), (3, 2), [5], 8, 6),
    '25x7':  ((5, 2), (7, 1), [3], 8, 6),
    '9x5':   ((3, 2), (5, 1), [7, None], 9, 5),
    '5x9':   ((5, 1), (3, 2), [7, None], 5, 9),
    '9x3':   ((3, 2), (3, 1), [5], 9, 3),
    '9x9':   ((3, 2), (3, 2), [5], 9, 7),
    '27x5':  ((3, 3), (5, 1), [7], 9, 5),
    '7x27':  ((7, 1), (3, 3), [5], 7, 7),
    '27x25': ((3, 3), (5, 2), [7], 8, 6),
}

if __name__ == '__main__':
    case = sys.argv[1]; seed = int(sys.argv[2]); count = int(sys.argv[3])
    T, Y, fields, wT, wY = CASES[case]
    rng = np.random.default_rng(seed)
    p, a = T; r_, c_ = Y
    for q in fields:
        t0 = time.time()
        st = {'functions': 0, 'rank1': 0, 'rank2': 0, 'least': Fr(1), 'least1': Fr(1), 'least2': Fr(1), 'maxB': Fr(0), 'max_sum': Fr(0),
              'max_union': Fr(0), 'max_lost_all': Fr(0)}
        for kind in KINDS:
            for _ in range(count):
                g = gen(rng, T, Y, q, kind, wT, wY)
                if not g.any(): continue
                analyse(g, T, Y, q, st)
        b1 = single(p, a) * single(r_, c_); b2 = Fr(3, 4) * single(r_, c_) - (c_ + 1) * lam(p, a)
        print(f'box Z_{p**a} x Z_{r_**c_} (T = Z_{p**a} the new coordinate, L_Y = {c_ + 1}), field {"Q" if q is None else "F_%d" % q}: {st["functions"]} functions '
              f'(rank one {st["rank1"]}, rank >= 2 {st["rank2"]}); no exception. Least share of good patterns: rank one {st["least1"]} (proved {b1}); '
              f'rank >= 2 {st["least2"] if st["rank2"] else "-"} (proved {b2 if b2 > 0 else "nothing: " + str(b2)}). '
              f'Largest |B(x)| share over all (sigma, level of Y): {st["maxB"]} (Lemma T: {lam(p, a)}); per sigma, largest sum over the levels of Y of the lost shares {st["max_sum"]}, '
              f'largest union {st["max_union"]} (L_Y 2^(1-p) = {(c_ + 1) * Fr(2, 2 ** p)}); largest share of pairs lost in all {st["max_lost_all"]}  [{time.time() - t0:.0f} s]', flush=True)
