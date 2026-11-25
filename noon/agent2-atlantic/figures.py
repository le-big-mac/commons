"""Figures for the fit of the South Atlantic.   usage: python -I figures.py results.npz OUTDIR"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from fit import latlon, unit, rotmat, w_of, BULLARD, DEPTHS

r = np.load(sys.argv[1])
OUT = sys.argv[2]
os.makedirs(OUT, exist_ok=True)
INK, MUTED, GRID = "#2b2622", "#6f675e", "#e4dfd6"
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
HALO = [pe.withStroke(linewidth=2.5, foreground="white")]
plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": INK, "axes.edgecolor": GRID, "axes.labelcolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED})
lats, lons, z = r['lats'], r['lons'], r['z']
w = r['w900']
Rm = rotmat(w)

fig = plt.figure(figsize=(13.2, 9.2))
ax = fig.add_axes([0.04, 0.13, 0.56, 0.76])
bx = fig.add_axes([0.68, 0.48, 0.3, 0.36])
# Africa as it is: land and shelf
LON, LAT = np.meshgrid(lons, lats)
ax.contourf(lons, lats, z, levels=[-900, 0, 9000], colors=["#dfe9f7", "#c9d8ee"], zorder=1)
# South America, rotated: land and shelf cells carried across as points
k = (LON < -34) & (LAT < 13) & (LAT > -56)
for lo_, hi_, col, size in ((-900, 0, "#fbe3d6", 5), (0, 9000, "#f6c9b3", 5)):
    m = k & (z > lo_) & (z <= hi_)
    v = unit(LAT[m][::3], LON[m][::3]) @ Rm.T
    la, lo = latlon(v)
    ax.scatter(lo, la, s=size, color=col, lw=0, zorder=2, rasterized=True)
for key, col, lw, zo in (("afr0", BLUE, 0.7, 4), ("afr900", BLUE, 2.2, 5)):
    la, lo = latlon(r[key])
    ax.plot(lo, la, color=col, lw=lw, zorder=zo)
for key, col, lw, zo in (("sam0", ORANGE, 0.7, 4), ("sam900", ORANGE, 2.2, 6)):
    la, lo = latlon(r[key] @ Rm.T)
    ax.plot(lo, la, color=col, lw=lw, zorder=zo)
la, lo = latlon(r["sam900"] @ rotmat(w_of(*BULLARD)).T)
ax.plot(lo, la, color=INK, lw=1.0, ls=(0, (4, 3)), zorder=7)
ax.set_xlim(-24, 26), ax.set_ylim(-44, 13), ax.set_aspect(1 / np.cos(np.radians(15)))
ax.set_xticks(range(-20, 21, 10)), ax.set_xticklabels([f"{abs(x)}°{'W' if x < 0 else 'E' if x > 0 else ''}" for x in range(-20, 21, 10)], fontsize=8.5)
ax.set_yticks(range(-40, 11, 10)), ax.set_yticklabels([f"{abs(y)}°{'S' if y < 0 else 'N' if y > 0 else ''}" for y in range(-40, 11, 10)], fontsize=8.5)
ax.tick_params(length=0)
for sp in ax.spines.values():
    sp.set_visible(False)
notes = [("Niger delta: built out since the\ncontinents parted; overlap of 330 km", (7.2, 5.6), (10.5, 9.5), "left"),
         ("Walvis ridge", (11.6, -19.5), (16.5, -17.5), "left"),
         ("ridge off Brazil at 20° S", (12.2, -7.6), (16.5, -5.5), "left"),
         ("the Guianas: nothing\nopposite them here", (-15.5, 4.6), (-21, -2.5), "left"),
         ("Argentina's shelf passes\nsouth of the Cape", (16.8, -37.0), (19.5, -41.5), "left")]
for text, xy, xt, ha in notes:
    ax.annotate(text, xy, xytext=xt, fontsize=9, color=INK, ha=ha, va="center", path_effects=HALO, zorder=9, arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.8))
ax.text(20, 1, "AFRICA", fontsize=13, color="#7d93b5", ha="center", fontweight="bold", zorder=3)
ax.text(-8, -14, "SOUTH AMERICA,\nturned 56.3°", fontsize=13, color="#c98a6c", ha="center", fontweight="bold", zorder=3)
ax.legend(handles=[Line2D([], [], color=BLUE, lw=2.2, label="Africa: the 900 m line (thin: the coast)"),
                   Line2D([], [], color=ORANGE, lw=2.2, label="South America, rotated to the best fit: its 900 m line (thin: its coast)"),
                   Line2D([], [], color=INK, lw=1, ls=(0, (4, 3)), label="South America's 900 m line under Bullard's rotation of 1965")],
          loc="upper left", bbox_to_anchor=(0.0, -0.035), frameon=False, fontsize=9)

# misfit against depth
mine = [float(r[f"f{d}"]) for d in DEPTHS]
bull = [float(r[f"fb{d}"]) for d in DEPTHS]
bx.plot(DEPTHS, mine, color=BLUE, lw=2, marker="o", ms=7, mec="white", mew=1.2, zorder=4)
bx.plot(DEPTHS, bull, color=ORANGE, lw=2, marker="o", ms=7, mec="white", mew=1.2, zorder=3)
fm = np.array([100, 500, 1000, 2000]) * 1.8288
bx.plot(fm, [140, 90, 85, 190], color=MUTED, lw=1.2, marker="s", ms=6, mfc="white", mew=1.3, zorder=2)
bx.set_ylim(0, 400), bx.set_xlim(-150, 3800)
bx.set_xlabel("depth of the line that is fitted (m)"), bx.set_ylabel("misfit (km)")
bx.grid(color=GRID, lw=0.8), bx.set_axisbelow(True), bx.tick_params(length=0)
for sp in ("top", "right"):
    bx.spines[sp].set_visible(False)
bx.set_title("The coast fits worst, the slope best", loc="left", fontsize=11, color=INK)
bx.text(60, mine[0] + 12, "coast", fontsize=9, color=INK)
fig.legend(handles=[Line2D([], [], color=BLUE, lw=2, marker="o", mec="white", label="the best rotation found here, at each depth"),
                    Line2D([], [], color=ORANGE, lw=2, marker="o", mec="white", label="Bullard's 1965 rotation, on today's depths"),
                    Line2D([], [], color=MUTED, lw=1.2, marker="s", mfc="white", label="Bullard's own table (his charts, his measure of misfit)")],
           loc="upper left", bbox_to_anchor=(0.665, 0.4), frameon=False, fontsize=9)
fig.text(0.68, 0.19, "Best fit at 900 m: 56.3° about 46.7° N, 31.2° W.\nBullard, Everett and Smith: 57.0° about 44.0° N, 30.6° W.\nThe two poles are 2.8° apart.", fontsize=10, color=INK, va="top", linespacing=1.5)
fig.suptitle("Closing the South Atlantic", x=0.04, y=0.975, ha="left", fontsize=16, color=INK)
fig.text(0.04, 0.925, "South America turned as one rigid piece on the sphere until the edge of its shelf meets the edge of Africa's. Africa is left where it is.",
         fontsize=10, color=MUTED)
fig.savefig(f"{OUT}/fit.png", dpi=125, facecolor="white")
