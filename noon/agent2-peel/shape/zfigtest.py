"""zfigtest.py: swing.svg read back. Every dot, bar, curve and mark is turned into values through the plate's own tick labels and
compared with figures computed here: the dots from the files of runs; the curve from the rounded quantity worked out again by another
sum (the density laid on one fine grid and added up cell by cell, where lattice.py takes each cell by Simpson's rule), with the
model's two forms written out again from ruler5.out's sources; the title from Z. Then the picture is drawn by a browser.
python -I zfigtest.py"""
import json, math, os, re, subprocess, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import fresh
svg = open(os.path.join(HERE, 'swing.svg'), encoding='utf-8').read(); J = json.load(open(os.path.join(HERE, 'zfig.json')))
npass = nfail = 0
def ok(name, cond, detail=''):
    global npass, nfail
    if cond: npass += 1; print('pass  ' + name)
    else: nfail += 1; print('FAIL  ' + name + ('   ' + str(detail) if detail != '' else ''))
C5 = 0.08227; mean_of = lambda n: 1.32594 * (n / math.pi) ** (2 / 3.0) * 0.75 + 0.2598 - 0.0411 * math.log10(n); smooth_of = lambda n: 0.08221 * n ** (1 / 3.0) - 0.0483 + 0.050 * n ** (-1 / 3.0); level_of = lambda n: 0.08205 * n ** (1 / 3.0) - 0.0414
def rounded(mu, s2, g):
    """mean and variance of a quantity of mean mu, variance s2 and standardized third cumulant g (normal density times 1 + g He3(z)/6), taken to the nearest whole number: one grid of 4,000 steps a layer"""
    s = math.sqrt(s2); lo = math.floor(mu - 10 * s) - 0.5; hi = math.ceil(mu + 10 * s) + 0.5; h = 1 / 4000.0; x = np.arange(lo + h / 2, hi, h); z = (x - mu) / s; f = np.exp(-0.5 * z * z) / (s * math.sqrt(2 * math.pi)) * (1 + g / 6.0 * (z ** 3 - 3 * z)) * h
    k = np.rint(x); tot = f.sum(); m = float((k * f).sum() / tot); return m, float(((k - m) ** 2 * f).sum() / tot)
def model(n, g):
    s2 = smooth_of(n) - 1 / 12.0; mu = mean_of(n)
    for _ in range(40): mu += mean_of(n) - rounded(mu, s2, g)[0]
    return rounded(mu, s2, g)[1] - C5 * n ** (1 / 3.0)
yt = [(float(v), float(y) - 4) for v, y in re.findall(r'<text class="ytick" data-v="([^"]+)" x="[\d.]+" y="([\d.]+)"', svg)]
ok('the eight tick labels up the side show the values they stand at, -0.055 to -0.020', len(yt) == 8 and all(abs(float(a) + float(b)) < 1e-9 for a, b in re.findall(r'<text class="ytick" data-v="([^"]+)"[^>]*>&#8722;([^<]+)</text>', svg)) and abs(yt[0][0] + 0.055) < 1e-9 and abs(yt[-1][0] + 0.020) < 1e-9)
Y = lambda py: yt[0][0] + (yt[-1][0] - yt[0][0]) * (py - yt[0][1]) / (yt[-1][1] - yt[0][1])
xt = [(int(n), float(x), lab) for n, x, lab in re.findall(r'<text class="xtick" data-n="(\d+)" x="([\d.]+)"[^>]*>([^<]+)</text>', svg)]
X = lambda px: xt[0][0] + (xt[-1][0] - xt[0][0]) * (px - xt[0][1]) / (xt[-1][1] - xt[0][1])
ok('nine ticks along the foot, 80 to 120 by fives, each labelled with its number and evenly spaced', [n for n, x, lab in xt] == list(range(80, 125, 5)) and all(lab == str(n) for n, x, lab in xt) and all(abs(X(x) - n) < 0.01 for n, x, lab in xt))
dots = {int(n): (float(cx), float(cy), fill) for n, cx, cy, fill in re.findall(r'<circle class="dot" data-n="(\d+)" cx="([\d.]+)" cy="([\d.]+)" r="5" fill="([^"]+)"', svg)}; bars = {int(n): (float(x), float(a), float(b), col) for n, x, a, b, col in re.findall(r'<line class="bar" data-n="(\d+)" x1="([\d.]+)" y1="([\d.]+)" x2="[\d.]+" y2="([\d.]+)" stroke="([^"]+)"', svg)}
ok('seven dots: the fifth sheet\'s six sizes and the fourth sheet\'s 100 points', sorted(dots) == [83, 90, 98, 100, 105, 113, 120])
mine = {}
for n in sorted(dots):
    x = fresh.counts('n%d-disc-%d' % (4 if n == 100 else 5, n)); v = float(x.var(ddof=1)); mine[n] = (v - C5 * n ** (1 / 3.0), v * math.sqrt(2.0 / len(x)), len(x)); cx, cy, fill = dots[n]; bx, by1, by2, col = bars[n]; want = '#eb6834' if n == 100 else '#2a78d6'
    ok('%d points: the dot is at its size and at B = %+.4f, the file\'s variance less 0.08227 n^(1/3); its bar is one error either way (%.4f; mine by the normal rule, to a quarter); %s' % (n, mine[n][0], mine[n][1], 'orange, the fourth sheet\'s' if n == 100 else 'blue'),
       abs(X(cx) - n) < 0.02 and abs(Y(cy) - mine[n][0]) < 6e-5 and abs(bx - cx) < 0.11 and abs((Y(by1) + Y(by2)) / 2 - mine[n][0]) < 6e-5 and 0.75 < abs(Y(by2) - Y(by1)) / 2 / mine[n][1] < 1.3 and fill == want and col == want, (X(cx), Y(cy)))
def poly(i): m = re.search(r'<polyline id="%s"[^>]*points="([^"]+)"' % i, svg); return [(float(a), float(b)) for a, b in (p.split(',') for p in m.group(1).split())]
g = J['gamma']; cv = poly('curve'); worst = max(abs(Y(py) - model(round(X(px)), g)) for px, py in cv)
ok('the solid curve has a point at every size from 80 to 124, and each is what the rounded quantity gives by my own sum (the furthest %.5f off); its skewness %.3f is the ruler\'s +0.079' % (worst, g), [round(X(px)) for px, py in cv] == list(range(80, 125)) and all(abs(X(px) - round(X(px))) < 0.02 for px, py in cv) and worst < 1.5e-4 and abs(g - 0.079) < 0.001 and 'standardized third cumulant, from the 100-point clouds: +0.079' in open(os.path.join(HERE, 'ruler5.out')).read())
lv = poly('level'); ok('the dashed line is the fourth sheet\'s straight line less 0.08227 n^(1/3) at every size (-0.0424 to -0.0425)', [round(X(px)) for px, py in lv] == list(range(80, 125)) and max(abs(Y(py) - (level_of(round(X(px))) - C5 * round(X(px)) ** (1 / 3.0))) for px, py in lv) < 6e-5)
mt = [(float(m), float(x), lab) for m, x, lab in re.findall(r'<text class="mlab" data-m="([\d.]+)" x="([\d.]+)"[^>]*>([^<]+)</text>', svg)]; mk = [(float(m), float(x)) for m, x in re.findall(r'<line class="mtick" data-m="([\d.]+)" x1="([\d.]+)"', svg)]
ok('six marks along the top, at the sizes where the expected mean count is 9, 9.5, 10, 10.5, 11 and 11.5, each labelled', [m for m, x, lab in mt] == [9.0, 9.5, 10.0, 10.5, 11.0, 11.5] and all(abs(mean_of(X(x)) - m) < 0.006 for m, x, lab in mt) and all(float(lab) == m for m, x, lab in mt) and [x for m, x in mk] == [x for m, x, lab in mt] and 'the mean count expected at each size' in svg)
ok('the sizes of the sheet sit where it says: mean counts expected %s' % ', '.join('%.2f' % mean_of(n) for n in (83, 90, 98, 105, 113, 120)), all(abs(mean_of(n) - m) < 0.06 for n, m in zip((83, 90, 98, 105, 113, 120), (9, 9.5, 10, 10.5, 11, 11.5))))
title = re.search(r'font-weight="600">([^<]+)</text>', svg).group(1); Z = (mine[90][0] + mine[105][0] + mine[120][0]) / 3 - (mine[83][0] + mine[98][0] + mine[113][0]) / 3; Ze = math.sqrt(sum(mine[n][1] ** 2 for n in (83, 90, 98, 105, 113, 120))) / 3
Zm = (model(90, g) + model(105, g) + model(120, g)) / 3 - (model(83, g) + model(98, g) + model(113, g)) / 3
want = 'A count in whole layers: its variance swings as the mean passes whole numbers and halves' if Z >= 0.008 else 'No swing: the variance runs level as the mean count passes whole numbers and halves' if Z <= 0.004 else None
ok('the title is the one that Z calls for: Z = %+.4f (%.4f) by my own sum from the files, the rounded quantity\'s %+.4f; and zfig.json holds the same Z' % (Z, Ze, Zm), (title == want or (want is None and title.startswith('A swing smaller'))) and J['title'] == title and abs(J['Z'][0] - Z) < 1e-9 and abs(Zm - 0.0131) < 3e-4)
keys = re.findall(r'<circle class="key"[^>]*fill="([^"]+)"/>\s*<text[^>]*>([^<]+)</text>', svg)
ok('the key names both sets of dots in their colours (and says the orange one is the curve\'s source), the curve and the dashed line; the lines under the title say what is plotted and that the curve was fixed before the blue clouds were peeled', keys == [('#2a78d6', 'the fifth sheet&#8217;s discs'), ('#eb6834', 'the fourth sheet&#8217;s 100 points (the curve&#8217;s source)')] and 'a rounded quantity' in svg and '>a level run<' in svg and 'less 0.08227&#183;n^(1/3)' in svg and 'The curve was fixed before the blue clouds were peeled' in svg)
ok('zfig.json holds the dots\' values and the curve', all(abs(J['dots'][str(n)][0] - mine[n][0]) < 1e-9 and J['dots'][str(n)][2] == mine[n][2] for n in mine) and len(J['curve']) == 45)
kl = [float(x) for x in re.findall(r'<line x1="([\d.]+)" y1="98"', svg)]; kt = [(float(x), lab) for x, lab in re.findall(r'<text x="([\d.]+)" y="102\.0"[^>]*>([^<]+)</text>', svg)]; width = lambda lab: 6.6 * len(re.sub(r'&#\d+;', 'x', lab))      # about 6.6 pixels a letter at this size
ok('in the key each line starts at least 12 pixels after the words before it end (by a count of letters), and the last words end inside the picture', len(kl) == 2 and all(min(x0 - (tx + width(lab)) for tx, lab in kt if tx < x0) >= 12 for x0 in kl) and max(tx + width(lab) for tx, lab in kt) < 880, [(round(x0), round(min(x0 - (tx + width(lab)) for tx, lab in kt if tx < x0))) for x0 in kl])
env = dict(os.environ, LD_LIBRARY_PATH=os.path.expanduser('~/web/sysroot/usr/lib/x86_64-linux-gnu'))
r = subprocess.run(['node', 'shot-svg.js', os.path.join(HERE, 'swing.svg'), '900', '520', os.path.join(HERE, 'swing.png')], cwd=os.path.expanduser('~/web'), env=env, capture_output=True, text=True)
ok('drawn by a browser: no script errors, every line of words inside the picture, none lying on another', 'PICTURE: ok' in r.stdout and 'outside the picture: []' in r.stdout and 'overlapping: []' in r.stdout, r.stdout[-200:])
print('%d passed, %d failed' % (npass, nfail)); sys.exit(1 if nfail else 0)
