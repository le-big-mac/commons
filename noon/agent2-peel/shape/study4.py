"""study4.py: the fourth sheet (expectations-4.md): does the constant taken from the variance of a disc's count hold in small clouds?
python -I study4.py     (SHAPE_AFTER=DIR for another folder of runs)
Discs of exactly 4, 100, 300 and 1,000 points made by the first study's own generator (own.py), 400,000 of each. For 100, 300 and
1,000: the variance V of the count, with its error by resampling whole clouds (4,000 times, the random numbers started from the
file's name); B = V - 0.08227 n^(1/3), where 0.08227 is the third sheet's coefficient (its constant was -0.0473); and the mean count
less 1.3259 rho^(2/3) T, with T = 3/4 exactly. For 4 points: the share of clouds peeled in one layer, which is 1 - 35/(12 pi^2) = 0.70448 by Sylvester's
four-point problem for a disc. A line holds if its figure is inside its band, ends included; a size short of its clouds by more than
1 in 1,000 makes the lines that need it "not run". Writes study4.json."""
import json, math, os, sys, zlib
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import theory, fresh
ASKED = {4: 400000, 100: 400000, 300: 400000, 1000: 400000}; NEW = (100, 300, 1000); C5, B5 = 0.08227, -0.0473; SYL = 1 - 35 / (12 * math.pi ** 2)
LINES = [('P0', 0.95, 'of clouds of four points, the share peeled in one layer is between 0.7020 and 0.7070 (Sylvester: 0.7045)'),
         ('P1', 0.50, 'B at 1,000 points is between -0.057 and -0.037'), ('P2', 0.40, 'B at 300 points is between -0.057 and -0.037'), ('P3', 0.30, 'B at 100 points is between -0.057 and -0.037'),
         ('P4', 0.70, 'B is below -0.025 at all three sizes'), ('P5', 0.40, 'B at 100 points is above B at 1,000 points by more than 0.004'),
         ('P6', 0.70, 'the mean count at 1,000 points exceeds 1.3259 rho^(2/3) T by between 0.130 and 0.165 of a layer'), ('P7', 0.45, 'the mean count at 100 points exceeds 1.3259 rho^(2/3) T by 0.245 of a layer or more')]
def verdicts(share4, b, ex):
    """the eight lines by the letter. share4: the share of one-layer clouds at four points; b[n]: B at n; ex[n]: the mean's excess at n. A missing figure (None) makes its lines None."""
    ok = lambda *xs: all(x is not None for x in xs); out = {}
    out['P0'] = bool(0.7020 <= share4 <= 0.7070) if ok(share4) else None
    for tag, n in (('P1', 1000), ('P2', 300), ('P3', 100)): out[tag] = bool(-0.057 <= b[n] <= -0.037) if ok(b.get(n)) else None
    out['P4'] = bool(all(b[n] <= -0.025 for n in NEW)) if ok(*[b.get(n) for n in NEW]) else None
    out['P5'] = bool(b[100] - b[1000] >= 0.004) if ok(b.get(100), b.get(1000)) else None
    out['P6'] = bool(0.130 <= ex[1000] <= 0.165) if ok(ex.get(1000)) else None
    out['P7'] = bool(ex[100] >= 0.245) if ok(ex.get(100)) else None
    return out
R = {}
for n, K0 in ASKED.items():
    name = 'n4-disc-%d' % n; x = fresh.counts(name)
    if x is None or len(x) < 0.999 * K0: R[n] = None; continue
    K = len(x); m = float(x.mean()); v = float(x.var(ddof=1)); rng = np.random.default_rng([20261125, zlib.crc32(name.encode())]); vals, cnt = np.unique(x, return_counts=True)
    H = rng.multinomial(K, cnt / K, size=4000); mb = H @ vals / K; vb = (H @ vals ** 2 - K * mb ** 2) / (K - 1); tm = 1.3259 * (n / math.pi) ** (2 / 3.0) * 0.75      # T = 3/4 exactly for the disc of radius 1 (theory.py has the flow program's 0.750001)
    R[n] = {'K': K, 'm': m, 'mse': float(mb.std(ddof=1)), 'v': v, 'vse': float(vb.std(ddof=1)), 'B': v - C5 * n ** (1 / 3.0), 'theory_m': tm, 'excess': m - tm, 'theory_v': theory.predictions('disc', n)['exact'], 'one': float((x == 1).mean()), 'most': float(x.max())}
if __name__ == '__main__':
    out = {'sizes': {str(n): v for n, v in R.items()}, 'lines': {}}
    print('Discs of exactly n points, the first study\'s own generator. B = variance - %.5f n^(1/3); the third sheet\'s constant was %+.4f' % (C5, B5))
    print('   points    clouds    mean count (se)       1.3259 rho^(2/3) T   excess, layers    variance (se)        the theory\'s   B')
    for n, v in R.items():
        if v is None: print('   %7d   not there, or short' % n)
        else: print('   %7d   %6d    %8.4f (%.4f)     %8.4f             %+.4f           %.4f (%.4f)      %.4f         %+.4f' % (n, v['K'], v['m'], v['mse'], v['theory_m'], v['excess'], v['v'], v['vse'], v['theory_v'], v['B']))
    r4 = R.get(4); share = None if r4 is None else r4['one']
    if r4 is not None: print('   four points: %.5f of %d clouds peeled in one layer (error %.5f); Sylvester\'s %.5f; the most layers %d' % (share, r4['K'], math.sqrt(share * (1 - share) / r4['K']), SYL, r4['most']))
    b = {n: (None if R[n] is None else R[n]['B']) for n in NEW}; ex = {n: (None if R[n] is None else R[n]['excess']) for n in NEW}; V = verdicts(share, b, ex)
    detail = {'P0': '' if share is None else '%.5f (%.5f)' % (share, math.sqrt(share * (1 - share) / r4['K']))}
    for tag, n in (('P1', 1000), ('P2', 300), ('P3', 100)): detail[tag] = '' if b[n] is None else '%+.4f (%.4f)' % (b[n], R[n]['vse'])
    detail['P4'] = '' if any(b[n] is None for n in NEW) else ', '.join('%+.4f' % b[n] for n in NEW)
    detail['P5'] = '' if b[100] is None or b[1000] is None else '%+.4f (%.4f)' % (b[100] - b[1000], math.hypot(R[100]['vse'], R[1000]['vse']))
    detail['P6'] = '' if ex[1000] is None else '%+.4f (%.4f)' % (ex[1000], R[1000]['mse']); detail['P7'] = '' if ex[100] is None else '%+.4f (%.4f)' % (ex[100], R[100]['mse'])
    held = failed = notrun = 0; brier = 0.0
    for tag, odds, what in LINES:
        ok = V[tag]
        if ok is None: notrun += 1; print('%-3s not run          %s' % (tag, what)); out['lines'][tag] = {'verdict': 'not run'}; continue
        held += ok; failed += (not ok); brier += (odds - (1.0 if ok else 0.0)) ** 2; print('%-3s %-7s (odds %.2f)  %s: %s' % (tag, 'HELD' if ok else 'FAILED', odds, what, detail[tag])); out['lines'][tag] = {'verdict': 'held' if ok else 'failed', 'odds': odds, 'detail': detail[tag]}
    n_ = held + failed; print(); print('%d held, %d failed, %d not run.%s' % (held, failed, notrun, (' Brier score of the odds %.3f.' % (brier / n_)) if n_ else ''))
    out['held'] = int(held); out['failed'] = int(failed); out['notrun'] = int(notrun); out['brier'] = brier / n_ if n_ else None
    json.dump(out, open(os.path.join(HERE, 'study4.json' if 'SHAPE_AFTER' not in os.environ else 'study4-other.json'), 'w'), indent=1, default=float)
