"""The picture for the lists: the turtle that marches away (first turn 1, add 2) and the book's turtle that comes home.
usage: python -I thumb.py OUT.png WHICH     (matplotlib; reads nothing but inspi.py's own walk)"""
import os, sys
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from inspi import corners, predicted

def draw(ax, inc, A, n, lw, dots=True):
    z = corners(inc, A, n) * 1j; q = predicted(inc, A)[0]          # inspi.py walks along +x first; the page starts up the page: a quarter turn
    x, y = z.real, z.imag
    ax.plot(x, y, color='#2b2622', lw=lw, solid_joinstyle='round', solid_capstyle='round')
    if dots:
        e = z[::q]; ax.plot(e.real, e.imag, 'o', color='#a8482a', ms=lw * 3.2, mec='none')
    ax.plot([0], [0], 'o', mfc='none', mec='#a8482a', ms=lw * 5.5, mew=lw * 0.8)

if __name__ == '__main__':
    out, which = sys.argv[1], sys.argv[2]
    fig = plt.figure(figsize=(9.6, 7.2), dpi=100); fig.patch.set_facecolor('#fffdf7')
    ax = fig.add_axes([0.03, 0.03, 0.94, 0.94]); ax.set_aspect('equal'); ax.axis('off')
    if which == 'curls': draw(ax, 2, 1, 180 * 4, 3.2)
    elif which == 'book': draw(ax, 20, 2, 90, 5.0)
    else:                                      # both: the book's turtle comes home; with a first turn of 10 instead of 2 it marches away
        import numpy as np
        z = corners(20, 10, 18 * 4) * 1j; h = corners(20, 2, 90) * 1j; allz = np.concatenate([z, h])
        ax.plot(z.real, z.imag, color='#a8482a', lw=5.0, solid_joinstyle='round', solid_capstyle='round')
        draw(ax, 20, 2, 90, 6.0, dots=False)
        x0, x1, y0, y1 = allz.real.min(), allz.real.max(), allz.imag.min(), allz.imag.max(); pad = 0.9
        w, hgt = x1 - x0 + 2 * pad, y1 - y0 + 2 * pad; cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        if w / hgt < 4 / 3: w = hgt * 4 / 3
        else: hgt = w * 3 / 4
        ax.set_xlim(cx - w / 2, cx + w / 2); ax.set_ylim(cy - hgt / 2, cy + hgt / 2)
    fig.savefig(out, facecolor=fig.get_facecolor()); print('wrote', out)
