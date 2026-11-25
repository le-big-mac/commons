import sys, numpy as np
from direction import load, profile, NB
dt = 1 / 320
print("== Q1: bound 1/sqrt(1-c^2) per walker, Noon's detour vs the same minus one time step (dt / straight distance)")
for c in ["0.1", "0.2", "0.3", "0.5", "0.8", "0.9"]:
    d = np.load(f"noon_copy/runs/instr-c{c}-s0.npz")
    det = d["detours"]; b = 1 / np.sqrt(1 - float(c) ** 2)
    print(f" cap {c}: bound {b:.4f}; Noon's mean {det.mean():.4f}, max {det.max():.4f}, walkers above bound {int((det > b).sum())}/{len(det)};"
          f" minus dt: mean {det.mean() - dt:.4f}, max {det.max() - dt:.4f}, above bound {int((det - dt > b + 1e-9).sum())}; min Noon's detour {det.min():.4f}")
print("== share of each edge's length (in steps of 1/50 of the edge) where the mean A->B path and the mean B->A path are more than k cells apart")
for c in ["0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9"]:
    gates, h, cl, det, cap = load(f"noon_copy/runs/instr-c{c}-s0.npz")
    fr = {1: [], 2: [], 3: [], 5: []}; sds = []
    for a, b in [(0, 1), (0, 2), (1, 2)]:
        cc = 3 - a - b
        mf, sf = profile(cl[(a, b)], gates[a], gates[b], gates[cc]); mb, sb = profile(cl[(b, a)], gates[a], gates[b], gates[cc])
        dd = np.abs(mf - mb)[1:-1] / h
        for k in fr: fr[k].append((dd > k).mean())
        sds.append(np.median(np.r_[sf[5:-5], sb[5:-5]]) / h)
    print(f" cap {c}: >1 cell {np.mean(fr[1]):.2f}, >2 cells {np.mean(fr[2]):.2f}, >3 cells {np.mean(fr[3]):.2f}, >5 cells {np.mean(fr[5]):.2f}; median lateral sd of one direction's footsteps {np.mean(sds):.2f} cells")
