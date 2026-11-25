"""after4.py: what was looked at after the fourth sheet was scored. Nothing here was sealed, but the sheet said these fits would be
made.   python -I after4.py
A  the eight sizes side by side (the fourth sheet's three and the third sheet's five)
B  the power of the lean left free, over all eight sizes and over the sizes from 300, 1,000 and 3,000 up
C  the variance as c n^(1/3) + b + e n^(-1/3) (+ g n^(-2/3)), over the same ranges: is b steady?
D  the mean count as alpha rho^(2/3) T + c + d n^(-p), alpha left free, over the same ranges
E  four points: the mean and variance of the count beside Sylvester's
F  B at the eight sizes: are they one number?"""
import math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import study3, study4, theory
def wls(ys, es, cols):
    X = np.stack([np.asarray(c, float) for c in cols], 1); w = 1 / np.asarray(es, float) ** 2; cov = np.linalg.inv(X.T @ (X * w[:, None])); b = cov @ (X.T @ (w * np.asarray(ys, float))); return b, np.sqrt(np.diag(cov)), float((w * (np.asarray(ys, float) - X @ b) ** 2).sum())
def gather():
    """the eight sizes: n -> K, mean, its error, variance, its error, the theory's variance, X = rho^(2/3) T with T = 3/4"""
    S = {}
    for n in study4.NEW:
        v = study4.R[n]
        if v is not None: S[n] = dict(K=v['K'], m=v['m'], mse=v['mse'], v=v['v'], vse=v['vse'], tv=v['theory_v'])
    for n, v in study3.R.items():
        if v is not None: S[n] = dict(K=v['K'], m=v['m'], mse=v['mse'], v=v['v'], vse=v['vse'], tv=v['theory_v'])
    for n in S: S[n]['X'] = (n / math.pi) ** (2 / 3.0) * 0.75
    return dict(sorted(S.items()))
def power(S, sizes, grid=None):
    """V / theory = a + s n^(-p): the best p on a grid of 0.01, the ranges within 1 and 4 of the least chi-square, a at the best"""
    grid = grid or [k / 100.0 for k in range(2, 201)]; y = [S[n]['v'] / S[n]['tv'] for n in sizes]; e = [S[n]['vse'] / S[n]['tv'] for n in sizes]
    fits = [wls(y, e, [[1.0] * len(sizes), [n ** -p for n in sizes]]) for p in grid]; ch = [f[2] for f in fits]; k = int(np.argmin(ch)); in1 = [p for p, c in zip(grid, ch) if c <= ch[k] + 1]; in4 = [p for p, c in zip(grid, ch) if c <= ch[k] + 4]
    return dict(p=grid[k], chi=ch[k], dof=len(sizes) - 3, in1=(in1[0], in1[-1]), in4=(in4[0], in4[-1]), a=float(fits[k][0][0]), a1=(float(fits[grid.index(in1[-1])][0][0]), float(fits[grid.index(in1[0])][0][0])), fixed={p: wls(y, e, [[1.0] * len(sizes), [n ** -p for n in sizes]]) for p in (1 / 6.0, 1 / 3.0, 0.5, 2 / 3.0)})
def series(S, sizes, terms):
    """V = c n^(1/3) + b (+ e n^(-1/3) (+ g n^(-2/3))): coefficients, errors, chi-square, degrees of freedom"""
    cols = [[n ** (1 / 3.0) for n in sizes], [1.0] * len(sizes)] + [[n ** (-k / 3.0) for n in sizes] for k in range(1, terms - 1)]; b, e, chi = wls([S[n]['v'] for n in sizes], [S[n]['vse'] for n in sizes], cols); return b, e, chi, len(sizes) - terms
def meanfit(S, sizes, p, extra=False):
    cols = [[S[n]['X'] for n in sizes], [1.0] * len(sizes), [n ** -p for n in sizes]] + ([[n ** (-2 * p) for n in sizes]] if extra else []); b, e, chi = wls([S[n]['m'] for n in sizes], [S[n]['mse'] for n in sizes], cols); return b, e, chi, len(sizes) - len(cols)
def main():
    S = gather(); N = list(S); c_th = theory.predictions('disc', 1.0)['exact']
    print('A  the eight sizes (B = variance - %.5f n^(1/3); the excess is the mean count less 1.3259 rho^(2/3) T with T = 3/4)' % study4.C5)
    print('    points    clouds   variance (se)        over the theory\'s    B (se)              the mean\'s excess (se)')
    for n in N: s = S[n]; print('   %7d   %6d   %.4f (%.4f)     %.4f (%.4f)      %+.4f (%.4f)    %+.4f (%.4f)' % (n, s['K'], s['v'], s['vse'], s['v'] / s['tv'], s['vse'] / s['tv'], s['v'] - study4.C5 * n ** (1 / 3.0), s['vse'], s['m'] - 1.3259 * s['X'], s['mse']))
    print()
    print('B  the lean with its power left free: variance over the theory\'s = a + s n^(-p)')
    for lo in (100, 300, 1000, 3000):
        sizes = [n for n in N if n >= lo]
        if len(sizes) < 4: continue
        f = power(S, sizes); print('   from %6s up (%d sizes): best p = %.2f, chi-square %.1f on %d; within 1 of it %.2f to %.2f; within 4, %.2f to %.2f; a = %.4f (%.4f to %.4f within 1)' % (format(lo, ','), len(sizes), f['p'], f['chi'], f['dof'], f['in1'][0], f['in1'][1], f['in4'][0], f['in4'][1], f['a'], f['a1'][0], f['a1'][1]))
        print('        at fixed powers: ' + '; '.join('n^(-%s): chi-square %.1f on %d, a = %.4f (%.4f)' % (lab, f['fixed'][p][2], len(sizes) - 2, f['fixed'][p][0][0], f['fixed'][p][1][0]) for lab, p in (('1/6', 1 / 6.0), ('1/3', 1 / 3.0), ('1/2', 0.5), ('2/3', 2 / 3.0))))
    print()
    print('C  the variance as a series in n^(-1/3): c n^(1/3) + b + e n^(-1/3) + g n^(-2/3)   (the theory: c = %.5f)' % c_th)
    for lo in (100, 300, 1000, 3000):
        sizes = [n for n in N if n >= lo]
        for terms in (2, 3, 4):
            if len(sizes) <= terms: continue
            b, e, chi, dof = series(S, sizes, terms); print('   from %6s up, %d terms: c = %.5f (%.5f)  b = %+.4f (%.4f)%s%s   chi-square %.1f on %d' % (format(lo, ','), terms, b[0], e[0], b[1], e[1], '  e = %+.3f (%.3f)' % (b[2], e[2]) if terms > 2 else '', '  g = %+.2f (%.2f)' % (b[3], e[3]) if terms > 3 else '', chi, dof))
    print()
    print('D  the mean count as alpha X + c + d n^(-p) (+ f n^(-2p)), alpha left free (X = rho^(2/3) T, T = 3/4)')
    for lo in (100, 300, 1000, 3000):
        sizes = [n for n in N if n >= lo]
        for lab, p, extra in (('n^(-1/3)', 1 / 3.0, False), ('n^(-1/6)', 1 / 6.0, False), ('n^(-1/3) and n^(-2/3)', 1 / 3.0, True), ('n^(-1/6) and n^(-1/3)', 1 / 6.0, True)):
            if len(sizes) <= 3 + extra: continue
            b, e, chi, dof = meanfit(S, sizes, p, extra); print('   from %6s up, %-22s alpha = %.5f (%.5f)  c = %+.4f (%.4f)  d = %+.3f (%.3f)%s   chi-square %.1f on %d' % (format(lo, ','), lab + ':', b[0], e[0], b[1], e[1], b[2], e[2], '  f = %+.2f (%.2f)' % (b[3], e[3]) if extra else '', chi, dof))
        if len(sizes) > 3:
            b, e, chi = wls([S[n]['m'] for n in sizes], [S[n]['mse'] for n in sizes], [[S[n]['X'] for n in sizes], [1.0] * len(sizes), [n ** (1 / 3.0) for n in sizes]]); print('   from %6s up, %-22s alpha = %.5f (%.5f)  c = %+.4f (%.4f)  k = %+.4f (%.4f)   chi-square %.1f on %d   (asked for by the referee: the next power below n^(2/3))' % (format(lo, ','), 'c + k n^(1/3):', b[0], e[0], b[1], e[1], b[2], e[2], chi, len(sizes) - 3))
            if len(sizes) > 4: b, e, chi = wls([S[n]['m'] for n in sizes], [S[n]['mse'] for n in sizes], [[S[n]['X'] for n in sizes], [1.0] * len(sizes), [n ** (1 / 3.0) for n in sizes], [n ** (-1 / 3.0) for n in sizes]]); print('   from %6s up, %-22s alpha = %.5f (%.5f)  c = %+.4f (%.4f)  k = %+.4f (%.4f)  d = %+.3f (%.3f)   chi-square %.1f on %d' % (format(lo, ','), 'c + k n^(1/3) + d n^(-1/3):', b[0], e[0], b[1], e[1], b[2], e[2], b[3], e[3], chi, len(sizes) - 4))
            b, e, chi = wls([S[n]['m'] for n in sizes], [S[n]['mse'] for n in sizes], [[S[n]['X'] for n in sizes], [1.0] * len(sizes), [math.log10(n) for n in sizes]]); print('   from %6s up, %-22s alpha = %.5f (%.5f)  c = %+.4f (%.4f)  d = %+.4f (%.4f) for each tenfold   chi-square %.1f on %d' % (format(lo, ','), 'the logarithm of n:', b[0], e[0], b[1], e[1], b[2], e[2], chi, len(sizes) - 3))
    print()
    print('   the excess over alpha X with alpha at 1.32596 and 1.32599 (the first addition\'s range): ' + '; '.join('%s: %+.4f, %+.4f' % (format(n, ','), S[n]['m'] - 1.32596 * S[n]['X'], S[n]['m'] - 1.32599 * S[n]['X']) for n in N))
    print()
    print('F  B at the eight sizes: are they one number? (B\'s own errors only; the coefficient %.5f is held fixed)' % study4.C5)
    for lo in (100, 1000):
        sizes = [n for n in N if n >= lo]; y = np.array([S[n]['v'] - study4.C5 * n ** (1 / 3.0) for n in sizes]); w = np.array([1 / S[n]['vse'] ** 2 for n in sizes]); m0 = float((w * y).sum() / w.sum()); print('   from %6s up: the weighted mean of B is %+.4f (%.4f); chi-square about it %.1f on %d; the least %+.4f, the greatest %+.4f' % (format(lo, ','), m0, 1 / math.sqrt(w.sum()), float((w * (y - m0) ** 2).sum()), len(sizes) - 1, y.min(), y.max()))
    print()
    r4 = study4.R.get(4)
    if r4 is not None:
        p = study4.SYL; print('E  four points: mean count %.5f (%.5f), Sylvester\'s 2 - p = %.5f; variance %.5f (%.5f), p(1 - p) = %.5f; the theory\'s formulas there: mean %.4f, variance %.4f' % (r4['m'], r4['mse'], 2 - p, r4['v'], r4['vse'], p * (1 - p), 1.3259 * (4 / math.pi) ** (2 / 3.0) * 0.75, c_th * 4 ** (1 / 3.0)))
if __name__ == '__main__': main()
