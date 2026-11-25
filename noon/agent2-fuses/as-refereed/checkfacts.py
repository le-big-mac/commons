# checkfacts.py -- the figures in README.md against the run files, each recomputed or read again here.  python -I checkfacts.py
import re, os, json, hashlib
from fractions import Fraction
here = os.path.dirname(os.path.abspath(__file__)); rd = lambda n: open(os.path.join(here, n), encoding='utf-8').read()
R = rd('README.md'); n_ok = 0; n_bad = 0
def ck(name, cond, extra=''):
    global n_ok, n_bad
    if cond: n_ok += 1
    else: n_bad += 1
    print(('ok    ' if cond else 'FAIL  ') + name + ((' [' + extra + ']') if extra else ''))
def inR(s): return s in R
num = lambda x: format(x, ',')
# the sealed sheet
h = hashlib.sha256(rd('expectations.md').encode()).hexdigest()
ck('the sealed sheet has the hash posted on the board', h == rd('expectations.sha256').split()[0] == 'dbefdd2fb740326a18a1b23eb7f4b59c5b4b21259f127dc0e527d726c4868f03')
v = rd('verdicts.out'); ck('verdicts.out: 9 of 9 held, worked 4 of 4, guessed 5 of 5, Brier 0.072; README says so', '9 of 9 held' in v and 'worked 4 of 4, guessed 5 of 5' in v and '0.072' in v and inR('Nine of nine; worked 4 of 4, guessed 5 of 5; mean squared error of the odds 0.072'))
ck('nine HELD lines in verdicts.out and nine "held" rows in the README table', len(re.findall(r'^\d\. HELD', v, re.M)) == 9 and len(re.findall(r'\| held \|', R)) == 9)
# the paper's formula, recomputed here
def d(n):
    c = [2]
    for k in range(1, n): c.append(1 + (k + 1) * c[-1])
    return n + 9 + sum((k + 3) * c[k] for k in range(1, n))
ds = [d(n) for n in range(1, 9)]
ck('the formula d(w^w^n), n = 1..8, recomputed: 10, 31, 112, 503, 2786, 18443, 141744, 1237755', ds == [10, 31, 112, 503, 2786, 18443, 141744, 1237755], str(ds))
ck('the formula at n = 11 is 1541023936 (the 2012 table\'s entry for n = 10; the paper states it plus one for 3)', d(11) == 1541023936 and inR('1,541,023,936'))
m = {}
for fn in ['runM-3-4.out', 'runM-5.out', 'runM-6.out', 'runM-7.out', 'runM-8.out']:
    for a, e, args, deep, secs in re.findall(r'M\((\S+)\) = 2\^-(\d+)   = the formula.*?;  (\d+) different arguments, calls nested (\d+) deep, ([\d.]+) s', rd(fn)): m[a] = (int(e), int(args), int(deep), float(secs))
ck('M at 11/4, 23/8, 47/16, 95/32, 191/64, 383/128 in the run files = the formula for n = 3..8', [m[a][0] for a in ['11/4', '23/8', '47/16', '95/32', '191/64', '383/128']] == ds[2:])
ck('README table row of -log2 M(3 - 2^-n), n = 1..7', inR('| −log₂ M(3 − 2⁻ⁿ) | 31 | 112 | 503 | 2,786 | 18,443 | 141,744 | 1,237,755 |') and ds[1:] == [31, 112, 503, 2786, 18443, 141744, 1237755])
ck('M(47/16) in 0.1 s and M(95/32) in 0.3 s', m['47/16'][3] == 0.1 and m['95/32'][3] == 0.3 and inR('2⁻²⁷⁸⁶ in 0.1 s') and inR('2⁻¹⁸⁴⁴³ in 0.3 s'))
ck('M(383/128): %.1f s, %s arguments, nested %s deep' % (m['383/128'][3], num(m['383/128'][1]), num(m['383/128'][2])), inR('took %.1f seconds: %s different arguments, calls nested %s deep' % (m['383/128'][3], num(m['383/128'][1]), num(m['383/128'][2]))))
# the grids
g = rd('grid12.out'); g16 = rd('grid16.out')
pts, secs = re.search(r'grid of 1/4096 in \[0, 9/4\]: (\d+) points, ([\d.]+) s', g).groups()
ck('grid of 1/4096: 9,217 points, first difference at 33/16, 768 of 768, meek differs at 0, largest denominator 2^40 at 9215/4096', pts == '9217' and 'first point where Succ != TameSucc: 33/16' in g and '768 of the 768 in [33/16, 9/4)' in g and 'points where MeekSucc (my reading) != Succ: 0' in g and 'largest denominator of a successor: 2^40 at r = 9215/4096' in g and inR('9,217') and inR('768 of 768 differ') and inR('the largest is 2⁴⁰, at 9215/4096'))
p16, s16 = re.search(r'grid of 1/65536 in \[0, 33/16\): (\d+) points, ([\d.]+) s', g16).groups()
ck('grid of 1/65536: 135,168 points, 0 differ', p16 == '135168' and 'points where Succ != TameSucc: 0' in g16 and inR('0 of 135,168 points differ'))
ck('the two grid runs took %s s and %s s' % (num(float(secs)), s16), inR('took %s s and %s s' % (num(float(secs)), s16)))
# the proved procedure at single numbers
rows = re.findall(r'above (\S+) is \S+; the gap is 2\^-(\d+);\s+([\d.]+) s, (\d+) computed.*?\nthe meek rule gives the gap 2\^-(\d+), the tame rule 2\^-(\d+)', rd('succ-three.out') + rd('succ-5-2.out'))
SUP = str.maketrans('0123456789-', '⁰¹²³⁴⁵⁶⁷⁸⁹⁻'); sup = lambda e: '2' + ('-' + str(e)).translate(SUP)
want = ''.join('| %s | %s | %s | %s | %s s | %s |\n' % (r, sup(a), sup(b), sup(c), num(float(t))if float(t) >= 1000 else t, num(int(k))) for r, a, t, k, b, c in rows)
ck('the table of the proved procedure at 9/4, 19/8, 39/16, 5/2 is the run files\' (four rows; proved = meek in each)', len(rows) == 4 and want in R and all(a == b for r, a, t, k, b, c in rows), want.replace('\n', ' '))
ck('5/2: 2^-51 in 1,009.5 s', rows[3][0] == '5/2' and rows[3][1] == '51' and rows[3][2] == '1009.5' and inR('run at 5/2 for 1,009.5 seconds, gives 2⁻⁵¹'))
mk = rd('meek-check.out'); ck('meek rule: 51 at 5/2 and 48804 at 11/4; the 9,217 points', 'meekM(5/2) = 2^-51' in mk and 'meekM(11/4) = 2^-48804' in mk and '9217 of 9217' in mk and inR('51 at 5/2\n  and 48,804 at 11/4'))
# the tests
t = rd('test.out'); tp, tf = map(int, re.search(r'(\d+) pass, (\d+) fail', t).groups())
ck('test.out: %d pass, %d fail; README says %d checks' % (tp, tf, tp), tf == 0 and inR('`test.js` (%d checks, all pass' % tp))
ck('4,000 random pairs', '4000 of 4000' in t and inR('4,000 random pairs'))
ck('5,086 numbers in the sample', t.count('5086 of 5086') >= 6 and inR('5,086 numbers'))
ck('sieve: 5,506 made, the same 5,506 called fusible, of 35,840 grid points; 31,512 on the grid and equal, 47 where tame differs', '(5506 made): 5506 of 5506' in t and '(5506 called fusible): 5506 of 5506' in t and '31512 of 31512' in t and '(47 of these' in t and 35 * 16384 // 16 == 35840 and inR('5,506 numbers') and inR('of 35,840') and inR('31,512 points') and inR('(47\n  of them'))
ck('recipes: 1,746 of 8,960 grid points', '(1746), one for every meek successor' in t and '8960 of 8960' in t and inR('1,746 of 8,960'))
ck('the certificate compared at 6,000 random places (two tests of 3,000)', t.count('3000 of 3000') == 2 and inR('at 6,000 random places'))
ck('the two memories compared at 4,980 numbers', t.count('4980 of 4980') >= 2 and inR('compare the two memories at 4,980 more'))
sixteen = len(re.findall(r'^ok    (ENX|Xu|NS)', t, re.M)); ck('checks of what the sources state: %d' % sixteen, sixteen == 15 and inR('fifteen things the sources state'))
gc = rd('gaps-check.out'); a, b = re.search(r'gap memory (\d+) ms .*?plain memory (\d+) ms', gc).groups()
ck('gap memory %.1f s against %.1f s at 901 points' % (int(b) / 1000, int(a) / 1000), '901 of 901' in gc and inR('from %.1f s to %.1f s with the same answers at all 901 points' % (int(b) / 1000, int(a) / 1000)))
w = rd('where-min.out'); ck('where the answer is found: 71,737 computations, 67,908 first pass, 3,829 later, the eleventh at the latest, never further than 1/8', '71737 computations' in w and 'first pass in 67908, at a later pass in 3829' in w and '"11":1}' in w and '= 0.125000' in w and inR('71,737 computations') and inR('67,908 times') and inR('3,829 times'))
w2 = rd('where-min-39-16.out'); ck('the same in the run at 39/16: 18,896 computations, never further than 1/8', '18896 computations' in w2 and '= 0.125000' in w2 and inR('18,896 computations'))
mu = rd('mutants.out'); mc = re.search(r'(\d+) of (\d+) broken copies caught', mu)
ck('mutants.out: %s; README names the count' % (mc.group(0) if mc else 'NOT FINISHED'), bool(mc) and mc.group(1) == '14' and mc.group(2) == '19' and inR('Fourteen of the nineteen are caught: eight by failing checks, four because the program\nstops with an error, and two because the tests do not finish') and (len(re.findall('tests fail', mu)), len(re.findall('stops with an error', mu)), len(re.findall('do not finish', mu)), len(re.findall('NOT caught', mu))) == (8, 4, 2, 5))
# the page
pt = rd('page-test.out'); times = [float(x) for x in re.findall(r'drawn in ([\d.]+) s', pt)]
ck('page test: eight views, 1,000 of 1,000 columns each, no error, slowest %.1f s' % max(times), pt.count('1000 of 1000 columns the same') == 8 and 'errors on the page: none' in pt and inR('The slowest view took %.1f s' % max(times)))
ck('the wild number on the bench: 13 fuses', 'with 13 fuses' in pt and inR('with 13 fuses'))
q = rd('quotes.out'); ck('quotes.out: 43 of 43', '43 of 43 quotations found' in q and inR('43 quoted pieces'))
pal = rd('palette.out'); ck('palette: all checks pass, worst pair 26.8', 'ALL CHECKS PASS' in pal and 'ΔE 26.8 (protan)' in pal and inR('26.8 apart'))
land = json.loads(rd('landmarks.json')); L = {r['r']: r for r in land}
ck('landmarks.json: tame 31, meek 51 at 5/2; tame 112, meek 48804 at 11/4; tame 503 at 23/8; tame 11, meek 12, proved 12 at 33/16', (L['5/2']['tame'], L['5/2']['meek'], L['11/4']['tame'], L['11/4']['meek'], L['23/8']['tame'], L['33/16']['tame'], L['33/16']['meek'], L['33/16']['proved']) == (31, 51, 112, 48804, 503, 11, 12, 12))
import math
ck('the page\'s "about 10^-14,688 seconds" at 11/4 and "10^-463,894,426" at 3', math.floor(math.log10(3600) - 48804 * math.log10(2)) == -14688 and math.floor(Fraction(math.log10(3600)) - 1541023937 * Fraction(math.log10(2))) == -463894426, '%d' % math.floor(Fraction(math.log10(3600)) - 1541023937 * Fraction(math.log10(2))))
ck('8449/4096 = 19/16 ~ 3969/2048 and lies between 33/16 and 4225/2048', (Fraction(19, 16) + Fraction(3969, 2048) + 1) / 2 == Fraction(8449, 4096) and Fraction(33, 16) < Fraction(8449, 4096) < Fraction(4225, 2048))
ck('as printed, the sixth procedure at 1/2: the second call\'s argument is 1 - 0 - 1 - 1 + 1/2 = -1/2, and 0 ~ 0 = 1/2', 2 * Fraction(1, 2) - 0 - 1 - 1 + Fraction(1, 2) == Fraction(-1, 2) and (0 + 0 + 1) / 2 == 0.5)
og = rd('offgrid.out'); ck('off the grid: 4,000 of 4,000 random (145 wild), 35,840 of 35,840 (2,048 wild); as printed 128 of 512 right, 384 stopped, first bad 1/2', 'the first at 4000 of 4000 (145 of them' in og and 'the same at 35840 of 35840 (2048 where' in og and 'true successor at 128, another number at 0' in og and 'input at 384; the first point that is not right: 1/2' in og and inR('4,000 of 4,000 random') and inR('(145 of them') and inR('(2,048 such)') and inR('128 of the 512 points') and inR('other 384'))
gf = rd('grid12-final.out'); g16f = rd('grid16-final.out'); s5f = rd('succ-5-2-final.out'); strip = lambda x: re.sub(r'[\d.]+ s$|^calls:.*$|^  \.\..*\n| that were run', '', x, flags=re.M)
tf1 = re.search(r'points, ([\d.]+) s', gf).group(1); tf2 = re.search(r'points, ([\d.]+) s', g16f).group(1); tf3 = re.search(r';\s+([\d.]+) s, 260928 computed', s5f).group(1)
ck('the reruns give the same lines as the sealed runs, times apart; times %s, %s, %s s' % (tf1, tf2, tf3), strip(g) == strip(gf) and strip(g16) == strip(g16f) and 'the gap is 2^-51' in s5f and inR('%s s and %s s for the two grids and %s s at 5/2' % (num(float(tf1)), tf2, num(float(tf3)))))
mf = re.findall(r'M\((\S+)\) = 2\^-(\d+)   = the formula', rd('runM-final.out')); ck('runM-final.out: n = 3..8 the formula\'s figures', [int(e) for a, e in mf] == ds[2:])
ck('core.js is the file the reruns were made with', hashlib.md5(open(os.path.join(here, 'core.js'), 'rb').read()).hexdigest() == rd('core-at-final-runs.md5').split()[0])
ck('no placeholder left in the README', not re.search(r'[A-Z]+-LINE|MUTANTS-PARAGRAPH|REFEREE-SECTION|RERUN-LINE', R))
print('\n%d pass, %d fail' % (n_ok, n_bad))
