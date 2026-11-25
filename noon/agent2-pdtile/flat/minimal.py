"""Which zero-patterns could belong to a pd-tiling SET?
A set A of size n pd-tiles iff D+(Z_A) = n, and D+(Z_A) <= n for every set. D+ is monotone in Z. So A pd-tiles iff
Z_A contains some inclusion-minimal Z0 with D+(Z0) = n. For a set, k(Z_A) := prod of p over prime powers in Z_A divides n.
For each minimal Z0 we report whether it is 'safe':  k(Z0) = n and Z0 is T2-closed  =>  every set A containing it in its
zero set with |A| = n satisfies T1 and T2 and therefore tiles (Coven-Meyerowitz). Unsafe minimal patterns need a search
over actual sets."""
import sys, pickle
from scan import factor
from collections import defaultdict
def analyse(M):
    O,D=pickle.load(open(f'D_{M}.pkl','rb')); n=len(O); N=1<<n
    pp=[d for d in O if len(factor(d))==1]; comp=[d for d in O if len(factor(d))>1]
    exact={d:[p**a for p,a in factor(d).items()] for d in comp}
    out=[]
    for mask in range(1,N):
        v=D[mask]
        if v.denominator!=1: continue
        if all(D[mask^(1<<i)]<v for i in range(n) if mask>>i&1):
            Z=[O[i] for i in range(n) if mask>>i&1]; Zs=set(Z); k=1
            for s in pp:
                if s in Zs: k*=next(iter(factor(s)))
            nn=int(v)
            if nn%k: status='impossible (k does not divide n)'
            elif k==nn and all(d in Zs for d in comp if all(s in Zs for s in exact[d])): status='safe'
            elif k==nn: status='T2-open'
            else: status='T1-short'
            out.append((nn,Z,k,status,[d for d in comp if all(s in Zs for s in exact[d]) and d not in Zs]))
    return out
if __name__=='__main__':
    for M in [int(x) for x in sys.argv[1:] if x.isdigit()]:
        out=analyse(M); c=defaultdict(int)
        for o in out: c[o[3]]+=1
        print(f'M={M}: minimal patterns with integer D+: {len(out)}  ',dict(c))
        byn=defaultdict(lambda: defaultdict(int))
        for nn,Z,k,st,miss in out: byn[nn][st]+=1
        for nn in sorted(byn): print(f'   n={nn}:',dict(byn[nn]))
        if '-v' in sys.argv:
            for nn,Z,k,st,miss in sorted(out):
                if st in('T2-open','T1-short'): print('   ',st,'n=%d k=%d'%(nn,k),'Z0=',Z,'missing T2 products:',miss)
