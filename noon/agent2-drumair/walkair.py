"""The weight walked up or down with air of fixed strength B, each search starting from the answer before it.
usage: python -u walkair.py tuned|free B up|down RINGS OUT.json"""
import sys, json
import numpy as np
import airlib as A
L = A.L; kind, B, way, R = sys.argv[1], float(sys.argv[2]), sys.argv[3], int(sys.argv[4]); free = kind == "free"; FIVE = [(1, 1), (2, 1), (0, 2), (3, 1), (1, 2), (4, 1), (2, 2), (0, 3)]
W = [1.0, 1.43, 2.0, 2.79, 4.0, 6.0, 12.0]; W = W if way == "up" else W[::-1]; sk = A.AirSkin(R, FIVE if free else L.NINE, B, free=free); out = []
a = np.array(json.load(open(f"s-{kind}-{B:g}-{W[0]:g}.json"))['rings'][str(R)]['a'])
for M in W:
    a, f = L.slp(sk, a if way == "up" else a * min(1.0, M / max(sk.mass(a), 1e-9)), M); out.append(dict(weight=M, miss=f, a=a.tolist(), used=sk.mass(a)))
    print(f"{kind} B = {B:g}, walking {way}, {R} rings, {M:g} skins: {100 * f:.4f}% (used {sk.mass(a):.2f})", flush=True)
json.dump(dict(walk=out), open(sys.argv[5], "w"))
