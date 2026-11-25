# Compare my backward eclipse predictions (eclipses_back_all.out) with NASA's Five Millennium Catalog (values fetched 22 Nov 2026).
# NASA dates before 1582 Oct 15 are Julian; times are TD. Matching is by Julian Day.
import numpy as np, sys
ALL = sys.argv[1] if len(sys.argv) > 1 else 'eclipses_back_all.out'   # which list of my eclipses to compare
NASA=[ # (year, month, day, 'hh:mm:ss', gamma, julian_calendar)
 (1918,6,8,'22:07:43',0.4658,0),(1918,12,3,'15:22:02',-0.2387,0),(1919,5,29,'13:08:55',-0.2955,0),(1919,11,22,'15:14:12',0.4549,0),(1920,5,18,'06:14:55',-1.0239,0),
 (1714,5,13,'18:39:35',1.4856,0),(1714,6,12,'04:40:01',-1.1610,0),(1714,11,7,'09:04:34',-1.4630,0),(1714,12,7,'01:27:09',1.4772,0),(1715,5,3,'09:36:30',0.7112,0),(1715,10,27,'09:02:48',-0.7939,0),(1716,4,22,'02:28:33',-0.0091,0),
 (1499,6,8,'23:13:39',0.0195,1),(1499,12,2,'20:11:32',-0.2557,1),(1500,5,27,'23:48:31',0.7832,1),(1500,11,21,'11:30:31',-0.9393,1),(1501,4,17,'16:15:52',-1.2071,1),(1501,5,17,'03:27:44',1.5002,1),
 (1199,1,28,'09:05:27',0.0033,1),(1199,7,24,'21:48:31',0.1439,1),(1200,1,17,'23:48:29',-0.6731,1),(1200,7,12,'22:22:50',0.9039,1),(1200,12,8,'03:30:03',1.3933,1),(1201,1,6,'15:24:30',-1.3491,1),(1201,6,2,'14:35:50',-1.0802,1),
 (999,4,18,'17:43:24',-0.5439,1),(999,10,12,'06:24:46',0.6349,1),(1000,4,7,'09:21:38',0.1892,1),(1000,9,30,'11:45:53',-0.1075,1),(1001,3,27,'19:20:56',0.9775,1),
 (-1,12,26,'19:13:58',-1.4044,1),(0,6,20,'13:45:32',1.0876,1),(0,7,19,'20:44:11',-1.4254,1),(0,12,14,'18:19:36',-0.7446,1),(1,6,10,'06:44:16',0.3625,1),(1,12,3,'20:05:38',-0.0397,1),(2,5,30,'19:45:43',-0.4168,1)]
def jd_of(y,m,d,hms,jul):
    h,mi,s=(int(x) for x in hms.split(':')); 
    if m<=2: y-=1; m+=12
    B=0 if jul else 2-y//100+(y//100)//4
    return np.floor(365.25*(y+4716))+np.floor(30.6001*(m+1))+d+B-1524.5+(h*3600+mi*60+s)/86400
mine=[(float(l.split()[0]),float(l.split()[-1])) for l in open(ALL) if not l.startswith('JD')]
rows=[]
print('NASA date (TD)            gamma      mine - NASA: time (s)   gamma')
for y,m,d,hms,g,jul in NASA:
    j=jd_of(y,m,d,hms,jul); k=min(mine,key=lambda x:abs(x[0]-j)); dt=(k[0]-j)*86400
    assert abs(dt)<3600,(y,m,d)
    rows.append(((2000.0-(j-2451545.0)/365.25-2000.0)/100.0*-1 if False else (2451545.0-j)/36525.0, dt, k[1]-g))
    print(f'{y:5d}-{m:02d}-{d:02d} {hms}   {g:+.4f}      {dt:+8.0f}             {k[1]-g:+.4f}')
R=np.array(rows); T=R[:,0]                         # centuries before J2000
A=np.vstack([T,T*T]).T; coef,res,_,_=np.linalg.lstsq(A,R[:,1],rcond=None); fit=A@coef
print(f'\nfit: offset = {coef[0]:.2f} s per century + {coef[1]:.3f} s per century^2  (T = centuries before 2000); rms residual {np.sqrt(((R[:,1]-fit)**2).mean()):.1f} s; largest offset {R[:,1].max():.0f} s')
print('by epoch (mean offset, mean of fit, range of offsets, largest |gamma difference|):')
for lo,hi,lab in ((0.5,1,'1918-20'),(2.5,3,'1714-16'),(4.9,5.1,'1499-1501'),(7.9,8.1,'1199-1201'),(9.9,10.1,'999-1001'),(19.9,20.1,'year -1 to 2')):
    m=(T>lo)&(T<hi); print(f'  {lab:13s} n={int(m.sum())}  mean {R[m,1].mean():+6.0f} s   fit {fit[m].mean():+6.0f} s   range {R[m,1].min():+.0f} to {R[m,1].max():+.0f} s   |dgamma| up to {abs(R[m,2]).max():.4f}')
print(f'in lunar longitude: mean motion {coef[0]*0.549:+.1f} arcsec per century, acceleration term {coef[1]*0.549:+.2f} arcsec per century^2 (i.e. n-dot differs by {2*coef[1]*0.549:.2f} arcsec/cy^2)')
