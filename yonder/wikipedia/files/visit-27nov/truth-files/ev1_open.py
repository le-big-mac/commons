"""Evidence reading 1: the open parts (everything outside the folds), marked old or new by program.
usage: python -I ev1_open.py candidate.html README.md [MINRUN]
Every block of the open text is tiled greedily with the longest runs of tokens that stand, contiguous, in the old
text (markup stripped on both sides).  Runs shorter than MINRUN tokens (default 4) count as NEW and are printed
between [[ ]].  Then every sentence is listed with OLD (whole sentence is a contiguous run of the old text) or NEW."""
import sys, re, html

cand = open(sys.argv[1], encoding='utf-8').read()
readme = open(sys.argv[2], encoding='utf-8').read()
MINRUN = int(sys.argv[3]) if len(sys.argv) > 3 else 4

INLINE = r'</?(em|strong|code|a|b|i|span)(\s[^>]*)?>'
def html_tokens(h):
    h = re.sub(INLINE, '', h); h = re.sub(r'<[^>]+>', ' ', h)
    return html.unescape(h).split()
def md_tokens(m):
    m = '\n'.join(l for l in m.split('\n') if not re.fullmatch(r'\s*\|(\s*:?-+:?\s*\|)+\s*', l))
    m = m.replace('**', '').replace('*', '').replace('`', '').replace('|', ' ').replace('## ', ' ').replace('# ', ' ')
    return m.split()

O = md_tokens(readme)
pos = {}
for j, t in enumerate(O): pos.setdefault(t, []).append(j)

def tile(P):
    """list of (is_old, tokens, where_in_old)"""
    out = []; i = 0
    while i < len(P):
        best, bj = 0, -1
        for j in pos.get(P[i], ()):
            L = 0
            while i + L < len(P) and j + L < len(O) and P[i + L] == O[j + L]: L += 1
            if L > best: best, bj = L, j
        if best >= MINRUN:
            out.append((True, P[i:i + best], bj)); i += best
        else:
            if out and not out[-1][0]: out[-1][1].append(P[i])
            else: out.append((False, [P[i]], -1))
            i += 1
    return out

open_html = re.sub(r'<details.*?</details>', '\n<p>[FOLD]</p>\n', cand, flags=re.S)
# blocks: headings, paragraphs, list items, table as one block
blocks = re.findall(r'<(h1|h2|p|li|table)(?:\s[^>]*)?>(.*?)</\1>', open_html, flags=re.S)
nnew = nold = 0
allsent = []
for tag, inner in blocks:
    P = html_tokens(inner)
    if P == ['[FOLD]']:
        print('\n        ---- [a fold stands here] ----'); continue
    tl = tile(P)
    line = []
    for is_old, toks, bj in tl:
        if is_old: line.append(' '.join(toks)); nold += len(toks)
        else: line.append('[[' + ' '.join(toks) + ']]'); nnew += len(toks)
    print('\n<%s> %s' % (tag, ' '.join(line)))
    # sentences
    txt = ' '.join(P)
    sents = re.split(r'(?<=[.!?])["\')]*\s+(?=[A-Z("\'*])', txt) if tag in ('p', 'li') else [txt]
    Ojoined = ' ' + ' '.join(O) + ' '
    for s in sents:
        st = s.strip()
        if not st: continue
        allsent.append((tag, st, (' ' + st + ' ') in Ojoined or (' ' + st) in Ojoined))
print('\n\ntokens of the open text: old %d, new %d (runs under %d tokens counted new)' % (nold, nnew, MINRUN))
print('\n==== sentence list (rough split; OLD = the whole sentence stands in the old text as a run)')
for tag, s, old in allsent:
    print(('OLD  ' if old else 'NEW  ') + '<%s> ' % tag + s)
print('\nsentences: %d, of which whole from the old text: %d' % (len(allsent), sum(1 for a in allsent if a[2])))
