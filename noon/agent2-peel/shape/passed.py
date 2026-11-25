"""passed.py: the one broken copy that the tests first let through, run beside the true program.   python -I passed.py
The fault: cloud.c draws the disc's points from a box 1 in 100 short on one side, so a sliver of the disc (x above 0.99) gets no
points. 2,000 discs of 100,000 points from each program, the same seeds; the mean count of layers of each."""
import json, math, os, shutil, subprocess, sys
import numpy as np
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); D = '/dev/shm/agent2-passed-%d' % os.getpid(); os.makedirs(D)
s = open(os.path.join(HERE, 'cloud.c')).read(); a = 'kind = 0; x0 = y0 = -1; x1 = y1 = 1; }'; assert s.count(a) == 1
open(os.path.join(D, 'cloud.c'), 'w').write(s.replace(a, 'kind = 0; x0 = y0 = -1; x1 = y1 = 1; x1 = 0.99; }')); subprocess.run(['gcc', '-O2', '-o', os.path.join(D, 'cloudm'), os.path.join(D, 'cloud.c'), '-lm'], check=True)
def one(job):
    prog, seed = job; f = os.path.join(D, 'c-%s-%d.txt' % (os.path.basename(prog), seed)); subprocess.run([prog, 'disc', '100000', str(seed)], stdout=open(f, 'w')); o = json.loads(subprocess.run([os.path.join(HERE, '..', 'peel'), 'file:' + f, '0', '0', '-fast'], capture_output=True, text=True).stdout); os.remove(f); return o['layers']
with ThreadPoolExecutor(max_workers=12) as ex:
    true = np.array(list(ex.map(one, [(os.path.join(HERE, 'cloud'), 70000000 + i) for i in range(2000)])), float); broken = np.array(list(ex.map(one, [(os.path.join(D, 'cloudm'), 70000000 + i) for i in range(2000)])), float)
shutil.rmtree(D)
cap = math.acos(0.99) - 0.99 * math.sqrt(1 - 0.99 ** 2)          # the area of the sliver
print('the sliver left empty is %.5f of the disc\'s area. By the equation the time to vanish falls by psi x area, worth %.2f layers, and the same 100,000 points in less area are denser, worth %.2f layers more: to first order no change (a disc is at the ceiling)' % (cap / math.pi, 998.79 * (cap / (2 * math.pi)) / 0.75, 998.79 * (2 / 3.0) * cap / math.pi))
print('2,000 discs each: the true program\'s mean count %.3f (%.3f), the broken one\'s %.3f (%.3f); the difference %.3f (%.3f); variances %.3f and %.3f' % (true.mean(), true.std(ddof=1) / math.sqrt(2000), broken.mean(), broken.std(ddof=1) / math.sqrt(2000), broken.mean() - true.mean(), math.hypot(true.std(ddof=1), broken.std(ddof=1)) / math.sqrt(2000), true.var(ddof=1), broken.var(ddof=1)))
