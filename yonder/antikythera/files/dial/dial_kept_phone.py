"""The eclipse dial's figure for the public page, drawn for a narrow screen: the same counts as dial_kept_page.py
(dial/two_lists.json, Freeth 2014's list), the same two lines and the same words on them, with one scale along the foot,
in calendar years, and lettering that can be read on a phone. The two lines of small print that stood inside the wide
picture are left to the page's caption and text, which say the same.
usage: dial_kept_phone.py TWO_LISTS.json OUT.png
At 350 pixels wide (a phone's column) the type comes out at about 10 to 11 pixels (capitals about 8 pixels high). Colours as in dial_kept_page.py."""
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
fig = plt.figure(figsize=(4.6, 4.5))
ax = fig.add_axes([0.105, 0.105, 0.875, 0.79])
ax.grid(axis='x', visible=False)
BOX = dict(fc=SURF, ec='none', pad=0.5)      # a patch of the paper's colour behind each label, so that no grid line runs through the words
ax.step(yr, [r['A'] for r in rows], where='post', color=BLUE, lw=2.2)
ax.step(yr, [r['S'] for r in rows], where='post', color=ORANGE, lw=2.2)
ax.text(120, 38.6, 'months marked for an eclipse\nof the Moon (38 in all)', fontsize=10, color=INK, ha='left', va='bottom', linespacing=1.25, bbox=BOX)
ax.text(20, 14.2, 'months marked for\nan eclipse of the Sun\n(28 in all)', fontsize=10, color=INK, ha='left', va='top', linespacing=1.25, bbox=BOX)
ax.annotate(f'Moon: none since\nabout AD {round(zl - 204, -1):.0f}', (zl, 0), xytext=(zl - 150, 19.5), textcoords='data', fontsize=10, color=INK, ha='center', va='bottom',
            linespacing=1.25, bbox=BOX, arrowprops=dict(arrowstyle='-', color=GREY, lw=0.8, shrinkB=3))
ax.annotate(f'Sun: none since\nabout AD {zs - 204:.0f}', (zs, 0), xytext=(1570, 8.0), textcoords='data', fontsize=10, color=INK, ha='right', va='bottom',
            linespacing=1.25, bbox=BOX, arrowprops=dict(arrowstyle='-', color=GREY, lw=0.8, shrinkB=3, relpos=(0.45, 0.0)))
ax.set_xlim(-20, 1580); ax.set_ylim(-1.5, 46)
ax.set_yticks([0, 10, 20, 30, 40])
# one scale, in calendar years: AD Y is Y + 204 years after 205 BC
ticks = [(0, '205 BC'), (204 + 250, 'AD 250'), (204 + 500, '500'), (204 + 750, '750'), (204 + 1000, '1000'), (204 + 1250, '1250')]
ax.set_xticks([t for t, _ in ticks]); ax.set_xticklabels([s_ for _, s_ in ticks])
ax.tick_params(length=3, color=GRID, labelsize=9.5)
fig.text(0.012, 0.975, 'Marked months that held an eclipse', fontsize=10, color=INK2, ha='left', va='top')
print('zero from', zl, zs, 'years after 205 BC, i.e. AD', zl - 204, zs - 204)
fig.savefig(out, dpi=230)
print('written', out, '; cycles:', len(rows), '; first row', rows[0]['A'], rows[0]['S'])
