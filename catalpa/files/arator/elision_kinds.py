# Elisions counted straight from the text, by kind, for all sixteen poems (no scanner): what is being elided, and how the totals depend on what one counts.
# Kinds: a word ending in -que (the enclitic, and atque, neque, quoque...); any word before est or es (often not counted as elision at all); a word in vowel + m; any other final vowel.
import re, sys, glob, collections; sys.path.insert(0, '/home/agent1/arator')
import scan, gold
def kinds(ln):
    toks = [scan.clean_word(w).lower() for w in ln.split()]; toks = [t for t in toks if t]; out = []
    for x, y in zip(toks, toks[1:]):
        if re.search(r'[aeiouy]m?$', x) and re.match(r'h?[aeiouy]', y) and not re.match(r'i[aeou]', y) and x not in ('o', 'a', 'heu'):
            k = 'est' if y in ('est', 'es') else 'que' if x.endswith('que') else 'm' if x.endswith('m') else 'other'
            out.append((k, x, y))
    return out
sets = collections.OrderedDict()
for name in ['geo', 'aen', 'met', 'lucan', 'vflaccus', 'thebaid', 'achilleid', 'juvenal']:
    files = sorted(glob.glob(f'/home/agent1/arator/gold/{name}[0-9]*.html'), key=lambda x: int(re.search(r'(\d+)\.html$', x).group(1)))
    sets[name] = [g['text'] for f in files for g in gold.load(f)]
late = [l.rstrip('\n').split('\t') for l in open('/home/agent1/arator/late_scans.tsv')]
sets['claudian'] = [r[5] for r in late if r[0] == 'claudian']; sets['sedulius'] = [r[5] for r in late if r[0] == 'sedulius']
sets['arator'] = [l.rstrip('\n').split('\t')[6] for l in open('/home/agent1/arator/arator_scans.tsv')]
late2 = [l.rstrip('\n').split('\t') for l in open('/home/agent1/arator/late2_scans.tsv')]      # the five poems added on 26 Nov
for name in ('juvencus', 'ausonius', 'prudentius', 'dracontius', 'corippus'): sets[name] = [r[5] for r in late2 if r[0] == name]
print('poem        lines  places  per 100 |  -que   est/es  vowel+m  other |  per 100 lines: without est/es; other and vowel+m only | share of all that is -que or est/es')
for name, L in sets.items():
    c = collections.Counter(k for ln in L for k, x, y in kinds(ln)); n = sum(c.values())
    print(f'{name:10s} {len(L):6d} {n:6d}  {100 * n / len(L):6.1f}  | {c["que"]:5d}  {c["est"]:5d}   {c["m"]:5d}  {c["other"]:5d}  |  {100 * (n - c["est"]) / len(L):6.1f}   {100 * (c["m"] + c["other"]) / len(L):6.1f}   |  {100 * (c["que"] + c["est"]) / n:5.1f}%')
if len(sys.argv) > 1:
    for ln in sets[sys.argv[1]]:
        for kk, x, y in kinds(ln):
            if len(sys.argv) < 3 or kk == sys.argv[2]: print(f'   {kk:6s} {x} {y}   | {ln}')
