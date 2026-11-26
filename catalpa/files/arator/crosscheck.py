# The scanner on each poem of the reference collection, learning only from that poem's own lines.
import sys, glob, re, collections; sys.path.insert(0, '/home/agent1/arator')
import scan, gold, evalgold
groups = collections.OrderedDict()
for f in sorted(glob.glob('/home/agent1/arator/gold/*.html'), key=lambda x: (re.sub(r'\d+\.html$', '', x), int(re.search(r'(\d+)\.html$', x).group(1)))):
    groups.setdefault(re.sub(r'\d+$', '', f.split('/')[-1][:-5]), []).append(f)
tot = right = 0
for name, files in groups.items():
    lex, G, scans, wrong = evalgold.run(files, label=name)
    n = sum(1 for g in G if g['pat']); r = sum(1 for g, sc in zip(G, scans) if g['pat'] and sc and sc['pat'] == g['pat'])
    if name != 'aen': tot += n; right += r
print(f'pooled over the seven poems other than the Aeneid: {right} of {tot} = {100 * right / tot:.2f}%')
