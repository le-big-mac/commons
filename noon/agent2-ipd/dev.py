# Where does the true best reply to the handshake differ from the handshake itself?
import numpy as np, itertools
from ev import *
import pomdp
h=M([1,1,0],[0,0,2],[1,2,0]); p,c,d,s0=h; n=3; res=1000
pc=np.where(p==0,1-EPS,EPS); Tn=np.zeros((2,n,n))
for a in (0,1):
    for fa in (0,1):
        xa=a^fa; np.add.at(Tn[a],(np.arange(n),c if xa==0 else d),EPS if fa else 1-EPS)
# re-run solver but keep internals
src=open('pomdp.py').read().replace("return (1-D)*V[0],N","return V,Q,B,Pr,Ix")
ns={}; exec(src.split("if __name__")[0],ns); V,Q,B,Pr,Ix=ns['true_br'](h,res,cap=10**6)
# walk: joint (belief id, handshake-as-player state), weighted by probability under OPTIMAL play
from collections import defaultdict
w=defaultdict(float); w[(0,0)]=1.0; diff=defaultdict(float); disc=1.0; tot=defaultdict(float)
for t in range(400):
    nw=defaultdict(float)
    for (i,hs),pr in w.items():
        a=int(Q[i].argmax()); ha=int(p[hs]); adv=Q[i].max()-Q[i,ha]
        if a!=ha: diff[(tuple(np.round(B[i],2)),hs,'CD'[a],'CD'[ha])]+=disc*pr*adv
        for o in (0,1):
            q=Pr[i,a,o]
            if q>0: nw[(Ix[i,a,o],int((c if o==0 else d)[hs]))]+=pr*q
    w=nw; disc*=D
    if len(w)>200000: break
print('belief over machine state (0,1,2) | handshake-as-player state | best reply plays | handshake would play | discounted weight x advantage')
for k,v in sorted(diff.items(),key=lambda x:-x[1])[:12]: print(k,f'{(1-D)*v:.5f}')
print('total',(1-D)*sum(diff.values()))
