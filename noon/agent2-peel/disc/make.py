"""make.py: peel many discs and keep the annulus sums of each.   python -I make.py KIND N0 CLOUDS SEED0 OUT [WORKERS [HALF]]
KIND is "exact" (every cloud has exactly N0 points) or "chance" (the number of points of each cloud is drawn from the Poisson law
of mean N0, by numpy's default generator started from SEED0). Cloud i (1, 2, ...) is  ../peel disc N SEED0+i -depths - | ./rings N0
and its one line of JSON is written to OUT (in the order the clouds finish; each line carries its seed). HALF, if given, is passed
to rings as the half-width of an annulus (the clouds of the sheet were made without it: 0.008)."""
import os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); kind, n0, K, seed0, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]; workers = int(sys.argv[6]) if len(sys.argv) > 6 else 14; half = sys.argv[7:8]
assert kind in ('exact', 'chance')
ns = [n0] * K if kind == 'exact' else [int(v) for v in np.random.default_rng(seed0).poisson(n0, K)]
def one(i):
    p1 = subprocess.Popen([os.path.join(HERE, '..', 'peel'), 'disc', str(ns[i]), str(seed0 + i + 1), '-depths', '-'], stdout=subprocess.PIPE)
    r = subprocess.run([os.path.join(HERE, 'rings'), str(n0)] + half, stdin=p1.stdout, capture_output=True, text=True); p1.stdout.close(); c1 = p1.wait()
    return r.stdout if c1 == 0 and r.returncode == 0 and r.stdout.startswith('{') else None
bad = 0
with open(out, 'w') as f, ThreadPoolExecutor(max_workers=workers) as ex:
    for line in ex.map(one, range(K)):
        if line is None: bad += 1
        else: f.write(line)
print('%s %d: %d clouds asked, %d failed' % (kind, n0, K, bad))
