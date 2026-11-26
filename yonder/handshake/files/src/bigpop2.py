import pickle, numpy as np, time
from multiprocessing import Pool
from evolve import run
jobs=[(e,0.99,3000+s,100000,1000,0.01,1.0,0.0) for e in (0.0,0.02) for s in range(3)]
def one(j):
    r=run(j); return (j[0],j[4],j[2],float(r["series"][:,1].mean()),r["dom"][:4])
if __name__=="__main__":
    t=time.time()
    with Pool(6) as p:
        for k,r in enumerate(p.imap_unordered(one,jobs,chunksize=1)): print(k+1,r,round(time.time()-t),flush=True)
    print("done")
