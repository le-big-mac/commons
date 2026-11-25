"""Referee post-processing: near-misses (from brute-force census) and end-to-end LP check on DP triples."""
import sys, os, glob
import numpy as np
from ref_certs_lp import order_sums, dplus, subsets


def lv(mask, n, lo):
    return frozenset(l for l in range(lo, n + 1) if (mask >> l) & 1)


def fmt(S):
    return "{" + ",".join(str(x) for x in sorted(S)) + "}"


def near_misses(p, n, q):
    cen = np.load(f"census_{p}_{n}_{q}.npy").tolist()
    M = p ** n * q
    divs, R = order_sums(M)
    print(f"== near-misses, p={p} n={n} q={q} M={M} (sets containing 0)")
    by_pat = {}
    for Eb, Fb, s, c in cen:
        by_pat.setdefault((Eb, Fb), {})[s] = c
    # (1) Lemma 3
    print(" Lemma 3 patterns (0 not in F, F\\E nonempty): E, F, bound p^e(p+q), min size, #sets at min, #sets total")
    nsharp = 0; npat = 0
    for (Eb, Fb), d in sorted(by_pat.items()):
        E, F = lv(Eb, n, 1), lv(Fb, n, 0)
        if 0 in F or not (F - E):
            continue
        npat += 1
        bound = p ** len(E) * (p + q)
        ms = min(d)
        nsharp += (ms == bound)
        print(f"   E={fmt(E):8s} F={fmt(F):10s} bound={bound:3d} min={ms:3d} {'SHARP' if ms == bound else 'slack':5s} "
              f"at-min={d[ms]:6d} total={sum(d.values())}")
    print(f"   sharp patterns: {nsharp} of {npat}")
    # (2) Phi_q | A, |A| = p^e q, E not inside F
    print(" sets with 0 in F, |A| = p^e q, E not in F: E, F, #sets, Lemma-2 side hypothesis, D+ (LP), p^e q / min(p,q)")
    tot = 0
    for (Eb, Fb), d in sorted(by_pat.items()):
        E, F = lv(Eb, n, 1), lv(Fb, n, 0)
        k = p ** len(E) * q
        if 0 in F and k in d and (E - F):
            a = max(E - F)
            hyp = not any((l in F and l not in E) for l in range(a + 1, n + 1))
            Z = set(p ** l for l in E) | set(p ** l * q for l in F)
            D = dplus(Z, divs, R)
            tot += d[k]
            print(f"   E={fmt(E):8s} F={fmt(F):10s} sets={d[k]:5d} hyp={'yes' if hyp else 'NO '} D+={D:.4f} bound={k / min(p, q):.4f}")
    print(f"   total such sets: {tot}")
    # (3) which constraint-satisfying patterns never occur for a pd-tiling set
    pd_pats = set()
    for (Eb, Fb), d in by_pat.items():
        E, F = lv(Eb, n, 1), lv(Fb, n, 0)
        k = p ** len(E) * (q if 0 in F else 1)
        if k in d and ((0 not in F and F <= E) or (0 in F and E <= F)):
            pd_pats.add((E, F))
    allowed = [(E, F) for E in subsets(range(1, n + 1)) for F in subsets(range(0, n + 1))
               if (0 not in F and F <= E) or (0 in F and E <= F)]
    missing = [(E, F) for (E, F) in allowed if (E, F) not in pd_pats]
    print(f" patterns allowed by the theorem's constraints: {len(allowed)}; realised by a (T1)+(T2) set: {len(pd_pats)}; "
          f"never realised: {len(missing)}")
    for E, F in missing:
        Z = set(p ** l for l in E) | set(p ** l * q for l in F)
        k = p ** len(E) * (q if 0 in F else 1)
        occurs = (sum(1 << l for l in E), sum(1 << l for l in F)) in by_pat
        print(f"   E={fmt(E):8s} F={fmt(F):10s} k={k:3d} D+={dplus(Z, divs, R):.4f} pattern occurs for some set: {occurs}")


def end_to_end_dp(p, n, q):
    fn = f"dp_triples_{p}_{n}_{q}.npy"
    tr = np.load(fn).tolist()
    M = p ** n * q
    divs, R = order_sums(M)
    cache = {}
    tol = 1e-6
    res = dict(triples=len(tr), patterns=0, I1_viol=0, pd_triples=0, concl_fail=0, t1t2_triples=0, t1t2_not_pd=0,
               closest_nonpd_gap=1e9)
    for Eb, Fb, s in tr:
        E, F = lv(Eb, n, 1), lv(Fb, n, 0)
        if (E, F) not in cache:
            Z = set(p ** l for l in E) | set(p ** l * q for l in F)
            cache[(E, F)] = dplus(Z, divs, R)
        D = cache[(E, F)]
        if D > s + tol:
            res["I1_viol"] += 1
        e = len(E)
        t1t2 = (s == p ** e * (q if 0 in F else 1)) and ((0 not in F) or E <= F)
        res["t1t2_triples"] += t1t2
        if abs(D - s) < tol:
            res["pd_triples"] += 1
            if not t1t2:
                res["concl_fail"] += 1
        else:
            res["closest_nonpd_gap"] = min(res["closest_nonpd_gap"], s - D)
            if t1t2:
                res["t1t2_not_pd"] += 1
    res["patterns"] = len(cache)
    res["closest_nonpd_gap"] = round(res["closest_nonpd_gap"], 6)
    print(f"end-to-end on DP triples p={p} n={n} q={q} M={M}: {res}", flush=True)


if __name__ == "__main__":
    mode = sys.argv[1]
    for s in sys.argv[2:]:
        p, n, q = (int(v) for v in s.split(","))
        if mode == "near":
            near_misses(p, n, q)
        else:
            end_to_end_dp(p, n, q)
