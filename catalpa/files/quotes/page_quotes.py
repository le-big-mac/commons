# Writes the tables of ~/site/quotes.html from verdicts.tsv, sample.json and score.out, between the page's markers.   Run: python3 -I page_quotes.py
import json, csv, re, html, math
S = json.load(open('/home/agent1/quotes/sample.json')); page = '/home/agent1/quotes/page/quotes.html'      # the page waits here until the owner has answered; it is copied to ~/site only then
forty = [s['id'] for s in S['sample']]; mag = [s['id'] for s in S['magnets']]; Q = {s['id']: s for s in S['sample'] + S['magnets']}
V = {int(r['id']): r for r in csv.DictReader(open('/home/agent1/quotes/verdicts.tsv', encoding='utf-8'), delimiter='\t')}
NAME = dict(V='sound', A='altered', M="someone else's first", U='not traced')
e = html.escape
def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d; return 100 * (c - h), 100 * (c + h)
def counts():
    rows = ['<div class="tablewrap"><table>', '<tr><th>Verdict</th><th>What it means</th><th class="n">Of the forty</th><th class="n">Likely range for the whole list, in 100</th></tr>']
    for v, what in (('V', 'the words are in the named author\'s own work, as the list gives them'), ('A', 'the author did say it, but the list\'s wording differs in substance'), ('M', 'the earliest source found is someone else\'s'), ('U', 'no page of the author\'s own could be reached')):
        k = sum(1 for i in forty if V[i]['verdict'] == v); lo, hi = wilson(k, 40)
        rows.append(f'<tr><td>{NAME[v].capitalize()}</td><td>{what}</td><td class="n">{k}</td><td class="n">{lo:.0f} to {hi:.0f}</td></tr>')
    rows.append('</table></div>'); return '\n'.join(rows)
def incipit(text):
    """the opening words only: the owner of the machine asked that the page should not reproduce too many of the quotations"""
    w = text.split(); k = 5 if len(w) >= 10 else max(2, len(w) // 2)
    return ' '.join(w[:k]).rstrip(',;:—-.') + '…'
def cut(cell):
    """a passage in quotation marks longer than eight words is cut to its first five"""
    def f(m):
        w = m.group(1).split()
        return '"' + (m.group(1) if len(w) <= 8 else ' '.join(w[:5]).rstrip(',;:—-.') + '…') + '"'
    return re.sub(r'"([^"]+)"', f, cell)
def every(ids):
    rows = ['<div class="tablewrap"><table>', '<tr><th>Whose, and how it begins</th><th>Verdict</th><th>Where it comes from</th><th>What differs</th><th>How I saw it</th></tr>']
    for i in ids:
        r = V[i]; w = cut(r['wording'].strip()); nm = r['name'].strip()
        diff = ('' if w in ('', 'as listed') else e(w)) + (('; ' if w not in ('', 'as listed') else '') + 'the name is ' + e(nm) if nm else '')
        rows.append(f"<tr><td><strong>{e(Q[i]['author'])}</strong>: \"{e(incipit(Q[i]['text']))}\"</td><td>{NAME[r['verdict']]}</td><td>{e(cut(r['where']))}</td><td>{diff or ('nothing' if r['verdict'] == 'V' else '—')}</td><td>{e(r['seen'])}</td></tr>")
    rows.append('</table></div>'); return '\n'.join(rows)
# public copies, for the site: the sample by author and opening words, the verdicts with long quoted passages cut short
json.dump(dict(note='The fifty-four quotations that were looked up, each by its author as listed and its opening words only.', n_all=S['n_all'], n_frame=S['n_frame'], seed=S['seed'],
               sample=[dict(id=x['id'], author=x['author'], begins=incipit(x['text'])) for x in S['sample']], magnets=[dict(id=x['id'], author=x['author'], begins=incipit(x['text'])) for x in S['magnets']]),
          open('/home/agent1/quotes/sample-public.json', 'w'), ensure_ascii=False, indent=1)
with open('/home/agent1/quotes/verdicts-public.tsv', 'w', encoding='utf-8', newline='') as f:
    rows_ = list(csv.DictReader(open('/home/agent1/quotes/verdicts.tsv', encoding='utf-8'), delimiter='\t')); w_ = csv.writer(f, delimiter='\t'); cols = list(rows_[0].keys())
    w_.writerow(['id', 'author', 'begins'] + cols[1:])
    for r in rows_: w_.writerow([r['id'], Q[int(r['id'])]['author'], incipit(Q[int(r['id'])]['text'])] + [cut(r[c]) if c in ('where', 'wording') else r[c] for c in cols[1:]])
t = open(page, encoding='utf-8').read()
for name, block in (('counts', counts()), ('forty', every(forty)), ('magnets', every([m for m in mag if m not in forty]))):
    t, n = re.subn(rf'(<!--BEGIN {name}-->).*?(<!--END {name}-->)', lambda m: m.group(1) + '\n' + block + '\n' + m.group(2), t, flags=re.S); assert n == 1, name
open(page, 'w', encoding='utf-8').write(t); print('written', page)
