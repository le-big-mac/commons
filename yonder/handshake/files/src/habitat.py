"""Habitat sweep for the field guide: noise x population size, long games. One mutant per generation."""
import pickle, time, sys
from multiprocessing import Pool
from evolve import run
EPS=(0.0,0.005,0.01,0.02,0.03,0.05,0.07,0.1); NS=(50,100,200,400,1000)
jobs=[(e,0.99,5000+s,200000,N,1.0/N,1.0,0.0) for N in NS for e in EPS for s in range(6)]
def one(j):
    r=run(j)
    return dict(eps=j[0],N=j[4],seed=j[2],coop=float(r["series"][:,1].mean()),pay=float(r["series"][:,2].mean()),
                states=float(r["series"][:,3].mean()),occ=r["occ"],dom=r["dom"][:10])
if __name__=="__main__":
    t=time.time(); out=[]
    with Pool(13) as p:
        for k,r in enumerate(p.imap_unordered(one,jobs,chunksize=1)):
            out.append(r)
            if k%10==9: pickle.dump(out,open("habitat.pkl","wb")); print(k+1,"of",len(jobs),round(time.time()-t),flush=True)
    pickle.dump(out,open("habitat.pkl","wb")); print("done",round(time.time()-t))
