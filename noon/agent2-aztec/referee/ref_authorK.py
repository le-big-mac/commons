"""Step 2: the AUTHOR's sampler (aztec.py, imported read-only) against the exact law of K, many growths to order 100.
usage: ref_authorK.py SEED0 NGROW OUT.npy"""
import sys, time
sys.dont_write_bytecode = True
import numpy as np
sys.path.insert(0, "/home/agent2/aztec")
import aztec as A
seed0 = int(sys.argv[1]); ng = int(sys.argv[2]); reads = (16, 25, 50, 100)
out = np.zeros((ng, 4), np.int32); t0 = time.time()
for g in range(ng):
    rng = np.random.default_rng(seed0 + g)
    x = np.zeros((2, 2), bool); w = A.holes(x); A.fill(x, w, rng.random(int(w.sum())) < 0.5); c = 0
    for order in range(2, 101):
        x = A.shuffle(x); w = A.holes(x); A.fill(x, w, rng.random(int(w.sum())) < 0.5)
        if order in reads:
            a, b, cc, d = A.parts(x); oa = a & ~b & ~cc & ~d; dg = np.diagonal(oa)
            out[g, c] = int(np.argmin(dg)) if not dg.all() else order; c += 1
np.save(sys.argv[3], out); print(f"author's sampler: {ng} growths to 100 in {time.time()-t0:.0f}s")
