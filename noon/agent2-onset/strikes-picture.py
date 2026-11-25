"""strikes-picture.py: the score of "Falling into step" as a picture: one dot for each stroke of each of the 24 bells.
    python -I strikes-picture.py step.json strikes.png
Made on 25 November for the front page of the public copy, where the piece had only a figure of four graphs to show for itself."""
import json, sys
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
d = json.load(open(sys.argv[1])); S = d['strikes']
INK, MUTED, BG, DOT = '#2b2622', '#6a625a', '#fcfcfb', '#1c5cab'
fig, ax = plt.subplots(figsize=(12.8, 8.0), dpi=100); fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
ax.scatter([s[0] for s in S], [s[1] for s in S], s=26, color=DOT, alpha=0.8, linewidths=0)
for t, label in ((d['t1'], 'the bells begin to feel each other'), (d['t2'], 'held together'), (d['t3'], 'let go')):
    ax.axvline(t, color=MUTED, lw=1, alpha=0.35)
    ax.text(t + 1.5, d['N'] + 0.35, label, color=MUTED, fontsize=15, va='bottom', ha='left')
ax.set_xlim(0, d['tend']); ax.set_ylim(-1, d['N'] + 2.2)
ax.set_xticks(range(0, int(d['tend']) + 1, 60)); ax.set_xticklabels(['%d min' % (t // 60) if t else '0' for t in range(0, int(d['tend']) + 1, 60)], fontsize=15, color=MUTED)
ax.set_yticks([0, d['N'] - 1]); ax.set_yticklabels(['lowest bell', 'highest bell'], fontsize=15, color=MUTED, rotation=90, va='center')
ax.tick_params(length=0)
for sp in ax.spines.values(): sp.set_visible(False)
fig.subplots_adjust(left=0.06, right=0.985, top=0.97, bottom=0.08); fig.savefig(sys.argv[2], facecolor=BG); print('strokes', len(S))
