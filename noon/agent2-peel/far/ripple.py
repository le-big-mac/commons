"""ripple.py: how fast does a ripple of the front die away with height?   python -I ripple.py [make]
The picture in the README says: at large scales the depth T(x, y) obeys dT/dy = alpha + (1/3) T_xx (+ noise), the 1/3 coming from
Calder and Smart's limit (the lifted front moves as the cube root of its curvature). So above a floor rippled as A (1 + cos kx) the
ripple in the depth at height y should be -alpha A exp(-k^2 y / 3) cos kx: its size falls by e in a height of 3 / k^2, whatever A is.
This measures it: cell2 -floor A L on windows 8,192 wide, the slabs written out, the cosine part of each slab's column means found
by least squares, and the rate of its fall fitted. "make" runs the windows (a few minutes); without it the files in runs-ripple/ are read.
The raw slabs are 2 MB a window; the cosine and sine parts found from them are kept in runs-ripple/amplitudes.json, and where
the raw files are absent (the published folder) those are used: the output is the same."""
import array, json, math, os, subprocess, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); BIN = os.environ.get('CELL2', os.path.join(HERE, 'cell2')); R = os.path.join(HERE, 'runs-ripple')
C, WCOL = 4096, 2; W = C * WCOL
CASES = [(64, 5.0, 1600), (64, 2.5, 1600), (128, 20.0, 6000), (128, 10.0, 6000), (256, 60.0, 20000), (256, 30.0, 20000)]      # wavelength, amplitude, height
SEEDS = (1, 2, 3, 4)
def name(L, A, s, ext): return os.path.join(R, 'ripple-%d-%g-%d.%s' % (L, A, s, ext))
if len(sys.argv) > 1 and sys.argv[1] == 'make':
    from concurrent.futures import ThreadPoolExecutor
    def one(job):
        L, A, HM, s = job
        r = subprocess.run([BIN, str(C), str(WCOL), str(HM), str(9000 + s), '-floor', str(A), str(L), '-snap', name(L, A, s, 'bin')], capture_output=True, text=True)
        open(name(L, A, s, 'json'), 'w').write(r.stdout); return r.returncode
    with ThreadPoolExecutor(max_workers=4) as ex: codes = list(ex.map(one, [(L, A, HM, s) for L, A, HM in CASES for s in SEEDS]))
    print('made %d windows; exit codes other than 0: %d' % (len(codes), sum(1 for c in codes if c)))
x = (np.arange(C) + 0.5) * WCOL
KEPT = os.path.join(R, 'amplitudes.json'); kept = json.load(open(KEPT)) if os.path.exists(KEPT) else {}; fresh = {}
def amplitudes(L, A, s):
    key = '%d-%g-%d' % (L, A, s)
    if not os.path.exists(name(L, A, s, 'bin')): return [tuple(t) for t in kept[key]]       # the raw slabs are not here: what was kept of them
    o = json.load(open(name(L, A, s, 'json'))); hs = o['snap_heights']; raw = np.frombuffer(open(name(L, A, s, 'bin'), 'rb').read(), dtype=np.float64).reshape(len(hs), C)
    k = 2 * math.pi / L; out = []
    for h, row in zip(hs, raw):
        m = ~np.isnan(row); M = np.column_stack([np.ones(m.sum()), np.cos(k * x[m]), np.sin(k * x[m])]); coef = np.linalg.lstsq(M, row[m], rcond=None)[0]
        out.append((h + 2.0, float(coef[1]), float(coef[2])))            # the middle of the slab; the cosine and the sine part
    fresh[key] = out
    return out
print('wavelength  amplitude   k^2/3      fitted over heights    rate of fall     rate / (k^2/3)   cosine part at the lowest and the highest height fitted (alpha A)   largest sine part')
allr = []; other = {}
for L, A, HM in CASES:
    k = 2 * math.pi / L; want = k * k / 3; per = [amplitudes(L, A, s) for s in SEEDS]
    hs = np.array([p[0] for p in per[0]]); cosp = np.mean([[p[1] for p in q] for q in per], axis=0); sinp = np.mean([[p[2] for p in q] for q in per], axis=0)
    lo, hi = 2 * A + 3 / (k * k) * 0.3, 2 * A + 3 / (k * k) * 3.0            # from a little above the crests to three e-folds
    m = (hs >= lo) & (hs <= hi) & (cosp < 0)
    rate = -np.polyfit(hs[m], np.log(-cosp[m]), 1)[0]
    each = []
    for q in per:
        c = np.array([p[1] for p in q]); mm = m & (c < 0); each.append(-np.polyfit(hs[mm], np.log(-c[mm]), 1)[0])
    allr.append((L, A, rate / want, np.std(each, ddof=1) / math.sqrt(len(each)) / want))
    for f0, f1 in ((0.5, 2.0), (0.3, 2.0), (1.0, 3.0)):      # other stretches of height to fit over
        m2 = (hs >= 2 * A + 3 / (k * k) * f0) & (hs <= 2 * A + 3 / (k * k) * f1) & (cosp < 0); other.setdefault((f0, f1), []).append(-np.polyfit(hs[m2], np.log(-cosp[m2]), 1)[0] / want)
    print('  %4d      %5.1f     %.3e   %6.0f to %6.0f (%2d slabs)   %.3e      %.3f (%.3f)      %7.2f, %6.2f  (%.2f)      %.2f' % (
        L, A, want, hs[m].min(), hs[m].max(), m.sum(), rate, rate / want, allr[-1][3], cosp[m][-1], cosp[m][0], 1.3259 * A, np.abs(sinp[m]).max()))
print('\nthe smoothing constant measured, as a multiple of 1/3 (four windows each; in brackets the standard error from the four): ' + ', '.join('%.3f (%.3f)' % (r, e) for L, A, r, e in allr))
print('so nu = %s' % ', '.join('%.3f' % (r / 3) for L, A, r, e in allr))
print('the table fits from 0.3 to 3 of the height in which the ripple should fall by e. Fitted over other stretches, the six multiples of 1/3 are:')
for (f0, f1), v in other.items(): print('   %.1f to %.1f: %s' % (f0, f1, ', '.join('%.3f' % x for x in v)))
w = [1 / e ** 2 for L, A, r, e in allr]; print('weighing each of the six by its standard error, the multiple of 1/3 is %.3f (%.3f)' % (sum(wi * r for wi, (L, A, r, e) in zip(w, allr)) / sum(w), 1 / math.sqrt(sum(w))))
if fresh and len(fresh) == len(CASES) * len(SEEDS): json.dump(fresh, open(KEPT, 'w'))
