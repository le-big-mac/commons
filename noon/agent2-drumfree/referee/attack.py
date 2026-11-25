"""Referee's attacks on the ring figures. usage:
 attack.py verify                       -- recompute best.json headline loads and the two discs by my exact matching
 attack.py search <tag> <note: half11|low> <fam: five|seven> <leave: none|m,n> <withlow 0/1> <mass> <nstarts> <seed0> [startfile:key]
"""
import sys, json, time
sys.path.insert(0, "/home/agent2/drumfree/referee")
import numpy as np
from scipy.optimize import minimize, linprog
from sol import *

NEED7 = {0: 4, 1: 3, 2: 3, 3: 2, 4: 2, 5: 1, 6: 1}


def make(K, N, targets, need, nm, div):
    fem = Fem(N); p = N // K
    cache = {}

    def ev(a):
        key = a.tobytes()
        if key in cache:
            return cache[key]
        f, G = fem_freqs(fem, np.repeat(1 + a, p), need, grad=True)
        note = f[nm] / div
        gn = G[nm].reshape(K, p).sum(1) / div
        ms = np.array([f[k] / (t * note) - 1 for k, t in targets])
        J = np.array([G[k].reshape(K, p).sum(1) / (t * note) - f[k] / (t * note ** 2) * gn for k, t in targets])
        cache.clear(); cache[key] = (ms, J)
        return ms, J
    return ev


def slsqp(ev, a0, wts, mass, nt):
    K = len(a0)
    x0 = np.concatenate([a0, [np.abs(ev(a0)[0]).max()]])
    one = np.ones((nt, 1))
    cons = [
        {'type': 'ineq', 'fun': lambda x: x[-1] - ev(x[:-1])[0], 'jac': lambda x: np.hstack([-ev(x[:-1])[1], one])},
        {'type': 'ineq', 'fun': lambda x: x[-1] + ev(x[:-1])[0], 'jac': lambda x: np.hstack([ev(x[:-1])[1], one])},
        {'type': 'ineq', 'fun': lambda x: mass - wts @ x[:-1], 'jac': lambda x: np.concatenate([-wts, [0]])},
    ]
    r = minimize(lambda x: x[-1], x0, jac=lambda x: np.concatenate([np.zeros(K), [1.0]]),
                 bounds=[(0, 400)] * K + [(0, None)], constraints=cons, method='SLSQP',
                 options={'maxiter': 500, 'ftol': 1e-10})
    a = np.clip(r.x[:-1], 0, None)
    return a, np.abs(ev(a)[0]).max()


def slp(ev, a, wts, mass, nt, iters=150, tr=1.0):
    K = len(a)
    a = np.array(a, float)
    ms, J = ev(a); cur = np.abs(ms).max()
    for it in range(iters):
        c = np.concatenate([np.zeros(K), [1.0]])
        A = np.vstack([np.hstack([J, -np.ones((nt, 1))]), np.hstack([-J, -np.ones((nt, 1))]),
                       np.concatenate([wts, [0]])[None, :]])
        b = np.concatenate([-ms, ms, [mass - wts @ a]])
        bounds = [(max(-a[i], -tr * max(1.0, a[i])), tr * max(1.0, a[i])) for i in range(K)] + [(0, None)]
        r = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='highs')
        if r.status != 0:
            tr *= 0.5
            if tr < 1e-7:
                break
            continue
        a2 = np.clip(a + r.x[:K], 0, None)
        ms2, J2 = ev(a2); new = np.abs(ms2).max()
        if new < cur - 1e-12:
            a, ms, J, cur = a2, ms2, J2, new
            tr = min(tr * 1.5, 2.0)
        else:
            tr *= 0.4
            if tr < 1e-7:
                break
    return a, cur


def exact_eval(a, targets, need, nm, div):
    K = len(a)
    f = exact_freqs(np.arange(1, K + 1) / K, 1 + np.asarray(a), need)
    note = f[nm] / div
    ms = np.array([f[k] / (t * note) - 1 for k, t in targets])
    return np.abs(ms).max(), f[(0, 1)] / (f[(1, 1)] / 2), ms


if __name__ == '__main__':
    if sys.argv[1] == 'verify':
        B = json.load(open('/home/agent2/drumfree/best.json'))
        for key in sys.argv[2:]:
            fam, mass, K = key.split('|')
            a = np.array(B[key]['a'])
            targets = list(SEVEN) + (EXTRA7 if fam == 'seven' else [])
            need = NEED7 if fam == 'seven' else NEED
            e, pl, ms = exact_eval(a, targets, need, (1, 1), 2)
            K = len(a); edges = np.arange(1, K + 1) / K
            wts = edges ** 2 - np.concatenate([[0], edges[:-1]]) ** 2
            print('%-14s author exact %.5f%% place %.4f | mine %.5f%% place %.4f | mass %.4f min a %.3g max a %.1f at ring %d' % (
                key, 100 * B[key]['exact'], B[key]['place'], 100 * e, pl, wts @ a, a.min(), a.max(), a.argmax()))
        for nm_, edges, rho in [('two discs full digits', [0.2768, 0.4933, 1.0], [8.120, 6.304, 1.0]),
                                ('two discs as in summary', [0.277, 0.493, 1.0], [8.1, 6.3, 1.0]),
                                ('one disc 4.343/0.5042', [0.5042, 1.0], [4.343, 1.0]),
                                ('makers edge 6.25/0.527', [0.5266, 1.0], [6.25, 1.0]),
                                ('1954 disc 9.77/0.4', [0.4, 1.0], [9.77, 1.0])]:
            f = exact_freqs(edges, rho)
            ms, pl = misses(f)
            mass = sum((r_ - 1) * (e_ ** 2 - e0 ** 2) for r_, e_, e0 in zip(rho, edges, [0] + edges[:-1]))
            print('%-24s miss %.4f%% place %.4f added mass %.4f' % (nm_, 100 * np.abs(ms).max(), pl, mass))
        sys.exit()
    tag, note, fam, leave, wl, mass, ns, seed0 = sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], int(sys.argv[6]), float(sys.argv[7]), int(sys.argv[8]), int(sys.argv[9])
    K = 40
    targets = list(SEVEN) + (EXTRA7 if fam == 'seven' else [])
    need = NEED7 if fam == 'seven' else NEED
    if note == 'low':
        nm, div = (0, 1), 1
        targets = [((1, 1), 2)] + targets
    else:
        nm, div = (1, 1), 2
        if wl:
            targets = targets + [((0, 1), 1)]
    if leave != 'none':
        lm = tuple(int(x) for x in leave.split(','))
        targets = [x for x in targets if x[0] != lm]
    nt = len(targets)
    edges = np.arange(1, K + 1) / K
    wts = edges ** 2 - np.concatenate([[0], edges[:-1]]) ** 2
    ev4 = make(K, 400, targets, need, nm, div)
    ev16 = make(K, 1600, targets, need, nm, div)
    res = []
    t0 = time.time()
    starts = []
    if len(sys.argv) > 10:
        fn, key = sys.argv[10].split(':', 1)
        starts.append(np.array(json.load(open(fn))[key]['a']))
    for s in range(seed0, seed0 + ns):
        rng = np.random.default_rng(s)
        kind = s % 4
        if kind == 0:
            a0 = np.where(edges <= rng.uniform(0.25, 0.6), rng.uniform(3, 12), 0.0)
        elif kind == 1:
            c, wd = rng.uniform(0, 0.6), rng.uniform(0.1, 0.4)
            a0 = rng.uniform(2, 10) * np.exp(-((edges - c) / wd) ** 2)
        elif kind == 2:
            a0 = rng.uniform(0, 6, K) * (edges < rng.uniform(0.4, 0.9))
        else:
            a0 = rng.uniform(0, 3, K)
        m0 = wts @ a0
        if m0 > mass:
            a0 *= mass / m0 * 0.95
        try:
            a, v = slsqp(ev4, a0, wts, mass, nt)
            res.append((v, a))
        except Exception as e:
            pass
    res.sort(key=lambda x: x[0])
    cands = [x[1] for x in res[:3]] + starts
    out = []
    for a in cands:
        a2, v = slp(ev16, a, wts, mass, nt)
        try:
            e, pl, ms = exact_eval(a2, targets, need, nm, div)
        except Exception as ex:
            continue
        out.append((e, pl, a2))
    out.sort(key=lambda x: x[0])
    e, pl, a = out[0]
    print('%s note=%s fam=%s leave=%s withlow=%d mass=%g: least exact %.4f%% place %.4f (polished: %s) raw SLSQP best %.4f%% n=%d  %.0fs' % (
        tag, note, fam, leave, wl, mass, 100 * e, pl, ' '.join('%.4f' % (100 * x[0]) for x in out), 100 * res[0][0] if res else -1, len(res), time.time() - t0), flush=True)
    json.dump({'a': a.tolist(), 'miss': e, 'place': pl}, open('att_%s.json' % tag, 'w'))
