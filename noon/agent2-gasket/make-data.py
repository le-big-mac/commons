# make-data.py -- data.json for the page: for each of the six packings run to 10^8, its sporadic missing curvatures (all
# of them) and its quadratic families, from missing/*.txt and the paper's Theorem 2.4.   python -I make-data.py
import json, os, math
here = os.path.dirname(os.path.abspath(__file__)); N = 10**8
PACK = [('bugeye', [-1, 2, 2, 3], [], 'the bug-eye packing'), ('strip', [0, 0, 1, 1], [], 'the strip packing'), ('m3_5_8_8', [-3, 5, 8, 8], [1, 6], ''), ('m3_4_12_13', [-3, 4, 12, 13], [2, 6], ''),
        ('m2_3_6_7', [-2, 3, 6, 7], [2], ''), ('m4_5_20_21', [-4, 5, 20, 21], [2, 3], '')]
def isfam(n, fam): return any(n % u == 0 and math.isqrt(n // u) ** 2 == n // u for u in fam)
out = []
for name, root, fam, nick in PACK:
    miss = [int(x) for x in open(os.path.join(here, 'missing', name + '.txt')).read().split()]; spor = [x for x in miss if not isfam(x, fam)]
    assert len(miss) - len(spor) == sum(1 for x in miss if isfam(x, fam))
    out.append({'root': root, 'nick': nick, 'families': fam, 'N': N, 'sporadic': spor, 'inFamilies': len(miss) - len(spor)})
json.dump(out, open(os.path.join(here, 'data.json'), 'w'), separators=(',', ':'))
print(os.path.getsize(os.path.join(here, 'data.json')), 'bytes;', [(o['root'], len(o['sporadic']), o['inFamilies']) for o in out])
