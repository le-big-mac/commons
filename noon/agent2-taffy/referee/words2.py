# Referee control: does the growth depend on the starting loop?  Other loops, same devices.
import numpy as np
from words import DEVICES, lengths, berlekamp_massey

LOOPS3 = {"places 1,2 (the sheet's)": [2, 1], "places 2,3": [3, 2], "places 1,3 (one side of rod 2)": [3, 1],
          "places 1,3 (other side)": [3, -2, 1, 2], "commutator x1 x2 X1 X2 (not simple)": [1, 2, -1, -2]}
LOOPS4 = {"places 1,2 (the sheet's)": [2, 1], "places 2,3": [3, 2], "places 3,4": [4, 3], "places 1,4": [4, 1],
          "places 1,2,3": [3, 2, 1], "places 2,3,4": [4, 3, 2], "places 1,3": [3, 1],
          "commutator x1 x3 X1 X3 (not simple)": [1, 3, -1, -3]}
for n, dev in DEVICES:
    print(f"== n={n} {dev}")
    for name, w in (LOOPS3 if n == 3 else LOOPS4).items():
        L = lengths(n, dev, w, maxper=24 if dev == "s1 s2" else 60)
        C = berlekamp_massey(L)
        roots = np.roots([float(c) for c in C]) if len(C) > 1 else []
        rmax = max(abs(r) for r in roots) if len(roots) else float('nan')
        ok = len(L) >= 2 * (len(C) - 1) + 2      # recurrence checked on at least 2 terms beyond those that fix it
        print(f"   {name:38s} first {L[:7]} periods {len(L)-1:2d} last ratio {L[-1]/L[-2]:.6f}  "
              f"recurrence order {len(C)-1} largest root {rmax:.6f} {'(overdetermined)' if ok else '(NOT overdetermined)'}", flush=True)
