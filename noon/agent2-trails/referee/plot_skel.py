import sys, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0, "/home/agent2/referee-trails/noon_copy")
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from measure import measure, footmask
caps = ["0.3", "0.5", "0.6", "0.8"]
fig, axs = plt.subplots(2, 4, figsize=(22, 10))
for j, c in enumerate(caps):
    d = np.load(f"noon_copy/runs/instr-c{c}-s0.npz"); h = float(d['h'])
    m = footmask(d); L, skel, br, nodes = measure(m, h)
    img = np.ones(m.shape + (3,)); img[m] = [0.75, 0.75, 0.75]; img[skel] = [0.85, 0, 0]
    axs[0, j].imshow(img, origin='lower', interpolation='nearest'); axs[0, j].set_title(f"cap {c}: footstep mask (grey) + skeleton (red), L={L:.2f}")
    f6 = d['foot6']; pairs = [tuple(p) for p in d['pairs']]
    cw = sum(f6[pairs.index(p)] for p in [(0, 1), (1, 2), (2, 0)]); ccw = sum(f6[pairs.index(p)] for p in [(1, 0), (2, 1), (0, 2)])
    ref = np.percentile(d['foot'][d['foot'] > 0], 98)
    img = np.ones(m.shape + (3,)); a = cw > 0.1 * ref; b = ccw > 0.1 * ref
    img[a & ~b] = [0.9, 0.2, 0.2]; img[b & ~a] = [0.2, 0.2, 0.9]; img[a & b] = [0, 0, 0]
    axs[1, j].imshow(img, origin='lower', interpolation='nearest'); axs[1, j].set_title("0>1,1>2,2>0 red; 1>0,2>1,0>2 blue; both black")
plt.tight_layout(); plt.savefig("skel.png", dpi=70)
