"""Usage: python -I brier_check.py FORECASTDIR  -- recompute each forecaster's Brier score from the raw files, outcomes from my blind verdicts."""
import sys, json
import numpy as np
ids = [f"X{i}" for i in range(1, 13)]
y = np.array([0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1.0])  # from blind.out
mine = np.array([.60, .80, .70, .85, .80, .75, .75, .65, .85, .65, .55, .85])  # read off expectations.md
F = np.array([[json.load(open(f"{sys.argv[1]}/f{k}.json"))[i] for i in ids] for k in (1, 2, 3)])
b = lambda p: float(((p - y) ** 2).mean())
print("mine", round(b(mine), 4), "median", round(b(np.median(F, 0)), 4), "mean-of-three", round(b(F.mean(0)), 4), "each", [round(b(f), 4) for f in F])
print("pairwise correlation of forecasters:", np.round(np.corrcoef(F), 3).tolist())
y2 = y.copy(); y2[9] = 0
b2 = lambda p: float(((p - y2) ** 2).mean())
print("if X10 failed: mine", round(b2(mine), 4), "median", round(b2(np.median(F, 0)), 4))
