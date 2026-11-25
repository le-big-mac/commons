"""Level-one (T2):  L1p: p zero and q^m zero => p q^m zero (m = 1, 2);   L1q: q zero and p^l zero => p^l q zero.
If p is a zero and L1p holds, the simple fold of any step complement is a weak complement supported in pZ.
Question: are the patterns where neither fold is available ('doubly bad') exactly patterns without weak tiles (b, H, N)?"""
import json
from collections import Counter
E=json.load(open('certificates_p2q2.json'))
for reg in 'AB':
    c=Counter(); viol=[]
    for e in E:
        if e['regime']!=reg: continue
        Ep,Eq,F=set(e['Ep']),set(e['Eq']),{tuple(x) for x in e['F']}
        foldp = 1 in Ep and all((1,m) in F for m in Eq)
        foldq = 1 in Eq and all((l,1) in F for l in Ep)
        good = foldp or foldq
        c[(('fold' if good else 'nofold'),e['cat'])]+=1
        if not good and e['cat'] in ('a','RP','RQ'): viol.append((sorted(Ep),sorted(Eq),sorted(F),e['cat']))
    print('regime',reg)
    for k in sorted(c): print('   ',k,c[k])
    print('    patterns with no fold available but category a/R:',len(viol))
    for v in viol[:20]: print('      ',v)
