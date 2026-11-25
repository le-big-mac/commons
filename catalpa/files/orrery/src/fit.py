import math
def load(p): return [(float(a),float(b)) for a,b,*_ in (l.split() for l in open(p))]
def unwrap(v):
    out=[v[0]]; P=360*3600
    for x in v[1:]:
        while x-out[-1]>P/2: x-=P
        while x-out[-1]<-P/2: x+=P
        out.append(x)
    return out
def slope(t,y):
    n=len(t); mt=sum(t)/n; my=sum(y)/n
    return sum((a-mt)*(b-my) for a,b in zip(t,y))/sum((a-mt)**2 for a in t)
g=load('peri_gr.txt'); n=load('peri_newt.txt')
t=[a for a,_ in g]; yg=unwrap([b for _,b in g]); yn=unwrap([b for _,b in n])
sg=slope(t,yg)*100; sn=slope(t,yn)*100
print(f'Newtonian (planets only): {sn:.3f} "/century')
print(f'With 1PN solar term:      {sg:.3f} "/century')
print(f'Difference (relativity):  {sg-sn:.3f} "/century')
a=0.38709893*149597870.7; e=0.20563; GM=132712440041.28; c=299792.458; T=87.9691/36525
print(f'Analytic 6πGM/(a(1-e²)c²) per orbit → {6*math.pi*GM/(a*(1-e*e)*c*c)/T*206264.806:.3f} "/century')
