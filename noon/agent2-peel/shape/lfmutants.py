"""lfmutants.py: plant one fault at a time in a copy of the third plate's script, lfig.py, draw the plate with it and see whether
lfigtest.py notices.   python -I lfmutants.py [WORKERS]    The first copy has no fault and must pass (the control). Writes lfmutants.out."""
import os, shutil, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); PY = sys.executable; WORKERS = int(sys.argv[1]) if len(sys.argv) > 1 else 3
M = [('control', [])]
def m(name, *pairs): M.append((name, list(pairs)))
m('the dots one error too high', ("(n, fx(x), fy(r), BLUE, SURF,", "(n, fx(x), fy(r + se), BLUE, SURF,"))
m('the bars two errors long each way', ("(n, fx(x), fy(r - se), fx(x), fy(r + se), BLUE))", "(n, fx(x), fy(r - 2 * se), fx(x), fy(r + 2 * se), BLUE))"))
m('the dots placed at n^(-1/2)', ("    x = n ** (-1 / 3.0); r, se, K = J['sizes'][str(n)]", "    x = n ** (-1 / 2.0) * 3; r, se, K = J['sizes'][str(n)]"))
m('the ticks along the foot placed at n^(-1/2)', ("x = 0.0 if n is None else n ** (-1 / 3.0); out.append('<line x1=", "x = 0.0 if n is None else n ** (-1 / 2.0) * 3; out.append('<line x1="))
m('the lean\'s dashed line with a slope of -0.32', ("fy(1.018 - 0.64 * XHI), MUTED))", "fy(1.018 - 0.32 * XHI), MUTED))"))
m('the plain line drawn at 1.01', ("(fx(XLO), fy(1.0), fx(XHI), fy(1.0), MUTED))", "(fx(XLO), fy(1.01), fx(XHI), fy(1.01), MUTED))"))
m('the solid line drawn on to 3,000 points', ("s, sse, a, ase, chi = F4; xr = 10000 ** (-1 / 3.0)", "s, sse, a, ase, chi = F4; xr = 3000 ** (-1 / 3.0)"))
m('the solid line with the slope halved', ("(fx(0), fy(a), fx(xr), fy(a + s * xr), INK, a, s))", "(fx(0), fy(a), fx(xr), fy(a + 0.5 * s * xr), INK, a, s))"))
m('the bar at the line\'s end two errors each way', ("(fx(0), fy(a - ase), fx(0), fy(a + ase), INK))", "(fx(0), fy(a - 2 * ase), fx(0), fy(a + 2 * ase), INK))"))
m('the figures beside the line\'s end are the slope\'s', ("'%.3f (%.3f)' % (a, ase), 11, INK2)", "'%.3f (%.3f)' % (s, sse), 11, INK2)"))
m('the title says no lean', ("    if F4[0] <= -0.32 and below and above and max(below) < 30000 <= min(above): title =", "    if F4[0] >= -0.18 and below and above and max(below) < 30000 <= min(above): title ="), ("    elif F4[0] <= -0.32: title =", "    elif F4[0] > 0: title ="))
m('the title keeps the first wording, "the further below the theory"', ("title = 'The smaller the cloud, the lower: below the theory under 30,000 points, above it over'", "title = 'The spread leans with the size of the cloud: the smaller, the further below the theory'"))
m('the tick labels up the side one step off', ("text-anchor=\"end\">%.2f</text>' % (v, X0 - 8, fy(v) + 4, MUTED, v))", "text-anchor=\"end\">%.2f</text>' % (v, X0 - 8, fy(v) + 4, MUTED, v + 0.01))"))
m('the 3,000-point dot left out', ("SIZES = [n for n in study3.ASKED if R[n] is not None]", "SIZES = [n for n in study3.ASKED if R[n] is not None and n != 3000]"))
m('the dots in the dashed lines\' grey', ("stroke=\"%s\" stroke-width=\"2\"><title>%s discs of %s points: %.4f, give or take %.4f</title></circle>' % (n, fx(x), fy(r), BLUE, SURF,", "stroke=\"%s\" stroke-width=\"2\"><title>%s discs of %s points: %.4f, give or take %.4f</title></circle>' % (n, fx(x), fy(r), MUTED, SURF,"))
m('a label runs off the picture', ("T(fx(0.066), fy(1.0) - 7, 'plain', 11, MUTED, 'middle')", "T(fx(0.078), fy(1.0) - 7, 'the plain reading, with no lean at all', 11, MUTED, 'start')"))
def one(job):
    i, (name, pairs) = job; d = '/dev/shm/agent2-lfmut-%d-%d' % (os.getpid(), i); os.makedirs(d); t0 = time.time()
    try:
        for x in ('lfig.py', 'lfigtest.py', 'study3.py', 'theory.py', 'theory.json', 'fresh.py', 'expectations-3.md'): shutil.copy(os.path.join(HERE, x), d)
        s = open(os.path.join(d, 'lfig.py')).read()
        for a, b in pairs:
            if s.count(a) != 1: return i, name, 'NOT PLANTED', 'the text to change was found %d times' % s.count(a), 0
            s = s.replace(a, b)
        open(os.path.join(d, 'lfig.py'), 'w').write(s); env = dict(os.environ, SHAPE_AFTER=os.path.join(HERE, 'runs-after'))
        r = subprocess.run(['nice', '-n', '19', PY, '-I', 'lfig.py'], cwd=d, env=env, capture_output=True, text=True, timeout=900)
        if r.returncode != 0: return i, name, 'noticed' if pairs else 'CONTROL FAILED', 'the script does not run', time.time() - t0
        r = subprocess.run(['nice', '-n', '19', PY, '-I', 'lfigtest.py'], cwd=d, env=env, capture_output=True, text=True, timeout=900); out = r.stdout
        fails = [l[6:120] for l in out.split('\n') if l.startswith('FAIL')]; last = out.strip().split('\n')[-1] if out.strip() else 'no output'
        if not pairs: return i, name, 'control passed' if r.returncode == 0 else 'CONTROL FAILED', last, time.time() - t0
        return i, name, 'noticed' if r.returncode != 0 else 'PASSED', ('%d tests failed; first: %s' % (len(fails), fails[0]) if fails else last), time.time() - t0
    finally: shutil.rmtree(d, ignore_errors=True)
if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=WORKERS) as ex: res = list(ex.map(one, enumerate(M)))
    lines = ['%-9s %-62s %-15s %4.0f s   %s' % ('' if r[1] == 'control' else 'fault %d' % r[0], r[1], r[2], r[4], r[3]) for r in res]
    planted = [r for r in res if r[1] != 'control' and r[2] != 'NOT PLANTED']; noticed = [r for r in planted if r[2] == 'noticed']
    lines.append('%d faults planted, %d noticed, %d passed every test, %d could not be planted; the control %s' % (len(planted), len(noticed), len(planted) - len(noticed), sum(1 for r in res if r[2] == 'NOT PLANTED'), res[0][2]))
    open(os.path.join(HERE, 'lfmutants.out'), 'w').write('\n'.join(lines) + '\n'); print('\n'.join(lines))
