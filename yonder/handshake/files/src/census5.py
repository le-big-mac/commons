"""Strict-Nash census among ALL behaviourally distinct machines with <= S states (S=5: millions), staged:
 1. every machine vs the 1,054 invaders with <= 3 states
 2. survivors vs all invaders with <= 4 states
 3. survivors vs everything."""
import sys, time, pickle, itertools, numpy as np
from multiprocessing import Pool
from ipd import FSM, canonical, PAY
S=int(sys.argv[1]); EPS=float(sys.argv[2]); DELTA=float(sys.argv[3])

def bfs_tables(n):
    """all transition tables on n states in BFS-canonical labelling with every state reachable"""
    out=[]; t=[0]*(2*n)
    def rec(pos,m):
        if pos==2*n:
            if m==n-1: out.append(tuple(t))
            return
        i=pos//2
        if i>m: return           # state i not discovered yet -> unreachable
        for v in range(min(m+1,n-1)+1):
            t[pos]=v; rec(pos+1,max(m,v))
    rec(0,0); return out

def minimal(play,nxt,n):
    cls=list(play)
    while True:
        sig={}; new=[sig.setdefault((cls[s],cls[nxt[s][0]],cls[nxt[s][1]]),len(sig)) for s in range(n)]
        if len(sig)==len(set(cls)): return len(sig)==n
        cls=new

def machines_of_size(n):
    P=[];N=[]
    for tb in bfs_tables(n):
        nx=[(tb[2*i],tb[2*i+1]) for i in range(n)]
        for play in itertools.product((0,1),repeat=n):
            if minimal(play,nx,n): P.append(play+(0,)*(S-n)); N.append(nx+[(s,s) for s in range(n,S)])
    return np.array(P,dtype=np.int8),np.array(N,dtype=np.int8)

def init(p,n):
    global PLAY,NXT
    PLAY,NXT=p,n

def versus(i,J,IP=None,IN=None):
    if IP is None: IP=PLAY[J]; IN=NXT[J]
    K=len(IP); N=S*S
    pa=np.where(PLAY[i][:,None]==np.arange(2),1-EPS,EPS)
    pb=np.where(IP[:,:,None]==np.arange(2),1-EPS,EPS)
    pj=pa[None,:,None,:,None]*pb[:,None,:,None,:]
    ub=(pj*PAY.T).sum((3,4)).reshape(K,N)
    P=np.zeros((K,N,N))
    kk=np.broadcast_to(np.arange(K)[:,None,None],(K,S,S))
    src=np.broadcast_to(np.arange(S)[None,:,None]*S+np.arange(S)[None,None,:],(K,S,S))
    ni=NXT[i].astype(np.int64); nj=IN.astype(np.int64)
    for x in (0,1):
        for y in (0,1):
            dst=ni[:,y][None,:,None]*S+nj[:,:,x][:,None,:]
            np.add.at(P,(kk,src,dst),pj[:,:,:,x,y])
    A=np.eye(N)[None]-DELTA*np.transpose(P,(0,2,1))
    e0=np.zeros((K,N,1)); e0[:,0,0]=1
    occ=(1-DELTA)*np.linalg.solve(A,e0)[:,:,0]
    return (occ*ub).sum(1)          # payoff to each invader j against i

def stage(arg):
    i,lo,hi=arg
    self_=versus(i,np.array([i]))[0]; best=-1.0; arg_=-1
    step=200 if hi<5000 else 3000
    for a in range(lo,hi,step):
        J=np.arange(a,min(a+step,hi)); v=versus(i,J); v[J==i]=-1
        j=int(np.argmax(v))
        if v[j]>best: best=float(v[j]); arg_=int(J[j])
        if best>self_+1e-10: break           # already beaten: stop early
    return self_,best,arg_

def mutants(i):
    """best payoff any one-step mutant (within S states) earns against i"""
    p=PLAY[i]; n=NXT[i]; P=[];Nn=[]
    me=canonical(FSM(0,p,n.astype(int))).key()
    def add(q,m):
        if canonical(FSM(0,q,m.astype(int))).key()!=me: P.append(q); Nn.append(m)
    for a in range(S):
        q=p.copy(); q[a]^=1; add(q,n)
        for x in (0,1):
            for t in range(S):
                if t!=n[a,x]:
                    m=n.copy(); m[a,x]=t; add(p,m)
    if not P: return versus(i,np.array([i]))[0],-1.0,-1
    self_=versus(i,np.array([i]))[0]
    v=versus(i,None,np.array(P),np.array(Nn))
    return self_,float(v.max()),-1

def show(i):
    n=int((np.arange(S)!=NXT[i][:,0]).sum()>=0)   # placeholder
    return repr(canonical(FSM(0,PLAY[i],NXT[i].astype(int))))

if __name__=="__main__":
    t=time.time()
    with Pool(5) as p: parts=p.map(machines_of_size,range(1,S+1))
    sizes=[len(a[0]) for a in parts]; cum=np.cumsum(sizes)
    play=np.concatenate([a[0] for a in parts]); nxt=np.concatenate([a[1] for a in parts]); K=len(play)
    print("machines by size",sizes,"total",K,"time",round(time.time()-t),flush=True)
    init(play,nxt)
    surv=list(range(K))
    with Pool(14,initializer=init,initargs=(play,nxt)) as p:
        import os
        for name,hi in (("<=3 states",cum[2]),("<=4 states",cum[3]),("own one-step mutants",-1),("all",K)):
            if hi>K: continue
            ck=f"census{S}_{EPS}_stage_{name.replace(' ','_').replace('<=','le')}.pkl"
            if os.path.exists(ck):
                surv,last=pickle.load(open(ck,"rb")); print("loaded",ck,len(surv),flush=True); continue
            if hi==-1: out=p.map(mutants,surv,chunksize=4)
            else: out=p.map(stage,[(i,0,int(hi)) for i in surv],chunksize=max(1,min(256,len(surv)//200+1)))
            keep=[(i,o) for i,o in zip(surv,out) if o[0]>o[1]+1e-10]
            print(f"stage vs {name}: {len(surv)} -> {len(keep)} survive, time {round(time.time()-t)}",flush=True)
            surv=[i for i,_ in keep]; last=keep
            pickle.dump((surv,last),open(ck,'wb'))
    print("strict Nash:",len(last))
    rows=sorted(last,key=lambda r:-r[1][0])
    for i,(s,b,a) in rows:
        print(f"  self {s:.4f} margin {s-b:.5f} {show(i)}   runner-up {show(a)}")
    pickle.dump([(play[i],nxt[i],o) for i,o in rows],open(f"census{S}_{EPS}.pkl","wb"))
