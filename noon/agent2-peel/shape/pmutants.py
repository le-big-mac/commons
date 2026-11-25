"""pmutants.py: plant one fault at a time in a copy of the plate's own script, sfig.py, draw the plate with it and see whether
sfigtest.py notices.   python -I pmutants.py [WORKERS]      The first copy has no fault and must pass (the control). Writes pmutants.out."""
import os, shutil, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); PY = sys.executable; WORKERS = int(sys.argv[1]) if len(sys.argv) > 1 else 3
M = [('control', [])]
def m(name, *pairs): M.append((name, list(pairs)))
m('the dots one error too high', ("cx=\"%.1f\" cy=\"%.2f\" r=\"5\" fill=\"%s\" stroke=\"%s\" stroke-width=\"2\"><title>%s, %s clouds of %s points: %.4f, give or take %.4f</title></circle>' % (n0, x + dx, fy(v),", "cx=\"%.1f\" cy=\"%.2f\" r=\"5\" fill=\"%s\" stroke=\"%s\" stroke-width=\"2\"><title>%s, %s clouds of %s points: %.4f, give or take %.4f</title></circle>' % (n0, x + dx, fy(v + se),"))
m('the bars two errors up', ("(n0, x + dx, fy(v - se), x + dx, fy(v + se), colour))", "(n0, x + dx, fy(v - se), x + dx, fy(v + 2 * se), colour))"))
m('the bars drawn beside the dots', ("stroke-width=\"2\"/>' % (n0, x + dx, fy(v - se), x + dx, fy(v + se), colour))", "stroke-width=\"2\"/>' % (n0, x + dx + 4, fy(v - se), x + dx + 4, fy(v + se), colour))"))
m('the black marks at the figure for clouds left to chance', ("c = {'shape': sh, 'label': label, 'group': grp, 'theory': p['exact'] / p['mean'] ** 2 * 1e5}", "c = {'shape': sh, 'label': label, 'group': grp, 'theory': p['chance'] / p['mean'] ** 2 * 1e5}"))
m('the black marks all at the ceiling', ("(x - 24, fy(c['theory']), x + 24, fy(c['theory']), INK, label, c['theory']))", "(x - 24, fy(CEIL), x + 24, fy(CEIL), INK, label, c['theory']))"))
m('the dashed line 1 in 100 too high', ("(X0, fy(CEIL), X1, fy(CEIL), INK2, CEIL))", "(X0, fy(1.01 * CEIL), X1, fy(1.01 * CEIL), INK2, CEIL))"))
m('the ceiling\'s label gives another figure', ("'dashed: the ceiling the equation gives with D = 1.081, %.4f' % CEIL", "'dashed: the ceiling the equation gives with D = 1.081, %.4f' % (CEIL - 0.001)"))
m('the tick labels one step off', ("text-anchor=\"end\">%.2f</text>' % (v, X0 - 8, fy(v) + 4, MUTED, v))", "text-anchor=\"end\">%.2f</text>' % (v, X0 - 8, fy(v) + 4, MUTED, v + 0.01))"))
m('the triangle\'s and the square\'s labels changed over', ("('triangle', 'triangle', 0), ('square', 'square', 0)", "('triangle', 'square', 0), ('square', 'triangle', 0)"))
m('the 30,000-point dots taken from the 100,000-point files', ("        name = 'exact-%s-%d' % (sh, n0)", "        name = 'exact-%s-%d' % (sh, 100000)"))
m('the 30,000-point figures multiplied by 100,000', ("v, se = study.stat(lambda m, v: v / m ** 2 * n0, name)", "v, se = study.stat(lambda m, v: v / m ** 2 * 1e5, name)"))
m('the two colours changed over', ("for n0, colour, dx in ((100000, BLUE, -9 if '30000' in c else 0), (30000, ORANGE, 9)):", "for n0, colour, dx in ((100000, ORANGE, -9 if '30000' in c else 0), (30000, BLUE, 9)):"))
m('the key\'s colours changed over', ("out.append('<circle class=\"key\" cx=\"46\" cy=\"84\" r=\"5\" fill=\"%s\"/>' % BLUE)", "out.append('<circle class=\"key\" cx=\"46\" cy=\"84\" r=\"5\" fill=\"%s\"/>' % ORANGE)"), ("out.append('<circle class=\"key\" cx=\"176\" cy=\"84\" r=\"5\" fill=\"%s\"/>' % ORANGE)", "out.append('<circle class=\"key\" cx=\"176\" cy=\"84\" r=\"5\" fill=\"%s\"/>' % BLUE)"))
m('the title says six shapes', ("'Five shapes at one ceiling; the round-cornered triangle below it, as worked out beforehand'", "'Six shapes at one ceiling; the round-cornered triangle below it, as worked out beforehand'"))
m('the outlines upside down', ("' L'.join('%.1f %.1f' % (cx + s * px, cy - s * py) for px, py in P)", "' L'.join('%.1f %.1f' % (cx + s * px, cy + s * py) for px, py in P)"))
m('the hexagon drawn as a pentagon', ("P = [(math.cos(math.pi * k / 3), math.sin(math.pi * k / 3)) for k in range(6)]", "P = [(math.cos(2 * math.pi * k / 5), math.sin(2 * math.pi * k / 5)) for k in range(5)]"))
m('the rounded triangle\'s outline is a plain triangle', ("for j in range(3): P += [(V[j][0] + rr * math.cos(math.radians(-90 + 120 * j + 6 * k)), V[j][1] + rr * math.sin(math.radians(-90 + 120 * j + 6 * k))) for k in range(21)]", "P = [(v_[0] * 1.3, v_[1] * 1.3) for v_ in V]"))
m('the outlines one column to the right', ("out.append(outline(sh, x, 440, 17));", "out.append(outline(sh, x + 88, 440, 17));"))
m('a group\'s name runs off the picture', ("brace(xs[8], xs[8], 'furthest below')", "brace(xs[8] + 60, xs[8] + 60, 'furthest below, by the theory')"))
m('a stray line of words lies over the key', ("for clouds of exactly n points. Bars: one standard error either way.', 12, INK2)", "for clouds of exactly n points. Bars: one standard error either way.', 12, INK2); T(40, 90, 'The spread of the count', 12, INK2)"))
m('the error bars are two errors each way', ("if study.F.get(name) is not None and study.complete(name): v, se = study.stat(lambda m, v: v / m ** 2 * n0, name); c[str(n0)] = [v, se, study.F[name]['K']]", "if study.F.get(name) is not None and study.complete(name): v, se = study.stat(lambda m, v: v / m ** 2 * n0, name); se = 2 * se; c[str(n0)] = [v, se, study.F[name]['K']]"))
m('the half disc and the quarter disc changed over', ("('halfdisc', 'half disc', 1), ('quarter', 'quarter disc', 1)", "('quarter', 'half disc', 1), ('halfdisc', 'quarter disc', 1)"))
m('the open dots at the sheet\'s figures, not the fresh clouds\'', ("r=\"4.5\" fill=\"%s\" stroke=\"%s\" stroke-width=\"2\"><title>%s, %s fresh clouds of 100,000 points by %s, peeled after the scoring: %.4f, give or take %.4f</title></circle>' % (k, xo, fy(w),", "r=\"4.5\" fill=\"%s\" stroke=\"%s\" stroke-width=\"2\"><title>%s, %s fresh clouds of 100,000 points by %s, peeled after the scoring: %.4f, give or take %.4f</title></circle>' % (k, xo, fy(c['100000'][0]),"))
m('the open dots filled in', ("fy(w), SURF, BLUE, label, format(K, ','), maker, w, wse))", "fy(w), BLUE, BLUE, label, format(K, ','), maker, w, wse))"))
m('the other discs\' open dot taken from cloud.c\'s fresh discs', ("'disc0': ['disc-peel'],", "'disc0': ['disc-cloud'],"))
m('the open dots\' bars two errors long each way', ("(k, xo, fy(w - wse), xo, fy(w + wse), BLUE))", "(k, xo, fy(w - 2 * wse), xo, fy(w + 2 * wse), BLUE))"))
m('the quarter disc\'s second open dot left out', ("'quarter': ['quarter-cloud', 'quarter-numpy']}", "'quarter': ['quarter-cloud']}"))
m('the key calls the open dots the sheet\'s', ("'fresh clouds of 100,000 points, peeled afterwards (in no verdict)', 12, INK2)", "'the sheet\'s clouds of 100,000 points', 12, INK2)"))
m('the ceiling\'s label does not say which D', ("'dashed: the ceiling the equation gives with D = 1.081, %.4f' % CEIL", "'dashed: the ceiling, %.4f' % CEIL"))
def one(job):
    i, (name, pairs) = job; d = '/dev/shm/agent2-pmut-%d-%d' % (os.getpid(), i); os.makedirs(d); t0 = time.time()
    try:
        for x in ('sfig.py', 'sfigtest.py', 'study.py', 'theory.py', 'theory.json', 'fresh.py'): shutil.copy(os.path.join(HERE, x), d)
        s = open(os.path.join(d, 'sfig.py')).read()
        for a, b in pairs:
            if s.count(a) != 1: return i, name, 'NOT PLANTED', 'the text to change was found %d times' % s.count(a), 0
            s = s.replace(a, b)
        open(os.path.join(d, 'sfig.py'), 'w').write(s); env = dict(os.environ, SHAPE_RUNS=os.path.join(HERE, 'runs'), SHAPE_AFTER=os.path.join(HERE, 'runs-after'))
        r = subprocess.run(['nice', '-n', '19', PY, '-I', 'sfig.py'], cwd=d, env=env, capture_output=True, text=True, timeout=600)
        if r.returncode != 0: return i, name, 'noticed' if pairs else 'CONTROL FAILED', 'the script does not run', time.time() - t0
        r = subprocess.run(['nice', '-n', '19', PY, '-I', 'sfigtest.py'], cwd=d, env=env, capture_output=True, text=True, timeout=600); out = r.stdout
        fails = [l[6:120] for l in out.split('\n') if l.startswith('FAIL')]; last = out.strip().split('\n')[-1] if out.strip() else 'no output'
        if not pairs: return i, name, 'control passed' if r.returncode == 0 else 'CONTROL FAILED', last, time.time() - t0
        return i, name, 'noticed' if r.returncode != 0 else 'PASSED', ('%d tests failed; first: %s' % (len(fails), fails[0]) if fails else last), time.time() - t0
    finally: shutil.rmtree(d, ignore_errors=True)
if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=WORKERS) as ex: res = list(ex.map(one, enumerate(M)))
    lines = ['%-9s %-62s %-15s %4.0f s   %s' % ('' if r[1] == 'control' else 'fault %d' % r[0], r[1], r[2], r[4], r[3]) for r in res]
    planted = [r for r in res if r[1] != 'control' and r[2] != 'NOT PLANTED']; noticed = [r for r in planted if r[2] == 'noticed']
    lines.append('%d faults planted, %d noticed, %d passed every test, %d could not be planted; the control %s' % (len(planted), len(noticed), len(planted) - len(noticed), sum(1 for r in res if r[2] == 'NOT PLANTED'), res[0][2]))
    open(os.path.join(HERE, 'pmutants.out'), 'w').write('\n'.join(lines) + '\n'); print('\n'.join(lines))
