import json, numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from couzin import School
res=json.load(open('sweep.json')); ds=sorted({r[0] for r in res})
ink="#22211f"; mute="#77756d"; bg="#fbfaf7"; C={'swarm':"#eda100",'mill':"#2a78d6",'aligned':"#1baf7a"}
def cls(p,m): return 'aligned' if p>.65 and p>m else ('mill' if m>.5 else 'swarm')
fig=plt.figure(figsize=(12,8.4),facecolor=bg); gs=fig.add_gridspec(2,3,height_ratios=[1,1.15],hspace=.3,wspace=.08,left=.07,right=.97,top=.9,bottom=.05)
ax=fig.add_subplot(gs[0,:]); ax.set_facecolor(bg)
for r in res: ax.scatter(r[0]+np.random.uniform(-.1,.1),r[2],s=30,color=C[cls(r[2],r[3])],edgecolor=bg,lw=1,zorder=3)
ax.set_xlabel('width of the orientation zone (body lengths)',color=ink); ax.set_ylabel('alignment of the largest group',color=ink)
ax.set_ylim(0,1.02); ax.grid(axis='y',color='#e6e3dc',lw=.8); ax.tick_params(colors=mute)
for s in ax.spines.values(): s.set_visible(False)
for i,(k,lab) in enumerate([('swarm','disordered / mixed'),('mill','mill (rotating)'),('aligned','aligned school')]):
    ax.scatter([],[],color=C[k],s=40,label=lab)
ax.legend(frameon=False,ncol=3,loc='upper left',bbox_to_anchor=(0,1.13),labelcolor=ink)
print({d:[cls(r[2],r[3]) for r in res if r[0]==d] for d in ds})
for j,(dro,seed,name) in enumerate([(0,0,'swarm'),(2.5,1,'mill'),(7.0,0,'aligned')]):
    ok=False
    for sd in range(seed,seed+30):
        s=School(ro=1+dro,seed=sd)
        for t in range(6000): s.step()
        p,m,n,k=s.order_largest()
        if cls(p,m)==name and n>55: ok=True; break
    a=fig.add_subplot(gs[1,j]); a.set_facecolor(bg); i=s.lab==np.bincount(s.lab).argmax(); x=s.x[i]-s.x[i].mean(0); v=s.v[i]
    a.quiver(x[:,0],x[:,1],v[:,0],v[:,1],color=C[name],scale=28,width=.006,headwidth=3.5,headlength=5,pivot='mid')
    L=max(np.abs(x).max()*1.1,6); a.set_xlim(-L,L); a.set_ylim(-L,L); a.set_aspect('equal'); a.set_xticks([]); a.set_yticks([])
    for sp in a.spines.values(): sp.set_color('#e6e3dc')
    a.set_title(f'{["disordered swarm","mill","aligned school"][j]}: zone width {dro:g}\nalignment {p:.2f}, rotation {m:.2f}, {n} of 100 fish'+('' if ok else ' (not typical)'),fontsize=10,color=ink)
fig.suptitle('Above a zone width of about 1.5 every run ends as either a mill or an aligned school, never in between',fontsize=13,color=ink,x=.07,ha='left')
fig.savefig('states.png',dpi=110,facecolor=bg)
