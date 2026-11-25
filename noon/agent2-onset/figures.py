"""Four panels on the onset of synchrony.   usage: python figures.py sheet.json sizes-random.json sizes-regular.json curves.json long.json onset.png"""
import sys, json, math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os
S = json.load(open(sys.argv[1])); RA = json.load(open(sys.argv[2]))['sizes']; RE = json.load(open(sys.argv[3]))['sizes']; C = json.load(open(sys.argv[4])); OUT = sys.argv[6]
LONG = json.load(open(sys.argv[5])) if os.path.exists(sys.argv[5]) else None
INK, MUTED, GRID, BLUE, ORANGE, AQUA, NEUTRAL = "#2b2622", "#6f675e", "#e4dfd6", "#2a78d6", "#eb6834", "#1baf7a", "#b9b1a5"
plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": INK, "axes.edgecolor": GRID, "axes.labelcolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED, "font.size": 9.5})
fig, axs = plt.subplots(2, 2, figsize=(12.4, 8.8)); fig.subplots_adjust(left=0.07, right=0.97, top=0.90, bottom=0.08, hspace=0.36, wspace=0.2)
def style(ax, title):
    ax.grid(color=GRID, lw=0.8); ax.set_axisbelow(True); ax.tick_params(length=0)
    for sp in ax.spines.values(): sp.set_visible(False)
    ax.set_title(title, loc='left', fontsize=10.5, color=INK, pad=8)
# ---- A: r against K for the three shapes
ax = axs[0, 0]; names = dict(lorentz="Lorentzian", gauss="Gaussian", uniform="uniform")
for sh, col in (("lorentz", BLUE), ("gauss", ORANGE), ("uniform", AQUA)):
    th = np.array(C['theory'][sh]); ax.plot(th[:, 0], th[:, 1], color=col, lw=1.6)
    pts = [p for p in C['curves'] if p['shape'] == sh]; ax.plot([p['K'] for p in pts], [p['r'] for p in pts], ls='none', marker='o', ms=4.2, markerfacecolor='white', markeredgecolor=col, markeredgewidth=1.1, label=names[sh])
ax.set_xlim(0.5, 2.5); ax.set_ylim(0, 1.02); ax.set_xlabel("coupling K (1 = the critical value)"); ax.set_ylabel("r")
ax.legend(loc='lower right', frameon=False, fontsize=9, title="circles: 2,000 oscillators\nlines: the limit of many", title_fontsize=8.5, alignment='left')
style(ax, "How far in step, against the coupling, for three spreads of tempo")
# ---- B: the size series at K = 1
ax = axs[0, 1]
N = np.array([q['N'] for q in RA]); r = np.array([q['r'] for q in RA]); se = np.array([q['sd'] / math.sqrt(q['runs']) for q in RA])
b, a = np.polyfit(np.log(N), np.log(r), 1)
ax.errorbar(N, r, yerr=2 * se, ls='none', marker='o', ms=5, color=BLUE, elinewidth=1, label=f"random tempos, runs of 600: slope {b:+.2f}")
ax.plot(N, np.exp(a) * N ** b, color=BLUE, lw=1.2)
N = np.array([q['N'] for q in RE]); r = np.array([q['r'] for q in RE]); rest = N <= 400
ax.plot(N[rest], r[rest], ls='none', marker='o', ms=5, color=ORANGE, label="evenly spaced, runs of 600")
ax.plot(N[~rest], r[~rest], ls='none', marker='o', ms=5, markerfacecolor='white', markeredgecolor=ORANGE, markeredgewidth=1.2, label="the same, still falling: these read the clock")
if LONG:
    N = np.array([q['N'] for q in LONG['sizes']]); r = np.array([q['r'] for q in LONG['sizes']]); b, a = np.polyfit(np.log(N), np.log(r), 1)
    ax.plot(N, r, ls='none', marker='s', ms=5, color=ORANGE, label=f"evenly spaced, runs of 4,000 to 24,000: slope {b:+.2f}")
    ax.plot(N, np.exp(a) * N ** b, color=ORANGE, lw=1.2)
N = np.array([100, 12800.0])
for expo, lab, y0 in ((-0.2, "−1/5", 0.62), (-0.4, "−2/5", 0.2)):
    ax.plot(N, y0 * (N / 100) ** expo, color=NEUTRAL, lw=1, ls=(0, (4, 3))); ax.text(N[1] * 1.05, y0 * (N[1] / 100) ** expo, lab, color=MUTED, fontsize=8.5, va='center')
ax.set_xscale('log'); ax.set_yscale('log'); ax.set_ylim(0.0045, 0.75); ax.set_yticks([0.01, 0.02, 0.05, 0.1, 0.2, 0.4]); ax.set_yticklabels(['0.01', '0.02', '0.05', '0.1', '0.2', '0.4']); ax.minorticks_off(); ax.set_xticks([100, 1000, 10000]); ax.set_xticklabels(['100', '1,000', '10,000']); ax.set_xlabel("number of oscillators")
ax.set_ylabel("mean measured r at K = 1")
ax.legend(loc='lower left', frameon=False, fontsize=8.5, title="bars: two standard errors; dashed: the slopes theory gives", title_fontsize=8.5, alignment='left')
style(ax, "Exactly at the critical coupling (Gaussian spread): r against size")
# ---- C: the sweep up and down
ax = axs[1, 0]
up = [s for s in S['sweep'] if s['leg'] == 'up']; down = [s for s in S['sweep'] if s['leg'] == 'down']
ax.plot([s['K'] for s in up], [s['r'] for s in up], color=BLUE, lw=1.4, marker='o', ms=4.5, label="coupling stepped up")
ax.plot([s['K'] for s in down], [s['r'] for s in down], color=ORANGE, lw=1.4, marker='o', ms=4.5, markerfacecolor='white', label="and back down")
ax.axhline(0.5, color=NEUTRAL, lw=1, ls=(0, (4, 3))); ax.set_xlabel("coupling K"); ax.set_ylabel("measured r"); ax.set_ylim(0, 1.02)
ax.legend(loc='upper left', frameon=False, fontsize=9)
style(ax, "Uniform spread: a jump at the same coupling up and down")
# ---- D: growth of the common rhythm
ax = axs[1, 1]
for q, col in zip(sorted(S['rise'], key=lambda q: -q['K']), (BLUE, ORANGE)):
    y = np.array(q['mean_curve']); t = np.arange(len(y)) * 1.0; K = q['K']
    ax.plot(t, y, color=col, lw=1.8, label=f"K = {K:g}: mean of 20 runs")
    r0 = y[0]; rinf2 = 1 - 1 / K; rate = K - 1                      # dr/dt = r (K/2 - 1/2 - K r^2/2):  r^2 = rinf^2 / (1 + (rinf^2/r0^2 - 1) e^(-rate t))
    ax.plot(t, np.sqrt(rinf2 / (1 + (rinf2 / r0 ** 2 - 1) * np.exp(-rate * t))), color=col, lw=1, ls=(0, (4, 3)))
    ax.axhline(q['target'], color=GRID, lw=1)
ax.set_xlim(0, 120); ax.set_ylim(0, 0.8); ax.set_xlabel("time"); ax.set_ylabel("r")
ax.legend(loc='lower right', frameon=False, fontsize=9, title="dashed: the reduced equation, from the same start", title_fontsize=8.5, alignment='left')
style(ax, "Lorentzian spread: the rhythm grows more slowly near the onset")
fig.suptitle("The onset of synchrony in Kuramoto's model", x=0.07, y=0.965, ha='left', fontsize=15, color=INK)
fig.savefig(OUT, dpi=130, facecolor='white')
