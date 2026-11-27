# rfast.py -- the same exact test "Phi_d divides the signed mask" for all 2^m signings, organised for more elements
# (m up to 24) and larger groups: the remainder modulo Phi_d is computed one coordinate at a time for all signings by
# doubling (s -> (s + g, s - g)); after two coordinates the signings still in question are verified row by row on
# all phi(d) coordinates.  Exact (whole numbers).  Signing number r has the sign -1 at element j iff bit j of r is set
# (the same convention as rlib.signs).
import numpy as np
from rlib import cyclo, divisors

_pt = {}


def ptable(d):
    """P[x] = coefficients of X^x modulo Phi_d, x = 0..d-1 (X^d = 1 modulo Phi_d).  int32."""
    if d not in _pt:
        phi = np.array(cyclo(d)[:-1], dtype=np.int64)
        k = len(phi)
        P = np.zeros((d, k), dtype=np.int64)
        cur = np.zeros(k, dtype=np.int64)
        cur[0] = 1
        for x in range(d):
            P[x] = cur
            top = cur[-1]
            nxt = np.empty(k, dtype=np.int64)
            nxt[0] = 0
            nxt[1:] = cur[:-1]
            if top:
                nxt -= top * phi
            cur = nxt
        # X^d = 1: the next one must be 1 again
        assert cur[0] == 1 and not cur[1:].any(), d
        assert np.abs(P).max() < 2 ** 20
        _pt[d] = P.astype(np.int32)
    return _pt[d]


def all_signed_sums(g):
    """s[r] = sum_j eps_j(r) g_j for all r in [0, 2^m)."""
    s = np.zeros(1, dtype=np.int32)
    for gj in g:
        gj = np.int32(gj)
        s = np.concatenate([s + gj, s - gj])
    return s


def bad_fast(B, d, chunk=1 << 16):
    """boolean vector over the 2^m signings: Phi_d | S (exact)."""
    m = len(B)
    G = ptable(d)[np.asarray(B, dtype=np.int64) % d]          # m x phi(d)
    k = G.shape[1]
    mask = all_signed_sums(G[:, 0]) == 0
    if k == 1 or not mask.any():
        return mask
    mask &= all_signed_sums(G[:, 1]) == 0
    if k == 2 or not mask.any():
        return mask
    cand = np.nonzero(mask)[0]
    j = np.arange(m, dtype=np.int64)[None, :]
    G64 = G.astype(np.int64)
    for a in range(0, len(cand), chunk):
        r = cand[a:a + chunk]
        Erows = 1 - 2 * ((r[:, None] >> j) & 1)
        nz = (Erows @ G64).any(axis=1)
        mask[r[nz]] = False
    return mask


def bad_counts_fast(B, n):
    """({d: number of signings bad at d}, number of good signings, vector 'bad somewhere')."""
    m = len(B)
    anybad = np.zeros(1 << m, dtype=bool)
    counts = {}
    for d in divisors(n):
        v = bad_fast(B, d)
        counts[d] = int(v.sum())
        anybad |= v
    return counts, (1 << m) - int(anybad.sum()), anybad
