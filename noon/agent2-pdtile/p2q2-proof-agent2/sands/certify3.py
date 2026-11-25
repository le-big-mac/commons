"""Can the 84 patterns handled by the periodicity reductions R2, R4 be settled by the LP alone (categories a, b, R)?"""
import sys, pickle, sympy as sp
from collections import Counter
from symb import *
from certify2 import classify
def r24():
    for Ep,Eq,F in patterns():
        Z=Zof(Ep,Eq,F)
        if 1 not in Ep and 1 not in Eq: continue
        r2={(2,0),(2,1),(2,2)}<=Z or {(0,2),(1,2),(2,2)}<=Z
        r4=not (Z & {(2,0),(2,1),(2,2)}) or not (Z & {(0,2),(1,2),(2,2)})
        if r2 or r4: yield Ep,Eq,F,Z
if __name__=='__main__':
    allout={}
    for regime in ('A','B'):
        out={}
        for Ep,Eq,F,Z in r24(): out[(Ep,Eq,F)]=classify(Ep,Eq,F,Z,regime)
        allout[regime]=out
        print('regime',regime,Counter(v[0] for v in out.values()),flush=True)
        for key,v in out.items():
            if v[0].startswith('FAIL') or v[0] in ('N','H'):
                print('   ',v[0],'Ep',key[0],'Eq',key[1],'F',key[2], v[1][0] if (v[1] is not None and not isinstance(v[1],sp.Basic)) else v[1],flush=True)
    pickle.dump({r:{k:(v[0],sp.srepr(v[1]) if v[1] is not None else None) for k,v in o.items()} for r,o in allout.items()},open('certs_r24.pkl','wb'))
    print('done')
