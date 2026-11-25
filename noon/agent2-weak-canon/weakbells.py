"""Weak bells: the twelve pentatonic bells of `bells-pentatonic`, and the same canon dissolved.

Twelve bells, each owning one pitch of D major pentatonic, each striking at the pulses a + t of a 72-pulse cycle,
where a is the bell's own entry (the set A) and t runs over a complement.  With the honest complement B every pulse
is struck by exactly one bell: that is `bells-pentatonic`.  A *weak* complement gives every offset t a weight
f(t) >= 0, f(0) = 1, such that on every pulse the weights of the bells striking there add to exactly one.  The
indicators of the six complements u*B (u a unit of Z_72) are such f, and so is every average of them.  The piece
starts as the honest canon, dissolves into the average of all six (each bell then strikes 21 times a cycle, softly),
re-forms as a different honest canon, and thins out.  Every strike's loudness is its weight."""
import numpy as np, wave
from math import gcd
from scipy.signal import fftconvolve, lfilter
SR=44100; N=72; PULSE=0.21
A=[0,1,5,6,12,25,29,36,42,48,49,53]; B=[0,8,10,18,26,64]
owner=np.zeros(N,int)
for v,a in enumerate(A):
    for b in B: owner[(a+b)%N]=v
assert sorted(np.bincount(owner))==[6]*12
# ---- pitches: exactly as in bells2.py (same seed, same search), so that the opening is that piece
PITCH=np.array([50,52,54,57,59,62,64,66,69,71,74,76])
def score(perm):
    m=PITCH[perm][owner]; s=0
    for d,w in ((1,1.0),(2,.4)):
        s-=w*np.abs(m-np.roll(m,d)).clip(0,14).sum()
    return s
rng=np.random.default_rng(12); best=None
for restart in range(30):
    p=rng.permutation(12); s=score(p); T=20.0
    for it in range(5000):
        i,j=rng.integers(0,12,2); q=p.copy(); q[i],q[j]=q[j],q[i]; t=score(q)
        if t>s or rng.random()<np.exp((t-s)/T): p,s=q,t
        T=max(.2,T*.998)
    if best is None or s>best[0]: best=(s,p.copy())
s,perm=best; names='C C# D Eb E F F# G Ab A Bb B'.split()
midi=[int(PITCH[perm][v]) for v in range(12)]
# ---- the six complements and their average
units=[u for u in range(N) if gcd(u,N)==1]; comps=[]
for u in units:
    Bu=tuple(sorted(u*b%N for b in B))
    assert sorted((a+b)%N for a in A for b in Bu)==list(range(N))
    if Bu not in comps: comps.append(Bu)
assert len(comps)==6 and comps[0]==tuple(B)
ind=lambda S: np.array([1.0 if t in S else 0.0 for t in range(N)])
F=[ind(S) for S in comps]; FBAR=sum(F)/6
# ---- the plan
order=list(np.argsort(A)); ALL=order
segments=[('hold',F[0],1,order[:3]),('hold',F[0],1,order[:6]),('hold',F[0],1,order[:9]),('hold',F[0],1,ALL),
          ('fade',(F[0],FBAR),2,ALL),('hold',FBAR,2,ALL),('fade',(FBAR,F[3]),2,ALL),('hold',F[3],1,ALL),
          ('hold',F[3],1,order[3:]),('hold',F[3],1,order[6:]),('hold',F[3],1,order[9:])]
weights=[]; active=[]
for kind,what,cycles,act in segments:
    n=cycles*N
    for i in range(n):
        if kind=='hold': weights.append(what)
        else:
            sm=0.5-0.5*np.cos(np.pi*(i+0.5)/n); weights.append((1-sm)*what[0]+sm*what[1])
        active.append(set(act))
CYC=len(weights)//N
for P,f in enumerate(weights):               # the defining property of a weak tiling, at every pulse of the piece
    assert abs(f[0]-1)<1e-9 and abs(sum(f[(P-a)%N] for a in A)-1)<1e-9 and f.min()>=0
np.save('weights.npy',np.array(weights))
fr=lambda m:440*2**((m-69)/12)
def bell(m,dur,bright=1.0):
    n=int(dur*SR); t=np.arange(n)/SR; w=2*np.pi*fr(m); out=np.zeros(n)
    for ratio,amp,dec in [(.5,.25,1.8),(1,1,1.4),(2.0,.45,.9),(2.76,.3*bright,.55),(4.07,.18*bright,.35),(5.4,.1*bright,.2)]:
        out+=amp*np.sin(w*ratio*t+rng.uniform(0,6))*np.exp(-t/(dec*dur/3))
    return out*np.minimum(t/.003,1)
pan=np.linspace(-.8,.8,12)[np.argsort(np.argsort(midi))]
T=CYC*N*PULSE+9; L=np.zeros(int(T*SR)); R=L.copy(); nstrikes=0; persec=[]
for P,f in enumerate(weights):
    p=P%N; tot=0.0
    for v,a in enumerate(A):
        w=f[(p-a)%N]
        if w<0.003 or v not in active[P]: continue
        tot+=w
        g=.5*(1.15 if p%12==0 else 1)*rng.uniform(.85,1.05)*w
        sig=bell(midi[v],3.2,bright=.8 if midi[v]>70 else 1.1)
        i=max(0,int((P*PULSE+rng.normal(0,.004))*SR)); th=(pan[v]+1)*np.pi/4
        L[i:i+len(sig)]+=sig*g*np.cos(th); R[i:i+len(sig)]+=sig*g*np.sin(th); nstrikes+=1
    if len(active[P])==12: assert abs(tot-1)<0.03, (P,tot)      # all bells in: the loudnesses on a pulse add to one (weights under 0.003 are dropped)
n=int(3.5*SR); ir=rng.normal(size=(2,n))*np.exp(-np.arange(n)/SR/.8); ir[:,:int(.015*SR)]=0; ir=lfilter([.1],[1,-.9],ir,axis=1)
for ch,k in ((L,0),(R,1)): ch+= .45*fftconvolve(ch,ir[k])[:len(ch)]/np.sqrt((ir[k]**2).sum())
x=np.stack([L,R],1)
rms=[float(np.sqrt((x[int(c*N*PULSE*SR):int((c+1)*N*PULSE*SR)]**2).mean())) for c in range(CYC)]
x=np.tanh(x/np.abs(x).max()*1.2)/np.tanh(1.2)*.7
fo=np.linspace(1,0,int(6*SR)); x[-len(fo):]*=fo[:,None]
w=wave.open('weak-bells-pentatonic.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((x*32767).astype('<i2').tobytes()); w.close()
print('cycles',CYC,'seconds %.1f'%T,'strikes',nstrikes)
print('voice pitches',[names[m%12]+str(m//12-1) for m in midi])
print('entries of the average complement:',int((FBAR>0).sum()),' weights:',sorted(set(np.round(FBAR[FBAR>0],4))))
print('level per cycle relative to the full honest canon (dB):',[round(20*np.log10(r/rms[3]),1) for r in rms])
