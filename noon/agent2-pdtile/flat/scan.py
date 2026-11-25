"""For a given M: D+(Z) for every set Z of orders (>1), exactly. Then list the 'tight' Z, those with
D+(Z) * D+(complement) = M, and say whether each satisfies the Coven-Meyerowitz conditions read off Z:
  T1:  D+(Z) = product of p over prime powers p^a in Z
  T2:  if d | M has at least two prime factors and every exact prime-power factor of d is in Z, then d is in Z.
Why this matters: a set A pd-tiles Z_M  iff  D+(Z_A) = |A|, where Z_A = {d : Phi_d | A(x)}; and then (Z_A, complement)
is tight. So if every tight Z satisfies T1 and T2, every pd-tiling set satisfies T1 and T2 and therefore tiles."""
import sys, json, pickle
from fractions import Fraction as Fr
from multiprocessing import Pool
from lp import Setup, divisors
def factor(n):
    f={}; p=2
    while p*p<=n:
        while n%p==0: f[p]=f.get(p,0)+1; n//=p
        p+=1
    if n>1: f[n]=f.get(n,0)+1
    return f
S=None
def init(M):
    global S; S=Setup(M)
def work(args):
    lo,hi=args; out=[]; O=S.orders
    for mask in range(lo,hi):
        Z=[O[i] for i in range(len(O)) if mask>>i&1]
        out.append((mask,S.Dplus(Z)[0]))
    return out
def scan(M,procs=14):
    O=[d for d in divisors(M) if d>1]; n=len(O); N=1<<n; step=max(1,N//(procs*8))
    with Pool(procs,initializer=init,initargs=(M,)) as p:
        res=p.map(work,[(lo,min(lo+step,N)) for lo in range(0,N,step)])
    D=[None]*N
    for chunk in res:
        for mask,v in chunk: D[mask]=v
    return O,D
def classify(M,O,D):
    n=len(O); N=1<<n; full=N-1; idx={d:i for i,d in enumerate(O)}
    pp=[d for d in O if len(factor(d))==1]; comp=[d for d in O if len(factor(d))>1]
    exact={d:[p**a for p,a in factor(d).items()] for d in comp}
    tight=[]; nonint=0
    for mask in range(N):
        if D[mask].denominator!=1: nonint+=1
        if D[mask]*D[full^mask]==M:
            Z=[O[i] for i in range(n) if mask>>i&1]; Zs=set(Z)
            k=1
            for s in pp:
                if s in Zs: k*=next(iter(factor(s)))
            t1=(D[mask]==k)
            t2=all(d in Zs for d in comp if all(s in Zs for s in exact[d]))
            tight.append((mask,Z,D[mask],k,t1,t2))
    return tight,nonint
if __name__=='__main__':
    for M in [int(x) for x in sys.argv[1:]]:
        O,D=scan(M); tight,nonint=classify(M,O,D)
        pickle.dump((O,D),open(f'D_{M}.pkl','wb'))
        ex=[t for t in tight if not (t[4] and t[5])]
        print(f'M={M}: {len(D)} sets of orders; D+ non-integer for {nonint}; tight: {len(tight)}; tight but failing T1 or T2: {len(ex)}',flush=True)
        for mask,Z,d,k,t1,t2 in ex[:40]: print('   Z =',Z,' D+ =',d,' k =',k,' T1' if t1 else ' not T1',' T2' if t2 else ' not T2')
