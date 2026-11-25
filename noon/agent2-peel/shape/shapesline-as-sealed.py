"""shapesline.py: every earlier set of clouds of exactly n points, of every shape, set against the straight line through the eight
disc sizes ("the theory's variance x a, less a constant"). Asked for by the referee's report on the third and fourth sheets, which
did it first (its shapes_b.py); this is my own, from the raw files.   python -I shapesline.py
For each file: the variance of the count over the theory's for that shape and size, less what the line gives, with its error
(variance x sqrt(2 / clouds), over the theory's). Then pooled by kind of shape, weighted by the errors. The line's own error is not
in the pooled errors; it is printed beside them."""
import json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import theory, after4
KIND = {'disc': 'discs and the ellipse', 'disc0': 'discs and the ellipse', 'ellipse': 'discs and the ellipse', 'triangle': 'polygons', 'square': 'polygons', 'hexagon': 'polygons', 'halfdisc': 'half and quarter discs', 'quarter': 'half and quarter discs', 'rtriangle': 'the rounded triangle'}
def sets():
    out = []
    for folder in ('runs', 'runs-after'):
        for f in sorted(os.listdir(os.path.join(HERE, folder))):
            if not f.endswith('.jsonl') or f.startswith(('chance-', 'n3-', 'n4-', 'n5-')): continue
            rows = [json.loads(l) for l in open(os.path.join(HERE, folder, f))]; sh = rows[0]['shape']; n0 = rows[0]['n0']; assert all(r['n'] == n0 for r in rows)
            x = np.array([r['layers'] for r in rows], float); v = float(x.var(ddof=1)); tv = theory.predictions('disc' if sh == 'disc0' else sh, n0)['exact']; out.append(dict(file=folder + '/' + f, shape=sh, n=n0, K=len(x), ratio=v / tv, se=v * math.sqrt(2.0 / len(x)) / tv, tv=tv))
    return out
def pool(rows, key='off'):
    w = np.array([1 / r['se'] ** 2 for r in rows]); y = np.array([r[key] for r in rows]); m = float((w * y).sum() / w.sum()); return m, 1 / math.sqrt(w.sum()), float((w * (y - m) ** 2).sum()), sum(r['K'] for r in rows)
def main():
    S = after4.gather(); b, e, chi, dof = after4.series(S, list(S), 2); cth = theory.predictions('disc', 1.0)['exact']; a = b[0] / cth; R = sets()
    for r in R: r['line'] = a + b[1] / r['tv']; r['off'] = r['ratio'] - r['line']; r['kind'] = KIND[r['shape']]
    print('the line: the theory\'s variance x %.4f (%.4f), less %.4f (%.4f); at a disc of 100,000 points its own error is %.4f of the variance' % (a, e[0] / cth, -b[1], e[1], math.hypot(e[0] / cth, e[1] / 3.745)))
    print('   file                                      shape       points   clouds   variance over the theory\'s   the line   off the line (se)')
    for r in R: print('   %-40s  %-10s %7d  %7d   %.4f                       %.4f     %+.4f (%.4f)' % (r['file'], r['shape'], r['n'], r['K'], r['ratio'], r['line'], r['off'], r['se']))
    print()
    first = 'runs/exact-quarter-100000.jsonl'
    groups = [('polygons (triangle, square, hexagon)', [r for r in R if r['kind'] == 'polygons']), ('half and quarter discs', [r for r in R if r['kind'] == 'half and quarter discs']), ('   the same without the first 8,000 quarter discs, which were chased', [r for r in R if r['kind'] == 'half and quarter discs' and r['file'] != first]),
              ('   the second sheet\'s sealed quarter discs alone', [r for r in R if '/q2-' in r['file']]), ('the rounded triangle', [r for r in R if r['kind'] == 'the rounded triangle']),
              ('every shape with a corner (polygons, half and quarter discs)', [r for r in R if r['kind'] in ('polygons', 'half and quarter discs')]), ('   the same without the first 8,000 quarter discs', [r for r in R if r['kind'] in ('polygons', 'half and quarter discs') and r['file'] != first]),
              ('every shape with a corner or a flat side (the rounded triangle too), without the first 8,000', [r for r in R if r['kind'] != 'discs and the ellipse' and r['file'] != first]), ('discs and the ellipse', [r for r in R if r['kind'] == 'discs and the ellipse'])]
    for lab, rows in groups:
        m, se, chi2, K = pool(rows); tv = float(np.mean([r['tv'] for r in rows])); print('%-92s %2d sets %9s clouds   %+.4f (%.4f), %+.1f errors; chi-square among them %.1f on %d; in the variance about %+.3f' % (lab, len(rows), format(K, ','), m, se, m / se, chi2, len(rows) - 1, m * tv))
if __name__ == '__main__': main()
