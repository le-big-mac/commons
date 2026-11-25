"""Blind step. usage: blind.py plain | rings <seed0> <nstarts> <withlow 0/1> [K] [mass] | disc"""
import sys, json, time
import numpy as np
from scipy.optimize import minimize
sys.path.insert(0, "/home/agent2/drumfree/referee")
from sol import *


def ring_problem(K, N, mass, with_low, targets=SEVEN, need=NEED, leave=None):
    fem = Fem(N); p = N // K
    edges = np.arange(1, K + 1) / K
    wts = edges ** 2 - np.concatenate([[0], edges[:-1]]) ** 2
    cache = {}

    def ev(a):
        key = a.tobytes()
        if key in cache:
            return cache[key]
        rho_e = np.repeat(1 + a, p)
        f, G = fem_freqs(fem, rho_e, need, grad=True)
        note = f[(1, 1)] / 2
        gn = G[(1, 1)].reshape(K, p).sum(1) / 2
        ms = []; J = []
        tl = list(targets) + ([((0, 1), 1)] if with_low else [])
        for k, t in tl:
            ms.append(f[k] / (t * note) - 1)
            J.append(G[k].reshape(K, p).sum(1) / (t * note) - f[k] / (t * note ** 2) * gn)
        cache.clear(); cache[key] = (np.array(ms), np.array(J))
        return cache[key]

    def solve(a0):
        x0 = np.concatenate([a0, [np.abs(ev(a0)[0]).max()]])
        cons = [
            {'type': 'ineq', 'fun': lambda x: x[-1] - ev(x[:-1])[0], 'jac': lambda x: np.hstack([-ev(x[:-1])[1], np.ones((len(tl_n), 1))])},
            {'type': 'ineq', 'fun': lambda x: x[-1] + ev(x[:-1])[0], 'jac': lambda x: np.hstack([ev(x[:-1])[1], np.ones((len(tl_n), 1))])},
            {'type': 'ineq', 'fun': lambda x: mass - wts @ x[:-1], 'jac': lambda x: np.concatenate([-wts, [0]])},
        ]
        r = minimize(lambda x: x[-1], x0, jac=lambda x: np.concatenate([np.zeros(K), [1.0]]),
                     bounds=[(0, 400)] * K + [(0, None)], constraints=cons, method='SLSQP',
                     options={'maxiter': 600, 'ftol': 1e-10})
        a = np.clip(r.x[:-1], 0, None)
        return a, np.abs(ev(a)[0]).max()

    tl_n = list(targets) + ([((0, 1), 1)] if with_low else [])
    return solve, edges, wts


def exact_ring(a, with_low, targets=SEVEN, need=NEED):
    K = len(a)
    edges = np.arange(1, K + 1) / K
    f = exact_freqs(edges, 1 + np.asarray(a), need)
    ms, place = misses(f, targets, with_low)
    return np.abs(ms).max(), place, f


if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'plain':
        f = exact_freqs([1.0], [1.0])
        note = f[(1, 1)] / 2
        print('plain skin: lowest place %.5f' % (f[(0, 1)] / note))
        print('overtones/note:', ' '.join('%s %.4f' % (k, f[k] / note) for k, t in SEVEN))
        ms, _ = misses(f)
        print('overtone miss %.3f%%' % (100 * np.abs(ms).max()))
    elif mode == 'rings':
        seed0, ns, wl = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
        K = int(sys.argv[5]) if len(sys.argv) > 5 else 40
        mass = float(sys.argv[6]) if len(sys.argv) > 6 else 4.0
        solve, edges, wts = ring_problem(K, 400 if K in (20, 40) else K * 8, mass, wl)
        best = None
        for s in range(seed0, seed0 + ns):
            rng = np.random.default_rng(s)
            kind = s % 4
            if kind == 0:   # disc start
                a0 = np.where(edges <= rng.uniform(0.25, 0.6), rng.uniform(3, 12), 0.0)
            elif kind == 1:  # smooth bump
                c, wd = rng.uniform(0, 0.6), rng.uniform(0.1, 0.4)
                a0 = rng.uniform(2, 10) * np.exp(-((edges - c) / wd) ** 2)
            elif kind == 2:
                a0 = rng.uniform(0, 6, K) * (edges < rng.uniform(0.4, 0.9))
            else:
                a0 = rng.uniform(0, 3, K)
            m0 = wts @ a0
            if m0 > mass:
                a0 *= mass / m0 * 0.95
            t0 = time.time()
            try:
                a, v = solve(a0)
            except Exception as e:
                print('seed', s, 'failed', e); continue
            try:
                ex, place, _ = exact_ring(a, wl)
            except Exception as e:
                print('seed', s, 'exact failed', e); continue
            print('seed %d fem %.4f%% exact %.4f%% place %.4f mass %.3f  %.1fs' % (s, 100 * v, 100 * ex, place, wts @ a, time.time() - t0), flush=True)
            if best is None or ex < best[0]:
                best = (ex, place, a.tolist(), s)
        print('BEST withlow=%d K=%d mass<=%g: miss %.4f%% place %.4f seed %d' % (wl, K, mass, 100 * best[0], best[1], best[3]))
        print('load by ring (centre out):', ' '.join('%.2f' % x for x in best[2]))
        json.dump({'a': best[2], 'miss': best[0], 'place': best[1]}, open('blind_rings_%d_%d_%d.json' % (wl, K, seed0), 'w'))
    elif mode == 'disc':
        fem = Fem(400)
        res = []
        for s in np.arange(1, 60.01, 1.0):
            for k in np.arange(0.05, 0.9501, 0.01):
                f = fem_freqs(fem, rho_elements(fem, [k, 1.0], [s, 1.0]))
                ms, place = misses(f)
                res.append((np.abs(ms).max(), s, k, place))
        res.sort()
        print('disc grid (FEM N=400) five best:')
        for x in res[:5]:
            print('  miss %.3f%% s %.2f k %.3f place %.4f' % (100 * x[0], x[1], x[2], x[3]))

        def obj(x):
            s, k = x
            if not (1 <= s <= 60 and 0.05 <= k <= 0.95):
                return 1.0
            f = exact_freqs([k, 1.0], [s, 1.0], N=800)
            return np.abs(misses(f)[0]).max()
        seen = []
        for x in res[:40]:
            if all(abs(x[1] - y[1]) > 3 or abs(x[2] - y[2]) > 0.05 for y in seen):
                seen.append(x)
        for x in seen[:4]:
            r = minimize(obj, [x[1], x[2]], method='Nelder-Mead', options={'xatol': 1e-5, 'fatol': 1e-9})
            f = exact_freqs([r.x[1], 1.0], [r.x[0], 1.0])
            ms, place = misses(f)
            print('refined exact: miss %.4f%% s %.4f k %.4f place %.4f added mass %.3f' % (100 * r.fun, r.x[0], r.x[1], place, (r.x[0] - 1) * r.x[1] ** 2))
            print('   misses %:', ' '.join('%+.3f' % (100 * v) for v in ms))
