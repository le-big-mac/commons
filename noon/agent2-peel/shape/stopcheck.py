"""stopcheck.py: two rules of flow.c that could decide its answers, varied.   python -I stopcheck.py [make]
(1) When the area is down to STOP of what it was (a thousandth), the rest of T and of I is taken as an ellipse's. A tenth of I
    comes from that last thousandth. Here STOP is a hundredth, a thousandth and a ten-thousandth.
(2) Every shape is swollen at the start by a disc of radius RHO0 (a millionth), so that its corners are not sharp. Here RHO0 is
    1e-8, 1e-6 and 1e-4 (a swelling of 1e-4 is itself a change of shape, of about 2 in 10,000 of the area).
For the triangle, the rounded triangle and the half disc, at 1,536 angles, step quality 0.5 and 0.25, carried to the limit."""
import json, math, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); KEPT = os.path.join(HERE, 'stopcheck.json')
CASES = [(sh, stop, rho0) for sh in ('triangle', 'rtriangle', 'halfdisc') for stop, rho0 in (('1e-2', '1e-6'), ('1e-3', '1e-6'), ('1e-4', '1e-6'), ('1e-3', '1e-8'), ('1e-3', '1e-4'))]
if len(sys.argv) > 1 and sys.argv[1] == 'make':
    def one(job):
        (sh, stop, rho0), q = job; return [sh, stop, rho0, q, json.loads(subprocess.run(['nice', '-n', '19', os.path.join(HERE, 'flow'), sh, '1536', '-q', q, '-stop', stop, '-rho0', rho0], capture_output=True, text=True).stdout)]
    with ThreadPoolExecutor(max_workers=3) as ex: json.dump(list(ex.map(one, [(c, q) for c in CASES for q in ('0.5', '0.25')])), open(KEPT, 'w'))
runs = json.load(open(KEPT)); rows = {}
for sh, stop, rho0 in CASES:
    a = [o for s, st, r, q, o in runs if (s, st, r, q) == (sh, stop, rho0, '0.5')][0]; b = [o for s, st, r, q, o in runs if (s, st, r, q) == (sh, stop, rho0, '0.25')][0]
    rows[(sh, stop, rho0)] = {k: 2 * b[k] - a[k] for k in ('T', 'I_edge', 'I', 'area')}
if __name__ == '__main__':
    print('shape       stop    swelling   area        T          I (edge)   I (summed)   I A/T^2    against the usual setting: T, I (edge), I (summed), in parts of 100,000')
    for (sh, stop, rho0), r in rows.items():
        base = rows[(sh, '1e-3', '1e-6')]
        print('%-10s  %-6s  %-8s   %.6f    %.6f   %.6f   %.6f     %.5f    %+.1f, %+.1f, %+.1f' % (sh, stop, rho0, r['area'], r['T'], r['I_edge'], r['I'], r['I_edge'] * r['area'] / r['T'] ** 2, (r['T'] / base['T'] - 1) * 1e5, (r['I_edge'] / base['I_edge'] - 1) * 1e5, (r['I'] / base['I'] - 1) * 1e5))
    worst_stop = max(abs(r[k] / rows[(sh, '1e-3', '1e-6')][k] - 1) for (sh, stop, rho0), r in rows.items() if rho0 == '1e-6' for k in ('T', 'I_edge', 'I'))
    worst_r8 = max(abs(r[k] / rows[(sh, '1e-3', '1e-6')][k] - 1) for (sh, stop, rho0), r in rows.items() if rho0 == '1e-8' for k in ('T', 'I_edge', 'I'))
    print('the most that the stop moves T or I: %.1e; the most that a swelling a hundred times smaller moves them: %.1e' % (worst_stop, worst_r8))
    print('the share of I that comes from the last thousandth of the area, for a disc: %.3f' % (1e-3 ** (1 / 3.0)))
