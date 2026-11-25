# verdicts.py -- score the nine sealed lines of expectations.md from the run files.   python -I verdicts.py
import re, hashlib, os
here = os.path.dirname(os.path.abspath(__file__)); rd = lambda n: open(os.path.join(here, n)).read()
print('sha256 of expectations.md:', hashlib.sha256(rd('expectations.md').encode()).hexdigest())
print('posted on the board      :', rd('expectations.sha256').split()[0], '\n')
out = []
def line(n, text, odds, kind, held, saw): out.append((n, text, odds, kind, held, saw))
m = {}
for fn in ['runM-3-4.out', 'runM-5.out', 'runM-6.out']:
    for a, e, secs in re.findall(r'M\((\S+)\) = 2\^-(\d+) .*?, ([\d.]+) s', rd(fn)): m[a] = (int(e), float(secs))
for n, (arg, want, odds, limit) in enumerate([('11/4', 112, 0.88, None), ('23/8', 503, 0.88, None), ('47/16', 2786, 0.8, 600), ('95/32', 18443, 0.6, 1200)], 1):
    got = m.get(arg); held = got is not None and got[0] == want and (limit is None or got[1] <= limit)
    line(n, 'M(%s) = 2^-%d' % (arg, want) + ('' if limit is None else ', computed within %d minutes' % (limit // 60)), odds, 'worked', held, 'not run' if got is None else '2^-%d in %.1f s' % got)
g = rd('grid12.out'); g16 = rd('grid16.out')
pts = int(re.search(r'grid of 1/4096 in \[0, 9/4\]: (\d+) points', g).group(1)); assert pts == 9217
first = re.search(r'first point where Succ != TameSucc: (\S+)', g).group(1)
line(5, 'going up the grid of 1/4096 from 0, the first point where the general and the tame successor differ is 33/16', 0.85, 'guessed', first == '33/16', 'first difference at ' + first)
n16 = int(re.search(r'grid of 1/65536 in \[0, 33/16\): (\d+) points', g16).group(1)); d16 = int(re.search(r'points where Succ != TameSucc: (\d+)', g16).group(1))
line(6, 'on the grid of 1/65536 no point below 33/16 where they differ', 0.7, 'guessed', d16 == 0 and n16 == 135168, '%d of %d points differ' % (d16, n16))
mb = int(re.search(r'points where MeekSucc \(my reading\) != Succ: (\d+)', g).group(1))
line(7, 'the sixth algorithm as I read it gives the general successor at every point of the grid of 1/4096 in [0, 9/4]', 0.88, 'guessed', mb == 0, '%d of %d points differ' % (mb, pts))
d768, n768 = map(int, re.search(r'(\d+) of the (\d+) in \[33/16, 9/4\)', g).groups())
line(8, 'on the grid of 1/4096 in [33/16, 9/4) they differ at more than a tenth of the 768 points', 0.5, 'guessed', n768 == 768 and d768 > 76.8, '%d of %d differ' % (d768, n768))
mx = int(re.search(r'largest denominator of a successor: 2\^(\d+)', g).group(1)); at = re.search(r'largest denominator of a successor: 2\^\d+ at r = (\S+)', g).group(1)
line(9, 'no successor of a point of the grid of 1/4096 in [0, 9/4] has a denominator above 2^40', 0.8, 'guessed', mx <= 40, 'the largest is 2^%d, at r = %s' % (mx, at))
h = 0; b = 0.0
for n, text, odds, kind, held, saw in out:
    print('%d. %-5s (%s, odds %.2f)  %s\n      saw: %s' % (n, 'HELD' if held else 'FELL', kind, odds, text, saw)); h += held; b += (odds - (1 if held else 0)) ** 2
print('\n%d of %d held; mean squared error of the odds (Brier) %.3f; by kind: worked %d of %d, guessed %d of %d' % (h, len(out), b / len(out),
      sum(o[4] for o in out if o[3] == 'worked'), sum(1 for o in out if o[3] == 'worked'), sum(o[4] for o in out if o[3] == 'guessed'), sum(1 for o in out if o[3] == 'guessed')))
