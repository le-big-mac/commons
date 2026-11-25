"""Referee brute force: every subset of Z_M containing 0, M = p^n q.

For each set:
  * E, F from exact integer residues of A(X) mod Phi_d                        ("poly")
  * E, F from the count criteria (I3)                                         ("cnt")   -> must agree
  * Fact 4: p^e q^[0 in F] divides |A|
  * Lemma 3, Lemma 4 (statements)
  * Lemma 0(a): E, F of the subtrees A^rho, computed by exact residues in Z_{M/p}, vs. E, F of A
  * intermediate claims inside the proofs of Lemma 3 and Lemma 4, and how often each case occurs
Writes a census {(E, F, size): count} to census_<p>_<n>_<q>.npy for the LP script.
"""
import sys, time, json
import numpy as np
from refcommon import *


def bitmask(levels):
    m = 0
    for l in levels:
        m |= 1 << l
    return m


def ef_tables_all_subsets(p, n, q):
    """E, F bitmasks (bit l = level l) by exact residues for ALL 2^M subsets of Z_{p^n q} (incl. empty)."""
    M = p ** n * q
    assert M <= 20
    E = np.zeros(1 << M, dtype=np.uint8)
    F = np.zeros(1 << M, dtype=np.uint8)
    for l in range(0, n + 1):
        for isF in (0, 1):
            d = p ** l * (q if isF else 1)
            if d == 1:
                continue
            R = np.array(residues(M, d), dtype=np.int64)
            T = subset_sum_table(R, np.int16)
            z = ~T.any(axis=1)
            if isF:
                F |= (z.astype(np.uint8) << l)
            else:
                E |= (z.astype(np.uint8) << l)
    return E, F


def run(p, n, q, out):
    t0 = time.time()
    M = p ** n * q
    fwd, inv = crt_table(p, n, q)
    L = min(12, M - 1)
    H = M - 1 - L
    # ---- linear functionals of the indicator vector
    cols = []          # list of (name, start, stop)
    blocks = []
    pos = 0
    for l in range(0, n + 1):
        for isF in (0, 1):
            d = p ** l * (q if isF else 1)
            if d == 1:
                continue
            R = np.array(residues(M, d), dtype=np.int64)
            blocks.append(R)
            cols.append((("F" if isF else "E", l), pos, pos + R.shape[1]))
            pos += R.shape[1]
    for l in range(0, n + 1):
        C = np.zeros((M, p ** l * q), dtype=np.int64)
        for x, (u, w) in enumerate(fwd):
            C[x, (u % p ** l) * q + w] = 1
        blocks.append(C)
        cols.append((("N", l), pos, pos + C.shape[1]))
        pos += C.shape[1]
    W = np.concatenate(blocks, axis=1)
    assert np.abs(W).sum(axis=0).max() < 127
    low = subset_sum_table(W[1:1 + L], np.int8) + W[0].astype(np.int8)   # element 0 always present
    high = subset_sum_table(W[1 + L:], np.int8)
    col = {name: (a, b) for name, a, b in cols}
    # ---- subtree index functional
    have_sub = n >= 1
    Mp = M // p
    fwd_s, inv_s = crt_table(p, n - 1, q)
    Widx = np.zeros((M, p), dtype=np.int64)
    for x, (u, w) in enumerate(fwd):
        rho = u % p
        y = inv_s[((u - rho) // p, w)]
        Widx[x, rho] = 1 << y
    low_idx = subset_sum_table(Widx[1:1 + L], np.int32) + Widx[0].astype(np.int32)
    high_idx = subset_sum_table(Widx[1 + L:], np.int32)
    Esub_t, Fsub_t = ef_tables_all_subsets(p, n - 1, q)   # exact residues in Z_{M/p}
    lev = bitmask(range(1, n + 1))            # levels 1..n
    sublev = bitmask(range(1, n))             # levels 1..n-1 (of a subtree)

    census = {}
    stats = dict(sets=0, I3_mismatch=0, fact4_fail=0, L3_app=0, L3_fail=0, L3_eq=0, L4_app=0, L4_nonvac=0,
                 L4_fail=0, L0a_fail=0,
                 L3_a1=0, L3_a1_claimfail=0, L3_alpha_1inE=0, L3_alpha_1notE=0, L3_beta_1inE=0,
                 L3_beta_1notE=0, L3_exist_claimfail=0, L3_beta_claimfail=0,
                 L4b_1inE=0, L4b_1inE_claimfail=0, L4b_1notE=0, L4b_1notE_claimfail=0)
    hb = max(1, (1 << 18) >> L)    # chunk of 2^18 sets
    nh = 1 << H
    for h0 in range(0, nh, hb):
        h1 = min(nh, h0 + hb)
        V = (high[h0:h1, None, :] + low[None, :, :]).reshape(-1, W.shape[1])
        I = (high_idx[h0:h1, None, :] + low_idx[None, :, :]).reshape(-1, p)
        m = V.shape[0]
        stats["sets"] += m
        # ---- E, F by exact residues
        E = np.zeros(m, dtype=np.uint8)
        F = np.zeros(m, dtype=np.uint8)
        for (kind, l), (a, b) in col.items():
            if kind == "E":
                E |= ((~V[:, a:b].any(axis=1)).astype(np.uint8) << l)
            elif kind == "F":
                F |= ((~V[:, a:b].any(axis=1)).astype(np.uint8) << l)
        # ---- E, F by counts (I3)
        Ec = np.zeros(m, dtype=np.uint8)
        Fc = np.zeros(m, dtype=np.uint8)
        N = {}
        for l in range(0, n + 1):
            a, b = col[("N", l)]
            N[l] = V[:, a:b].reshape(m, p ** l, q).astype(np.int16)   # [set, r mod p^l, j]
        size = N[0].sum(axis=(1, 2))
        lay = N[0][:, 0, :]
        Fc |= (lay == lay[:, :1]).all(axis=1).astype(np.uint8)
        for l in range(1, n + 1):
            # r = r0 + i p^{l-1}: index r -> (i, r0) with r = i * p^{l-1} + r0
            X = N[l].reshape(m, p, p ** (l - 1), q)          # [set, i, r0, j]
            tot = X.sum(axis=3)                               # [set, i, r0]
            okE = (tot == tot[:, :1, :]).all(axis=(1, 2))
            D = X - X[:, :1, :, :] - X[:, :, :, :1] + X[:, :1, :, :1]
            okF = ~D.any(axis=(1, 2, 3))
            Ec |= okE.astype(np.uint8) << l
            Fc |= okF.astype(np.uint8) << l
        stats["I3_mismatch"] += int(((E != Ec) | (F != Fc)).sum())
        e = popcount8(E).astype(np.int64)
        f0 = (F & 1).astype(bool)
        size = size.astype(np.int64)
        k = p ** e * np.where(f0, q, 1)
        stats["fact4_fail"] += int((size % k != 0).sum())
        # ---- Lemma 3 (statement)
        FmE = F & ~E & lev
        app3 = (~f0) & (FmE != 0)
        bound3 = p ** e * (p + q)
        stats["L3_app"] += int(app3.sum())
        stats["L3_fail"] += int((app3 & (size < bound3)).sum())
        stats["L3_eq"] += int((app3 & (size == bound3)).sum())
        # ---- Lemma 4 (statement)
        app4 = f0 & (size == p ** e * q)
        viol4 = np.zeros(m, dtype=bool)
        nonvac4 = np.zeros(m, dtype=bool)
        for b_ in range(1, n + 1):
            hasb = ((FmE >> b_) & 1).astype(bool)
            below = bitmask(range(1, b_))
            nonvac4 |= hasb & ((E & below) != 0)
            viol4 |= hasb & ((E & below & ~F) != 0)
        stats["L4_app"] += int(app4.sum())
        stats["L4_nonvac"] += int((app4 & nonvac4).sum())
        stats["L4_fail"] += int((app4 & viol4).sum())
        # ---- census
        code = E.astype(np.int64) | (F.astype(np.int64) << 8) | (size << 16)
        u, c = np.unique(code, return_counts=True)
        for uu, cc in zip(u.tolist(), c.tolist()):
            census[uu] = census.get(uu, 0) + cc
        # ---- subtrees
        Es = Esub_t[I]            # [set, rho]  bits 1..n-1
        Fs = Fsub_t[I]            # bits 0..n-1
        ssz = N[1].sum(axis=2) if n >= 1 else None    # [set, rho] = |A^rho|
        nonempty = ssz > 0
        if n >= 2:
            # Lemma 0(a): bit l of E(A) (l >= 2)  ==  AND over rho of bit l-1 of E(A^rho)  (empty: all ones)
            andE = np.bitwise_and.reduce(Es & sublev, axis=1)
            andF = np.bitwise_and.reduce(Fs & sublev, axis=1)
            stats["L0a_fail"] += int((((E >> 1) & sublev) != andE).sum() + (((F >> 1) & sublev) != andF).sum())
        # ---- inside Lemma 3
        Eminus = (E >> 1) & sublev
        in1E = ((E >> 1) & 1).astype(bool)
        # case a = 1
        c1 = app3 & ((FmE >> 1) & 1).astype(bool)
        if c1.any():
            X = N[1][c1]                                   # [set, rho, j]
            a0 = X.min(axis=(1, 2))
            alpha = X.min(axis=2) - a0[:, None]
            beta = X.min(axis=1) - a0[:, None]
            okform = (X == a0[:, None, None] + alpha[:, :, None] + beta[:, None, :]).all(axis=(1, 2))
            pe = (p ** e[c1])
            Sa = alpha.sum(axis=1); Sb = beta.sum(axis=1)
            ok = okform & (Sa >= pe) & (q * a0 + Sb >= pe) & ((alpha % pe[:, None]) == 0).all(axis=1) \
                & (Sa >= 1) & (Sb >= 1) & (popcount8(Eminus[c1]) == e[c1])
            stats["L3_a1"] += int(c1.sum())
            stats["L3_a1_claimfail"] += int((~ok).sum())
        for a_ in range(2, n + 1):
            ca = app3 & ((FmE >> a_) & 1).astype(bool)
            if not ca.any():
                continue
            pr1 = nonempty & (((Es >> (a_ - 1)) & 1) == 0)         # a-1 not in E(A^rho)
            pr2 = nonempty & ((Fs & 1) == 0)                       # 0 not in F(A^rho)
            pr0 = (~nonempty) | (((Fs >> (a_ - 1)) & 1) == 1)      # a-1 in F(A^rho) for nonempty
            stats["L3_exist_claimfail"] += int((ca & ~(pr1.any(axis=1) & pr2.any(axis=1) & pr0.all(axis=1))).sum())
            alpha_case = (pr1 & pr2).any(axis=1)
            stats["L3_alpha_1inE"] += int((ca & alpha_case & in1E).sum())
            stats["L3_alpha_1notE"] += int((ca & alpha_case & ~in1E).sum())
            beta_case = ca & ~alpha_case
            stats["L3_beta_1inE"] += int((beta_case & in1E).sum())
            stats["L3_beta_1notE"] += int((beta_case & ~in1E).sum())
            if beta_case.any():
                # claims in (beta): |A^rho0| multiple of p^{|E-|} q ; |A^rho1| multiple of p^{|E-|+1};
                # if 1 in E: all sizes equal and >= p^e q
                em = popcount8(Eminus).astype(np.int64)
                m0 = np.where(pr1, ssz % (p ** em * q)[:, None], 0)
                m1 = np.where(pr2, ssz % (p ** (em + 1))[:, None], 0)
                bad = beta_case & (m0.any(axis=1) | m1.any(axis=1))
                bad |= beta_case & in1E & ~((ssz == ssz[:, :1]).all(axis=1) & (ssz[:, 0] >= p ** e * q))
                stats["L3_beta_claimfail"] += int(bad.sum())
        # ---- inside Lemma 4 (b >= 2)
        hasb2 = (FmE & ~np.uint8(2)) != 0
        app4b = app4 & hasb2
        if app4b.any():
            A1 = app4b & in1E
            stats["L4b_1inE"] += int(A1.sum())
            if A1.any():
                pe1 = p ** np.maximum(e - 1, 0)   # rows with e = 0 are masked out by A1
                ok = ((Es & sublev) == Eminus[:, None]).all(axis=1)          # E(A^rho) = E^- exactly
                ok &= ((Fs & 1) == 1).all(axis=1)                            # all layers equal
                ok &= (N[1] == pe1[:, None, None]).all(axis=(1, 2))          # all layers have size p^{e-1}
                ok &= ((F >> 1) & 1).astype(bool)                            # 1 in F(A)
                stats["L4b_1inE_claimfail"] += int((A1 & ~ok).sum())
            A0 = app4b & ~in1E
            stats["L4b_1notE"] += int(A0.sum())
            if A0.any():
                ok = nonempty.sum(axis=1) == 1
                stats["L4b_1notE_claimfail"] += int((A0 & ~ok).sum())
    cen = np.array([[k_ & 0xFF, (k_ >> 8) & 0xFF, k_ >> 16, v] for k_, v in sorted(census.items())], dtype=np.int64)
    np.save(f"census_{p}_{n}_{q}.npy", cen)
    stats["patterns"] = len(set((int(r[0]), int(r[1])) for r in cen))
    stats["seconds"] = round(time.time() - t0, 1)
    print(f"p={p} n={n} q={q} M={M}: " + json.dumps(stats), file=out, flush=True)
    return stats


if __name__ == "__main__":
    cases = [tuple(int(v) for v in s.split(",")) for s in sys.argv[1:]]
    for (p, n, q) in cases:
        run(p, n, q, sys.stdout)
