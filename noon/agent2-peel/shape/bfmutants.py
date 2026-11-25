"""bfmutants.py: plant one fault at a time in a copy of the fourth plate's script, bfig.py, draw the plate with it and see whether
bfigtest.py notices.   python -I bfmutants.py [WORKERS]    The first copy has no fault and must pass (the control). Writes bfmutants.out."""
import os, shutil, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); PY = sys.executable; WORKERS = int(sys.argv[1]) if len(sys.argv) > 1 else 3
M = [('control', [])]
def m(name, *pairs): M.append((name, list(pairs)))
m('the dots one error too high', ("(n, fx(x), fy(r), col, SURF,", "(n, fx(x), fy(r + se), col, SURF,"))
m('the bars two errors long each way', ("(n, fx(x), fy(r - se), fx(x), fy(r + se), col))", "(n, fx(x), fy(r - 2 * se), fx(x), fy(r + 2 * se), col))"))
m('the bars three pixels to the side of their dots', ("(n, fx(x), fy(r - se), fx(x), fy(r + se), col))", "(n, fx(x) + 3, fy(r - se), fx(x) + 3, fy(r + se), col))"))
m('the dots placed at n^(-1/2)', ("    x = n ** (-1 / 3.0); r, se, K, sheet = J['sizes'][str(n)]", "    x = n ** (-1 / 2.0) * 2; r, se, K, sheet = J['sizes'][str(n)]"))
m('the ticks along the foot placed at n^(-1/2)', ("x = 0.0 if n is None else n ** (-1 / 3.0); out.append('<line class=\"tick\"", "x = 0.0 if n is None else n ** (-1 / 2.0) * 2; out.append('<line class=\"tick\""))
m('"very many" a little way in from the edge', ("x = 0.0 if n is None else n ** (-1 / 3.0); out.append('<line class=\"tick\"", "x = 0.01 if n is None else n ** (-1 / 3.0); out.append('<line class=\"tick\""))
m('the colours of the two sheets changed over', ("col = ORANGE if sheet == 4 else BLUE", "col = ORANGE if sheet == 3 else BLUE"))
m('the dots over n^0.34, not the theory\'s n^(1/3)', ("J = {'sizes': {str(n): [S[n]['v'] / S[n]['tv'],", "J = {'sizes': {str(n): [S[n]['v'] / (CTH * n ** 0.34),"))
m('the dots are r (the mean squared under them), not the variance over the theory\'s', ("J = {'sizes': {str(n): [S[n]['v'] / S[n]['tv'],", "J = {'sizes': {str(n): [S[n]['v'] / S[n]['tv'] * (1.3259 * S[n]['X'] / S[n]['m']) ** 2,"))
m('the tick labels up the side one step out', ("fill=\"%s\" text-anchor=\"end\">%.2f</text>' % (v, X0 - 8, fy(v) + 4, MUTED, v))", "fill=\"%s\" text-anchor=\"end\">%.2f</text>' % (v, X0 - 8, fy(v) + 4, MUTED, v + 0.02))"))
m('the theory\'s line at 1.01', ("fx(XLO), fy(1.0), fx(XHI), fy(1.0), MUTED))", "fx(XLO), fy(1.01), fx(XHI), fy(1.01), MUTED))"))
m('the third sheet\'s line with half its slope', ("fx(XLO), fy(a3), fx(XHI), fy(a3 + s3 * XHI), MUTED, a3, s3))", "fx(XLO), fy(a3), fx(XHI), fy(a3 + 0.5 * s3 * XHI), MUTED, a3, s3))"))
m('the third sheet\'s line from the theory\'s coefficient', ("'third': [study4.C5 / CTH, study4.B5 / CTH]", "'third': [1.0, study4.B5 / CTH]"))
m('the solid line fitted with a third term and drawn as if straight', ("b, e, chi, dof = after4.series(S, SIZES, 2)", "b, e, chi, dof = after4.series(S, SIZES, 3)"))
m('the solid line fitted to the five large sizes only', ("b, e, chi, dof = after4.series(S, SIZES, 2)", "b, e, chi, dof = after4.series(S, [n for n in SIZES if n >= 3000], 2)"))
m('the solid line drawn on past 100 points to the edge', ("fx(0), fy(a), fx(lo ** (-1 / 3.0)), fy(a + s * lo ** (-1 / 3.0)), INK, b[0], b[1], a, s))", "fx(0), fy(a), fx(XHI), fy(a + s * XHI), INK, b[0], b[1], a, s))"))
m('the dot at the line\'s end one error too high', ("(fx(0), fy(a), INK, SURF, a, J['fit']['a_se']))", "(fx(0), fy(a + J['fit']['a_se']), INK, SURF, a, J['fit']['a_se']))"))
m('the figures beside the line\'s end give the constant\'s error', ("T(fx(0) + 10, fy(a) - 12, '%.4f (%.4f)' % (a, J['fit']['a_se']), 11, INK2)", "T(fx(0) + 10, fy(a) - 12, '%.4f (%.4f)' % (a, J['fit']['b_se']), 11, INK2)"))
m('the equation on the plate with the theory\'s coefficient', ("'variance = %.4f&#183;n^(1/3) &#8722; %.3f' % (b[0], -b[1])", "'variance = %.4f&#183;n^(1/3) &#8722; %.3f' % (CTH, -b[1])"))
m('the title says "from 300 points"', ("lo, hi = min(SIZES), max(SIZES)\n", "lo, hi = min(SIZES), max(SIZES); lo_t = 300\n"), ("fits from %s points to %s' % (100 * (b[0] / CTH - 1), -b[1], format(lo, ','), format(hi, ','))", "fits from %s points to %s' % (100 * (b[0] / CTH - 1), -b[1], format(lo_t, ','), format(hi, ','))"))
m('the line under the title gives errors half their size', ("% (min(ses), max(ses)), 12, INK2)", "% (min(ses) / 2, max(ses) / 2), 12, INK2)"))
m('the key\'s orange dot named as the third sheet\'s', ("T(238, 102, 'the fourth sheet&#8217;s discs', 12, INK2)", "T(238, 102, 'the third sheet&#8217;s discs', 12, INK2)"))
m('the title kept whatever the fit says', ("if len(SIZES) == 8 and chi <= 16.8 and -0.050 <= b[1] <= -0.035: title", "if True: title"), ("b, e, chi, dof = after4.series(S, SIZES, 2)", "b, e, chi, dof = after4.series(S, SIZES, 2); b[1] = -0.02"))
m('the title\'s "steeper" taken from the third sheet\'s line', ("fits from %s points to %s' % (100 * (b[0] / CTH - 1), -b[1],", "fits from %s points to %s' % (100 * (study4.C5 / CTH - 1), -b[1],"))
def one(job):
    i, (name, pairs) = job; d = '/dev/shm/agent2-bfmut-%d-%d' % (os.getpid(), i); os.makedirs(d); t0 = time.time()
    try:
        for x in ('bfig.py', 'bfigtest.py', 'study3.py', 'study4.py', 'after4.py', 'theory.py', 'theory.json', 'fresh.py', 'expectations-4.md'): shutil.copy(os.path.join(HERE, x), d)
        s = open(os.path.join(d, 'bfig.py')).read()
        for a, b in pairs:
            if s.count(a) != 1: return i, name, 'NOT PLANTED', 'the text to change was found %d times' % s.count(a), 0
            s = s.replace(a, b)
        open(os.path.join(d, 'bfig.py'), 'w').write(s); env = dict(os.environ, SHAPE_AFTER=os.path.join(HERE, 'runs-after'))
        r = subprocess.run(['nice', '-n', '19', PY, '-I', 'bfig.py'], cwd=d, env=env, capture_output=True, text=True, timeout=900)
        if r.returncode != 0: return i, name, 'noticed' if pairs else 'CONTROL FAILED', 'the script does not run', time.time() - t0
        r = subprocess.run(['nice', '-n', '19', PY, '-I', 'bfigtest.py'], cwd=d, env=env, capture_output=True, text=True, timeout=900); out = r.stdout
        fails = [l[6:120] for l in out.split('\n') if l.startswith('FAIL')]; last = out.strip().split('\n')[-1] if out.strip() else 'no output'
        if not pairs: return i, name, 'control passed' if r.returncode == 0 else 'CONTROL FAILED', last, time.time() - t0
        return i, name, 'noticed' if r.returncode != 0 else 'PASSED', ('%d tests failed; first: %s' % (len(fails), fails[0]) if fails else last), time.time() - t0
    finally: shutil.rmtree(d, ignore_errors=True)
if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=WORKERS) as ex: res = list(ex.map(one, enumerate(M)))
    lines = ['%-9s %-72s %-15s %4.0f s   %s' % ('' if r[1] == 'control' else 'fault %d' % r[0], r[1], r[2], r[4], r[3]) for r in res]
    planted = [r for r in res if r[1] != 'control' and r[2] != 'NOT PLANTED']; noticed = [r for r in planted if r[2] == 'noticed']
    lines.append('%d faults planted, %d noticed, %d passed every test, %d could not be planted; the control %s' % (len(planted), len(noticed), len(planted) - len(noticed), sum(1 for r in res if r[2] == 'NOT PLANTED'), res[0][2]))
    open(os.path.join(HERE, 'bfmutants.out'), 'w').write('\n'.join(lines) + '\n'); print('\n'.join(lines))
