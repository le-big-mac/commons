"""For every T2-open minimal pattern (Z0, n) with M <= 200 (and 400): is there any set at all with |A| = n and zero set
containing Z0?  Plain counts model (no Proposition 3), no violation clause."""
import sys, pickle, os
from multiprocessing import Pool
from minimal import analyse
from sat import search
def job(a):
    M,n,Z=a; name,A,t=search(M,n,Z,time_limit=600,workers=1,formulation='counts',violation=False); return M,n,Z,name,A,t
if __name__=='__main__':
    todo=[]
    for M in list(range(2,201))+[400]:
        if not os.path.exists(f'D_{M}.pkl'): continue
        for n,Z,k,st,miss in analyse(M):
            if st=='T2-open': todo.append((M,n,Z))
    with Pool(8) as p: res=p.map(job,todo,chunksize=1)
    import collections
    print(len(res),'T2-open patterns;',collections.Counter(r[3] for r in res))
    for M,n,Z,name,A,t in res:
        if name!='INFEASIBLE': print('  ',M,n,Z,name,A)
    byM=collections.Counter(r[0] for r in res); print(dict(byM))
