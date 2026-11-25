import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from rsolve import exact_miss
E40 = np.linspace(0, 1, 41)
up = json.load(open('/home/agent2/drum/chain-free-up.json'))
a = np.array([r for r in up if abs(r['weight'] - 1.43) < 1e-9][0]['a'])
print('two discs +12.94 inside 0.438 and +5.63 inside 0.234: exact miss %.4f%%' % (100 * exact_miss([0, .234, .438, 1], [12.94 + 5.63, 12.94, 0])[0]))
rng = np.random.default_rng(4)
for s in (0.01, 0.03):
    v = [100 * exact_miss(E40, a * (1 + s * rng.standard_normal(40)))[0] for _ in range(12)]
    print('author 40-ring load at 1.43, each ring load off by %.0f%% (s.d.), 12 draws: median miss %.3f%%, range %.3f%% to %.3f%%' % (100 * s, np.median(v), min(v), max(v)))
b = a.copy(); b[6] *= 1.02
print('hoop ring alone 2%% heavier: %.3f%%' % (100 * exact_miss(E40, b)[0]))
