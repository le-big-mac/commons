# True best reply to a fixed machine: the deviator sees only the machine's (noisy) moves, not its state
# and not its own slips. Belief-state MDP over a rounded set of reachable beliefs.
import numpy as np, sys
from ev import *
def true_br(m,res=400,cap=200000):
    p,c,d,s0=m; n=len(p)
    pc=np.where(p==0,1-EPS,EPS)                    # P(machine seen to play C | state)
    Tn=np.zeros((2,n,n))                           # my intended a -> machine state transition
    for a in (0,1):
        for fa in (0,1):
            xa=a^fa; np.add.at(Tn[a],(np.arange(n),c if xa==0 else d),EPS if fa else 1-EPS)
    def rew(b,a):
        pa=np.array([1-EPS,EPS]) if a==0 else np.array([EPS,1-EPS])  # P(my actual C,D)
        q=b@pc                                                        # P(their actual C)
        return pa[0]*(3*q)+pa[1]*(5*q+1*(1-q))
    key=lambda b:tuple(np.round(b*res).astype(int))
    b0=np.zeros(n); b0[s0]=1; ids={key(b0):0}; B=[b0]; nxt=[]; front=[0]
    while front:
        i=front.pop(); b=B[i]; row=[]
        for a in (0,1):
            for o,po in ((0,pc),(1,1-pc)):
                w=b*po; pr=w.sum()
                if pr<1e-12: row.append((0.,0)); continue
                nb=(w/pr)@Tn[a]; k=key(nb)
                if k not in ids:
                    if len(B)>=cap: raise RuntimeError('belief set too large')
                    ids[k]=len(B); B.append(nb); front.append(ids[k])
                row.append((pr,ids[k]))
        while len(nxt)<=i: nxt.append(None)
        nxt[i]=row
    N=len(B); B=np.array(B)
    R=np.array([[rew(b,a) for a in (0,1)] for b in B])
    Pr=np.array([[x[0] for x in r] for r in nxt]).reshape(N,2,2); Ix=np.array([[x[1] for x in r] for r in nxt]).reshape(N,2,2)
    V=np.zeros(N)
    for _ in range(1500):
        Q=R+D*(Pr*V[Ix]).sum(2); V=Q.max(1)
    return (1-D)*V[0],N
if __name__=='__main__':
    from br import P, best_response
    for n,m in P.items():
        s=score(m,m)
        try: t,N=true_br(m); print(f'{n[:28]:28s} self {s:.3f}  true best reply {t:.3f}  gap {t-s:+.3f}  ({N} beliefs)',flush=True)
        except RuntimeError as e: print(n[:28],e)
