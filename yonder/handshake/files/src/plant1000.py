from multiprocessing import Pool
from evolve import run
from ipd import M
h=M("h",0,[("D",0,1),("D",0,2),("C",2,0)])
jobs=[(e,0.99,7000+s,60000,1000,0.001,1.0,0.0,h) for e in (0.03,0.05) for s in range(3)]
def one(j):
    r=run(j); return (j[0],j[2],round(float(r["series"][:,1].mean()),3),round(float(r["series"][-200:,1].mean()),3),r["dom"][:2])
if __name__=="__main__":
    with Pool(6) as p:
        for r in p.imap_unordered(one,jobs): print(r,flush=True)
