import sys, glob, math
import numpy as np
alpha, D = 1.3259, 1.081
RR = [0.2, 0.3, 0.5, 0.7, 0.8]

def pred(n):
    q = (n / math.pi) ** (1 / 3)
    VP = lambda r: 3 * D * q * (1 - r ** (2 / 3)) / (4 * math.pi)
    g = lambda r: alpha * math.sqrt(q / (4 * math.pi)) * (1 - r ** (4 / 3))
    VF = lambda r: VP(r) - g(r) ** 2
    def cP(r1, r2):
        return VP(max(r1, r2)) / math.sqrt(VP(r1) * VP(r2))
    def cF(r1, r2):
        return (VP(max(r1, r2)) - g(r1) * g(r2)) / math.sqrt(VF(r1) * VF(r2))
    def Pm(m, r):
        if m == 1:
            return D * q / (2 * math.pi) * r ** (2 / 3) * math.log(1 / r)
        return D * q / (2 * math.pi) * 3 * (r ** (2 / 3) - r ** (2 * m * m / 3)) / (2 * (m * m - 1))
    def ring(r, mmax=200000):
        s = 2 * Pm(1, r)
        # tail summed exactly: sum_{m>=2} 1/(m^2-1) = 3/4
        s += D * q / math.pi * 1.5 * (0.75 * r ** (2 / 3) - sum(r ** (2 * m * m / 3) / (m * m - 1) for m in range(2, 400)))
        return s
    def ringcut(r, mc):
        return sum(2 * Pm(m, r) for m in range(1, int(mc) + 1))
    return VP, VF, cP, cF, Pm, ring, ringcut, q

def boot(f, K, B=1000, seed=1):
    rg = np.random.default_rng(seed)   # PCG64
    v = [f(rg.integers(0, K, K)) for _ in range(B)]
    return np.std(v)

if len(sys.argv) > 1 and sys.argv[1] == 'pred':
    n = float(sys.argv[2])
    VP, VF, cP, cF, Pm, ring, ringcut, q = pred(n)
    print('n', n, 'rho^(1/3)', q, 'A', 0.75 * alpha * q * q)
    for r in [0.2, 0.5, 0.8]:
        print('r', r, 'VarPoisson', VP(r), 'VarFixed', VF(r))
    print('corr(0.8,0.3) Poisson', cP(0.8, 0.3), 'fixed', cF(0.8, 0.3))
    for m in [1, 2, 3]:
        print('m', m, 'r=0.5 E(c2+s2)/4', Pm(m, 0.5))
    for r in [0.3, 0.5, 0.7]:
        a = (r * math.pi / n) ** (1 / 3)
        print('r', r, 'ring var all m', ring(r), ' cut at m=r/a', ringcut(r, r / a), ' cut at m=pi r/a', ringcut(r, math.pi * r / a))
    print('layers var Poisson', VP(0), 'fixed', VF(0))
    sys.exit()

n = int(sys.argv[1])
VP, VF, cP, cF, Pm, ring, ringcut, q = pred(n)
for kind, name in [(1, 'POISSON'), (0, 'FIXED')]:
    fs = sorted(glob.glob('/home/agent2/disc-referee/out_%d_%d_*.txt' % (n, kind)))
    X = np.concatenate([np.loadtxt(f, ndmin=2) for f in fs])
    K = len(X)
    print('==== n=%d %s clouds=%d files=%d  mean N=%.1f sd N=%.1f  mean layers=%.2f (A=%.2f)' % (n, name, K, len(fs), X[:, 0].mean(), X[:, 0].std(ddof=1), X[:, 1].mean(), 0.75 * alpha * q * q))
    M = {r: X[:, 2 + 9 * i + 1] for i, r in enumerate(RR)}
    V = {r: X[:, 2 + 9 * i + 2] for i, r in enumerate(RR)}
    C = {r: X[:, 2 + 9 * i + 3: 2 + 9 * i + 9] for i, r in enumerate(RR)}
    NP = {r: X[:, 2 + 9 * i] for i, r in enumerate(RR)}
    P = VP if kind == 1 else VF
    print(' ring-mean depth residual: variance across clouds')
    for r in RR:
        v = M[r].var(ddof=1); e = boot(lambda ix: M[r][ix].var(ddof=1), K)
        line = '  r=%.1f  mean=%+.3f  var=%.3f +- %.3f   predicted %.3f   ratio %.3f +- %.3f  (z=%+.1f)' % (r, M[r].mean(), v, e, P(r), v / P(r), e / P(r), (v - P(r)) / e)
        if kind == 1:
            dn = X[:, 0] - n
            b = np.cov(M[r], dn)[0, 1] / dn.var(ddof=1)
            res = M[r] - b * dn
            line += '  | slope on N: %.5f (pred %.5f); var after removing N: %.3f (pred fixed %.3f)' % (b, (2 / 3) * 0.75 * alpha * q * q * (1 - r ** (4 / 3)) / n, res.var(ddof=1), VF(r))
        print(line)
    c = np.corrcoef(M[0.8], M[0.3])[0, 1]
    e = boot(lambda ix: np.corrcoef(M[0.8][ix], M[0.3][ix])[0, 1], K)
    pc = cP(0.8, 0.3) if kind == 1 else cF(0.8, 0.3)
    print(' corr(M(0.8),M(0.3)) = %.3f +- %.3f   predicted %.3f (z=%+.1f)' % (c, e, pc, (c - pc) / e))
    for (r1, r2) in [(0.8, 0.5), (0.5, 0.2), (0.7, 0.3), (0.8, 0.2)]:
        c = np.corrcoef(M[r1], M[r2])[0, 1]
        pc = cP(r1, r2) if kind == 1 else cF(r1, r2)
        print('   extra corr(%.1f,%.1f) = %.3f   predicted %.3f' % (r1, r2, c, pc))
    print(' modes: mean over clouds of (c^2+s^2)/4')
    for r in RR:
        for m in [1, 2, 3]:
            p = (C[r][:, 2 * m - 2] ** 2 + C[r][:, 2 * m - 1] ** 2) / 4
            noise = V[r].mean() / NP[r].mean()
            print('  r=%.1f m=%d  %.3f +- %.3f  predicted %.3f  ratio %.3f +- %.3f (z=%+.1f) [sampling bias ~%.3f not removed]' % (r, m, p.mean(), p.std(ddof=1) / math.sqrt(K), Pm(m, r), p.mean() / Pm(m, r), p.std(ddof=1) / math.sqrt(K) / Pm(m, r), (p.mean() - Pm(m, r)) / (p.std(ddof=1) / math.sqrt(K)), noise))
    print(' variance round the ring about fitted line (mean over clouds)')
    for r in RR:
        a = (r * math.pi / n) ** (1 / 3)
        v = V[r].mean(); e = V[r].std(ddof=1) / math.sqrt(K)
        print('  r=%.1f  %.3f +- %.3f  predicted (all m) %.3f  ratio %.3f +- %.3f ; cut m<=r/a: %.3f ; cut m<=pi r/a: %.3f ; points in annulus %.0f' % (r, v, e, ring(r), v / ring(r), e / ring(r), ringcut(r, r / a), ringcut(r, math.pi * r / a), NP[r].mean()))
    L = X[:, 1]
    v = L.var(ddof=1); e = boot(lambda ix: L[ix].var(ddof=1), K)
    print(' layers: mean %.2f  var %.3f +- %.3f  predicted %.3f  ratio %.3f +- %.3f (z=%+.1f)' % (L.mean(), v, e, P(0), v / P(0), e / P(0), (v - P(0)) / e))
    if kind == 1:
        dn = X[:, 0] - n
        b = np.cov(L, dn)[0, 1] / dn.var(ddof=1)
        print('   layers slope on N %.5f (pred %.5f); var after removing N %.3f (pred fixed %.3f)' % (b, (2 / 3) * 0.75 * alpha * q * q / n, (L - b * dn).var(ddof=1), VF(0)))
