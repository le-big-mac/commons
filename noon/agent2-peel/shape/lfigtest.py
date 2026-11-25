"""lfigtest.py: lean.svg read back. Every dot, bar and line is turned into values through the plate's own tick labels and compared
with what study3.py gives from the runs; the title is checked against the fitted slope; and the picture is drawn by a browser to
see that every word is inside it and none lies on another.   python -I lfigtest.py"""
import json, math, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import study3
svg = open(os.path.join(HERE, 'lean.svg'), encoding='utf-8').read(); J = json.load(open(os.path.join(HERE, 'lfig.json')))
npass = nfail = 0
def ok(name, cond, detail=''):
    global npass, nfail
    if cond: npass += 1; print('pass  ' + name)
    else: nfail += 1; print('FAIL  ' + name + ('   ' + str(detail) if detail != '' else ''))
yt = [(float(v), float(y) - 4) for v, y in re.findall(r'<text class="ytick" data-v="([^"]+)" x="[\d.]+" y="([\d.]+)"', svg)]
ok('the seven tick labels up the side show the values they stand at', len(yt) == 7 and all(abs(float(a) - float(b)) < 1e-9 for a, b in re.findall(r'<text class="ytick" data-v="([^"]+)"[^>]*>([^<]+)</text>', svg)))
Y = lambda py: yt[0][0] + (yt[-1][0] - yt[0][0]) * (py - yt[0][1]) / (yt[-1][1] - yt[0][1])
xt = [(int(n), float(x), lab) for n, x, lab in re.findall(r'<text class="xtick" data-n="(\d+)" x="([\d.]+)"[^>]*>([^<]+)</text>', svg)]
x0 = [x for n, x, lab in xt if n == 0][0]; x3 = [x for n, x, lab in xt if n == 3000][0]; X = lambda px: (px - x0) / (x3 - x0) * 3000 ** (-1 / 3.0)
ok('the six ticks along the foot stand at n^(-1/3) for the n they name, "very many" at nought', len(xt) == 6 and all(abs(X(x) - (n ** (-1 / 3.0) if n else 0)) < 2e-5 for n, x, lab in xt) and all(lab == (format(n, ',') if n else 'very many') for n, x, lab in xt))
R = study3.R; F4 = study3.F4
dots = {int(n): (float(cx), float(cy), fill) for n, cx, cy, fill in re.findall(r'<circle class="dot" data-n="(\d+)" cx="([\d.]+)" cy="([\d.]+)" r="5" fill="([^"]+)"', svg)}; bars = {int(n): (float(x), float(a), float(b)) for n, x, a, b in re.findall(r'<line class="bar" data-n="(\d+)" x1="([\d.]+)" y1="([\d.]+)" x2="[\d.]+" y2="([\d.]+)"', svg)}
ok('five dots, one for each size of the sheet', sorted(dots) == [3000, 10000, 30000, 100000, 300000])
for n in sorted(dots):
    cx, cy, fill = dots[n]; bx, by1, by2 = bars[n]
    ok('%s points: the dot is at n^(-1/3) and at r = %.4f, its bar one error either way (%.4f), blue' % (format(n, ','), R[n]['r'], R[n]['rse']), abs(X(cx) - n ** (-1 / 3.0)) < 3e-5 and abs(Y(cy) - R[n]['r']) < 1e-4 and abs(Y(by1) - (R[n]['r'] - R[n]['rse'])) < 1.5e-4 and abs(Y(by2) - (R[n]['r'] + R[n]['rse'])) < 1.5e-4 and abs(bx - cx) < 0.01 and fill == '#2a78d6')
def seg(i): m = re.search(r'<line id="%s" x1="([\d.]+)" y1="([\d.]+)" x2="([\d.]+)" y2="([\d.]+)"' % i, svg); return [float(v) for v in m.groups()]
p = seg('plain'); ok('the dashed line named "plain" is r = 1 across the plate', abs(Y(p[1]) - 1) < 1e-4 and abs(Y(p[3]) - 1) < 1e-4 and abs(X(p[0])) < 1e-4 and X(p[2]) > 0.07 and '>plain<' in svg)
l = seg('lean'); ok('the other dashed line is r = 1.018 - 0.64 n^(-1/3), the reading written on the sheet, and is named', abs(Y(l[1]) - (1.018 - 0.64 * X(l[0]))) < 1e-4 and abs(Y(l[3]) - (1.018 - 0.64 * X(l[2]))) < 1e-4 and X(l[2]) - X(l[0]) > 0.07 and 'the lean read from the earlier clouds' in svg and 's = −0.64 and a = 1.018' in open(os.path.join(HERE, 'expectations-3.md'), encoding='utf-8').read())
f = seg('fit'); ok('the solid line is the line fitted to the four sizes (r = %.4f %+.3f n^(-1/3)), drawn from very many points to 10,000 and no further' % (F4[2], F4[0]), abs(X(f[0])) < 1e-4 and abs(Y(f[1]) - F4[2]) < 1e-4 and abs(X(f[2]) - 10000 ** (-1 / 3.0)) < 3e-5 and abs(Y(f[3]) - (F4[2] + F4[0] * 10000 ** (-1 / 3.0))) < 1e-4)
ad = re.search(r'<circle id="adot" cx="([\d.]+)" cy="([\d.]+)"', svg); ab = re.search(r'<line id="abar" x1="[\d.]+" y1="([\d.]+)" x2="[\d.]+" y2="([\d.]+)"', svg)
ok('where the solid line ends there is a dot with a bar: %.4f, one error either way (%.4f), and the figures written beside it' % (F4[2], F4[3]), abs(Y(float(ad.group(2))) - F4[2]) < 1e-4 and abs(X(float(ad.group(1)))) < 1e-4 and abs(Y(float(ab.group(1))) - (F4[2] - F4[3])) < 1.5e-4 and abs(Y(float(ab.group(2))) - (F4[2] + F4[3])) < 1.5e-4 and '>%.3f (%.3f)<' % (F4[2], F4[3]) in svg)
title = re.search(r'font-weight="600">([^<]+)</text>', svg).group(1)
ok('the title says the smaller the cloud the lower its spread, below the theory under 30,000 points and above it over: the fitted slope is %.3f, more than four of its errors (%.3f) below nought and below -0.32; r rises from each size to the next; it is below 1 at 3,000 and 10,000 points and above at 30,000, 100,000 and 300,000' % (F4[0], F4[1]), title == 'The smaller the cloud, the lower: below the theory under 30,000 points, above it over' and all(R[n]['r'] >= 1 for n in (30000, 100000, 300000)) and F4[0] <= -0.32 and F4[0] < -4 * F4[1] and all(R[a]['r'] < R[b]['r'] for a, b in zip((3000, 10000, 30000, 100000), (10000, 30000, 100000, 300000))) and R[3000]['r'] < 1 and R[10000]['r'] < 1)
keys = re.findall(r'<circle class="key"[^>]*fill="([^"]+)"/>\s*<text[^>]*>([^<]+)</text>', svg); ok('the key names the dots, the solid line and the dashed lines', keys == [('#2a78d6', 'the third sheet&#8217;s discs')] and 'the line fitted' in svg and 'the two readings written beforehand' in svg and 'fitted to the four sizes from 10,000 to 300,000' in svg)
ok('lfig.json holds the same numbers', all(abs(J['sizes'][str(n)][0] - R[n]['r']) < 1e-12 for n in dots) and abs(J['fit'][0] - F4[0]) < 1e-12 and J['lean'] == [1.018, -0.64])
env = dict(os.environ, LD_LIBRARY_PATH=os.path.expanduser('~/web/sysroot/usr/lib/x86_64-linux-gnu'))
r = subprocess.run(['node', 'shot-svg.js', os.path.join(HERE, 'lean.svg'), '900', '500', os.path.join(HERE, 'lean.png')], cwd=os.path.expanduser('~/web'), env=env, capture_output=True, text=True)
ok('drawn by a browser: no script errors, every line of words inside the picture, none lying on another', 'PICTURE: ok' in r.stdout and 'outside the picture: []' in r.stdout and 'overlapping: []' in r.stdout, r.stdout[-200:])
print('%d passed, %d failed' % (npass, nfail)); sys.exit(1 if nfail else 0)
