# page-mutants.py -- can the page test fail?  The true page is built and run first by the same command (the control); then
# copies with one thing broken in the page's own script.   python -I page-mutants.py
import subprocess, os, re
here = os.path.dirname(os.path.abspath(__file__)); rd = lambda n: open(os.path.join(here, n), encoding='utf-8').read()
src = rd('page.src.html'); core = rd('ccore.js')
M = [
 ('turning-of-the-start', "the turning number shown is the first curve's, whatever the curve now is", "var w = now(), pts = w.pts, i, q, cr = C.crossings(pts), n = C.turning(pts),", "var w = now(), pts = w.pts, i, q, cr = C.crossings(pts), n = A.n,"),
 ('always-the-plain-way', "the plain way is drawn whichever way is chosen", "if (way === 'w' && laid) return C.whitney(A, B, u()); return C.straight(A, B, u()); }", "return C.straight(A, B, u()); }"),
 ('slider-in-hundredths', "the slider's thousandths are read as hundredths", "function u() { return +$('u').value / 1000; }", "function u() { return Math.min(1, +$('u').value / 100); }"),
 ('whitney-offered-anyway', "Whitney's way stays chosen when the turning numbers differ", "if (!laid && $('way').value === 'w') $('way').value = 'p'; $('u').value = 0; chart(); draw(); }", "$('u').value = 0; chart(); draw(); }"),
 ('kinks-of-the-target', "the opposed places are counted between the target and itself", "kinkList = C.kinks(A, B); series = null;", "kinkList = C.kinks(B, B); series = null;"),
 ('lost-never-marked', "the places where the direction is lost are never marked", "if (sp < 0.12) lost.push(i); }", "}"),
 ('arrow-ten-times', "an arrow key moves a tenth of the way", "var d = e.key === 'ArrowRight' ? 10 : e.key === 'ArrowLeft' ? -10 : 0;", "var d = e.key === 'ArrowRight' ? 100 : e.key === 'ArrowLeft' ? -100 : 0;"),
 ('play-never-ends', "Play does not stop at the end", "if (v >= 1000) { $('u').value = 1000; draw(); stop(); return; }", "if (v >= 1000) { $('u').value = 0; draw(); }"),
 ('drawing-not-mirrored', "a curve drawn is taken with the screen's downward heights", "C.resample(d.map(function (p) { return [p[0], -p[1]]; }), N)", "C.resample(d.map(function (p) { return [p[0], p[1]]; }), N)"),
 ('short-strokes-taken', "a stroke of any length is taken as a curve", "if (d.length < 12 || C.length(d) < 200) { draw(); return; }", "if (d.length < 2) { draw(); return; }"),
 ('series-swapped', "the chart's two lines are each other's", "out.p.push(C.straight(A, B, t).least); out.w.push(laid ? C.whitney(A, B, t).least : null);", "out.w.push(C.straight(A, B, t).least); out.p.push(laid ? C.whitney(A, B, t).least : 0);"),
 ('table-off-by-a-row', "the table's rows are one step late", "+ '</td><td>' + series.p[i].toFixed(3) + '</td></tr>'; $('tab2')", "+ '</td><td>' + series.p[Math.min(100, i + 5)].toFixed(3) + '</td></tr>'; $('tab2')"),
 ('target-off-by-one', "the target chosen is the next in the list", "var t = TARGETS[+$('target').value][1],", "var t = TARGETS[Math.min(5, +$('target').value + 1)][1],"),
 ('target-not-laid', "the target is taken as it stands, not laid", "if (n === A.n) { laid = C.lay(A, std); B = laid.shape; }", "if (n === A.n) { B = C.shape(std); laid = { shape: B, clear: C.clearance(A, B), turn: 0, start: 0, mirrored: false }; }"),
 ('crossings-of-the-start', "the crossings counted are the first curve's", "state = { n: n, crossings: cr.length,", "state = { n: n, crossings: C.crossings(A.pts).length,"),
 ('click-on-chart-dead', "a click on the chart does nothing", "if (v >= 0 && v <= 1) { $('u').value = Math.round(v * 1000); draw(); } });", "});"),
 ('least-of-the-other-way', "the least speed in the line below is the plain way's", "least speed <b>' + w.least.toFixed(3) + '</b>'", "least speed <b>' + C.straight(A, B, u()).least.toFixed(3) + '</b>'"),
 ('drawn-curve-turned', "a curve drawn is turned a quarter round before it is used", "custom = C.resample(pts, N);", "custom = C.resample(C.rotate(pts, 1.5708), N);"),
]
for name, what, a, b in M: assert src.count(a) == 1, name
os.makedirs(os.path.join(here, 'mutants', 'page'), exist_ok=True); env = dict(os.environ, LD_LIBRARY_PATH=os.path.expanduser('~/web/sysroot/usr/lib/x86_64-linux-gnu'))
test = os.path.expanduser('~/web/shot-comb.js'); assert open(test, encoding='utf-8').read() == rd(os.path.join('tools', 'shot-comb.js')), 'the test in ~/web is not the copy in tools/'
def run(text):
    path = os.path.join(here, 'mutants', 'page', 'copy.html'); open(path, 'w', encoding='utf-8').write(text.replace('/*CORE*/', core))
    try: return subprocess.run(['node', test, path, os.path.join(here, 'mutants', 'page'), os.path.join(here, 'ccore.js')], cwd=os.path.expanduser('~/web'), env=env, capture_output=True, text=True, timeout=300)
    except subprocess.TimeoutExpired: return None
r = run(src); m = re.search(r'PAGE TEST: (\d+) assertions, (\d+) failed', r.stdout if r else ''); assert m and m.group(2) == '0', 'the true page does not pass by this runner'
print('control: the true page, built and run in the same way: %s assertions, 0 failed\n' % m.group(1), flush=True); caught = 0
for name, what, a, b in M:
    r = run(src.replace(a, b))
    if r is None: res = 'caught: the test does not finish'
    else:
        m = re.search(r'PAGE TEST: (\d+) assertions, (\d+) failed(.*)', r.stdout)
        res = ('caught: %s of %s assertions fail%s' % (m.group(2), m.group(1), m.group(3)[:90])) if m and int(m.group(2)) > 0 else ('NOT caught: all %s assertions pass' % m.group(1)) if m else 'caught: the test stops with an error'
    caught += res.startswith('caught'); print('%-26s %s -- %s' % (name, what, res), flush=True)
print('\n%d of %d broken copies of the page caught' % (caught, len(M)))
