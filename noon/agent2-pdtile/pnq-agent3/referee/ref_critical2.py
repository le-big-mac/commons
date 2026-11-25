"""Referee: where does the Delsarte bound alone leave room for a counterexample to the THEOREM'S STATEMENT?
A set A with exact zero pattern (E, F) and |A| = D+(E, F) pd-tiles.  It violates (T1) or (T2) iff
  kind A: 0 not in F and D+ != p^e          (then F is not inside E; only Lemma 3 excludes such a set)
  kind B: 0 in F, E not inside F, D+ = p^e q (only Lemma 4 excludes such a set; Lemma 2 cannot apply)
(0 in F and D+ < p^e q is excluded by Fact 4; D+ > p^e q never happens by (U1).)
For each kind: number of patterns with D+ an integer multiple of k (so that Fact 4 does not already exclude),
how many of them occur for some set, and the smallest ratio (min |A| over sets with that pattern) / D+.
Sizes from the brute-force census if present, else from the state recursion. D+ by float LP."""
import sys, os
import numpy as np
from ref_certs_lp import order_sums, dplus, subsets

def fmt(S): return "{" + ",".join(str(x) for x in sorted(S)) + "}"
for s in sys.argv[1:]:
    p, n, q = (int(v) for v in s.split(","))
    M = p ** n * q
    divs, R = order_sums(M)
    src = f"census_{p}_{n}_{q}.npy" if os.path.exists(f"census_{p}_{n}_{q}.npy") else f"dp_triples_{p}_{n}_{q}.npy"
    sizes = {}
    for row in np.load(src).tolist():
        sizes.setdefault((row[0], row[1]), set()).add(row[2])
    out = {"A": [0, 0, 1e9, None, 0], "B": [0, 0, 1e9, None, 0]}   # patterns, occurring, min ratio, example, counterexamples
    for E in subsets(range(1, n + 1)):
        for F in subsets(range(0, n + 1)):
            Z = set(p ** l for l in E) | set(p ** l * q for l in F)
            D = dplus(Z, divs, R)
            k = p ** len(E) * (q if 0 in F else 1)
            Dint = round(D)
            if abs(D - Dint) > 1e-6 or Dint % k:
                continue
            if 0 not in F and Dint != k:
                kind = "A"
                assert not (F <= E)
            elif 0 in F and (E - F) and Dint == k:
                kind = "B"
            else:
                continue
            key = (sum(1 << l for l in E), sum(1 << l for l in F))
            occ = sorted(sizes.get(key, []))
            o = out[kind]
            o[0] += 1
            if occ:
                o[1] += 1
                if Dint in occ:
                    o[4] += 1
                if occ[0] / Dint < o[2]:
                    o[2] = occ[0] / Dint
                    o[3] = f"E={fmt(E)} F={fmt(F)} D+={Dint} k={k} min|A|={occ[0]}"
    print(f"p={p} n={n} q={q} M={M} [{src.split('_')[0]}]")
    for kind in "AB":
        o = out[kind]
        print(f"   kind {kind}: patterns {o[0]}, occurring for some set {o[1]}, sets of size D+ (counterexamples) {o[4]}, "
              f"smallest min|A|/D+ = {o[2] if o[1] else 'n/a'}  at {o[3]}")
