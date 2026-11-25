import numpy as np, sys
from multiprocessing import Pool
from pd import tiles, pd_tiles
def chunk(a):
    M,lo,hi=a; b=np.arange(2*lo+1,2*hi+1,2,dtype=np.int64); full=(1<<M)-1
    keep=np.ones(len(b),bool)
    for k in range(1,M): keep&=b<=(((b<<k)|(b>>(M-k)))&full)      # smallest rotation only: one set per translation class
    b=b[keep]; o=[0,0,[],[]]
    if len(b)==0: return o
    X=((b[:,None]>>np.arange(M))&1).astype(float)
    zero=np.abs(np.fft.fft(X,axis=1))<1e-9; sz=X.sum(1)
    for i in np.nonzero(zero[:,1:].any(1)&(sz>1)&(sz<M))[0]:
        A=np.nonzero(X[i])[0]
        p=pd_tiles(A,M,np.nonzero(zero[i])[0]); t=(M%len(A)==0) and tiles(A,M)
        o[0]+=p; o[1]+=t
        if p and not t: o[2].append(A.tolist())
        if t and not p: o[3].append(A.tolist())
    return o
if __name__=='__main__':
    M=int(sys.argv[1]); n=2**(M-1); step=1<<18; tot=[0,0,[],[]]; done=0
    with Pool(15) as p:
        for o in p.imap_unordered(chunk,[(M,lo,min(lo+step,n)) for lo in range(0,n,step)]):
            for k in range(4): tot[k]+=o[k]
            done+=1
            if done%200==0: print('progress',done,'of',n//step,tot[0],tot[1],len(tot[2]),flush=True)
    print(M,'classes that pd-tile',tot[0],'classes that tile',tot[1],'pd but not tiling',len(tot[2]),tot[2][:5],'tiling but not pd',len(tot[3]),flush=True)
