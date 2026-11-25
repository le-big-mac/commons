"""Test of the 'equality case' idea for M = p^2 q^2 (pattern level, exponent form; no primes involved in the prediction).
Prediction: an orphan-free pattern that violates (T2) at (l,m) can have D^w = k only if, for EVERY missing (l,m)
with l in E_p, m in E_q, some 'negative term' is available: gamma(l-1, j) with j >= m, j not in V_q, or
gamma(i, m-1) with i >= l, i not in V_p, where V_p = {l'-1 : l' in E_p} u {2}.  Compare with the exact LP."""
import itertools, sys
sys.path.insert(0,'/home/agent2/weak'); sys.path.insert(0,'/home/agent2/pdflat')
from weaklp import WSetup
def patterns():
    lv=(1,2); pairs=[(1,1),(1,2),(2,1),(2,2)]
    subs=lambda S: itertools.chain.from_iterable(itertools.combinations(S,r) for r in range(len(S)+1))
    for Ep in subs(lv):
        for Eq in subs(lv):
            for F in subs(pairs):
                if any(l not in Ep and m not in Eq for l,m in F): continue      # orphan
                miss=[(l,m) for l in Ep for m in Eq if (l,m) not in F]
                if miss: yield set(Ep),set(Eq),set(F),miss
def negative_available(Ep,Eq,l,m):
    Vp={x-1 for x in Ep}|{2}; Vq={x-1 for x in Eq}|{2}
    return any(j not in Vq for j in range(m,3)) or any(i not in Vp for i in range(l,3))
pred={(frozenset(Ep),frozenset(Eq),frozenset(F)):all(negative_available(Ep,Eq,l,m) for l,m in miss) for Ep,Eq,F,miss in patterns()}
print('orphan-free patterns violating T2:',len(pred),' predicted possibly tight:',sum(pred.values()))
for (p,q) in [(2,3),(3,2),(3,5),(5,3),(2,5),(5,7)]:
    M=p*p*q*q; S=WSetup(M); wrong=0; tight=0; tight_pred=0
    for (Ep,Eq,F),pt in pred.items():
        Z=[p**l for l in Ep]+[q**m for m in Eq]+[p**l*q**m for l,m in F]
        k=p**len(Ep)*q**len(Eq); w=S.Dweak(Z)[0]
        if w>=k:
            tight+=1
            if not pt: wrong+=1
        if pt: tight_pred+=1
    print((p,q),'LP-tight patterns:',tight,' of which predicted impossible (would refute the idea):',wrong,' predicted possibly tight:',tight_pred)
