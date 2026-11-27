"""Evidence reading 1: where each earlier reader's replacement wording now stands: whole in the open text, partly, or
only under a fold.  For every item of the four lists of changes, the item's "new" text is tiled with runs of the
open text (outside <details>) and of the folded text; runs of fewer than 4 tokens do not count.
usage: python -I ev1_musts.py candidate.html LIST.json [LIST.json ...]"""
import sys, re, html, json

cand = open(sys.argv[1], encoding='utf-8').read()
INLINE = r'</?(em|strong|code|a|b|i|span)(\s[^>]*)?>'
def html_tokens(h):
    h = re.sub(INLINE, '', h); h = re.sub(r'<[^>]+>', ' ', h)
    return html.unescape(h).split()
def md_tokens(m):
    m = '\n'.join(l for l in m.split('\n') if not re.fullmatch(r'\s*\|(\s*:?-+:?\s*\|)+\s*', l))
    return m.replace('**', '').replace('*', '').replace('`', '').replace('|', ' ').replace('## ', ' ').split()
OPEN = html_tokens(re.sub(r'<details.*?</details>', ' ', cand, flags=re.S))
FOLD = html_tokens(' '.join(re.findall(r'<details.*?</details>', cand, flags=re.S)))
def index(T):
    d = {}
    for j, t in enumerate(T): d.setdefault(t, []).append(j)
    return d
IO, IF = index(OPEN), index(FOLD)
def covered(P, T, I, minrun=4):
    n = 0; i = 0; missing = []
    while i < len(P):
        best = 0
        for j in I.get(P[i], ()):
            L = 0
            while i + L < len(P) and j + L < len(T) and P[i + L] == T[j + L]: L += 1
            best = max(best, L)
        if best >= minrun: n += best; i += best
        else: missing.append(P[i]); i += 1
    return n, missing
for path in sys.argv[2:]:
    items = json.load(open(path, encoding='utf-8'))
    print('\n==== %s (%d items)' % (path, len(items)))
    for it in items:
        P = md_tokens(it['new'])
        no, miss_o = covered(P, OPEN, IO); nf, miss_f = covered(P, FOLD, IF)
        where = 'WHOLE in the open' if no == len(P) else ('none of it in the open' if no == 0 else 'PART in the open')
        print('  %-42s must=%-5s  %3d tokens; in the open %3d; in the folds %3d   -> %s' % (it['id'], it.get('must'), len(P), no, nf, where))
        if 0 < no < len(P) and it.get('must'):
            print('        not in the open: ' + ' '.join(miss_o)[:700])
