"""stest.py: tests of the programs of this folder (cloud.c, flow.c, erode.c, smake.py, theory.py).   python -I stest.py [DIR]
DIR (default: this folder) is where the programs under test are; a copy with a fault planted can be put through the same tests
(smutants.py). Exit status 0 when every test passes."""
import json, math, os, subprocess, sys, tempfile
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); DIR = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else HERE
PY = sys.executable; PEEL = os.path.join(HERE, '..', 'peel'); TMP = tempfile.mkdtemp(prefix='agent2-stest-', dir='/dev/shm')
passed = failed = 0
def check(name, ok, detail=''):
    global passed, failed
    if ok: passed += 1
    else: failed += 1
    print('%s  %s%s' % ('pass' if ok else 'FAIL', name, ('   [' + detail + ']') if detail else ''))
def run(cmd, timeout=600):
    try: return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired: return None
def J(cmd, timeout=600):
    r = run(cmd, timeout)
    try: return json.loads(r.stdout)
    except Exception: return None

# ---------- the shapes, written again here from their definitions ----------
SQ3 = math.sqrt(3.0)
def inside(shape, u, v):
    if shape == 'disc': return u * u + v * v <= 1
    if shape == 'ellipse': return u * u / 3 + 3 * v * v <= 1
    if shape == 'square': w = math.sqrt(math.pi) / 2; return (np.abs(u) <= w) & (np.abs(v) <= w)
    if shape == 'rect': w = math.sqrt(3 * math.pi) / 2; return (np.abs(u) <= w) & (np.abs(v) <= math.pi / (4 * w))
    if shape == 'triangle':
        a = math.sqrt(4 * math.pi / SQ3); rin = a / (2 * SQ3)                      # three half-planes at distance rin from the centre
        return (v >= -rin) & (u * SQ3 / 2 + v / 2 <= rin) & (-u * SQ3 / 2 + v / 2 <= rin)
    if shape == 'hexagon':
        r = math.sqrt(2 * math.pi / (3 * SQ3)); ap = r * SQ3 / 2; ok = np.ones_like(u, bool)
        for k in range(6): th = math.pi / 6 + k * math.pi / 3; ok &= u * math.cos(th) + v * math.sin(th) <= ap
        return ok
    if shape == 'halfdisc': c = 4 * math.sqrt(2) / (3 * math.pi); return (v + c >= 0) & (u * u + (v + c) ** 2 <= 2)
    if shape == 'quarter': c = 8 / (3 * math.pi); return (u + c >= 0) & (v + c >= 0) & ((u + c) ** 2 + (v + c) ** 2 <= 4)
    if shape == 'rtriangle':
        rin = math.sqrt(math.pi / (4.5 * SQ3 + math.pi / 16)); rr = rin / 4; a = 2 * SQ3 * rin; V = [(-a / 2, -rin), (a / 2, -rin), (0, 2 * rin)]
        d = np.full(np.shape(u), np.inf)                                             # distance to the triangle: 0 inside it
        tri = (v >= -rin) & (u * SQ3 / 2 + v / 2 <= rin) & (-u * SQ3 / 2 + v / 2 <= rin)
        for j in range(3):
            (px, py), (qx, qy) = V[j], V[(j + 1) % 3]; ex, ey = qx - px, qy - py
            t = np.clip(((u - px) * ex + (v - py) * ey) / (ex * ex + ey * ey), 0, 1); d = np.minimum(d, np.hypot(u - px - t * ex, v - py - t * ey))
        return tri | (d <= rr)
SHAPES = ['disc', 'ellipse', 'square', 'rect', 'triangle', 'hexagon', 'halfdisc', 'quarter', 'rtriangle']
G = np.linspace(-2.2, 2.2, 2201) + 0.000731; GX, GY = np.meshgrid(G, G); CELL = (G[1] - G[0]) ** 2           # shifted, so that no side of a square lies along a line of the grid
def box(shape):                                   # the smallest upright box round the shape, from its definition
    if shape == 'disc': return -1, 1, -1, 1
    if shape == 'ellipse': return -SQ3, SQ3, -1 / SQ3, 1 / SQ3
    if shape == 'square': w = math.sqrt(math.pi) / 2; return -w, w, -w, w
    if shape == 'rect': w = math.sqrt(3 * math.pi) / 2; return -w, w, -math.pi / (4 * w), math.pi / (4 * w)
    if shape == 'triangle': a = math.sqrt(4 * math.pi / SQ3); rin = a / (2 * SQ3); return -a / 2, a / 2, -rin, 2 * rin
    if shape == 'hexagon': r = math.sqrt(2 * math.pi / (3 * SQ3)); return -r, r, -r * SQ3 / 2, r * SQ3 / 2
    if shape == 'halfdisc': c = 4 * math.sqrt(2) / (3 * math.pi); return -math.sqrt(2), math.sqrt(2), -c, math.sqrt(2) - c
    if shape == 'quarter': c = 8 / (3 * math.pi); return -c, 2 - c, -c, 2 - c
    if shape == 'rtriangle': rin = math.sqrt(math.pi / (4.5 * SQ3 + math.pi / 16)); rr = rin / 4; a = 2 * SQ3 * rin; return -a / 2 - rr, a / 2 + rr, -rin - rr, 2 * rin + rr

# ---------- cloud.c ----------
NPT = 200000
for sh in SHAPES:
    f = os.path.join(TMP, 'c-%s.txt' % sh); r = subprocess.run([os.path.join(DIR, 'cloud'), sh, str(NPT), '7'], stdout=open(f, 'w'))
    try: raw = np.loadtxt(f)
    except Exception: raw = np.zeros((0, 2))
    ok_n = raw.shape == (NPT, 2)
    check('cloud %s: exactly %d lines of two whole numbers below 2^29' % (sh, NPT), ok_n and bool(np.all(raw == np.round(raw))) and float(np.abs(raw).max()) < 2 ** 29)
    if not ok_n: continue
    p = raw / 2 ** 28; m = inside(sh, GX, GY); area = m.sum() * CELL
    check('cloud %s: the shape as written here has area pi and its centre of area at the origin' % sh, abs(area - math.pi) < 0.004 and abs(GX[m].mean()) < 2e-3 and abs(GY[m].mean()) < 2e-3, 'area %.4f, centre %.4f %.4f' % (area, GX[m].mean(), GY[m].mean()))
    out = int((~inside(sh, p[:, 0] * (1 - 1e-7), p[:, 1] * (1 - 1e-7))).sum())
    check('cloud %s: every point is in the shape' % sh, out == 0, '%d outside' % out)
    ex = [GX[m].mean(), GY[m].mean(), (GX[m] ** 2).mean(), (GY[m] ** 2).mean(), (GX[m] * GY[m]).mean()]; cols = [p[:, 0], p[:, 1], p[:, 0] ** 2, p[:, 1] ** 2, p[:, 0] * p[:, 1]]
    zs = [(c.mean() - e) / (c.std() / math.sqrt(NPT)) for c, e in zip(cols, ex)]
    check('cloud %s: the means of x, y, x^2, y^2, xy are the shape\'s (each within 4 standard errors)' % sh, max(abs(z) for z in zs) < 4, 'z = ' + ', '.join('%.1f' % z for z in zs))
    # evenness: 24 x 24 cells over the box; among cells wholly inside, the counts are even; and the share of points in them is their share of area
    x0, x1, y0, y1 = box(sh); nb = 24
    check('cloud %s: the points reach the sides of the shape\'s box (to 1 in 100 of its width: a corner holds few) and do not pass them' % sh, x0 <= p[:, 0].min() < x0 + 1e-2 * (x1 - x0) and x1 - 1e-2 * (x1 - x0) < p[:, 0].max() <= x1 and y0 <= p[:, 1].min() < y0 + 1e-2 * (y1 - y0) and y1 - 1e-2 * (y1 - y0) < p[:, 1].max() <= y1)
    ix = np.minimum(((p[:, 0] - x0) / (x1 - x0) * nb).astype(int), nb - 1); iy = np.minimum(((p[:, 1] - y0) / (y1 - y0) * nb).astype(int), nb - 1); cnt = np.zeros((nb, nb)); np.add.at(cnt, (ix, iy), 1)
    sub = np.linspace(1e-9, 1 - 1e-9, 23); whole = np.zeros((nb, nb), bool)
    for i in range(nb):
        for j in range(nb):
            U, V = np.meshgrid(x0 + (i + sub) * (x1 - x0) / nb, y0 + (j + sub) * (y1 - y0) / nb); whole[i, j] = bool(inside(sh, U, V).all())
    k = int(whole.sum()); e = cnt[whole].sum() / k; chi = float(((cnt[whole] - e) ** 2 / e).sum()); z = (chi - (k - 1)) / math.sqrt(2 * (k - 1))
    share = k * (x1 - x0) * (y1 - y0) / nb ** 2 / math.pi; zz = (cnt[whole].sum() - NPT * share) / math.sqrt(NPT * share * (1 - share)) if share < 1 - 1e-9 else (0.0 if cnt[whole].sum() == NPT else 99.0)
    check('cloud %s: even over the %d cells wholly inside (chi-square within 4 sd), and they hold their share of the points' % (sh, k), abs(z) < 4 and abs(zz) < 4, 'chi z = %.1f, share z = %.1f' % (z, zz))
f1 = run([os.path.join(DIR, 'cloud'), 'triangle', '500', '7']).stdout; f2 = run([os.path.join(DIR, 'cloud'), 'triangle', '500', '7']).stdout; f3 = run([os.path.join(DIR, 'cloud'), 'triangle', '500', '8']).stdout; f4 = run([os.path.join(DIR, 'cloud'), 'square', '500', '7']).stdout; f5 = run([os.path.join(DIR, 'cloud'), 'rect', '500', '7']).stdout
check('cloud: the same seed gives the same file; another seed, or another shape with the same seed, other numbers', f1 == f2 and f1 != f3 and len(set(f1.split()) & set(f3.split())) < 5 and len(set(f4.split()) & set(f5.split())) < 5)
check('cloud: a wrong shape, or no points, is refused', run([os.path.join(DIR, 'cloud'), 'blob', '10', '1']).returncode != 0 and run([os.path.join(DIR, 'cloud'), 'disc', '0', '1']).returncode != 0)

# ---------- flow.c ----------
runs = json.load(open(os.path.join(DIR, 'theory.json'))) if os.path.exists(os.path.join(DIR, 'theory.json')) else []
def at(sh, key, m=1536):
    f = {round(o['dtmax'] / 1e-4, 4): o[key] for prog, o in runs if prog == 'flow' and o['shape'] == sh and o['M'] == m}; return 2 * f[0.25] - f[0.5] if 0.25 in f else f[0.5]
check('flow (theory.json): the disc and the ellipse have T = 3/4 and I = 3/(4 pi) at the limit, to 2 in 100,000', all(abs(at(sh, 'T') / 0.75 - 1) < 2e-5 and abs(at(sh, k) / (3 / (4 * math.pi)) - 1) < 2e-5 for sh in ('disc', 'ellipse') for k in ('I', 'I_edge')), 'disc T %.6f I %.6f' % (at('disc', 'T'), at('disc', 'I')))
check('flow (theory.json): I summed over the inside and I from the edge agree at the limit to 1 in 10,000, for all nine shapes', all(abs(at(sh, 'I') / at(sh, 'I_edge') - 1) < 1e-4 for sh in SHAPES), ', '.join('%.1e' % (at(sh, 'I') / at(sh, 'I_edge') - 1) for sh in SHAPES))
check('flow (theory.json): the integral of psi over the shape is T at the limit to 1 in 10,000', all(abs(at(sh, 'psi_integral') / at(sh, 'T') - 1) < 1e-4 for sh in SHAPES))
check('flow (theory.json): doubling the angles moves T and I by less than 5 in 100,000', all(abs(at(sh, k, 3072) / [o[k] for prog, o in runs if prog == 'flow' and o['shape'] == sh and o['M'] == 1536 and abs(o['dtmax'] - 5e-5) < 1e-9][0] - 1) < 5e-5 for sh in SHAPES for k in ('T', 'I_edge')))
check('flow (theory.json): the shortfall below (4/3) T^2 / A is nothing for the ellipse, triangle, square, rectangle and hexagon and positive for the other three', all(abs(at(sh, 'shortfall')) * math.pi / at(sh, 'T') ** 2 < 3e-5 for sh in ('disc', 'ellipse', 'triangle', 'square', 'rect', 'hexagon')) and all(at(sh, 'shortfall') * math.pi / at(sh, 'T') ** 2 > 1e-3 for sh in ('rtriangle', 'halfdisc', 'quarter')))
check('flow (theory.json): (4/3) T^2/A less the shortfall is I', all(abs((4 / 3 * at(sh, 'T') ** 2 / math.pi - at(sh, 'shortfall')) / at(sh, 'I_edge') - 1) < 1e-4 for sh in SHAPES))
check('flow and erode (theory.json): the two programs give the same T to 3 in 10,000', all(abs(at(sh, 'T') / (lambda e: e[3e-5] + (e[3e-5] - e[1e-4]) / ((1e-4 / 3e-5) ** (2 / 3.0) - 1))({o['eta']: o['T'] for prog, o in runs if prog == 'erode' and o['shape'] == sh}) - 1) < 3e-4 for sh in SHAPES))
F = {}
for sh in ['disc', 'triangle', 'poly:0,0,1,0,0,1', 'square', 'rect', 'poly:0,0,4,0,3,1,1,1', 'halfdisc', 'wave:3:0.1']:
    F[sh] = {q: J([os.path.join(DIR, 'flow'), sh, '768', '-q', q]) for q in ('1', '0.5')}
okF = all(F[sh][q] is not None for sh in F for q in F[sh]); check('flow: runs on eight shapes at 768 angles', okF)
if okF:
    lim = lambda sh, k: 2 * F[sh]['0.5'][k] - F[sh]['1'][k]
    check('flow: the error of T and of I falls in proportion to the step quality (disc: the q = 0.5 error is half the q = 1 error)', all(abs((F['disc']['0.5'][k] - x) / (F['disc']['1'][k] - x) - 0.5) < 0.05 for k, x in (('T', 0.75), ('I', 3 / (4 * math.pi)), ('I_edge', 3 / (4 * math.pi)))))
    check('flow: every shape has area pi, no cos or sin in g, and the integral of psi round a curve stays 1 to 2 in 100', all(abs(F[sh]['0.5']['area'] - math.pi) < 2e-3 and F[sh]['0.5']['leak'] < 1e-8 and F[sh]['0.5']['worst_step_check'] < 0.02 for sh in F), ', '.join('%.0e' % F[sh]['0.5']['worst_step_check'] for sh in F))
    check('flow: a right triangle has the T and I of the equilateral one, a long rectangle those of the square (affine maps change nothing)', abs(lim('poly:0,0,1,0,0,1', 'T') / lim('triangle', 'T') - 1) < 2e-4 and abs(lim('poly:0,0,1,0,0,1', 'I_edge') / lim('triangle', 'I_edge') - 1) < 3e-4 and abs(lim('rect', 'T') / lim('square', 'T') - 1) < 2e-4 and abs(lim('rect', 'I_edge') / lim('square', 'I_edge') - 1) < 3e-4)
    check('flow: T^2/A <= I <= (4/3) T^2/A for every shape (to 1 in 10,000)', all(lim(sh, 'T') ** 2 / math.pi * (1 - 1e-4) <= lim(sh, 'I_edge') <= 4 / 3 * lim(sh, 'T') ** 2 / math.pi * (1 + 1e-4) for sh in F))
    check('flow: I is not below the Cauchy bound (the integral of dt over the affine length)', all(lim(sh, 'lower_bound_affine') <= lim(sh, 'I_edge') * (1 + 1e-4) for sh in F))
    check('flow: the trapezoid and the wavy shape fall short of 4/3 (by 0.0005 and 0.0027 of T^2/A)', abs(lim('poly:0,0,4,0,3,1,1,1', 'shortfall') * math.pi / lim('poly:0,0,4,0,3,1,1,1', 'T') ** 2 - 0.00053) < 1.5e-4 and abs(lim('wave:3:0.1', 'shortfall') * math.pi / lim('wave:3:0.1', 'T') ** 2 - 0.00273) < 2e-4)
    a = J([os.path.join(DIR, 'flow'), 'triangle', '768', '-q', '1', '-rho0', '1e-4']); b = J([os.path.join(DIR, 'flow'), 'triangle', '768', '-q', '1', '-stop', '1e-2'])
    check('flow: a larger swelling at the start (1e-4) or an earlier stop (a hundredth of the area) moves T by less than 3 in 10,000', a is not None and b is not None and abs(a['T'] / F['triangle']['1']['T'] - 1) < 3e-4 and abs(b['T'] / F['triangle']['1']['T'] - 1) < 3e-4)
check('flow: a wrong shape or too few angles is refused', run([os.path.join(DIR, 'flow'), 'blob', '768']).returncode != 0 and run([os.path.join(DIR, 'flow'), 'disc', '8']).returncode != 0)

# ---------- I for a polygon from erode.c alone: the gradient of T by moving each side, then I = (3/2) <g, L^(-1) g> ----------
# (a square with one corner cut off, which falls short of the ceiling by 1 in 100, and a triangle, which does not)
def polygon(normals, hs):                         # the corners of the polygon whose sides have these outward normals (degrees) at these distances
    P = []
    for i in range(len(hs)):
        a1, a2 = math.radians(normals[i]), math.radians(normals[(i + 1) % len(hs)]); A = np.array([[math.cos(a1), math.sin(a1)], [math.cos(a2), math.sin(a2)]]); P.append(np.linalg.solve(A, [hs[i], hs[(i + 1) % len(hs)]]))
    return np.array(P)
def Terode(P, tag):
    f = os.path.join(TMP, 'poly-%s.txt' % tag); np.savetxt(f, P, fmt='%.12f'); a = J([os.path.join(DIR, 'erode'), 'file:' + f, '16384', '1e-4', '1e-3']); b = J([os.path.join(DIR, 'erode'), 'file:' + f, '16384', '3e-5', '1e-3'])
    return None if a is None or b is None else b['T'] + (b['T'] - a['T']) / ((1e-4 / 3e-5) ** (2 / 3.0) - 1)
def green(th):                                    # the kernel of L^(-1) on the circle, cos and sin left out: (1/2pi)(1 - 2 sum_{m>=2} cos(m th)/(m^2-1))
    th = th % (2 * math.pi); return (1 - 2 * (0.5 + math.cos(th) / 4 - (math.pi - th) / 2 * math.sin(th))) / (2 * math.pi)
ms = np.arange(2, 200001); series = lambda th: (1 - 2 * float((np.cos(ms * th) / (ms ** 2 - 1.0)).sum())) / (2 * math.pi)
check('the kernel of L^(-1) in closed form is its series (at 0.3, 2 and 5 radians)', all(abs(green(t) - series(t)) < 1e-5 for t in (0.3, 2.0, 5.0)))
for name, normals, hs, flowname in (('cut square', [270, 0, 45, 90, 180], [0.5, 0.5, 0.1 / math.sqrt(2), 0.5, 0.5], 'poly:0,0,1,0,1,0.1,0.1,1,0,1'), ('triangle', [270, 30, 150], [0.6, 0.6, 0.6], 'triangle')):
    P0 = polygon(normals, hs); A0 = 0.5 * abs(sum(P0[i][0] * P0[(i + 1) % len(P0)][1] - P0[(i + 1) % len(P0)][0] * P0[i][1] for i in range(len(P0))))
    T0 = Terode(P0, name.replace(' ', '')); d = 0.02; g = []          # 0.01 is worse (the noise of the erosion's own steps), 0.05 is worse (the cut side is 0.07 from the centre)
    for e in range(len(hs)):
        hp = list(hs); hp[e] += d; hm = list(hs); hm[e] -= d; tp, tm = Terode(polygon(normals, hp), 'p%d' % e), Terode(polygon(normals, hm), 'm%d' % e); g.append(None if tp is None or tm is None else (tp - tm) / (2 * d))
    if T0 is None or any(x is None for x in g): check('erode: I for the %s from the gradient of T by moved sides' % name, False, 'a run failed'); continue
    g = np.array(g); ang = np.radians(normals)
    check('erode, %s: moving the sides, sum of g h = (4/3) T and sum of g n = 0 (to 5 in 10,000)' % name, abs(float(g @ np.array(hs)) / (4 / 3 * T0) - 1) < 5e-4 and abs(float(g @ np.cos(ang))) < 5e-4 * T0 and abs(float(g @ np.sin(ang))) < 5e-4 * T0, 'sum g h / (4T/3) = %.5f' % (float(g @ np.array(hs)) / (4 / 3 * T0)))
    Ifd = 1.5 * sum(g[i] * g[j] * green(ang[i] - ang[j]) for i in range(len(g)) for j in range(len(g)))
    fl = {q: J([os.path.join(DIR, 'flow'), flowname, '1536', '-q', q]) for q in ('0.5', '0.25')}
    if any(v is None for v in fl.values()): check('flow: runs on the %s' % name, False); continue
    Ifl = (2 * fl['0.25']['I_edge'] - fl['0.5']['I_edge']) * (A0 / math.pi) ** (1 / 3.0); Tfl = (2 * fl['0.25']['T'] - fl['0.5']['T']) * (A0 / math.pi) ** (2 / 3.0)
    check('%s: I from erode.c alone (gradient of T by moved sides, then the edge formula) is flow.c\'s I to 1 in 1,000%s' % (name, ', and both fall short of (4/3) T^2/A by more than 1 in 100 of T^2/A' if name != 'triangle' else ''), abs(Ifd / Ifl - 1) < 1e-3 and (name == 'triangle' or (Ifd * A0 / T0 ** 2 < 4 / 3 - 0.01 and Ifl * A0 / Tfl ** 2 < 4 / 3 - 0.01)), 'erode %.6f, flow %.6f, ratio %.5f; I A/T^2 erode %.5f flow %.5f' % (Ifd, Ifl, Ifd / Ifl, Ifd * A0 / T0 ** 2, Ifl * A0 / Tfl ** 2))
e1 = J([os.path.join(DIR, 'erode'), 'disc', '8192', '1e-4', '1e-3']); e2 = J([os.path.join(DIR, 'erode'), 'ellipse', '8192', '1e-4', '1e-3'])
check('erode: the disc and the ellipse vanish in 3/4 (to 5 in 10,000), and the Cauchy bound there is 3/(4 pi) to 1 in 1,000', e1 is not None and e2 is not None and abs(e1['T'] / 0.75 - 1) < 5e-4 and abs(e2['T'] / 0.75 - 1) < 5e-4 and abs(e1['lower'] / (3 / (4 * math.pi)) - 1) < 1e-3, '' if e1 is None else 'T %.5f lower %.5f' % (e1['T'], e1['lower']))

# ---------- smake.py and the way through peel ----------
o1 = os.path.join(TMP, 'm1.jsonl'); o2 = os.path.join(TMP, 'm2.jsonl'); o3 = os.path.join(TMP, 'm3.jsonl'); o4 = os.path.join(TMP, 'm4.jsonl')
r1 = run([PY, '-I', os.path.join(DIR, 'smake.py'), 'triangle', 'exact', '3000', '401', '5000', o1, '4']); r2 = run([PY, '-I', os.path.join(DIR, 'smake.py'), 'triangle', 'exact', '3000', '401', '5000', o2, '2'])
r3 = run([PY, '-I', os.path.join(DIR, 'smake.py'), 'hexagon', 'chance', '3000', '400', '6000', o3, '4']); r4 = run([PY, '-I', os.path.join(DIR, 'smake.py'), 'disc0', 'exact', '3000', '50', '5000', o4, '4'])
def lines(f):
    try: return [json.loads(l) for l in open(f)]
    except Exception: return []
L1, L2, L3, L4 = lines(o1), lines(o2), lines(o3), lines(o4)
check('smake: 401 clouds asked, 401 lines, each of exactly 3,000 points, seeds 5001 to 5401 in order', len(L1) == 401 and all(o['n'] == 3000 and o['n0'] == 3000 and o['shape'] == 'triangle' and o['kind'] == 'exact' for o in L1) and [o['seed'] for o in L1] == list(range(5001, 5402)))
check('smake: the same again with other workers gives the same file', len(L1) == 401 and open(o1).read() == open(o2).read())
check('smake: every 200th cloud was peeled both ways and the two agreed; the others one way', len(L1) == 401 and [o['same'] for o in L1] == [1 if i % 200 == 0 else -1 for i in range(401)])
ns = np.array([o['n'] for o in L3], float)
check('smake: left to chance, the numbers of points have mean 3,000 and variance 3,000 (within 4 standard errors) and are what numpy gives for that seed', len(L3) == 400 and abs(ns.mean() - 3000) < 4 * math.sqrt(3000 / 400) and abs(ns.var(ddof=1) / 3000 - 1) < 4 * math.sqrt(2 / 399) and list(ns.astype(int)) == [int(v) for v in np.random.default_rng(6000).poisson(3000, 400)], 'mean %.1f var %.0f' % (ns.mean() if len(ns) else 0, ns.var(ddof=1) if len(ns) > 1 else 0))
if len(L1) == 401:
    f = os.path.join(TMP, 'one.txt'); subprocess.run([os.path.join(DIR, 'cloud'), 'triangle', '3000', '5003'], stdout=open(f, 'w')); a = J([PEEL, 'file:' + f, '0', '0', '-plain'])
    pts = open(f).read().split('\n')[:-1]; g = os.path.join(TMP, 'rev.txt'); open(g, 'w').write('\n'.join(reversed(pts)) + '\n'); b = J([PEEL, 'file:' + g, '0', '0', '-fast'])
    check('smake: the count of cloud 5003 is what peel gives, by the plain method, for cloud.c\'s file of that seed; and the same with the points in reverse order', a is not None and b is not None and a['layers'] == L1[2]['layers'] == b['layers'], 'layers %s' % (a and a['layers']))
check('smake: the shape disc0 is peel\'s own disc of that seed', len(L4) == 50 and (J([PEEL, 'disc', '3000', '5007']) or {}).get('layers') == L4[6]['layers'])
f = os.path.join(TMP, 'hand.txt'); open(f, 'w').write('0 0\n100 0\n100 100\n0 100\n50 50\n40 60\n60 60\n50 40\n50 55\n'); a = J([PEEL, 'file:' + f, '0', '0', '-both'])
check('peel: nine points by hand (a square, a triangle inside it, two points inside that) make three layers, by both methods', a is not None and a['layers'] == 3 and a.get('same') == 1, str(a and a['layers']))
check('smake: nothing of its own is left in /dev/shm', not [x for x in os.listdir('/dev/shm') if x.startswith('agent2-shape-')])
mt = np.array([o['layers'] for o in L1], float)
check('smake: the mean count of 401 triangles of 3,000 points is within 2 in 100 of alpha rho^(2/3) T (finite-size effects are larger at 3,000)', len(L1) == 401 and abs(mt.mean() / (1.3259 * (3000 / math.pi) ** (2 / 3.0) * 0.81991) - 1) < 0.02, '%.2f against %.2f' % (mt.mean() if len(mt) else 0, 1.3259 * (3000 / math.pi) ** (2 / 3.0) * 0.81991))

# ---------- theory.py ----------
r = run([PY, '-I', '-c', 'import sys, json; sys.path.insert(0, %r); import theory; print(json.dumps([theory.predictions("disc", 1e5), theory.predictions("triangle", 1e5), theory.TH["rtriangle"]["I"], theory.TH["rtriangle"]["T"]]))' % DIR])
try: pd, pt, Irt, Trt = json.loads(r.stdout)
except Exception: pd = None
check('theory: the disc at 100,000 points: mean 998.79, variance 8.179 (chance) and 3.745 (exactly n), as ../disc/dtheory.py has them', pd is not None and abs(pd['mean'] - 998.79) < 0.02 and abs(pd['chance'] - 8.179) < 0.004 and abs(pd['exact'] - 3.745) < 0.004, str(pd))
check('theory: the triangle: variance over the square of the mean, times n, is (4 D / 3 - (4/9) alpha^2) / alpha^2 = 0.3754 with exactly n and 0.8199 left to chance', pd is not None and abs(pt['exact'] / pt['mean'] ** 2 * 1e5 - 0.3754) < 3e-4 and abs(pt['chance'] / pt['mean'] ** 2 * 1e5 - 0.8199) < 3e-4)
check('theory: the rounded triangle has I A / T^2 = 1.3056', pd is not None and abs(Irt * math.pi / Trt ** 2 - 1.3056) < 2e-4)
import shutil; shutil.rmtree(TMP)
print('%d passed, %d failed' % (passed, failed)); sys.exit(1 if failed else 0)
