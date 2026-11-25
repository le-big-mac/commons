# words.py -- from a line-end word of the corpus to a dictionary entry.
# normal(w) cleans the token; lookup(w, D) returns (key, kind): kind is 'exact'; or 'elision:...' / 'british:...' (the corpus has
# had its apostrophes removed, so crown'd is "crownd"; and the American dictionary lacks some British spellings); or 'old:...'
# (an early modern spelling brought to a modern one: flagged, and kept out of the main figures); or (None, None).
import re
CONTRACTIONS = {'oer': ["o'er", 'ore'], 'eer': ["e'er", 'air'], 'neer': ["ne'er"], 'whateer': ["whate'er"], 'whereer': ["where'er"], 'whoeer': ["whoe'er"],
                'howeer': ["howe'er"], 'tis': ["'tis"], 'twas': ["'twas"], 'een': ["e'en"], 'taen': ["ta'en"], 'evn': ['even'], 'heavn': ['heaven'],
                'powr': ['power'], 'flowr': ['flower'], 'towr': ['tower'], 'bowr': ['bower'], 'showr': ['shower'], 'powrs': ['powers'], 'flowrs': ['flowers'],
                'towrs': ['towers'], 'bowrs': ['bowers'], 'showrs': ['showers'], 'heavns': ['heavens'], 'thro': ['through'], 'tho': ['though'],
                'chast': ['chaste'], 'sayd': ['said'], 'sayde': ['said'], 'payd': ['paid'], 'spright': ['sprite'], 'nought': ['nought', 'naught']}
def normal(w):
    w = w.lower().replace('’', "'").replace('`', "'")
    return re.sub(r"^[^a-z']+|[^a-z']+$", '', w)
def elisions(w):
    out = []
    for c in CONTRACTIONS.get(w, []): out.append((c, 'elision:list'))
    if '-' in w: out.append((w.replace('-', ''), 'elision:hyphen'))
    if "'" in w: out.append((w.replace("'", 'e'), "elision:'->e")); out.append((w.replace("'", ''), "elision:'"))
    if len(w) >= 3 and w.endswith('yd'): out.append((w[:-2] + 'ied', 'elision:yd->ied'))            # cryd, replyd, dyd
    if len(w) > 3 and w.endswith('d') and w[-2] not in 'e': out.append((w[:-1] + 'ed', 'elision:d->ed'))                # crownd, passd, viewd, raisd
    if len(w) > 3 and w.endswith('st'): out.append((w[:-2] + 'ssed', 'elision:st->ssed'))    # drest, opprest
    if len(w) > 3 and w.endswith('t') and w[-2] in 'pkxshc':
        out.append((w[:-1] + w[-2] + 'ed', 'elision:t->Ced'))                       # stopt, dropt, stript
        out.append((w[:-1] + 'ed', 'elision:t->ed'))                               # fixt, vext
    if len(w) > 3 and w.endswith('n') and w[-2] in 'vlsz': out.append((w[:-1] + 'en', 'elision:n->en'))           # givn, falln, stoln, risn
    return out
def british(w):
    out = []
    if w.endswith('ence'): out.append((w[:-2] + 'se', 'british:ence'))
    if w.endswith('our'): out.append((w[:-3] + 'or', 'british:our'))
    if w.endswith('ours'): out.append((w[:-4] + 'ors', 'british:our'))
    if w.endswith('tre'): out.append((w[:-2] + 'er', 'british:re'))
    if w.endswith('ize'): out.append((w[:-3] + 'ise', 'british:ize'))
    if w.endswith('ise'): out.append((w[:-3] + 'ize', 'british:ise'))
    return out
def old_spellings(w):
    out = []
    v = re.sub(r'(?<=[aeiou])u(?=[aeiouy])', 'v', w); v = re.sub(r'^v(?=[^aeiouy])', 'u', v)
    v = re.sub(r'^i(?=[aeou])', 'j', v)                                             # ioy, iust
    if v != w: out.append((v, 'u/v'))
    for b in [w] + ([v] if v != w else []):
        tag = '' if b == w else 'u/v+'
        if b.endswith('aies'): out.append((b[:-4] + 'ays', tag + 'aies->ays'))
        if b.endswith('es') and len(b) > 4: out.append((b[:-2] + 's', tag + 'es->s'))                               # dayes, teares
        if b.endswith('ie') and len(b) > 4: out.append((b[:-2] + 'y', tag + 'ie->y'))                               # victorie
        m = re.search(r'([bdgmnprt])\1e$', b)
        if m and len(b) > 4: out.append((b[:-2], tag + 'doubled+e'))                                               # sunne, warre
        if len(b) > 4 and re.search(r'([aeiou][aeiouwy][b-df-hj-np-tv-z]|[b-df-hj-np-tvxz][b-df-hj-np-tv-z])e$', b): out.append((b[:-1], tag + 'e-dropped'))   # feare, minde; not clime
        if b.endswith('ee') and len(b) in (3, 4): out.append((b[:-1], tag + 'ee->e'))                               # hee, shee
        if 'y' in b[1:-1]: out.append((b[0] + b[1:-1].replace('y', 'i') + b[-1], tag + 'y->i'))                     # wyde, lyfe
        if b.endswith('ll') and len(b) > 5: out.append((b[:-1], tag + 'll->l'))                                     # funerall, withall
    return [(c, r) for c, r in out if len(c) >= 3 or r.endswith('ee->e')]
def lookup(w, D):
    w = normal(w)
    if not w: return None, None
    if w in D: return w, 'exact'
    for c, rule in elisions(w) + british(w):
        if c in D: return c, rule
    for c, rule in old_spellings(w):
        if c in D: return c, 'old:' + rule
    for c, rule in old_spellings(w):
        for c2, rule2 in elisions(c):
            if c2 in D: return c2, 'old:' + rule + '+' + rule2.split(':')[1]
    return None, None
