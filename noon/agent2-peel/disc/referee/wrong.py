# Referee: what plausible WRONG theories would have sealed, and whether each line (same tolerances, the measured values of study.out) would have failed.
import sys, math, os
sys.path.insert(0, '/home/agent2/disc-referee/addition/disc')
import numpy as np
import dtheory as th
import dlib
n = 10 ** 6
ALPHA, D, DC = th.ALPHA, th.D, th.DC
q = lambda n: (n / math.pi) ** (1 / 3)
def gm(m, r, nu=1 / 3.0):
    # mean square factor for smoothing nu/r: integral_r^1 (r/s)^(2 nu m^2) s^(-1/3) ds
    p = 2 * nu * m * m
    if abs(p - 2 / 3.0) < 1e-12: return r ** (2 / 3.0) * math.log(1 / r)
    return (r ** (2 / 3.0) - r ** p) / (p - 2 / 3.0)
def mode(m, r, n, d=D, nu=1 / 3.0): return d * q(n) / (2 * math.pi) * gm(m, r, nu)
def local(r, n, d=D, nu=1 / 3.0, M=200000):
    m = np.arange(1, M + 1, dtype=float); p = 2 * nu * m * m
    with np.errstate(divide='ignore', invalid='ignore'):
        g = np.where(np.abs(p - 2 / 3.0) < 1e-12, r ** (2 / 3.0) * math.log(1 / r), (r ** (2 / 3.0) - r ** p) / (p - 2 / 3.0))
    return 2 * d * q(n) / (2 * math.pi) * (g.sum() + r ** (2 / 3.0) / (2 * nu * M))
def level(r, n): return 0.65 * math.sqrt(0.75 * ALPHA * (n / math.pi) ** (2 / 3.0) * th.u(r))
def ring(kind, r, n, d=D, cut=True):
    f = th.cov_chance if (kind == 'chance' or not cut) else th.cov_fixed
    return th.annulus(f, r, r, n, d=d)
def corr(kind, r1, r2, n, d=D, cut=True):
    f = th.cov_chance if (kind == 'chance' or not cut) else th.cov_fixed
    return th.annulus(f, r1, r2, n, d=d) / math.sqrt(th.annulus(f, r1, r1, n, d=d) * th.annulus(f, r2, r2, n, d=d))
# measured values (study.out)
M = {'C1': [11.584, 8.923, 6.587, 4.479, 2.433], 'C2': [4.327, 3.535, 2.959, 2.420, 1.784], 'C3': 0.449, 'C4': (0.501, 0.151),
     'C5': [0.0651, 0.0659, 0.0671], 'C6': [23.98, 24.73, 22.03], 'C7': [5.02, 2.75, 1.35], 'C8': (1.226, 14.27), 'C9': (17.15, 5.74), 'C10': 0.0803, 'C11': 0.1808, 'C12': 11.41}
def within(meas, pred, tol): return abs(meas / pred - 1) <= tol
def judge(name, d=D, nu=1 / 3.0, cut=True, lvl=False, nodie=False, quarter=False):
    out = {}
    R5 = (0.2, 0.35, 0.5, 0.65, 0.8)
    fx = (lambda r: ring('exact', r, n, d, cut)) if not quarter else (lambda r: th.S(n) * (d - 0.75 * DC) * th.tau(r))
    out['C1'] = all(within(m, ring('chance', r, n, d), 0.15) for m, r in zip(M['C1'], R5))
    out['C2'] = all(within(m, fx(r), 0.25) for m, r in zip(M['C2'], R5))
    p3 = fx(0.5) / ring('chance', 0.5, n, d); out['C3'] = abs(M['C3'] - p3) <= 0.07     # the sheet's band is about +-0.07 round its prediction
    pc, pf = corr('chance', 0.8, 0.3, n, d), (corr('exact', 0.8, 0.3, n, d, cut) if not quarter else corr('chance', 0.8, 0.3, n, d))
    out['C4'] = (abs(M['C4'][0] - pc) <= 0.065) and (pf - 0.107 <= M['C4'][1] <= pf + 0.113)
    out['C5'] = all(within(m, ring('chance', 0.5, 10 ** 6, d) / 100.0, 0.20) for m in M['C5'])
    rv = (lambda r, nn: level(r, nn)) if lvl else ((lambda r, nn: float('inf')) if nodie else (lambda r, nn: local(r, nn, d, nu)))
    md = (lambda m, r: d * q(n) / (2 * math.pi) * 1.5 * (1 - r ** (2 / 3.0))) if nodie else (lambda m, r: mode(m, r, n, d, nu))
    out['C6'] = all(within(m, rv(r, n), 0.15) for m, r in zip(M['C6'], (0.3, 0.5, 0.7)))
    out['C7'] = all(within(m, md(k, 0.5), 0.20) for m, k in zip(M['C7'], (1, 2, 3)))
    out['C8'] = within(M['C8'][0], ring('chance', 0.9, n, d), 0.15) and within(M['C8'][1], rv(0.9, n), 0.15)
    out['C9'] = within(M['C9'][0], rv(0.1, n), 0.20) and within(M['C9'][1], md(1, 0.1), 0.25)
    p10 = th.S(1) * (d - (0.75 * DC if cut else 0)); out['C10'] = abs(M['C10'] / p10 - 1) <= 0.105
    p11 = th.S(1) * d; out['C11'] = abs(M['C11'] / p11 - 1) <= 0.10
    out['C12'] = within(M['C12'], rv(0.5, 10 ** 5), 0.15)
    failed = [k for k in ('C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12') if not out[k]]
    print('%-46s lines that would have FAILED: %s' % (name, ', '.join(failed) if failed else 'none'))
judge('the sheet\'s theory (control: none should fail)')
judge('no cut for a fixed number', cut=False)
judge('a quarter of the count\'s share left at every r', quarter=True)
judge('level law 0.65 sqrt(depth) round the ring', lvl=True)
judge('ripples that do not die', nodie=True)
for nu in (0.2, 0.25, 0.28, 0.30, 0.37, 0.40, 0.45, 0.5): judge('smoothing %.2f in place of 1/3' % nu, nu=nu)
for f in (0.8, 0.85, 0.9, 0.95, 1.05, 1.1, 1.15, 1.2): judge('noise D x %.2f' % f, d=D * f)
print('smoothing 0.40: parts 1,2,3 at r=0.5 over the sheet\'s: %s; ring variance at 0.3,0.5,0.7 over the sheet\'s: %s' % (
    ', '.join('%.3f' % (mode(m, 0.5, n, D, 0.4) / mode(m, 0.5, n)) for m in (1, 2, 3)), ', '.join('%.3f' % (local(r, n, D, 0.4) / local(r, n)) for r in (0.3, 0.5, 0.7))))
print('D x 1.1: exact-n ring mean predictions over the sheet\'s at 0.2, 0.5, 0.8: %s; with D = 1.095: %s; count of layers exact: %.4f -> %.4f' % (
    ', '.join('%.3f' % (ring('exact', r, n, D * 1.1) / ring('exact', r, n)) for r in (0.2, 0.5, 0.8)), ', '.join('%.3f' % (ring('exact', r, n, 1.095) / ring('exact', r, n)) for r in (0.2, 0.5, 0.8)), th.S(1) * (D - 0.75 * DC), th.S(1) * (1.095 - 0.75 * DC)))
# honest errors for the 13-annuli mean of 'round the ring' at 10^7 and the kinds' difference; bootstrap over clouds
rng = np.random.default_rng(5)
for nn in (10 ** 5, 10 ** 6, 10 ** 7):
    res = {}
    for kind in ('chance', 'exact'):
        d = dlib.load(kind, nn); ks = [dlib.K(0.2 + 0.05 * i) for i in range(13)]
        pred = np.array([th.local(dlib.RAD[k], nn) for k in ks]); V = d['V'][:, ks]; Kc = d['clouds']
        est = (V.mean(axis=0) / pred).mean(); bs = [(V[rng.integers(0, Kc, Kc)].mean(axis=0) / pred).mean() for _ in range(400)]
        Q = d['Q'][:, ks]; pq = np.array([dlib.pred_ring(kind, dlib.RAD[k], nn) for k in ks])
        eq = (Q.var(axis=0, ddof=1) / pq).mean(); bq = [(Q[rng.integers(0, Kc, Kc)].var(axis=0, ddof=1) / pq).mean() for _ in range(400)]
        res[kind] = (est, np.std(bs))
        print('n=%d %-6s clouds %d distinct seeds %d sd of points %.1f | round the ring, 13 annuli: %.3f (bootstrap %.3f) abs shortfall at r=0.5: %.3f | ring mean 13 annuli: %.3f (bootstrap %.3f)' % (
            nn, kind, Kc, len(set(d['seeds'])), d['npts'].std(ddof=1), est, np.std(bs), th.local(0.5, nn) - d['V'][:, dlib.K(0.5)].mean(), eq, np.std(bq)))
    print('   chance minus exact, round the ring: %+.3f (%.3f)' % (res['chance'][0] - res['exact'][0], math.hypot(res['chance'][1], res['exact'][1])))
