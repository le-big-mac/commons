"""q5mutants.py: plant one fault at a time in a copy of study5.py (tried by qtest.py) or of study5b.py (tried by q5btest.py) and see
whether the test notices.   python -I q5mutants.py [WORKERS]
The first two copies have no fault and must pass (the controls). Writes q5mutants.out."""
import os, shutil, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); PY = sys.executable; WORKERS = int(sys.argv[1]) if len(sys.argv) > 1 else 3
M = [('control', 'study5.py', []), ('control', 'study5b.py', [])]
def m(name, *pairs): M.append((name, 'study5.py', list(pairs)))
def mb(name, *pairs): M.append((name, 'study5b.py', list(pairs)))
m('the small discs\' B with the theory\'s coefficient', ("LAT = (83, 90, 98, 105, 113, 120); C5 = 0.08227;", "LAT = (83, 90, 98, 105, 113, 120); C5 = 0.08068;"))
m('the shapes\' B with the theory itself, not 1.0197 of it', ("RATIO = 1.0197;", "RATIO = 1.0;"))
m('the shapes\' B with the disc\'s theory for every shape', ("p = theory.predictions(shape, n)", "p = theory.predictions('disc', n)"))
m('Z the other way up', ("(Bl[90] + Bl[105] + Bl[120]) / 3 - (Bl[83] + Bl[98] + Bl[113]) / 3 >= 0.008)", "(Bl[83] + Bl[98] + Bl[113]) / 3 - (Bl[90] + Bl[105] + Bl[120]) / 3 >= 0.008)"))
m('Z with no margin', ("(Bl[90] + Bl[105] + Bl[120]) / 3 - (Bl[83] + Bl[98] + Bl[113]) / 3 >= 0.008)", "(Bl[90] + Bl[105] + Bl[120]) / 3 - (Bl[83] + Bl[98] + Bl[113]) / 3 >= -0.008)"))
m('Z from two sizes a side', ("(Bl[90] + Bl[105] + Bl[120]) / 3 - (Bl[83] + Bl[98] + Bl[113]) / 3 >= 0.008)", "(Bl[90] + Bl[105]) / 3 - (Bl[83] + Bl[98]) / 3 >= 0.008)"))
m('Q2 holds if any one size is near', ("bool(all(abs(Bl[n] - PRED[n]) <= 0.004 for n in LAT))", "bool(any(abs(Bl[n] - PRED[n]) <= 0.004 for n in LAT))"))
m('Q2 within 0.04', ("bool(all(abs(Bl[n] - PRED[n]) <= 0.004 for n in LAT))", "bool(all(abs(Bl[n] - PRED[n]) <= 0.04 for n in LAT))"))
m('Q2 against the swing at the wrong sizes (the list turned round)', ("PRED = {83: -0.0467, 90: -0.0294, 98: -0.0450, 105: -0.0320, 113: -0.0435, 120: -0.0346}", "PRED = {120: -0.0467, 113: -0.0294, 105: -0.0450, 98: -0.0320, 90: -0.0435, 83: -0.0346}"))
m('Q3 within 0.06', ("bool(abs(Bc - OWN[1000]) <= 0.006)", "bool(abs(Bc - OWN[1000]) <= 0.06)"))
m('Q3 against the 300-point disc', ("bool(abs(Bc - OWN[1000]) <= 0.006)", "bool(abs(Bc - OWN[300]) <= 0.006)"))
m('Q4 with the band at nought', ("bool(Bt[1000] - Bc <= -0.020)", "bool(Bt[1000] - Bc <= 0.0)"))
m('Q4 on the rounded triangle', ("bool(Bt[1000] - Bc <= -0.020)", "bool(Br[1000] - Bc <= -0.020)"))
m('Q5 open below', ("bool(abs(Bt[1000] - Bc) <= 0.006)", "bool(Bt[1000] - Bc <= 0.006)"))
m('Q6 against the control disc', ("bool(Bt[1000] - Br[1000] <= -0.012)", "bool(Bt[1000] - Bc <= -0.012)"))
m('Q6 the other way round', ("bool(Bt[1000] - Br[1000] <= -0.012)", "bool(Br[1000] - Bt[1000] <= -0.012)"))
m('Q7 open below', ("bool(abs(Br[1000] - Bc) <= 0.008)", "bool(Br[1000] - Bc <= 0.008)"))
m('Q8 on the 1,000-point triangles', ("bool(Bt[300] <= OWN[300] - 0.015) if has(Bt, [300])", "bool(Bt[1000] <= OWN[300] - 0.015) if has(Bt, [1000])"))
m('Q9 without its 0.015', ("bool(Bt[3000] <= OWN[3000] - 0.015)", "bool(Bt[3000] <= OWN[3000])"))
m('Q8 and Q9 from the rounded triangle', ("bool(Bt[300] <= OWN[300] - 0.015) if has(Bt, [300])", "bool(Br[300] <= OWN[300] - 0.015) if has(Br, [300])"), ("bool(Bt[3000] <= OWN[3000] - 0.015) if has(Bt, [3000])", "bool(Br[3000] <= OWN[3000] - 0.015) if has(Br, [3000])"))
m('a file a thirtieth short still counts', ("if x is None or len(x) < 0.999 * K0: R[key] = None; continue", "if x is None or len(x) < 0.9 * K0: R[key] = None; continue"))
m('held and failed the wrong way round', ("out['lines'][tag] = {'verdict': 'held' if ok_ else 'failed', 'odds': odds, 'detail': detail[tag]}", "out['lines'][tag] = {'verdict': 'failed' if ok_ else 'held', 'odds': odds, 'detail': detail[tag]}"))
mb('Q10 open below', ("bool(-0.020 <= fig['Q10'] <= -0.006)", "bool(fig['Q10'] <= -0.006)"))
mb('Q10 open above', ("bool(-0.020 <= fig['Q10'] <= -0.006)", "bool(-0.020 <= fig['Q10'])"))
mb('Q10 against the rounded triangle', ("fig['Q10'] = Bt[1000] - Bc;", "fig['Q10'] = Bt[1000] - Br[1000];"))
mb('Q11 and Q12 at the same size', ("for tag, n in (('Q11', 1000), ('Q12', 300)):", "for tag, n in (('Q11', 1000), ('Q12', 1000)):"))
mb('Q11 and Q12 the other way round', ("fig[tag] = Bt[n] - Br[n]; out[tag] = bool(fig[tag] <= -0.008)", "fig[tag] = Br[n] - Bt[n]; out[tag] = bool(fig[tag] <= -0.008)"))
mb('Q11 and Q12 with the band at -0.0005', ("fig[tag] = Bt[n] - Br[n]; out[tag] = bool(fig[tag] <= -0.008)", "fig[tag] = Bt[n] - Br[n]; out[tag] = bool(fig[tag] <= -0.0005)"))
mb('Q13 without weights', ("w = {n: 1 / (Et[n] ** 2 + Er[n] ** 2) for n in (300, 1000, 3000)};", "w = {n: 1.0 for n in (300, 1000, 3000)};"))
mb('Q13 from two sizes', ("w = {n: 1 / (Et[n] ** 2 + Er[n] ** 2) for n in (300, 1000, 3000)};", "w = {n: 1 / (Et[n] ** 2 + Er[n] ** 2) for n in (300, 1000)};"))
mb('Q13 weighted by the errors, not their squares', ("w = {n: 1 / (Et[n] ** 2 + Er[n] ** 2) for n in (300, 1000, 3000)};", "w = {n: 1 / (Et[n] + Er[n]) for n in (300, 1000, 3000)};"))
mb('Q13 with the band at -0.004', ("out['Q13'] = bool(fig['Q13'] <= -0.008)", "out['Q13'] = bool(fig['Q13'] <= -0.004)"))
def one(job):
    i, (name, target, pairs) = job; d = '/dev/shm/agent2-q5mut-%d-%d' % (os.getpid(), i); os.makedirs(d); t0 = time.time(); test = 'qtest.py' if target == 'study5.py' else 'q5btest.py'
    try:
        for x in ('study5.py', 'study5b.py', 'theory.py', 'theory.json', 'fresh.py'): shutil.copy(os.path.join(HERE, x), d)
        s = open(os.path.join(d, target)).read()
        for a, b in pairs:
            if s.count(a) != 1: return i, name, target, 'NOT PLANTED', 'the text to change was found %d times' % s.count(a), 0
            s = s.replace(a, b)
        open(os.path.join(d, target), 'w').write(s)
        try: r = subprocess.run(['nice', '-n', '19', PY, '-I', os.path.join(HERE, test), os.path.join(d, target)], capture_output=True, text=True, timeout=1800, env=dict(os.environ, SHAPE_AFTER=os.path.join(HERE, 'runs-after'))); rc, out = r.returncode, r.stdout
        except subprocess.TimeoutExpired: rc, out = -9, ''
        fails = [l[6:110] for l in out.split('\n') if l.startswith('FAIL')]; last = out.strip().split('\n')[-1] if out.strip() else 'no output'
        if not pairs: return i, name, target, 'control passed' if rc == 0 else 'CONTROL FAILED', last, time.time() - t0
        return i, name, target, 'noticed' if rc != 0 else 'PASSED', ('%d cases failed; first: %s' % (len(fails), fails[0]) if fails else last), time.time() - t0
    finally: shutil.rmtree(d, ignore_errors=True)
if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=WORKERS) as ex: res = list(ex.map(one, enumerate(M)))
    lines = ['%-9s %-11s %-62s %-15s %4.0f s   %s' % ('' if r[1] == 'control' else 'fault %d' % (r[0] - 1), r[2], r[1], r[3], r[5], r[4]) for r in res]
    planted = [r for r in res if r[1] != 'control' and r[3] != 'NOT PLANTED']; noticed = [r for r in planted if r[3] == 'noticed']; ctl = [r[3] for r in res if r[1] == 'control']
    lines.append('%d faults planted, %d noticed, %d passed every case, %d could not be planted; the controls %s' % (len(planted), len(noticed), len(planted) - len(noticed), sum(1 for r in res if r[3] == 'NOT PLANTED'), 'both passed' if ctl == ['control passed'] * 2 else 'DID NOT BOTH PASS'))
    open(os.path.join(HERE, 'q5mutants.out'), 'w').write('\n'.join(lines) + '\n'); print('\n'.join(lines))
