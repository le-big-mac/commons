import sys
names=['Sun','Mercury','Venus','Earth','Moon','Mars','Jupiter','Saturn','Uranus','Neptune','Pluto']
def load(p):
    d={}
    for l in open(p):
        w=l.split(); d[(float(w[0]),int(w[1]))]=[float(x) for x in w[2:5]]
    return d
ref=load(sys.argv[1]); out=load(sys.argv[2])
jds=sorted({k[0] for k in ref})
for jd in [jds[1],jds[5],jds[12],jds[-1]]:
    print(f'JD {jd} (+{(jd-2451545)/365.25:.0f} yr): position error in km')
    print('  '+'  '.join(f'{names[i]}={149597870.7*sum((a-b)**2 for a,b in zip(ref[(jd,i)],out[(jd,i)]))**.5:.3g}' for i in range(11)))
