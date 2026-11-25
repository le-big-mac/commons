# The time offsets scatter about the fitted parabola by an amount that alternates between eclipses and grows with time.
# If that is an error in the Moon's perigee (anomaly), the residual should go with where the Moon is on its ellipse at the eclipse:
# test it against the rate of change of the Moon's distance (zero at perigee and apogee, largest in between) and against the distance itself.
import numpy as np
AU=149597870.7
a=np.loadtxt('ecl_back.txt'); n=len(a)//11; a=a[:n*11].reshape(n,11,8); jd=a[:,0,0]; o=np.argsort(jd); a=a[o]; jd=jd[o]
E,M=a[:,3,2:],a[:,4,2:]
import importlib.util, sys
spec=importlib.util.spec_from_file_location('cmp','src/eclipse_back_cmp.py')
src=open('src/eclipse_back_cmp.py').read().split("mine=[")[0]; ns={}; exec(src,ns)
mine=[(float(l.split()[0]),float(l.split()[-1])) for l in open('eclipses_back_all.out') if not l.startswith('JD')]
rows=[]
for y,m,d,hms,g,jul in ns['NASA']:
    j=ns['jd_of'](y,m,d,hms,jul); k=min(mine,key=lambda x:abs(x[0]-j)); i=np.argmin(abs(jd-k[0]))
    r=M[i,:3]-E[i,:3]; v=M[i,3:]-E[i,3:]; dist=np.linalg.norm(r)*AU; rdot=(r@v)/np.linalg.norm(r)*AU/86400
    rows.append(((2451545.0-j)/36525.0,(k[0]-j)*86400,dist,rdot))
R=np.array(rows); T=R[:,0]; A=np.vstack([T,T*T]).T; coef=np.linalg.lstsq(A,R[:,1],rcond=None)[0]; res=R[:,1]-A@coef
sc=res/np.maximum(T,0.5)                       # residual per century, so that epochs can be pooled
print('correlation of (residual per century) with: Moon distance %+.2f ; radial velocity %+.2f'%(np.corrcoef(sc,R[:,2])[0,1],np.corrcoef(sc,R[:,3])[0,1]))
B=np.vstack([(R[:,2]-R[:,2].mean())/1e4,R[:,3]*10,np.ones(len(sc))]).T; c2=np.linalg.lstsq(B,sc,rcond=None)[0]; fit=B@c2
print('two-term fit of residual per century: %.2f s per 10,000 km of distance, %.2f s per 0.1 km/s of radial velocity; explains %.0f%% of its variance'%(c2[0],c2[1],100*(1-((sc-fit)**2).sum()/((sc-sc.mean())**2).sum())))
