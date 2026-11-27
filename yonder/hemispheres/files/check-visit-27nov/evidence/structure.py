"""Structure of the candidate as built: folds balanced, ids unique, where "How far to trust this" stands, the place kept for the reading.
usage: python structure.py NEW_BUILT"""
import re, sys, html, collections
s = open(sys.argv[1], encoding='utf-8').read()
print('details opened', len(re.findall(r'<details\b', s)), 'closed', len(re.findall(r'</details>', s)))
ids = re.findall(r'\bid="([^"]*)"', s)
print('ids:', len(ids), 'unique:', len(set(ids)), 'repeated:', [k for k, v in collections.Counter(ids).items() if v > 1])
body = s[s.index('<h1>'):s.index('<footer>')]
body = re.sub(r'<script.*?</script>', ' ', body, flags=re.S)
closed = re.sub(r'<details[^>]*>\s*<summary>(.*?)</summary>.*?</details>', r' \1 ', body, flags=re.S)
def words(x): return len(re.sub(r'<[^>]+>', ' ', html.unescape(x)).split())
i = closed.index('id="how-far-to-trust-this"')
print(f'folds closed: {words(closed)} words on the page; "How far to trust this" begins after {words(closed[:i])} of them ({100 * words(closed[:i]) / words(closed):.0f}%) and runs to word {words(closed[:closed.index("For those who want to check </details>") if "For those who want to check </details>" in closed else len(closed)])}')
j = body.index('id="how-far-to-trust-this"')
print(f'all folds open: {words(body)} words; "How far to trust this" begins after {words(body[:j])} ({100 * words(body[:j]) / words(body):.0f}%)')
print('after the section, with folds closed, the page shows:', ' | '.join(x.strip() for x in re.sub(r'<[^>]+>', '\n', closed[closed.index('None of the data is mine'):]).split('\n') if x.strip())[-200:])
print('"TODO" on the page:', [m.group(0) for m in re.finditer(r'[^<>]{0,30}TODO[^<>]{0,30}', s)])
for m in re.finditer(r'the paragraph above dated 26 November', body):
    before = body[:m.start()]
    cands = [x.start() for x in re.finditer(r'<p[^>]*>Added 26 November', before)]
    print('"the paragraph above dated 26 November": paragraphs above it that begin "Added 26 November":', len(cands), [re.sub(r'<[^>]+>', '', before[c:c + 90]) for c in cands])
