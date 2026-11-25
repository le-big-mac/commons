"""Second, independent check of certificates_p2q2.json: exact rational arithmetic at every pair of primes p < q < 60
(136 pairs), without the sign test of check_p2q2.py; where scipy is available the value y[norm] is also compared with
the optimum found by a solver (so that 'the certificate is optimal' is tested, not only 'the certificate is valid')."""
import json, sys, itertools
from fractions import Fraction as Fr
import sympy as sp
try:
    import numpy as np
    from scipy.optimize import linprog
except Exception: linprog=None
p,q=sp.symbols('p q')
CLS=[(i,j) for i in range(3) for j in range(3)]; ORDS=CLS
def c(P,l,i): return [[P*P-P,P-1,1],[-P,P-1,1],[0,-1,1]][l][i]
def coef(pv,qv,o,cl): return c(pv,o[0],cl[0])*c(qv,o[1],cl[1])
def val(expr,pv,qv): 
    r=sp.Rational(sp.sympify(expr,locals={'p':p,'q':q}).subs({p:pv,q:qv})); return Fr(int(r.p),int(r.q))
primes=[n for n in range(2,60) if all(n%d for d in range(2,n))]
entries=json.load(open(sys.argv[1] if len(sys.argv)>1 else 'certificates_p2q2.json'))
checks=fails=0
for e in entries:
    if e['cat']=='a': continue
    Ep,Eq,F=e['Ep'],e['Eq'],[tuple(x) for x in e['F']]
    Z={(l,0) for l in Ep}|{(0,m) for m in Eq}|set(F)
    rows=[o for o in ORDS if o!=(0,0) and o not in Z]
    for pv in primes:
        for qv in primes:
            if not pv<qv or (e['regime']=='A')!=(qv<pv*pv): continue
            M=pv*pv*qv*qv; k=pv**len(Ep)*qv**len(Eq); checks+=1
            y0=val(e['y']['norm'],pv,qv); y={o:val(e['y']['%d,%d'%o],pv,qv) for o in rows}
            ok=all(coef(pv,qv,(0,0),cl)-(y0 if cl==(2,2) else 0)-sum(y[o]*coef(pv,qv,o,cl) for o in rows)>=0 for cl in CLS)
            if e['cat']=='b': ok&=(y0>Fr(M,k))
            if e['cat']=='H': ok&=(y0==Fr(M,k))
            if 'gamma' in e:
                g={cl:Fr(0) for cl in CLS}
                for key,v in e['gamma'].items(): g[tuple(int(x) for x in key.split(','))]=val(v,pv,qv)
                ok&=g[(2,2)]==1 and all(v>=0 for v in g.values())
                ok&=all(sum(g[cl]*coef(pv,qv,o,cl) for cl in CLS)==0 for o in rows)
                ok&=sum(g[cl]*coef(pv,qv,(0,0),cl) for cl in CLS)==y0
                if e['cat']=='RP': ok&=all(g[(0,j)]==0 for j in range(3))
                if e['cat']=='RQ': ok&=all(g[(i,0)]==0 for i in range(3))
                if e['cat']=='N': ok&=(Fr(M)/y0/k).denominator!=1
            if linprog is not None and e['cat']!='b':
                A=[[1.0 if cl==(2,2) else 0.0 for cl in CLS]]+[[float(coef(pv,qv,o,cl)) for cl in CLS] for o in rows]
                r=linprog([float(coef(pv,qv,(0,0),cl)) for cl in CLS],A_eq=np.array(A),b_eq=np.array([1.0]+[0.0]*len(rows)),bounds=[(0,None)]*9,method='highs')
                ok&=abs(r.fun-float(y0))<1e-6*max(1.0,r.fun)
            if not ok: fails+=1; print('FAIL',e['regime'],e['cat'],Ep,Eq,F,(pv,qv))
print('exact checks (pattern, regime, prime pair):',checks,' failures:',fails)
