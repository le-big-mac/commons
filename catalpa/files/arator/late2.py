# Readers for five more late poems fetched from Latin Wikisource as raw wikitext (texts2/*.wiki): Juvencus, Ausonius (Mosella), Prudentius (Psychomachia),
# Dracontius (Carmen de Deo) and Corippus (Iohannis).  Each returns a list of plain lines of hexameter.  Corippus's copy writes u for v; restore_v() puts the v back.
import re, collections, html
T = '/home/agent1/arator/texts2/'
def sections(t):
    """split wikitext at == headings ==; returns [(heading, body)]"""
    parts = re.split(r'^(=+[^=\n]+=+)\s*$', t, flags=re.M); out = [('', parts[0])]
    for h, b in zip(parts[1::2], parts[2::2]): out.append((h.strip('= ').strip(), b))
    return out
DROPPED = collections.defaultdict(list)      # lines left out because the editors mark them as damaged: a dagger, square brackets, a row of dots, asterisks
def clean_lines(body, name=''):
    body = html.unescape(body)
    body = re.sub(r'\{\{[^{}]*\}\}', '', body)                      # {{Versus|5}} and other templates
    body = re.sub(r'</?poem>|<br\s*/?>', '\n', body)
    body = re.sub(r'<(/?)(\w+)>', r'\2', body)                      # editors' supplements <quod> keep the word
    body = re.sub(r'\(p\.\s*\d+\)', '', body)                       # page markers of Migne
    body = re.sub(r"'{2,}", '', body); body = re.sub(r'\[\[[^\]]*\]\]', '', body)
    out = []
    for ln in body.split('\n'):
        if re.search(r'†|[\[\]]|\.\.\.|…|\*\s*\*', ln):
            if re.search(r'[A-Za-z]{3}', ln): DROPPED[name].append(ln.strip())
            continue
        ln = re.sub(r'\s+\d+\s*$', '', ln).strip()                  # a verse number at the end of a line
        ln = ln.replace('[', '').replace(']', '').replace('†', '').replace('*', '')
        ln = re.sub(r'[«»]', '', ln); ln = re.sub(r'\s*\d+\s*', ' ', ln).replace(')', ' ').replace('(', ' ').strip(); ln = re.sub(r'\s+', ' ', ln)   # quotation marks, footnote numbers
        if len(re.findall(r'[A-Za-z]+', ln)) < 3: continue           # blank lines, lacunae, stray numbers
        out.append(ln)
    return out
def load(name):
    t = open(T + name + '.wiki', encoding='utf-8').read(); S = sections(t)
    if name == 'juvencus': keep = [b for h, b in S if h in ('Praefatio', 'Liber primus', 'Liber secundus', 'Liber tertius', 'Liber quartus')]      # the bracketed first preface is a later addition
    elif name == 'dracontius': keep = [b for h, b in S if h.startswith('Liber')]
    elif name == 'corippus': keep = [b for h, b in S if h.startswith('Liber')]                                                                    # the preface is in elegiac couplets
    elif name == 'corippus_iustin': keep = [b for h, b in S if h]                                                                              # In laudem Iustini: the preface is in hexameters too
    elif name == 'prudentius': keep = [b for h, b in S if h == 'Psychomachia']                                                                    # the preface is in iambics
    elif name == 'ausonius': keep = [re.sub(r'^.*?\}\}', '', S[0][1], count=1, flags=re.S)]
    DROPPED[name] = []
    return [ln for b in keep for ln in clean_lines(b, name)]
# ---- u for v ----
def vocabulary(texts):
    """from texts that write v: for each word with every v turned to u, the spellings seen and how often"""
    voc = collections.defaultdict(collections.Counter)
    for ln in texts:
        ln = ln.replace('æ', 'ae').replace('Æ', 'Ae').replace('œ', 'oe').replace('Œ', 'Oe')
        for w in re.findall(r'[A-Za-z]+', ln):
            if w[0] == 'V' and len(w) > 1 and w[1].lower() not in 'aeiouy': w = 'U' + w[1:]       # Vt, Vrbis
            w = w.lower()
            if 'u' in w or 'v' in w: voc[w.replace('v', 'u')][w] += 1
    return voc
# Forms of the Iohannis that are in none of the v-spelled poems and that the rules below leave wrong: set by hand after reading the whole list of such forms (26 Nov 2026).
BY_HAND = {w.replace('v', 'u'): w for w in """alvearia cervicibus cervixque curvant ferventis ferventque fervescunt fervoribus fervorque fulvos incurvas incurvis incurvo incurvos
recurvo nervi nervo nervoque nervosque observat reserva parvamque parvas parvosque persolverit dissolvitque resolvo resolvunt solvique salvans salvas salvasset salvat salvate
salvem salvetque silvarum silvasque silvisque torvis torvo convolvens convolvunt revolventi revolvi volvebant servavitque silvaizan""".split()}
PREFIX = ('circum', 'super', 'inter', 'trans', 'prae', 'con', 'per', 'sub', 'dis', 'pro', 'ad', 'in', 'ob', 're', 'de', 'se')
def by_rule(w):
    w = list(w); V = 'aeiouy'
    for k, c in enumerate(w):
        if c != 'u': continue
        prev = w[k - 1] if k else ''; nxt = w[k + 1] if k + 1 < len(w) else ''; nxt2 = w[k + 2] if k + 2 < len(w) else ''
        if prev == 'q' or nxt == '' or nxt not in V: continue
        if k == 0: w[k] = 'v'                                                   # uir, uulnus
        elif prev in V and not (prev == 'i' and k == 1):                        # between vowels: nouus, saeuus; but iuuenis keeps its first u
            if nxt == 'u' and nxt2 in V and nxt2: continue                      # the u of iu-u-enis, flu-u-ius: the next one is the consonant
            w[k] = 'v'
        elif ''.join(w[:k]) in PREFIX: w[k] = 'v'                               # aduenit, inuitus, conuiua
    return ''.join(w)
def enclitic_ve(w, voc):
    """uirtusue, faciemue: -ue after a consonant is the enclitic -ve when what is left is a word"""
    if len(w) > 4 and w.endswith('ue') and w[-3] in 'mstrxcdn' and w[-4] in 'aeiouy': return w[:-2] + 've'      # cygnumue, uirtusue; not praecipue, construe
    return w
def restore_v(lines, voc, report=None):
    how = collections.Counter(); out = []; unknown = collections.Counter(); ambiguous = collections.Counter()
    def fix(m):
        word = m.group(0); w = word.lower()
        if word[0] == 'V' and (len(word) == 1 or w[1] not in 'aeiouy'): word = 'U' + word[1:]; w = 'u' + w[1:]      # Vlixem, Vt
        w = w.replace('v', 'u')
        if 'u' not in w: return word
        if w in voc:
            new = voc[w].most_common(1)[0][0]; how['in the vocabulary'] += 1
            if len(voc[w]) > 1 and min(voc[w].values()) >= 2: ambiguous[(w, tuple(sorted(voc[w])))] += 1
        elif w in BY_HAND: new = BY_HAND[w]; how['by hand'] += 1
        else:
            w2 = enclitic_ve(w, voc); stem = w2[:-2] if w2 != w else w
            base = voc[stem].most_common(1)[0][0] if stem in voc else BY_HAND.get(stem) or by_rule(stem)
            new = base + ('ve' if w2 != w else ''); how['by rule, changed' if new != w else 'by rule, unchanged'] += 1; unknown[(w, new)] += 1
        return ''.join(b.upper() if a.isupper() else b for a, b in zip(word, new))
    for ln in lines: out.append(re.sub(r'[A-Za-z]+', fix, ln))
    if report is not None: report['how'] = how; report['unknown'] = unknown; report['ambiguous'] = ambiguous
    return out
if __name__ == '__main__':
    for name in ('juvencus', 'ausonius', 'prudentius', 'dracontius', 'corippus'):
        L = load(name); print(f'{name}: {len(L)} lines | {L[0]} | {L[-1]}')
        odd = [l for l in L if re.search(r'[^A-Za-zæœÆŒëïü\s.,;:!?\'"()\-–—]', l)]
        print('   lines with other characters:', len(odd), odd[:6])
        n = [len(l.split()) for l in L]; print('   words per line: min', min(n), 'max', max(n), '; shortest:', sorted(L, key=len)[:3], '; longest:', sorted(L, key=len)[-2:])
