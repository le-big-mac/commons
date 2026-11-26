import pickle, numpy as np, time
from multiprocessing import Pool
from evolve import run
jobs=[(e,0.99,2000+s,200000,N,1.0/N,1.0,0.0) for N in (400,1000) for e in (0.0,0.02) for s in range(5)]
def one(j):
    r=run(j); return (j[0],j[4],j[2],float(r["series"][:,1].mean()),r["dom"][:4])
if __name__=="__main__":
    t=time.time(); out=[]
    with Pool(5) as p:
        for k,r in enumerate(p.imap_unordered(one,jobs,chunksize=1)):
            out.append(r); pickle.dump(out,open("bigpop.pkl","wb")); print(k+1,r[:4],round(time.time()-t),flush=True)
    print("done")
