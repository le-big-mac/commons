# Find all Vuza canons of Z_72 with a 6-note inner rhythm: A (+) B = Z_72, both aperiodic.
import numpy as np, itertools, json, sys
N=72
divs=[d for d in range(2,N+1) if N%d==0]
# enumerate A = {0<a1<..<a5}
combs=np.array(list(itertools.combinations(range(1,N),5)),dtype=np.int16)
print(len(combs),file=sys.stderr)
A=np.concatenate([np.zeros((len(combs),1),dtype=np.int16),combs],axis=1)
# Phi_d | A  iff A(exp(2 pi i /d))=0
def van(d):
    return np.abs(np.exp(2j*np.pi*A/d).sum(axis=1))<1e-9
z={d:van(d) for d in divs}
# T1: exactly one of Phi_2,4,8 and one of Phi_3,9
ok=(z[2].astype(int)+z[4]+z[8]==1)&(z[3].astype(int)+z[9]==1)
A=A[ok]; print(len(A),file=sys.stderr)
def periodic(S):
    s=set(S)
    return any(all((x+p)%N in s for x in s) for p in (d for d in range(1,N) if N%d==0))
res=[]
seen=set()
for a in A:
    a=[int(x) for x in a]
    if periodic(a): continue
    # canonical under translation
    canon=min(tuple(sorted((x-t)%N for x in a)) for t in a)
    if canon in seen: continue
    seen.add(canon)
    a=list(canon)
    # backtrack: tile Z_72 by translates of a; B always contains 0 (cell 0 covered by translate 0 w.l.o.g.? no: by translate -a_i)
    sols=[]
    cov=[False]*N
    def bt(B):
        try: i=cov.index(False)
        except ValueError:
            sols.append(tuple(sorted(B))); return
        for x in a:
            t=(i-x)%N
            cells=[(t+y)%N for y in a]
            if any(cov[c] for c in cells): continue
            for c in cells: cov[c]=True
            B.append(t); bt(B); B.pop()
            for c in cells: cov[c]=False
    bt([])
    for B in set(sols):
        if not periodic(B):
            res.append((a,list(B)))
print(len(res),file=sys.stderr)
json.dump(res,open('vuza72.json','w'))
