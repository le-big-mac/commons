"""Consistency: every zero pattern of an actual tile of Z_36 must be in category 'a', 'RP' or 'RQ' (never b, H, N),
or among the 64 patterns of Lemma 2 -- and then the tile must lie in 2Z or 3Z."""
import json, itertools, cmath
from collections import defaultdict, Counter
p,q,M=2,3,36
def order_of(d):
    l=0
    while d%p==0: d//=p; l+=1
    m=0
    while d%q==0: d//=q; m+=1
    return (l,m)
def digit(S):
    T=[0]
    for s in S:
        pr=p if s%p==0 else q; Mp=M
        while Mp%pr==0: Mp//=pr
        e=0; x=s
        while x%pr==0: x//=pr; e+=1
        g=pr**(e-1)*Mp; T=[(t+c*g)%M for t in T for c in range(pr)]
    return sorted(T)
def tiles_with(B):
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
    for c in B: cov[c]=True
    rec([0]); return out
def zeros(A):
    Z=set()
    for d in range(2,M+1):
        if M%d==0 and abs(sum(cmath.exp(2j*cmath.pi*x/d) for x in A))<1e-7: Z.add(order_of(d))
    return frozenset(Z)
cert={(tuple(e['Ep']),tuple(e['Eq']),tuple(tuple(x) for x in e['F'])):e['cat'] for e in json.load(open('../certificates_p2q2.json')) if e['regime']=='A'}
pat=defaultdict(lambda:[0,0])
for r in range(1,5):
    for S in itertools.combinations([2,4,3,9],r):
        for A in tiles_with(digit(S)):
            Z=zeros(A); pat[Z][0]+=1
            if all(x%p==0 for x in A) or all(x%q==0 for x in A): pat[Z][1]+=1
c=Counter(); bad=[]
for Z,(n,nsub) in pat.items():
    Ep=tuple(sorted(l for (l,m) in Z if m==0)); Eq=tuple(sorted(m for (l,m) in Z if l==0)); F=tuple(sorted((l,m) for (l,m) in Z if l and m))
    if 1 not in Ep and 1 not in Eq:
        c['Lemma2']+=1
        if nsub!=n: bad.append(('not in subgroup',Z))
    else:
        cat=cert[(Ep,Eq,F)]; c[cat]+=1
        if cat not in ('a','RP','RQ'): bad.append((cat,Z))
print('tile patterns of Z_36:',len(pat),dict(c),' inconsistencies:',bad)
