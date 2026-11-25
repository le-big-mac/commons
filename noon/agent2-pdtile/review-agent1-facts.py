# Independent check of Facts 1-3 of Noon's flatness.md on ALL subsets of Z_M for small M = p^a q^b (vectorised).
# Phi_d | A(X) is tested by evaluating the mask polynomial at a primitive d-th root of unity; a nonzero value is an
# algebraic integer of degree <= phi(d) with conjugates bounded by M, so it cannot be below ~1e-6 here (tolerance 1e-8).
import numpy as np, sys
def subsets(M):
    m=np.arange(1,1<<M,dtype=np.int64)[:,None]; return ((m>>np.arange(M))&1).astype(np.float64)
def run(p,al,q,be):
    M=p**al*q**be; xs=np.arange(M); S=subsets(M); bad=0; hits={}
    for a in range(al+1):
        for b in range(be+1):
            d=p**a*q**b
            if d==1: continue
            div=np.abs(S@np.exp(2j*np.pi*xs/d))<1e-8
            P=np.zeros((M,p**a*q**b)); P[xs,(xs%p**a)*q**b+(xs%q**b)]=1
            N=(S@P).reshape(-1,p**a,q**b)                      # N[set, r, t]
            cond=np.ones(len(S),bool)
            if a>=1 and b==0:
                for i in range(1,p): cond&=np.all(np.roll(N,-i*p**(a-1),axis=1)==N,axis=(1,2))
            elif a==0:
                for i in range(1,q): cond&=np.all(np.roll(N,-i*q**(b-1),axis=2)==N,axis=(1,2))
            else:
                for i in range(1,p):
                    diff=np.roll(N,-i*p**(a-1),axis=1)-N          # diff[set, r, t]
                    for j in range(1,q): cond&=np.all(np.roll(diff,-j*q**(b-1),axis=2)==diff,axis=(1,2))
            bad+=int((div!=cond).sum()); hits[d]=int(div.sum())
    print(f'M={M}={p}^{al}*{q}^{be}: {len(S)} nonempty subsets; Facts 1-2 mismatches {bad}; number of sets with Phi_d | A, by d: {hits}',flush=True)
    Mq=M//q; xq=np.arange(Mq); Sq=subsets(Mq); bad3=0
    for d in [d for d in range(2,M+1) if M%d==0]:
        emb=np.zeros((Mq,M)); emb[xq,q*xq]=1
        lhs=np.abs((Sq@emb)@np.exp(2j*np.pi*xs/d))<1e-8
        e=d//np.gcd(d,q); rhs=np.abs(Sq@np.exp(2j*np.pi*xq/e))<1e-8
        bad3+=int((lhs!=rhs).sum())
    print(f'   Fact 3: {len(Sq)} subsets of qZ_M x {sum(1 for d in range(2,M+1) if M%d==0)} divisors; mismatches {bad3}',flush=True)
for args in [(2,2,3,1),(2,1,3,2),(3,1,2,2),(3,2,2,1)]: run(*args)
