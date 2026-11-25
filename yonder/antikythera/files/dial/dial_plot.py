"""One figure: how many of the dial's months still hold an eclipse possibility, cycle by cycle.
usage: dial_plot.py   (reads survival.json from dial_after.py; the measured points are from dial.out)"""
import json, os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
H = os.path.dirname(os.path.abspath(__file__))
SURF, INK, INK2, GRID, GREY = '#fcfcfb', '#0b0b0b', '#52514e', '#e4e3df', '#b4b3ad'
BLUE, ORANGE = '#2a78d6', '#eb6834'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10, 'text.color': INK, 'axes.labelcolor': INK2, 'xtick.color': INK2,
                     'ytick.color': INK2, 'axes.edgecolor': GRID, 'axes.facecolor': SURF, 'figure.facecolor': SURF,
                     'savefig.facecolor': SURF, 'axes.spines.top': False, 'axes.spines.right': False, 'axes.grid': True,
                     'grid.color': GRID, 'grid.linewidth': 0.8, 'axes.axisbelow': True, 'lines.solid_capstyle': 'round'})
rows = json.load(open(os.path.join(H, 'survival.json')))
yr = [r['years'] for r in rows]
fig, ax = plt.subplots(figsize=(7.6, 4.3))
ax.plot(yr, [r['lunar'] for r in rows], color=BLUE, lw=2, label='lunar glyph months still holding a possible lunar eclipse (of 38)')
ax.plot(yr, [r['solar'] for r in rows], color=ORANGE, lw=2, label='solar glyph months still inside the dial\'s own limits (of 28)')
# measured in the tables: cycles 0 to 3, and today (cycle 123)
mx = [0, 18.03, 36.06, 54.09]
ax.plot(mx, [37, 37, 37, 37], ls='none', marker='o', ms=7, mfc=BLUE, mec=SURF, mew=1.2, zorder=4)
ax.plot(mx, [27, 26, 25, 25], ls='none', marker='o', ms=7, mfc=ORANGE, mec=SURF, mew=1.2, zorder=4)
ax.plot([2230.5], [0], ls='none', marker='o', ms=7, mfc=INK2, mec=SURF, mew=1.2, zorder=4)
ax.annotate('today: none of either', (2230.5, 0), xytext=(-8, 12), textcoords='offset points', ha='right', fontsize=9, color=INK)
ax.annotate('lunar', (yr[40], rows[40]['lunar']), xytext=(8, 6), textcoords='offset points', fontsize=9, color=INK)
ax.annotate('solar', (yr[24], rows[24]['solar']), xytext=(-34, -14), textcoords='offset points', fontsize=9, color=INK)
ax.set_xlim(-40, 2300); ax.set_ylim(-1.5, 40)
ax.set_xlabel('years after 205 BC'); ax.set_ylabel('months of the dial')
ax.set_title('The mechanism\'s own eclipse dial: how long its months kept their eclipses', fontsize=11, color=INK, loc='left')
leg = ax.legend(loc='upper right', frameon=False, fontsize=8.5, labelcolor=INK2, handlelength=1.6)
fig.text(0.125, 0.015, 'Lines: the dial\'s arithmetic with the node slipping as measured. Dots: counted in the sky tables.', fontsize=8, color=INK2)
fig.tight_layout(rect=(0, 0.03, 1, 1))
fig.savefig(os.path.join(H, 'dial-survival.png'), dpi=190)
print('written')
