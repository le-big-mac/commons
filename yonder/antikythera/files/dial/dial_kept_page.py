"""The eclipse dial's figure for the public page: the same counts as the note's dial-kept.png (dial/two_lists.json, Freeth 2014's list),
with plain labels and calendar years along the top. The note's third line (lunar eclipses that are partial or total) is left to the note's own figure.
usage: dial_kept_page.py TWO_LISTS.json OUT.png
Colours: two slots of the chart palette (validated as a pair), text in ink; the dashed line is the same months as the blue one, counted more strictly."""
import json, sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
src, out = sys.argv[1:3]
SURF, INK, INK2, GRID, GREY = '#fcfcfb', '#0b0b0b', '#52514e', '#e4e3df', '#b4b3ad'
BLUE, ORANGE = '#2a78d6', '#eb6834'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10, 'text.color': INK, 'axes.labelcolor': INK2, 'xtick.color': INK2,
                     'ytick.color': INK2, 'axes.edgecolor': GRID, 'axes.facecolor': SURF, 'figure.facecolor': SURF,
                     'savefig.facecolor': SURF, 'axes.spines.top': False, 'axes.spines.right': False, 'axes.grid': True,
                     'grid.color': GRID, 'grid.linewidth': 0.8, 'axes.axisbelow': True, 'lines.solid_capstyle': 'round'})
rows = json.load(open(src))['F']
yr = [r['cycle'] * 18.03 for r in rows]
zl = next(r['cycle'] for r in rows if r['A'] == 0) * 18.03       # the first cycle in which no marked month held an eclipse of the Moon
zs = next(r['cycle'] for r in rows if r['S'] == 0) * 18.03       # the same for the Sun
fig, ax = plt.subplots(figsize=(7.6, 4.7))
ax.grid(axis='x', visible=False)
ax.step(yr, [r['A'] for r in rows], where='post', color=BLUE, lw=2.2)
ax.step(yr, [r['S'] for r in rows], where='post', color=ORANGE, lw=2.2)
ax.text(150, 37.6, 'months marked for an eclipse of the Moon (38 in all)', fontsize=9.5, color=INK, ha='left', va='bottom')
ax.text(30, 15.6, 'months marked for an eclipse\nof the Sun (28 in all)', fontsize=9.5, color=INK, ha='left', va='top')
ax.annotate(f'Moon: none since\nabout AD {round(zl - 204, -1):.0f}', (zl, 0), xytext=(zl + 10, 15.5), textcoords='data', fontsize=9, color=INK, ha='center', va='bottom',
            arrowprops=dict(arrowstyle='-', color=GREY, lw=0.8, shrinkB=3))
ax.annotate(f'Sun: none since\nabout AD {zs - 204:.0f}', (zs, 0), xytext=(zs + 190, 7.0), textcoords='data', fontsize=9, color=INK, ha='center', va='bottom',
            arrowprops=dict(arrowstyle='-', color=GREY, lw=0.8, shrinkB=3))
ax.set_xlim(-20, 1680); ax.set_ylim(-1.5, 41)
ax.set_xlabel('years after 205 BC'); ax.set_ylabel('marked months that held an eclipse')
top = ax.secondary_xaxis('top', functions=(lambda x: x, lambda x: x))     # the same scale, labelled in calendar years: AD Y is Y + 204 years after 205 BC
ticks = [(0, '205 BC'), (204 + 1, 'AD 1'), (204 + 250, '250'), (204 + 500, '500'), (204 + 750, '750'), (204 + 1000, '1000'), (204 + 1250, '1250')]
top.set_xticks([t for t, _ in ticks]); top.set_xticklabels([s_ for _, s_ in ticks]); top.tick_params(length=3, color=GRID)
top.spines['top'].set_visible(False)
fig.text(0.075, 0.012, 'Counted in NASA\'s catalogue of eclipses, one step to each eighteen-year cycle.\nThe marked months are those of Freeth\'s reconstruction of the dial (2014).', fontsize=7.8, color=INK2, linespacing=1.35)
fig.tight_layout(rect=(0, 0.06, 1, 1))
print('zero from', zl, zs, 'years after 205 BC, i.e. AD', zl - 204, zs - 204)
fig.savefig(out, dpi=170)
print('written', out, '; cycles:', len(rows), '; first row', rows[0]['A'], rows[0]['S'])
