"""Fallback for degenerate duals: enumerate dual vertices (subsets of classes of size = number of rows on which the reduced
cost vanishes), keep one that is dual feasible on the whole regime and has the target value."""
import sys, pickle, itertools, sympy as sp
from symb import *
from formulas import todo, inP, inQ
from certify import sign, SAMPLES, primal_cert, dual_cert
def dual_enum(Z,regime,target,pred=None):
    cl,rows,cost=system(Z,P,Q); n=len(rows)
    ys=sp.symbols('y0:%d'%n)
    Amat=sp.Matrix([[rows[i][1][k] for i in range(n)] for k in range(len(cl))])   # 9 x n ; reduced = cost - Amat*y
    cvec=sp.Matrix(cost)
    best=None
    for T in itertools.combinations(range(len(cl)),n):
        sub=Amat.extract(list(T),list(range(n)))
        if sub.det()==0: continue
        y=sub.LUsolve(cvec.extract(list(T),[0])); y=y.applyfunc(sp.factor)
        if target is not None and sp.simplify(y[0]-target)!=0: continue
        if pred is not None and not pred(y[0]): continue
        red={c:sp.factor(sp.simplify(cost[k]-sum(y[i]*rows[i][1][k] for i in range(n)))) for k,c in enumerate(cl)}
        signs={c:sign(e,regime) for c,e in red.items()}
        if all(v in ('+','0','+0') for v in signs.values()):
            return sp.factor(y[0]),red,dict(zip([r_[0] for r_ in rows],list(y)))
    return None
def classify(Ep,Eq,F,Z,regime):
    pv,qv=SAMPLES[regime][0]
    k=P**len(Ep)*Q**len(Eq); Mk=P**(2-len(Ep))*Q**(2-len(Eq))
    t2=all((l,m) in F for l in Ep for m in Eq); orph=[(l,m) for (l,m) in F if l not in Ep and m not in Eq]
    if t2 and not orph: return ('a',None)
    pcs={}
    for name,allowed in (('P',inP),('Q',inQ),('U',None)):
        pc=primal_cert(Z,pv,qv,regime,allowed)
        if pc is not None and pc[1]: pcs[name]=pc
    def dual_for(target):
        d=dual_cert(Z,pv,qv,regime)
        if d is not None and d[1] and (target is None or sp.simplify(d[0]-target)==0): return d[0],d[4]
        e=dual_enum(Z,regime,target)
        return None if e is None else (e[0],e[2])
    def numeric_ok(target):
        for (a,b) in SAMPLES[regime]:
            r=numeric(Z,a,b)
            if abs(float(target.subs({P:a,Q:b}))-r[0])>1e-6*max(1,abs(r[0])): return False
        return True
    # 1. a complement supported in pZ or qZ that is optimal
    for name in ('P','Q'):
        if name in pcs and numeric_ok(pcs[name][0]):
            du=dual_for(pcs[name][0])
            if du is not None:
                y0,ysol=du
                if sign(y0-Mk,regime)=='+': return ('b',(y0,ysol))          # D^w < k : no weak tile at all
                return ('R'+name,(y0,ysol,pcs[name][3]))
    # 2. otherwise: an upper bound D^w < k
    if 'U' in pcs and numeric_ok(pcs['U'][0]):
        du=dual_for(pcs['U'][0])
        if du is None:
            e=dual_enum(Z,regime,None,pred=lambda y0: sign(y0-Mk,regime)=='+')
            if e is not None: return ('b',(e[0],e[2]))
            return ('FAIL-dual',pcs['U'][0])
        y0,ysol=du
        if sign(y0-Mk,regime)=='+': return ('b',(y0,ysol))
        if sp.simplify(y0-Mk)==0 and len(Ep)==1 and len(Eq)==1: return ('H',(y0,ysol))
        return ('N',(y0,ysol,pcs['U'][3]))
    e=dual_enum(Z,regime,None,pred=lambda y0: sign(y0-Mk,regime)=='+')
    if e is not None: return ('b',(e[0],e[2]))
    return ('FAIL-primal',None)
if __name__=='__main__':
    from collections import Counter
    allout={}
    for regime in ('A','B'):
        out={}
        for Ep,Eq,F,Z in todo():
            out[(Ep,Eq,F)]=classify(Ep,Eq,F,Z,regime)
        allout[regime]=out
        print('regime',regime,Counter(v[0] for v in out.values()),flush=True)
        for key,v in out.items():
            if v[0].startswith('FAIL') or v[0] in ('N','H'):
                print('   ',v[0],'Ep',key[0],'Eq',key[1],'F',key[2], v[1][0] if (v[1] is not None and not isinstance(v[1],sp.Basic)) else v[1],flush=True)
    pickle.dump({r:{k:(v[0],sp.srepr(v[1]) if v[1] is not None else None) for k,v in o.items()} for r,o in allout.items()},open('certs.pkl','wb'))
