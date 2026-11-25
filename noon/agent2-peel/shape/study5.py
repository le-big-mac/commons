"""study5.py: the fifth sheet (expectations-5.md): does the variance of a small disc's count swing as its mean passes whole numbers,
and is what is missing from the variance the same for a triangle, with sharp corners and with round ones?
python -I study5.py     (SHAPE_AFTER=DIR for another folder of runs)
Discs of 83, 90, 98, 105, 113 and 120 points by the first study's own generator (own.py), 200,000 of each: B = variance - 0.08227 n^(1/3).
Triangles, rounded triangles and one set of discs through cloud.c (smake.py), 400,000 at 300 and at 1,000 points, 200,000 at 3,000:
B = variance - 1.0197 x the theory's variance for that shape and size. Errors by resampling whole clouds (4,000 times, started from the
file's name). A line holds if its figure is inside its band, ends included; a file short by more than 1 in 1,000 makes the lines that
need it "not run". Writes study5.json."""
import json, math, os, sys, zlib
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import theory, fresh
LAT = (83, 90, 98, 105, 113, 120); C5 = 0.08227; RATIO = 1.0197; OWN = {300: -0.0401, 1000: -0.0450, 3000: -0.0471}      # the disc's B by the first study's generator, from the fourth sheet (300, 1,000) and the third (3,000)
PRED = {83: -0.0467, 90: -0.0294, 98: -0.0450, 105: -0.0320, 113: -0.0435, 120: -0.0346}                               # ruler5.py: B if the count swings
FILES = dict([('disc-%d' % n, 200000) for n in LAT] + [('cdisc-1000', 400000), ('triangle-300', 400000), ('triangle-1000', 400000), ('triangle-3000', 200000), ('rtriangle-300', 400000), ('rtriangle-1000', 400000), ('rtriangle-3000', 200000)])
LINES = [('Q1', 0.85, 'Z, the mean of B at 90, 105 and 120 points less its mean at 83, 98 and 113, is +0.008 or more'), ('Q2', 0.55, 'B at each of the six sizes is within 0.004 of what the swinging count gives'),
         ('Q3', 0.90, 'the control: B of discs through cloud.c at 1,000 points is within 0.006 of the first generator\'s -0.0450'), ('Q4', 0.45, 'the triangle\'s B at 1,000 points is below the control disc\'s by 0.020 or more'),
         ('Q5', 0.20, 'the triangle\'s B at 1,000 points is within 0.006 of the control disc\'s'), ('Q6', 0.45, 'at 1,000 points the triangle\'s B is below the rounded triangle\'s by 0.012 or more'),
         ('Q7', 0.40, 'the rounded triangle\'s B at 1,000 points is within 0.008 of the control disc\'s'), ('Q8', 0.40, 'the triangle\'s B at 300 points is below -0.0551 (the disc\'s -0.0401 less 0.015)'), ('Q9', 0.40, 'the triangle\'s B at 3,000 points is below -0.0621 (the disc\'s -0.0471 less 0.015)')]
def verdicts(Bl, Bc, Bt, Br):
    """the nine lines by the letter. Bl[n]: the discs' B at the six small sizes; Bc: the control disc's B at 1,000; Bt[n], Br[n]: the triangle's and the rounded triangle's B. A missing figure (None) makes its lines None."""
    ok = lambda *xs: all(x is not None for x in xs); out = {}; has = lambda d, ks: d is not None and all(d.get(k) is not None for k in ks)
    out['Q1'] = bool((Bl[90] + Bl[105] + Bl[120]) / 3 - (Bl[83] + Bl[98] + Bl[113]) / 3 >= 0.008) if has(Bl, LAT) else None
    out['Q2'] = bool(all(abs(Bl[n] - PRED[n]) <= 0.004 for n in LAT)) if has(Bl, LAT) else None
    out['Q3'] = bool(abs(Bc - OWN[1000]) <= 0.006) if ok(Bc) else None
    out['Q4'] = bool(Bt[1000] - Bc <= -0.020) if ok(Bc) and has(Bt, [1000]) else None
    out['Q5'] = bool(abs(Bt[1000] - Bc) <= 0.006) if ok(Bc) and has(Bt, [1000]) else None
    out['Q6'] = bool(Bt[1000] - Br[1000] <= -0.012) if has(Bt, [1000]) and has(Br, [1000]) else None
    out['Q7'] = bool(abs(Br[1000] - Bc) <= 0.008) if ok(Bc) and has(Br, [1000]) else None
    out['Q8'] = bool(Bt[300] <= OWN[300] - 0.015) if has(Bt, [300]) else None
    out['Q9'] = bool(Bt[3000] <= OWN[3000] - 0.015) if has(Bt, [3000]) else None
    return out
R = {}
for key, K0 in FILES.items():
    name = 'n5-' + key; x = fresh.counts(name); sh, n = key.split('-'); n = int(n); shape = 'disc' if sh in ('disc', 'cdisc') else sh
    if x is None or len(x) < 0.999 * K0: R[key] = None; continue
    K = len(x); m = float(x.mean()); v = float(x.var(ddof=1)); rng = np.random.default_rng([20261125, zlib.crc32(name.encode())]); vals, cnt = np.unique(x, return_counts=True)
    H = rng.multinomial(K, cnt / K, size=4000); mb = H @ vals / K; vb = (H @ vals ** 2 - K * mb ** 2) / (K - 1); p = theory.predictions(shape, n)
    R[key] = {'K': K, 'n': n, 'shape': sh, 'm': m, 'mse': float(mb.std(ddof=1)), 'v': v, 'vse': float(vb.std(ddof=1)), 'theory_v': p['exact'], 'theory_m': p['mean'], 'B': (v - C5 * n ** (1 / 3.0)) if sh == 'disc' else (v - RATIO * p['exact'])}
if __name__ == '__main__':
    out = {'sets': R, 'lines': {}}
    print('B: for the small discs, variance - %.5f n^(1/3); for the shapes through cloud.c, variance - %.4f x the theory\'s' % (C5, RATIO))
    print('   set               clouds    mean count (se)       the theory\'s mean   variance (se)        the theory\'s   B (se)')
    for key, v in R.items():
        if v is None: print('   %-15s   not there, or short' % key)
        else: print('   %-15s   %6d    %8.4f (%.4f)     %8.4f            %.4f (%.4f)      %.4f         %+.4f (%.4f)%s' % (key, v['K'], v['m'], v['mse'], v['theory_m'], v['v'], v['vse'], v['theory_v'], v['B'], v['vse'], ('   swinging: %+.4f' % PRED[v['n']]) if v['shape'] == 'disc' else ''))
    g = lambda key: None if R.get(key) is None else R[key]['B']; e = lambda key: R[key]['vse']
    Bl = {n: g('disc-%d' % n) for n in LAT}; Bc = g('cdisc-1000'); Bt = {n: g('triangle-%d' % n) for n in (300, 1000, 3000)}; Br = {n: g('rtriangle-%d' % n) for n in (300, 1000, 3000)}; V = verdicts(Bl, Bc, Bt, Br); detail = {}
    if V['Q1'] is not None: detail['Q1'] = '%+.4f (%.4f)' % ((Bl[90] + Bl[105] + Bl[120]) / 3 - (Bl[83] + Bl[98] + Bl[113]) / 3, math.sqrt(sum(e('disc-%d' % n) ** 2 for n in LAT)) / 3); detail['Q2'] = ', '.join('%+.4f' % (Bl[n] - PRED[n]) for n in LAT)
    if V['Q3'] is not None: detail['Q3'] = '%+.4f (%.4f)' % (Bc, e('cdisc-1000'))
    if V['Q4'] is not None: detail['Q4'] = detail['Q5'] = '%+.4f (%.4f)' % (Bt[1000] - Bc, math.hypot(e('triangle-1000'), e('cdisc-1000')))
    if V['Q6'] is not None: detail['Q6'] = '%+.4f (%.4f)' % (Bt[1000] - Br[1000], math.hypot(e('triangle-1000'), e('rtriangle-1000')))
    if V['Q7'] is not None: detail['Q7'] = '%+.4f (%.4f)' % (Br[1000] - Bc, math.hypot(e('rtriangle-1000'), e('cdisc-1000')))
    if V['Q8'] is not None: detail['Q8'] = '%+.4f (%.4f)' % (Bt[300], e('triangle-300'))
    if V['Q9'] is not None: detail['Q9'] = '%+.4f (%.4f)' % (Bt[3000], e('triangle-3000'))
    held = failed = notrun = 0; brier = 0.0
    for tag, odds, what in LINES:
        ok_ = V[tag]
        if ok_ is None: notrun += 1; print('%-3s not run          %s' % (tag, what)); out['lines'][tag] = {'verdict': 'not run'}; continue
        held += ok_; failed += (not ok_); brier += (odds - (1.0 if ok_ else 0.0)) ** 2; print('%-3s %-7s (odds %.2f)  %s: %s' % (tag, 'HELD' if ok_ else 'FAILED', odds, what, detail[tag])); out['lines'][tag] = {'verdict': 'held' if ok_ else 'failed', 'odds': odds, 'detail': detail[tag]}
    n_ = held + failed; print(); print('%d held, %d failed, %d not run.%s' % (held, failed, notrun, (' Brier score of the odds %.3f.' % (brier / n_)) if n_ else ''))
    out['held'] = int(held); out['failed'] = int(failed); out['notrun'] = int(notrun); out['brier'] = brier / n_ if n_ else None
    json.dump(out, open(os.path.join(HERE, 'study5.json' if 'SHAPE_AFTER' not in os.environ else 'study5-other.json'), 'w'), indent=1, default=float)
