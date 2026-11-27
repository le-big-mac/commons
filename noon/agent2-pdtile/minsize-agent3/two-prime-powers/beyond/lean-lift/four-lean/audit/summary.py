"""Totals of the outputs of the audit, for the report.  usage: summary.py (run in the audit folder)"""
import glob
import os
import re
import sys
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import core

here = os.path.dirname(os.path.abspath(__file__))

# ---- t1: the parts ----
tot = Counter()
fam = 0
viol = 0
files = sorted(glob.glob(os.path.join(here, 't1_parts_s*.out')))
sizes = Counter()
for f in files:
    for line in open(f):
        m = re.match(r'seed (\d+) families (\d+) sizes (\{.*\})', line)
        if m:
            fam += int(m.group(2))
            for k, v in eval(m.group(3)).items():
                sizes[k] += v
            continue
        m = re.match(r'\s+VIOLATIONS (\d+)', line)
        if m:
            viol += int(m.group(1))
            continue
        m = re.match(r'\s+(.*?)\s+(\d+)$', line)
        if m:
            tot[m.group(1)] += int(m.group(2))
print('PARTS (t1_parts): %d runs, %d families, sizes %s, violations %d' % (len(files), fam, dict(sorted(sizes.items())), viol))
for k in sorted(tot):
    print('   %-62s %d' % (k, tot[k]))

# ---- t3: A1 ----
def read_t3(pattern, key):
    rows = []
    for f in sorted(glob.glob(os.path.join(here, pattern))):
        for line in open(f):
            w = line.split()
            if len(w) > 14 and w[0] == key:
                rows.append((int(w[2]), int(w[5]), int(w[7]), int(w[9]), int(w[11]), int(w[13])))
    return rows

rows = read_t3('t3_a1_*.out', 'n')
odd = [r for r in rows if r[0] % 2 == 1]
even = [r for r in rows if r[0] % 2 == 0]
print('A1 / exists_signs_odd (t3_a1): odd moduli %d (%s), multisets %d, "all +" fails %d, most signings tried %d, WITHOUT a good signing %d'
      % (len({r[0] for r in odd}), ' '.join(str(x) for x in sorted({r[0] for r in odd})), sum(r[2] for r in odd),
         sum(r[3] for r in odd), max(r[4] for r in odd), sum(r[5] for r in odd)))
by = {}
for r in odd:
    by.setdefault(r[0], []).append(r)
print('   largest size m for each n: ' + ', '.join('%d: %d' % (n, max(r[1] for r in by[n])) for n in sorted(by)))
three = [r for r in odd if len(core.factor(r[0])) >= 3]
print('   moduli with three or more primes: %s; multisets %d, "all +" fails %d, without %d'
      % (sorted({r[0] for r in three}), sum(r[2] for r in three), sum(r[3] for r in three), sum(r[5] for r in three)))
evenm = [r for r in odd if r[1] % 2 == 0 and r[1] >= 12]
print('   even sizes m >= 12 (n, m): %s; multisets %d' % (sorted({(r[0], r[1]) for r in evenm}), sum(r[2] for r in evenm)))
print('   control, even moduli %s: multisets %d, WITHOUT a good signing %d (by modulus: %s)'
      % (sorted({r[0] for r in even}), sum(r[2] for r in even), sum(r[5] for r in even),
         ', '.join('%d: %d' % (n, sum(r[5] for r in even if r[0] == n)) for n in sorted({r[0] for r in even}))))

# ---- t4: lifts ----
rows = read_t3('t4_lift_*.out', 'N')
print('exists_lift_two_all (t4_lift): %d values of N, multisets %d, "all low" fails %d, most lifts tried %d, WITHOUT a lift %d'
      % (len({r[0] for r in rows}), sum(r[2] for r in rows), sum(r[3] for r in rows), max(r[4] for r in rows), sum(r[5] for r in rows)))
by = {}
for r in rows:
    by.setdefault(r[0], []).append(r)
print('   largest size m for each N: ' + ', '.join('%d: %d' % (n, max(r[1] for r in by[n])) for n in sorted(by)))
def oddpart(n):
    while n % 2 == 0:
        n //= 2
    return n
three = [r for r in rows if len(core.factor(oddpart(r[0]))) >= 3]
print('   N whose odd part has three or more primes: %s; multisets %d, "all low" fails %d, without %d'
      % (sorted({r[0] for r in three}), sum(r[2] for r in three), sum(r[3] for r in three), sum(r[5] for r in three)))
pow2 = [r for r in rows if oddpart(r[0]) == 1]
print('   N a power of 2: %s; multisets %d, "all low" fails %d, without %d'
      % (sorted({r[0] for r in pow2}), sum(r[2] for r in pow2), sum(r[3] for r in pow2), sum(r[5] for r in pow2)))

# ---- t4b: sizes ----
pairs = 0; pats = 0; diff = 0; cN = 0; c2N = 0; outside = 0
Ns = []
for f in sorted(glob.glob(os.path.join(here, 't4b_sizes_*.out'))):
    for line in open(f):
        m = re.match(r'N = (\d+) S = (\d+) multisets (\d+) on Z_N and (\d+) on Z_2N; patterns P .*?: (\d+); DIFFERENT sets of sizes: (\d+) .*not dividing N: (\d+)', line)
        if m:
            pairs += 1; Ns.append((int(m.group(1)), int(m.group(2))))
            cN += int(m.group(3)); c2N += int(m.group(4)); pats += int(m.group(5)); diff += int(m.group(6)); outside += int(m.group(7))
print('sizes_eq_two_all (t4b_sizes): %d pairs (Z_N, Z_2N), multisets %d + %d, sets P with a nonempty side %d, P with DIFFERENT sets of sizes %d; '
      'patterns on Z_2N with a divisor not dividing N %d' % (pairs, cN, c2N, pats, diff, outside))
print('   (N, S): ' + ', '.join('%d: %d' % x for x in Ns))

# ---- t5: assembly ----
tot = Counter(); viol = 0; nf = 0
for f in sorted(glob.glob(os.path.join(here, 't5_fit_s*.out'))):
    for line in open(f):
        m = re.match(r'\s+VIOLATIONS (\d+)', line)
        if m:
            viol += int(m.group(1)); continue
        m = re.match(r'\s+(.*?)\s+(\d+)$', line)
        if m:
            if 'largest' in m.group(1):
                tot[m.group(1)] = max(tot[m.group(1)], int(m.group(2)))
            else:
                tot[m.group(1)] += int(m.group(2))
print('ASSEMBLY (t5_fit): violations %d' % viol)
for k in sorted(tot):
    print('   %-55s %d' % (k, tot[k]))
