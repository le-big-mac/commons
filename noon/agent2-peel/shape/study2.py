"""study2.py: the second sheet (expectations-2.md) against its runs and its search.   python -I study2.py     (SHAPE_AFTER=DIR, FLOOR=FILE for others)
A. For each of the four sets of quarter discs: r = (variance of the count x n / mean^2) / the quarter disc's own line by theory.py,
   with its error by resampling whole clouds (4,000 times, the random numbers started from the set's name). Sets are put together
   weighted by their errors. A line holds if its figure is inside its band, ends included; a set short of its clouds by more than
   1 in 1,000 makes its lines "not run".
B. From floor.json, the record of floor.py's search. Writes study2.json."""
import json, math, os, sys, zlib
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import theory, fresh
FLOOR = os.environ.get('FLOOR', os.path.join(HERE, 'floor.json'))
SETS = {'cloud.c, 100,000': ('q2-cloud-quarter-100000', 100000), 'numpy, 100,000': ('q2-numpy-quarter-100000', 100000), 'cloud.c, 30,000': ('q2-cloud-quarter-30000', 30000), 'numpy, 30,000': ('q2-numpy-quarter-30000', 30000)}; ASKED = 120000
def line_of(n): p = theory.predictions('quarter', n); return p['exact'] / p['mean'] ** 2 * n, p
R = {}
for key, (name, n) in SETS.items():
    x = fresh.counts(name)
    if x is None or len(x) < 0.999 * ASKED: R[key] = None; continue
    K = len(x); m = float(x.mean()); v = float(x.var(ddof=1)); ln, p = line_of(n); rng = np.random.default_rng([20261125, zlib.crc32(name.encode())]); vals, cnt = np.unique(x, return_counts=True)
    H = rng.multinomial(K, cnt / K, size=4000); mb = H @ vals / K; vb = (H @ vals ** 2 - K * mb ** 2) / (K - 1)
    R[key] = {'K': K, 'm': m, 'mse': float(mb.std(ddof=1)), 'v': v, 'vse': float(vb.std(ddof=1)), 'r': v * n / m ** 2 / ln, 'rse': float((vb * n / mb ** 2 / ln).std(ddof=1)), 'theory_m': p['mean'], 'theory_v': p['exact'], 'line': ln}
def together(keys):
    if any(R[k] is None for k in keys): return None
    m, s, chi = fresh.pool([(R[k]['r'], R[k]['rse']) for k in keys]); return m, s
def diff(a, b):
    if a is None or b is None: return None
    return a[0] - b[0], math.hypot(a[1], b[1])
ALL = list(SETS); out = {'sets': {k: (None if v is None else v) for k, v in R.items()}, 'lines': {}}
LINES = [('A1', 'r of all four sets together', 0.65, together(ALL), 0.996, 1.008),
         ('A2', 'r of the two cloud.c sets less r of the two numpy sets', 0.90, diff(together(['cloud.c, 100,000', 'cloud.c, 30,000']), together(['numpy, 100,000', 'numpy, 30,000'])), -0.010, 0.010),
         ('A3', 'r of the two sets at 100,000 less r of the two at 30,000', 0.85, diff(together(['cloud.c, 100,000', 'numpy, 100,000']), together(['cloud.c, 30,000', 'numpy, 30,000'])), -0.010, 0.010),
         ('A4', 'r of the new cloud.c set at 100,000 alone', 0.70, together(['cloud.c, 100,000']), 0.992, 1.012)]
if __name__ == '__main__':
    print('A. The quarter disc. Its own line: variance x n / mean^2 = %.5f' % line_of(1e5)[0])
    print('   set                 clouds    mean count (se)       theory     variance (se)        theory    r (se)')
    for k, v in R.items():
        if v is None: print('   %-18s  not there, or short' % k)
        else: print('   %-18s  %6d    %8.3f (%.3f)      %8.2f   %.4f (%.4f)      %.4f    %.4f (%.4f)' % (k, v['K'], v['m'], v['mse'], v['theory_m'], v['v'], v['vse'], v['theory_v'], v['r'], v['rse']))
    held = failed = notrun = 0; brier = 0.0
    def judge(tag, what, odds, ok, detail):
        global held, failed, notrun, brier
        if ok is None: notrun += 1; print('%-3s not run          %s' % (tag, what)); out['lines'][tag] = {'verdict': 'not run'}; return
        held += ok; failed += (not ok); brier += (odds - (1.0 if ok else 0.0)) ** 2; print('%-3s %-7s (odds %.2f)  %s: %s' % (tag, 'HELD' if ok else 'FAILED', odds, what, detail)); out['lines'][tag] = dict({'verdict': 'held' if ok else 'failed', 'odds': odds, 'detail': detail})
    for tag, what, odds, val, lo, hi in LINES:
        if val is None: judge(tag, what, odds, None, ''); continue
        judge(tag, what, odds, bool(lo <= val[0] <= hi), '%+.4f (%.4f); band %+.3f to %+.3f; %.1f errors from the nearer end' % (val[0], val[1], lo, hi, min(val[0] - lo, hi - val[0]) / val[1]) if lo < 0 else '%.4f (%.4f); band %.3f to %.3f; %.1f errors from the nearer end' % (val[0], val[1], lo, hi, min(val[0] - lo, hi - val[0]) / val[1])); out['lines'][tag]['value'] = val[0]; out['lines'][tag]['se'] = val[1]
    print(); print('B. The floor (%s)' % os.path.basename(FLOOR))
    if not os.path.exists(FLOOR): fl = None
    else: fl = json.load(open(FLOOR))['runs']
    done = fl is not None and len(fl) == 8 and sum(1 for r in fl if 'fine_Q' in r) == 5
    if not done:
        for tag, what, odds in (('B1', 'the least found is not below 1.3040', 0.55), ('B2', 'it is a triangle with round corners', 0.75), ('B3', 'its rho is between 0.15 and 0.35', 0.70), ('B4', 'two of the five random starts end within 0.002 of the least', 0.50)): judge(tag, what, odds, None, '')
    else:
        import floor
        best = min((r for r in fl if 'fine_Q' in r), key=lambda r: r['fine_Q']); d = floor.describe(np.array(best['x'])); per = sum(L for a, L in d['sides']); big = [(a, L / per) for a, L in d['sides'] if L / per > 0.03]; low240 = min(r['best_Q'] for r in fl); near = [r['seed'] for r in fl if r['seed'] >= 4 and r['best_Q'] <= low240 + 0.002]
        judge('B1', 'the least found, as run again at 1,440 angles, is not below 1.3040', 0.55, bool(best['fine_Q'] >= 1.3040), '%.5f (start %d)' % (best['fine_Q'], best['seed']))
        judge('B2', 'the shape that has it is a triangle with round corners: exactly three sides each over 3 in 100 of its flat edge', 0.75, len(big) == 3, '%d such sides (%s)' % (len(big), ', '.join('%d degrees %.3f' % b for b in big)))
        judge('B3', 'if B2 holds, its rho is between 0.15 and 0.35', 0.70, (bool(0.15 <= d['rho'] <= 0.35) if len(big) == 3 else None), 'rho %.4f' % d['rho'])
        judge('B4', 'at least two of the five starts from random polygons end within 0.002 of the least (at 240 angles)', 0.50, len(near) >= 2, 'starts %s; the least at 240 angles %.5f' % (near or 'none', low240))
        out['floor'] = {'least': best['fine_Q'], 'seed': best['seed'], 'rho': d['rho'], 'sides': big, 'least240': low240}
    n = held + failed; print(); print('%d held, %d failed, %d not run.%s' % (held, failed, notrun, (' Brier score of the odds %.3f.' % (brier / n)) if n else ''))
    out['held'] = int(held); out['failed'] = int(failed); out['notrun'] = int(notrun); out['brier'] = brier / n if n else None
    json.dump(out, open(os.path.join(HERE, 'study2.json' if 'SHAPE_AFTER' not in os.environ and 'FLOOR' not in os.environ else 'study2-other.json'), 'w'), indent=1, default=float)
