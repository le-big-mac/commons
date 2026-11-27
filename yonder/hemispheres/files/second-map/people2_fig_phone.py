"""Drawn for a narrow screen: the same points and lines as people2_fig.py (how many more people the half centred near Berlin
holds than the half centred in the Alps, by year, on three population maps), with the same words, the three names set in a
list above the chart beside their marks, and lettering a phone can show.
usage: people2_fig_phone.py OUT_DIR FIGURE.png      (reads OUT_DIR/{ghs,g1,g2}-YEAR.json written by run_people2.py)
At 350 pixels wide (a phone's column) the type comes out at about 10 to 11 pixels (capitals about 7 to 8 pixels high). Colours and marks as in people2_fig.py."""
import sys, json, os
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
od, figp = sys.argv[1], sys.argv[2]
SURF, INK, INK2, GRID = '#fcfcfb', '#0b0b0b', '#52514e', '#d9d8d2'
SER = [('ghs', 'GHS-POP: the maps first used', '#2a78d6', 'o', (1975, 2000, 2005, 2010, 2015, 2020, 2025, 2030)),
       ('g1', "WorldPop's older maps (made in 2018; their\n2020 is a projection, drawn hollow)", '#eb6834', 's', (2000, 2010, 2020)),
       ('g2', "WorldPop's newer maps, which know\nthe censuses of about 2020", '#1baf7a', 'D', (2015, 2020, 2025, 2030))]
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10, 'text.color': INK, 'figure.facecolor': SURF, 'axes.facecolor': SURF, 'savefig.facecolor': SURF,
                     'axes.edgecolor': GRID, 'axes.labelcolor': INK2, 'xtick.color': INK2, 'ytick.color': INK2})
fig = plt.figure(figsize=(4.6, 5.7))
ax = fig.add_axes([0.185, 0.068, 0.775, 0.60])
ax.axhline(0, color=INK2, lw=1.0, zorder=1)
ax.axvspan(2022.5, 2031.5, color='#f1f0ec', zorder=0, lw=0)
ax.text(2031.2, -12.9, 'projections', color=INK2, ha='right', va='bottom', fontsize=9.5)
ax.text(1974.3, 12.9, '5 million people is 0.06% of the world', color=INK2, fontsize=9.5, va='top')
ends = {}
for key, name, col, mk, years in SER:
    xs, ys = [], []
    for y in years:
        p = f'{od}/{key}-{y}.json'
        if not os.path.exists(p): continue
        r = json.load(open(p)); xs.append(y); ys.append((r['only_berlin'] - r['only_valais']) / 1e6)
    ax.plot(xs, ys, color=col, lw=2, marker=mk, ms=6.5, mec=SURF, mew=1.2, zorder=3)
    if key == 'g1': ax.plot(xs[-1:], ys[-1:], marker=mk, ms=6.5, mfc=SURF, mec=col, mew=1.8, zorder=4, ls='none')      # hollow: a projection
    ends[key] = (xs, ys, name, col)
ax.text(1974.3, 0.5, 'above the line, the half centred\nnear Berlin holds more', color=INK2, fontsize=9.5, va='bottom', linespacing=1.15)
ax.text(1974.3, -0.6, 'below it, the half centred\nin the Alps holds more', color=INK2, fontsize=9.5, va='top', linespacing=1.15)
ax.set_xlim(1973.5, 2031.5); ax.set_ylim(-13.5, 13.5)
ax.set_xticks([1975, 1990, 2000, 2010, 2020, 2030]); ax.set_yticks([-10, -5, 0, 5, 10]); ax.set_yticklabels(['10 fewer', '5 fewer', 'level', '5 more', '10 more'])
ax.grid(axis='y', color=GRID, lw=0.6); ax.set_axisbelow(True)
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
ax.tick_params(length=0, labelsize=9.5)
# above the chart: what is counted, then the three names, each beside its own mark and line
fig.text(0.012, 0.988, 'How many more people in the half centred near Berlin\nthan in the half centred in the Alps, millions', fontsize=10, color=INK2, ha='left', va='top', linespacing=1.3)
handles = [Line2D([0], [0], color=col, lw=2, marker=mk, ms=6.5, mec=SURF, mew=1.2) for _, _, col, mk, _ in SER]
leg = fig.legend(handles, [name for _, name, _, _, _ in SER], loc='upper left', bbox_to_anchor=(0.0, 0.89), frameon=False, fontsize=10, labelcolor=INK,
                 handlelength=2.2, handletextpad=0.6, labelspacing=0.75, borderaxespad=0.2)
fig.savefig(figp, dpi=230); print('written', figp)
for key, (xs, ys, name, col) in ends.items(): print(key, [(x, round(y, 1)) for x, y in zip(xs, ys)])
