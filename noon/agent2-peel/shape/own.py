"""own.py: clouds made by the first study's program itself (../peel SHAPE N SEED: disc, square or triangle), with no file of points
and none of cloud.c, peeled and counted. An after-check asked for by the referee: is the small excess at 100,000 points the
generator's?   python -I own.py SHAPE N CLOUDS SEED0 OUT [WORKERS]      One line of JSON a cloud; cloud i has seed SEED0 + i + 1."""
import json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); shape, n, K, seed0, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]; workers = int(sys.argv[6]) if len(sys.argv) > 6 else 14
def one(i):
    try: o = json.loads(subprocess.run([os.path.join(HERE, '..', 'peel'), shape, str(n), str(seed0 + i + 1)], capture_output=True, text=True).stdout)
    except Exception: return None
    return json.dumps({'shape': shape, 'kind': 'exact', 'maker': 'peel', 'n0': n, 'n': o['n'], 'seed': seed0 + i + 1, 'layers': o['layers']}) + '\n' if o['n'] == n else None
bad = 0
with open(out, 'w') as f, ThreadPoolExecutor(max_workers=workers) as ex:
    for line in ex.map(one, range(K)):
        if line is None: bad += 1
        else: f.write(line)
print('%s by peel itself, %d points: %d clouds asked, %d failed' % (shape, n, K, bad))
