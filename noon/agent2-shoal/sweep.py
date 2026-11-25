import numpy as np, json, sys
from multiprocessing import Pool
from couzin import School
def run(a):
    dro,seed=a; s=School(ro=1.0+dro,seed=seed); P=[];M=[]
    for t in range(6000):
        s.step()
        if t>=4000 and t%50==0: p,m,n,k=s.order_largest(); P.append(p); M.append(m)
    return dro,seed,float(np.mean(P)),float(np.mean(M)),k,n
if __name__=='__main__':
    jobs=[(d,k) for d in np.round(np.arange(0,8.01,.5),2) for k in range(6)]
    with Pool(15) as p: res=p.map(run,jobs,chunksize=2)
    json.dump(res,open('sweep.json','w'))
    for d in sorted({r[0] for r in res}):
        rs=[r for r in res if r[0]==d]; print(f'dro {d:4.2f}  p {np.mean([r[2] for r in rs]):.2f}  m {np.mean([r[3] for r in rs]):.2f}  frags {np.mean([r[4] for r in rs]):.1f}  largest {np.mean([r[5] for r in rs]):.0f}')
