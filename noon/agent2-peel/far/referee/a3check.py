import glob, json, math, os, sys
import numpy as np
R = sys.argv[1]; THICK = 1.3259**2 / 12
def expo(y, v, lo, hi):
    m = (y >= lo) & (y <= hi); yy, vv = y[m], v[m]
    k = np.floor(16 * np.log2(yy / lo) + 1e-9).astype(int); xs = []; zs = []
    for j in sorted(set(k)): xs.append(math.log(yy[k == j].mean())); zs.append(math.log(vv[k == j].mean()))
    return float(np.polyfit(xs, zs, 1)[0])
W = []
for f in sorted(glob.glob(os.path.join(R, 'run-*.json'))):
    o = json.loads(open(f).read())
    if int(o['HM']) != 128000: continue
    a = np.loadtxt(f.replace('run-', 'profile-').replace('.json', '.txt') + '.gz')
    W.append({'seeding': o.get('seeding', 1), 'seed': o['seed'], 'c': a[:, 1], 'mu': a[:, 2], 'var': a[:, 3]})
def pooled(S, lo, hi):
    c = sum(w['c'] for w in S); v = sum(w['c'] * w['var'] for w in S) / c
    return expo(np.arange(len(v)) + 0.5, v - THICK, lo, hi)
for nm, S in (('first batch, 3 tall windows (the design when sheet 1 was sealed)', [w for w in W if w['seeding'] == 1]), ('second batch, 12 tall', [w for w in W if w['seeding'] == 2]), ('all 15 tall', W)):
    print(nm, len(S), 'windows: exponent 64000-128000 = %.3f; 32000-64000 = %.3f; 4000-128000 = %.3f' % (pooled(S, 64000, 128000), pooled(S, 32000, 64000), pooled(S, 4000, 128000)))
    if len(S) == 3: print('   one by one, 64000-128000:', ', '.join('%.3f' % pooled([w], 64000, 128000) for w in S))
