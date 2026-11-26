import pickle, numpy as np, time, sys
from multiprocessing import Pool
from evolve import run
EPS=(0.0,0.005,0.01,0.02,0.03,0.05,0.07,0.1); DEL=(0.95,0.98,0.99)
jobs=[(e,d,1000+s,200000,100,0.01,1.0,0.0) for d in DEL for e in EPS for s in range(12)]
def one(j):
    r=run(j); return (j[0],j[1],j[2],float(r["series"][:,1].mean()),float(r["series"][:,2].mean()),r["dom"][:4])
if __name__=="__main__":
    t=time.time(); out=[]
    with Pool(5) as p:
        for k,r in enumerate(p.imap_unordered(one,jobs,chunksize=1)):
            out.append(r)
            if k%12==11: pickle.dump(out,open("curve.pkl","wb")); print(k+1,"of",len(jobs),round(time.time()-t),flush=True)
    pickle.dump(out,open("curve.pkl","wb")); print("done",time.time()-t)
