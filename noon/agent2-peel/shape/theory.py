"""theory.py: what the equation says about the count of layers of a convex cloud of any shape.   python -I theory.py [make]
For a shape K of area A holding n points (density rho = n / A), the flow of flow.c gives T, the time K takes to vanish, and
psi(p), the time lost for a unit of area removed at p as the front passes it; the integral of psi over K is T. Then, with the
level problem's noise D and its share (4/9) alpha^2 that is the count of points (../far/):
    mean count of layers                 alpha rho^(2/3) T
    its variance, number left to chance  rho^(1/3) D I,                      I = the integral of psi^2 over K
    its variance, exactly n points       rho^(1/3) (D I - (4/9) alpha^2 T^2 / A)
(a point at p adds (2/3) alpha rho^(-1/3) psi(p) layers; with exactly n points the square of the mean of that goes out).

Two things about I, both worked on paper (notes.md) and both checked by flow.c:
    I = (3/2) <g, L^(-1) g>      g(theta) = psi R on the starting curve (the gradient of T in the support function), L = 1 + d^2/dtheta^2
    T^2 / A  <=  I  <=  (4/3) T^2 / A,      and  (4/3) T^2 / A - I = -(3/2) <z, L^(-1) z>,   z = g - (2/3)(T/A) R,
the upper end reached exactly by the shapes at which T / A^(2/3) stands still: ellipses among all shapes; and among polygons
(whose sides alone can be moved) every triangle, every parallelogram, every regular polygon.

"make" runs flow for each shape at 1,536 angles with step quality 0.5 and 0.25, and at 3,072 angles with 0.5, and erode at two
step sizes, and keeps the lines in theory.json; without it theory.json is read. A figure "at the limit" is twice the q = 0.25 run
less the q = 0.5 run (the error of the stepping is in proportion to q); what doubling the angles moves is printed beside it."""
import json, math, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); KEPT = os.path.join(HERE, 'theory.json')
ALPHA = 1.3259; D = 1.081; DC = 4 / 9.0 * ALPHA ** 2
SHAPES = ['disc', 'ellipse', 'triangle', 'square', 'rect', 'hexagon', 'rtriangle', 'halfdisc', 'quarter']
if len(sys.argv) > 1 and sys.argv[1] == 'make':
    jobs = [('flow', sh, m, q) for sh in SHAPES for m, q in ((1536, '0.5'), (1536, '0.25'), (3072, '0.5'))] + [('erode', sh, m, eta) for sh in SHAPES for m, eta in ((16384, '1e-4'), (16384, '3e-5'))]
    def one(job):
        prog, sh, m, x = job; cmd = ['nice', '-n', '15', os.path.join(HERE, prog), sh, str(m)] + (['-q', x] if prog == 'flow' else [x, '1e-3'])
        return [prog, json.loads(subprocess.run(cmd, capture_output=True, text=True).stdout)]
    with ThreadPoolExecutor(max_workers=12) as ex: json.dump(list(ex.map(one, jobs)), open(KEPT, 'w'))
runs = json.load(open(KEPT))
def limit(sh, key):
    """(the figure at the limit of fine steps, what doubling the angles moved it by, the three runs)"""
    f = {(o['M'], round(o['dtmax'] / 1e-4, 4)): (o[key] if key != 'ratio' else o['I_edge'] * o['area'] / o['T'] ** 2) for prog, o in runs if prog == 'flow' and o['shape'] == sh}
    a, b, c = f[(1536, 0.5)], f[(1536, 0.25)], f[(3072, 0.5)]; return 2 * b - a, c - a, (a, b, c)
def erosion(sh):
    e = {o['eta']: o['T'] for prog, o in runs if prog == 'erode' and o['shape'] == sh}; return e[3e-5] + (e[3e-5] - e[1e-4]) / ((1e-4 / 3e-5) ** (2 / 3.0) - 1)       # the error of a step of erosion falls as its area to the 2/3
TH = {}
for sh in SHAPES:
    T, dT, Ts = limit(sh, 'T'); I, dI, Is = limit(sh, 'I_edge'); Isum, dS, Ss = limit(sh, 'I'); low, _, _ = limit(sh, 'lower_bound_affine'); sf, dsf, _ = limit(sh, 'shortfall')
    TH[sh] = {'T': T, 'I': I, 'Isum': Isum, 'lower': low, 'shortfall': sf, 'Te': erosion(sh), 'dT': dT, 'dI': dI, 'Ts': Ts, 'Is': Is}
def predictions(sh, n=1.0, d=D, dc=DC, I=None):
    t = TH[sh]; I = t['I'] if I is None else I; rho = n / math.pi
    return {'mean': ALPHA * rho ** (2 / 3.0) * t['T'], 'chance': rho ** (1 / 3.0) * d * I, 'exact': rho ** (1 / 3.0) * (d * I - dc * t['T'] ** 2 / math.pi)}
if __name__ == '__main__':
    print('D = %.3f, the count\'s share (4/9) alpha^2 = %.4f, alpha = %.4f. Every shape has area pi. All figures at the limit of fine steps.' % (D, DC, ALPHA))
    print('shape       T (flow)   T (erosion)  T over disc\'s  I (edge)   I (summed)  moved by doubling the angles: T, I   I A / T^2   4/3 - that, from z   least I by Cauchy       variance over n^(1/3): chance, exactly n   sd over mean x sqrt(n): chance, exactly n')
    for sh in SHAPES:
        t = TH[sh]; p = predictions(sh); q = t['I'] * math.pi / t['T'] ** 2
        print('%-10s  %.5f    %.5f      %.5f        %.5f    %.5f     %+.0e, %+.0e                       %.5f     %.5f              %.5f (%.3f of I)    %.4f, %.4f                             %.4f, %.4f' % (
            sh, t['T'], t['Te'], t['T'] / 0.75, t['I'], t['Isum'], t['dT'], t['dI'], q, t['shortfall'] * math.pi / t['T'] ** 2, t['lower'], t['lower'] / t['I'], p['chance'], p['exact'], math.sqrt(p['chance']) / p['mean'], math.sqrt(p['exact']) / p['mean']))
    print('the disc exactly: T = 3/4, I = 3/(4 pi) = %.5f, I A / T^2 = 4/3. At I A / T^2 = 4/3 the last two columns are %.4f and %.4f; at I A / T^2 = 1 (which no shape reaches) %.4f and %.4f' % (
        3 / (4 * math.pi), math.sqrt(4 / 3.0 * D) / ALPHA, math.sqrt(4 / 3.0 * D - DC) / ALPHA, math.sqrt(D) / ALPHA, math.sqrt(D - DC) / ALPHA))
    print('ratios to the disc: of the mean; of the variance (chance; exactly n); of the square of the mean; and what two other rules would give for the variance with exactly n')
    for sh in SHAPES[2:]:
        p = predictions(sh); p0 = predictions('disc'); pl = predictions(sh, I=TH[sh]['lower'])
        print('   %-10s %.5f;  %.4f; %.4f;  %.4f      if psi were level along each curve (the least I): %.4f; if the variance went as the mean: %.4f' % (sh, p['mean'] / p0['mean'], p['chance'] / p0['chance'], p['exact'] / p0['exact'], (p['mean'] / p0['mean']) ** 2, pl['exact'] / p0['exact'], p['mean'] / p0['mean']))
    p = predictions('rtriangle'); p3 = predictions('triangle')
    print('the rounded triangle against the triangle, exactly n: variance %.4f, square of the mean %.4f, so the variance over the square of the mean %.4f' % (p['exact'] / p3['exact'], (p['mean'] / p3['mean']) ** 2, p['exact'] / p3['exact'] / (p['mean'] / p3['mean']) ** 2))
