# page-mutants.py -- can the page test fail?  Copies of the page with one thing broken in its own script (not in core.js), each built
# and run through tools/shot-thunder.js in a headless browser.   python -I page-mutants.py > page-mutants.out
import subprocess, os, re
here = os.path.dirname(os.path.abspath(__file__)); rd = lambda n: open(os.path.join(here, n), encoding='utf-8').read()
src = rd('page.src.html'); core = rd('core.js')
M = [
 ('ring-slow', "the ring is drawn growing at four fifths of the speed of sound", "var R = Math.max(0, C * st.t);", "var R = Math.max(0, 0.8 * C * st.t);"),
 ('ring-squashed', "the ring is drawn as an oval", "R / (Z1 - Z0) * H, 0, Math.PI, 2 * Math.PI); sc.stroke();", "0.7 * R / (Z1 - Z0) * H, 0, Math.PI, 2 * Math.PI); sc.stroke();"),
 ('sound-early', "the sound starts at once, whatever the distance", "src.start(now + Math.max(0, r.t0 - st.offset), Math.max(0, st.offset - r.t0));", "src.start(now, 0);"),
 ('sound-late', "the sound comes half a second after the ring", "src.start(now + Math.max(0, r.t0 - st.offset), Math.max(0, st.offset - r.t0));", "src.start(now + 0.5 + Math.max(0, r.t0 - st.offset), Math.max(0, st.offset - r.t0));"),
 ('dry-to-speaker', "the loudspeaker gets the sound without the air", "for (var i = 0; i < n; i++) out[i] = r.p[i] * k;", "for (var i = 0; i < n; i++) out[i] = r.dry[i] * k;"),
 ('loudness-rule', "loudness is squeezed two to one, not four", "function level(peak) { return 0.9 * Math.min(1, Math.sqrt(Math.sqrt(peak / REF))); }", "function level(peak) { return 0.9 * Math.min(1, Math.sqrt(peak / REF)); }"),
 ('skip-three', "skipping the silence starts three seconds before the sound", "st.offset = skip ? Math.max(0, (r.firstHeard === null ? r.first : r.firstHeard) - 0.6) : 0;", "st.offset = skip ? Math.max(0, (r.firstHeard === null ? r.first : r.firstHeard) - 3) : 0;"),
 ('skip-ignored', "the silence is skipped whether asked or not", "var r = st.res, skip = document.getElementById('skip').checked;", "var r = st.res, skip = true;"),
 ('drag-no-sound', "dragging the listener leaves the old sound", "if (st.kind === 'bow' || st.kind === 'away') rebuild(); else compute(); }", "if (st.kind === 'bow' || st.kind === 'away') rebuild(); }"),
 ('bow-stays', "the bow stays where it was when the listener moves", "if (st.kind === 'bow' || st.kind === 'away') rebuild(); else compute(); }", "compute(); }"),
 ('drag-half', "the listener goes half as far as the hand", "st.L = [Math.max(X0 + 300, Math.min(X1 - 300, Math.round(w[0]))), 0];", "st.L = [Math.max(X0 + 300, Math.min(X1 - 300, Math.round((w[0] + st.L[0]) / 2))), 0];"),
 ('sky-press-moves', "a press anywhere moves the listener", "if (nearListener(ev) || onGround(ev)) { stop();", "if (true) { stop();"),
 ('ground-press-dead', "a press on the ground does nothing", "if (nearListener(ev) || onGround(ev)) { stop();", "if (nearListener(ev)) { stop();"),
 ('jag-always', "the stroke is crooked whether asked or not", "var jagOn = document.getElementById('jag').checked;", "var jagOn = true;"),
 ('bow-opens-crooked', "the bow opens crooked", "bow: false, away: true };", "bow: true, away: true };"),
 ('straight-opens-crooked', "the straight one opens crooked", "straight: false, bow: false,", "straight: true, bow: false,"),
 ('away-opens-smooth', "pointing away opens smooth", "bow: false, away: true };", "bow: false, away: false };"),
 ('away-askew', "pointing away does not point away: its far end is 600 m too high", "[st.L[0] + side * far * ce, far * se]];", "[st.L[0] + side * far * ce, far * se + 600]];"),
 ('drawn-ignored', "a drawn line is thrown away", "st.kind = 'own'; st.raw = d; st.seed++; rebuild(); }", "st.kind = 'own'; st.seed++; rebuild(); }"),
 ('drawn-backwards', "a drawn line is taken from its end to its beginning", "st.kind = 'own'; st.raw = d; st.seed++; rebuild(); }", "st.kind = 'own'; st.raw = d.reverse(); st.seed++; rebuild(); }"),
 ('finger-ignored', "only a mouse can draw", "if (st.draw) { stop(); st.t = 0; st.drawing = [inSky(toWorld(ev))];", "if (st.draw && ev.pointerType !== 'touch') { stop(); st.t = 0; st.drawing = [inSky(toWorld(ev))];"),
 ('no-cap', "a drawn line may be as long as you like", "if (step > 30 && st.drawn + step <= LONGEST) {", "if (step > 30) {"),
 ('not-kept-in', "a drawn line may leave the picture", "function inSky(w) { return [Math.max(X0, Math.min(X1, w[0])), Math.max(0, Math.min(Z1, w[1]))]; }", "function inSky(w) { return w; }"),
 ('short-line-silent', "a line too short is refused without a word", "say.textContent = 'Too short to be a stroke: draw a line at least 150 metres long. The stroke is as it was.';", ""),
 ('lit-behind', "the lit part trails half a second behind the ring", "var lo = C * (st.t - 0.05), hi = C * st.t;", "var lo = C * (st.t - 0.55), hi = C * (st.t - 0.5);"),
 ('trace-shifted', "the line under the picture is drawn a second late", "var ta = c / cols * tmax, tb = (c + 1) / cols * tmax,", "var ta = c / cols * tmax - 1, tb = (c + 1) / cols * tmax - 1,"),
 ('marker-wrong', "the marker on the line runs at half speed", "tc.fillRect(tx(Math.min(st.t, tmax)) - DPR,", "tc.fillRect(tx(Math.min(st.t / 2, tmax)) - DPR,"),
 ('says-far-for-near', "the sentence gives the farthest point's distance for the first sound", "from <b>' + km(fh * C)", "from <b>' + km(r.farthest)"),
 ('says-last', "the sentence gives the time of the last sound as the first", "The first sound comes <b>' + fh.toFixed(1) + ' s</b>", "The first sound comes <b>' + r.last.toFixed(1) + ' s</b>"),
 ('says-near-for-far', "the sentence gives the nearest point's distance for the last sound", "</b> away; the last from ' + km(r.farthest)", "</b> away; the last from ' + km(r.nearest)"),
 ('decibels-true-for-played', "the sentence gives the true loudness as the loudness played", "and played ' + Math.round(played) + ' below.'", "and played ' + Math.round(down) + ' below.'"),
 ('decibels-halved', "the decibels are worked out with 10 for 20", "function decibels(x) { return 20 * Math.log(x) / Math.LN10; }", "function decibels(x) { return 10 * Math.log(x) / Math.LN10; }"),
 ('hidden-unsaid', "the sentence never says that part of the stroke is hidden", "(hiddenCount() > 0 ? ' The dim part of the stroke is more than half hidden from you by the bending of sound.' : '')", "''"),
 ('silence-unsaid', "a stroke deep in the shadow is described as if it could be heard", "if (fh === null) { say.textContent = 'The stroke is ' + km(len) + ' long, and nearly all of it lies in the shadow that the bending of sound makes: by this model you would hear next to nothing.'; return; }", "if (fh === null) fh = r.first;"),
 ('no-stop-at-end', "it never stops by itself", "if (st.t > st.res.last + 0.6) { stop();", "if (st.t > st.res.last + 600) { stop();"),
 ('negative-time', "the picture's clock runs 0.3 s behind the sound", "st.t = Math.max(0, st.ctx.currentTime - st.tFlash);", "st.t = st.ctx.currentTime - st.tFlash - 0.3;"),
 ('small-letters', "the lettering does not grow on a narrow screen", "FONT = Math.round(Math.max(11.5 * DPR, 20 * w / 1200));", "FONT = Math.round(20 * w / 1200);"),
 ('stroke-off-frame', "the stroke is drawn 3 km to the left", "sc.lineTo(wx(p[i + 1][0]), wz(p[i + 1][1]));", "sc.lineTo(wx(p[i + 1][0] - 3000), wz(p[i + 1][1]));"),
]
for name, what, a, b in M: assert src.count(a) == 1, name
work = os.path.join(here, 'mutants', 'page'); os.makedirs(work, exist_ok=True)
env = dict(os.environ, LD_LIBRARY_PATH=os.path.expanduser('~/web/sysroot/usr/lib/x86_64-linux-gnu'), NODE_PATH=os.path.expanduser('~/web/node_modules'))
test = os.path.expanduser('~/web/shot-thunder.js'); assert open(test, encoding='utf-8').read() == rd(os.path.join('tools', 'shot-thunder.js')), 'the test in ~/web is not the copy in tools/'
def run(path): return subprocess.run(['node', test, path, work, os.path.join(here, 'core.js')], cwd=os.path.expanduser('~/web'), env=env, capture_output=True, text=True, timeout=300)
if __name__ == '__main__':
    path = os.path.join(work, 'true.html'); open(path, 'w', encoding='utf-8').write(src.replace('/*CORE*/', core)); r = run(path)
    m = re.search(r'PAGE TEST: (\d+) assertions, (\d+) failed', r.stdout); assert m and m.group(2) == '0', 'the true page does not pass by this runner: ' + (r.stdout[-300:] + r.stderr[-300:])
    print('control: the true page, built and run in the same way: %s assertions, 0 failed\n' % m.group(1), flush=True); os.remove(path)
    caught = 0
    for name, what, a, b in M:
        path = os.path.join(work, name + '.html'); open(path, 'w', encoding='utf-8').write(src.replace(a, b).replace('/*CORE*/', core))
        try:
            r = run(path); m = re.search(r'PAGE TEST: (\d+) assertions, (\d+) failed(.*)', r.stdout)
            res = ('caught: %s of %s assertions fail%s' % (m.group(2), m.group(1), m.group(3)[:110])) if m and int(m.group(2)) > 0 else ('NOT caught: all %s assertions pass' % m.group(1)) if m else 'caught: the test stops (%s)' % (r.stderr.strip().splitlines() or ['no output'])[-1][:90]
        except subprocess.TimeoutExpired: res = 'caught: the test does not finish'
        caught += res.startswith('caught'); print('%-22s %s -- %s' % (name, what, res), flush=True)
        os.remove(path)
    for f in os.listdir(work):
        if f.endswith('.png'): os.remove(os.path.join(work, f))
    print('\n%d of %d broken copies of the page caught' % (caught, len(M)))
