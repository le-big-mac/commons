"""For each of the 108 patterns (after R1, R2, R4) and each regime (A: p<q<p^2, B: q>p^2), produce and verify symbolically:
   cat a: T2 holds, no orphan            -> nothing (|A| = k by the digit-set bound, then Coven-Meyerowitz)
   cat b: dual y with y_0 > M/k          -> D^w < k <= |A|: no weak tile
   cat R: primal supported in pZ or qZ and dual with the same value -> Lemma L
   cat H: dual with y_0 = M/k, pattern has Phi_p, Phi_{p^2 q^2}, no Phi_{pq^2}, k = pq -> Lemma Y'
   cat N: exact value with D^w/k not an integer
"""
import sys, pickle, sympy as sp
from symb import *
from formulas import todo, inP, inQ
s,t,z=sp.symbols('s t z',nonnegative=True)
def sign_poly(poly,regime):
    """sign of a polynomial in p,q on the regime: '+', '-', '0' or '?' (sufficient test by nonnegative coefficients)."""
    if poly==0: return '0'
    if regime=='B': e=sp.expand(poly.subs({Q:P**2+1+t}).subs({P:2+s})); gens=(s,t)
    elif regime=='A':
        d=sp.degree(poly,Q)
        e=sp.expand(sp.cancel(poly.subs({Q:((P+1)+(P**2-1)*z)/(1+z)})*(1+z)**d).subs({P:2+s})); gens=(s,z)
    else:
        e=sp.expand(poly.subs({Q:P+1+t}).subs({P:2+s})); gens=(s,t)
    co=sp.Poly(e,*gens).coeffs()
    const=e.subs({g_:0 for g_ in gens})          # value at the corner; strict sign needs a nonzero constant term
    if all(c>0 for c in co) and const>0: return '+'
    if all(c<0 for c in co) and const<0: return '-'
    if all(c>=0 for c in co): return '+0'
    if all(c<=0 for c in co): return '-0'
    return '?'
def sign(expr,regime):
    """sign of a rational function on the regime ('+','-','0','?'); strictness: '+' means > 0 everywhere."""
    expr=sp.together(sp.simplify(expr))
    if expr==0: return '0'
    num,den=sp.fraction(expr)
    sg=1; strict=True
    for part in (num,den):
        c,facs=sp.factor_list(part)
        if c<0: sg=-sg
        for f,mult in facs:
            r=sign_poly(f,regime)
            if r=='?': return '?'
            if r.startswith('-') and mult%2==1: sg=-sg
            if r.endswith('0'): strict=False
    if not strict: return ('+0' if sg>0 else '-0')
    return '+' if sg>0 else '-'
SAMPLES={'A':[(7,11),(11,13),(5,7),(13,17)],'B':[(3,11),(5,29),(7,53),(2,5)]}
def dual_cert(Z,pv,qv,regime,target=None):
    r=numeric(Z,pv,qv); cl,rows,cost=system(Z,pv,qv)
    y=r[2]; red=[float(cost[k])-sum(y[i]*float(rows[i][1][k]) for i in range(len(rows))) for k in range(len(cl))]
    tight=[c for k,c in enumerate(cl) if abs(red[k])<1e-7]
    for T in (tight,):
        res=dual_symbolic(Z,T)
        if res is None: continue
        sol,ys,free,cl_,rows_,cost_=res
        if free:
            # fit free parameters: set them to the numeric dual value's simplest closed form -> try 0, then give up
            sol=tuple(e.subs({f:0 for f in free}) for e in sol)
        red_s={c:sp.factor(sp.simplify(cost_[k]-sum(sol[i]*rows_[i][1][k] for i in range(len(rows_))))) for k,c in enumerate(cl_)}
        signs={c:sign(e,regime) for c,e in red_s.items()}
        ok=all(v in ('+','0','+0') for v in signs.values())
        return sp.factor(sp.simplify(sol[0])),ok,signs,red_s,dict(zip([r_[0] for r_ in rows_],sol))
    return None
def primal_cert(Z,pv,qv,regime,allowed):
    rr=numeric(Z,pv,qv,allowed)
    if rr is None: return None
    supp=[c for c,x in rr[1].items() if x>1e-9]
    ps=primal_symbolic(Z,supp)
    if ps is None: return None
    g,val=ps
    signs={c:sign(e,regime) for c,e in g.items()}
    ok=all(v in ('+','0','+0') for v in signs.values())
    return val,ok,signs,g
def run(regime,verbose=False):
    out={}
    pv,qv=SAMPLES[regime][0]
    for Ep,Eq,F,Z in todo():
        key=(Ep,Eq,F); k=P**len(Ep)*Q**len(Eq); Mk=P**(2-len(Ep))*Q**(2-len(Eq))    # M/k
        t2=all((l,m) in F for l in Ep for m in Eq); orph=[(l,m) for (l,m) in F if l not in Ep and m not in Eq]
        if t2 and not orph: out[key]=('a',None); continue
        d=dual_cert(Z,pv,qv,regime)
        if d is None: out[key]=('FAIL-dual',None); continue
        y0,okd,dsigns,red,ysol=d
        if not okd: out[key]=('FAIL-dualsign',(y0,dsigns,red)); continue
        # D^w <= M/y0.  category b if y0 > M/k
        sgn=sign(y0-Mk,regime)
        if sgn=='+' and not t2: out[key]=('b',(y0,ysol)); continue
        got=None
        for name,allowed in (('P',inP),('Q',inQ)):
            pc=primal_cert(Z,pv,qv,regime,allowed)
            if pc is None: continue
            val,okp,psigns,g=pc
            if sp.simplify(val-y0)==0 and okp: got=(name,val,g); break
        if got: out[key]=('R'+got[0],(y0,ysol,got[2])); continue
        # exact value without subgroup support
        pc=primal_cert(Z,pv,qv,regime,None)
        exact = pc is not None and sp.simplify(pc[0]-y0)==0 and pc[1]
        if sp.simplify(y0-Mk)==0 and Ep==(1,) and (2,2) in F and (1,2) not in F and len(Eq)==1:
            out[key]=('H',(y0,ysol)); continue
        out[key]=('N' if exact else 'FAIL-exact',(y0,ysol,pc[3] if pc else None)); continue
    return out
if __name__=='__main__':
    from collections import Counter
    allout={}
    for regime in ('A','B'):
        out=run(regime); allout[regime]=out
        print('regime',regime,Counter(v[0] for v in out.values()),flush=True)
        for key,v in out.items():
            if v[0].startswith('FAIL') or v[0] in ('N','H'):
                print('   ',v[0],'Ep',key[0],'Eq',key[1],'F',key[2], (v[1][0] if v[1] else ''), (v[1][1] if v[0]=='FAIL-dualsign' else ''))
    pickle.dump({r:{k:(v[0],sp.srepr(v[1]) if v[1] is not None else None) for k,v in o.items()} for r,o in allout.items()},open('certs.pkl','wb'))
