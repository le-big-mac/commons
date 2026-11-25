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
 ('a dot is caught at twice the distance', "if (d < CATCH) { if (!st.inside) st.inside = now; if (now - st.inside > DWELL) { st.inside = 0; st.lastD = d; var d0", "if (d < 2 * CATCH) { if (!st.inside) st.inside = now; if (now - st.inside > DWELL) { st.inside = 0; st.lastD = d; var d0"),
 ('a round is seven dots', "if (st.trial === 8) {", "if (st.trial === 7) {"),
 ('the table\'s middle figure is the largest', "var mid = sorted.length ? (sorted.length % 2 ? sorted[(sorted.length - 1) / 2] : (sorted[sorted.length / 2 - 1] + sorted[sorted.length / 2]) / 2) : Infinity;", "var mid = sorted.length ? sorted[sorted.length - 1] : Infinity;"),
 ('the chaser\'s column gives the sine for the cosine', "P.pathRatio = function (deg) { var c = Math.cos(deg * Math.PI / 180);", "P.pathRatio = function (deg) { var c = Math.sin(deg * Math.PI / 180);"),
 ('a turn the other way is called running away', "var a = Math.abs(((deg % 360) + 540) % 360 - 180); return a < 89.5", "var a = ((deg % 360) + 360) % 360; return a < 89.5"),
 ('a surprise shows its angle on the mouse', "var grp = el('g', { transform: st.hidden ? '' : 'rotate(' + st.angle + ')' });", "var grp = el('g', { transform: 'rotate(' + st.angle + ')' }); st.hiddenShown = true;"),
 ('a surprise is not told afterwards', "rd.label + (rd.hidden ? ' (it was ' + rd.angle + ' degrees)' : '')", "rd.label"),
 ('the chaser\'s words give a surprise away', "(st.hidden ? 'this turn' : 'a turn of ' + st.angle + ' degrees')", "('a turn of ' + st.angle + ' degrees')"),
 ('a dot is given before the pointer has come', "if (st.robot || !st.seen) return;", "if (st.robot) return;"),
 ('choosing a turn keeps the old round\'s dots', "st.order = shuffle(); st.trial = 0; st.results = []; st.phase = 'home'; st.path = []; st.robot = null; st.ring", "st.order = shuffle(); st.phase = 'home'; st.path = []; st.robot = null; st.ring"),
 ('the page\'s chaser is slow to give the board back', "}, 1500); })();", "}, 9000); })();"),
 ('the page\'s chaser takes steps too big to be steady', "run = P.run(st.angle, R, k, 0.04, CATCH, 4000);", "run = P.run(st.angle, R, k, 1.7, CATCH, 4000);"),
 ('the board is wider than a phone', "#wrap { position: relative; max-width: 34rem; margin: .6rem 0; }", "#wrap { position: relative; width: 34rem; margin: .6rem 0; }"),
 ('the dots are a sixteenth of a turn apart', "P.target = function (k, R) { var a = (k % 8) * Math.PI / 4;", "P.target = function (k, R) { var a = (k % 8) * Math.PI / 8;"),
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
