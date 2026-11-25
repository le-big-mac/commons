"""npq.py: quarter discs whose points come from numpy's generator and not from cloud.c, peeled and counted. An after-check asked
for by the referee: is the quarter disc's excess the generator's?   python -I npq.py N CLOUDS SEED0 OUT [WORKERS]
A point is two reals drawn evenly from the square [0, 2) x [0, 2), kept if within 2 of the corner, moved so that the centre of
area is at the origin, and rounded down to whole numbers of 2^-28, as cloud.c does. One line of JSON a cloud."""
import json, math, os, subprocess, sys
import numpy as np
from concurrent.futures import ProcessPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); n, K, seed0, out = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]; workers = int(sys.argv[5]) if len(sys.argv) > 5 else 14
C = 8 / (3 * math.pi); UNIT = 2.0 ** 28
def one(i):
    seed = seed0 + i + 1; rng = np.random.default_rng(seed); pts = np.empty((0, 2))
    while len(pts) < n:
        p = rng.random((int(1.35 * (n - len(pts))) + 16, 2)) * 2; pts = np.vstack([pts, p[(p ** 2).sum(1) <= 4]])
    q = np.floor((pts[:n] - C) * UNIT).astype(np.int64); f = '/dev/shm/agent2-npq-%d-%d.txt' % (os.getpid(), i)
    with open(f, 'w') as fh: fh.write('\n'.join('%d %d' % (a, b) for a, b in q.tolist()) + '\n')
    try: o = json.loads(subprocess.run([os.path.join(HERE, '..', 'peel'), 'file:' + f, '0', '0', '-both' if i % 200 == 0 else '-fast'], capture_output=True, text=True).stdout)
    except Exception: o = None
    os.remove(f)
    return json.dumps({'shape': 'quarter', 'kind': 'exact', 'maker': 'numpy', 'n0': n, 'n': o['n'], 'seed': seed, 'layers': o['layers'], 'same': o.get('same', -1)}) + '\n' if o and o['n'] == n else None
bad = 0
with open(out, 'w') as f, ProcessPoolExecutor(max_workers=workers) as ex:
    for line in ex.map(one, range(K), chunksize=8):
        if line is None: bad += 1
        else: f.write(line)
print('quarter disc by numpy, %d points: %d clouds asked, %d failed' % (n, K, bad))
