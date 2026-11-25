"""after3.py: what was looked at after the third sheet was scored. Nothing here was sealed.   python -I after3.py
A  the line fitted other lawful ways: with the 3,000-point clouds; without the 10,000; against other powers of n; with a bend
B  the earlier clouds set beside the line: the discs of the first two sheets and between, and every shape pooled at two sizes
C  the mean count's excess over alpha rho^(2/3) T, size by size
D  what the line means: the constant taken from the variance, and the D that very many points want
E  the shape of the spread: skewness and excess kurtosis by size
F  the second addition's discs (a million and ten million points) beside the line
G  the variance itself fitted directly, and how much of r's lean is the mean's
H  the power of n left free
I  the mean's excess with alpha as the first addition left it, and the five means fitted with alpha free
(G, H and I were added after the referee's blind step, which had done the first two and pointed at the third.)"""
import gzip, json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import study, study3, fresh, theory
R = study3.R; LINE = study3.LINE; ALL = [n for n in study3.ASKED if R[n] is not None]
def wls(sizes, power=-1 / 3.0, bend=False, extra=()):
    """r = a + s n^power (+ q n^(2 power)); returns coefficients, their errors, chi-square, degrees of freedom"""
    pts = [(n, R[n]['r'], R[n]['rse']) for n in sizes] + list(extra); x = np.array([n ** power for n, r, e in pts]); y = np.array([r for n, r, e in pts]); w = np.array([1 / e ** 2 for n, r, e in pts])
    X = np.stack([np.ones_like(x), x] + ([x * x] if bend else []), 1); A = X.T @ (X * w[:, None]); cov = np.linalg.inv(A); beta = cov @ (X.T @ (w * y)); chi = float((w * (y - X @ beta) ** 2).sum())
    return beta, np.sqrt(np.diag(cov)), chi, len(pts) - X.shape[1]
print('A  r = a + s n^(-1/3), fitted other ways (the sheet\'s way first)')
print('   which clouds                                   a (se)             s (se)            chi-square')
for lab, sizes in (('10,000 to 300,000 (the sheet\'s)', study3.FIT), ('3,000 to 300,000 (all five)', ALL), ('30,000 to 300,000', (30000, 100000, 300000)), ('3,000 to 100,000', (3000, 10000, 30000, 100000)), ('3,000 to 30,000', (3000, 10000, 30000))):
    if all(n in ALL for n in sizes): b, e, chi, dof = wls(sizes); print('   %-44s   %.4f (%.4f)    %+.3f (%.3f)    %.1f on %d' % (lab, b[0], e[0], b[1], e[1], chi, dof))
if len(ALL) == 5:
    print('   all five sizes against other powers of n: ' + '; '.join('n^(%s): chi-square %.1f on 3, a = %.4f' % (lab, wls(ALL, p)[2], wls(ALL, p)[0][0]) for lab, p in (('-1/6', -1 / 6.0), ('-1/3', -1 / 3.0), ('-1/2', -0.5), ('-2/3', -2 / 3.0))))
    b, e, chi, dof = wls(ALL, bend=True); print('   all five with a bend, r = a + s n^(-1/3) + q n^(-2/3): a = %.4f (%.4f), s = %+.3f (%.3f), q = %+.2f (%.2f); chi-square %.1f on %d' % (b[0], e[0], b[1], e[1], b[2], e[2], chi, dof))
print()
print('B  the earlier clouds beside the sheet\'s line (r over each set\'s own line)')
s4, se4, a4, ae4, chi4 = study3.F4 if study3.F4 else (float('nan'),) * 5; at = lambda n: a4 + s4 * n ** (-1 / 3.0)
def r1(n_): sh = n_.split('-')[1]; sh = 'disc' if sh == 'disc0' else sh; n0 = study.F[n_]['n0']; p = theory.predictions(sh, n0); ln = p['exact'] / p['mean'] ** 2 * n0; w_, s_ = study.stat(lambda m_, v_: v_ / m_ ** 2 * n0, n_); return (w_ / ln, s_ / ln)
def rf(k): f = fresh.reckon(k); return (f['w'] / f['line'], f['wse'] / f['line'])
import study2
q2 = {k: (v['r'], v['rse']) for k, v in study2.R.items()}
rows = [('discs by cloud.c, 100,000 (the first sheet\'s and the fresh)', 100000, fresh.pool([r1('exact-disc-100000'), rf('disc-cloud')])), ('discs by the first study\'s generator, 100,000 (20,000 and 75,000)', 100000, fresh.pool([r1('exact-disc0-100000'), rf('disc-peel')])), ('discs by cloud.c, 30,000 (the first sheet\'s)', 30000, r1('exact-disc-30000') + (0,)),
        ('every shape of both sheets and between, 100,000 (18 sets; the first 8,000 quarter discs left out)', 100000, fresh.pool([r1(n) for n in study.F if n.startswith('exact-') and n.endswith('-100000') and 'quarter' not in n] + [rf(k) for k in ('disc-cloud', 'halfdisc-cloud', 'disc-peel', 'square-peel', 'triangle-peel', 'quarter-cloud-a', 'quarter-cloud-b', 'quarter-numpy')] + [q2['cloud.c, 100,000'], q2['numpy, 100,000']])),
        ('every shape of both sheets, 30,000 (5 sets)', 30000, fresh.pool([r1(n) for n in study.F if n.endswith('-30000')] + [q2['cloud.c, 30,000'], q2['numpy, 30,000']]))]
for lab, n, v in rows: print('   %-98s %.4f (%.4f); the line there %.4f; %+.1f errors from it; this sheet\'s discs there %.4f (%.4f)' % (lab, v[0], v[1], at(n), (v[0] - at(n)) / math.hypot(v[1], se4 * 0 + 0.001), R[n]['r'] if R.get(n) else float('nan'), R[n]['rse'] if R.get(n) else float('nan')))
print()
print('C  the mean count less alpha rho^(2/3) T, in layers')
for n in ALL: print('   %7d   %+.4f (%.4f)   which is %.2f in 10,000 of the mean' % (n, R[n]['excess'], R[n]['mse'], R[n]['excess'] / R[n]['m'] * 1e4))
if len(ALL) >= 4:
    x = np.array([math.log(n) for n in ALL]); y = np.array([R[n]['excess'] for n in ALL]); w = np.array([1 / R[n]['mse'] ** 2 for n in ALL]); X = np.stack([np.ones_like(x), x], 1); cov = np.linalg.inv(X.T @ (X * w[:, None])); beta = cov @ (X.T @ (w * y)); chi = float((w * (y - X @ beta) ** 2).sum()); m0 = float((w * y).sum() / w.sum())
    print('   as a constant: %.4f, chi-square %.0f on %d; as a constant and a slope in log n: %.4f %+.4f per tenfold, chi-square %.1f on %d' % (m0, float((w * (y - m0) ** 2).sum()), len(ALL) - 1, beta[0] + beta[1] * math.log(1e5), beta[1] * math.log(10), chi, len(ALL) - 2))
print()
c1 = theory.predictions('disc', 1.0)['exact']; K_ = (4 / 3.0 * theory.D - theory.DC)
print('D  what the sheet\'s line means for a disc: variance of the count = %.4f n^(1/3) %+.4f (the theory: %.4f n^(1/3)); the constant is %.3f (%.3f) of a squared layer' % (a4 * c1, s4 * c1, c1, -s4 * c1, se4 * c1))
Dp = (a4 * K_ + theory.DC) * 0.75; Dpe = ae4 * K_ * 0.75; print('   for very many points the spread wants D = %.4f (%.4f) where %.3f is used; the ceiling of variance x n / mean^2 would then be %.4f (%.4f) and not %.4f; the standard deviation over the mean %.4f over sqrt(n) and not %.4f' % (Dp, Dpe, theory.D, a4 * LINE, ae4 * LINE, LINE, math.sqrt(a4 * LINE), math.sqrt(LINE)))
print('   at which size is the theory as it stands exactly right (r = 1)? n = %.0f' % ((-s4 / (a4 - 1)) ** 3 if a4 > 1 and s4 < 0 else float('nan')))
print()
print('E  skewness and excess kurtosis of the count (errors sqrt(6/K), sqrt(24/K))')
for n in ALL:
    x = fresh.counts('n3-disc-%d' % n); z = (x - x.mean()) / x.std(); print('   %7d   %+.4f (%.4f)   %+.4f (%.4f)' % (n, (z ** 3).mean(), math.sqrt(6 / len(x)), (z ** 4).mean() - 3, math.sqrt(24 / len(x))))
print()
print('F  the second addition\'s discs of exactly n points (../disc/runs), r and the line there')
for n in (100000, 1000000, 10000000):
    p = os.path.join(HERE, '..', 'disc', 'runs', 'exact-%d.jsonl' % n); op = open
    if not os.path.exists(p): p += '.gz'; op = lambda f: gzip.open(f, 'rt')
    if not os.path.exists(p): print('   %9d   not there' % n); continue
    x = np.array([json.loads(l)['layers'] for l in op(p)], float); r = x.var(ddof=1) * n / x.mean() ** 2 / LINE; print('   %9d   %5d clouds   r = %.4f (%.4f)   the line there %.4f' % (n, len(x), r, r * math.sqrt(2 / len(x)), at(n)))
print()
print('G  the variance itself, fitted directly: variance = c n^(1/3) + b (weighted; free of the mean\'s own excess, which sits squared under r)')
def vfit(sizes, power=1 / 3.0):
    x = np.array([n ** power for n in sizes]); y = np.array([R[n]['v'] for n in sizes]); w = np.array([1 / R[n]['vse'] ** 2 for n in sizes]); X = np.stack([x, np.ones_like(x)], 1); cov = np.linalg.inv(X.T @ (X * w[:, None])); beta = cov @ (X.T @ (w * y)); return beta, np.sqrt(np.diag(cov)), float((w * (y - X @ beta) ** 2).sum()), len(sizes) - 2
for lab, sizes in (('10,000 to 300,000', study3.FIT), ('3,000 to 300,000 (all five)', ALL)):
    if all(n in ALL for n in sizes): b, e, chi, dof = vfit(sizes); print('   %-30s c = %.5f (%.5f)   b = %+.4f (%.4f)   chi-square %.1f on %d   (the theory: c = %.5f, b = 0; c over the theory\'s %.4f)' % (lab, b[0], e[0], b[1], e[1], chi, dof, c1, b[0] / c1))
print('   how much of the lean in r is the mean\'s excess: r with the theory\'s mean under it, less r as defined: ' + ', '.join('%+.4f at %s' % (R[n]['v'] * n / R[n]['theory_m'] ** 2 / LINE - R[n]['r'], format(n, ',')) for n in ALL))
print()
print('H  the power left free: r = a + s n^(-p), all five sizes (a and s solved at each p; p on a grid of 0.01)')
if len(ALL) == 5:
    grid = [k / 100.0 for k in range(2, 151)]; chis = [wls(ALL, -p)[2] for p in grid]; best = min(chis); pb = grid[chis.index(best)]; in1 = [p for p, c in zip(grid, chis) if c <= best + 1]; in4 = [p for p, c in zip(grid, chis) if c <= best + 4]
    print('   best p = %.2f (chi-square %.2f on 2); within 1 of it: %.2f to %.2f; within 4: %.2f to %.2f' % (pb, best, in1[0], in1[-1], in4[0], in4[-1]))
    print('   a at those powers: %.4f at the best; %.4f to %.4f within 1; %.4f to %.4f within 4' % (wls(ALL, -pb)[0][0], wls(ALL, -in1[-1])[0][0], wls(ALL, -in1[0])[0][0], wls(ALL, -in4[-1])[0][0], wls(ALL, -in4[0])[0][0]))
    DD = lambda a_: (a_ * K_ + theory.DC) * 0.75; print('   read as D: %.4f at the best; %.4f to %.4f within 1; %.4f to %.4f within 4' % (DD(wls(ALL, -pb)[0][0]), DD(wls(ALL, -in1[-1])[0][0]), DD(wls(ALL, -in1[0])[0][0]), DD(wls(ALL, -in4[-1])[0][0]), DD(wls(ALL, -in4[0])[0][0])))
    chis4 = [wls(study3.FIT, -p)[2] for p in grid]; b4 = min(chis4); i1 = [p for p, c in zip(grid, chis4) if c <= b4 + 1]; print('   the four sizes from 10,000 alone: best p = %.2f; within 1 of it: %.2f to %.2f%s' % (grid[chis4.index(b4)], i1[0], i1[-1], ' (the grid\'s end)' if i1[-1] == grid[-1] or i1[0] == grid[0] else ''))
    b, e, chi, dof = wls(ALL, 1.0); x = np.array([math.log(n) for n in ALL]); y = np.array([R[n]['r'] for n in ALL]); w = np.array([1 / R[n]['rse'] ** 2 for n in ALL]); X = np.stack([np.ones_like(x), x], 1); cov = np.linalg.inv(X.T @ (X * w[:, None])); beta = cov @ (X.T @ (w * y)); print('   against log n (no limit for very many points): chi-square %.1f on 3;  against 1/n: %.1f on 3' % (float((w * (y - X @ beta) ** 2).sum()), wls(ALL, -1.0)[2]))
print()
print('I  the mean\'s excess again, with T = 3/4 exactly (C above, like the sealed script, has the flow program\'s T for the disc, %.6f), and with alpha as the first addition left it (1.32596 to 1.32599) beside the rounded 1.3259 of the sheet' % theory.TH['disc']['T'])
for n in ALL:
    X_ = (n / math.pi) ** (2 / 3.0) * 0.75; print('   %7d   with 1.3259: %+.4f   with 1.32596: %+.4f   with 1.32599: %+.4f   (error %.4f; one unit in alpha\'s fifth decimal is %.4f of a layer here)' % (n, R[n]['m'] - 1.3259 * X_, R[n]['m'] - 1.32596 * X_, R[n]['m'] - 1.32599 * X_, R[n]['mse'], 1e-5 * X_))
if len(ALL) == 5:
    Xs = np.array([(n / math.pi) ** (2 / 3.0) * 0.75 for n in ALL]); y = np.array([R[n]['m'] for n in ALL]); w = np.array([1 / R[n]['mse'] ** 2 for n in ALL]); nn = np.array(ALL, float)
    def mfit(cols, lab):
        X = np.stack(cols, 1); cov = np.linalg.inv(X.T @ (X * w[:, None])); beta = cov @ (X.T @ (w * y)); chi = float((w * (y - X @ beta) ** 2).sum()); print('   mean = alpha X + %-34s alpha = %.5f (%.5f); the rest: %s; chi-square %.1f on %d' % (lab + ':', beta[0], math.sqrt(cov[0, 0]), ', '.join('%+.4f (%.4f)' % (b_, math.sqrt(cov[i + 1, i + 1])) for i, b_ in enumerate(beta[1:])), chi, len(ALL) - X.shape[1]))
    print('   the five means fitted with alpha left free (X = rho^(2/3) T):')
    mfit([Xs, np.ones(5)], 'c'); mfit([Xs, np.ones(5), nn ** (-1 / 3.0)], 'c + d n^(-1/3)'); mfit([Xs, np.ones(5), nn ** (-1 / 6.0)], 'c + d n^(-1/6)'); mfit([Xs, np.ones(5), np.log(nn)], 'c + d log n'); mfit([Xs, nn ** (1 / 3.0)], 'd n^(1/3) (no constant)'); mfit([Xs, np.ones(5), nn ** (1 / 3.0)], 'c + d n^(1/3)')
