# checkfacts.py -- the figures in README.md against the run files.   python -I checkfacts.py
import re, os, hashlib
here = os.path.dirname(os.path.abspath(__file__)); rd = lambda n: open(os.path.join(here, n), encoding='utf-8').read()
R = rd('README.md'); RN = re.sub(r'\s+', ' ', R); inR = lambda s: re.sub(r'\s+', ' ', s) in RN; n_ok = n_bad = 0
def ck(name, cond, extra=''):
    global n_ok, n_bad
    n_ok += bool(cond); n_bad += not cond; print(('ok    ' if cond else 'FAIL  ') + name + ((' [' + extra + ']') if extra else ''))
h = hashlib.sha256(open(os.path.join(here, 'expectations.md'), 'rb').read()).hexdigest(); s = rd('study.out')
ck('the sealed sheet has the hash posted on the board, and the trial was run on that sheet', h == rd('expectations.sha256').split()[0] == 'a6b52040cd5235324bb33458edd32015801b0f1a9b291d9cd76f2b4cc3848153' and h in s)
ck('study.out is the first and only run of the trial', s == rd('verdicts-as-first-run.out'))
ck('study.out: 8 of 8 held; worked 4 of 4, guessed 4 of 4; Brier 0.102', '8 of 8 held' in s and 'worked: 4 of 4' in s and 'guessed: 4 of 4' in s and '0.102' in s and inR('Eight of eight; worked 4 of 4, guessed 4 of 4; mean squared error of the odds 0.102') and len(re.findall(r'\| held \|', R)) == 8)
ck('lines 1, 3, 5, 6: 1,000 of 1,000 each', all(x in s for x in ['in 1000 of 1,000 (0 random curves', 'n1 - n0 in 1000 of 1,000 pairs', 'is odd in 1000 of 1,000', 'turning number in 1000 of 1,000']) and R.count('| 1,000 of 1,000 | held |') == 4)
ck('line 2: 1,000; the least 0.120; line 4: 22, median 6; line 7: 0.110; line 8: 863, greatest excess 14', all(x in s for x in ['above 0.05 in 1000 of 1,000', 'the least of all 0.1201', '22 of 1,000 pairs', 'median number of opposed places 6', 'median 0.110', 'in 863 of 1,000', 'the greatest excess 14']) and all(inR(x) for x in ['| 1,000; the least 0.120 | held |', '| 22 | held |', '| 0.110 | held |', '| 863; the greatest excess 14 | held |', 'only 22 pairs of 1,000 have no such place (the median is 6)', 'never falls below 0.120']))
m = re.search(r'counts without sign, by \|n1 - n0\|: (.*)', s).group(1); least = [int(x) for x in re.findall(r'least (\d+)', m)]; meds = [float(x) for x in re.findall(r'median ([\d.]+)', m)]
ck('line 3: the least count of opposed places is the difference itself, 0 to 6; the medians 5 to 7', least == [0, 1, 2, 3, 4, 5, 6] and min(meds) == 5 and max(meds) == 7 and inR('has a median of 5 to 7') and inR('(0, 1, ..., 6)'))
ck('the five nearest to a kink all have turning number 0', re.search(r'the five nearest to a kink .*: ((?:[\d.]+ seed \d+ n 0(?:; )?){5})$', s, re.M) is not None and inR('The five curves nearest to a kink all have turning number 0'))
a = rd('after.out')
ck('after.out: class 0, 142 curves: bare 0.120, laid 0.692; the eight and its mirror: least 0.000 half way, length nothing', 'The 142 curves of turning number 0' in a and 'by the bare formula least 0.120' in a and 'with the target laid least 0.692' in a and 'least speed 0.742, 0.225, 0.000, 0.225, 0.742' in a and 'its length half way 0.0e+0' in a and inR('among the 142 curves of class 0 from 0.120 to 0.692'))
ck('after.out: other classes never below 0.696', min(float(x) for x in re.findall(r'\|n\| = \d: least ([\d.]+)', a)) == 0.696 and inR('never falls below 0.696'))
ck('after.out: the median of line 7 goes from 0.048 to 0.235 with the size of the waves', 'waves of size 1.0: 0.048' in a and 'waves of size 2.5: 0.235' in a and inR('goes from 0.048 to 0.235'))
ck('after.out: 98 of 99 pairs within 0.002 of the moment, the farthest 0.0036', 'Of 99 pairs with kinks' in a and 'in 98; the farthest 0.0036' in a and inR('within 0.002 of that moment in 98, and within 0.004 in the other'))
t = rd('ctest.out'); ck('ctest.out: 23 pass, 0 fail', '23 pass, 0 fail' in t and inR('`ctest.js` (23 checks'))
c = rd('cmutants.out'); c1 = rd('cmutants-round1.out'); b = rd('beside.out')
ck('cmutants: a control, then 18 of 20; round 1: 16 of 20; the two that pass differ on 0 of 400 curves', 'control: the true ccore.js, run in the same way: 23 pass, 0 fail' in c and '18 of 20 broken copies caught' in c and '16 of 20 broken copies caught' in c1 and b.count('0 of 400 curves') == 2 and sorted(l.split()[0] for l in c.split('\n') if 'NOT caught' in l) == ['lay-mirror-always', 'wrap-half-open'] and inR('**Eighteen of twenty are caught.**') and inR('sixteen of twenty caught'))
pt = rd('page-test.out'); ck('page test: 54 assertions, 0 failed; drawn curves -1, 0, -2', 'PAGE TEST: 54 assertions, 0 failed' in pt and 'errors on the page: none' in pt and 'a loop -1, a figure of eight 0, a loop within a loop -2' in pt and inR('54 assertions') and inR('−1, 0, −2'))
pm = rd('page-mutants.out'); mm = re.search(r'(\d+) of 18 broken copies of the page caught', pm)
ck('page-mutants.out: a control that passes, then as many of eighteen as the README says', 'control: the true page, built and run in the same way: 54 assertions, 0 failed' in pm and '15 of 18 broken copies of the page caught' in rd('page-mutants-round1.out') and '17 of 18 broken copies of the page caught' in rd('page-mutants-round2.out') and inR('after runs that caught fifteen and then seventeen') and mm is not None and inR({'18': 'all eighteen are caught', '17': 'seventeen are caught'}.get(mm.group(1), 'XX')), mm.group(0) if mm else 'not finished')
ck('quotes.out: 6 of 6', '6 of 6 quotations found' in rd('quotes.out') and inR('six quotations'))
ck('no placeholder left in the README', 'PAGE-MUTANTS' not in R)
print('\n%d pass, %d fail' % (n_ok, n_bad))
