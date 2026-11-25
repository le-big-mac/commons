"""study.py: the sealed lines of expectations.md against the runs.   python -I study.py            (SHAPE_RUNS=DIR for another folder of runs)
For a file: K clouds, m the mean of the counts of layers, v their variance (divisor K - 1), w = v / m^2. A line holds if its
figure is inside its band, ends included. The standard errors printed are by resampling whole clouds (4,000 times, each file on
its own, the random numbers started from the file's name so that every script that asks gets the same errors); the verdicts do
not use them. Writes study.json.
(The first scoring, verdicts-as-first-run.out, was made by study-as-first-run.py, which resampled 1,000 times from one stream of
random numbers, so that its errors depended on the order of asking; the figures and the verdicts are the same.)"""
import json, math, os, sys, zlib
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); RUNS = os.environ.get('SHAPE_RUNS', os.path.join(HERE, 'runs'))
sys.path.insert(0, HERE); import theory
ASKED = {'exact-triangle-100000': 50000, 'exact-rtriangle-100000': 50000, 'exact-disc-100000': 30000, 'exact-square-100000': 16000, 'exact-hexagon-100000': 16000, 'exact-ellipse-100000': 8000,
         'exact-halfdisc-100000': 8000, 'exact-quarter-100000': 8000, 'exact-disc0-100000': 20000, 'chance-disc-100000': 20000, 'chance-triangle-100000': 20000, 'chance-square-100000': 8000,
         'exact-triangle-30000': 50000, 'exact-rtriangle-30000': 50000, 'exact-disc-30000': 30000}
def load(name):
    p = os.path.join(RUNS, name + '.jsonl')
    if not os.path.exists(p) and os.path.exists(p + '.gz'):
        import gzip; L = [json.loads(l) for l in gzip.open(p + '.gz', 'rt')]
    elif os.path.exists(p): L = [json.loads(l) for l in open(p)]
    else: return None
    kind, shape, n0 = name.split('-'); n0 = int(n0)
    assert all(o['kind'] == kind and o['shape'] == shape and o['n0'] == n0 for o in L), name
    assert kind == 'chance' or all(o['n'] == n0 for o in L), name
    assert len(set(o['seed'] for o in L)) == len(L), name
    x = np.array([o['layers'] for o in L], float); both = [o['same'] for o in L if o['same'] != -1]
    return {'name': name, 'x': x, 'K': len(x), 'asked': ASKED.get(name), 'm': x.mean(), 'v': x.var(ddof=1), 'both': len(both), 'agree': sum(1 for b in both if b == 1), 'n': np.array([o['n'] for o in L], float), 'n0': n0}
F = {name: load(name) for name in ASKED}
def complete(*names): return all(F[n] is not None and F[n]['K'] >= 0.999 * F[n]['asked'] for n in names)       # a file short of its clouds by more than 1 in 1,000 is "not run"
def boot(name, B=4000):
    """B resamplings of the file's clouds: (means, variances)"""
    f = F[name]
    if 'boot' not in f:
        rng = np.random.default_rng([20261125, zlib.crc32(name.encode())]); vals, cnt = np.unique(f['x'], return_counts=True); H = rng.multinomial(f['K'], cnt / f['K'], size=B); m = H @ vals / f['K']; f['boot'] = (m, (H @ vals ** 2 - f['K'] * m ** 2) / (f['K'] - 1))
    return f['boot']
def stat(fn, *names):
    """the figure fn(m1, v1, m2, v2, ...) and its standard error by resampling"""
    args = []; bargs = []
    for n in names: args += [F[n]['m'], F[n]['v']]; b = boot(n); bargs += [b[0], b[1]]
    return float(fn(*args)), float(np.std(fn(*bargs), ddof=1))
P = lambda sh, n=1e5: theory.predictions(sh, n)
D5 = 'exact-disc-100000'
LINES = []
def line(tag, what, odds, parts):
    """parts: list of (label, fn, names, theory, lo, hi); the line holds if every part is inside its band"""
    LINES.append((tag, what, odds, parts))
mr = lambda m1, v1, m2, v2: m1 / m2; vr = lambda m1, v1, m2, v2: v1 / v2; wr = lambda m1, v1, m2, v2: (v1 / m1 ** 2) / (v2 / m2 ** 2); v1_ = lambda m1, v1: v1
line('S1', 'mean count over the disc\'s, exactly n, 100,000: hexagon, half disc, quarter disc', 0.80, [(sh, mr, ('exact-%s-100000' % sh, D5), t, t - 0.0006, t + 0.0006) for sh, t in (('hexagon', 1.02016), ('halfdisc', 1.02843), ('quarter', 1.03834))])
line('S2', 'the same for triangle, square, rounded triangle, ellipse, disc0', 0.85, [(sh, mr, ('exact-%s-100000' % sh, D5), t, t - 0.0006, t + 0.0006) for sh, t in (('triangle', 1.09321), ('square', 1.04807), ('rtriangle', 1.07121), ('ellipse', 1.0), ('disc0', 1.0))])
line('S3', 'variance of the disc, exactly n, 100,000', 0.85, [('disc', v1_, (D5,), 3.745, 3.60, 3.90)])
line('S4', 'variance of the triangle over the disc\'s, exactly n, 100,000', 0.70, [('triangle', vr, ('exact-triangle-100000', D5), 1.1951, 1.155, 1.235)])
line('S5', 'variance of the square over the disc\'s', 0.75, [('square', vr, ('exact-square-100000', D5), 1.0984, 1.058, 1.138)])
line('S6', 'variance of the hexagon over the disc\'s', 0.85, [('hexagon', vr, ('exact-hexagon-100000', D5), 1.0407, 1.000, 1.082)])
line('S7', 'w of the rounded triangle over w of the triangle, exactly n, 100,000', 0.70, [('100,000', wr, ('exact-rtriangle-100000', 'exact-triangle-100000'), 0.9547, 0.935, 0.975)])
line('S8', 'the same at 30,000 points', 0.60, [('30,000', wr, ('exact-rtriangle-30000', 'exact-triangle-30000'), 0.9547, 0.935, 0.975)])
line('S9', 'the controls: variance of the ellipse, and of disc0, over the disc\'s', 0.85, [('ellipse', vr, ('exact-ellipse-100000', D5), 1.0, 0.95, 1.05), ('disc0', vr, ('exact-disc0-100000', D5), 1.0, 0.965, 1.035)])
line('S10', 'variance of the half disc and of the quarter disc over the disc\'s', 0.80, [('halfdisc', vr, ('exact-halfdisc-100000', D5), 1.0526, 1.003, 1.103), ('quarter', vr, ('exact-quarter-100000', D5), 1.0743, 1.024, 1.124)])
line('S11', 'variance of the triangle over the disc\'s, both left to chance, 100,000', 0.70, [('triangle', vr, ('chance-triangle-100000', 'chance-disc-100000'), 1.1951, 1.145, 1.245)])
line('S12', 'variance of the square over the disc\'s, both left to chance', 0.75, [('square', vr, ('chance-square-100000', 'chance-disc-100000'), 1.0985, 1.04, 1.16)])
line('S13', 'variance of the disc left to chance, 100,000', 0.80, [('disc', v1_, ('chance-disc-100000',), 8.179, 7.77, 8.59)])
line('S14', 'w n of the triangle, exactly n, 100,000', 0.75, [('triangle', lambda m, v: v / m ** 2 * 1e5, ('exact-triangle-100000',), 0.3754, 0.360, 0.390)])
line('S15', 'w n of the triangle, exactly n, 30,000', 0.60, [('triangle', lambda m, v: v / m ** 2 * 3e4, ('exact-triangle-30000',), 0.3754, 0.356, 0.394)])
line('S16', 'w of the rounded triangle below w of the triangle at both sizes', 0.88, [('100,000', wr, ('exact-rtriangle-100000', 'exact-triangle-100000'), 0.9547, -1e9, 1 - 1e-12), ('30,000', wr, ('exact-rtriangle-30000', 'exact-triangle-30000'), 0.9547, -1e9, 1 - 1e-12)])
if __name__ == '__main__':
    out = {'files': {}, 'lines': {}}
    print('The files (runs in %s)' % os.path.relpath(RUNS, HERE))
    print('file                       asked   kept    peeled both ways, agreed   mean count (se)      variance (se)       theory: mean, variance     w n = variance x n / mean^2 (se)')
    for name, f in F.items():
        if f is None: print('%-26s %6d   not there' % (name, ASKED[name])); continue
        kind, shape, n0 = name.split('-'); p = P('disc' if shape == 'disc0' else shape, f['n0']); bm, bv = boot(name); wn = f['v'] / f['m'] ** 2 * f['n0']
        print('%-26s %6d  %6d   %4d, %4d                 %8.3f (%.3f)     %.4f (%.4f)     %8.2f, %.4f           %.4f (%.4f)' % (name, f['asked'], f['K'], f['both'], f['agree'], f['m'], bm.std(ddof=1), f['v'], bv.std(ddof=1), p['mean'], p['chance' if kind == 'chance' else 'exact'], wn, (bv / bm ** 2 * f['n0']).std(ddof=1)))
        out['files'][name] = {'asked': f['asked'], 'kept': f['K'], 'both': f['both'], 'agree': f['agree'], 'mean': f['m'], 'mean_se': float(bm.std(ddof=1)), 'var': f['v'], 'var_se': float(bv.std(ddof=1)), 'wn': wn, 'theory_mean': p['mean'], 'theory_var': p['chance' if kind == 'chance' else 'exact']}
    print(); print('The lines'); held = failed = notrun = 0; brier = 0.0
    for tag, what, odds, parts in LINES:
        names = sorted(set(n for part in parts for n in part[2]))
        if not complete(*names): print('%-4s not run   %s' % (tag, what)); notrun += 1; out['lines'][tag] = {'verdict': 'not run'}; continue
        res = []; ok = True
        for label, fn, nm, th, lo, hi in parts:
            val, se = stat(fn, *nm); inside = lo <= val <= hi; ok = ok and inside
            res.append({'part': label, 'value': val, 'se': se, 'theory': th, 'lo': lo, 'hi': hi, 'inside': bool(inside)})
        held += ok; failed += (not ok); brier += (odds - (1.0 if ok else 0.0)) ** 2
        print('%-4s %-7s (odds %.2f)  %s' % (tag, 'HELD' if ok else 'FAILED', odds, what))
        for r in res: print('        %-10s %.5f (%.5f)   theory %.5f   band %s to %s   %s%s' % (r['part'], r['value'], r['se'], r['theory'], ('%.4f' % r['lo']) if r['lo'] > -1e8 else 'any', '%.4f' % r['hi'] if r['hi'] < 0.9999999 or r['hi'] > 1.0000001 else 'below 1', 'inside' if r['inside'] else 'OUTSIDE', '; %.1f errors from the theory' % ((r['value'] - r['theory']) / r['se']) if r['se'] > 0 else ''))
        out['lines'][tag] = {'verdict': 'held' if ok else 'failed', 'odds': odds, 'parts': res}
    n = held + failed
    print(); print('%d held, %d failed, %d not run.%s' % (held, failed, notrun, (' Brier score of the odds %.3f (always saying one half would score 0.250).' % (brier / n)) if n else ''))
    out['held'] = int(held); out['failed'] = int(failed); out['notrun'] = int(notrun); out['brier'] = brier / n if n else None
    json.dump(out, open(os.path.join(HERE, 'study.json' if RUNS == os.path.join(HERE, 'runs') else 'study-other.json'), 'w'), indent=1)
