"""The picture for the lists: the top left corner of the page's grid (its first 15 rows and 20 of its 40 columns): one
square for each odd denominator, rust where the turtle comes home, dark where the denominator holds the square of a prime
and the turtle marches away all the same, pale where it holds none.  Colours and layout are the page's; whether a turtle
comes home is read from table.json, which table.py makes by adding up the round.
usage: python -I thumb.py ../table.json OUT.png      (matplotlib)"""
import json, sys
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

COLS, SHOWC, SHOWR = 40, 20, 15

def has_square(m):
    l = 3
    while l * l <= m:
        if m % (l * l) == 0: return True
        l += 2
    return False

if __name__ == '__main__':
    odd = json.load(open(sys.argv[1]))['odd']
    fig = plt.figure(figsize=(9.6, 7.2), dpi=100); fig.patch.set_facecolor('#f6f1e7')
    ax = fig.add_axes([0.02, 0.02, 0.96, 0.96]); ax.set_xlim(0, SHOWC); ax.set_ylim(SHOWR, 0); ax.axis('off')
    n = {'#a8482a': 0, '#2b2622': 0, '#e9e1cf': 0}
    for row in range(SHOWR):
        for col in range(SHOWC):
            m = 3 + 2 * (row * COLS + col); home = odd[str(m)][0]
            c = '#a8482a' if home else '#2b2622' if has_square(m) else '#e9e1cf'; n[c] += 1
            ax.add_patch(Rectangle((col + 0.06, row + 0.06), 0.88, 0.88, color=c, lw=0))
    fig.savefig(sys.argv[2], facecolor=fig.get_facecolor()); print('wrote', sys.argv[2], '; squares:', n)
