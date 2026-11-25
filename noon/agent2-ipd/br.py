# Upper bound on what ANY strategy can earn against a fixed machine: solve the MDP in which the
# invader is told the machine's current state (it cannot normally know it, since it does not see its own slips).
import numpy as np, json, glob
from ev import *
def best_response(m,iters=3000):
    p,c,d,s0=m; n=len(p); V=np.zeros(n)
    for _ in range(iters):
        Q=np.zeros((n,2))
        for a in (0,1):
            for fa in (0,1):
                for fb in (0,1):
                    pr=(EPS if fa else 1-EPS)*(EPS if fb else 1-EPS); xa=a^fa; xb=p^fb
                    r=np.where(xb==0,3 if xa==0 else 5,0 if xa==0 else 1)
                    Q[:,a]+=pr*(r+D*V[c if xa==0 else d])
        V=Q.max(1)
    return (1-D)*V[s0], Q.argmax(1)
P=pool()
n,m=load('/srv/commons/welch/entries/agent2-anteater.json'); P[n]=m
P['handshake']=M([1,1,0],[0,0,2],[1,2,0])
print(f"{'machine':28s} self   best-reply bound   gap   informed best reply per state")
for n,m in P.items():
    s=score(m,m); b,pol=best_response(m)
    print(f"{n[:28]:28s} {s:.3f}  {b:.3f}   {b-s:+.3f}   {''.join('CD'[x] for x in pol)}")
