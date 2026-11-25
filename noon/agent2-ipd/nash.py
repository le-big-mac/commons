# Search for machines that cooperate with themselves AND leave little for any deviator to gain.
import numpy as np, json, sys
from multiprocessing import Pool
from ev import *
def br(m):
    p,c,d,s0=m; n=len(p); R=np.zeros((2,n)); T=np.zeros((2,n,n)); ar=np.arange(n)
    for a in (0,1):
        for fa in (0,1):
            for fb in (0,1):
                pr=(EPS if fa else 1-EPS)*(EPS if fb else 1-EPS); xa=a^fa; xb=p^fb
                R[a]+=pr*np.where(xb==0,3 if xa==0 else 5,0 if xa==0 else 1)
                np.add.at(T[a],(ar,c if xa==0 else d),pr)
    pol=np.zeros(n,int)
    for _ in range(50):
        V=np.linalg.solve(np.eye(n)-D*T[pol,ar],R[pol,ar]); Q=R+D*T@V; new=Q.argmax(0)
        if (new==pol).all(): break
        pol=new
    return (1-D)*V[s0],pol
def fit(m,w):
    m=(np.array(m[0]),np.array(m[1]),np.array(m[2]),m[3]); s=score(m,m); g=br(m)[0]-s
    return s-w*max(g,0), s, g
def run(args):
    seed,w,n=args; r=np.random.default_rng(seed)
    m=[r.integers(0,2,n),r.integers(0,n,n),r.integers(0,n,n),0]; best=fit(m,w); stale=0
    while stale<6000:
        c=[m[0].copy(),m[1].copy(),m[2].copy(),0]
        for _ in range(r.integers(1,4)):
            k=r.integers(0,3); i=r.integers(0,n); c[k][i]=1-c[k][i] if k==0 else r.integers(0,n)
        f=fit(c,w)
        if f[0]>=best[0]: stale=0 if f[0]>best[0]+1e-9 else stale+1; m,best=c,f
        else: stale+=1
    return w,n,best,[x.tolist() for x in m[:3]]
if __name__=='__main__':
    jobs=[(s,w,n) for w in (1,3,10) for n in (4,8,16) for s in range(5)]
    with Pool(15) as p: res=p.map(run,jobs)
    json.dump([(w,n,[float(x) for x in b],m) for w,n,b,m in res],open('nash.json','w'))
    for w in (1,3,10):
        for n in (4,8,16):
            b=max((x for x in res if x[0]==w and x[1]==n),key=lambda x:x[2][0])
            print(f'w={w:2d} n={n:2d}  self {b[2][1]:.3f}  gap {b[2][2]:+.4f}  {b[3]}')
