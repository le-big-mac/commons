"""smutants.py: plant one fault at a time in a copy of the programs and see whether stest.py notices.   python -I smutants.py [WORKERS] [ONLY]
Each copy is made in its own folder under /dev/shm, the C programs built there, theory.json made afresh there when the fault is in
flow.c, erode.c or theory.py (it is what those programs give), and stest.py run on the folder. The first copy has no fault and
must pass every test (the control). A copy whose build fails, or which runs past its time, counts as noticed. Writes smutants.out.
(The first run, smutants-first-run.out, is void: its control failed. smake.py looks for the peeling program one folder up from
itself, and the copies had nothing there, so seven tests failed for every copy, the true one among them, and all 58 faults were
"noticed" for that reason alone. Each copy now sits in a folder of its own with a link to the peeling program beside it.
The fault that makes the runner leave its files of points behind does leave them, some 1,200 small files in /dev/shm named
agent2-shape-*: remove them afterwards, when no batch is running.)"""
import os, shutil, signal, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); PY = sys.executable
WORKERS = int(sys.argv[1]) if len(sys.argv) > 1 else 4; ONLY = sys.argv[2] if len(sys.argv) > 2 else None
FILES = ['cloud.c', 'flow.c', 'erode.c', 'smake.py', 'theory.py', 'theory.json']
M = [('control', None, None, None)]
def m(name, f, a, b): M.append((name, f, a, b))
# ---- cloud.c
m('cloud: the disc\'s radius 1 in 100 short', 'cloud.c', 'case 0: in = u * u + v * v <= 1; break;', 'case 0: in = u * u + v * v <= 0.98; break;')
m('cloud: the ellipse a little too tall', 'cloud.c', 'case 1: in = u * u / 3 + 3 * v * v <= 1; break;', 'case 1: in = u * u / 3 + 2.9 * v * v <= 1; break;')
m('cloud: the triangle\'s slanted sides 1 in 100 off', 'cloud.c', 'in = v >= -h / 3 && fabs(u) * h <= (a / 2) * (2 * h / 3 - v); break; }', 'in = v >= -h / 3 && fabs(u) * h <= (a / 2) * (2 * h / 3 - 0.99 * v); break; }')
m('cloud: the hexagon without one pair of sides', 'cloud.c', 'in = fabs(v) <= ap && fabs(sqrt(3.0) / 2 * u + v / 2) <= ap && fabs(sqrt(3.0) / 2 * u - v / 2) <= ap; break; }', 'in = fabs(v) <= ap && fabs(sqrt(3.0) / 2 * u + v / 2) <= ap; break; }')
m('cloud: the half disc not centred (5 in 100 off)', 'cloud.c', 'double r = sqrt(2.0), c = 4 * r / (3 * M_PI); kind = 5;', 'double r = sqrt(2.0), c = 0.95 * 4 * r / (3 * M_PI); kind = 5;')
m('cloud: the quarter disc\'s arc 1 in 100 short', 'cloud.c', '(u + c) * (u + c) + (v + c) * (v + c) <= r * r; break; }', '(u + c) * (u + c) + (v + c) * (v + c) <= 0.98 * r * r; break; }')
m('cloud: the rounded triangle\'s corners rounded too tightly', 'cloud.c', 'if (dx * dx + dy * dy <= rr * rr) in = 1; }', 'if (dx * dx + dy * dy <= 0.9 * rr * rr) in = 1; }')
m('cloud: the rounded triangle is the plain triangle', 'cloud.c', 'for (j = 0; j < 3 && !in; j++) { double px = vx[j]', 'for (j = 0; j < 0 && !in; j++) { double px = vx[j]')
m('cloud: the disc\'s box 1 in 100 short on one side', 'cloud.c', 'kind = 0; x0 = y0 = -1; x1 = y1 = 1; }', 'kind = 0; x0 = y0 = -1; x1 = y1 = 1; x1 = 0.99; }')
m('cloud: the seed is not used', 'cloud.c', 'z = sd * 0x100000001B3ULL;', 'z = 0x100000001B3ULL;')
m('cloud: the shape\'s name is not mixed into the seed', 'cloud.c', 'for (i = 0; name[i]; i++) z = z * 31 + (unsigned char)name[i];', '')
m('cloud: points a little denser to one side', 'cloud.c', 'double x = floor((x0 + (x1 - x0) * U01()) * UNIT),', 'double x = floor((x0 + (x1 - x0) * pow(U01(), 1.01)) * UNIT),')
m('cloud: x and y written the wrong way round', 'cloud.c', 'printf("%.0f %.0f\\n", x, y);', 'printf("%.0f %.0f\\n", y, x);')
m('cloud: one point too few', 'cloud.c', 'for (i = 0; i < n; ) {', 'for (i = 1; i < n; ) {')
m('cloud: the square 1 in 100 too small (points still even)', 'cloud.c', 'kind = 2; x1 = y1 = sqrt(M_PI) / 2; x0 = y0 = -x1; }', 'kind = 2; x1 = y1 = 0.99 * sqrt(M_PI) / 2; x0 = y0 = -x1; }')
# ---- flow.c
m('flow: the speed is the curvature to the 0.34', 'flow.c', 'F[k] = hn[k] + dt * pow(R[k], -1.0 / 3.0) - h[k];', 'F[k] = hn[k] + dt * pow(R[k], -0.34) - h[k];')
m('flow: the second difference divided by dtheta^2', 'flow.c', 'dth = 2 * M_PI / M; cdiv = 2 - 2 * cos(dth);', 'dth = 2 * M_PI / M; cdiv = dth * dth;')
m('flow: the time left at the stop is 0.74 (area/pi)^(2/3)', 'flow.c', 'double T = t + 0.75 * pow(A / M_PI, 2.0 / 3.0),', 'double T = t + 0.74 * pow(A / M_PI, 2.0 / 3.0),')
m('flow: the gradient at the stop a tenth too small', 'flow.c', 'dTdA = 0.5 * pow(A / M_PI, -1.0 / 3.0) / M_PI;', 'dTdA = 0.45 * pow(A / M_PI, -1.0 / 3.0) / M_PI;')
m('flow: the backward system is not transposed', 'flow.c', 'a[k] = -wm / cdiv; c[k] = -wp / cdiv; b[k] = 1 - wk * (1 - 2 / cdiv); }\n        cyclic(a, b, c, g, g2);', 'a[k] = -wk / cdiv; c[k] = -wk / cdiv; b[k] = 1 - wk * (1 - 2 / cdiv); }\n        cyclic(a, b, c, g, g2);')
m('flow: psi without the width of an angle', 'flow.c', 'double psi = g[k] / (Rn[k] * dth), sw =', 'double psi = g[k] / (Rn[k]), sw =')
m('flow: the edge formula with 1.4 for 3/2', 'flow.c', 'Iedge *= 1.5 / (M * dth); zLz *= 1.5 / (M * dth);', 'Iedge *= 1.4 / (M * dth); zLz *= 1.5 / (M * dth);')
m('flow: the edge formula with the smooth eigenvalue 1 - m^2', 'flow.c', 'lam = 1 - (2 - 2 * cos(m * dth)) / cdiv, mult', 'lam = 1 - (double)m * m, mult')
m('flow: the edge formula keeps the wave m = 1', 'flow.c', 'if (m == 1) { leak = sqrt(cr * cr + ci * ci); continue; }', 'if (m == 1) { leak = sqrt(cr * cr + ci * ci); }')
m('flow: the shortfall taken about 0.6 T/A', 'flow.c', 'cc = 2.0 / 3.0 * T / A0;', 'cc = 0.6 * T / A0;')
m('flow: the triangle\'s top corner too low', 'flow.c', 'vy[3] = {-ht / 3, -ht / 3, 2 * ht / 3}; int i; for (i = 0; i < 3; i++) { v = vx[i] * c + vy[i] * s; if (v > m) m = v; } return m; }', 'vy[3] = {-ht / 3, -ht / 3, 0.6 * ht}; int i; for (i = 0; i < 3; i++) { v = vx[i] * c + vy[i] * s; if (v > m) m = v; } return m; }')
m('flow: the rounded triangle swollen by a fifth of its inradius', 'flow.c', 'return m + rr; }', 'return m + 0.8 * rr; }')
m('flow: the hexagon 1 in 100 too large', 'flow.c', 'if (!strcmp(name, "hexagon")) { double r = sqrt(2 * M_PI / (3 * sqrt(3.0))), m = -1e300;', 'if (!strcmp(name, "hexagon")) { double r = 1.01 * sqrt(2 * M_PI / (3 * sqrt(3.0))), m = -1e300;')
m('flow: -q does not shorten the last steps', 'flow.c', 'dtmax = 1e-4 * q; frac = 0.01 * q; grow = 1 + q / 12; }', 'dtmax = 1e-4 * q; frac = 0.01; grow = 1 + q / 12; }')
m('flow: the radius of curvature 1 in 1,000 off', 'flow.c', 'R[k] = h[k] + (h[(k + 1) % M] - 2 * h[k] + h[(k + M - 1) % M]) / cdiv; }', 'R[k] = h[k] + (h[(k + 1) % M] - 2 * h[k] + h[(k + M - 1) % M]) / (1.001 * cdiv); }')
m('flow: the area swept goes as R to the 0.6', 'flow.c', 'sw = wt * pow(Rn[k], 2.0 / 3.0) * dth; I += psi * psi * sw;', 'sw = wt * pow(Rn[k], 0.6) * dth; I += psi * psi * sw;')
m('flow: the integral left over at the stop is left out', 'flow.c', 'name, M, dtmax, frac, grow, stop, rho0, A0, N, fails, T, I + Irem,', 'name, M, dtmax, frac, grow, stop, rho0, A0, N, fails, T, I,')
m('flow: the linearised step uses 1/2 for 1/3', 'flow.c', 'double wk = pow(Rn[k], -4.0 / 3.0) * dts[n] / 3, wm = pow(Rn[(k + M - 1) % M], -4.0 / 3.0) * dts[n] / 3, wp = pow(Rn[(k + 1) % M], -4.0 / 3.0) * dts[n] / 3;', 'double wk = pow(Rn[k], -4.0 / 3.0) * dts[n] / 2, wm = pow(Rn[(k + M - 1) % M], -4.0 / 3.0) * dts[n] / 2, wp = pow(Rn[(k + 1) % M], -4.0 / 3.0) * dts[n] / 2;')
m('flow: the half disc is a disc', 'flow.c', 'return s >= 0 ? r : r * fabs(c); }', 'return r; }')
# ---- erode.c
m('erode: the step\'s time with 0.66 for 0.6552', 'erode.c', 'OMEGA = 0.65518535034906170;', 'OMEGA = 0.66;')
m('erode: the time left at the stop 0.7 (area/pi)^(2/3)', 'erode.c', None, None)
m('erode: the rounded triangle\'s corners are arcs of 110 degrees', 'erode.c', 'double th = (-90 + 120 * j + 0.25 * i) * M_PI / 180;', 'double th = (-85 + 120 * j + 0.25 * i * 110 / 120) * M_PI / 180;')
m('erode: the half disc\'s radius 1.40', 'erode.c', 'else if (!strcmp(name, "halfdisc")) { double r = sqrt(2.0);', 'else if (!strcmp(name, "halfdisc")) { double r = 1.40;')
m('erode: the triangle 1 in 100 too tall', 'erode.c', 'pt v[3] = {{-a / 2, -h / 3}, {a / 2, -h / 3}, {0, 2 * h / 3}};', 'pt v[3] = {{-a / 2, -h / 3}, {a / 2, -h / 3}, {0, 2.03 * h / 3}};')
# ---- smake.py
m('smake: the seeds begin one early', 'smake.py', '    seed = seed0 + i + 1', '    seed = seed0 + i')
m('smake: every cloud has the same seed', 'smake.py', '    seed = seed0 + i + 1', '    seed = seed0 + 1')
m('smake: chance numbers of points 1 in 100 too many', 'smake.py', 'np.random.default_rng(seed0).poisson(n0, K)', 'np.random.default_rng(seed0).poisson(1.01 * n0, K)')
m('smake: chance numbers from another seed', 'smake.py', 'np.random.default_rng(seed0).poisson(n0, K)', 'np.random.default_rng(seed0 + 1).poisson(n0, K)')
m('smake: chance numbers too even (binomial)', 'smake.py', 'np.random.default_rng(seed0).poisson(n0, K)', 'np.random.default_rng(seed0).binomial(2 * n0, 0.5, K)')
m('smake: no cloud is peeled both ways', 'smake.py', "'-both' if i % 200 == 0 else '-fast'", "'-fast'")
m('smake: every shape is a disc', 'smake.py', "[os.path.join(HERE, 'cloud'), shape, str(ns[i]), str(seed)]", "[os.path.join(HERE, 'cloud'), 'disc', str(ns[i]), str(seed)]")
m('smake: the files of points are left behind', 'smake.py', '        os.remove(f)\n', '')
m('smake: a cloud has one point too few', 'smake.py', "[os.path.join(HERE, 'cloud'), shape, str(ns[i]), str(seed)]", "[os.path.join(HERE, 'cloud'), shape, str(ns[i] - 1), str(seed)]")
m('smake: the count written down is one too many', 'smake.py', "'layers': o['layers'],", "'layers': o['layers'] + 1,")
m('smake: disc0 goes through cloud.c like the rest', 'smake.py', "    if shape == 'disc0': r =", "    if shape == 'disc00': r =")
m('smake: the lines come out of order', 'smake.py', 'for line in ex.map(one, range(K)):', 'for line in ex.map(one, reversed(range(K))):')
# ---- theory.py
m('theory: alpha 1.33', 'theory.py', 'ALPHA = 1.3259;', 'ALPHA = 1.33;')
m('theory: D 1.073', 'theory.py', 'D = 1.081;', 'D = 1.073;')
m('theory: the count\'s share 0.45 alpha^2', 'theory.py', 'DC = 4 / 9.0 * ALPHA ** 2', 'DC = 0.45 * ALPHA ** 2')
m('theory: with exactly n the count\'s share times T and not T^2', 'theory.py', "'exact': rho ** (1 / 3.0) * (d * I - dc * t['T'] ** 2 / math.pi)}", "'exact': rho ** (1 / 3.0) * (d * I - dc * t['T'] / math.pi)}")
m('theory: the variance goes as the density to the 0.34', 'theory.py', "'chance': rho ** (1 / 3.0) * d * I,", "'chance': rho ** 0.34 * d * I,")
m('theory: figures not carried to the limit', 'theory.py', 'a, b, c = f[(1536, 0.5)], f[(1536, 0.25)], f[(3072, 0.5)]; return 2 * b - a, c - a, (a, b, c)', 'a, b, c = f[(1536, 0.5)], f[(1536, 0.25)], f[(3072, 0.5)]; return b, c - a, (a, b, c)')
m('theory: the mean with the density to the 0.66', 'theory.py', "'mean': ALPHA * rho ** (2 / 3.0) * t['T'],", "'mean': ALPHA * rho ** 0.66 * t['T'],")
def find_erode_final():
    s = open(os.path.join(HERE, 'erode.c')).read(); a = '0.75 * pow('
    return (a, '0.7 * pow(') if s.count(a) == 1 else (None, None)
M = [(n, f, *(find_erode_final() if n.startswith('erode: the time left at the stop') else (a, b))) for n, f, a, b in M]
def killgroup(p):
    try: os.killpg(p.pid, signal.SIGKILL)
    except Exception: pass
def sh(cmd, cwd, timeout):
    p = subprocess.Popen(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, start_new_session=True)
    try: out, _ = p.communicate(timeout=timeout); return p.returncode, out
    except subprocess.TimeoutExpired: killgroup(p); p.communicate(); return -9, 'ran past %d s' % timeout
def one(job):
    i, (name, f, a, b) = job; top = '/dev/shm/agent2-smut-%d-%d' % (os.getpid(), i); d = os.path.join(top, 'shape'); os.makedirs(d); t0 = time.time()
    os.symlink(os.path.join(HERE, '..', 'peel'), os.path.join(top, 'peel'))                # smake.py looks for ../peel
    try:
        for x in FILES: shutil.copy(os.path.join(HERE, x), d)
        if f is not None:
            if a is None: return i, name, 'NOT PLANTED', 'the text to change was not found once', 0
            s = open(os.path.join(d, f)).read()
            if s.count(a) != 1: return i, name, 'NOT PLANTED', 'the text to change was found %d times' % s.count(a), 0
            open(os.path.join(d, f), 'w').write(s.replace(a, b))
        for prog in ('cloud', 'flow', 'erode'):
            rc, out = sh(['gcc', '-O2', '-o', prog, prog + '.c', '-lm'], d, 120)
            if rc != 0: return i, name, 'noticed', 'does not build', time.time() - t0
        if f is None or f in ('flow.c', 'erode.c'):
            rc, out = sh([PY, '-I', 'theory.py', 'make'], d, 1500)
            if rc != 0: return i, name, 'noticed' if f is not None else 'CONTROL FAILED', 'theory.py make failed or ran past its time', time.time() - t0
        rc, out = sh([PY, '-I', os.path.join(HERE, 'stest.py'), d], d, 1500)
        fails = [l[6:90] for l in out.split('\n') if l.startswith('FAIL')]; last = out.strip().split('\n')[-1] if out.strip() else ''
        if f is None: return i, name, 'control passed' if rc == 0 else 'CONTROL FAILED', last, time.time() - t0
        return i, name, 'noticed' if rc != 0 else 'PASSED', ('%d tests failed; first: %s' % (len(fails), fails[0]) if fails else last), time.time() - t0
    finally: shutil.rmtree(top, ignore_errors=True)
if __name__ == '__main__':
    jobs = [(i, x) for i, x in enumerate(M) if ONLY is None or ONLY in x[0] or x[1] is None]
    with ThreadPoolExecutor(max_workers=WORKERS) as ex: res = list(ex.map(one, jobs))
    lines = ['%-9s %-62s %-15s %5.0f s   %s' % ('' if r[1] == 'control' else 'fault %d' % r[0], r[1], r[2], r[4], r[3]) for r in res]
    planted = [r for r in res if r[1] != 'control' and r[2] != 'NOT PLANTED']; noticed = [r for r in planted if r[2] == 'noticed']
    lines.append('%d faults planted, %d noticed, %d passed every test, %d could not be planted; the control %s' % (len(planted), len(noticed), len(planted) - len(noticed), sum(1 for r in res if r[2] == 'NOT PLANTED'), res[0][2]))
    open(os.path.join(HERE, 'smutants.out' if ONLY is None else 'smutants-part.out'), 'w').write('\n'.join(lines) + '\n'); print('\n'.join(lines))
