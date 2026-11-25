"""test.py: lantern.py tried on cases whose answers are known some other way.   python -I test.py [a copy of lantern.py]"""
import importlib.util, math, os, random, sys
HERE = os.path.dirname(os.path.abspath(__file__)); path = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(HERE, 'lantern.py')
spec = importlib.util.spec_from_file_location('lantern_under_test', path); L = importlib.util.module_from_spec(spec); spec.loader.exec_module(L)
npass = nfail = 0
def ok(name, cond, detail=''):
    global npass, nfail
    if cond: npass += 1; print('pass  ' + name)
    else: nfail += 1; print('FAIL  ' + name + ('   ' + str(detail) if detail != '' else ''))
rnd = random.Random(1806)
# the lens
w = max(abs(1 / L.focus(D, f)[0] + 1 / (D - L.focus(D, f)[0]) - 1 / f) * f for D, f in ((rnd.uniform(4.0, 60.0) * f, f) for f in (rnd.uniform(0.3, 3.0) for _ in range(500))))
ok('focus(): 1/s + 1/s\' = 1/f at 500 screens and focal lengths (worst %.1e), the nearer of the two places, and nothing nearer than 4 f' % w, w < 1e-10 and all(L.focus(D)[0] <= D / 2 for D in (4.0, 4.5, 9.0, 30.0)) and L.focus(3.99) is None and abs(L.focus(4.0)[0] - 2.0) < 1e-12)
ok('D_of_m and focus are each other\'s inverse: the image at D_of_m(m) is m times the slider', all(abs(L.focus(L.D_of_m(m))[1] - m) < 1e-9 * m for m in (1.0, 1.3, 2.0, 7.0, 20.0, 55.0)))
def rays(D, s, f=1.0, A=1.0):      # two rays from a point of the slider on the axis through the lens's two edges: a thin lens turns a ray at height y by -y / f; where do they strike the screen?
    hit = [y + (y / s - y / f) * (D - s) for y in (A / 2, -A / 2)]; return abs(hit[0] - hit[1])
w = max(abs(L.blur(D, s) - rays(D, s)) for D, s in ((rnd.uniform(4.2, 30.0), rnd.uniform(1.02, 2.5)) for _ in range(500)))
ok('blur(): the patch is where two rays through the lens\'s edges strike the screen (500 cases, worst difference %.1e), and nought when the lens is in its place' % w, w < 1e-10 and all(L.blur(L.D_of_m(m), L.focus(L.D_of_m(m))[0]) < 1e-12 for m in (1.5, 4.0, 19.0)))
# the rods
bad = 0; worst = 0.0
for _ in range(2000):
    a = rnd.uniform(1.5, 30.0); b = rnd.uniform(0.3, 0.999) * a; p = rnd.uniform(0.5, 3.0); q = rnd.uniform(0.2, 2.0); e = rnd.uniform(-0.5, 0.5); r = L.Rods(a=a, b=b, p=p, q=q, e=e); D = rnd.uniform(p - e + 2 * math.sqrt(a * a - b * b) + 1e-9, p - e + 2 * a - 1e-9); s = r.lens(D)      # I and N no nearer than the rods can fold, no farther than they stretch
    if s is None: bad += 1; continue
    IL = (s + q) - p; LN = (D + e) - (s + q); K = r.K(D); worst = max(worst, abs(IL * LN - (a * a - b * b)) / (a * a), abs(math.hypot(K[0] - p, K[1]) - a) / a, abs(math.hypot(K[0] - D - e, K[1]) - a) / a, abs(math.hypot(K[0] - (s + q), K[1]) - b) / a)
ok('the theorem: with the three pivots in one line, IL x LN = IK^2 - KL^2 whatever the rods, the pivots\' places and the screen (2,000 arrangements; worst %.1e of IK^2; %d could not be closed), and K is a rod\'s length from each pivot' % (worst, bad), worst < 1e-9 and bad == 0)
w = max(abs(L.Rods(a=a).lens(L.D_of_m(m)) - L.focus(L.D_of_m(m))[0]) for a, m in ((rnd.uniform(1.2, 40.0), rnd.uniform(1.0, 30.0)) for _ in range(3000)) if L.D_of_m(m) < 2 + 2 * a - 1e-6)
ok('Young\'s conditions with IK^2 - KL^2 = f^2: the rods put the lens where the lens equation wants it (3,000 rods and sizes, worst %.1e f)' % w, w < 1e-9)
ok('the rods say so when they cannot reach, or jam', L.Rods(a=5.0).lens(13.0) is None and L.Rods(a=5.0).lens(11.99) is not None and abs(L.Rods(a=5.0).reach() - 12.0) < 1e-12 and L.Rods(a=11.0, yN=0.1).lens(L.D_of_m(2.0)) is None and L.Rods(a=11.0, yN=0.1).lens(L.D_of_m(3.0)) is not None)
# added after the first run of broken copies let one through (the two long rods taken as equal): rods unequal, pivots at any heights
w = 0.0
for _ in range(1000):
    a = rnd.uniform(2.0, 20.0); a2 = a * rnd.uniform(0.8, 1.25); r = L.Rods(a=a, a2=a2, yI=rnd.uniform(-0.5, 0.5), yN=rnd.uniform(-0.5, 0.5), e=rnd.uniform(-0.3, 0.3)); D = rnd.uniform(2 + abs(a - a2) + 1.0, 2 + a + a2 - 1.0); K = r.K(D)
    w = max(w, abs(math.hypot(K[0] - r.p, K[1] - r.yI) - a) / a, abs(math.hypot(K[0] - D - r.e, K[1] - r.yN) - a2) / a2, 0.0 if K[1] > min(r.yI, r.yN) else 1.0)
ok('K with unequal rods and pivots at any heights: a rod\'s length from I, the other rod\'s from N, and above them (1,000 cases, worst %.1e)' % w, w < 1e-9)
# first-order rules, each worked with a pencil
m = 10.0; D = L.D_of_m(m); eps = 1e-3; c = L.blur(D, L.Rods(a=11.0, b=math.sqrt(121 - (1 + eps))).lens(D)); ok('KL cut a little wrong: the patch is the error times m / (m + 1) (%.6f for %.6f)' % (c, eps * m / (m + 1)), abs(c / (eps * m / (m + 1)) - 1) < 0.01)
h = 1e-3; r = L.Rods(a=11.0, yN=h); s = r.lens(D); d = D - 2; H = math.sqrt(121 - d * d / 4); x_true = 1 / m; shift = 2 * h * H / d; x_pred = ((d - shift) - math.sqrt((d - shift) ** 2 - 4)) / 2
ok('N a little high: the circle about K meets the pivots\' line 2 h H / d short of N, and the lens goes where IL x (LN - that) = f^2 (%.8f for %.8f)' % (s - 1, x_pred), abs((s - 1 - x_true) / (x_pred - x_true) - 1) < 0.01)
r = L.Rods(a=11.0, yL=h); s = r.lens(D); K = L.Rods(a=11.0).K(D); gain = K[1] / (K[0] - (1 + 1 / m + 1)); ok('L a little high: the lens moves toward the slider by the height times the slope of KL (%.6f for %.6f)' % (s - (1 + 1 / m), -h * gain), abs((s - (1 + 1 / m)) / (-h * gain) - 1) < 0.01)
# the cam, the shade, the sag
def cam_again(m_lo, m_hi, turn=300.0, alpha=30.0, n=20000):      # by magnification, with ds/dD = -1 / (m^2 - 1) worked with a pencil
    Phi = math.radians(turn); t = math.tan(math.radians(alpha)); span = L.D_of_m(m_hi) - L.D_of_m(m_lo); best = 0.0
    for i in range(n + 1): m = m_lo + (m_hi - m_lo) * i / n; best = max(best, (1 / (m * m - 1)) * span / Phi / t - (1 / m - 1 / m_hi))
    return best, best + (1 / m_lo - 1 / m_hi)
ok('cam(): the least and largest radius by another sum, for three ranges', all(abs(L.cam(lo, 20.0)[i] / cam_again(lo, 20.0)[i] - 1) < 2e-3 for lo in (1.5, 2.0, 3.0) for i in (0, 1)), [L.cam(2.0, 20.0), cam_again(2.0, 20.0)])
if hasattr(L.Rods, 'thrust'):
    r = L.Rods(a=11.0); D = L.D_of_m(5.0); th = r.thrust(D); K = r.K(D); Lx = r.lens(D) + 1.0; fx, fy = (Lx - K[0]) / math.hypot(Lx - K[0], K[1]), -K[1] / math.hypot(Lx - K[0], K[1])      # a unit thrust along KL, from K to L
    ok('thrust(): KL\'s angle is the angle of the line from L to K; a unit thrust along it pushes the lens with its cosine and presses the slider with its sine; the three figures hang together (%.1f degrees, %.2f times, friction %.3f)' % th, abs(math.degrees(math.atan2(K[1], K[0] - Lx)) - th[0]) < 1e-9 and abs(abs(fx) - 1 / th[1]) < 1e-12 and abs(abs(fx) / abs(fy) - th[2]) < 1e-12 and abs(th[1] - 1 / math.cos(math.radians(th[0]))) < 1e-12)
    ok('thrust(): steeper for a smaller image and for longer rods; upright when the image is the slider\'s size', r.thrust(L.D_of_m(2.0))[0] > th[0] > r.thrust(L.D_of_m(10.0))[0] and L.Rods(a=4.0).thrust(D)[0] < th[0] and abs(r.thrust(4.0 + 1e-9)[0] - 90) < 0.01)
try: cp = [L.cam(lo, 20.0, press=True) for lo in (1.5, 2.0, 3.0)]
except TypeError: cp = None
if cp is not None: ok('cam(press=True): the same least radius at the steepest place as the other sense needs there, and the lens\'s whole travel more at the other end', all(abs(cp[i][0] - L.cam(lo, 20.0)[1]) < 2e-3 * cp[i][0] and abs((cp[i][1] - cp[i][0]) - (1 / lo - 1 / 20.0)) < 1e-9 for i, lo in enumerate((1.5, 2.0, 3.0))), cp)
def shade_again(m_lo, m_hi):      # every x0 on a fine grid
    ms = [m_lo * (m_hi / m_lo) ** (i / 300.0) for i in range(301)]; best = 1e9
    for k in range(1, 4000):
        x0 = 1 / m_lo + k * 0.0005; v = [math.log((x0 - 1 / m) ** 2 / (1 + m) ** 2) for m in ms]; best = min(best, math.exp((max(v) - min(v)) / 2))
    return best
ok('shade(): the best factor by trying every place on a fine grid, for two ranges; and with no shade the factor is (1 + m_hi) / (1 + m_lo)', all(abs(L.shade(lo, hi)[1] / shade_again(lo, hi) - 1) < 2e-3 for lo, hi in ((1.5, 4.0), (1.5, 10.0))) and abs(L.shade(1.5, 10.0)[2] - 11 / 2.5) < 1e-12, [L.shade(1.5, 4.0)[1], shade_again(1.5, 4.0)])
Lr, wq, EI = 2.2, 2.35, 133.0; ok('sag_shortening(): 17 w^2 L^7 / (40320 EI^2) with no push; a push of half the buckling load doubles the sag and so quadruples it', abs(L.sag_shortening(Lr, wq, EI) / (17 * wq * wq * Lr ** 7 / (40320 * EI * EI)) - 1) < 1e-6 and abs(L.sag_shortening(Lr, wq, EI, P=0.5 * math.pi ** 2 * EI / Lr ** 2) / L.sag_shortening(Lr, wq, EI) - 4) < 1e-9)
if hasattr(L, 'light'): ok('light(): four times the distance, a sixteenth the brightness; the shade shut at x0 and open at nought', abs(L.light(3.0, 1 + 1 / 3.0) / L.light(15.0, 1 + 1 / 15.0) - 16.0) < 1e-9 and L.light(2.0, 1.5, 0.5) == 0.0 and abs(L.light(2.0, 1.0, 0.5) - L.light(2.0, 1.0)) < 1e-15 and abs(L.light(2.0, 1.25, 0.5) / L.light(2.0, 1.25) - 0.25) < 1e-12)
print('%d passed, %d failed' % (npass, nfail)); sys.exit(1 if nfail else 0)
