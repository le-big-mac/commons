# The same shadow-axis geometry as src/eclipse.py, applied to JPL Horizons states (DE441) at 1-minute steps.
import numpy as np, re, sys
AU=149597870.7; C=299792.458*86400/AU; RE=6378.137/AU; EPS=np.radians(23.4392911)
num=r'([-+]?\d\.\d+E[-+]\d+)'
def rows(p):
    b=open(p).read().split('$$SOE')[1].split('$$EOE')[0]; out=[]
    for m in re.finditer(r'(\d+\.\d+) = A\.D\..*?\n\s*X\s*=\s*'+num+r'\s*Y\s*=\s*'+num+r'\s*Z\s*=\s*'+num+r'\s*\n\s*VX=\s*'+num+r'\s*VY=\s*'+num+r'\s*VZ=\s*'+num,b):
        out.append([float(x) for x in m.groups()])
    return np.array(out)
def gamma_at(Sx,Ex,Mx):
    e=Ex[:3]; tauM=np.linalg.norm(Mx[:3]-e)/C; m=Mx[:3]-Mx[3:]*tauM; tauS=tauM+np.linalg.norm(m-Sx[:3])/C
    for _ in range(2): tauM=np.linalg.norm(m-e)/C; m=Mx[:3]-Mx[3:]*tauM
    s=Sx[:3]-Sx[3:]*tauS; u=(m-s)/np.linalg.norm(m-s); w=e-m; p=-(w-(w@u)*u)
    return np.sign(np.sin(EPS)*p[1]+np.cos(EPS)*p[2])*np.linalg.norm(p)/RE
def herm(X,i,f,h):
    p0,v0,p1,v1=X[i,:3],X[i,3:],X[i+1,:3],X[i+1,3:]
    pos=(2*f**3-3*f**2+1)*p0+(f**3-2*f**2+f)*h*v0+(-2*f**3+3*f**2)*p1+(f**3-f**2)*h*v1
    vel=((6*f**2-6*f)/h)*p0+(3*f**2-4*f+1)*v0+((-6*f**2+6*f)/h)*p1+(3*f**2-2*f)*v1
    return np.concatenate([pos,vel])
for tag,lab in (('a','2027 Aug 02'),('b','2030 Jun 01')):
    S,E,M=(rows(f'data/ecl/hz_{tag}_{i}.txt') for i in (10,399,301)); jd=S[:,0]; h=1/1440.0; best=(9,None)
    for i in range(len(jd)-1):
        for f in np.arange(0,1,1/600):                     # 0.1-second grid
            g=gamma_at(herm(S[:,1:],i,f,h),herm(E[:,1:],i,f,h),herm(M[:,1:],i,f,h))
            if abs(g)<best[0]: best=(abs(g),(jd[i]+f*h,g))
    t,g=best[1]; sec=((t+0.5)%1)*86400
    print(f'{lab}: from JPL Horizons states, greatest eclipse at {int(sec//3600):02d}:{int(sec%3600//60):02d}:{sec%60:04.1f} TDB, gamma {g:+.4f}')
