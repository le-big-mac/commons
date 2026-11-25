# lexicon.py -- the three pronouncing dictionaries, read into {word: [list of pronunciations]}, each pronunciation a list of
# (phone, stress) with stress None for consonants.   Imported by the other scripts; python -I lexicon.py DATA_DIR prints sizes.
import os, re, sys, unicodedata
def load_cmu(path):
    d = {}
    for l in open(path, encoding='utf-8', errors='replace'):
        l = l.split('#')[0].strip()
        if not l: continue
        w, *ph = l.split()
        w = re.sub(r'\(\d+\)$', '', w).lower()
        d.setdefault(w, []).append([(p.rstrip('012'), int(p[-1]) if p[-1] in '012' else None) for p in ph])
    return d
IPA_V = ['aɪə', 'aʊə', 'eɪ', 'aɪ', 'ɔɪ', 'əʊ', 'aʊ', 'ɪə', 'eə', 'ʊə', 'iː', 'ɑː', 'ɔː', 'uː', 'ɜː', 'ɪ', 'e', 'æ', 'ʌ', 'ɒ', 'ʊ', 'ə', 'i', 'u', 'ɛ', 'a', 'o', 'ɔ', 'ɜ', 'ɑ']
IPA_C = ['tʃ', 'dʒ', 'p', 'b', 't', 'd', 'k', 'ɡ', 'g', 'f', 'v', 'θ', 'ð', 's', 'z', 'ʃ', 'ʒ', 'h', 'm', 'n', 'ŋ', 'l', 'r', 'ɹ', 'j', 'w', 'x']
def ipa_tokens(s):
    """IPA string (with stress marks) -> [(phone, stress)], stress 1/2/0 on vowels, None on consonants; None if a symbol is unknown."""
    s = unicodedata.normalize('NFC', s); out = []; i = 0; pending = 0
    while i < len(s):
        ch = s[i]
        if ch in 'ˈ\'': pending = 1; i += 1; continue
        if ch == 'ˌ': pending = 2; i += 1; continue
        if ch in ' .‿-': i += 1; continue
        for v in IPA_V:
            if s.startswith(v, i): out.append((v, pending)); pending = 0; i += len(v); break
        else:
            for c in IPA_C:
                if s.startswith(c, i): out.append(('ɡ' if c == 'g' else 'r' if c == 'ɹ' else c, None)); i += len(c); break
            else: return None
    return out
def load_ipadict(path):
    d = {}; bad = 0
    for l in open(path, encoding='utf-8'):
        if '\t' not in l: continue
        w, prons = l.rstrip('\n').split('\t', 1)
        for p in prons.split(','):
            t = ipa_tokens(p.strip().strip('/'))
            if t is None or not any(st is not None for ph, st in t): bad += 1; continue
            d.setdefault(w.lower(), []).append(t)
    return d, bad
def load_britfone(path):
    d = {}; bad = 0
    for l in open(path, encoding='utf-8'):
        if ',' not in l: continue
        w, p = l.rstrip('\n').split(',', 1); w = re.sub(r'\(\d+\)$', '', w.strip()).lower()
        t = ipa_tokens(p.strip())
        if t is None or not any(st is not None for ph, st in t): bad += 1; continue
        d.setdefault(w, []).append(t)
    return d, bad
def load_all(data):
    cmu = load_cmu(os.path.join(data, 'cmudict', 'cmudict.dict'))
    uk, bad1 = load_ipadict(os.path.join(data, 'ipadict', 'en_UK.txt'))
    bf, bad2 = load_britfone(os.path.join(data, 'britfone', 'britfone.main.3.0.1.csv'))
    return cmu, uk, bf, (bad1, bad2)
if __name__ == '__main__':
    cmu, uk, bf, bad = load_all(sys.argv[1])
    print('cmudict words', len(cmu), '| en_UK words', len(uk), 'unreadable entries', bad[0], '| britfone words', len(bf), 'unreadable entries', bad[1])
    for w in ['prayer', 'dreary', 'tea', 'obey', 'join', 'line', 'war', 'far', 'wind', 'majesty', 'heaven', 'given', 'been', 'again']:
        f = lambda d: ' / '.join(' '.join(p + ('' if s is None else str(s)) for p, s in pr) for pr in d.get(w, [])) or '-'
        print('%-8s cmu: %-34s uk: %-22s britfone: %s' % (w, f(cmu), f(uk), f(bf)))
