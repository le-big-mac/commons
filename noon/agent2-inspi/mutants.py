# mutants.py -- can the tests of core.js fail?  Copies of core.js with one thing broken, each run through test-core.js.
#   python -I mutants.py > mutants.out
import subprocess, os, re
here = os.path.dirname(os.path.abspath(__file__)); rd = lambda n: open(os.path.join(here, n), encoding='utf-8').read()
core = rd('core.js'); test = rd('test-core.js')
M = [
 ('gcd-stops-early', "the greatest common divisor stops one step early", "while (b) { var t = a % b; a = b; b = t; } return a; }", "while (b > 1) { var t = a % b; a = b; b = t; } return a; }"),
 ('mod-negative', "a negative number is not brought into one whole turn", "function mod(a, m) { return ((a % m) + m) % m; }", "function mod(a, m) { return a % m; }"),
 ('parse-four', "four decimals are accepted", "(?:\\.(\\d{0,3}))?", "(?:\\.(\\d{0,4}))?"),
 ('parse-sign', "a minus sign is dropped", "return (m[1] === '-' || m[1] === '\\u2212') ? -v : v;", "return v;"),
 ('point-first-refused', "a number that begins with its point is refused", "(\\d{0,6})", "(\\d{1,6})"),
 ('printed-minus-refused', "the minus sign the page prints is not taken when typed", "([+\\-\\u2212]?)", "([+\\-]?)"),
 ('seven-figures', "seven figures before the point are accepted", "(\\d{0,6})", "(\\d{0,7})"),
 ('least-is-first', "the census keeps the first number of steps it meets as the least", "if (!least || f.steps < least) least = f.steps;", "if (!least) least = f.steps;"),
 ('show-zeros', "trailing noughts are kept", "frac = frac.replace(/0+$/, ''); ", ""),
 ('lap-term-dropped', "the turning in a lap leaves out the part from the amount added", "var T = mod(q * a + (FULL / 2) * ((p * (q - 1)) % 2), FULL);", "var T = mod(q * a, FULL);"),
 ('lap-term-pq', "the turning in a lap uses p q for p (q - 1)", "((p * (q - 1)) % 2)", "((p * q) % 2)"),
 ('lap-quarter', "the part from the amount added is a quarter turn, not a half", "(FULL / 2) *", "(FULL / 4) *"),
 ('laps-numerator', "the number of laps is the numerator, not the denominator", "var v = FULL / gcd(T, FULL);", "var v = T / gcd(T, FULL);"),
 ('steps-are-laps', "the forecast gives the laps as the steps", "laps: v, steps: q * v };", "laps: v, steps: v };"),
 ('gain-q', "the gain in a lap is q, not its square root", "gain: Math.sqrt(q) };", "gain: q };"),
 ('lap-always-360', "a lap is 360 steps whatever the amount", "q = i === 0 ? 1 : FULL / g, p = i === 0 ? 0 : i / g;", "q = i === 0 ? 1 : 360, p = i === 0 ? 0 : i / UNIT;"),
 ('p-is-one', "p is taken as 1", "p = i === 0 ? 0 : i / g;", "p = i === 0 ? 0 : 1;"),
 ('turns-left', "the turtle turns left", "x += Math.sin(head * K); y += Math.cos(head * K);", "x -= Math.sin(head * K); y += Math.cos(head * K);"),
 ('faces-right', "the turtle starts facing to the right", "x += Math.sin(head * K); y += Math.cos(head * K);", "x += Math.cos(head * K); y -= Math.sin(head * K);"),
 ('adds-first', "the amount is added before the turn, not after", "head = (head + ang) % FULL; ang = (ang + inc) % FULL;", "ang = (ang + inc) % FULL; head = (head + ang) % FULL;"),
 ('home-any-heading', "home does not ask which way it faces", "if (!home && head === 0 && ang === a0) home = k;", "if (!home && ang === a0) home = k;"),
 ('home-any-turn', "home does not ask what its next turn is", "if (!home && head === 0 && ang === a0) home = k;", "if (!home && head === 0) home = k;"),
 ('near-is-a-tenth', "'at the start' means within a tenth of a step", "var NEAR = 1e-7;", "var NEAR = 0.1;"),
 ('never-there', "it never notices standing on its start", "if (!there) there = k; ", ""),
 ('tenfold-angles', "angles are taken ten times too large", "K = 2 * Math.PI / FULL;", "K = 20 * Math.PI / FULL;"),
 ('box-ignores-stop', "the box ignores where it was told to stop", "var n = upto === undefined ? w.xs.length - 1 : upto,", "var n = w.xs.length - 1,"),
 ('box-without-start', "the box leaves out the start", "x0 = 0, x1 = 0, y0 = 0, y1 = 0;", "x0 = w.xs[1], x1 = w.xs[1], y0 = w.ys[1], y1 = w.ys[1];"),
 ('census-from-nought', "the census counts the turtles that add nothing", "for (var inc = 1; inc < 360; inc++) for (var a = 0; a < 360; a++) {\n      var f = forecast(", "for (var inc = 0; inc < 360; inc++) for (var a = 0; a < 360; a++) {\n      var f = forecast("),
 ('census-least', "the census keeps the least number of steps as the longest", "if (f.steps > longest) longest = f.steps;", "if (f.steps < longest || !longest) longest = f.steps;"),
 ('no-commas', "thousands are not set off", "function commas(n) { return String(n).replace(/\\B(?=(\\d{3})+$)/g, ','); }", "function commas(n) { return String(n); }"),
]
# one broken copy that no whole-degree turtle can tell from the true one: test-core.js counts that the case never arises (0 of 129,240)
EQUAL = {'home-any-turn': 'as expected: no turtle tried ever stands on its start facing as it began with another turn to come (test-core.js counts 0 of 129,240)'}
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
