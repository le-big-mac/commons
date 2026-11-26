import sys, numpy as np, time
import census
from census import enumerate_machines, pad, init, row
from ipd import M
t=time.time()
ms=enumerate_machines(4); print("4-state-or-fewer machines",len(ms),round(time.time()-t,1),flush=True)
res=[M("stiffened wooer",0,[("C",0,1),("D",1,2),("D",1,0)]),M("shifty handshake",0,[("D",1,2),("D",1,0),("C",2,1)]),M("handshake",0,[("D",0,1),("D",0,2),("C",2,0)])]
allm=res+ms
play,nxt=pad(allm,4); init(play,nxt)
for eps in (0.01,0.05):
    census.EPS=eps
    for i,r in enumerate(res):
        u,v=row(i)
        v2=v.copy(); 
        same=[j for j,m in enumerate(allm) if m.key()==r.key()]
        v2[same]=-1
        j=int(np.argmax(v2)); better=(v2>u[i]+1e-9).sum()
        print(f"eps {eps} {r.name:17s} self {u[i]:.4f}; invaders doing better: {better}; best invader earns {v2[j]:.4f}: {allm[j]}")
