"""Referee: 'critical' patterns = not allowed by the theorem's conclusion, yet D+(Z) = k(Z) (float LP).
A set with exactly such a zero set and |A| = k would pd-tile and contradict the note. For each, report the sizes
that actually occur (brute-force census, or the state recursion's triples)."""
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
    print(f"== p={p} n={n} q={q} M={M}  (sizes from {src})")
    ncrit = 0; nocc = 0; kinds = {}
    lines = []
    for E in subsets(range(1, n + 1)):
        for F in subsets(range(0, n + 1)):
            allowed = (0 not in F and F <= E) or (0 in F and E <= F)
            if allowed:
                continue
            Z = set(p ** l for l in E) | set(p ** l * q for l in F)
            D = dplus(Z, divs, R)
            k = p ** len(E) * (q if 0 in F else 1)
            if abs(D - k) < 1e-6:
                ncrit += 1
                key = (sum(1 << l for l in E), sum(1 << l for l in F))
                occ = sorted(sizes.get(key, []))
                if 0 in F:
                    a = max(E - F)
                    hyp = not any((l in F and l not in E) for l in range(a + 1, n + 1))
                    kind = "0 in F, E not in F, Lemma-2 hypothesis " + ("HOLDS (!)" if hyp else "fails -> Lemma 4 needed")
                else:
                    kind = "0 not in F, F not in E -> Lemma 3 needed"
                kinds[kind] = kinds.get(kind, 0) + 1
                nocc += bool(occ)
                bad = k in occ
                lines.append(f"   E={fmt(E):10s} F={fmt(F):12s} k=D+={k:4d}  sizes occurring: "
                             f"{(str(occ[:6]) + (' ...' if len(occ) > 6 else '')) if occ else 'pattern never occurs'}"
                             f"{'   <-- COUNTEREXAMPLE SIZE PRESENT' if bad else ''}")
    for l in lines[:40]:
        print(l)
    if len(lines) > 40:
        print(f"   ... {len(lines) - 40} more")
    print(f"   critical patterns: {ncrit}; of these the pattern occurs for some set: {nocc}; kinds: {kinds}")
