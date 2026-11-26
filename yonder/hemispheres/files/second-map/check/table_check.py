"""Compare every cell of the note's main table with the study's JSON files (author's) and with the checker's own halves.json.
usage: python -I table_check.py README.md AUTHOR_OUT_DIR CHECK_HALVES.json"""
import sys, json, re
readme, ad, hj = sys.argv[1:4]
mine = json.load(open(hj))
rows = [l for l in open(readme) if re.match(r'^\| (GHS|WorldPop|\|)? ?', l) and re.search(r'\| (19|20)\d\d', l)]
ds = None; bad = 0; n = 0
for l in rows:
    c = [x.strip() for x in l.strip().strip('|').split('|')]
    if c[0].startswith('GHS'): ds = 'ghs'
    elif 'older' in c[0]: ds = 'g1'
    elif 'newer' in c[0]: ds = 'g2'
    year = int(c[1][:4]); key = f'{ds}-{year}'
    a = json.load(open(f'{ad}/{key}.json')); m = mine[key]
    cands = [a['best']] + list(a['climb'].values()); t = max(cands, key=lambda v: v['share'])
    exp = [f"{a['total'] / 1e9:.3f}", f"{t['lat']:.2f}° N, {t['lon']:.2f}° E", f"{100 * t['share']:.3f}%", f"{100 * a['hard']['valais']:.3f}%", f"{100 * a['hard']['berlin']:.3f}%",
           f"{(a['only_berlin'] - a['only_valais']) / 1e6:+.1f}".replace('-', '−')]
    expm = [f"{m['total'] / 1e9:.3f}", None, None, f"{100 * m['share']['valais']:.3f}%", f"{100 * m['share']['berlin']:.3f}%", f"{m['diff_millions']:+.1f}".replace('-', '−')]
    for k in range(6):
        n += 1
        ok = c[2 + k] == exp[k] and (expm[k] is None or c[2 + k] == expm[k])
        if not ok:
            bad += 1; print('MISMATCH', key, 'column', k, 'note:', c[2 + k], 'author json:', exp[k], 'checker:', expm[k])
    proj = 'projection' in c[1]
    if proj != (year >= 2025): print('projection label?', key, c[1])
print(f'{len(rows)} rows, {n} cells compared, {bad} mismatches')
