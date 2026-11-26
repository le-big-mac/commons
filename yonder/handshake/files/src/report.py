import pickle, sys
from collections import defaultdict
import numpy as np

res = pickle.load(open(sys.argv[1], "rb"))
by = defaultdict(list)
for r in res:
    by[(r["eps"], r["delta"])].append(r)
print("mean cooperation rate (rows eps, cols delta); mean #states in brackets")
deltas = sorted({k[1] for k in by})
print("eps\\delta " + "".join(f"{d:>14}" for d in deltas))
for eps in sorted({k[0] for k in by}):
    row = []
    for d in deltas:
        rs = by[(eps, d)]
        c = np.mean([r["series"][:, 1].mean() for r in rs])
        n = np.mean([r["series"][:, 3].mean() for r in rs])
        row.append(f"{c:8.2f} [{n:.1f}]")
    print(f"{eps:<10}" + "".join(f"{x:>14}" for x in row))
print()
for k in sorted(by):
    tot = defaultdict(int)
    for r in by[k]:
        for d, v in r["dom"]:
            tot[d] += v
    G = sum(r["gens"] for r in by[k])
    print(f"eps={k[0]} delta={k[1]}")
    for d, v in sorted(tot.items(), key=lambda x: -x[1])[:5]:
        print(f"   {100*v/G:5.1f}%  {d}")
