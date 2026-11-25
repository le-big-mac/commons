"""The figure.   usage: python figures.py drumair.png     (reads named.json, ref-*.json, ../drum/rings2-free-*.json, ../drumfree/best.json)"""
import sys, json, glob, math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import airlib as A
L = A.L
INK, MUTED, GRID, BLUE, ORANGE, AQUA, NEUTRAL = "#2b2622", "#6f675e", "#e4dfd6", "#2a78d6", "#eb6834", "#1baf7a", "#b9b1a5"
plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": INK, "axes.edgecolor": GRID, "axes.labelcolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED, "font.size": 9.5})
def tidy(ax, axis='y'):
    ax.tick_params(length=0); ax.grid(axis=axis, color=GRID, lw=0.8); ax.set_axisbelow(True)
    for sp in ax.spines.values(): sp.set_visible(False)
N = {r['name']: r for r in json.load(open("named.json"))}; REF = {}
for f in glob.glob("ref-*.json"): d = json.load(open(f)); REF[(d['kind'], d['weight'], d['volume'])] = d
def ring_row(d):
    """a ring load of the reference drum: vacuum place, place with its air, and with the cavity doubled and halved (the load unchanged)"""
    a = np.array(d['a']); e, r = A.load_pieces(a); vac = A.vacuum(a, [(0, 1), (1, 1)]); note = vac[(1, 1)] / 2; B = A.reference(vac[(1, 1)])[0]
    return vac[(0, 1)] / note, *[A.round_modes(e, r, B * f, 1)[0] / note for f in (1.0, 0.5, 2.0)]
rows = []
def named(label, key): r = next(v for k, v in N.items() if k.startswith(key)); rows.append((label, r['vacuum'], r['reference']['place'], r['double']['place'], r['half']['place']))
named("the 1954 disc (9.77 times the skin over 0.40)", "the 1954 disc"); named("a disc of the makers' range: 6.25 times over 0.45", "an even disc: 6.25 times over 0.45"); named("16 times over 0.45", "an even disc: 16 times over 0.45")
named("10 times over 0.50", "an even disc: 10 times over 0.5"); named("6.25 times over 0.55", "an even disc: 6.25 times over 0.55"); named("16 times over 0.55", "an even disc: 16 times over 0.55")
named("the third study's best disc, lowest mode free", "the third study's best disc"); named("the third study's two discs", "the third study's two discs")
for M in (2.0, 4.0, 6.0): rows.append((f"40 rings, {M:g} skins, overtones tuned, lowest mode free", *ring_row(REF[("free", M, 1.0)])))
rows.append(("40 rings, 4 skins, all nine tuned to the lowest", *ring_row(REF[("tuned", 4.0, 1.0)])))
fig = plt.figure(figsize=(12.4, 10.0))
ax = fig.add_axes([0.345, 0.52, 0.62, 0.345]); n = len(rows)
ax.axvspan(1.09, 1.112, color=ORANGE, alpha=0.22, lw=0); ax.axvspan(1.112, 1.24, color=ORANGE, alpha=0.07, lw=0); ax.axvline(1.03, color=ORANGE, lw=1.2, ls=(0, (3, 3)))
ax.text(1.118, n - 0.15, "four real drums: 1.09 to 1.11 (two tablas, two mridangams);\nother readings of the tabla report run to 1.24", ha='left', va='bottom', fontsize=8, color=INK); ax.text(1.024, n - 0.15, "a table credited\nto Raman: 1.03", ha='right', va='bottom', fontsize=8, color=INK)
for j, (label, vac, air, dbl, half) in enumerate(rows):
    y = n - 1 - j; ax.plot([dbl, half], [y, y], color=BLUE, lw=1.4, alpha=0.45, solid_capstyle='butt'); ax.plot([vac, air], [y, y], color=NEUTRAL, lw=1.0, zorder=1)
    ax.plot([vac], [y], marker='o', ms=7, markerfacecolor='white', markeredgecolor=MUTED, markeredgewidth=1.4, zorder=3); ax.plot([air], [y], marker='o', ms=8, color=BLUE, markeredgecolor='white', markeredgewidth=0.8, zorder=4)
    ax.text(0.925, y, label, ha='right', va='center', fontsize=8.8, color=INK)
ax.plot([], [], ls='none', marker='o', ms=7, markerfacecolor='white', markeredgecolor=MUTED, markeredgewidth=1.4, label="in a vacuum"); ax.plot([], [], ls='none', marker='o', ms=8, color=BLUE, label="with the reference drum's air")
ax.plot([], [], color=BLUE, lw=1.4, alpha=0.45, label="its cavity doubled to halved"); ax.legend(loc='lower right', frameon=False, fontsize=8.5)
ax.set_xlim(0.93, 1.47); ax.set_ylim(-0.7, n + 1.0); ax.set_yticks([]); ax.set_xticks([1.0, 1.1, 1.2, 1.3, 1.4]); tidy(ax, 'x'); ax.set_xlabel("the lowest mode's frequency, in units of the note (half the second mode's frequency)")
fig.text(0.065, 0.885, "Where the lowest mode sits, without air and with it", fontsize=10.5, color=INK)
# least miss against weight on the reference drum
ax = fig.add_axes([0.065, 0.075, 0.40, 0.335]); W = [1.43, 2.0, 2.79, 4.0, 6.0, 12.0]; nine = {}
for f in glob.glob("../drum/rings2-free-*.json"): d = json.load(open(f)); nine[d['weight']] = d['rings']['40']['exact']
VB = json.load(open("../drumfree/best.json"))
series = [("all nine tuned to the lowest mode", AQUA, [nine[M] for M in W], [REF[("tuned", M, 1.0)]['exact'] for M in W]), ("the lowest mode left free", BLUE, [VB[f"five|{M:g}|40"]['exact'] for M in W], [REF[("free", M, 1.0)]['exact'] for M in W])]
for name, col, vac, air in series:
    ax.plot(W, [100 * v for v in vac], color=col, lw=1.6, ls=(0, (4, 3)), marker='o', ms=3.5, markerfacecolor='white', markeredgecolor=col); ax.plot(W, [100 * v for v in air], color=col, lw=2.2, marker='o', ms=4.5, markeredgecolor='white', markeredgewidth=0.7)
Wt = [M for M in W if ("tabla", M, 1.0) in REF]; ax.plot(Wt, [100 * REF[("tabla", M, 1.0)]['exact'] for M in Wt], color=ORANGE, lw=2.2, marker='o', ms=4.5, markeredgecolor='white', markeredgewidth=0.7)
ax.text(12.9, 100 * series[0][3][-1], "all nine tuned\nto the lowest", va='center', fontsize=8.5, color=INK); ax.text(12.9, 100 * series[1][3][-1] * 0.80, "lowest mode\nleft free", va='center', fontsize=8.5, color=INK); ax.text(12.9, 100 * REF[("tabla", Wt[-1], 1.0)]['exact'] * 1.45, "lowest mode\naimed at 1.10", va='center', fontsize=8.5, color=INK)
ax.plot([], [], color=MUTED, lw=1.6, ls=(0, (4, 3)), label="in a vacuum (the earlier studies)"); ax.plot([], [], color=MUTED, lw=2.2, label="on the reference drum, with its air"); ax.legend(loc='upper right', frameon=False, fontsize=8.5)
ax.set_xscale('log'); ax.set_yscale('log'); ax.set_xticks([1.43, 2, 2.79, 4, 6, 12]); ax.set_xticklabels(["1.43", "2", "2.79", "4", "6", "12"]); ax.set_yticks([0.05, 0.1, 0.2, 0.5, 1, 2, 5]); ax.set_yticklabels(["0.05%", "0.1%", "0.2%", "0.5%", "1%", "2%", "5%"]); ax.minorticks_off(); ax.set_xlim(1.3, 21); ax.set_ylim(0.045, 9); tidy(ax)
ax.annotate("uses 4.7 skins,\nwhatever is allowed", xy=(6, 100 * REF[("tabla", 6.0, 1.0)]['exact']), xytext=(4.6, 0.28), fontsize=8, color=INK, ha='left', arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.8))
ax.set_xlabel("added mass allowed, in skins"); ax.set_ylabel("least largest miss found (air as a spring; its mass left out)"); ax.set_title("Forty rings: how near whole multiples, by weight", loc='left', fontsize=10.5, color=INK, pad=8)
# the free lowest mode against weight and cavity
ax = fig.add_axes([0.575, 0.075, 0.39, 0.335]); curves = {"in a vacuum": [], "the reference cavity": [], "cavity doubled": [], "cavity halved": []}
for M in W:
    v, air, dbl, half = ring_row(REF[("free", M, 1.0)]); curves["in a vacuum"].append(v); curves["the reference cavity"].append(air); curves["cavity doubled"].append(dbl); curves["cavity halved"].append(half)
ax.axhspan(1.09, 1.112, color=ORANGE, alpha=0.22, lw=0); ax.text(2.3, 1.285, "the band, 1.09 to 1.11: four real drums (two of them probable)", va='center', ha='left', fontsize=8, color=INK)
for name, col, lw, ls in (("cavity halved", BLUE, 1.4, (0, (1, 2))), ("the reference cavity", BLUE, 2.2, '-'), ("cavity doubled", BLUE, 1.4, (0, (5, 2))), ("in a vacuum", MUTED, 1.6, (0, (4, 3)))):
    ax.plot(W, curves[name], color=col, lw=lw, ls=ls, marker='o', ms=4, markeredgecolor='white', markeredgewidth=0.6); ax.text(12.9, curves[name][-1] + {"cavity halved": 0.004, "the reference cavity": 0.004, "cavity doubled": -0.001, "in a vacuum": -0.005}[name], name, va='center', fontsize=8.5, color=INK)
ax.set_xscale('log'); ax.set_xticks([1.43, 2, 2.79, 4, 6, 12]); ax.set_xticklabels(["1.43", "2", "2.79", "4", "6", "12"]); ax.minorticks_off(); ax.set_xlim(1.3, 26); ax.set_ylim(1.0, 1.30); ax.set_yticks([1.0, 1.05, 1.1, 1.15, 1.2, 1.25, 1.3]); tidy(ax)
ax.set_xlabel("added mass, in skins (each load found on the reference drum)"); ax.set_ylabel("the free lowest mode, in notes"); ax.set_title("In the model, where it sits turns on weight and cavity", loc='left', fontsize=10.5, color=INK, pad=8)
fig.suptitle("Air in the drum", x=0.065, y=0.975, ha='left', fontsize=15, color=INK)
fig.text(0.065, 0.945, "A loaded drumskin over a closed cavity. The air shut inside stiffens the modes that change its volume, the lowest most of all. On a drum of a tabla's size,\nas guessed here, that lifts the lowest mode by 2% to 17% in the loads tried. Four measured drums have theirs about a tenth above the note; this cannot say that is the air.", fontsize=9.5, color=MUTED, va='top', linespacing=1.45)
fig.savefig(sys.argv[1], dpi=130, facecolor='white')
