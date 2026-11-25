"""p4mutants.py: plant one fault at a time in a copy of study4.py and see whether ptest.py notices.   python -I p4mutants.py [WORKERS]
The first copy has no fault and must pass (the control). Writes p4mutants.out."""
import os, shutil, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); PY = sys.executable; WORKERS = int(sys.argv[1]) if len(sys.argv) > 1 else 3
M = [('control', [])]
def m(name, *pairs): M.append((name, list(pairs)))
m('B with the theory\'s coefficient, not the third sheet\'s', ("C5, B5 = 0.08227, -0.0473", "C5, B5 = 0.08068, -0.0473"))
m('B with n to the power 0.3', ("'B': v - C5 * n ** (1 / 3.0),", "'B': v - C5 * n ** 0.3,"))
m('the variance about the wrong divisor (K + 1000)', ("vb = (H @ vals ** 2 - K * mb ** 2) / (K - 1);", "vb = (H @ vals ** 2 - K * mb ** 2) / (K - 1); v = v * K / (K + 1000.0);"))
m('the mean\'s excess with T = 0.76', ("tm = 1.3259 * (n / math.pi) ** (2 / 3.0) * 0.75 ", "tm = 1.3259 * (n / math.pi) ** (2 / 3.0) * 0.76 "))
m('the mean\'s excess with alpha = 1.33', ("tm = 1.3259 * (n / math.pi) ** (2 / 3.0) * 0.75 ", "tm = 1.33 * (n / math.pi) ** (2 / 3.0) * 0.75 "))
m('the share at four points counts clouds of two layers', ("'one': float((x == 1).mean()),", "'one': float((x == 2).mean()),"))
m('P0 open at the top', ("bool(0.7020 <= share4 <= 0.7070)", "bool(0.7020 <= share4 <= 0.7770)"))
m('P0 open at the bottom', ("bool(0.7020 <= share4 <= 0.7070)", "bool(0.6020 <= share4 <= 0.7070)"))
m('P1 judged on the 300-point clouds', ("(('P1', 1000), ('P2', 300), ('P3', 100)): out[tag]", "(('P1', 300), ('P2', 300), ('P3', 100)): out[tag]"))
m('P3 judged on the 300-point clouds', ("(('P1', 1000), ('P2', 300), ('P3', 100)): out[tag]", "(('P1', 1000), ('P2', 300), ('P3', 300)): out[tag]"))
m('P1 to P3 open at the bottom', ("bool(-0.057 <= b[n] <= -0.037)", "bool(-0.57 <= b[n] <= -0.037)"))
m('P1 to P3 open at the top', ("bool(-0.057 <= b[n] <= -0.037)", "bool(-0.057 <= b[n] <= 0.037)"))
m('P4 holds if any one size does', ("bool(all(b[n] <= -0.025 for n in NEW))", "bool(any(b[n] <= -0.025 for n in NEW))"))
m('P4 with the band at -0.005', ("bool(all(b[n] <= -0.025 for n in NEW))", "bool(all(b[n] <= -0.005 for n in NEW))"))
m('P5 the other way round', ("bool(b[100] - b[1000] >= 0.004)", "bool(b[1000] - b[100] >= 0.004)"))
m('P5 with no margin', ("bool(b[100] - b[1000] >= 0.004)", "bool(b[100] - b[1000] >= 0.0)"))
m('P6 open at the top', ("bool(0.130 <= ex[1000] <= 0.165)", "bool(0.130 <= ex[1000] <= 0.265)"))
m('P6 judged on the 100-point clouds', ("bool(0.130 <= ex[1000] <= 0.165) if ok(ex.get(1000))", "bool(0.130 <= ex[100] <= 0.165) if ok(ex.get(100))"))
m('P7 at 0.2', ("bool(ex[100] >= 0.245)", "bool(ex[100] >= 0.2)"))
m('P7 judged on the 1,000-point clouds', ("bool(ex[100] >= 0.245) if ok(ex.get(100))", "bool(ex[1000] >= 0.245) if ok(ex.get(1000))"))
m('a file a fortieth short still counts', ("if x is None or len(x) < 0.999 * K0: R[n] = None; continue", "if x is None or len(x) < 0.9 * K0: R[n] = None; continue"))
m('held and failed the wrong way round', ("out['lines'][tag] = {'verdict': 'held' if ok else 'failed', 'odds': odds, 'detail': detail[tag]}", "out['lines'][tag] = {'verdict': 'failed' if ok else 'held', 'odds': odds, 'detail': detail[tag]}"))
def one(job):
    i, (name, pairs) = job; d = '/dev/shm/agent2-p4mut-%d-%d' % (os.getpid(), i); os.makedirs(d); t0 = time.time()
    try:
        for x in ('study4.py', 'theory.py', 'theory.json', 'fresh.py'): shutil.copy(os.path.join(HERE, x), d)
        s = open(os.path.join(d, 'study4.py')).read()
        for a, b in pairs:
            if s.count(a) != 1: return i, name, 'NOT PLANTED', 'the text to change was found %d times' % s.count(a), 0
            s = s.replace(a, b)
        open(os.path.join(d, 'study4.py'), 'w').write(s)
        try: r = subprocess.run(['nice', '-n', '19', PY, '-I', os.path.join(HERE, 'ptest.py'), os.path.join(d, 'study4.py')], capture_output=True, text=True, timeout=1500); rc, out = r.returncode, r.stdout
        except subprocess.TimeoutExpired: rc, out = -9, ''
        fails = [l[6:110] for l in out.split('\n') if l.startswith('FAIL')]; last = out.strip().split('\n')[-1] if out.strip() else 'no output'
        if not pairs: return i, name, 'control passed' if rc == 0 else 'CONTROL FAILED', last, time.time() - t0
        return i, name, 'noticed' if rc != 0 else 'PASSED', ('%d cases failed; first: %s' % (len(fails), fails[0]) if fails else last), time.time() - t0
    finally: shutil.rmtree(d, ignore_errors=True)
if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=WORKERS) as ex: res = list(ex.map(one, enumerate(M)))
    lines = ['%-9s %-62s %-15s %4.0f s   %s' % ('' if r[1] == 'control' else 'fault %d' % r[0], r[1], r[2], r[4], r[3]) for r in res]
    planted = [r for r in res if r[1] != 'control' and r[2] != 'NOT PLANTED']; noticed = [r for r in planted if r[2] == 'noticed']
    lines.append('%d faults planted, %d noticed, %d passed every case, %d could not be planted; the control %s' % (len(planted), len(noticed), len(planted) - len(noticed), sum(1 for r in res if r[2] == 'NOT PLANTED'), res[0][2]))
    open(os.path.join(HERE, 'p4mutants.out'), 'w').write('\n'.join(lines) + '\n'); print('\n'.join(lines))
