"""zfmutants.py: plant one fault at a time in a copy of the swing plate's script, zfig.py, draw the plate with it and see whether
zfigtest.py notices.   python -I zfmutants.py [WORKERS]    The first copy has no fault and must pass (the control). Writes zfmutants.out."""
import os, shutil, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); PY = sys.executable; WORKERS = int(sys.argv[1]) if len(sys.argv) > 1 else 3
M = [('control', [])]
def m(name, *pairs): M.append((name, list(pairs)))
m('the dots one error too high', ("(n, fx(n), fy(B), col, SURF,", "(n, fx(n), fy(B + se), col, SURF,"))
m('the bars two errors long each way', ("(n, fx(n), fy(B - se), fx(n), fy(B + se), col))", "(n, fx(n), fy(B - 2 * se), fx(n), fy(B + 2 * se), col))"))
m('the dots one point to the right', ("(n, fx(n), fy(B), col, SURF,", "(n, fx(n + 1), fy(B), col, SURF,"))
m('the dots\' B with the theory\'s coefficient', ("DOTS = {n: (study5.R['disc-%d' % n]['B'],", "DOTS = {n: (study5.R['disc-%d' % n]['v'] - 0.08068 * n ** (1 / 3.0),"))
m('the colours of the two sheets changed over', ("col = ORANGE if sheet == 4 else BLUE", "col = ORANGE if sheet == 5 else BLUE"))
m('the fourth sheet\'s dot left out', ("if study4.R.get(100) is not None: DOTS[100]", "if False: DOTS[100]"))
m('the curve a plain rounded normal (no skewness)', ("CURVE = {n: ruler5.swing_model(n, G) - C5 * n ** (1 / 3.0) for n in NS}", "CURVE = {n: ruler5.swing_model(n, 0.0) - C5 * n ** (1 / 3.0) for n in NS}"))
m('the curve moved one point along', ("CURVE = {n: ruler5.swing_model(n, G) - C5 * n ** (1 / 3.0) for n in NS}", "CURVE = {n: ruler5.swing_model(n + 1, G) - C5 * (n + 1) ** (1 / 3.0) for n in NS}"))
m('the curve with half its swing', ("CURVE = {n: ruler5.swing_model(n, G) - C5 * n ** (1 / 3.0) for n in NS}", "CURVE = {n: 0.5 * (ruler5.swing_model(n, G) + ruler5.smooth_of(n)) - C5 * n ** (1 / 3.0) for n in NS}"))
m('the level line 0.002 too high', ("LEVEL = {n: ruler5.line_of(n) - C5 * n ** (1 / 3.0) for n in NS}", "LEVEL = {n: ruler5.line_of(n) + 0.002 - C5 * n ** (1 / 3.0) for n in NS}"))
m('the level line is the swing-off trend, not the fourth sheet\'s line', ("LEVEL = {n: ruler5.line_of(n) - C5 * n ** (1 / 3.0) for n in NS}", "LEVEL = {n: ruler5.smooth_of(n) - C5 * n ** (1 / 3.0) for n in NS}"))
m('the tick labels up the side one step out', ("text-anchor=\"end\">&#8722;%.3f</text>' % (v, X0 - 8, fy(v) + 4, MUTED, -v))", "text-anchor=\"end\">&#8722;%.3f</text>' % (v, X0 - 8, fy(v) + 4, MUTED, -v + 0.005))"))
m('the ticks along the foot one point out', ("out.append('<text class=\"xtick\" data-n=\"%d\" x=\"%.1f\" y=\"%d\" font-size=\"11\" fill=\"%s\" text-anchor=\"middle\">%d</text>' % (n, fx(n), YB + 20, MUTED, n))", "out.append('<text class=\"xtick\" data-n=\"%d\" x=\"%.1f\" y=\"%d\" font-size=\"11\" fill=\"%s\" text-anchor=\"middle\">%d</text>' % (n, fx(n), YB + 20, MUTED, n + 1))"))
m('the marks of the mean count a quarter of a layer out', ("m = h / 2.0; n = min((abs(ruler5.mean_of(x / 20.0) - m), x / 20.0)", "m = h / 2.0; n = min((abs(ruler5.mean_of(x / 20.0) - m - 0.25), x / 20.0)"))
m('the marks of the mean count labelled a half too high', ("MUTED, ('%d' % m) if h % 2 == 0 else ('%.1f' % m)))", "MUTED, ('%.1f' % (m + 0.5))))"))
m('the title says "swings" whatever Z is', ("    if Z >= 0.008: title =", "    if True: title ="), ("Z = (DOTS[90][0] + DOTS[105][0] + DOTS[120][0]) / 3 - (DOTS[83][0] + DOTS[98][0] + DOTS[113][0]) / 3;", "Z = (DOTS[83][0] + DOTS[98][0] + DOTS[113][0]) / 3 - (DOTS[90][0] + DOTS[105][0] + DOTS[120][0]) / 3;"))
m('the title says no swing', ("    if Z >= 0.008: title =", "    if Z >= 0.8: title ="), ("    elif Z <= 0.004: title =", "    elif Z <= 0.4: title ="))
m('the key\'s orange dot named as the fifth sheet\'s', ("T(228, 102, 'the fourth sheet&#8217;s 100 points (the curve&#8217;s source)', 12, INK2)", "T(228, 102, 'the fifth sheet&#8217;s discs', 12, INK2)"))
m('the key does not say the curve was made from the orange dot', ("T(228, 102, 'the fourth sheet&#8217;s 100 points (the curve&#8217;s source)', 12, INK2)", "T(228, 102, 'the fourth sheet&#8217;s 100 points', 12, INK2)"))
m('the line under the title names the theory\'s coefficient', ("less 0.08227&#183;n^(1/3), against n.", "less 0.08068&#183;n^(1/3), against n."))
def one(job):
    i, (name, pairs) = job; d = '/dev/shm/agent2-zfmut-%d-%d' % (os.getpid(), i); os.makedirs(d); t0 = time.time()
    try:
        for x in ('zfig.py', 'zfigtest.py', 'study3.py', 'study4.py', 'study5.py', 'after4.py', 'lattice.py', 'ruler5.py', 'ruler5.out', 'theory.py', 'theory.json', 'fresh.py'): shutil.copy(os.path.join(HERE, x), d)
        s = open(os.path.join(d, 'zfig.py')).read()
        for a, b in pairs:
            if s.count(a) != 1: return i, name, 'NOT PLANTED', 'the text to change was found %d times' % s.count(a), 0
            s = s.replace(a, b)
        open(os.path.join(d, 'zfig.py'), 'w').write(s); env = dict(os.environ, SHAPE_AFTER=os.path.join(HERE, 'runs-after'))
        r = subprocess.run(['nice', '-n', '19', PY, '-I', 'zfig.py'], cwd=d, env=env, capture_output=True, text=True, timeout=900)
        if r.returncode != 0: return i, name, 'noticed' if pairs else 'CONTROL FAILED', 'the script does not run', time.time() - t0
        r = subprocess.run(['nice', '-n', '19', PY, '-I', 'zfigtest.py'], cwd=d, env=env, capture_output=True, text=True, timeout=900); out = r.stdout
        fails = [l[6:120] for l in out.split('\n') if l.startswith('FAIL')]; last = out.strip().split('\n')[-1] if out.strip() else 'no output'
        if not pairs: return i, name, 'control passed' if r.returncode == 0 else 'CONTROL FAILED', last, time.time() - t0
        return i, name, 'noticed' if r.returncode != 0 else 'PASSED', ('%d tests failed; first: %s' % (len(fails), fails[0]) if fails else last), time.time() - t0
    finally: shutil.rmtree(d, ignore_errors=True)
if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=WORKERS) as ex: res = list(ex.map(one, enumerate(M)))
    lines = ['%-9s %-72s %-15s %4.0f s   %s' % ('' if r[1] == 'control' else 'fault %d' % r[0], r[1], r[2], r[4], r[3]) for r in res]
    planted = [r for r in res if r[1] != 'control' and r[2] != 'NOT PLANTED']; noticed = [r for r in planted if r[2] == 'noticed']
    lines.append('%d faults planted, %d noticed, %d passed every test, %d could not be planted; the control %s' % (len(planted), len(noticed), len(planted) - len(noticed), sum(1 for r in res if r[2] == 'NOT PLANTED'), res[0][2]))
    open(os.path.join(HERE, 'zfmutants.out'), 'w').write('\n'.join(lines) + '\n'); print('\n'.join(lines))
