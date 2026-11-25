import sys
sys.path.insert(0,'/home/agent2/weak'); sys.path.insert(0,'/home/agent2/pdflat')
from weaklp import WSetup
def tight(p,q):
    M=p*p*q*q; S=WSetup(M); O=S.orders; n=len(O); ex={}
    for d in O:
        a=0; x=d
        while x%p==0: x//=p; a+=1
        b=0
        while x%q==0: x//=q; b+=1
        ex[d]=(a,b)
    out=[]
    for mask in range(1<<n):
        Z=[O[i] for i in range(n) if mask>>i&1]; Zs={ex[d] for d in Z}
        Ep={a for (a,b) in Zs if b==0}; Eq={b for (a,b) in Zs if a==0}
        Fm={(a,b) for (a,b) in Zs if a>0 and b>0}
        if any(a not in Ep and b not in Eq for (a,b) in Fm): continue
        if all((a,b) in Fm for a in Ep for b in Eq): continue
        k=p**len(Ep)*q**len(Eq)
        if S.Dweak(Z)[0]>=k: out.append((tuple(sorted(Ep)),tuple(sorted(Eq)),tuple(sorted(Fm))))
    return out
for pq in [(3,5),(5,3),(2,5),(5,2)]:
    print(pq)
    for t in tight(*pq): print('   Ep',t[0],'Eq',t[1],'F',t[2])
