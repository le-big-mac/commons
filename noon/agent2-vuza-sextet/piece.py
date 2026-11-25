"""Sextet for a tiled hour-glass: a six-voice Vuza canon on Z_72.
Every pulse of the 72-pulse cycle is struck by exactly one voice; neither the
rhythm nor the pattern of entries repeats within the cycle."""
import numpy as np, wave
from scipy.signal import fftconvolve
SR=44100; N=72; PULSE=0.13
A=[0,1,5,6,12,25,29,36,42,48,49,53]; B=[0,8,10,18,26,64]
def tiles(A,B): return sorted((a+b)%N for a in A for b in B)==list(range(N))
def aper(S): return not any({(x+p)%N for x in S}==set(S) for p in range(1,N) if N%p==0)
RH={k:sorted(k*a%N for a in A) for k in (1,5,7,11)}
for k,r in RH.items(): assert tiles(r,B) and aper(r), k   # Tijdeman: kA (+) B still tiles
rng=np.random.default_rng(72)
# harmony: six chords x 12 pulses, pitch classes
CH=[(2,[2,5,9,0,4]),      # Dm9
    (10,[10,2,5,9,4]),    # Bbmaj7#11
    (7,[7,10,2,5,0]),     # Gm11
    (3,[3,7,10,2,5]),     # Ebmaj9
    (0,[0,3,7,10,2]),     # Cm9
    (9,[9,1,4,7,10,5])]   # A7b9b13
f=lambda m:440*2**((m-69)/12)
def env(n,a,d):
    t=np.arange(n)/SR; return np.minimum(t/a,1)*np.exp(-t/d)
def pluck(m,dur,v):
    n=int(dur*SR); p=int(SR/f(m)); buf=rng.uniform(-1,1,p); buf=.5*(buf+np.roll(buf,1)); buf=.5*(buf+np.roll(buf,1)); out=np.empty(n)
    for i in range(0,n,p):
        k=min(p,n-i); out[i:i+k]=buf[:k]; buf=0.497*(buf+np.roll(buf,1))
    return out*env(n,.002,dur/3)
def bell(m,dur,v):
    n=int(dur*SR); t=np.arange(n)/SR; w=2*np.pi*f(m)
    return np.sin(w*t+2.5*np.exp(-t/.25)*np.sin(w*3.51*t))*env(n,.002,dur/2.5)
def marimba(m,dur,v):
    n=int(dur*SR); t=np.arange(n)/SR; w=2*np.pi*f(m)
    return (np.sin(w*t)+.35*np.sin(4*w*t)*np.exp(-t/.05)+.1*np.sin(9.2*w*t)*np.exp(-t/.02))*env(n,.002,dur/4)+.35*click(n,5,2500)
def reed(m,dur,v):
    n=int(dur*SR); t=np.arange(n)/SR; w=2*np.pi*f(m)*(1+.004*np.sin(2*np.pi*5.3*t))
    ph=np.cumsum(w)/SR; s=sum(np.sin((2*k+1)*ph)/(2*k+1)**1.6 for k in range(6))
    return s*env(n,.03,dur/1.8)
def click(n,ms,hz):
    k=int(ms/1000*SR); c=np.zeros(n); b=rng.normal(size=k)*np.exp(-np.arange(k)/k*4)
    c[:k]=b-np.convolve(b,np.ones(int(SR/hz))/int(SR/hz),'same'); return c
def thumb(m,dur,v):
    n=int(dur*SR); t=np.arange(n)/SR; w=2*np.pi*f(m)
    ph=w*t+6*(1-np.exp(-t/.012))*-1          # tiny downward pitch blip at the attack
    return (np.sin(ph)+.6*np.sin(2*ph)*np.exp(-t/.09)+.4*np.sin(3*ph)*np.exp(-t/.05)+.25*np.sin(5*ph)*np.exp(-t/.03))*env(n,.002,dur/5)+.5*click(n,6,1500)
def glass(m,dur,v):
    n=int(dur*SR); t=np.arange(n)/SR; w=2*np.pi*f(m)
    return (np.sin(w*t)+.5*np.sin(2.76*w*t)*np.exp(-t/.3)+.25*np.sin(5.4*w*t)*np.exp(-t/.12))*env(n,.002,dur/3)+.3*click(n,4,4000)
def epiano(m,dur,v):
    n=int(dur*SR); t=np.arange(n)/SR; w=2*np.pi*f(m)
    return np.sin(w*t+1.2*np.exp(-t/.4)*np.sin(w*t)+.3*np.sin(14*w*t)*np.exp(-t/.03))*env(n,.002,dur/3)+.3*click(n,5,3000)
# voice: (synth, low midi, pan, gain, ring seconds, step through chord tones)
V=[(thumb,45,-.1,.95,.9,1),(marimba,57,.5,.95,.7,2),(epiano,60,-.5,.75,1.0,3),
   (pluck,64,.25,.6,1.0,2),(glass,72,-.8,.6,1.1,3),(bell,76,.85,.33,1.5,4)]
def tones(ch,lo,span=14):
    return [m for m in range(lo,lo+span) if m%12 in ch]
# score: per cycle (rhythm multiplier, active voices, transpose)
order=[3,1,0,4,2,5]
plan=[(1,order[:i+1],0) for i in range(6)]
plan+=[(1,order,0)]*2+[(5,order,0)]*2+[(7,order,5)]*2+[(11,order,5),(11,order,0)]
plan+=[(1,order,0)]+[(1,order[i:],0) for i in range(1,6)]+[(1,[],0)]
T=len(plan)*N*PULSE+6; L=np.zeros(int(T*SR)); R=L.copy()
def put(sig,t,pan,g):
    i=int(t*SR); n=min(len(sig),len(L)-i); th=(pan+1)*np.pi/4
    L[i:i+n]+=sig[:n]*g*np.cos(th); R[i:i+n]+=sig[:n]*g*np.sin(th)
for c,(k,act,tr) in enumerate(plan):
    full=len(act)==6
    for v in act:
        syn,lo,pan,g,ring,step=V[v]
        on=sorted((a+B[v])%N for a in RH[k])
        for j,p in enumerate(on):
            root,ch=CH[p//12]; ts=tones([(x+tr)%12 for x in ch],lo)
            m=ts[(j*step+c+(p%12)//4)%len(ts)]
            acc=1.25 if j==0 else (1.0 if p%12 in(0,6) else .8)
            t=(c*N+p)*PULSE+rng.normal(0,.003)
            put(syn(m,ring,v),t,pan,g*acc*rng.uniform(.9,1.05))
    if full or c>=5:                       # bass + pad once the tiling is (nearly) whole
        for h,(root,ch) in enumerate(CH):
            t=(c*N+h*12)*PULSE; d=12*PULSE
            nb=int(d*1.3*SR); tb=np.arange(nb)/SR
            put(np.sin(2*np.pi*f(36+(root+tr-36)%12)*tb)*np.sin(np.pi*tb/(d*1.3))**2,t,0,.3 if act else .15)
            n=int(d*1.5*SR); tt=np.arange(n)/SR
            pad=sum(np.sin(2*np.pi*f(60+(x+tr)%12)*tt+rng.uniform(0,6)) for x in ch)
            pad*=np.sin(np.pi*np.minimum(tt/(d*1.5),1))**2
            put(pad,t,-.3,.02); put(np.roll(pad,37),t,.3,.02)
# reverb
n=int(2.8*SR); ir=rng.normal(size=(2,n))*np.exp(-np.arange(n)/SR/.55); ir[:, :int(.012*SR)]=0
from scipy.signal import lfilter
ir=lfilter([.12],[1,-.88],ir,axis=1)   # darken the tail
wetL=fftconvolve(L,ir[0])[:len(L)]; wetR=fftconvolve(R,ir[1])[:len(R)]
s=np.sqrt((ir[0]**2).sum())
L=L+.3*wetL/s; R=R+.3*wetR/s
x=np.stack([L,R],1); x=np.tanh(x/np.abs(x).max()*1.2)/np.tanh(1.2)*.7
fo=np.linspace(1,0,int(4*SR)); x[-len(fo):]*=fo[:,None]
w=wave.open('sextet.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((x*32767).astype('<i2').tobytes()); w.close()
print("ok",T,"dry rms",np.sqrt((L**2).mean()))
