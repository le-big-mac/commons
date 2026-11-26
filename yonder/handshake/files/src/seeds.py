import pickle, numpy as np, time
from multiprocessing import Pool
from evolve import run
jobs=[(e,0.99,100+s,200000,100,0.01,1.0,0.0) for e in (0.0,0.01,0.03,0.05) for s in range(12)]
if __name__=="__main__":
    t=time.time()
    with Pool(8) as p: res=p.map(run,jobs,chunksize=1)
    pickle.dump([(r["eps"],r["seed"],float(r["series"][:,1].mean()),r["dom"][:5]) for r in res],open("seeds.pkl","wb"))
    for e in (0.0,0.01,0.03,0.05):
        c=np.array([r["series"][:,1].mean() for r in res if r["eps"]==e])
        print(f"noise {e}: mean coop {c.mean():.3f}  sd {c.std(ddof=1):.3f}  se {c.std(ddof=1)/np.sqrt(len(c)):.3f}  min {c.min():.2f} max {c.max():.2f}  seeds {np.round(np.sort(c),2)}")
    print("time",time.time()-t)
