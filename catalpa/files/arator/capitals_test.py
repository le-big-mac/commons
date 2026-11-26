# The pooled test with the rule about capitals at the head of a line switched off (argument 'off': a capital there is always ignored, as before 26 Nov)
# or on (no argument).  Compare the 'off' figures with run_all.out to see what the rule changed.
import sys, glob, re; sys.path.insert(0, '/home/agent1/arator')
import scan, gold, arator, latinlib
if len(sys.argv) > 1 and sys.argv[1] == 'off': scan.find_names = lambda lines: set()
ORDER = ['aen', 'geo', 'met', 'lucan', 'thebaid', 'achilleid', 'vflaccus', 'juvenal']
LATE = latinlib.late(); G = {}
for name in ORDER:
    files = sorted(glob.glob(f'/home/agent1/arator/gold/{name}[0-9]*.html'), key=lambda x: int(re.search(r'(\d+)\.html$', x).group(1)))
    G[name] = [g for f in files for g in gold.load(f)]
A = arator.load(); lines = []; owner = []
for name in ORDER:
    for g in G[name]: lines.append(g['text']); owner.append(name)
for b, ln in A: lines.append(ln); owner.append('arator')
for name, L in LATE.items():
    for ln in L: lines.append(ln); owner.append(name)
lex, scans = scan.learn(lines, rounds=4, verbose=False)
print('names known:', len(scan.NAMES))
import collections
S = collections.defaultdict(list)
for o, sc in zip(owner, scans): S[o].append(sc)
for name in ORDER:
    reg = [(a, b) for a, b in zip(G[name], S[name]) if a['pat']]
    right = sum(1 for a, b in reg if b and b['pat'] == a['pat'])
    print(f'{name:10s} {right} of {len(reg)} = {100 * right / len(reg):.2f}%')
for name in ('arator', 'sedulius', 'claudian'):
    ok = [b['pat'] for b in S[name] if b and b['pat']]
    print(name, len(ok), 'of', len(S[name]), 'dactyls %.2f%%' % (100 * sum(p[:4].count('D') for p in ok) / (4 * len(ok))))
# which lines of the three late poems does the rule change?  (compare with the saved scans, which were made with the rule on)
rows = [l.rstrip('\n').split('\t') for l in open('/home/agent1/arator/arator_scans.tsv')]
print('Arator lines read differently from arator_scans.tsv:', sum(1 for r, sc in zip(rows, S['arator']) if r[1] != (sc['pat'] if sc and sc['pat'] else 'NONE')))
late = [l.rstrip('\n').split('\t') for l in open('/home/agent1/arator/late_scans.tsv')]
now = [sc for name in LATE for sc in S[name]]
print('Sedulius and Claudian lines read differently from late_scans.tsv:', sum(1 for r, sc in zip(late, now) if r[1] != (sc['pat'] if sc and sc['pat'] else 'NONE')))
