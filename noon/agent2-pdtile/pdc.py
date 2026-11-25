import numpy as np, sys
from multiprocessing import Pool
from pd import tiles, pd_tiles
def chunk(a):
    M,b=a; X=((b[:,None]>>np.arange(M))&1).astype(float); zero=np.abs(np.fft.fft(X,axis=1))<1e-9; o=[0,0,[],[]]
    for i in range(len(b)):
        A=np.nonzero(X[i])[0]; p=pd_tiles(A,M,np.nonzero(zero[i])[0]); t=(M%len(A)==0) and tiles(A,M)
        o[0]+=p; o[1]+=t
        if p and not t: o[2].append(A.tolist())
        if t and not p: o[3].append(A.tolist())
    return o
if __name__=='__main__':
    M=int(sys.argv[1]); b=np.loadtxt(sys.argv[2],dtype=np.int64); tot=[0,0,[],[]]; step=5000; done=0
    with Pool(15) as p:
        for o in p.imap_unordered(chunk,[(M,b[i:i+step]) for i in range(0,len(b),step)]):
            for k in range(4): tot[k]+=o[k]
            done+=1
            if done%100==0: print('progress',done*step,'of',len(b),tot[0],tot[1],len(tot[2]),len(tot[3]),flush=True)
    print(M,'classes that pd-tile',tot[0],'classes that tile',tot[1],'pd but not tiling',len(tot[2]),tot[2][:5],'tiling but not pd',len(tot[3]),flush=True)
