"""bfigtest.py: small.svg read back. Every dot, bar and line is turned into values through the plate's own tick labels and compared
with figures computed here from the runs (the variances from the files, the least-squares line written out again); the title is
checked against the fit; and the picture is drawn by a browser to see that every word is inside it and none lies on another.
python -I bfigtest.py"""
import json, math, os, re, subprocess, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import fresh, study3, study4
svg = open(os.path.join(HERE, 'small.svg'), encoding='utf-8').read(); J = json.load(open(os.path.join(HERE, 'bfig.json')))
npass = nfail = 0
def ok(name, cond, detail=''):
    global npass, nfail
    if cond: npass += 1; print('pass  ' + name)
    else: nfail += 1; print('FAIL  ' + name + ('   ' + str(detail) if detail != '' else ''))
# my own figures, from the files: the variance over the theory's c n^(1/3), c written out from alpha and D
ALPHA, D = 1.3259, 1.081; CTH = (D * 3 / (4 * math.pi) - (4 / 9.0) * ALPHA ** 2 * 0.5625 / math.pi) / math.pi ** (1 / 3.0); SHEET = {100: 4, 300: 4, 1000: 4, 3000: 3, 10000: 3, 30000: 3, 100000: 3, 300000: 3}
V = {n: fresh.counts('n%d-disc-%d' % (SHEET[n], n)) for n in SHEET}; mine = {n: (float(V[n].var(ddof=1)) / (CTH * n ** (1 / 3.0)), float(V[n].var(ddof=1)) * math.sqrt(2.0 / len(V[n])) / (CTH * n ** (1 / 3.0))) for n in SHEET}
ok('the theory\'s coefficient written out here in closed form, %.6f, is the one on the plate and in bfig.json (the flow program\'s, %.6f) to 2 parts in 100,000' % (CTH, J['theory_c']), abs(CTH - J['theory_c']) < 2e-6 and ('where the theory has %.4f&#183;n^(1/3)' % CTH) in svg)
yt = [(float(v), float(y) - 4) for v, y in re.findall(r'<text class="ytick" data-v="([^"]+)" x="[\d.]+" y="([\d.]+)"', svg)]
ok('the nine tick labels up the side show the values they stand at, 0.88 to 1.04', len(yt) == 9 and all(abs(float(a) - float(b)) < 1e-9 for a, b in re.findall(r'<text class="ytick" data-v="([^"]+)"[^>]*>([^<]+)</text>', svg)) and abs(yt[0][0] - 0.88) < 1e-9 and abs(yt[-1][0] - 1.04) < 1e-9)
Y = lambda py: yt[0][0] + (yt[-1][0] - yt[0][0]) * (py - yt[0][1]) / (yt[-1][1] - yt[0][1])
xt = [(int(n), float(x), lab) for n, x, lab in re.findall(r'<text class="xtick" data-n="(\d+)" x="([\d.]+)"[^>]*>([^<]+)</text>', svg)]; tk = [(int(n), float(x)) for n, x in re.findall(r'<line class="tick" data-n="(\d+)" x1="([\d.]+)"', svg)]
x0 = [x for n, x, lab in xt if n == 0][0]; x1 = [x for n, x, lab in xt if n == 100][0]; X = lambda px: (px - x0) / (x1 - x0) * 100 ** (-1 / 3.0)
ok('seven labelled ticks along the foot stand at n^(-1/3) for the n they name, "very many" at nought; nine marks, the two without a label at 300,000 and 30,000 as the foot says', len(xt) == 7 and all(abs(X(x) - (n ** (-1 / 3.0) if n else 0)) < 1e-4 for n, x, lab in xt) and all(lab == (format(n, ',') if n else 'very many') for n, x, lab in xt)
   and sorted(n for n, x in tk) == [0, 100, 300, 1000, 3000, 10000, 30000, 100000, 300000] and all(abs(X(x) - (n ** (-1 / 3.0) if n else 0)) < 1e-4 for n, x in tk) and 'the unlabelled marks are 300,000 and 30,000' in svg)
dots = {int(n): (float(cx), float(cy), fill) for n, cx, cy, fill in re.findall(r'<circle class="dot" data-n="(\d+)" cx="([\d.]+)" cy="([\d.]+)" r="5" fill="([^"]+)"', svg)}; bars = {int(n): (float(x), float(a), float(b_), col) for n, x, a, b_, col in re.findall(r'<line class="bar" data-n="(\d+)" x1="([\d.]+)" y1="([\d.]+)" x2="[\d.]+" y2="([\d.]+)" stroke="([^"]+)"', svg)}
ok('eight dots, one for each size of the two sheets', sorted(dots) == sorted(SHEET))
for n in sorted(dots):
    cx, cy, fill = dots[n]; bx, by1, by2, col = bars[n]; r, se = mine[n]; want = '#eb6834' if SHEET[n] == 4 else '#2a78d6'
    ok('%s points: the dot is at n^(-1/3) and at %.4f, the variance from the file over the theory\'s; its bar is one error either way (%.4f; mine by the normal rule, to a fifth); %s' % (format(n, ','), r, se, 'orange, the fourth sheet\'s' if SHEET[n] == 4 else 'blue, the third sheet\'s'),
       abs(X(cx) - n ** (-1 / 3.0)) < 1e-4 and abs(Y(cy) - r) < 3e-4 and abs(bx - cx) < 0.11 and abs((Y(by2) + Y(by1)) / 2 - r) < 3e-4 and 0.8 < (Y(by2) - Y(by1)) / 2 / se < 1.25 and fill == want and col == want, (X(cx), Y(cy), (Y(by2) - Y(by1)) / 2))
def seg(i): m = re.search(r'<line id="%s" x1="([\d.]+)" y1="([\d.]+)" x2="([\d.]+)" y2="([\d.]+)"' % i, svg); return [float(v) for v in m.groups()]
p = seg('plain'); ok('the dashed line named "the theory" is 1 across the plate', abs(Y(p[1]) - 1) < 2e-4 and abs(Y(p[3]) - 1) < 2e-4 and abs(X(p[0])) < 1e-4 and X(p[2]) > 0.22 and '>the theory<' in svg)
# the third sheet's line: variance = c5 n^(1/3) + b5 fitted here to its five sizes, over the theory's
def line(sizes):
    x = np.array([n ** (1 / 3.0) for n in sizes]); y = np.array([float(V[n].var(ddof=1)) for n in sizes]); w = np.array([1 / (float(V[n].var(ddof=1)) * math.sqrt(2.0 / len(V[n]))) ** 2 for n in sizes]); A = np.stack([x, np.ones_like(x)], 1); cov = np.linalg.inv(A.T @ (A * w[:, None])); be = cov @ (A.T @ (w * y)); return be, np.sqrt(np.diag(cov)), float((w * (y - A @ be) ** 2).sum())
b5, e5, chi5 = line([n for n in SHEET if SHEET[n] == 3]); t = seg('third')
ok('the other dashed line is the third sheet\'s: its five sizes fitted here give %.5f n^(1/3) %+.4f; the sheet wrote 0.08227 and -0.0473; over the theory\'s that is %.4f %+.3f n^(-1/3), drawn right across and named' % (b5[0], b5[1], 0.08227 / CTH, -0.0473 / CTH),
   abs(b5[0] - 0.08227) < 1.5e-4 and abs(b5[1] + 0.0473) < 2e-3 and abs(Y(t[1]) - 0.08227 / CTH) < 3e-4 and abs(Y(t[3]) - (0.08227 - 0.0473 * X(t[2])) / CTH) < 3e-4 and abs(X(t[0])) < 1e-4 and X(t[2]) > 0.22 and 'the third sheet&#8217;s line, carried down' in svg and '0.08227 n^(1/3) − 0.0473' in open(os.path.join(HERE, 'expectations-4.md'), encoding='utf-8').read())
b8, e8, chi8 = line(sorted(SHEET)); f = seg('fit')
ok('the solid line is the straight line fitted here to all eight variances (%.5f n^(1/3) %+.4f, chi-square %.1f on 6; errors by the normal rule), over the theory\'s, drawn from very many points to 100 and no further' % (b8[0], b8[1], chi8),
   abs(X(f[0])) < 1e-4 and abs(Y(f[1]) - b8[0] / CTH) < 6e-4 and abs(X(f[2]) - 100 ** (-1 / 3.0)) < 1e-4 and abs(Y(f[3]) - (b8[0] + b8[1] * X(f[2])) / CTH) < 6e-4 and abs(J['fit']['c'] - b8[0]) < 5e-5 and abs(J['fit']['b'] - b8[1]) < 5e-4, (Y(f[1]), b8[0] / CTH, Y(f[3])))
ad = re.search(r'<circle id="adot" cx="([\d.]+)" cy="([\d.]+)"', svg)
ok('where the solid line ends there is a dot, and beside it the figures %.4f (%.4f); the line\'s equation is written on the plate as it is in bfig.json' % (J['fit']['a'], J['fit']['a_se']), abs(Y(float(ad.group(2))) - J['fit']['a']) < 2e-4 and abs(X(float(ad.group(1)))) < 1e-4 and ('>%.4f (%.4f)<' % (J['fit']['a'], J['fit']['a_se'])) in svg
   and ('variance = %.4f&#183;n^(1/3) &#8722; %.3f' % (J['fit']['c'], -J['fit']['b'])) in svg and abs(J['fit']['a'] - J['fit']['c'] / CTH) < 5e-5 and abs(J['fit']['a_se'] - e8[0] / CTH) < 3e-4)
title = re.search(r'font-weight="600">([^<]+)</text>', svg).group(1)
worst = max((abs(mine[n][0] - (b8[0] + b8[1] * n ** (-1 / 3.0)) / CTH) / mine[n][1], n) for n in SHEET)
left = [float(V[n].var(ddof=1)) - b8[0] * n ** (1 / 3.0) for n in SHEET]
ok('the title says a line 1.7 in 100 steeper than the theory\'s, less 0.04, fits from 100 points to 300,000: the line fitted here is %.4f of the theory\'s (%.0f of its errors above 1), its constant %.4f, %.0f of its errors from nought; the chi-square about the line is %.1f on 6 (below 16.8, the one-in-a-hundred mark); the dot furthest from the line is %.1f errors off (%s points); and the eight variances less the line\'s first term run from %.3f to %.3f' % (b8[0] / CTH, (b8[0] / CTH - 1) / (e8[0] / CTH), b8[1], abs(b8[1] / e8[1]), chi8, worst[0], format(worst[1], ','), min(left), max(left)),
   title == 'A line 1.7 in 100 steeper than the theory&#8217;s, less 0.04, fits from 100 points to 300,000' and '%.1f' % (100 * (b8[0] / CTH - 1)) == '1.7' and (b8[0] / CTH - 1) / (e8[0] / CTH) > 5 and chi8 <= 16.8 and b8[1] / e8[1] < -5 and worst[0] < 3.5 and J['title'] == title and -0.0445 < b8[1] < -0.0355 and -0.055 < min(left) and max(left) < -0.025)
keys = re.findall(r'<circle class="key"[^>]*fill="([^"]+)"/>\s*<text[^>]*>([^<]+)</text>', svg); ses = [mine[n][1] for n in SHEET]; sub = re.search(r'Bars: one standard error either way \((\d\.\d{3}) to (\d\.\d{3}); most are hidden by their dots\)', svg)
hidden = sum(1 for n in dots if abs(bars[n][1] - bars[n][2]) / 2 <= 5.0)
ok('the key names both sets of dots in their colours, the solid line and the dashed lines; the line under the title gives the errors\' range (%.3f to %.3f) and says most bars are hidden by their dots (%d of 8 are)' % (min(ses), max(ses), hidden),
   keys == [('#2a78d6', 'the third sheet&#8217;s discs'), ('#eb6834', 'the fourth sheet&#8217;s discs')] and 'the line fitted' in svg and 'the theory; the third sheet&#8217;s line carried down' in svg and sub is not None and abs(float(sub.group(1)) - min(ses)) < 6e-4 and abs(float(sub.group(2)) - max(ses)) < 6e-4 and hidden >= 5)
ok('bfig.json holds the dots\' values', all(abs(J['sizes'][str(n)][0] - mine[n][0]) < 3e-5 and J['sizes'][str(n)][3] == SHEET[n] and J['sizes'][str(n)][2] == len(V[n]) for n in SHEET))
env = dict(os.environ, LD_LIBRARY_PATH=os.path.expanduser('~/web/sysroot/usr/lib/x86_64-linux-gnu'))
r = subprocess.run(['node', 'shot-svg.js', os.path.join(HERE, 'small.svg'), '900', '520', os.path.join(HERE, 'small.png')], cwd=os.path.expanduser('~/web'), env=env, capture_output=True, text=True)
ok('drawn by a browser: no script errors, every line of words inside the picture, none lying on another', 'PICTURE: ok' in r.stdout and 'outside the picture: []' in r.stdout and 'overlapping: []' in r.stdout, r.stdout[-200:])
print('%d passed, %d failed' % (npass, nfail)); sys.exit(1 if nfail else 0)
