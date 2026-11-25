"""ceiling.py: how far below the ceiling (4/3) T^2/A the integral I falls, for every shape I tried.   python -I ceiling.py [make]
Each shape goes through flow at 1,440 angles (a quarter of a degree, so that the sides of every polygon here lie on mesh
directions) at step quality 0.5 and 0.25; the figure printed is at the limit (twice the second less the first). "make" runs them
and keeps the lines in ceiling.json. A polygon "+ r" is the polygon, scaled to area pi, then swollen by a disc of radius r."""
import json, math, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); KEPT = os.path.join(HERE, 'ceiling.json')
TRI, RIGHT, T369 = 'triangle', 'poly:0,0,1,0,0,1', 'poly:0,0,1.7320508075688772,0,0,1'
PENT = 'poly:' + ','.join('%.12f,%.12f' % (math.cos(math.radians(72 * k)), math.sin(math.radians(72 * k))) for k in range(5))
SHAPES = [('disc', 'disc', None), ('ellipse 3:1', 'ellipse', None), ('equilateral triangle', TRI, None), ('right triangle', RIGHT, None), ('triangle 30-60-90', T369, None), ('square', 'square', None), ('rectangle 3:1', 'rect', None),
          ('regular pentagon', PENT, None), ('regular hexagon', 'hexagon', None), ('trapezoid (0,0) (4,0) (3,1) (1,1)', 'poly:0,0,4,0,3,1,1,1', None), ('square with a corner cut off at 0.9', 'poly:0,0,1,0,1,0.1,0.1,1,0,1', None),
          ('square with a corner cut off at 0.5', 'poly:0,0,1,0,1,0.5,0.5,1,0,1', None), ('half disc', 'halfdisc', None), ('quarter disc', 'quarter', None)] + \
         [('disc cut by a chord seen under %d degrees' % (2 * a), 'cap:%d' % a, None) for a in (30, 60, 120, 150)] + \
         [('wavy disc, %d waves of %g' % (m, e), 'wave:%d:%g' % (m, e), None) for m, e in ((2, 0.3), (3, 0.1), (4, 0.06), (5, 0.04))] + \
         [('equilateral triangle + %g' % r, TRI, r) for r in (0.02, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.45, 0.7, 1.0)] + [('the rounded triangle of the runs (+ a quarter of the inradius)', 'rtriangle', None)] + \
         [('right triangle + %g' % r, RIGHT, r) for r in (0.1, 0.2, 0.3, 0.45)] + [('triangle 30-60-90 + %g' % r, T369, r) for r in (0.1, 0.2, 0.3)] + \
         [('square + %g' % r, 'square', r) for r in (0.05, 0.1, 0.2, 0.4)] + [('regular hexagon + %g' % r, 'hexagon', r) for r in (0.1, 0.2)] + [('regular pentagon + %g' % r, PENT, r) for r in (0.1, 0.2)] + \
         [('square with a corner cut off at 0.9, + %g' % r, 'poly:0,0,1,0,1,0.1,0.1,1,0,1', r) for r in (0.1, 0.2)] + [('half disc + %g' % r, 'halfdisc', r) for r in (0.1, 0.2)]
if len(sys.argv) > 1 and sys.argv[1] == 'make':
    def one(job):
        (label, name, r), q = job; cmd = ['nice', '-n', '19', os.path.join(HERE, 'flow'), name, '1440', '-q', q] + (['-rho0', str(r)] if r else [])
        try: return [label, q, json.loads(subprocess.run(cmd, capture_output=True, text=True).stdout)]
        except Exception: return [label, q, None]
    with ThreadPoolExecutor(max_workers=int(sys.argv[2]) if len(sys.argv) > 2 else 3) as ex: json.dump(list(ex.map(one, [(s, q) for s in SHAPES for q in ('0.5', '0.25')])), open(KEPT, 'w'))
runs = json.load(open(KEPT)); rows = []
for label, name, r in SHAPES:
    a = [o for l, q, o in runs if l == label and q == '0.5'][0]; b = [o for l, q, o in runs if l == label and q == '0.25'][0]
    if a is None or b is None: rows.append((None, label)); continue
    f = lambda o, k: o[k] * o['area'] / o['T'] ** 2; sf = 2 * f(b, 'shortfall') - f(a, 'shortfall'); ie = 2 * f(b, 'I_edge') - f(a, 'I_edge'); isum = 2 * f(b, 'I') - f(a, 'I')
    tt = lambda o: o['T'] / o['area'] ** (2 / 3.0) / (0.75 / math.pi ** (2 / 3.0)); rows.append((ie, label, sf, isum, 2 * tt(b) - tt(a), a['area']))
if __name__ == '__main__':
    print('%d shapes; I A/T^2 at the ceiling is 4/3 = 1.33333' % len(rows)); print('I A/T^2 (from the edge)   (summed inside)   4/3 less the shortfall   T/A^(2/3) over the disc\'s   shape')
    for row in rows:
        if row[0] is None: print('   the run failed                                                                              %s' % row[1]); continue
        ie, label, sf, isum, tt, area = row; print('   %.5f                 %.5f           %.5f                  %.5f                    %s' % (ie, isum, 4 / 3.0 - sf, tt, label))
    good = sorted(r for r in rows if r[0] is not None)
    print('the least: %.5f (%s); the next: %.5f (%s); the greatest: %.5f (%s)' % (good[0][0], good[0][1], good[1][0], good[1][1], good[-1][0], good[-1][1]))
    print('at the ceiling to 5 in 100,000 (%d): %s' % (sum(1 for r in good if r[0] > 4 / 3.0 - 5e-5), '; '.join(r[1] for r in good if r[0] > 4 / 3.0 - 5e-5)))
    print('the largest difference between the two ways of getting I (edge, summed): %.1e of I' % max(abs(r[0] / r[3] - 1) for r in good))
