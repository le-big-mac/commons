# checkfacts.py -- the figures in README.md against the run files, each read again or recomputed here.  python -I checkfacts.py
import re, os, json, hashlib, math
here = os.path.dirname(os.path.abspath(__file__)); rd = lambda n: open(os.path.join(here, n), encoding='utf-8').read()
R = rd('README.md'); n_ok = n_bad = 0
def ck(name, cond, extra=''):
    global n_ok, n_bad
    n_ok += bool(cond); n_bad += not cond; print(('ok    ' if cond else 'FAIL  ') + name + ((' [' + extra + ']') if extra else ''))
inR = lambda s: s in R; num = lambda x: format(x, ',')
ck('the sealed sheet has the hash posted on the board', hashlib.sha256(rd('expectations.md').encode()).hexdigest() == rd('expectations.sha256').split()[0] == '454f951238463b99ef8e2893dcab23ac6116a3372001bf2fa13bb5480d6bcc9a')
v = rd('verdicts.out'); ck('verdicts.out: 10 of 12 held; read 8 of 8, worked 0 of 1, guessed 2 of 3; Brier 0.123', '10 of 12 held' in v and 'read 8 of 8, worked 0 of 1, guessed 2 of 3' in v and '0.123' in v and inR('Ten of twelve; read 8 of 8, worked 0 of 1, guessed 2 of 3; mean squared error of the odds 0.123'))
ck('ten HELD and two FELL lines; the README table has ten "held" and two "fell" rows', len(re.findall(r'^ ?\d+\. HELD', v, re.M)) == 10 and len(re.findall(r'^ ?\d+\. FELL', v, re.M)) == 2 and len(re.findall(r'\| held \|', R)) == 10 and len(re.findall(r'\| \*\*fell\*\* \|', R)) == 2)
c = rd('classify.out'); rows = [('bugeye', '(−1, 2, 2, 3)', ''), ('strip', '(0, 0, 1, 1)', ''), ('m3_5_8_8', '(−3, 5, 8, 8)', 'n², 6n²'), ('m3_4_12_13', '(−3, 4, 12, 13)', '2n², 6n²'), ('m2_3_6_7', '(−2, 3, 6, 7)', '2n²'), ('m4_5_20_21', '(−4, 5, 20, 21)', '2n², 3n²')]
tot = 0; fives = []; threes = []
for name, shown, fam in rows:
    log = rd('missing/%s.log' % name); m = re.search(r'curvatures up to 100000000: (\d+) circles, \d+ different curvatures, deepest word \d+, ([\d.]+) s', log)
    k = re.search(r'^%s .*?missing (\d+); in the families .*?of which present as curvatures: (\d+).*?; sporadic (\d+), the largest (\d+)' % re.escape(name), c, re.M)
    miss, present, spor, largest = map(int, k.groups()); tot += spor
    listed = len(rd('missing/%s.txt' % name).split()); row = '| %s | %s | %s | %s | %s | %s | %s s |' % (shown, num(int(m.group(1))), num(miss), ('%s (%s)' % (num(miss - spor), fam)) if fam else 'none', num(spor), num(largest), m.group(2))
    ck('the runs table, %s: the README row is the files\' (and the list has %d numbers, none of the family present)' % (shown, listed), inR(row) and listed == miss and present == 0, row)
    t = re.search(r'^%s .*\n.*\n   of its 100 largest sporadic: multiples of 5: (\d+), of 13: \d+, of 11: \d+, of 7: \d+, of 17: \d+, of 3: (\d+)' % re.escape(name), c, re.M)
    if t: fives.append(int(t.group(1))); threes.append(int(t.group(2)))
ck('In short 1: the six counts and largest members', inR('61, 215, 676, 731, 236 and 3,659, the largest of them 97,287,\n   1,199,820, 3,122,880, 7,354,464, 429,039 and 32,084,460'))
ck('fives among the 100 largest sporadic of five gaskets: %s; threes: %s to %s' % (fives, min(threes), max(threes)), fives == [47, 38, 48, 51, 54] and inR('47, 38, 48, 51 and 54') and inR('%d to %d are\n  multiples of 3' % (min(threes), max(threes))) and inR('Between 38 and 54 of 100'))
p = re.search(r'pooled \(500 numbers\): multiples of 13: (\d+), of 11: (\d+)', c); ck('pooled: 76 multiples of 13, 35 of 11; chance about 38 and 45', p.groups() == ('76', '35') and round(500 / 13) == 38 and round(500 / 11) == 45 and inR('76 and 35 of 500, where chance would give about 38 and 45'))
cm = rd('compare.out'); ck('compare.out: all six lists the same as the authors\'; %s numbers in all' % num(tot), 'all six the same: True' in cm and cm.count('the same, number for number') == 6 and tot == 5578 and inR('5,578 numbers'))
t = rd('types.out'); m = re.search(r'residues as the type: (\d+) of 42; chi_2 as the type: (\d+) of 42; of the (\d+) packings whose type allows a fourth-power form, a witness below 10\^6 and nothing forbidden: (\d+)', t)
ck('types.out: residues 42 of 42; chi_2 by positive pairs 41 of 42; witnesses 9 of 9; 0 of 267 in each of the three', m.groups() == ('42', '41', '9', '9') and t.count('admissible numbers of the four forms: 267; occurring as curvatures: 0') == 3 and inR('| 41 of 42 |') and inR('9 of 9; 0 of 267 in each of the three'))
ck('the one packing without a positive coprime pair is (-11, 21, 24, 28), and with the outer circle its sign is the type\'s', re.search(r'\(-11, 21, 24, 28\).*?positive coprime pairs of the root: \[\] NOT the type \(with a negative partner allowed: \[-1\]\)', t) is not None and all(math.gcd(a, b) > 1 for a, b in [(21, 24), (21, 28), (24, 28)]) and inR('(−11, 21, 24, 28) has no such pair'))
ck('ratios of my bound to the largest sporadic: 3.1 and 13.6', round(1e8 / 32084460, 1) == 3.1 and round(1e8 / 7354464, 1) == 13.6 and inR('3.1 times it for\n(−4, 5, 20, 21) and 13.6 times for (−3, 4, 12, 13)'))
ck('the bug-eye run took 721.4 s, four and a half times the 160 s I had reckoned', round(721.4 / 160, 1) == 4.5 and inR('721.4 s for the bug-eye') and '0.4 s' in rd('expectations.md'))
g = rd('gtest.out'); gp, gf = map(int, re.search(r'(\d+) pass, (\d+) fail', g).groups())
ck('gtest.out: %d pass, %d fail' % (gp, gf), gf == 0 and inR('`gtest.js` (%d checks' % gp) and inR('%d checks pass' % gp) and gp == 17)
ck('gtest: 20,000 Kronecker cases; 156 of 156; 48 of 48; 1,680 walks; 1,208,115 numbers; 55 roots; 420 rectangles; 100 deep views in at most 4,978 gaps', all(x in g for x in ['20000 of 20000', '156 of 156', '48 of 48', '1680 of 1680', '(1208115 numbers in all): 42 of 42', '55 in all), four different circles, each pair touching: 55 of 55', '420 of 420', 'in at most 4978 gaps visited: 100 of 100', 'gaps visited): 120 of 120', 'K=30000000: curvature 9.00e+14', 'is shown: 9 of 9']) and all(inR(x) for x in ['20,000 cases', '156 cases of 156', '48 of 48', '1,680 random walks', '1,208,115 numbers', '55 root quadruples', '420 random rectangles', 'at most 4,978 gaps visited', '120 views against the first, plain form', 'nine rows of circles, to the 30,000,000th', 'curvature 9 × 10^14']))
ar = re.search(r'\[-1,2,2,3\] ([\d.]+); \[-3,5,8,8\] ([\d.]+); \[-6,11,14,15\] ([\d.]+); \[-11,21,24,28\] ([\d.]+); \[-23,48,49,52\] ([\d.]+); strip ([\d.]+)', g); a5 = [float(x) for x in ar.groups()[:5]]
ck('areas: %.1f%% to %.1f%% in five gaskets, %.1f%% of a period of the strip' % (100 * min(a5), 100 * max(a5), 100 * float(ar.group(6))), inR('cover %.1f%% to %.1f%% of the outer circle in five gaskets and %.1f%% of a' % (100 * min(a5), 100 * max(a5), 100 * float(ar.group(6)))))
dwm = re.search(r'a walk down to curvature ([\d.]+)e\+(\d+)', g); dw = '%.1f × 10^%s' % (float(dwm.group(1)), dwm.group(2)); ck('gtest: a walk down to curvature ' + dw, inR('- a walk down to curvature %s keeps' % dw) and inR('down to a curvature of %s checking' % dw))
mu = rd('mutants.out'); mc = re.search(r'(\d+) of (\d+) broken copies caught', mu); nc = sorted(re.findall(r'^(\S+) .* NOT caught', mu, re.M))
ck('mutants.out: 23 of 23 caught', mc.groups() == ('23', '23') and nc == [] and inR('**Twenty-three of twenty-three copies are caught.**') and inR('all twenty-three\n   deliberately broken copies'))
b = rd('beside.out'); ck('beside.out: 164 root quadruples, 6,724 views, no difference; the rule met 0 times on walks from the root', b.count('164 root quadruples; place() differs for 0; of 6724 views (394595 circles shown) the lists differ in 0') == 1 and b.count('was met 0 times') == 1 and inR('on 164 gaskets and 6,724 views') and inR('that rule was met 0 times in those 6,724 views'))
pt = rd('page-test.out'); ck('page test: seven gaskets with the same list as gcore.js; 24 of 24 deep views, curvature up to 1.36e13, 18,238 circles, no square; 36, 144, 1,296; no error', pt.count('the same list from gcore.js here: true') == 7 and 'the same list as gcore.js here in 24 of 24; 18238 circles drawn in all, 0 of them squares' in pt and '1.36e+13' in pt and '(36, 144, 1296); twice a square: 0' in pt and 'errors on the page: none' in pt and all(inR(x) for x in ['1.36 × 10^13', '18,238 circles', '36, 144 and 1,296']))
tc = re.findall(r'where circles \S+ and \S+ touch:(.*)', pt); tms = [int(x) for l in tc for x in re.findall(r'(\d+) ms;', l)]
ck('page test: four points of contact, four magnifications each, all the same as gcore.js, at most %d ms' % max(tms), len(tc) == 4 and len(tms) == 16 and sum(l.count('same as here true') for l in tc) == 16 and max(tms) < 100 and inR('four points where two\ncircles touch, each at four magnifications'))
ck('page test: six charts with the right number of ticks; nine inputs to the third panel', pt.count('expected: true') == 6 and len(re.findall(r"^(-6, 11, 14, 15|15 2 2 3|1, 2, 3, 4|-2, 4, 4, 6|-8, 12, 25, 25|-4, 8, 9, 9|0 0 1 1|-16, 32, 33, 41|x) -> ", pt, re.M)) == 9 and inR('nine inputs to the third panel'))
ck('quotes.out: 35 of 35', '35 of 35 quotations found' in rd('quotes.out') and inR('35 quoted pieces'))
ck('the page allows magnification up to 10^11', 's > lim * 1e11' in rd('page.src.html') and inR('magnification up to 10^11'))
d = json.loads(rd('data.json')); ck('data.json: six gaskets, the sporadic counts of the table, bound 10^8', [len(x['sporadic']) for x in d] == [61, 215, 676, 731, 236, 3659] and all(x['N'] == 10**8 for x in d))
ck('no placeholder left in the README', not re.search(r'REFEREE-LINE|REFEREE-SECTION', R))
print('\n%d pass, %d fail' % (n_ok, n_bad))
