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
# choose which pitch class each voice owns: bells overlap, so reward consonance between notes close in time
cons={0:0,1:-3,2:-.5,3:1.5,4:2,5:1.5,6:-1.5,7:2.5,8:1.5,9:2,10:-.5,11:-2.5}   # by interval class mod 12
W={1:1.0,2:.6,3:.35,4:.2}
def score(perm):
    pc=perm[owner]; s=0
    for d,w in W.items(): 
        iv=(pc-np.roll(pc,d))%12; s+=w*sum(cons[int(i)] for i in iv)
    return s
rng=np.random.default_rng(12); best=None
for restart in range(40):
    p=rng.permutation(12); s=score(p); T=2.0
    for it in range(6000):
        i,j=rng.integers(0,12,2); q=p.copy(); q[i],q[j]=q[j],q[i]; t=score(q)
        if t>s or rng.random()<np.exp((t-s)/T): p,s=q,t
        T=max(.02,T*.999)
    if best is None or s>best[0]: best=(s,p.copy())
s,perm=best; perm=(perm-perm[owner[0]]+2)%12      # transpose so the first note is D
names='C C# D Eb E F F# G Ab A Bb B'.split()
print('consonance score',round(s,1),'(random assignment averages',round(np.mean([score(rng.permutation(12)) for _ in range(300)]),1),')')
print('melody:',' '.join(names[perm[owner[p]]] for p in range(N)))
f=lambda m:440*2**((m-69)/12)
def bell(m,dur,bright=1.0):
    n=int(dur*SR); t=np.arange(n)/SR; w=2*np.pi*f(m); out=np.zeros(n)
    for ratio,amp,dec in [(.5,.25,1.8),(1,1,1.4),(2.0,.45,.9),(2.76,.3*bright,.55),(4.07,.18*bright,.35),(5.4,.1*bright,.2)]:
        out+=amp*np.sin(w*ratio*t+rng.uniform(0,6))*np.exp(-t/(dec*dur/3))
    return out*np.minimum(t/.003,1)
# registers: spread pitch classes over two and a half octaves, by voice entry order low -> high-ish zigzag
octv=[60,72,48,60,72,60,48,72,60,48,72,60]
midi=[octv[v]+int(perm[v]) for v in range(12)]; pan=np.linspace(-.8,.8,12)[np.argsort(np.argsort(midi))]
order=list(np.argsort(A))                                  # voices in order of entry
plan=[order[:3],order[:6],order[:9],order,order,order,order[3:],order[6:],order[9:]]
T=len(plan)*N*PULSE+8; L=np.zeros(int(T*SR)); R=L.copy()
for c,act in enumerate(plan):
    for p in range(N):
        v=owner[p]
        if v not in act: continue
        g=.5*(1.15 if p%12==0 else 1)*rng.uniform(.85,1.05); sig=bell(midi[v],3.2,bright=.8 if midi[v]>70 else 1.1)
        i=int(((c*N+p)*PULSE+rng.normal(0,.004))*SR); th=(pan[v]+1)*np.pi/4
        L[i:i+len(sig)]+=sig*g*np.cos(th); R[i:i+len(sig)]+=sig*g*np.sin(th)
n=int(3.5*SR); ir=rng.normal(size=(2,n))*np.exp(-np.arange(n)/SR/.8); ir[:,:int(.015*SR)]=0; ir=lfilter([.1],[1,-.9],ir,axis=1)
for ch,k in ((L,0),(R,1)): ch+= .45*fftconvolve(ch,ir[k])[:len(ch)]/np.sqrt((ir[k]**2).sum())
x=np.stack([L,R],1); x=np.tanh(x/np.abs(x).max()*1.2)/np.tanh(1.2)*.7
fo=np.linspace(1,0,int(5*SR)); x[-len(fo):]*=fo[:,None]
w=wave.open('bells.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((x*32767).astype('<i2').tobytes()); w.close()
print('seconds',round(T,1),'voice pitches',[names[m%12]+str(m//12-1) for m in midi])
