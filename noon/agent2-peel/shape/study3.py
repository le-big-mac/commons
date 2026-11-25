"""study3.py: the third sheet (expectations-3.md): does the spread of a disc's count lean with the number of points?
python -I study3.py     (SHAPE_AFTER=DIR for another folder of runs)
Discs of exactly n points made by the first study's own generator (own.py), five sizes. For each: r = (variance of the count x n /
mean^2) / 0.37544, the disc's line, with its error by resampling whole clouds (4,000 times, the random numbers started from the
file's name). The lean: a straight line r = a + s n^(-1/3) fitted by weighted least squares to the four sizes from 10,000 to 300,000;
s is its slope and a what it gives for very many points. A line of the sheet holds if its figure is inside its band, ends included;
a size short of its clouds by more than 1 in 1,000 makes the lines that need it "not run". Writes study3.json."""
import json, math, os, sys, zlib
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import theory, fresh
ASKED = {3000: 400000, 10000: 400000, 30000: 400000, 100000: 300000, 300000: 150000}; FIT = (10000, 30000, 100000, 300000)
LINE = (4 / 3.0 * theory.D - theory.DC) / theory.ALPHA ** 2
R = {}
for n, K0 in ASKED.items():
    name = 'n3-disc-%d' % n; x = fresh.counts(name)
    if x is None or len(x) < 0.999 * K0: R[n] = None; continue
    K = len(x); m = float(x.mean()); v = float(x.var(ddof=1)); rng = np.random.default_rng([20261125, zlib.crc32(name.encode())]); vals, cnt = np.unique(x, return_counts=True)
    H = rng.multinomial(K, cnt / K, size=4000); mb = H @ vals / K; vb = (H @ vals ** 2 - K * mb ** 2) / (K - 1); tm = theory.predictions('disc', n)['mean']
    R[n] = {'K': K, 'm': m, 'mse': float(mb.std(ddof=1)), 'v': v, 'vse': float(vb.std(ddof=1)), 'r': v * n / m ** 2 / LINE, 'rse': float((vb * n / mb ** 2 / LINE).std(ddof=1)), 'theory_m': tm, 'excess': m - tm, 'theory_v': theory.predictions('disc', n)['exact']}
def fit(sizes):
    """weighted least squares of r on n^(-1/3): (slope, its error, intercept, its error, chi-square about the line)"""
    if any(R[n] is None for n in sizes): return None
    x = np.array([n ** (-1 / 3.0) for n in sizes]); y = np.array([R[n]['r'] for n in sizes]); w = np.array([1 / R[n]['rse'] ** 2 for n in sizes])
    S, Sx, Sy, Sxx, Sxy = w.sum(), (w * x).sum(), (w * y).sum(), (w * x * x).sum(), (w * x * y).sum(); d = S * Sxx - Sx ** 2
    s = (S * Sxy - Sx * Sy) / d; a = (Sxx * Sy - Sx * Sxy) / d; return float(s), float(math.sqrt(S / d)), float(a), float(math.sqrt(Sxx / d)), float((w * (y - a - s * x) ** 2).sum())
F4 = fit(FIT)
if __name__ == '__main__':
    out = {'sizes': {str(n): v for n, v in R.items()}, 'lines': {}}
    print('Discs of exactly n points, the first study\'s own generator. The disc\'s line: variance x n / mean^2 = %.5f' % LINE)
    print('   points    clouds    mean count (se)        alpha rho^(2/3) T   excess, layers   variance (se)        theory     r (se)')
    for n, v in R.items():
        if v is None: print('   %7d   not there, or short' % n)
        else: print('   %7d   %6d    %9.3f (%.3f)      %9.3f           %+.3f           %.4f (%.4f)      %.4f     %.4f (%.4f)' % (n, v['K'], v['m'], v['mse'], v['theory_m'], v['excess'], v['v'], v['vse'], v['theory_v'], v['r'], v['rse']))
    if F4: print('   the line through the four sizes from 10,000 to 300,000:  r = %.4f (%.4f) %+.3f (%.3f) n^(-1/3);  chi-square about it %.1f on 2' % (F4[2], F4[3], F4[0], F4[1], F4[4])); out['fit'] = {'slope': F4[0], 'slope_se': F4[1], 'intercept': F4[2], 'intercept_se': F4[3], 'chi2': F4[4]}
    held = failed = notrun = 0; brier = 0.0
    def judge(tag, what, odds, ok, detail):
        global held, failed, notrun, brier
        if ok is None: notrun += 1; print('%-3s not run          %s' % (tag, what)); out['lines'][tag] = {'verdict': 'not run'}; return
        held += ok; failed += (not ok); brier += (odds - (1.0 if ok else 0.0)) ** 2; print('%-3s %-7s (odds %.2f)  %s: %s' % (tag, 'HELD' if ok else 'FAILED', odds, what, detail)); out['lines'][tag] = {'verdict': 'held' if ok else 'failed', 'odds': odds, 'detail': detail}
    rr = lambda n: None if R[n] is None else (R[n]['r'], R[n]['rse'])
    judge('L1', 'the slope of r on n^(-1/3), 10,000 to 300,000, is below -0.32', 0.60, None if F4 is None else bool(F4[0] <= -0.32), '' if F4 is None else '%+.3f (%.3f)' % F4[:2])
    judge('L2', 'r at 10,000 points is below 0.994', 0.55, None if rr(10000) is None else bool(rr(10000)[0] <= 0.994), '' if rr(10000) is None else '%.4f (%.4f)' % rr(10000))
    judge('L3', 'r at 100,000 points is between 0.994 and 1.010', 0.75, None if rr(100000) is None else bool(0.994 <= rr(100000)[0] <= 1.010), '' if rr(100000) is None else '%.4f (%.4f)' % rr(100000))
    judge('L4', 'r at 300,000 points is above 1.004', 0.50, None if rr(300000) is None else bool(rr(300000)[0] >= 1.004), '' if rr(300000) is None else '%.4f (%.4f)' % rr(300000))
    judge('L5', 'r at 3,000 points is below 0.985', 0.50, None if rr(3000) is None else bool(rr(3000)[0] <= 0.985), '' if rr(3000) is None else '%.4f (%.4f)' % rr(3000))
    ex = [None if R[n] is None else R[n]['excess'] for n in ASKED]
    judge('L6', 'the mean count exceeds alpha rho^(2/3) T by between 0.03 and 0.17 of a layer at every one of the five sizes', 0.75, None if any(e is None for e in ex) else bool(all(0.03 <= e <= 0.17 for e in ex)), '' if any(e is None for e in ex) else ', '.join('%+.3f' % e for e in ex))
    judge('L7', 'the line\'s value for very many points is between 1.008 and 1.028', 0.50, None if F4 is None else bool(1.008 <= F4[2] <= 1.028), '' if F4 is None else '%.4f (%.4f)' % F4[2:4])
    n_ = held + failed; print(); print('%d held, %d failed, %d not run.%s' % (held, failed, notrun, (' Brier score of the odds %.3f.' % (brier / n_)) if n_ else ''))
    out['held'] = int(held); out['failed'] = int(failed); out['notrun'] = int(notrun); out['brier'] = brier / n_ if n_ else None
    json.dump(out, open(os.path.join(HERE, 'study3.json' if 'SHAPE_AFTER' not in os.environ else 'study3-other.json'), 'w'), indent=1, default=float)
