"""ruler5.py: before the fifth sheet is sealed: what each reading says its clouds will show.   python -I ruler5.py
(1) Discs of 83, 90, 98, 105, 113 and 120 points, whose mean counts should sit near 9, 9.5, 10, 10.5, 11 and 11.5 layers. If the count
is a smooth quantity taken to a whole number, its variance swings down where the mean is near a whole number and up where it is near
a half (lattice.py); if not, B = variance - 0.08227 n^(1/3) runs level. The smooth quantity is given the mean, the variance and the
skewness that the fourth sheet's clouds of 100 to 300,000 points fix (the forms are written out below).
(2) Triangles with sharp corners and with round ones (the first sheet's "rtriangle"), and a disc as control, all through cloud.c, at
300, 1,000 and 3,000 points. B for a shape is its variance less 1.0197 of the theory's for that shape (1.0197 = 0.08227 / 0.08068,
the third sheet's coefficient over the theory's). Three readings of what is missing from the variance: the same amount for every
shape (it is made at the centre); the same share of every shape's variance; more where there are corners."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import lattice, theory
LAT = (83, 90, 98, 105, 113, 120); C5 = 0.08227; RATIO = 1.0197
mean_of = lambda n: 1.32594 * (n / math.pi) ** (2 / 3.0) * 0.75 + 0.2598 - 0.0411 * math.log10(n)          # after4.out, D: the logarithm, all eight sizes
smooth_of = lambda n: 0.08221 * n ** (1 / 3.0) - 0.0483 + 0.050 * n ** (-1 / 3.0)                           # lattice.out, B (skewed): the variance with the swing off, three terms
line_of = lambda n: 0.08205 * n ** (1 / 3.0) - 0.0414                                                       # after4.out, C: the straight line through the eight variances as measured
def swing_model(n, gamma):
    """the variance of the count at n points if it is a smooth quantity of mean mean_of(n), variance smooth_of(n) - 1/12 and standardized third cumulant gamma, taken to the nearest whole number"""
    s2 = smooth_of(n) - 1 / 12.0; k3 = gamma * s2 ** 1.5; mu = mean_of(n)
    for _ in range(60): mu += mean_of(n) - lattice.moments(mu, s2, k3)[0]
    return lattice.moments(mu, s2, k3)[1]
def gamma100():
    t = lattice.table(); return t[100]['k3'] / t[100]['s2_sk'] ** 1.5
def shapes(Bd):
    """B of the triangle and of the rounded triangle at n under the three readings, given the disc's B there"""
    out = {}
    for n in (300, 1000, 3000):
        vt, vr, vd = (theory.predictions(sh, n)['exact'] for sh in ('triangle', 'rtriangle', 'disc')); out[n] = {'the same amount (the centre)': (Bd[n], Bd[n]), 'the same share': (Bd[n] * vt / vd, Bd[n] * vr / vd), 'corners add (0.045 more with corners)': (Bd[n] - 0.045, Bd[n])}
    return out
if __name__ == '__main__':
    import study5
    g = gamma100(); print('the smooth quantity\'s standardized third cumulant, from the 100-point clouds: %+.3f' % g)
    print('1  discs: points, the mean count expected, B if the count swings, B if it does not (the straight line)')
    Bs, Bl = {}, {}
    for n in LAT: Bs[n] = swing_model(n, g) - C5 * n ** (1 / 3.0); Bl[n] = line_of(n) - C5 * n ** (1 / 3.0); print('   %4d   %7.3f   %+.4f   %+.4f' % (n, mean_of(n), Bs[n], Bl[n]))
    Z = lambda B: (B[90] + B[105] + B[120]) / 3 - (B[83] + B[98] + B[113]) / 3
    print('   Z, the three sizes near a half less the three near a whole number: %+.4f if it swings, %+.4f if not; its error with 200,000 clouds a size about %.4f' % (Z(Bs), Z(Bl), 0.34 * math.sqrt(2 / 2e5) * math.sqrt(2 / 3.0)))
    print('   as a check of the model on a size in hand: 100 points %+.4f (the clouds: -0.0432); 300 points %+.4f (-0.0401)' % (swing_model(100, g) - C5 * 100 ** (1 / 3.0), swing_model(300, g) - C5 * 300 ** (1 / 3.0)))
    print('   the lines: swings -> ' + ' '.join('%s:%s' % (k, 'Y' if v else 'n') for k, v in study5.verdicts(Bs, None, None, None).items() if v is not None) + ';  level -> ' + ' '.join('%s:%s' % (k, 'Y' if v else 'n') for k, v in study5.verdicts(Bl, None, None, None).items() if v is not None))
    print()
    Bd = {300: -0.0401, 1000: -0.0450, 3000: -0.0471}; sh = shapes(Bd)
    print('2  shapes: B of the triangle, of the rounded triangle (the disc\'s B, from the fourth and third sheets: %s)' % ', '.join('%+.4f at %s' % (Bd[n], format(n, ',')) for n in Bd))
    for lab in sh[300]:
        Bt = {n: sh[n][lab][0] for n in sh}; Br = {n: sh[n][lab][1] for n in sh}; v = study5.verdicts(None, Bd[1000], Bt, Br); print('   %-40s %s   ->  %s' % (lab, '; '.join('%s: %+.4f, %+.4f' % (format(n, ','), Bt[n], Br[n]) for n in sh), ' '.join('%s:%s' % (k, 'Y' if x else 'n') for k, x in v.items() if x is not None)))
    print('   errors to expect of a variance: ' + ', '.join('%.4f at %s (%s clouds)' % (theory.predictions('triangle', n)['exact'] * math.sqrt(2.0 / K), format(n, ','), format(K, ',')) for n, K in ((300, 400000), (1000, 400000), (3000, 200000))))
