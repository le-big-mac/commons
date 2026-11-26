import pickle, numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
res = pickle.load(open("curve.pkl", "rb"))
EPS = (0.0, 0.005, 0.01, 0.02, 0.03, 0.05, 0.07, 0.1); DEL = (0.99, 0.98, 0.95)
COL = {0.99: "#2a78d6", 0.98: "#eb6834", 0.95: "#1baf7a"}          # validated categorical slots 1-3
NAME = {0.99: "games of 100 rounds on average", 0.98: "50 rounds", 0.95: "20 rounds"}
SURF, INK, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e6e5e0"
fig, ax = plt.subplots(figsize=(8.6, 5.0), dpi=160); fig.patch.set_facecolor(SURF); ax.set_facecolor(SURF)
x = np.arange(len(EPS))
ax.plot(x, EPS, color=MUTED, lw=1, ls=(0, (2, 3)), zorder=1)
ax.text(x[-1] + 0.15, EPS[-1] - 0.035, "what all-defectors\nproduce by slipping", color=MUTED, fontsize=8, va="center")
table = []
for d in DEL:
    means, ses, ns = [], [], []
    for i, e in enumerate(EPS):
        c = np.array([r[3] for r in res if r[0] == e and r[1] == d])
        ns.append(len(c))
        if len(c) == 0: means.append(np.nan); ses.append(np.nan); continue
        means.append(c.mean()); ses.append(c.std(ddof=1) / np.sqrt(len(c)) if len(c) > 1 else 0)
        off = {0.99: -0.16, 0.98: 0.0, 0.95: 0.16}[d]
        ax.scatter(np.full(len(c), i + off), c, s=7, color=COL[d], alpha=0.22, lw=0, zorder=2)
    means, ses = np.array(means), np.array(ses)
    ax.fill_between(x, means - ses, means + ses, color=COL[d], alpha=0.15, lw=0, zorder=3)
    ax.plot(x, means, color=COL[d], lw=2, marker="o", ms=5.5, mec=SURF, mew=1.2, zorder=4, label=NAME[d])
    import matplotlib.patheffects as pe
    lx, ly, txt = {0.99: (2.0, 0.675, "100 rounds"), 0.98: (1.5, 0.395, "50 rounds"), 0.95: (2.62, 0.375, "20 rounds")}[d]
    ax.text(lx, ly, txt, color=INK, fontsize=8.5, ha="center", zorder=6, path_effects=[pe.withStroke(linewidth=3, foreground=SURF)])
    table.append((d, means, ses, ns))
ax.set_xticks(x); ax.set_xticklabels(["0", "0.5%", "1%", "2%", "3%", "5%", "7%", "10%"])
ax.set_xlim(-0.4, len(EPS) + 0.9); ax.set_ylim(0, 0.85)
ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8]); ax.set_yticklabels(["0", "20%", "40%", "60%", "80%"])
ax.set_xlabel("noise: share of moves that come out wrong", color=MUTED, fontsize=9)
ax.set_ylabel("cooperative moves, averaged over 200,000 generations", color=MUTED, fontsize=9)
ax.tick_params(colors=MUTED, labelsize=8.5, length=0)
ax.grid(axis="y", color=GRID, lw=0.8); ax.set_axisbelow(True)
for s in ax.spines.values(): s.set_visible(False)
ax.set_title("A little noise roughly doubles cooperation; a lot destroys it", color=INK, fontsize=11.5, loc="left", pad=22)
ax.text(0, 1.035, "Evolving populations of 100 machines, 12 runs per point. Dots are single runs, lines are means, bands are ± one standard error.", transform=ax.transAxes, color=MUTED, fontsize=8)
ax.legend(loc="upper right", frameon=False, fontsize=8.5, labelcolor=INK, bbox_to_anchor=(1.0, 0.99))
fig.tight_layout(); fig.savefig("cooperation-vs-noise.png", facecolor=SURF)
print("| noise | " + " | ".join(NAME[d].split(" (")[0] for d, *_ in table) + " |"); print("|---|---|---|---|")
for i, e in enumerate(EPS):
    print(f"| {e*100:g}% | " + " | ".join(f"{m[i]:.2f} ± {s[i]:.2f} (n={n[i]})" for d, m, s, n in table) + " |")
