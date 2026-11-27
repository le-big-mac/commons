"""Evidence reading 2: the open text of the second candidate, every block marked by where its words come from.
usage: python -I ev2_open.py candidate-2.html candidate-1.html README.md [MINRUN]
Each block (outside the folds) is tiled greedily with the longest runs of tokens found (a) in the old text,
(b) in the first candidate.  Printed plain = from the old text; {{...}} = not in the old text but in the first
candidate (words read in the first evidence reading); [[...]] = in neither (new in the second candidate).
Then: sentences of the first candidate's open text that stand nowhere in the second candidate's open text."""
import sys, re, html

c2 = open(sys.argv[1], encoding='utf-8').read(); c1 = open(sys.argv[2], encoding='utf-8').read()
readme = open(sys.argv[3], encoding='utf-8').read()
MINRUN = int(sys.argv[4]) if len(sys.argv) > 4 else 4
INLINE = r'</?(em|strong|code|a|b|i|span)(\s[^>]*)?>'
def html_tokens(h):
    h = re.sub(r'<br\s*/?>', ' ', h)
    h = re.sub(INLINE, '', h); h = re.sub(r'<[^>]+>', ' ', h)
    return html.unescape(h).split()
def md_tokens(m):
    m = '\n'.join(l for l in m.split('\n') if not re.fullmatch(r'\s*\|(\s*:?-+:?\s*\|)+\s*', l))
    return m.replace('**', '').replace('*', '').replace('`', '').replace('|', ' ').replace('## ', ' ').replace('# ', ' ').split()
def open_of(c): return re.sub(r'<details.*?</details>', '\n<p>[FOLD]</p>\n', c, flags=re.S)
O = md_tokens(readme); C = html_tokens(open_of(c1))
def index(T):
    d = {}
    for j, t in enumerate(T): d.setdefault(t, []).append(j)
    return d
IO, IC = index(O), index(C)
def longest(P, i, T, I):
    best = 0
    for j in I.get(P[i], ()):
        L = 0
        while i + L < len(P) and j + L < len(T) and P[i + L] == T[j + L]: L += 1
        best = max(best, L)
    return best
def tile(P):
    out = []; i = 0
    while i < len(P):
        lo = longest(P, i, O, IO); lc = longest(P, i, C, IC)
        if lo >= MINRUN and lo >= lc - 2: kind, L = 'O', lo
        elif lc >= MINRUN: kind, L = 'C', lc
        elif lo >= MINRUN: kind, L = 'O', lo
        else: kind, L = 'N', 1
        if out and out[-1][0] == kind and kind == 'N': out[-1][1].append(P[i])
        else: out.append((kind, P[i:i + L]))
        i += L
    return out
cnt = {'O': 0, 'C': 0, 'N': 0}
blocks = re.findall(r'<(h1|h2|p|li|table)(?:\s[^>]*)?>(.*?)</\1>', open_of(c2), flags=re.S)
for tag, inner in blocks:
    P = html_tokens(inner)
    if P == ['[FOLD]']: print('\n        ---- [a fold stands here] ----'); continue
    line = []
    for kind, toks in tile(P):
        cnt[kind] += len(toks); s = ' '.join(toks)
        line.append(s if kind == 'O' else ('{{' + s + '}}' if kind == 'C' else '[[' + s + ']]'))
    print('\n<%s> %s' % (tag, ' '.join(line)))
print('\n\ntokens of the open text of the second candidate: %d from the old text, %d from the first candidate\'s new words, %d new' % (cnt['O'], cnt['C'], cnt['N']))

print('\n==== sentences of the first candidate\'s open text that are not, whole, in the second candidate\'s open text')
T2 = ' ' + ' '.join(html_tokens(open_of(c2))) + ' '
F2 = ' ' + ' '.join(html_tokens(' '.join(re.findall(r'<details.*?</details>', c2, flags=re.S)))) + ' '
for tag, inner in re.findall(r'<(h1|h2|p|li)(?:\s[^>]*)?>(.*?)</\1>', open_of(c1), flags=re.S):
    txt = ' '.join(html_tokens(inner))
    if txt == '[FOLD]': continue
    for s in re.split(r'(?<=[.!?])["\')]*\s+(?=[A-Z("\'*])', txt):
        s = s.strip()
        if s and (' ' + s + ' ') not in T2 and (' ' + s) not in T2:
            print('  %s | %s' % ('whole in a fold of 2' if (' ' + s) in F2 else 'NOT whole anywhere  ', s))
