"""page-mutants.py: break the page's own script on purpose, one fault at a time, build each broken page and run the
headless test on it. First a control: the true page must pass with all its assertions, or "caught" would mean nothing
(a test that cannot start also "fails").      python -I page-mutants.py       The test is run from ~/web."""
import os, shutil, subprocess, sys, re
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); WORK = os.path.join(HERE, 'mutants-page'); WEB = os.path.expanduser('~/web')
rd = lambda n: open(os.path.join(HERE, n), encoding='utf-8').read()
SRC = rd('page.src.html'); CORE = rd('ocore.js')
M = [
 ('tile-layers-shows-the-disc', "tile('tile-n', fmt(N),", "tile('tile-n', fmt(D),"),
 ('tile-first-layer-is-the-second', "the first layer has ' + S.peel.sizes[1] + ', the last '", "the first layer has ' + S.peel.sizes[2] + ', the last '"),
 ('tile-difference-always-plus', "tile('tile-diff', (diff >= 0 ? '+' : '−') + Math.abs(diff).toFixed(1) + '%',", "tile('tile-diff', '+' + Math.abs(diff).toFixed(1) + '%',"),
 ('tile-spread-wrong', "var spread = 1.32 * Math.pow(S.n / 10000, 0.176);", "var spread = 1.0 * Math.pow(S.n / 10000, 0.176);"),
 ('tile-disc-with-four-thirds', "tile('tile-disc', 'about ' + fmt(D),", "tile('tile-disc', 'about ' + fmt(D * (4 / 3) / 1.326),"),
 ('layers-taken-away-still-drawn', "for (i = 0; i < n; i++) if (d[i] > S.k) buckets[", "for (i = 0; i < n; i++) if (d[i] > 0) buckets["),
 ('orange-ring-is-the-layer-just-gone', "      var k1 = S.k + 1;\n", "      var k1 = Math.max(1, S.k);\n"),
 ('tenth-rings-one-layer-out', "var kk = 1 + Math.floor(b * N / 10);", "var kk = Math.floor(b * N / 10);"),
 ('tenth-rings-shown-when-gone', "if (kk > S.k + 1 && kk <= N && S.peel.sizes[kk] >= 3) over.appendChild", "if (kk <= N && S.peel.sizes[kk] >= 3) over.appendChild"),
 ('points-left-counts-one-layer-too-many', "var left = 0; for (i = S.k + 1; i <= N; i++) left += S.peel.sizes[i];", "var left = 0; for (i = Math.max(1, S.k); i <= N; i++) left += S.peel.sizes[i];"),
 ('next-layer-size-is-this-layer', "points are left. The next layer has <b>' + S.peel.sizes[S.k + 1] + '</b> points.'", "points are left. The next layer has <b>' + S.peel.sizes[Math.max(1, S.k)] + '</b> points.'"),
 ('cloud-runs-off-the-picture', "var s = Math.min((W - 2 * pad) / Math.max(1, x1 - x0), (H - 2 * pad) / Math.max(1, y1 - y0));", "var s = (W - 2 * pad) / Math.max(1, x1 - x0);"),
 ('view-not-refitted-after-stretching', "    if (S.k > S.peel.layers) S.k = S.peel.layers;\n    fit();", "    if (S.k > S.peel.layers) S.k = S.peel.layers;\n    if (!S.view) fit();"),
 ('picture-upside-down', "function sy(v) { return S.view.oy - S.view.s * v; }", "function sy(v) { return S.view.oy + S.view.s * v; }"),
 ('rings-not-where-the-points-are', "function ringPoints(k) { return O.ring(S.cloud.x, S.cloud.y, S.peel.depth, k).map(function (i) { return sx(S.cloud.x[i]).toFixed(1)", "function ringPoints(k) { return O.ring(S.cloud.x, S.cloud.y, S.peel.depth, k).map(function (i) { return (sx(S.cloud.x[i]) + 3).toFixed(1)"),
 ('stretch-button-does-not-stretch', "if (S.stretched) { S.cloud = O.stretch(S.base.x, S.base.y); S.peel = O.peel(S.cloud.x, S.cloud.y); }", "if (false) { S.cloud = O.stretch(S.base.x, S.base.y); S.peel = O.peel(S.cloud.x, S.cloud.y); }"),
 ('stretched-not-said', "(S.stretched ? ' ' + stretchSays() : '');", "'';"),
 ('new-cloud-is-the-same-cloud', "function fresh() { stop(); S.k = 0; S.seed += 1; S.n = Number($('n').value);", "function fresh() { stop(); S.k = 0; S.n = Number($('n').value);"),
 ('new-cloud-keeps-layers-taken', "function fresh() { stop(); S.k = 0; S.seed += 1; S.n = Number($('n').value);", "function fresh() { stop(); S.seed += 1; S.n = Number($('n').value);"),
 ('shape-change-stays-stretched', "stop(); S.shape = $('shape').value; S.stretched = false; $('stretch').setAttribute('aria-pressed', 'false');", "stop(); S.shape = $('shape').value;"),
 ('number-of-points-ignored', "S.seed += 1; S.n = Number($('n').value); notice('');", "S.seed += 1; notice('');"),
 ('number-of-points-taken-before-there-is-a-cloud', "$('n').addEventListener('change', function () { if (S.shape === 'own' && !S.poly) return; fresh(); });", "$('n').addEventListener('change', function () { S.n = Number($('n').value); if (S.shape === 'own' && !S.poly) return; fresh(); });"),
 ('seed-shown-is-stale', "f.setAttribute('data-seed', S.seed);", "f.setAttribute('data-seed', S.seed - 1);"),
 ('shade-light-at-the-rim', "var a = [42, 90, 146], b = [183, 213, 247], t = Math.max(0, Math.min(1, f));", "var b = [42, 90, 146], a = [183, 213, 247], t = Math.max(0, Math.min(1, f));"),
 ('chart-line-one-layer-on', "d = ''; for (k = 1; k <= N; k++) d += (k === 1 ? 'M' : 'L') + X(k).toFixed(2) + ',' + Y(sizes[k]).toFixed(2);", "d = ''; for (k = 1; k <= N; k++) d += (k === 1 ? 'M' : 'L') + X(k).toFixed(2) + ',' + Y(sizes[Math.min(N, k + 1)]).toFixed(2);"),
 ('chart-formula-for-twice-the-points', "v = O.discSize(S.n, k); if (v <= 0) break; d += (k === 1 ? 'M' : 'L')", "v = O.discSize(2 * S.n, k); if (v <= 0) break; d += (k === 1 ? 'M' : 'L')"),
 ('chart-axis-labels-one-out', "svg.appendChild(el('text', { x: BOX.l - 6, y: Y(v) + 4, 'text-anchor': 'end' }, String(v))); }", "svg.appendChild(el('text', { x: BOX.l - 6, y: Y(v) + 4, 'text-anchor': 'end' }, String(v + st))); }"),
 ('chart-top-cut-off', "top = Math.max(top, O.discSize(S.n, 1)) * 1.06;", "top = Math.max(top, O.discSize(S.n, 1)) * 0.8;"),
 ('chart-label-runs-off', "svg.appendChild(el('text', { x: X(ka) + 30, y: ya - 42, 'text-anchor': 'start', 'class': 'dlabel' }, 'this cloud'));", "svg.appendChild(el('text', { x: X(ka) + 250, y: ya - 42, 'text-anchor': 'start', 'class': 'dlabel' }, 'this cloud'));"),
 ('chart-mark-left-behind', "    var pick = $('pick'); if (pick && geo) { pick.setAttribute('x1', geo.X(Math.max(1, S.k + 1))); pick.setAttribute('x2', geo.X(Math.max(1, S.k + 1))); }\n", ""),
 ('hover-one-layer-out', "var k = 1 + Math.round((px - BOX.l) / (1000 - BOX.l - BOX.r) * (N - 1));", "var k = Math.round((px - BOX.l) / (1000 - BOX.l - BOX.r) * (N - 1));"),
 ('tooltip-formula-of-the-next-layer', "points; a disc, by the formula, <b>' + O.discSize(S.n, k).toFixed(1) + '</b>.'; }", "points; a disc, by the formula, <b>' + O.discSize(S.n, k + 1).toFixed(1) + '</b>.'; }"),
 ('tooltip-runs-off-the-figure', "tip.style.left = Math.max(4, Math.min(fig.width - tip.offsetWidth - 4, x + 12)) + 'px';", "tip.style.left = (x + 12) + 'px';"),
 ('click-takes-the-layer-itself', "C.addEventListener('click', function (e) { stop(); setK(layerAt(e) - 1); });", "C.addEventListener('click', function (e) { stop(); setK(layerAt(e)); });"),
 ('arrow-key-steps-two', "if (e.key === 'ArrowRight') { hover(Math.min(S.peel.layers, k + 1)); e.preventDefault(); }", "if (e.key === 'ArrowRight') { hover(Math.min(S.peel.layers, k + 2)); e.preventDefault(); }"),
 ('first-layer-sentence-is-the-second', "'The first layer has <b>' + S.peel.sizes[1] + '</b> points, about '", "'The first layer has <b>' + S.peel.sizes[2] + '</b> points, about '"),
 ('table-sizes-one-layer-on', "h += '<tr><td>' + k + '</td><td>' + sizes[k] + '</td><td>'", "h += '<tr><td>' + k + '</td><td>' + sizes[Math.min(N, k + 1)] + '</td><td>'"),
 ('table-button-does-not-open', "$('tab2').className = 'tables' + (on ? ' on' : '');", "$('tab2').className = 'tables';"),
 ('play-never-stops', "setK(S.k + step); if (S.k >= S.peel.layers) { stop(); return; } requestAnimationFrame(tick);", "setK(S.k + step); requestAnimationFrame(tick);"),
 ('play-at-the-end-does-nothing', "    if (S.k >= S.peel.layers) setK(0);\n", ""),
 ('tenths-button-does-not-redraw', "S.tenths = !S.tenths; $('tenths').setAttribute('aria-pressed', S.tenths ? 'true' : 'false'); draw(); });", "S.tenths = !S.tenths; $('tenths').setAttribute('aria-pressed', S.tenths ? 'true' : 'false'); });"),
 ('own-shape-upside-down', "py = s.map(function (p) { return Math.round((H / 2 - p[1]) * sc); });", "py = s.map(function (p) { return Math.round((p[1] - H / 2) * sc); });"),
 ('own-small-loop-taken', "if (s.length < 8 || filled(px, py) < 0.02 * 4 * 1.6 * 1.6 * O.RAD * O.RAD) {", "if (s.length < 3) {"),
 ('own-area-by-signed-sum', "if (s.length < 8 || filled(px, py) < 0.02 * 4 * 1.6 * 1.6 * O.RAD * O.RAD) {", "if (s.length < 8 || O.polygonArea(px, py) < 0.02 * 4 * 1.6 * 1.6 * O.RAD * O.RAD) {"),
 ('own-loop-not-held-at-the-edge', "return [Math.max(0, Math.min(W, (e.clientX - b.left) / b.width * W)), Math.max(0, Math.min(H, (e.clientY - b.top) / b.height * H))]; }", "return [(e.clientX - b.left) / b.width * W, (e.clientY - b.top) / b.height * H]; }"),
 ('own-shape-asks-for-nothing', "if (S.shape === 'own' && !S.poly) { notice('Draw a closed loop on the picture: press, go round, and let go.'); $('fig1').setAttribute('data-shape', 'own'); return; }", "if (S.shape === 'own' && !S.poly) { $('fig1').setAttribute('data-shape', 'own'); return; }"),
 ('stretch-before-a-shape-is-drawn', "if (!S.base || (S.shape === 'own' && !S.poly)) return; stop();", "if (!S.base) return; stop();"),
 ('own-shape-points-anywhere', "S.poly = { x: px, y: py }; S.stretched = false;", "S.poly = { x: px.map(function (v) { return Math.round(v * 0.5); }), y: py }; S.stretched = false;"),
]
def build(name, old, new):
    d = os.path.join(WORK, name); os.makedirs(d, exist_ok=True); s = SRC
    if old is not None:
        if s.count(old) != 1: raise SystemExit('mutant %s: pattern found %d times' % (name, s.count(old)))
        s = s.replace(old, new)
    open(os.path.join(d, 'peel.html'), 'w', encoding='utf-8').write(s.replace('/*CORE*/', CORE))
    return d
def run(d):
    env = dict(os.environ, LD_LIBRARY_PATH=os.path.join(WEB, 'sysroot/usr/lib/x86_64-linux-gnu'))
    try: r = subprocess.run(['node', 'shot-peel.js', os.path.join(d, 'peel.html'), d, os.path.join(HERE, 'ocore.js')], cwd=WEB, env=env, capture_output=True, text=True, timeout=900)
    except subprocess.TimeoutExpired: return None, ['TIMEOUT']
    m = re.search(r'PAGE TEST: (\d+) assertions, (\d+) failed', r.stdout)
    return (m.groups() if m else None), [l[8:] for l in r.stdout.split('\n') if l.startswith('FAILED: ')] + ([] if m else [(r.stderr.strip().split('\n') or [''])[0][:160]])
if os.path.isdir(WORK): shutil.rmtree(WORK)
res, fails = run(build('CONTROL', None, None))
print('control (the true page): %s' % ('%s assertions, %s failed' % res if res else 'THE TEST DID NOT FINISH: ' + '; '.join(fails)))
if not res or res[1] != '0': sys.exit('the control does not pass; nothing below would mean anything')
dirs = [(name, build(name, old, new)) for name, old, new in M]
with ThreadPoolExecutor(max_workers=5) as ex: out = list(ex.map(lambda nd: (nd[0],) + run(nd[1]), dirs))
caught = 0; passed = []; crashed = []
for name, res, fails in out:
    if res is None: caught += 1; crashed.append(name); print('caught   %-40s the test could not finish: %s' % (name, (fails[0] if fails else '')[:120]))
    elif res[1] != '0': caught += 1; print('caught   %-40s by %s: %s' % (name, res[1], fails[0][:120]))
    else: passed.append(name); print('PASSED   %s' % name)
print('\n%d of %d broken pages caught (%d of them because the test could not finish: %s); passed: %s' % (caught, len(M), len(crashed), ', '.join(crashed) or 'none', ', '.join(passed) or 'none'))
