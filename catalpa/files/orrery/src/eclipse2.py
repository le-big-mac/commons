# Solar eclipses from integrator states printed in windows (any order in time). Same geometry as eclipse.py.
# usage: eclipse2.py states.txt
import numpy as np, sys
AU=149597870.7; C=299792.458*86400/AU; RE=6378.137/AU; EPS=np.radians(23.4392911); H=0.05
def gamma_at(Sx,Ex,Mx):
    e=Ex[:3]; tauM=np.linalg.norm(Mx[:3]-e)/C; m=Mx[:3]-Mx[3:]*tauM; tauS=tauM+np.linalg.norm(m-Sx[:3])/C
    for _ in range(2): tauM=np.linalg.norm(m-e)/C; m=Mx[:3]-Mx[3:]*tauM
    s=Sx[:3]-Sx[3:]*tauS; u=(m-s)/np.linalg.norm(m-s); w=e-m
    if w@u<=0: return 99.0
    p=-(w-(w@u)*u); return np.sign(np.sin(EPS)*p[1]+np.cos(EPS)*p[2])*np.linalg.norm(p)/RE
def herm(X,i,f):
    p0,v0,p1,v1=X[i,:3],X[i,3:],X[i+1,:3],X[i+1,3:]
    pos=(2*f**3-3*f**2+1)*p0+(f**3-2*f**2+f)*H*v0+(-2*f**3+3*f**2)*p1+(f**3-f**2)*H*v1
    vel=((6*f**2-6*f)/H)*p0+(3*f**2-4*f+1)*v0+((-6*f**2+6*f)/H)*p1+(3*f**2-2*f)*v1
    return np.concatenate([pos,vel])
def cal(jd, julian=False):
    z=int(jd+0.5); f=jd+0.5-z
    if julian: A=z
    else: al=int((z-1867216.25)/36524.25); A=z+1+al-al//4
    B=A+1524; Cc=int((B-122.1)/365.25); D=int(365.25*Cc); Ee=int((B-D)/30.6001)
    day=B-D-int(30.6001*Ee); mon=Ee-1 if Ee<14 else Ee-13; yr=Cc-4716 if mon>2 else Cc-4715
    sec=int(round(f*86400)); 
    if sec==86400: sec=86399
    return f'{yr:04d}-{mon:02d}-{day:02d} {sec//3600:02d}:{sec%3600//60:02d}:{sec%60:02d}'
def find(fn):
    a=np.loadtxt(fn); n=len(a)//11; a=a[:n*11].reshape(n,11,8); jd=a[:,0,0]
    o=np.argsort(jd); a=a[o]; jd=jd[o]; S,E,M=a[:,0,2:],a[:,3,2:],a[:,4,2:]
    g=np.array([gamma_at(S[i],E[i],M[i]) for i in range(n)]); ag=np.abs(g); out=[]
    for i in range(1,n-1):
        if abs(jd[i]-jd[i-1]-H)>1e-6 or abs(jd[i+1]-jd[i]-H)>1e-6: continue          # window edges
        if ag[i]<ag[i-1] and ag[i]<=ag[i+1] and ag[i]<1.6:
            best=(9e9,None)
            for j in (i-1,i):
                for fr in np.arange(0,1,1/4320):
                    gg=gamma_at(herm(S,j,fr),herm(E,j,fr),herm(M,j,fr))
                    if abs(gg)<best[0]: best=(abs(gg),(jd[j]+fr*H,gg))
            out.append(best[1])
    return out
if __name__=='__main__':
    ev=find(sys.argv[1])
    print('JD (TT)          Gregorian (proleptic)     Julian calendar           gamma')
    for jd,g in ev: print(f'{jd:.5f}   {cal(jd)}   {cal(jd,True)}   {g:+.4f}')
