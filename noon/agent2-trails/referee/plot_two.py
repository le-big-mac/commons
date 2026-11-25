import sys, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
fns = sys.argv[2:]
fig, axs = plt.subplots(len(fns), 2, figsize=(15, 3.6 * len(fns)))
axs = np.atleast_2d(axs)
for i, fn in enumerate(fns):
    d = np.load(fn); lo, hi = d['lo'], d['hi']; ext = [lo[0], hi[0], lo[1], hi[1]]
    axs[i, 0].imshow(d['G'], origin='lower', extent=ext, cmap='gray_r'); axs[i, 0].set_title(f"{fn.split('/')[-1]}: G at end")
    f6 = d['foot6']; ny, nx = f6[0].shape
    rgb = np.ones((ny, nx, 3)); a = np.clip(f6[0] / np.percentile(f6[0][f6[0] > 0], 90), 0, 1); b = np.clip(f6[1] / np.percentile(f6[1][f6[1] > 0], 90), 0, 1)
    rgb[..., 1] -= np.maximum(a, b); rgb[..., 2] -= a; rgb[..., 0] -= b
    axs[i, 1].imshow(np.clip(rgb, 0, 1), origin='lower', extent=ext); axs[i, 1].set_title("footsteps: gate0->gate1 red, gate1->gate0 blue")
    for ax in axs[i]:
        ax.plot(d['gates'][:, 0], d['gates'][:, 1], 'k^', ms=5)
plt.tight_layout(); plt.savefig(sys.argv[1], dpi=80)
