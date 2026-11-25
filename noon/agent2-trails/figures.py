"""Figures for the trails (rewritten after the referee's report).   usage: python figures.py OUTDIR"""
import sys, os, warnings
warnings.filterwarnings("ignore")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.lines import Line2D
from matplotlib.colors import LinearSegmentedColormap
from measure import measure, footmask, STEINER_L, STEINER_D
OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
INK, MUTED, GRID = "#2b2622", "#6f675e", "#e4dfd6"
BLUE, ORANGE = "#2a78d6", "#eb6834"
HALO = [pe.withStroke(linewidth=2.5, foreground="white")]
plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": INK, "axes.edgecolor": GRID, "axes.labelcolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED,
                     "axes.spines.top": False, "axes.spines.right": False})
caps = ['0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9']
rows = []
fig, axes = plt.subplots(3, 3, figsize=(11.5, 10.6))
for ax, c in zip(axes.ravel(), caps):
    d = np.load(f'run-c{c}.npz')
    h = float(d['h'])
    L = measure(footmask(d), h)[0]
    Lc = measure(footmask(d), h, merge=4)[0]
    rows.append((float(c), L, Lc, float(d['detour']), float(d['route'])))
    lo, hi = d['lo'], d['hi']
    ax.imshow(d['G'], origin='lower', cmap='Greens_r', vmin=0, vmax=1.15, extent=[lo[0], hi[0], lo[1], hi[1]])
    ax.plot(d['gates'][:, 0], d['gates'][:, 1], ls='', marker='o', ms=7, color='white', mec=INK, mew=1.2)
    ax.set_title(f"a trail may turn a walker by up to {np.degrees(np.arcsin(float(c))):.0f}°", loc='left', fontsize=10.5, color=INK, pad=4)
    ax.set_xticks([]), ax.set_yticks([])
    ax.set_xlabel(f"routes {100 * (float(d['route']) - 1):.1f}% longer than straight", fontsize=10, color=INK, labelpad=4)
    for sp in ax.spines.values():
        sp.set_visible(False)
fig.suptitle("Desire paths on a triangular lawn, as trails grow more compelling", x=0.03, y=0.988, ha='left', fontsize=15, color=INK)
fig.text(0.03, 0.932, "Worn ground at the end of each run (pale = bare earth). Under each: how much longer the walkers' routes are than the straight line.\n"
         "A plain triangle would cost them nothing; the shortest possible network, a Y, 15.5%.", fontsize=9.5, color=MUTED)
fig.subplots_adjust(left=0.02, right=0.98, top=0.885, bottom=0.035, hspace=0.24, wspace=0.04)
fig.savefig(f"{OUT}/gallery.png", dpi=120, facecolor='white')
plt.close(fig)

r = np.array(rows)
ang = np.degrees(np.arcsin(r[:, 0]))
fig, (a, b) = plt.subplots(1, 2, figsize=(12.4, 5.2), gridspec_kw={"wspace": 0.22})
a.plot(ang, 100 * (r[:, 3] - 1), color=ORANGE, lw=2, marker='o', ms=6, mec='white', mew=1, zorder=3)
a.plot(ang, 100 * (r[:, 4] - 1), color=BLUE, lw=2, marker='o', ms=6, mec='white', mew=1, zorder=4)
a.axhline(100 * (STEINER_D - 1), color=INK, lw=1, ls=(0, (4, 3)), zorder=1)
a.text(6, 100 * (STEINER_D - 1) + 0.8, "what the shortest network, a Y, costs: 15.5%", fontsize=9, color=INK)
a.text(ang[-1] - 1, 100 * (r[-1, 3] - 1) - 1, "every step counted:\nincludes a zig-zag\nacross the trail", fontsize=9, color=INK, ha='right', va='top')
a.text(ang[-1] + 0.5, 100 * (r[-1, 4] - 1) - 2.6, "the route", fontsize=9.5, color=INK, ha='right')
a.set_ylim(0, 52), a.set_xlabel("how far a trail may turn a walker from the line of sight (°)"), a.set_ylabel("extra distance (%)")
a.grid(color=GRID, lw=0.8), a.set_axisbelow(True), a.tick_params(length=0)
a.set_title("How much further walkers go", loc='left', fontsize=11, color=INK)
b.plot(ang, r[:, 1], color=ORANGE, lw=2, marker='o', ms=6, mec='white', mew=1, zorder=3)
b.plot(ang, r[:, 2], color=BLUE, lw=2, marker='o', ms=6, mec='white', mew=1, zorder=4)
for lvl, name, dy in ((3.0, "a plain triangle: 3", 0.06), (STEINER_L, "the shortest network: 1.73", -0.2)):
    b.axhline(lvl, color=INK, lw=1, ls=(0, (4, 3)), zorder=1)
    b.text(5.5, lvl + dy, name, fontsize=9, color=INK, ha='left')
b.text(31, 4.25, "going and coming\ncounted as two trails", fontsize=9, color=INK, ha='center', va='bottom')
b.text(24, 2.25, "counted as one\nbroad trail", fontsize=9, color=INK, ha='center', va='top')
b.set_ylim(1.4, 4.9), b.set_xlabel("how far a trail may turn a walker from the line of sight (°)"), b.set_ylabel("length of trail (side of the lawn = 1)")
b.grid(color=GRID, lw=0.8), b.set_axisbelow(True), b.tick_params(length=0)
b.set_title("How much trail there is depends on what counts as one trail", loc='left', fontsize=11, color=INK)
fig.suptitle("The cost of the walkers' trails, to the walkers and to the gardener", x=0.055, y=0.985, ha='left', fontsize=14, color=INK)
fig.subplots_adjust(left=0.055, right=0.985, top=0.86, bottom=0.115)
fig.savefig(f"{OUT}/costs.png", dpi=130, facecolor='white')
plt.close(fig)

# going and coming at one setting: footsteps of walkers leaving the top gate, and of walkers arriving at it
d = np.load('run-c0.5.npz')
fp, pairs, lo, hi = d['foot_pair'], d['pairs'], d['lo'], d['hi']
top = 2
leave = sum(fp[k] for k, (x, y) in enumerate(pairs) if x == top)
arrive = sum(fp[k] for k, (x, y) in enumerate(pairs) if y == top)
fig, ax = plt.subplots(figsize=(7.4, 6.6))
ext = [lo[0], hi[0], lo[1], hi[1]]
for m, col in ((leave, ORANGE), (arrive, BLUE)):
    cm = LinearSegmentedColormap.from_list("c", [(1, 1, 1, 0), col])
    ax.imshow(np.clip(m / np.percentile(m[m > 0], 90), 0, 1), origin='lower', cmap=cm, extent=ext, zorder=2)
ax.plot(d['gates'][:, 0], d['gates'][:, 1], ls='', marker='o', ms=8, color='white', mec=INK, mew=1.3, zorder=4)
ax.set_xticks([]), ax.set_yticks([])
for sp in ax.spines.values():
    sp.set_visible(False)
ax.legend(handles=[Line2D([], [], color=ORANGE, lw=3, label="footsteps of walkers leaving the top gate"), Line2D([], [], color=BLUE, lw=3, label="footsteps of walkers arriving at it")],
          loc='lower center', bbox_to_anchor=(0.5, -0.08), frameon=False, fontsize=9.5, ncols=2)
ax.annotate("arriving walkers share\none stem into the gate", (0.5, 0.62), xytext=(0.70, 0.74), fontsize=9.5, color=INK, arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.8), path_effects=HALO)
ax.annotate("leaving walkers part\nat once, one each side", (0.455, 0.72), xytext=(0.03, 0.80), fontsize=9.5, color=INK, arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.8), path_effects=HALO)
fig.suptitle("Going and coming wear different trails", x=0.06, y=0.975, ha='left', fontsize=14, color=INK)
fig.text(0.06, 0.915, "The lawn where a trail may turn a walker by 30°. The two ways between two gates cross in the middle.", fontsize=9.5, color=MUTED)
fig.subplots_adjust(left=0.03, right=0.97, top=0.89, bottom=0.07)
fig.savefig(f"{OUT}/direction.png", dpi=130, facecolor='white')
with open('table.out', 'w') as f:
    f.write("cap  turn(deg)  route   walked  zig-zag  trail (two)  trail (one)\n")
    for c, L, Lc, D, R in rows:
        f.write(f"{c:.1f}  {np.degrees(np.arcsin(c)):5.1f}      {R:.4f}  {D:.4f}  {D - R:.4f}   {L:.2f}         {Lc:.2f}\n")
print(open('table.out').read())
