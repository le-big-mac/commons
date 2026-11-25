"""Lemma B: which subsets of its six hypotheses already exclude every set?  (agent3 / Yonder)
M = p^4 q^2, |B| = p^2 q, 0 in B.  HiGHS through scipy, my own residue encoding; sets returned are re-verified exactly.
"infeasible" is a solver's word."""
import sys, itertools
from lemma_variants import exists
for p, q in [tuple(map(int, a.split(","))) for a in sys.argv[1:]] or [(2, 3)]:
    names = {p*p: "p^2", p**3: "p^3", q*q: "q^2", p*q: "pq", p*q*q: "pq^2", p*p*q: "p^2q"}
    full = list(names); res = {}
    print(f"p={p} q={q} M={p**4*q*q} |B|={p*p*q}", flush=True)
    for r in range(len(full), -1, -1):
        for Z in itertools.combinations(full, r):
            # a subset of a feasible set of hypotheses is feasible: skip
            if any(set(Z) <= set(Y) and st.startswith("SET") for Y, st in res.items()): res[Z] = "SET (implied)"; continue
            st, A, dt = exists(p, q, list(Z), limit=300); res[Z] = st
            print(f"   {' '.join(names[d] for d in Z) or '(none)':34s} {st:24s} {dt:6.1f} s", flush=True)
    inf = [set(Z) for Z, st in res.items() if st == "infeasible"]
    minimal = [Z for Z in inf if not any(Y < Z for Y in inf)]
    print("   minimal infeasible subsets:", [" ".join(names[d] for d in full if d in Z) for Z in minimal])
    print("   undecided:", [" ".join(names[d] for d in Z) for Z, st in res.items() if not (st == "infeasible" or st.startswith("SET"))], flush=True)
