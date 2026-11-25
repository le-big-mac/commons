"""lattice.py: the whole-number count's own term in the variance (asked for by the referee's report on the third and fourth sheets).
python -I lattice.py
A count is a whole number. If it is a smooth quantity X taken to the nearest whole number, its variance is var(X) + 1/12 + a part
that swings with where the mean sits between two whole numbers (below it when the mean is near a whole number, above when near a
half), and the swing dies off as exp(-2 pi^2 var(X)). Here X is taken as normal, or as normal with a third cumulant (a
Gram-Charlier term) chosen to give the count its measured skewness; mean and variance of X are solved for so that the rounded
count has the measured mean and variance. Printed for each of the eight sizes: var(X), the swing, and B with the swing taken off;
then the fits of after4.py again with the swing off; then the 100-point clouds' histogram beside the two models'."""
import math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import after4, study4, fresh, theory
def pmf(mu, s2, k3=0.0):
    """the count's distribution when X has mean mu, variance s2 and third cumulant k3 (density: normal times 1 + k3 He3(z)/(6 s^3)),
    taken to the nearest whole number; cell probabilities by Simpson's rule on 400 steps a cell"""
    s = math.sqrt(s2); lo = int(math.floor(mu - 9 * s)) - 1; hi = int(math.ceil(mu + 9 * s)) + 1; ks = np.arange(lo, hi + 1); t = np.linspace(-0.5, 0.5, 401); w = np.ones(401); w[1:-1:2] = 4; w[2:-1:2] = 2; w *= (1.0 / 400) / 3
    z = (ks[:, None] + t[None, :] - mu) / s; f = np.exp(-0.5 * z * z) / (s * math.sqrt(2 * math.pi)) * (1 + k3 / (6 * s ** 3) * (z ** 3 - 3 * z)); p = (f * w[None, :]).sum(1); return ks, p / p.sum()
def moments(mu, s2, k3=0.0):
    ks, p = pmf(mu, s2, k3); m = float((ks * p).sum()); v = float(((ks - m) ** 2 * p).sum()); return m, v, float(((ks - m) ** 3 * p).sum()) / v ** 1.5
def solve(m, v, skew=None):
    """mean, variance (and third cumulant) of X such that the rounded count has mean m, variance v (and the skewness given)"""
    mu, s2, k3 = m, v - 1 / 12.0, 0.0
    for _ in range(200):
        mm, vv, sk = moments(mu, s2, k3); mu += m - mm; s2 += v - vv
        if skew is not None: k3 += (skew - sk) * s2 ** 1.5
    return mu, s2, k3
def swing(m, v, skew=None): mu, s2, k3 = solve(m, v, skew); return v - s2 - 1 / 12.0, s2, mu, k3
def table():
    S = after4.gather(); out = {}
    for n in S:
        x = fresh.counts('n%d-disc-%d' % (4 if n in study4.NEW else 3, n)); z = (x - x.mean()) / x.std(); sk = float((z ** 3).mean()); a = swing(S[n]['m'], S[n]['v']); b = swing(S[n]['m'], S[n]['v'], sk); out[n] = dict(S[n], skew=sk, swing=a[0], s2=a[1], swing_sk=b[0], s2_sk=b[1], k3=b[3], x=x)
    return out
def main():
    S = table(); N = list(S); C5 = study4.C5; cth = theory.predictions('disc', 1.0)['exact']
    print('A  the swing, by a rounded normal and by a rounded normal with the count\'s own skewness (B = variance - %.5f n^(1/3))' % C5)
    print('    points   mean count   variance   skewness   var(X), normal   swing     var(X), skewed   swing     B         B, swing off (normal; skewed)')
    for n in N: s = S[n]; print('   %7d   %9.4f   %.4f     %+.3f     %.4f           %+.4f   %.4f           %+.4f   %+.4f   %+.4f; %+.4f' % (n, s['m'], s['v'], s['skew'], s['s2'], s['swing'], s['s2_sk'], s['swing_sk'], s['v'] - C5 * n ** (1 / 3.0), s['v'] - s['swing'] - C5 * n ** (1 / 3.0), s['v'] - s['swing_sk'] - C5 * n ** (1 / 3.0)))
    print('   a rounded normal of the 100-point clouds\' spread has a swing between %+.4f (mean on a whole number) and %+.4f (mean on a half)' % (swing(10.0, S[100]['v'])[0], swing(10.5, S[100]['v'])[0]))
    print()
    for lab, key in (('normal', 'swing'), ('skewed', 'swing_sk')):
        T = {n: dict(S[n], v=S[n]['v'] - S[n][key]) for n in N}
        print('B  the fits of after4.py again with the swing (%s) taken off the variances' % lab)
        b, e, chi, dof = after4.series(T, N, 2); print('   all eight, a straight line: c = %.5f (%.5f), over the theory\'s %.4f (%.4f); b = %+.4f (%.4f); chi-square %.1f on %d; with the 1/12 off as well the constant is %+.4f' % (b[0], e[0], b[0] / cth, e[0] / cth, b[1], e[1], chi, dof, b[1] - 1 / 12.0))
        for lo in (100, 300, 1000):
            sizes = [n for n in N if n >= lo]; f = after4.power(T, sizes); b, e, chi, dof = after4.series(T, sizes, 2); print('   from %5s up: the power left free: best -%.2f (chi-square %.1f on %d); within 1: -%.2f to -%.2f; within 4: -%.2f to -%.2f; a = %.4f; the power -1/3 (a constant): %.1f on %d, %.1f above the least; c over the theory\'s %.4f, b = %+.4f (%.4f)' % (format(lo, ','), f['p'], f['chi'], f['dof'], f['in1'][0], f['in1'][1], f['in4'][0], f['in4'][1], f['a'], chi, dof, chi - f['chi'], b[0] / cth, b[1], e[1]))
        b, e, chi, dof = after4.series(T, N, 3); print('   all eight with a term e n^(-1/3): c = %.5f, b = %+.4f (%.4f), e = %+.3f (%.3f); chi-square %.1f on %d' % (b[0], b[1], e[1], b[2], e[2], chi, dof))
        print('   P5\'s figure, B at 100 points less B at 1,000: %+.4f as measured; %+.4f with the swing off' % ((S[100]['v'] - C5 * 100 ** (1 / 3.0)) - (S[1000]['v'] - C5 * 10.0), (T[100]['v'] - C5 * 100 ** (1 / 3.0)) - (T[1000]['v'] - C5 * 10.0)))
        print()
    print('C  the 100-point clouds\' histogram beside the two models\' (shares of clouds)')
    x = S[100]['x']; K = len(x); obs = {int(k): float((x == k).mean()) for k in np.unique(x)}; mu, s2, k3 = solve(S[100]['m'], S[100]['v']); ks, p0 = pmf(mu, s2); mu1, s21, k31 = solve(S[100]['m'], S[100]['v'], S[100]['skew']); ks1, p1 = pmf(mu1, s21, k31); d0 = dict(zip(ks.tolist(), p0.tolist())); d1 = dict(zip(ks1.tolist(), p1.tolist()))
    print('    layers   clouds\'   rounded normal   rounded, skewed')
    for k in sorted(obs): print('   %6d   %.5f   %.5f          %.5f' % (k, obs[k], d0.get(k, 0), d1.get(k, 0)))
    for lab, d in (('rounded normal', d0), ('rounded, skewed', d1)):
        cells = [k for k in sorted(obs) if K * d.get(k, 0) >= 5]; rest_o = 1 - sum(obs[k] for k in cells); rest_e = 1 - sum(d[k] for k in cells); chi = sum(K * (obs[k] - d[k]) ** 2 / d[k] for k in cells) + (K * (rest_o - rest_e) ** 2 / rest_e if rest_e * K >= 5 else 0)
        print('   chi-square of the clouds\' histogram about the %s: %.0f on %d cells' % (lab, chi, len(cells) + (1 if rest_e * K >= 5 else 0)))
if __name__ == '__main__': main()
