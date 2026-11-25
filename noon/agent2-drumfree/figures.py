"""The figure (redrawn after the referee's report).   usage: python figures.py drumfree.png
(reads disc.json, best.json, shape-two-five-1.43.json, after3.json, leaveout3-2-*.json, ../drum/rings2-free-*.json, ../drum12/best.json)"""
import sys, json, glob
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import libfree as F
L = F.L
INK, MUTED, GRID, BLUE, ORANGE, AQUA, NEUTRAL = "#2b2622", "#6f675e", "#e4dfd6", "#2a78d6", "#eb6834", "#1baf7a", "#b9b1a5"
plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": INK, "axes.edgecolor": GRID, "axes.labelcolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED, "font.size": 9.5})
def tidy(ax, axis='y'):
    ax.tick_params(length=0); ax.grid(axis=axis, color=GRID, lw=0.8); ax.set_axisbelow(True)
    for sp in ax.spines.values(): sp.set_visible(False)
D = json.load(open("disc.json")); B = json.load(open("best.json")); two = json.load(open("shape-two-five-1.43.json")); T = [L.target(m, n) for m, n in F.FIVE]
def cells(a, per):
    sk = F.FreeSkin(len(a), F.FIVE + [(0, 1)], per); c = sk.solve(np.asarray(a, float), grad=False); r = (c + 1) * np.array(T[1:] + [1.0]); return [2.0] + list(r[:-1]), float(r[-1])
TD = json.load(open("after3.json"))['tuned_disc']; tr, tp = F.disc_modes(TD['s'], TD['k'], F.FIVE)     # the best disc with the lowest mode aimed at 1 as well, searched in this study's measure
N = 800; e = np.arange(N + 1) / N; ko, ki = two['radii']; lo = two['share'] * two['used'] / ko ** 2; li = (1 - two['share']) * two['used'] / ki ** 2
twoload = sum(l * np.clip((np.minimum(k, e[1:]) ** 2 - e[:-1] ** 2) / (e[1:] ** 2 - e[:-1] ** 2), 0, 1) for l, k in ((lo, ko), (li, ki))); r2, p2 = cells(twoload, 1); rr, pr = cells(B["five|4|40"]['a'], 50)
RAMAN = ([2.00, 3.00, 3.00, 4.00, 4.00, 5.03, 5.08, 5.04], 1.03)             # (1,1), (2,1), (0,2), (3,1), (1,2), (4,1), (2,2), (0,3); and the lowest
miss = lambda r: max(abs(x / t - 1) for x, t in zip(r[1:], T[1:]))
rows = [("a tabla's right drum, as measured\n(a paper's table, which credits Raman)", RAMAN[0], RAMAN[1]), (f"one even disc, the lowest mode tuned too\n({TD['s']:.2f} times the skin over {TD['k']:.3f})", tr, tp), (f"one even disc, the lowest mode left free\n({D['five']['s']:.2f} times over {D['five']['k']:.3f})", D['five']['ratios'], D['five']['place']),
        (f"two discs, the lowest mode left free\n({1 + lo:.1f} times to {ko:.3f}, {1 + lo + li:.1f} inside {ki:.3f})", r2, p2), ("forty rings, the lowest mode left free\n(4 skins)", rr, pr)]
fig = plt.figure(figsize=(12.4, 8.8))
ax = fig.add_axes([0.065, 0.49, 0.90, 0.335])
for h in range(1, 6): ax.axvline(h, color=GRID, lw=6, zorder=0); ax.text(h, 5.72, f"{h}", ha='center', fontsize=10, color=MUTED)
for j, (name, r, pl) in enumerate(rows):
    y = 4.7 - j * 1.1
    for x in r: ax.plot([x, x], [y - 0.36, y + 0.36], color=INK, lw=2.0)
    ax.plot([pl, pl], [y - 0.36, y + 0.36], color=ORANGE, lw=2.6); ax.text(-1.05, y, name, ha='left', va='center', fontsize=9, color=INK, linespacing=1.3); ax.text(6.0, y, f"{100 * miss(r):.2f}%" if j else f"{100 * miss(r):.1f}%", ha='right', va='center', fontsize=9.5, color=INK)
ax.text(6.0, 5.72, "largest miss of the\nseven overtones", ha='right', va='bottom', fontsize=8.5, color=MUTED); ax.text(-1.05, 5.72, "multiple of the note:", fontsize=9.5, color=MUTED, va='bottom')
ax.plot([], [], color=ORANGE, lw=2.6, label="the lowest mode"); ax.plot([], [], color=INK, lw=2.0, label="the second mode (set at 2) and the seven overtones"); ax.legend(loc='lower center', bbox_to_anchor=(0.55, -0.13), ncol=2, frameon=False, fontsize=8.5)
ax.set_xlim(-1.1, 6.05); ax.set_ylim(-0.25, 6.1); ax.set_yticks([]); ax.set_xticks([])
for sp in ax.spines.values(): sp.set_visible(False)
ax.set_title("Eight modes of five skins, in units of half the second mode's frequency", loc='left', fontsize=10.5, color=INK, pad=8)
nine = {}
for f in glob.glob("../drum/rings2-free-*.json"): d = json.load(open(f)); nine[d['weight']] = d['rings']['40']['exact']
B12 = json.load(open("../drum12/best.json")); W = [0.6, 0.8, 1.0, 1.1, 1.2, 1.3, 1.43, 2.0, 2.79, 4.0, 6.0, 12.0]
for i, (name, title, tuned) in enumerate((("five", "Five families: 40 rings, by weight", sorted(nine.items())), ("seven", "Seven families", sorted((float(k.split("|")[1]), v['exact']) for k, v in B12.items() if k.startswith("sixteen|") and k.endswith("|40"))))):
    ax = fig.add_axes([0.065 + i * 0.30, 0.085, 0.235, 0.30]); ax.plot([m for m, v in tuned], [100 * v for m, v in tuned], color=AQUA, lw=2, marker='o', ms=3.5, markeredgecolor='white', markeredgewidth=0.6, label="the lowest mode tuned too,\nin the earlier studies' measure")
    Wb = sorted(float(k.split("|")[1]) for k, v in B.items() if k.startswith(name + "|") and k.endswith("|40") and v is not None)
    ax.plot(Wb, [100 * B[f"{name}|{m:g}|40"]['exact'] for m in Wb], color=BLUE, lw=2, marker='o', ms=3.5, markeredgecolor='white', markeredgewidth=0.6, label="the lowest mode left free")
    ax.set_xscale('log'); ax.set_yscale('log'); ax.set_xticks([0.6, 1, 1.43, 2, 4, 12]); ax.set_xticklabels(["0.6", "1", "1.43", "2", "4", "12"]); ax.set_yticks([0.05, 0.1, 0.2, 0.5, 1, 2, 5]); ax.set_yticklabels(["0.05%", "0.1%", "0.2%", "0.5%", "1%", "2%", "5%"]); ax.minorticks_off(); ax.set_xlim(0.55, 13); ax.set_ylim(0.045, 9.5); tidy(ax)
    ax.set_xlabel("added mass allowed, in skins"); ax.set_title(title, loc='left', fontsize=10.5, color=INK, pad=8)
    if i == 0:
        here = [(M, json.load(open(f"leaveout3-2-{M:g}.json"))['nothing']['exact']) for M in (1.43, 4.0)]
        ax.plot([m for m, v in here], [100 * v for m, v in here], ls='none', marker='D', ms=6, markerfacecolor='white', markeredgecolor=AQUA, markeredgewidth=1.6, label="tuned too, in this study's measure", zorder=4)
        ax.set_ylabel("least largest miss found"); ax.legend(loc='upper right', bbox_to_anchor=(1.08, 1.02), frameon=False, fontsize=7.8, labelspacing=0.5)
ax = fig.add_axes([0.745, 0.085, 0.22, 0.30]); pts = [("the paper's table (a tabla)", 1.03, INK), ("the 1954 disc", F.disc_miss(9.77, 0.4, F.FIVE)[1], INK), ("forty rings, 4 skins", pr, BLUE), ("two discs, 1.43 skins", p2, BLUE), ("the paper's smooth step", 1.0995, INK), ("one disc, lowest free", D['five']['place'], BLUE)]
ax.axvspan(1.09, 1.12, color=ORANGE, alpha=0.18, lw=0); ax.text(1.105, len(pts) - 0.25, "a partial in mridangam strokes\n(Yonder), read as the lowest mode", ha='center', va='bottom', fontsize=8, color=INK)
for j, (name, x, col) in enumerate(pts): ax.plot([x], [j], marker='o', ms=7, color=col, markeredgecolor='white'); ax.text(x - 0.006 if x > 1.06 else x + 0.006, j, name, ha='right' if x > 1.06 else 'left', va='center', fontsize=8.5, color=INK)
ax.set_xlim(1.0, 1.16); ax.set_ylim(-0.6, len(pts) + 0.9); ax.set_yticks([]); ax.set_xticks([1.0, 1.05, 1.10, 1.15]); tidy(ax, 'x'); ax.set_xlabel("the lowest mode, in units of the note"); ax.set_title("Where the lowest mode sits", loc='left', fontsize=10.5, color=INK, pad=8)
fig.suptitle("The note the drum does not sound", x=0.065, y=0.975, ha='left', fontsize=15, color=INK)
fig.text(0.065, 0.938, "A round skin held at its rim, loaded at the centre. The note is half the frequency of the second mode. Only the modes above the second are asked to be\nwhole multiples of the note; the lowest is left to fall where it will. Rings then bring the seven overtones of five families seven to ten times closer,\nand the best disc lands at half the radius, where a paper puts the tabla's patches. The lowest mode sits sharp, as in nearly any skin loaded at the centre.", fontsize=9.5, color=MUTED, va='top', linespacing=1.45)
fig.savefig(sys.argv[1], dpi=130, facecolor='white')
