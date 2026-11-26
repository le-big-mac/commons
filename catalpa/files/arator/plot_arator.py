# One figure for the page: share of dactyls in the first four feet, and elisions per 100 lines, for sixteen poems in order of date; Arator picked out, the rest as context.
# Colours and mark sizes follow the charting guide I use (one accent hue, grey for context, thin bars with a rounded data end, values at the tips, no gridlines).
import json, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib.transforms import IdentityTransform
M = json.load(open('/home/agent1/arator/metrics.json'))
M2 = json.load(open('/home/agent1/arator/late2_metrics.json'))          # the five poems added on 26 Nov, from the run in which the scanner learned from all sixteen
for k in ('juvencus', 'ausonius', 'prudentius', 'dracontius', 'corippus'): M[k] = M2[k]
ROWS = [('geo', 'Virgil, Georgics', '29 BC'), ('aen', 'Virgil, Aeneid', '19 BC'), ('met', 'Ovid, Metamorphoses', 'AD 8'), ('lucan', 'Lucan', 'c. 65'), ('vflaccus', 'Valerius Flaccus', 'c. 80'),
        ('thebaid', 'Statius, Thebaid', 'c. 92'), ('achilleid', 'Statius, Achilleid', 'c. 95'), ('juvenal', 'Juvenal', 'c. 120'), ('juvencus', 'Juvencus', 'c. 330'), ('ausonius', 'Ausonius, Mosella', 'c. 371'),
        ('claudian', 'Claudian', 'c. 400'), ('prudentius', 'Prudentius', 'c. 405'), ('sedulius', 'Sedulius', 'c. 430'), ('dracontius', 'Dracontius', 'c. 490'), ('arator', 'Arator', '544'), ('corippus', 'Corippus', 'c. 550')]
SURF, INK, INK2, MUTED, BASE, ACCENT, GREY = '#fcfcfb', '#0b0b0b', '#52514e', '#898781', '#c3c2b7', '#2a78d6', '#898781'
W, H, DPI = 1500, 970, 200
fig = plt.figure(figsize=(W / DPI, H / DPI), dpi=DPI, facecolor=SURF)
top, pitch, bar = 150, 50, 26                     # pixels
panels = [(480, 390, 'dact', 100.0, 60.0, 'Dactyls in the first four feet', 'per cent of feet'), (1015, 390, 'el', 1.0, 60.0, 'Elisions', 'per 100 lines')]
def px(x, y): return x, H - y                      # image pixels, origin top left -> display coordinates
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis('off')
for i, (k, name, date) in enumerate(ROWS):
    y = top + i * pitch; arator = (k == 'arator')
    ax.text(312, H - y, name, ha='right', va='center', fontsize=8.6, color=INK if arator else INK2, fontweight='bold' if arator else 'normal')
    ax.text(326, H - y, date, ha='left', va='center', fontsize=7.4, color=MUTED)
for x0, width, key, scale, vmax, title, sub in panels:
    ax.text(x0, H - 62, title, ha='left', va='center', fontsize=9.6, color=INK, fontweight='bold')
    ax.text(x0, H - 94, sub, ha='left', va='center', fontsize=7.8, color=MUTED)
    ax.plot([x0, x0], [H - (top - 26), H - (top + (len(ROWS) - 1) * pitch + 26)], color=BASE, lw=0.8, solid_capstyle='butt')
    for i, (k, name, date) in enumerate(ROWS):
        v = M[k][key] * scale; L = width * v / vmax; y = top + i * pitch; col = ACCENT if k == 'arator' else GREY
        # a bar square at the baseline and rounded at the data end: a rounded box that starts left of the baseline, clipped at it
        p = FancyBboxPatch((x0 - 20, H - y - bar / 2), L + 20, bar, boxstyle='round,pad=0,rounding_size=8', fc=col, ec='none', transform=ax.transData, clip_on=True)
        ax.add_patch(p); p.set_clip_box(matplotlib.transforms.Bbox([[x0 * 1.0, 0], [W, H]]).transformed(ax.transData))
        ax.text(x0 + L + 10, H - y, f'{v:.1f}', ha='left', va='center', fontsize=8.2, color=INK if k == 'arator' else INK2, fontweight='bold' if k == 'arator' else 'normal')
fig.savefig('/home/agent1/site/img/arator.png', dpi=DPI, facecolor=SURF)
print('saved')
