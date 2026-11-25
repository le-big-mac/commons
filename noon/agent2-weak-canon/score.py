"""Score of the weak canon as a heatmap: one row per possible entry (rotation of the rhythm), one column per pulse;
ink = the weight of that entry at that pulse. One sequential hue (more weight = darker); the six players are named in
text beside their rows, not by colour."""
import json, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
d=json.load(open('weakcanon.json')); N=d['N']; A=d['A']
ev=d['events']; NP=max(P for P,t,w in ev)+1; CYC=NP//N
Wt=np.load('weights.npy')                      # Wt[P, t]: the weight of entry t in force at pulse P (exact)
assert Wt.shape==(NP,N)
support=[t for t in range(N) if Wt[:,t].max()>0]
grid=Wt[:,support].T
names={0:'thumb piano',4:'marimba',5:'electric piano',3:'plucked string',1:'glass',2:'bell'}
order=[0,4,5,3,1,2]                                   # low to high register, as in the sextet
SURF='#fcfcfb'; T1='#0b0b0b'; T2='#52514e'; GRID='#e4e3df'
ramp=['#cde2fb','#b7d3f6','#9ec5f4','#86b6ef','#6da7ec','#5598e7','#3987e5','#2a78d6','#256abf','#1c5cab','#184f95','#104281','#0d366b']
cmap=LinearSegmentedColormap.from_list('seqblue',ramp); cmap.set_under(SURF)
fig=plt.figure(figsize=(13,6.6),dpi=150,facecolor=SURF)
ax=fig.add_axes([0.16,0.13,0.80,0.66]); ax.set_facecolor(SURF)
y=0; yticks=[]; ylabels=[]; groups=[]
for pl in order:
    rows=[r for r,t in enumerate(support) if (t%12)//2==pl]
    y0=y
    for r in rows:
        ax.imshow(grid[r:r+1],aspect='auto',cmap=cmap,vmin=0.02,vmax=1,extent=(0,NP,y+0.86,y+0.0),interpolation='nearest')
        yticks.append(y+0.43); ylabels.append(str(support[r])); y+=1
    groups.append((names[pl],y0,y)); y+=0.7
ax.set_ylim(y-0.7+0.1,-0.25); ax.set_xlim(0,NP)
ax.set_yticks(yticks); ax.set_yticklabels(ylabels,fontsize=7,color=T2)
ax.tick_params(axis='y',length=0,pad=3); ax.tick_params(axis='x',length=0)
for c in range(1,CYC): ax.axvline(c*N,color=GRID,lw=0.8,zorder=-1)
ax.set_xticks([c*N+N/2 for c in range(CYC)]); ax.set_xticklabels([str(c+1) for c in range(CYC)],fontsize=8,color=T2)
ax.set_xlabel('cycle of 72 pulses (9.4 seconds each)',fontsize=9,color=T2,labelpad=6)
for s in ax.spines.values(): s.set_visible(False)
for name,y0,y1 in groups:
    fig.text(0.012,ax.get_position().y1-(ax.get_position().height)*((y0+y1)/2-0.43+0.25)/(y-0.7+0.1+0.25),name,fontsize=9.5,color=T1,va='center')
fig.text(0.118,ax.get_position().y1+0.012,'entry',fontsize=7.5,color=T2,ha='left')
# sections, in text above the plot
secs=[(0,2,'the canon of the sextet'),(2,3,'→'),(3,4,'a second canon'),(4,5,'→'),(5,6,'a third'),(6,8,'dissolving'),
      (8,10,'all six canons at once'),(10,12,'returning'),(12,13,'the first again')]
for a,b,txt in secs:
    xm=ax.get_position().x0+ax.get_position().width*((a+b)/2)/CYC
    fig.text(xm,ax.get_position().y1+0.035,txt,fontsize=8.5,color=T1,ha='center',va='bottom')
    if txt!='→':
        x0=ax.get_position().x0+ax.get_position().width*a/CYC+0.004; x1=ax.get_position().x0+ax.get_position().width*b/CYC-0.004
        fig.add_artist(plt.Line2D([x0,x1],[ax.get_position().y1+0.028]*2,color=GRID,lw=1))
fig.text(0.012,0.955,'Weak canon: how much of each entry is sounding',fontsize=14,color=T1,weight='bold',va='top')
fig.text(0.012,0.912,'One rhythm of twelve notes, 21 places it may enter. Darker = more weight. In every column the weights of the entries sounding on that pulse add to exactly one.',fontsize=9,color=T2,va='top')
# legend for the single hue
lax=fig.add_axes([0.80,0.045,0.14,0.018]); lax.imshow(np.linspace(0.02,1,200)[None,:],aspect='auto',cmap=cmap,vmin=0.02,vmax=1)
lax.set_xticks([0,199]); lax.set_xticklabels(['weight 0','1'],fontsize=7.5,color=T2); lax.set_yticks([]); lax.tick_params(length=0)
for s in lax.spines.values(): s.set_visible(False)
fig.savefig('weakcanon-score.png',facecolor=SURF)
print('rows',len(support),'pulses',NP,'max weight',grid.max(),'column sums need not be 1 here (rows are entries, not pulses)')
