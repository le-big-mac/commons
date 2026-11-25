"""figures.py -- the study's two pictures.
river.png: (a) length over valley length through time, base case, four seeds; (b) its long-run mean against the cutoff
distance, one line for each P: the sealed grid and the runs added after it.
usage: python figures.py"""
import json, glob, math
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

INK, MUTED, GRID, SURF = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
BLUES = {2: "#9cc3ef", 3: "#5a9ae0", 4.5: "#2a6fc4", 6: "#163f73"}      # one hue, light to dark, for an ordered setting
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.edgecolor": MUTED, "axes.labelcolor": INK, "xtick.color": MUTED, "ytick.color": MUTED,
                     "axes.spines.top": False, "axes.spines.right": False, "figure.facecolor": SURF, "axes.facecolor": SURF, "savefig.facecolor": SURF})
G = json.load(open("out/grid/settings.json"))
fig, (a, b) = plt.subplots(1, 2, figsize=(12.5, 4.6), gridspec_kw={"width_ratios": [1.25, 1]})

# (a) four seeds of the base case
base = [r for r in G if r["P"] == 3 and r["DC"] == 0.4][0]
for k, f in enumerate(sorted(glob.glob("out/grid/P3-dc0.4-s*.out"))):
    r = np.array([[float(v) for v in l.split()[:3]] for l in open(f) if l.strip() and not l.startswith("#")])
    a.plot(r[:, 0], r[:, 2], lw=0.7, color=BLUES[3], alpha=0.9 if k == 0 else 0.45, zorder=3 if k == 0 else 2)
T = r[-1, 0]
a.axhline(math.pi, color="#b0892f", lw=1, ls=(0, (5, 4)), zorder=1); a.text(T * 1.005, math.pi, "π", color="#8a6a1c", va="center", fontsize=11)
a.axhline(base["Sbar"], color=INK, lw=1, zorder=4); a.text(T * 1.005, base["Sbar"], "%.2f" % base["Sbar"], color=INK, va="center", fontsize=9)
a.axvspan(T / 2, T, color="#000000", alpha=0.035, lw=0); a.text(T * 0.75, 1.12, "the half the mean is taken over", color=MUTED, ha="center", fontsize=8.5)
a.set_xlim(0, T); a.set_ylim(1, None); a.set_xlabel("time, in units of D²/(E b U)"); a.set_ylabel("river length ÷ valley length")
a.set_title("One setting, four rivers (P = 3, cutoff distance 0.4 D)", loc="left", fontsize=10.5, color=INK)
a.grid(axis="y", color=GRID, lw=0.6); a.set_axisbelow(True)

# (b) the long-run mean against the cutoff distance: the sealed grid (filled, four seeds) and the runs added after it (open, two seeds)
W = json.load(open("out/wide/settings.json")); A = [r for r in json.load(open("out/after/settings.json")) if r["seeds"] == 2 and r["DS"] == 0.1]
for P in (2, 3, 4.5, 6):
    rows = sorted([r for r in G if r["P"] == P and r["LX"] == 200] + [r for r in W if r["P"] == P] + [r for r in A if r["P"] == P], key=lambda r: r["DC"])
    x = [r["DC"] for r in rows]; y = [r["Sbar"] for r in rows]
    b.plot(x[:-1], y[:-1], color=BLUES[P], lw=2, zorder=3, label="P = %g" % P); b.plot(x[-2:], y[-2:], color=BLUES[P], lw=1.2, ls=(0, (2, 2)), zorder=3)
    for r in rows:
        sealed = r["seeds"] == 4; err = r["se"] if sealed else abs(r["each"][0] - r["each"][1]) / 2
        b.errorbar([r["DC"]], [r["Sbar"]], yerr=[err], color=BLUES[P], marker="o", ms=5.5, mfc=BLUES[P] if sealed else SURF, mec=SURF if sealed else BLUES[P], mew=1.3, capsize=2.5, elinewidth=1.1, zorder=4)
    b.text(x[-1] * 1.07, y[-1], "P = %g" % P, color=INK, va="center", fontsize=9)
b.axhline(math.pi, color="#b0892f", lw=1, ls=(0, (5, 4)), zorder=1); b.text(0.092, math.pi + 0.05, "π", color="#8a6a1c", va="bottom", ha="left", fontsize=11)
b.axvspan(0.17, 0.95, color="#000000", alpha=0.035, lw=0); b.text(0.4, 1.58, "the sealed grid", color=MUTED, ha="center", fontsize=8.5)
b.axvspan(2.25, 5.6, color="#b0892f", alpha=0.08, lw=0); b.text(3.55, 3.55, "here a rule of mine\ndecides most cuts,\nnot the river\n(Table 8)", color="#6f5514", ha="center", va="center", fontsize=8.5)
b.set_xscale("log"); b.set_xticks([0.1, 0.2, 0.4, 0.8, 1.6, 3.2]); b.set_xticklabels(["0.1", "0.2", "0.4", "0.8", "1.6", "3.2"]); b.minorticks_off(); b.set_xlim(0.085, 5.6); b.set_ylim(1.5, 4.1)
b.set_xlabel("cutoff distance, in units of D"); b.set_ylabel("long-run mean of river length ÷ valley length")
b.set_title("Thirty-six settings (filled: four seeds; open: two)", loc="left", fontsize=10.5, color=INK)
b.grid(axis="y", color=GRID, lw=0.6); b.set_axisbelow(True); b.legend(frameon=False, fontsize=9, loc="lower left", title="upstream weight", title_fontsize=8.5)
fig.tight_layout(); fig.savefig("river.png", dpi=110)
print("river.png written; base case mean %.3f; sealed grid from %.3f to %.3f; added runs from %.3f to %.3f" % (base["Sbar"], min(r["Sbar"] for r in G), max(r["Sbar"] for r in G), min(r["Sbar"] for r in W), max(r["Sbar"] for r in W)))
