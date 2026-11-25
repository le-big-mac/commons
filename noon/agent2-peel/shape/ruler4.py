"""ruler4.py: before the fourth sheet is sealed: what each reading of the lean says for discs of 100, 300 and 1,000 points, and which
of the sheet's lines each reading would pass.   python -I ruler4.py
The readings are fitted to the five sizes of the third sheet (3,000 to 300,000) and carried down. Errors of the new variances will be
about 0.0007 to 0.0017 (400,000 clouds), far smaller than what separates the readings, so no random runs are drawn: this is a table."""
import math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import study3, theory
NEW = (100, 300, 1000); C5, B5 = 0.08227, -0.0473      # the third sheet's variance = C5 n^(1/3) + B5, written into the fourth sheet
def wls(ys, es, cols):
    X = np.stack([np.asarray(c, float) for c in cols], 1); w = 1 / np.asarray(es, float) ** 2; cov = np.linalg.inv(X.T @ (X * w[:, None])); b = cov @ (X.T @ (w * np.asarray(ys, float))); return b, np.sqrt(np.diag(cov)), float((w * (np.asarray(ys, float) - X @ b) ** 2).sum())
def readings():
    R = study3.R; N = list(study3.ASKED); c_th = theory.predictions('disc', 1.0)['exact']; vr = [R[n]['v'] / R[n]['theory_v'] for n in N]; ve = [R[n]['vse'] / R[n]['theory_v'] for n in N]; out = {}
    out['the theory as it stood'] = lambda n: c_th * n ** (1 / 3.0)
    out['a constant (power -1/3)'] = lambda n: C5 * n ** (1 / 3.0) + B5
    for p in (0.22, 0.52):
        b, e, chi = wls(vr, ve, [[1.0] * 5, [n ** -p for n in N]]); out['power -%.2f' % p] = (lambda n, b=b, p=p: c_th * n ** (1 / 3.0) * (b[0] + b[1] * n ** -p))
    for e_ in (0.3, 0.1, -0.1, -0.3): out['a constant and %+.1f n^(-1/3)' % e_] = (lambda n, e_=e_: C5 * n ** (1 / 3.0) + B5 + e_ * n ** (-1 / 3.0))
    return out
def B(v, n): return v - C5 * n ** (1 / 3.0)
MEANS = {'c + d n^(-1/3)': lambda n: 0.0472 + 1.0363 * n ** (-1 / 3.0), 'c + d n^(-1/6)': lambda n: -0.0110 + 0.4905 * n ** (-1 / 6.0), 'a tenth of a layer': lambda n: 0.10}      # the mean's excess, as fitted to the five sizes
if __name__ == '__main__':
    import study4
    rd = readings(); tags = ['P1', 'P2', 'P3', 'P4', 'P5']
    print('%-34s %s   %s' % ('reading of the variance', '   '.join('B(%d)' % n for n in NEW), '  '.join(tags)))
    for lab, f in rd.items():
        b = {n: B(f(n), n) for n in NEW}; v = study4.verdicts(None, b, {}); print('%-34s %s   %s' % (lab, '   '.join('%+.4f' % b[n] for n in NEW), '  '.join(' Y' if v[t] else ' n' for t in tags)))
    print('errors to expect of a variance from 400,000 clouds: ' + ', '.join('%.4f at %d' % ((C5 * n ** (1 / 3.0) + B5) * math.sqrt(2 / 4e5), n) for n in NEW))
    print()
    print('%-34s %s   P6  P7' % ('reading of the mean\'s excess', '   '.join('at %d' % n for n in NEW)))
    for lab, f in MEANS.items():
        ex = {n: f(n) for n in NEW}; v = study4.verdicts(None, {}, ex); print('%-34s %s   %s' % (lab, '   '.join('%+.3f' % ex[n] for n in NEW), '  '.join(' Y' if v[t] else ' n' for t in ('P6', 'P7'))))
    print('errors to expect of a mean from 400,000 clouds: ' + ', '.join('%.4f at %d' % (math.sqrt((C5 * n ** (1 / 3.0) + B5) / 4e5), n) for n in NEW))
    print()
    print('P0: Sylvester\'s share %.5f; the error of a share from 400,000 clouds %.5f; the band is 0.7020 to 0.7070, 3.5 errors each way: %s' % (study4.SYL, math.sqrt(study4.SYL * (1 - study4.SYL) / 4e5), 'held' if study4.verdicts(study4.SYL, {}, {})['P0'] else 'FAILED'))
    print('    a program that lost or gained one layer in 100 four-point clouds would give %.4f or %.4f: %s, %s' % (study4.SYL - 0.01, study4.SYL + 0.01, 'held' if study4.verdicts(study4.SYL - 0.01, {}, {})['P0'] else 'failed', 'held' if study4.verdicts(study4.SYL + 0.01, {}, {})['P0'] else 'failed'))
