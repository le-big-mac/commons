"""Weak tiling version of the pipeline in ~/pdflat.
For a modulus M: exact D^w for every pattern (cached W_M.pkl); the weak-minimal patterns (D^w(Z0) = n an integer, every
single removal lowers D^w); their classification read off Z0; and whether D+(Z0) < n (a 'new' pattern, not covered by
the pd computation)."""
import os
HERE=os.path.dirname(os.path.abspath(__file__))
import sys, pickle, os
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','flat'))
from fractions import Fraction as Fr
from multiprocessing import Pool
from lp import divisors
from scan import factor
from weaklp import WSetup
S=None; HAVE_D=False
def init(M,have):
    global S,HAVE_D; S=WSetup(M); HAVE_D=have
def work(args):
    lo,hi=args; O=S.orders; out=[]
    for mask in range(lo,hi):
        Z=[O[i] for i in range(len(O)) if mask>>i&1]
        out.append((mask,S.Dweak(Z)[0],None if HAVE_D else S.Dplus(Z)[0]))
    return out
def scan(M,procs=14):
    fn=os.path.join(HERE,f'W_{M}.pkl')
    if os.path.exists(fn): return pickle.load(open(fn,'rb'))
    O=[d for d in divisors(M) if d>1]; n=len(O); N=1<<n; step=max(1,N//(procs*8))
    dfn=os.path.join(HERE,'..','flat',f'D_{M}.pkl'); Dc=None
    if os.path.exists(dfn):
        O2,Dc=pickle.load(open(dfn,'rb')); assert O2==O
    with Pool(procs,initializer=init,initargs=(M,Dc is not None)) as p:
        res=p.map(work,[(lo,min(lo+step,N)) for lo in range(0,N,step)])
    W=[None]*N; D=[None]*N
    for chunk in res:
        for mask,w,d in chunk: W[mask]=w; D[mask]=Dc[mask] if Dc is not None else d
    pickle.dump((O,W,D),open(fn,'wb')); return O,W,D
def analyse(M,procs=14):
    O,W,D=scan(M,procs); n=len(O); N=1<<n
    pp=[d for d in O if len(factor(d))==1]; comp=[d for d in O if len(factor(d))>1]
    exact={d:[p**a for p,a in factor(d).items()] for d in comp}
    out=[]
    for mask in range(1,N):
        v=W[mask]
        if v.denominator!=1: continue
        if all(W[mask^(1<<i)]<v for i in range(n) if mask>>i&1):
            Z=[O[i] for i in range(n) if mask>>i&1]; Zs=set(Z); k=1
            for s in pp:
                if s in Zs: k*=next(iter(factor(s)))
            nn=int(v)
            if nn%k: status='impossible'
            elif k==nn and all(d in Zs for d in comp if all(s in Zs for s in exact[d])): status='safe'
            elif k==nn: status='T2-open'
            else: status='T1-short'
            out.append((nn,Z,k,status,D[mask]<v))
    ndiff=sum(1 for m in range(N) if W[m]!=D[m])
    return out,ndiff,N
if __name__=='__main__':
    from collections import Counter
    for M in [int(a) for a in sys.argv[1:]]:
        out,ndiff,N=analyse(M)
        c=Counter((st,new) for nn,Z,k,st,new in out)
        print(f'M={M}: {N} patterns, D^w > D+ for {ndiff}; weak-minimal: {len(out)};',{f"{st}{'/new' if new else ''}":v for (st,new),v in sorted(c.items())},flush=True)
