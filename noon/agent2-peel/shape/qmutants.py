"""qmutants.py: plant one fault at a time in a copy of the second plate's script, qfig.py, draw the plate with it and see whether
qfigtest.py notices.   python -I qmutants.py [WORKERS]     The first copy has no fault and must pass (the control). Writes qmutants.out."""
import os, shutil, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); PY = sys.executable; WORKERS = int(sys.argv[1]) if len(sys.argv) > 1 else 3
M = [('control', [])]
def m(name, *pairs): M.append((name, list(pairs)))
m('the dots one error too high', ("(x, fy(r['r']), COL[r['maker']], SURF,", "(x, fy(r['r'] + r['se']), COL[r['maker']], SURF,"))
m('the bars two errors long each way', ("(x, fy(r['r'] - r['se']), x, fy(r['r'] + r['se']), COL[r['maker']]))", "(x, fy(r['r'] - 2 * r['se']), x, fy(r['r'] + 2 * r['se']), COL[r['maker']]))"))
m('the two colours changed over', ("COL = {'cloud.c': BLUE, 'numpy': ORANGE}", "COL = {'cloud.c': ORANGE, 'numpy': BLUE}"))
m('the key\'s colours changed over', ("cy=\"100\" r=\"5\" fill=\"%s\"/>' % BLUE)", "cy=\"100\" r=\"5\" fill=\"%s\"/>' % ORANGE)"), ("cy=\"100\" r=\"5\" fill=\"%s\"/>' % ORANGE); T(248", "cy=\"100\" r=\"5\" fill=\"%s\"/>' % BLUE); T(248"))
m('r reckoned over the ceiling, not the quarter disc\'s line', ("LINE = study2.line_of(1e5)[0]; CEIL", "LINE = (4 / 3.0 * theory.D - theory.DC) / theory.ALPHA ** 2; CEIL"))
m('the second chased set left out', ("for key in ('quarter-cloud-a', 'quarter-cloud-b', 'quarter-numpy'):", "for key in ('quarter-cloud-a', 'quarter-numpy'):"))
m('the two halves of the chase drawn as one set', ("for key in ('quarter-cloud-a', 'quarter-cloud-b', 'quarter-numpy'):", "for key in ('quarter-cloud', 'quarter-numpy'):"))
m('the last mark is the two sets of 100,000 only', ("allfour = study2.together(study2.ALL)", "allfour = study2.together(study2.ALL[:2])"))
m('the band drawn from 0.99 to 1.01', ("(xt - 28, fy(1.008), fy(0.996) - fy(1.008), GRID))", "(xt - 28, fy(1.010), fy(0.990) - fy(1.010), GRID))"))
m('the title says "off its line"', ("if 0.996 <= allfour[0] <= 1.008 else", "if not (0.996 <= allfour[0] <= 1.008) else"))
m('the title gives the first set\'s figure', ("sets give %.3f (%.3f)' % (200 * allfour[1], allfour[0], allfour[1])) if 0.996", "sets give %.3f (%.3f)' % (200 * allfour[1], rows[0]['r'], rows[0]['se'])) if 0.996"))
m('the tick labels one step off', ("text-anchor=\"end\">%.2f</text>' % (v, X0 - 8, fy(v) + 4, MUTED, v))", "text-anchor=\"end\">%.2f</text>' % (v, X0 - 8, fy(v) + 4, MUTED, v + 0.02))"))
m('the heavy line drawn at 1.02', ("MUTED if v == 1.0 else GRID, '1.5' if v == 1.0 else '1'))", "MUTED if v == 1.02 else GRID, '1.5' if v == 1.02 else '1'))"))
m('the numbers of clouds under the wrong sets', ("T(x, YB + 22, format(r['K'], ','), 12, INK2, 'middle', cls='xlabel');", "T(x, YB + 22, format(rows[-1]['K'] if r is rows[0] else r['K'], ','), 12, INK2, 'middle', cls='xlabel');"))
m('the sets drawn right to left', ("for r, x in zip(rows, xs):\n    out.append('<g class=\"set\"", "for r, x in zip(rows, xs[::-1]):\n    out.append('<g class=\"set\""))
m('a group\'s name runs off the picture', ("if g2: brace(g2[0], g2[-1], 'the second sheet: sealed before they were peeled')", "if g2: brace(g2[-1] + 150, g2[-1] + 150, 'the second sheet: sealed before they were peeled')"))
m('the sizes are not written under the sets', ("T(x, YB + 37, format(r['n'], ','), 11, MUTED, 'middle', cls='xlabel'); out.append('</g>')", "out.append('</g>')"))
def one(job):
    i, (name, pairs) = job; d = '/dev/shm/agent2-qmut-%d-%d' % (os.getpid(), i); os.makedirs(d); t0 = time.time()
    try:
        for x in ('qfig.py', 'qfigtest.py', 'study.py', 'study2.py', 'theory.py', 'theory.json', 'fresh.py', 'floor.py', 'floor.json'): shutil.copy(os.path.join(HERE, x), d)
        s = open(os.path.join(d, 'qfig.py')).read()
        for a, b in pairs:
            if s.count(a) != 1: return i, name, 'NOT PLANTED', 'the text to change was found %d times' % s.count(a), 0
            s = s.replace(a, b)
        open(os.path.join(d, 'qfig.py'), 'w').write(s); env = dict(os.environ, SHAPE_RUNS=os.path.join(HERE, 'runs'), SHAPE_AFTER=os.path.join(HERE, 'runs-after'), FLOOR=os.path.join(HERE, 'floor.json'))
        r = subprocess.run(['nice', '-n', '19', PY, '-I', 'qfig.py'], cwd=d, env=env, capture_output=True, text=True, timeout=600)
        if r.returncode != 0: return i, name, 'noticed' if pairs else 'CONTROL FAILED', 'the script does not run', time.time() - t0
        r = subprocess.run(['nice', '-n', '19', PY, '-I', 'qfigtest.py'], cwd=d, env=env, capture_output=True, text=True, timeout=600); out = r.stdout
        fails = [l[6:120] for l in out.split('\n') if l.startswith('FAIL')]; last = out.strip().split('\n')[-1] if out.strip() else 'no output'
        if not pairs: return i, name, 'control passed' if r.returncode == 0 else 'CONTROL FAILED', last, time.time() - t0
        return i, name, 'noticed' if r.returncode != 0 else 'PASSED', ('%d tests failed; first: %s' % (len(fails), fails[0]) if fails else last), time.time() - t0
    finally: shutil.rmtree(d, ignore_errors=True)
if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=WORKERS) as ex: res = list(ex.map(one, enumerate(M)))
    lines = ['%-9s %-62s %-15s %4.0f s   %s' % ('' if r[1] == 'control' else 'fault %d' % r[0], r[1], r[2], r[4], r[3]) for r in res]
    planted = [r for r in res if r[1] != 'control' and r[2] != 'NOT PLANTED']; noticed = [r for r in planted if r[2] == 'noticed']
    lines.append('%d faults planted, %d noticed, %d passed every test, %d could not be planted; the control %s' % (len(planted), len(noticed), len(planted) - len(noticed), sum(1 for r in res if r[2] == 'NOT PLANTED'), res[0][2]))
    open(os.path.join(HERE, 'qmutants.out'), 'w').write('\n'.join(lines) + '\n'); print('\n'.join(lines))
