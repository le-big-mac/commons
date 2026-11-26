# Arator's two books from the Latin Wikisource copy (Arntzen's edition of 1769, as in Migne): the lines of verse, without the editors' marks.
import re
# four misprints of the Wikisource copy, corrected here so that the lines can be scanned (the first two do not scan at all as printed, the third scans wrongly, the fourth does not affect the feet)
MISPRINTS = (('Destinant aeternae', 'Destinat aeternae'), ('qaaerit', 'quaerit'), ('commuue', 'commune'), ('fallare suasit', 'fallere suasit'))
def load():
    out = []
    for book, fn in ((1, 'arator_De_actibus_apostolorum_Liber_Primus.wiki'), (2, 'arator_De_actibus_apostolorum_Liber_Secundus.wiki')):
        t = open('/home/agent1/arator/texts/' + fn, encoding='utf-8').read()
        for poem in re.findall(r'<poem>(.*?)</poem>', t, flags=re.S):
            for ln in poem.split('\n'):
                ln = re.sub(r'\{\{[^}]*\}\}', '', ln); ln = re.sub(r'\([^)]*\)', '', ln); ln = re.sub(r"'{2,}", '', ln); ln = re.sub(r'<[^>]+>', '', ln); ln = re.sub(r'\[\[[^\]]*\]\]', '', ln).strip()
                for bad, good in MISPRINTS: ln = ln.replace(bad, good)
                if len(re.sub(r'[^A-Za-z]', '', ln)) >= 20: out.append((book, ln))
    return out
if __name__ == '__main__':
    L = load(); print(len(L), 'lines; book 1:', sum(1 for b, _ in L if b == 1), 'book 2:', sum(1 for b, _ in L if b == 2))
    for b, ln in L[:3] + L[-3:]: print(b, ln)
    import collections
    print('characters outside plain letters and punctuation:', collections.Counter(c for _, ln in L for c in ln if not (c.isascii())).most_common(20))
    short = [ln for _, ln in L if len(ln) < 30]; long_ = [ln for _, ln in L if len(ln) > 60]
    print('shortest:', short[:5]); print('longest:', long_[:5])
