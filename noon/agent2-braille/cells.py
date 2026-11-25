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
        core = span.strip()                              # the American code joins some words to the next: the unit is then the word and its space
        if j - i > 1 and core.isalpha() and len(core) > 1:
            k0 = i + (len(span) - len(span.lstrip())); k1 = k0 + len(core)
            whole = (k0 == 0 or not par[k0 - 1].isalpha()) and (k1 == n or not par[k1].isalpha())
            out.append((core.lower(), b2[r2[i]:r2[i] + cells], sum(c1[i:j]) - cells, whole))
        i = j
    return len(b1), len(b2), out

STRONG = {'and': '&', 'for': '=', 'of': '(', 'the': '!', 'with': ')'}       # five signs whose cell means nothing else
def sign_cells(par, table):
    """how often the cells of seven signs stand in the contracted braille of a paragraph, however the translator grouped the letters:
    and, for, of, the, with (each a cell of its own); in (dots 3-5, not doubled, which is an asterisk); be (the cell alone as a word, or at
    the head of a word before a letter). Used where the units cannot be trusted to show a sign inside a word."""
    b = louis.translateString([table], par); out = {w: b.count(c) for w, c in STRONG.items()}
    out['in'] = len(re.findall(r'(?<!9)9(?!9)', b)); n = 0
    for tok in b.split(' '):
        tok = tok.lstrip(',8"\'(-'); 
        if tok.rstrip('14680,.-;:\'"') == '2' or (len(tok) > 1 and tok[0] == '2' and tok[1].isalpha()): n += 1
    out['be'] = n
    return out
def book(path, table=UEB, g1=G1, trim=None):
    """trim, if given, takes the cleaned paragraphs and returns those to be counted (story.py: the story alone)"""
    U = C = 0; by = collections.defaultdict(lambda: [0, 0]); words = letters = 0; vocab = collections.Counter(); sc = collections.Counter(); caps = collections.Counter()
    for par in (trim(clean(path)) if trim else clean(path)):
        u, c, us = units(par, table, g1); U += u; C += c; sc.update(sign_cells(par, table))
        toks = re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", par); words += len(toks); letters += sum(ch.isalpha() for ch in par)
        vocab.update(w.lower() for w in toks); caps.update(w.lower() for w in toks if w[0].isupper())
        for span, cells, saved, whole in us:
            k = span + ('|w' if whole else '|p'); by[k][0] += 1; by[k][1] += saved
    return dict(U=U, C=C, words=words, letters=letters, by={k: v for k, v in by.items()}, vocab=dict(vocab), caps=dict(caps), sign_cells=dict(sc))

if __name__ == '__main__':
    r = book(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else UEB)
    U, C, W = r['U'], r['C'], r['words']; tot = sum(v[1] for v in r['by'].values())
    print('%d words, %d letters; %d cells uncontracted, %d contracted: %.2f%% saved; the units account for %d of the %d cells saved' % (W, r['letters'], U, C, 100 * (U - C) / U, tot, U - C))
    for k, v in sorted(r['by'].items(), key=lambda kv: -kv[1][1])[:40]: print('   %-16s %7d times  %7d cells  %6.0f per 100,000 words' % (k, v[0], v[1], 1e5 * v[1] / W))
    print('   distinct units:', len(r['by']))
