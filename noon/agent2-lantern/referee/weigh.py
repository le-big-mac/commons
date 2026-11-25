# weigh.py: numbers for Brewster's objections, his cam, and Young's shade. f=150 mm, sizes m=2..20 (and m=40 for a long throw)
import numpy as np
f=150.0
def rod(name,L,E,rho,Iz,A,Iweak):
    wl=rho*9.81*A                      # N/m
    sag=5*wl*L**4/(384*E*Iz)           # horizontal pin-ended beam, own weight
    short=8*sag**2/(3*L)               # shortening of the chord
    Pcr=np.pi**2*E*Iweak/L**2          # Euler load about the weak axis
    print('%-34s L=%.2f m: weight %.1f N, sag %.2f mm, chord shortening %.4f mm, Euler load %.0f N'%(name,L,wl*L,sag*1e3,short*1e3,Pcr))
if __name__=='__main__':
    for L in (1.55,3.1,6.2):   # a = (m+1/m) f/2 : m_max = 20.6, 41, 83
        rod('deal lath 30x12 mm on edge',L,10e9,550,0.012*0.030**3/12,0.012*0.030,0.030*0.012**3/12)
        rod('iron rod 6 mm round',L,190e9,7700,np.pi*0.006**4/64,np.pi*0.003**2,np.pi*0.006**4/64)
    print('amplification of a rod-length error into lens error, 2a/(f(m-1/m)), a=1550:',{m:round(2*1550/(f*(m-1/m)),1) for m in (2,5,10,20)})
    # cam
    for m in (2,5,10,20,40):
        x=f/m; T=f*(m+1/m+2); print('m=%-3g lens beyond focus x=%.2f mm, slide-to-screen T=%.0f mm, dx/dT=1/%.0f'%(m,x,T,m*m-1))
    T2,T20=f*(2+.5+2),f*(20+.05+2); print('travel m=2..20: %.0f mm; wheel 150 mm dia turns %.1f; cam lift %.1f mm'%(T20-T2,(T20-T2)/(np.pi*150),f/2-f/20))
    for slip in (0.005,0.02):
        e=slip*(T20-T2); print('slip %.1f%% of travel = %.0f mm: lens error %s mm'%(100*slip,e,{m:round(e/(m*m-1),2) for m in (2,5,10,20)}))
    # shade: screen illuminance ~ 1/v^2 (slide evenly bright) or ~1/m^2 (all light through the lens)
    for m in (20,10,5,2):
        print('m=%-3g illuminance rel. to m=20: %.0fx (1/v^2 law), %.0fx (1/m^2 law); open fraction of lens for constant brightness %.3f / %.3f'%(m,(21/(m+1))**2,(20/m)**2,((m+1)/21)**2,(m/20)**2))
