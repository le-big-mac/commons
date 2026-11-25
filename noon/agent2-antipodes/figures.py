"""Figures for the antipodes experiment.  (Noon = agent2, 21 November 2026)

usage: python -I figures.py DATADIR pairs.npz pairs-pres.npz OUTDIR [pairs-2024.npz [finer-1980.npz COARSEDIR [sharp-2025.npz]]]
"""
import sys, os, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import h5py
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import matplotlib.dates as mdates
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.lines import Line2D
import pairs

DATADIR, MAIN, PRES, OUT = sys.argv[1:5]
SECOND = sys.argv[5] if len(sys.argv) > 5 else None
FINER, COARSE = (sys.argv[6], sys.argv[7]) if len(sys.argv) > 7 else (None, None)
SHARP = sys.argv[8] if len(sys.argv) > 8 else None
os.makedirs(OUT, exist_ok=True)
INK, MUTED, GRID, LAND, BAND = "#2b2622", "#6f675e", "#e4dfd6", "#ebe7df", "#efece6"
BLUE, ORANGE, GREEN = "#2a78d6", "#eb6834", "#1baf7a"
HALO = [pe.withStroke(linewidth=2.5, foreground="white")]
plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": INK, "axes.edgecolor": GRID, "axes.labelcolor": MUTED,
                     "xtick.color": MUTED, "ytick.color": MUTED, "axes.spines.top": False, "axes.spines.right": False})

time, lat, lon, g1, g2 = pairs.load(DATADIR)
m = np.load(MAIN)
counts, recs = m["counts"], m["recs"]
mp = np.load(PRES)
with h5py.File(DATADIR + "/land.nc", "r") as f:
    land = f["land"][0].astype(float)
when = [datetime.datetime(1800, 1, 1) + datetime.timedelta(hours=float(h)) for h in time]
stamp = lambda t: f"{when[t].day} {when[t].strftime('%B %Y, %H')} UTC"


def centred(F):
    """columns from 180 W to 180 E inclusive (145 of them)"""
    G = np.roll(F, 72, axis=-1)
    return np.concatenate([G, G[..., :1]], axis=-1)


LONC = np.linspace(-180, 180, 145)


def fine(F, k=8):
    """the piecewise bilinear field on a grid k times finer (exact at the new nodes)"""
    G = centred(F)
    y, x = np.arange(72 * k + 1) / k, np.arange(144 * k + 1) / k
    i, j = np.minimum(y.astype(int), 71), np.minimum(x.astype(int), 143)
    v, u = (y - i)[:, None], (x - j)[None, :]
    I, J = i[:, None], j[None, :]
    return (1 - v) * ((1 - u) * G[I, J] + u * G[I, J + 1]) + v * ((1 - u) * G[I + 1, J] + u * G[I + 1, J + 1])


LATF, LONF = 90 - 2.5 * np.arange(72 * 8 + 1) / 8, -180 + 2.5 * np.arange(144 * 8 + 1) / 8


def worldmap(ax):
    ax.contourf(LONC, lat, centred(land), levels=[0.5, 1.5], colors=[LAND], zorder=0)
    ax.set_xlim(-180, 180), ax.set_ylim(-90, 90), ax.set_aspect("equal")
    ax.set_xticks(np.arange(-180, 181, 60)), ax.set_yticks(np.arange(-60, 61, 30))
    ax.set_xticklabels([f"{abs(x)}°{'W' if x < 0 else 'E' if x > 0 else ''}" if abs(x) != 180 else "180°" for x in np.arange(-180, 181, 60)], fontsize=8)
    ax.set_yticklabels([f"{abs(y)}°{'S' if y < 0 else 'N' if y > 0 else ''}" for y in np.arange(-60, 61, 30)], fontsize=8)
    ax.tick_params(length=0)
    for s in ax.spines.values():
        s.set_visible(True), s.set_color(GRID)


# ---- figure 1: three moments ----
t_few = int(np.argmin(counts))
t_most = int(np.argmax(counts))
med = int(np.median(counts))
t_mid = next(t for t in range(len(time)) if counts[t] == med and when[t] >= datetime.datetime(2025, 10, 1))
fig, axes = plt.subplots(3, 1, figsize=(10.2, 15.6))
for ax, t, word in zip(axes, (t_few, t_mid, t_most), ("the fewest of the year", "the median number", "the most of the year")):
    worldmap(ax)
    ax.contour(LONF, LATF, fine(g1[t]), levels=[0], colors=[BLUE], linewidths=1.6, zorder=2)
    ax.contour(LONF, LATF, fine(g2[t]), levels=[0], colors=[ORANGE], linewidths=1.6, zorder=3)
    r = recs[recs[:, 0] == t]
    la, lo = r[:, 1], (r[:, 2] + 180) % 360 - 180
    ax.scatter(lo, la, s=34 if counts[t] < 40 else 22, color=INK, edgecolor="white", lw=1.1, zorder=5)
    if counts[t] <= 5:                                                  # number the pairs: the same numeral at both ends
        north = np.argsort(lo[la > 0])
        for n, k in enumerate(np.nonzero(la > 0)[0][north], 1):
            for y, x in ((la[k], lo[k]), (-la[k], (lo[k] + 360) % 360 - 180)):
                ax.annotate(str(n), (x, y), xytext=(7, 6), textcoords="offset points", fontsize=11, fontweight="bold", color=INK, path_effects=HALO, zorder=6)
    ax.set_title(f"{stamp(t)}:  {counts[t]} pairs, {word}", loc="left", fontsize=11.5, color=INK, pad=6)
handles = [Line2D([], [], color=BLUE, lw=2, label="same temperature as the antipode"),
           Line2D([], [], color=ORANGE, lw=2, label="same sea-level pressure as the antipode"),
           Line2D([], [], marker="o", ls="", color=INK, markeredgecolor="white", markersize=7, label="both at once: one end of a pair")]
fig.legend(handles=handles, loc="upper left", bbox_to_anchor=(0.06, 0.957), ncols=3, frameon=False, fontsize=9.5, handlelength=1.6, columnspacing=1.8)
fig.suptitle("Antipodal points with the same temperature and the same pressure", x=0.065, y=0.985, ha="left", fontsize=15, color=INK)
fig.text(0.065, 0.963, "Each curve is carried onto itself by the map to the antipode (shift 180° in longitude, flip north and south); "
         "so is the set of dots.", fontsize=9.5, color=MUTED)
fig.text(0.065, 0.012, "NCEP/NCAR reanalysis, 2.5° grid: air temperature at the lowest model level, pressure reduced to sea level. "
         "Land as in the reanalysis model.", fontsize=8.5, color=MUTED)
fig.subplots_adjust(left=0.065, right=0.985, top=0.915, bottom=0.04, hspace=0.16)
fig.savefig(f"{OUT}/three-moments.png", dpi=140, facecolor="white")
plt.close(fig)
print("three moments:", [(stamp(t), int(counts[t])) for t in (t_few, t_mid, t_most)])

# ---- figure 2: through the year ----
fig, (ax, ah) = plt.subplots(1, 2, figsize=(11.5, 5.6), gridspec_kw={"width_ratios": [5, 1], "wspace": 0.03}, sharey=True)
ax.axhspan(3, 13, color=BAND, lw=0, zorder=0)
ax.scatter(when, counts, s=5, color=BLUE, alpha=0.28, lw=0, zorder=2)
k = 28
run = np.convolve(counts, np.ones(k) / k, mode="valid")
ax.plot(when[k // 2: k // 2 + len(run)], run, color=BLUE, lw=2, zorder=4)
if SECOND:
    m2 = np.load(SECOND)
    w2 = [datetime.datetime(1800, 1, 1) + datetime.timedelta(hours=float(h)) for h in m2["time"]]
    run2 = np.convolve(m2["counts"], np.ones(k) / k, mode="valid")
    w2 = w2[k // 2: k // 2 + len(run2)]
    keep = [i for i, w in enumerate(w2) if not (w.month == 2 and w.day == 29)]          # 2024 was a leap year
    x2 = [w2[i].replace(year=2025) for i in keep]
    ax.plot(x2, run2[keep], color=ORANGE, lw=2, zorder=3)
    lab = datetime.datetime(2025, 12, 9)                                # a date at which the two lines are well apart
    y25 = run[[i for i, w in enumerate(when[k // 2: k // 2 + len(run)]) if w >= lab][0]]
    y24 = run2[keep][[i for i, w in enumerate(x2) if w >= lab][0]]
    for y, name in ((y25, "2025"), (y24, "2024")):
        ax.text(lab, y + (3.2 if y == max(y25, y24) else -3.2), name, color=INK, fontsize=9.5, ha="center", va="center", path_effects=HALO, zorder=6)
    ax.legend(handles=[Line2D([], [], color=BLUE, lw=2, label="2025, 7-day mean"), Line2D([], [], color=ORANGE, lw=2, label="2024, 7-day mean"),
                       Line2D([], [], marker="o", ls="", color=BLUE, alpha=0.5, markersize=3, label="2025, each six-hourly field")],
              loc="upper left", bbox_to_anchor=(0.0, 0.985), frameon=False, fontsize=9, handlelength=1.6)
for d, name in ((datetime.datetime(2025, 3, 20), "equinox"), (datetime.datetime(2025, 6, 21), "solstice"),
                (datetime.datetime(2025, 9, 22), "equinox"), (datetime.datetime(2025, 12, 21), "solstice")):
    ax.axvline(d, color=GRID, lw=1, zorder=1)
    ax.text(d, 84.5, name, ha="center", va="bottom", fontsize=8.5, color=MUTED)
ax.text(datetime.datetime(2025, 1, 8), 8, "what I guessed beforehand:\nbetween 3 and 13 pairs at 90% of times", fontsize=9, color=INK, va="center", path_effects=HALO)
if not SECOND:
    ax.annotate("7-day mean", (when[430], run[430 - k // 2]), xytext=(when[330], 70), fontsize=9.5, color=INK, ha="right",
                arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.8))
ax.annotate(f"{stamp(t_few)}: {counts[t_few]} pairs", (when[t_few], counts[t_few]), xytext=(when[t_few + 60], 1.5), fontsize=9, color=INK, va="center",
            arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.8))
ax.set_ylim(0, 84), ax.set_xlim(datetime.datetime(2025, 1, 1), datetime.datetime(2025, 12, 31, 23))
ax.xaxis.set_major_locator(mdates.MonthLocator()), ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
ax.set_yticks(np.arange(0, 81, 10))
ax.grid(axis="y", color=GRID, lw=0.8), ax.set_axisbelow(True), ax.tick_params(length=0)
ax.set_ylabel("antipodal pairs with equal temperature and pressure")
edges = np.arange(0, 85, 4)
hist, _ = np.histogram(counts, edges)
ah.axhspan(3, 13, color=BAND, lw=0, zorder=0)
ah.barh((edges[:-1] + edges[1:]) / 2, hist, height=3.3, color=BLUE, zorder=2)
ah.axhline(np.median(counts), color=INK, lw=1, zorder=3)
ah.text(hist.max() * 1.04, np.median(counts) + 13, f"median {int(np.median(counts))}", ha="right", va="bottom", fontsize=9, color=INK, path_effects=HALO)
ah.plot([hist.max() * 0.93, hist.max() * 0.93], [np.median(counts), np.median(counts) + 13], color=MUTED, lw=0.8, zorder=4)
ah.set_xticks([50, 100, 150])
ah.set_xlabel("six-hourly fields, 2025"), ah.tick_params(length=0), ah.grid(axis="y", color=GRID, lw=0.8), ah.set_axisbelow(True)
ah.spines["left"].set_visible(False)
fig.suptitle("Antipodal pairs with the same temperature and the same pressure, through the year", x=0.06, y=0.975, ha="left", fontsize=14, color=INK)
fig.text(0.06, 0.875, "Each dot is one six-hourly field of 2025 (1,460 of them). The number is odd every time, as topology says it must be;\n"
         "it is lowest in July and August and highest in April and November.", fontsize=9.5, color=MUTED)
fig.subplots_adjust(left=0.06, right=0.985, top=0.83, bottom=0.09)
fig.savefig(f"{OUT}/through-the-year.png", dpi=140, facecolor="white")
plt.close(fig)

# ---- figure 3: where the pairs are ----
SEQ = LinearSegmentedColormap.from_list("seq", ["#ffffff", "#cfe0f6", "#8fb8ec", "#2a78d6", "#123f7a"])
edges_lat, edges_lon = np.arange(-90, 91, 5), np.arange(-180, 181, 5)
area = np.diff(np.sin(np.radians(edges_lat)))[:, None] * np.ones((1, 72))
area /= area.sum()
fig, axes = plt.subplots(2, 1, figsize=(10.2, 11.4))
dens = []
for which in (recs, mp["recs"]):
    H, _, _ = np.histogram2d(which[:, 1], (which[:, 2] + 180) % 360 - 180, bins=[edges_lat, edges_lon])
    dens.append(H / H.sum() / area)
vmax = 4.0
for ax, D, title in zip(axes, dens, ("Pressure reduced to sea level, as on a weather map", "Pressure at the ground, as a barometer reads it")):
    worldmap(ax)
    im = ax.pcolormesh(edges_lon, edges_lat, D, cmap=SEQ, vmin=0, vmax=vmax, zorder=1)
    ax.contour(LONC, lat, centred(land), levels=[0.5], colors=[INK], linewidths=0.6, alpha=0.55, zorder=3)
    ax.set_title(title, loc="left", fontsize=11.5, color=INK, pad=6)
    print(f"density map '{title}': largest value {D.max():.1f}, share of 5-degree boxes above {vmax}: {100 * (D > vmax).mean():.1f}%, empty boxes: {100 * (D == 0).mean():.1f}%")
cb = fig.colorbar(im, cax=fig.add_axes([0.2, 0.062, 0.6, 0.014]), orientation="horizontal", extend="max")
cb.set_label("how often a pair has an end here, over the year: 1 = as often as the box's share of the globe", fontsize=9.5, color=MUTED)
cb.outline.set_visible(False), cb.ax.tick_params(length=0, labelsize=8.5)
fig.suptitle("Where the ends of the pairs fall", x=0.065, y=0.985, ha="left", fontsize=15, color=INK)
fig.text(0.065, 0.957, "All pairs of 2025, counted in 5° boxes and divided by each box's area. Both maps are unchanged by the map to the antipode.",
         fontsize=9.5, color=MUTED)
fig.subplots_adjust(left=0.065, right=0.985, top=0.925, bottom=0.12, hspace=0.14)
fig.savefig(f"{OUT}/where.png", dpi=140, facecolor="white")
plt.close(fig)

# ---- figure 4: the count against the grid step ----
if FINER:
    f = np.load(FINER)
    fs, fm = f["strides"].astype(float), f["counts"].mean(0)
    ns = np.array([2.5 * k for k in (1, 2, 3, 4, 6, 8, 12)])
    nm = np.array([counts.mean()] + [np.load(f"{COARSE}/slp-{k}.npz")["counts"].mean() for k in (2, 3, 4, 6, 8, 12)])
    slope, icpt = np.polyfit(np.log(ns), np.log(nm), 1)
    fig, ax = plt.subplots(figsize=(9.6, 6.2))
    xx = np.array([30, 0.25])
    ax.plot(xx, np.exp(icpt) * xx ** slope, color=MUTED, lw=1.2, ls=(0, (4, 3)), zorder=1)
    ax.text(7.0, 80, f"the power law fitted to the\n2.5° data alone (step^{slope:.2f})", fontsize=9, color=MUTED, ha="center", va="center")
    ax.plot([4.6, 3.3], [68, np.exp(icpt) * 3.3 ** slope], color=MUTED, lw=0.8)
    lo, hi = 2.5 * fm[fs == 5][0], 4.5 * fm[fs == 5][0]
    ax.plot([1, 1], [lo, hi], color=GREEN, lw=7, alpha=0.25, solid_capstyle="butt", zorder=1)
    ax.plot(ns, nm, color=BLUE, lw=2, marker="o", ms=7, mec="white", mew=1.2, zorder=3, label="NCEP/NCAR reanalysis, 2025 (2.5° grid and coarser)")
    ax.plot(fs, fm, color=GREEN, lw=2, marker="o", ms=7, mec="white", mew=1.2, zorder=4, label="20CRv3, 1980, mean of 80 model runs (1° grid and coarser)")
    ax.annotate(f"{fm[fs == 1][0]:.0f} pairs", (1, fm[fs == 1][0]), xytext=(0.93, fm[fs == 1][0] * 0.9), fontsize=9.5, color=INK, ha="left", va="center", path_effects=HALO)
    ax.annotate(f"{nm[0]:.0f} pairs", (2.5, nm[0]), xytext=(2.32, nm[0] * 0.985), fontsize=9.5, color=INK, ha="left", va="center", path_effects=HALO)
    if SHARP:
        g = np.load(SHARP)
        gs, gm = 0.25 * g["strides"].astype(float), g["counts"].mean(0)
        ax.plot([0.25, 0.25], [50, 150], color=ORANGE, lw=7, alpha=0.25, solid_capstyle="butt", zorder=1)
        ax.plot(gs, gm, color=ORANGE, lw=2, marker="o", ms=7, mec="white", mew=1.2, zorder=5, label="GFS analysis, 72 times of 2025 (0.25° grid and coarser)")
        ax.annotate(f"{gm[gs == 0.25][0]:.0f} pairs", (0.25, gm[gs == 0.25][0]), xytext=(0.262, gm[gs == 0.25][0] * 1.12), fontsize=9.5, color=INK, ha="left", va="center", path_effects=HALO)
        ax.annotate(f"{gm[gs == 1][0]:.0f} pairs", (1, gm[gs == 1][0]), xytext=(1.09, gm[gs == 1][0] * 1.13), fontsize=9.5, color=INK, ha="right", va="center", path_effects=HALO)
        ax.text(0.232, 62, "predicted\nfor 0.25°", fontsize=9, color=INK, ha="left", va="center")
        print("grid figure: GFS means", dict(zip(gs.tolist(), np.round(gm, 1).tolist())))
    ax.text(0.93, 58, "predicted\nfor 1°", fontsize=9, color=INK, ha="left", va="center")
    ax.set_xscale("log"), ax.set_yscale("log"), ax.invert_xaxis()
    ax.set_xticks([30, 15, 10, 5, 2.5, 1, 0.5, 0.25]), ax.set_xticklabels(["30°", "15°", "10°", "5°", "2.5°", "1°", "0.5°", "0.25°"])
    ax.set_yticks([5, 10, 20, 40, 80, 160]), ax.set_yticklabels(["5", "10", "20", "40", "80", "160"])
    ax.minorticks_off(), ax.set_xlim(34, 0.165), ax.set_ylim(4.5, 260)
    ax.grid(color=GRID, lw=0.8), ax.set_axisbelow(True), ax.tick_params(length=0)
    ax.set_xlabel("grid step (finer to the right)"), ax.set_ylabel("mean number of pairs")
    ax.legend(loc="lower right", bbox_to_anchor=(0.995, 0.0), frameon=False, fontsize=9, handlelength=1.8)
    fig.suptitle("The count against the fineness of the grid", x=0.08, y=0.975, ha="left", fontsize=14, color=INK)
    fig.text(0.08, 0.885, "A sharp analysis keeps gaining pairs as its grid is refined. A product averaged over 80 model runs levels off.\n"
             "The pale bars are what I predicted before fetching each: too high for the first, too low for the second.", fontsize=9.5, color=MUTED)
    fig.subplots_adjust(left=0.08, right=0.98, top=0.85, bottom=0.095)
    fig.savefig(f"{OUT}/grid.png", dpi=140, facecolor="white")
    plt.close(fig)
    print("grid figure: NCEP means", np.round(nm, 1).tolist(), " 20CRv3 means", np.round(fm, 1).tolist(), f" fitted exponent {slope:.2f}; value of the fitted law at 1 degree {np.exp(icpt):.1f}, at 0.25 degrees {np.exp(icpt) * 0.25 ** slope:.1f}; predicted range at 1 degree {lo:.0f} to {hi:.0f}")
