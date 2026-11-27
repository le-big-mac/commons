"""Referee, third pass: Lemma 3T with Y a box of two trees (the second step of the induction of Proposition 5).
X = T x Y1 x Y2, T = Z_{p^a} the new coordinate, Y = Y1 x Y2 with L_Y = (c1 + 1)(c2 + 1) levels.
Functions with few active rows of T (the signs on the other rows do not matter); every sign vector on the active rows
and every pattern of Y.  Checks as in tree3T_own.py: rank one factorises; for rank >= 2, for every (sigma_Y, level P' of Y)
the set B(x) has share <= lam(p, a); the count against min(single(T) gamma, (3/4) gamma - L_Y lam(p, a)), gamma = the
proved value for Y.
usage: tree3trees_own.py CASE SEED COUNT
"""
import sys, time
import numpy as np
from fractions import Fraction as Fr
from itertools import product
from treetools import level_matrix, all_signs
from treeTS_own import lam, single, make_support
from tree3T_own import rank_mod, rank_Q, nonzero

CASES = {
    # name: (T, Y1, Y2, field, gamma proved for Y, most active rows)
    '49x3x5': ((7, 2), (3, 1), (5, 1), 11, Fr(1, 4), 7),      # gamma: Theorem P on 3 x 5
    '25x3x7': ((5, 2), (3, 1), (7, 1), 11, Fr(1, 4), 6),
    '49x3x5Q': ((7, 2), (3, 1), (5, 1), None, Fr(1, 4), 6),
}

def run(case, seed, count):
    T, Y1, Y2, q, gammaY, wT = CASES[case]
    p, a = T; n1 = Y1[0] ** Y1[1]; n2 = Y2[0] ** Y2[1]; nT = p ** a
    rng = np.random.default_rng(seed)
    M1 = [level_matrix(*Y1, j) for j in range(Y1[1] + 1)]; M2 = [level_matrix(*Y2, l) for l in range(Y2[1] + 1)]
    S1 = all_signs(n1); S2 = all_signs(n2)
    W1 = [S1[:, None, :] * M1[j][None] for j in range(len(M1))]; W2 = [S2[:, None, :] * M2[l][None] for l in range(len(M2))]
    LY = len(M1) * len(M2); lamT = lam(p, a)
    b1 = single(p, a) * gammaY; b2 = Fr(3, 4) * gammaY - LY * lamT
    st = dict(n=0, r1=0, r2=0, least1=Fr(1), least2=Fr(1), maxB=Fr(0), max_all=Fr(0)); t0 = time.time()
    hi = q if q else 4
    kinds = ['zero_one', 'product', 'rank2', 'block_plus', 'random_values']
    for kind in kinds:
        for _ in range(count):
            rows = make_support(rng, p, a, rng.choice(['random', 'whole_groups', 'one_leaf_per_class', 'nested']), wT)[:wT] if a >= 2 \
                else rng.permutation(nT)[:rng.integers(1, min(wT, nT) + 1)]
            w = len(rows)
            def rv(shape): return rng.integers(1, hi, size=shape)
            if kind == 'zero_one': blk = (rng.random((w, n1, n2)) < rng.choice([0.2, 0.5])).astype(np.int64)
            elif kind == 'product': blk = rv(w)[:, None, None] * ((rng.random(n1) < 0.7) * rv(n1))[None, :, None] * ((rng.random(n2) < 0.6) * rv(n2))[None, None, :]
            elif kind == 'rank2':
                blk = rv(w)[:, None, None] * (rng.random((n1, n2)) < 0.5)[None] + (rv(w) * (rng.random(w) < 0.6))[:, None, None] * ((rng.random((n1, n2)) < 0.4) * rv((n1, n2)))[None]
            elif kind == 'block_plus':
                h = (rng.random((n1, n2)) < 0.6).astype(np.int64); blk = np.ones(w, dtype=np.int64)[:, None, None] * h[None]
                blk = blk.copy(); blk[rng.integers(0, w), rng.integers(0, n1), rng.integers(0, n2)] += 1
            else: blk = rng.integers(0, hi, size=(w, n1, n2)) * (rng.random((w, n1, n2)) < 0.5)
            blk = np.asarray(blk, dtype=np.int64)
            if q: blk = blk % q
            keep = nonzero(blk, q).reshape(w, -1).any(axis=1)
            rows = rows[keep]; blk = blk[keep]; w = len(rows)
            if w == 0: continue
            ST = all_signs(w); BT = ST.shape[0]
            MT = [level_matrix(p, a, i)[:, rows] for i in range(a + 1)]          # only the active rows matter
            nz = {}
            for i in range(a + 1):
                P = np.tensordot(MT[i][None] * ST[:, None, :], blk, axes=([2], [0]))            # (BT, rows_i, n1, n2)
                for j in range(len(M1)):
                    Q1 = np.tensordot(P, W1[j], axes=([2], [2]))                                # (BT, rows_i, n2, B1, rows_j)
                    for l in range(len(M2)):
                        R = np.tensordot(Q1, W2[l], axes=([2], [2]))                            # (BT, rows_i, B1, rows_j, B2, rows_l)
                        nz[i, j, l] = nonzero(R, q).any(axis=(1, 3, 5)).reshape(BT, -1)          # (BT, B1*B2)
            BY = S1.shape[0] * S2.shape[0]
            good = np.ones((BT, BY), dtype=bool)
            for v in nz.values(): good &= v
            share = Fr(int(good.sum()), BT * BY)
            flat = blk.reshape(w, -1)
            rk = rank_mod(flat, q) if q else rank_Q(flat)
            st['n'] += 1
            A = np.ones((BT, BY), dtype=bool)
            for j in range(len(M1)):
                for l in range(len(M2)): A &= nz[0, j, l]
            if rk == 1:
                v0 = 0; y0 = int(np.argmax(nonzero(flat[0], q)))
                cvec = flat[:, y0]; h = blk[0]
                gT = np.ones(BT, dtype=bool)
                for i in range(a + 1): gT &= nonzero((ST * cvec[None, :]) @ MT[i].T, q).any(axis=1)
                gY = np.ones(BY, dtype=bool)
                for j in range(len(M1)):
                    for l in range(len(M2)):
                        R = np.tensordot(np.tensordot(h, W1[j], axes=([0], [2])), W2[l], axes=([0], [2]))   # (B1, rows_j, B2, rows_l)
                        gY &= nonzero(R, q).any(axis=(1, 3)).reshape(-1)
                assert (good == (gT[:, None] & gY[None, :])).all(), ('rank one: factorisation fails', blk.tolist())
                assert share >= b1
                st['r1'] += 1; st['least1'] = min(st['least1'], share)
            else:
                union = np.zeros((BT, BY), dtype=bool)
                for j in range(len(M1)):
                    for l in range(len(M2)):
                        deg = np.zeros((BT, BY), dtype=bool)
                        for i in range(1, a + 1): deg |= ~nz[i, j, l]
                        Bx = nz[0, j, l] & deg
                        mx = int(Bx.sum(axis=0).max())
                        assert mx <= lamT * BT, ('Lemma T fails inside Lemma 3T', blk.tolist(), mx, BT)
                        st['maxB'] = max(st['maxB'], Fr(mx, BT))
                        union |= A & deg
                assert (good == (A & ~union)).all()
                assert share >= b2, ('count below (3/4) gamma - L_Y lam', share, b2)
                st['max_all'] = max(st['max_all'], Fr(int(union.sum()), BT * BY))
                st['r2'] += 1; st['least2'] = min(st['least2'], share)
    print(f'box Z_{nT} x Z_{n1} x Z_{n2} (T = Z_{nT} new, Y = Z_{n1} x Z_{n2}, L_Y = {LY}), field {"Q" if q is None else "F_%d" % q}: {st["n"]} functions '
          f'(rank one {st["r1"]}, rank >= 2 {st["r2"]}); no exception. Least share of good patterns: rank one {st["least1"]} (proved {b1}); rank >= 2 {st["least2"]} '
          f'(proved {b2 if b2 > 0 else "nothing: " + str(b2)}); largest |B(x)| share {st["maxB"]} (Lemma T: {lamT}); largest share of pairs lost in all {st["max_all"]}  [{time.time() - t0:.0f} s]')

if __name__ == '__main__':
    run(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
