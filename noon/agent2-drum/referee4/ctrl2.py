import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from scipy.linalg import eigh_tridiagonal
from scipy.optimize import minimize
from rsolve import Drum, slp, exact_miss, MODES, TARG
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'blind.py')).read()
exec(src[src.index('def polish'):src.index('M = float')])
D = '/home/agent2/drum/'
E40 = np.linspace(0, 1, 41); W40 = E40[1:] ** 2 - E40[:-1] ** 2
mine = np.array(json.load(open(os.path.join(HERE, 'blind_f143.json')))['a'])
mine12 = np.array(json.load(open(os.path.join(HERE, 'blind_f12.json')))['a'])
up = json.load(open(D + 'chain-free-up.json'))
auth = np.array([r for r in up if abs(r['weight'] - 1.43) < 1e-9][0]['a'])
which = sys.argv[1]


def best(dr, a0, M, mono=False):
    a, f = slp(dr, a0 * dr.w, M, mono=mono, maxit=120)
    a, f = polish(dr, a, M, mono)
    a, f = slp(dr, a * dr.w, M, mono=mono, maxit=80)
    return a, f


if which == 'weights':
    print('--- free 40-ring load near the disc weight (continuation from my 1.43 answer; exact matching)')
    dr = Drum(E40, 20)
    a = mine.copy()
    for M in (1.43, 1.433, 1.46, 1.50, 1.60):
        a, f = best(dr, a * M / (a * W40).sum(), M)
        print('   mass allowed %.3f : miss %.4f%% exact (mass used %.4f)' % (M, 100 * exact_miss(E40, a)[0], (a * W40).sum()), flush=True)
    a = mine.copy()
    for M in (1.40, 1.36):
        a, f = best(dr, a * M / (a * W40).sum(), M)
        print('   mass allowed %.3f : miss %.4f%% exact (mass used %.4f)' % (M, 100 * exact_miss(E40, a)[0], (a * W40).sum()), flush=True)

if which == 'floor':
    print('--- control: no bare skin inside the patch (every ring inside r<0.375, resp. 0.4, carries at least `floor`)')

    class DrumB(Drum):
        base = None
        def lams(self, a, grad=False):
            return Drum.lams(self, np.asarray(a, float) + self.base, grad)
    for M, opt, rin, floors in ((1.43, mine, 15, (0.5, 1.0, 3.0)), (12.0, mine12, 16, (10.0,))):
        for fl in floors:
            dr = DrumB(E40, 10)
            base = np.zeros(40); base[:rin] = fl
            dr.base = base
            Meff = M - (base * W40).sum()
            res = []
            mid = 0.5 * (E40[1:] + E40[:-1])
            for name, a0 in (('from optimum', np.clip(opt - base, 0, None)), ('from disc 0.4', np.where(mid < 0.4, 1.0, 0) * 0.5)):
                a0 = a0 * min(1, Meff / max((a0 * W40).sum(), 1e-12))
                a, f = best(dr, a0, Meff)
                res.append((exact_miss(E40, a + base)[0], name, a + base))
            res.sort(key=lambda z: z[0])
            print('   %.2f skins, floor %+.1f inside %.3f: least miss %.4f%% exact (%s); other start %.4f%%' % (M, fl, E40[rin], 100 * res[0][0], res[0][1], 100 * res[1][0]))
            print('      load:', np.round(res[0][2][:18], 1).tolist(), flush=True)

if which == 'misc':
    print('--- rounding of the README three-piece load (exact matching)')
    p = json.load(open(D + 'pieces2-1.43.json')); R = np.array(p['radii']); L = np.array(p['loads'])
    ev = lambda R, L: exact_miss(np.concatenate([[0], R, [1]]), [L[0], 0, L[1], 0, L[2], 0])[0]
    print('   full precision %.4f%% | radii to 3 d.p., loads full %.4f%% | radii full, loads to 1 d.p. %.4f%% | both rounded %.4f%%' % (100 * ev(R, L), 100 * ev(np.round(R, 3), L), 100 * ev(R, np.round(L, 1)), 100 * ev(np.round(R, 3), np.round(L, 1))))
    for i in range(5):
        for dlt in (0.001, -0.001):
            R2 = R.copy(); R2[i] += dlt
            print('   edge %d moved %+.3f: %.4f%%' % (i + 1, dlt, 100 * ev(R2, L)), end=' ;')
    print()
    print('--- the next three modes for the author 1.43 load, (5,1),(3,2),(1,3), 4000 cells')
    dr = Drum(E40, 100)
    rho = 1 + auth[dr.ring]; Dm = dr.r * rho * dr.hc; sD = np.sqrt(Dm); e = dr.off / (sD[:-1] * sD[1:])
    def lam(m, n):
        d = (dr.d0 + m * m * dr.hc / dr.r) / Dm
        return eigh_tridiagonal(d, e, eigvals_only=True, select='i', select_range=(0, n - 1))[n - 1]
    l0 = lam(0, 1)
    allm = sorted([(np.sqrt(lam(m, n) / l0), (m, n)) for m in range(0, 9) for n in range(1, 5)])
    print('   ', [(round(r, 3), k) for r, k in allm if r < 6.7])
