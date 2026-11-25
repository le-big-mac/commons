"""For each weak-minimal pattern (Z0, n) of M that is not safe and not impossible: search for a set A, |A| = n, Z_A >= Z0,
violating (T1) or (T2) (plain counts model of ~/pdflat/sat.py; nothing of Prop. 3). For 'new' patterns (D+(Z0) < n) also
ask whether ANY set of size n has Z_A >= Z0.  Env: LIMIT (s), WORKERS, ONLYNEW=1."""
import os
HERE=os.path.dirname(os.path.abspath(__file__))
import sys, os, json, time
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','flat'))
from wscan import analyse
from sat import search
from cyc import zero_set
LIMIT=int(os.environ.get('LIMIT','300')); WORKERS=int(os.environ.get('WORKERS','8')); ONLYNEW=os.environ.get('ONLYNEW')=='1'
for M in [int(a) for a in sys.argv[1:]]:
    out,ndiff,N=analyse(M); t0=time.time()
    todo=[o for o in out if o[3] in('T1-short','T2-open') and (o[4] or not ONLYNEW)]
    res={'INFEASIBLE':0,'found':0,'UNKNOWN':0}; newexist=[]
    fn=os.path.join(HERE,f'wdecide_{M}.jsonl'); f=open(fn,'a')
    for nn,Z,k,st,new in sorted(todo):
        name,A,t=search(M,nn,Z,time_limit=LIMIT,workers=WORKERS,violation=True,formulation='counts')
        rec={'M':M,'n':nn,'Z0':Z,'k':k,'status':st,'new':new,'violating':name,'A':A,'t':round(t,2)}
        if A is not None: res['found']+=1; rec['ZA']=sorted(zero_set(A,M)) if callable(zero_set) else None
        elif name=='INFEASIBLE': res['INFEASIBLE']+=1
        else: res['UNKNOWN']+=1
        if new:
            name2,A2,t2=search(M,nn,Z,time_limit=LIMIT,workers=WORKERS,violation=False,formulation='counts')
            rec['any']=name2; rec['A_any']=A2
            if A2 is not None: newexist.append((nn,Z,A2))
        f.write(json.dumps(rec)+'\n'); f.flush()
    print(f'M={M}: searched {len(todo)} (new: {sum(1 for o in todo if o[4])}); no violating set: {res["INFEASIBLE"]}; violating set FOUND: {res["found"]}; undecided: {res["UNKNOWN"]}; new patterns realised by some set: {len(newexist)}; {time.time()-t0:.0f}s',flush=True)
    for nn,Z,A2 in newexist[:10]: print('    new pattern realised: n=%d Z0=%s A=%s'%(nn,Z,A2))
