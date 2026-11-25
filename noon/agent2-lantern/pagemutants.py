"""pagemutants.py: plant one fault at a time in a copy of the page's sources (core.js or page.js), build the page from the copy and
see whether pagetest.py notices.   python -I pagemutants.py [WORKERS]
The first copy has no fault and must pass (the control). Writes pagemutants.out."""
import os, shutil, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); PY = sys.executable; WORKERS = int(sys.argv[1]) if len(sys.argv) > 1 else 4
M = [('control', None, [])]
def c(name, *pairs): M.append((name, 'core.js', list(pairs)))
def p(name, *pairs): M.append((name, 'page.js', list(pairs)))
c('the lens equation\'s farther place', ("var s = (D - Math.sqrt(D * D - 4 * D)) / 2;", "var s = (D + Math.sqrt(D * D - 4 * D)) / 2;"))
c('the lens put on the far side of K', ("return k[0] - Math.sqrt(w2) - r.q;", "return k[0] + Math.sqrt(w2) - r.q;"))
c('the patch over the screen\'s distance', ("var si = s / (s - 1); return Math.abs((D - s) - si) / si;", "var si = s / (s - 1); return Math.abs((D - s) - si) / (D - s);"))
c('brightness by the distance, not its square', ("var sp = DofM(m) - s; return open / (sp * sp);", "var sp = DofM(m) - s; return open / sp;"))
c('the shade\'s opening as a length', ("open = u <= 0 ? 0 : Math.min(u * u, 1);", "open = u <= 0 ? 0 : Math.min(u, 1);"))
c('K below the pivots', ("return [r.p + t * dx / d - h * dy / d, r.yI + t * dy / d + h * dx / d];", "return [r.p + t * dx / d + h * dy / d, r.yI + t * dy / d - h * dx / d];"))
c('KL cut to IK less f', ("b: o.b === undefined ? Math.sqrt(a * a - 1) : o.b", "b: o.b === undefined ? a - 1 : o.b"))
p('"the rods as they should be" with KL a little short', ("make: function () { return C.rods({ a: A_RODS }); } },\n    plate", "make: function () { return C.rods({ a: A_RODS, b: Math.sqrt(A_RODS * A_RODS - 1.05) }); } },\n    plate"), ("if (st.mech === 'right') must(", "if (false) must("))
p('the engraving\'s rods with I two focal lengths out', ("p: 1.84, e: 0 }", "p: 2.0, e: 0 }"))
p('the words under the side view always say 11 focal lengths', ("fmt(rr.a, 2) + ' and ' + fmt(rr.a2, 2)", "'11.00 and 11.00'"))
p("the Britannica's rods given Young's equal pair after all (KN = IK)", ("return C.rods({ a: A_RODS, a2: b, b: b }); } },", "return C.rods({ a: A_RODS, a2: A_RODS, b: b }); } },"))
p("the Britannica's rods with KL a hundredth short of KN", ("return C.rods({ a: A_RODS, a2: b, b: b }); } },", "return C.rods({ a: A_RODS, a2: b, b: 0.99 * b }); } },"))
p('N a twentieth too high, not a tenth', ("C.rods({ a: A_RODS, yN: 0.1 })", "C.rods({ a: A_RODS, yN: 0.05 })"))
p('L a twentieth too high, not a fiftieth', ("C.rods({ a: A_RODS, yL: 0.02 })", "C.rods({ a: A_RODS, yL: 0.05 })"))
p('no rods: the lens left where it was sharp at three times', ("} else s = C.focus(C.DofM(5))[0];", "} else s = C.focus(C.DofM(3))[0];"))
p('the shade shut at 1.2 f', ("X0_SHADE = 0.833", "X0_SHADE = 1.2"))
p('a jam passed over: the lens shown where it ought to be', ("if (s === null || s <= 1) { jam = true; s = null; }", "if (s === null || s <= 1) { s = want; }"))
p('the size of the ghost taken from where the lantern stands', ("out.size = (D - s) / s;", "out.size = st.m;"))
p('brightness set against a ghost of five times', ("out.light / C.light(10, C.focus(C.DofM(10))[0],", "out.light / C.light(5, C.focus(C.DofM(5))[0],"))
p('the words give twice the patch', ("' + fmt(o.patch, 4) + ' of the lens", "' + fmt(o.patch * 2, 4) + ' of the lens"))
p('the words give the wanted place for the lens\'s own', ("'The lens stands ' + fmt(o.s, 4)", "'The lens stands ' + fmt(o.want, 4)"))
p('the words say "with no shade" always', ("(state.shade ? 'under the same shade.' : 'with no shade.')", "'with no shade.'"))
p('the ghost drawn to one side', ("ghost(ctx, W / 2, Hh / 2, H, alpha);", "ghost(ctx, W / 2 + 150, Hh / 2, H, alpha);"))
p('the ghost never blurred', ("ctx.filter = blurPx > 0.15 ? 'blur(' + blurPx.toFixed(2) + 'px)' : 'none';", "ctx.filter = 'none';"))
p('the ghost as bright at every size', ("alpha = Math.max(0.04, Math.min(1, Math.pow(o.light10, 1 / 2.2) * 0.62));", "alpha = 0.62;"))
p('K drawn half a focal length off', ("K = [X(o.K[0]), Y(o.K[1])];", "K = [X(o.K[0] + 0.5), Y(o.K[1])];"))
p('L drawn at the lens', ("L = [X(o.s + r.q), Y(r.yL)]", "L = [X(o.s), Y(r.yL)]"))
p('the rods drawn grey', ("ctx.strokeStyle = '#eb6834'; ctx.lineWidth = 2.5;", "ctx.strokeStyle = '#8a8fa3'; ctx.lineWidth = 2.5;"))
p('the pivots not drawn', ("ctx.fillStyle = '#f4f4f6'; [I, L, N, K].forEach(function (p) { ctx.beginPath(); ctx.arc(p[0], p[1], 3.5, 0, 6.2832); ctx.fill(); });", "ctx.fillStyle = '#f4f4f6';"))
p('the slider reads to 10 times at its end', ("set({ m: Math.pow(20, Number(e.target.value) / 1000) });", "set({ m: Math.pow(10, Number(e.target.value) / 1000) });"))
p('the buttons for the rods do nothing', ("el.addEventListener('change', function () { set({ mech: el.value }); });", "el.addEventListener('change', function () { });"))
p('the shade\'s box does nothing', ("$('shade').addEventListener('change', function (e) { set({ shade: e.target.checked }); });", "$('shade').addEventListener('change', function (e) { });"))
p('the ghost does not advance', ("set({ m: Math.exp(Math.log(1.3) + u * (Math.log(18) - Math.log(1.3))) });", "set({ m: state.m });"))
p('Stop does not stop', ("if (timer) { clearInterval(timer); timer = null;", "if (timer) { timer = null;"))
p('the buttons left as they were when the state is set', ("if (rb) rb.checked = true; $('shade').checked = !!state.shade;", ""))
p('the slider left where it was when the state is set', ("    $('slider').value = String(Math.round(1000 * Math.log(state.m) / Math.log(20)));", ""))
def one(job):
    i, (name, target, pairs) = job; d = '/dev/shm/agent2-pgmut-%d-%d' % (os.getpid(), i); os.makedirs(d); t0 = time.time()
    try:
        for x in ('lantern.src.html', 'core.js', 'page.js'): shutil.copy(os.path.join(HERE, x), d)
        if pairs:
            s = open(os.path.join(d, target)).read()
            for a, b in pairs:
                if s.count(a) != 1: return i, name, target, 'NOT PLANTED', 'the text to change was found %d times' % s.count(a), 0
                s = s.replace(a, b)
            open(os.path.join(d, target), 'w').write(s)
        try: r = subprocess.run(['nice', '-n', '19', PY, '-I', os.path.join(HERE, 'pagetest.py'), d], capture_output=True, text=True, timeout=900); rc, out = r.returncode, r.stdout
        except subprocess.TimeoutExpired: rc, out = -9, ''
        fails = [l[6:110] for l in out.split('\n') if l.startswith('FAIL')]; last = out.strip().split('\n')[-1][:100] if out.strip() else 'no output'
        if not pairs: return i, name, '', 'control passed' if rc == 0 else 'CONTROL FAILED', last, time.time() - t0
        return i, name, target, 'noticed' if rc != 0 else 'PASSED', ('%d tests failed; first: %s' % (len(fails), fails[0]) if fails else last), time.time() - t0
    finally: shutil.rmtree(d, ignore_errors=True)
if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=WORKERS) as ex: res = list(ex.map(one, enumerate(M)))
    lines = ['%-9s %-8s %-62s %-15s %4.0f s   %s' % ('' if r[1] == 'control' else 'fault %d' % r[0], r[2], r[1], r[3], r[5], r[4]) for r in res]
    planted = [r for r in res if r[1] != 'control' and r[3] != 'NOT PLANTED']; noticed = [r for r in planted if r[3] == 'noticed']
    lines.append('%d faults planted, %d noticed, %d passed every test, %d could not be planted; the control %s' % (len(planted), len(noticed), len(planted) - len(noticed), sum(1 for r in res if r[3] == 'NOT PLANTED'), res[0][3]))
    open(os.path.join(HERE, 'pagemutants.out'), 'w').write('\n'.join(lines) + '\n'); print('\n'.join(lines))
