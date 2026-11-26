# Checks asked for by the third reader (26 Nov), computed from the saved scans without running the scanner again.
import sys, glob, re, collections, math, random; sys.path.insert(0, '/home/agent1/arator')
import scan, gold
PATS = [''.join(p) for p in __import__('itertools').product('DS', repeat=4)]
def dist(pats):
    c = collections.Counter(p[:4] for p in pats); return [c[p] / len(pats) for p in PATS]
def js(p, q):
    m = [(a + b) / 2 for a, b in zip(p, q)]
    kl = lambda a, b: sum(x * math.log2(x / y) for x, y in zip(a, b) if x > 0)
    return math.sqrt((kl(p, m) + kl(q, m)) / 2)
rows = [l.rstrip('\n').split('\t') for l in open('/home/agent1/arator/arator_scans.tsv')]
# (1) elisions counted straight from the text: in all lines, and in the lines the scanner reads as they stand
def places(ln):
    toks = [scan.clean_word(w).lower() for w in ln.split()]; toks = [t for t in toks if t]
    return sum(1 for x, y in zip(toks, toks[1:]) if re.search(r'[aeiouy]m?$', x) and re.match(r'h?[aeiouy]', y) and not re.match(r'i[aeou]', y) and x not in ('o', 'a', 'heu'))
allc = [places(r[6]) for r in rows]; plain = [places(r[6]) for r in rows if r[2] == 'plain']
print(f'elisions from the text: {sum(allc)} places in {sum(1 for x in allc if x)} of {len(allc)} lines; in the {len(plain)} lines read as they stand: {sum(plain)} places in {sum(1 for x in plain if x)} lines = {100 * sum(plain) / len(plain):.2f} per 100')
print('  lines read by an alternative that have one:', [(i, r[6]) for i, r in enumerate(rows) if r[2] != 'plain' and places(r[6])])
# (2) nearest neighbour, with the reference's patterns for the eight classical poems in place of the scanner's
ORDER = ['aen', 'geo', 'met', 'lucan', 'thebaid', 'achilleid', 'vflaccus', 'juvenal']
P = {}
for name in ORDER:
    files = sorted(glob.glob(f'/home/agent1/arator/gold/{name}[0-9]*.html'), key=lambda x: int(re.search(r'(\d+)\.html$', x).group(1)))
    P[name] = [g['pat'] for f in files for g in gold.load(f) if g['pat']]
late = [l.rstrip('\n').split('\t') for l in open('/home/agent1/arator/late_scans.tsv')]
for name in ('sedulius', 'claudian'): P[name] = [r[1] for r in late if r[0] == name and r[1] != 'NONE']
P['arator'] = [r[1] for r in rows if r[1] != 'NONE']
d0 = {k: js(dist(P[k]), dist(P['arator'])) for k in P if k != 'arator'}
print('distances from Arator, classical poems by the reference: ' + ', '.join(f'{k} {v:.4f}' for k, v in sorted(d0.items(), key=lambda t: t[1])))
rng = random.Random(2026); near = collections.Counter(); nearc = collections.Counter(); B = 1000
for _ in range(B):
    D = {k: dist(rng.choices(v, k=len(v))) for k, v in P.items()}
    d = {k: js(D[k], D['arator']) for k in P if k != 'arator'}
    near[min(d, key=d.get)] += 1; dc = {k: v for k, v in d.items() if k in ORDER}; nearc[min(dc, key=dc.get)] += 1
print(f'resampling {B} times with the reference\'s patterns: nearest ' + ', '.join(f'{k} {100 * v / B:.0f}%' for k, v in near.most_common()) + '; nearest classical ' + ', '.join(f'{k} {100 * v / B:.1f}%' for k, v in nearc.most_common()))
# (3) what a hand sample of 44 lines can exclude (95 in 100)
def bound(n, k):
    lo, hi = 0.0, 1.0
    for _ in range(60):
        p = (lo + hi) / 2
        if sum(math.comb(n, j) * p ** j * (1 - p) ** (n - j) for j in range(k + 1)) > 0.05: lo = p
        else: hi = p
    return lo
print(f'95% upper bound on the error rate: none wrong in 44: {100 * bound(44, 0):.1f}%; one wrong in 44: {100 * bound(44, 1):.1f}%; none wrong in 12: {100 * bound(12, 0):.1f}%; none in 24: {100 * bound(24, 0):.1f}%')
# (4) the Statius floor: how often is a random 1,123 lines of the Thebaid further from the rest than the Achilleid is from the Thebaid? (reference patterns)
obs = js(dist(P['thebaid']), dist(P['achilleid'])); t = P['thebaid']; ds = []
for _ in range(400):
    idx = set(rng.sample(range(len(t)), len(P['achilleid']))); ds.append(js(dist([t[i] for i in idx]), dist([p for i, p in enumerate(t) if i not in idx])))
print(f'Thebaid - Achilleid by the reference {obs:.4f}; random {len(P["achilleid"])} lines of the Thebaid against the rest: mean {sum(ds) / len(ds):.4f}, share above the observed {100 * sum(1 for x in ds if x > obs) / len(ds):.0f}%')
# (5) dactyl share of the Metamorphoses and its standard error, by the reference
m = P['met']; sh = [p[:4].count('D') / 4 for p in m]; mu = sum(sh) / len(sh); se = (sum((x - mu) ** 2 for x in sh) / len(sh)) ** 0.5 / len(sh) ** 0.5
a = [p[:4].count('D') / 4 for p in P['arator']]; mua = sum(a) / len(a); sea = (sum((x - mua) ** 2 for x in a) / len(a)) ** 0.5 / len(a) ** 0.5
print(f'Metamorphoses by the reference {100 * mu:.2f}% (se {100 * se:.2f}); Arator {100 * mua:.2f}% (se {100 * sea:.2f}); difference {100 * (mua - mu):.2f} = {(mua - mu) / (se ** 2 + sea ** 2) ** 0.5:.1f} standard errors')
