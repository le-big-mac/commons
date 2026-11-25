"""qfigtest.py: quarter.svg read back. Every dot and bar is turned into a value through the plate's own tick labels and compared with
what study.py, fresh.py and study2.py give from the runs; the title is checked against the numbers; and the picture is drawn by a
browser to see that every word is inside it and none lies on another.   python -I qfigtest.py"""
import json, math, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import study, study2, fresh
svg = open(os.path.join(HERE, 'quarter.svg'), encoding='utf-8').read(); J = json.load(open(os.path.join(HERE, 'qfig.json')))
npass = nfail = 0
def ok(name, cond, detail=''):
    global npass, nfail
    if cond: npass += 1; print('pass  ' + name)
    else: nfail += 1; print('FAIL  ' + name + ('   ' + str(detail) if detail != '' else ''))
yt = [(float(v), float(y) - 4) for v, y in re.findall(r'<text class="ytick" data-v="([^"]+)" x="[\d.]+" y="([\d.]+)"', svg)]
ok('the five tick labels show the values they stand at', len(yt) == 5 and all(abs(float(a) - float(b)) < 1e-9 for a, b in re.findall(r'<text class="ytick" data-v="([^"]+)"[^>]*>([^<]+)</text>', svg)))
Y = lambda py: yt[0][0] + (yt[-1][0] - yt[0][0]) * (py - yt[0][1]) / (yt[-1][1] - yt[0][1])
LINE = study2.line_of(1e5)[0]; w, se = study.stat(lambda m, v: v / m ** 2 * 1e5, 'exact-quarter-100000')
want = [(0, 'cloud.c', 100000, study.F['exact-quarter-100000']['K'], w / LINE, se / LINE)]
for key in ('quarter-cloud-a', 'quarter-cloud-b', 'quarter-numpy'): f = fresh.reckon(key); want.append((1, f['maker'], 100000, f['K'], f['w'] / LINE, f['wse'] / LINE))
for key, (name, n) in study2.SETS.items(): v = study2.R[key]; want.append((2, 'cloud.c' if key.startswith('cloud') else 'numpy', n, v['K'], v['r'], v['rse']))
sets = re.findall(r'<g class="set" data-group="(\d)" data-maker="([\w.]+)" data-n="(\d+)" data-k="(\d+)">(.*?)</g>', svg, re.S)
ok('eight sets, in the order they were made: the first sheet\'s, three chased, the second sheet\'s four', [(int(a), b, int(c), int(d)) for a, b, c, d, g in sets] == [(g_, mk, n, K) for g_, mk, n, K, r, s in want], [(a, b, c, d) for a, b, c, d, g in sets])
xs = []
for (grp, maker, n, K, g), (g_, mk, n_, K_, r, s) in zip(sets, want):
    d = re.search(r'<circle class="dot" cx="([\d.]+)" cy="([\d.]+)" r="5" fill="([^"]+)"', g); b = re.search(r'<line class="bar" x1="([\d.]+)" y1="([\d.]+)" x2="[\d.]+" y2="([\d.]+)" stroke="([^"]+)"', g); labels = re.findall(r'<text class="xlabel"[^>]*>([^<]+)</text>', g); xs.append(float(d.group(1)))
    colour = '#2a78d6' if mk == 'cloud.c' else '#eb6834'
    ok('%s clouds of %s points by %s: the dot is at r = %.4f, its bar one error either way (%.4f), in that generator\'s colour, with its numbers under it' % (format(K_, ','), format(n_, ','), mk, r, s),
       abs(Y(float(d.group(2))) - r) < 2e-4 and abs(Y(float(b.group(2))) - (r - s)) < 3e-4 and abs(Y(float(b.group(3))) - (r + s)) < 3e-4 and abs(float(b.group(1)) - float(d.group(1))) < 0.01 and d.group(3) == colour and b.group(4) == colour and labels == [format(K_, ','), format(n_, ',')])
ok('the sets run from left to right', xs == sorted(xs) and len(set(xs)) == 8)
tog = study2.together(study2.ALL); td = re.search(r'<circle id="tdot" cx="([\d.]+)" cy="([\d.]+)"', svg); tb = re.search(r'<line id="tbar" x1="[\d.]+" y1="([\d.]+)" x2="[\d.]+" y2="([\d.]+)"', svg); band = re.search(r'<rect id="band" x="([\d.]+)" y="([\d.]+)" width="[\d.]+" height="([\d.]+)"', svg)
ok('the last mark is the second sheet\'s four sets together (%.4f, error %.4f), to the right of all the sets, on a band from 0.996 to 1.008' % tog, td is not None and abs(Y(float(td.group(2))) - tog[0]) < 2e-4 and abs(Y(float(tb.group(1))) - (tog[0] - tog[1])) < 3e-4 and abs(Y(float(tb.group(2))) - (tog[0] + tog[1])) < 3e-4 and float(td.group(1)) > max(xs) + 30 and abs(Y(float(band.group(2))) - 1.008) < 2e-4 and abs(Y(float(band.group(2)) + float(band.group(3))) - 0.996) < 2e-4)
keys = re.findall(r'<circle class="key"[^>]*fill="([^"]+)"/>\s*<text[^>]*>([^<]+)</text>', svg)
ok('the key: blue for my generator, orange for numpy\'s', keys == [('#2a78d6', 'points from my generator'), ('#eb6834', 'points from numpy&#8217;s')], keys)
ok('the line drawn heavier than the grid is at 1, and it is named', len(re.findall(r'<line class="grid"[^>]*stroke="#898781" stroke-width="1.5"/>', svg)) == 1 and abs(Y(float(re.search(r'<line class="grid" x1="\d+" y1="([\d.]+)"[^>]*stroke="#898781"', svg).group(1))) - 1.0) < 1e-9 and 'the theory&#8217;s line for the quarter disc' in svg)
title = re.search(r'font-weight="600">([^<]+)</text>', svg).group(1)
ok('the title says the four sealed sets together stand at %.3f, give or take %.3f, and "on its line to %.1f parts in 100" (two errors), which the band allows' % (tog + (200 * tog[1],)), title == 'The quarter disc is on its line to %.1f parts in 100: the four sealed sets give %.3f (%.3f)' % (200 * tog[1], tog[0], tog[1]) and 0.996 <= tog[0] <= 1.008 and abs(tog[0] - 1) < 2 * tog[1], title)
ok('the three groups are named: the first sheet; peeled to chase it, in no verdict; the second sheet, sealed before', all(t in svg for t in ('the first', 'peeled to chase it, in no verdict', 'the second sheet: sealed before they were peeled')))
ok('qfig.json holds the same numbers', len(J['rows']) == 8 and all(abs(a['r'] - b[4]) < 1e-12 for a, b in zip(J['rows'], want)) and abs(J['together'][0] - tog[0]) < 1e-12)
env = dict(os.environ, LD_LIBRARY_PATH=os.path.expanduser('~/web/sysroot/usr/lib/x86_64-linux-gnu'))
r = subprocess.run(['node', 'shot-svg.js', os.path.join(HERE, 'quarter.svg'), '940', '520', os.path.join(HERE, 'quarter.png')], cwd=os.path.expanduser('~/web'), env=env, capture_output=True, text=True)
ok('drawn by a browser: no script errors, every line of words inside the picture, none lying on another', 'PICTURE: ok' in r.stdout and 'outside the picture: []' in r.stdout and 'overlapping: []' in r.stdout, r.stdout[-200:])
print('%d passed, %d failed' % (npass, nfail)); sys.exit(1 if nfail else 0)
