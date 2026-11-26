# page-mutants.py -- can the page test fail?  Copies of the page with one thing broken in its own script, style or text (not in core.js),
# each built and run through tools/shot-gospel.js in a headless browser, three at a time.   python -I page-mutants.py > page-mutants.out
import subprocess, os, re, sys
here = os.path.dirname(os.path.abspath(__file__)); rd = lambda n: open(os.path.join(here, n), encoding='utf-8').read()
src = rd('page.src.html'); core = rd('core.js')
M = [
 ('one-step-short', "a turtle that comes home is stopped one step early", "else if (f.bounded) { rounds = 1; total = s + n; }", "else if (f.bounded) { rounds = 1; total = s + n - 1; }"),
 ('one-round-only', "a turtle that marches away is drawn for one round at the least, not four", "rounds = Math.max(4, Math.min(40, Math.round(240 / n)));", "rounds = Math.max(1, Math.min(40, Math.round(240 / n)));"),
 ('no-cap', "the page draws as many steps as the round has, however many", "    if (total > MAXDRAW) { rounds = Math.floor((MAXDRAW - s) / n); total = rounds >= 1 ? s + n * rounds : MAXDRAW; }\n", ""),
 ('walks-another', "the page walks a turtle whose upper number is one more than was typed", "S.w = T.walk(S.P, S.Q, total);", "S.w = T.walk(S.P + 1, S.Q, total);"),
 ('too-big', "the figure is drawn to fill the longer side", "var k = Math.min((W - 2 * pad) / bw, (H - 2 * pad) / bh); k = Math.min(k, 90 * DPR);", "var k = Math.max((W - 2 * pad) / bw, (H - 2 * pad) / bh); k = Math.min(k, 90 * DPR);"),
 ('upside-down', "the picture is drawn upside down", "function px(x, y) { return [S.view.ox + S.view.k * x, S.view.oy - S.view.k * y]; }", "function px(x, y) { return [S.view.ox + S.view.k * x, H - (S.view.oy - S.view.k * y)]; }"),
 ('mirrored', "the picture is drawn left for right", "function px(x, y) { return [S.view.ox + S.view.k * x, S.view.oy - S.view.k * y]; }", "function px(x, y) { return [W - (S.view.ox + S.view.k * x), S.view.oy - S.view.k * y]; }"),
 ('all-at-first-step', "the whole figure is drawn at the first step", "if (n > S.drawn) { drawSteps(S.drawn, n); S.drawn = n; drawTurtle(); }", "if (n > S.drawn) { drawSteps(S.drawn, S.total); S.drawn = n; drawTurtle(); }"),
 ('dots-late', "the dots are put one step after the end of each round", "var d = px(w.xs[at], w.ys[at]); fc.beginPath();", "var d = px(w.xs[Math.min(S.total, at + 1)], w.ys[Math.min(S.total, at + 1)]); fc.beginPath();"),
 ('no-dots', "no dots are drawn", "if (at > from && at <= to && at > 0) {", "if (false) {"),
 ('dots-every-other', "only every other round gets its dot", "for (var j = 0; j <= S.rounds; j++) { var at = s + j * n;", "for (var j = 0; j <= S.rounds; j += 2) { var at = s + j * n;"),
 ('guide-short', "the dashed line is laid to the end of the first round only", "x1: S.w.xs[s + n * S.rounds], y1: S.w.ys[s + n * S.rounds] };", "x1: S.w.xs[s + n], y1: S.w.ys[s + n] };"),
 ('guide-undrawn', "the dashed line is spoken of and not drawn", "    var g = S.guide; if (!g) return;\n    fc.strokeStyle = 'rgba(168,72,42,0.55)';", "    var g = null; if (!g) return;\n    fc.strokeStyle = 'rgba(168,72,42,0.55)';"),
 ('turtle-stays', "the turtle is left at the start", "var w = S.w, k = S.drawn, p = px(w.xs[k], w.ys[k]), hx, hy;", "var w = S.w, k = S.drawn, p = px(0, 0), hx, hy;"),
 ('turtle-behind', "the turtle is drawn one corner behind", "var w = S.w, k = S.drawn, p = px(w.xs[k], w.ys[k]), hx, hy;", "var w = S.w, k = S.drawn, p = px(w.xs[Math.max(0, k - 1)], w.ys[Math.max(0, k - 1)]), hx, hy;"),
 ('turtle-backwards', "the turtle is drawn pointing backwards", "tc.rotate(Math.atan2(hx, hy));", "tc.rotate(Math.atan2(hx, hy) + Math.PI);"),
 ('turtle-always-up', "the turtle always points up the page", "if (k > 0) { hx = w.xs[k] - w.xs[k - 1]; hy = w.ys[k] - w.ys[k - 1]; } else { hx = 0; hy = 1; }", "hx = 0; hy = 1;"),
 ('says-one-step-more', "the forecast gives one step too many", "s += 'it comes home after <b>' + T.commas(n) + ' steps</b>.", "s += 'it comes home after <b>' + T.commas(n + 1) + ' steps</b>."),
 ('says-home-always', "the forecast says home for every turtle that does not walk straight", "else if (f.home) s += 'it comes home after", "else if (true) s += 'it comes home after"),
 ('why-wrong-prime', "the reason names the wrong prime power as the one that serves", "return odd + ' holds ' + power(sv.l, sv.e) + ', and nothing spoils it: '", "return odd + ' holds ' + power(sv.l + 2, sv.e) + ', and nothing spoils it: '"),
 ('why-wrong-power', "the reason says l where it should say the power of l that the order holds: false for 1/189 (the referee's)", "var sv = f.serves, lk = power(sv.l, sv.k),", "var sv = f.serves, lk = power(sv.l, 1),"),
 ('why-lone-prime-wrong', "for a power of one prime the reason names the wrong prime", "' holds its prime ' + sv.l + ' at least squared", "' holds its prime ' + (sv.l + 2) + ' at least squared"),
 ('why-wrong-order', "the reason gives a wrong order of 2", "x[0] + ' (which is ' + T.commas(T.order2(x[0])) + ')'", "x[0] + ' (which is ' + T.commas(T.order2(x[0]) + 1) + ')'"),
 ('why-spoiler-wrong', "the reason names the wrong prime as the spoiler", "' divides the order of 2 modulo ' + b.r + ' (which is '", "' divides the order of 2 modulo ' + b.l + ' (which is '"),
 ('why-no-square-always', "every turtle that marches away is said to hold no square", "    if (!f.squares) return odd +", "    if (true) return odd +"),
 ('tail-unsaid', "the forecast does not mention the tail", "tail = f.tail ? 'After a tail of ' + T.commas(f.tail) + (f.tail === 1 ? ' step' : ' steps') + ' its' : 'Its';", "tail = 'Its';"),
 ('odd-part-unsaid', "the reason is given for the whole denominator when it is even", "var odd = f.tail ? 'The odd part of the denominator, ' + name + ',' :", "var odd = false ? 'The odd part of the denominator, ' + name + ',' :"),
 ('degrees-halved', "the first turn is shown as half its degrees", "var d = 360 * f.p / f.q,", "var d = 180 * f.p / f.q,"),
 ('lowest-terms-unsaid', "the page does not say what the fraction is in lowest terms", "+ '° (' + frac() + ' in lowest terms' + (within ? '' : ', whole turns left out') + ')';", "+ '°';"),
 ('whole-turns-unsaid', "the page does not say that whole turns were left out of 10/9 (the referee's)", "(within ? '' : ', whole turns left out')", "''"),
 ('report-as-typed', "the report gives the fraction as typed, not in lowest terms", "its next turn would be ' + frac() + ' of a turn again.'", "its next turn would be ' + S.P + '/' + S.Q + ' of a turn again.'"),
 ('loop-says-home', "a turtle circling its loop is reported as home", "s = '<b>Step ' + T.commas(k) + ': back where it stood at step ' + T.commas(t) + '</b>, at the end of its tail.", "s = '<b>Step ' + T.commas(k) + ': home.</b> It stood at step ' + T.commas(t) + ', at the end of its tail."),
 ('gain-doubled', "the report gives twice the distance a round carries it", "' has carried it ' + S.gain.toFixed(3) + ' steps further'", "' has carried it ' + (2 * S.gain).toFixed(3) + ' steps further'"),
 ('rounds-one-more', "the report counts one round too many", "mark the end of each of the ' + T.commas(S.rounds) + ' rounds drawn.'", "mark the end of each of the ' + T.commas(S.rounds + 1) + ' rounds drawn.'"),
 ('straight-unsaid', "a turtle walking straight on is reported as going round", "It is walking straight on.';", "It is going round.';"),
 ('stop-unsaid', "the forecast does not say the page will stop early", "s += ' That is more than this page draws: it will stop at step ' + T.commas(S.total) + '.';", "s += '';"),
 ('cut-said-uncut', "the forecast says the walk is cut when exactly 20,000 steps make whole rounds (the fault the referee found)", "if (!f.straight && !(S.rounds >= 1 && S.total === f.tail + n * S.rounds)) s +=", "if (S.total === MAXDRAW || (f.bounded && f.tail + n > MAXDRAW)) s +="),
 ('count-frozen', "the report does not count while the turtle walks", "    report(); requestAnimationFrame(step);\n  }", "    requestAnimationFrame(step);\n  }"),
 ('keeps-walking', "changing a number does not stop the turtle", "S.running = false; S.done = false; S.drawn = 0; S.valid = P !== null && okQ;", "S.done = false; S.valid = P !== null && okQ;"),
 ('slow-is-fast', "slow is 50 steps a second", "S.rate = pace === 'slow' ? 5 :", "S.rate = pace === 'slow' ? 50 :"),
 ('quick-is-slow', "quick takes eighteen seconds", "Math.max(30, S.total / 6)", "Math.max(5, S.total / 18)"),
 ('enter-dead', "Enter in the lower box does nothing", "  $('den').addEventListener('keydown', function (e) { if (e.key === 'Enter') go(); });", ""),
 ('button-swapped', "one button has its two numbers the wrong way round", "{ p: '1', q: '45', name: '1/45: home, against the claim' },", "{ p: '45', q: '1', name: '1/45: home, against the claim' },"),
 ('button-idle', "a button fills the boxes but does not send the turtle off", "b.addEventListener('click', function () { setPair(p.p, p.q); go(); });", "b.addEventListener('click', function () { setPair(p.p, p.q); });"),
 ('boxes-not-filled', "a button or a square sends the turtle off but leaves the boxes as they were", "if (!fromBox) { $('num').value = pStr; $('den').value = qStr; }", ""),
 ('go-when-bad', "Go stays alive when a box holds no number", "$('go').disabled = !S.valid;", "$('go').disabled = false;"),
 ('bad-keeps-picture', "a box with no number leaves the old picture standing", "else { fc.setTransform(1, 0, 0, 1, 0, 0); fc.clearRect(0, 0, W, H); tc.clearRect(0, 0, W, H); }", ""),
 ('bad-unmarked', "the box with no number is not marked", "$('num').classList.toggle('bad', P === null); ", ""),
 ('too-large-taken', "a lower number above the limit is taken", "var okQ = Q !== null && Q >= 1 && Q <= T.QMAX;", "var okQ = Q !== null && Q >= 1 && Q <= 10 * T.QMAX;"),
 ('grid-colours-swapped', "the grid paints those that come home dark and the spoilt squares rust", "var SHADE = ['#e9e1cf', '#2b2622', '#a8482a'];", "var SHADE = ['#e9e1cf', '#a8482a', '#2b2622'];"),
 ('grid-shifted', "the grid is drawn one square to the right of where pointing reads it", "return [(i % COLS) * cw, Math.floor(i / COLS) * chh, cw, chh]; }", "return [((i + 1) % COLS) * cw, Math.floor(i / COLS) * chh, cw, chh]; }"),
 ('pointer-one-on', "pointing at the grid names the next denominator", "var i = Math.min(CENSUS.kind.length - 1, row * COLS + col); return 2 * i + 3;", "var i = Math.min(CENSUS.kind.length - 1, row * COLS + col); return 2 * i + 5;"),
 ('cell-says-swapped', "pointing at a square says home for those that march away, and the other way", "(f.bounded ? 'comes home after ' + T.commas(f.round) + ' steps. ' : 'marches away. ')", "(!f.bounded ? 'comes home after ' + T.commas(f.round) + ' steps. ' : 'marches away. ')"),
 ('click-idle', "clicking the grid names the turtle but does not send it off", "setPair('1', String(m)); go(); });", "setPair('1', String(m)); });"),
 ('frame-on-next', "the blue frame is drawn on the next square", "var c = cellBox((f.q - 3) / 2);", "var c = cellBox((f.q - 1) / 2);"),
 ('frame-any-upper', "a turn of 8/9 is framed on the grid as if it were 1/9", "if (f.p === 1 && f.q % 2 === 1 && f.q >= 3 && f.q <= TOP) {", "if (f.q % 2 === 1 && f.q >= 3 && f.q <= TOP) {"),
 ('count-swapped', "the grid's sentence counts the spoilt squares as those that come home", "T.commas(CENSUS.closes) + ' come home; ' + T.commas(CENSUS.spoilt) + ' hold the square", "T.commas(CENSUS.spoilt) + ' come home; ' + T.commas(CENSUS.closes) + ' hold the square"),
 ('note-count-wrong', "the note's count of squares that do not save is out of the wrong total", "$('spoiltcount').textContent = T.commas(CENSUS.spoilt) + ' of the ' + T.commas(CENSUS.spoilt + CENSUS.closes) +", "$('spoiltcount').textContent = T.commas(CENSUS.spoilt) + ' of the ' + T.commas(CENSUS.spoilt + CENSUS.plain) +"),
 ('no-refit', "the figure is not drawn again when the window changes", "if (S.w && S.valid) { setView(); redraw(); }", ""),
 ('junk-redrawn', "after a refused number, a change of width brings the ring and the turtle back (the fault the referee found)", "if (S.w && S.valid) { setView(); redraw(); }", "if (S.w) { setView(); redraw(); }"),
 ('guide-lost-on-resize', "the dashed line is not drawn again when the window changes (the referee's)", "function redraw() { drawBase(); drawSteps(0, S.drawn); if (S.done) drawGuide(); drawTurtle(); }", "function redraw() { drawBase(); drawSteps(0, S.drawn); drawTurtle(); }"),
 ('no-scroll-on-go', "on a small phone Go leaves the picture below the screen (the fault the referee found)", "    bringUp();\n", "\n"),
 ('scroll-canvas-only', "Go brings the canvas up but leaves the foot of its frame off the screen", "var frame = field.parentNode, H = window.innerHeight", "var frame = field, H = window.innerHeight"),
 ('scroll-browser', "Go leaves the bringing up to the browser's own scrollIntoView, which stops short of the frame's lower edge", "    if (r.top >= 0 && r.bottom <= H) return;\n", "    if (r.top >= 0 && r.bottom <= H) return;\n    frame.scrollIntoView({ block: 'nearest' }); return;\n"),
 ('scroll-top-only', "a picture above the screen is not brought down", "fits && r.top >= 0 ? Math.ceil(r.bottom - H) : Math.floor(r.top)", "fits && r.top >= 0 ? Math.ceil(r.bottom - H) : 0"),
 ('key-swapped', "the key under the grid calls the dark squares 'comes home' (the referee's)", '<span class="sw" style="background:#a8482a"></span>comes home', '<span class="sw" style="background:#2b2622"></span>comes home'),
 ('rule-misstated', "the folded rule says 'as many times as' for 'more times than' (after the referee's)", "more times than the order of 2 modulo any other prime of <i>q</i> is.", "as many times as the order of 2 modulo any other prime of <i>q</i> is."),
 ('rule-lone-prime', "the folded rule drops 'divisible by l': read to the letter it would have a lone prime such as 7 close (my own wording until the mending)", "<i>l</i>, and by <i>l</i> more times than", "<i>l</i> more times than"),
 ('tail-one-more', "the forecast gives a tail one step too long (the referee's)", "tail = f.tail ? 'After a tail of ' + T.commas(f.tail) +", "tail = f.tail ? 'After a tail of ' + T.commas(f.tail + 1) +"),
 ('tail-always-plural', "a tail of one step is called '1 steps'", "(f.tail === 1 ? ' step' : ' steps') + ' its' : 'Its';", "' steps' + ' its' : 'Its';"),
 ('fifty-to-a-row', "the grid has fifty squares to a row where the page says forty (the referee's)", "var TOP = 2001, COLS = 40;", "var TOP = 2001, COLS = 50;"),
 ('grid-backwards', "the grid is drawn right to left (the referee's)", "return [(i % COLS) * cw, Math.floor(i / COLS) * chh, cw, chh]; }", "return [(COLS - 1 - i % COLS) * cw, Math.floor(i / COLS) * chh, cw, chh]; }"),
 ('memo-45-wrong', "the note says the memo's rule gets 45 wrong", "(the memo's own rule gets 45 right)", "(the memo's own rule gets 45 wrong)"),
 ('fuchs-date', "the note misdates Fuchs", "dated Berlin, 1862, and printed in 1863", "dated Berlin, 1872, and printed in 1873"),
 ('sheets-apart', "the turtle's sheet is a little larger than the line's", ".stage { position: relative; border: 1px solid var(--line); border-radius: 6px; background: #fffdf7; overflow: hidden; }", ".stage { position: relative; width: 100%; } #field { border: 1px solid var(--line); border-radius: 6px; background: #fffdf7; }"),
 ('grid-too-wide', "the grid does not shrink to a narrow screen", "#map { display: block; width: 100%; max-width: 720px;", "#map { display: block; width: 720px; max-width: 720px;"),
 ('label-no-wrap', "the row of boxes cannot wrap on a very narrow screen (the fault the test first found)", "display: inline-flex; flex-wrap: wrap; gap: 6px; align-items: center; }", "display: inline-flex; gap: 6px; align-items: center; }"),
 ('note-2457', "the note's second count is one too many", "636,963 have such a prime and 2,456\n", "636,963 have such a prime and 2,457\n"),
 ('note-share', "the note's weighted share is wrong in its second decimal", "0.109 for odd", "0.119 for odd"),
 ('note-example', "the folded rule gives a wrong order of 2 modulo 5", "because 2 has order 4 modulo 5 and 3 does not divide 4", "because 2 has order 3 modulo 5 and 3 does not divide 4"),
 ('note-quote', "HAKMEM is misquoted", "which must occur at least cubed”", "which must occur at least squared”"),
 ('note-salvaged', "the note says again that the memo doubts its .155 (a misreading of mine and the referee's, found in the check of the mending)", "with the memo's own exceptions not taken off. By the rule", "and adds that this “might, however, be salvaged by quantities like 171”. By the rule"),
 ('note-ends', "the note says the book's exercise ends with its question (it has one more sentence)", "and asks: “Can you prove", "and ends: “Can you prove"),
 ('note-q1', "the note's true half of the claim takes in a denominator of 1", "an odd denominator greater than 1 divides", "an odd denominator divides"),
 ('note-proof', "the first note says 'A proof is in the write-up', not saying whose", "The write-up has an argument for it that I made before I knew of his.", "A proof is in the write-up."),
]
for name, what, a, b in M: assert src.count(a) == 1, (name, src.count(a))
work = os.path.join(here, 'mutants', 'page'); os.makedirs(work, exist_ok=True)
env = dict(os.environ, LD_LIBRARY_PATH=os.path.expanduser('~/web/sysroot/usr/lib/x86_64-linux-gnu'), NODE_PATH=os.path.expanduser('~/web/node_modules'))
test = os.path.expanduser('~/web/shot-gospel.js'); assert open(test, encoding='utf-8').read() == rd(os.path.join('tools', 'shot-gospel.js')), 'the test in ~/web is not the copy in tools/'
def run(path, out=None): return subprocess.run(['node', test, path, out or work, os.path.join(here, 'core.js'), os.path.join(here, 'table.json'), os.path.join(here, 'gospel.sealed-run.out'), os.path.join(here, 'more.sealed-run.out')], cwd=os.path.expanduser('~/web'), env=env, capture_output=True, text=True, timeout=400)
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
