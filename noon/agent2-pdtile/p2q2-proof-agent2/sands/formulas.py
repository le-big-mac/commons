import sys, sympy as sp
from symb import *
def todo():
    for Ep,Eq,F in patterns():
        Z=Zof(Ep,Eq,F)
        if 1 not in Ep and 1 not in Eq: continue
        if {(2,0),(2,1),(2,2)}<=Z or {(0,2),(1,2),(2,2)}<=Z: continue
        if not (Z & {(2,0),(2,1),(2,2)}) or not (Z & {(0,2),(1,2),(2,2)}): continue
        yield Ep,Eq,F,Z
inP={c for c in CLS if c[0]>=1}; inQ={c for c in CLS if c[1]>=1}
def analyse(Ep,Eq,F,Z,pv,qv):
    r=numeric(Z,pv,qv); v=r[0]
    out={'val':v}
    for name,allowed in (('P',inP),('Q',inQ)):
        rr=numeric(Z,pv,qv,allowed)
        if rr is not None and abs(rr[0]-v)<1e-7*max(1,abs(v)):
            out[name]=[c for c,x in rr[1].items() if x>1e-9]
    out['supp']=[c for c,x in r[1].items() if x>1e-9]
    return out
if __name__=='__main__':
    pv,qv=int(sys.argv[1]),int(sys.argv[2])
    k_=lambda Ep,Eq: P**len(Ep)*Q**len(Eq)
    for Ep,Eq,F,Z in todo():
        a=analyse(Ep,Eq,F,Z,pv,qv)
        which='P' if 'P' in a else ('Q' if 'Q' in a else None)
        supp=a[which] if which else a['supp']
        ps=primal_symbolic(Z,supp)
        if ps is None: print('Ep',Ep,'Eq',Eq,'F',F,which,'SYMBOLIC FAIL',supp); continue
        g,val=ps
        Dk=sp.factor(sp.simplify(P**2*Q**2/val/k_(Ep,Eq)))
        chk=float(Dk.subs({P:pv,Q:qv}))- (pv*pv*qv*qv/a['val'])/(pv**len(Ep)*qv**len(Eq))
        print('Ep',Ep,'Eq',Eq,'F',F,which or '--','D/k =',Dk,'' if abs(chk)<1e-7 else '  MISMATCH %g'%chk,flush=True)
