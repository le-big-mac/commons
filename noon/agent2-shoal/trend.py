import numpy as np, json
from multiprocessing import Pool
from couzin import School
def run(a):
    dro,seed=a; s=School(ro=1+dro,seed=1000+seed)
    for t in range(4000): s.step()
    P=[];M=[]
    for t in range(500):
        s.step()
        if t%50==0: p,m,n,k=s.order_largest(); P.append(p); M.append(m)
    p,m=np.mean(P),np.mean(M)
    return dro,seed,'A' if p>.65 and p>m else ('M' if m>.5 else '.'),n,k
if __name__=='__main__':
    with Pool(15) as p: res=p.map(run,[(d,k) for d in (2,3,4,5,6,7,8) for k in range(40)],chunksize=2)
    json.dump(res,open('trend.json','w'))
    for d in (2,3,4,5,6,7,8):
        r=[x for x in res if x[0]==d]; print(d,'mills',sum(x[2]=='M' for x in r),'aligned',sum(x[2]=='A' for x in r),'other',sum(x[2]=='.' for x in r),'mean groups',np.mean([x[4] for x in r]))
