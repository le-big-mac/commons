"""Second reader: read Ioannou's Figure 4 (average payoffs by generation, four error rates) off the image embedded in the
discussion paper's page, by pixel. The image is data only: it is opened with PIL and nothing in it is run.
The image is not kept here (it is the paper's). To get it again, into a new empty folder:
    pdfimages -f 13 -l 13 -png /home/agent3/downloads/ioannou-2011-dp/paper.pdf FOLDER/fig4      (gives FOLDER/fig4-000.png, 842 by 616)
The output of the one run made is read_fig4.out.
usage: python -I -B read_fig4.py IMAGE.png"""
import sys
import numpy as np
from PIL import Image

im = np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(int)
H, W, _ = im.shape
r, g, b = im[..., 0], im[..., 1], im[..., 2]
dark = (r < 90) & (g < 90) & (b < 90)

# the plot frame: the left axis is the first long dark vertical run right of the outer black border, the bottom axis likewise
col_dark = dark[40:560, :].sum(0); row_dark = dark[:, 100:780].sum(1)
print('columns with long dark runs (candidates for the left axis):', [int(x) for x in np.where(col_dark > 300)[0]][:12])
print('rows with long dark runs (candidates for the bottom axis):', [int(y) for y in np.where(row_dark > 500)[0]][:12])

def runs(v):
    out = []; start = None
    for i, x in enumerate(v):
        if x and start is None: start = i
        if not x and start is not None: out.append((start, i - 1)); start = None
    if start is not None: out.append((start, len(v) - 1))
    return out

# y ticks: short dark marks just left of the left axis; x ticks: just below the bottom axis
ax_x = int([x for x in np.where(col_dark > 300)[0] if 30 < x < 120][0])
ax_y = int([y for y in np.where(row_dark > 500)[0] if 380 < y < 520][-1])
print('left axis at column', ax_x, '; bottom axis at row', ax_y)
yt = [(a + b_) / 2 for a, b_ in runs(dark[:ax_y + 5, ax_x - 6:ax_x - 2].all(1))]
xt = [(a + b_) / 2 for a, b_ in runs(dark[ax_y + 2:ax_y + 6, ax_x - 5:].all(0))]
xt = [x + ax_x - 5 for x in xt]
print('y tick rows:', yt); print('x tick columns:', xt)

# calibration from the tick marks found above: rows 42, 140, 337, 436 are payoffs 3, 2.5, 1.5, 1; columns 81 ... 800 are generations 0 ... 500
ys = [t for t in yt if 20 < t < ax_y]; xs = [t for t in xt if t < ax_x + 760]
assert len(xs) == 6, xs
y3, y1 = min(ys), max(ys); x0, x500 = xs[0], xs[-1]
val = lambda row: 1 + 2 * (y1 - row) / (y1 - y3)
gen = lambda col: 500 * (col - x0) / (x500 - x0)
print(f'calibration: payoff 3 at row {y3}, payoff 1 at row {y1}; generation 0 at column {x0}, 500 at column {x500}')
for t in ys: print(f'   tick at row {t}: payoff {val(t):.3f}')

# the four curves by colour, sampled from the legend's own line samples (rows about 527 and 560)
def near(c, tol=45): return (abs(r - c[0]) + abs(g - c[1]) + abs(b - c[2])) < tol
leg = {}
for name, (row, c0, c1) in {'0%': (527, 310, 400), '1%': (527, 470, 550), '2%': (560, 310, 400), '4%': (560, 470, 550)}.items():
    best = None
    for rr in range(row - 8, row + 9):
        seg = im[rr, c0:c1]; sat = seg.max(1) - seg.min(1)
        if best is None or sat.mean() > best[0]: best = (sat.mean(), np.median(seg[sat > sat.mean() * 0.8], 0) if (sat > sat.mean() * 0.8).any() else seg.mean(0))
    leg[name] = best[1]
    print(f'legend colour for {name}:', [int(v) for v in best[1]])
curve = {}
for name, c in leg.items():
    mask = near(c); mask[ax_y - 2:, :] = False; mask[:, :ax_x + 2] = False
    pts = {}; prev = None
    for col in range(int(x0), int(x500) + 1):
        rows = np.where(mask[:ax_y - 2, col])[0]
        if prev is not None: rows = rows[abs(rows - prev) <= 8]      # stay on this curve: another curve's blurred edge can match the colour
        if len(rows): pts[col] = prev = float(rows.mean())
    curve[name] = pts
    print(f'{name}: {len(pts)} columns traced of {int(x500 - x0) + 1}')
print('generation:  ' + '  '.join(f'{k:>6}' for k in curve))
for G in (5, 25, 50, 100, 150, 200, 250, 300, 350, 400, 425, 450, 475, 490, 500):
    out = []
    for name, pts in curve.items():
        col = x0 + G * (x500 - x0) / 500; near_cols = [cc for cc in pts if abs(cc - col) <= 2]
        out.append(f'{np.mean([val(pts[cc]) for cc in near_cols]):6.2f}' if near_cols else '     -')
    print(f'{G:10d}:  ' + '  '.join(out))
print('mean of the curve over generations 400 to 500 (what the note averages over), and its value at the last generation traced:')
for name, pts in curve.items():
    tail = [val(v) for cc, v in pts.items() if 400 <= gen(cc) <= 500]; last = max(pts)
    print(f'   {name}: mean over 400-500 {np.mean(tail):.3f} (lowest {min(tail):.3f}, highest {max(tail):.3f}); at generation {gen(last):.0f}: {val(pts[last]):.3f}')
