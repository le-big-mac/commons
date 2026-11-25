"""Summary of the weak-tiling computation from the cached scans (W_M.pkl) and the search logs (wdecide_M.jsonl)."""
import os
HERE=os.path.dirname(os.path.abspath(__file__))
import sys, json, os, pickle, glob
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','flat'))
from wscan import analyse
def fac(n):
    f={}; p=2
    while p*p<=n:
        while n%p==0: f[p]=f.get(p,0)+1; n//=p
        p+=1
    if n>1: f[n]=1
    return f
def report(mods):
    tot=dict(patterns=0,diff=0,wmin=0,new_search=0,new_imp=0,old_cov=0,safe=0,searched=0,infeasible=0,found=0,unknown=0,realised=0,tmax=0.0)
    diffmods=[]; missing=[]
    for M in mods:
        if not os.path.exists(os.path.join(HERE,f'W_{M}.pkl')): missing.append(M); continue
        out,nd,N=analyse(M)
        tot['patterns']+=N; tot['diff']+=nd; tot['wmin']+=len(out)
        if nd: diffmods.append(M)
        need={}
        for nn,Z,k,st,new in out:
            if st=='safe': tot['safe']+=1
            elif st=='impossible': tot['new_imp']+=new
            elif new: tot['new_search']+=1; need[(nn,tuple(Z))]=None
            else: tot['old_cov']+=1
        fn=os.path.join(HERE,f'wdecide_{M}.jsonl')
        if os.path.exists(fn):
            for line in open(fn):
                r=json.loads(line)
                key=(r['n'],tuple(r['Z0']))
                if key in need and r.get('new'): need[key]=r
        for key,r in need.items():
            if r is None: tot['unknown']+=1; continue
            tot['searched']+=1; tot['tmax']=max(tot['tmax'],r['t'])
            if r['violating']=='INFEASIBLE': tot['infeasible']+=1
            elif r['A'] is not None: tot['found']+=1
            else: tot['unknown']+=1
            if r.get('A_any') is not None: tot['realised']+=1
    return tot,diffmods,missing
if __name__=='__main__':
    lo,hi=int(sys.argv[1]),int(sys.argv[2]); extra=[int(a) for a in sys.argv[3:]]
    for name,mods in (('%d..%d'%(lo,hi),range(lo,hi+1)),('extras',extra)):
        if not mods: continue
        tot,diffmods,missing=report(mods)
        print(name,tot); print('  moduli with D^w != D+:',len(diffmods),[M for M in diffmods if len(fac(M))==2],'(two-prime ones listed)'); print('  missing scans:',missing)
