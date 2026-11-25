"""Check the reduction 'A pd-tiles  iff  D+(Z_A) = |A|' against the old per-set floating-point LP (pdtile/pd.py),
which does not use step functions, Ramanujan sums or the exact solver."""
import sys, pickle, random
sys.path.insert(0,'/home/agent2/pdtile')
import numpy as np
from pd import pd_tiles
from cyc import zero_set
from scan import scan
import os
M=int(sys.argv[1]); cand=np.loadtxt(sys.argv[2],dtype=np.int64); limit=int(sys.argv[3]) if len(sys.argv)>3 else len(cand)
if not os.path.exists(f'D_{M}.pkl'):
    O,D=scan(M); pickle.dump((O,D),open(f'D_{M}.pkl','wb'))
O,D=pickle.load(open(f'D_{M}.pkl','rb')); idx={d:i for i,d in enumerate(O)}
random.seed(0); pick=cand if len(cand)<=limit else np.array(random.sample(list(cand),limit))
agree=0; yes=0; bad=[]
for b in pick:
    b=int(b); A=[i for i in range(M) if b>>i&1]
    x=np.zeros(M); x[A]=1; zero=np.nonzero(np.abs(np.fft.fft(x))<1e-9)[0]
    old=pd_tiles(np.array(A),M,zero)
    Z=zero_set(A,M); new=(D[sum(1<<idx[d] for d in Z)]==len(A))
    agree+=(old==new); yes+=new
    if old!=new: bad.append((A,Z,old,new))
print(f'M={M}: {len(pick)} sets compared; agree {agree}; pd-tiling by the new criterion {yes}; disagreements {len(bad)}',bad[:3])
