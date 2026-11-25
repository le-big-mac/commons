"""dmutants.py: break dlib.py (what the study computes from the clouds) and dtheory.py (what it sets beside them) on purpose, one
fault at a time, and run ruler.py and dew.py on each broken copy. First a control: an unbroken copy, run by the very same steps,
must pass.     python -I dmutants.py"""
import os, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); WORK = os.path.join(HERE, 'dmutants'); FILES = ['dlib.py', 'dtheory.py', 'ruler.py', 'dew.py']
M = [
 ('ring-mean-without-the-profile-taken-off', 'dlib.py', "d['Q'] = a[:, :, 1] / cnt", "d['Q'] = a[:, :, 2] / cnt"),
 ('round-the-ring-with-the-slope-left-in', 'dlib.py', "d['V'] = (sdd - srd ** 2 / srr) / (cnt - 2)", "d['V'] = sdd / (cnt - 2)"),
 ('parts-without-the-mean-depth-taken-off', 'dlib.py', "c = 2 * (a[:, :, 5 + 4 * m] - dbar * a[:, :, 3 + 4 * m]) / cnt;", "c = 2 * a[:, :, 5 + 4 * m] / cnt;"),
 ('parts-halved-not-quartered', 'dlib.py', "d['P'][m] = (c ** 2 + s ** 2) / 4", "d['P'][m] = (c ** 2 + s ** 2) / 2"),
 ('sine-part-is-the-cosine-part', 'dlib.py', "s = 2 * (a[:, :, 6 + 4 * m] - dbar * a[:, :, 4 + 4 * m]) / cnt;", "s = 2 * (a[:, :, 5 + 4 * m] - dbar * a[:, :, 3 + 4 * m]) / cnt;"),
 ('parts-one-place-along', 'dlib.py', "for m in (1, 2, 3, 4):\n        c = 2 * (a[:, :, 5 + 4 * m]", "for m in (1, 2, 3):\n        c = 2 * (a[:, :, 9 + 4 * m]"),
 ('correlation-of-a-ring-with-itself', 'dlib.py', "def corr(d, r1, r2): return float(np.corrcoef(d['Q'][:, K(r1)], d['Q'][:, K(r2)])[0, 1])", "def corr(d, r1, r2): return float(np.corrcoef(d['Q'][:, K(r1)], d['Q'][:, K(r1)])[0, 1])"),
 ('annulus-one-place-out', 'dlib.py', "def K(r): return int(round(r / 0.05)) - 1", "def K(r): return int(round(r / 0.05))"),
 ('standard-error-of-a-variance-too-small', 'dlib.py', "math.sqrt(2.0 / (len(x) - 1))", "math.sqrt(1.0 / (len(x) - 1))"),
 ('variance-about-nought', 'dlib.py', "def var(x): return float(np.var(x, ddof=1))", "def var(x): return float(np.mean(np.square(x)))"),
 ('predictions-of-the-two-kinds-swapped', 'dlib.py', "def pred_ring(kind, r, n): return th.annulus(th.cov_chance if kind == 'chance' else th.cov_fixed, r, r, n)", "def pred_ring(kind, r, n): return th.annulus(th.cov_fixed if kind == 'chance' else th.cov_chance, r, r, n)"),
 ('predicted-correlation-always-for-chance', 'dlib.py', "c = th.cov_chance if kind == 'chance' else th.cov_fixed; return", "c = th.cov_chance; return"),
 ('theory-tau-with-the-cube-root', 'dtheory.py', "def tau(r): return 1 - r ** (2 / 3.0)", "def tau(r): return 1 - r ** (1 / 3.0)"),
 ('theory-u-with-two-thirds', 'dtheory.py', "def u(r): return 1 - r ** (4 / 3.0)", "def u(r): return 1 - r ** (2 / 3.0)"),
 ('theory-factor-without-its-three', 'dtheory.py', "def S(n): return 3 / (4 * math.pi)", "def S(n): return 1 / (4 * math.pi)"),
 ('theory-fixed-number-cut-by-a-half', 'dtheory.py', "dc * (tau(max(r1, r2)) - 0.75 * u(r1) * u(r2))", "dc * (tau(max(r1, r2)) - 0.5 * u(r1) * u(r2))"),
 ('theory-fixed-number-covariance-at-the-smaller-radius', 'dtheory.py', "def cov_fixed(r1, r2, n, d=D, dc=DC): return S(n) * ((d - dc) * tau(max(r1, r2)) + dc * (tau(max(r1, r2))", "def cov_fixed(r1, r2, n, d=D, dc=DC): return S(n) * ((d - dc) * tau(min(r1, r2)) + dc * (tau(min(r1, r2))"),
 ('theory-chance-covariance-at-the-smaller-radius', 'dtheory.py', "def cov_chance(r1, r2, n, d=D): return S(n) * d * tau(max(r1, r2))", "def cov_chance(r1, r2, n, d=D): return S(n) * d * tau(min(r1, r2))"),
 ('theory-first-part-without-the-two-thirds', 'dtheory.py', "if m == 1: return r ** (2 / 3.0) * math.log(1 / r)", "if m == 1: return r * math.log(1 / r)"),
 ('theory-parts-over-m-squared', 'dtheory.py', "/ (m * m - 1)\ndef mode", "/ (m * m)\ndef mode"),
 ('theory-parts-die-as-r-to-the-m', 'dtheory.py', "r ** (2 * m * m / 3.0)) / (m * m - 1)", "r ** (2 * m / 3.0)) / (m * m - 1)"),
 ('theory-ring-mean-without-three-halves', 'dtheory.py', "if m == 0: return 1.5 * (1 - r ** (2 / 3.0))", "if m == 0: return 1.0 * (1 - r ** (2 / 3.0))"),
 ('theory-part-over-pi-not-two-pi', 'dtheory.py', "def mode(m, r, n, d=D): return d * (n / math.pi) ** (1 / 3.0) / (2 * math.pi) * g(m, r)", "def mode(m, r, n, d=D): return d * (n / math.pi) ** (1 / 3.0) / math.pi * g(m, r)"),
 ('theory-round-the-ring-not-doubled', 'dtheory.py', "return 2 * d * (n / math.pi) ** (1 / 3.0) / (2 * math.pi) * s", "return d * (n / math.pi) ** (1 / 3.0) / (2 * math.pi) * s"),
 ('theory-count-part-two-thirds-alpha-squared', 'dtheory.py', "DC = 4 / 9.0 * ALPHA ** 2", "DC = 2 / 3.0 * ALPHA ** 2"),
 ('theory-noise-as-first-measured', 'dtheory.py', "D = 1.081;", "D = 1.073;"),
]
def build(name, f, old, new):
    d = os.path.join(WORK, name); os.makedirs(d, exist_ok=True)
    for x in FILES:
        s = open(os.path.join(HERE, x), encoding='utf-8').read()
        if x == f:
            if s.count(old) != 1: raise SystemExit('mutant %s: pattern found %d times in %s' % (name, s.count(old), f))
            s = s.replace(old, new)
        open(os.path.join(d, x), 'w', encoding='utf-8').write(s)
    shutil.copy(os.path.join(HERE, 'rings'), os.path.join(d, 'rings'))
    return d
def run(d):
    fails = []; code = 0
    for t in ('ruler.py', 'dew.py'):
        try: r = subprocess.run([sys.executable, '-I', os.path.join(d, t)], capture_output=True, text=True, timeout=900)
        except subprocess.TimeoutExpired: return 1, ['TIMEOUT']
        code = code or r.returncode; fails += [l for l in r.stdout.split('\n') if l.startswith('FAIL')] + ([r.stderr.strip().split('\n')[-1][:150]] if r.returncode and r.stderr.strip() and 'FAIL' not in r.stdout else [])
    return code, fails
if os.path.isdir(WORK): shutil.rmtree(WORK)
code, fails = run(build('CONTROL', None, None, None))
print('control (nothing broken): %s' % ('passes' if code == 0 else 'FAILS: ' + '; '.join(fails)))
if code != 0: sys.exit('the control does not pass; nothing below would mean anything')
dirs = [(name, build(name, f, old, new)) for name, f, old, new in M]
with ThreadPoolExecutor(max_workers=int(os.environ.get('WORKERS', '6'))) as ex: out = list(ex.map(lambda nd: (nd[0],) + run(nd[1]), dirs))
caught = 0; passed = []
for name, code, fails in out:
    if code != 0: caught += 1; print('caught   %-52s by %d: %s' % (name, len(fails), (fails[0] if fails else '')[:100]))
    else: passed.append(name); print('PASSED   %s' % name)
print('\n%d of %d broken copies caught; passed: %s' % (caught, len(M), ', '.join(passed) or 'none'))
shutil.rmtree(WORK)
