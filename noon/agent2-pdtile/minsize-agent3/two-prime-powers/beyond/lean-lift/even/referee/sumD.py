# totals of the tD_*.out files: per category and m, the number of multisets, the least share of good signings, the
# largest first-order sum; and the totals of the checks.
import re, glob
from fractions import Fraction as F
files = sorted(glob.glob(__file__.rsplit('/', 1)[0] + '/tD_*.out'))
tot = {}
agg = {}
maxb = {'even': F(0), 'odd': F(0)}
fin = 0
for f in files:
    s = open(f).read()
    if '\nOK\n' not in s or 'exit 0' not in s:
        print("NOT FINISHED:", f); continue
    fin += 1
    m = re.search(r'multisets (\d+); S1 checked (\d+) times \(of these with p odd and d/p\^i even: (\d+)\); step-down (\d+); Corollary N on (\d+) live e \(bound attained (\d+)\); live but not dangerous, no bad signing: (\d+); Proposition P (\d+)', s)
    for k, v in zip(['multisets', 'S1', 'S1_even_d', 'step-down', 'CN', 'CN_attained', 'not_dangerous', 'P'], m.groups()):
        tot[k] = tot.get(k, 0) + int(v)
    m = re.search(r'largest proof bound, 3 not\| n: even m>=4: (\S+) = .*? ; odd m: (\S+) =', s)
    maxb['even'] = max(maxb['even'], F(m.group(1))); maxb['odd'] = max(maxb['odd'], F(m.group(2)))
    for line in s.splitlines():
        m = re.match(r'  (.*?)\s+m=\s*(\d+):\s+(\d+) multisets; least share of good signings (\S+) = \S+ \(n=(\d+), (\(.*?\))\); largest first-order sum over live dangerous e>1: (\S+)', line)
        if m:
            key = (m.group(1).strip(), int(m.group(2)))
            a = agg.setdefault(key, [0, F(2), None, None, F(0)])
            a[0] += int(m.group(3))
            g = F(m.group(4))
            if g < a[1]:
                a[1], a[2], a[3] = g, int(m.group(5)), m.group(6)
            a[4] = max(a[4], F(m.group(7)))
print(fin, "files finished of", len(files))
print(tot)
print("largest proof bound (3/4 [m even >= 4] + first-order sum) when 3 does not divide n: even m: %s = %.4f; odd m: %s = %.4f" % (maxb['even'], float(maxb['even']), maxb['odd'], float(maxb['odd'])))
for (c, m), a in sorted(agg.items()):
    print("%-46s m=%2d: %8d multisets; least share good %-9s = %.4f at n=%d %s; largest first-order sum %s" % (c, m, a[0], a[1], float(a[1]), a[2], a[3], a[4]))
