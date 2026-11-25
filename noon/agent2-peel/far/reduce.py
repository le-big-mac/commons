"""reduce.py: from each raw file of slabs in a folder of runs (snap-HM-SEED.bin, 13 MB each) write slabs-HM-SEED.json: for every slab
its height and what slabs.py keeps of it. And gzip a copy of each profile. The published folder holds these small files and not
the raw ones; study.py and after.py give the same output from either (ftest of that: `python -I reduce.py check`).
   python -I reduce.py FROM TO      (FROM: a folder of runs; TO: where the reduced copies go)"""
import glob, gzip, json, os, shutil, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from slabs import slabstats, lags_for
src, dst = sys.argv[1], sys.argv[2]; os.makedirs(dst, exist_ok=True); n = 0
for f in sorted(glob.glob(os.path.join(src, 'run-*.json'))):
    o = json.load(open(f)); base = os.path.basename(f); shutil.copyfile(f, os.path.join(dst, base))
    pf = f.replace('run-', 'profile-').replace('.json', '.txt')
    with open(pf, 'rb') as a, gzip.GzipFile(os.path.join(dst, os.path.basename(pf) + '.gz'), 'wb', mtime=0) as b: shutil.copyfileobj(a, b)
    sf = f.replace('run-', 'snap-').replace('.json', '.bin')
    if 'snap_heights' in o and os.path.exists(sf):
        raw = np.fromfile(sf, dtype=np.float64).reshape(len(o['snap_heights']), int(o['C'])); lags = lags_for(raw.shape[1])
        json.dump({'heights': o['snap_heights'], 'lags': lags, 'slabs': [slabstats(row, lags) for row in raw]}, open(os.path.join(dst, base.replace('run-', 'slabs-')), 'w'))
    n += 1
print('%d windows reduced into %s' % (n, dst))
