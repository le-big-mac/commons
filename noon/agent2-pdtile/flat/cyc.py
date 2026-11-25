"""Integer cyclotomic polynomials and residues x^i mod Phi_d (exact)."""
from functools import lru_cache
def polymul(a,b):
    r=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        if x:
            for j,y in enumerate(b): r[i+j]+=x*y
    return r
def polydivexact(a,b):
    a=a[:]; q=[0]*(len(a)-len(b)+1)
    for i in range(len(q)-1,-1,-1):
        c=a[i+len(b)-1]//b[-1]; q[i]=c
        for j,y in enumerate(b): a[i+j]-=c*y
    assert not any(a),'inexact division'
    return q
@lru_cache(None)
def Phi(n):
    """coefficients, lowest degree first"""
    p=[-1]+[0]*(n-1)+[1]
    for d in range(1,n):
        if n%d==0: p=polydivexact(p,list(Phi(d)))
    return tuple(p)
@lru_cache(None)
def residues(d,M):
    """R[i] = coefficient vector (length phi(d)) of x^i mod Phi_d, for i < M"""
    P=Phi(d); k=len(P)-1; R=[]; v=[1]+[0]*(k-1) if k>0 else []
    for i in range(M):
        R.append(tuple(v))
        top=v[-1]; v=[0]+v[:-1]                      # multiply by x
        if top: v=[a-top*b for a,b in zip(v,P[:k])]  # x^k = -(lower part of Phi)
    return R
def zero_set(A,M):
    """orders d>1, d|M, with Phi_d | A(x); exact integer arithmetic"""
    Z=[]
    for d in range(2,M+1):
        if M%d==0:
            R=residues(d,M); k=len(R[0])
            if all(sum(R[a][j] for a in A)==0 for j in range(k)): Z.append(d)
    return Z
if __name__=='__main__':
    assert Phi(12)==(1,0,-1,0,1) and Phi(6)==(1,-1,1) and Phi(9)==(1,0,0,1,0,0,1)
    print(zero_set([0,3],12), zero_set([0,1,2,6,7,8],12), zero_set([0,1,5,6,12,25,29,36,42,48,49,53],72), zero_set([0,8,10,18,26,64],72))
    print(max(abs(c) for d in (2,3,4,6,8,9,12,16,18,24,36,48,72,144) for r in residues(d,144) for c in r))
