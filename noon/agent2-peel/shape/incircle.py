"""incircle.py: are polygons with an incircle at the ceiling? (The referee's blind step could not tell four of them from 4/3 to
5 parts in 10,000.)   python -I incircle.py [make]
A polygon whose sides, with outward normals at given angles, all lie at distance 1 from a point has an incircle. Six such, none
regular, none a triangle or a parallelogram; two of them again with one side moved out by a tenth (no incircle any more); and a
rectangle for comparison. flow at 1,440 angles, step quality 0.5 and 0.25, carried to the limit; the two that fall furthest short
again at 2,880 angles, at half the step, and with a hundredth of the starting swell."""
import json, math, os, subprocess, sys
import numpy as np
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); KEPT = os.path.join(HERE, 'incircle.json')
def circ(normals, hs=None):
    hs = hs or [1.0] * len(normals); P = []
    for i in range(len(normals)):
        a1, a2 = math.radians(normals[i]), math.radians(normals[(i + 1) % len(normals)]); A = np.array([[math.cos(a1), math.sin(a1)], [math.cos(a2), math.sin(a2)]]); P.append(np.linalg.solve(A, [hs[i], hs[(i + 1) % len(normals)]]))
    return 'poly:' + ','.join('%.14f,%.14f' % (x, y) for x, y in P)
CASES = [('incircle', 'kite, normals 45 120 240 315', circ([45, 120, 240, 315])), ('incircle', 'quadrilateral, normals 10 100 200 290', circ([10, 100, 200, 290])), ('incircle', 'quadrilateral, normals 0 75 160 250', circ([0, 75, 160, 250])),
         ('incircle', 'pentagon, normals 10 75 130 200 290', circ([10, 75, 130, 200, 290])), ('incircle', 'hexagon, normals 0 40 110 170 230 300', circ([0, 40, 110, 170, 230, 300])), ('incircle', 'heptagon, normals 5 50 95 160 215 265 320', circ([5, 50, 95, 160, 215, 265, 320])),
         ('none', 'the quadrilateral 10 100 200 290, one side moved out a tenth', circ([10, 100, 200, 290], [1.1, 1, 1, 1])), ('none', 'the pentagon, one side moved out a tenth', circ([10, 75, 130, 200, 290], [1, 1, 1.1, 1, 1])),
         ('none', 'rectangle 2 to 1 (a parallelogram)', circ([0, 90, 180, 270], [2, 1, 2, 1]))]
EXTRA = [(1440, '0.25', '1e-6'), (1440, '0.125', '1e-6'), (2880, '0.5', '1e-6'), (2880, '0.25', '1e-6'), (1440, '0.5', '1e-8'), (1440, '0.25', '1e-8')]
if len(sys.argv) > 1 and sys.argv[1] == 'make':
    jobs = [(lab, nm, 1440, q, '1e-6') for kind, lab, nm in CASES for q in ('0.5', '0.25')] + [(lab, nm, M, q, rho) for kind, lab, nm in CASES if lab.startswith('hexagon') or lab.startswith('quadrilateral, normals 0 75') for M, q, rho in EXTRA]
    def one(j):
        lab, nm, M, q, rho = j; return [lab, M, q, rho, json.loads(subprocess.run(['nice', '-n', '19', os.path.join(HERE, 'flow'), nm, str(M), '-q', q, '-rho0', rho], capture_output=True, text=True).stdout)]
    with ThreadPoolExecutor(max_workers=3) as ex: json.dump(list(ex.map(one, jobs)), open(KEPT, 'w'))
runs = json.load(open(KEPT)); f = lambda o: o['shortfall'] * o['area'] / o['T'] ** 2
def lim(lab, M, q1, q2, rho='1e-6'):
    a = [o for l, m, q, r, o in runs if (l, m, q, r) == (lab, M, q1, rho)][0]; b = [o for l, m, q, r, o in runs if (l, m, q, r) == (lab, M, q2, rho)][0]; return 2 * f(b) - f(a), a['halvings'] + b['halvings']
SHORT = {lab: lim(lab, 1440, '0.5', '0.25')[0] for kind, lab, nm in CASES}
if __name__ == '__main__':
    print('how far below 4/3 (in I A/T^2)   shape'); 
    for kind, lab, nm in CASES: print('   %.6f                      %s%s' % (SHORT[lab], lab, ' (it has an incircle)' if kind == 'incircle' else ''))
    for lab in ('hexagon, normals 0 40 110 170 230 300', 'quadrilateral, normals 0 75 160 250'):
        print('%s: at half the step %.6f; at 2,880 angles %.6f; with a hundredth of the swell %.6f' % (lab, lim(lab, 1440, '0.25', '0.125')[0], lim(lab, 2880, '0.5', '0.25')[0], lim(lab, 1440, '0.5', '0.25', '1e-8')[0]))
    print('(a triangle, a square and a regular hexagon read 0.00001, 0.00001 and 0.00000 by the same reckoning: theory.out)')
