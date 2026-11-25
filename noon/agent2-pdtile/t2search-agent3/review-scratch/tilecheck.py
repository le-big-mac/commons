"""Side check of the step '(T1) and (T2) relative to M  =>  A tiles Z_M' (Coven-Meyerowitz) on the weak tiles found by the direct method:
for every certified weak tile, look for a 0/1 complement B with A + B = Z_M (integer programme, result verified exactly)."""
import sys, pickle, numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
for M in (36, 72, 108):
    res = pickle.load(open(f"res{M}.pkl", "rb")); tiles = [r for r in res if r[2] == "yes"]; ok = bad = 0
    for r in tiles:
        A = [x for x in range(M) if r[0] >> x & 1]; C = np.zeros((M, M))
        for y in range(M):
            for x in A: C[y, (y - x) % M] = 1
        s = milp(c=np.zeros(M), constraints=LinearConstraint(C, 1, 1), integrality=np.ones(M), bounds=Bounds(np.zeros(M), np.ones(M)), options={"time_limit": 30})
        if s.x is not None:
            B = [t for t in range(M) if s.x[t] > 0.5]
            if sorted((x + y) % M for x in A for y in B) == list(range(M)): ok += 1; continue
        bad += 1; print("   weak tile without a tiling complement found:", M, A, s.status)
    print(f"Z_{M}: {len(tiles)} weak-tile orbits from the direct method; tiling complement found and verified for {ok}; not found for {bad}", flush=True)
