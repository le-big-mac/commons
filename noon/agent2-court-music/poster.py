"""The piece drawn as a score: pitch against time for the winds and strings, a strip for the three drums.
usage: python poster.py events.json out.png"""
import sys, json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from tuning import freq

ev = json.load(open(sys.argv[1]))
E, T0, T1, TOTAL, beats = ev['events'], ev['T_NETORI'], ev['T_END'], ev['TOTAL'], ev['beats']
INK, MUTED, GRID = "#2b2622", "#6f675e", "#e4dfd6"
BLUE, ORANGE, AQUA, SHO = "#2a78d6", "#eb6834", "#1baf7a", "#cfc9bd"
plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": INK, "axes.edgecolor": GRID, "axes.labelcolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED})

# the sho's chords as (start, end, pitches); a chord lasts until the next one of the same stretch
sho = [e for e in E if e[0] == 'sho']
bars = []
for k, e in enumerate(sho):
    nxt = sho[k + 1][2] if k + 1 < len(sho) and sho[k + 1][2] > e[2] else None
    end = nxt if nxt is not None else (40.5 if e[2] < T0 else T1 + 2.5)
    bars.append((e[2], end, e[1], e[3]))

SYSTEMS = [(0, 118), (118, 236), (236, TOTAL)]
fig = plt.figure(figsize=(17, 15.5))
gs = fig.add_gridspec(len(SYSTEMS) * 3, 1, height_ratios=[5.2, 1, 0.75] * len(SYSTEMS), hspace=0.07)
YT = ['E2', 'B2', 'E3', 'B3', 'E4', 'B4', 'E5', 'B5', 'E6', 'B6']
section_of = {0: 'A', 2: 'A (again)', 4: 'B', 6: 'B (again)', 8: 'C', 10: 'C (again): the drums twice as fast'}
for s, (a, b) in enumerate(SYSTEMS):
    ax = fig.add_subplot(gs[3 * s])
    px = fig.add_subplot(gs[3 * s + 1], sharex=ax)
    ax.set_yscale('log'), ax.set_ylim(70, 2300), ax.set_xlim(a, a + 118)
    ax.set_yticks([freq(n) for n in YT]), ax.set_yticklabels(YT, fontsize=8.5), ax.minorticks_off()
    ax.grid(axis='y', color=GRID, lw=0.6), ax.set_axisbelow(True), ax.tick_params(length=0, labelbottom=False)
    for sp in ('top', 'right'):
        ax.spines[sp].set_visible(False), px.spines[sp].set_visible(False)
    # measures and phrases
    for k, t in enumerate(beats[::4]):
        if a <= t <= b:
            ax.axvline(t, color=GRID, lw=1.3 if k % 4 == 0 else 0.5, zorder=0)
            px.axvline(t, color=GRID, lw=1.3 if k % 4 == 0 else 0.5, zorder=0)
    for p, name in section_of.items():
        t = beats[16 * p]
        if a <= t < b:
            ax.text(t + 0.4, 1.015, name, fontsize=10, color=INK, va='bottom', fontweight='bold', transform=ax.get_xaxis_transform())
    if s == 0:
        ax.text(0.6, 1.015, "prelude: one player at a time, no beat", fontsize=10, color=INK, va='bottom', fontweight='bold', transform=ax.get_xaxis_transform())
    if a <= T1 < b:
        ax.text(T1 + 5.5, 1.015, "ending: the lute, then the koto, alone", fontsize=10, color=INK, va='bottom', fontweight='bold', transform=ax.get_xaxis_transform())
    # sho
    for t0, t1, name, notes in bars:
        if t1 < a or t0 > b:
            continue
        for n in notes:
            f = freq(n)
            ax.fill_between([t0, t1], f * 0.985, f * 1.015, color=SHO, lw=0, zorder=1)
        if a <= t0 + 0.25 < a + 116:
            ax.text(t0 + 0.25, freq(notes[-1]) * 1.06, name, fontsize=7, color=MUTED, va='bottom', zorder=2)
    # winds
    for e in E:
        if e[0] in ('hichiriki', 'ryuteki'):
            lf, am = np.array(e[3][0]), np.array(e[3][1])
            t = e[2] + np.arange(len(lf)) / 100.0
            f = np.where(am > 0.05, 2.0 ** lf, np.nan)
            ax.plot(t, f, color=BLUE if e[0] == 'hichiriki' else AQUA, lw=2.0, zorder=4 if e[0] == 'hichiriki' else 3, solid_capstyle='round')
    # strings
    for e in E:
        if e[0] == 'biwa' and a - 2 <= e[2] <= b:
            n = e[3]
            ts = np.linspace(e[2] - 0.45, e[2], len(n))
            ax.plot(ts, [freq(x) for x in n], color=ORANGE, lw=1.0, marker='o', ms=3.6, zorder=5)
        if e[0] == 'koto' and a - 2 <= e[2] <= b:
            ax.plot([e[2]], [freq(e[3])], color=ORANGE, marker='D', ms=4.2, mfc='white', mew=1.3, ls='', zorder=5)
    # drums
    px.set_ylim(-0.6, 2.6), px.set_yticks([0, 1, 2]), px.set_yticklabels(['big drum', 'kakko', 'small gong'], fontsize=8.5)
    px.tick_params(length=0)
    for e in E:
        if not (a - 1 <= e[2] <= b):
            continue
        if e[0] == 'taiko':
            px.plot([e[2]], [0], marker='o', ms=11 if e[1] == 'strong' else 5, color=INK, ls='', zorder=3)
        if e[0] == 'kakko':
            px.plot([e[2], e[2]], [0.72, 0.72 + 0.6 * e[3]], color=INK, lw=0.9, zorder=3)
        if e[0] == 'shoko' and e[3] > 0.9:
            px.plot([e[2]], [2], marker='|', ms=9, mew=1.4, color=INK, ls='', zorder=3)
    px.set_xlabel("seconds" if s == len(SYSTEMS) - 1 else "")
    px.tick_params(axis='x', labelsize=8.5)
    if s == 0:
        ax.annotate("sho: each grey line is one pipe;\nthe name is the chord", (9, freq('F#6') * 1.02), xytext=(16, 300), fontsize=9, color=INK, arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.8))
        ax.annotate("the flute begins alone", (beats[1], freq('B5') * 1.05), xytext=(beats[1] - 1, 190), fontsize=9, color=INK, ha='center', arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.8))
        ax.annotate("the first strong stroke: sho and hichiriki join", (beats[8], freq('E5') * 0.93), xytext=(beats[8] - 1.5, 105), fontsize=9, color=INK, ha='right', arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.8))
handles = [Line2D([], [], color=AQUA, lw=2.4, label="ryūteki (flute): the melody an octave up, a little early, with turns"),
           Line2D([], [], color=BLUE, lw=2.4, label="hichiriki (reed): the melody, sliding into its notes"),
           Patch(color=SHO, label="shō (mouth organ): one chord a measure, named for the melody's note"),
           Line2D([], [], color=ORANGE, lw=1, marker='o', ms=4, label="biwa (lute): a sweep arriving on each downbeat"),
           Line2D([], [], color=ORANGE, marker='D', ms=5, mfc='white', mew=1.3, ls='', label="koto: a quiet figure every second measure")]
fig.legend(handles=handles, loc='upper left', bbox_to_anchor=(0.045, 0.953), ncols=3, frameon=False, fontsize=9.5, columnspacing=2.2)
fig.suptitle("The Breath Apportioned: slow music for an imagined court", x=0.048, y=0.985, ha='left', fontsize=17, color=INK)
fig.text(0.048, 0.957, "Pitch against time. Thick grey verticals are the four-measure cycles; the big drum's strong stroke falls at the middle of each.",
         fontsize=10, color=MUTED)
fig.subplots_adjust(left=0.048, right=0.992, top=0.905, bottom=0.0)
fig.savefig(sys.argv[2], dpi=110, facecolor='white')
