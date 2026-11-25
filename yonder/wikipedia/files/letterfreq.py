"""The big table of Wikipedia's article "Letter frequency": column sums, and the cells that differ between two revisions.
usage: letterfreq.py NOW.wiki OLD.wiki        (run with -I; the files are fetched wikitext, read as text only)"""
import sys, re
def table(path):
    t = open(path, encoding='utf-8').read()
    k = max(m.start() for m in re.finditer(r'\n! ?Letter', t)); i = t.rfind('{|', 0, k); j = t.index('\n|}', i)      # the last table headed "Letter"
    block = t[i:j]
    heads = [h or g for g, h in re.findall(r'^! ?(?:data-sort-type ?= ?"?number"? ?\|)? ?\[\[([^\]|]*)\|?([^\]]*)\]\]', block, re.M)]
    rows = {}
    for m in re.finditer(r"^\|'''(.+?)'''\s*\n\|(.+)$", block, re.M):
        cells = [c.strip() for c in m.group(2).split('||')]
        rows[m.group(1)] = cells
    return heads, rows
def num(c):
    c = re.sub(r'<ref.*', '', c); m = re.search(r'-?\d+(?:\.\d+)?', c.replace('~0', '0'))
    return float(m.group(0)) if m else 0.0
hn, rn = table(sys.argv[1]); ho, ro = table(sys.argv[2])
print('languages now:', len(hn), hn); print('languages in the old revision:', len(ho))
print('letters now:', len(rn), '; old:', len(ro))
print('\ncolumn sums now, and in the old revision where the language is in both (per cent):')
for k, lang in enumerate(hn):
    s = sum(num(r[k]) for r in rn.values() if k < len(r))
    so = sum(num(r[ho.index(lang)]) for r in ro.values() if lang in ho and ho.index(lang) < len(r)) if lang in ho else None
    print(f'  {lang:12s} {s:8.3f}' + (f'   old {so:8.3f}' if so is not None else '   (not in the old revision)') + ('   <-- not 100' if abs(s - 100) > 0.6 else ''))
print('\ncells that differ between the two revisions (language: letter old -> new):')
for k, lang in enumerate(hn):
    if lang not in ho: continue
    ko = ho.index(lang); ch = []
    for L in rn:
        if L in ro and k < len(rn[L]) and ko < len(ro[L]):
            a, b = re.sub(r'<ref.*', '', ro[L][ko]).strip(), re.sub(r'<ref.*', '', rn[L][k]).strip()
            if a != b: ch.append(f'{L} {a} -> {b}')
    if ch: print(f'  {lang}: ' + '; '.join(ch) + f'   (net {sum(num(x.split(" -> ")[1]) - num(x.split(" ")[1]) for x in ch):+.3f})')
