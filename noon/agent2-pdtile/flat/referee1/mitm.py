"""Referee's solver-free exhaustive check of Lemmas A and B for p=2, q=3 (M=144, |A|=12).

No SAT/MILP solver, and none of the paper's Facts beyond what is re-derived here by enumeration.

Idea.  "Phi_d | A for all d in D" is a system of integer linear equations  sum_{x in A} T_d[x] = 0,
T_d[x] = coefficient vector of X^x mod Phi_d.  Take a random linear form over Z/2^64 of all those
coordinates: h(x) in Z/2^64 per element, and  A satisfies the system  ==>  sum_{x in A} h(x) = 0 mod 2^64
(no false negatives; false positives are possible in principle and every hit is re-verified exactly).

Splits (each derived by brute-force enumeration of count vectors, not quoted from the document):
  * mode "halves", modulus m: the count vectors (number of elements of A in each class mod m) allowed by
    the conditions d | m are enumerated exhaustively; for each allowed vector, all ways of filling the
    classes 0..m/2-1 (left) and m/2..m-1 (right) are enumerated and joined on the hash by sort + search.
  * mode "three" (needs 3 in D): counts mod 3 are forced to (4,4,4) [enumerated]; WLOG 0 in A
    (translation multiplies A(X) by a unit mod X^M-1); 16215 x 194580 pairs (A_0, A_1) looked up
    against the 194580 choices of A_2.

Controls: planted-target recovery (search for hash-sum = that of a random planted set; must find it),
and the drop-one variants, where the document claims that sets exist for some and not for others.
"""
import itertools
import multiprocessing as mp
import random
import sys
import time
from math import comb

import numpy as np

from cyclo import xpow_table, divides_exact, divides_numeric, zero_set

M, NSIZE = 144, 12
MASK = (1 << 64) - 1
LEMMA_A = (3, 16, 48, 24, 72, 36)
LEMMA_B = (4, 8, 9, 6, 18, 12)


def elem_hash(D, seed):
    rng = random.Random(seed)
    h = [0] * M
    for d in D:
        T = xpow_table(M, d)
        c = [rng.getrandbits(64) for _ in range(T.shape[1])]
        for x in range(M):
            s = 0
            for k in range(T.shape[1]):
                s += int(T[x, k]) * c[k]
            h[x] = (h[x] + s) & MASK
    return np.array(h, dtype=np.uint64)


def satisfies(A, D):
    ex = all(divides_exact(A, M, d) for d in D)
    nu = all(divides_numeric(A, d) for d in D)
    assert ex == nu, "exact and floating-point divisibility tests disagree"
    return ex


def half_vectors(parts, cap, maxtotal):
    def rec(k, left):
        if k == 0:
            yield ()
            return
        for i in range(min(cap, left) + 1):
            for rest in rec(k - 1, left - i):
                yield (i,) + rest
    return rec(parts, maxtotal)


def allowed_counts(m, ds):
    """All vectors v in Z_{>=0}^m, sum = NSIZE, v_r <= M/m, with sum_r v_r (X^r mod Phi_d) = 0 for d in ds.
    Exhaustive (meet in the middle over the two halves of the vector)."""
    tabs = []
    for d in ds:
        assert m % d == 0
        T = xpow_table(M, d)
        assert all((T[x] == T[x % m]).all() for x in range(M))  # depends on x mod m only
        tabs.append(T[:m])
    K = np.concatenate(tabs, axis=1) if tabs else np.zeros((m, 0), dtype=np.int64)
    hm = m // 2 if m % 2 == 0 else m // 2 + 1
    left = {}
    for v in half_vectors(hm, M // m, NSIZE):
        sig = tuple(int(z) for z in (np.array(v, dtype=np.int64) @ K[:hm])) + (sum(v),)
        left.setdefault(sig, []).append(v)
    out = []
    for w in half_vectors(m - hm, M // m, NSIZE):
        s = np.array(w, dtype=np.int64) @ K[hm:]
        sig = tuple(int(-z) for z in s) + (NSIZE - sum(w),)
        for v in left.get(sig, ()):
            out.append(v + w)
    return out


_combo_cache = {}


def class_sums(h, m, r, c):
    key = (h.tobytes(), m, r, c)
    if key not in _combo_cache:
        cls = [x for x in range(M) if x % m == r]
        if c == 0:
            combos = np.zeros((1, 0), dtype=np.int64)
            K = np.zeros(1, dtype=np.uint64)
        else:
            combos = np.array(list(itertools.combinations(cls, c)), dtype=np.int64)
            K = h[combos].sum(axis=1, dtype=np.uint64)
        _combo_cache[key] = (combos, K)
    return _combo_cache[key]


def side(h, m, rs, vec):
    S = np.zeros(1, dtype=np.uint64)
    shapes = []
    for r in rs:
        combos, K = class_sums(h, m, r, vec[r])
        S = (S[:, None] + K[None, :]).ravel()
        shapes.append(len(K))
    return S, shapes


def decode(h, m, rs, vec, shapes, idx):
    parts = np.unravel_index(idx, shapes)
    A = []
    for r, i in zip(rs, parts):
        combos, _ = class_sums(h, m, r, vec[r])
        A += [int(x) for x in combos[i]]
    return A


def join_halves(h, D, m, ds, target=0, want=3, verbose=True):
    """Exhaustive search for 12-sets with hash-sum == target whose counts mod m obey the conditions ds."""
    vecs = allowed_counts(m, ds)
    lr, rr = list(range(m // 2)), list(range(m // 2, m))
    total_left = total_right = 0
    hash_hits = 0
    found = []
    for vec in vecs:
        L, shl = side(h, m, lr, vec)
        R, shr = side(h, m, rr, vec)
        total_left += len(L)
        total_right += len(R)
        order = np.argsort(R, kind="stable")
        Rs = R[order]
        q = np.uint64(target) - L
        pos = np.searchsorted(Rs, q)
        pos[pos == len(Rs)] = 0
        hit = np.nonzero(Rs[pos] == q)[0]
        hash_hits += len(hit)
        todo = hit if target != 0 else hit[: max(0, want - len(found)) + 2]
        for i in todo:
            j0 = pos[i]
            j = j0
            while j < len(Rs) and Rs[j] == q[i]:
                A = sorted(decode(h, m, lr, vec, shl, int(i)) + decode(h, m, rr, vec, shr, int(order[j])))
                if target == 0:
                    if satisfies(A, D) and len(found) < want:
                        found.append(A)
                else:
                    found.append(A)
                j += 1
        if len(found) >= want and target == 0:
            break
    if verbose:
        print(f"    split mod {m} using d in {list(ds)}: {len(vecs)} admissible count vectors, "
              f"{total_left:,} left fillings x {total_right:,} right fillings examined, "
              f"hash hits {hash_hits}, verified sets {len(found)}", flush=True)
    return found, hash_hits, len(vecs)


# ---------- three-way join (needs 3 in D) ----------
_G = {}


def _three_worker(args):
    lo, hi, target = args
    H0, H1, H2s = _G["H0"], _G["H1"], _G["H2s"]
    hits = []
    for i in range(lo, hi):
        q = _G["T"] - (H1 + H0[i])
        pos = np.searchsorted(H2s, q)
        pos[pos == len(H2s)] = 0
        w = np.nonzero(H2s[pos] == q)[0]
        for j in w[:50]:
            pj = int(pos[j])
            while pj < len(H2s) and H2s[pj] == q[j]:
                hits.append((i, int(j), pj))
                pj += 1
        if len(hits) > 50 and target == 0:
            return hits, i + 1 - lo
    return hits, hi - lo


def join_three(h, D, target=0, want=3, verbose=True, procs=14):
    assert 3 in D
    vecs = allowed_counts(3, [3])
    assert vecs == [(4, 4, 4)], vecs
    G = [[x for x in range(M) if x % 3 == j] for j in range(3)]
    c0 = np.array([(0,) + c for c in itertools.combinations(G[0][1:], 3)], dtype=np.int64)
    c1 = np.array(list(itertools.combinations(G[1], 4)), dtype=np.int64)
    c2 = np.array(list(itertools.combinations(G[2], 4)), dtype=np.int64)
    H0 = h[c0].sum(axis=1, dtype=np.uint64)
    H1 = h[c1].sum(axis=1, dtype=np.uint64)
    H2 = h[c2].sum(axis=1, dtype=np.uint64)
    order = np.argsort(H2, kind="stable")
    _G.update(H0=H0, H1=H1, H2s=H2[order], T=np.full(len(H1), target, dtype=np.uint64))
    step = 64
    tasks = [(lo, min(lo + step, len(H0)), target) for lo in range(0, len(H0), step)]
    found, hash_hits, done = [], 0, 0
    with mp.get_context("fork").Pool(procs) as pool:
        for hits, cnt in pool.imap_unordered(_three_worker, tasks):
            done += cnt
            hash_hits += len(hits)
            for (i, j, pj) in hits:
                A = sorted([int(x) for x in c0[i]] + [int(x) for x in c1[j]] + [int(x) for x in c2[order[pj]]])
                if target == 0:
                    if satisfies(A, D) and len(found) < want:
                        found.append(A)
                else:
                    found.append(A)
            if target == 0 and len(found) >= want:
                pool.terminate()
                break
    if verbose:
        complete = "ALL" if done == len(H0) else f"{done} of"
        print(f"    split mod 3, counts (4,4,4), 0 in A: {complete} {len(H0):,} x {len(H1):,} pairs "
              f"looked up against {len(H2):,}; hash hits {hash_hits}{'+' if done < len(H0) else ''}, "
              f"verified sets {len(found)}", flush=True)
    return found, hash_hits, done == len(H0)


def planted_controls():
    rng = random.Random(7)
    print("Planted-target controls (the join must return the planted set):")
    ok = True
    # halves, m=16 (structure n_r = n_{r+8})
    hA = elem_hash(LEMMA_A, 101)
    vecs = allowed_counts(16, [16])
    assert all(v[:8] == v[8:] for v in vecs) and len(vecs) == comb(13, 7), len(vecs)
    for _ in range(2):
        v = rng.choice(vecs)
        P = sorted(x for r in range(16) for x in rng.sample([y for y in range(M) if y % 16 == r], v[r]))
        t = int(hA[P].sum(dtype=np.uint64))
        found, _, _ = join_halves(hA, LEMMA_A, 16, [16], target=t, verbose=False)
        ok &= P in found and all(int(hA[S].sum(dtype=np.uint64)) == t for S in found)
        print(f"  halves mod 16: planted {P} recovered: {P in found} (returned {len(found)} set(s))", flush=True)
    hB = elem_hash(LEMMA_B, 202)
    vecs = allowed_counts(8, [4, 8])
    for _ in range(2):
        v = rng.choice(vecs)
        P = sorted(x for r in range(8) for x in rng.sample([y for y in range(M) if y % 8 == r], v[r]))
        t = int(hB[P].sum(dtype=np.uint64))
        found, _, _ = join_halves(hB, LEMMA_B, 8, [4, 8], target=t, verbose=False)
        ok &= P in found and all(int(hB[S].sum(dtype=np.uint64)) == t for S in found)
        print(f"  halves mod 8:  planted {P} recovered: {P in found} (returned {len(found)} set(s))", flush=True)
    for _ in range(1):
        P = sorted([0] + rng.sample(range(3, M, 3), 3) + rng.sample(range(1, M, 3), 4) + rng.sample(range(2, M, 3), 4))
        t = int(hA[P].sum(dtype=np.uint64))
        found, _, complete = join_three(hA, LEMMA_A, target=t, verbose=False)
        ok &= P in found and complete
        print(f"  three-way mod 3: planted {P} recovered: {P in found} (returned {len(found)} set(s))", flush=True)
    return ok


def report(name, D, found, expect_sets):
    verdict = "SETS EXIST" if found else "NO SET"
    agree = (bool(found) == expect_sets)
    ex = ""
    if found:
        A = found[0]
        ex = f"  e.g. {A}, zero set {zero_set(A, M)}"
    print(f"  {name}: D={sorted(D)} -> {verdict}; document says "
          f"{'sets exist' if expect_sets else 'no set'}: {'AGREE' if agree else 'DISAGREE'}{ex}", flush=True)
    return agree


def main(what):
    t0 = time.time()
    ok = True
    if "controls" in what:
        ok &= planted_controls()
        print(f"[{time.time() - t0:.0f}s]", flush=True)
    if "B" in what:
        print("Lemma B, (p,q)=(2,3): D = {4,8,9,6,18,12}")
        vecs = allowed_counts(8, [4, 8])
        print(f"  count vectors mod 8 allowed by Phi_4, Phi_8 (exhaustive): {sorted(vecs)}")
        for seed in (11, 12):
            h = elem_hash(LEMMA_B, seed)
            found, hh, nv = join_halves(h, LEMMA_B, 8, [4, 8])
            ok &= report(f"Lemma B full list (hash seed {seed})", LEMMA_B, found, False)
        print(f"[{time.time() - t0:.0f}s]", flush=True)
    if "Bdrop" in what:
        print("Lemma B drop-one variants:")
        for d, expect in ((9, False), (6, True), (18, False), (12, False)):
            D = tuple(x for x in LEMMA_B if x != d)
            found, _, _ = join_halves(elem_hash(D, 30 + d), D, 8, [4, 8])
            ok &= report(f"drop Phi_{d}", D, found, expect)
        D = tuple(x for x in LEMMA_B if x != 4)
        found, _, _ = join_halves(elem_hash(D, 34), D, 8, [8])
        ok &= report("drop Phi_4", D, found, False)
        D = tuple(x for x in LEMMA_B if x != 8)
        found, _, _ = join_halves(elem_hash(D, 38), D, 4, [4])
        ok &= report("drop Phi_8", D, found, True)
        print(f"[{time.time() - t0:.0f}s]", flush=True)
    if "A" in what:
        print("Lemma A, (p,q)=(2,3): D = {3,16,48,24,72,36}")
        h = elem_hash(LEMMA_A, 21)
        found, hh, nv = join_halves(h, LEMMA_A, 16, [16])
        ok &= report("Lemma A full list, split mod 16", LEMMA_A, found, False)
        print(f"[{time.time() - t0:.0f}s]", flush=True)
    if "A3" in what:
        h = elem_hash(LEMMA_A, 22)
        found, hh, complete = join_three(h, LEMMA_A)
        assert complete or found
        ok &= report("Lemma A full list, split mod 3 (independent second split)", LEMMA_A, found, False)
        print(f"[{time.time() - t0:.0f}s]", flush=True)
    if "Adrop" in what:
        print("Lemma A drop-one variants:")
        for d, expect in ((3, True), (48, False), (24, False), (72, True), (36, True)):
            D = tuple(x for x in LEMMA_A if x != d)
            found, _, _ = join_halves(elem_hash(D, 40 + d), D, 16, [16])
            ok &= report(f"drop Phi_{d}", D, found, expect)
            print(f"[{time.time() - t0:.0f}s]", flush=True)
        D = tuple(x for x in LEMMA_A if x != 16)
        found, _, complete = join_three(elem_hash(D, 56), D)
        assert complete or found
        ok &= report("drop Phi_16 (three-way split)", D, found, True)
        print(f"[{time.time() - t0:.0f}s]", flush=True)
    print("ALL AS EXPECTED:", ok)


if __name__ == "__main__":
    main(sys.argv[1:] or ["controls", "B", "A"])
