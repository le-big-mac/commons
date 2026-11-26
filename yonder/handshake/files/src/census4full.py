"""Strict-Nash census among ALL machines with <= 4 states (57,068), in two stages:
1. screen every machine against the 1,054 invaders with <= 3 states;
2. test the survivors against all 57,068."""
import sys, time, pickle, numpy as np
from multiprocessing import Pool
import census
from census import enumerate_machines, pad
from ipd import PAY
EPS=float(sys.argv[2]); DELTA=float(sys.argv[3]); S=4

def init(p,n,sub):
    global PLAY,NXT,SUB
    PLAY,NXT,SUB=p,n,sub

def versus(i, J):
    """returns (payoff to i vs each j in J, payoff to each j vs i)"""
    K=len(J); N=S*S
    pa=np.where(PLAY[i][:,None]==np.arange(2),1-EPS,EPS)
    pb=np.where(PLAY[J][:,:,None]==np.arange(2),1-EPS,EPS)
    pj=pa[None,:,None,:,None]*pb[:,None,:,None,:]
    ua=(pj*PAY).sum((3,4)).reshape(K,N); ub=(pj*PAY.T).sum((3,4)).reshape(K,N)
    P=np.zeros((K,N,N))
    kk=np.broadcast_to(np.arange(K)[:,None,None],(K,S,S))
    src=np.broadcast_to(np.arange(S)[None,:,None]*S+np.arange(S)[None,None,:],(K,S,S))
    for x in (0,1):
        for y in (0,1):
            dst=NXT[i][:,y][None,:,None]*S+NXT[J][:,:,x][:,None,:]
            np.add.at(P,(kk,src,dst),pj[:,:,:,x,y])
    A=np.eye(N)[None]-DELTA*np.transpose(P,(0,2,1))
    e0=np.zeros((K,N,1)); e0[:,0,0]=1
    occ=(1-DELTA)*np.linalg.solve(A,e0)[:,:,0]
    return (occ*ua).sum(1),(occ*ub).sum(1)

def screen(i):
    u,v=versus(i,SUB)
    self_=versus(i,np.array([i]))[0][0]
    return self_, v.max()   # SUB includes i itself possibly (v==self then); strictness handled later

def full(i):
    K=PLAY.shape[0]; best=-1; arg=-1
    self_=versus(i,np.array([i]))[0][0]
    for a in range(0,K,4000):
        J=np.arange(a,min(a+4000,K))
        v=versus(i,J)[1]
        v[J==i]=-1
        j=int(np.argmax(v))
        if v[j]>best: best=v[j]; arg=int(J[j])
    return self_,best,arg

if __name__=="__main__":
    t=time.time()
    ms=enumerate_machines(S); K=len(ms)
    sub=np.array([i for i,m in enumerate(ms) if m.n<=3])
    print("machines",K,"screen set",len(sub),flush=True)
    play,nxt=pad(ms,S)
    with Pool(14,initializer=init,initargs=(play,nxt,sub)) as p:
        sc=p.map(screen,range(K),chunksize=64)
        sc=np.array(sc)
        surv=[i for i in range(K) if sc[i,1]<=sc[i,0]+1e-12]
        print("survive the <=3-state screen:",len(surv),"time",round(time.time()-t),flush=True)
        out=p.map(full,surv,chunksize=1)
    nash=[(i,s,b,a) for i,(s,b,a) in zip(surv,out) if s>b+1e-10]
    print("strict Nash among all",K,":",len(nash),"time",round(time.time()-t))
    for i,s,b,a in sorted(nash,key=lambda r:-r[1]):
        print(f"  self {s:.4f} margin {s-b:.5f} {ms[i]}   runner-up invader {ms[a]}")
    near=sorted([(s-b,i,s,a) for i,(s,b,a) in zip(surv,out) if s<=b+1e-10 and s>2],reverse=True)[:10]
    print("cooperative near-misses (self>2), smallest deficits:")
    for d,i,s,a in near: print(f"  self {s:.4f} deficit {d:.5f} {ms[i]}  beaten by {ms[a]}")
    pickle.dump((nash,near),open(f"census4_{EPS}.pkl","wb"))
