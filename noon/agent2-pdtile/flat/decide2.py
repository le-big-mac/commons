"""As decide.py, but resumable: each pattern's result is appended to decide_M.jsonl as it finishes."""
import sys, os, json, pickle, time
from multiprocessing import Pool
from scan import scan
from minimal import analyse
from sat import search
from lp import Setup
_S={}
def job(a):
    M,n,Z,limit=a
    if os.environ.get('FORBID','0')=='1':
        if M not in _S: _S[M]=Setup(M)
        E=_S[M].forbidden_orders(Z); cov=_S[M].complement(Z) if M<=1000 else None
        name,A,t=search(M,n,Z,time_limit=limit,workers=int(os.environ.get('WORKERS','1')),formulation=os.environ.get('FORM','residues'),forbid=E,cover=cov)
        return n,Z,name,A,t
    name,A,t=search(M,n,Z,time_limit=limit,workers=int(os.environ.get('WORKERS','1')),formulation=os.environ.get('FORM','residues'))
    return n,Z,name,A,t
if __name__=='__main__':
    limit=float(os.environ.get('LIMIT','600')); procs=int(os.environ.get('PROCS','14'))
    for M in [int(x) for x in sys.argv[1:]]:
        if not os.path.exists(f'D_{M}.pkl'):
            O,D=scan(M,procs); pickle.dump((O,D),open(f'D_{M}.pkl','wb'))
        FORM=os.environ.get('FORM','residues'); FB=os.environ.get('FORBID','0')=='1'; pats=analyse(M)
        tag=os.environ.get('TAG') or (FORM+('+fd' if FB else '')); fn=f'decide_{M}.jsonl' if tag=='residues' else f'decide_{M}_{tag}.jsonl'; done={}
        if os.path.exists(fn):
            for l in open(fn):
                r=json.loads(l)
                if r['status'] in('INFEASIBLE','OPTIMAL','FEASIBLE') or r['limit']>=limit: done[(r['n'],tuple(r['Z']))]=r
        todo=[(M,n,Z,limit) for n,Z,k,st,miss in pats if st in('T1-short','T2-open') and (n,tuple(Z)) not in done]
        todo.sort(key=lambda a:(a[1],len(a[2])))
        print(f'M={M}: {len(pats)} minimal patterns, {len(done)} already decided, {len(todo)} to search (limit {limit}s)',flush=True)
        with Pool(procs) as p, open(fn,'a') as f:
            for n,Z,name,A,t in p.imap_unordered(job,todo,chunksize=1):
                f.write(json.dumps({'n':n,'Z':Z,'status':name,'A':A,'time':t,'limit':limit})+'\n'); f.flush()
                if A is not None: print('   FOUND',n,Z,A,flush=True)
        allr={}
        for l in open(fn):
            r=json.loads(l); k=(r['n'],tuple(r['Z']))
            if k not in allr or r['status']!='UNKNOWN': allr[k]=r
        st={}
        for r in allr.values(): st[r['status']]=st.get(r['status'],0)+1
        cnt={}
        for p in pats: cnt[p[3]]=cnt.get(p[3],0)+1
        line=f'M={M} [{tag}]: minimal patterns {cnt}; searched {len(allr)}: {st}; slowest {max([r["time"] for r in allr.values()],default=0):.1f}s'
        print(line,flush=True); open('summary.txt','a').write(line+'\n')
