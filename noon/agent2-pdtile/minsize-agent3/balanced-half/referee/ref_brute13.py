"""Referee, second reading: literal brute force for the new end of section 7 (fibre classes, Proposition 13).

usage:  ref_brute13.py bal p q n mmax [dump.npy]     every balanced multiset with m = 1..mmax elements per layer
        ref_brute13.py all p q n smax [dump.npy]     every multiset with 1..smax elements

For every multiset, literally from the definitions: the root's vector, E, F, balancedness, and the least depth of a
nonempty fibre class (a class all of whose subclasses, itself included, are balanced).
 (1) Proposition 13 for every pattern (E, F) with 0 in F, F not everything, k' >= 1 whose size q p^(e+k') is in range:
     (*) "some balanced multiset with exact pattern (E+, F) and exactly q p^(e+k') elements has a nonempty fibre
     class of depth < g1"  against  x = 0.
 (2) The construction in the proof of "(*) => x = 0", run on EVERY witness: replace the inside of the fibre class Z
     by m.Fib(D_Z) and check that the result has exact pattern (E, F) and the same size.
 (3) optional dump of {(vector, E, F): least depth} for comparison with ref_dp13.
"""
import sys, time, itertools
import numpy as np
from ref_common import rule, literal_patterns, bits_to_set
from ref_brute import gen_all, gen_bal

INF = 254


def least_fibre_depth(p, q, n, W):
    """W (K, p^n, q).  Returns (K,) least depth d of a nonempty fibre class, INF if none; and per depth the boolean
    arrays fib[d] (K, p^d): class c of depth d is a nonempty fibre class."""
    K = W.shape[0]
    leafconst = (W == W[:, :, :1]).all(axis=2)                  # (K, p^n): the class of depth n is balanced
    tot = W.sum(axis=2)
    out = np.full(K, INF, dtype=np.int64)
    fibs = []
    for d in range(n, -1, -1):
        allc = leafconst.reshape(K, p ** (n - d), p ** d).all(axis=1)       # every string in the class is whole fibres
        nonempty = tot.reshape(K, p ** (n - d), p ** d).sum(axis=1) > 0
        fib = allc & nonempty
        fibs.append(fib)
        out = np.where(fib.any(axis=1), d, out)
    return out, fibs[::-1]


def pattern_of(p, q, n, W):
    r = literal_patterns(p, q, n, W.reshape(1, p ** n, q))[0]
    return bits_to_set(r["E"][0, 0]), bits_to_set(r["F"][0, 0]) | ({0} if r["bal"][0, 0] else set())


def main():
    mode = sys.argv[1]
    p, q, n, smax = (int(x) for x in sys.argv[2:6])
    dump = sys.argv[6] if len(sys.argv) > 6 else None
    pn = p ** n
    t0 = time.time()
    best = {}            # (g tuple, Ebits, Fbits) -> least fibre depth
    nms = 0
    nwit = 0
    nconstr = 0
    nconstr_bad = 0
    full = (1 << n) - 1
    for s in range(1, smax + 1):
        blocks = gen_all(pn * q, s, 300000) if mode == "all" else gen_bal(pn, q, s, 300000)
        for blk in blocks:
            W = blk.reshape(len(blk), pn, q).astype(np.int16)
            K = len(W)
            nms += K
            r = literal_patterns(p, q, n, W)[0]
            md, fibs = least_fibre_depth(p, q, n, W)
            g = r["G"][:, 0, :].astype(np.int64)
            Eb = r["E"][:, 0]
            Fb = r["F"][:, 0]
            bal = r["bal"][:, 0]
            rows = np.concatenate([g, Eb[:, None], Fb[:, None], md[:, None]], axis=1)
            for row in np.unique(rows, axis=0):
                key = tuple(int(v) for v in row[:-1])
                v = int(row[-1])
                if key not in best or v < best[key]:
                    best[key] = v
            # (2) the construction of "(*) => x = 0" on every witness
            tot = g.sum(axis=1)
            ecount = np.array([bin(int(e)).count("1") for e in range(full + 1)])[Eb]
            cand = np.flatnonzero(bal & (Fb != full) & (tot == q * p ** ecount) & (md < n))
            for k in cand:
                Ep = bits_to_set(Eb[k])
                Fs = bits_to_set(Fb[k]) | {0}
                a0 = min(a for a in range(1, n + 1) if a not in Fs)
                if any((a in Fs and a not in Ep) for a in range(a0 + 1, n + 1)):
                    continue                       # (E+, F) must have no level of F \ E+ beyond a0
                pool = [a for a in range(a0 + 1, n + 1) if a in Ep and a in Fs]
                if not pool:
                    continue
                Wk = W[k].astype(np.int64)
                for d in range(0, n):
                    for c in np.flatnonzero(fibs[d][k]):
                        # Z = class c of depth d, a nonempty fibre class
                        for rr in range(1, len(pool) + 1):
                            for G in itertools.combinations(pool, rr):
                                if min(G) <= d:
                                    continue       # depth of Z must be < g1 = min G'
                                E = Ep - set(G)
                                nwit += 1
                                inZ = (np.arange(pn) % p ** d) == c
                                Zt = int(Wk[inZ].sum())
                                free = [a for a in E if a > d]
                                m, rem = divmod(Zt, q * p ** len(free))
                                ok = rem == 0 and m >= 1
                                A = Wk.copy()
                                A[inZ] = 0
                                DZ = inZ.copy()
                                u = np.arange(pn)
                                for a in range(d + 1, n + 1):
                                    if a not in E:
                                        DZ &= ((u // p ** (a - 1)) % p) == 0
                                A[DZ] = m
                                nconstr += 1
                                EA, FA = pattern_of(p, q, n, A)
                                val, x, _, kp = rule(p, q, n, E, Fs)
                                if not (ok and EA == E and FA == Fs and int(A.sum()) == int(Wk.sum()) and x == 0
                                        and int(A.sum()) == val):
                                    nconstr_bad += 1
                                    if nconstr_bad <= 3:
                                        print("   CONSTRUCTION FAILS:", sorted(Ep), sorted(Fs), "Z depth", d, "class", int(c), "G'", G,
                                              "got", sorted(EA), sorted(FA), "x", x)
        print(f"  size {s if mode == 'all' else s * q}: cumulative multisets {nms}, {time.time() - t0:.0f} s", flush=True)
    B = smax if mode == "all" else smax * q
    print(f"=== {mode} p={p} q={q} n={n} (Z_{pn * q}), sizes up to {B}: {nms} multisets; {len(best)} distinct root states ===")
    # (1) Proposition 13
    npat = nin = nbad = 0
    for e_ in range(full + 1):
        for f_ in range(full + 1):
            E = bits_to_set(e_)
            F = bits_to_set(f_) | {0}
            val, x, a0, kp = rule(p, q, n, E, F)
            if x is None or kp == 0:
                continue
            npat += 1
            Gp = sorted(a for a in range(a0 + 1, n + 1) if a in F and a not in E)
            g1 = Gp[0]
            size = q * p ** (len(E) + kp)
            if size > B or (mode == "bal" and size % q):
                continue
            nin += 1
            ep = sum(1 << (a - 1) for a in (E | set(Gp)))
            key = tuple([size // q] * q) + (ep, f_)
            v = best.get(key)
            star = v is not None and v < g1
            if v is None:
                print(f"   NOT SEEN: pattern (E+, F) = ({sorted(E | set(Gp))}, {sorted(F)}) at its claimed least size {size}")
                nbad += 1
            if star != (x == 0):
                nbad += 1
                print(f"   PROPOSITION 13 FAILS: E={sorted(E)} F={sorted(F)} x={x} g1={g1} least fibre depth {v}")
    print(f"  Proposition 13: {npat} patterns with k' >= 1, {nin} with q p^(e+k') in range, disagreements {nbad}")
    print(f"  construction of '(*) => x = 0': {nconstr} triples (witness multiset, fibre class Z, G') built, failures {nconstr_bad}")
    if dump:
        arr = np.array(sorted(k + (v,) for k, v in best.items()), dtype=np.int64)
        np.save(dump, arr)
        print(f"  dumped {len(arr)} states to {dump}")
    print(f"  time {time.time() - t0:.0f} s")


if __name__ == "__main__":
    main()
