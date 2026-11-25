"""Twelve bells: the dual canon. Twelve voices, each owning ONE pitch class, each striking six times per
72-pulse cycle (rhythm B) at entries A. The tiling therefore dictates a 72-note chromatic melody in which
every pitch class sounds exactly six times."""
import numpy as np, wave, itertools
from scipy.signal import fftconvolve, lfilter
SR=44100; N=72; PULSE=0.21
A=[0,1,5,6,12,25,29,36,42,48,49,53]; B=[0,8,10,18,26,64]
owner=np.zeros(N,int)
for v,a in enumerate(A):
    for b in B: owner[(a+b)%N]=v
assert sorted(np.bincount(owner))==[6]*12
# Pentatonic variant: twelve distinct pitches from D major pentatonic, so whatever rings together is consonant.
PITCH=np.array([50,52,54,57,59,62,64,66,69,71,74,76])
def score(perm):
    m=PITCH[perm][owner]; s=0
    for d,w in ((1,1.0),(2,.4)):
        s-=w*np.abs(m-np.roll(m,d)).clip(0,14).sum()     # prefer small steps between neighbouring notes
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
print('mean step between consecutive notes (semitones):',round(float(np.abs(np.diff(PITCH[perm][owner])).mean()),2),' random:',round(float(np.mean([np.abs(np.diff(PITCH[rng.permutation(12)][owner])).mean() for _ in range(200)])),2))
print('melody:',' '.join(names[m%12]+str(m//12-1) for m in PITCH[perm][owner]))
f=lambda m:440*2**((m-69)/12)
def bell(m,dur,bright=1.0):
    n=int(dur*SR); t=np.arange(n)/SR; w=2*np.pi*f(m); out=np.zeros(n)
    for ratio,amp,dec in [(.5,.25,1.8),(1,1,1.4),(2.0,.45,.9),(2.76,.3*bright,.55),(4.07,.18*bright,.35),(5.4,.1*bright,.2)]:
        out+=amp*np.sin(w*ratio*t+rng.uniform(0,6))*np.exp(-t/(dec*dur/3))
    return out*np.minimum(t/.003,1)
pan=np.linspace(-.8,.8,12)[np.argsort(np.argsort(midi))]
order=list(np.argsort(A))                                  # voices in order of entry
plan=[order[:3],order[:6],order[:9],order,order,order,order[3:],order[6:],order[9:]]
T=len(plan)*N*PULSE+8; L=np.zeros(int(T*SR)); R=L.copy()
for c,act in enumerate(plan):
    for p in range(N):
        v=owner[p]
        if v not in act: continue
        g=.5*(1.15 if p%12==0 else 1)*rng.uniform(.85,1.05); sig=bell(midi[v],3.2,bright=.8 if midi[v]>70 else 1.1)
        i=max(0,int(((c*N+p)*PULSE+rng.normal(0,.004))*SR)); th=(pan[v]+1)*np.pi/4
        L[i:i+len(sig)]+=sig*g*np.cos(th); R[i:i+len(sig)]+=sig*g*np.sin(th)
n=int(3.5*SR); ir=rng.normal(size=(2,n))*np.exp(-np.arange(n)/SR/.8); ir[:,:int(.015*SR)]=0; ir=lfilter([.1],[1,-.9],ir,axis=1)
for ch,k in ((L,0),(R,1)): ch+= .45*fftconvolve(ch,ir[k])[:len(ch)]/np.sqrt((ir[k]**2).sum())
x=np.stack([L,R],1); x=np.tanh(x/np.abs(x).max()*1.2)/np.tanh(1.2)*.7
fo=np.linspace(1,0,int(5*SR)); x[-len(fo):]*=fo[:,None]
w=wave.open('bells-pentatonic.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((x*32767).astype('<i2').tobytes()); w.close()
print('seconds',round(T,1),'voice pitches',[names[m%12]+str(m//12-1) for m in midi])
