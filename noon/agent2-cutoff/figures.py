"""The figure.   usage: python -I figures.py profiles.json cutoff.png"""
import sys, json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
P = json.load(open(sys.argv[1])); ORDER = ["hep-th", "hep-ph", "astro-ph", "gr-qc", "quant-ph", "cs.CL", "maths"]
NAMES = {"hep-th": "hep-th (high-energy theory)", "hep-ph": "hep-ph (high-energy phenomenology)", "astro-ph": "astro-ph (astrophysics)", "gr-qc": "gr-qc (gravity)", "quant-ph": "quant-ph (quantum physics)", "cs.CL": "cs.CL (language and computation)", "maths": "math.CO and math.AP (two of maths)"}
INK, MUTED, GRID, BLUE, ORANGE, NEUTRAL = "#2b2622", "#6f675e", "#e4dfd6", "#2a78d6", "#eb6834", "#b9b1a5"
plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": INK, "axes.edgecolor": GRID, "axes.labelcolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED, "font.size": 9.5})
fig = plt.figure(figsize=(12.4, 9.2)); FLOOR = 0.3
for k, g in enumerate(ORDER):
    row, col = divmod(k, 4); ax = fig.add_axes([0.065 + col * 0.235, 0.60 - row * 0.275, 0.205, 0.20]); n = P[g]["n"]; pm = np.array(P[g]["per_minute"], float); x = np.arange(-60, 60); lvl = n / 1440.0; y = np.maximum(pm / lvl, FLOOR); sel = (x >= -30) & (x < 30)
    ax.axhline(1, color=NEUTRAL, lw=1, ls=(0, (4, 3))); ax.axvline(0, color=MUTED, lw=0.8, ls=(0, (1, 2)))
    b = sel & (x < 0); a = sel & (x >= 0); ax.step(x[b], y[b], where='post', color=ORANGE, lw=1.6); ax.step(x[a], y[a], where='post', color=BLUE, lw=1.6)
    ax.set_yscale('log'); ax.set_ylim(FLOOR, 500); ax.set_xlim(-30, 30); ax.set_xticks([-30, -15, 0, 15, 30]); ax.set_xticklabels(["13:30", "13:45", "14:00", "14:15", "14:30"], fontsize=8); ax.set_yticks([1, 10, 100]); ax.set_yticklabels(["1", "10", "100"] if col == 0 else [])
    ax.grid(color=GRID, lw=0.8); ax.set_axisbelow(True); ax.tick_params(length=0, which='both')
    for sp in ax.spines.values(): sp.set_visible(False)
    ax.set_title(NAMES[g], loc='left', fontsize=9.3, color=INK, pad=5); fm = pm[60]; lm = pm[59]
    if col == 0: ax.set_ylabel("papers a minute,\ntimes a level day", fontsize=8.5)
ax = fig.add_axes([0.77, 0.325, 0.205, 0.20]); ax.axis('off')
ax.text(0, 0.95, "Orange: stamped before 14:00:00.\nBlue: stamped from 14:00:00 on.\n\nDashed line: a day with papers\narriving evenly round the clock.\nMinutes with no paper are drawn at\nthe foot. Percentages are of each\ngroup's papers on weekdays.", fontsize=8.8, color=MUTED, va='top', linespacing=1.45)
# bottom: two bar panels
gs = ORDER; fm = [100 * P[g]["per_minute"][60] / P[g]["n"] for g in gs]; lm = [100 * P[g]["per_minute"][59] / P[g]["n"] for g in gs]; yp = np.arange(len(gs))[::-1]
for j, (vals, col, title, xmax) in enumerate(((fm, BLUE, "Share of the group's papers that arrive in the first minute after the boundary", 21), (lm, ORANGE, "…and in the last minute before it", 1.6))):
    ax = fig.add_axes([0.20 + j * 0.42, 0.045, 0.33, 0.165]); ax.barh(yp, vals, height=0.62, color=col)
    for yv, v in zip(yp, vals): ax.text(v + xmax * 0.012, yv, f"{v:.1f}%" if j == 0 else f"{v:.2f}%", va='center', fontsize=8.5, color=INK)
    ax.set_yticks(yp); ax.set_yticklabels([g if g != "maths" else "two of maths" for g in gs] if j == 0 else [], fontsize=9, color=INK); ax.set_xlim(0, xmax); ax.tick_params(length=0); ax.grid(axis='x', color=GRID, lw=0.8); ax.set_axisbelow(True)
    for sp in ax.spines.values(): sp.set_visible(False)
    ax.set_title(title, loc='left', fontsize=9.3, color=INK, pad=6); ax.set_xlabel("% of weekday papers (a level day: 0.07%)", fontsize=8.5)
fig.suptitle("One second apart: the minute before the arXiv's daily boundary, and the minute after", x=0.065, y=0.975, ha='left', fontsize=15, color=INK)
fig.text(0.065, 0.935, "Every paper first submitted from January to June 2025 in seven groups of categories (33,820 papers, 29,363 of them on weekdays), by the minute of its\ntime stamp in US Eastern time, Mondays to Fridays. The arXiv's mailings are cut at 14:00.", fontsize=9.5, color=MUTED, va='top', linespacing=1.5)
fig.savefig(sys.argv[2], dpi=130, facecolor='white')
