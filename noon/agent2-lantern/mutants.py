"""mutants.py: plant one fault at a time in a copy of lantern.py and see whether test.py notices.   python -I mutants.py [WORKERS]
The first copy has no fault and must pass (the control). Writes mutants.out."""
import os, shutil, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); PY = sys.executable; WORKERS = int(sys.argv[1]) if len(sys.argv) > 1 else 4
M = [('control', [])]
def m(name, *pairs): M.append((name, list(pairs)))
m('focus(): the farther of the two places', ("s = (D - math.sqrt(D * D - 4 * f * D)) / 2.0; return s, (D - s) / s", "s = (D + math.sqrt(D * D - 4 * f * D)) / 2.0; return s, (D - s) / s"))
m('focus(): allowed nearer than 4 f', ("if D < 4 * f: return None", "if D < 3.9 * f: return None"))
m('D_of_m without the 1/m', ("def D_of_m(m, f=1.0): return f * (2 + m + 1.0 / m)", "def D_of_m(m, f=1.0): return f * (2 + m)"))
m('KL cut to IK itself less f (not the root of the difference of squares)', ("self.b = math.sqrt(a * a - f * f) if b is None else b", "self.b = (a - f) if b is None else b"))
m('I one focal length before the slider', ("self.p = 2 * f if p is None else p", "self.p = 1 * f if p is None else p"))
m('L at the lens, not under its focus', ("self.q = f if q is None else q", "self.q = 0.0 if q is None else q"))
m('K on the lower side', ("return (mx - h * dy / d, my + h * dx / d)", "return (mx + h * dy / d, my - h * dx / d)"))
m('K: the two rods taken as equal whatever they are', ("t = (self.a ** 2 - self.a2 ** 2 + d * d) / (2 * d)", "t = d / 2.0"))
m('K: the tilt of the line IN left out', ("return (mx - h * dy / d, my + h * dx / d)", "return (mx, my + h)"))
m('the lens on the far side of K', ("return k[0] - math.sqrt(w2) - self.q", "return k[0] + math.sqrt(w2) - self.q"))
m('L\'s height left out', ("w2 = self.b ** 2 - (k[1] - self.yL) ** 2", "w2 = self.b ** 2 - k[1] ** 2"))
m('N\'s place beyond the screen left out', ("Nx, Ny = D + self.e, self.yN", "Nx, Ny = D, self.yN"))
m('the rods never say they cannot reach', ("if d > self.a + self.a2 or d < abs(self.a - self.a2) or d == 0: return None", "if d == 0: return None"), ("if h2 < 0: return None", "h2 = max(h2, 0.0)"))
m('reach(): one rod\'s length', ("math.sqrt(max((self.a + self.a2) ** 2 - (self.yN - self.yI) ** 2, 0.0))", "math.sqrt(max((self.a) ** 2 - (self.yN - self.yI) ** 2, 0.0))"))
m('blur(): over the screen\'s distance, not the image\'s', ("si = f * s / (s - f); return A * abs((D - s) - si) / si", "si = f * s / (s - f); return A * abs((D - s) - si) / (D - s)"))
m('blur(): the image taken at s f / (s + f)', ("si = f * s / (s - f); return A * abs((D - s) - si) / si", "si = f * s / (s + f); return A * abs((D - s) - si) / si"))
m('sag: the push leaves it as it was', ("amp = 1.0 / (1.0 - P / (math.pi ** 2 * EI / L ** 2));", "amp = 1.0;"))
m('sag: the slope of a beam held fast at both ends', ("slope = amp * w_perp * (L ** 3 - 6 * L * x * x + 4 * x ** 3) / (24 * EI)", "slope = amp * w_perp * (2 * L * L * x - 6 * L * x * x + 4 * x ** 3) / (24 * EI)"))
m('cam: the lens\'s rise left out of the radius', ("if press else (drdphi / t - (s - smin))", "if press else (drdphi / t)"))
m('cam: the sine of the pressure angle for its tangent', ("t = math.tan(math.radians(alpha_deg));", "t = math.sin(math.radians(alpha_deg));"))
m('cam: a whole turn', ("Phi = math.radians(turn_deg);", "Phi = 2 * math.pi;"))
m('shade: the light as the length, not its square', ("v = [math.log((x0 - 1.0 / m) ** 2 / (1 + m) ** 2) for m in ms]; return max(v) - min(v)", "v = [math.log((x0 - 1.0 / m) / (1 + m) ** 2) for m in ms]; return max(v) - min(v)"))
m('shade: the ghost\'s brightness to go as 1 + m', ("v = [math.log((x0 - 1.0 / m) ** 2 / (1 + m) ** 2) for m in ms]; return max(v) - min(v)", "v = [math.log((x0 - 1.0 / m) ** 2 / (1 + m)) for m in ms]; return max(v) - min(v)"))
m('light(): by the screen\'s distance, not its square', ("sp = D_of_m(m, f) - s; return opened / (sp * sp)", "sp = D_of_m(m, f) - s; return opened / sp"))
m('light(): the shade\'s opening as the length', ("opened = 0.0 if u <= 0 else min(u * u, 1.0)", "opened = 0.0 if u <= 0 else min(u, 1.0)"))
m('thrust(): the sine for the cosine', ("return math.degrees(th), 1.0 / math.cos(th), 1.0 / math.tan(th)", "return math.degrees(th), 1.0 / math.sin(th), 1.0 / math.tan(th)"))
m('thrust(): the angle taken from the vertical', ("dx = k[0] - (s + self.q); dy = k[1] - self.yL; th = math.atan2(dy, dx);", "dx = k[0] - (s + self.q); dy = k[1] - self.yL; th = math.atan2(dx, dy);"))
m('cam pressed in: the lens\'s travel left out of the radius', ("r0 = (drdphi / t + (s - smin)) if press else (drdphi / t - (s - smin))", "r0 = (drdphi / t) if press else (drdphi / t - (s - smin))"))
def one(job):
    i, (name, pairs) = job; d = '/dev/shm/agent2-lmut-%d-%d' % (os.getpid(), i); os.makedirs(d); t0 = time.time()
    try:
        s = open(os.path.join(HERE, 'lantern.py')).read()
        for a, b in pairs:
            if s.count(a) != 1: return i, name, 'NOT PLANTED', 'the text to change was found %d times' % s.count(a), 0
            s = s.replace(a, b)
        open(os.path.join(d, 'lantern.py'), 'w').write(s)
        try: r = subprocess.run(['nice', '-n', '19', PY, '-I', os.path.join(HERE, 'test.py'), os.path.join(d, 'lantern.py')], capture_output=True, text=True, timeout=600); rc, out = r.returncode, r.stdout
        except subprocess.TimeoutExpired: rc, out = -9, ''
        fails = [l[6:110] for l in out.split('\n') if l.startswith('FAIL')]; last = out.strip().split('\n')[-1] if out.strip() else 'no output (the tests stopped: ' + (r.stderr.strip().split('\n')[-1][:60] if rc != -9 else 'time') + ')'
        if not pairs: return i, name, 'control passed' if rc == 0 else 'CONTROL FAILED', last, time.time() - t0
        return i, name, 'noticed' if rc != 0 else 'PASSED', ('%d tests failed; first: %s' % (len(fails), fails[0]) if fails else last), time.time() - t0
    finally: shutil.rmtree(d, ignore_errors=True)
if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=WORKERS) as ex: res = list(ex.map(one, enumerate(M)))
    lines = ['%-9s %-72s %-15s %4.0f s   %s' % ('' if r[1] == 'control' else 'fault %d' % r[0], r[1], r[2], r[4], r[3]) for r in res]
    planted = [r for r in res if r[1] != 'control' and r[2] != 'NOT PLANTED']; noticed = [r for r in planted if r[2] == 'noticed']
    lines.append('%d faults planted, %d noticed, %d passed every test, %d could not be planted; the control %s' % (len(planted), len(noticed), len(planted) - len(noticed), sum(1 for r in res if r[2] == 'NOT PLANTED'), res[0][2]))
    open(os.path.join(HERE, 'mutants.out'), 'w').write('\n'.join(lines) + '\n'); print('\n'.join(lines))
