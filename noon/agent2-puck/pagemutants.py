"""pagemutants.py: the page broken on purpose, one fault at a time, and pagetest.js run on each broken copy (core.js is inside the page).
    python3 -I pagemutants.py [WORKERS]     (a control run of the true page first; it must pass)"""
import os, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__))
ENV = dict(os.environ, NODE_PATH=os.path.expanduser('~/web/node_modules'), LD_LIBRARY_PATH=os.path.expanduser('~/web/sysroot/usr/lib/x86_64-linux-gnu'))
M = [
 ('the pointer is turned the other way', "return [c * x - s * y, s * x + c * y]; };", "return [c * x + s * y, -s * x + c * y]; };"),
 ('the pointer is not turned at all', "P.ring = function (hx, hy, deg) { return P.turn(hx, hy, deg); };", "P.ring = function (hx, hy, deg) { return [hx, hy]; };"),
 ('the pointer is stretched as well as turned', "P.ring = function (hx, hy, deg) { return P.turn(hx, hy, deg); };", "P.ring = function (hx, hy, deg) { var q = P.turn(hx, hy, deg); return [1.3 * q[0], q[1]]; };"),
 ('an eighth turn is a sixth', "['an eighth turn', 45]", "['an eighth turn', 60]"),
 ('the path is measured against the whole distance to the dot', "finishTrial(P.length(st.path) / (d0 - d)); return; }", "finishTrial(P.length(st.path) / d0); return; }"),
 ('the path kept is every other point', "if (st.phase === 'go' && !st.robot) st.path.push(st.ring.slice());", "if (st.phase === 'go' && !st.robot && Math.random() < 0.5) st.path.push(st.ring.slice());"),
 ('a dot is caught at twice the distance', "if (d < CATCH) { if (!st.inside) st.inside = now; if (now - st.inside > DWELL) { st.inside = 0; st.lastD = d;", "if (d < 2 * CATCH) { if (!st.inside) st.inside = now; if (now - st.inside > DWELL) { st.inside = 0; st.lastD = d;"),
 ('a round is seven dots', "if (st.trial === 8) {", "if (st.trial === 7) {"),
 ('the middle figure is of the caught dots only', "var mid = (sorted[3] + sorted[4]) / 2;", "var cs = sorted.filter(isFinite); var mid = cs.length ? cs[Math.floor(cs.length / 2)] : Infinity;"),
 ('the equation\'s column gives the sine for the cosine', "var c = Math.cos(P.fold(deg) * Math.PI / 180); return c > 1e-9 ? 1 / c : Infinity; };", "var c = Math.sin(P.fold(deg) * Math.PI / 180); return c > 1e-9 ? 1 / c : Infinity; };"),
 ('a turn the other way is called running away', "P.fold = function (deg) { return Math.abs(((deg % 360) + 540) % 360 - 180); };", "P.fold = function (deg) { return ((deg % 360) + 360) % 360; };"),
 ('the mouse in the picture is turned the same way as the pointer', "P.mouseTurn = function (deg) { return -deg; };", "P.mouseTurn = function (deg) { return deg; };"),
 ('a surprise shows its angle on the mouse', "var grp = el(s, 'g', st.hidden ? {} : { transform: 'rotate(' + P.mouseTurn(st.angle) + ')' });", "var grp = el(s, 'g', { transform: 'rotate(' + P.mouseTurn(st.angle) + ')' });"),
 ('a surprise is not told afterwards', "rd.label + (rd.hidden ? ' (it was ' + rd.angle + ' degrees)' : '')", "rd.label"),
 ('the chaser\'s words give a surprise away', "var turn = st.hidden ? 'this turn' : st.angle === 0", "var turn = false ? 'this turn' : st.angle === 0"),
 ('the pointer is followed before it has been on the board', "    if (!st.seen) return;\n    var h = place(e)", "    var h = place(e)"),
 ('choosing a turn keeps the old round\'s dots', "st.order = shuffle(); st.trial = 0; st.results = []; st.phase = 'home'; st.path = []; st.inside = 0; st.gap = false; st.ring", "st.order = shuffle(); st.phase = 'home'; st.path = []; st.inside = 0; st.gap = false; st.ring"),
 ('the page\'s chaser is slow to give the board back', "}, 1500); })();", "}, 9000); })();"),
 ('the page\'s chaser drifts outward, so that a quarter turn is no circle', "var m = Math.exp(-tau * c), q", "var m = Math.exp(-tau * c + 0.01 * tau), q"),
 ('the board is wider than a phone', "#wrap { position: relative; max-width: 34rem; margin: .6rem 0; }", "#wrap { position: relative; width: 34rem; margin: .6rem 0; }"),
 ('the dots are a sixteenth of a turn apart', "P.target = function (k, R) { var a = (k % 8) * Math.PI / 4;", "P.target = function (k, R) { var a = (k % 8) * Math.PI / 8;"),
 ('the dots stand too far out for a circle about one to fit the board', "R = 0.235 * N", "R = 0.36 * N"),
 ('the pointer is not followed off the board', "window.addEventListener('pointermove', move);", "cv.addEventListener('pointermove', move);"),
 ('no mark shows where a ring off the board is', "g.fillStyle = css('--ink'); g.beginPath(); g.arc(C + e[0], C + e[1], 9, 0, 7); g.fill();", ""),
 ('the ring is drawn at the hand, not turned', "} else { g.strokeStyle = css('--ink'); g.lineWidth = 4; g.beginPath(); g.arc(C + r[0], C + r[1], 11, 0, 7); g.stroke(); }", "} else { var rr = st.robot ? r : st.hand; g.strokeStyle = css('--ink'); g.lineWidth = 4; g.beginPath(); g.arc(C + rr[0], C + rr[1], 11, 0, 7); g.stroke(); }"),
 ('the ring is not drawn', "} else { g.strokeStyle = css('--ink'); g.lineWidth = 4; g.beginPath(); g.arc(C + r[0], C + r[1], 11, 0, 7); g.stroke(); }", "} else { }"),
 ('the dot is not drawn', "g.fillStyle = css('--b'); g.beginPath(); g.arc(C + t[0], C + t[1], 0.024 * N, 0, 7); g.fill(); }", "}"),
 ('a pointer that went away and came back elsewhere is counted', "if (away && st.phase === 'go' && !st.robot && jump > 2 * CATCH) {", "if (away && st.phase === 'go' && !st.robot && jump > 2000 * CATCH) {"),
 ('a lifted finger or pen is not noticed', "window.addEventListener('pointerup', function (e) { if (e.pointerType !== 'mouse') st.gap = true; });", ""),
 ('a pen is not covered', "if (e.pointerType !== 'mouse') st.gap = true;", "if (e.pointerType === 'touch') st.gap = true;"),
 ('a mouse out of the window and back is not noticed', "document.documentElement.addEventListener('pointerleave', function () { st.gap = true; });", ""),
 ('a finger put down beside the board is not noticed', " window.addEventListener('pointerdown', move);", ""),
 ('a page left alone goes on losing dots', "if (now - st.lastMove > IDLE) {", "if (false) {"),
 ('a dot comes without any movement', "if (d < HOME && st.fresh) {", "if (d < HOME) {"),
 ('the chaser\'s path runs past the edge of the board', "if (Math.abs(p[0]) > half || Math.abs(p[1]) > half) break;", ""),
 ('the chaser at a quarter turn stops after half a round', "if (out === 'circles' && tau * Math.abs(s) >= 4 * Math.PI) break;", "if (out === 'circles' && tau * Math.abs(s) >= 1 * Math.PI) break;"),
 ('choosing a turn does not stop the chaser', "stopRobot(); st.label = label;", "st.label = label;"),
]
def run(page):
    with tempfile.TemporaryDirectory(dir=HERE) as t:
        f = os.path.join(t, 'puck.html'); open(f, 'w', encoding='utf-8').write(page)
        try: r = subprocess.run(['node', os.path.join(HERE, 'pagetest.js'), f], env=ENV, capture_output=True, text=True, timeout=400)
        except subprocess.TimeoutExpired: return 1, ['FAILED: the test did not finish in 400 seconds'], []
        return r.returncode, [l for l in r.stdout.splitlines() if l.startswith('FAILED')], r.stderr.strip().splitlines()[-1:]
if __name__ == '__main__':
    true = open(os.path.join(HERE, 'puck.html'), encoding='utf-8').read(); workers = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    code, fails, err = run(true); print('control (the true page): %s' % ('passes' if code == 0 else 'FAILS %s %s' % (fails, err))); assert code == 0
    for what, a, b in M: assert true.count(a) == 1, 'this fault does not find its text exactly once: ' + what
    with ThreadPoolExecutor(workers) as ex: res = list(ex.map(lambda m: run(true.replace(m[1], m[2])), M))
    caught = 0
    for (what, a, b), (code, fails, err) in zip(M, res):
        caught += code != 0; print('%-58s %s' % (what, ('caught: ' + (fails[0][8:90] if fails else 'the test stopped: ' + ' '.join(err)[:60])) if code else 'PASSED, not caught'))
    print('%d of %d broken copies caught' % (caught, len(M)))
