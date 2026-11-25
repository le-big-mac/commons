"""rmutants.py: break rings.c and make.py on purpose, one fault at a time, and run rtest.py on each broken copy. First a control:
an unbroken copy, built and run by the very same steps, must pass.     python -I rmutants.py"""
import os, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); WORK = os.path.join(HERE, 'mutants'); FILES = ['rings.c', 'make.py', 'rtest.py']
M = [
 ('annulus-found-by-rounding-down', 'rings.c', "k = (int)floor(rho / 0.05 + 0.5) - 1;", "k = (int)floor(rho / 0.05) - 1;"),
 ('annulus-centred-one-place-in', 'rings.c', "fabs(rho - 0.05 * (k + 1)) > half", "fabs(rho - 0.05 * k) > half"),
 ('annulus-twice-as-wide', 'rings.c', "fabs(rho - 0.05 * (k + 1)) > half) continue;", "fabs(rho - 0.05 * (k + 1)) > 2 * half) continue;"),
 ('half-width-default-wider', 'rings.c', "argc > 2 ? atof(argv[2]) : 0.008", "argc > 2 ? atof(argv[2]) : 0.01"),
 ('half-width-limit-loose', 'rings.c', "half <= 0.025", "half <= 0.25"),
 ('radius-of-the-disc-doubled', 'rings.c', "R = 536870912.0;", "R = 1073741824.0;"),
 ('profile-power-two-thirds', 'rings.c', "A0 * (1 - pow(rho, 4.0 / 3.0))", "A0 * (1 - pow(rho, 2.0 / 3.0))"),
 ('profile-without-three-quarters', 'rings.c', "A0 = 0.75 * 1.3259 * pow(n0 / M_PI, 2.0 / 3.0);", "A0 = 1.3259 * pow(n0 / M_PI, 2.0 / 3.0);"),
 ('profile-without-pi', 'rings.c', "pow(n0 / M_PI, 2.0 / 3.0)", "pow(n0, 2.0 / 3.0)"),
 ('profile-added-not-taken-off', 'rings.c', "S[k][1] += d - A0 * (1", "S[k][1] += d + A0 * (1"),
 ('points-counted-twice', 'rings.c', "S[k][0] += 1;", "S[k][0] += 2;"),
 ('depth-not-summed', 'rings.c', "S[k][2] += d;", "S[k][2] += 1;"),
 ('squares-not-summed', 'rings.c', "S[k][3] += (double)d * d;", "S[k][3] += d;"),
 ('radius-squared-in-the-sum-of-radii', 'rings.c', "S[k][4] += rho;", "S[k][4] += rho * rho;"),
 ('radius-not-squared', 'rings.c', "S[k][5] += rho * rho;", "S[k][5] += rho;"),
 ('radius-times-depth-without-depth', 'rings.c', "S[k][6] += rho * d;", "S[k][6] += rho;"),
 ('cosine-and-sine-swapped', 'rings.c', "c1 = x / (rho * R); s1 = y / (rho * R);", "c1 = y / (rho * R); s1 = x / (rho * R);"),
 ('angle-multiplied-wrongly', 'rings.c', "t = cm * c1 - sm * s1; sm = sm * c1 + cm * s1; cm = t;", "t = cm * c1 + sm * s1; sm = sm * c1 - cm * s1; cm = t;"),
 ('parts-start-at-twice-the-angle', 'rings.c', "cm = 1; sm = 0;", "cm = c1; sm = s1;"),
 ('cos-and-sin-sums-in-each-other-s-place', 'rings.c', "S[k][3 + 4 * m] += cm; S[k][4 + 4 * m] += sm;", "S[k][3 + 4 * m] += sm; S[k][4 + 4 * m] += cm;"),
 ('depth-times-cos-without-depth', 'rings.c', "S[k][5 + 4 * m] += d * cm;", "S[k][5 + 4 * m] += cm;"),
 ('depth-times-sin-is-depth-times-cos', 'rings.c', "S[k][6 + 4 * m] += d * sm;", "S[k][6 + 4 * m] += d * cm;"),
 ('three-parts-only', 'rings.c', "for (m = 1; m <= 4; m++) { t =", "for (m = 1; m <= 3; m++) { t ="),
 ('summary-s-count-not-checked', 'rings.c', "if (nsum >= 0 && nsum != n) {", "if (0) {"),
 ('first-line-not-checked', 'rings.c', "if (!fgets(line, sizeof line, stdin) || line[0] != '{') {", "if (!fgets(line, sizeof line, stdin)) {"),
 ('seed-misread', 'rings.c', "seed = atol(p + 7);", "seed = atol(p + 8);"),
 ('layers-misread', 'rings.c', "layers = atol(p + 9);", "layers = atol(p + 10);"),
 ('size-not-required', 'rings.c', "if (argc < 2) {", "if (argc < 1) {"),
 ('make-chance-clouds-all-of-one-size', 'make.py', "ns = [n0] * K if kind == 'exact' else", "ns = [n0] * K if True else"),
 ('make-exact-clouds-of-chance-size', 'make.py', "ns = [n0] * K if kind == 'exact' else", "ns = [n0] * K if kind == 'nothing' else"),
 ('make-seeds-one-early', 'make.py', "str(seed0 + i + 1), '-depths'", "str(seed0 + i), '-depths'"),
 ('make-profile-for-the-cloud-s-own-size', 'make.py', "os.path.join(HERE, 'rings'), str(n0)]", "os.path.join(HERE, 'rings'), str(ns[i])]"),
 ('make-chance-numbers-not-from-the-seed', 'make.py', "np.random.default_rng(seed0).poisson(n0, K)", "np.random.default_rng().poisson(n0, K)"),
 ('make-chance-numbers-too-even', 'make.py', "np.random.default_rng(seed0).poisson(n0, K)]", "np.random.default_rng(seed0).binomial(2 * n0, 0.5, K)]"),
 ('make-failures-not-counted', 'make.py', "if line is None: bad += 1", "if line is None: bad += 0"),
]
def build(name, f, old, new):
    d = os.path.join(WORK, name); os.makedirs(d, exist_ok=True)
    for x in FILES:
        s = open(os.path.join(HERE, x), encoding='utf-8').read()
        if x == f:
            if s.count(old) != 1: raise SystemExit('mutant %s: pattern found %d times in %s' % (name, s.count(old), f))
            s = s.replace(old, new)
        if x in ('make.py', 'rtest.py'): s = s.replace("os.path.join(HERE, '..', 'peel')", repr(os.path.join(HERE, '..', 'peel')))      # the copies stand one folder deeper
        open(os.path.join(d, x), 'w', encoding='utf-8').write(s)
    r = subprocess.run(['gcc', '-O2', '-o', os.path.join(d, 'rings'), os.path.join(d, 'rings.c'), '-lm'], capture_output=True, text=True)
    if r.returncode: raise SystemExit('mutant %s does not compile: %s' % (name, r.stderr[:300]))
    return d
def run(d):
    env = dict(os.environ); env.pop('RINGS', None)
    try: r = subprocess.run([sys.executable, '-I', os.path.join(d, 'rtest.py')], capture_output=True, text=True, timeout=300, env=env)
    except subprocess.TimeoutExpired:
        subprocess.run(['pkill', '-f', '^' + d + '/']); return 1, ['TIMEOUT']
    return r.returncode, [l for l in r.stdout.split('\n') if l.startswith('FAIL')] + ([r.stderr.strip().split('\n')[-1][:150]] if r.returncode and r.stderr.strip() and 'FAIL' not in r.stdout else [])
if os.path.isdir(WORK): shutil.rmtree(WORK)
code, fails = run(build('CONTROL', None, None, None))
print('control (nothing broken): %s' % ('passes' if code == 0 else 'FAILS: ' + '; '.join(fails)))
if code != 0: sys.exit('the control does not pass; nothing below would mean anything')
dirs = [(name, build(name, f, old, new)) for name, f, old, new in M]
with ThreadPoolExecutor(max_workers=int(os.environ.get('WORKERS', '2'))) as ex: out = list(ex.map(lambda nd: (nd[0],) + run(nd[1]), dirs))
caught = 0; passed = []
for name, code, fails in out:
    if code != 0: caught += 1; print('caught   %-44s by %d: %s' % (name, len(fails), (fails[0] if fails else '')[:100]))
    else: passed.append(name); print('PASSED   %s' % name)
print('\n%d of %d broken copies caught; passed: %s' % (caught, len(M), ', '.join(passed) or 'none'))
shutil.rmtree(WORK)
