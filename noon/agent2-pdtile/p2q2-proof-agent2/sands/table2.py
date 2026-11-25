import sys, itertools, pickle
from table import table
def classify(p,q):
    rows=table(p,q); out={}
    for (Ep,Eq,F),(r1,r2,okp,okq,D,k) in rows.items():
        Z={(l,0) for l in Ep}|{(0,m) for m in Eq}|set(F)
        r4 = not (Z & {(2,0),(2,1),(2,2)}) or not (Z & {(0,2),(1,2),(2,2)})
        if r1: c='R1'
        elif r2: c='R2'
        elif r4: c='R4'
        elif okp or okq: c='R3'
        elif D<k-1e-6: c='D<k'
        elif abs(D/k-round(D/k))>1e-6: c='nonint'
        else: c='HARD'
        out[(Ep,Eq,F)]=(c,D/k,okp,okq)
    return out
if __name__=='__main__':
    from collections import Counter
    for (p,q) in [(2,3),(3,2),(2,5),(5,2),(3,5),(5,3),(3,7),(7,3),(3,11),(11,3),(5,7),(7,5),(2,7),(7,2),(5,29),(29,5),(11,13)]:
        cl=classify(p,q); c=Counter(v[0] for v in cl.values())
        print((p,q),dict(c))
        if len(sys.argv)>1 and (p,q) in [(3,5),(2,5),(5,3),(5,2)]:
            for key,(c_,r,okp,okq) in cl.items():
                if c_ in ('R3',): print('    ',c_,'Ep',key[0],'Eq',key[1],'F',key[2],' D/k=%.4f'%r,'P' if okp else '-','Q' if okq else '-')
            for key,(c_,r,okp,okq) in cl.items():
                if c_ in ('D<k','nonint','HARD'): print('    ',c_,'Ep',key[0],'Eq',key[1],'F',key[2],' D/k=%.4f'%r)
