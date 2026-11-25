import glob, math
import numpy as np
alpha, D = 1.3259, 1.081
n = 100000; q = (n / math.pi) ** (1 / 3); A = 0.75 * alpha * q * q
RR = [0.3, 0.5, 0.7]; HW = [0.004, 0.008, 0.016]
def g(m, r):
    if m == 1: return r ** (2 / 3) * math.log(1 / r)
    return 1.5 * (r ** (2 / 3) - r ** (2 * m * m / 3)) / (m * m - 1)
def mode(m, r): return D * q / (2 * math.pi) * g(m, r)
X = np.concatenate([np.loadtxt(f, ndmin=2) for f in sorted(glob.glob('/home/agent2/disc-referee/p2_*.txt'))]); K = len(X)
print('clouds', K, 'exactly n = 100000')
se = lambda v: v.std(ddof=1) / math.sqrt(len(v))
tot = {}
for a, r in enumerate(RR):
    for w, h in enumerate(HW):
        B = X[:, (a * 3 + w) * 19:(a * 3 + w + 1) * 19]
        Np, vraw, ve = B[:, 0], B[:, 1], B[:, 2]
        det = B[:, 3:11]; raw = B[:, 11:19]; smp = raw - det
        G = A * (4 / 3) * r ** (1 / 3)
        atrend = G * G * h * h / 3 / Np.mean()
        addition = (vraw / Np).mean()            # what the page takes off
        avg = D * q * r ** (-1 / 3) / (2 * math.pi) * h / 3     # annulus averaging, the same amount as for the ring's mean
        print('r=%.1f half-width %.3f: points %.0f; page\'s "addition" (whole variance / points) %.4f, of which slope part %.4f; averaging loss predicted %.4f' % (r, h, Np.mean(), addition, atrend, avg))
        for m in (1, 2, 3, 4):
            cd, sd, cs, ss = det[:, 2 * m - 2], det[:, 2 * m - 1], smp[:, 2 * m - 2], smp[:, 2 * m - 1]
            Pdet = (cd ** 2 + sd ** 2) / 4; Praw = (raw[:, 2 * m - 2] ** 2 + raw[:, 2 * m - 1] ** 2) / 4
            S2 = (cs ** 2 + ss ** 2) / 4; cr = (cd * cs + sd * ss) / 2
            pm = mode(m, r)
            print('   m=%d pred %.3f | profile off first: %.4f (%.4f) | raw (sheet): %.4f | raw - detrended %+.4f (%.4f) = slope-sampling square %+.4f (%.4f) [expect %+.4f] + cross %+.4f (%.4f) [independent sampling: 0; my pencil: %+.4f]' % (
                m, pm, Pdet.mean(), se(Pdet), Praw.mean(), (Praw - Pdet).mean(), se(Praw - Pdet), S2.mean(), se(S2), atrend, cr.mean(), se(cr), -4 / 3 * atrend))
            tot.setdefault((w, 'cross'), []).append(cr / atrend); tot.setdefault((w, 'diff'), []).append((Praw - Pdet) / atrend)
            tot.setdefault((w, 'short'), []).append((Pdet - ve / Np - pm) / avg)
            tot.setdefault((w, 'rawshort'), []).append((Praw - pm))
print()
for w, h in enumerate(HW):
    c = np.mean(tot[(w, 'cross')], axis=0); d = np.mean(tot[(w, 'diff')], axis=0); s = np.mean(tot[(w, 'short')], axis=0)
    print('half-width %.3f, 3 radii x 4 parts pooled: cross term / slope part = %+.3f (%.3f) [independent sampling 0, my pencil -1.333];  (raw - detrended)/slope part = %+.3f (%.3f) [page +1, my pencil -0.333];  (detrended - its own sampling - predicted)/averaging loss = %+.2f (%.2f) [no averaging 0; averaging as for the mean -1]' % (
        h, c.mean(), se(c), d.mean(), se(d), s.mean(), se(s)))
# width trend on the same clouds, detrended with own sampling term off, pooled over radii, by m
for m in (1, 2, 3, 4):
    out = []
    for w, h in enumerate(HW):
        v = []
        for a, r in enumerate(RR):
            B = X[:, (a * 3 + w) * 19:(a * 3 + w + 1) * 19]; det = B[:, 3:11]
            v.append(((det[:, 2 * m - 2] ** 2 + det[:, 2 * m - 1] ** 2) / 4 - B[:, 2] / B[:, 0]) / mode(m, r))
        v = np.mean(v, axis=0); out.append('%.3f (%.3f)' % (v.mean(), se(v)))
    # paired narrow minus wide
    print('m=%d measured/predicted (profile off, own sampling off), half-width 0.004, 0.008, 0.016: %s' % (m, ', '.join(out)))
