"""Which zero patterns of Z_{p^2 q^2} survive the reductions?
 R1: 1 not in E_p and 1 not in E_q            -> A in pZ or qZ (Claim S), reduce to Z_{M/p}.
 R2: (2,0),(2,1),(2,2) all zeros (or q-version) -> A periodic, reduce to quotient.
 R3: optimal face has a point supported in pZ (or qZ) -> Lemma L.
 Otherwise 'bad': must show no set A with exactly this zero set has |A| = D^w."""
import sys, itertools
from steplp import Step
def subs(S): return itertools.chain.from_iterable(itertools.combinations(S,r) for r in range(len(S)+1))
def run(p,q,verbose=False):
    S=Step(p,2,q,2); pairs=[(1,1),(1,2),(2,1),(2,2)]; out=[]
    tot=[float(S.C[((0,0),cl)]) for cl in S.cls]
    outp=[tot[k] if cl[0]==0 else 0.0 for k,cl in enumerate(S.cls)]
    outq=[tot[k] if cl[1]==0 else 0.0 for k,cl in enumerate(S.cls)]
    cnt={'R1':0,'R2':0,'R3':0,'bad':0}
    for Ep in subs((1,2)):
        for Eq in subs((1,2)):
            for F in subs(pairs):
                Z={(l,0) for l in Ep}|{(0,m) for m in Eq}|set(F)
                if 1 not in Ep and 1 not in Eq: cnt['R1']+=1; continue
                if {(2,0),(2,1),(2,2)}<=Z or {(0,2),(1,2),(2,2)}<=Z: cnt['R2']+=1; continue
                v,g=S.solve(Z)
                mp=S.solve(Z,obj=outp,extra_eq=[(tot,v)])[0]; mq=S.solve(Z,obj=outq,extra_eq=[(tot,v)])[0]
                if mp<1e-7 or mq<1e-7: cnt['R3']+=1; continue
                cnt['bad']+=1; k=p**len(Ep)*q**len(Eq); D=S.M/v
                orph=[(l,m) for (l,m) in F if l not in Ep and m not in Eq]
                t2=all((l,m) in F for l in Ep for m in Eq)
                out.append((Ep,Eq,F,D,k,orph,t2,mp,mq))
    return cnt,out
if __name__=='__main__':
    for (p,q) in [(2,3),(3,2),(2,5),(5,2),(3,5),(5,3),(2,7),(7,2),(3,7),(7,3),(5,7),(7,5),(11,13),(13,11),(3,11),(11,3),(2,13),(13,2)]:
        cnt,out=run(p,q)
        integral=[o for o in out if abs(o[3]-round(o[3]))<1e-6 and round(o[3])%o[4]==0]
        print((p,q),cnt,' bad with D^w a multiple of k:',len(integral))
        if len(sys.argv)>1:
            for Ep,Eq,F,D,k,orph,t2,mp,mq in integral:
                print('     Ep',Ep,'Eq',Eq,'F',F,' D^w=%.4f k=%d D/k=%.4f'%(D,k,D/k),' orphans',orph,' T2' if t2 else ' notT2')
