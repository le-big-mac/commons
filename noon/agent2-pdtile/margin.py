# How close do the rejected candidates come to pd-tiling?  max f(0) over f>=0, fhat>=0 supported on zeros(A)+{0}, fhat(0)=M/|A|.
# A pd-tiles iff this maximum reaches 1.
import numpy as np, sys
from multiprocessing import Pool
from scipy.optimize import linprog
def chunk(a):
    M,b=a; X=((b[:,None]>>np.arange(M))&1).astype(float); zero=np.abs(np.fft.fft(X,axis=1))<1e-9; out=[]
    for i in range(len(b)):
        Z=np.nonzero(zero[i])[0]; n=X[i].sum(); C=np.cos(2*np.pi*np.outer(np.arange(M),Z)/M)/M
        r=linprog(-np.ones(len(Z))/M,A_ub=-C,b_ub=np.full(M,1/n),bounds=[(0,None)]*len(Z),method='highs')
        out.append(1/n-r.fun)
    return out
if __name__=='__main__':
    M=int(sys.argv[1]); b=np.loadtxt(sys.argv[2],dtype=np.int64)
    with Pool(14) as p: v=np.concatenate(p.map(chunk,[(M,b[i:i+2000]) for i in range(0,len(b),2000)]))
    yes=v>1-1e-7; print(M,'reach 1:',int(yes.sum()),' of',len(v)); w=v[~yes]
    print('rejected: largest max f(0) =',w.max(),' smallest =',w.min(),' accepted: smallest =',v[yes].min(),' largest =',v[yes].max())
