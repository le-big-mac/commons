"""One figure for the clinching dates.   usage: python -I figure.py results.json out.png"""
import sys, json, collections
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
res = json.load(open(sys.argv[1]))
INK, MUTED, GRID, BLUE = "#2b2622", "#6f675e", "#e4dfd6", "#2a78d6"
plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": INK, "axes.edgecolor": GRID, "axes.labelcolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED})
names = [('title', "sure of the title"), ('out', "out of the title race"), ('top4', "sure of the top four"), ('doomed', "relegated"), ('safe', "safe from relegation")]
fig, (a, b) = plt.subplots(1, 2, figsize=(12.2, 4.6), gridspec_kw={"width_ratios": [1.25, 1], "wspace": 0.42})
for k, (m, label) in enumerate(names):
    rr = [r for s in res for r in s['results'] if r['matter'] == m and 'undetermined' not in r]
    lead = np.array([r['lead_rounds'] for r in rr])
    y = len(names) - 1 - k
    a.barh(y, 100 * (lead > 0).mean(), height=0.56, color=BLUE, zorder=3)
    a.text(100 * (lead > 0).mean() + 1, y, f"{int((lead > 0).sum())} of {len(rr)}" + (f"; at most {lead.max():.1f} rounds" if lead.max() > 0 else ""), va="center", fontsize=9.5, color=INK)
a.set_yticks(range(len(names))), a.set_yticklabels([n for _, n in names][::-1], fontsize=10, color=INK)
a.set_xlim(0, 60), a.set_xlabel("share of cases in which the exact answer came before the simple count (%)")
a.grid(axis="x", color=GRID, lw=0.8), a.set_axisbelow(True), a.tick_params(length=0)
for sp in ("top", "right", "left"):
    a.spines[sp].set_visible(False)
a.set_title("How often the simple count is late", loc="left", fontsize=11, color=INK)
by = collections.defaultdict(list)
for s in res:
    pos = {t: i + 1 for i, (t, _) in enumerate(s['table'])}
    for r in s['results']:
        if r['matter'] == 'safe' and 'undetermined' not in r:
            by[min((pos[r['team']] - 1) // 4, 4)].append(r['lead_rounds'])
labels = ["1–4", "5–8", "9–12", "13–16", "17"]
vals = [np.mean(by[k]) for k in range(5)]
b.bar(range(5), vals, width=0.6, color=BLUE, zorder=3)
for k, v in enumerate(vals):
    b.text(k, v + 0.02, f"{v:.2f}", ha="center", fontsize=9.5, color=INK)
b.set_xticks(range(5)), b.set_xticklabels(labels, fontsize=9)
b.set_ylabel("mean lead of the exact answer (rounds)"), b.set_xlabel("final position of the team")
b.grid(axis="y", color=GRID, lw=0.8), b.set_axisbelow(True), b.tick_params(length=0)
for sp in ("top", "right"):
    b.spines[sp].set_visible(False)
b.set_title("\"Safe\": late mainly for the top clubs", loc="left", fontsize=11, color=INK)
fig.suptitle("When is it mathematically settled? Ten Premier League seasons, 2014–15 to 2023–24", x=0.02, y=0.985, ha="left", fontsize=14, color=INK)
fig.subplots_adjust(left=0.17, right=0.985, top=0.84, bottom=0.14)
fig.savefig(sys.argv[2], dpi=130, facecolor="white")
