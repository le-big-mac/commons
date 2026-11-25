"""Weak Sands test at M = p^2 q^2 (default 36): for every tile A (0 in A), with zero pattern Z:
 is it true that A in pZ, or A in qZ, or every optimal step complement lives in pZ, or every one lives in qZ?"""
import sys, itertools, cmath
from collections import defaultdict
from steplp import Step
p,q=int(sys.argv[1]),int(sys.argv[2]); a=b=2; M=p*p*q*q; S=Step(p,a,q,b)
PP=[p,p*p,q,q*q]
def g(s):
    pr=p if s%p==0 else q; Mp=M
    while Mp%pr==0: Mp//=pr
    e=0; x=s
    while x%pr==0: x//=pr; e+=1
    return pr**(e-1)*Mp, pr
def digit(Sset):
    T=[0]
    for s in Sset:
        gs,pr=g(s); T=[(t+c*gs)%M for t in T for c in range(pr)]
    return sorted(T)
def tiles_with(B):
    """all A containing 0 with A + B = Z_M (exact cover)."""
    out=[]; cov=[False]*M
    def rec(A):
        x=next((i for i in range(M) if not cov[i]),None)
        if x is None: out.append(tuple(sorted(A))); return
        for bb in B:
            t=(x-bb)%M; cells=[(t+c)%M for c in B]
            if any(cov[c] for c in cells): continue
            for c in cells: cov[c]=True
            A.append(t); rec(A); A.pop()
            for c in cells: cov[c]=False
    # force 0 in A
    for c in B: cov[c]=True
    rec([0]); return out
def zeros(A):
    Z=set()
    for d in range(2,M+1):
        if M%d: continue
        w=cmath.exp(2j*cmath.pi/d)
        if abs(sum(w**x for x in A))<1e-7: Z.add(S.order_of(d))
    return frozenset(Z)
pat=defaultdict(lambda:[0,0,None])    # pattern -> [count, count not in pZ nor qZ, example]
for r in range(5):
    for Sset in itertools.combinations(PP,r):
        B=digit(Sset)
        if len(B)==1: continue
        As=tiles_with(B)
        for A in As:
            Z=zeros(A); e=pat[Z]; e[0]+=1
            if any(x%p for x in A) and any(x%q for x in A):
                e[1]+=1
                if e[2] is None: e[2]=A
print('M',M,'patterns of tiles:',len(pat),' tiles:',sum(e[0] for e in pat.values()))
viol=0
for Z,e in sorted(pat.items(),key=lambda t:sorted(t[0])):
    v,mp,mq,both=S.face(Z)
    freeA = e[1]>0
    okf = (mp is not None and mp<1e-7) or (mq is not None and mq<1e-7)
    flag = '' if (okf or not freeA) else '  <-- weak Sands FAILS'
    if flag: viol+=1
    print(sorted(Z),'n=%d free=%d'%(e[0],e[1]),' |A|=%.3f'%(M/v),' max mass off pZ %.4f, off qZ %.4f'%(mp,mq),flag, e[2] if flag else '')
print('violations:',viol)
