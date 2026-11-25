"""The figure.   usage: python figures.py drum12.png     (reads best.json, after-N-*.json and ../drum/rings2-free-*.json)"""
import sys, json, glob, os
sys.path.insert(0, "../drum")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import drum, lib12 as L
INK, MUTED, GRID, BLUE, ORANGE, AQUA, YELLOW, NEUTRAL = "#2b2622", "#6f675e", "#e4dfd6", "#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#b9b1a5"
plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": INK, "axes.edgecolor": GRID, "axes.labelcolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED, "font.size": 9.5})
def tidy(ax, axis='y'):
    ax.tick_params(length=0); ax.grid(axis=axis, color=GRID, lw=0.8); ax.set_axisbelow(True)
    for sp in ax.spines.values(): sp.set_visible(False)
BEST = json.load(open("best.json"))
def best(name, M):
    """the least found at this weight on 40 rings (best.json: the searches and the walks), by exact matching, and its load"""
    d = BEST[f"{name}|{M:g}|40"]; return d['exact'], d['a']
T16 = np.array([L.target(m, n) for m, n in L.SIXTEEN]); s16 = L.Skin(40, L.SIXTEEN)
fd = lambda a: np.concatenate([[1.0], (s16.solve(np.array(a), grad=False) + 1) * T16[1:]])
nine143 = json.load(open("../drum/rings2-free-1.43.json"))['rings']['40']['a']; six4 = best("sixteen", 4.0)[1]; wd = drum.modes(9.938, 0.4004, L.SIXTEEN); disc = np.array(wd) / wd[0]
rows = [("a plain skin", fd(np.zeros(40)), INK), ("one even disc (1.43 skins)", disc, ORANGE), ("rings tuned for nine modes (1.43 skins)", fd(nine143), AQUA), ("rings tuned for sixteen modes (4 skins)", fd(six4), BLUE)]
fig = plt.figure(figsize=(12.4, 8.6))
ax = fig.add_axes([0.065, 0.53, 0.90, 0.30])
for h in range(1, 8): ax.axvline(h, color=GRID, lw=6, zorder=0); ax.text(h, 4.62, f"{h}", ha='center', fontsize=10, color=MUTED)
for j, (name, r, col) in enumerate(rows):
    y = 3.6 - j * 1.1
    for i, x in enumerate(r): ax.plot([x, x], [y - 0.36, y + 0.36], color=col, lw=2.0, alpha=1.0 if i < 9 else 0.55)
    ax.text(-1.55, y, name, ha='left', va='center', fontsize=9.5, color=INK); ax.text(8.0, y, f"{100 * np.abs(r[1:] / T16[1:] - 1).max():.1f}%", ha='right', va='center', fontsize=9.5, color=INK)
ax.text(8.0, 4.62, "largest miss,\nsixteen modes", ha='right', va='bottom', fontsize=8.5, color=MUTED); ax.text(-1.55, 4.62, "harmonic:", fontsize=9.5, color=MUTED, va='bottom')
ax.set_xlim(-1.6, 8.05); ax.set_ylim(-0.3, 5.0); ax.set_yticks([]); ax.set_xticks([])
for sp in ax.spines.values(): sp.set_visible(False)
ax.set_title("The sixteen modes of the first seven families, as multiples of the lowest (the seven beyond the ninth drawn fainter)", loc='left', fontsize=10.5, color=INK, pad=8)
# (b) miss against weight
ax = fig.add_axes([0.065, 0.085, 0.36, 0.33]); W = [1.0, 1.43, 1.6, 1.8, 1.85, 1.9, 2.0, 2.2, 2.4, 2.79, 3.0, 3.2, 3.4, 3.6, 4.0, 6.0, 9.6, 12.0]
nine = {}
for f in glob.glob("../drum/rings2-free-*.json"): d = json.load(open(f)); nine[d['weight']] = d['rings']['40']['exact']
x9 = sorted(nine); ax.plot(x9, [100 * nine[m] for m in x9], color=AQUA, lw=2, marker='o', ms=4, markeredgecolor='white', markeredgewidth=0.7, label="nine modes, five harmonics")
for name, col, lab in (("twelve", YELLOW, "twelve modes, six harmonics"), ("sixteen", BLUE, "sixteen modes, seven harmonics")):
    y = [100 * best(name, m)[0] for m in W]; ax.plot(W, y, color=col, lw=2, marker='o', ms=4, markeredgecolor='white', markeredgewidth=0.7, label=lab)
ax.set_xscale('log'); ax.set_yscale('log'); ax.set_xticks([1, 1.43, 2, 2.79, 4, 6, 12]); ax.set_xticklabels(["1", "1.43", "2", "2.79", "4", "6", "12"]); ax.set_yticks([0.5, 1, 2, 3, 5, 8]); ax.set_yticklabels(["0.5%", "1%", "2%", "3%", "5%", "8%"]); ax.minorticks_off(); ax.set_xlim(0.95, 12.6); ax.set_ylim(0.45, 9); tidy(ax)
ax.set_xlabel("added mass allowed, in skins"); ax.set_ylabel("least largest miss found (40 rings)"); ax.legend(loc='upper right', frameon=False, fontsize=8.5)
ax.set_title("More harmonics want more weight", loc='left', fontsize=10.5, color=INK, pad=8)
# (c) miss against the number of harmonics
ax = fig.add_axes([0.50, 0.085, 0.20, 0.33]); fam = {5: "nine", 6: "twelve", 7: "sixteen"}
for M, col in ((4.0, NEUTRAL), (12.0, INK)):
    xs, ys = [], []
    for F in range(5, 11):
        if F == 5: v = nine.get(M)
        elif F in fam: v = best(fam[F], M)[0]
        else:
            f = f"after-N-{F}-{M:g}.json"; v = json.load(open(f))['rings']['40']['exact'] if os.path.exists(f) else None
        if v is not None: xs.append(F); ys.append(100 * v)
    ax.plot(xs, ys, color=col, lw=2, marker='o', ms=4, markeredgecolor='white', markeredgewidth=0.7, label=f"{M:g} skins")
ax.set_xticks(range(5, 11)); ax.set_xticklabels(["5\n(9)", "6\n(12)", "7\n(16)", "8\n(20)", "9\n(25)", "10\n(30)"]); ax.set_ylim(0, None); tidy(ax); ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, p: f"{v:g}%"))
ax.set_xlabel("harmonics tuned (modes)"); ax.legend(loc='upper left', frameon=False, fontsize=8.5); ax.set_title("More families, 40 rings", loc='left', fontsize=10.5, color=INK, pad=8)
# (d) the loads
ax = fig.add_axes([0.765, 0.085, 0.20, 0.33]); E = np.arange(41) / 40; nine4 = json.load(open("../drum/rings2-free-4.json"))['rings']['40']['a']
for a, col, lab in ((nine4, AQUA, "nine modes"), (six4, BLUE, "sixteen modes")): ax.step(E, np.concatenate([a, [a[-1]]]), where='post', color=col, lw=1.8, label=lab)
ax.set_xlim(0, 0.6); ax.set_ylim(0, None); tidy(ax); ax.set_xlabel("distance from the centre (rim = 1)"); ax.set_ylabel("added weight per area, in skins"); ax.legend(loc='upper right', frameon=False, fontsize=8.5)
ax.set_title("The loads, with 4 skins", loc='left', fontsize=10.5, color=INK, pad=8)
fig.suptitle("A drumskin tuned beyond its ninth mode", x=0.065, y=0.975, ha='left', fontsize=15, color=INK)
fig.text(0.065, 0.93, "A round skin held at its rim, loaded in 40 rings. Each tick is a mode of vibration; a mode with m nodal diameters, the n-th of its m, is aimed at the multiple m + 2n − 1.\nSearches look for the load that brings the modes nearest those multiples. These are the least found, not the least there is, and a membrane in a model, not a drum.", fontsize=9.5, color=MUTED, va='top', linespacing=1.5)
fig.savefig(sys.argv[1], dpi=130, facecolor='white')
