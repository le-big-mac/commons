# rhyme.py -- does a pair of words rhyme in a pronouncing dictionary?  Two dictionaries, never mixed:
#   A  the Carnegie Mellon dictionary (American, with stress);   B  BEEP (British, without stress).
# Short stem: the last vowel of the word and every sound after it.  Long stem (A only): from the vowel with primary stress on.
# A pair rhymes in a dictionary if some listed pronunciation of the one has the same stem as some listed pronunciation of the other.
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lexicon as L, words as W
BEEP_V = {'aa', 'ae', 'ah', 'ao', 'aw', 'ax', 'ay', 'ea', 'eh', 'er', 'ey', 'ia', 'ih', 'iy', 'oh', 'ow', 'oy', 'ua', 'uh', 'uw'}
def load_beep(path):
    d = {}
    for l in open(path, encoding='latin-1'):
        if l.startswith('#') or not l.strip(): continue
        w, *ph = l.split()
        if not ph or not re.match(r"^[A-Z']+$", w) or any(p not in BEEP_V and not re.match(r'^[a-z]+$', p) for p in ph): continue
        if ph[-1] == 'r' and len(ph) > 1 and ph[-2] in BEEP_V: ph = ph[:-1]                    # the linking r of a non-rhotic accent is not part of the word
        if ph not in d.setdefault(w.lower(), []): d[w.lower()].append(ph)
    return d
def short_a(pron):
    i = max(k for k, (p, s) in enumerate(pron) if s is not None); return tuple(p for p, s in pron[i:])
def long_a(pron):
    v = [k for k, (p, s) in enumerate(pron) if s is not None]; one = [k for k in v if pron[k][1] == 1]; two = [k for k in v if pron[k][1] == 2]
    i = one[-1] if one else two[-1] if two else v[0]; return tuple(p for p, s in pron[i:])
def short_b(pron):
    v = [k for k, p in enumerate(pron) if p in BEEP_V]
    return tuple(pron[v[-1]:]) if v else None
class Judge:
    def __init__(self, data):
        self.A = {w: [p for p in ps if any(s is not None for _, s in p)] for w, ps in L.load_cmu(os.path.join(data, 'cmudict', 'cmudict.dict')).items()}
        self.A = {w: ps for w, ps in self.A.items() if ps}
        self.B = {w: [p for p in ps if short_b(p)] for w, ps in load_beep(os.path.join(data, 'beep', 'beep', 'beep-1.0')).items()}
        self.B = {w: ps for w, ps in self.B.items() if ps}
        self.cache = {}
    def word(self, w):
        """-> dict with, for each dictionary, the entry used, how it was found, and the sets of stems"""
        if w in self.cache: return self.cache[w]
        ka, ra = W.lookup(w, self.A); kb, rb = W.lookup(w, self.B)
        r = {'a': ka, 'ra': ra, 'b': kb, 'rb': rb,
             'sa': [short_a(p) for p in self.A[ka]] if ka else None, 'la': [long_a(p) for p in self.A[ka]] if ka else None,
             'sb': [short_b(p) for p in self.B[kb]] if kb else None}
        self.cache[w] = r; return r
    def pair(self, w1, w2):
        """-> dict: for A short ('as'), A long ('al'), A short by first-listed pronunciations only ('a1'), B short ('bs'): True / False, or None if a word is unknown;
           'old': True if either word was found only by an early modern respelling in that dictionary ('olda', 'oldb')"""
        x, y = self.word(w1), self.word(w2); r = {}
        if x['a'] and y['a']:
            r['as'] = bool(set(x['sa']) & set(y['sa'])); r['al'] = bool(set(x['la']) & set(y['la'])); r['a1'] = x['sa'][0] == y['sa'][0]
            r['olda'] = x['ra'].startswith('old') or y['ra'].startswith('old')
        else: r['as'] = r['al'] = r['a1'] = None; r['olda'] = False
        if x['b'] and y['b']:
            r['bs'] = bool(set(x['sb']) & set(y['sb'])); r['oldb'] = x['rb'].startswith('old') or y['rb'].startswith('old')
        else: r['bs'] = None; r['oldb'] = False
        return r
if __name__ == '__main__':
    J = Judge(sys.argv[1]); print('A', len(J.A), 'words; B', len(J.B), 'words')
    for a, b in [('tea', 'obey'), ('tea', 'see'), ('join', 'line'), ('love', 'move'), ('love', 'dove'), ('war', 'far'), ('war', 'for'), ('majesty', 'eye'), ('majesty', 'be'),
                 ('nature', 'creature'), ('heaven', 'given'), ('dawn', 'morn'), ('again', 'rain'), ('been', 'seen'), ('wind', 'mind'), ('crownd', 'round'), ('oer', 'more'),
                 ('pass', 'was'), ('command', 'hand'), ('prayer', 'air'), ('dreary', 'weary'), ('xyzzy', 'tea')]:
        r = J.pair(a, b); x, y = J.word(a), J.word(b)
        print('%-9s %-9s A short %-5s long %-5s first %-5s | B short %-5s | %s ~ %s | %s ~ %s' % (a, b, r['as'], r['al'], r['a1'], r['bs'],
              '/'.join(' '.join(s) for s in (x['sa'] or [])), '/'.join(' '.join(s) for s in (y['sa'] or [])), '/'.join(' '.join(s) for s in (x['sb'] or [])), '/'.join(' '.join(s) for s in (y['sb'] or []))))
