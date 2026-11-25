"""Blind step, item 3: growths with the referee's sampler, read at given orders.
usage: ref_sample.py SEED0 NGROW OUTPREFIX n1,n2,...
Each growth has its own seed (SEED0 + g). Saves readings to OUTPREFIX.npz, and the final tilings.
"""
import sys, time
import numpy as np
from ref_core import *

seed0 = int(sys.argv[1]); ng = int(sys.argv[2]); out = sys.argv[3]
reads = [int(x) for x in sys.argv[4].split(",")]
save_tilings = len(sys.argv) > 5 and sys.argv[5] == "save"
nmax = max(reads)
rows = []
kept = {}
t0 = time.time()
for g in range(ng):
    rng = np.random.default_rng([20261122, seed0 + g])
    v = np.zeros((0, 0), np.uint8)
    tosses = 0
    for n in range(1, nmax + 1):
        v, k = grow_step(v, rng)
        tosses += k
        if n in reads:
            assert is_tiling(v)
            parts = frozen_parts(v)
            cnt, sh = central_shares(v)
            cnt2, sh2 = central_shares(v, inclusive=True)
            npair = int(((v == 9) | (v == 6)).sum()); nempty = int((v == 0).sum())
            rows.append([seed0 + g, n, K_of(v), sum(parts) / v.size, *parts, *cnt, *cnt2, tosses, npair, nempty])
            if save_tilings:
                kept[f"g{seed0+g}_n{n}"] = v.copy()
rows = np.array(rows, float)
np.savez_compressed(out + ".npz", rows=rows, **kept)
print(f"done {ng} growths to {nmax} in {time.time()-t0:.1f}s", flush=True)
