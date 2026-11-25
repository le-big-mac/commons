import sys
from formulas import todo, analyse
from symb import *
def cat(pv,qv):
    res={}
    for Ep,Eq,F,Z in todo():
        a=analyse(Ep,Eq,F,Z,pv,qv); k=pv**len(Ep)*qv**len(Eq); D=pv*pv*qv*qv/a['val']
        t2=all((l,m) in F for l in Ep for m in Eq)
        orph=[(l,m) for (l,m) in F if l not in Ep and m not in Eq]
        r=D/k
        if t2 and r<2-1e-9: c='a'       # T2 and D<2k: |A|=k, CM
        elif (not t2) and r<1-1e-9: c='b'
        else: c='c'
        res[(Ep,Eq,F)]=(c,r,t2,orph,'P' if 'P' in a else '-','Q' if 'Q' in a else '-')
    return res
if __name__=='__main__':
    from collections import Counter
    allc={}
    for (pv,qv) in [(2,3),(3,5),(7,11),(11,13),(2,5),(3,11),(5,29),(2,7)]:
        res=cat(pv,qv); print((pv,qv),Counter(v[0] for v in res.values()))
        for key,v in res.items(): allc.setdefault(key,{})[(pv,qv)]=v
    print('patterns in category c for some pair:')
    for key,d in allc.items():
        if any(v[0]=='c' for v in d.values()):
            print(' Ep',key[0],'Eq',key[1],'F',key[2],'T2' if list(d.values())[0][2] else 'noT2','orph',list(d.values())[0][3],
                  ' | '.join('%s:%s %.3f %s%s'%(pq,v[0],v[1],v[4],v[5]) for pq,v in d.items() if pq in [(2,3),(3,5),(7,11),(2,5),(3,11)]))
