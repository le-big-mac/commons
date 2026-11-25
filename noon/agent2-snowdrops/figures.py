"""Figures for the snowdrops.   usage: python -I figures.py results.npz OUTDIR"""
import sys, os, datetime
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.lines import Line2D

r = np.load(sys.argv[1])
OUT = sys.argv[2]
os.makedirs(OUT, exist_ok=True)
INK, MUTED, GRID = "#2b2622", "#6f675e", "#e4dfd6"
BLUE, ORANGE = "#2a78d6", "#eb6834"
HALO = [pe.withStroke(linewidth=2.5, foreground="white")]
plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": INK, "axes.edgecolor": GRID, "axes.labelcolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED,
                     "axes.spines.top": False, "axes.spines.right": False})
years, yearly, tjf = r['years'], r['yearly2'], r['tjf']       # stations and years fitted together (the series the referee's checks support)
date = lambda d: (datetime.date(2023, 1, 1) + datetime.timedelta(days=int(round(d)) - 1)).strftime("%-d %b")
DAYTICKS = [32, 46, 60, 74, 88]

# ---- figure 1: the years, and winter warmth
fig, (a, b) = plt.subplots(1, 2, figsize=(12.4, 5.3), gridspec_kw={"width_ratios": [1.55, 1], "wspace": 0.2})
a.scatter(years, yearly, s=26, color=BLUE, edgecolor="white", lw=0.8, zorder=3)
k = 11
run = np.convolve(yearly, np.ones(k) / k, mode="valid")
a.plot(years[k // 2: k // 2 + len(run)], run, color=BLUE, lw=2, zorder=2)
a.text(years[k // 2 + 3], run[3] + 3.2, "11-year mean", fontsize=9, color=INK, path_effects=HALO)
for y in (1963, 2008, 1996, 2020):
    i = int(np.nonzero(years == y)[0][0])
    a.annotate(f"{y}: {date(yearly[i])}", (y, yearly[i]), xytext=(0, 9 if yearly[i] > 60 else -15), textcoords="offset points", ha="center", fontsize=9, color=INK, path_effects=HALO)
a.set_yticks(DAYTICKS), a.set_yticklabels([date(d) for d in DAYTICKS]), a.set_ylim(30, 90)
a.grid(axis="y", color=GRID, lw=0.8), a.set_axisbelow(True), a.tick_params(length=0)
a.set_title("First snowdrop flowers, Germany, year by year", loc="left", fontsize=11, color=INK)
b.scatter(tjf, yearly, s=26, color=BLUE, edgecolor="white", lw=0.8, zorder=3)
cf = np.polyfit(tjf, yearly, 1)
xx = np.array([tjf.min() - 0.3, tjf.max() + 0.3])
b.plot(xx, np.polyval(cf, xx), color=INK, lw=1.2, zorder=2)
b.text(0.2, 84, f"{-cf[0]:.1f} days earlier\nper degree", fontsize=9.5, color=INK, ha="left", va="center")
for y in (1963, 2008, 2020, 1996):
    i = int(np.nonzero(years == y)[0][0])
    b.annotate(str(y), (tjf[i], yearly[i]), xytext=(6, 4), textcoords="offset points", fontsize=9, color=INK, path_effects=HALO)
b.set_yticks(DAYTICKS), b.set_yticklabels([date(d) for d in DAYTICKS]), b.set_ylim(30, 90)
b.set_xlabel("mean temperature of January and February, Germany (°C)")
b.grid(color=GRID, lw=0.8), b.set_axisbelow(True), b.tick_params(length=0)
b.set_title("The same years against winter warmth", loc="left", fontsize=11, color=INK)
fig.suptitle("The snowdrops come when the winter lets them", x=0.055, y=0.985, ha="left", fontsize=15, color=INK)
fig.text(0.055, 0.905, f"{int(r['st_n'].sum()):,} records from {len(r['st_id']):,} stations of the German weather service, 1951 to 2023. Each dot is one year: "
         "a level for every station and every year, fitted together.", fontsize=9.5, color=MUTED)
fig.subplots_adjust(left=0.065, right=0.985, top=0.83, bottom=0.11)
fig.savefig(f"{OUT}/years.png", dpi=130, facecolor="white")
plt.close(fig)

# ---- figure 2: the map
SEQ = LinearSegmentedColormap.from_list("seq", ["#e3eefb", "#9ec5f4", "#5598e7", "#256abf", "#0d366b"])
lat, lon, eff, alt = r['st_lat'], r['st_lon'], r['st_eff'], r['st_alt']
fig, ax = plt.subplots(figsize=(7.6, 9.4))
order = np.argsort(eff)
sc = ax.scatter(lon[order], lat[order], c=eff[order], s=9, cmap=SEQ, vmin=40, vmax=80, lw=0, zorder=2)
ax.set_aspect(1 / np.cos(np.radians(51)))
ax.set_xticks(range(6, 16, 2)), ax.set_xticklabels([f"{x}° E" for x in range(6, 16, 2)], fontsize=8.5)
ax.set_yticks(range(48, 56, 2)), ax.set_yticklabels([f"{y}° N" for y in range(48, 56, 2)], fontsize=8.5)
ax.tick_params(length=0)
for sp in ax.spines.values():
    sp.set_visible(False)
for name, x, y, ha in (("upper Rhine", 7.75, 48.55, "right"), ("Cologne lowland", 6.55, 50.9, "right"), ("Alps", 11.2, 47.42, "center"), ("Ore Mountains", 13.1, 50.42, "center"),
                       ("Baltic coast", 12.6, 54.4, "center"), ("Harz", 10.7, 51.82, "center"), ("Black Forest", 8.2, 47.95, "center")):
    ax.text(x, y, name, fontsize=9, color=INK, ha=ha, va="center", path_effects=HALO, zorder=4)
cb = fig.colorbar(sc, ax=ax, orientation="horizontal", fraction=0.035, pad=0.06, aspect=40, extend="both", ticks=[46, 53, 60, 67, 74])
cb.ax.set_xticklabels([date(d) for d in (46, 53, 60, 67, 74)])
cb.set_label("usual date of the first snowdrop flowers (year-to-year swings removed)", fontsize=9.5, color=MUTED)
cb.outline.set_visible(False), cb.ax.tick_params(length=0, labelsize=8.5)
fig.suptitle("Where the snowdrops come first", x=0.06, y=0.985, ha="left", fontsize=15, color=INK)
fig.text(0.06, 0.925, f"Each dot is a station with 15 or more years of records ({len(lat):,} of them). There is no map underneath:\nthe stations draw the country.", fontsize=9.5, color=MUTED)
fig.subplots_adjust(left=0.09, right=0.97, top=0.9, bottom=0.03)
fig.savefig(f"{OUT}/map.png", dpi=130, facecolor="white")
plt.close(fig)

# ---- figure 3: Hopkins
coef = r['coef']
hop = [4 / (400 * 0.3048 / 100), 4.0, 0.8]
X = [alt / 100.0, lat, lon]
labels = ["altitude (m)", "latitude (° N)", "longitude (° E)"]
units = ["per 100 m up", "per degree north", "per degree east"]
edges = [np.array([0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 600, 700, 850]) / 100.0, np.arange(47.5, 55.01, 0.5), np.arange(6, 15.01, 0.75)]
fig, axes = plt.subplots(1, 3, figsize=(13, 4.9), sharey=True, gridspec_kw={"wspace": 0.06})
for j, ax in enumerate(axes):
    others = sum(coef[i] * (X[i] - X[i].mean()) for i in range(3) if i != j)
    part = eff - others                                                 # the station's date with the other two effects taken out
    xs, ys, ns = [], [], []
    for lo_, hi_ in zip(edges[j][:-1], edges[j][1:]):
        m = (X[j] >= lo_) & (X[j] < hi_)
        if m.sum() >= 8:
            xs.append(X[j][m].mean()), ys.append(part[m].mean()), ns.append(m.sum())
    xs, ys = np.array(xs), np.array(ys)
    scale = 100 if j == 0 else 1
    x0 = X[j].mean()
    y0 = part.mean()
    xx = np.array([xs.min(), xs.max()])
    ax.plot(xx * scale, y0 + hop[j] * (xx - x0), color=ORANGE, lw=2, zorder=2)
    ax.plot(xx * scale, y0 + coef[j] * (xx - x0), color=BLUE, lw=2, zorder=3)
    ax.scatter(xs * scale, ys, s=np.clip(np.array(ns) / 6, 14, 90), color=BLUE, edgecolor="white", lw=0.9, zorder=4)
    ax.set_xlabel(labels[j])
    ax.set_title(f"{coef[j]:.1f} days later {units[j]}  (Hopkins: {hop[j]:.1f})", loc="left", fontsize=10.5, color=INK)
    ax.grid(color=GRID, lw=0.8), ax.set_axisbelow(True), ax.tick_params(length=0)
axes[0].set_yticks([39, 46, 53, 60, 67, 74, 81]), axes[0].set_yticklabels([date(d) for d in (39, 46, 53, 60, 67, 74, 81)])
fig.legend(handles=[Line2D([], [], color=BLUE, lw=2, marker="o", mec="white", label="the snowdrop records: stations grouped, other two effects taken out; line fitted to all records"),
                    Line2D([], [], color=ORANGE, lw=2, label="Hopkins's law of 1918: 4 days per degree north, per 5 degrees east, per 400 feet up")],
           loc="upper left", bbox_to_anchor=(0.045, 0.9), frameon=False, fontsize=9.5, ncols=1)
fig.suptitle("Hopkins's law, tried on German snowdrops", x=0.05, y=0.985, ha="left", fontsize=15, color=INK)
fig.subplots_adjust(left=0.065, right=0.985, top=0.71, bottom=0.115)
fig.savefig(f"{OUT}/hopkins.png", dpi=130, facecolor="white")
