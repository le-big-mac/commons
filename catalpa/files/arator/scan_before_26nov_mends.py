# A scanner for Latin dactylic hexameters from plain text (no vowel lengths marked).
# It works by constraint: syllables that must be long (diphthongs, vowels before two consonants) and syllables that are probably short (a vowel before another vowel) are fixed;
# every line must be five feet of dactyl (long short short) or spondee (long long) and a last foot of two syllables; the lengths of the remaining vowels are learned from the scanner's
# own confident lines and reused.  No scansion made by anyone else is used for the learning; the reference scansion (hypotactic.com) is used only to measure how often the scanner is right.
import re, unicodedata, itertools, math, collections

VOW = set('aeiouy')
MUTES = set('bcdgptf'); LIQ = set('lr')
PREFIX = ('ad', 'ab', 'ob', 'sub', 'con', 'in', 'dis', 'per', 'inter', 'circum', 'super', 'trans')
JSTEM = ('iac', 'iec', 'iug', 'iun', 'iur', 'ius', 'iuv', 'iud', 'ioc', 'iub', 'iung', 'iect', 'iict')
I_VOWEL_INITIAL = ('iamb', 'iaspi', 'iason', 'iasi', 'iapy', 'iapet', 'ioni', 'iacch', 'iarb', 'iopa', 'ioll', 'iolc', 'iocast')
I_VOWEL_WORDS = {'io', 'iulus', 'iule', 'iuli', 'iulo', 'iulum', 'ion', 'iones', 'ionas'}
OE_SPLIT = ('poet', 'coea', 'coeg', 'coerc', 'coeo', 'coeu', 'coemp', 'coemi', 'coex', 'boet', 'noe', 'simoe', 'aloe', 'chloe')
EU_WORDS = ('seu', 'neu', 'heu', 'eheu', 'ceu', 'heus')
SU_GLIDE = ('suad', 'suav', 'sues', 'suet')
EUS_TWO = {'deus', 'epicureus', 'pythagoreus', 'cythereus', 'sophocleus', 'nazareus', 'hebreus', 'iudeus', 'pharisaeus'}      # capitalised words in -eus that are not Greek names in one syllable

def strip_marks(s):
    s = unicodedata.normalize('NFD', s)
    return ''.join(c for c in s if not unicodedata.combining(c))

def clean_word(w):
    w = strip_marks(w).replace('æ', 'ae').replace('œ', 'oe').replace('Æ', 'Ae').replace('Œ', 'Oe')
    w = re.sub(r'[^A-Za-z]', '', w)
    return w.replace('j', 'i').replace('J', 'I')

def segment(word, opt=frozenset()):
    """word (letters, original capitals) -> list of units: ('C', n_consonant_weight, text) and ('V', text, is_diphthong).  opt holds alternative choices to try when a line will not scan."""
    cap = word[:1].isupper(); w = word.lower()
    if w == 'dehinc': w = 'deinc'                      # usually one syllable in verse
    n = len(w); units = []; i = 0
    def is_v(k): return 0 <= k < n and w[k] in VOW
    while i < n:
        c = w[i]
        # ---- consonantal i
        if c == 'i' and w[i:i + 3] == 'iic' and w[:i] in ('ob', 'ad', 'ab', 'in', 'con', 'sub', 'pro', 're', 'e', 'de', 'tra', 'dis') and ('iflip', i) not in opt:
            units.append(('C', 2 if w[i - 1] in VOW else 1, 'i')); i += 1; continue      # proiicit, obiice: the first i is the consonant of iacio
        if c == 'i' and is_v(i + 1) and w[i + 1] != 'i':
            initial = (i == 0)
            intervoc = i > 0 and is_v(i - 1) and not (i >= 2 and w[i - 2:i] == 'qu')
            comp = any(w[:i] == p for p in PREFIX) and any(w[i:].startswith(j) for j in JSTEM) and w[i:] != 'ius'
            as_cons = False
            if initial and not any(w.startswith(x) for x in I_VOWEL_INITIAL) and w not in I_VOWEL_WORDS: as_cons = True
            if intervoc and not cap and not w.startswith('isai'): as_cons = True
            if intervoc and w[:i] in ('co', 'prae', 'intro', 'retro', 'ante') and w[i + 1] in 'ei': as_cons = False      # coiere, praeiit: forms of ire, where the i is a vowel
            if intervoc and cap and any(w.startswith(x) for x in ('troi', 'mai', 'grai', 'cai', 'ai', 'bai', 'pompei', 'tei', 'vei', 'boi')): as_cons = True
            if comp: as_cons = True
            if ('iflip', i) in opt: as_cons = not as_cons
            if as_cons:
                units.append(('C', 2 if (intervoc and not initial) else 1, 'i')); i += 1; continue
        # ---- qu, ngu + vowel, su + vowel in a few words
        if c == 'q' and i + 1 < n and w[i + 1] == 'u':
            units.append(('C', 1, 'qu')); i += 2; continue
        if c == 'g' and i + 2 < n and w[i + 1] == 'u' and is_v(i + 2) and i > 0 and w[i - 1] == 'n' and ('guflip', i) not in opt:
            units.append(('C', 1, 'gu')); i += 2; continue
        if c == 's' and w[i:i + 4] in SU_GLIDE:
            units.append(('C', 1, 'su')); i += 2; continue
        if c in VOW:
            two = w[i:i + 2]; dip = False
            if len(two) == 2 and two[1] in VOW:
                if two == 'ae': dip = not (w == 'aer' or (i == 0 and w.startswith('aeri') and n > 4 and w[4] in VOW) or (i == 2 and w.startswith('phaeth')) or w.endswith('ael') or (i == 0 and not cap and w.startswith('aen') and not w.startswith('aenigm')))
                elif two == 'au': dip = not ((cap and n > 5 and i == n - 3 and w.endswith('aus')) or (i == n - 3 and w.endswith('aum')))
                elif two == 'oe': dip = not any(w.startswith(x) and x.find('oe') == i for x in OE_SPLIT)
                elif two == 'eu': dip = (w[i:i + 3] != 'eun' or w.startswith('eunuch')) and ((w in EU_WORDS) or i == 0 or (i + 2 < n and w[i + 2] not in VOW and w[i + 2] not in 'ms') or (cap and i == n - 3 and w.endswith('eus') and w not in EUS_TWO))
                elif two == 'ui': dip = w in ('cui', 'huic', 'hui')
                elif two == 'ei': dip = w in ('dein', 'deinde', 'deinceps', 'hei', 'deinc')
                if ('dflip', i) in opt: dip = not dip
            if dip:
                units.append(('V', two, True)); i += 2
            else:
                units.append(('V', c, False)); i += 1
            continue
        if c == 'h':
            i += 1; continue                     # h counts for nothing (ch, ph, th are single consonants)
        units.append(('C', 2 if c in 'xz' else 1, c)); i += 1
    # merge consonant runs
    out = []
    for u in units:
        if u[0] == 'C' and out and out[-1][0] == 'C': out[-1] = ('C', out[-1][1] + u[1], out[-1][2] + u[2])
        else: out.append(u)
    return out

class Syl:
    __slots__ = ('w', 'k', 'key', 'hard', 'soft', 'final')
    def __init__(s, w, k, key): s.w = w; s.k = k; s.key = key; s.hard = None; s.soft = None; s.final = False

def build(words, opt=frozenset()):
    """words: cleaned words of a line.  Returns the syllables left after elision, each with what is known of its length: hard 'L', or soft 'S' (vowel before vowel), or nothing."""
    segs = [segment(w, frozenset((t, i) for (t, wi, i) in opt if wi == n)) for n, w in enumerate(words)]
    syls = []
    for wi, units in enumerate(segs):
        vs = [j for j, u in enumerate(units) if u[0] == 'V']
        if not vs: continue
        nxt = None
        for wj in range(wi + 1, len(segs)):
            if any(u[0] == 'V' for u in segs[wj]): nxt = segs[wj]; break
        lw = words[wi].lower()
        for vk, j in enumerate(vs):
            last = (vk == len(vs) - 1)
            after = units[j + 1:]            # units after this nucleus within the word
            # elision: last nucleus, word ends in the vowel or vowel + m, next word begins with a vowel (h is nothing)
            if last and nxt is not None and nxt[0][0] == 'V' and ('hiatus', wi, 0) not in opt:
                tail = ''.join(u[2] if u[0] == 'C' else u[1] for u in after)
                if tail in ('', 'm') and lw not in ('o', 'a', 'heu', 'io'):
                    continue
            s = Syl(wi, vk, (lw, vk)); s.final = last
            dip = units[j][2]
            if dip: s.hard = 'L'
            else:
                if not last:
                    nx = units[j + 1]
                    if nx[0] == 'V': s.soft = 'S'                       # vowel before vowel
                    else:
                        wgt = nx[1]; txt = nx[2]
                        if wgt >= 2:
                            mcl = (len(txt) == 2 and txt[0] in MUTES and txt[1] in LIQ and wgt == 2)
                            if not mcl: s.hard = 'L'
                else:
                    wgt = sum(u[1] for u in after if u[0] == 'C')
                    if nxt is not None and nxt[0][0] == 'C':
                        if wgt >= 1: wgt += nxt[0][1]
                        # a final open vowel before two consonants of the next word is left unknown
                    if wgt >= 2: s.hard = 'L'
            syls.append(s)
    return syls

def candidates(n):
    """all ways of placing dactyls in feet 1-5 for a line of n syllables"""
    nd = n - 12
    if nd < 0 or nd > 5: return []
    out = []
    for dset in itertools.combinations(range(5), nd):
        pat = ''.join('D' if f in dset else 'S' for f in range(5)); q = []
        for f in range(5): q += ['L', 'S', 'S'] if f in dset else ['L', 'L']
        q += ['L', 'X']; out.append((pat, q))
    return out

class Lexicon:
    def __init__(s): s.c = collections.defaultdict(lambda: [0, 0]); s.suf = collections.defaultdict(lambda: [0, 0])
    def add(s, syl, q):
        i = 0 if q == 'L' else 1
        s.c[syl.key][i] += 1
        if syl.final: s.suf[syl.key[0][-3:]][i] += 1
    def p_long(s, syl):
        a, b = s.c.get(syl.key, (0, 0))
        if a + b >= 1: return min(0.985, max(0.015, (a + 0.3) / (a + b + 0.6)))
        if syl.final:
            a, b = s.suf.get(syl.key[0][-3:], (0, 0))
            if a + b >= 5: return min(0.9, max(0.1, (a + 1.0) / (a + b + 2.0)))
        return 0.5

def score(syls, q, lex):
    sc = 0.0; hardbad = 0
    for s, x in zip(syls, q):
        if x == 'X': continue
        if s.hard == 'L':
            if x != 'L': hardbad += 1
            continue
        p = lex.p_long(s) if lex is not None else 0.5
        if s.soft == 'S' and p == 0.5: p = 0.06
        sc += math.log(p if x == 'L' else 1 - p)
    return hardbad, sc

def scan_words(words, lex=None, opt=frozenset()):
    syls = build(words, opt); res = []
    for pat, q in candidates(len(syls)):
        hb, sc = score(syls, q, lex)
        if hb == 0:
            if pat[4] == 'S': sc += math.log(0.02)        # a spondee in the fifth foot is rare
            res.append((sc, pat, q))
    res.sort(reverse=True)
    return syls, res

def options(words):
    """alternative readings to try when a line will not scan as it stands: no elision at one place; a diphthong split or two vowels joined; i taken the other way"""
    out = []
    for wi, w in enumerate(words):
        lw = w.lower()
        if wi + 1 < len(words) and re.search(r'[aeiouy]m?$', lw) and re.match(r'h?[aeiouy]', words[wi + 1].lower()): out.append(frozenset([('hiatus', wi, 0)]))
        for i in range(len(lw) - 1):
            if lw[i] in VOW and lw[i + 1] in VOW: out.append(frozenset([('dflip', wi, i)]))
            if lw[i] == 'i' and lw[i + 1] in VOW: out.append(frozenset([('iflip', wi, i)]))
            if lw[i] == 'g' and lw[i + 1] == 'u': out.append(frozenset([('guflip', wi, i)]))
    return out

NAMES = set()      # filled by learn(): words written with a capital inside a sentence somewhere in the collection

def scan_line(text, lex=None, allow_options=True, first_cap=False):
    """-> dict(pat, margin, n_ok, how, syls, q) or None"""
    words = [clean_word(w) for w in re.split(r'[\s\-–—]+', text)]; words = [w for w in words if w]
    if not words: return None
    if not first_cap and not (words[0].lower() in NAMES or words[0].lower().startswith('aen')): words[0] = words[0][:1].lower() + words[0][1:]   # a capital at the head of a line says nothing, unless the word is known as a name
    syls, res = scan_words(words, lex)
    how = 'plain'
    if not res and allow_options:
        best = None
        for o in options(words):
            s2, r2 = scan_words(words, lex, o)
            if r2 and (best is None or r2[0][0] > best[1][0][0]): best = (s2, r2, o)
        if best: syls, res, how = best[0], best[1], 'option:' + ','.join(sorted(t for t, _, _ in best[2]))
    if res and allow_options and res[0][1][4] == 'S':            # a spondee in the fifth foot is rare: prefer another reading of the line that avoids it
        for o in options(words):
            s2, r2 = scan_words(words, lex, o)
            if r2 and r2[0][1][4] == 'D':
                syls, res, how = s2, r2, 'option:' + ','.join(sorted(t for t, _, _ in o)); break
    if not res: return dict(pat=None, n=len(syls), how='fail')
    margin = res[0][0] - res[1][0] if len(res) > 1 else 99.0
    return dict(pat=res[0][1], margin=margin, n_ok=len(res), how=how, syls=syls, q=res[0][2], n=len(syls), words=words)

def find_names(lines):
    """words written with a capital where neither the head of a line nor the start of a sentence explains it"""
    out = collections.Counter(); low = collections.Counter()
    for t in lines:
        toks = t.split()
        for k, tok in enumerate(toks):
            w = clean_word(tok)
            if not w: continue
            if w[0].isupper():
                if k > 0 and not re.search(r'[.!?:;"\'’”]\W*$', toks[k - 1]) and not re.match(r'\W', tok): out[w.lower()] += 1
            else: low[w.lower()] += 1
    return {w for w, c in out.items() if c > low.get(w, 0)}

def learn(lines, rounds=4, lex=None, verbose=True, threshold=2.5):
    """lines: list of plain strings.  Returns the lexicon and the final scans."""
    lex = lex or Lexicon()
    NAMES.clear(); NAMES.update(find_names(lines))
    for r in range(rounds):
        new = Lexicon(); conf = 0; scans = []
        for t in lines:
            sc = scan_line(t, lex if r > 0 else None, allow_options=(r > 0))
            scans.append(sc)
            if sc and sc['pat'] and sc['how'] == 'plain' and (sc['n_ok'] == 1 or sc['margin'] >= threshold):
                conf += 1
                for s, x in zip(sc['syls'], sc['q']):
                    if x != 'X' and s.hard is None: new.add(s, x)
        lex = new
        if verbose: print(f'  round {r}: {conf} of {len(lines)} lines confident; lexicon {len(lex.c)} syllables of word forms')
    scans = [scan_line(t, lex) for t in lines]
    return lex, scans

def elisions(sc):
    """number of syllables lost by elision in a scanned line (plain readings only; None otherwise)"""
    if not sc or not sc.get('pat') or sc['how'] != 'plain': return None
    nuclei = sum(sum(1 for u in segment(w) if u[0] == 'V') for w in sc['words'])
    return nuclei - sc['n']
