# mutants.py -- can the tests of core.js fail?  Copies of core.js with one thing broken, each run through test-core.js.
#   python -I mutants.py > mutants.out
import subprocess, os, re
here = os.path.dirname(os.path.abspath(__file__)); rd = lambda n: open(os.path.join(here, n), encoding='utf-8').read()
core = rd('core.js'); test = rd('test-core.js')
M = [
 ('order-early', "the order of 2 stops one doubling early", "while (x !== 1) { x = x * 2 % m; n++; } return n;", "while (x !== 1) { x = x * 2 % m; n++; } return Math.max(1, n - 1);"),
 ('exponents-lost', "every prime is listed as occurring once", "out.push([l, e]); } l +=", "out.push([l, 1]); } l +="),
 ('rule-any-square', "HAKMEM's rule: any square of an odd prime serves", "if (by) spoilt.push(by); else if (!serves) serves = { l: l, e: e, k: here };", "if (!serves) serves = { l: l, e: e, k: here };"),
 ('rule-all-squares', "the book's claim: every prime must occur squared", "bounded: !!serves, serves: serves,", "bounded: !!serves && f.every(function (x) { return x[1] >= 2; }), serves: serves,"),
 ('exceptional-ignored', "1093 squared is taken to serve like any square", "if (here <= before) by = { l: l, e: e, self: true };", ""),
 ('spoil-needs-more', "a square is spoilt only when a higher power divides the other order", "if (val(o, l) >= here) by =", "if (val(o, l) > here) by ="),
 ('spoil-by-r-less-1', "spoiling is judged by r - 1, not by the order of 2 modulo r", "var o = order2(f[j][0]); if (val(o, l) >= here)", "var o = f[j][0] - 1; if (val(o, l) >= here)"),
 ('tail-one-short', "the tail is counted one step short", "while (m % 2 === 0) { m /= 2; s++; }", "while (m % 2 === 0) { m /= 2; s++; } if (s) s--;"),
 ('not-lowest-terms', "the fraction is not brought to lowest terms", "var g = gcd(P, Q) || 1, p = P / g, q = Q / g, s = 0, m = q;", "var g = 1, p = P / g, q = Q / g, s = 0, m = q;"),
 ('home-with-tail', "a turtle with a tail is called home", "home: !!serves && s === 0,", "home: !!serves,"),
 ('straight-missed', "a power of two is not seen as walking straight", "straight: m === 1 };", "straight: false };"),
 ('negative-kept', "a negative upper number is not brought into range", "    p = mod(p, q);\n", ""),
 ('counts-one-more', "how often a prime divides is counted one too many", "function val(o, l) { var k = 0;", "function val(o, l) { var k = 1;"),
 ('turns-right', "the turtle turns right", "x -= Math.sin(head * K); y += Math.cos(head * K);", "x += Math.sin(head * K); y += Math.cos(head * K);"),
 ('steps-first', "the turtle steps before it turns", "      head = (head + turn) % q; turn = turn * 2 % q;\n      x -= Math.sin(head * K); y += Math.cos(head * K);", "      x -= Math.sin(head * K); y += Math.cos(head * K); head = (head + turn) % q; turn = turn * 2 % q; //"),
 ('trebles', "the turn is trebled", "turn = turn * 2 % q;", "turn = turn * 3 % q;"),
 ('adds', "the first turn is added each time, not doubled (the other turtle)", "turn = turn * 2 % q;", "turn = (turn + p) % q;"),
 ('home-anywhere', "home is any return to the starting point", "if (!home && head === 0 && turn === p) home = k;", "if (!home) home = k;"),
 ('home-any-heading', "home does not ask which way it faces", "if (!home && head === 0 && turn === p) home = k;", "if (!home && turn === p) home = k;"),
 ('home-any-turn', "home does not ask what its next turn is", "if (!home && head === 0 && turn === p) home = k;", "if (!home && head === 0) home = k;"),
 ('never-there', "it never notices standing on its start", "if (!there) there = k; ", ""),
 ('box-without-start', "the box leaves out the start", "var x0 = 0, x1 = 0, y0 = 0, y1 = 0;", "var x0 = w.xs[1], x1 = w.xs[1], y0 = w.ys[1], y1 = w.ys[1];"),
 ('census-from-5', "the census begins at 5", "for (var m = 3, i = 0; m <= top; m += 2, i++) {", "for (var m = 5, i = 0; m <= top; m += 2, i++) {"),
 ('census-kinds', "the census does not tell a spoilt square from none", "else if (f.squares) { kind[i] = 1; spoilt++; } else plain++;", "else plain++;"),
 ('decimal-taken', "a number with a decimal point is taken", "(\\d{1,7})\\s*$", "(\\d{1,7})(?:\\.\\d+)?\\s*$"),
 ('eight-figures', "eight figures are taken", "(\\d{1,7})", "(\\d{1,8})"),
 ('clock-skips-tail', 'the clock marks the turns from the first, tail and all', '    for (k = 0; k < f.tail; k++) t = t * 2 % q;\n    var hours = new Int32Array(n)', '    var hours = new Int32Array(n)'),
 ('clock-clockwise', 'the balance point is reckoned with the hours counted rightwards', 'cx -= Math.sin(t * K); cy += Math.cos(t * K); t = t * 2 % q; }', 'cx += Math.sin(t * K); cy += Math.cos(t * K); t = t * 2 % q; }'),
 ('clock-step-wrong', 'the polygons are looked for with steps of q over l squared', 'var l = f.factors[i][0], step = q / l, all', 'var l = f.factors[i][0], step = q / (l * l), all'),
 ('clock-any-hour', "every prime that comes in twice is said to give polygons (the memo's rule, on the clock)", 'if (!mark[(hours[j] + step) % q]) all = false;', 'if (false) all = false;'),
 ('clock-off-not-mean', "the balance point's distance is the sum's, not the mean's", 'off: Math.hypot(cx, cy) / n };', 'off: Math.hypot(cx, cy) };'),
 ('polygon-short', 'a polygon is given one corner too few', 'for (k = 0; k < l; k++) out.push((a + k * (q / l)) % q); return out; }', 'for (k = 0; k < l - 1; k++) out.push((a + k * (q / l)) % q); return out; }'),
 ('clock-once-prime', 'polygons are looked for with a prime that comes in once as well', 'all = f.factors[i][1] >= 2;', 'all = true;'),
 ('clock-first-hour', 'only the first hour is asked whether its polygon is whole', 'for (j = 0; j < n && all; j++) if (!mark[', 'for (j = 0; j < 1 && all; j++) if (!mark['),
 ('takeout-once-prime', 'primes that come in once are listed among those taken out', 'if (e < 2) continue;\n      var n1 = order2(f.m / l);', 'var n1 = order2(f.m / l);'),
 ('takeout-two-out', 'the round is compared with the turtle that has two of the prime taken out', 'var n1 = order2(f.m / l); out.push(', 'var n1 = order2(f.m / l / l); out.push('),
 ('takeout-long-always', 'every repeated prime is said to make the round l times as long', 'long: f.round === l * n1 });', 'long: true });'),
 ('takeout-not-same', 'the round is called l times as long whenever it is not the same length', 'long: f.round === l * n1 });', 'long: f.round !== n1 });'),
 ('no-commas', "thousands are not set off", "function commas(n) { return String(n).replace(/\\B(?=(\\d{3})+$)/g, ','); }", "function commas(n) { return String(n); }"),
]
# two broken copies that no turtle can tell from the true one: for this turtle the heading is back exactly when the turn is
# (after k steps the heading has changed by (2^k - 1) p/q of a turn and the turn is 2^k p/q), so either clause of "home" implies the other
EQUAL = {'home-any-heading': 'as expected: the heading is back whenever the turn is ((2^k - 1) p/q is whole exactly when 2^k p/q = p/q)',
         'home-any-turn': 'as expected: the turn is back whenever the heading is ((2^k - 1) p/q is whole exactly when 2^k p/q = p/q)',
         # two more, of the clock (27 November): for a prime l that comes in once, the l-gon through an hour holds an hour that l divides more
         # often than it divides the hours of the round, and doubling never reaches it; and the hours of a round are one hour's multiples by
         # powers of 2, so if one hour's polygon is whole every hour's is
         'clock-once-prime': 'as expected: with a prime that comes in once no round falls into polygons, so asking changes nothing',
         'clock-first-hour': 'as expected: the hours of a round are the first hour times powers of 2, so one whole polygon means all are whole',
         'takeout-not-same': 'as expected: a round is always either l times as long as the round with one l out or no longer, so "not the same" is "l times"'}
for name, what, a, b in M: assert core.count(a) == 1, name
work = os.path.join(here, 'mutants'); os.makedirs(work, exist_ok=True)
def run(text):
    open(os.path.join(work, 'core.js'), 'w', encoding='utf-8').write(text); open(os.path.join(work, 'test-core.js'), 'w', encoding='utf-8').write(test)
    try: r = subprocess.run(['node', 'test-core.js', os.path.join(here, 'table.json')], cwd=work, capture_output=True, text=True, timeout=300)
    except subprocess.TimeoutExpired: return None, 'the test does not finish'
    m = re.search(r'CORE TEST: (\d+) assertions, (\d+) failed', r.stdout)
    first = next((l[5:95] for l in r.stdout.splitlines() if l.startswith('FAIL')), '')
    return m, first if m else (r.stderr.strip().splitlines() or ['no output'])[-1][:90]
if __name__ == '__main__':
    m, _ = run(core); assert m and m.group(2) == '0', 'the true core does not pass by this runner'
    print('control: the true core.js, run in the same way: %s assertions, 0 failed\n' % m.group(1), flush=True)
    caught = 0
    for name, what, a, b in M:
        m, first = run(core.replace(a, b))
        if m and m.group(2) == '0': res = 'NOT caught: all %s assertions pass' % m.group(1) + ('; ' + EQUAL[name] if name in EQUAL else '')
        elif m: res = 'caught: %s of %s fail; first: %s' % (m.group(2), m.group(1), first)
        else: res = 'caught: the test stops (%s)' % first
        caught += res.startswith('caught'); print('%-20s %s -- %s' % (name, what, res), flush=True)
    for f in ('core.js', 'test-core.js'): os.remove(os.path.join(work, f))
    print('\n%d of %d broken copies caught; %d not caught and expected not to be' % (caught, len(M), sum(1 for name, what, a, b in M if name in EQUAL)))
