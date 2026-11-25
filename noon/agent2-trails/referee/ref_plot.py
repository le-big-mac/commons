import sys, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
GATES = np.array([[0.0, 0.0], [1.0, 0.0], [0.5, np.sqrt(3) / 2]])
outdir = sys.argv[1]; seed = int(sys.argv[2]); outpng = sys.argv[3]
caps = [float(c) for c in sys.argv[4:]] or [0.3, 0.5, 0.8]
fig, axs = plt.subplots(3, len(caps), figsize=(5.2*len(caps), 14))
axs = np.atleast_2d(axs).reshape(3, len(caps))
for j, c in enumerate(caps):
    r = np.load(f"{outdir}/run_c{c:.2f}_s{seed}.npz")
    h = float(r["h"]); x0 = float(r["x0"]); y0 = float(r["y0"]); nx, ny = r["G"].shape
    ext = [x0, x0 + nx*h, y0, y0 + ny*h]
    ax = axs[0, j]
    ax.imshow(r["Gmean"].T, origin="lower", extent=ext, cmap="gray_r", vmin=0, vmax=max(0.05, r["Gmean"].max()))
    ax.set_title(f"cap {c}: mean wear, last 40%  (detour {float(r['mean_detour']):.3f})")
    ax = axs[1, j]
    F = r["foot"]
    # edge 0-1: out red, back blue
    rgb = np.ones((ny, nx, 3))
    out = (F[0] + F[2] + F[4]).T; back = (F[1] + F[3] + F[5]).T
    out = np.clip(out / np.percentile(out[out > 0], 90), 0, 1); back = np.clip(back / np.percentile(back[back > 0], 90), 0, 1)
    rgb[..., 1] -= np.maximum(out, back); rgb[..., 2] -= out; rgb[..., 0] -= back
    ax.imshow(np.clip(rgb, 0, 1), origin="lower", extent=ext)
    ax.set_title("footsteps: lo->hi gate red, hi->lo gate blue")
    ax = axs[2, j]
    col = ["tab:red", "tab:blue", "tab:orange", "tab:cyan", "tab:purple", "tab:green"]
    for k in range(6):
        for q in range(int(r[f"ntrk{k}"])):
            tr = r[f"trk{k}_{q}"]
            ax.plot(tr[:, 0], tr[:, 1], color=col[k], lw=0.5, alpha=0.6)
    ax.set_title("last walkers' tracks (0>1 red, 1>0 blue, 0>2 orange,\n2>0 cyan, 1>2 purple, 2>1 green)")
    for a in axs[:, j]:
        a.plot(GATES[:, 0], GATES[:, 1], "k^", ms=5); a.set_aspect("equal")
        a.set_xlim(ext[0], ext[1]); a.set_ylim(ext[2], ext[3])
plt.tight_layout(); plt.savefig(outpng, dpi=75)
