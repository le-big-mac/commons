import numpy as np, json, sys
from multiprocessing import Pool
from ev import *
P=pool(); names=list(P); opps=[P[n] for n in names]
def fit(m):
    mine=np.array([score(m,o) for o in opps]); theirs=np.array([score(o,m) for o in opps]); s=score(m,m)
    inv=np.maximum(theirs-s,0).max()          # can any pool member invade a population of me?
    return (mine.sum()+s)/(len(opps)+1)+0.5*s-3*inv, mine.mean(), s, inv
def run(seed):
    r=np.random.default_rng(seed); n=8
    m=[r.integers(0,2,n),r.integers(0,n,n),r.integers(0,n,n),0]; m[0][0]=0
    best=fit(tuple(m)); stale=0
    while stale<4000:
        c=[x.copy() if hasattr(x,'copy') else x for x in m]
        for _ in range(r.integers(1,3)):
            k=r.integers(0,3); i=r.integers(0,n)
            c[k][i]=1-c[k][i] if k==0 else r.integers(0,n)
        f=fit(tuple(c))
        if f[0]>=best[0]:
            stale=0 if f[0]>best[0]+1e-9 else stale+1; m,best=c,f
        else: stale+=1
    return best,[x.tolist() if hasattr(x,'tolist') else x for x in m]
if __name__=='__main__':
    with Pool(14) as p: res=p.map(run,range(42))
    res.sort(key=lambda x:-x[0][0])
    for b,m in res[:6]: print([round(float(x),3) for x in b],m)
    json.dump(res[0][1],open('best.json','w'))
