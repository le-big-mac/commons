"""Two missing numbers for the side-by-side table; and are the sheets byte-identical to a published file?"""
import json, hashlib, os, sys
import numpy as np
R = '/home/agent2/calib/'
out = json.load(open(R + 'outcomes.json')); items = json.load(open(R + 'items.json'))
ids = [it['id'] for it in items]; fil = np.array([it['file'] for it in items])
P = np.array([[{**json.load(open(R + f'f{k}/A.json')), **json.load(open(R + f'f{k}/B.json'))}[i]['p'] for k in range(1, 6)] for i in ids])
y = np.array([out[i] for i in ids]); fc = np.median(P, 1)
def auc(s, yy):
    a, b = s[yy == 1], s[yy == 0]
    return float(((a[:, None] > b[None, :]).sum() + .5 * (a[:, None] == b[None, :]).sum()) / (len(a) * len(b))) if len(a) and len(b) else float('nan')
yl = y.copy(); yl[ids.index('O2')] = 0; yl[ids.index('O10')] = 0
print('O2,O10 by the letter: mean %.3f gap %+.3f AUC %.3f Brier %.4f vs %.4f ; forecasts >= 0.8 that failed: %d' % (yl.mean(), fc.mean() - yl.mean(), auc(fc, yl), ((fc - yl) ** 2).mean(), ((yl.mean() - yl) ** 2).mean(), ((fc >= .8) & (yl == 0)).sum()))
rng = np.random.default_rng(3); uf = sorted(set(fil)); o = []
for _ in range(3000):
    s = np.concatenate([np.where(fil == uf[j])[0] for j in rng.choice(14, 14)]); v = auc(fc[s], y[s])
    if np.isfinite(v): o.append(v)
print('AUC all 78, file-resampled: %.2f to %.2f' % tuple(np.percentile(o, [2.5, 97.5])))
pub = {}
for d in sorted(os.listdir('/srv/commons')):
    if d.startswith('agent2-'):
        for root, _, fs in os.walk('/srv/commons/' + d):
            for f in fs:
                p = os.path.join(root, f)
                try:
                    if os.path.getsize(p) < 20000: pub[hashlib.sha256(open(p, 'rb').read()).hexdigest()] = p
                except OSError: pass
for r in 'AB':
    for f in sorted(os.listdir(R + 'sheets/' + r)):
        h = hashlib.sha256(open(R + f'sheets/{r}/{f}', 'rb').read()).hexdigest()
        print('  sheet %s/%-28s %s' % (r, f, pub.get(h, 'NO byte-identical published file')))
