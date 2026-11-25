"""Draw a grove from its JSON: the wood, the leaves, and where the bells rang.   usage: python -I picture.py grove.json out.png [time]"""
import sys, json, math
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
INK, MUTED, PAPER = "#2b2622", "#6f675e", "#f6f1e7"
HUES = ["#2a78d6", "#1baf7a", "#c79a2b", "#eb6834", "#8e5aa8"]
g = json.load(open(sys.argv[1])); P = g["params"]; T = float(sys.argv[3]) if len(sys.argv) > 3 else None
fig, ax = plt.subplots(figsize=(14, 7.2), dpi=110); fig.patch.set_facecolor(PAPER); ax.set_facecolor(PAPER)
for t in g["trees"]:
    X, Y, par, born = np.array(t["X"]), np.array(t["Y"]), t["par"], np.array(t["born"])
    step = len(X) if T is None else float(np.searchsorted(t["clock"], T, side="right")) - 1 + 1   # nodes born in steps already begun
    shown = born <= step; tipsub = np.zeros(len(X))
    kids = [0] * len(X)
    for v in range(1, len(X)):
        if shown[v]: kids[par[v]] += 1
    for v in range(len(X) - 1, 0, -1):
        if not shown[v]: continue
        if kids[v] == 0: tipsub[v] = 1
        tipsub[par[v]] += tipsub[v]
    segs = [[(X[par[v]], Y[par[v]]), (X[v], Y[v])] for v in range(1, len(X)) if shown[v]]
    lw = [0.55 + 1.05 * tipsub[v] ** 0.5 for v in range(1, len(X)) if shown[v]]
    ax.add_collection(LineCollection(segs, linewidths=lw, colors=INK, capstyle="round"))
    tips = [v for v in t["tips"] if shown[v]]
    ax.scatter(X[tips], Y[tips], s=34, color=HUES[t["i"]], alpha=0.55, linewidths=0, zorder=3)
for s in g["strikes"]:
    if s["kind"] == "fork" and (T is None or s["t"] <= T): ax.scatter([s["x"]], [s["y"]], s=14 + 5 * s["weight"] ** 0.5, facecolors="none", edgecolors=HUES[s["tree"]], linewidths=0.8, zorder=4)
ax.plot([0, P["W"]], [0, 0], color=MUTED, lw=1)
ax.set_xlim(0, P["W"]); ax.set_ylim(-0.3, P["YTOP"] + 0.2); ax.set_aspect("equal"); ax.axis("off")
ax.text(0.1, P["YTOP"], f"Dryads, seed {g['seed']}" + ("" if T is None else f", at {T:.0f} s"), color=INK, fontsize=13, va="top")
fig.savefig(sys.argv[2], facecolor=PAPER, bbox_inches="tight"); print("wrote", sys.argv[2])
