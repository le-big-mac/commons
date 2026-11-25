import numpy as np, json
from multiprocessing import Pool
from couzin import School
def run(a):
    dro,seed=a; s=School(ro=1+dro,seed=seed); out=[]
    for t in range(30000):
        s.step()
        if t%500==499:
            p,m,n,k=s.order_largest(); out.append('A' if p>.65 and p>m else ('M' if m>.5 else '.'))
    return dro,seed,''.join(out)
if __name__=='__main__':
    with Pool(15) as p: res=p.map(run,[(d,k) for d in (2.5,6.0) for k in range(12)],chunksize=1)
    json.dump(res,open('long.json','w'))
    for r in res: print(r[0],r[1],r[2])
