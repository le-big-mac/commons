"""far/study.py: the nine sealed lines of the addition (far up the cell problem; A1 to A6 in expectations.md, A7 to A9 in
expectations-2.md), each computed from runs/ and judged.
   python -I study.py > study.out
   python -I study.py try     the same on small windows in runs-try/ with every height 16 times smaller: only to try the script
   FAR_RUNS=DIR python -I study.py     the same on the windows in DIR (ruler.py uses this with made-up windows whose answers are known)
Each window is one run of cell2 (period 32,768, columns 2 wide): a line of JSON and a profile, one row for each band of height
1 unit thick: band, points, mean depth, variance of depth among the points of the band. The windows of the second batch also
have a file of slabs (cell2 -snap): the mean depth of each column's points in slabs 4 thick at chosen heights."""
import glob, json, math, os, random, subprocess, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); P = lambda *a: os.path.join(HERE, *a); sys.path.insert(0, HERE)
from slabs import slabstats, lags_for
TRY = len(sys.argv) > 1 and sys.argv[1] == 'try'; SC = 16 if TRY else 1; RUNS = os.environ.get('FAR_RUNS') or ('runs-try' if TRY else 'runs')
BIN = os.environ.get('CELL2', P('cell2'))
H4, H2, TOPMIN = 4000 // SC, 2000 // SC, 30000 // SC
THICK = 1.326 ** 2 / 12          # what the thickness of a band (1 unit of height, 1.326 layers) adds to the variance within it
verdicts = []
def line(n, kind, odds, held, text):
    verdicts.append((n, kind, odds, held))
    print('LINE A%d (%s, odds %s): %s. %s\n' % (n, kind, odds, {True: 'HELD', False: 'FAILED', None: 'HALF'}[held], text))

# ---------- the windows ----------
W = []
for f in sorted(glob.glob(P(RUNS, 'run-*.json'))):
    t = open(f).read().strip()
    if not t: continue
    o = json.loads(t); pf = f.replace('run-', 'profile-').replace('.json', '.txt'); a = np.loadtxt(pf if os.path.exists(pf) else pf + '.gz')
    assert len(a) == int(o['HM']) and (a[:, 0] == np.arange(len(a))).all(), f
    W.append({'o': o, 'HM': int(o['HM']), 'c': a[:, 1], 'mu': a[:, 2], 'var': a[:, 3], 'seed': o['seed'], 'seeding': o.get('seeding', 1)})
    sf = f.replace('run-', 'snap-').replace('.json', '.bin'); rf = f.replace('run-', 'slabs-')
    if 'snap_heights' in o and os.path.exists(sf):                    # the raw slabs: one row of column means for each
        raw = np.fromfile(sf, dtype=np.float64).reshape(len(o['snap_heights']), int(o['C'])); lg = lags_for(raw.shape[1])
        W[-1]['snapH'] = o['snap_heights']; W[-1]['lags'] = lg; W[-1]['slab'] = [slabstats(row, lg) for row in raw]
    elif 'snap_heights' in o and os.path.exists(rf):                  # or what reduce.py kept of them
        r = json.load(open(rf)); assert r['heights'] == o['snap_heights']; W[-1]['snapH'] = r['heights']; W[-1]['lags'] = r['lags']; W[-1]['slab'] = r['slabs']
tops = sorted(set(w['HM'] for w in W)); LOW, TALL = tops[0], tops[-1]
assert len(tops) == 2 and TALL == 2 * LOW and LOW >= TOPMIN, tops
SHORT = [w for w in W if w['HM'] == LOW]; LONG = [w for w in W if w['HM'] == TALL]
print('Windows: %d to a height of %d and %d to %d; period %s, columns %s wide; %.3g points peeled in all (those up to the top of each window).' % (
    len(SHORT), LOW, len(LONG), TALL, W[0]['o']['W'], W[0]['o']['wcol'], sum(w['c'].sum() for w in W)))
print('   layers peeled: %s' % ', '.join('%d' % w['o']['layers'] for w in W))
print('   points to the unit of area in each window: %s' % ', '.join('%.5f' % (w['c'].sum() / (w['o']['W'] * w['HM'])) for w in W))

def pool(S, T=None):
    """heights, mean depth and variance of depth (the mean over windows of the variance within each), band by band, of the windows S up to height T;
    where the windows are of different heights, a band has what the windows that reach it give"""
    T = T or max(w['HM'] for w in S); c = np.zeros(T); m = np.zeros(T); v = np.zeros(T)
    for w in S:
        n = min(T, w['HM']); c[:n] += w['c'][:n]; m[:n] += w['c'][:n] * w['mu'][:n]; v[:n] += w['c'][:n] * w['var'][:n]
    return np.arange(T) + 0.5, m / c, v / c
def expo(y, v, lo, hi, how):
    """the exponent b of v = a y^b over lo <= y <= hi by least squares on the logarithms: 'bands', every band a point (so the top of the range, where the
    bands are many, weighs most); 'steps', the bands gathered in 16 equal steps of the logarithm to each doubling (so each doubling weighs the same)"""
    m = (y >= lo) & (y <= hi); yy, vv = y[m], v[m]
    if how == 'bands': return float(np.polyfit(np.log(yy), np.log(vv), 1)[0])
    k = np.floor(16 * np.log2(yy / lo) + 1e-9).astype(int); xs = []; zs = []
    for j in sorted(set(k)): xs.append(math.log(yy[k == j].mean())); zs.append(math.log(vv[k == j].mean()))
    return float(np.polyfit(xs, zs, 1)[0])
def boot(S, fn, n=300, seed=1):
    """the middle 95% of fn over n resamplings of the windows S (with replacement; the windows of each height resampled among themselves)"""
    rng = random.Random(seed); groups = [[w for w in S if w['HM'] == t] for t in sorted(set(w['HM'] for w in S))]
    out = sorted(fn([rng.choice(g) for g in groups for _ in g]) for _ in range(n)); return out[int(0.025 * n)], out[int(0.975 * n) - 1]
def fmt(lohi): return '%.3f to %.3f' % lohi
SETS = [('the %d windows to %d' % (len(SHORT), LOW), SHORT, LOW), ('the %d windows to %d' % (len(LONG), TALL), LONG, TALL),
        ('all %d, up to %d' % (len(W), LOW), W, LOW), ('all %d, the %d tall ones alone above %d' % (len(W), len(LONG), LOW), W, TALL)]

# ---------- A1: the shear ----------
cases = [(200, 20, 1, 4096), (200, 20, 2, -6000), (300, 12, 3, 1), (180, 30, 4, 20480), (400, 50, 5, -1), (1000, 60, 6, 700), (1000, 60, 7, -204800), (2000, 100, 8, 3000),
         (500, 200, 9, -4096), (250, 400, 10, 2048), (3000, 30, 11, 9999), (600, 80, 12, 100000)]
tried = same = pts = 0; worst = ''
for C, HM, seed, S in cases:
    r = subprocess.run([BIN, str(C), '2', str(HM), str(seed), '-sheartest', str(S)], capture_output=True, text=True); tried += 1
    try: o = json.loads(r.stdout)
    except Exception: o = None
    good = bool(o) and o['differ'] == 0 and o['layers'] == o['layers_sheared'] and o['moved'] >= 0.99 * o['points'] and o['points'] > 0.8 * 2 * C * HM
    same += good; pts += o['points'] if o else 0
    if not good: worst += ' [%s]' % (r.stdout.strip()[:200] or r.stderr.strip()[:200])
line(1, 'worked', 0.95, tried == 12 and same == 12, 'twelve windows with walls (360 to 6,000 wide, 12 to 400 high, %s points in all), each peeled to the end as it is and again after (x, y) -> (x, y + s x) with s from 0.0005 to 100 either way: every point has the same depth in %d of %d.%s' % (
    format(pts, ','), same, tried, worst))

# ---------- A2: the exponent of the variance from 4,000 to the top ----------
print('A2. The variance of depth among points at one height as a power of the height, fitted from %d to the top.' % H4)
print('    Fitted two ways (every band a point; 16 equal steps of the logarithm to each doubling), with and without taking off what the thickness of a band adds (%.3f):' % THICK)
allA2 = []
for name, S, T in SETS:
    y, mu, v = pool(S, T); row = []
    for how in ('bands', 'steps'):
        for th in (THICK, 0.0): row.append(expo(y, v - th, H4, T, how))
    allA2 += row
    iv = boot(S, lambda SS: expo(*[pool(SS, T)[i] for i in (0, 2)], H4, T, 'steps')) if len(S) >= 6 else None
    print('    %-46s bands %.3f (%.3f)   steps %.3f (%.3f)%s' % (name + ':', row[0], row[1], row[2], row[3], '   [steps, 95%% of resamplings of the windows: %s]' % fmt(iv) if iv else ''))
per = [expo(w['c'] * 0 + np.arange(w['HM']) + 0.5, w['var'] - THICK, H4, w['HM'], 'steps') for w in W]
print('    window by window (steps): %s' % ', '.join('%.3f' % e for e in per))
lo2, hi2 = min(allA2), max(allA2)
line(2, 'worked', 0.7, True if (lo2 >= 0.45 and hi2 <= 0.55) else False if (hi2 < 0.45 or lo2 > 0.55) else None,
     'over the four ways of taking the windows and the four ways of fitting, the exponent runs from %.3f to %.3f; the line asked for 0.45 to 0.55.' % (lo2, hi2))

# ---------- A3: octave by octave ----------
print('A3. The same exponent doubling by doubling above %d (steps; in brackets, bands; then 95%% of resamplings of the windows where there are six or more):' % H2)
edges = [H2]
while edges[-1] * 2 <= TALL: edges.append(edges[-1] * 2)
last = {}
for lo, hi in zip(edges, edges[1:]):
    S = W if hi <= LOW else LONG; y, mu, v = pool(S, hi); e1 = expo(y, v - THICK, lo, hi, 'steps'); e2 = expo(y, v - THICK, lo, hi, 'bands')
    iv = boot(S, lambda SS: expo(*[pool(SS, hi)[i] for i in (0, 2)], lo, hi, 'steps')) if len(S) >= 6 else None
    each = [expo(np.arange(w['HM']) + 0.5, w['var'] - THICK, lo, hi, 'steps') for w in S]
    print('    %6d to %6d (%2d windows): %.3f (%.3f)%s   window by window: mean %.3f, standard deviation %.3f' % (lo, hi, len(S), e1, e2, '   [%s]' % fmt(iv) if iv else '', np.mean(each), np.std(each, ddof=1)))
    last[hi] = (e1, e2, len(S))
    if hi == LOW and LONG and len(SHORT) >= 2:
        y, mu, v = pool(SHORT, hi); print('         the same with the %d windows to %d alone: %.3f (%.3f)' % (len(SHORT), LOW, expo(y, v - THICK, lo, hi, 'steps'), expo(y, v - THICK, lo, hi, 'bands'))); last['short'] = (expo(y, v - THICK, lo, hi, 'steps'), expo(y, v - THICK, lo, hi, 'bands'))
lastvals = list(last[TALL][:2]) + list(last[LOW][:2]) + list(last.get('short', ()))
line(3, 'guessed', 0.65, True if max(lastvals) <= 0.58 else False if min(lastvals) > 0.58 else None,
     'the last doubling of the tall windows (%d to %d, %d windows) gives %.3f (%.3f); the last of the others (%d to %d) gives %.3f (%.3f) with all the windows%s; the line asked for no more than 0.58.' % (
         TALL // 2, TALL, last[TALL][2], last[TALL][0], last[TALL][1], LOW // 2, LOW, last[LOW][0], last[LOW][1], ' and %.3f (%.3f) with the %d alone' % (last['short'] + (len(SHORT),)) if 'short' in last else ''))

# ---------- A4: variance over the square root of the depth ----------
def ratio(S, T, frac):
    y, mu, v = pool(S, T); n = max(1, int(round(frac * T))); return float((v[T - n:] - THICK).mean() / math.sqrt(mu[T - n:].mean()))
print('A4. The variance of depth over the square root of the depth, at the top (the top hundredth of the height; in brackets the top band alone and the top twentieth):')
allA4 = []
for name, S, T in SETS[:3]:
    r = [ratio(S, T, 0.01), ratio(S, T, 1.0 / T), ratio(S, T, 0.05)]; allA4 += r
    each = [ratio([w], T, 0.01) for w in S]
    print('    %-30s %.3f (%.3f, %.3f)   window by window: %s' % (name + ':', r[0], r[1], r[2], ', '.join('%.2f' % e for e in each)))
print('    lower down, all windows that reach: ' + ', '.join('%.3f at %d' % (ratio(W if h <= LOW else LONG, h, 0.01), h) for h in [H4 // 4, H4 // 2] + edges[1:]))
line(4, 'guessed', 0.6, True if (min(allA4) >= 0.55 and max(allA4) <= 0.75) else False if (max(allA4) < 0.55 or min(allA4) > 0.75) else None,
     'at the top it is %.3f (the %d windows at %d), %.3f (all %d at %d) and %.3f (the %d at %d); with the other two ways of taking "the top" the nine values run from %.3f to %.3f; the line asked for 0.55 to 0.75.' % (
         allA4[0], len(SHORT), LOW, allA4[6], len(W), LOW, allA4[3], len(LONG), TALL, min(allA4), max(allA4)))

# ---------- A5: the constant ----------
def slope_of(w, lo, hi):
    y = np.arange(w['HM']) + 0.5; m = (y >= lo) & (y <= hi); c = w['c'][m]; yy = y[m]; d = w['mu'][m]
    n = c.sum(); my = (c * yy).sum() / n; md = (c * d).sum() / n; return float((c * (yy - my) * (d - md)).sum() / (c * (yy - my) ** 2).sum())
for w in W:
    w['slope'] = slope_of(w, w['HM'] / 2, w['HM']); assert abs(w['slope'] - w['o']['slope_upper_half']) < 3e-6, (w['slope'], w['o']['slope_upper_half'])
def ms(v): v = list(v); return float(np.mean(v)), (float(np.std(v, ddof=1) / math.sqrt(len(v))) if len(v) > 1 else float('nan'))
print('A5. The slope of mean depth against height over the upper half of each window (as cell2 reports it; recomputed here from the profile, the same to 3 in the sixth place):')
print('    the %d to %d: %s' % (len(SHORT), LOW, ', '.join('%.5f' % w['slope'] for w in SHORT)))
print('    the %d to %d: %s' % (len(LONG), TALL, ', '.join('%.5f' % w['slope'] for w in LONG)))
wts = [w['HM'] for w in W]
pools = [('the %d windows to %d' % (len(SHORT), LOW),) + ms(w['slope'] for w in SHORT), ('the %d windows to %d' % (len(LONG), TALL),) + ms(w['slope'] for w in LONG),
         ('all %d, each counted once' % len(W),) + ms(w['slope'] for w in W),
         ('all %d, each weighted by its height' % len(W), float(np.average([w['slope'] for w in W], weights=wts)), float('nan')),
         ('all %d over the same heights, %d to %d' % (len(W), LOW // 2, LOW),) + ms(slope_of(w, LOW / 2, LOW) for w in W)]
mid = (1.32585 + 1.32600) / 2; pools.sort(key=lambda p: -abs(p[1] - mid))
print('    pooled, the unkindest to the line first (mean, and standard error from the spread of the windows):')
for name, m, s in pools: print('      %-44s %.6f (%.6f)%s' % (name + ':', m, s, '' if 1.32585 <= m <= 1.32600 else '   outside'))
inside = [1.32585 <= m <= 1.32600 for name, m, s in pools]
line(5, 'guessed', 0.7, True if all(inside) else False if not any(inside) else None,
     'of the five ways of pooling the windows, %d give a slope between 1.32585 and 1.32600; they run from %.6f to %.6f.' % (sum(inside), min(p[1] for p in pools), max(p[1] for p in pools)))

# ---------- A6: the mean has no slowly growing correction ----------
def offset(S, T, alpha, h, half=50):
    y, mu, v = pool(S, T); a, b = int(h) - half, int(h) + half
    if b > T: a, b = T - 2 * half, T
    return float((mu[a:b] - alpha * y[a:b]).mean())
half = max(2, 50 // SC)
print('A6. Mean depth less the constant times the height (the constant of A5 for the same windows), a mean over %d bands at each height:' % (2 * half))
ch = []
for name, S, T in SETS[:3]:
    alpha = ms(w['slope'] for w in S)[0]; hs = [h for h in [H4] + [e for e in edges if e > H4] if h <= T]
    offs = [offset(S, T, alpha, h, half) for h in hs]; ch.append(offs[-1] - offs[0])
    print('    %-30s constant %.6f: %s; change from %d to the top %+.2f layers' % (name + ':', alpha, ', '.join('%.2f at %d' % (o, h) for o, h in zip(offs, hs)), H4, ch[-1]))
    each = [offset([w], T, w['slope'], T, half) - offset([w], T, w['slope'], H4, half) for w in S]
    print('         window by window, each with its own slope: %s' % ', '.join('%+.1f' % e for e in each))
line(6, 'worked', 0.6, True if all(abs(c) < 2 for c in ch) else False if all(abs(c) >= 2 for c in ch) else None,
     'the change between %d and the top is %+.2f layers (the %d windows to %d), %+.2f (the %d to %d) and %+.2f (all %d, to %d); the line asked for less than 2 either way.' % (
         H4, ch[0], len(SHORT), LOW, ch[1], len(LONG), TALL, ch[2], len(W), LOW))

# ---------- A7: the wander of a window's mean depth accounts for the variance ----------
STEP, FIRST, NEAR = 4000 // SC, 8000 // SC, max(4, 100 // SC); PERIOD = W[0]['o']['W']
def offsets_at(w, step=STEP, first=FIRST, near=NEAR):
    y = np.arange(w['HM']) + 0.5; out = []
    for h in range(first, w['HM'] + 1, step):
        sl = slice(h - near, h); c = w['c'][sl]; out.append(float((c * (w['mu'][sl] - 1.3259 * y[sl])).sum() / c.sum()))
    return out
def wander(S, step=STEP, first=FIRST):
    ch = np.concatenate([np.diff(offsets_at(w, step, first)) for w in S]); return float(PERIOD * ch.var(ddof=1) / step), len(ch)
D, nch = wander(W); top4 = ratio(W, LOW, 0.01); K600 = math.sqrt(3 / (2 * math.pi * 1.3259)); R7 = K600 * D / top4
print('A7. The wander of a window\'s mean depth: at heights %d, %d, ... the mean depth over the %d bands just below, less 1.3259 times their mean height; the changes from each to the next.' % (FIRST, FIRST + STEP, NEAR))
print('    all %d windows: %d changes; D = period x variance of the changes / %d = %.3f; %.3f D = %.3f; variance of depth over root depth at %d (all windows): %.3f; ratio %.3f' % (len(W), nch, STEP, D, K600, K600 * D, LOW, top4, R7))
iv = boot(W, lambda SS: K600 * wander(SS)[0] / ratio(SS, LOW, 0.01)); print('    95%% of resamplings of the windows: %s' % fmt(iv))
for nm, S in (('the first batch (seeding 1)', [w for w in W if w['seeding'] == 1]), ('the second batch (seeding 2)', [w for w in W if w['seeding'] == 2]), ('the windows to %d' % LOW, SHORT), ('the windows to %d' % TALL, LONG)):
    if len(S) >= 2: d, n = wander(S); print('    %-30s %3d changes, D = %.3f, ratio %.3f' % (nm + ':', n, d, K600 * d / ratio(S, min(w['HM'] for w in S) if nm.startswith('the windows') else LOW, 0.01)))
print('    with other steps (all windows): ' + ', '.join('%d: D = %.3f' % (st, wander(W, st)[0]) for st in (STEP // 4, STEP // 2, STEP, STEP * 2)))
line(7, 'worked', 0.55, 0.8 <= R7 <= 1.4, '%.3f D is %.3f and the variance of depth over the square root of depth at %d is %.3f: a ratio of %.3f, where the line asked for 0.8 to 1.4.' % (K600, K600 * D, LOW, top4, R7))

# ---------- A8 and A9: the slabs of the second batch ----------
SNAP = [w for w in W if 'slab' in w]; HSN = 16000 // SC
if SNAP:
    hs = SNAP[0]['snapH']; assert all(w['snapH'] == hs for w in SNAP); wcol = SNAP[0]['o']['wcol']; LAGS = SNAP[0]['lags']; assert all(w['lags'] == LAGS for w in SNAP)
    sk = {}; ku = {}; va = {}
    for k, h in enumerate(hs):
        va[h] = float(np.mean([w['slab'][k]['v'] for w in SNAP])); sk[h] = [w['slab'][k]['sk'] for w in SNAP]; ku[h] = [w['slab'][k]['ku'] for w in SNAP]
    high = [h for h in hs if h >= HSN]; allsk = [x for h in high for x in sk[h]]; allku = [x for h in high for x in ku[h]]
    msk = float(np.mean(allsk)); perwin = [float(np.mean([sk[h][i] for h in high])) for i in range(len(SNAP))]
    print('A8. The skewness of the column means of depth, slab by slab (%d windows with slabs; a slab is 4 thick; mean over the windows, and the excess of kurtosis):' % len(SNAP))
    for h in hs:
        if h >= HSN // 16 and hs.index(h) % 4 == 0: print('    height %6d: skewness %+.3f, excess of kurtosis %+.3f, variance of the column means %.1f' % (h, np.mean(sk[h]), np.mean(ku[h]), va[h]))
    print('    over the %d slabs at %d or above: mean skewness %+.4f (the %d windows one by one: %s; standard error from them %.4f); mean excess of kurtosis %+.4f' % (
        len(high), HSN, msk, len(SNAP), ', '.join('%+.3f' % x for x in perwin), np.std(perwin, ddof=1) / math.sqrt(len(perwin)), np.mean(allku)))
    line(8, 'guessed', 0.65, -0.08 <= msk <= 0.08, 'the mean of the %d skewnesses (%d windows, %d slabs at %d or above) is %+.4f; the line asked for between -0.08 and 0.08.' % (len(allsk), len(SNAP), len(high), HSN, msk))
    def gcurve(k, S=None):
        """the mean square difference of the column means of slab k between columns j apart (the window is a ring), the windows S together; and twice their variance"""
        g = np.zeros(len(LAGS)); n = np.zeros(len(LAGS)); v = []
        for w in (S or SNAP):
            st = w['slab'][k]; v.append(st['v']); g += np.array(st['g']); n += np.array(st['n'])
        return g / n, 2 * float(np.mean(v))
    def reach(k, S=None):
        g, plateau = gcurve(k, S); i = int(np.argmax(g >= plateau / 2))
        if g[i] < plateau / 2 or i == 0: return float('nan')
        x0, x1 = math.log(LAGS[i - 1] * wcol), math.log(LAGS[i] * wcol); return math.exp(x0 + (x1 - x0) * (plateau / 2 - g[i - 1]) / (g[i] - g[i - 1]))
    print('A9. The reach: the distance at which the mean square difference of depth between two columns is half of twice the variance of the column means; over 0.5715 x root height (the middle of the slab):')
    rr = {}
    for k, h in enumerate(hs):
        if h >= HSN // 16: rr[h] = reach(k) / (0.5715 * math.sqrt(h + 2))
    print('    ' + '; '.join('%d: %.0f (%.3f)' % (h, rr[h] * 0.5715 * math.sqrt(h + 2), rr[h]) for h in hs if h in rr and hs.index(h) % 4 == 0))
    mr = float(np.mean([rr[h] for h in high])); each = [float(np.mean([reach(hs.index(h), [w]) / (0.5715 * math.sqrt(h + 2)) for h in high])) for w in SNAP]
    print('    over the %d slabs at %d or above: the ratios run from %.3f to %.3f, mean %.3f; window by window the mean ratio is %s' % (len(high), HSN, min(rr[h] for h in high), max(rr[h] for h in high), mr, ', '.join('%.2f' % e for e in each)))
    line(9, 'worked', 0.5, 0.8 <= mr <= 1.2, 'the mean over the %d slabs at %d or above of the reach divided by 0.5715 times the square root of the height is %.3f; the line asked for 0.8 to 1.2.' % (len(high), HSN, mr))
else:
    print('A8, A9: no window with slabs.')

full = [v for v in verdicts]; held = sum(1 for v in full if v[3] is True); halfn = sum(1 for v in full if v[3] is None)
brier = sum((v[2] - (1 if v[3] is True else 0.5 if v[3] is None else 0)) ** 2 for v in full) / len(full)
print('HELD %d of %d, HALF %d, FAILED %d. Brier score %.3f (a half counted as a half).' % (held, len(full), halfn, len(full) - held - halfn, brier))
for k in ('worked', 'guessed'):
    v = [x for x in full if x[1] == k]
    print('  %s: %d of %d held (lines %s; * failed, ~ half)' % (k, sum(1 for x in v if x[3] is True), len(v), ', '.join('A' + str(x[0]) + ('' if x[3] is True else '~' if x[3] is None else '*') for x in v)))
