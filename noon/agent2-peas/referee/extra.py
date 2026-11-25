# Referee: small extra checks. usage: python -I extra.py EXPECTATIONS.md MENDEL.txt
import sys, os, re, math, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(sys.argv[0])))
import numpy as np
from scipy import stats
from blind import F2, F3, PLANTS, BI, TRI, BACK
import contextlib, io
with contextlib.redirect_stdout(io.StringIO()):
    import step2 as S          # reruns step2 silently; only its functions are wanted
norm = stats.norm

print('--- which account wins, split by split (72 splits) ---')
allrows = []
for scheme in ('hyb', 'pheno', 'dom'):
    rows = S.res[scheme]; win = {'shrunk': 0, 'cut': 0, 'b2': 0}
    for r in rows:
        win[('shrunk', 'cut', 'b2')[int(np.argmax(r[6:9]))]] += 1
    cs = sorted(math.exp(r[7] - r[6]) for r in rows); sm = sorted(r[4] for r in rows); mx = sorted(r[3] for r in rows)
    print(f"{scheme:6s} best of three: {win}; cut-off over shrunk: median {np.median(cs):.1f}, below 1 in {sum(c < 1 for c in cs)}, above 10 in {sum(c > 10 for c in cs)}; largest |z| = the 35's 1.424 in {sum(abs(m - 1.42374) < 1e-4 for m in mx)}; median largest {np.median(mx):.3f}; counts <0.3: {sm}")
    allrows += rows
mx = np.array([r[3] for r in allrows]); print(f"all 72: largest |z| {mx.min():.3f} to {mx.max():.3f}; 'none beyond' odds from 1 in {1/(2*norm.cdf(mx.max())-1)**84:,.0f} to 1 in {1/(2*norm.cdf(mx.min())-1)**84:,.0f}; count <0.3 at or above 25 in {sum(r[4] >= 25 for r in allrows)}, at or below 21 in {sum(r[4] <= 21 for r in allrows)}")
z, nm = S.all_z(scheme='dom'); c = 1.4237369936; v = 1 - 2 * c * norm.pdf(c) / (2 * norm.cdf(c) - 1)
print(f"dom split, Mendel's order: the 49 new tests' largest |z| {np.abs(z[35:]).max():.3f}; a cut at 1.424 (fitted on the 35) predicts a sum of {84*v:.1f}; seen {np.sum(z**2):.2f}")
z, nm = S.all_z(); c = np.abs(z).max(); print(f"author's split: Kolmogorov distance of the 84 p from uniform {stats.kstest(2*norm.sf(np.abs(z)), 'uniform').statistic:.4f}, chance {stats.kstest(2*norm.sf(np.abs(z)), 'uniform').pvalue:.4f}")
print('tally of test kinds in the pheno split: 3:1', 27 + 4 + 13, ' 1:1', 15, ' 2:1', 8 + 4 + 13)

print('--- the six tests of 100: exact binomial ---')
pf = (2 / 3) * (1 - .75 ** 10); print(f"P(399 or more of 600 | {pf:.4f}) = {stats.binom.sf(398, 600, pf):.4f} (normal .034); two-sided about {2*stats.binom.sf(398, 600, pf):.3f}")

print('--- the extremes among single plants: exact binomial, one-sided, 253 or 258 plants of that size ---')
for a, b, npl in ((43, 2, 253), (14, 15, 253), (32, 1, 258), (20, 19, 258)):
    n = a + b; p1 = stats.binom.cdf(b, n, .25) if b < n / 4 else stats.binom.sf(b - 1, n, .25)
    print(f"   {a}:{b}: one plant so extreme or more, that side: {p1:.2e}; at least one among {npl}: {1-(1-p1)**npl:.2f}")

print('--- the counts written on the sealed sheet against the referee\'s own counts from the text ---')
sheet = open(sys.argv[1]).read().split('What I remember')[1].split("- Fisher's table")[0]
pairs = [(int(a), int(b)) for a, b in re.findall(r'(\d+):(\d+)', sheet.replace('1:1:1:1:2:2:2:2:4', ''))]
want = F2 + F3 + PLANTS
print('   pairs on the sheet:', len(pairs), '; equal to the text, in order:', pairs == want)
nine = [int(x) for x in re.search(r'529 plants, ([\d, ]+), expected', sheet).group(1).split(',')]; print('   nine kinds equal:', nine == list(BI.values()))
tri = [int(x) for x in re.findall(r'\d+', re.search(r'639 plants \((.*?)\)', sheet, re.S).group(1))]; print('   27 kinds equal (same order as my table):', tri == list(TRI.values()), len(tri))
bc = [int(x) for x in re.findall(r'\d+', re.search(r'degrees of freedom\)\. I remember (.*?) and am unsure', sheet, re.S).group(1))]; print('   back-cross counts on the sheet:', len(bc), bc)
print('   counts written on the sheet:', 2 * len(pairs) + len(nine) + len(tri) + len(bc))
t = ' '.join(open(sys.argv[2], encoding='utf-8').read().split())
print('   quotation in the text:', 'Experiment 5, which shows the greatest departure, was repeated' in t, '| "in lieu of the ratio of 60:40, that of 65:35 resulted":', 'in lieu of the ratio of 60:40, that of 65:35 resulted' in t)
