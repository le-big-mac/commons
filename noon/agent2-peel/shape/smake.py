"""smake.py: peel many clouds of one shape and keep the count of layers of each.   python -I smake.py SHAPE KIND N0 CLOUDS SEED0 OUT [WORKERS]
KIND is "exact" (every cloud has exactly N0 points) or "chance" (the number of points of each cloud drawn from the Poisson law of
mean N0, by numpy's default generator started from SEED0). Cloud i (1, 2, ...) has seed SEED0 + i. Every shape goes the same
way:  ./cloud SHAPE N SEED > a file in /dev/shm, then ../peel file:... -fast;  only the shape "disc0" is peeled by
../peel disc N SEED, with that program's own points (a check on the way through cloud.c).
Every 200th cloud is peeled both ways (-both), and the line says whether every point got the same depth. One line of JSON a cloud."""
import json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); shape, kind, n0, K, seed0, out = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), sys.argv[6]; workers = int(sys.argv[7]) if len(sys.argv) > 7 else 14
assert kind in ('exact', 'chance')
ns = [n0] * K if kind == 'exact' else [int(v) for v in np.random.default_rng(seed0).poisson(n0, K)]
PEEL = os.path.join(HERE, '..', 'peel')
def one(i):
    seed = seed0 + i + 1
    if shape == 'disc0': r = subprocess.run([PEEL, 'disc', str(ns[i]), str(seed)], capture_output=True, text=True)
    else:
        f = '/dev/shm/agent2-shape-%d-%d.txt' % (os.getpid(), i)
        with open(f, 'w') as fh: c = subprocess.run([os.path.join(HERE, 'cloud'), shape, str(ns[i]), str(seed)], stdout=fh).returncode
        r = subprocess.run([PEEL, 'file:' + f, '0', '0', '-both' if i % 200 == 0 else '-fast'], capture_output=True, text=True) if c == 0 else None
        os.remove(f)
    try: o = json.loads(r.stdout)
    except Exception: return None
    if o['n'] != ns[i]: return None
    return json.dumps({'shape': shape, 'kind': kind, 'n0': n0, 'n': o['n'], 'seed': seed, 'layers': o['layers'], 'same': o.get('same', -1)}) + '\n'
bad = 0
with open(out, 'w') as f, ThreadPoolExecutor(max_workers=workers) as ex:
    for line in ex.map(one, range(K)):
        if line is None: bad += 1
        else: f.write(line)
print('%s %s %d: %d clouds asked, %d failed' % (shape, kind, n0, K, bad))
