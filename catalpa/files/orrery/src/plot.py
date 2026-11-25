import numpy as np
d=np.loadtxt('neptune_resid.txt'); d=d[np.argsort(d[:,0])]; d=d[(d[:,0]>=1781)&(d[:,0]<=1846.5)]
W,H,L,R,T,B=760,380,64,24,56,44
x=lambda y:L+(y-1780)/(1847-1780)*(W-L-R); yv=lambda v:H-B-(v+10)/(180)*(H-T-B)
pts=' '.join(f'{x(a):.1f},{yv(b):.1f}' for a,b,_ in d)
s=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="system-ui,sans-serif" font-size="12">',
 f'<rect width="{W}" height="{H}" fill="#fcfcfb"/>',
 f'<text x="{L}" y="22" font-size="15" font-weight="600" fill="#0b0b0b">Uranus drifts off a Neptune-less orbit after 1821</text>',
 f'<text x="{L}" y="40" fill="#52514e">Heliocentric longitude residual (arcseconds), model fitted to 1781–1821 without Neptune</text>']
for v in range(0,180,40):
    s.append(f'<line x1="{L}" x2="{W-R}" y1="{yv(v):.1f}" y2="{yv(v):.1f}" stroke="{"#52514e" if v==0 else "#e6e5e0"}" stroke-width="1"/><text x="{L-8}" y="{yv(v)+4:.1f}" text-anchor="end" fill="#52514e">{v}″</text>')
for y in range(1780,1850,10): s.append(f'<text x="{x(y):.1f}" y="{H-B+18}" text-anchor="middle" fill="#52514e">{y}</text>')
s.append(f'<rect x="{x(1781):.1f}" y="{T}" width="{x(1821)-x(1781):.1f}" height="{H-T-B}" fill="#52514e" opacity="0.06"/><text x="{x(1801):.1f}" y="{T+16}" text-anchor="middle" fill="#52514e">fit window</text>')
s.append(f'<polyline points="{pts}" fill="none" stroke="#2a78d6" stroke-width="2" stroke-linejoin="round"/>')
for a,b,_ in d: s.append(f'<circle cx="{x(a):.1f}" cy="{yv(b):.1f}" r="7" fill="transparent"><title>{a:.0f}: {b:+.1f}″</title></circle>')
a,b,_=d[-1]; s.append(f'<circle cx="{x(a):.1f}" cy="{yv(b):.1f}" r="4" fill="#2a78d6" stroke="#fcfcfb" stroke-width="2"/><text x="{x(a)-10:.1f}" y="{yv(b)-4:.1f}" text-anchor="end" fill="#0b0b0b">1846: {b:.0f}″ — Neptune found</text>')
s.append('</svg>'); open('uranus_residual.svg','w').write('\n'.join(s))
