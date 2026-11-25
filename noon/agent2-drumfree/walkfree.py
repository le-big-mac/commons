"""The weight walked up or down, each search starting from the answer at the weight before (and from the search's own answer there).
usage: python -u walkfree.py five|seven up|down RINGS OUT.json"""
import sys, json, os
import numpy as np
import libfree as F
L = F.L; name, way, R = sys.argv[1], sys.argv[2], int(sys.argv[3]); sk = F.FreeSkin(R, F.SETS[name])
WW = [0.6, 0.8, 1.0, 1.1, 1.2, 1.3, 1.43, 2.0, 2.79, 4.0, 6.0, 12.0]; order = WW if way == "up" else WW[::-1]; prev = None; out = []
for M in order:
    starts = []
    if prev is not None: starts.append(("the weight before", prev * min(1.0, M / sk.mass(prev))))
    f = f"s-{name}-{M:g}.json"
    if os.path.exists(f) and str(R) in json.load(open(f))['rings']: starts.append(("the search's answer", np.array(json.load(open(f))['rings'][str(R)]['a'])))
    if not starts: starts.append(("a disc to 0.5", L.disc(sk, M / 0.25, 0.5)))
    best = None
    for nm, a0 in starts:
        a, fm = L.slp(sk, a0, M)
        if best is None or fm < best[0]: best = (fm, a, nm)
    fm, a, nm = best; prev = a; out.append(dict(weight=M, miss=fm, a=a.tolist(), start=nm)); print(f"{name} {way:4s} {R} rings {M:5.2f}: {100 * fm:.4f}% from '{nm}'", flush=True); json.dump(dict(walk=out), open(sys.argv[4], "w"))
