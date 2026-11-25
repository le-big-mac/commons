"""fresh.py: the clouds peeled after the scoring (runs-after/), reckoned in one place for after.py, sfig.py and sfacts.py.
None of them is in any verdict. Every set is of clouds of exactly 100,000 points.
  made before the referee's second step, because two of the sheet's sets stood furthest from their lines (batchK.sh, batchK2.sh):
     discs, quarter discs (two batches) and half discs, by cloud.c as the sheet's were;
  made after it, because the referee asked whether the small excess at 100,000 points was the generator's (batchL.sh):
     discs, squares and triangles by the first study's own generator (own.py: ../peel SHAPE N SEED, no cloud.c, no file),
     and quarter discs whose points are numpy's (npq.py)."""
import gzip, json, math, os, zlib
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); AF = os.environ.get('SHAPE_AFTER', os.path.join(HERE, 'runs-after'))
import theory
SETS = {'disc-cloud': ('disc', 'cloud.c', ['exact-disc-100000']), 'quarter-cloud-a': ('quarter', 'cloud.c', ['exact-quarter-100000']), 'quarter-cloud-b': ('quarter', 'cloud.c', ['exact-quarter-100000-b']),
        'quarter-cloud': ('quarter', 'cloud.c', ['exact-quarter-100000', 'exact-quarter-100000-b']), 'halfdisc-cloud': ('halfdisc', 'cloud.c', ['exact-halfdisc-100000']),
        'disc-peel': ('disc', 'peel', ['own-disc-100000']), 'square-peel': ('square', 'peel', ['own-square-100000']), 'triangle-peel': ('triangle', 'peel', ['own-triangle-100000']), 'quarter-numpy': ('quarter', 'numpy', ['numpy-quarter-100000'])}
def counts(name):
    p = os.path.join(AF, name + '.jsonl')
    if os.path.exists(p): return np.array([json.loads(l)['layers'] for l in open(p)], float)
    if os.path.exists(p + '.gz'): return np.array([json.loads(l)['layers'] for l in gzip.open(p + '.gz', 'rt')], float)
    return None
_kept = {}
def reckon(key, B=4000):
    """the set's clouds, its mean count, variance (about each file's own mean), w n = variance x 100,000 / mean^2, and their errors by resampling whole clouds"""
    if key in _kept: return _kept[key]
    shape, maker, files = SETS[key]; xs = [counts(f) for f in files]
    if any(x is None for x in xs): _kept[key] = None; return None
    m = float(np.mean(np.concatenate(xs))); x = np.concatenate([x_ - x_.mean() + m for x_ in xs]); K = len(x); rng = np.random.default_rng([20261125, zlib.crc32(key.encode())])
    vals, cnt = np.unique(np.round(x, 6), return_counts=True); H = rng.multinomial(K, cnt / K, size=B); mb = H @ vals / K; vb = (H @ vals ** 2 - K * mb ** 2) / (K - len(xs)); v = float(((x - m) ** 2).sum() / (K - len(xs)))
    th = theory.predictions(shape, 1e5); _kept[key] = {'shape': shape, 'maker': maker, 'K': K, 'm': m, 'v': v, 'vse': float(vb.std(ddof=1)), 'w': v / m ** 2 * 1e5, 'wse': float((vb / mb ** 2 * 1e5).std(ddof=1)), 'line': th['exact'] / th['mean'] ** 2 * 1e5, 'theory_v': th['exact']}
    return _kept[key]
def pool(pairs):
    """the weighted mean of (value, error) pairs, its error, and chi-square about it"""
    w = np.array([1 / s ** 2 for v, s in pairs]); vals = np.array([v for v, s in pairs]); m = float((w * vals).sum() / w.sum()); return m, 1 / math.sqrt(w.sum()), float((w * (vals - m) ** 2).sum())
