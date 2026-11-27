"""Referee's test of the inner statements of the proof of Lemma 3 (sign-general-result.md, section 3), from the text.

X = X_1 x Y, p = |X_1|; a pattern is (s, sigma_Y); slices g_v; u_t = sum_v t_v g_v; K = {t : u_t = 0}.
For every function tried and EVERY pair (s, sigma_Y) (all 2^p sign vectors, all patterns of Y):
  (A) "(s, sigma_Y) g is L-good"  <=>  (i) and (ii)                                   [Lemma 1 as used]
  (B) Lost = (i) and not (ii).  If K != 0: every lost pair has s in K-perp.
  (C) the Claim: for a lost pair with (ii) failing at P', with b = class of s_0 sigma_Y g_0 modulo the functions
      degenerate at P':  b != 0, and sigma_Y u_t - <s,t> s_0 sigma_Y g_0 is degenerate at P' for random t.
  (D) for each (sigma_Y, P'): at most two sign vectors s are lost with (ii) failing at P', and they are s, -s.
  (E) counts: sign vectors outside K u K-perp >= 2^(p-1) when 0 != K (Lemma 2(d));
      for s not in K the number of sigma_Y with (i) is >= gamma |Sigma_Y| (gamma = the bound known for Y, given);
      good pairs >= (gamma/2)|Sigma_X| if K != 0, and >= (gamma - |L_1| 2^(1-p)) |Sigma_X| if K = 0.
Fields: F_q (exact linear algebra modulo q) and Q (fractions).
usage: lemma3_own.py CASE SEED COUNT
"""
import sys, time
import numpy as np
from fractions import Fraction as Fr
from itertools import product, combinations
from boxtools import all_levels, pattern_array, good_batch, good_at

def nullspace_mod(M, q):
    """basis of {t : M t = 0} over F_q; M integer array (rows x cols)."""
    M = [[int(x) % q for x in row] for row in M]
    rows, cols = len(M), len(M[0]); piv = []; r = 0
    for c in range(cols):
        pr = next((i for i in range(r, rows) if M[i][c]), None)
        if pr is None: continue
        M[r], M[pr] = M[pr], M[r]
        inv = pow(M[r][c], -1, q); M[r] = [x * inv % q for x in M[r]]
        for i in range(rows):
            if i != r and M[i][c]:
                f = M[i][c]; M[i] = [(x - f * y) % q for x, y in zip(M[i], M[r])]
        piv.append(c); r += 1
        if r == rows: break
    free = [c for c in range(cols) if c not in piv]; basis = []
    for fc in free:
        v = [0] * cols; v[fc] = 1
        for i, pc in enumerate(piv): v[pc] = (-M[i][fc]) % q
        basis.append(v)
    return basis

def nullspace_Q(M):
    M = [[Fr(int(x)) for x in row] for row in M]
    rows, cols = len(M), len(M[0]); piv = []; r = 0
    for c in range(cols):
        pr = next((i for i in range(r, rows) if M[i][c] != 0), None)
        if pr is None: continue
        M[r], M[pr] = M[pr], M[r]
        inv = 1 / M[r][c]; M[r] = [x * inv for x in M[r]]
        for i in range(rows):
            if i != r and M[i][c] != 0:
                f = M[i][c]; M[i] = [x - f * y for x, y in zip(M[i], M[r])]
        piv.append(c); r += 1
        if r == rows: break
    free = [c for c in range(cols) if c not in piv]; basis = []
    for fc in free:
        v = [Fr(0)] * cols; v[fc] = Fr(1)
        for i, pc in enumerate(piv): v[pc] = -M[i][fc]
        # clear denominators
        den = 1
        for x in v: den = den * x.denominator // np.gcd(den, x.denominator)
        basis.append([int(x * den) for x in v])
    return basis

def is_zero(x, q):
    return (x == 0) if q is None else (x % q == 0)

def check_function(g, fam, q, gamma, rng, stats):
    """g: array (p, *Ysides); fam: list of levels of X (tuples of axes, axis 0 is the one split off)."""
    p = g.shape[0]; Ys = g.shape[1:]; kY = len(Ys)
    L0 = [tuple(i - 1 for i in P) for P in fam if 0 not in P]
    L1 = [tuple(i - 1 for i in P if i != 0) for P in fam if 0 in P]
    assert set(L1) <= set(L0), 'L_1 is not inside L_0: the family is not subset-closed'
    if kY:
        PAY, _ = pattern_array(Ys, normalized=False)
    else:
        PAY = np.ones((1,), dtype=np.int8)
    PAY = PAY.astype(np.int64); nY = PAY.shape[0]
    S = np.array(list(product((1, -1), repeat=p)), dtype=np.int64)
    # K
    M = g.reshape(p, -1).T
    Kb = nullspace_mod(M, q) if q else nullspace_Q(M)
    Kb = np.array(Kb, dtype=object).reshape(len(Kb), p)
    def inK(s):
        return all(is_zero(int(x), q) for x in (M.astype(object) @ np.array(s, dtype=object)))
    def inKperp(s):
        return all(is_zero(int(sum(int(a) * int(b) for a, b in zip(s, kap))), q) for kap in Kb)
    outside = sum(1 for s in S if not inK(s) and not inKperp(s))
    if len(Kb) > 0:
        assert outside >= 2 ** (p - 1), ('Lemma 2(d) fails', g, q)
        stats['min_outside'] = min(stats.get('min_outside', 1), Fr(outside, 2 ** p))
    lost_by = {}          # (index of sigma_Y, P') -> list of s
    n_good = 0; n_A = 0; n_lost = 0
    for s in S:
        H = s.reshape((1, p) + (1,) * kY) * PAY.reshape((nY, 1) + Ys) * g[None]
        good = good_batch(H, fam, q)
        us = np.tensordot(s, g, axes=(0, 0))                 # u_s on Y
        cond_i = good_batch(PAY.reshape((nY,) + Ys) * us[None], L0, q)
        fails = {}
        cond_ii = np.ones(nY, dtype=bool)
        for P in L1:
            allcong = np.ones(nY, dtype=bool)
            # literally: for all v, v' the difference of the slices s_v sigma_Y g_v is degenerate at P'
            for v, w in combinations(range(p), 2):
                diff = PAY.reshape((nY,) + Ys) * (s[v] * g[v] - s[w] * g[w])[None]
                allcong &= ~good_at(diff, P, q)
            fails[P] = allcong
            cond_ii &= ~allcong
        assert (good == (cond_i & cond_ii)).all(), ('(A) fails', g, s, q)
        sinK = inK(s)
        if not sinK:
            assert cond_i.sum() >= gamma * nY, ('hypothesis gamma fails for Y', us, q, cond_i.sum(), nY)
        else:
            assert not cond_i.any()                          # u_s = 0 is good at no level (the level 0 = empty set)
        lost = cond_i & ~cond_ii
        n_good += int(good.sum()); n_A += int(cond_i.sum()); n_lost += int(lost.sum())
        if lost.any():
            if len(Kb) > 0:
                assert inKperp(s), ('(B) fails: lost pair with s outside K-perp', g, s, q)
            for P in L1:
                for iy in np.nonzero(cond_i & fails[P])[0]:
                    lost_by.setdefault((int(iy), P), []).append(tuple(int(x) for x in s))
                    # (C) the Claim
                    sy = PAY.reshape((nY,) + Ys)[iy]
                    b = s[0] * sy * g[0]
                    assert good_at(b[None], P, q)[0], ('(C) fails: b = 0', g, s, q)
                    for _ in range(2):
                        t = rng.integers(0, q if q else 7, size=p).astype(np.int64)
                        ut = np.tensordot(t, g, axes=(0, 0))
                        st = int((s * t).sum())
                        assert not good_at((sy * ut - st * b)[None], P, q)[0], ('(C) fails', g, s, t, q)
                    stats['claim'] = stats.get('claim', 0) + 1
    # (D)
    for key, lst in lost_by.items():
        assert len(lst) <= 2, ('(D) fails: more than two lost sign vectors', g, key, lst, q)
        if len(lst) == 2:
            assert tuple(-x for x in lst[0]) == lst[1], ('(D) fails: not s, -s', lst)
    nX = nY * 2 ** p
    assert n_lost <= 2 * len(L1) * nY
    if len(Kb) > 0:
        bound = Fr(gamma) / 2
        stats['K!=0'] = stats.get('K!=0', 0) + 1
        stats['min_K!=0'] = min(stats.get('min_K!=0', 1), Fr(n_good, nX))
    else:
        bound = Fr(gamma) - Fr(len(L1) * 2, 2 ** p)
        stats['K=0'] = stats.get('K=0', 0) + 1
        stats['min_K=0'] = min(stats.get('min_K=0', 1), Fr(n_good, nX))
        stats['bound_K=0'] = bound
    assert Fr(n_good, nX) >= bound, ('(E) fails: count below the bound of the case', g, q, n_good, nX, bound)
    stats['functions'] = stats.get('functions', 0) + 1
    stats['lost_pairs'] = stats.get('lost_pairs', 0) + n_lost
    if n_lost:
        stats['with_lost'] = stats.get('with_lost', 0) + 1
        stats['max_lost_share'] = max(stats.get('max_lost_share', 0), Fr(n_lost, 2 * len(L1) * nY))
    stats['min_all'] = min(stats.get('min_all', 1), Fr(n_good, nX))

def gen(rng, sides, q, kind, fam):
    p = sides[0]; Ys = sides[1:]; nYc = int(np.prod(Ys)) if Ys else 1
    hi = q if q else 5
    def rv(shape):
        return rng.integers(0, hi, size=shape) if q else rng.integers(-3, 4, size=shape)
    s0 = rng.choice([1, -1], size=p)
    col = lambda a: a.reshape((p,) + (1,) * len(Ys))
    if kind == 'random': g = rv(sides)
    elif kind == 'zero_one': g = (rng.random(sides) < rng.choice([0.2, 0.4, 0.7])).astype(np.int64)
    elif kind == 'sparse': g = rv(sides) * (rng.random(sides) < 0.2)
    elif kind == 'rank1_sign': g = col(s0) * rv(Ys)[None]                      # K = s0-perp, K-perp = F s0
    elif kind == 'rank1': g = col(rv(p)) * rv(Ys)[None]
    elif kind == 'rank2': g = col(rv(p)) * rv(Ys)[None] + col(rv(p)) * rv(Ys)[None]
    elif kind == 'kernel_sign':                                               # sum_v s0_v g_v = 0: K contains s0
        g = rv(sides); g[0] = -s0[0] * np.tensordot(s0[1:], g[1:], axes=(0, 0))
    elif kind == 'cong':        # slices equal up to sign modulo functions degenerate at a level of L_1: lost pairs
        L1 = [tuple(i - 1 for i in P if i != 0) for P in fam if 0 in P]
        P = L1[rng.integers(0, len(L1))]
        u = rv(Ys); g = np.zeros(sides, dtype=np.int64)
        sy = np.ones(Ys, dtype=np.int64)
        for j, n in enumerate(Ys):                                            # a random pattern of Y
            sh = [1] * len(Ys); sh[j] = n; sy = sy * rng.choice([1, -1], size=n).reshape(sh)
        for v in range(p):
            d = np.zeros(Ys, dtype=np.int64)
            if len(P) == 0:
                d = rv(Ys); flat = d.reshape(-1); flat[0] -= flat.sum()       # total 0
            else:
                for j in P:                                                   # functions not depending on coordinate j
                    sh = list(Ys); sh[j] = 1; d = d + rv(sh)
                # plus anything whose marginal on P vanishes
                outside = [j for j in range(len(Ys)) if j not in P]
                if outside:
                    e = rv(Ys); e = e - np.take(e, [0], axis=outside[0]) * 0
                    j0 = outside[0]
                    idx0 = [slice(None)] * len(Ys); idx0[j0] = 0
                    e[tuple(idx0)] -= e.sum(axis=j0)                          # sums to 0 along axis j0
                    d = d + e
            g[v] = sy * (s0[v] * u + d)
    g = np.asarray(g, dtype=np.int64)
    return g % q if q else g

KINDS = ['random', 'zero_one', 'sparse', 'rank1_sign', 'rank1', 'rank2', 'kernel_sign', 'cong']

def tree_levels(labels):
    """labels: list of primes, one per axis; levels with at most one axis per prime."""
    k = len(labels)
    return [P for P in all_levels(k) if len({labels[i] for i in P}) == len(P)]

CASES = {
    # name: (sides with the split coordinate first, family, fields, gamma for Y with L_0)
    '5x3':   ((5, 3), 'all', [None, 7, 11], Fr(1, 2)),
    '5x5':   ((5, 5), 'all', [None, 3, 7], Fr(1, 2)),
    '3x5':   ((3, 5), 'all', [None, 7], Fr(1, 2)),
    '7x5':   ((7, 5), 'all', [3, 11], Fr(1, 2)),
    '5x7':   ((5, 7), 'all', [3], Fr(1, 2)),
    '7x3x5': ((7, 3, 5), 'all', [None, 11], Fr(1, 4)),                 # the step k = 3 of Theorem P
    '5x3x3t': ((5, 3, 3), ('tree', [5, 3, 3]), [None, 7], Fr(1, 4)),    # digits of 45, split off the 5: gamma = c(9) = 1/4
    '3x3x5t': ((3, 3, 5), ('tree', [3, 3, 5]), [None, 7], Fr(1, 4)),    # digits of 45, split off a 3: Y = 3x5, all levels
    '5x3x5odd': ((5, 3, 5), ('list', [(), (0,), (1,), (2,), (0, 1)]), [7], Fr(1, 4)),   # another subset-closed family
}

if __name__ == '__main__':
    case = sys.argv[1]; seed = int(sys.argv[2]); count = int(sys.argv[3])
    sides, famspec, fields, gamma = CASES[case]
    k = len(sides)
    if famspec == 'all': fam = all_levels(k)
    elif famspec[0] == 'tree': fam = tree_levels(famspec[1])
    else: fam = [tuple(P) for P in famspec[1]]
    rng = np.random.default_rng(seed)
    L1n = sum(1 for P in fam if 0 in P)
    for q in fields:
        t0 = time.time(); stats = {}
        for kind in KINDS:
            for _ in range(count):
                g = gen(rng, sides, q, kind, fam)
                if not g.any(): continue
                check_function(g, fam, q, gamma, rng, stats)
        print(f'case {case}: sides {sides} (first split off), family {famspec if famspec == "all" else famspec[0]} ({len(fam)} levels, |L_1| = {L1n}), '
              f'field {"Q" if q is None else "F_%d" % q}, gamma = {gamma}: {stats.get("functions", 0)} functions, every pair (s, sigma_Y) tested; '
              f'(A)-(E) hold. K != 0: {stats.get("K!=0", 0)} functions, least share good {stats.get("min_K!=0", "-")} (bound {gamma / 2}), '
              f'least share of sign vectors outside K u K-perp {stats.get("min_outside", "-")}; '
              f'K = 0: {stats.get("K=0", 0)} functions, least share good {stats.get("min_K=0", "-")} (bound {stats.get("bound_K=0", "-")}); '
              f'functions with lost pairs {stats.get("with_lost", 0)}, lost pairs {stats.get("lost_pairs", 0)}, Claim tested on {stats.get("claim", 0)}, '
              f'largest |Lost| / (2 |L_1| |Sigma_Y|) = {stats.get("max_lost_share", 0)}  [{time.time() - t0:.0f} s]', flush=True)
