"""floormutants.py: plant one fault at a time in a copy of floor.py or of study2.py and see whether floortest.py notices.
python -I floormutants.py [WORKERS]     The first copy has no fault and must pass (the control). Writes floormutants.out."""
import os, shutil, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); PY = sys.executable; WORKERS = int(sys.argv[1]) if len(sys.argv) > 1 else 4
M = [('control', None, [])]
def m(name, f, *pairs): M.append((name, f, list(pairs)))
F, S = 'floor.py', 'study2.py'
m('polygon: where a line crosses a side, reckoned wrongly', F, ("t = da / (da - db); Q.append", "t = da / (da + db); Q.append"))
m('polygon: the line\'s direction taken as (cos, cos)', F, ("da, db = a[0] * NX[k] + a[1] * NY[k] - h[k], b[0] * NX[k] + b[1] * NY[k] - h[k]", "da, db = a[0] * NX[k] + a[1] * NX[k] - h[k], b[0] * NX[k] + b[1] * NX[k] - h[k]"))
m('polygon: the last line is left out', F, ("    for k in range(NDIR):\n        Q = []; n = len(P)", "    for k in range(NDIR - 1):\n        Q = []; n = len(P)"))
m('polygon: a set that the starting box bounds, and not the lines, is accepted', F, ("or max(max(abs(p[0]), abs(p[1])) for p in out) > 49: return None", "or max(max(abs(p[0]), abs(p[1])) for p in out) > 490: return None"))
m('describe: scaled by pi over the area, not its square root', F, ("s = math.sqrt(math.pi / A); P = ", "s = math.pi / A; P = "))
m('describe: a side\'s normal pointing inward', F, ("d = math.degrees(math.atan2(-(b[0] - a[0]), b[1] - a[1])) % 360.0", "d = math.degrees(math.atan2((b[0] - a[0]), -(b[1] - a[1]))) % 360.0"))
m('describe: the rounding read from the wrong number', F, ("rho = float(np.exp(x[NDIR]));", "rho = float(np.exp(x[NDIR - 1]));"))
m('describe: widths without the rounding', F, ("- min(p[0] * NX[k] + p[1] * NY[k] for p in P) + 2 * rho for k in range(NDIR // 2)]", "- min(p[0] * NX[k] + p[1] * NY[k] for p in P) for k in range(NDIR // 2)]"))
m('describe: the narrowest over the widest', F, ("'aspect': max(w) / min(w)}", "'aspect': min(w) / max(w)}"))
m('Q_of: long thin shapes are not refused', F, ("or d['aspect'] > 3: return 2.0", "or d['aspect'] > 30: return 2.0"))
m('Q_of: any rounding is allowed', F, ("or not (1e-3 <= d['rho'] <= 1.5) or", "or not (1e-9 <= d['rho'] <= 150) or"))
m('Q_of: not carried to the limit', F, ("    v = 2 * out[1] - out[0]\n", "    v = out[1]\n"))
m('Q_of: the rounding is not passed to the flow', F, ("'-q', q, '-rho0', '%.10f' % d['rho']],", "'-q', q],"))
m('Q_of: the area taken as pi', F, ("out.append(o['I_edge'] * o['area'] / o['T'] ** 2)", "out.append(o['I_edge'] * math.pi / o['T'] ** 2)"))
m('Q_of: the rounding doubled', F, ("'-rho0', '%.10f' % d['rho']],", "'-rho0', '%.10f' % (2 * d['rho'])],"))
m('the starting triangle is not equilateral', F, ("h[[2, 10, 18]] = 1.0        #", "h[[2, 10, 17]] = 1.0        #"))
m('cma: the mean moves away from the best', F, ("ysel = Y[order[:mu]]; yw = w @ ysel; m = m + sigma * yw", "ysel = Y[order[:mu]]; yw = w @ ysel; m = m - sigma * yw"))
m('cma: the worst half is selected', F, ("f = np.array(list(pool.map(Q_of, X))); order = np.argsort(f)", "f = np.array(list(pool.map(Q_of, X))); order = np.argsort(-f)"))
m('cma: the step never changes', F, ("        sigma *= math.exp((cs / damps) * (np.linalg.norm(ps) / chiN - 1))\n", ""))
m('cma: the step grows when it should shrink', F, ("sigma *= math.exp((cs / damps) * (np.linalg.norm(ps) / chiN - 1))", "sigma *= math.exp((cs / damps) * (1 - np.linalg.norm(ps) / chiN))"))
m('cma: it never stops early', F, ("        else: since += 1\n", "        else: since += 0\n"))
m('cma: it stops after three generations without gain', F, ("        if since >= 30: break", "        if since >= 3: break"))
m('cma: the seed is not used', F, ("rng = np.random.default_rng(seed); n = len(x0); mu = lam // 2;", "rng = np.random.default_rng(); n = len(x0); mu = lam // 2;"))
m('cma: the best is the last generation\'s, not the best of all', F, ("        if f[order[0]] < best[0]: best = (float(f[order[0]]), X[order[0]].copy())", "        best = (float(f[order[0]]), X[order[0]].copy())"))
m('cma: the shapes tried are not the ones scored', F, ("Y = (Z * D) @ B.T; X = m + sigma * Y", "Y = (Z * D) @ B.T; X = m + sigma * Y[::-1]"))
m('study2: A1 open at the top', S, ("together(ALL), 0.996, 1.008)", "together(ALL), 0.996, 1.08)"))
m('study2: A1 open at the bottom', S, ("together(ALL), 0.996, 1.008)", "together(ALL), 0.96, 1.008)"))
m('study2: A2 compares the sizes', S, ("0.90, diff(together(['cloud.c, 100,000', 'cloud.c, 30,000']), together(['numpy, 100,000', 'numpy, 30,000'])), -0.010, 0.010)", "0.90, diff(together(['cloud.c, 100,000', 'numpy, 100,000']), together(['cloud.c, 30,000', 'numpy, 30,000'])), -0.010, 0.010)"))
m('study2: A3 compares the generators', S, ("0.85, diff(together(['cloud.c, 100,000', 'numpy, 100,000']), together(['cloud.c, 30,000', 'numpy, 30,000'])), -0.010, 0.010)", "0.85, diff(together(['cloud.c, 100,000', 'cloud.c, 30,000']), together(['numpy, 100,000', 'numpy, 30,000'])), -0.010, 0.010)"))
m('study2: A4 from numpy\'s set', S, ("0.70, together(['cloud.c, 100,000']), 0.992, 1.012)", "0.70, together(['numpy, 100,000']), 0.992, 1.012)"))
m('study2: A4 open at the top', S, ("0.70, together(['cloud.c, 100,000']), 0.992, 1.012)", "0.70, together(['cloud.c, 100,000']), 0.992, 1.12)"))
m('study2: a set a sixth short still counts', S, ("if x is None or len(x) < 0.999 * ASKED: R[key] = None; continue", "if x is None or len(x) < 0.5 * ASKED: R[key] = None; continue"))
m('study2: r over the ceiling, not over the quarter disc\'s line', S, ("def line_of(n): p = theory.predictions('quarter', n); return p['exact'] / p['mean'] ** 2 * n, p", "def line_of(n): p = theory.predictions('quarter', n); return (4 / 3.0 * theory.D - theory.DC) / theory.ALPHA ** 2, p"))
m('study2: r from the variance over the mean, not its square', S, ("'r': v * n / m ** 2 / ln, 'rse'", "'r': v * n / m / ln, 'rse'"))
m('study2: B1\'s floor at 1.30', S, ("bool(best['fine_Q'] >= 1.3040)", "bool(best['fine_Q'] >= 1.30)"))
m('study2: the least taken at 240 angles', S, ("best = min((r for r in fl if 'fine_Q' in r), key=lambda r: r['fine_Q']);", "best = min((r for r in fl if 'fine_Q' in r), key=lambda r: r['best_Q']);"))
m('study2: every side counts, however short', S, ("big = [(a, L / per) for a, L in d['sides'] if L / per > 0.03];", "big = [(a, L / per) for a, L in d['sides'] if L / per > 0.0];"))
m('study2: B3 open at the top', S, ("(bool(0.15 <= d['rho'] <= 0.35) if len(big) == 3 else None)", "(bool(0.15 <= d['rho'] <= 3.5) if len(big) == 3 else None)"))
m('study2: B3 judged even when the shape is no triangle', S, ("(bool(0.15 <= d['rho'] <= 0.35) if len(big) == 3 else None)", "bool(0.15 <= d['rho'] <= 0.35)"))
m('study2: B4 counts all eight starts', S, ("if r['seed'] >= 4 and r['best_Q'] <= low240 + 0.002]", "if r['seed'] >= 1 and r['best_Q'] <= low240 + 0.002]"))
m('study2: B4 within 0.02', S, ("if r['seed'] >= 4 and r['best_Q'] <= low240 + 0.002]", "if r['seed'] >= 4 and r['best_Q'] <= low240 + 0.02]"))
m('study2: an unfinished search is scored', S, ("done = fl is not None and len(fl) == 8 and sum(1 for r in fl if 'fine_Q' in r) == 5", "done = fl is not None and len(fl) == 8"))
m('study2: held and failed the wrong way round', S, ("dict({'verdict': 'held' if ok else 'failed', 'odds': odds, 'detail': detail})", "dict({'verdict': 'failed' if ok else 'held', 'odds': odds, 'detail': detail})"))
def one(job):
    i, (name, f, pairs) = job; d = '/dev/shm/agent2-fmut-%d-%d' % (os.getpid(), i); os.makedirs(d); t0 = time.time()
    try:
        for x in ('floor.py', 'study2.py', 'theory.py', 'theory.json', 'fresh.py', 'flow'): shutil.copy(os.path.join(HERE, x), d)
        if f:
            s = open(os.path.join(d, f)).read()
            for a, b in pairs:
                if s.count(a) != 1: return i, name, 'NOT PLANTED', 'the text to change was found %d times' % s.count(a), 0
                s = s.replace(a, b)
            open(os.path.join(d, f), 'w').write(s)
        try: r = subprocess.run(['nice', '-n', '19', PY, '-I', os.path.join(HERE, 'floortest.py'), d], capture_output=True, text=True, timeout=1500); rc, out = r.returncode, r.stdout
        except subprocess.TimeoutExpired: rc, out = -9, ''
        fails = [l[6:110] for l in out.split('\n') if l.startswith('FAIL')]; last = out.strip().split('\n')[-1] if out.strip() else 'no output (it ran past its time or fell over)'
        if not f: return i, name, 'control passed' if rc == 0 else 'CONTROL FAILED', last, time.time() - t0
        return i, name, 'noticed' if rc != 0 else 'PASSED', ('%d tests failed; first: %s' % (len(fails), fails[0]) if fails else last), time.time() - t0
    finally: shutil.rmtree(d, ignore_errors=True)
if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=WORKERS) as ex: res = list(ex.map(one, enumerate(M)))
    lines = ['%-9s %-74s %-15s %4.0f s   %s' % ('' if r[1] == 'control' else 'fault %d' % r[0], r[1], r[2], r[4], r[3]) for r in res]
    planted = [r for r in res if r[1] != 'control' and r[2] != 'NOT PLANTED']; noticed = [r for r in planted if r[2] == 'noticed']
    lines.append('%d faults planted, %d noticed, %d passed every test, %d could not be planted; the control %s' % (len(planted), len(noticed), len(planted) - len(noticed), sum(1 for r in res if r[2] == 'NOT PLANTED'), res[0][2]))
    open(os.path.join(HERE, 'floormutants.out'), 'w').write('\n'.join(lines) + '\n'); print('\n'.join(lines))
