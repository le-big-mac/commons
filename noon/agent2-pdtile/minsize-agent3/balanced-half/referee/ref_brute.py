"""Referee's brute force, from the literal definitions of section 1 of proof-as-sent.md.

usage:  ref_brute.py all p q n smax      every multiset with 1..smax elements on Z_{p^n} x Z_q
        ref_brute.py bal p q n mmax      every balanced multiset with m = 1..mmax elements in each layer

For every multiset: the vector, total, balancedness, E(N), F(N) of EVERY class N (all depths), literally; then
Lemmas 2, 3, 4, 5, 6 for every pair (E', F') contained in the pattern of N; Lemma 1(c); and at the root
Theorem A (lower bound), Proposition 7, Theorem B (lower bound), plus the least size seen for each exact pattern.
"""
import sys, time, functools, os
import numpy as np
from ref_common import set_tables, rule, literal_patterns, bits_to_set, popcount
from ref_lemmas import Tally, test_records


@functools.lru_cache(maxsize=None)
def comps(m, s):
    """all vectors of m nonnegative integers with sum s, as an int8 array (K, m)"""
    if m == 1:
        return np.array([[s]], dtype=np.int8)
    a = m // 2
    b = m - a
    parts = []
    for t in range(s + 1):
        A = comps(a, t)
        Bm = comps(b, s - t)
        parts.append(np.concatenate([np.repeat(A, len(Bm), axis=0), np.tile(Bm, (len(A), 1))], axis=1))
    return np.concatenate(parts)


def gen_all(M, s, chunk):
    """all multisets of size s on M cells, in blocks (K, M)"""
    a = M // 2
    b = M - a
    for t in range(s + 1):
        A = comps(a, t)
        Bm = comps(b, s - t)
        step = max(1, chunk // len(Bm))
        for i in range(0, len(A), step):
            Ai = A[i:i + step]
            yield np.concatenate([np.repeat(Ai, len(Bm), axis=0), np.tile(Bm, (len(Ai), 1))], axis=1)


def gen_bal(pn, q, m, chunk):
    """all multisets with exactly m elements in each of the q layers; blocks (K, pn, q)"""
    L = comps(pn, m)                      # (KL, pn)
    KL = len(L)
    # product over the q layers; chunk over the index of layer 0
    rest = KL ** (q - 1)
    step = max(1, chunk // rest)
    grids = np.indices((KL,) * (q - 1)).reshape(q - 1, -1)      # indices of layers 1..q-1
    for i in range(0, KL, step):
        L0 = L[i:i + step]
        k0 = len(L0)
        W = np.empty((k0 * rest, pn, q), dtype=np.int8)
        W[:, :, 0] = np.repeat(L0, rest, axis=0)
        for w in range(1, q):
            W[:, :, w] = np.tile(L[grids[w - 1]], (k0, 1))
        yield W


def main():
    mode = sys.argv[1]
    p, q, n, smax = (int(x) for x in sys.argv[2:6])
    chunk = int(sys.argv[6]) if len(sys.argv) > 6 else 400000
    pn = p ** n
    M = pn * q
    B = smax if mode == "all" else smax * q
    tabs = set_tables(p, q, n + 1, B)
    tally = Tally()
    examples = []
    t0 = time.time()
    nms = 0
    ncls = 0
    minsize = {}          # (balanced, Ebits, Fbits) at the root -> least size seen
    thm = Tally()
    dump = os.environ.get("REF_DUMP")
    rootstates = set()
    sizes = range(1, smax + 1)
    for s in sizes:
        blocks = gen_all(M, s, chunk) if mode == "all" else gen_bal(pn, q, s, chunk)
        for blk in blocks:
            W = blk.reshape(len(blk), pn, q).astype(np.int16)
            K = len(W)
            nms += K
            pats = literal_patterns(p, q, n, W)
            for d in range(n + 1):
                r = pats[d]
                j = n - d
                tot = r["tot"].ravel().astype(np.int64)
                bal = r["bal"].ravel()
                Eb = r["E"].ravel()
                Fb = r["F"].ravel()
                ncls += len(tot)
                test_records(p, q, j, tot, bal, Eb, Fb, tabs, tally, examples, tag=f"size{s} depth{d}")
            # root: theorems with the exact pattern
            r = pats[0]
            tot = r["tot"][:, 0].astype(np.int64)
            bal = r["bal"][:, 0]
            Eb = r["E"][:, 0]
            Fb = r["F"][:, 0]
            key = (bal.astype(np.int64) << (2 * n)) | (Eb << n) | Fb
            if dump:
                rows = np.concatenate([r["G"][:, 0, :].astype(np.int64), Eb[:, None], Fb[:, None]], axis=1)
                for row in np.unique(rows, axis=0):
                    rootstates.add(tuple(int(v) for v in row))
            for kv in np.unique(key):
                selk = key == kv
                b_ = bool((kv >> (2 * n)) & 1)
                e_ = int((kv >> n) & ((1 << n) - 1))
                f_ = int(kv & ((1 << n) - 1))
                mn = int(tot[selk].min())
                kk = (b_, e_, f_)
                if kk not in minsize or mn < minsize[kk]:
                    minsize[kk] = mn
                if b_:
                    Es = bits_to_set(e_)
                    Fs = bits_to_set(f_) | {0}
                    val, x, a0, kp = rule(p, q, n, Es, Fs)
                    cnt = int(selk.sum())
                    if x is None:
                        thm.add("Theorem A lower bound |A| >= q p^e", cnt, int((tot[selk] < val).sum()))
                    else:
                        thm.add("Proposition 7 |A| >= q p^(e+k')", cnt, int((tot[selk] < q * p ** (len(Es) + kp)).sum()))
                        thm.add(f"Theorem B lower bound, patterns with x = {x}", cnt, int((tot[selk] < val).sum()))
                        if x == 0:
                            thm.add("CONTROL (false) Theorem B bound with x = 1 for patterns with x = 0", cnt,
                                    int((tot[selk] < val + q * p ** len(Es)).sum()))
                    # Lemma 1(c): levels 1..a0-1 in F => every class of depth <= a0-1 balanced
                    a0_ = a0 if a0 is not None else n + 1
                    badc = 0
                    for d in range(0, a0_):
                        if d <= n:
                            badc += int((~pats[d]["bal"][selk]).sum())
                    thm.add("Lemma 1(c) classes of depth <= a0-1 balanced", cnt, badc)
        print(f"  size {s if mode == 'all' else s * q}: cumulative multisets {nms}, class records {ncls}, "
              f"{time.time() - t0:.0f} s", flush=True)
    print(f"\n=== {mode} p={p} q={q} n={n} (Z_{M}), sizes up to {B}: {nms} multisets, {ncls} class records ===")
    tally.report("  ")
    thm.report("  ")
    if examples:
        print("  FIRST COUNTEREXAMPLE RECORDS:", examples[:10])
    # least sizes against the claimed values
    print("  least size seen per exact pattern of the root (balanced ones against the rule):")
    nb = 0
    nagree = 0
    nabove = 0
    nbelow = 0
    for (b_, e_, f_), mn in sorted(minsize.items()):
        Es = bits_to_set(e_)
        Fs = bits_to_set(f_)
        if b_:
            val, x, a0, kp = rule(p, q, n, Es, Fs | {0})
            nb += 1
            st = "=" if mn == val else ("ABOVE (claimed value not reached in this enumeration)" if mn > val else "BELOW: LOWER BOUND BROKEN")
            nagree += mn == val
            nabove += mn > val
            nbelow += mn < val
            print(f"    balanced   E={sorted(Es)} F={sorted(Fs | {0})}: least seen {mn}, claimed {val} (x={x}) {st}")
        else:
            e = len(Es)
            k = len(Fs - Es)
            val = p ** e if k == 0 else p ** e * (p ** k + q)
            st = "=" if mn == val else ("above" if mn > val else "BELOW the README formula")
            print(f"    unbalanced E={sorted(Es)} F={sorted(Fs)}: least seen {mn}, README sec.2 value {val} {st}")
    npat = 4 ** n
    print(f"  balanced patterns seen: {nb} of {npat} possible; least seen = claimed in {nagree}, above in {nabove}, below in {nbelow}")
    if dump:
        arr = np.array(sorted(rootstates), dtype=np.int64)
        np.save(dump, arr)
        print(f"  dumped {len(arr)} distinct root states (vector, E, F) to {dump}")
    print(f"  time {time.time() - t0:.0f} s")


if __name__ == "__main__":
    main()
