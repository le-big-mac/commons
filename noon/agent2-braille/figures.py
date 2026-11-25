"""figures.py: the two pictures of the write-up.
    ~/vuza/.venv/bin/python -I figures.py study.json speech-study.json [TAG]  ->  booksTAG.png, speechTAG.png"""
import json, sys
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
INK, MUTED, BG, DOT, RULE = '#2b2622', '#6a625a', '#fcfcfb', '#1c5cab', '#e4dfd6'
YEAR = {'austen-pride-1813': 1813, 'shelley-frankenstein-1818': 1818, 'bronte-jane-eyre-1847': 1847, 'melville-moby-dick-1851': 1851, 'dickens-great-1861': 1861, 'eliot-middlemarch-1871': 1871,
        'conrad-lord-jim-1900': 1900, 'wharton-age-of-innocence-1920': 1920, 'christie-styles-1920': 1920, 'lewis-babbitt-1922': 1922, 'fitzgerald-gatsby-1925': 1925, 'hemingway-sun-1926': 1926,
        'hoover-daedalus-1991': 1991, 'hoover-life-blood-2000': 2000, 'hoover-syndrome-2003': 2003, 'doctorow-down-and-out-2003': 2003, 'doctorow-little-brother-2008': 2008, 'doctorow-makers-2009': 2009}
LABEL = {'austen-pride-1813': ('Pride and Prejudice', 6, 4), 'bronte-jane-eyre-1847': ('Jane Eyre', 6, -12), 'eliot-middlemarch-1871': ('Middlemarch', 6, 4), 'lewis-babbitt-1922': ('Babbitt', 6, -12),
         'conrad-lord-jim-1900': ('Lord Jim', -6, 6), 'doctorow-makers-2009': ('Makers', -6, 7)}
def clean(ax):
    for sp in ('top', 'right'): ax.spines[sp].set_visible(False)
    for sp in ('left', 'bottom'): ax.spines[sp].set_color(RULE)
    ax.tick_params(colors=MUTED, length=0, labelsize=11); ax.grid(axis='y', color=RULE, lw=0.8); ax.set_axisbelow(True)
if __name__ == '__main__':
    st = json.load(open(sys.argv[1])); sp = json.load(open(sys.argv[2])); TAG = sys.argv[3] if len(sys.argv) > 3 else ''
    fig, ax = plt.subplots(figsize=(9.6, 5.4), dpi=120); fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    for f, y in YEAR.items():
        s = 100 * st['S'][f][0]; ax.scatter([y], [s], s=64, color=DOT, zorder=3, edgecolors=BG, linewidths=1.5)
        if f in LABEL:
            t, dx, dy = LABEL[f]; ax.annotate(t, (y, s), xytext=(dx, dy), textcoords='offset points', fontsize=10, color=MUTED, ha='left' if dx > 0 else 'right')
    for e, (a, b) in (('1', (1808, 1876)), ('2', (1895, 1931)), ('3', (1986, 2014))):
        m = 100 * st['mean'][e]; ax.plot([a, b], [m, m], color=INK, lw=2, zorder=2)
        if e == '1': ax.text((a + b) / 2, m + 0.42, 'mean %.1f%%' % m, ha='center', fontsize=11, color=INK)
        elif e == '2': ax.text(b + 3, m, 'mean %.1f%%' % m, ha='left', va='center', fontsize=11, color=INK)
        else: ax.text(a - 3, m, 'mean %.1f%%' % m, ha='right', va='center', fontsize=11, color=INK)
    kj = 100 * st['S']['kjv-1611'][0]; ax.axhline(kj, color=MUTED, lw=1, ls=(0, (4, 3)), zorder=1); ax.text(1810, kj + 0.12, 'the King James Bible of 1611: %.1f%%' % kj, fontsize=11, color=MUTED)
    ax.set_xlim(1800, 2020); ax.set_ylim(20.6, 26.2); ax.set_yticks([21, 22, 23, 24, 25, 26]); ax.set_yticklabels(['21%', '22%', '23%', '24%', '25%', '26%'])
    ax.set_title('Share of braille cells that contractions save, by the year of the book', loc='left', fontsize=13, color=INK, pad=12); clean(ax)
    fig.subplots_adjust(left=0.07, right=0.98, top=0.9, bottom=0.08); fig.savefig('books%s.png' % TAG, facecolor=BG); plt.close(fig)

    fig, ax = plt.subplots(figsize=(9.6, 4.4), dpi=120); fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    OUT, IN = '#1c5cab', '#c8622a'
    xs = [1, 2, 3]; o = [100 * sp['out'][str(e)] for e in xs]; i = [100 * sp['ins'][str(e)] for e in xs]
    ax.plot(xs, o, color=OUT, lw=2, marker='o', ms=8, zorder=3); ax.plot(xs, i, color=IN, lw=2, marker='s', ms=8, zorder=3)
    for x, v in zip(xs, o): ax.annotate('%.1f%%' % v, (x, v), xytext=(0, 9), textcoords='offset points', ha='center', fontsize=11, color=INK)
    for x, v in zip(xs, i): ax.annotate('%.1f%%' % v, (x, v), xytext=(0, -17), textcoords='offset points', ha='center', fontsize=11, color=INK)
    ax.text(1.5, (o[0] + o[1]) / 2 + 0.16, 'narration', color=INK, fontsize=12, ha='center'); ax.text(1.5, (i[0] + i[1]) / 2 - 0.3, 'speech', color=INK, fontsize=12, ha='center')
    ax.set_xticks(xs); ax.set_xticklabels(['six novels of 1813 to 1871', 'six of 1900 to 1926', 'six of 1991 to 2009'], fontsize=11); ax.set_xlim(0.7, 3.3); ax.set_ylim(21.2, 24.5)
    ax.set_yticks([22, 23, 24]); ax.set_yticklabels(['22%', '23%', '24%'])
    ax.set_title('The same share inside quotation marks (speech) and outside them (narration)', loc='left', fontsize=13, color=INK, pad=12); clean(ax)
    fig.subplots_adjust(left=0.07, right=0.98, top=0.88, bottom=0.1); fig.savefig('speech%s.png' % TAG, facecolor=BG); plt.close(fig)
    print('books%s.png, speech%s.png' % (TAG, TAG))
