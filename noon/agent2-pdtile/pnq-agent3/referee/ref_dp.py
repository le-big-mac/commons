"""Referee: exhaustive check of Lemma 3 and Lemma 4 beyond brute-force range, by a state recursion.

This RELIES on (I3) and Lemma 0 (which ref_brute.py verified against exact residues for every subset at n <= 3):
the state of a set S in Z_{p^m} x Z_q is (E(S), F(S) minus {0}, layer sizes c in {0..p^m}^q), and the state of
A in Z_{p^{m+1}} x Z_q is a function of the states of its p subtrees A^rho:
    E(A)   = {l+1 : l in every E(A^rho), A^rho nonempty}  U  {1 if all |A^rho| equal}
    F+(A)  = {l+1 : l in every F+(A^rho), nonempty}       U  {1 if all rows c^rho differ by constants}
    c(A)   = sum of c^rho ;  0 in F(A) iff c(A) constant.
So the set of ALL achievable states at level n is computed exactly (no sampling), and Lemma 3 / Lemma 4 / Fact 4
are checked on every achievable state.  Bits here: bit (l-1) <-> level l.
Symmetry used: simultaneous permutation of the q layers (first subtree taken with c sorted; closure afterwards).
"""
import sys, time, itertools, os, json
import numpy as np


def popcnt_table(nbits):
    t = np.zeros(1 << nbits, dtype=np.int64)
    for b in range(nbits):
        t += (np.arange(1 << nbits) >> b) & 1
    return t


def run(p, q, nmax, out=sys.stdout, budget_pairs=6e8):
    t0 = time.time()
    # level 0: all subsets of Z_q
    C = np.array(list(itertools.product((0, 1), repeat=q)), dtype=np.int16)
    E = np.zeros(len(C), dtype=np.int32)
    F = np.zeros(len(C), dtype=np.int32)
    results = {}
    for m in range(0, nmax):
        lvl = m + 1                      # level being built: subsets of Z_{p^lvl} x Z_q
        Mlvl = p ** lvl * q
        N = len(C)
        size = C.sum(axis=1).astype(np.int32)
        shape = (C - C.min(axis=1, keepdims=True)).astype(np.int16)
        can = (np.diff(C, axis=1) >= 0).all(axis=1) if q > 1 else np.ones(N, bool)
        # intermediate = (Ecap, Fcap, csum, se, sh)
        iE, iF, iC = E[can].copy(), F[can].copy(), C[can].astype(np.int16).copy()
        ise = np.ones(len(iE), dtype=bool)
        ish = np.ones(len(iE), dtype=bool)
        est = len(iE) * N
        # lookup tables on final patterns (E bits lvl, F+ bits lvl): pc = (E << lvl) | F
        npat = 1 << (2 * lvl)
        pcs = np.arange(npat)
        Ep, Fp = pcs >> lvl, pcs & ((1 << lvl) - 1)
        pe = p ** popcnt_table(lvl)[Ep]
        app3 = (Fp & ~Ep) != 0
        viol4 = np.zeros(npat, dtype=bool)
        nonvac4 = np.zeros(npat, dtype=bool)
        for b in range(1, lvl + 1):
            hasb = ((Fp >> (b - 1)) & 1 == 1) & ((Ep >> (b - 1)) & 1 == 0)
            below = (1 << (b - 1)) - 1
            viol4 |= hasb & ((Ep & below & ~Fp) != 0)
            nonvac4 |= hasb & ((Ep & below) != 0)
        T3 = np.zeros(npat * 2 * (Mlvl + 1), dtype=bool)     # (pattern, f0, size) seen
        store = lvl < nmax
        B = p ** lvl + 1
        if store:
            Tfull = np.zeros(npat * B ** q, dtype=bool)
        stat = dict(pairs=0, fact4_fail=0, L3_fail=0, L4_fail=0)
        for k in range(1, p):
            last = (k == p - 1)
            Bk = (k + 1) * p ** m + 1
            wts = (Bk ** np.arange(q)).astype(np.int64)
            if not last:
                Tint = np.zeros((1 << (2 * m)) * 4 * Bk ** q, dtype=bool)
            isum = iC.sum(axis=1).astype(np.int32)
            ishape = (iC - iC.min(axis=1, keepdims=True)).astype(np.int16)
            chunk = max(1, int(3e6 // N))
            if len(iE) * N > budget_pairs:
                print(f"p={p} q={q} level {lvl}: stage {k} needs {len(iE) * N:.2e} pair ops > budget; stopping",
                      file=out, flush=True)
                return results
            for a0 in range(0, len(iE), chunk):
                a1 = min(len(iE), a0 + chunk)
                Ec = iE[a0:a1, None] & E[None, :]
                Fc = iF[a0:a1, None] & F[None, :]
                cs = iC[a0:a1, None, :] + C[None, :, :]
                se = ise[a0:a1, None] & (size[None, :] * k == isum[a0:a1, None])
                sh = ish[a0:a1, None] & (shape[None, :, :] * k == ishape[a0:a1, None, :]).all(axis=2)
                stat["pairs"] += Ec.size
                if not last:
                    key = (((Ec.astype(np.int64) << m) | Fc) * 4 + se * 2 + sh) * (Bk ** q) + (cs.astype(np.int64) @ wts)
                    Tint[key.ravel()] = True
                else:
                    En = (Ec << 1) | se
                    Fn = (Fc << 1) | sh
                    pc = ((En.astype(np.int64) << lvl) | Fn).ravel()
                    c2 = cs.reshape(-1, q)
                    sz = c2.sum(axis=1).astype(np.int64)
                    f0 = (c2 == c2[:, :1]).all(axis=1)
                    nonempty = sz > 0
                    pep = pe[pc]
                    stat["fact4_fail"] += int((nonempty & (sz % (pep * np.where(f0, q, 1)) != 0)).sum())
                    stat["L3_fail"] += int((nonempty & app3[pc] & ~f0 & (sz < pep * (p + q))).sum())
                    stat["L4_fail"] += int((nonempty & viol4[pc] & f0 & (sz == pep * q)).sum())
                    T3[(pc * 2 + f0) * (Mlvl + 1) + sz] = True
                    if store:
                        w2 = (B ** np.arange(q)).astype(np.int64)
                        Tfull[pc * (B ** q) + (c2.astype(np.int64) @ w2)] = True
            if not last:
                idx = np.nonzero(Tint)[0]
                del Tint
                code = idx % (Bk ** q)
                rest = idx // (Bk ** q)
                ish = (rest & 1).astype(bool)
                ise = ((rest >> 1) & 1).astype(bool)
                pat = rest >> 2
                iE = (pat >> m).astype(np.int32)
                iF = (pat & ((1 << m) - 1)).astype(np.int32)
                iC = np.stack([(code // Bk ** j) % Bk for j in range(q)], axis=1).astype(np.int16)
        # ---- summarise level lvl from T3
        idx = np.nonzero(T3)[0]
        szs = idx % (Mlvl + 1)
        r = idx // (Mlvl + 1)
        f0s = r & 1
        pat = r >> 1
        keep = szs > 0
        szs, f0s, pat = szs[keep], f0s[keep], pat[keep]
        Es, Fs = pat >> lvl, pat & ((1 << lvl) - 1)
        triples = set(zip((Es << 1).tolist(), ((Fs << 1) | f0s).tolist(), szs.tolist()))   # brute-force bit convention
        # Lemma 3 sharpness per pattern; Lemma 4 applicability
        minsize = {}
        for Eb, Fb, s in triples:
            minsize[(Eb, Fb)] = min(minsize.get((Eb, Fb), 10 ** 9), s)
        l3pat = [(Eb, Fb) for (Eb, Fb) in minsize if (Fb & 1) == 0 and (Fb & ~Eb & ~1) != 0]
        sharp = sum(1 for (Eb, Fb) in l3pat if minsize[(Eb, Fb)] == p ** bin(Eb).count("1") * (p + q))
        l3fail = sum(1 for (Eb, Fb) in l3pat if minsize[(Eb, Fb)] < p ** bin(Eb).count("1") * (p + q))
        l4tr = [(Eb, Fb, s) for (Eb, Fb, s) in triples if (Fb & 1) and s == p ** bin(Eb).count("1") * q]
        l4nonvac = sum(1 for (Eb, Fb, s) in l4tr if nonvac4[((Eb >> 1) << lvl) | (Fb >> 1)])
        l4fail = sum(1 for (Eb, Fb, s) in l4tr if viol4[((Eb >> 1) << lvl) | (Fb >> 1)])
        # compare with brute-force census if present
        cmpres = "n/a"
        fn = f"census_{p}_{lvl}_{q}.npy"
        if os.path.exists(fn):
            cen = np.load(fn)
            bt = set((int(a), int(b), int(c)) for a, b, c, _ in cen.tolist())
            cmpres = "IDENTICAL" if bt == triples else f"DIFFERENT (dp-only {len(triples - bt)}, brute-only {len(bt - triples)})"
        if store:
            # closure under layer permutations, then decode
            Tv = Tfull.reshape((npat,) + (B,) * q)
            U = np.zeros_like(Tv)
            # axes of Tv: (pattern, c_{q-1}, ..., c_0); any permutation of the last q axes is a layer permutation
            for perm in itertools.permutations(range(q)):
                U |= Tv.transpose((0,) + tuple(1 + i for i in perm))
            idx = np.nonzero(U.ravel())[0]
            del Tv, U, Tfull
            code = idx % (B ** q)
            pat2 = idx // (B ** q)
            E = (pat2 >> lvl).astype(np.int32)
            F = (pat2 & ((1 << lvl) - 1)).astype(np.int32)
            C = np.stack([(code // B ** j) % B for j in range(q)], axis=1).astype(np.int16)
            nstates = len(E)
        else:
            nstates = None
        res = dict(level=lvl, M=Mlvl, child_states=N, pair_ops=stat["pairs"], states_stored=nstates,
                   triples=len(triples), patterns=len(minsize),
                   fact4_fail=stat["fact4_fail"], L3_fail_states=stat["L3_fail"], L4_fail_states=stat["L4_fail"],
                   L3_patterns=len(l3pat), L3_patterns_sharp=sharp, L3_patterns_fail=l3fail,
                   L4_triples=len(l4tr), L4_triples_nonvacuous=l4nonvac, L4_triples_fail=l4fail,
                   vs_brute=cmpres, seconds=round(time.time() - t0, 1))
        print(f"p={p} q={q}: " + json.dumps(res), file=out, flush=True)
        results[lvl] = dict(triples=triples, res=res)
        np.save(f"dp_triples_{p}_{lvl}_{q}.npy", np.array(sorted(triples), dtype=np.int64))
    return results


if __name__ == "__main__":
    for s in sys.argv[1:]:
        p, q, nmax = (int(v) for v in s.split(","))
        run(p, q, nmax)
