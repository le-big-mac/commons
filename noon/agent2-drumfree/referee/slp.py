"""SLP polish of a ring load (minimax), FEM values+gradients, exact check at the end.
usage: slp.py <json with key a | best.json:key> <withlow 0/1> <mass> [N] [iters] [targets: five|seven|leave:<m>,<n>]"""
import sys, json
sys.path.insert(0, "/home/agent2/drumfree/referee")
import numpy as np
from scipy.optimize import linprog
from sol import *

NEED7 = {0: 4, 1: 3, 2: 3, 3: 2, 4: 2, 5: 1, 6: 1}


def setup(K, N, targets, need):
    fem = Fem(N); p = N // K

    def ev(a):
        f, G = fem_freqs(fem, np.repeat(1 + a, p), need, grad=True)
        note = f[(1, 1)] / 2
        gn = G[(1, 1)].reshape(K, p).sum(1) / 2
        ms = np.array([f[k] / (t * note) - 1 for k, t in targets])
        J = np.array([G[k].reshape(K, p).sum(1) / (t * note) - f[k] / (t * note ** 2) * gn for k, t in targets])
        return ms, J
    return ev


def polish(a, targets, need, mass, N=1600, iters=200, tr=1.0, verbose=False):
    K = len(a)
    edges = np.arange(1, K + 1) / K
    wts = edges ** 2 - np.concatenate([[0], edges[:-1]]) ** 2
    ev = setup(K, N, targets, need)
    a = np.array(a, float)
    ms, J = ev(a); cur = np.abs(ms).max()
    nt = len(targets)
    for it in range(iters):
        # vars: da (K), t
        c = np.concatenate([np.zeros(K), [1.0]])
        A = np.vstack([np.hstack([J, -np.ones((nt, 1))]), np.hstack([-J, -np.ones((nt, 1))]),
                       np.concatenate([wts, [0]])[None, :]])
        b = np.concatenate([-ms, ms, [mass - wts @ a]])
        bounds = [(max(-a[i], -tr * max(1.0, a[i])), tr * max(1.0, a[i])) for i in range(K)] + [(0, None)]
        r = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='highs')
        if r.status != 0:
            tr *= 0.5; continue
        a2 = np.clip(a + r.x[:K], 0, None)
        ms2, J2 = ev(a2); new = np.abs(ms2).max()
        if new < cur - 1e-12:
            a, ms, J, cur = a2, ms2, J2, new
            tr = min(tr * 1.5, 2.0)
        else:
            tr *= 0.4
            if tr < 1e-7:
                break
        if verbose and it % 20 == 0:
            print(it, '%.5f%%' % (100 * cur), tr, flush=True)
    return a, cur


def exact_eval(a, targets, need):
    K = len(a)
    f = exact_freqs(np.arange(1, K + 1) / K, 1 + np.asarray(a), need)
    note = f[(1, 1)] / 2
    ms = np.array([f[k] / (t * note) - 1 for k, t in targets])
    return np.abs(ms).max(), f[(0, 1)] / note, ms


if __name__ == '__main__':
    src, wl, mass = sys.argv[1], int(sys.argv[2]), float(sys.argv[3])
    N = int(sys.argv[4]) if len(sys.argv) > 4 else 1600
    iters = int(sys.argv[5]) if len(sys.argv) > 5 else 200
    tg = sys.argv[6] if len(sys.argv) > 6 else 'five'
    if ':' in src:
        fn, key = src.split(':', 1)
        a = json.load(open(fn))[key]['a']
    else:
        a = json.load(open(src))['a']
    targets = list(SEVEN); need = dict(NEED)
    if tg == 'seven':
        targets += EXTRA7; need = NEED7
    if wl:
        targets.append(((0, 1), 1))
    e0, p0, _ = exact_eval(a, targets, need)
    print('start: exact miss %.4f%% place %.4f' % (100 * e0, p0))
    a2, cur = polish(a, targets, need, mass, N, iters, verbose=True)
    e1, p1, ms = exact_eval(a2, targets, need)
    K = len(a2); edges = np.arange(1, K + 1) / K
    wts = edges ** 2 - np.concatenate([[0], edges[:-1]]) ** 2
    print('end: fem %.4f%% exact miss %.4f%% place %.4f mass %.4f' % (100 * cur, 100 * e1, p1, wts @ a2))
    print('load:', ' '.join('%.2f' % x for x in a2))
    json.dump({'a': a2.tolist(), 'miss': e1, 'place': p1}, open(sys.argv[7] if len(sys.argv) > 7 else 'slp_out.json', 'w'))
