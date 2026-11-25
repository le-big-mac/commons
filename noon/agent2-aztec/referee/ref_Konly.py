"""Step 2: many growths with the referee's sampler, reading only K, to compare with the exact law of K.
usage: ref_Konly.py SEED0 NGROW n1,n2,... OUT.npy"""
import sys, time
import numpy as np
from ref_core import grow_step, K_of
seed0 = int(sys.argv[1]); ng = int(sys.argv[2]); reads = [int(x) for x in sys.argv[3].split(",")]; nmax = max(reads)
out = np.zeros((ng, len(reads)), np.int32); t0 = time.time()
for g in range(ng):
    rng = np.random.default_rng([777, seed0 + g]); v = np.zeros((0, 0), np.uint8); c = 0
    for n in range(1, nmax + 1):
        v, _ = grow_step(v, rng)
        if n in reads: out[g, c] = K_of(v); c += 1
np.save(sys.argv[4], out); print(f"{ng} growths to {nmax}: {time.time()-t0:.0f}s")
