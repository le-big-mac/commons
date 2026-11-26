# The word classes whose rules were mended on 26 Nov after the fourth reader's report, measured against the reference scansion: lines of the eight classical poems that
# contain a word of the class, and how many of them the scanner reads differently from the reference.  Run with "old" to use the scanner as it was before those mends
# (a copy is kept beside this file as scan_before_26nov_mends.py).
import sys, glob, re, collections; sys.path.insert(0, '/home/agent1/arator')
if len(sys.argv) > 1 and sys.argv[1] == 'old':
    import importlib.util
    spec = importlib.util.spec_from_file_location('scan', '/home/agent1/arator/scan_before_26nov_mends.py'); scan = importlib.util.module_from_spec(spec); sys.modules['scan'] = scan; spec.loader.exec_module(scan)
else: import scan
import gold, arator, latinlib
ORDER = ['aen', 'geo', 'met', 'lucan', 'thebaid', 'achilleid', 'vflaccus', 'juvenal']
G = {}
for name in ORDER:
    files = sorted(glob.glob(f'/home/agent1/arator/gold/{name}[0-9]*.html'), key=lambda x: int(re.search(r'(\d+)\.html$', x).group(1)))
    G[name] = [g for f in files for g in gold.load(f)]
lines = [g['text'] for name in ORDER for g in G[name]] + [ln for b, ln in arator.load()] + [ln for L in latinlib.late().values() for ln in L]
lex, scans = scan.learn(lines, rounds=4, verbose=False)
ref = [g for name in ORDER for g in G[name]]
CLASSES = collections.OrderedDict([
    ('dehinc', r'^dehinc$'), ('cui in compounds, alicui', r'^(cui(que|quam|cumque|cunque|libet|vis|dam|nam|piam)|alicui|necui|sicui)$'),
    ('adiut-, coniux', r'^(ad|con)iu[tx]'), ('suasi-, suase-, suaso-, suasu-', r'suas[ieou]'), ('aera, aere, aeris, aeri', r'^(aera|aere|aeris|aeri)$')])
tot = right = 0
res = {k: [0, 0, 0, 0] for k in CLASSES}       # lines, wrong, of which fewer dactyls, more dactyls
for g, sc in zip(ref, scans):
    if not g['pat']: continue
    ok = bool(sc and sc.get('pat') == g['pat']); tot += 1; right += ok
    words = [scan.clean_word(w).lower() for w in g['text'].split()]
    for k, rx in CLASSES.items():
        if any(re.search(rx, w) for w in words):
            res[k][0] += 1
            if not ok:
                res[k][1] += 1
                if sc and sc.get('pat'):
                    d = sc['pat'].count('D') - g['pat'].count('D'); res[k][2] += d < 0; res[k][3] += d > 0
print(f'all regular reference lines: {right} of {tot} = {100 * right / tot:.2f}%')
for k, (n, w, lo, hi) in res.items(): print(f'  {k:32s} lines {n:4d}   read differently from the reference {w:3d}   (fewer dactyls {lo}, more {hi})')
