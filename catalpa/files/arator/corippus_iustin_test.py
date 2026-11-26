# A test of one published disagreement.  Duckworth (as search-engine fragments of his 1969 book and of Orchard 1994 p. 86 give it; pages not seen) has DSDS as Corippus's commonest
# pattern, 18.06%.  My scan of the Iohannis has DDSS first (20.1%) and DSDS second (18.2%).  Did he count both of Corippus's poems?  This scans the other one, In laudem Iustini
# (Latin Wikisource, Partsch 1879 by way of MQDQ), with the same scanner, learning from the sixteen poems and this one, and prints the patterns of each poem and of both together.
import sys, glob, re, collections; sys.path.insert(0, '/home/agent1/arator')
import scan, gold, arator, latinlib, late2
ORDER = ['aen', 'geo', 'met', 'lucan', 'thebaid', 'achilleid', 'vflaccus', 'juvenal']
T = collections.OrderedDict()
for name in ORDER:
    files = sorted(glob.glob(f'/home/agent1/arator/gold/{name}[0-9]*.html'), key=lambda x: int(re.search(r'(\d+)\.html$', x).group(1)))
    T[name] = [g['text'] for f in files for g in gold.load(f)]
T['arator'] = [ln for b, ln in arator.load()]
for name, L in latinlib.late().items(): T[name] = L
for name in ('juvencus', 'ausonius', 'prudentius', 'dracontius'): T[name] = late2.load(name)
voc = late2.vocabulary([ln for L in T.values() for ln in L])
rep = {}; T['corippus'] = late2.restore_v(late2.load('corippus'), voc, rep)
for a, b in (('Romano seruit iam', 'Romano servit iam'), ('Nunc volvere dei', 'Nunc voluere dei'), ('metu, volvitque in terga', 'metu, voluitque in terga'), ('incendia volui', 'incendia volvi')):
    T['corippus'] = [ln.replace(a, b) for ln in T['corippus']]
rep2 = {}; T['iustin'] = late2.restore_v(late2.load('corippus_iustin'), voc, rep2)
print('In laudem Iustini:', len(T['iustin']), 'lines; left out as damaged', len(late2.DROPPED['corippus_iustin']), '; v restored:', dict(rep2['how']))
lines = [ln for L in T.values() for ln in L]; owner = [name for name, L in T.items() for _ in L]
lex, scans = scan.learn(lines, rounds=4, verbose=False)
S = collections.defaultdict(list)
for o, sc in zip(owner, scans): S[o].append(sc)
def show(label, scs):
    ok = [b['pat'][:4] for b in scs if b and b['pat']]; c = collections.Counter(ok)
    print(f'{label:28s} {len(scs):5d} lines, {len(ok)} scanned; dactyls {100 * sum(p.count("D") for p in ok) / (4 * len(ok)):.1f}%; ' + ', '.join(f'{p} {100 * v / len(ok):.2f}' for p, v in c.most_common(5)) + f'; first eight {100 * sum(v for _, v in c.most_common(8)) / len(ok):.1f}%')
show('Iohannis', S['corippus']); show('In laudem Iustini', S['iustin']); show('both poems', S['corippus'] + S['iustin'])
# the Iohannis in eight equal parts (the scan file does not keep the book divisions)
n = len(S['corippus'])
for k in range(8): show(f'  Iohannis, eighth {k + 1}', S['corippus'][k * n // 8:(k + 1) * n // 8])
for name in ('arator', 'sedulius', 'juvencus'): show(name, S[name])
