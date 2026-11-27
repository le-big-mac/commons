"""Referee, third pass: Lemma T and Lemma S of sign-all-result.md on single trees, from the text.

  B(x) = { s : (sx)(T) != 0 and sx flat at some level i in 1..a };   Lemma T: |B(x)| <= lam(p, a) 2^(p^a).
  Lemma S: for scalar c != 0 over Q or F_q (q odd, q != p) at least single(p, a) 2^(p^a) sign vectors make sc good.

parts:  exh9         Z_9: every nonzero function with values in {-2..2}, over Q and over F_5 (that is every function Z_9 -> F_5),
                     all 512 sign vectors; and every function Z_9 -> F_3 (q = p: Lemma T allows it, Lemma S does not)
        samp SEED    Z_27, Z_25, Z_49, Z_81: functions with at most 13 active leaves, all sign vectors on the active leaves
        vec SEED     Lemma T for vector-valued x (dimension 2, 3) on Z_9, Z_27, Z_25; and an ascent on the lost share on Z_9
"""
import sys, time
import numpy as np
from fractions import Fraction as Fr
from itertools import product
from treetools import level_matrix, flat_at, all_signs

def lam(p, a): return sum(Fr(1, 2 ** ((p - 1) * l)) for l in range(1, a + 1))
def single(p, a): return Fr(1, 2) if (a == 1 or p >= 5) else Fr(5, 8) - lam(3, a)

def part_exh9():
    p, a = 3, 2; n = 9
    S = all_signs(n).astype(np.int16)
    M1 = level_matrix(3, 2, 1).astype(np.int16); M2 = level_matrix(3, 2, 2).astype(np.int16)
    tail = np.array(list(product(range(-2, 3), repeat=5)), dtype=np.int16)
    fields = [None, 5]
    least = {q: 512 for q in fields}; most_lost = {q: 0 for q in fields}; nmin = {q: 0 for q in fields}; nfun = 0
    lost_by_level = {q: [0, 0] for q in fields}
    t0 = time.time()
    for head in product(range(-2, 3), repeat=4):
        C = np.concatenate([np.tile(np.array(head, dtype=np.int16), (tail.shape[0], 1)), tail], axis=1)
        C = C[C.any(axis=1)]
        H = C[:, None, :] * S[None, :, :]
        tot = H.sum(axis=2); T1 = H @ M1.T; T2 = H @ M2.T
        nfun += C.shape[0]
        for q in fields:
            if q is None:
                nz = tot != 0; f1 = ~(T1 != 0).any(axis=2); f2 = ~(T2 != 0).any(axis=2)
            else:
                nz = tot % q != 0; f1 = ~(T1 % q != 0).any(axis=2); f2 = ~(T2 % q != 0).any(axis=2)
            good = (nz & ~f1 & ~f2).sum(axis=1); lost = (nz & (f1 | f2)).sum(axis=1)
            mn = int(good.min())
            if mn < least[q]: least[q] = mn; nmin[q] = 0
            if mn == least[q]: nmin[q] += int((good == mn).sum())
            most_lost[q] = max(most_lost[q], int(lost.max()))
            lost_by_level[q][0] = max(lost_by_level[q][0], int((nz & f1).sum(axis=1).max()))
            lost_by_level[q][1] = max(lost_by_level[q][1], int((nz & f2).sum(axis=1).max()))
    for q in fields:
        print(f'Z_9, every nonzero function with values in -2..2 ({nfun}), field {"Q" if q is None else "F_5 (every nonzero function into F_5)"}: '
              f'least share of good sign vectors {Fr(least[q], 512)} (Lemma S: {single(3, 2)}), attained by {nmin[q]} functions; '
              f'largest lost share |B|/512 = {Fr(most_lost[q], 512)} (Lemma T: {lam(3, 2)}); largest share lost at level 1: {Fr(lost_by_level[q][0], 512)}, at level 2: {Fr(lost_by_level[q][1], 512)}')
    # F_3: q = p
    C = np.array(list(product(range(-1, 2), repeat=9)), dtype=np.int16); C = C[C.any(axis=1)]
    H = C[:, None, :] * S[None, :, :]
    tot = H.sum(axis=2); T1 = H @ M1.T; T2 = H @ M2.T
    nz = tot % 3 != 0; f1 = ~(T1 % 3 != 0).any(axis=2); f2 = ~(T2 % 3 != 0).any(axis=2)
    good = (nz & ~f1 & ~f2).sum(axis=1); lost = (nz & (f1 | f2)).sum(axis=1)
    print(f'Z_9, every nonzero function into F_3 ({C.shape[0]}; q = p, outside Lemma S, inside Lemma T): largest lost share {Fr(int(lost.max()), 512)} '
          f'(Lemma T: {lam(3, 2)}); least share of good sign vectors {Fr(int(good.min()), 512)} (for information)')
    print(f'   [{time.time() - t0:.0f} s]')

def make_support(rng, p, a, kind, wmax):
    n = p ** a
    if kind == 'random':
        w = rng.integers(1, wmax + 1); return rng.permutation(n)[:w]
    if kind == 'one_class':                       # inside one class at depth 1 (or deeper)
        d = rng.integers(1, a); c = rng.integers(0, p ** d)
        leaves = np.nonzero(np.arange(n) % p ** d == c)[0]
        w = rng.integers(1, min(wmax, len(leaves)) + 1); return rng.permutation(leaves)[:w]
    if kind == 'whole_groups':                    # whole groups of leaves (classes modulo p^(a-1))
        ng = rng.integers(1, max(1, wmax // p) + 1)
        gs = rng.permutation(p ** (a - 1))[:ng]
        return np.concatenate([np.nonzero(np.arange(n) % p ** (a - 1) == g)[0] for g in gs])
    if kind == 'one_leaf_per_class':              # one leaf in each subclass of a group at a random level, possibly several groups
        i = rng.integers(1, a + 1); res = []
        for _ in range(rng.integers(1, max(1, wmax // p) + 1)):
            g = rng.integers(0, p ** (i - 1))
            for t in range(p):
                cls = np.nonzero(np.arange(n) % p ** i == g + t * p ** (i - 1))[0]
                res.append(rng.choice(cls))
        return np.unique(np.array(res))
    if kind == 'nested':                          # a full group at every level along one path: p leaves, then one leaf in each sibling class above
        v0 = rng.integers(0, n); res = [v0]
        for i in range(a, 0, -1):
            g = v0 % p ** (i - 1)
            for t in range(p):
                c = g + t * p ** (i - 1)
                if v0 % p ** i == c: continue
                cls = np.nonzero(np.arange(n) % p ** i == c)[0]
                res.append(rng.choice(cls))
        res = np.unique(np.array(res))
        return res[:wmax] if len(res) > wmax else res

KINDS = ['random', 'one_class', 'whole_groups', 'one_leaf_per_class', 'nested']

def tree_counts(x, p, a, q):
    """x: (n,) or (n, d) integer.  Returns (number of sign vectors on the active leaves, good, lost, lost per level)."""
    n = p ** a
    act = np.nonzero(x.reshape(n, -1).any(axis=1))[0]
    w = len(act); Sg = all_signs(w)
    full = np.ones((Sg.shape[0], n), dtype=np.int64); full[:, act] = Sg
    H = full[:, :, None] * x.reshape(n, -1)[None]                 # (B, n, d)
    tot_nz = ~flat_at(H, p, a, 0, q)
    fl = [flat_at(H, p, a, i, q) for i in range(1, a + 1)]
    anyflat = np.zeros(Sg.shape[0], dtype=bool)
    for f in fl: anyflat |= f
    return Sg.shape[0], int((tot_nz & ~anyflat).sum()), int((tot_nz & anyflat).sum()), [int((tot_nz & f).sum()) for f in fl]

def part_samp(seed):
    rng = np.random.default_rng(seed)
    for (p, a, fields, wmax, cnt) in [(3, 3, [5, 7, None], 13, 500), (5, 2, [3, 7, None], 13, 500), (7, 2, [3, 5], 14, 300), (3, 4, [5], 13, 300)]:
        n = p ** a
        for q in fields:
            t0 = time.time(); least = Fr(1); most = Fr(0); nf = 0; most_level = [Fr(0)] * a
            for kind in KINDS:
                for _ in range(cnt):
                    sup = make_support(rng, p, a, kind, wmax)
                    c = np.zeros(n, dtype=np.int64)
                    mode = rng.integers(0, 3)
                    if mode == 0: vals = rng.integers(1, q if q else 4, size=len(sup))
                    elif mode == 1: vals = np.ones(len(sup), dtype=np.int64)
                    else: vals = rng.choice([1, -1], size=len(sup))
                    c[sup] = vals
                    if q: c = c % q
                    if not c.any(): continue
                    tot, good, lost, per = tree_counts(c, p, a, q)
                    nf += 1
                    least = min(least, Fr(good, tot)); most = max(most, Fr(lost, tot))
                    most_level = [max(m, Fr(x, tot)) for m, x in zip(most_level, per)]
                    assert Fr(good, tot) >= single(p, a), ('Lemma S fails', p, a, q, c.tolist())
                    assert Fr(lost, tot) <= lam(p, a), ('Lemma T fails', p, a, q, c.tolist())
            print(f'Z_{n} (p = {p}, a = {a}), field {"Q" if q is None else "F_%d" % q}, {nf} functions with at most {wmax} active leaves: least share good {least} '
                  f'(Lemma S: {single(p, a)}); largest lost share {most} (Lemma T: {lam(p, a)}; 2^(1-p) = {Fr(2, 2 ** p)}); largest share lost level by level: {[str(m) for m in most_level]}  [{time.time() - t0:.0f} s]', flush=True)

def part_vec(seed):
    rng = np.random.default_rng(seed)
    for (p, a, q, d, wmax, cnt) in [(3, 2, 5, 2, 9, 400), (3, 2, 3, 2, 9, 400), (3, 2, 7, 3, 9, 300), (3, 3, 5, 2, 12, 250), (3, 3, 7, 3, 12, 200), (5, 2, 3, 2, 12, 250), (5, 2, 7, 2, 12, 250)]:
        n = p ** a; t0 = time.time(); most = Fr(0); nf = 0; most_level = [Fr(0)] * a
        for kind in KINDS:
            for _ in range(cnt):
                sup = make_support(rng, p, a, kind, wmax)
                x = np.zeros((n, d), dtype=np.int64)
                mode = rng.integers(0, 5)
                b = rng.integers(0, q, size=d)
                if not b.any(): b[0] = 1
                if mode == 0: x[sup] = rng.integers(0, q, size=(len(sup), d))
                elif mode == 1: x[sup] = b
                elif mode == 2: x[sup] = rng.choice([1, -1], size=(len(sup), 1)) * b
                elif mode == 3: x[sup] = rng.integers(1, q, size=(len(sup), 1)) * b
                else:
                    b2 = rng.integers(0, q, size=d); x[sup] = np.where(rng.random((len(sup), 1)) < 0.5, b, b2)
                x = x % q
                if not x.any(): continue
                tot, good, lost, per = tree_counts(x, p, a, q)
                nf += 1; most = max(most, Fr(lost, tot)); most_level = [max(m, Fr(y, tot)) for m, y in zip(most_level, per)]
                assert Fr(lost, tot) <= lam(p, a), ('Lemma T fails', p, a, q, x.tolist())
        print(f'Lemma T, x : Z_{n} -> F_{q}^{d}, {nf} functions: largest lost share {most} (bound {lam(p, a)}; 2^(1-p) = {Fr(2, 2 ** p)}); level by level {[str(m) for m in most_level]}  [{time.time() - t0:.0f} s]', flush=True)
    # ascent on the lost share, Z_9
    for (q, d) in [(5, 1), (7, 1), (5, 2), (3, 2), (None, 1)]:
        best = Fr(0); bestx = None
        for r in range(40):
            hi = q if q else 5
            x = rng.integers(0, hi, size=(9, d)) if q else rng.integers(-2, 3, size=(9, d))
            if not x.any(): x[0, 0] = 1
            tc0 = tree_counts(x, 3, 2, q); cur = Fr(tc0[2], tc0[0])
            for _ in range(250):
                y = x.copy(); y[rng.integers(0, 9)] = rng.integers(0, hi, size=d) if q else rng.integers(-2, 3, size=d)
                if not (y % q if q else y).any(): continue
                if q: y = y % q
                tc = tree_counts(y, 3, 2, q); val = Fr(tc[2], tc[0])
                if val >= cur: x, cur = y, val
            if cur > best or bestx is None: best, bestx = max(best, cur), x.copy()
        assert best <= lam(3, 2)
        print(f'ascent on the lost share, x : Z_9 -> {"Q" if q is None else "F_%d" % q}^{d}, 40 starts of 250 steps: largest reached {best} (bound {lam(3, 2)}); at x = {bestx.tolist()}')

if __name__ == '__main__':
    if sys.argv[1] == 'exh9': part_exh9()
    elif sys.argv[1] == 'samp': part_samp(int(sys.argv[2]))
    elif sys.argv[1] == 'vec': part_vec(int(sys.argv[2]))
