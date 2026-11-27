"""Totals of the outputs for the sixteenth statement (t6_mul, t6b_liftmul).  A pair (N, s) that was run twice (once
within the small budget, once deeper) is counted once, with its deeper run.  usage: summary_mul.py"""
import glob
import os
import re

here = os.path.dirname(os.path.abspath(__file__))

rows = {}
longest = 0
for f in sorted(glob.glob(os.path.join(here, 't6_mul_*.out'))):
    for line in open(f):
        m = re.match(r'N = (\d+) s = (\d+) S = (\d+) multisets (\d+) and (\d+) patterns-P-with-a-nonempty-side (\d+) '
                     r'nonempty-on-both (\d+) DIFFERENT (\d+) .*patterns-with-a-new-divisor (\d+) kind (\S+) (\S+) \((\d+) s\)', line)
        if m:
            N, s, S, c1, c2, pats, both, diff, outside = (int(m.group(i)) for i in range(1, 10))
            longest = max(longest, int(m.group(12)))
            key = (N, s)
            if key not in rows or S > rows[key][0]:
                rows[key] = (S, c1, c2, pats, both, diff, outside, m.group(10), m.group(11))
            if diff:
                print('DIFFERENT:', line.strip())
def tot(sel):
    r = [v for k, v in rows.items() if sel(k, v)]
    return len(r), sum(v[1] for v in r), sum(v[2] for v in r), sum(v[3] for v in r), sum(v[4] for v in r), sum(v[5] for v in r), sum(v[6] for v in r)
print('CENSUS (t6_mul): pairs (N, s) %d; multisets %d on Z_N and %d on Z_Ns; sets P with a nonempty side %d (nonempty on both sides %d); '
      'P with DIFFERENT sets of sizes %d; patterns on Z_Ns with a divisor not dividing N %d; longest run %d s' % (tot(lambda k, v: True) + (longest,)))
print('   s even and not 2: pairs %d; multisets %d and %d; sets P %d (both %d); different %d; outside %d' % tot(lambda k, v: v[7] == 's-even-not-2'))
print('   s even and not 2, N not of the form p^n q: pairs %d; multisets %d and %d; sets P %d (both %d); different %d; outside %d'
      % tot(lambda k, v: v[7] == 's-even-not-2' and v[8] == 'N-not-pnq'))
print('   s = 1: pairs %d; multisets %d and %d; sets P %d (both %d); different %d; outside %d' % tot(lambda k, v: k[1] == 1))
print('   s even and not 2, odd part of N with three or more primes (N = 105, 210): pairs %d; multisets %d and %d; sets P %d (both %d); different %d; outside %d'
      % tot(lambda k, v: v[7] == 's-even-not-2' and k[0] in (105, 210, 315, 330, 420)))
print('   values of s:', sorted({k[1] for k in rows}), '; values of N:', sorted({k[0] for k in rows}))
print('   N not of the form p^n q:', sorted({k[0] for k, v in rows.items() if v[8] == 'N-not-pnq'}))
print('   (N, s): S for s even and not 2: ' + ', '.join('(%d, %d): %d' % (k[0], k[1], rows[k][0]) for k in sorted(rows) if rows[k][7] == 's-even-not-2'))

rows = {}
longest = 0
for f in sorted(glob.glob(os.path.join(here, 't6b_liftmul_*.out'))):
    for line in open(f):
        m = re.match(r'N = (\d+) s = (\d+) sizes-up-to (\d+) multisets (\d+) all-low-fails (\d+) most-lifts-tried (\d+) WITHOUT-lift (\d+) '
                     r'.*new-divisors (\d+) kind (\S+) (\S+) \((\d+) s\)', line)
        if m:
            N, s, top, mult, lf, mt, none, nd = (int(m.group(i)) for i in range(1, 9))
            longest = max(longest, int(m.group(11)))
            key = (N, s)
            if key not in rows or top > rows[key][0]:
                rows[key] = (top, mult, lf, mt, none, m.group(9), m.group(10))
            if none:
                print('WITHOUT LIFT:', line.strip())
def tot2(sel):
    r = [v for k, v in rows.items() if sel(k, v)]
    return len(r), sum(v[1] for v in r), sum(v[2] for v in r), max(v[3] for v in r), sum(v[4] for v in r)
print('LIFTS (t6b_liftmul): pairs (N, s) %d; multisets %d; "all low" fails %d; most lifts tried %d; WITHOUT a lift %d; longest run %d s'
      % (tot2(lambda k, v: True) + (longest,)))
print('   s even and not 2: pairs %d; multisets %d; "all low" fails %d; most lifts tried %d; without %d' % tot2(lambda k, v: v[5] == 's-even-not-2'))
print('   s even and not 2, N not of the form p^n q: pairs %d; multisets %d; "all low" fails %d; most lifts tried %d; without %d'
      % tot2(lambda k, v: v[5] == 's-even-not-2' and v[6] == 'N-not-pnq'))
print('   s even and not 2, odd part of N with three or more primes (N = 105, 210, 315, 330, 420): pairs %d; multisets %d; "all low" fails %d; most lifts tried %d; without %d'
      % tot2(lambda k, v: v[5] == 's-even-not-2' and k[0] in (105, 210, 315, 330, 420)))
print('   values of s:', sorted({k[1] for k in rows}), '; values of N:', sorted({k[0] for k in rows}))
print('   (N, s): largest size, for N = 30, 36, 60, 105, 210, 315, 330, 420: ' +
      ', '.join('(%d, %d): %d' % (k[0], k[1], rows[k][0]) for k in sorted(rows) if k[0] in (30, 36, 60, 105, 210, 315, 330, 420)))
