"""Drawn for a narrow screen (the same six figures and the same words as handshake_popsize.py, in lettering a phone can show):
cooperation with and without noise at three population sizes, for the public page on the handshake study. The six figures and
their standard errors are typed from the table "The headline depends on population size" in the study's README (five runs of
200,000 generations each for 400 and 1,000; twelve for 100); the study kept no machine-readable output for them.
usage: handshake_popsize_phone.py OUT.png
At 350 pixels wide (a phone's column) the lettering comes out at about 10 to 11 pixels.
Colours: two slots of the chart palette (validated as a pair); labels in ink."""
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
out = sys.argv[1]
SURF, INK, INK2, GRID = '#fcfcfb', '#0b0b0b', '#52514e', '#e4e3df'
BLUE, ORANGE = '#2a78d6', '#eb6834'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10, 'text.color': INK, 'axes.labelcolor': INK2, 'xtick.color': INK2, 'ytick.color': INK2,
                     'axes.edgecolor': GRID, 'axes.facecolor': SURF, 'figure.facecolor': SURF, 'savefig.facecolor': SURF, 'axes.spines.top': False,
                     'axes.spines.right': False, 'axes.grid': True, 'grid.color': GRID, 'grid.linewidth': 0.8, 'axes.axisbelow': True})
POP = [100, 400, 1000]
NONE = [(0.25, 0.01), (0.57, 0.04), (0.85, 0.03)]       # cooperation with no noise: mean, standard error
TWO = [(0.59, 0.02), (0.77, 0.05), (0.79, 0.03)]        # with 2% of moves flipped
x = [0, 1, 2]
fig = plt.figure(figsize=(4.6, 4.1))
ax = fig.add_axes([0.135, 0.135, 0.845, 0.765])
ax.grid(axis='x', visible=False)
for vals, col, name, dy in ((NONE, BLUE, 'no slips', -0.075), (TWO, ORANGE, '2% of moves slip', 0.065)):
    m = [v for v, _ in vals]; e = [s for _, s in vals]
    ax.errorbar(x, m, yerr=e, color=col, lw=2.2, marker='o', ms=8, mfc=col, mec=SURF, mew=1.5, capsize=3, elinewidth=1.2)
    ax.text(0.36 if col == ORANGE else 0.62, (0.815 if col == ORANGE else 0.345), name, color=INK, fontsize=10, ha='center', va='center')   # each name beside its own line, clear of the marks
    for xi, v in zip(x, m): ax.text(xi + (0.09 if xi < 2 else -0.09), v + (0.085 if (col == ORANGE and xi == 0) else 0.06 if col == ORANGE else -0.055) * (1 if xi < 2 else -1), f'{round(100 * v)}%', ha='left' if xi < 2 else 'right', va='center', fontsize=10, color=INK2)
ax.set_xticks(x); ax.set_xticklabels(['100 machines', '400', '1,000']); ax.set_xlim(-0.4, 2.4); ax.tick_params(labelsize=9.5, length=3, color=GRID)
ax.set_ylim(0, 1); ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0]); ax.set_yticklabels(['0', '25%', '50%', '75%', '100%'])
ax.set_xlabel('size of the evolving population', fontsize=10)
fig.text(0.012, 0.975, 'Share of moves that are cooperative', fontsize=10, color=INK2, ha='left', va='top')
fig.savefig(out, dpi=230); print('written', out)
