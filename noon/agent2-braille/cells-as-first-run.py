"""cells.py: a text put into braille by the standard translator (liblouis), uncontracted and contracted, and every
contraction read off the translator's own map of which letters became which cells.
    /usr/bin/python3 -I cells.py BOOK.txt [TABLE]  ->  prints totals and the commonest contractions
A "unit" is a run of letters that the contracted translation turned into one group of cells. Its saving is the cells
the same letters take uncontracted, less the cells they take contracted. The units of a text add up to the whole saving."""
import json, os, re, sys, collections
import louis

G1 = 'en-ueb-g1.ctb'; UEB = 'en-ueb-g2.ctb'; EBAE = 'en-us-g2.ctb'; EBAE1 = 'en-us-g1.ctb'

def clean(path):
    """the book's own text: Project Gutenberg's head and foot off; typography flattened so that printers' habits do not count"""
    t = open(path, encoding='utf-8', errors='replace').read().replace('\r', '')
    a = re.search(r'\*\*\* ?START OF (?:THE|THIS) PROJECT GUTENBERG EBOOK[^\n]*\n', t); b = re.search(r'\*\*\* ?END OF (?:THE|THIS) PROJECT GUTENBERG EBOOK', t)
    if a: t = t[a.end():]
    if b: t = t[:t.index(b.group(0))] if b.group(0) in t else t
    t = t.replace('“', '"').replace('”', '"').replace('‘', "'").replace('’', "'").replace('—', ' - ').replace('–', '-').replace('_', '')
    t = re.sub(r'\[Illustration[^\]]*\]', ' ', t)
    paras = [re.sub(r'\s+', ' ', p).strip() for p in re.split(r'\n\s*\n', t)]
    return [p for p in paras if p]

def units(par, table, g1=G1):
    """(cells uncontracted, cells contracted, [(letters, cells, saved, whole_word)]) for one paragraph"""
    b1, _, r1, _ = louis.translate([g1], par); b2, _, r2, _ = louis.translate([table], par)
    n = len(par); c1 = [(r1[i + 1] if i + 1 < n else len(b1)) - r1[i] for i in range(n)]
    out = []; i = 0
    while i < n:
        j = i + 1
        while j < n and r2[j] == r2[i]: j += 1
        cells = (r2[j] if j < n else len(b2)) - r2[i]; span = par[i:j]
        if j - i > 1 and span.isalpha():
            whole = (i == 0 or not par[i - 1].isalpha()) and (j == n or not par[j].isalpha())
            out.append((span.lower(), b2[r2[i]:r2[i] + cells], sum(c1[i:j]) - cells, whole))
        i = j
    return len(b1), len(b2), out

def book(path, table=UEB, g1=G1):
    U = C = 0; by = collections.defaultdict(lambda: [0, 0]); words = letters = 0; vocab = collections.Counter()
    for par in clean(path):
        u, c, us = units(par, table, g1); U += u; C += c
        toks = re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", par); words += len(toks); letters += sum(ch.isalpha() for ch in par)
        vocab.update(w.lower() for w in toks)
        for span, cells, saved, whole in us:
            k = span + ('|w' if whole else '|p'); by[k][0] += 1; by[k][1] += saved
    return dict(U=U, C=C, words=words, letters=letters, by={k: v for k, v in by.items()}, vocab=dict(vocab))

if __name__ == '__main__':
    r = book(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else UEB)
    U, C, W = r['U'], r['C'], r['words']; tot = sum(v[1] for v in r['by'].values())
    print('%d words, %d letters; %d cells uncontracted, %d contracted: %.2f%% saved; the units account for %d of the %d cells saved' % (W, r['letters'], U, C, 100 * (U - C) / U, tot, U - C))
    for k, v in sorted(r['by'].items(), key=lambda kv: -kv[1][1])[:40]: print('   %-16s %7d times  %7d cells  %6.0f per 100,000 words' % (k, v[0], v[1], 1e5 * v[1] / W))
    print('   distinct units:', len(r['by']))
