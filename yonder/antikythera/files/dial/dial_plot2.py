"""One figure: how many of the dial's months held a catalogued eclipse, cycle by cycle from 205 BC.
usage: dial_plot2.py   (reads two_lists.json written by two_lists.py; Freeth 2014's list, the one the sheets were sealed for)
Colours: two slots of the chart palette (validated as a pair), text in ink; the dashed line is the same months as the blue one, counted more strictly."""
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
rows = json.load(open(os.path.join(H, 'two_lists.json')))['F']
yr = [r['cycle'] * 18.03 for r in rows]
fig, ax = plt.subplots(figsize=(7.6, 4.5))
ax.step(yr, [r['A'] for r in rows], where='post', color=BLUE, lw=2, label='lunar glyph months with a lunar eclipse of any kind (of 38)')
ax.step(yr, [r['Aum'] for r in rows], where='post', color=BLUE, lw=1.4, ls=(0, (4, 2)), label='the same, counting only partial and total eclipses')
ax.step(yr, [r['S'] for r in rows], where='post', color=ORANGE, lw=2, label='solar glyph months with a solar eclipse somewhere on Earth (of 28)')
ax.annotate('lunar, any kind', (yr[22], rows[22]['A']), xytext=(10, 8), textcoords='offset points', fontsize=9, color=INK)
ax.text(640, 6.6, 'lunar, partial or total', fontsize=9, color=INK, ha='right', va='center')
ax.text(654, 11.2, 'solar', fontsize=9, color=INK, ha='left', va='center')
ax.annotate('none of either from here\nto November 2026', (1262, 0), xytext=(1290, 5.5), textcoords='data', fontsize=9, color=INK, va='center',
            arrowprops=dict(arrowstyle='-', color=GREY, lw=0.8))
ax.set_xlim(-20, 1680); ax.set_ylim(-1.5, 40)
ax.set_xlabel('years after 205 BC'); ax.set_ylabel('months of the dial')
ax.set_title('The mechanism\'s eclipse dial, kept turning: months that still held an eclipse', fontsize=10.5, color=INK, loc='left')
ax.legend(loc='upper right', frameon=False, fontsize=8.5, labelcolor=INK2, handlelength=2.2)
fig.text(0.125, 0.015, 'Counted in NASA\'s catalogue of eclipses, one step to each eighteen-year cycle. Months as in Freeth (2014).', fontsize=8, color=INK2)
fig.tight_layout(rect=(0, 0.03, 1, 1))
fig.savefig(os.path.join(H, 'dial-kept.png'), dpi=190)
print('written')
