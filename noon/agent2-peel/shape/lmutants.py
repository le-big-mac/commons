"""lmutants.py: plant one fault at a time in a copy of study3.py and see whether ltest.py notices.   python -I lmutants.py [WORKERS]
The first copy has no fault and must pass (the control). Writes lmutants.out."""
import os, shutil, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); PY = sys.executable; WORKERS = int(sys.argv[1]) if len(sys.argv) > 1 else 2
M = [('control', [])]
def m(name, *pairs): M.append((name, list(pairs)))
m('r from the variance over the mean, not its square', ("'r': v * n / m ** 2 / LINE,", "'r': v * n / m / LINE,"))
m('r over the figure for clouds left to chance', ("LINE = (4 / 3.0 * theory.D - theory.DC) / theory.ALPHA ** 2", "LINE = (4 / 3.0 * theory.D) / theory.ALPHA ** 2"))
m('the line fitted against n^(-1/2)', ("x = np.array([n ** (-1 / 3.0) for n in sizes]);", "x = np.array([n ** (-1 / 2.0) for n in sizes]);"))
m('the fit takes in the 3,000-point clouds', ("FIT = (10000, 30000, 100000, 300000)", "FIT = (3000, 10000, 30000, 100000, 300000)"))
m('the fit leaves out the 300,000-point clouds', ("FIT = (10000, 30000, 100000, 300000)", "FIT = (10000, 30000, 100000)"))
m('the fit without weights', ("w = np.array([1 / R[n]['rse'] ** 2 for n in sizes])", "w = np.array([1.0 for n in sizes])"))
m('slope and value for many points changed over', ("return float(s), float(math.sqrt(S / d)), float(a), float(math.sqrt(Sxx / d)),", "return float(a), float(math.sqrt(Sxx / d)), float(s), float(math.sqrt(S / d)),"))
m('the slope\'s sign turned', ("s = (S * Sxy - Sx * Sy) / d;", "s = -(S * Sxy - Sx * Sy) / d;"))
m('L1 open: any slope below +0.32', ("bool(F4[0] <= -0.32)", "bool(F4[0] <= 0.32)"))
m('L2 from the 30,000-point clouds', ("None if rr(10000) is None else bool(rr(10000)[0] <= 0.994)", "None if rr(30000) is None else bool(rr(30000)[0] <= 0.994)"))
m('L3 open at the top', ("bool(0.994 <= rr(100000)[0] <= 1.010)", "bool(0.994 <= rr(100000)[0] <= 1.10)"))
m('L4 from the 100,000-point clouds', ("None if rr(300000) is None else bool(rr(300000)[0] >= 1.004)", "None if rr(100000) is None else bool(rr(100000)[0] >= 1.004)"))
m('L5 from the 10,000-point clouds', ("None if rr(3000) is None else bool(rr(3000)[0] <= 0.985)", "None if rr(10000) is None else bool(rr(10000)[0] <= 0.985)"))
m('L6 open at the top', ("bool(all(0.03 <= e <= 0.17 for e in ex))", "bool(all(0.03 <= e <= 1.7 for e in ex))"))
m('L6 holds if any one size does', ("bool(all(0.03 <= e <= 0.17 for e in ex))", "bool(any(0.03 <= e <= 0.17 for e in ex))"))
m('L7 open at the bottom', ("bool(1.008 <= F4[2] <= 1.028)", "bool(0.908 <= F4[2] <= 1.028)"))
m('L7 judged on the slope', ("bool(1.008 <= F4[2] <= 1.028)", "bool(1.008 <= F4[0] <= 1.028)"))
m('a size a tenth short still counts', ("if x is None or len(x) < 0.999 * K0: R[n] = None; continue", "if x is None or len(x) < 0.5 * K0: R[n] = None; continue"))
m('held and failed the wrong way round', ("out['lines'][tag] = {'verdict': 'held' if ok else 'failed', 'odds': odds, 'detail': detail}", "out['lines'][tag] = {'verdict': 'failed' if ok else 'held', 'odds': odds, 'detail': detail}"))
m('the mean\'s excess against the formula with exponent 0.66', ("tm = theory.predictions('disc', n)['mean']", "tm = theory.ALPHA * (n / math.pi) ** 0.66 * 0.75"))
def one(job):
    i, (name, pairs) = job; d = '/dev/shm/agent2-lmut-%d-%d' % (os.getpid(), i); os.makedirs(d); t0 = time.time()
    try:
        for x in ('study3.py', 'theory.py', 'theory.json', 'fresh.py'): shutil.copy(os.path.join(HERE, x), d)
        s = open(os.path.join(d, 'study3.py')).read()
        for a, b in pairs:
            if s.count(a) != 1: return i, name, 'NOT PLANTED', 'the text to change was found %d times' % s.count(a), 0
            s = s.replace(a, b)
        open(os.path.join(d, 'study3.py'), 'w').write(s)
        try: r = subprocess.run(['nice', '-n', '19', PY, '-I', os.path.join(HERE, 'ltest.py'), os.path.join(d, 'study3.py')], capture_output=True, text=True, timeout=1500); rc, out = r.returncode, r.stdout
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
    open(os.path.join(HERE, 'lmutants.out'), 'w').write('\n'.join(lines) + '\n'); print('\n'.join(lines))
