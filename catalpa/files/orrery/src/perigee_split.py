# The arcsecond left in my Moon's perigee against both JPL references: how much of it is my different tidal braking?
# Takes the tables of moon_vs_de431.py (my two runs against DE441 and DE431, nineteen century windows) and the response of my model to a change of tidal lag (cen_back_tide185 - cen_back_k2,
# the same windows), scales the response so that it cancels the T^2 term of the mean longitude in each comparison, and takes it out of the perigee and the node.
# usage: python -I perigee_split.py      (run from anywhere; reads the runs in ~/orrery)
import sys, os, io, runpy, contextlib, numpy as np; HERE = os.path.dirname(os.path.abspath(__file__)); TOP = HERE + '/..'
sys.argv = ['moon_vs_de431.py', TOP + '/cen_back_k2.txt', TOP + '/cen_back_j2t.txt', TOP + '/cen_back_j2dot431.txt']
with contextlib.redirect_stdout(io.StringIO()): G = runpy.run_path(HERE + '/moon_vs_de431.py')
T = np.array(G['T']); tab = {k: np.array(v) for k, v in G['tab'].items()}
sys.argv = ['tide_response.py', TOP + '/cen_back_tide185.txt', TOP + '/cen_back_k2.txt']
with contextlib.redirect_stdout(io.StringIO()): H = runpy.run_path(HERE + '/tide_response.py')
assert np.allclose(H['T'], T); resp = np.array(H['R'])[:, :3]            # mean longitude, perigee, node of (lag 185 - lag 195)
def fit(y, powers):
    M = np.vstack([T ** p for p in powers]).T; c = np.linalg.lstsq(M, y, rcond=None)[0]; r = y - M @ c; s2 = (r ** 2).sum() / (len(y) - len(powers)); se = np.sqrt(np.diag(s2 * np.linalg.inv(M.T @ M)))
    return c, se, np.sqrt((r ** 2).mean())
print('The response of my model to a shorter tidal lag (185 s for 195), T^2 terms from c + a T + b T^2:  mean longitude %+.5f, perigee %+.5f, node %+.5f' % tuple(fit(resp[:, k], (0, 1, 2))[0][2] for k in range(3)))
print('T in centuries back from 2000; arcsec.  "matched" = my run carries the same numbers for the Earth\'s oblateness as the reference (J2E, J2EDOT and, for DE441, J2ET2), so no cube is expected and none is fitted;')
print('"nearly matched" = my constant-oblateness run against DE431, whose oblateness has a steady rate that this run lacks (the pair I first took for matched; the checking reader made the properly matched run, and run_back16.sh repeats it);')
print('otherwise a cube is fitted as well.\n')
NOCUBE = ('cen_back_j2t.txt - DE441', 'cen_back_j2dot431.txt - DE431', 'cen_back_k2.txt - DE431')
for name in ('cen_back_j2t.txt - DE441', 'cen_back_j2dot431.txt - DE431', 'cen_back_k2.txt - DE431', 'cen_back_k2.txt - DE441', 'cen_back_j2t.txt - DE431'):
    R = tab[name]; matched = name in NOCUBE; pw = (0, 1, 2) if matched else (0, 1, 2, 3)
    s = fit(R[:, 0], pw)[0][2] / fit(resp[:, 0], (0, 1, 2))[0][2]; C = R[:, :3] - s * resp
    print(f'=== {name}  ({"matched" if name in NOCUBE[:2] else "nearly matched" if matched else "not matched"}); the tidal response is taken out {s:+.4f} times (that is, a run of mine with the lag changed by {10 * s:+.1f} s would have no square against this reference in the mean longitude)')
    for k, lab in ((1, 'perigee'), (2, 'node')):
        c0, se0, rms0 = fit(R[:, k], pw); c1, se1, rms1 = fit(C[:, k], pw); cl, sel, rmsl = fit(C[:, k], (0, 1) if matched else (0, 1, 3))
        print(f'   {lab:8s} as it is:      at T = 19 {R[-1, k]:+6.2f};  steady {c0[1]:+.4f} +- {se0[1]:.4f} a century, square {c0[2]:+.5f} +- {se0[2]:.5f}' + ('' if matched else f', cube {c0[3]:+.5f}') + f'  (rms {rms0:.3f})')
        print(f'   {"":8s} share of the tide: at T = 19 {s * resp[-1, k]:+6.2f};  square {s * fit(resp[:, k], (0, 1, 2))[0][2]:+.5f}')
        print(f'   {"":8s} with it out:    at T = 19 {C[-1, k]:+6.2f};  steady {c1[1]:+.4f} +- {se1[1]:.4f}, square {c1[2]:+.5f} +- {se1[2]:.5f}' + ('' if matched else f', cube {c1[3]:+.5f}') + f'  (rms {rms1:.3f});   as a straight line' + ('' if matched else ' and a cube') + f': steady {cl[1]:+.4f} +- {sel[1]:.4f}, rms about it {rmsl:.3f}, largest residual {np.abs(C[:, k] - np.vstack([T ** q for q in ((0, 1) if matched else (0, 1, 3))]).T @ cl).max():.2f}')
    print('   with the tide out, epoch by epoch:  perigee ' + ' '.join(f'{x:+.2f}' for x in C[:, 1]) + '\n' + ' ' * 39 + 'node    ' + ' '.join(f'{x:+.2f}' for x in C[:, 2]) + '\n')
# the same separation for the run before the in-phase tides went in (cen_back_cass.txt), against DE441: what was the steady part of the perigee then?
sys.argv = ['moon_vs_de431.py', TOP + '/cen_back_cass.txt']
with contextlib.redirect_stdout(io.StringIO()): G2 = runpy.run_path(HERE + '/moon_vs_de431.py')
print('The steady part of the perigee, mine - DE441, by the form of the fit (arcsec a century back):')
for nm, R in (('before the in-phase tides (cen_back_cass.txt)', np.array(G2['tab']['cen_back_cass.txt - DE441'])), ('with the in-phase tides (cen_back_k2.txt)', tab['cen_back_k2.txt - DE441'])):
    a = fit(R[:, 1], (0, 1, 3))[0]; b = fit(R[:, 1], (0, 1, 2, 3))[0]; s = fit(R[:, 0], (0, 1, 2, 3))[0][2] / fit(resp[:, 0], (0, 1, 2))[0][2]; c = fit(R[:, 1] - s * resp[:, 1], (0, 1, 3))[0]
    print(f'   {nm:46s} c + aT + bT^3 (the fit of the README table): {a[1]:+.4f};   with a square as well: {b[1]:+.4f} (square {b[2]:+.5f});   with the tidal response taken out first, then c + aT + bT^3: {c[1]:+.4f}')
# what separates the two references once each is set against a run of mine that carries its own oblateness: (j2dot431 - DE431) - (j2t - DE441)
d = tab['cen_back_j2dot431.txt - DE431'] - tab['cen_back_j2t.txt - DE441']
print('\nThe two matched pairs against each other, (my run with DE431\'s oblateness - DE431) - (my run with DE441\'s - DE441), fitted c + aT + bT^2:')
for k, lab in ((0, 'mean longitude'), (1, 'perigee'), (2, 'node')):
    c, se, rms = fit(d[:, k], (0, 1, 2)); print(f'   {lab:14s} steady {c[1]:+.4f}, square {c[2]:+.5f} +- {se[2]:.5f} (rms {rms:.3f}); at T = 19 {d[-1, k]:+.2f}')
# the in-phase tides: the two runs differenced directly, which needs no reference and no choice of fit
sys.argv = ['tide_response.py', TOP + '/cen_back_k2.txt', TOP + '/cen_back_cass.txt']
with contextlib.redirect_stdout(io.StringIO()): H2 = runpy.run_path(HERE + '/tide_response.py')
r2 = np.array(H2['R'])
print('\nThe run with the in-phase tides minus the run without them (cen_back_k2 - cen_back_cass), no reference involved:')
for k, lab in ((0, 'mean longitude'), (1, 'perigee'), (2, 'node')):
    c, se, rms = fit(r2[:, k], (0, 1)); c2, se2, rms2 = fit(r2[:, k], (0, 1, 2)); print(f'   {lab:14s} a straight line of {c[1]:+.4f} +- {se[1]:.4f} a century (rms {rms:.3f}); with a square allowed: steady {c2[1]:+.4f}, square {c2[2]:+.5f} +- {se2[2]:.5f}')
# a second, smaller square: my Sun against JPL's.  earth_helio_vs_jpl.out has the mean longitude of my Earth-Moon barycentre about the Sun, mine - DE441, in seven windows; the perigee's and
# the node's rates are n f(n'/n), so a difference in the Sun's place along its orbit moves them by f'(m) times that difference (the same series, differentiated by n' this time).
import re
rows = [re.sub(r'\[[^\]]*\]', '', l).split() for l in open(TOP + '/earth_helio_vs_jpl.out') if re.match(r'\s+-?\d+\.\d+\s', l)]
Ts = np.array([float(r[0]) for r in rows]); Ls = np.array([float(r[3]) for r in rows]); Ms = np.vstack([Ts ** q for q in (0, 1, 2)]).T; cs = np.linalg.lstsq(Ms, Ls, rcond=None)[0]
m = 0.0748013; cp = [(2, 3 / 4), (3, 225 / 32), (4, 4071 / 128), (5, 265493 / 2048), (6, 12822631 / 24576), (7, 1273925965 / 589824)]; cn = [(2, -3 / 4), (3, 9 / 32), (4, 273 / 128), (5, 9797 / 2048)]
fp = sum(c * k * m ** (k - 1) for k, c in cp); fn = sum(c * k * m ** (k - 1) for k, c in cn)
print(f'\nThe Sun: my Sun\'s place along its orbit minus DE441\'s, seven windows of earth_helio_vs_jpl.out fitted c + aT + bT^2: {cs[1]:+.4f} T {cs[2]:+.5f} T^2 (rms {np.sqrt(((Ls - Ms @ cs) ** 2).mean()):.4f}).')
print(f'   By the series differentiated by n\' (perigee {fp:+.3f}, node {fn:+.3f}) that puts {fp * cs[1]:+.4f} T {fp * cs[2]:+.5f} T^2 into the perigee and {fn * cs[1]:+.4f} T {fn * cs[2]:+.5f} T^2 into the node.')
R = tab['cen_back_j2t.txt - DE441']; sc = fit(R[:, 0], (0, 1, 2))[0][2] / fit(resp[:, 0], (0, 1, 2))[0][2]
for k, lab, f1 in ((1, 'perigee', fp), (2, 'node', fn)):
    y = R[:, k] - sc * resp[:, k] - f1 * (cs[1] * T + cs[2] * T ** 2); c, se, rms = fit(y, (0, 1, 2)); cl, sel, rmsl = fit(y, (0, 1))
    print(f'   (my run with the header\'s numbers - DE441), {lab}, with the tide\'s share AND the Sun\'s out: steady {c[1]:+.4f}, square {c[2]:+.5f} +- {se[2]:.5f} (rms {rms:.3f}); as a straight line {cl[1]:+.4f}, rms about it {rmsl:.3f}; at T = 19 the square left is {c[2] * 361:+.2f}')

