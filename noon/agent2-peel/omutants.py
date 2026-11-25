"""omutants.py: break ocore.js, peel.c and cell.c on purpose, one fault at a time, and run otest.js on each broken
copy. A fault the tests do not notice is a hole in the tests. First a control: an unbroken copy, built and run by the
very same steps, must pass, or "caught" would mean nothing.     python -I omutants.py
"""
import os, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); WORK = os.path.join(HERE, 'mutants')
FILES = ['ocore.js', 'otest.js', 'peel.c', 'cell.c']
M = [
 # --- ocore.js ---
 ('js-turn-reversed', 'ocore.js', "return v > 0 ? 1 : v < 0 ? -1 : 0;", "return v > 0 ? -1 : v < 0 ? 1 : 0;"),
 ('js-points-on-a-lower-side-left-behind', 'ocore.js', "              if (turn(x, y, hull[lo], hull[lo + 1], p) === 0) on = true;\n              else {", "              if (false) on = true;\n              else {"),
 ('js-points-on-an-upper-side-left-behind', 'ocore.js', "if (turn(x, y, hull[up % k], hull[up - 1], p) === 0) on = true;", "if (false) on = true;"),
 ('js-right-upright-side-forgotten', 'ocore.js', "if (x[p] === xmin || x[p] === xmax) on = true;", "if (x[p] === xmin) on = true;"),
 ('js-points-in-a-line-not-one-layer', 'ocore.js', "if (k <= 2) { for (i = 0; i < m; i++) depth[cur[i]] = layer; removed = m; }", "if (k <= 1) { for (i = 0; i < m; i++) depth[cur[i]] = layer; removed = m; }"),
 ('js-upper-chain-starts-at-the-last', 'ocore.js', "for (i = m - 2, t = k + 1; i >= 0; i--) {", "for (i = m - 2, t = k; i >= 0; i--) {"),
 ('js-lower-edge-pointer-stuck', 'ocore.js', "while (lo + 1 < topV && x[hull[lo + 1]] <= x[p]) lo++;", ""),
 ('js-coordinates-not-checked', 'ocore.js', "if (!(Math.abs(x[i]) < LIMIT && Math.abs(y[i]) < LIMIT) || x[i] !== Math.floor(x[i]) || y[i] !== Math.floor(y[i])) throw", "if (false) throw"),
 ('js-disc-is-a-smaller-disc', 'ocore.js', "if (a * a + b * b > RAD * RAD) continue; }", "if (a * a + b * b > RAD * RAD / 2) continue; }"),
 ('js-ellipse-axes-swapped', 'ocore.js', "var ea = Math.floor(RAD * Math.sqrt(3)), eb = Math.floor(RAD / Math.sqrt(3)),", "var eb = Math.floor(RAD * Math.sqrt(3)), ea = Math.floor(RAD / Math.sqrt(3)),"),
 ('js-square-too-small', 'ocore.js', "var sqHalf = Math.floor(RAD * Math.sqrt(Math.PI) / 2),", "var sqHalf = Math.floor(RAD * Math.sqrt(Math.PI) / 2.2),"),
 ('js-triangle-upside-down-test', 'ocore.js', "if (Math.abs(a) * hgt > hb * (top - b)) continue;", "if (Math.abs(a) * hgt > hb * (b - bot)) continue;"),
 ('js-own-shape-ignored', 'ocore.js', "if (!inside(poly.x, poly.y, a, b)) continue; }", "}"),
 ('js-own-shape-cut-off-at-a-box', 'ocore.js', "a = Math.floor(bx0 + rand() * (bx1 - bx0)); b = Math.floor(by0 + rand() * (by1 - by0));", "a = Math.floor(Math.max(bx0, -1.6 * RAD) + rand() * (Math.min(bx1, 1.6 * RAD) - Math.max(bx0, -1.6 * RAD))); b = Math.floor(by0 + rand() * (by1 - by0));"),
 ('js-stretch-is-another-map', 'ocore.js', "X[i] = 3 * x[i] + y[i]; Y[i] = y[i];", "X[i] = 3 * x[i] - y[i]; Y[i] = y[i];"),
 ('js-stretch-squashes-flat', 'ocore.js', "X[i] = 3 * x[i] + y[i]; Y[i] = y[i];", "X[i] = 3 * x[i] + y[i]; Y[i] = Math.round(y[i] / 64);"),
 ('js-ring-clockwise', 'ocore.js', "return Math.atan2(y[p] - cy, x[p] - cx) - Math.atan2(y[q] - cy, x[q] - cx) || p - q; });", "return Math.atan2(y[q] - cy, x[q] - cx) - Math.atan2(y[p] - cy, x[p] - cx) || p - q; });"),
 ('js-ring-of-the-next-layer', 'ocore.js', "for (i = 0; i < depth.length; i++) if (depth[i] === k) { idx.push(i); cx += x[i]; cy += y[i]; }", "for (i = 0; i < depth.length; i++) if (depth[i] === k + 1) { idx.push(i); cx += x[i]; cy += y[i]; }"),
 ('js-constant-is-four-thirds', 'ocore.js', "var ALPHA = 1.326;", "var ALPHA = 4 / 3;"),
 ('js-disc-layers-without-three-quarters', 'ocore.js', "return 0.75 * ALPHA * Math.pow(n / Math.PI, 2 / 3); }", "return ALPHA * Math.pow(n / Math.PI, 2 / 3); }"),
 ('js-disc-size-straight-not-root', 'ocore.js', "Math.pow(n, 1 / 3) * Math.sqrt(f) : 0;", "Math.pow(n, 1 / 3) * f : 0;"),
 ('js-atot-without-four-thirds', 'ocore.js', "return (4 / 3) * layers / Math.pow(n / Math.PI, 2 / 3); }", "return layers / Math.pow(n / Math.PI, 2 / 3); }"),
 ('js-inside-is-outside', 'ocore.js', "    return c;\n  }\n  function polygonArea", "    return !c;\n  }\n  function polygonArea"),
 ('js-area-doubled', 'ocore.js', "return Math.abs(s) / 2;", "return Math.abs(s);"),
 ('js-roundness-upside-down', 'ocore.js', "return mn > 0 && mx > 0 ? mx / mn : NaN;", "return mn > 0 && mx > 0 ? mn / mx : NaN;"),
 # --- peel.c ---
 ('c-turn-reversed', 'peel.c', "    return (v > 0) - (v < 0);\n}\n\n/* ---------- random numbers", "    return (v < 0) - (v > 0);\n}\n\n/* ---------- random numbers"),
 ('c-points-on-a-lower-side-left-behind', 'peel.c', "                if (turn(hull[lo], hull[lo + 1], p) == 0) on = 1;", "                if (0) on = 1;"),
 ('c-right-upright-side-forgotten', 'peel.c', "if (X[p] == xmin || X[p] == xmax) on = 1;", "if (X[p] == xmin) on = 1;"),
 ('c-points-in-a-line-not-one-layer', 'peel.c', "    if (k <= 2) {                                           /* everything left is in one line (or one place) */", "    if (k <= 1) {"),
 ('c-vertices-mode-takes-the-whole-boundary', 'peel.c', "    if (verticesOnly) {\n        for (i = 0; i < k; i++)", "    if (0) {\n        for (i = 0; i < k; i++)"),
 ('c-sectors-bound-too-far-out', 'peel.c', "d2 = cr * cr / (ex * ex + ey * ey) * (1 - 1e-9);", "d2 = cr * cr / (ex * ex + ey * ey) * (1 + 3e-3);"),
 ('c-sectors-tight-bound-too-tight', 'peel.c', "                        if (r2 > lim) lim = r2;", "                        if (r2 > lim) lim = r2 * 1.02;"),
 ('c-sectors-foot-test-dropped', 'peel.c', "if (c0 < -1e-6 * fr || c1 > 1e-6 * fr) {            /* the foot is clearly outside this sector */", "if (1) {"),
 ('c-sectors-removed-points-still-outermost', 'peel.c', "            while (top[b] < start[b + 1] && depth[list[top[b]].idx] != 0) top[b]++;\n            if (top[b] < start[b + 1]) { s0[m0] = list[top[b]].idx; s0sec[m0] = b; m0++; }", "            if (top[b] < start[b + 1]) { s0[m0] = list[top[b]].idx; s0sec[m0] = b; m0++; }"),
 ('c-sectors-nearest-first', 'peel.c', "    if (p->r2 != q->r2) return p->r2 > q->r2 ? -1 : 1;", "    if (p->r2 != q->r2) return p->r2 < q->r2 ? -1 : 1;"),
 ('c-sectors-edge-covers-one-sector-only', 'peel.c', "                if (lim < rho2[b]) rho2[b] = lim;\n                if (b == bv) break;", "                if (lim < rho2[b]) rho2[b] = lim;\n                break;"),
 ('c-disc-is-a-square', 'peel.c', "if (x * x + y * y <= RAD * RAD) { X[i] = (coord)x; Y[i] = (coord)y; i++; } }\n    } else if (!strcmp(shape, \"square\")) {", "if (1) { X[i] = (coord)x; Y[i] = (coord)y; i++; } }\n    } else if (!strcmp(shape, \"square\")) {"),
 ('c-points-crowd-the-middle', 'peel.c', "while (i < n) { x = (i64)(next() >> 34) - RAD; y = (i64)(next() >> 34) - RAD; if (x * x + y * y <= RAD * RAD)", "while (i < n) { x = ((i64)(next() >> 34) - RAD) / 2; y = ((i64)(next() >> 34) - RAD) / 2; if (x * x + y * y <= RAD * RAD)"),
 ('c-triangle-lopsided', 'peel.c', "#define TRI_TOP 834898854LL", "#define TRI_TOP 734898854LL"),
 ('c-atot-without-four-thirds', 'peel.c', "           (4.0 / 3.0) * N / K, slope, (4.0 / 3.0) * slope / K,", "           N / K, slope, (4.0 / 3.0) * slope / K,"),
 ('c-slope-over-a-wider-ring', 'peel.c', "if (r >= 0.3 && r <= 0.9) { su += u;", "if (r >= 0.2 && r <= 0.9) { su += u;"),
 ('c-slope-through-the-origin', 'peel.c', "double slope = cnt > 2 ? (sud - su * sd2 / cnt) / (suu - su * su / cnt) : 0;", "double slope = cnt > 2 ? sud / suu : 0;"),
 ('c-sizes-fitted-over-all-layers', 'peel.c', "if (f >= 0.1 && f <= 0.7) { double w = sqrt(1 - f);", "if (f >= 0.0 && f <= 1.0) { double w = sqrt(1 - f);"),
 ('c-layers-20-to-40-are-21-to-40', 'peel.c', "for (k = 20; k <= 40 && k <= N; k++) { mean2040 += sizes[k]; c2040++; }", "for (k = 21; k <= 40 && k <= N; k++) { mean2040 += sizes[k]; c2040++; }"),
 ('c-half-depth-is-four-tenths', 'peel.c', "int k1 = (int)floor(0.5 * N + 0.5),", "int k1 = (int)floor(0.4 * N + 0.5),"),
 ('c-affine-is-another-map', 'peel.c', "for (i = 0; i < n; i++) X[i] = 3 * X[i] + Y[i];", "for (i = 0; i < n; i++) X[i] = 2 * X[i] + Y[i];"),
 ('c-unwritable-file-ignored', 'peel.c', "    if (!f) { fprintf(stderr, \"cannot write to %s\\n\", name); exit(3); }", "    if (!f) return stdout;"),
 # --- cell.c ---
 ('cell-no-lift', 'cell.c', "    wide ax = XU[a], ay = (wide)YU[a] + (wide)XU[a] * XU[a], bx = XU[b], by = (wide)YU[b] + (wide)XU[b] * XU[b], cx = XU[c], cy = (wide)YU[c] + (wide)XU[c] * XU[c];",
    "    wide ax = XU[a], ay = (wide)YU[a], bx = XU[b], by = (wide)YU[b], cx = XU[c], cy = (wide)YU[c];"),
 ('cell-lift-doubled', 'cell.c', "    wide ax = XU[a], ay = (wide)YU[a] + (wide)XU[a] * XU[a], bx = XU[b], by = (wide)YU[b] + (wide)XU[b] * XU[b], cx = XU[c], cy = (wide)YU[c] + (wide)XU[c] * XU[c];",
    "    wide ax = XU[a], ay = (wide)YU[a] + 2 * (wide)XU[a] * XU[a], bx = XU[b], by = (wide)YU[b] + 2 * (wide)XU[b] * XU[b], cx = XU[c], cy = (wide)YU[c] + 2 * (wide)XU[c] * XU[c];"),
 ('cell-columns-margin-dropped', 'cell.c', "            double lim = bound[c] * (1 + 1e-9) + margin;", "            double lim = bound[c] * (1 - 2e-4) - margin;"),
 ('cell-columns-one-end-only', 'cell.c', "                t = (b - xu) / (xv - xu); y = lu + (lv - lu) * t - b * b; if (y > bound[c]) bound[c] = y;\n", ""),
 ('cell-columns-removed-points-still-lowest', 'cell.c', "            while (top[c] < start[c + 1] && depth[list[top[c]].idx] != 0) top[c]++;\n", ""),
 ('cell-slope-over-the-upper-half-only', 'cell.c', "for (q = 0; q < 2; q++) if (y >= (q ? 0.5 : 0.2) * HM)", "for (q = 0; q < 2; q++) if (y >= (q ? 0.5 : 0.6) * HM)"),
 ('cell-margin-a-tenth', 'cell.c', "    double HM = HD / 1.25, marg = mfac * sqrt(2 * HM);", "    double HM = HD / 1.25, marg = 0.1 * mfac * sqrt(2 * HM);"),
]
def build(name, f, old, new):
    d = os.path.join(WORK, name); os.makedirs(d, exist_ok=True)
    for x in FILES:
        s = open(os.path.join(HERE, x), encoding='utf-8').read()
        if x == f:
            if s.count(old) != 1: raise SystemExit('mutant %s: pattern found %d times in %s' % (name, s.count(old), f))
            s = s.replace(old, new)
        open(os.path.join(d, x), 'w', encoding='utf-8').write(s)
    for out, extra, src in (('peel', [], 'peel.c'), ('peel-wide', ['-DWIDE'], 'peel.c'), ('cell', [], 'cell.c')):
        r = subprocess.run(['gcc', '-O2'] + extra + ['-o', os.path.join(d, out), os.path.join(d, src), '-lm'], capture_output=True, text=True)
        if r.returncode: raise SystemExit('mutant %s does not compile: %s' % (name, r.stderr[:300]))
    return d
def run(d):
    try: r = subprocess.run(['node', os.path.join(d, 'otest.js')], capture_output=True, text=True, timeout=420)
    except subprocess.TimeoutExpired:
        subprocess.run(['pkill', '-f', '^' + d + '/'])
        return 1, ['TIMEOUT']
    return r.returncode, [l for l in r.stdout.split('\n') if l.startswith('FAIL')] + ([r.stderr.strip().split('\n')[-1][:150]] if r.returncode and r.stderr.strip() and 'FAIL' not in r.stdout else [])
if os.path.isdir(WORK): shutil.rmtree(WORK)
code, fails = run(build('CONTROL', None, None, None))
print('control (nothing broken): %s' % ('passes' if code == 0 else 'FAILS: ' + '; '.join(fails)))
if code != 0: sys.exit('the control does not pass; nothing below would mean anything')
dirs = [(name, build(name, f, old, new)) for name, f, old, new in M]
with ThreadPoolExecutor(max_workers=6) as ex: out = list(ex.map(lambda nd: (nd[0],) + run(nd[1]), dirs))
caught = 0; passed = []
for name, code, fails in out:
    if code != 0: caught += 1; print('caught   %-44s by %d: %s' % (name, len(fails), (fails[0] if fails else '')[:100]))
    else: passed.append(name); print('PASSED   %s' % name)
print('\n%d of %d broken copies caught; passed: %s' % (caught, len(M), ', '.join(passed) or 'none'))
