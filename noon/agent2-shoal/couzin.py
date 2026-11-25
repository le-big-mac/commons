"""2-D version of the Couzin et al. (2002) zone model of schooling: repulsion / orientation / attraction."""
import numpy as np
def rot(v,ang):
    c,s=np.cos(ang),np.sin(ang); return np.stack([c*v[:,0]-s*v[:,1],s*v[:,0]+c*v[:,1]],1)
class School:
    def __init__(s,N=100,rr=1.0,ro=1.0,ra=14.0,speed=3.0,turn=np.radians(40),noise=0.05,blind=np.radians(90),dt=0.1,seed=0):
        s.__dict__.update(N=N,rr=rr,ro=ro,ra=ra,speed=speed,turn=turn,noise=noise,blind=blind,dt=dt)
        s.rng=np.random.default_rng(seed); R=np.sqrt(N)*0.9
        s.x=s.rng.uniform(-R,R,(N,2)); a=s.rng.uniform(0,2*np.pi,N); s.v=np.stack([np.cos(a),np.sin(a)],1)
    def step(s):
        d=s.x[None]-s.x[:,None]; dist=np.linalg.norm(d,axis=2); np.fill_diagonal(dist,np.inf)
        u=d/np.where(np.isfinite(dist),dist,1)[...,None]
        vis=(u*s.v[:,None]).sum(2)>np.cos(np.pi-s.blind/2)          # not in the blind wedge behind
        rep=dist<s.rr
        zo=(dist>=s.rr)&(dist<s.ro)&vis; za=(dist>=s.ro)&(dist<s.ra)&vis
        d_r=-(u*rep[...,None]).sum(1)
        d_o=(s.v[None]*zo[...,None]).sum(1); d_a=(u*za[...,None]).sum(1)
        nrm=lambda w:w/np.maximum(np.linalg.norm(w,axis=1,keepdims=True),1e-12)
        ho=zo.any(1)[:,None]; ha=za.any(1)[:,None]
        want=np.where(ho&ha,.5*(nrm(d_o)+nrm(d_a)),np.where(ho,d_o,d_a))
        want=np.where(rep.any(1)[:,None],d_r,want)
        want=np.where(np.linalg.norm(want,axis=1,keepdims=True)<1e-9,s.v,want)
        cur=np.arctan2(s.v[:,1],s.v[:,0]); tgt=np.arctan2(want[:,1],want[:,0])+s.rng.normal(0,s.noise,s.N)
        dth=(tgt-cur+np.pi)%(2*np.pi)-np.pi; dth=np.clip(dth,-s.turn*s.dt,s.turn*s.dt)
        cur+=dth; s.v=np.stack([np.cos(cur),np.sin(cur)],1); s.x+=s.v*s.speed*s.dt
    def order(s):
        c=s.x.mean(0); r=s.x-c; rn=r/np.maximum(np.linalg.norm(r,axis=1,keepdims=True),1e-12)
        return np.linalg.norm(s.v.mean(0)), abs((rn[:,0]*s.v[:,1]-rn[:,1]*s.v[:,0]).mean())
    def fragments(s):                      # number of connected groups (link if within attraction range)
        d=np.linalg.norm(s.x[None]-s.x[:,None],axis=2)<s.ra; lab=-np.ones(s.N,int); k=0
        for i in range(s.N):
            if lab[i]<0:
                st=[i]; lab[i]=k
                while st:
                    j=st.pop()
                    for m in np.nonzero(d[j]&(lab<0))[0]: lab[m]=k; st.append(m)
                k+=1
        s.lab=lab; return k
    def order_largest(s):
        k=s.fragments(); big=np.bincount(s.lab).argmax(); i=s.lab==big; x=s.x[i]; v=s.v[i]
        r=x-x.mean(0); rn=r/np.maximum(np.linalg.norm(r,axis=1,keepdims=True),1e-12)
        return np.linalg.norm(v.mean(0)), abs((rn[:,0]*v[:,1]-rn[:,1]*v[:,0]).mean()), int(i.sum()), k
