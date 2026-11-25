"""facts.py: the quotations against the saved sources, and the README's figures recomputed.
    python3 -I facts.py ~/puck-data"""
import json, math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import puck
def squeeze(s): return re.sub(r'\s+', '', s)
if __name__ == '__main__':
    root = os.path.expanduser(sys.argv[1]); bad = 0; n = 0
    def check(ok, what):
        global bad, n
        n += 1; bad += not ok; print('%s  %s' % ('ok    ' if ok else 'FAILED', what))
    for q in json.load(open(os.path.join(HERE, 'quotes.json'))):
        src = open(os.path.join(root, q['source']), encoding='utf-8', errors='replace').read()
        joined = re.sub(r'-\s*\n\s*', '', src)                 # a word broken at a line's end with a hyphen, put together again
        check(squeeze(q['quote']) in squeeze(src) or squeeze(q['quote']) in squeeze(joined), 'quoted words are in %s: "%s..."' % (q['source'], q['quote'][:60]))
    readme = re.sub(r'\s+', ' ', open(os.path.join(HERE, 'README.md'), encoding='utf-8').read())
    src = open(os.path.join(HERE, 'page.src.html'), encoding='utf-8').read(); Rr = float(re.search(r'R = ([\d.]+) \* N', src).group(1)); Cc = float(re.search(r'CATCH = ([\d.]+) \* N', src).group(1))
    claims = [
        ('the spiral\'s lengths', '%.2f times at 15 degrees, %.2f at 30, %.2f at 45, %d at 60, %.2f at 75' % (puck.ratio(15), puck.ratio(30), puck.ratio(45), round(puck.ratio(60)), puck.ratio(75)), abs(puck.ratio(60) - 2) < 1e-9),
        ('the picture is shown, and its legend gives the lengths as computed', 'spirals.png', all(t in open(os.path.join(HERE, 'figure.py')).read() for t in ('%.2f times as long' % puck.ratio(30), '%.1f times as long' % puck.ratio(80), 'a sixth of a turn: twice as long'))),
        ('in brief', '%.2f times the distance at an eighth of a turn, twice at a sixth' % puck.ratio(45), True),
        ('the delays', 'a delay of %.2f s with no turn, %.2f s at 30 degrees, %.2f s at 45 and %.2f s at 60' % tuple(puck.limit_delay(a, 5) for a in (0, 30, 45, 60)), True),
        ('the turn a fifth of a second allows', 'steady only under a turn of less than %.1f degrees' % math.degrees(math.pi / 2 - 5 * 0.2), puck.simulate(32.0, k=5.0, tau=0.2, T=120)[0] < 0.1 and puck.simulate(33.4, k=5.0, tau=0.2, T=120)[0] > 2),
        ('the stepped hand of the test', '%.2f times the distance at 45 degrees in steps of a twentieth, %.2f at 60 degrees the other way in steps of a twenty-fifth' % (puck.step_ratio(45, 0.05), puck.step_ratio(60, 0.04)), 'round(0.05, 45)' in open(os.path.join(HERE, 'pagetest.js')).read() and 'round(0.04, -60)' in open(os.path.join(HERE, 'pagetest.js')).read()),
        ('a straight line that clips the dot', "a straight line that only clips the dot's side scores about %.2f, and one that overshoots to its far edge %.2f" % (math.hypot(Rr, Cc) / (Rr - Cc), (Rr + Cc) / (Rr - Cc)), True),
        ('the README quotes the report as the report has it', 'The condition which produced the highest average RMS ERROR was the 90° rotation. This was followed by the two reflections (which were the same) and the 135° rotation. The 45° and 180° rotations produced the least error and were similar to one another.', True),
        ('the README quotes Wikipedia as it has it', 'widely considered clumsy, due to its small size and tendency to rotate in use', True),
        ('the page quotes the same five words', 'tendency to rotate in use', 'tendency to rotate in use' in src),
        ('the page gives the clipped dot\'s figure too', 'clips the dot\'s side scores about %.2f' % (math.hypot(Rr, Cc) / (Rr - Cc)), 'clips the dot\'s side scores about %.2f' % (math.hypot(Rr, Cc) / (Rr - Cc)) in src),
        ('the page\'s words from the report are the report\'s', 'will initially be in the wrong direction', all(t in src for t in ('small, quick, and largely automatic corrections', 'will initially be in the wrong direction', 'is far less difficult than reversing only one'))),
    ]
    checks = re.search(r'(\d+) checks', open(os.path.join(HERE, 'README.md')).read())
    for what, text, also in claims: check(re.sub(r'\s+', ' ', text) in readme and also, 'the README says, as computed here (%s): "%s"' % (what, text[:80]))
    tests = int(re.search(r'(\d+) of \d+ tests pass', os.popen('/usr/bin/python3 -I %s' % os.path.join(HERE, 'test.py')).read()).group(1))
    check('(%d tests)' % tests in readme, 'the README\'s count of tests is the count that pass: %d' % tests)
    print('%d of %d checks pass' % (n - bad, n)); sys.exit(1 if bad else 0)
