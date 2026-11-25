"""ymutants.py: plant one fault at a time in a copy of the scoring script, study.py, and see whether ruler.py notices.
python -I ymutants.py [WORKERS]      The first copy has no fault and must pass (the control). Writes ymutants.out."""
import os, shutil, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); PY = sys.executable; WORKERS = int(sys.argv[1]) if len(sys.argv) > 1 else 3
M = [('control', [])]
def m(name, *pairs): M.append((name, list(pairs)))
m('S4 from the means, not the variances', ("[('triangle', vr, ('exact-triangle-100000', D5), 1.1951, 1.155, 1.235)]", "[('triangle', mr, ('exact-triangle-100000', D5), 1.1951, 1.155, 1.235)]"))
m('S7 from the variances, not the variances over the squares of the means', ("[('100,000', wr, ('exact-rtriangle-100000', 'exact-triangle-100000'), 0.9547, 0.935, 0.975)]", "[('100,000', vr, ('exact-rtriangle-100000', 'exact-triangle-100000'), 0.9547, 0.935, 0.975)]"))
m('S16 held whatever the figures', ("0.9547, -1e9, 1 - 1e-12), ('30,000'", "0.9547, -1e9, 9.0), ('30,000'"), ("0.9547, -1e9, 1 - 1e-12)])", "0.9547, -1e9, 9.0)])"))
m('a missing file is not noticed', ("def complete(*names): return all(F[n] is not None and F[n]['K'] >= 0.999 * F[n]['asked'] for n in names)", "def complete(*names): return True"))
m('a file a fifth short still counts', (">= 0.999 * F[n]['asked'] for n in names)", ">= 0.5 * F[n]['asked'] for n in names)"))
m('S3 open at the top', ("[('disc', v1_, (D5,), 3.745, 3.60, 3.90)]", "[('disc', v1_, (D5,), 3.745, 3.60, 39.0)]"))
m('S5 open at the bottom', ("('exact-square-100000', D5), 1.0984, 1.058, 1.138)]", "('exact-square-100000', D5), 1.0984, 0.058, 1.138)]"))
m('S5 from the hexagons', ("[('square', vr, ('exact-square-100000', D5), 1.0984, 1.058, 1.138)]", "[('square', vr, ('exact-hexagon-100000', D5), 1.0984, 1.058, 1.138)]"))
m('S6 open at the top', ("('exact-hexagon-100000', D5), 1.0407, 1.000, 1.082)]", "('exact-hexagon-100000', D5), 1.0407, 1.000, 9.082)]"))
m('S8 from the 100,000-point files', ("[('30,000', wr, ('exact-rtriangle-30000', 'exact-triangle-30000'), 0.9547, 0.935, 0.975)]", "[('30,000', wr, ('exact-rtriangle-100000', 'exact-triangle-100000'), 0.9547, 0.935, 0.975)]"))
m('S9 open for the ellipse', ("('exact-ellipse-100000', D5), 1.0, 0.95, 1.05)", "('exact-ellipse-100000', D5), 1.0, 0.5, 1.5)"))
m('S9 open for disc0', ("('exact-disc0-100000', D5), 1.0, 0.965, 1.035)]", "('exact-disc0-100000', D5), 1.0, 0.5, 1.5)]"))
m('S10 open at the top', ("1.0526, 1.003, 1.103), ('quarter', vr, ('exact-quarter-100000', D5), 1.0743, 1.024, 1.124)]", "1.0526, 1.003, 9.103), ('quarter', vr, ('exact-quarter-100000', D5), 1.0743, 1.024, 9.124)]"))
m('S11 from the clouds of exactly n', ("('chance-triangle-100000', 'chance-disc-100000'), 1.1951, 1.145, 1.245)]", "('exact-triangle-100000', 'exact-disc-100000'), 1.1951, 1.145, 1.245)]"))
m('S12 open at the top', ("('chance-square-100000', 'chance-disc-100000'), 1.0985, 1.04, 1.16)]", "('chance-square-100000', 'chance-disc-100000'), 1.0985, 1.04, 9.16)]"))
m('S13 open at the top', ("[('disc', v1_, ('chance-disc-100000',), 8.179, 7.77, 8.59)]", "[('disc', v1_, ('chance-disc-100000',), 8.179, 7.77, 80.59)]"))
m('S14 with 30,000 for n', ("lambda m, v: v / m ** 2 * 1e5, ('exact-triangle-100000',), 0.3754, 0.360, 0.390)]", "lambda m, v: v / m ** 2 * 3e4, ('exact-triangle-100000',), 0.3754, 0.360, 0.390)]"))
m('S15 open at the top', ("('exact-triangle-30000',), 0.3754, 0.356, 0.394)]", "('exact-triangle-30000',), 0.3754, 0.356, 9.394)]"))
m('S1 a hundred times too wide', ("t, t - 0.0006, t + 0.0006) for sh, t in (('hexagon', 1.02016)", "t, t - 0.06, t + 0.06) for sh, t in (('hexagon', 1.02016)"))
m('S2 a hundred times too wide', ("t, t - 0.0006, t + 0.0006) for sh, t in (('triangle', 1.09321)", "t, t - 0.06, t + 0.06) for sh, t in (('triangle', 1.09321)"))
m('held and failed the wrong way round', ("out['lines'][tag] = {'verdict': 'held' if ok else 'failed', 'odds': odds, 'parts': res}", "out['lines'][tag] = {'verdict': 'failed' if ok else 'held', 'odds': odds, 'parts': res}"))
m('the ratio of the means upside down', ("mr = lambda m1, v1, m2, v2: m1 / m2;", "mr = lambda m1, v1, m2, v2: m2 / m1;"))
m('variance over the mean, not over its square', ("wr = lambda m1, v1, m2, v2: (v1 / m1 ** 2) / (v2 / m2 ** 2);", "wr = lambda m1, v1, m2, v2: (v1 / m1) / (v2 / m2);"))
m('a line with two parts holds if either does', ("val, se = stat(fn, *nm); inside = lo <= val <= hi; ok = ok and inside", "val, se = stat(fn, *nm); inside = lo <= val <= hi; ok = (ok or inside) if res else inside"))
def one(job):
    i, (name, pairs) = job; d = '/dev/shm/agent2-ymut-%d-%d' % (os.getpid(), i); os.makedirs(d); t0 = time.time()
    try:
        for x in ('study.py', 'theory.py', 'theory.json'): shutil.copy(os.path.join(HERE, x), d)
        s = open(os.path.join(d, 'study.py')).read()
        for a, b in pairs:
            if s.count(a) != 1: return i, name, 'NOT PLANTED', 'the text to change was found %d times' % s.count(a), 0
            s = s.replace(a, b)
        open(os.path.join(d, 'study.py'), 'w').write(s)
        try: r = subprocess.run(['nice', '-n', '19', PY, '-I', os.path.join(HERE, 'ruler.py'), os.path.join(d, 'study.py')], capture_output=True, text=True, timeout=1500); rc, out = r.returncode, r.stdout
        except subprocess.TimeoutExpired: rc, out = -9, ''
        fails = [l[6:110] for l in out.split('\n') if l.startswith('FAIL')]; last = out.strip().split('\n')[-1] if out.strip() else 'no output'
        if not pairs: return i, name, 'control passed' if rc == 0 else 'CONTROL FAILED', last, time.time() - t0
        return i, name, 'noticed' if rc != 0 else 'PASSED', ('%d cases failed; first: %s' % (len(fails), fails[0]) if fails else last), time.time() - t0
    finally: shutil.rmtree(d, ignore_errors=True)
if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=WORKERS) as ex: res = list(ex.map(one, enumerate(M)))
    lines = ['%-9s %-72s %-15s %4.0f s   %s' % ('' if r[1] == 'control' else 'fault %d' % r[0], r[1], r[2], r[4], r[3]) for r in res]
    planted = [r for r in res if r[1] != 'control' and r[2] != 'NOT PLANTED']; noticed = [r for r in planted if r[2] == 'noticed']
    lines.append('%d faults planted, %d noticed, %d passed every case, %d could not be planted; the control %s' % (len(planted), len(noticed), len(planted) - len(noticed), sum(1 for r in res if r[2] == 'NOT PLANTED'), res[0][2]))
    open(os.path.join(HERE, 'ymutants.out'), 'w').write('\n'.join(lines) + '\n'); print('\n'.join(lines))
