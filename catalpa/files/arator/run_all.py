# Arator beside eight classical hexameter poems, all scanned by the same scanner, which learns vowel lengths from the confident lines of the whole collection (Arator's included).
# For the classical poems the reference scansion gives a check on every figure.
import sys, glob, re, collections, math, json, random; sys.path.insert(0, '/home/agent1/arator')
import scan, gold, arator, latinlib
ORDER = ['aen', 'geo', 'met', 'lucan', 'thebaid', 'achilleid', 'vflaccus', 'juvenal']
LATE = latinlib.late()
NAMES = dict(sedulius='Sedulius (5th c.)', claudian='Claudian (c. 400)', aen='Aeneid', geo='Georgics', met='Metamorphoses', lucan='Lucan', thebaid='Thebaid', achilleid='Achilleid', vflaccus='Valerius Flaccus', juvenal='Juvenal', arator='Arator')
G = {}
for name in ORDER:
    files = sorted(glob.glob(f'/home/agent1/arator/gold/{name}[0-9]*.html'), key=lambda x: int(re.search(r'(\d+)\.html$', x).group(1)))
    G[name] = [g for f in files for g in gold.load(f)]
A = arator.load()
lines = []; owner = []
for name in ORDER:
    for g in G[name]: lines.append(g['text']); owner.append(name)
for b, ln in A: lines.append(ln); owner.append('arator')
for name, L in LATE.items():
    for ln in L: lines.append(ln); owner.append(name)
print(len(lines), 'lines in all;', len(A), 'of Arator'); sys.stdout.flush()
lex, scans = scan.learn(lines, rounds=4, verbose=True)
S = collections.defaultdict(list)
for o, sc in zip(owner, scans): S[o].append(sc)
PATS = [''.join(p) for p in __import__('itertools').product('DS', repeat=4)]
def metrics(pats5, nel=None):
    n = len(pats5); c = collections.Counter(p[:4] for p in pats5)
    dist = [c[p] / n for p in PATS]
    feet = [sum(1 for p in pats5 if p[f] == 'D') / n for f in range(4)]
    top = c.most_common(8)
    return dict(n=n, dist=dist, feet=feet, dact=sum(feet) / 4, first=top[0], top8=sum(v for _, v in top) / n, sp5=sum(1 for p in pats5 if p[4] == 'S') / n, top=top)
def js(p, q):
    m = [(a + b) / 2 for a, b in zip(p, q)]
    kl = lambda a, b: sum(x * math.log2(x / y) for x, y in zip(a, b) if x > 0)
    return math.sqrt((kl(p, m) + kl(q, m)) / 2)
M = {}; R = {}
print('\nAgreement with the reference, learning from the whole collection:')
for name in ORDER:
    g = G[name]; sc = S[name]; reg = [(a, b) for a, b in zip(g, sc) if a['pat']]
    right = sum(1 for a, b in reg if b and b['pat'] == a['pat']); notplain = sum(1 for a, b in reg if (not b) or b['pat'] is None or b['how'] != 'plain')
    M[name] = metrics([b['pat'] for a, b in reg if b and b['pat']]); R[name] = metrics([a['pat'] for a, b in reg])
    el_m = [scan.elisions(b) for a, b in reg]; el_ok = [(x, a['nel']) for x, (a, b) in zip(el_m, reg) if x is not None]
    M[name]['el'] = 100 * sum(x for x, _ in el_ok) / len(el_ok); R[name]['el'] = 100 * sum(a['nel'] for a, b in reg) / len(reg); M[name]['notplain'] = notplain / len(reg)
    print(f'  {NAMES[name]:17s} {len(reg):6d} regular lines; same pattern as the reference {100 * right / len(reg):6.2f}%; not scanned as it stands {100 * notplain / len(reg):5.2f}%')
sc = S['arator']; ok = [b for b in sc if b and b['pat']]
M['arator'] = metrics([b['pat'] for b in ok]); el = [scan.elisions(b) for b in ok]; el = [x for x in el if x is not None]
M['arator']['el'] = 100 * sum(el) / len(el); M['arator']['notplain'] = sum(1 for b in sc if (not b) or b['pat'] is None or b['how'] != 'plain') / len(sc)
how = collections.Counter((b['how'].split(':')[0] if b and b['pat'] else 'fail') for b in sc); conf = sum(1 for b in ok if b['how'] == 'plain' and (b['n_ok'] == 1 or b['margin'] >= 2.5))
print(f'\nArator: {len(sc)} lines; scanned {len(ok)}; {dict(how)}; confident {conf}')
print('\n                      lines  dactyls in feet 1-4 (by foot)            commonest pattern    first eight  5th-foot spondee  elisions/100 lines   [reference: dactyls, commonest, elisions]')
for name in ORDER + ['arator']:
    m = M[name]; r = R.get(name)
    ref = f'   [{100 * r["dact"]:.1f}%, {r["first"][0]} {100 * r["first"][1] / r["n"]:.1f}%, {r["el"]:.1f}]' if r else ''
    print(f'  {NAMES[name]:17s} {m["n"]:6d}  {100 * m["dact"]:5.1f}%  ({", ".join(f"{100 * x:.0f}" for x in m["feet"])})   {m["first"][0]} {100 * m["first"][1] / m["n"]:5.1f}%        {100 * m["top8"]:5.1f}%        {100 * m["sp5"]:5.2f}%          {m["el"]:5.1f}       {ref}')
for name in LATE:
    sc_ = S[name]; ok_ = [b for b in sc_ if b and b['pat']]
    M[name] = metrics([b['pat'] for b in ok_]); el_ = [x for x in (scan.elisions(b) for b in ok_) if x is not None]
    M[name]['el'] = 100 * sum(el_) / len(el_); M[name]['notplain'] = sum(1 for b in sc_ if (not b) or b['pat'] is None or b['how'] != 'plain') / len(sc_)
    m = M[name]
    print(f'  {NAMES[name]:17s} {m["n"]:6d}  {100 * m["dact"]:5.1f}%  ({", ".join(f"{100 * x:.0f}" for x in m["feet"])})   {m["first"][0]} {100 * m["first"][1] / m["n"]:5.1f}%        {100 * m["top8"]:5.1f}%        {100 * m["sp5"]:5.2f}%          {m["el"]:5.1f}        (no reference; not scanned as it stands {100 * m["notplain"]:.1f}% of {len(sc_)})')
ORDER_ALL = ORDER + list(LATE)
print('\nDistance of each poem\'s pattern frequencies from Arator\'s (Jensen-Shannon, 0 = identical):')
for name in sorted(ORDER_ALL, key=lambda k: js(M[k]['dist'], M['arator']['dist'])):
    print(f'  {NAMES[name]:17s} {js(M[name]["dist"], M["arator"]["dist"]):.4f}')
print('\nFor scale, the same distance between pairs of the classical poems:')
for a, b in (('aen', 'geo'), ('aen', 'met'), ('aen', 'lucan'), ('thebaid', 'achilleid'), ('met', 'vflaccus'), ('lucan', 'thebaid')):
    print(f'  {NAMES[a]} - {NAMES[b]}: {js(M[a]["dist"], M[b]["dist"]):.4f}')
print('\nAmong the others: ' + '; '.join(f'{NAMES[a]} - {NAMES[b]}: {js(M[a]["dist"], M[b]["dist"]):.4f}' for a, b in (('sedulius', 'claudian'), ('sedulius', 'aen'), ('claudian', 'aen'), ('claudian', 'thebaid'), ('sedulius', 'thebaid'), ('claudian', 'lucan'), ('sedulius', 'met'))))
print('\nArator, all sixteen patterns of the first four feet (%):', ', '.join(f'{p} {100 * x:.1f}' for p, x in sorted(zip(PATS, M['arator']['dist']), key=lambda t: -t[1])))
print('Aeneid (my scanner):', ', '.join(f'{p} {100 * x:.1f}' for p, x in sorted(zip(PATS, M['aen']['dist']), key=lambda t: -t[1])))
# Arator's two books apart, and how large the distance is between two samples of ONE poem (the floor that sampling alone gives)
pa = [(b, s_['pat']) for (b, ln), s_ in zip(A, sc) if s_ and s_['pat']]
m1 = metrics([p for b, p in pa if b == 1]); m2 = metrics([p for b, p in pa if b == 2])
print(f"\nArator book 1: {m1['n']} lines, dactyls {100 * m1['dact']:.1f}%, commonest {m1['first'][0]} {100 * m1['first'][1] / m1['n']:.1f}%;  book 2: {m2['n']} lines, dactyls {100 * m2['dact']:.1f}%, commonest {m2['first'][0]} {100 * m2['first'][1] / m2['n']:.1f}%;  distance between the two books {js(m1['dist'], m2['dist']):.4f}")
random.seed(544)
for name, size in (('aen', 2324), ('met', 2324), ('thebaid', 2324), ('thebaid', 1123)):
    pats = [b['pat'] for a, b in zip(G[name], S[name]) if a['pat'] and b and b['pat']]; d = []
    for _ in range(40):
        idx = set(random.sample(range(len(pats)), size)); d.append(js(metrics([pats[i] for i in idx])['dist'], metrics([p for i, p in enumerate(pats) if i not in idx])['dist']))
    print(f'  floor: a random {size} lines of the {NAMES[name]} against the rest of it: distance {sum(d) / len(d):.4f} on average (largest of 40 draws {max(d):.4f})')
# save Arator's scans for reading by eye
with open('/home/agent1/arator/arator_scans.tsv', 'w') as f:
    for (b, ln), s_ in zip(A, sc):
        if s_ and s_['pat']:
            q = ''.join('-' if x == 'L' else 'u' if x == 'S' else 'x' for x in s_['q'])
            f.write(f"{b}\t{s_['pat']}\t{s_['how']}\t{s_['margin']:.1f}\t{s_['n_ok']}\t{q}\t{ln}\n")
        else: f.write(f"{b}\tNONE\tfail\t\t\t\t{ln}\n")
with open('/home/agent1/arator/late_scans.tsv', 'w') as f:
    for name, L in LATE.items():
        for ln, s_ in zip(L, S[name]):
            if s_ and s_['pat']: f.write(f"{name}\t{s_['pat']}\t{s_['how']}\t{s_['margin']:.1f}\t{''.join('-' if x == 'L' else 'u' if x == 'S' else 'x' for x in s_['q'])}\t{ln}\n")
            else: f.write(f"{name}\tNONE\tfail\t\t\t{ln}\n")
json.dump({k: {kk: vv for kk, vv in v.items() if kk != 'top'} for k, v in M.items()}, open('/home/agent1/arator/metrics.json', 'w'))

# ---- further checks, added after a second reader's report (26 Nov) ----
print('\n--- further checks ---')
# (1) the lines the second reader found misread: what the mended scanner now gives (row = 0-based line of Arator; expected = the reader's hand scansion of the first four feet)
EXPECT = {34: 'DDDD', 156: 'DDDS', 164: 'SSDS', 184: 'DDSS', 337: 'SDDD', 437: 'DSSS', 449: 'DSDD', 718: 'SDSS', 1054: 'DDSS', 1120: 'DSDD', 1193: 'DSDS', 1205: 'DSDS', 1358: 'DDDD', 1976: 'DDDS', 1981: 'SDSD',
          31: 'DDSS', 724: 'DDDS', 1811: 'DDSS', 212: 'DDSD', 1564: 'DSSD', 687: 'SSDS', 1343: 'SDSS', 2124: 'DDDS', 445: 'SSDS', 503: 'DSSD', 888: 'DDDS'}
bad = [(r, sc[r]['pat'][:4] if sc[r] and sc[r]['pat'] else None, e) for r, e in sorted(EXPECT.items()) if not (sc[r] and sc[r]['pat'] and sc[r]['pat'][:4] == e)]
print(f'the reader\'s {len(EXPECT)} corrected lines: {len(EXPECT) - len(bad)} now read as the reader read them; still different: {bad}')
# (2) Ovid book by book, by the reference
files = sorted(glob.glob('/home/agent1/arator/gold/met[0-9]*.html'), key=lambda x: int(re.search(r'(\d+)\.html$', x).group(1)))
ob = [100 * metrics([g['pat'] for g in gold.load(f) if g['pat']])['dact'] for f in files]
print('Metamorphoses, share of dactyls book by book (reference): ' + ', '.join(f'{x:.1f}' for x in ob) + f'; lowest {min(ob):.1f}, highest {max(ob):.1f}')
se = (sum((sum(1 for c in p[:4] if c == 'D') / 4 - M['arator']['dact']) ** 2 for b, p in pa) / len(pa)) ** 0.5 / len(pa) ** 0.5
print(f'Arator: standard error of the share of dactyls, taking lines as the unit: {100 * se:.2f} points')
# (3) how secure are "nearest" and "farthest"?  resample the lines of every poem
P = {name: [b['pat'] for a, b in zip(G[name], S[name]) if a['pat'] and b and b['pat']] for name in ORDER}
for name in LATE: P[name] = [b['pat'] for b in S[name] if b and b['pat']]
P['arator'] = [p for b, p in pa]
rng = random.Random(2026); near = collections.Counter(); nearc = collections.Counter(); far = collections.Counter(); B = 1000
for _ in range(B):
    D = {k: metrics(rng.choices(v, k=len(v)))['dist'] for k, v in P.items()}
    d = {k: js(D[k], D['arator']) for k in P if k != 'arator'}
    near[min(d, key=d.get)] += 1; far[max(d, key=d.get)] += 1; dc = {k: v for k, v in d.items() if k in ORDER}; nearc[min(dc, key=dc.get)] += 1
print(f'resampling the lines of each poem {B} times: nearest to Arator: ' + ', '.join(f'{NAMES[k]} {100 * v / B:.0f}%' for k, v in near.most_common()) + '; nearest classical: ' + ', '.join(f'{NAMES[k]} {100 * v / B:.0f}%' for k, v in nearc.most_common()) + '; farthest: ' + ', '.join(f'{NAMES[k]} {100 * v / B:.0f}%' for k, v in far.most_common()))
# (4) Arator's two books against a random split of his lines into the same sizes
allp = P['arator']; n1 = sum(1 for b, p in pa if b == 1); ds = []
for _ in range(1000):
    idx = set(rng.sample(range(len(allp)), n1)); ds.append(js(metrics([allp[i] for i in idx])['dist'], metrics([p for i, p in enumerate(allp) if i not in idx])['dist']))
ds.sort(); obs = js(metrics([p for b, p in pa if b == 1])['dist'], metrics([p for b, p in pa if b == 2])['dist'])
print(f'Arator book 1 against book 2: {obs:.4f}; random splits of the same sizes: mean {sum(ds) / len(ds):.4f}, 95th percentile {ds[949]:.4f}, share above the observed {100 * sum(1 for x in ds if x > obs) / len(ds):.0f}%')
# (5) a spondee in the fifth foot: how many of the reference's does the scanner find?
tot = found = false = 0
for name in ORDER:
    for a, b in zip(G[name], S[name]):
        if not a['pat']: continue
        r5 = a['pat'][4] == 'S'; m5 = bool(b and b['pat'] and b['pat'][4] == 'S'); tot += r5; found += (r5 and m5); false += (m5 and not r5)
print(f'fifth-foot spondees in the eight classical poems: the reference has {tot}; the scanner finds {found} of them and reports {false} that are not there')
# (6) which way do the scanner's errors lean?
fewer = more = same = 0
for name in ORDER:
    for a, b in zip(G[name], S[name]):
        if a['pat'] and b and b['pat'] and b['pat'] != a['pat']:
            x = b['pat'].count('D') - a['pat'].count('D'); fewer += x < 0; more += x > 0; same += x == 0
print(f'lines the scanner reads differently from the reference: {fewer + more + same}; with fewer dactyls {fewer}, with more {more}, with the same number {same}')
# (7) elisions in Arator counted straight from the text, without the scanner
cnt = 0
for b, ln in A:
    toks = [scan.clean_word(w).lower() for w in ln.split()]; toks = [t for t in toks if t]
    for x, y in zip(toks, toks[1:]):
        if re.search(r'[aeiouy]m?$', x) and re.match(r'h?[aeiouy]', y) and not re.match(r'i[aeou]', y) and x not in ('o', 'a', 'heu'): cnt += 1
print(f'places in Arator where a final vowel or vowel + m meets an initial vowel or h (words beginning with consonantal i left out): {cnt} in {len(A)} lines = {100 * cnt / len(A):.2f} per 100; lines with at least one elision by the scanner: {sum(1 for x in el if x > 0)}')
