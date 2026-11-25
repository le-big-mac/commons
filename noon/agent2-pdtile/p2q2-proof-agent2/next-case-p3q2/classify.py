"""Numerical classification of zero patterns of Z_{p^a q^b} by the method used for p^2 q^2 (exploration, no claims).
 L2: neither p nor q is a zero (Lemma 2);  a: (T2) and no orphan;  b: D^w < k;  R: an optimal step complement is supported
 in pZ or qZ;  N: D^w/k not an integer;  H: none of these (would need a counting lemma)."""
import sys, itertools
from collections import Counter
from steplp import Step
def run(p,a,q,b,show=False):
    S=Step(p,a,q,b); ords=[o for o in S.ords if o!=(0,0)]; M=S.M
    tot=[float(S.C[((0,0),cl)]) for cl in S.cls]
    outp=[tot[k] if cl[0]==0 else 0.0 for k,cl in enumerate(S.cls)]
    outq=[tot[k] if cl[1]==0 else 0.0 for k,cl in enumerate(S.cls)]
    cnt=Counter(); hard=[]
    for mask in range(1<<len(ords)):
        Z={o for i,o in enumerate(ords) if mask>>i&1}
        if (1,0) not in Z and (0,1) not in Z: cnt['L2']+=1; continue
        t2=all((l,m) in Z for l in range(1,a+1) for m in range(1,b+1) if (l,0) in Z and (0,m) in Z)
        orph=any((l,0) not in Z and (0,m) not in Z for (l,m) in Z if l and m)
        if t2 and not orph: cnt['a']+=1; continue
        k=p**sum(1 for l in range(1,a+1) if (l,0) in Z)*q**sum(1 for m in range(1,b+1) if (0,m) in Z)
        r=S.solve(Z); v=r[0]; D=M/v
        if D<k*(1-1e-9): cnt['b']+=1; continue
        mp=S.solve(Z,obj=outp,extra_eq=[(tot,v)])[0]; mq=S.solve(Z,obj=outq,extra_eq=[(tot,v)])[0]
        if mp<1e-7*max(1,v) or mq<1e-7*max(1,v): cnt['R']+=1; continue
        if abs(D/k-round(D/k))>1e-6: cnt['N']+=1; continue
        cnt['H']+=1; hard.append((sorted(Z),round(D/k,4),t2,orph))
    return cnt,hard
if __name__=='__main__':
    a,b=int(sys.argv[1]),int(sys.argv[2])
    for pq in sys.argv[3:]:
        p,q=map(int,pq.split(','))
        cnt,hard=run(p,a,q,b)
        print('p^%d q^%d'%(a,b),(p,q),dict(cnt),flush=True)
        for h in hard[:40]: print('     H:',h)
