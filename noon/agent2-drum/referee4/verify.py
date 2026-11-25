import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from rsolve import Drum, slp, exact_miss, exact_freqs, MODES, TARG
from scipy.optimize import minimize_scalar
HERE = os.path.dirname(os.path.abspath(__file__))
D = '/home/agent2/drum/'
E40 = np.linspace(0, 1, 41)
W40 = E40[1:] ** 2 - E40[:-1] ** 2
cents = lambda r: 1200 * np.log2(r / TARG)


def show(label, edges, a, auth=None):
    edges = np.asarray(edges, float); a = np.asarray(a, float)
    em, r, fv, ex = exact_miss(edges, a)
    c = cents(r)
    mass = float((a * (edges[1:] ** 2 - edges[:-1] ** 2)).sum())
    print('%-46s mass %.4f  exact miss %.4f%%  max|cents| %.2f  max|ln| %.4f%%%s' % (label, mass, 100 * em, np.abs(c[1:]).max(), 100 * np.abs(np.log(r[1:] / TARG[1:])).max(), ('  [author: %s]' % auth) if auth else ''))
    return em, r, c


print('--- one even disc at 1.43 skins, radius refitted (exact matching)')
def disc(k, M=1.43):
    return exact_miss([0, k, 1], [M / k ** 2, 0])[0]
res = minimize_scalar(disc, bounds=(0.36, 0.44), method='bounded', options=dict(xatol=1e-6))
print('   best radius %.4f load %.3f miss %.4f%%   [author 3.188%% at 0.400, 9.95]' % (res.x, 1.43 / res.x ** 2, 100 * res.fun))
res2 = minimize_scalar(lambda k: disc(k, 1.433), bounds=(0.36, 0.44), method='bounded', options=dict(xatol=1e-6))
print('   at 1.433 skins: radius %.4f miss %.4f%%' % (res2.x, 100 * res2.fun))
d143 = res.fun

print('--- the three-piece load as quoted in the README (rounded figures)')
show('README: +10.4<0.126, +47.0 .152-.176, +13.7 .253-.360', [0, .126, .152, .176, .253, .360, 1], [10.4, 0, 47.0, 0, 13.7, 0], '0.77% / 0.7687% exact')
for wt in ('1.43', '2.79', '12'):
    p = json.load(open(D + 'pieces2-%s.json' % wt))
    R = p['radii']; L = p['loads']
    show('pieces2-%s.json (full precision)' % wt, [0] + R + [1], [L[0], 0, L[1], 0, L[2], 0], 'miss4000 %.4f%%' % (100 * p['miss4000']))

print('--- 40-ring loads: author (chain-free-up.json) and mine (blind), exact matching, sealed measure')
up = json.load(open(D + 'chain-free-up.json')); dn = json.load(open(D + 'chain-free-down.json'))
pu = json.load(open(D + 'chain-piled-up.json'))
get = lambda d, w: [r for r in d if abs(r['weight'] - w) < 1e-9][0]
for wt in (1.43, 2.79, 12.0):
    row = get(up, wt)
    em, r, c = show('author free %g' % wt, E40, row['a'], 'FD2000 %.4f%%' % (100 * row['miss']))
    if wt in (1.43, 12.0):
        print('     ratios', np.round(r, 4), ' cents', np.round(c[1:], 1))
        print('     pairs apart: (2,1)-(0,2) %.1f c, (3,1)-(1,2) %.1f c, span of the three at 5: %.1f c' % (abs(c[2] - c[3]), abs(c[4] - c[5]), c[6:9].max() - c[6:9].min()))
        a = np.array(row['a']); thr = 0.03 * a.max()
        print('     rings over 3%% of heaviest: %s ; outermost ring with any load >1e-6: ends at %.3f' % (np.nonzero(a > thr)[0].tolist(), E40[np.nonzero(a > 1e-6)[0].max() + 1]))
show('author free 12 (walk down)', E40, get(dn, 12.0)['a'], 'FD2000 %.4f%%' % (100 * get(dn, 12.0)['miss']))
show('author piled 12', E40, get(pu, 12.0)['a'], 'FD2000 %.4f%%' % (100 * get(pu, 12.0)['miss']))
show('author piled 1.43', E40, get(pu, 1.43)['a'], 'FD2000 %.4f%%' % (100 * get(pu, 1.43)['miss']))
for t in ('f143', 'f12', 'm12'):
    b = json.load(open(os.path.join(HERE, 'blind_%s.json' % t)))
    show('MINE 40 rings ' + t, E40, b['a'])
for t in ('f143_80', 'f12_80', 'm12_80'):
    fn = os.path.join(HERE, 'ctrl_%s.json' % t)
    if os.path.exists(fn):
        b = json.load(open(fn))
        em, r, c = show('MINE 80 rings ' + t, np.linspace(0, 1, 81), b['a'])
        a = np.array(b['a']); print('     a per 80th:', np.round(a[:40], 1).tolist(), ' nondecreasing-violations:', int((np.diff(a) > 1e-9).sum()))
print('--- "four times closer": disc(1.43) / free(1.43): author exact %.2f ; with my 40-ring load %.2f' % (d143 / 0.007703, d143 / json.load(open(os.path.join(HERE, 'blind_f143.json')))['miss_exact']))
