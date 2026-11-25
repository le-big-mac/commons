"""study5b.py: the four lines of the addendum to the fifth sheet (expectations-5-addendum.md), from study5.py's figures.
python -I study5b.py     Writes study5b.json."""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import study5
LINES = [('Q10', 0.50, 'the triangle\'s B at 1,000 points less the control disc\'s is between -0.020 and -0.006'), ('Q11', 0.40, 'the triangle\'s B less the rounded triangle\'s at 1,000 points is -0.008 or below'),
         ('Q12', 0.40, 'the triangle\'s B less the rounded triangle\'s at 300 points is -0.008 or below'), ('Q13', 0.40, 'the triangle\'s B less the rounded triangle\'s, pooled over 300, 1,000 and 3,000 points, is -0.008 or below')]
def verdicts(Bc, Bt, Br, Et, Er):
    """Bc: the control disc's B at 1,000; Bt[n], Br[n]: the triangle's and the rounded triangle's B; Et[n], Er[n]: their errors (for the pooling's weights). None where a file is missing."""
    has = lambda d, ks: d is not None and all(d.get(k) is not None for k in ks); out = {}; fig = {}
    if Bc is not None and has(Bt, [1000]): fig['Q10'] = Bt[1000] - Bc; out['Q10'] = bool(-0.020 <= fig['Q10'] <= -0.006)
    else: out['Q10'] = None
    for tag, n in (('Q11', 1000), ('Q12', 300)):
        if has(Bt, [n]) and has(Br, [n]): fig[tag] = Bt[n] - Br[n]; out[tag] = bool(fig[tag] <= -0.008)
        else: out[tag] = None
    if has(Bt, [300, 1000, 3000]) and has(Br, [300, 1000, 3000]):
        w = {n: 1 / (Et[n] ** 2 + Er[n] ** 2) for n in (300, 1000, 3000)}; fig['Q13'] = sum(w[n] * (Bt[n] - Br[n]) for n in w) / sum(w.values()); fig['Q13se'] = 1 / math.sqrt(sum(w.values())); out['Q13'] = bool(fig['Q13'] <= -0.008)
    else: out['Q13'] = None
    return out, fig
if __name__ == '__main__':
    R = study5.R; g = lambda k: None if R.get(k) is None else R[k]['B']; e = lambda k: None if R.get(k) is None else R[k]['vse']; S = (300, 1000, 3000)
    V, fig = verdicts(g('cdisc-1000'), {n: g('triangle-%d' % n) for n in S}, {n: g('rtriangle-%d' % n) for n in S}, {n: e('triangle-%d' % n) for n in S}, {n: e('rtriangle-%d' % n) for n in S})
    err = {'Q10': lambda: math.hypot(e('triangle-1000'), e('cdisc-1000')), 'Q11': lambda: math.hypot(e('triangle-1000'), e('rtriangle-1000')), 'Q12': lambda: math.hypot(e('triangle-300'), e('rtriangle-300')), 'Q13': lambda: fig['Q13se']}
    out = {'lines': {}}; held = failed = notrun = 0; brier = 0.0
    for tag, odds, what in LINES:
        ok = V[tag]
        if ok is None: notrun += 1; print('%-3s not run          %s' % (tag, what)); out['lines'][tag] = {'verdict': 'not run'}; continue
        held += ok; failed += (not ok); brier += (odds - (1.0 if ok else 0.0)) ** 2; d = '%+.4f (%.4f)' % (fig[tag], err[tag]()); print('%-3s %-7s (odds %.2f)  %s: %s' % (tag, 'HELD' if ok else 'FAILED', odds, what, d)); out['lines'][tag] = {'verdict': 'held' if ok else 'failed', 'odds': odds, 'detail': d}
    n_ = held + failed; print(); print('%d held, %d failed, %d not run.%s' % (held, failed, notrun, (' Brier score of the odds %.3f.' % (brier / n_)) if n_ else ''))
    out['held'] = int(held); out['failed'] = int(failed); out['notrun'] = int(notrun); out['brier'] = brier / n_ if n_ else None; json.dump(out, open(os.path.join(HERE, 'study5b.json'), 'w'), indent=1, default=float)
