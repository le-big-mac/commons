"""The corrected figure of 26 November 2026: the refit on Bullard's own stretch.
usage: python -I figures2.py ends.npz fit.out ends4.out OUTDIR      (ends.npz from: ends.py GRID figdata ends.npz)"""
import sys, os, re
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.lines import Line2D
from fit import latlon, unit, rotmat, pole_of, DEPTHS

r = np.load(sys.argv[1])
OUT = sys.argv[4]
os.makedirs(OUT, exist_ok=True)
INK, MUTED, GRID = "#2b2622", "#6f675e", "#e4dfd6"
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
HALO = [pe.withStroke(linewidth=2.5, foreground="white")]
plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": INK, "axes.edgecolor": GRID, "axes.labelcolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED})
lats, lons, z = r['lats'], r['lons'], r['z']
w = r['w']; cut = float(r['cut'])
plat, plon, ang = pole_of(w)
Rm = rotmat(w)
# the two rows of misfits, read from the programs' own output
first = [float(m) for m in re.findall(r"^depth\s+\d+ m:.*?misfit ([\d.]+) km", open(sys.argv[2]).read(), flags=re.M)]
refit = [float(m) for m in re.findall(r"E\s+([\d.]+) km", open(sys.argv[3]).read())]
assert len(first) == len(refit) == len(DEPTHS), (first, refit)

fig = plt.figure(figsize=(13.2, 9.2))
ax = fig.add_axes([0.04, 0.13, 0.56, 0.76])
bx = fig.add_axes([0.68, 0.48, 0.3, 0.36])
LON, LAT = np.meshgrid(lons, lats)
ax.contourf(lons, lats, z, levels=[-900, 0, 9000], colors=["#dfe9f7", "#c9d8ee"], zorder=1)
k = (LON < -34) & (LAT < 13) & (LAT > -56)
for lo_, hi_, col, size in ((-900, 0, "#fbe3d6", 5), (0, 9000, "#f6c9b3", 5)):
    m = k & (z > lo_) & (z <= hi_)
    v = unit(LAT[m][::3], LON[m][::3]) @ Rm.T
    la, lo = latlon(v)
    ax.scatter(lo, la, s=size, color=col, lw=0, zorder=2, rasterized=True)
for key, lw, zo in (("afr0", 0.7, 4), ("afr900", 2.2, 5)):
    la, lo = latlon(r[key])
    ax.plot(lo, la, color=BLUE, lw=lw, zorder=zo)
la, lo = latlon(r["sam0"] @ Rm.T)
ax.plot(lo, la, color=ORANGE, lw=0.7, zorder=4)
la_s, _ = latlon(r["sam900"])
la, lo = latlon(r["sam900"] @ Rm.T)
fitted = la_s < cut
ax.plot(lo[fitted], la[fitted], color=ORANGE, lw=2.2, zorder=6)
ax.plot(lo[~fitted], la[~fitted], color=ORANGE, lw=2.2, ls=(0, (1.2, 1.6)), zorder=6)
ax.set_xlim(-24, 26), ax.set_ylim(-44, 13), ax.set_aspect(1 / np.cos(np.radians(15)))
ax.set_xticks(range(-20, 21, 10)), ax.set_xticklabels([f"{abs(x)}°{'W' if x < 0 else 'E' if x > 0 else ''}" for x in range(-20, 21, 10)], fontsize=8.5)
ax.set_yticks(range(-40, 11, 10)), ax.set_yticklabels([f"{abs(y)}°{'S' if y < 0 else 'N' if y > 0 else ''}" for y in range(-40, 11, 10)], fontsize=8.5)
ax.tick_params(length=0)
for sp in ax.spines.values():
    sp.set_visible(False)
notes = [("Niger delta: built out since the\ncontinents parted; overlap of 230 km", (6.6, 5.4), (10.5, 9.5), "left"),
         ("Walvis ridge: overlap of 130 km", (11.9, -19.3), (16.0, -17.5), "left"),
         ("ridge running out to Trindade (South\nAmerica's 20° S): overlap of 130 km", (12.6, -7.6), (16.0, -5.0), "left"),
         ("the Guianas (dotted, not fitted): 370 km out\nin the east, 750 in the west. No one turn\ncloses this and the rest", (-14.5, 4.15), (-23.0, -3.4), "left"),
         ("Guinea plateau, where the\nDemerara plateau belongs", (-16.6, 9.6), (-23.0, 6.4), "left"),
         ("Argentina: gaps of up to 190 km", (16.4, -35.5), (-2.0, -40.5), "left")]
for text, xy, xt, ha in notes:
    ax.annotate(text, xy, xytext=xt, fontsize=9, color=INK, ha=ha, va="center", path_effects=HALO, zorder=9, arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.8))
ax.text(20, 1, "AFRICA", fontsize=13, color="#7d93b5", ha="center", fontweight="bold", zorder=3)
ax.text(-8, -16, f"SOUTH AMERICA,\nturned {ang:.1f}°", fontsize=13, color="#c98a6c", ha="center", fontweight="bold", zorder=3)
ax.legend(handles=[Line2D([], [], color=BLUE, lw=2.2, label="Africa: the 900 m line (thin: the coast)"),
                   Line2D([], [], color=ORANGE, lw=2.2, label="South America, turned to the best fit of its 900 m line from the Amazon southward (thin: its coast)"),
                   Line2D([], [], color=ORANGE, lw=2.2, ls=(0, (1.2, 1.6)), label="the same line north of 2° N, which this turn was not asked to fit (Bullard's stretch ends about there)")],
          loc="upper left", bbox_to_anchor=(0.0, -0.035), frameon=False, fontsize=9)

bx.plot(DEPTHS, refit, color=BLUE, lw=2, marker="o", ms=7, mec="white", mew=1.2, zorder=4)
bx.plot(DEPTHS, first, color=AQUA, lw=2, marker="^", ms=7.5, mec="white", mew=1.2, zorder=3)
fm = np.array([100, 500, 1000, 2000]) * 1.8288
bx.plot(fm, [140, 90, 85, 190], color=MUTED, lw=1.2, marker="s", ms=6, mfc="white", mew=1.3, zorder=2)
bx.set_ylim(0, 250), bx.set_xlim(-150, 3800)
bx.set_xlabel("depth of the line that is fitted (m)"), bx.set_ylabel("misfit (km)")
bx.grid(color=GRID, lw=0.8), bx.set_axisbelow(True), bx.tick_params(length=0)
for sp in ("top", "right"):
    bx.spines[sp].set_visible(False)
bx.set_title("The coast fits worst", loc="left", fontsize=11, color=INK)
bx.text(0, first[0] + 14, "coast", fontsize=9, color=INK, va="center", ha="center")
fig.legend(handles=[Line2D([], [], color=BLUE, lw=2, marker="o", mec="white", label="best turn at each depth, from the Amazon southward"),
                    Line2D([], [], color=AQUA, lw=2, marker="^", mec="white", label="the same with the Guianas in (my first try)"),
                    Line2D([], [], color=MUTED, lw=1.2, marker="s", mfc="white", label="Bullard's table, fits 1 to 4 (his charts, his measure)")],
           loc="upper left", bbox_to_anchor=(0.665, 0.4), frameon=False, fontsize=9)
fig.text(0.68, 0.225, f"Best fit of the 900 m line from the Amazon\nsouthward: {ang:.1f}° about {plat:.1f}° N, {-plon:.1f}° W.\nBullard, Everett and Smith (1965):\n57.0° about 44.0° N, 30.6° W (their fit 9),\n57.1° about 42.9° N, 30.1° W (their fit 2).\nThis fit puts South America 20 to 37 km from\nwhere fit 9 does, and 4 to 55 km from fit 2.",
         fontsize=10, color=INK, va="top", linespacing=1.5)
fig.suptitle("Closing the South Atlantic", x=0.04, y=0.975, ha="left", fontsize=16, color=INK)
fig.text(0.04, 0.925, "South America turned as one rigid piece on the sphere until its 900 m line, from the Amazon southward, meets Africa's. Africa is left where it is.",
         fontsize=10, color=MUTED)
fig.savefig(f"{OUT}/fit-26nov.png", dpi=125, facecolor="white")
print("refit row:", refit, "first row:", first)
