"""Groundwork for Z_{p^2 q^2} (no claims). For each way of choosing which prime-power cyclotomic factors a set has
(E_p, E_q, each empty or one level) and ONE orphan zero (l, m) with l not in E_p, m not in E_q:
the smallest set A (0 in A) with exactly those prime-power zeros and with Phi_{p^l q^m} | A.
Compared with k = p^|E_p| q^|E_q| and with the product-majorant bound U = k * min(p, q)."""
import sys, itertools, json, time
sys.path.insert(0,'/home/agent2/pdflat')
from ortools.sat.python import cp_model
from sat import count_exprs
from multiprocessing import Pool
LIMIT=int(sys.argv[3]) if len(sys.argv)>3 else 900
def minsize(args):
    p,q,Ep,Eq,orph=args; M=p*p*q*q
    m=cp_model.CpModel(); x=[m.NewBoolVar(f'x{i}') for i in range(M)]; m.Add(x[0]==1)
    res=count_exprs(m,x,M)
    def must(d):
        for e in res(d): m.Add(e==0)
    def mustnot(d):
        lits=[]
        for j,e in enumerate(res(d)):
            a=m.NewBoolVar(f'p{d}_{j}'); b=m.NewBoolVar(f'n{d}_{j}'); m.Add(e>=1).OnlyEnforceIf(a); m.Add(e<=-1).OnlyEnforceIf(b); lits+=[a,b]
        m.AddBoolOr(lits)
    for l in (1,2): (must if l in Ep else mustnot)(p**l)
    for k in (1,2): (must if k in Eq else mustnot)(q**k)
    must(p**orph[0]*q**orph[1])
    kk=p**len(Ep)*q**len(Eq)
    n=m.NewIntVar(1,M,'n'); m.Add(n==sum(x)); mult=m.NewIntVar(1,M//kk,'mult'); m.Add(n==kk*mult)   # k divides |A|
    m.Minimize(n); s=cp_model.CpSolver(); s.parameters.max_time_in_seconds=LIMIT; s.parameters.num_workers=4
    t0=time.time(); st=s.Solve(m)
    if st==cp_model.OPTIMAL: r=('=',int(s.ObjectiveValue()))
    elif st==cp_model.FEASIBLE: r=('in',[int(s.BestObjectiveBound()),int(s.ObjectiveValue())])
    elif st==cp_model.INFEASIBLE: r=('none',None)
    else: r=('?',int(s.BestObjectiveBound()))
    return dict(p=p,q=q,Ep=list(Ep),Eq=list(Eq),orphan=list(orph),k=kk,U=kk*min(p,q),result=r,secs=round(time.time()-t0,1))
if __name__=='__main__':
    p,q=int(sys.argv[1]),int(sys.argv[2]); jobs=[]
    for Ep in ((),(1,),(2,)):
        for Eq in ((),(1,),(2,)):
            for l in (1,2):
                for mm in (1,2):
                    if l not in Ep and mm not in Eq: jobs.append((p,q,Ep,Eq,(l,mm)))
    out=open(f'orphan_min_{p}_{q}.jsonl','a')
    with Pool(4) as pool:
        for r in pool.imap_unordered(minsize,jobs):
            out.write(json.dumps(r)+'\n'); out.flush()
            print(r,flush=True)
