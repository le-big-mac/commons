"""after5.py: what was looked at after the fifth sheet was scored. Nothing here was sealed, but the sheet said these would be done.
python -I after5.py
A  the six small discs: B beside the swinging count's figure and the level one; the size of the swing fitted
B  fourteen sizes of disc (the six, and the eight of the third and fourth sheets) with the swing taken off: is what is left one constant?
C  the triangle, the rounded triangle and the discs: B at each size, each shape's B as one constant, and the differences
D  the mean counts of the shapes beside the theory's"""
import math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import study5, study4, after4, lattice, ruler5, theory, fresh
wls = after4.wls
def small():
    """the six small discs: n -> mean, variance, error, skewness, B, the swing by the rounded count with the set's own mean, variance and skewness"""
    out = {}
    for n in study5.LAT:
        r = study5.R.get('disc-%d' % n)
        if r is None: continue
        x = fresh.counts('n5-disc-%d' % n); z = (x - x.mean()) / x.std(); sk = float((z ** 3).mean()); sw = lattice.swing(r['m'], r['v'], sk); out[n] = dict(K=r['K'], m=r['m'], mse=r['mse'], v=r['v'], vse=r['vse'], tv=r['theory_v'], skew=sk, B=r['B'], swing=sw[0], s2=sw[1], X=(n / math.pi) ** (2 / 3.0) * 0.75)
    return out
def main():
    S6 = small(); N6 = list(S6); C5 = study5.C5; cth = theory.predictions('disc', 1.0)['exact']
    print('A  the six small discs (B = variance - %.5f n^(1/3))' % C5)
    print('    points   mean count (se)     expected   variance (se)      B (se)             if it swings   if level   the set\'s own swing (its mean, variance and skewness %s)' % '')
    lev = {n: ruler5.line_of(n) - C5 * n ** (1 / 3.0) for n in study5.LAT}
    for n in N6: s = S6[n]; print('   %5d   %8.4f (%.4f)   %6.3f     %.4f (%.4f)    %+.4f (%.4f)   %+.4f        %+.4f    %+.4f   (skewness %+.3f)' % (n, s['m'], s['mse'], ruler5.mean_of(n), s['v'], s['vse'], s['B'], s['vse'], study5.PRED[n], lev[n], s['swing'], s['skew']))
    if len(N6) == 6:
        y = [S6[n]['B'] - lev[n] for n in N6]; x = [study5.PRED[n] - lev[n] for n in N6]; e = [S6[n]['vse'] for n in N6]; b, be, chi = wls(y, e, [[1.0] * 6, x])
        print('   B less the level figure = offset + size x (the swinging figure less the level one): offset %+.4f (%.4f), size %.2f (%.2f); chi-square %.1f on 4' % (b[0], be[0], b[1], be[1], chi))
        b0, be0, chi0 = wls(y, e, [[1.0] * 6]); print('   with no swing at all (an offset alone): chi-square %.1f on 5; with the swing as modelled and no offset: %.1f on 6' % (chi0, sum(((S6[n]['B'] - study5.PRED[n]) / S6[n]['vse']) ** 2 for n in N6)))
        Z = (S6[90]['B'] + S6[105]['B'] + S6[120]['B']) / 3 - (S6[83]['B'] + S6[98]['B'] + S6[113]['B']) / 3; print('   Z = %+.4f (%.4f); the swinging count gives +0.0131' % (Z, math.sqrt(sum(S6[n]['vse'] ** 2 for n in N6)) / 3))
        print('   the six with each set\'s own swing taken off: ' + ', '.join('%+.4f' % (S6[n]['B'] - S6[n]['swing']) for n in N6) + '; chi-square about their mean %.1f on 5' % wls([S6[n]['B'] - S6[n]['swing'] for n in N6], e, [[1.0] * 6])[2])
    print()
    T8 = lattice.table(); T = {n: dict(T8[n], v=T8[n]['v'] - T8[n]['swing_sk']) for n in T8}; T.update({n: dict(S6[n], v=S6[n]['v'] - S6[n]['swing']) for n in N6}); T = dict(sorted(T.items())); N = list(T)
    print('B  fourteen sizes of disc with the swing off (each set\'s own, by the rounded count with its skewness)' if len(N) == 14 else 'B  %d sizes of disc with the swing off' % len(N))
    print('   B, swing off: ' + '; '.join('%s: %+.4f (%.4f)' % (format(n, ','), T[n]['v'] - C5 * n ** (1 / 3.0), T[n]['vse']) for n in N))
    for lo in (83, 300, 1000):
        sizes = [n for n in N if n >= lo]; f = after4.power(T, sizes); b, e, chi, dof = after4.series(T, sizes, 2); b3, e3, chi3, dof3 = after4.series(T, sizes, 3)
        print('   from %5s up (%2d sizes): a straight line: c over the theory\'s %.4f (%.4f), b = %+.4f (%.4f), chi-square %.1f on %d; the power left free: -%.2f (within 1: -%.2f to -%.2f; within 4: -%.2f to -%.2f), chi-square %.1f on %d, a = %.4f; with e n^(-1/3): c over the theory\'s %.4f, b = %+.4f (%.4f), e = %+.3f (%.3f), chi-square %.1f on %d' % (format(lo, ','), len(sizes), b[0] / cth, e[0] / cth, b[1], e[1], chi, dof, f['p'], f['in1'][0], f['in1'][1], f['in4'][0], f['in4'][1], f['chi'], f['dof'], f['a'], b3[0] / cth, b3[1], e3[1], b3[2], e3[2], chi3, dof3))
    print('   one straight line over parts of the range (asked for by the referee: where does a constant stop fitting?):')
    for lab, sizes in (('all fourteen sizes', N), ('83 to 10,000', [n for n in N if n <= 10000]), ('83 to 3,000', [n for n in N if n <= 3000]), ('83 to 120 and the three largest', [n for n in N if n <= 120 or n >= 30000]), ('300 up', [n for n in N if n >= 300]), ('1,000 up', [n for n in N if n >= 1000]), ('3,000 up', [n for n in N if n >= 3000])):
        b_, e_, chi_, dof_ = after4.series(T, sizes, 2); print('      %-32s c over the theory\'s %.4f (%.4f), b = %+.4f (%.4f), chi-square %.1f on %d' % (lab, b_[0] / cth, e_[0] / cth, b_[1], e_[1], chi_, dof_))
    print()
    print('C  the shapes through cloud.c (B = variance - %.4f x the theory\'s for the shape and size), and the first generator\'s discs' % study5.RATIO)
    R = study5.R; g = lambda k: None if R.get(k) is None else (R[k]['B'], R[k]['vse']); S3 = (300, 1000, 3000); own_e = {300: 0.0011, 1000: 0.0018, 3000: 0.0025}
    print('    points   triangle            rounded triangle    disc, the first generator (third and fourth sheets)   disc through cloud.c')
    for n in S3: print('   %6d   %s   %s   %+.4f (%.4f)                                    %s' % (n, '%+.4f (%.4f)' % g('triangle-%d' % n) if g('triangle-%d' % n) else 'not there       ', '%+.4f (%.4f)' % g('rtriangle-%d' % n) if g('rtriangle-%d' % n) else 'not there       ', study5.OWN[n], own_e[n], ('%+.4f (%.4f)' % g('cdisc-1000')) if n == 1000 and g('cdisc-1000') else ''))
    def const(vals): b, e, chi = wls([v[0] for v in vals], [v[1] for v in vals], [[1.0] * len(vals)]); return float(b[0]), float(e[0]), chi
    tri = [g('triangle-%d' % n) for n in S3]; rtr = [g('rtriangle-%d' % n) for n in S3]; dsc = [(study5.OWN[n], own_e[n]) for n in S3]
    if all(tri) and all(rtr):
        ct, cr, cd = const(tri), const(rtr), const(dsc)
        print('   as one constant each: triangle %+.4f (%.4f), chi-square %.1f on 2; rounded triangle %+.4f (%.4f), %.1f on 2; disc %+.4f (%.4f), %.1f on 2' % (ct + cr + cd))
        for lab, A, Bv in (('triangle less disc', tri, dsc), ('rounded triangle less disc', rtr, dsc), ('triangle less rounded triangle', tri, rtr)):
            d = [(a[0] - b_[0], math.hypot(a[1], b_[1])) for a, b_ in zip(A, Bv)]; c = const(d); print('   %-32s %s; together %+.4f (%.4f), %+.1f errors, chi-square %.1f on 2' % (lab + ':', '; '.join('%s: %+.4f (%.4f)' % (format(n, ','), x[0], x[1]) for n, x in zip(S3, d)), c[0], c[1], c[0] / c[1], c[2]))
        sh = ruler5.shapes(study5.OWN); print('   what the readings gave: the same share: triangle less disc %s, rounded triangle less disc %s, triangle less rounded %s' % tuple('; '.join('%+.4f' % f_(n) for n in S3) for f_ in (lambda n: sh[n]['the same share'][0] - study5.OWN[n], lambda n: sh[n]['the same share'][1] - study5.OWN[n], lambda n: sh[n]['the same share'][0] - sh[n]['the same share'][1])))
        print('   the triangle\'s B over the disc\'s: ' + '; '.join('%s: %.2f (%.2f)' % (format(n, ','), t[0] / d_[0], abs(t[0] / d_[0]) * math.hypot(t[1] / t[0], d_[1] / d_[0])) for n, t, d_ in zip(S3, tri, dsc)) + '; the same share would be %.3f; the rounded triangle\'s over the disc\'s: ' % (theory.predictions('triangle', 1000)['exact'] / theory.predictions('disc', 1000)['exact']) + '; '.join('%s: %.2f (%.2f)' % (format(n, ','), t[0] / d_[0], abs(t[0] / d_[0]) * math.hypot(t[1] / t[0], d_[1] / d_[0])) for n, t, d_ in zip(S3, rtr, dsc)) + '; the same share %.3f' % (theory.predictions('rtriangle', 1000)['exact'] / theory.predictions('disc', 1000)['exact']))
    if all(tri) and all(rtr):
        print('   as shares (B over %.4f x the theory\'s variance for the shape and size):' % study5.RATIO)
        tvs = lambda sh, n: study5.RATIO * theory.predictions(sh, n)['exact']; SH = {}
        for n, t, r_, d_ in zip(S3, tri, rtr, dsc): SH[n] = ((t[0] / tvs('triangle', n), t[1] / tvs('triangle', n)), (r_[0] / tvs('rtriangle', n), r_[1] / tvs('rtriangle', n)), (d_[0] / tvs('disc', n), d_[1] / tvs('disc', n))); print('   %6d   triangle %+.4f (%.4f)   rounded triangle %+.4f (%.4f)   disc %+.4f (%.4f)   triangle less disc %+.4f (%.4f)   rounded less disc %+.4f (%.4f)   triangle less rounded %+.4f (%.4f)' % (n, SH[n][0][0], SH[n][0][1], SH[n][1][0], SH[n][1][1], SH[n][2][0], SH[n][2][1], SH[n][0][0] - SH[n][2][0], math.hypot(SH[n][0][1], SH[n][2][1]), SH[n][1][0] - SH[n][2][0], math.hypot(SH[n][1][1], SH[n][2][1]), SH[n][0][0] - SH[n][1][0], math.hypot(SH[n][0][1], SH[n][1][1])))
        if g('cdisc-1000'): c_ = g('cdisc-1000'); print('   at 1,000 points against the disc through cloud.c (%+.4f (%.4f) as a share): triangle less it %+.4f (%.4f), rounded triangle less it %+.4f (%.4f)' % (c_[0] / tvs('disc', 1000), c_[1] / tvs('disc', 1000), SH[1000][0][0] - c_[0] / tvs('disc', 1000), math.hypot(SH[1000][0][1], c_[1] / tvs('disc', 1000)), SH[1000][1][0] - c_[0] / tvs('disc', 1000), math.hypot(SH[1000][1][1], c_[1] / tvs('disc', 1000))))
        shr = ruler5.shapes(study5.OWN); beyond = [(t[0] - r_[0] - (shr[n]['the same share'][0] - shr[n]['the same share'][1]), math.hypot(t[1], r_[1])) for n, t, r_ in zip(S3, tri, rtr)]; beyond_d = [(t[0] - d_[0] - (shr[n]['the same share'][0] - study5.OWN[n]), math.hypot(t[1], d_[1])) for n, t, d_ in zip(S3, tri, dsc)]; beyond_r = [(r_[0] - d_[0] - (shr[n]['the same share'][1] - study5.OWN[n]), math.hypot(r_[1], d_[1])) for n, r_, d_ in zip(S3, rtr, dsc)]
        for lab, bb in (('triangle less rounded triangle, beyond the same share', beyond), ('triangle less disc, beyond the same share', beyond_d), ('rounded triangle less disc, beyond the same share', beyond_r)): c = const(bb); print('   %-52s %s; together %+.4f (%.4f), chi-square %.1f on 2' % (lab + ':', '; '.join('%s: %+.4f (%.4f), %+.1f errors' % (format(n, ','), x[0], x[1], x[0] / x[1]) for n, x in zip(S3, bb)), c[0], c[1], c[2]))
    print()
    print('D  the mean counts beside the theory\'s (alpha rho^(2/3) T with alpha = 1.3259 and T from the flow program)')
    for k, r in R.items():
        if r is not None and r['shape'] != 'disc': print('   %-15s mean %9.4f (%.4f)   the theory\'s %9.4f   excess %+.4f' % (k, r['m'], r['mse'], r['theory_m'], r['m'] - r['theory_m']))
if __name__ == '__main__': main()
