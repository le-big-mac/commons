# Find solar eclipses from the integrator's own Sun, Earth and Moon (barycentric ecliptic J2000, au, days; one sample per 0.05 d).
# Geometry, in the inertial frame: light reaching Earth's centre at time t passed the Moon at t - tauM and left the Sun at
# t - tauM - |M - S|/c. The shadow axis is the line through those two retarded points; gamma is the distance of Earth's centre
# from it in equatorial Earth radii, signed positive when the axis passes north of the centre. Greatest eclipse = minimum |gamma|.
import numpy as np, sys
AU=149597870.7; C=299792.458*86400/AU          # au/day
RE=6378.137/AU; EPS=np.radians(23.4392911)
a=np.loadtxt(sys.argv[1] if len(sys.argv)>1 else 'ecl_states.txt',usecols=(1,2,3,4,5,6,7))
n=len(a)//11; a=a[:n*11].reshape(n,11,7)
i0=round(9496.5/0.05); t=(i0+np.arange(n))*0.05                 # days since J2000 (TDB), exact
S,E,M=a[:,0,1:],a[:,3,1:],a[:,4,1:]                              # Sun, Earth, Moon: x y z vx vy vz
def gamma_at(Sx,Ex,Mx):
    """Sx, Ex, Mx: (6,) states at the same instant. returns signed gamma"""
    e=Ex[:3]; tauM=np.linalg.norm(Mx[:3]-e)/C
    m=Mx[:3]-Mx[3:]*tauM; tauS=tauM+np.linalg.norm(m-Sx[:3])/C
    for _ in range(2): tauM=np.linalg.norm(m-e)/C; m=Mx[:3]-Mx[3:]*tauM
    s=Sx[:3]-Sx[3:]*tauS
    u=(m-s)/np.linalg.norm(m-s); w=e-m; perp=w-(w@u)*u            # from the axis's nearest point to Earth's centre
    p=-perp                                                        # nearest point of the axis, relative to Earth's centre
    north=np.sin(EPS)*p[1]+np.cos(EPS)*p[2]
    if w@u<=0: return 99.0                                         # Earth is not beyond the Moon: full moon, not a solar eclipse
    return np.sign(north)*np.linalg.norm(p)/RE
def hermite(X,i,f):
    """state between samples i and i+1 at fraction f (cubic Hermite on position, with consistent velocity)"""
    h=0.05; p0,v0,p1,v1=X[i,:3],X[i,3:],X[i+1,:3],X[i+1,3:]
    h00=2*f**3-3*f**2+1; h10=f**3-2*f**2+f; h01=-2*f**3+3*f**2; h11=f**3-f**2
    pos=h00*p0+h10*h*v0+h01*p1+h11*h*v1
    d00=(6*f**2-6*f)/h; d10=3*f**2-4*f+1; d01=(-6*f**2+6*f)/h; d11=3*f**2-2*f
    vel=d00*p0+d10*v0+d01*p1+d11*v1
    return np.concatenate([pos,vel])
g=np.array([gamma_at(S[i],E[i],M[i]) for i in range(n)])
ag=np.abs(g); out=[]
for i in range(1,n-1):
    if ag[i]<ag[i-1] and ag[i]<=ag[i+1] and ag[i]<3.0:
        # refine on a 1-second grid across the two neighbouring steps
        best=(9e9,None)
        for j,fr in [(i-1,f) for f in np.arange(0,1,1/4320)]+[(i,f) for f in np.arange(0,1,1/4320)]:
            gg=gamma_at(hermite(S,j,fr),hermite(E,j,fr),hermite(M,j,fr))
            if abs(gg)<best[0]: best=(abs(gg),(t[j]+fr*0.05,gg))
        out.append(best[1])
def cal(d):   # days since J2000 (TT ~ TDB) -> calendar
    jd=d+2451545.0; z=int(jd+0.5); f=jd+0.5-z; al=int((z-1867216.25)/36524.25); A=z+1+al-al//4; B=A+1524; Cc=int((B-122.1)/365.25); D=int(365.25*Cc); Ee=int((B-D)/30.6001)
    day=B-D-int(30.6001*Ee); mon=Ee-1 if Ee<14 else Ee-13; yr=Cc-4716 if mon>2 else Cc-4715
    sec=round(f*86400); return f'{yr:04d}-{mon:02d}-{day:02d} {sec//3600:02d}:{sec%3600//60:02d}:{sec%60:02d}'
print('solar eclipses found (|gamma| < 1.6), time of greatest eclipse in TT, gamma:')
for d,gg in out:
    if abs(gg)<1.6: print(f'  {cal(d)}   gamma {gg:+.4f}')
print('new moons that miss (1.6 <= |gamma| < 3):', '; '.join(f'{cal(d)[:10]} {gg:+.2f}' for d,gg in out if 1.6<=abs(gg)<3))
