"""Second reading, item 4 (the figure). Copies ../hours_plot.py and ../hours_run.json into a folder of its own inside this one, runs the copy there
(so the author's picture is not overwritten), compares the picture it draws with ../hours-sixteen.png pixel for pixel, compares that with the
first version, lists the best longitude of each of the sixteen, and removes the copies.
usage: s4_figure.py   (under -I -B)"""
import os, sys, json, shutil, subprocess
import numpy as np, matplotlib.image as mi
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); D = os.path.join(HERE, 'redraw')
os.makedirs(D, exist_ok=True)
for f in ('hours_plot.py', 'hours_run.json'): shutil.copy(os.path.join(ROOT, f), D)
subprocess.run([sys.executable, '-I', '-B', os.path.join(D, 'hours_plot.py')], check=True, stdout=subprocess.DEVNULL)
a = mi.imread(os.path.join(D, 'hours-sixteen.png')); b = mi.imread(os.path.join(ROOT, 'hours-sixteen.png')); c = mi.imread(os.path.join(ROOT, 'hours-sixteen-first.png'))
shutil.rmtree(D)
print('redrawn from hours_plot.py as it stands:', a.shape, '; kept picture:', b.shape, '; equal pixel for pixel:', a.shape == b.shape and bool(np.array_equal(a, b)))
d = np.abs(b[..., :3] - c[..., :3]).max(axis=2) > 0.02; ys, xs = np.where(d)
print(f'the kept picture differs from the first version only in rows {ys.min()} to {ys.max()} of {b.shape[0]} (the footnote)')
ink = np.abs(b[..., :3] - b[0, 0, :3]).max(axis=2) > 0.05; r = np.where(ink.any(axis=1))[0]; k = np.where(ink.any(axis=0))[0]
print(f'ink runs from row {r.min()} to {r.max()} of {b.shape[0] - 1} and from column {k.min()} to {k.max()} of {b.shape[1] - 1}: nothing is cut off')
R = json.load(open(os.path.join(ROOT, 'hours_run.json')))['18']['scores']
S16 = {299: -1162, 223: -223, 205: 0, 187: 223, 183: 270, 169: 446, 165: 493, 147: 716, 129: 939, 111: 1162, 93: 1385, 89: 1432, 71: 1655, 53: 1878, 35: 2101, 17: 2324}
print('the sixteen (year BC, score, best longitude E, colour in the figure):')
for bc, kk in S16.items():
    s, lon = R[str(kk)]
    print(f'   {bc:3d}  {s:.2f}  {lon:+7.2f}  {"blue" if s < 3.0 else "grey"}' + ('   <- best longitude between 10 and 40 E' if 10 <= lon <= 40 else ''))
v = np.array([x[0] for x in R.values()]); print(f'median of all {len(v)} starts: {np.median(v):.2f} (the dashed line is drawn at 5.58)')
