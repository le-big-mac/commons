import sys, itertools
from steplp import Step
def subs(S): return itertools.chain.from_iterable(itertools.combinations(S,r) for r in range(len(S)+1))
def table(p,q):
    S=Step(p,2,q,2); pairs=[(1,1),(1,2),(2,1),(2,2)]; rows={}
    tot=[float(S.C[((0,0),cl)]) for cl in S.cls]
    outp=[tot[k] if cl[0]==0 else 0.0 for k,cl in enumerate(S.cls)]
    outq=[tot[k] if cl[1]==0 else 0.0 for k,cl in enumerate(S.cls)]
    for Ep in subs((1,2)):
        for Eq in subs((1,2)):
            for F in subs(pairs):
                Z={(l,0) for l in Ep}|{(0,m) for m in Eq}|set(F)
                r1 = 1 not in Ep and 1 not in Eq
                r2 = {(2,0),(2,1),(2,2)}<=Z or {(0,2),(1,2),(2,2)}<=Z
                v,g=S.solve(Z)
                mp=S.solve(Z,obj=outp,extra_eq=[(tot,v)])[0]; mq=S.solve(Z,obj=outq,extra_eq=[(tot,v)])[0]
                k=p**len(Ep)*q**len(Eq)
                rows[(Ep,Eq,F)]=(r1,r2,mp<1e-7,mq<1e-7,S.M/v,k)
    return rows
if __name__=='__main__':
    p,q=int(sys.argv[1]),int(sys.argv[2]); rows=table(p,q)
    n=0
    for (Ep,Eq,F),(r1,r2,okp,okq,D,k) in rows.items():
        if r1 or r2: continue
        tag=('P' if okp else '-')+('Q' if okq else '-')
        need=('p' if 1 in Ep else '')+('q' if 1 in Eq else '')
        print('Ep',Ep,'Eq',Eq,'F',F,' D/k=%.4f'%(D/k),tag,' 1in:',need, '' if (okp or okq) else ' BAD')
