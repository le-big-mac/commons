"""figtest.py: far.svg read back. Every mark's place is turned into a value through the plate's own tick labels and compared with
farfig.json and with after.out; every mark and every label is inside the picture.   python -I figtest.py"""
import json, math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); svg = open(os.path.join(HERE, 'far.svg'), encoding='utf-8').read(); J = json.load(open(os.path.join(HERE, 'farfig.json')))
npass = nfail = 0
def ok(name, cond, detail=''):
    global npass, nfail
    if cond: npass += 1; print('pass  ' + name)
    else: nfail += 1; print('FAIL  ' + name + ('   ' + str(detail) if detail else ''))
def part(i): return re.search(r'<g id="%s">(.*?)</g>' % i, svg, re.S).group(1)
def axis(g, cls, log):
    t = [(float(v), float(x), float(y)) for v, x, y in re.findall(r'<text class="%s" data-v="([^"]+)" x="([\d.]+)" y="([\d.]+)"' % cls, g)]
    labels = re.findall(r'<text class="%s" data-v="([^"]+)"[^>]*>([^<]+)</text>' % cls, g)
    assert all(abs(float(a) - float(b.replace(',', ''))) < 1e-9 for a, b in labels), labels      # the label shown is the value it stands at
    (v0, x0, y0), (v1, x1, y1) = t[0], t[-1]; f = (lambda v: math.log(v)) if log else (lambda v: v); inv = (lambda u: math.exp(u)) if log else (lambda u: u)
    if cls == 'xtick': return lambda px: inv(f(v0) + (f(v1) - f(v0)) * (px - x0) / (x1 - x0))
    return lambda py: inv(f(v0) + (f(v1) - f(v0)) * (py + 4 - y0 - 4) / (y1 - y0))
L = part('left'); X = axis(L, 'xtick', True); Y = axis(L, 'ytick', False)
marks = [(X(float(cx)), Y(float(cy) + 4)) for cx, cy in re.findall(r'<circle class="measured" cx="([\d.]+)" cy="([\d.]+)"', L)]
ok('left plate: %d dots, each read back through the tick labels to the height and the value in farfig.json (within 1 in 300 of the height and 0.002 of the value)' % len(marks),
   len(marks) == len(J['left']) == 9 and all(abs(h / p['height'] - 1) < 0.004 and abs(r - p['ratio']) < 0.002 for (h, r), p in zip(marks, J['left'])), marks)
after = open(os.path.join(HERE, 'after.out')).read(); tab = {int(a): float(b) for a, b in re.findall(r'^\s+(\d+)\s+[\d.]+\s+(0\.\d{3})\s+[\d.]+\s+[\d.]+$', after, re.M)}
ok('and they are the table of after.out (C), height by height', all(abs(tab[p['height']] - p['ratio']) < 0.0006 for p in J['left']) and len(tab) == 9, tab)
lv = re.search(r'<line id="level" x1="([\d.]+)" y1="([\d.]+)" x2="([\d.]+)" y2="([\d.]+)"', L).groups(); study = open(os.path.join(HERE, 'study.out')).read()
want = float(re.search(r'0\.600 D = ([\d.]+);', study).group(1))
ok('the level line is flat, runs from 500 to 128,000, and stands at 0.600 D = %.3f of study.out (read back: %.3f)' % (want, Y(float(lv[1]) + 4)), lv[1] == lv[3] and abs(Y(float(lv[1]) + 4) - want) < 0.002 and abs(X(float(lv[0])) / 500 - 1) < 0.01 and abs(X(float(lv[2])) / 128000 - 1) < 0.01)
op = [tuple(map(float, q.split(','))) for q in re.search(r'<polyline id="other" points="([^"]+)"', L).group(1).split()]
ok('the curve of the other kind starts at the measured value at 4,000 and rises as the sixth root of the height (to %.2f at 128,000)' % Y(op[-1][1] + 4),
   abs(X(op[0][0]) / 4000 - 1) < 0.01 and abs(Y(op[0][1] + 4) - J['other_at_4000']) < 0.002 and all(abs(Y(py + 4) - J['other_at_4000'] * (X(px) / 4000) ** (1 / 6.0)) < 0.004 for px, py in op) and abs(X(op[-1][0]) / 128000 - 1) < 0.01)
R = part('right'); X2 = axis(R, 'xtick', True); Y2 = axis(R, 'ytick', False); bad = 0; n = 0
for c in J['right']:
    got = [(X2(float(cx)), Y2(float(cy) + 4)) for cx, cy in re.findall(r'<circle class="curve h%d" cx="([\d.]+)" cy="([\d.]+)"' % c['height'], R)]
    n += len(got); bad += len(got) != len(c['points']) or any(abs(gx / p['x'] - 1) > 0.01 or abs(gy - p['g']) > 0.003 for (gx, gy), p in zip(got, c['points']))
ok('right plate: %d dots in four heights (%s), each read back to its distance over root height and its value' % (n, ', '.join(str(c['height']) for c in J['right'])), bad == 0 and n == 96 and [c['height'] for c in J['right']] == [2000, 8000, 31999, 127996])
def shape(s): return 1 - math.exp(-s * s) + s * math.sqrt(math.pi) * math.erfc(s)
tp = [tuple(map(float, q.split(','))) for q in re.search(r'<polyline id="theory" points="([^"]+)"', R).group(1).split()]
ok('the predicted curve drawn is 1 - exp(-s^2) + s sqrt(pi) erfc(s) with s = x / sqrt(8/3), at each of its %d points' % len(tp), all(abs(Y2(py + 4) - shape(X2(px) / math.sqrt(8 / 3.0))) < 0.004 for px, py in tp) and len(tp) > 100)
far = [abs(p['g'] - shape(p['x'] / math.sqrt(8 / 3.0))) for c in J['right'] for p in c['points'] if p['r'] >= 48]
ok('the dots from 48 apart outward lie within %.3f of that curve (the README says within 0.06)' % max(far), max(far) < 0.06)
W_, H_ = map(int, re.search(r'viewBox="0 0 (\d+) (\d+)"', svg).groups())
xs = [float(v) for v in re.findall(r'\bc?x[12]?="([\d.]+)"', svg)]; ys = [float(v) for v in re.findall(r'\bc?y[12]?="([\d.]+)"', svg)]
pl = [tuple(map(float, q.split(','))) for m in re.findall(r'points="([^"]+)"', svg) for q in m.split()]
ok('every mark is inside the picture (%d by %d)' % (W_, H_), all(0 <= v <= W_ for v in xs) and all(0 <= v <= H_ for v in ys) and all(0 <= a <= W_ and 0 <= b <= H_ for a, b in pl))
texts = re.findall(r'<text x="([\d.]+)" y="([\d.]+)" font-size="(\d+)" fill="[^"]+" text-anchor="(\w+)"[^>]*>([^<]+)</text>', svg); over = []
for x, y, fs, anc, t in texts:
    w = 0.56 * int(fs) * len(t); x = float(x); a, b = (x, x + w) if anc == 'start' else (x - w, x) if anc == 'end' else (x - w / 2, x + w / 2)
    if a < 0 or b > W_: over.append(t)
ok('no line of words runs off the picture, at a generous width for each letter (%d lines)' % len(texts), not over and len(texts) >= 12, over)
ok('no words in a series colour; the two colours of the left plate and the four of the right are those that were validated', not re.search(r'<text[^>]*fill="#(2a78d6|eb6834|86b6ef|3987e5|1c5cab|0d366b)"', svg) and all(c in svg for c in ('#2a78d6', '#eb6834', '#86b6ef', '#3987e5', '#1c5cab', '#0d366b')))
print('\n%d passed, %d failed' % (npass, nfail)); sys.exit(1 if nfail else 0)
