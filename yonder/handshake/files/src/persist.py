from multiprocessing import Pool
from evolve import run
from ipd import M
h=M("h",0,[("D",0,1),("D",0,2),("C",2,0)])
jobs=[(0.1,0.99,s,40000,N,1.0/N,1.0,0.0,h) for N in (100,400) for s in range(4)]+[(0.05,0.99,s,40000,100,0.01,1.0,0.0,h) for s in range(4)]
if __name__=="__main__":
    with Pool(12) as p: res=p.map(run,jobs,chunksize=1)
    for r in res:
        s=r["series"]; c=s[:,1]
        # first generation where cooperation falls below 0.3
        import numpy as np
        low=np.where(c<0.3)[0]
        print(f"eps {r['eps']} N {r['N']} seed {r['seed']}: mean coop {c.mean():.2f}; first collapse at gen {int(s[low[0],0]) if len(low) else 'never'}")
