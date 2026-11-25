"""Weak canon: the sextet, dissolved.

The six-voice Vuza canon on a 72-pulse cycle (rhythm A, entries B: every pulse struck by exactly one voice) is an
honest tiling A (+) B = Z_72. A *weak* tiling replaces the set of entries by nonnegative weights f on the 72 possible
entries, with f(0) = 1, such that on every pulse the weights of the voices sounding add to exactly 1. The indicator of
B is one such f; so is the indicator of u*B for each unit u of Z_72 (six different canons with the same rhythm), and
so is every average of these. The piece moves between them: every note's loudness is the weight of its voice at that
pulse, so at every pulse of the whole piece the loudnesses add to one.
"""
import numpy as np, wave, json
from math import gcd
from scipy.signal import fftconvolve, lfilter
SR=44100; N=72; PULSE=0.13
A=[0,1,5,6,12,25,29,36,42,48,49,53]; B=[0,8,10,18,26,64]
units=[u for u in range(N) if gcd(u,N)==1]
comps=[]
for u in units:
    Bu=tuple(sorted(u*b%N for b in B))
    assert sorted((a+b)%N for a in A for b in Bu)==list(range(N))
    if Bu not in comps: comps.append(Bu)
assert len(comps)==6 and comps[0]==tuple(B)
ind=lambda S: np.array([1.0 if t in S else 0.0 for t in range(N)])
F=[ind(S) for S in comps]; FBAR=sum(F)/6
for f in F+[FBAR]:
    assert abs(f[0]-1)<1e-12 and all(abs(sum(f[(p-a)%N] for a in A)-1)<1e-12 for p in range(N))
# ---- the plan: which complement at which cycle (s goes 0 -> 1 smoothly over a transition)
segments=[('hold',F[0],2),('fade',(F[0],F[1]),1),('hold',F[1],1),('fade',(F[1],F[4]),1),('hold',F[4],1),
          ('fade',(F[4],FBAR),2),('hold',FBAR,2),('fade',(FBAR,F[0]),2),('hold',F[0],1)]
weights=[]                                   # weights[P] = the complement in force at global pulse P
for kind,what,cycles in segments:
    n=cycles*N
    for i in range(n):
        if kind=='hold': weights.append(what)
        else:
            s=0.5-0.5*np.cos(np.pi*(i+0.5)/n); weights.append((1-s)*what[0]+s*what[1])
CYC=len(weights)//N
for P,f in enumerate(weights):               # the defining property, at every pulse of the piece
    assert abs(f[0]-1)<1e-9 and abs(sum(f[(P-a)%N] for a in A)-1)<1e-9 and f.min()>=0
rng=np.random.default_rng(72)
CH=[(2,[2,5,9,0,4]),(10,[10,2,5,9,4]),(7,[7,10,2,5,0]),(3,[3,7,10,2,5]),(0,[0,3,7,10,2]),(9,[9,1,4,7,10,5])]
fr=lambda m:440*2**((m-69)/12)
def env(n,a,d):
    t=np.arange(n)/SR; return np.minimum(t/a,1)*np.exp(-t/d)
def click(n,ms,hz):
    k=int(ms/1000*SR); c=np.zeros(n); b=rng.normal(size=k)*np.exp(-np.arange(k)/k*4)
    c[:k]=b-np.convolve(b,np.ones(int(SR/hz))/int(SR/hz),'same'); return c
def pluck(m,dur):
    n=int(dur*SR); p=int(SR/fr(m)); buf=rng.uniform(-1,1,p); buf=.5*(buf+np.roll(buf,1)); buf=.5*(buf+np.roll(buf,1)); out=np.empty(n)
    for i in range(0,n,p):
        k=min(p,n-i); out[i:i+k]=buf[:k]; buf=0.497*(buf+np.roll(buf,1))
    return out*env(n,.002,dur/3)
def bell(m,dur):
    n=int(dur*SR); t=np.arange(n)/SR; w=2*np.pi*fr(m)
    return np.sin(w*t+2.5*np.exp(-t/.25)*np.sin(w*3.51*t))*env(n,.002,dur/2.5)
def marimba(m,dur):
    n=int(dur*SR); t=np.arange(n)/SR; w=2*np.pi*fr(m)
    return (np.sin(w*t)+.35*np.sin(4*w*t)*np.exp(-t/.05)+.1*np.sin(9.2*w*t)*np.exp(-t/.02))*env(n,.002,dur/4)+.35*click(n,5,2500)
def thumb(m,dur):
    n=int(dur*SR); t=np.arange(n)/SR; w=2*np.pi*fr(m)
    ph=w*t+6*(1-np.exp(-t/.012))*-1
    return (np.sin(ph)+.6*np.sin(2*ph)*np.exp(-t/.09)+.4*np.sin(3*ph)*np.exp(-t/.05)+.25*np.sin(5*ph)*np.exp(-t/.03))*env(n,.002,dur/5)+.5*click(n,6,1500)
def glass(m,dur):
    n=int(dur*SR); t=np.arange(n)/SR; w=2*np.pi*fr(m)
    return (np.sin(w*t)+.5*np.sin(2.76*w*t)*np.exp(-t/.3)+.25*np.sin(5.4*w*t)*np.exp(-t/.12))*env(n,.002,dur/3)+.3*click(n,4,4000)
def epiano(m,dur):
    n=int(dur*SR); t=np.arange(n)/SR; w=2*np.pi*fr(m)
    return np.sin(w*t+1.2*np.exp(-t/.4)*np.sin(w*t)+.3*np.sin(14*w*t)*np.exp(-t/.03))*env(n,.002,dur/3)+.3*click(n,5,3000)
# the six players of the sextet; a rotation t belongs to player (t mod 12)//2, so every honest canon uses each player once
#          synth   low  pan  gain ring step
PLAYER={0:(thumb,  45, -.1, .95, .9, 1), 4:(marimba,57, .5, .95, .7, 2), 5:(epiano, 60, -.5, .75, 1.0, 3),
        3:(pluck,  64, .25, .6, 1.0, 2), 1:(glass,  72, -.8, .6, 1.1, 3), 2:(bell,   76, .85, .33, 1.5, 4)}
def tones(ch,lo,span=14): return [m for m in range(lo,lo+span) if m%12 in ch]
T=CYC*N*PULSE+7; L=np.zeros(int(T*SR)); R=L.copy()
def put(sig,t,pan,g):
    i=int(t*SR); n=min(len(sig),len(L)-i); th=(pan+1)*np.pi/4
    L[i:i+n]+=sig[:n]*g*np.cos(th); R[i:i+n]+=sig[:n]*g*np.sin(th)
events=[]; nnotes=0
onsets={t:sorted((a+t)%N for a in A) for t in range(N)}
for c in range(CYC):
    for t in range(0,N,2):
        syn,lo,pan,g,ring,step=PLAYER[(t%12)//2]
        for j,p in enumerate(onsets[t]):
            P=c*N+p; w=weights[P][t]
            if w<=0: continue
            root,ch=CH[p//12]; ts=tones(ch,lo)
            m=ts[(j*step+c+(p%12)//4)%len(ts)]
            acc=1.2 if j==0 else (1.0 if p%12 in(0,6) else .85)
            tt=max(0.0,P*PULSE+rng.normal(0,.003))
            put(syn(m,ring),tt,pan,g*acc*w*rng.uniform(.93,1.04)); nnotes+=1
            events.append((P,t,round(float(w),4)))
    for h,(root,ch) in enumerate(CH):               # bass and a very soft pad, as in the sextet
        tt=(c*N+h*12)*PULSE; d=12*PULSE
        nb=int(d*1.3*SR); tb=np.arange(nb)/SR
        put(np.sin(2*np.pi*fr(36+(root-36)%12)*tb)*np.sin(np.pi*tb/(d*1.3))**2,tt,0,.28)
        n=int(d*1.5*SR); t2=np.arange(n)/SR
        pad=sum(np.sin(2*np.pi*fr(60+x%12)*t2+rng.uniform(0,6)) for x in ch)*np.sin(np.pi*np.minimum(t2/(d*1.5),1))**2
        put(pad,tt,-.3,.02); put(np.roll(pad,37),tt,.3,.02)
n=int(2.8*SR); ir=rng.normal(size=(2,n))*np.exp(-np.arange(n)/SR/.55); ir[:, :int(.012*SR)]=0
ir=lfilter([.12],[1,-.88],ir,axis=1)
wetL=fftconvolve(L,ir[0])[:len(L)]; wetR=fftconvolve(R,ir[1])[:len(R)]
s=np.sqrt((ir[0]**2).sum()); L=L+.3*wetL/s; R=R+.3*wetR/s
x=np.stack([L,R],1); x=np.tanh(x/np.abs(x).max()*1.2)/np.tanh(1.2)*.7
fo=np.linspace(1,0,int(4*SR)); x[-len(fo):]*=fo[:,None]
w=wave.open('weakcanon.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((x*32767).astype('<i2').tobytes()); w.close()
np.save('weights.npy',np.array(weights))
json.dump({'N':N,'PULSE':PULSE,'A':A,'complements':[list(c) for c in comps],'segments':[(k,c) for k,_,c in segments],
           'events':events},open('weakcanon.json','w'))
# what is true of the piece, for the README
per_pulse={}
for P,t,wt in events: per_pulse.setdefault(P,[]).append(wt)
print('cycles',CYC,'seconds %.1f'%T,'notes',nnotes)
print('pulses',len(per_pulse),'of',CYC*N,'; sum of weights per pulse: min %.6f max %.6f'%(min(sum(v) for v in per_pulse.values()),max(sum(v) for v in per_pulse.values())))
print('voices sounding on one pulse: min',min(len(v) for v in per_pulse.values()),'max',max(len(v) for v in per_pulse.values()))
