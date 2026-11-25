"""A map of the proof of Theorem C: how each of the 256 zero patterns of Z_{p^2 q^2} is settled (p < q < p^2),
from certificates_p2q2.json.  Colours: three validated categorical hues (all-pairs) + neutrals; R cells carry a letter."""
import json, itertools
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch
SURF='#fcfcfb'; INK='#0b0b0b'; SEC='#52514e'; MUTED='#898781'; GRID='#e1e0d9'; BASE='#c3c2b7'
BLUE='#2a78d6'; ORANGE='#eb6834'; AQUA='#1baf7a'
E=json.load(open('certificates_p2q2.json'))
cat={}
for e in E: cat[(e['regime'],tuple(e['Ep']),tuple(e['Eq']),frozenset(tuple(x) for x in e['F']))]=e['cat']
def category(reg,Ep,Eq,F):
    if 1 not in Ep and 1 not in Eq: return 'L2'
    return cat[(reg,Ep,Eq,frozenset(F))]
SUB1=[(),(1,),(2,),(1,2)]
ROWF=[[],[(1,1)],[(1,2)],[(1,1),(1,2)]]; COLF=[[],[(2,1)],[(2,2)],[(2,1),(2,2)]]
fill={'L2':BASE,'a':BLUE,'b':ORANGE,'RP':AQUA,'RQ':AQUA,'H':SEC,'N':SEC}
letter={'RP':'p','RQ':'q','H':'Y','N':'N'}
fig=plt.figure(figsize=(13.2,9.6),dpi=130,facecolor=SURF)
ax=fig.add_axes([0.035,0.03,0.63,0.80]); ax.set_facecolor(SURF)
cell=1.0; gap=0.09; block=4*cell+3*gap; bgap=0.9
counts={}; changed=[]
for i,Ep in enumerate(SUB1):
    for j,Eq in enumerate(SUB1):
        x0=j*(block+bgap); y0=(3-i)*(block+bgap)
        for r in range(4):
            for c in range(4):
                F=ROWF[r]+COLF[c]
                k=category('A',Ep,Eq,F); kb=category('B',Ep,Eq,F)
                counts[k]=counts.get(k,0)+1
                x=x0+c*(cell+gap); y=y0+(3-r)*(cell+gap)
                ax.add_patch(Rectangle((x,y),cell,cell,facecolor=fill[k],edgecolor='none'))
                if k in letter:
                    ax.text(x+cell/2,y+cell/2-0.02,letter[k],ha='center',va='center',fontsize=10.5,
                            color=(SURF if k in ('H','N') else INK),fontweight='bold' if k in ('H','N') else 'normal')
                if k!=kb:
                    changed.append((Ep,Eq,F,k,kb))
                    ax.add_patch(Rectangle((x-0.035,y-0.035),cell+0.07,cell+0.07,fill=False,edgecolor=INK,linewidth=1.6))
names=['none','p','p²','p, p²']; namesq=['none','q','q²','q, q²']
for j in range(4):
    ax.text(j*(block+bgap)+block/2,4*(block+bgap)-bgap+0.35,namesq[j],ha='center',va='bottom',fontsize=12,color=INK)
for i in range(4):
    ax.text(-0.45,(3-i)*(block+bgap)+block/2,names[i],ha='right',va='center',fontsize=12,color=INK)
ax.text(2*(block+bgap)-bgap/2,4*(block+bgap)-bgap+1.25,'prime-power zeros in q',ha='center',va='bottom',fontsize=11,color=SEC)
ax.text(-2.15,2*(block+bgap)-bgap/2,'prime-power zeros in p',ha='center',va='center',rotation=90,fontsize=11,color=SEC)
ax.set_xlim(-2.6,4*(block+bgap)-bgap+0.2); ax.set_ylim(-0.2,4*(block+bgap)-bgap+2.0); ax.set_aspect('equal'); ax.axis('off')
# title
fig.text(0.035,0.955,'A map of the proof: every possible set of cyclotomic divisors of a subset of Z$_{p^2q^2}$',fontsize=16.5,color=INK,fontweight='bold',va='top')
fig.text(0.035,0.915,'Each small square is one of the 256 zero patterns; its colour says how the pattern is settled when p < q < p².  '
                     'The two outlined squares are settled differently when q > p².',fontsize=10.5,color=SEC,va='top')
# key for the inner layout
kx=fig.add_axes([0.70,0.60,0.27,0.27]); kx.set_facecolor(SURF)
for r in range(4):
    for c in range(4):
        kx.add_patch(Rectangle((c*1.09,(3-r)*1.09),1,1,facecolor=GRID,edgecolor='none'))
rl=['none','pq','pq²','pq, pq²']; cl=['none','p²q','p²q²','both']
for r in range(4): kx.text(-0.2,(3-r)*1.09+0.5,rl[r],ha='right',va='center',fontsize=9.5,color=INK)
for c in range(4): kx.text(c*1.09+0.5,4*1.09+0.05,cl[c],ha='center',va='bottom',fontsize=9.5,color=INK)
kx.text(2.13,5.35,'Inside each block: the mixed zeros',ha='center',va='bottom',fontsize=10.5,color=INK,fontweight='bold')
kx.text(-2.45,2.13,'with p¹',ha='center',va='center',rotation=90,fontsize=9.5,color=SEC)
kx.text(2.13,-0.25,'with p²',ha='center',va='top',fontsize=9.5,color=SEC)
kx.set_xlim(-3.0,4.6); kx.set_ylim(-0.9,6.1); kx.set_aspect('equal'); kx.axis('off')
# legend with counts
lx=fig.add_axes([0.70,0.09,0.29,0.48]); lx.set_facecolor(SURF); lx.axis('off'); lx.set_xlim(0,10); lx.set_ylim(0,10)
rp=counts.get('RP',0); rq=counts.get('RQ',0)
items=[(BASE,None,'%d'%counts['L2'],'Neither p nor q is a zero','the set lies in a coset of a subgroup;\nthe pⁿq theorem applies'),
       (BLUE,None,'%d'%counts['a'],'(T2) holds, no orphan zero','so |A| = k, and Coven–Meyerowitz\ngives a tiling'),
       (ORANGE,None,'%d'%counts['b'],'The programme forces |A| < k','but k divides |A|: no weak tile\nhas this pattern'),
       (AQUA,'p q','%d + %d'%(rp,rq),'A best complement lives in pZ or qZ','so the pieces of A share a tiling\ncomplement (the letter says which subgroup)'),
       (SEC,'Y','%d'%counts['H'],'|A| = pq, then a counting lemma','p and p²q² zeros force pq² (Lemma Y′)'),
       (SEC,'N','%d'%counts.get('N',0),'|A| would not be an integer','(only when q < p²)')]
y=9.55
lx.text(0,10.0,'How a pattern is settled',fontsize=10.5,color=INK,fontweight='bold',va='bottom')
for col,let,num,head,sub in items:
    lx.add_patch(Rectangle((0,y-0.62),0.62,0.62,facecolor=col,edgecolor='none'))
    if let: lx.text(0.31,y-0.33,let,ha='center',va='center',fontsize=8.5 if len(let)>1 else 9.5,color=(SURF if col==SEC else INK),fontweight='bold' if col==SEC else 'normal')
    lx.text(1.0,y-0.04,head,fontsize=10,color=INK,va='top')
    lx.text(9.9,y-0.04,num,fontsize=10,color=INK,va='top',ha='right')
    lx.text(1.0,y-0.50,sub,fontsize=8.8,color=SEC,va='top',linespacing=1.25)
    y-=1.62 if '\n' in sub else 1.28
fig.text(0.70,0.028,'k = p^(number of zeros among p, p²) · q^(number among q, q²).\n'
         'Source: certificates_p2q2.json. The whole case distinction is\nchecked by Lean (P2q2/DispatchA.lean, DispatchB.lean).',fontsize=8.3,color=MUTED,va='bottom',linespacing=1.3)
fig.savefig('proof-map.png',facecolor=SURF)
print(counts); print('changed in regime B:',changed)
