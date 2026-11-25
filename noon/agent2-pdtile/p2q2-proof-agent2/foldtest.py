"""Numerical test of Proposition F at M = 36 (p = 2, q = 3) and with the roles exchanged: for tiles A whose pattern has
p a zero and (q^m zero => p q^m zero), take random optimal step complements f, fold them along the p-direction and check
that the fold is a weak complement vanishing outside pZ.  Also count how often f itself already charges numbers prime to p."""
import sys, itertools, cmath, random
import numpy as np
from scipy.optimize import linprog
sys.path.insert(0,'sands')
from steplp import Step
def run(p,q,ntiles=400,seed=1):
    random.seed(seed); M=p*p*q*q; S=Step(p,2,q,2)
    # coordinates: x -> (u,w) = (x mod p^2, x mod q^2)
    def cls(x):
        u=x%(p*p); w=x%(q*q)
        i=2 if u==0 else (1 if u%p==0 else 0); j=2 if w==0 else (1 if w%q==0 else 0)
        return (i,j)
    def order_of(d):
        l=0
        while d%p==0: d//=p; l+=1
        m=0
        while d%q==0: d//=q; m+=1
        return (l,m)
    def digit(Sset):
        T=[0]
        for s in Sset:
            pr=p if s%p==0 else q; Mp=M
            while Mp%pr==0: Mp//=pr
            e=0; x=s
            while x%pr==0: x//=pr; e+=1
            g=pr**(e-1)*Mp; T=[(t+c*g)%M for t in T for c in range(pr)]
        return sorted(T)
    def random_tile(B):
        cov=[False]*M; A=[]
        for c in B: cov[c]=True
        A=[0]
        order=list(range(M)); 
        while True:
            x=next((i for i in range(M) if not cov[i]),None)
            if x is None: return A
            cand=[(x-b)%M for b in B if not any(cov[((x-b)+c)%M] for c in B)]
            if not cand: return None
            t=random.choice(cand)
            for c in B: cov[(t+c)%M]=True
            A.append(t)
    def zeros(A):
        Z=set()
        for d in range(2,M+1):
            if M%d==0 and abs(sum(cmath.exp(2j*cmath.pi*x/d) for x in A))<1e-7: Z.add(order_of(d))
        return Z
    PP=[p,p*p,q,q*q]; tested=0; bad=0; charged=0; ncomp=0
    tot=[float(S.C[((0,0),cl)]) for cl in S.cls]
    for _ in range(ntiles):
        Sset=random.choice([c for r in range(1,4) for c in itertools.combinations(PP,r)])
        A=None
        for _try in range(20):
            A=random_tile(digit(Sset))
            if A: break
        if not A: continue
        Z=zeros(A)
        if (1,0) not in Z: continue
        if not all((1,m) in Z for m in (1,2) if (0,m) in Z): continue      # level-one (T2) for p
        v=S.solve(Z)[0]
        for k in range(4):
            obj=[random.random() for _ in S.cls]
            r=S.solve(Z,obj=obj,extra_eq=[(tot,v)])
            if r is None: continue
            g=r[1]; ncomp+=1
            f=np.array([g[cls(x)] for x in range(M)])
            if sum(f[x] for x in range(M) if x%p)>1e-9: charged+=1
            # fold along the p-direction: shift by delta*e with e = the element (1,0) of Z_{p^2} x Z_{q^2}
            e=next(x for x in range(M) if x%(p*p)==1 and x%(q*q)==0)
            fp=np.array([sum(f[(x+d*e)%M] for d in range(p)) if x%p==0 else 0.0 for x in range(M)])
            conv=np.array([sum(fp[(vv-a)%M] for a in A) for vv in range(M)])
            tested+=1
            if abs(fp[0]-1)>1e-7 or np.max(np.abs(conv-1))>1e-7 or fp.min()<-1e-9: bad+=1
    return tested,bad,ncomp,charged
for (p,q) in [(2,3),(3,2)]:
    t,b,n,c=run(p,q)
    print('(p,q)=',(p,q),': folds tested',t,' failures',b,' | complements that charged numbers prime to p before folding:',c,'of',n)
