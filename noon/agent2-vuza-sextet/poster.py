import json, numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
N=72; r=json.load(open('vuza72.json'))
canon=lambda s:min(tuple(sorted((x-t)%N for x in s)) for t in s)
Bs=sorted({tuple(a) for a,b in r}); As=sorted({canon(b) for a,b in r})   # 3 six-sets (entries), 6 twelve-sets (rhythms)
col=["#2a78d6","#eb6834","#1baf7a","#eda100","#e87ba4","#008300"]; ink="#22211f"; mute="#77756d"; bg="#fbfaf7"
fig,axs=plt.subplots(3,6,figsize=(18,10.2),facecolor=bg)
th=lambda p:np.pi/2-2*np.pi*p/N
for i,B in enumerate(Bs):
    for j,A in enumerate(As):
        ax=axs[i,j]; ax.set_aspect('equal'); ax.axis('off'); ax.set_xlim(-1.25,1.25); ax.set_ylim(-1.25,1.25)
        owner={}
        for v,b in enumerate(B):
            for a in A: owner[(a+b)%N]=v
        assert len(owner)==N
        for v,b in enumerate(B):      # each voice: polygon through its 12 onsets, on its own ring
            ps=sorted((a+b)%N for a in A); rad=0.38+0.1*v
            ax.plot([rad*np.cos(th(p)) for p in ps+ps[:1]],[rad*np.sin(th(p)) for p in ps+ps[:1]],color=col[v],lw=.8,alpha=.55)
            ax.scatter([rad*np.cos(th(p)) for p in ps],[rad*np.sin(th(p)) for p in ps],s=9,color=col[v],zorder=3)
        for p in range(N):            # outer ring: the complete tiling
            ax.plot([1.02*np.cos(th(p)),1.14*np.cos(th(p))],[1.02*np.sin(th(p)),1.14*np.sin(th(p))],color=col[owner[p]],lw=2.6,solid_capstyle='butt')
        if i==0: ax.set_title('rhythm '+'abcdef'[j],fontsize=11,color=ink,pad=2)
        if j==0: ax.text(-1.45,0,'entries '+'ABC'[i],rotation=90,va='center',ha='center',fontsize=11,color=ink)
fig.suptitle('The eighteen Vuza canons of the 72-pulse cycle',fontsize=19,color=ink,y=.985)
fig.text(.5,.94,'Six voices play one 12-note rhythm at six different entries. Outer ring: every pulse belongs to exactly one voice. '
 'Inner rings: each voice alone (voice 1 innermost, in entry order).',ha='center',fontsize=10.5,color=mute)
for v in range(6):
    fig.text(.33+.06*v,.035,'●',color=col[v],fontsize=13,ha='right',va='center'); fig.text(.333+.06*v,.035,f'voice {v+1}',color=ink,fontsize=10,va='center')
fig.text(.5,.008,'entries  A = %s   B = %s   C = %s        the sextet uses entries A with rhythm %s'%(*[str(list(b)) for b in Bs],'abcdef'[As.index(canon([0,1,5,6,12,25,29,36,42,48,49,53]))]),ha='center',fontsize=9,color=mute)
plt.subplots_adjust(left=.035,right=.99,top=.9,bottom=.07,wspace=.02,hspace=.04)
fig.savefig('poster.png',dpi=110,facecolor=bg)
