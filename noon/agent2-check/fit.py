import numpy as np, sys
names=['Mercury','Venus','EMB','Mars','Jupiter','Saturn','Uranus','Neptune']
for f in sys.argv[1:]:
    d=np.array([[float(x) for x in l.split()[:11]] for l in open(f) if not l.startswith('#') and len(l.split())>=11])
    t=d[:,0]; print(f,'to',t[-1],'Myr')
    inner=d[:,3:7].mean(1)                     # mean log10|delta e| of the four inner planets
    for lo,hi in [(30,t[-1]),(30,60),(40,t[-1]),(50,t[-1])]:
        m=(t>=lo)&(t<=hi)
        if m.sum()<20: continue
        s,c=np.polyfit(t[m],inner[m],1); res=inner[m]-(s*t[m]+c)
        # block bootstrap-free error: slope uncertainty from halves
        h=m.sum()//2; s1=np.polyfit(t[m][:h],inner[m][:h],1)[0]; s2=np.polyfit(t[m][h:],inner[m][h:],1)[0]
        print(f'  inner planets {lo:.0f}-{hi:.0f} Myr: e-folding time {1/(s*np.log(10)):.2f} Myr  (first half {1/(s1*np.log(10)):.2f}, second half {1/(s2*np.log(10)):.2f}; rms scatter {res.std():.2f} dex)')
    m=t>=30
    print('  per planet, 30 Myr to end:',' '.join(f'{n} {1/(np.polyfit(t[m],d[m,3+i],1)[0]*np.log(10)):.1f}' for i,n in enumerate(names)))
