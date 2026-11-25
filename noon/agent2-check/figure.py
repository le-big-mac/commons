import numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
d=np.array([[float(x) for x in l.split()[:11]] for l in open('slow_dt8_seed1.txt') if not l.startswith('#') and len(l.split())>=11]); t=d[:,0]
ink="#22211f"; mute="#77756d"; bg="#fbfaf7"; col=["#2a78d6","#eb6834","#1baf7a","#eda100"]; names=['Mercury','Venus','Earth–Moon','Mars']
fig,ax=plt.subplots(figsize=(10.5,5.6),facecolor=bg); ax.set_facecolor(bg)
def smooth(y,w=5): return np.convolve(y,np.ones(w)/w,mode='same')
for k,nm in enumerate(['Jupiter','Saturn','Uranus','Neptune']):
    ax.plot(t[2:-2],smooth(d[:,7+k])[2:-2]-smooth(d[:,7+k])[2],color="#c9c6bd",lw=1,zorder=1)
ax.text(101,5.2,'outer planets',color=mute,fontsize=9,va='center')
finals={}
for k,nm in enumerate(names):
    y=smooth(d[:,3+k])-smooth(d[:,3+k])[2]; ax.plot(t[2:-2],y[2:-2],color=col[k],lw=2,zorder=3 if k!=1 else 4,ls='-' if k!=1 else (0,(1,1.2))); finals[nm]=y[-3]
ax.text(101,max(finals['Mercury'],finals['Mars'])+.25,'Mars',color=ink,fontsize=9.5,va='center'); ax.plot([98.6,100.6],[finals['Mars']]*2,color=col[3],lw=0)
ax.text(101,max(finals['Mercury'],finals['Mars'])-.25,'Mercury',color=ink,fontsize=9.5,va='center')
ax.text(101,finals['Venus'],'Venus (dotted),\nEarth–Moon',color=ink,fontsize=9.5,va='center')
for nm,c,dy in (('Mars',col[3],.25),('Mercury',col[0],-.25)):
    ax.plot([100.2,100.8],[finals[nm],max(finals['Mercury'],finals['Mars'])+dy],color=c,lw=1.2)
# reference slope: e-folding 4.2 Myr
tt=np.array([40,100]); ax.plot(tt,0.6+(tt-40)/(4.2*np.log(10)),color=ink,lw=1,ls=(0,(4,3)),zorder=2)
ax.text(74,3.55,'slope for an e-folding time of 4.2 Myr',color=ink,fontsize=9,rotation=28.5,ha='center',va='center')
ax.axvspan(30,40,color="#e9e4d8",zorder=0); ax.axvspan(50,60,color="#e9e4d8",zorder=0)
ax.text(35,-0.75,'burst',ha='center',color=mute,fontsize=9); ax.text(55,-0.75,'burst',ha='center',color=mute,fontsize=9)
ax.set_xlim(0,116); ax.set_ylim(-1,10.8); ax.set_xlabel('time (million years)',color=ink)
ax.set_ylabel('growth of the perturbation in each planet\'s eccentricity vector\n(powers of ten, relative to its size at 0.3 Myr)',color=ink,fontsize=9.5)
ax.grid(axis='y',color='#e6e3dc',lw=.8); ax.tick_params(colors=mute); ax.set_xticks(range(0,101,10))
for s in ax.spines.values(): s.set_visible(False)
fig.suptitle('Thirty quiet million years, then the inner planets diverge together, in bursts',x=.07,ha='left',fontsize=13,color=ink)
fig.text(.07,.905,'Sun and eight planets, no relativity; one trajectory with its variational equations (REBOUND WHFast, 8-day step); agent2, 19 Nov 2026',fontsize=8.5,color=mute)
plt.subplots_adjust(left=.1,right=.97,top=.87,bottom=.11)
fig.savefig('lyapunov-agent2.png',dpi=120,facecolor=bg)
