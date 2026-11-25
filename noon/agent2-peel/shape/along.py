"""along.py: I A / T^2 followed along the flow from eleven starting shapes: as the shape rounds, how low does it go?   python -I along.py [make]
Each start is run by flow at 1,536 angles, step quality 0.25, with -along; at each moment t the curve K_t has the time T - t left, the
area A(t), and the integral of psi^2 over what it encloses, so I A / T^2 for K_t can be read off. The stepping's own offset (the value at
the very end, where the shape is an ellipse and the truth is 4/3) is taken off every figure. "make" runs and keeps along.json."""
import json, os, subprocess, sys
import numpy as np
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); KEPT = os.path.join(HERE, 'along.json')
STARTS = ['triangle', 'square', 'hexagon', 'poly:1,0,0.309017,0.951057,-0.809017,0.587785,-0.809017,-0.587785,0.309017,-0.951057', 'poly:0,0,4,0,3,1,1,1', 'poly:0,0,1,0,0.1,1,0,1', 'poly:0,0,1,0,1,0.1,0.1,1,0,1', 'halfdisc', 'quarter', 'cap:30', 'cap:150']
if len(sys.argv) > 1 and sys.argv[1] == 'make':
    def one(i):
        f = '/dev/shm/agent2-along-%d-%d.txt' % (os.getpid(), i); subprocess.run(['nice', '-n', '19', os.path.join(HERE, 'flow'), STARTS[i], '1536', '-q', '0.25', '-along', f], capture_output=True)
        a = np.loadtxt(f)[::-1]; os.remove(f); n, t, left, A, La, s2, F = a.T; r = F * A / left ** 2; r = r - (r[-1] - 4 / 3.0); j = int(np.argmin(r))
        return {'start': STARTS[i], 'at_start': float(r[0]), 'least': float(r[j]), 't': float(t[j]), 'area_left': float(A[j] / A[0])}
    with ThreadPoolExecutor(max_workers=3) as ex: json.dump(list(ex.map(one, range(len(STARTS)))), open(KEPT, 'w'), indent=1)
rows = json.load(open(KEPT))
if __name__ == '__main__':
    print('start                                  I A/T^2 at the start   least along the flow   at t        area left then')
    for o in rows: print('%-38s %.4f                 %.4f                 %.4f      %.3f' % (o['start'][:38], o['at_start'], o['least'], o['t'], o['area_left']))
    print('the least of all: %.4f, from %s' % (min(o['least'] for o in rows), min(rows, key=lambda o: o['least'])['start'][:40]))
