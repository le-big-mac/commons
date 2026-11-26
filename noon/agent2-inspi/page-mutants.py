# page-mutants.py -- can the page test fail?  Copies of the page with one thing broken in its own script or style (not in core.js),
# each built and run through tools/shot-inspi.js in a headless browser, three at a time.   python -I page-mutants.py > page-mutants.out
import subprocess, os, re, sys
here = os.path.dirname(os.path.abspath(__file__)); rd = lambda n: open(os.path.join(here, n), encoding='utf-8').read()
src = rd('page.src.html'); core = rd('core.js')
M = [
 ('one-step-short', "a turtle that comes home is stopped one step early", "if (f.home) total = Math.min(f.steps, MAXDRAW);", "if (f.home) total = Math.min(f.steps - 1, MAXDRAW);"),
 ('part-lap', "a turtle that marches away is stopped in the middle of a lap", "total = q * laps; if (total > MAXDRAW)", "total = q * laps + Math.floor(q / 2); if (total > MAXDRAW)"),
 ('no-cap', "the page draws as many steps as the forecast says, however many", "if (f.home) total = Math.min(f.steps, MAXDRAW);", "if (f.home) total = f.steps;"),
 ('walks-another', "the page walks a turtle whose first turn is one degree more than was typed", "S.total = total; S.w = T.walk(S.A, S.I, total);", "S.total = total; S.w = T.walk(S.A + 1000, S.I, total);"),
 ('too-big', "the figure is drawn to fill the longer side", "var k = Math.min((W - 2 * pad) / bw, (H - 2 * pad) / bh); k = Math.min(k, 90 * DPR);", "var k = Math.max((W - 2 * pad) / bw, (H - 2 * pad) / bh); k = Math.min(k, 90 * DPR);"),
 ('upside-down', "the picture is drawn upside down", "function px(x, y) { return [S.view.ox + S.view.k * x, S.view.oy - S.view.k * y]; }", "function px(x, y) { return [S.view.ox + S.view.k * x, H - (S.view.oy - S.view.k * y)]; }"),
 ('mirrored', "the picture is drawn left for right", "function px(x, y) { return [S.view.ox + S.view.k * x, S.view.oy - S.view.k * y]; }", "function px(x, y) { return [W - (S.view.ox + S.view.k * x), S.view.oy - S.view.k * y]; }"),
 ('all-at-first-step', "the whole figure is drawn at the first step", "if (n > S.drawn) { drawSteps(S.drawn, n); S.drawn = n; drawTurtle(); }", "if (n > S.drawn) { drawSteps(S.drawn, S.total); S.drawn = n; drawTurtle(); }"),
 ('dots-late', "the dots are put one step after the end of each lap", "var d = px(w.xs[m * q], w.ys[m * q]); fc.beginPath();", "var d = px(w.xs[Math.min(S.total, m * q + 1)], w.ys[Math.min(S.total, m * q + 1)]); fc.beginPath();"),
 ('no-dots', "no dots are drawn", "if (nl <= MAXDOTS) { fc.fillStyle = '#a8482a';", "if (nl <= 0) { fc.fillStyle = '#a8482a';"),
 ('no-dots-over-20-laps', "no dots when there are more than 20 laps, though the report speaks of them (the referee's)", "if (nl <= MAXDOTS) { fc.fillStyle = '#a8482a';", "if (nl <= 20) { fc.fillStyle = '#a8482a';"),
 ('dots-said-undrawn', "the report speaks of dots however many laps there are", "return Math.floor(S.total / S.f.q) <= MAXDOTS ? ' The dots,", "return true ? ' The dots,"),
 ('turtle-backwards', "the turtle is drawn pointing backwards (the referee's)", "tc.rotate(Math.atan2(hx, hy));", "tc.rotate(Math.atan2(hx, hy) + Math.PI);"),
 ('circle-out-of-view', "the view is fitted to the corners only, so a dashed circle can be cut off (the fault the referee found)", "    if (g && g.kind === 'circle') b = [Math.min(b[0], g.cx - g.r), Math.max(b[1], g.cx + g.r), Math.min(b[2], g.cy - g.r), Math.max(b[3], g.cy + g.r)];   // the dashed circle is part of the picture\n", ""),
 ('note-formula', "the folded note prints a wrong formula (the referee's)", "180° × <i>p</i> × (<i>q</i> − 1).</p>", "90° × <i>p</i> × (<i>q</i> + 1).</p>"),
 ('note-eighth', "the folded note says 20 degrees is 1/8 of a turn (the referee's)", "(20° is 1/18)", "(20° is 1/8)"),
 ('note-q-for-root', "the folded note says a marching lap ends q steps from its start (the referee's)", "one lap ends exactly √<i>q</i> steps from where it began,", "one lap ends exactly <i>q</i> steps from where it began,"),
 ('polygon-parts', "a plain polygon is promised one matching part too many (the referee's)", "' steps bring it round; the figure will have ' + T.commas(f.laps) + ' matching parts.'", "' steps bring it round; the figure will have ' + T.commas(f.laps + 1) + ' matching parts.'"),
 ('odd-never', "the map's sentence says an odd amount never comes home (the referee's)", "one that adds an odd amount always comes home.'", "one that adds an odd amount never comes home.'"),
 ('odd-unlimited', "the map's sentence is said of every turtle, not of the whole-degree ones (the fault the referee found)", "among these whole-degree turtles, one that adds an odd amount always comes home.'", "add an odd number of degrees and the turtle always comes home.'"),
 ('decimal-product', "the report multiplies by a rounded figure that does not give its own total (the fault the referee found)", "' × √' + T.commas(q) + '.'", "' × ' + f.gain.toFixed(3) + '.'"),
 ('key-says-two', "the key says home after 2 steps, which no turtle on the map is", "$('keylow').textContent = 'home after ' + T.commas(CENSUS.least) + ' steps';", "$('keylow').textContent = 'home after 2 steps';"),
 ('shade-from-two', "the palest shade is kept for 2 steps, which no turtle on the map takes", "var t = Math.log(steps / CENSUS.least) / Math.log(CENSUS.longest / CENSUS.least);", "var t = Math.log(steps / 2) / Math.log(360);"),
 ('message-vague', "the message for a refused number does not say what is taken", "'Type each turn as a plain number of degrees, such as 20, 2.5 or -7, with at most six figures before the point and three after.'", "'Type each turn as a number of degrees, with at most three decimals.'"),
 ('lap-on-start-unsaid', "the folded note says the lap ends always go round a circle", " (or all fall on the start, when a lap happens to end there)", ""),
 ('circle-big', "the dashed circle is drawn a fifth too big", "fc.arc(c[0], c[1], g.r * S.view.k, 0, 2 * Math.PI); }", "fc.arc(c[0], c[1], 1.2 * g.r * S.view.k, 0, 2 * Math.PI); }"),
 ('circle-about-start', "the dashed circle is drawn about the start", "var c = px(g.cx, g.cy); fc.arc(", "var c = px(0, 0); fc.arc("),
 ('circle-from-two', "the circle's middle is taken from the first two lap ends only", "for (var n = 0; n < f.laps; n++) { cx += S.w.xs[n * q]; cy += S.w.ys[n * q]; } cx /= f.laps; cy /= f.laps;", "for (var n = 0; n < 2; n++) { cx += S.w.xs[n * q]; cy += S.w.ys[n * q]; } cx /= 2; cy /= 2;"),
 ('line-short', "the dashed line stops at the end of the first lap", "S.guide = { kind: 'line', x: S.w.xs[Math.floor(total / q) * q], y: S.w.ys[Math.floor(total / q) * q] };", "S.guide = { kind: 'line', x: S.w.xs[q], y: S.w.ys[q] };"),
 ('turtle-stays', "the turtle is left at the start", "var w = S.w, k = S.drawn, p = px(w.xs[k], w.ys[k]), hx, hy;", "var w = S.w, k = S.drawn, p = px(0, 0), hx, hy;"),
 ('turtle-behind', "the turtle is drawn one corner behind", "var w = S.w, k = S.drawn, p = px(w.xs[k], w.ys[k]), hx, hy;", "var w = S.w, k = S.drawn, p = px(w.xs[Math.max(0, k - 1)], w.ys[Math.max(0, k - 1)]), hx, hy;"),
 ('says-lap-for-steps', "the forecast gives the length of a lap as the number of steps", "s += 'it comes home after <b>' + T.commas(f.steps) + ' steps</b>. ';", "s += 'it comes home after <b>' + T.commas(f.q) + ' steps</b>. ';"),
 ('says-first-turn', "the forecast gives the first turn as the turning in a lap", "' leaves it turned by ' + deg(f.T) + ', so '", "' leaves it turned by ' + deg(S.A) + ', so '"),
 ('says-steps-for-laps', "the forecast gives the steps as the number of laps", "', so ' + T.commas(f.laps) + ' laps bring it round; the figure will have '", "', so ' + T.commas(f.steps) + ' laps bring it round; the figure will have '"),
 ('says-laps-for-parts', "the forecast gives the length of a lap as the number of matching parts", "' laps bring it round; the figure will have ' + T.commas(f.laps) + ' matching parts.';", "' laps bring it round; the figure will have ' + T.commas(f.q) + ' matching parts.';"),
 ('says-home-always', "the forecast says home for a turtle that never comes home", "    if (f.home) {\n      s += 'it comes home after <b>'", "    if (true) {\n      s += 'it comes home after <b>'"),
 ('root-unrooted', "the forecast prints q for its square root", "' = ' + f.gain.toFixed(3) + ' steps further along a straight line.'", "' = ' + f.q.toFixed(3) + ' steps further along a straight line.'"),
 ('polygon-turn', "for a plain polygon the forecast prints the amount added, not the turn", "s += q === 1 ? lap + ', ' + deg(f.T) + ', so '", "s += q === 1 ? lap + ', ' + deg(S.I) + ', so '"),
 ('stop-unsaid', "the forecast does not say the page will stop early", "if (f.steps > MAXDRAW) s += ' That is more than this page draws: it will stop at step ' + T.commas(MAXDRAW) + '.';", ""),
 ('long-lap-unsaid', "the forecast does not say a lap is too long to draw", "if (q > MAXDRAW) s += ' A lap is more than this page draws: it will stop at step ' + T.commas(MAXDRAW) + '.';", ""),
 ('times-the-steps', "the report multiplies by the steps, not the laps", "' steps from its start, which is ' + T.commas(laps) + ' × √'", "' steps from its start, which is ' + T.commas(k) + ' × √'"),
 ('hides-earlier-visit', "the report does not say the turtle stood on its start before", "if (w.there && w.there < w.home) s +=", "if (false) s +="),
 ('typed-turn-lost', "the report gives the first turn brought into one whole turn, not as typed", "its next turn would be ' + deg(S.A) + ' again.'", "its next turn would be ' + deg(T.mod(S.A, T.FULL)) + ' again.'"),
 ('first-lap-unsaid', "the report hides that it stopped inside the first lap", "s = '<b>Stopped at step ' + T.commas(k) + '</b>, before the end of its first lap of ' + T.commas(q) + ' steps.'; }", "s = '<b>Stopped at step ' + T.commas(k) + '</b>.'; }"),
 ('stopped-says-home', "a turtle stopped early is reported as home", "s = '<b>Stopped at step ' + T.commas(k) + '</b> of the ' + T.commas(f.steps) + ' it needs' +", "s = '<b>Step ' + T.commas(k) + ': home.</b> of the ' + T.commas(f.steps) + ' it needs' +"),
 ('count-frozen', "the report does not count while the turtle walks", "    report(); requestAnimationFrame(step);\n  }", "    requestAnimationFrame(step);\n  }"),
 ('keeps-walking', "changing a number does not stop the turtle", "S.running = false; S.done = false; S.drawn = 0; S.valid = A !== null && I !== null;", "S.done = false; S.valid = A !== null && I !== null;"),
 ('slow-is-fast', "slow is 50 steps a second", "S.rate = pace === 'slow' ? 5 :", "S.rate = pace === 'slow' ? 50 :"),
 ('quick-is-slow', "quick takes eighteen seconds", "Math.max(30, S.total / 6)", "Math.max(5, S.total / 18)"),
 ('enter-dead', "Enter in the second box does nothing", "  $('inc').addEventListener('keydown', function (e) { if (e.key === 'Enter') go(); });", ""),
 ('button-swapped', "one button has its two numbers the wrong way round", "{ a: '112', i: '135', name: 'the widest' },", "{ a: '135', i: '112', name: 'the widest' },"),
 ('button-idle', "a button fills the boxes but does not send the turtle off", "b.addEventListener('click', function () { setPair(p.a, p.i); go(); });", "b.addEventListener('click', function () { setPair(p.a, p.i); });"),
 ('boxes-not-filled', "a button or a dot sends the turtle off but leaves the boxes as they were", "if (!fromBox) { $('angle').value = aStr; $('inc').value = iStr; }", ""),
 ('go-when-bad', "Go stays alive when a box holds no number", "$('go').disabled = !S.valid;", "$('go').disabled = false;"),
 ('bad-keeps-picture', "a box with no number leaves the old picture standing", "else { fc.setTransform(1, 0, 0, 1, 0, 0); fc.clearRect(0, 0, W, H); tc.clearRect(0, 0, W, H); }", ""),
 ('bad-unmarked', "the box with no number is not marked", "$('angle').classList.toggle('bad', A === null); ", ""),
 ('map-never-pale', "the map paints the turtles that never come home as if they came home at once", "if (!steps) return [43, 38, 34];", "if (!steps) return [246, 240, 226];"),
 ('map-darker-sooner', "among those that come home, fewer steps is the darker dot", "var t = Math.log(steps / CENSUS.least) / Math.log(CENSUS.longest / CENSUS.least); t = Math.max(0, Math.min(1, t));", "var t = 1 - Math.log(steps / CENSUS.least) / Math.log(CENSUS.longest / CENSUS.least); t = Math.max(0, Math.min(1, t));"),
 ('map-upside-down', "the map is drawn with the first turn running downward", "j = 4 * ((359 - a) * 359 + (inc - 1));", "j = 4 * (a * 359 + (inc - 1));"),
 ('map-shifted', "the map is drawn one amount to the right", "j = 4 * ((359 - a) * 359 + (inc - 1));", "j = 4 * ((359 - a) * 359 + (inc % 359));"),
 ('pointer-upside-down', "pointing at the map reads the first turn from the top", "a = 359 - Math.floor((ev.clientY - r.top) / r.height * 360);", "a = Math.floor((ev.clientY - r.top) / r.height * 360);"),
 ('pointer-one-left', "pointing at the map names the dot to the left", "inc = 1 + Math.floor((ev.clientX - r.left) / r.width * 359),", "inc = Math.floor((ev.clientX - r.left) / r.width * 359),"),
 ('click-idle', "clicking the map names the turtle but does not send it off", "setPair(String(c.angle), String(c.inc)); go(); });", "setPair(String(c.angle), String(c.inc)); });"),
 ('no-scroll-on-go', "on a small phone Go leaves the picture below the screen (found by the second turtle's referee)", "    bringUp();\n", "\n"),
 ('scroll-canvas-only', "Go brings the canvas up but leaves the foot of its frame off the screen", "var frame = field.parentNode, H = window.innerHeight", "var frame = field, H = window.innerHeight"),
 ('scroll-browser', "Go leaves the bringing up to the browser's own scrollIntoView, which stops short of the frame's lower edge", "    if (r.top >= 0 && r.bottom <= H) return;\n", "    if (r.top >= 0 && r.bottom <= H) return;\n    frame.scrollIntoView({ block: 'nearest' }); return;\n"),
 ('scroll-top-only', "a picture above the screen is not brought down", "fits && r.top >= 0 ? Math.ceil(r.bottom - H) : Math.floor(r.top)", "fits && r.top >= 0 ? Math.ceil(r.bottom - H) : 0"),
 ('ring-mirrored', "the ring on the map is drawn at the mirror place", "var x = (S.pick.inc - 1 + 0.5) * map.width / 359,", "var x = (359 - S.pick.inc + 0.5) * map.width / 359,"),
 ('ring-for-decimals', "a pair with decimals gets a ring on the whole-degree map", "if (a % U === 0 && i % U === 0 && i > 0) {", "if (i > 0) {"),
 ('count-swapped', "the map's sentence counts the ones that come home as the ones that never do", "'Dark dots never come home: ' + T.commas(CENSUS.away) + ' of the '", "'Dark dots never come home: ' + T.commas(CENSUS.home) + ' of the '"),
 ('longest-wrong', "the map's sentence gives the number of turtles that come home as the most steps", "' Every other one comes home within ' + T.commas(CENSUS.longest) + ' steps", "' Every other one comes home within ' + T.commas(CENSUS.home) + ' steps"),
 ('ramp-backwards', "the key's strip runs the wrong way", "var cc = shade(CENSUS.least * Math.pow(CENSUS.longest / CENSUS.least, x / 119));", "var cc = shade(CENSUS.least * Math.pow(CENSUS.longest / CENSUS.least, 1 - x / 119));"),
 ('no-refit', "the figure is not drawn again when the window changes", "if (S.w) { setView(); redraw(); }", ""),
 ('sheets-apart', "the turtle's sheet is a little larger than the line's (the fault the test first found)", ".stage { position: relative; border: 1px solid var(--line); border-radius: 6px; background: #fffdf7; overflow: hidden; }", ".stage { position: relative; width: 100%; } #field { border: 1px solid var(--line); border-radius: 6px; background: #fffdf7; }"),
 ('map-too-wide', "the map does not shrink to a narrow screen", "#map { display: block; width: 100%; max-width: 718px;", "#map { display: block; width: 718px; max-width: 718px;"),
]
for name, what, a, b in M: assert src.count(a) == 1, (name, src.count(a))
work = os.path.join(here, 'mutants', 'page'); os.makedirs(work, exist_ok=True)
env = dict(os.environ, LD_LIBRARY_PATH=os.path.expanduser('~/web/sysroot/usr/lib/x86_64-linux-gnu'), NODE_PATH=os.path.expanduser('~/web/node_modules'))
test = os.path.expanduser('~/web/shot-inspi.js'); assert open(test, encoding='utf-8').read() == rd(os.path.join('tools', 'shot-inspi.js')), 'the test in ~/web is not the copy in tools/'
def run(path, out=None): return subprocess.run(['node', test, path, out or work, os.path.join(here, 'core.js'), os.path.join(here, 'table.json')], cwd=os.path.expanduser('~/web'), env=env, capture_output=True, text=True, timeout=400)
def one(job):
    name, what, a, b = job; out = os.path.join(work, name); os.makedirs(out, exist_ok=True); path = os.path.join(out, name + '.html')
    open(path, 'w', encoding='utf-8').write((src if a is None else src.replace(a, b)).replace('/*CORE*/', core))
    try:
        r = run(path, out); m = re.search(r'PAGE TEST: (\d+) assertions, (\d+) failed(.*)', r.stdout)
        res = ('caught: %s of %s assertions fail%s' % (m.group(2), m.group(1), m.group(3)[:110])) if m and int(m.group(2)) > 0 else ('NOT caught: all %s assertions pass' % m.group(1)) if m else 'caught: the test gives no tally (%s)' % ((r.stdout.strip().splitlines() or r.stderr.strip().splitlines() or ['no output'])[-1][:110])
    except subprocess.TimeoutExpired: res = 'caught: the test does not finish'
    shutil.rmtree(out, ignore_errors=True)
    return name, what, res
if __name__ == '__main__':
    import shutil, concurrent.futures
    workers = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    path = os.path.join(work, 'true.html'); open(path, 'w', encoding='utf-8').write(src.replace('/*CORE*/', core)); r = run(path)
    m = re.search(r'PAGE TEST: (\d+) assertions, (\d+) failed', r.stdout); assert m and m.group(2) == '0', 'the true page does not pass by this runner: ' + (r.stdout[-300:] + r.stderr[-300:])
    print('control: the true page, built and run in the same way, alone: %s assertions, 0 failed' % m.group(1), flush=True); os.remove(path)
    for f in os.listdir(work):
        if f.endswith('.png'): os.remove(os.path.join(work, f))
    # the broken copies are run %d at a time; the true page is run twice more among them, to show that running side by side fails nothing
    jobs = list(M); jobs.insert(len(M) // 4, ('true-among-them-1', 'the true page, run among the broken copies', None, None)); jobs.insert(3 * len(M) // 4, ('true-among-them-2', 'the true page, run among the broken copies', None, None))
    caught = 0; controls = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as ex:
        for name, what, res in ex.map(one, jobs):
            if name.startswith('true-among-them'): controls.append(res); continue
            caught += res.startswith('caught'); print('%-22s %s -- %s' % (name, what, res), flush=True)
    print('\ncontrol: the true page run twice among them (%d at a time): %s' % (workers, '; '.join('passes' if c.startswith('NOT caught') else 'FAILS: ' + c for c in controls)))
    print('%d of %d broken copies of the page caught' % (caught, len(M)))
