"""Problem 1.1 of Kiss-Londner-Matolcsi-Somlai (arXiv 2411.03854): if A pd-tiles Z_M, must A tile Z_M properly?
Brute force over all subsets A of Z_M containing 0, for small M.
pd-tiling: exists f with f(0)=1, f>=0, fhat>=0, 1_A * f = 1."""
import numpy as np, sys, itertools
from scipy.optimize import linprog
def tiles(A,M):
    A=list(A); cov=[False]*M
    def bt():
        try: i=cov.index(False)
        except ValueError: return True
        for x in A:
            t=(i-x)%M; cells=[(t+y)%M for y in A]
            if any(cov[c] for c in cells): continue
            for c in cells: cov[c]=True
            if bt(): return True
            for c in cells: cov[c]=False
        return False
    return bt()
def pd_tiles(A,M,zeros):
    # fhat supported on {0} U zeros(A), fhat>=0, fhat(0)=M/|A|; f(z)=(1/M) sum_xi fhat(xi) cos(2 pi z xi/M) >=0; f(0)=1
    Z=[int(x) for x in zeros]; k=len(Z)
    if k==0: return False
    z=np.arange(M); C=np.cos(2*np.pi*np.outer(z,Z)/M)/M          # f = 1/|A| + C c
    r=linprog(np.zeros(k),A_ub=-C,b_ub=np.full(M,1/len(A)),A_eq=np.ones((1,k))/M,b_eq=[1-1/len(A)],bounds=[(0,None)]*k,method='highs')
    return r.status==0
def study(M):
    bits=np.arange(1,2**(M-1)*2,2,dtype=np.int64)          # subsets containing 0
    out={'pd':0,'tile':0,'pd_not_tile':[],'tile_not_pd':[]}
    for lo in range(0,len(bits),1<<18):
        b=bits[lo:lo+(1<<18)]; X=((b[:,None]>>np.arange(M))&1).astype(float)
        F=np.abs(np.fft.fft(X,axis=1)); zero=F<1e-9; sz=X.sum(1)
        cand=np.nonzero(zero[:,1:].any(1)&(sz>1)&(sz<M))[0]
        for i in cand:
            A=np.nonzero(X[i])[0]
            if A[1]>M-A[-1]: continue                      # cheap partial symmetry reduction (translation): first gap <= wrap gap
            p=pd_tiles(A,M,np.nonzero(zero[i])[0]); t=(M%len(A)==0) and tiles(A,M)
            out['pd']+=p; out['tile']+=t
            if p and not t: out['pd_not_tile'].append(A.tolist())
            if t and not p: out['tile_not_pd'].append(A.tolist())
    return out
if __name__=='__main__':
    for M in [int(x) for x in sys.argv[1:]]:
        o=study(M); print(M,'pd-tiling sets',o['pd'],'tiling sets',o['tile'],'pd but not tiling',len(o['pd_not_tile']),o['pd_not_tile'][:5],'tiling but not pd',len(o['tile_not_pd']),flush=True)
