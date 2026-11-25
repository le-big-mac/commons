"""Extract sealed lines (label, odds) from the sealed files. Usage: extract.py sealed_dir sealed-list.txt"""
import re, sys, os

sealed_dir, listfile = sys.argv[1], sys.argv[2]
rows = []
for ln in open(listfile).read().splitlines()[1:]:
    if not ln.strip():
        continue
    f, study, kind, folder = [x.strip() for x in ln.split('|')]
    rows.append((f, study, kind, folder))

label_re = re.compile(r'^\s*(?:[-*]\s*)?(?:\*\*)?([A-Za-z]{1,4}\d+[a-z]?)\.(?:\*\*)?\s')
odds_re = re.compile(r'odds\s+(0\.\d+|1\.0+|1|0)\s*\**\s*$')

def parse(path):
    out = []
    cur = None
    text = open(path).read().splitlines()
    for i, line in enumerate(text):
        m = label_re.match(line)
        if m:
            cur = {'label': m.group(1), 'start': i + 1, 'text': line, 'odds': None}
            out.append(cur)
        elif cur is not None and cur['odds'] is None:
            cur['text'] += ' ' + line.strip()
        if cur is not None and cur['odds'] is None:
            mo = odds_re.search(line)
            if mo:
                cur['odds'] = float(mo.group(1))
                cur['end'] = i + 1
    return out, text

if __name__ == '__main__':
    total = 0
    for f, study, kind, folder in rows:
        lines, text = parse(os.path.join(sealed_dir, f))
        n_odds_lines = sum(1 for l in text if re.search(r'odds\s+0\.\d+', l))
        print(f'== {f} | {study} | {kind} | n_labels={len(lines)} | lines mentioning "odds 0.x"={n_odds_lines}')
        for l in lines:
            print(f"   {l['label']:6s} odds={l['odds']}  [{l['start']}-{l.get('end')}]  {l['text'][:110]}")
            if l['odds'] is not None:
                total += 1
    print('TOTAL with odds', total)
