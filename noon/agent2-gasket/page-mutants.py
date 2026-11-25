# page-mutants.py -- can the page test fail?  Copies of the page with one thing broken in its own script (not in gcore.js),
# each built and run through tools/shot-gasket.js in a headless browser.   python -I page-mutants.py
import subprocess, os, re
here = os.path.dirname(os.path.abspath(__file__)); src = open(os.path.join(here, 'page.src.html'), encoding='utf-8').read()
core = open(os.path.join(here, 'gcore.js'), encoding='utf-8').read(); data = open(os.path.join(here, 'data.json'), encoding='utf-8').read()
muts = [
 ('big-circle-label-unguarded', "the number of a very large circle is placed without asking whether there is a place (the error the referee found)", "if (b > 0 && at2 && at2[0] > 30", "if (b > 0 && at2[0] > 30"),
 ('pointer-upside-down', "the pointer's height is read upside down", "wy = -(py - H / 2) / view.s, best", "wy = (py - H / 2) / view.s, best"),
 ('fives-wrong', "\"multiples of 5\" lights numbers one more than a multiple of 5", "return function (b) { return b % 5 === 0; };", "return function (b) { return b % 5 === 1; };"),
 ('strip-centre-forgets-period', "a circle's centre in the strip is given without the periods it was moved along", "function trueX(c) { return BigInt(c[1]) + 2n * BigInt(c[5] || 0) * BigInt(c[0]); }", "function trueX(c) { return BigInt(c[1]); }"),
 ('squares-as-doubles', "\"squares\" lights twice a square", "var u = +h; return function (b)", "var u = +h * 2; return function (b)"),
 ('left-out-unsaid', "the page does not say when circles are left out for want of exact numbers", "(res.leftOut ? ' (some circles may be missing here", "(false ? ' (some circles may be missing here"),
 ('inside-of-wrong', "the page says the view is inside a circle when it is not, and not when it is", "* view.s / c[0] >= 589) insideOf", "* view.s / c[0] < 589) insideOf"),
 ('chart-drops-a-family', "the chart leaves out the last family", "d.families.forEach(function (u) { var list = [];", "d.families.slice(0, -1).forEach(function (u) { var list = [];"),
]
for name, what, a, b in muts: assert src.count(a) == 1, name
os.makedirs(os.path.join(here, 'mutants'), exist_ok=True); env = dict(os.environ, LD_LIBRARY_PATH=os.path.expanduser('~/web/sysroot/usr/lib/x86_64-linux-gnu')); caught = 0
for name, what, a, b in muts:
    path = os.path.join(here, 'mutants', 'page-' + name + '.html'); open(path, 'w', encoding='utf-8').write(src.replace(a, b).replace('/*CORE*/', core).replace('/*DATA*/[]', data))
    try:
        r = subprocess.run(['node', os.path.expanduser('~/web/shot-gasket.js'), path, os.path.join(here, 'mutants'), os.path.join(here, 'gcore.js'), os.path.join(here, 'data.json')], cwd=os.path.expanduser('~/web'), env=env, capture_output=True, text=True, timeout=400)
        m = re.search(r'PAGE TEST: (\d+) assertions, (\d+) failed(.*)', r.stdout)
        res = ('caught: %s of %s assertions fail%s' % (m.group(2), m.group(1), m.group(3)[:110])) if m and int(m.group(2)) > 0 else ('NOT caught: all %s assertions pass' % m.group(1)) if m else 'caught: the test stops with an error'
    except subprocess.TimeoutExpired: res = 'caught: the test does not finish'
    caught += res.startswith('caught'); print('%-28s %s -- %s' % (name, what, res), flush=True)
print('\n%d of %d broken copies of the page caught' % (caught, len(muts)))
