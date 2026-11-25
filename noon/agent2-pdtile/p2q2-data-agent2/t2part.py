"""For M = p^2 q^2: among patterns with no orphan that violate (T2), is D^w(Z) < k(Z) always?  (Exact rationals.)
If so, the (T2) half of 'weak tile => tile' for p^2 q^2 needs no counting on sets, only upper bounds."""
import sys, itertools
sys.path.insert(0,'/home/agent2/weak'); sys.path.insert(0,'/home/agent2/pdflat')
from weaklp import WSetup
def run(p,q):
    M=p*p*q*q; S=WSetup(M); O=S.orders; n=len(O)
    ex={}
    for d in O:
        a=0; x=d
        while x%p==0: x//=p; a+=1
        b=0
        while x%q==0: x//=q; b+=1
        ex[d]=(a,b)
    tot=0; bad=[]; ratios=[]
    for mask in range(1<<n):
        Z=[O[i] for i in range(n) if mask>>i&1]; Zs={ex[d] for d in Z}
        Ep={a for (a,b) in Zs if b==0}; Eq={b for (a,b) in Zs if a==0}
        Fm={(a,b) for (a,b) in Zs if a>0 and b>0}
        if any(a not in Ep and b not in Eq for (a,b) in Fm): continue          # has an orphan
        if all((a,b) in Fm for a in Ep for b in Eq): continue                  # T2 holds
        k=p**len(Ep)*q**len(Eq); w=S.Dweak(Z)[0]; tot+=1
        ratios.append(float(w)/k)
        if w>=k: bad.append((sorted(Zs),str(w),k))
    return tot,bad,max(ratios) if ratios else None
for (p,q) in [(2,3),(3,2),(2,5),(5,2),(3,5),(5,3),(2,7),(3,7),(5,7),(7,5),(7,11),(11,13)]:
    tot,bad,mx=run(p,q)
    print((p,q),'orphan-free patterns violating T2:',tot,' with D^w >= k:',len(bad),' max D^w/k: %.4f'%mx,bad[:3],flush=True)
