import pickle, sys
from collections import defaultdict
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

res = pickle.load(open(sys.argv[1], "rb"))
by = defaultdict(list)
for r in res:
    by[(r["eps"], r["delta"])].append(r)
E = sorted({k[0] for k in by}); Dl = sorted({k[1] for k in by})
fig, ax = plt.subplots(len(E), len(Dl), figsize=(4 * len(Dl), 2.2 * len(E)), sharex=True, sharey=True)
for i, e in enumerate(E):
    for j, d in enumerate(Dl):
        a = ax[i, j]
        r = by[(e, d)][0]
        s = r["series"]
        w = 50
        sm = np.convolve(s[:, 1], np.ones(w) / w, mode="valid")
        a.plot(s[: len(sm), 0], sm, lw=0.6, color="#2a6f97")
        a.set_ylim(0, 1)
        a.set_title(f"noise {e}, continuation {d}", fontsize=9)
        if j == 0: a.set_ylabel("cooperation")
        if i == len(E) - 1: a.set_xlabel("generation")
fig.suptitle("Cooperation over time in evolving FSM populations (one run per cell, starting from all-defect)")
fig.tight_layout()
fig.savefig(sys.argv[2], dpi=110)
