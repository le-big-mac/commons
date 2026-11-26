# Five more late poems beside Arator: Juvencus, Ausonius (Mosella), Prudentius (Psychomachia), Dracontius (Carmen de Deo), Corippus (Iohannis).
# Everything is scanned again with one lexicon learned from all the poems together (the eight classical ones, Arator, Sedulius, Claudian and the five).
# Writes late2_scans.tsv (the five, line by line) and late2_newforms.txt (their word forms that the classical poems never contain, with the scanner's division, for reading).
import sys, glob, re, collections, math, json, random; sys.path.insert(0, '/home/agent1/arator')
import scan, gold, arator, latinlib, late2
ORDER = ['aen', 'geo', 'met', 'lucan', 'thebaid', 'achilleid', 'vflaccus', 'juvenal']
NEW = ['juvencus', 'ausonius', 'prudentius', 'dracontius', 'corippus']
NAMES = dict(sedulius='Sedulius (c. 430)', claudian='Claudian (c. 400)', aen='Aeneid', geo='Georgics', met='Metamorphoses', lucan='Lucan', thebaid='Thebaid', achilleid='Achilleid', vflaccus='Valerius Flaccus',
             juvenal='Juvenal', arator='Arator (544)', juvencus='Juvencus (c. 330)', ausonius='Ausonius, Mosella (c. 371)', prudentius='Prudentius, Psych. (c. 405)', dracontius='Dracontius (c. 490)', corippus='Corippus (c. 550)')
G = {}
for name in ORDER:
    files = sorted(glob.glob(f'/home/agent1/arator/gold/{name}[0-9]*.html'), key=lambda x: int(re.search(r'(\d+)\.html$', x).group(1)))
    G[name] = [g for f in files for g in gold.load(f)]
A = arator.load(); LATE = latinlib.late()
T = collections.OrderedDict()
for name in ORDER: T[name] = [g['text'] for g in G[name]]
T['arator'] = [ln for b, ln in A]
for name, L in LATE.items(): T[name] = L
for name in NEW[:4]: T[name] = late2.load(name)
voc = late2.vocabulary([ln for L in T.values() for ln in L]); rep = {}
T['corippus'] = late2.restore_v(late2.load('corippus'), voc, rep)
print('lines left out as damaged (dagger, brackets, dots, asterisks):', {k: len(v) for k, v in late2.DROPPED.items()})
print('Corippus, v restored:', dict(rep['how']), '; forms spelled both ways in the other poems:', {k[0]: v for k, v in rep['ambiguous'].items()})
lines = [ln for L in T.values() for ln in L]; owner = [name for name, L in T.items() for _ in L]
print(len(lines), 'lines in all'); sys.stdout.flush()
lex, scans = scan.learn(lines, rounds=4, verbose=True)
S = collections.defaultdict(list)
for o, sc in zip(owner, scans): S[o].append(sc)
# Corippus: three forms that the other poems spell both ways (seruit / servit, voluere / volvere, voluit / volvit) scan either way in these lines; set by the sense, by hand:
#   "Laetaque Romano servit iam purpura regno" (serves), "Nunc voluere dei" (the gods have willed), "voluitque in terga redire" (and wished to turn back).
#   The nine other lines with "voluit" (wished) are right as the vocabulary gives them.  A fourth, found by the fourth reader: "incendia volvi" (to be rolled), which the vocabulary gave as volui.
HAND = (('Romano seruit iam', 'Romano servit iam'), ('Nunc volvere dei', 'Nunc voluere dei'), ('metu, volvitque in terga', 'metu, voluitque in terga'), ('incendia volui', 'incendia volvi'))
for i, ln in enumerate(T['corippus']):
    for a, b in HAND:
        if a in ln:
            T['corippus'][i] = ln.replace(a, b); old = S['corippus'][i]; S['corippus'][i] = scan.scan_line(T['corippus'][i], lex)
            print(f"   by hand: {T['corippus'][i]}   [{old['pat'] if old else None} -> {S['corippus'][i]['pat'] if S['corippus'][i] else None}]")
PATS = [''.join(p) for p in __import__('itertools').product('DS', repeat=4)]
def metrics(pats5):
    n = len(pats5); c = collections.Counter(p[:4] for p in pats5)
    dist = [c[p] / n for p in PATS]; feet = [sum(1 for p in pats5 if p[f] == 'D') / n for f in range(4)]; top = c.most_common(8)
    return dict(n=n, dist=dist, feet=feet, dact=sum(feet) / 4, first=top[0], top8=sum(v for _, v in top) / n, sp5=sum(1 for p in pats5 if p[4] == 'S') / n, top=top)
def js(p, q):
    m = [(a + b) / 2 for a, b in zip(p, q)]
    kl = lambda a, b: sum(x * math.log2(x / y) for x, y in zip(a, b) if x > 0)
    return math.sqrt((kl(p, m) + kl(q, m)) / 2)
def kinds(ln):
    toks = [scan.clean_word(w).lower() for w in ln.split()]; toks = [t for t in toks if t]; out = []
    for x, y in zip(toks, toks[1:]):
        if re.search(r'[aeiouy]m?$', x) and re.match(r'h?[aeiouy]', y) and not re.match(r'i[aeou]', y) and x not in ('o', 'a', 'heu'):
            out.append('est' if y in ('est', 'es') else 'que' if x.endswith('que') else 'm' if x.endswith('m') else 'other')
    return out
print('\nAgreement with the reference, learning from the larger collection (run_all.out has the figures with the smaller one):')
for name in ORDER:
    reg = [(a, b) for a, b in zip(G[name], S[name]) if a['pat']]; right = sum(1 for a, b in reg if b and b['pat'] == a['pat'])
    print(f'  {NAMES[name]:17s} {right} of {len(reg)} = {100 * right / len(reg):.2f}%')
M = {}
print('\n                               lines scanned (plain, option, fail)   dactyls 1-4 (by foot)        commonest      first eight  5th-foot sp.  elisions/100: scanner, text  | of the text count: -que, est/es, vowel+m, other; share -que or est')
for name in T:
    sc = S[name]; ok = [b for b in sc if b and b['pat']]; M[name] = m = metrics([b['pat'] for b in ok])
    how = collections.Counter(('fail' if not (b and b['pat']) else 'plain' if b['how'] == 'plain' else 'option') for b in sc)
    el = [x for x in (scan.elisions(b) for b in ok) if x is not None]; c = collections.Counter(k for ln in T[name] for k in kinds(ln)); n = sum(c.values())
    m['el'] = 100 * sum(el) / len(el); m['el_text'] = 100 * n / len(T[name]); m['kinds'] = dict(c); m['fail'] = how['fail'] / len(sc); m['lines'] = len(sc)
    print(f'  {NAMES[name]:27s} {len(sc):6d} {len(ok):6d} ({how["plain"]}, {how["option"]}, {how["fail"]} = {100 * how["fail"] / len(sc):.2f}%)   {100 * m["dact"]:5.1f}% ({", ".join(f"{100 * x:.0f}" for x in m["feet"])})   {m["first"][0]} {100 * m["first"][1] / m["n"]:4.1f}%   {100 * m["top8"]:5.1f}%   {100 * m["sp5"]:5.2f}%   {m["el"]:5.1f} {m["el_text"]:5.1f}  | {c["que"]}, {c["est"]}, {c["m"]}, {c["other"]}; {100 * (c["que"] + c["est"]) / n:.1f}%')
print('\nDistance of each poem\'s pattern frequencies from Arator\'s:')
for name in sorted([k for k in T if k != 'arator'], key=lambda k: js(M[k]['dist'], M['arator']['dist'])): print(f'  {NAMES[name]:27s} {js(M[name]["dist"], M["arator"]["dist"]):.4f}')
print('\nNearest neighbour of each of the late poems (and its distance):')
for name in ['juvencus', 'ausonius', 'claudian', 'prudentius', 'sedulius', 'dracontius', 'arator', 'corippus']:
    d = sorted((js(M[name]['dist'], M[k]['dist']), k) for k in T if k != name)
    print(f'  {NAMES[name]:27s} ' + '; '.join(f'{NAMES[k]} {x:.3f}' for x, k in d[:3]))
print('\nAll sixteen patterns (%), the late poems:')
for name in ['juvencus', 'ausonius', 'claudian', 'prudentius', 'sedulius', 'dracontius', 'arator', 'corippus']:
    print(f'  {NAMES[name]:27s} ' + ', '.join(f'{p} {100 * x:.1f}' for p, x in sorted(zip(PATS, M[name]['dist']), key=lambda t: -t[1])))
# standard errors of the dactyl share, and resampling of who is the most dactylic and who is nearest to Arator
P = {k: [b['pat'] for b in S[k] if b and b['pat']] for k in T}
print('\nShare of dactyls with its standard error (lines as the unit):')
for name in T:
    sh = [p[:4].count('D') / 4 for p in P[name]]; mu = sum(sh) / len(sh); se = (sum((x - mu) ** 2 for x in sh) / len(sh)) ** 0.5 / len(sh) ** 0.5
    print(f'  {NAMES[name]:27s} {100 * mu:6.2f} +- {100 * se:.2f}')
rng = random.Random(2026); B = 1000; top = collections.Counter(); near = collections.Counter()
for _ in range(B):
    R = {k: rng.choices(v, k=len(v)) for k, v in P.items()}; D = {k: metrics(v) for k, v in R.items()}
    top[max(D, key=lambda k: D[k]['dact'])] += 1; d = {k: js(D[k]['dist'], D['arator']['dist']) for k in D if k != 'arator'}; near[min(d, key=d.get)] += 1
print(f'resampling {B} times: most dactylic: ' + ', '.join(f'{NAMES[k]} {100 * v / B:.0f}%' for k, v in top.most_common()) + '; nearest to Arator: ' + ', '.join(f'{NAMES[k]} {100 * v / B:.0f}%' for k, v in near.most_common()))
with open('/home/agent1/arator/late2_scans.tsv', 'w') as f:
    for name in NEW:
        for ln, s_ in zip(T[name], S[name]):
            if s_ and s_['pat']: f.write(f"{name}\t{s_['pat']}\t{s_['how']}\t{s_['margin']:.1f}\t{''.join('-' if x == 'L' else 'u' if x == 'S' else 'x' for x in s_['q'])}\t{ln}\n")
            else: f.write(f"{name}\tNONE\tfail\t\t\t{ln}\n")
json.dump({k: {kk: vv for kk, vv in v.items() if kk != 'top'} for k, v in M.items()}, open('/home/agent1/arator/late2_metrics.json', 'w'))
# word forms of the five that the eight classical poems never contain and that have two vowels together, an i before a vowel, or a capital inside a line: the classes in which the scanner was found wrong on Arator
classical = set(scan.clean_word(w).lower() for name in ORDER for ln in T[name] for w in ln.split())
with open('/home/agent1/arator/late2_newforms.txt', 'w') as f:
    for name in NEW + ['sedulius', 'claudian']:
        forms = collections.Counter(); where = {}; nl = 0
        for ln in T[name]:
            hit = False
            for k, w in enumerate(ln.split()):
                c = scan.clean_word(w)
                if c and k == 0 and not (c.lower() in scan.NAMES or c.lower().startswith('aen')): c = c[:1].lower() + c[1:]      # as the scanner does with a capital at the head of a line
                if not c or c.lower() in classical: continue
                if re.search(r'[aeiouy]{2}', c.lower()) or re.search(r'i[aeiouy]', c.lower()) or (k > 0 and c[0].isupper()):
                    forms[c] += 1; where.setdefault(c, ln); hit = True
            nl += hit
        print(f'{NAMES[name]}: {len(forms)} such forms in {nl} of {len(T[name])} lines ({100 * nl / len(T[name]):.1f}%)')
        f.write(f'===== {NAMES[name]}: {len(forms)} forms in {nl} of {len(T[name])} lines\n')
        for c, n in sorted(forms.items(), key=lambda t: t[0].lower()):
            div = '.'.join((u[2] if u[0] == 'C' else u[1].upper()) for u in scan.segment(c))
            f.write(f'{c}\t{n}\t{div}\t{where[c]}\n')
